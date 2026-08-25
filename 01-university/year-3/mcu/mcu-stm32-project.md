---
title: Modular Synthesizer — Piano Project
tags: [mcu, stm32, hardware, synth, piano]
status: active
created: 2026-08-23
due: 2026-09-08
points: 100
subject: mcu
---

# Modular Synthesizer — Piano Project

**What:** modular synth/piano — per-octave PCB boards that snap together via 4-pin magnetic connectors.
**Why:** Microcontroller Interfacing coursework (01276314, Wed). **100 points**, group of 6–7.
**Where:** files → `~/Documents/University/Year-3/Microcon/`
**Stack:** STM32F4 Black Pill (F411) · HAL + CubeIDE · I2C bus · MPR121 cap touch.
**Constraint:** STM32 + HAL + CubeIDE mandatory. Must use **interrupts from 2 modules** (EXTI/UART/TIM) and **2 of 3** from {ADC, PWM, graphic LCD}, with **4–6 features**. F411 is fixed — F7 ruled out (team unfamiliar, IOC migration cost). F411 has no TSC peripheral, hence MPR121. **Late = −10 pts/day, per deadline.**

*Session log → [[mcu-stm32-log]]*

---

## Schedule

**Next up: proposal, 2026-09-08.** `due:` tracks the nearest open deadline, not
the final one — update it as each passes so `HOME.md` shows what is actually next.

