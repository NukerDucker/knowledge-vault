---
title: I2C Implementation Plan — Modular Synth
tags: [mcu, stm32, i2c, synth, piano]
status: in-progress
created: 2026-09-23
subject: mcu
---

# I2C Implementation Plan

## Architecture

- 1 master + up to **8** slaves (S=0→C0, S=7→C7)
- Each slave = one octave board (**12** keys, H3503 hall effect, **74HC4067 16-ch mux**)
- Pins: I2C1, PB6 (SCL) / PB7 (SDA), Fast Mode 400kHz, 2kΩ pull-ups
- Slave addresses: 0x10–**0x17** (8 boards)
- SMBA: **not used** (HAL support flaky, doesn't solve which-slave problem, V1 already routed)
- V2: master and slave share **identical pin layout** (PA0–PA3 mux select, PA4 ADC). Slave: ch 0–11 → H3503 hall effect. Master: ch 0–11 → **12 potentiometers**. `mux_read(ch)` is universal — `read_adc_channel()` in waveform-gen replaced by `mux_read` loop. `KeyFrame adc[12]` and one IOC serve both roles. No PA1 conflict.

## Timing

- Poll loop: master calls `poll_slaves()` + `process_keys()` + `stale_check()` every ~10ms via `HAL_GetTick()` in main loop (no dedicated TIM)
- Slave: fills `KeyFrame` on each master request (no independent timer; blocking ADC scan in `update_keyframe()`)
- Audio ISR on TIM4 (48kHz) runs concurrently — guard VoiceManager writes with `__disable_irq`/`__enable_irq`

## Data

```c
typedef struct {
    int16_t adc[12];  // raw ADC per key, 24 bytes total
} KeyFrame;

int16_t  keys[8][12];          // current depth (master) — 8 slaves max
int16_t  baseline[8][12];      // boot-cal rest values
int16_t  prev_keys[8][12];     // previous tick snapshot
KeyState key_state[8][12];     // IDLE or PRESSED
int16_t  key_velocity[8][12];  // locked on note-on
uint32_t last_update_tick[8];  // stale detection
```

S=0 → C0, S=7 → C7 (full 8-octave range). Flat key ID: `key_id = (s * 12) + k`.

## Interface (creambun coord + Putt velocity spec, updated 2026-09-29)

`process_keys` takes `VoiceManager*` + callbacks; `synth_comms.h` `#include`s `voice_manager.h`:

```c
void process_keys(VoiceManager *vm,
                  uint8_t (*note_on)(VoiceManager*, uint16_t key_id, uint8_t vel),
                  void    (*note_off)(VoiceManager*, uint16_t key_id));
```

- `key_id = (slave_index * 12) + key_index` — flat uint16_t
- Mind side: derive frequency from `key_id` inside note_on wrapper (no freq on wire)
- `note_on` returns 0 = voice pool full or duplicate key_id
- Callbacks wrapped in `__disable_irq`/`__enable_irq` — audio ISR reads VoiceManager concurrently
- Max slaves: **8** — addresses 0x10–0x17

## Velocity (updated 2026-09-29)

Two-threshold time-based method (time-accurate regardless of main loop cadence):

1. Key depth crosses `MOVE_THRESHOLD` (~PRESS_THRESHOLD/3) → record `press_start_tick[s][k] = HAL_GetTick()`
2. Key depth crosses `PRESS_THRESHOLD` → `delta_ms = HAL_GetTick() - press_start_tick[s][k]`; `vel = map_velocity(delta_ms)` (fast press = low ms = high vel)
3. Lock key — no further measurement while pressed
4. Key releases (depth drops below threshold) → note_off, unlock

Replaces single-tick ADC delta method (unreliable at variable loop rates).

```c
// threshold crossing → note-on
int16_t delta = depth - prev_depth;
key_velocity[s][k] = map_to_volume(delta);
note_on(s, k, key_velocity[s][k]);
key_state[s][k] = KEY_PRESSED;

// release → note-off
key_state[s][k] = KEY_IDLE;
note_off(s, k);
```

## Boot sequence

1. Init I2C1 + TIM (CubeIDE IOC)
2. 200ms cal loop → fill `baseline[][]` (keys at rest)
3. Scan 0x10–0x15 → count responding slaves
4. Enter 10ms poll loop

## Stale detection

If slave silent >30ms → zero its `keys[][]` row (release all notes).

## Implementation order

1. ~~IOC: I2C1 Fast 400kHz + TIM 10ms interrupt → code gen~~ ✅ 2026-09-25
2. ~~Boot-cal~~ ✅ 2026-09-25
3. ~~Slave TIM ISR → `KeyFrame` fill~~ ✅ 2026-09-25
4. ~~Master TIM ISR → poll + update array~~ ✅ 2026-09-25
5. ~~`process_keys()` state machine~~ ✅ 2026-09-25
6. ~~Stale detection~~ ✅ 2026-09-25
7. ~~Wire `note_on` / `note_off` to synth engine~~ ✅ 2026-09-25

**Phase 2 — VoiceManager integration (pending approval):**
8. New branch `feat/i2c-integrate` off `origin/waveform-gen`; cherry-pick `82da076`
9. API update: MAX_SLAVES→8, process_keys new sig, time-based velocity, drop g_active_freq
10. Pin abstraction: `#define` block for all GPIO/ADC pins (V1/V2 swappable)
11. IOC fix: add PA0 GPIO_Out, PA7 TIM3_CH2
12. main.c: wire VoiceManager into audio ISR + callbacks into process_keys

## Implementation notes

**Branch:** `feat/i2c-comms` — pushed to `origin/feat/i2c-comms` (push-blocked note in memory was stale)

**Files created:**
- `STM32/Core/Inc/synth_comms.h` + `Src/synth_comms.c` — master/slave logic, IS_MASTER guard
- `STM32/Core/Inc/mux_adc.h` + `Src/mux_adc.c` — HC4067 mux_read(), uses CubeMX hadc1
- `STM32/Core/Src/i2c.c` / `adc.c` / `i2c.h` / `adc.h` — CubeMX-generated

**Confirmed pins (from syth_mcu schematic):**
- I2C1: PB6 (SCL), PB7 (SDA) — AF4, Open-Drain
- Mux S0–S3: PA0–PA3 — GPIO output
- Mux Z (ADC): PA4 — ADC1_IN4
- CHAIN_IN: PC14, CHAIN_OUT: PC15 (V2, not yet wired in firmware)

**Architecture drift from ADRs:** mcu-i2c-plan.md (2026-09-23) overrides ADR 0001 — slave sends raw `KeyFrame` (24 bytes), master computes events. 10ms poll via HAL_GetTick().

**SLAVE_ID:** compile-time define 0–7 (bumped from 0–5). Chain auto-discovery (ADR 0002) deferred.

**Interface update (2026-09-29, creambun):** `process_keys` now takes `VoiceManager*` + two fn-ptr callbacks (`note_on`, `note_off`). `key_id = (s*12)+k`. Mind derives frequency from key_id internally.

## Team responsibility split

| Person | Scope |
|---|---|
| Nuker (NukerDucker) | I2C master comms, `process_keys`, VoiceManager glue, pot reads (`mux_adc.c` master side) | `feat/i2c-comms` |
| Mind (mindchuu) | VoiceManager, waveform engine, LFO, pitch bend | `origin/waveform-gen` |
| creambun (Pawikan) | Base project, stereo output, project coord | `origin/main`, `origin/stereo` |
| Bento (ttithipan) | Hall effect / touch sensor — slave firmware, mux scan | `origin/touch-sensor` |
| Putt | ADSR, noise wave type | — |

`mux_read()` shared between Nuker (pots on master) and Bento (keys on slave) — coordinate to avoid duplicate impl.
Note: `origin/touch-sensor` uses capacitive RC method (different from H3503 hall effect via mux ADC). Bento's hall effect work may be separate from that branch.

## Master board — pot/button mapping (V2)

Pots read via mux ch 0–11 (same `mux_read(ch)` as slave hall effect):

| Ch | Parameter | Status |
|---|---|---|
| 0 | wave slope up period | `rise_pct` in WaveformConfig |
| 1 | wave slope down period | `fall_pct` in WaveformConfig |
| 2 | ADSR — Attack | not in WaveformConfig yet |
| 3 | ADSR — Decay | not in WaveformConfig yet |
| 4 | ADSR — Sustain | not in WaveformConfig yet |
| 5 | ADSR — Release | not in WaveformConfig yet |
| 6 | pitch bend | not implemented yet |
| 7 | LFO | not implemented yet |
| 8 | effect param | reserved |
| 9 | effect strength | reserved |
| 10 | reserved | — |
| 11 | reserved | — |

Buttons (GPIO, 6 total): wave slope up type · wave slope down type · kick sound · hihat sound · effect type · reserved.
(`rise_shape`/`fall_shape` in WaveformConfig map to buttons 0–1. Others reserved.)
