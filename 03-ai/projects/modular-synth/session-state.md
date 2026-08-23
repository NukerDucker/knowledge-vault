---
title: Modular Synth — Session State
tags: [mcu, stm32, synth, session]
status: active
created: 2026-08-23
updated: 2026-08-23
---

*Reference note → [[mcu-stm32-project]]*

# Modular Synth — Session State

Course: MCU Interfacing (01276314, Wed)

---

## 2026-08-23 — Session 1 (Design)

**What happened:** Full architecture discussion. No code written. All decisions below finalized.

### Decisions locked

| Decision | Choice | Reason |
|----------|--------|--------|
| MCU | STM32F411 Black Pill | Prof requires HAL + CubeIDE; IOC already done |
| Cap touch | MPR121 via I2C | F411 has no TSC; MPR121 = 12ch, ~฿80, I2C native |
| Audio | PWM (TIM3 or TIM4, 2ch stereo) → MOSFET + RC LP filter → analog | No external DAC; teammate confirmed; see `stereo` branch for IOC + schematic |
| Inter-module bus | I2C | 2 wires, addressable, HAL native, no transceiver |
| Board ID | DIP switch → I2C address | Set on boot, master lookup table maps board→controls |
| Connector | 4-pin mag pogo: `5V\|GND\|SDA\|SCL` | Daisy-chain, hotswap-friendly |
| Key pads | Seaweed-shaped copper ENIG | Organic wavy fronds, 12 per key module |
| Board width | ~16cm per octave | 23–24mm per white key |
| Packet | `[board_id\|key_bitmask\|pot0\|pot1\|btn_state]` | Fixed-size, master knows exact size, no handshake |
| I2C polling | Master round-robins all addresses | Slaves preload TX buffer; master reads on demand |

### Rejected options

- **SPI** — N slaves = N CS lines, too many GPIO
- **UART** — shared bus → TX collision, no arbitration
- **CAN** — needs TJA1050 transceiver, overkill for <30cm desktop runs
- **STM32F7** — team IOC is on F4, no measurable benefit to migrate

### Key constraints

- F411 has no TSC (cap touch) → MPR121 required
- Audio: PWM via TIM3 or TIM4 (2 channels = stereo) → MOSFET → RC low-pass → analog out; no external DAC
- IOC config + schematic: `stereo` branch (check teammate's repo)
- MPR121 default I2C addr `0x5A`; ADDR pin float/3.3V/GND/SDA changes it → chain 4 max per bus
- Max simultaneous keypresses: **12 per MPR121**, all independent, no ghosting

### Polyphony math

- 12 keys per MPR121
- Multiple MPR121 on same I2C bus (different addrs) → more keys per module
- Each key module = one Black Pill, up to 4 MPR121s = 48 keys per board
- Master sees all key states per I2C poll cycle

---

## Open Tasks (next session)

- [ ] Lock Black Pill pinout: I2C1 (SDA=PB7, SCL=PB6), I2S2 (CK=PB13, SD=PB15, WS=PB12), DIP GPIOs
- [ ] CubeMX IOC: enable I2C1 + TIM3/TIM4 PWM channels (stereo) — pull from `stereo` branch IOC
- [ ] MPR121 wiring diagram (ADDR pin config for each module)
- [ ] Write MPR121 init + read loop: `HAL_I2C_Master_Receive` to addr `0x5A`
- [ ] Fixed packet struct in C: `typedef struct { uint8_t board_id; uint16_t key_bitmask; uint8_t pot0; uint8_t pot1; uint8_t btn_state; } SlavePacket;`
- [ ] PCB layout: key module first
- [ ] Power supply spec: separate 3.3V analog rail for audio

## Blockers

- **Deadline TBA** — no brief yet; update `assignments-tracker.md` when prof announces
- **Black key pad design** — confirm with team (offset narrow pads between white pads)
- **Number of modules** — determines DIP address bit width needed

---

## Files

| File | Location | Status |
|------|----------|--------|
| Reference note | `01-university/year-3/mcu/mcu-stm32-project.md` | ✅ Done |
| This session state | `03-ai/projects/modular-synth/session-state.md` | ✅ Done |
| Assignment tracker | `01-university/assignments-tracker.md` | 🔄 Update when deadline drops |
| Code | none yet | — |