| Deadline | Item | Weight |
|---|---|---|
| **Sept 8** | Proposal — [form](https://forms.gle/ZktBTfTz4MVToxwMA) | 10 pts |
| Sept 9 | Proposal comments in lab; development starts | — |
| Sept 23 | Progress report — [form](https://forms.gle/jjktDcC4a98Wker4A) | 10 pts |
| Oct 7 | Answer questions, in class or online | — |
| Oct 21 | Demonstrate the project | 60 pts |
| Oct 21 | Report + demo clip + code — [form](https://forms.gle/n2s17x8d1tJonu2b9) | 20 pts |
| Oct 21 | Return all lab equipment | — |

**Penalty: −10 points per day, applied after *each* deadline.** With the proposal
worth only 10, two days late on it is worth zero — the deadline matters more than
the content.

## Requirements check

> [!warning] Gap: only one of the three required modules is covered
> The rule is **2 of 3** from {ADC, PWM, graphic LCD}. The current design has
> **PWM only** (audio out). Pick a second before the proposal:
>
> - **ADC** — cheapest fit. A potentiometer for volume, filter cutoff, or pitch
>   bend is one knob, one pin, and it reads naturally as a synth control.
> - **Graphic LCD** — more visible in a demo (waveform, patch name, octave), but
>   more pins, more code, and more to go wrong on modular boards.
>
> ADC is the low-risk answer; the LCD is the one that scores better on "design and
> creativity" at demo time. Decide and record it under Decisions.

| Requirement | Status |
|---|---|
| Interrupts from 2 modules | ✅ EXTI (MPR121 IRQ) + TIM (PWM audio) |
| 2 of 3: ADC / PWM / graphic LCD | ⚠️ **PWM only — needs one more** |
| 4–6 features | ✅ likely (keys, audio, modularity, board ID, …) — enumerate for the proposal |
| STM32 + HAL + CubeIDE | ✅ |

## Proposal contents (10 pts, due Sept 8)

≤10 slides:

1. Motivation and main features
2. Brief explanation of how it works + top-level flowchart
3. Bill of materials
4. Relevant pictures
5. Links to the inspiration project (AKAI MPK mini)

## Report contents (part of the final 20 pts)

Introduction/motivation · design explanation (MCU↔device connectivity diagram,
complete flowchart) · important functions · BOM with prices and links · results
with pictures · problems and solutions · **knowledge used from other courses**
(digital circuits, electronics, programming) · references.

Demo clip: 3–6 min, uploaded to YouTube, for publication.

## Decisions

### 2026-08-26 — Audio out: PWM via Timer, not PCM5102/I2S

**PWM via Timer 3/4 → MOSFET + RC low-pass → analog out.** No external DAC chip.

Rejected PCM5102 over I2S. The F411 has no onboard DAC, which is what made an
external DAC look necessary — but PWM plus an RC filter gets adequate audio for
a prototype without adding a chip, a footprint, or I2S wiring to every board.
Fewer parts per module matters more here than fidelity, because the whole design
is modular boards that snap together.

Revisit only if PWM audio quality proves unacceptable in testing; PCM5102 stays
the fallback.

*(Recorded because the vault note and a Claude memory disagreed — the memory
claimed PCM5102/I2S. The memory was wrong and has been corrected.)*

Reference: AKAI MPK mini form factor. Modular PCB system, snap together via magnetic connectors.

---

## Hardware

**MCU:** STM32F4 Black Pill (F411)
- Prof requirement: HAL Library + CubeIDE
- IOC file already set up for F4 — no migration to F7
- F7 ruled out: team unfamiliar, IOC cost not worth it for prototype

**Audio out:** PWM via Timer 3 or 4 (2 channels → stereo) → MOSFET + RC low-pass → analog out. No external DAC chip needed.
- Check `stereo` branch for IOC config and schematic.

**Capacitive touch:** F411 has no TSC peripheral → use **MPR121** (12-channel cap touch IC, I2C, ~฿80/chip)
- All 12 electrodes scanned independently → 12-key simultaneous press, no ghosting
- Chain multiple MPR121s on same I2C bus (ADDR pin sets address) for more keys

---

## Module Architecture

| Module | Contents |
|--------|----------|
| **Key module** | Black Pill + PCB, 12 cap touch keys via MPR121, mag connectors L/R |
| **Control module** | Black Pill + PCB, drum pads + knobs + joystick |
| **Master module** | Black Pill + PCB, audio out (PWM → MOSFET + RC filter), screen, I2C master, USB to host |

Modules snap together magnetically. Master collects all data over I2C, outputs audio.

---

## PCB Design

**Board dimensions:** ~16cm wide per octave (white key = 23–24mm, 8 keys × ~20mm + spacing)
**Board height:** stretched tall to fit controls above keys (screen + knobs + buttons + keys stacked vertically)

**Per board:**
- Capacitive touch pads: seaweed-shaped copper traces (organic wavy fronds), gold ENIG finish
- 2+2 STM32 dev pin headers (development stage)
- 3.5mm audio output jack (on master)
- Rotary knobs (potentiometers)
- Tactile buttons
- 2.4-inch TFT LCD screen

**Black keys:** shorter narrower seaweed pads offset between white key pads

---

## Communication: I2C

Chosen over: SPI (too many CS lines), UART (collision on shared bus), CAN (needs transceiver, overkill for short desktop distances).

- 2 wires (SDA, SCL) + power = 4 pins per mag connector
- Each slave board address set via DIP switch on boot
- Master polls slaves by I2C address
- Short wires (<30cm desktop) → clock stretching risk low
- `HAL_I2C_*` functions, native F4 peripheral

**Connector per board:** `5V | GND | SDA | SCL` — 4-pin magnetic pogo, daisy-chain between modules

**Board ID:** DIP switch → hardcoded I2C address on boot. Master lookup table maps `board_id → {controls}` (e.g. pot0=reverb_wet, btn0=mute)

---

## Packet Design

Fixed-size packet per slave: `[board_id | key_bitmask | pot0_val | pot1_val | btn_state]`
Master knows exact size, no handshake needed.

---

## Power

Separate power supply for multi-board setup. Clean regulated 3.3V analog rail for audio (keep digital switching noise off it). Common ground shared.

---

## Protocols Considered & Rejected

| Protocol | Problem |
|----------|---------|
| SPI | N CS lines for N slaves — too many pins |
| UART | Point-to-point; shared bus = collision if 2 slaves send simultaneously |
| CAN | Good but needs TJA1050 transceiver chip, more complex, overkill for desktop |
| I2C | ✅ Chosen — 2 wires, addressable, HAL native, sufficient for short runs |
| PCM5102 I2S DAC | Tried, failed; also line-level out (1kΩ min load), needs amp to drive headphones |

---

## Next Steps

- [ ] Lock down Black Pill pinout for I2C + I2S + GPIOs
- [ ] MPR121 wiring diagram
- [ ] IOC config: enable I2C1/I2C2, I2S for PCM5102
- [ ] PCB layout: key module first
- [ ] Power supply spec

---

*See also: [[mcu-stm32-log]] — session log, git state, dated progress*
