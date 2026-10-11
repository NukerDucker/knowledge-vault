---
title: "KMITL B-App — Figma Changelog 2026-10-11"
tags:
  - university
  - project
  - reference
status: active
subject: uxui
course: 01276545
updated: 2026-10-11
---

# Figma Changelog — 2026-10-11

Every change made to `UX/UI 2026 — KMITL-BApp` (`bhuuET1PKmzZSGMkVr2de7`) in the 2026-10-11
session, with before → after and the rule it serves. This is the authority for the report's
"what changed and why" and for the AI Use Log.

Verified by re-census through the Desktop Bridge at the end of the session. **Live hexes only** —
`#1B2A5B` navy, `#E8622D` orange. Any note still carrying `#1A2340` / `#E86027` is stale.

---

## 1 · Badge instances (session start)

| # | Change | Before | After | Detail |
|---|---|---|---|---|
| B1 | Stale instance overrides swept | 29 of 126 badge instances carried old fills/strokes (`#059669` halo on Screens, `#D97706` fill on Components) | All match their main components | The component set was already fixed; the instances were not. Same failure mode as the earlier repair — **the component set is not where a fix lands** |
| B2 | Section labels renamed | `Chonnanok / User / …` | `Chonchanok / Student / …` | Typo + user type now matches the brief's `Alex / Buyer` format |
| B3 | Caption text renamed | `Chonnanok / User` (11 frames) | `Chonchanok / Student` | Captions under frames |
| B4 | Stale loose Map frame deleted | `4782:10855`, bare `1–7` floor numerals, unlinked | gone | Pre-fix copy; the two live Maps inside Room Info keep `1F–7F` and stay linked |

## 2 · Navy text sweep (A1)

| # | Change | Before | After |
|---|---|---|---|
| N1 | 49 TEXT fills | `#1A2340` | `#1B2A5B` |

Post-census: **0 text nodes render `#1A2340`.** The old navy was a second, slightly-different
colour used by stepper labels, chips, room-card meta and buttons.

## 3 · Grey text audit (A2)

The failing grey was `#9CA3AF` (2.54:1 on white). It entered the file three ways:

| # | Path | Change | Count |
|---|---|---|---|
| G1 | Token `Text/Hint` (`VariableID:4094:7332`) | value `Neutral/300 #9CA3AF` → `Neutral/400 #6B7280` (4.83:1) | token-level — every placeholder and hint, incl. disabled-field placeholders, now readable |
| G2 | Direct `Neutral/300` bindings on content text | rebound → `Text/Secondary` (`#6B7280`) | 13 nodes: room-card meta (`Cap:`, counts, `·`, building), Upload File labels, activity-name placeholder |
| G3 | History Tab Bar labels misusing `Text/Disabled` | rebound → `Text/Secondary` on both the instances and the primary Button variant main | 6 nodes — an inactive tab is still readable text, not a disabled control |
| G4 | Disabled-state placeholders | rebound → `Text/Disabled` (kept `#9CA3AF`) | 3 nodes (`4509:12106`, `4509:12115`, `4509:12127`) — disabled controls are WCAG-exempt |

Post-census: remaining `#9CA3AF` text = 33 nodes, **all inside Disabled states or calendar Day
Cells** — the exempt set.

Correction made during the work: the primary Button variant's label was briefly rebound to
`Text/Secondary` in error and immediately restored to `Text/OnPrimary` (white). Net change: none.

## 4 · Button label typography (A3, revised)

The first attempt bumped only the Primary variant's label to 18.66px Bold for the WCAG large-text
exemption. That broke the type scale and left Outline/Destructive at 14px — three different button
label sizes in one file. **Replaced with a single rule:**

| # | Change | Before | After |
|---|---|---|---|
| C1 | Every Button label — all 4 variants of the `Button` set, all 41 instances, plus the 4 standalone auth buttons (Sign In, Create Account, Send Reset Link, Reset Password) | 18.66 Bold (Primary) · 14 Medium (Outline/Destructive) · 16–17 SemiBold (auth) | **16px Semi Bold, everywhere — 49 labels** |

16 SemiBold is the standard mobile button tier and sits cleanly between Body Large 16 and H3 20 in
the existing scale. Bottom-navigation labels stay at 12 Medium — a nav-label tier, not a button.

**Contrast position for CTA labels: white on `#E8622D` = 3.38:1, below AA for normal text — deliberate.**
No large-text exemption is claimed (16px SemiBold is not large text). The position rests on the
perception argument (contrast ratio is an approximation; white carries no hue distortion on a
saturated fill) plus five real usability participants, none of whom raised button legibility. Both
caveats must travel with the claim: the source's own evidence is preference survey, and its
low-ratio allowance is justified via large text, which this is not. Verified by screenshot: Sign In,
Review Booking.

