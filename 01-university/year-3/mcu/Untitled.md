## Board Review: kicadrt_analysis_syth_mcu.kicad_pcb

  

2-layer board (F.Cu/B.Cu, 1.51 mm core), 813 segments, 97 vias, 392 pads, 16 zones. Graded at **0.2 mm** — the board's own `min_clearance` / Default netclass from the sibling `.kicad_pro`. No `.kicad_dru` sibling → no per-layer rules. Zone DRC ran on a copy (`/tmp/rvw_syth.kicad_pcb` + its `.kicad_pro`); source board untouched.

  

| Check | Result |

|---|---|

| DRC (check_drc.py) | **FAIL** — 2 same-net soft joints (+4 same-net self-crossing warnings) |

| Zone DRC (kicad-cli, refilled) | **FAIL** — 87 `annular_width` errors; **0 clearance/short/track-width** |

| Connectivity | **FAIL** — 2 nets with disconnected pads (kicad-cli agrees: 2 unconnected items) |

| Orphan stubs | **FAIL** — 1 orphan (MCU5V, F.Cu) |

  

### Failures

  

**Connectivity (hard fail).** Both failures land on the same two connectors, J5/J10:

- `3V3` (net 10): pads (170.59, 101.74) [J5], (175.50, 101.74) [J10] disconnected.

- `MCU5V` (net 28): pads (170.59, 96.66) [J5], (175.50, 96.66) [J10] disconnected.

  

**MCU5V's three findings are one net, likely one failure:** disconnected J5/J10 pads, a 0.515 mm soft joint at (194.415, 51.520)↔(193.900, 51.500), and an orphan stub at (201.39, 53.48).

  

**Soft joints (2).** `C2` F.Cu, gap 0.043 mm at (155.037, 121.795)↔(155.037, 121.838) — marginal, cap overlap 0.211 mm. `MCU5V` above — real break.

  

**Annular width (87).** Split from the DRC JSON: **51 vias**, **36 pads**.

- Vias: 43 × 0.45/0.20 (annular 0.125), 8 × 0.50/0.30 (annular 0.10) vs `min_via_annular_width` 0.18.

- Pads: pre-existing footprint PTH — not caused by routing.

- **Board rules are self-inconsistent:** `min_via_diameter` 0.45 with `min_via_annular_width` 0.18 is unsatisfiable at a 0.2 mm drill (needs ≥0.56 mm). A via sized to the board's own minimum trips its own annular rule. Fix one side, not the copper.

  

Out of scope for routing: 25 `lib_footprint_issues`, 1 `lib_footprint_mismatch`, 1 `text_thickness`; 19 silk/dangling ignored per grader convention.

  

### Informational

2-layer, GND pour on B.Cu only, F.Cu carries 11 small power/local pours → the 2124 mm "over void" and the Z0 deltas from `check_impedance.py` are structural, on uncontrolled-impedance GPIO/USB-CC nets. Escalate none.

  

### Next actions

1. `/diagnose-routing-failures` with the routing logs for `3V3` and `MCU5V` (both fail at J5/J10 — check that region for blockage), which should also clear the MCU5V soft joint + orphan stub.

2. Decide the via rule: rerun with via diameter ≥0.56 mm (0.2 drill) / ≥0.66 mm (0.3 drill), or relax `min_via_annular_width` to the fab's real limit.

3. Re-check the C2 0.043 mm joint after the reroute; it is borderline, not a break.

  

RESULT=FAIL