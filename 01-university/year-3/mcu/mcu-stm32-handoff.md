# MCU Modular Synth — Design Handoff

**Session date:** 2026-08-30 (updated from 2026-08-28 baseline)
**Project:** Modular Synthesizer Piano — MCU Interfacing (01276314)
**Proposal due:** 2026-09-08 | **Demo:** 2026-10-21
**Team size:** 6–7 | **Points:** 100
**Repo:** `github.com/NukerDucker/mcu-synth` — branches `main`, `review/creambun` (Cream Bun design-review branch)

> [!warning] Architecture drift since 2026-08-28
> The zone-based single-Gerber master/slave split described below (locked 2026-08-28) has **not been re-confirmed** against the current `syth_mcu` board, which is now a single combined board carrying controls + DAC audio stage + a 12-key hall row on one PCB (286×133mm). Verify with team whether the master/slave zone-population plan is still the intended multi-board scheme, or whether `syth_mcu` has become the whole instrument on one board.

---

## What This Is

STM32F411-based modular synthesizer. STM32 IS the synth — no external MIDI, no PC needed. Current physical board (`syth_mcu`): 286×133mm, control row (5 pots, 5+3 buttons, TFT connector) + stereo DAC output stage + a 12-key hall-effect row along the bottom edge.

---

## Current PCB State (`syth_mcu`, as of 2026-08-30)

**Board outline:** 286mm × 133mm (`Edge.Cuts`, start 8.74,20.48 → end 294.74,153.48). Widened from an earlier 167×94.5mm to fit a full 12-key real-pitch (~23mm) hall row below the control row.

**Repo:** `~/Documents/University/Year-3/Microcon/synth/` — `syth_mcu/syth_mcu.kicad_sch` + `.kicad_pcb`, project libs `synth.kicad_sym` / `synth.pretty/`. Committed and pushed to `main` (`c7e0188`) and mirrored to `review/creambun` for Cream Bun's review.

**ERC:** 0 pin_not_connected, 2 remaining (both minor, unaddressed): U2 pin 20 (3V3, duplicate power pin) and U2 pin 21 (VBat) not driven — trivial GUI wire-adds, not blocking.

### Connectors (confirmed parts, not placeholders)

| Ref | Part | Source |
|---|---|---|
| J3 | USB-C receptacle | `Connector_USB:USB_C_Receptacle_Amphenol_12401610E4-2A` |
| J1, J2 | 5-pin magnetic pogo | `synth:CONN-TH_PR5L4015-5P-C-F` — real LCSC part (C41361292), symbol+footprint pulled via `easyeda2kicad`, added to project lib |
| J4 | 3.5mm audio jack | `Connector_Audio:Jack_3.5mm_CUI_SJ1-3533N_Horizontal` |
| J5, J6 | 2× 20-pin IDC-style breakout headers flanking U2 | `Connector_Generic:Conn_01x20`, net-labeled to mirror every U2 pin (used + spare) for future expansion |
| TFT | screen connector only, not full module footprint | swapped from full `TFT-320x240` outline+mount-holes footprint to a **10-way IDC box header** (`Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical`) — 9 real signals (VCC/GND/CS/RST/DC/MOSI/SCK/LED/MISO) + 1 spare GND pin. Screen itself mounts off-board, wired via ribbon cable, not board-mounted. |

Also fixed: pogo connectors were originally 4-pin, needed 5 signals (5V/GND/PB6/PB7/PA11-PA12) → replaced with 5-pin part. U2 footprint corrected to `YAAJ_WeAct_BlackPill_2` (40 pads — the two other candidate footprints only had 34, missing pins 35–40).

### DAC / Audio Output Stage

Replaced the old "PWM → 2N7002 → RC filter → jack" plan with a full stereo P-channel gate-driver DAC circuit, integrated as a hierarchical sheet (`dac-pchannel.kicad_sch`, sourced from `STM32Synth-main` reference project, wired into the main schematic with proper hierarchical labels — a stray external-path duplicate sheet was found and deleted).