Deliberately **not** changed: 12px chips, 10px selects, day cells, time slots, attendee presets and
similar tiny white-on-orange text — same documented position, and bumping them to 18.66px would
break every tile.

## 5 · Touch targets (A4)

| # | Change | Detail |
|---|---|---|
| T1 | `BACKUP / Select Date & Time (delete after verify)` deleted | `4923:4750` — a working artifact that alone carried 34 sub-44px interactive nodes |
| T2 | 21 header back-buttons | reaction moved from the 24×24 chevron to the `402×68` Header Bar instance — the tappable frame the rubric measures is now ≥44pt; behaviour unchanged (BACK/NAVIGATE actions preserved via `setReactionsAsync`) |

**Documented exceptions (not changed):** 60 Day Cells at 24×24 — that is the WCAG 2.5.8 AA floor,
and the 7-column calendar grid cannot take 44px cells without a redesign; 31 small content icons
(16–24px: attachment actions, accordion chevrons, pencil, bell) sit inside instance subtrees that
the plugin cannot restructure in dynamic-page mode. Report states both numbers honestly.

## 6 · Grid (A6)

27 frames received the layout grid (spec read from `Select Date & Time`: columns, 8px gutter, 16px
offset, orange at 10%). **34 of 34 screens now carry it.** Layout grids do not render into PNG
exports — a screens PDF will not show them unless the export enables grids.

## 7 · Caption node names (A7)

10 nodes renamed `Chonchanok / User` → `Chonchanok / Student` (node name only; characters were
already correct).

## 8 · Re-census (A8) — end of session

| Check | Result |
|---|---|
| Text rendering `#1A2340` | 0 |
| Text rendering `#9CA3AF` outside Disabled/Day Cell | 0 |
| Badge instance ↔ main mismatch | 0 |
| Screens with layout grid | 34 / 34 |
| Dead-end reactions (destination node missing) | **0** — 28 found and repaired, see §9 |

## 9 · Dead-end repair (same session)

A full reaction sweep found 28 actions pointing at deleted nodes — all `CHANGE_TO` variant swaps,
none on the happy path:

| Group | Count | Was | Now |
|---|---|---|---|
| Attachment action hover states (`Action 1/2` inside `Booking Summary Dropdown` variants and their instances) | 20 | ON_HOVER → deleted `4059:1572` | dangling hover targets removed — hover is desktop-only on a mobile prototype and the target variant no longer exists |
| Dropdown header toggles (`Booking Summary Dropdown`, `Documents Dropdown`) | 8 | ON_CLICK → deleted `4249:17031` / `4249:17465` (older duplicate sets) | retargeted to the surviving sibling variant — Collapsed⇄Expanded now toggles: `4336:15073`↔`4249:17076` and `4349:11055`↔`4249:17467` |

Post-repair verification: **0 reactions with a missing destination in the whole file.** The accordion
toggle is now functional feedback in the prototype — a Criterion 3 positive, not just defect removal.

---

## Measured contrast table (live hexes, 2026-10-11)

| Pair | Ratio | Verdict |
|---|---|---|
| Navy `#1B2A5B` on white | 13.74:1 | ✅ AAA |
| White on `#047857` (Available, Approved) | 5.48:1 | ✅ AA |
| White on `#C2410C` (Partial, Under Review) | 5.18:1 | ✅ AA |
| White on `#B45309` (Upcoming, Busy) | 5.02:1 | ✅ AA |
| White on `#4B5563` (Cancelled) | 7.56:1 | ✅ AAA |
| White on `#DC2626` (Rejected) | 4.83:1 | ✅ AA |
| `#6B7280` on white (secondary text, hint token) | 4.83:1 | ✅ AA |
| White on orange CTA `#E8622D`, label 16px Semi Bold | 3.38:1 | ⚠️ deliberate, defended |
| White on orange, small controls (chips/tiles) | 3.38:1 | ⚠️ deliberate, defended |
| Orange `#E8622D` button shape vs page — white / Neutral/50 `#F5F7FA` (WCAG 1.4.11, non-text) | 3.38:1 / 3.15:1 | ✅ AA |
| Orange `#E8622D` booking ID, 24px Bold, on white (large text) | 3.38:1 | ✅ AA large |
| Navy `#1B2A5B` on orange (unused fallback) | 4.07:1 | fails normal text |
| `#9CA3AF` on white (disabled only) | 2.54:1 | ✅ exempt |

**Deck warning:** the Canva deck currently claims `Navy (#1A2340) on White: 14.18:1`. Live navy is
`#1B2A5B` → **13.74:1**. Any slide still quoting 14.18, or `4.58:1` navy-on-orange, is quoting the
old navy and must be corrected.

---

*Feeds → [[uxui-build-handoff]] · Hub → [[uxui-facility-booking-project]] · Status → [[uxui-project-state]]*
