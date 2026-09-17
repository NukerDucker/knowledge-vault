---
title: PCB V2 — Change Plan
tags: [mcu, stm32, hardware, pcb, v2]
status: active
created: 2026-09-14
subject: mcu
---

# PCB V2 — Change Plan

V1 board (`syth_mcu`) exists for testing. V2 is the revision to fix known bugs
and add the features needed for the full multi-board architecture.

See [[mcu-stm32-handoff]] for open items inherited into this plan.
See [[mcu-stm32-project]] for project schedule.

---

## 🔴 Critical Fixes (blocks functionality)

### 1. DAC Transistor Pinout — Q1–Q4 (SI2307DS / SI2304DS)
**Problem:** Symbol has pad1=D, pad2=G, pad3=S. Actual Vishay SOT-23: pin1=Gate, pin2=Source, pin3=Drain. Audio stage will not switch.  
**Action:** Fix symbol in KiCad schematic editor → reroute Q1–Q4 pads.  
**Scope:** Schematic + layout.

### 2. PB7 I2C SDA Trace Cut
**Problem:** Two isolated copper islands on F.Cu. Gap at bbox (182.26, 122.67)→(191.53, 130.30). I2C bus non-functional.  
**Action:** Route one trace segment on F.Cu to bridge the gap.  
**Scope:** Layout only.

---

## 🟠 Feature Changes (required for target architecture)

### 3. Replace 74HC4051 with 74HC4067
**Why:** HC4051 has 8 channels (covers H1–H8 only). HC4067 has 16 channels — covers all 12 hall keys + 4 pots on one chip.  
**GPIO cost:** +1 select pin (S3). Assign to a free GPIO (PA15 / PC14 / PC15 candidates).  
**Budget with HC4067:**

| Channel | Signal |
|---|---|
| Y0–Y11 | Hall keys H1–H12 |
| Y12–Y15 | RV1–RV4 (vol, attack, decay, filter) |

**Note:** RV5 (effect wet) needs either a free ADC GPIO or a second mux. Check PA4/PA5.  
**Scope:** Schematic swap + layout (same interface footprint, +1 GPIO trace).

### 4. Pogo Pin 5 — GND → CHAIN GPIO (J1 and J2)
**Why:** Enables auto-discovery of slave positions at boot. One GND per connector is sufficient (pins 1 and 2 provide power/ground; pin 2 GND remains).  
**Change:**
- J1 pin 5: net `GND` → net `CHAIN_IN` → GPIO input (PULL-DOWN)
- J2 pin 5: net `GND` → net `CHAIN_OUT` → GPIO output

**New GPIOs needed:**

| Signal | Pin candidate | Notes |
|---|---|---|
| S3 (HC4067 select) | PA15 | Not ADC-capable — fine for digital select |
| CHAIN_IN (J1 pin 5) | PC14 | Not ADC-capable — fine for digital input |
| CHAIN_OUT (J2 pin 5) | PC15 | Not ADC-capable — fine for digital output |

Confirm PA15/PC14/PC15 are free in the `.ioc` before committing.  
**Scope:** Schematic net relabel on J1/J2 pin 5 + 3 new GPIO traces.

---

## 🟡 Minor Cleanup

### 5. Mounting Holes H5/H7 — Zone Connection
Change pad zone connection from Thermal to Solid. Refill zones, re-DRC.

### 6. U2 Pin 20 (3V3) and Pin 21 (VBat)
Unconnected power inputs per ERC. Wire to appropriate nets or add PWR_FLAG.

### 7. TFT Ribbon Connector Pitch
Confirm actual pitch of TFT module ribbon (2.54mm assumed, some cheap modules use 2.0mm).
Update IDC connector footprint before fab.

### 8. Fuse F1 Placement
Run Update-PCB-from-Schematic. Confirm F1 appears on board. Place if missing.

### 9. Trace Width Confirmation
Verify track width against Cream Bun's JLCPCB minimums screenshot.
Via sizing already confirmed adequate. Track width unconfirmed.

### 10. Board Name
Shortlisted: Apollo, Pandora. Decision pending team vote.

---

## V2 Checklist (work order)

Do in this order to minimise re-spins:

- [ ] Confirm PA15/PC14/PC15 free in `.ioc`
- [ ] Fix Q1–Q4 symbol and reroute
- [ ] Bridge PB7 trace
- [ ] Swap HC4051 → HC4067 in schematic; add S3 trace
- [ ] Relabel J1/J2 pin 5 nets; add CHAIN_IN/CHAIN_OUT traces
- [ ] Wire U2 pins 20/21
- [ ] Confirm TFT pitch; update footprint if needed
- [ ] Run Update-PCB-from-Schematic; place F1
- [ ] Fix H5/H7 zone connection; refill
- [ ] Verify track widths vs JLCPCB minimums
- [ ] Full DRC — target 0 errors
- [ ] Decide board name
- [ ] Add MPNs to all BOM parts
- [ ] Send Gerbers to JLCPCB (order 5 boards)

---

## What Does NOT Change

| Item | Reason |
|---|---|
| Board outline (286×133mm) | Fits all 12 keys; no mechanical reason to change |
| Pogo connector part (CONN-TH_PR5L4015-5P-C-F) | Real part, confirmed fit |
| I2C pull-up values (2kΩ) | Rise time 0.17µs — within spec |
| USB-C (J3) | No changes needed |
| DAC stage topology | Correct after Q1–Q4 pinout fix |
| STM32F411 Black Pill (U2) | Fixed by course requirement |

---

*See [[mcu-stm32-handoff]] for full open-item history.*  
*See [[mcu-hc4067-mux]] for HC4067 wiring details.*
