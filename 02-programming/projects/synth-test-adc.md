---
title: Synth Test ADC — Hall Effect Sensor Mux
tags: [stm32, adc]
status: active
updated: 2026-09-23
---

# Synth Test ADC

STM32F401RC (Black Pill) reading 5 hall effect sensors through a 74HC4067 16-channel mux.
Working code at `~/Documents/University/Year-3/Microcon/synth_f401/`.
(F767ZI prototype code at `~/Documents/University/Year-3/Microcon/synth_test_adc/` — reference only.)

## Confirmed Working (2026-09-23)

- ST-Link V2 clone connects via SWD (direct USB-A to Mac, no hub)
- Black Pill powered separately via USB-C
- Chip detected as STM32F401RC (not F411 — same HAL, compatible)
- Resting ADC ~2500–2850, pressed ~1000–1100
- Auto-calibration on boot: 32-sample average per channel → threshold = baseline − 500
- LED PC13 lights on keypress

## Hardware — synth_f401 (F401RC, active)

| Pin | Function |
|---|---|
| PC14 | S0 (mux select bit 0) |
| PC15 | S1 (mux select bit 1) |
| PB10 | S2 (mux select bit 2) |
| PB12 | S3 (mux select bit 3) |
| PA5  | SIG → ADC1_IN5 |
| PC13 | LED (active-low) |

Mux channels C11–C15 connected to hall effect sensors.

## CubeMX Settings — synth_f401

- HCLK: 16 MHz (HSI, no PLL) — bare HSI confirmed stable
- ADC1 IN5 (PA5): 12-bit, right-aligned, single conversion, 84 cycles sampling
- ADC clock: PCLK2/2 = 8 MHz
- S0–S3 pins: GPIO Output Push-Pull
- USART1: 115200 8-N-1 (PA9 TX)

## Hardware — synth_test_adc (F767ZI, reference)

| Pin | Function |
|---|---|
| PF5 | S0 | PF3 | S1 | PC3 | S2 | PC0 | S3 |
| PA3 | SIG → ADC1_IN3 |

## CubeMX Settings — synth_test_adc (F767ZI)

- HCLK: 216 MHz (HSI, Over-Drive on)
- ADC1 IN3: 12-bit, 480 cycles, PCLK2/4 = 27 MHz
- USART3: 115200 8-N-1

## Firmware Notes — synth_f401 (active)

- Auto-calibration on boot: 32 samples per channel, average = `baseline[ch]`
- LED blinks fast during calibration (~1s) — keep keys released
- Trigger: `adc_val[ch] < baseline[ch] - 500`
- 1ms settle delay after mux_select before ADC read
- `adc_val[16]` array indexed by channel number (11–15 used)

## Firmware Notes — synth_test_adc (F767ZI reference)

- Read each channel with 8-sample average → divide by 8
- 5ms settle delay after MUX_SelectChannel before ADC read
- Output format: `C11:%lu C12:%lu C13:%lu C14:%lu C15:%lu\r\n`

## Visualisation

`plot_sensors.py` in project root — requires pyserial, matplotlib.
Run inside `.venv`:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pyserial matplotlib
python3 plot_sensors.py
```

Port hardcoded: `/dev/tty.usbmodem132103` — update if it changes.

## Known Issues

- Common-mode noise when multiple keys pressed (shared VCC rail) — hardware fix: 100nF decoupling cap on each sensor VCC
- C9/C10 were false-wired; only C11–C15 are physically connected
