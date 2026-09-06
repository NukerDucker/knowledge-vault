---
title: 74HC4067 — 16-Channel Analog MUX
tags: [mcu, stm32, hardware, component, adc, mux]
status: active
updated: 2026-09-06
subject: mcu
---

# 74HC4067 — 16-Channel Analog MUX

**Manufacturer:** NXP Semiconductors (74HC4067; 74HCT4067 Rev. 6, 2015)  
**On hand:** two breakout board references

**Files:**

| Folder | Contents | Source |
|---|---|---|
| `~/Downloads/HC4067-MUX-Breakout-Board-master/` | `74HC_HCT4067_Datasheet.pdf`, `HC4067_breakout_board.lbr` (Eagle lib), board image | Third-party clone |
| `~/Downloads/Analog_Digital_MUX_Breakout-master/` | `Analog-Digital-Mux-Breakout.brd`, `.sch` (Eagle schematic + layout) | **SparkFun BOB-09056** (official) |

SparkFun product: [BOB-09056](https://www.sparkfun.com/products/9056) — CC BY-SA 3.0.  
Use the SparkFun `.sch` as the reference schematic for wiring; use the `.lbr` for the Eagle symbol if importing into KiCad.

---

## What It Is

SP16T analog switch — single-pole 16-throw. Operates as:
- **16:1 MUX** (16 inputs → 1 common output), or
- **1:16 DEMUX** (1 common → 16 outputs)

Handles both analog and digital signals.

---

## Key Specs

| Parameter | Value |
|---|---|
| Channels | 16 (Y0–Y15) |
| Supply voltage | 2.0 V – 6.0 V (3.3 V ✅) |
| ON resistance | ~80 Ω at VCC = 4.5 V |
| Select pins | S0, S1, S2, S3 (4 pins) |
| Enable pin | E — active **HIGH** disables (active LOW enables) |
| Common pin | Z (the single ADC input) |
| Logic levels | CMOS (74HC) or TTL (74HCT) |
| Break-before-make | Yes (built-in) |
| ESD protection | >2000 V HBM |

---

## Pin Interface

```
STM32 GPIO × 4  →  S0, S1, S2, S3   (channel select, binary encoded)
STM32 GPIO × 1  →  E                 (pull LOW to enable; tie LOW if always-on)
STM32 ADC pin   →  Z                 (common analog input to ADC)
                   Y0–Y15            (16 sensor/signal inputs)
```

Channel selected = `S3<<3 | S2<<2 | S1<<1 | S0`.

**Note:** E is active HIGH disable. To enable the mux, drive E LOW (or tie to GND if always active).

---

## Relevance to Synth Project

See [[mcu-stm32-handoff]] — **Open Item: mux budget is full.**

Current board: 74HC4051 (8-ch) — handles hall keys H1–H8 only. H9–H12 (4 keys) + 5 pots = **9 signals with no ADC GPIO**.

HC4067 replaces the HC4051 with 16 channels on the same interface footprint:

| | 74HC4051 | 74HC4067 |
|---|---|---|
| Channels | 8 | **16** |
| Select pins | S0, S1, S2 (3) | S0, S1, S2, S3 **(4)** |
| Enable | E (active HIGH disable) | E (active HIGH disable) |
| Common (ADC) | Z | Z |
| Total GPIO | 4 + 1 ADC | **5 + 1 ADC** |

**Budget with HC4067:**

| Channel | Signal |
|---|---|
| Y0–Y11 | Hall keys H1–H12 (all 12) |
| Y12–Y15 | 4 of 5 pots (vol, attack, decay, filter) |

Covers 12 keys + 4 pots = 16 ch exactly. Fifth pot (effect wet) needs either a free ADC GPIO or a second mux channel — check if PA4 or PA5 are free on F411.

**Cost:** +1 GPIO vs HC4051 (need S3). Check [[mcu-stm32-handoff]] pin table for a free GPIO (PB13/14/15 are used for mode buttons; PA15, PC14, PC15 are spare but not ADC-capable — S3 doesn't need ADC, any GPIO works).

---

## Wiring Note

Breakout board is a pass-through; no onboard logic other than the HC4067 IC itself. Wire directly:
- VCC → 3.3 V
- GND → GND
- E → GND (always-enable) or a GPIO if sleep/disable needed
- Z → one ADC pin (e.g. existing PC0 / ADC1_IN10)
- S0–S3 → 4 free GPIOs

---

*See also: [[mcu-stm32-project]] | [[mcu-stm32-handoff]] | [[mcu-lab05-adc]]*
