---
title: I2C Implementation Plan — Modular Synth
tags: [stm32, synth]
status: in-progress
created: 2026-09-23
subject: mcu
course: 01276314
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
// last_update_tick removed — stale_check dropped, I2C error handles absence
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
- `note_off` callback sets `voice.state = RELEASING` only — single aligned-word write, atomic on Cortex-M, no IRQ disable needed here
- `__disable_irq`/`__enable_irq` needed only in `voice_manager_update()` if freeing a voice resets multiple fields simultaneously
- Max slaves: **8** — addresses 0x10–0x17

## Note-off model (updated 2026-09-30)

`note_off` is a **request**, not an immediate voice free. Voice stays alive through ADSR release tail.

- `note_off_cb(vm, key_id)` → marks voice `RELEASING`
- `voice_manager_update(vm)` runs in main loop each tick, scans for voices where `state == RELEASING && adsr_is_idle()` → frees them
- `adsr_is_idle()`: amplitude < epsilon OR envelope stage == IDLE (Putt's ADSR module must expose this)
- IRQ disable only if freeing resets multiple fields:

```c
void voice_manager_update(VoiceManager *vm) {
    for each voice:
        if (voice.state == RELEASING && adsr_is_idle(&voice.adsr)) {
            __disable_irq();
            voice.state = FREE;   // + any other field resets
            __enable_irq();
        }
}
```

If freeing is just `voice.state = FREE`, no critical section needed (single aligned write = atomic).

**Pending:** coordinate `adsr_is_idle()` API with Putt before implementing `voice_manager_update()`.

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

## Slave absence handling (updated 2026-09-30)

`scan_slaves()` removed — no boot discovery needed.
`stale_check()` + `last_update_tick[8]` removed — keys held seconds; frozen row is acceptable.

`poll_slaves()` always tries all 8 (0x10–0x17). On `HAL_I2C_Master_Receive` error:
- Zero `keys[s][]`
- Call `note_off` for any `KEY_PRESSED` on that slave
- I2C timeout = slave absence signal; no separate tracking needed.

## Implementation order

1. ~~IOC: I2C1 Fast 400kHz + TIM 10ms interrupt → code gen~~ ✅ 2026-09-25
2. ~~Boot-cal~~ ✅ 2026-09-25
3. ~~Slave TIM ISR → `KeyFrame` fill~~ ✅ 2026-09-25
4. ~~Master TIM ISR → poll + update array~~ ✅ 2026-09-25
5. ~~`process_keys()` state machine~~ ✅ 2026-09-25
6. ~~Stale detection~~ ✅ 2026-09-25
7. ~~Wire `note_on` / `note_off` to synth engine~~ ✅ 2026-09-25

**Phase 2 — VoiceManager integration:**
8. ~~New branch `feat/i2c-integrate` off `origin/waveform-gen`; cherry-pick `82da076`~~ ✅ 2026-09-29
9. ~~API update: MAX_SLAVES→8, process_keys new sig, time-based velocity, drop g_active_freq~~ ✅ 2026-09-29
10. ~~Pin abstraction: `#define` block for all GPIO/ADC pins (V1/V2 swappable)~~ ✅ 2026-09-29
11. ~~IOC fix: add PA0 GPIO_Out, PA7 TIM3_CH2~~ ✅ 2026-09-29
12. ~~main.c: wire VoiceManager into audio ISR + callbacks into process_keys~~ ✅ 2026-09-29

**Pending Mind:**
13. Swap `stub_note_on` → real `voice_manager_note_on` wrapper (sig: `uint8_t fn(VoiceManager*, uint16_t key_id, uint8_t vel)`) in `process_keys()` call in `main.c`

**Pending Putt:**
14. Add ADSR fields to `WaveformConfig` in `waveform.h` → Nuker wires `controls.c` ch 2–11

## Implementation notes

**Branches:**
- `feat/i2c-comms` — original I2C layer (pushed to origin)
- `feat/i2c-integrate` — **active branch**, cherry-picked onto `origin/waveform-gen`, pushed 2026-09-29. All Phase 2 complete.

**Files created/updated (feat/i2c-integrate):**
- `STM32/Core/Inc/synth_comms.h` + `Src/synth_comms.c` — master/slave logic, IS_MASTER guard, VoiceManager callbacks, time-based velocity
- `STM32/Core/Inc/mux_adc.h` + `Src/mux_adc.c` — `mux_adc_init()` + `mux_read()`, channel configured once at startup
- `STM32/Core/Inc/controls.h` + `Src/controls.c` — pots via mux (ch 0–1 wired, ch 2–11 stubbed), debounced buttons PB0/PB1
- `STM32/Core/Inc/audio_out.h` + `Src/audio_out.c` — TIM3 CCR1/CCR2 DAC, 48kHz TIM4 ISR using `voice_manager_get_sample`
- `STM32/Core/Src/i2c.c` / `adc.c` / `i2c.h` / `adc.h` — CubeMX-generated
- `STM32/STM32.ioc` — merged: PA0–PA3 mux GPIO, PA4 ADC_IN4, PA6/PA7 TIM3, PB0/PB1 input, PB6/PB7 I2C1 Fast Mode

**Ponytail review fixes (2026-09-29):**
- `init_slave()`: added `HAL_I2C_DeInit` before re-init (safe OwnAddress1 override post-CubeMX)
- `HAL_I2C_ErrorCallback`: clears AF/BERR/ARLO/OVR flags before re-enabling listen (prevents error loop)
- `mux_adc_init()`: ADC channel configured once at startup, not on every `mux_read` call

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
