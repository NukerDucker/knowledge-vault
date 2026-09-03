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

> [!note] Updated 2026-08-30 — see [[mcu-stm32-handoff]] for current architecture (architecture drift flagged there — master/slave zone plan unconfirmed against current single-board layout)
> Key sensing: **H3503 hall effect** (not Velostat/MPR121). Role: **compile-time #define** (not DIP switch). Mux: **74HC4051** (not CD4051) — full at 8/8 channels, no spare ADC GPIO for remaining 4 keys + 5 pots. KiCad schematic: `~/Documents/University/Year-3/Microcon/synth/syth_mcu/`, repo `github.com/NukerDucker/mcu-synth` (main + review/creambun). ERC: 0 pin_not_connected, 2 minor power-pin warnings open. Board now 286×133mm with DAC audio stage + 12-key hall row on one PCB.
>
> **Updated 2026-09-01 — see [[mcu-stm32-log]] Session 3 for full detail.** Session 3 proposed dropping the magnetic pogo connector for a JST-PH 2.0mm 8-pin pigtail cable — **never implemented; reversed 2026-09-03 (Session 4).** Actual `syth_mcu` board still uses **5-pin magnetic pogo** (J1/J2, `CONN-TH_PR5L4015-5P-C-F`), confirmed against pushed kicad (`f4e23e9`). See [[mcu-stm32-handoff]] for the real connector BOM. Build path confirmed **THT hand-solder** (Shopee/Lazada sourcing), not SMD/JLC-assembly — `synth_smd/` folder exists as an abandoned pricing-comparison copy, not the active project. Fixed a real bug in `dac-pchannel.kicad_sch`: C1/C2 were spec'd as 80nF electrolytic (no such part exists) — now 100nF ceramic disc.

**What:** modular synth/piano — per-octave PCB boards that snap together via 5-pin magnetic connectors.
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
| Interrupts from 2 modules | ✅ EXTI (joystick button) + TIM (PWM audio) |
| 2 of 3: ADC / PWM / graphic LCD | ✅ ADC (H3503 hall sensors + pots) + PWM (audio) + LCD (ILI9341 TFT) — all 3 covered |
| 4–6 features | ✅ keys/velocity, synthesis modes, modularity, TFT display, joystick expression, arpeggiator |
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

## Vision

**Seaboard + traditional synth hybrid.** Not a MIDI controller — STM32 *is* the synth. Touch data feeds internal synthesis engine → PWM audio out. MIDI USB output optional bonus (zero extra hardware, USB-C already on board).

Per-note expression axes:
- **Pressure** — force/cap magnitude → amplitude or filter cutoff
- **Glide** — finger position along key (pad A/B/C) → pitch bend cents / vibrato
- **Slide** — cross-key movement → portamento

---

## Synthesis Modes

Switch selector (5-position rotary) picks mode:

| Position | Mode | Character |
|---|---|---|
| 0 | Karplus-Strong | Piano / pluck, natural decay |
| 1 | Sine DDS | Pure tone, organ-like |
| 2 | Sawtooth DDS | Bright, classic synth lead |
| 3 | Square DDS | Hollow, retro |
| 4 | Noise burst | Percussion / hit |

**Karplus-Strong:** strike impulse fills delay line ring buffer with noise/half-sine → low-pass filter feedback loop → natural decaying harmonic tone. No lookup tables. Pure math.

**DDS:** phase accumulator + `arm_sin_f32()` (CMSIS-DSP, FPU-accelerated). Generates waveform mathematically in real time.

Expression per mode:

| Axis | K-S | Sine/Saw/Square | Noise |
|---|---|---|---|
| Pressure | damping coefficient | amp + filter cutoff | amp |
| Glide position | delay line fine-tune | pitch bend cents | — |
| Cross-key slide | portamento | portamento | — |

### 5 Pot Mapping

| Pot | Function |
|---|---|
| 0 | Master volume |
| 1 | Attack / pluck hardness |
| 2 | Decay / release |
| 3 | Filter cutoff |
| 4 | Effect wet (reverb / chorus) |

---

## Key Sensing — DECIDED: Resistive + Velostat

Cap touch rejected — MPR121 raw cap gives effectively binary touched/not-touched on bare PCB. Pressure gradient unreliable. Resistive approach chosen instead.

### Physical stack (per key, cross-section)

```
[Finger]
[Silicone layer]     ← compliance, squishiness (see below)
[Velostat sheet]     ← pressure-sensitive conductive material
[Pad A] [Pad B]      ← copper traces on PCB (2–3 zones per key)
```

Nothing conducts until pressed. Press → Velostat bridges pads → circuit completes. Harder press → Velostat resistance drops → ADC voltage shifts → pressure data.

### Circuit per key

```
3.3V ──[R1]──┬──[R2]── GND
             │
           ADC (via CD4051 mux)
             │
      [pad A]  [pad B]   ← Velostat contact pulls node
```

- **Position:** which pad activates → different voltage → which zone finger is on
- **Pressure:** contact resistance of Velostat drops under harder press → ADC reads magnitude
- **Interpolation:** both pads active simultaneously → voltage between A and B → sub-zone position

### Mux (CD4051)

12 keys = 12 ADC lines without mux. CD4051 (8:1): 3 GPIO selects key → 1 ADC reads it. Two CD4051s = 16 keys on 6 GPIO + 1 ADC. Scan cycle ~1ms → feels instant.

