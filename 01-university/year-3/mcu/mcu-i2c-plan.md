---
title: I2C Implementation Plan — Modular Synth
tags: [mcu, stm32, i2c, synth, piano]
status: planning
created: 2026-09-23
subject: mcu
---

# I2C Implementation Plan

## Architecture

- 1 master + up to 6 slaves
- Each slave = one octave board (12 keys, H3503 hall effect, **74HC4067 16-ch mux**)
- Pins: I2C1, PB6 (SCL) / PB7 (SDA), Fast Mode 400kHz, 2kΩ pull-ups
- Slave addresses: 0x10–0x15 (assigned by position)
- SMBA: **not used** (HAL support flaky, doesn't solve which-slave problem, V1 already routed)

## Timing

- TIM interrupt every **10ms** on both master and slave
- Slave ISR: scan all 12 keys via ADC mux → fill `KeyFrame`
- Master ISR: poll each slave → `HAL_I2C_Master_Receive` → update `keys[][]`

## Data

```c
typedef struct {
    int16_t adc[12];  // raw ADC per key, 24 bytes total
} KeyFrame;

int16_t  keys[6][12];          // current depth (master)
int16_t  baseline[6][12];      // boot-cal rest values
int16_t  prev_keys[6][12];     // previous tick snapshot
KeyState key_state[6][12];     // IDLE or PRESSED
int16_t  key_velocity[6][12];  // locked on note-on
uint32_t last_update_tick[6];  // stale detection
```

## Velocity (Putt's spec, 2026-09-23)

Poll continuously. When key crosses `PRESS_THRESHOLD` (IDLE → PRESSED):
- Measure rate of change **once** (`depth - prev_depth` over 10ms tick)
- Lock key — no further velocity measurement while pressed
- Map delta → volume (0–127)

When key releases (crosses back above threshold): unlock, send note-off.

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

1. IOC: I2C1 Fast 400kHz + TIM 10ms interrupt → code gen
2. Boot-cal
3. Slave TIM ISR → `KeyFrame` fill
4. Master TIM ISR → poll + update array
5. `process_keys()` state machine
6. Stale detection
7. Wire `note_on` / `note_off` to synth engine
