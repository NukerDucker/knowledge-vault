---
title: Modular Synthesizer — Piano Project
tags: [mcu, stm32, hardware, synth, piano]
status: active
created: 2026-08-23
---

# Modular Synthesizer — Piano Project

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

*See also: [[session-state]] — session log, git state, dated progress*