### Pin budget for sensing

| Block | Pins |
|---|---|
| CD4051 mux select | 3 GPIO |
| ADC (key sensing) | 1 |
| Total | 4 |

### Inspiration

Exact same principle as Nintendo DS touchscreen and laptop Synaptics touchpads — resistive voltage divider, ADC reads position + contact. Velostat drum pads common in DIY music gear.

---

## Surface Feel — Seaboard-Inspired

### Option 1: Poured silicone *(target for demo)*

Smooth-On Ecoflex or Dragon Skin (shore 10–30 = very squishy). Pour into 3D-printed or laser-cut acrylic mold shaped to key layout. Cast single continuous slab covering all keys. This is literally how Seaboard is manufactured.

Cost: ~฿600–800 small kit. Mold: 3D printed.

### Option 2: Silicone keyboard dome sheet *(fallback)*

Generic rubber keyboard dome sheets (calculator buttons, cheap rubber keyboards). Cut to key shapes. Sit on top of Velostat. Tactile snap on press.

Cost: ~฿50–100, Shopee.

### Option 3: Neoprene foam *(emergency fallback)*

Craft foam or neoprene sheet. Compressible, not as squishy. Cost: ~฿30.

**Call it "seaboard-inspired expression" in the proposal — accurate and strong.**

### Silicone mold design

Ecoflex 30 cast with raised ridges at key borders, recessed pockets above pad zones. Underside walls sit on PCB edges; recessed ceiling floats ~1mm above Velostat. Press → top deflects → Velostat contacts pad. One pour, one piece, no separate spacer.

---

## Rejected Alternatives — Key Sensing

### Capacitive sandwich (rejected 2026-08-26)

Proposed: conductor / compressible dielectric / conductor. Squeeze dielectric → gap `d` decreases → capacitance increases (`C = ε₀εᵣA/d`).

**Why rejected:** DIY dielectric (foam/silicone, εᵣ ≈ 1–3, gap ~1mm) gives small, environment-dependent cap delta. Needs dedicated capacitance readout (MPR121 or 555 oscillator) — adds circuit complexity. Velostat resistance swings ~10kΩ → ~100Ω (100× range), reads directly on ADC via voltage divider. Larger signal, simpler circuit. Capacitive sandwich only wins at MEMS scale with micrometer gaps.

### Capacitive touch / MPR121 (rejected 2026-08-26)

Binary touch on bare PCB. No reliable pressure gradient without silicone compliance layer. Velostat gives pressure natively and reads simpler.

---

## Universal PCB Design

**One board, two roles.** Same gerber, same fab order. Role set at assembly:

- **Bit 0 of DIP switch** = MASTER / SLAVE. Firmware reads on boot.
- **Master config:** populate screen connector + audio jack + USB connector.
- **Slave config:** DNP (Do Not Place) those three. Same PCB, unpopulated pads.

Same firmware binary. `if (role == MASTER)` branch at init. If master dies → bridge a slave's solder jumper → instant replacement.

---

## Per-Board Power

**USB-C 5V only. No 12V barrel. No buck converter.**

Each board self-powered. Any board is a valid power entry point.

```
USB-C 5V → (CC pins: 2×5.1kΩ to GND) → Schottky OR-ing diode → 5V_BUS (mag connector)
5V_BUS   → [AMS1117-3.3 LDO] → 3.3V rail → STM32, sensors, screen
```

Power daisy-chains through magnetic connectors. One USB-C cable into any board → whole chain alive.

**OR-ing diode (SS14 Schottky):** prevents two simultaneously-powered boards from fighting on the 5V bus.

**Power budget:** STM32 ~100mA + screen ~80mA + MPR121 ~3mA + misc ≈ 250mA per board. 3 boards = 750mA. USB-C 5V/3A = 3000mA. Plenty of headroom.

**Noise advantage:** no buck = no switching noise. LDO only → cleaner analog rail for audio.

**Analog/digital ground separation:** separate 3.3V pour for analog audio stage, join at one star point. Keeps switching noise off audio output.

**BOM per board:**

| Part | Component |
|---|---|
| LDO 5V→3.3V | AMS1117-3.3 (SOT-223) |
| OR-ing diode | SS14 Schottky (SOD-123) |
| USB-C connector | + 2×5.1kΩ on CC pins |

---

## Audio Output — DECISION PENDING

PWM → RC low-pass filter → audio out. Output target determines if MOSFET is needed.

| Target | Circuit |
|---|---|
| 3.5mm → powered speakers / DAW interface | RC filter direct from STM32 GPIO (high-Z load, no MOSFET needed) |
| 3.5mm → headphones (32Ω) | Small amp IC (PAM8403 or similar) — headphones too low-Z for direct drive |
| Passive speaker (4–8Ω) | MOSFET + RC filter, or dedicated amp IC |

**STM32 GPIO max 25mA** — fine for high-impedance loads, not for headphones or passive speakers directly.

> **Open question: what is the audio output target? Powered speakers, headphones, or passive speaker?**

---

## Keys Per Board

**12 keys.** 24 too tight on F411 pin budget (~32 usable pins).

12 = one MPR121 unit (one chip, one IRQ, one I2C address). Chain two boards for 24-key range.

---

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
