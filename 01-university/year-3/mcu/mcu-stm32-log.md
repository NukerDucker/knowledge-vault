---
title: Modular Synth — Session State
tags: [mcu, stm32, synth, session]
status: active
created: 2026-08-23
updated: 2026-09-02
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
- **PCM5102 I2S DAC** — tried and failed; also line-level out (1kΩ min load), can't drive headphones without amp → scrapped

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

## 2026-08-30 — Session 2 (PCB layout, DAC integration, Cream Bun review)

**What happened:** KiCad `syth_mcu` board built out heavily. Full detail: [[mcu-stm32-handoff]]. Summary:

- Sourced real magnetic pogo connector parts (5-pin, LCSC C41361292) via `easyeda2kicad`, added to project lib.
- Fixed U2 footprint (40-pad `YAAJ_WeAct_BlackPill_2`), USB-C footprint confirmed (Amphenol 12401610E4-2A).
- Integrated a full stereo DAC output stage as a hierarchical sheet (from `STM32Synth-main` reference), wired `+3V3 DAC`/`GNDDAC` out to `AMS2_3.3V`/`GND` — previously dangling. PWM pins: `PA6` (Left, TIM3_CH1) + `PB3` (Right, TIM2_CH2, own pick — free of TFT SPI conflict).
- Resolved footprints for the whole DAC BOM (transistors, 4 cap types, fuse, trim pots, jack).
- Fixed a malformed-courtyard DRC bug on U5 (one F.CrtYd line 0.254mm off).
- Widened board 167×94.5mm → 286×133mm to fit a 12-key real-pitch hall row; relocated H1-H12 mounting holes to the new bottom edge.
- Added 2× 20-pin breakout headers (J5/J6) flanking U2, net-labeled to expose every MCU pin.
- Dropped the 5-position mode-select rotary (not sourceable in Thailand) → 3 discrete buttons (SW6/7/8, PB13/14/15) instead.
- Swapped the TFT connector from a full module footprint to a 10-way IDC box header — screen mounts off-board via ribbon cable, not on the PCB.
- Added F.Cu=`D_5V` / B.Cu=`GND` filled zones as a power plane (user's own GUI work, post-routing).
- Committed + pushed to `github.com/NukerDucker/mcu-synth` — `main` and a `review/creambun` mirror branch for design review.

### Newly surfaced problem

- **Mux is full.** Single 74HC4051 (8 channels) is entirely consumed by hall keys 0–7. Remaining 4 hall keys + 5 pots have **zero free ADC-capable GPIO** on the real F401/411 pinout (verified against the actual U2 symbol, not assumption). 2nd mux explicitly declined by user — unresolved, real constraint, not just a TODO.
- **Architecture drift, unconfirmed:** the 2026-08-23 master/slave zone-population plan (one Gerber, populate differently per role) doesn't obviously match the current single combined board carrying controls + DAC + keys together. Needs a straight answer from the team, not an assumption either way.

### Blocked/open (carried forward, see [[mcu-stm32-handoff]] for full list)

- DAC cluster physical placement not finalized (blind placement attempt reverted this session — do via GUI only).
- H5/H7 zone thermal-relief DRC, U4/PB7 clearance, J3 edge clearance — all minor, unresolved.
- Board name undecided (Apollo / Pandora shortlisted).

---

## 2026-09-01 — Session 3 (kicad-happy review, SMD-vs-THT decision, split-board joint spec)

**What happened:**

- Ran `kicad-happy` schematic + PCB analyzers on `syth_mcu`. Confirmed RV6/RV7 courtyard overlap (fix: smaller footprint, same coords, no relocation needed) and traced R1/R2 CC1/CC2 pull-downs as a **false-positive** analyzer warning (nets are unnamed `__unnamed_0`/`__unnamed_2` but correctly wired 5.1k to GND — analyzer just doesn't label them).
- Verified USB-C receptacle (J3) end-to-end: `USB_C_Receptacle_PowerOnly_6P` symbol + Amphenol `12401610E4-2A` footprint, VBUS→D1 (OR-ing diode)→AMS1117, GND correct, CC1/CC2→R1/R2 5.1k pulldowns correct (standard no-PD-chip 5V/3A default-sink trick). Shield pin is `NO_CONNECT` — optional EMC improvement, not a blocker.
- Duplicated project to `synth_smd/` to price an all-SMD BOM variant via JLCPCB assembly. Sourced real LCSC parts for the DAC passives (100nF→`C49678` basic, 1uF→`C1848` basic, 33uF elec→`C53200078` extended). **Decision: not SMD** — staying THT, hand-solder, sourcing off Shopee/Lazada. `synth_smd/` is now a dead-end reference copy, not the active project.
- Found and fixed a real schematic bug while sourcing: **C1/C2 were specified as 80nF electrolytic — no such part exists** (electrolytics don't go below ~0.1-1uF). Fixed in `dac-pchannel.kicad_sch`: C1/C2 value 80nF→100nF, footprint `CP_Radial_D4.0mm_P2.00mm`→`C_Disc_D5.0mm_W2.5mm_P2.50mm` (ceramic disc, correct part family for that value). Also widened C6/C8 (33uF DC-block caps) footprint `CP_Radial_D4.0mm`→`D5.0mm` to match the actual sourced part body size (ELNA 5×11mm).
- C5/C7 (1uF, rail decoupling — confirmed not in the audio signal path) still undecided between two Shopee options: CBB film 450V (check lead pitch fits `C_Rect_L9.0mm_W3.2mm_P7.50mm_MKT` footprint) vs ELNA 50V electrolytic 5×11mm (needs footprint swap to `CP_Radial_D5.0mm_P2.00mm` + polarity-correct placement, `+`→`+3V3 DAC`, `-`→`GNDDAC`).
- **Split left/right half-octave board — clarified the internal joint spec.** Left half (5 keys, no MCU) has zero I2C-capable silicon on it, so the I2C bus arriving at the left-edge octave-chaining connector must **pass straight through** the left board to reach the right board's STM32 — it's not just analog hall-sensor lines crossing the solder seam. Joint carries **8 unique nets, 1 shared GND**: `5V, GND, SDA, SCL` (bus pass-through) + 5× hall-sensor analog outs (GND doubles as both bus ground and sensor return — no need to split it).
- **Octave-to-octave chaining connector — dropped magnetic pogo plan.** Sourcing/aligning real pogo hardware in Thailand was flagged as unnecessary risk for the deadline. New pick: **JST-PH 2.0mm 8-pin, pre-crimped pigtail cable** (buy the whole assembly pre-terminated off Shopee, not raw connector + crimp pins) — solder one 8-pin header per board edge, plug cable between octaves. Trade mechanical "boards click together" elegance for near-zero assembly labor and reliable sourcing.

### Open / carried forward

- [ ] Decide C5/C7 part (CBB film vs ELNA electrolytic) and apply the matching footprint
- [ ] Update `syth_mcu.kicad_pcb` footprints to match the schematic edits above (schematic-only fix so far — PCB will show stale footprints until "Update PCB from Schematic" is run in KiCad)
- [ ] RV6/RV7 courtyard fix not yet applied to the PCB file
- [ ] Shield pin on J3 — optional GND tie for EMC, not done
- [ ] Physically confirm: is the left/right half-octave joint one continuous PCB, or two separate fabbed boards bridged by solder? Changes whether pogo-connector Z-height alignment across octaves is a real risk.
- [ ] Order bare PCB gerbers from JLCPCB (steps scoped, not yet executed)

---

## 2026-09-03 — Session 4

> [!warning] Reverses Session 3's "dropped magnetic pogo" call
> Actual `syth_mcu.kicad_sch`/`.kicad_pcb` (pushed `f4e23e9`) still carry J1/J2 as
> 5-pin magnetic pogo (`synth:CONN-TH_PR5L4015-5P-C-F`), matching the
> [[mcu-stm32-handoff]] BOM. JST-PH pigtail plan above was never implemented —
> board is back on pogo. Treat the JST-PH line above as abandoned, not current.

**New risk flagged:** H3503 hall sensor (key row) sits ~3mm from the pogo mag
connector. Pogo connectors hold retention magnets — stray field at 3mm is close
enough to bias or saturate the H3503's analog output. Not yet measured on
hardware. Added to Open Items.

**Committed/pushed:** `syth_mcu.kicad_pcb`, `.kicad_sch`, `.wrl` — `f4e23e9`.

---

## 2026-09-06 — Session 5 (Cream Bun review triage, kicad-happy analysis)

Ran kicad-happy analyzers (schematic + PCB --full + cross-analysis) against `syth_mcu` to triage Cream Bun's review list. Enabled kicad-happy MCP plugin.

### Confirmed findings

**Serious — schematic fix + PCB rework required:**
- **SI2307DS / SI2304DS pinout wrong (Q1–Q4):** Symbol encodes pad1=D, pad2=G, pad3=S. Actual Vishay SOT-23 pin1=Gate, pin2=Source, pin3=Drain. Gate driver PWM wired to Source physical pin; audio stage will not switch. Fix: correct symbol pin assignments in schematic editor, re-route two pads per transistor (4×). Added to Open Items.
- **PB7 I2C trace cut — confirmed:** PB7 net has 2 isolated copper islands on F.Cu. Gap bbox: (182.26, 122.67) → (191.53, 130.30). Island 0: J2:3, J5:15, J10:15, D10:1, SDAPullUpM1:2. Island 1: J1:3, D11:1. Fix: route one trace segment on F.Cu across the gap. Added to Open Items.

**Slightly serious — assembly/layout:**
- **Fuse height:** RXEF160 = 20.8mm tall, RXEF040 = 13.4mm. 5mm footprint pitch is correct for bent horizontal mounting. Assembly instruction only: bend all three fuses (F1–F3) flat before soldering.
- **BlackPill header edge distance:** +1mm from measured. GUI fix — nudge J5/J10 pair toward board center.

**MUX:**
- J7 (MUX channel socket, 1×16) moved −2.54mm in x: `(154.35, 142.2175)` → `(151.81, 142.2175)`. Applied directly to `syth_mcu.kicad_pcb`. ✅
- J8/J9 misalignment: J9 does not exist in PCB. Cream Bun clarification needed — which two connectors she measured.
- C0 mux label: move to GND side by relabeling hall sensors in schematic (no trace rework).

**Also found by cross-analysis:**
- GND plane: 15 copper islands, 49 signals crossing splits — EMI risk. Pre-existing; not from Cream Bun's list.
- 3V3 plane: 2 islands, 9 signals crossing.

---

## Open Tasks (next session)

**PCB fixes (Cream Bun — in priority order):**
- [ ] **Fix SI2307DS / SI2304DS symbol pinout** in schematic editor: pin1=Gate, pin2=Source, pin3=Drain. Then Update PCB from Schematic + re-route Q1–Q4 (2 pads per transistor swapped).
- [ ] **Bridge PB7 trace gap** on F.Cu at bbox (182.26, 122.67)→(191.53, 130.30) — route one segment connecting J1:3 island to SDAPullUpM1/J2 island.
- [ ] **BlackPill header edge distance** — measure board edge at J5/J10 y-position, shift both +1mm toward board center in GUI.
- [ ] **Relabel hall sensors** so C0 appears on GND side of mux (schematic label change only).
- [ ] **Clarify with Cream Bun**: J8/J9 alignment — J9 doesn't exist in PCB; which connectors she measured.
- [ ] Minor PCB items (GUI): C14-18 caps move up, silkscreen collisions, ground bridge moves/additions, 5V corner smoothing, 2-pin voltage source headers.

**From previous sessions:**
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

## Parts Ordered

- **PJ-316 3.5mm audio jack** (J4) — ฿125.00, ร้าน มหาชัยอิเล็กทรอนิกส์ (mahachaielectronics.com), Shop ID 533057, Order ID 16657 — [order link](https://lnw.me/order/mahachaielectronics/16657?s=8952f322)

## Files

| File | Location | Status |
|------|----------|--------|
| Reference note | `01-university/year-3/mcu/mcu-stm32-project.md` | ✅ Done |
| This session state | `01-university/year-3/mcu/mcu-stm32-log.md` | ✅ Done |
| Assignment tracker | `01-university/assignments-tracker.md` | 🔄 Update when deadline drops |
| Code | none yet | — |