- **Left channel:** `PA6` (TIM3_CH1) — matches upstream reference firmware.
- **Right channel:** `PB3` (TIM2_CH2) — confirmed free via net-label grep; not in upstream reference firmware, this session's own pick.
- Per channel: R5/R3 or R6/R4 → Q1/Q2 or Q3/Q4 (SI2307DS/SI2304DS, SOT-23) gate driver pair → R7/R8 (100Ω 1%) series → C1/C2 or filter node → C6/C8 (33µF) DC-block → RV6/RV7 (100k trim pot) → `AudOutRight`/`AudOutLeft` → J4.
- Power: `+3V3 DAC` / `GNDDAC` nets, now wired out via hierarchical labels to **AMS2_3.3V** (U4's regulator — the audio-dedicated one, not U3/AMS1 which feeds MCU/TFT) and main `GND`. Previously these nets existed only inside the DAC sub-sheet with no path out — this was the "power not properly line[d]" gap, now closed.
- Footprints resolved for the full DAC BOM: Q1-4 SOT-23; C3/C4 (0.1µF) `C_Disc_D5.0mm_W2.5mm_P2.50mm`; C5/C7 (1µF) `C_Rect_L9.0mm_W3.2mm_P7.50mm_MKT`; C1/C2 (80nF) — same non-polarized `C_Rect` box-film type as C5/C7 (was wrongly `CP_Radial`, fixed); C6/C8 (33µF) `CP_Radial_D4.0mm_P2.00mm`; F1 `Fuse_Bourns_MF-RHT200`; RV6/RV7 `Potentiometer_Bourns_3296W_Vertical`.

### Piano Key Row (12 hall keys, real-pitch layout)

Placed as a 12-key row (7 white + 5 black per octave) along the widened bottom edge, replacing the earlier plan of a separate per-octave key-module board (see architecture-drift warning above — this board now appears to carry the keys directly).

- White key centers: `x_i = i·W + W/2`, i = 0..7 (8 positions incl. next-octave C boundary key)
- Black key centers (boundary midpoints, skip E–F and B–C gaps): C♯ = 1.0W, D♯ = 2.0W, F♯ = 4.0W, G♯ = 5.0W, A♯ = 6.0W
- W (white key pitch) — use real finger-width pitch (~23–24mm), not the earlier compressed 20mm board-math figure. Board width derives from `8W` after W is fixed.
- H1–H12 mounting holes relocated to the new true bottom edge (~y=178, 7mm margin) below the key row, using Align+Distribute rather than manual per-hole placement.

**Mux budget is full:** the single 74HC4051 on board handles hall keys 0–7 only (8 channels, all claimed). No second mux added (explicitly declined) — remaining 4 keys + 5 pots have **no free ADC-capable GPIO** (confirmed against the real U2 pinout: only PB13, PB14, PB15, PA15, PC13, PC14, PC15 are unconnected, and none of those are ADC1 pins on F401/411). This is an open, unresolved constraint — see Open Items.

### Extra Buttons (mode select)

5-position rotary switch (for synth-mode select) dropped — not sourceable in Thailand. Replaced with discrete buttons on free GPIO instead:

| SW | GPIO | Suggested function |
|---|---|---|
| SW6 | PB13 | Mode Next |
| SW7 | PB14 | Mode Prev |
| SW8 | PB15 | spare (arpeggiator toggle / hold) |

Leaves PA15, PC13(LED), PC14, PC15 still free (PC14/15 are also the LSE crystal pins — only safe as GPIO if no 32kHz crystal populated).

### Power Plane

User added filled copper zones via GUI (F.Cu = `D_5V`, B.Cu = `GND`) as a power plane, per Cream Bun's suggestion, done after signal routing was complete. Hit "thermal relief connection to zone incomplete" DRC errors on H5/H7 mounting-hole pads (min spoke count 2 vs. actual — pad too small) — fix is Pad Properties → Zone Connection → Solid on those two pads; not yet confirmed re-DRC'd clean.

### DRC Fixes This Session

- U5 malformed courtyard (F.CrtYd rectangle had one edge 0.254mm off from the other three, KiCad didn't see it as closed) — root-caused and fixed directly in the file, verified 66→5 violations via `kicad-cli sch/pcb drc`.
- A blind, file-level batch reposition of the 19-part DAC cluster was attempted and **reverted** — courtyard/trace collisions from not accounting for U2's real (much larger than its reference point suggests) footprint extent. Lesson: do footprint/copper-geometry placement via GUI with visual + DRC feedback, not blind coordinate edits. (The U5 fix above was safe because it was a single, precisely-diagnosed line coordinate with no dependent geometry — not a placement job.)
- Remaining open DRC: U4/PB7 clearance (2µm short, trivial GUI nudge), J3 edge clearance (recommended: DRC-exclude as intentional edge-mount, not move).

---

## Key Decisions Still Valid From 2026-08-28 Baseline

### Key Sensing — Hall Effect + Custom Mechanism

**No MX switches.** Custom 3D-printed key mechanism:

```
[ Keycap — 3D printed ]
[ guide rail ] ← prevents wobble
[ compression spring ] ← return force (pen spring or 8mm coil)
[ magnet 6×2mm neodymium, epoxied to key bottom ]
↕ 3–4mm travel
[ H3503 hall sensor on PCB ]
```

- **Sensor:** H3503 linear hall effect, TO-92, ~14mA each, analog output
- **Signal:** stem travel depth → voltage → velocity
- **Magnet-to-sensor gap at rest:** 3–5mm; at full press: 1–2mm
- **Test one key first** before printing all 12

### Communication — I2C

**I2C GPIO:** all boards — Alternate Function, Open-Drain, `GPIO_NOPULL` in firmware.
**Pull-ups:** external 2kΩ resistors on SDA + SCL. Rise time = 0.8473 × 2000 × 100pF = 0.17µs — within UM10204 §6.1 1000ns limit.
> **Why not internal pull-up:** STM32 internal = 40kΩ → rise time ~3.4µs >> 1µs spec limit → bit errors.
**I2C speed:** still TBD — open item.

### Synthesis Engine

5 modes via button selection (now SW6/SW7 Next/Prev instead of a rotary):

| Mode | Character |
|---|---|
| Karplus-Strong | Piano/pluck, natural decay |
| Sine DDS | Pure tone, organ |
| Sawtooth DDS | Bright synth lead |
| Square DDS | Hollow, retro |
| Noise burst | Percussion |

### 5-Pot Mapping

| Pot | Function |
|---|---|
| RV1 | Master volume |
| RV2 | Attack / pluck hardness |
| RV3 | Decay / release |
| RV4 | Filter cutoff |
| RV5 | Effect wet (reverb/chorus) |

---

## Open Items

- [ ] **Resolve architecture drift** — is `syth_mcu` now the whole instrument on one board, or is the master/slave zone-population multi-board plan still current? Confirm with team before committing further.
- [ ] Mux is full (8/8 channels, hall 0–7) with no free ADC GPIO for the remaining 4 hall keys + 5 pots — 2nd mux was explicitly declined; needs a decision (drop the 4 extra keys, drop some pots, or reconsider the mux).
- [ ] Finalize physical placement of the 19-part DAC cluster on the real PCB (previous attempt reverted — do via GUI, not blind edit).
- [ ] H5/H7 mounting-hole pads → switch Zone Connection to Solid, refill zones, re-DRC.
- [ ] U4/PB7 clearance (2µm), J3 edge clearance (DRC-exclude) — both trivial, unresolved.
- [ ] U2 pin 20 (3V3) and pin 21 (VBat) — unconnected power inputs per ERC, wire or accept.
- [ ] Confirm TFT module's actual ribbon pin pitch (2.54mm assumed, some cheap modules use 2.0mm) before finalizing IDC connector footprint.
- [ ] Verify trace-width table from Cream Bun's screenshot against actual netclass settings (only the via/hole spec was ever transcribed — via sizing already exceeds her JLCPCB minimums, track width unconfirmed against her exact numbers).
- [ ] Board name — still undecided (Apollo vs Pandora shortlisted, no pick made).
- [ ] F1 (fuse) — flagged missing from PCB placement earlier, needs an Update-PCB-from-Schematic pass to confirm it's on the board now.
- [ ] IDC ribbon crimping — no dedicated crimp tool assumed; vice-press method identified as the practical no-tool approach (padded vice jaws > groove-joint pliers > standard pliers).
- [ ] 3D print test key mechanism — verify H3503 signal at rest + full press before printing all 12.
- [ ] H3503 (key row) sits ~3mm from J1/J2 pogo mag connector — pogo retention magnet stray field may bias/saturate the sensor. Unmeasured. See [[mcu-stm32-log]] Session 4.
- [ ] Add MPNs to all BOM parts before fab.

---

## What NOT to Revisit

| Rejected | Reason |
|---|---|
| Velostat | No reliable velocity gradient |
| MX switches | Hall-only custom mechanism chosen |
| MPR121 cap touch | Binary on/off only |
| CD4067 | Sourcing — use 74HC4051 instead |
| I2S DAC IC | Replaced by discrete P-channel gate-driver DAC stage (see above) — not PWM+RC either anymore |
| Buck for 3.3V rail | Switching noise on audio rail |
| 12V / 9V distribution | 5V USB-C per board sufficient |
| MPU-6050 tilt | Tabletop keyboard can't tilt |
| Aftertouch | Too complex, not demo-visible |
| IR sensor | Ambient light sensitivity |
| 2× 74HC4051 at 2026-08-28 baseline | later needed again for full 12-key + pot budget — see Open Items, this rejection is now under reconsideration |
| Toggle switch (master/slave) | Compile-time #define instead |
| 4.7kΩ I2C pull-up | Never decided — 2kΩ used instead |
| Internal STM32 pull-up for I2C | 40kΩ → 3.4µs rise time >> 1µs spec limit |
| 5-position rotary mode switch | Not sourceable in Thailand — replaced with 2-3 discrete buttons |
| Full TFT module footprint on-board | Replaced with 10-way IDC connector only — screen mounts off-board via ribbon |
| Loose Dupont jumper wires for TFT | User wants proper IDC ribbon cable, sourceable in Thailand (Shopee TH) |

---

*See also: [[mcu-stm32-project]] — main project note | [[mcu-stm32-log]] — session log*
