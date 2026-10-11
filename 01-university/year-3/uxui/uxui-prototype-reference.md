---
title: "KMITL B-App — Hi-fi Prototype Reference (2026-10-06)"
tags:
  - university
  - project
status: stable
subject: uxui
course: 01276545
---

> **Scope.** The hi-fi prototype specification as it stood on **2026-10-06**, lifted out of
> [[uxui-facility-booking-project]] to keep the hub navigable. It was superseded in part by the
> 2026-10-10 fix batch — sixteen fixes, node ids in [[uxui-prototype-buglist-2026-10-10]]. Read that
> buglist before trusting any node id below. Overall status: [[uxui-project-state]].

## Hi-fi Prototype — Final Submission (2026-10-06)

**Figma file:** "UX/UI 2026 — KMITL-BApp" · fileKey `bhuuET1PKmzZSGMkVr2de7` · page "Screens"  
**Status: ✅ Complete and submitted**

### Rubric (Part 2 — 20 pts, graded from Figma file)

| Criterion | Weight | Status |
|---|---|---|
| Screen Elements, Layout & Real Data | 5 (individual) | ✅ All screens have real data, consistent spacing |
| Consistency & Design System | 5 (group) | ✅ Variables, components, text styles applied file-wide |
| Defined User Flow | 5 (group) | ✅ Core Task S6→S10 wired; overlays connected; all 15 Chonnanok/Mawin screens verified connected |
| Usability & Accessibility | 5 (individual) | ⚠️ WCAG AA contrast — verify manually for presentation slides |

**Min screen count:** 5/person, ≥3 full-function, ≥2 core, supporting max 2 toward quota.

### Screen inventory (final, 2026-10-06)

**Napaul / User — 16 screens**

| Section | Screens |
|---|---|
| Authentication | Sign In, Sign Up, Forgot Password, Reset Password |
| Booking Flow | Select Date & Time, Booking Details (Empty/Filled), Upload Documents (Empty/Uploaded), Review Booking, Booking Submitted |
| Overlays | Notification, Sort Sheet, Confirm Sheet, Cancel Sheet, Action Confirm Sheet |

**Chonnanok / User — 9 screens**

| Section | Screens |
|---|---|
| Discovery / Home | Home |
| Discovery / Search Flow | Search Results, Search Results - Empty, Filter |
| Discovery / Room Info | Room Detail (Available/Unavailable/Fully Booked/Review/Unavailable Review), Map |

**Mawin / User — 6 screens**

| Section | Screens |
|---|---|
| Booking History | Booking History - Past, Booking History - Upcoming |
| Booking Details | Booking Detail - Approved, Booking Detail - Completed, Edit Booking |
| Profile | Profile |

### Figma file structure (final)

- **Page "Screens":** All screens inside top-level "Screens" section → subsections named `Person / User / Section Name` (e.g. `Napaul / User / Booking Flow`)
- **Page "Components":** UI Components (left) · Icons Used in Screens + Design Tokens + Lucide Library (right column)
- **Name labels:** Attribution frame inside each screen frame, positioned below screen content (y = screen height + 16px, centered), visible on canvas
- **Sections layout:** Auth → Discovery Flow → Booking Flow → Booking History/Details/Profile → Overlays (all within parent "Screens" section)

**Brand palette:** orange #E8621D · navy #1B2A5B · white #FFFFFF · bg #F0F2F5  
**Rule:** navy = text only, NEVER as surface/background  
**Status colors:** green #059669 · amber #D97706 · red #DC2626 · grey #6B7280

### AI Use Log (for PDF submission — 1 page at end)

**Print-ready artifact:** https://claude.ai/artifact/DRyeDWrBR9kZ3ZZ6T56eEZ — open → Cmd+P → Save as PDF → append to submission

All AI use was Green level. No Before/After required.

**Declaration statement (Napaul-voice):**
> As someone who participated in this project from start to finish, I can confirm that AI tools were used only to help with naming and organizing components, as well as for background research on design standards and user flows. By Using Figma throughout the process, the team handled all actual screen design and prototype wiring without AI making any of the design decisions. This approach ensured that all choices came from the team's own understanding of the user needs and project requirements.

| # | Tool | Used for | Level | What changed + why | Member |
|---|---|---|---|---|---|
| 1 | Claude | Renaming: layer names, component names, screen names to consistent readable conventions | Green | Reviewed and adjusted all names by team before applying | Napaul |
| 2 | Claude | Organization: grouping screens into logical sections in Figma | Green | Team directed the grouping structure and section names | Napaul |
| 3 | Claude | Research: reviewing UX patterns and checking completeness of booking flow screens | Green | Team verified findings against actual design decisions | All |

### Resolved issues (sessions 2026-09-28 → 2026-10-06)

- ✅ All brand violations fixed (navy surface → amber for status badges)
- ✅ S1: HM Building second card added
- ✅ S4: Equipment labels correct; Book Now CTA added; Unavailable variant built
- ✅ S9: "Upcoming" badge amber (Status/Pending variable)
- ✅ Auth screens: Sign In / Sign Up / Forgot Password / Reset Password
- ✅ Notification overlay, Sort Sheet, Confirm Sheet, Cancel Sheet, Action Confirm Sheet
- ✅ All 9 CTA buttons replaced with Actions/Button component instances
- ✅ All remote Lucide icons replaced with local components (52 local, 0 remote)
- ✅ All component sets renamed (strip prefix — "Actions/Button" → "Button")
- ✅ All screen frames renamed (clean Title Case)
- ✅ Prototype flow wired: S6→S7 Filled→S8 Uploaded→S9→Confirm Sheet→S10→S12 Approved
- ✅ Name labels (attribution) under every frame: `Person / User`
- ✅ File organized for presentation: sections per owner, screens in flow order

### Contrast — verified numbers

> Recomputed 2026-10-09 with the WCAG 2.x relative-luminance formula — exact, not estimated.
> The table that stood here was wrong in both directions: it understated several pairs and
> **claimed the green badge passed AA, which it does not.** Superseded artifact link removed;
> do not present the old table.
>
> ✅ **Palette resolved 2026-10-09** by reading the live file (key `bhuuET1PKmzZSGMkVr2de7`)
> through the Figma bridge — a fill census across all three sections, not a guess.
>
> **Neither vault palette was correct.** Live orange is **`#E8622D`** — a third value, matching
> neither `#E8621D` (10-06 note) nor `#E86027` (10-07 note). Navy exists as **two** colours in the
> file. The old columns are deleted; the numbers below are measured.
>
> ⚠️ **No large-text exemption anywhere.** Text styles run 10 / 11 / 12 / 14 / 16px, plus a single
> 24px Display. WCAG large text starts at 18.66px bold, so **every** pair below is normal text and
> needs 4.5:1. The 3:1 UI allowance applies only to non-text marks — icons, borders, indicators.

*Text and UI pairs, measured:*

| Pair | Where used | Ratio | Verdict |
|---|---|---|---|
| `#111827` on white | Default body text | 17.74:1 | ✅ |
| Navy `#1A2340` on white | Headings | 15.46:1 | ✅ |
| Navy `#1B2A5B` on white | Headings, nav, body | 13.74:1 | ✅ |
| White on navy `#1B2A5B` | Nav active, header | 13.74:1 | ✅ |
| `#6B7280` on white | Caption / placeholder | 4.83:1 | ✅ |
| `#787878` on white | Stepper inactive | 4.42:1 | ❌ marginal |
| `#848B96` on white | Secondary label (285 uses) | 3.43:1 | ❌ |
| White on orange `#E8622D` | **Primary CTA label** | 3.38:1 | ❌ |
| Orange `#E8622D` on white | Active tab, icons | 3.38:1 | ❌ text · ✅ UI |
| Orange `#E8622D` on `#F5F7FA` | Active tab on app bg | 3.15:1 | ❌ |
| `#9CA3AF` on white | Muted / disabled | 2.54:1 | ❌ |
| White on `#34C759` | iOS green accent | 2.22:1 | ❌ |
| White on `#FFD60A` | iOS yellow accent | 1.41:1 | ❌ worst in file |

*Status Badge — all 10 variants, all 12px white text, all needing 4.5:1:*

| Variant | Label | Fill | Ratio | |
|---|---|---|---|---|
| `Status=Busy` | Busy | `#DC2626` | 4.83:1 | ✅ |
| `Status=Rejected` | Rejected | `#DC2626` | 4.83:1 | ✅ |
| `Status=Unavailable` | Unavailable | `#6B7280` | 4.83:1 | ✅ |
| `Status=Completed` | Completed | `#6B7280` | 4.83:1 | ✅ |
| `Status=Available` | Available | `#059669` | 3.77:1 | ❌ |
| `Status=Approved` | Approved | `#059669` | 3.77:1 | ❌ |
| `Status=Partial` | Partial | `#E8622D` | 3.38:1 | ❌ |
| `Status=Reviewing` | Under Review | `#E8622D` | 3.38:1 | ❌ |
| `Status=Upcoming` | Upcoming | `#D97706` | 3.19:1 | ❌ |
| `Status=Cancelled` | Cancelled | `#9CA3AF` | 2.54:1 | ❌ |

**6 of 10 badge variants fail — including `Available` and `Approved`, the two most-used states.**

**Four colour collisions** — one colour, two meanings, distinguishable only by the label text:
`Busy` ≡ `Rejected` · `Available` ≡ `Approved` · `Partial` ≡ `Reviewing` · `Unavailable` ≡ `Completed`.
Cheesy misread ECC-608 as "broken / on maintenance" because `Busy` is red like `Rejected`.

**Post-fix targets — Option A: darken the fills, keep white text.** Chosen over a tinted-bg
pattern because it is **6 fill swaps and nothing else** — no text colour changes, no layout
changes, and all 10 badges keep uniform white text.

| Variant(s) | Now | → Fill | Ratio after |
|---|---|---|---|
| Available, Approved | `#059669` 3.77 ❌ | **`#047857`** | 5.48:1 ✅ |
| Partial, Under Review | `#E8622D` 3.38 ❌ | **`#C2410C`** | 5.18:1 ✅ |
| Upcoming | `#D97706` 3.19 ❌ | **`#B45309`** | 5.02:1 ✅ |
| Cancelled | `#9CA3AF` 2.54 ❌ | **`#4B5563`** | 7.56:1 ✅ |
| Busy | `#DC2626` 4.83 ✅ *but reads as broken* | **`#B45309`** | 5.02:1 ✅ |
| Rejected | `#DC2626` 4.83 ✅ | unchanged | — |
| Unavailable, Completed | `#6B7280` 4.83 ✅ | unchanged | — |

**CTA label:** white → **`#1A2340`** on orange `#E8622D` = **4.58:1 ✅**.
Do **not** use `#1B2A5B` here — on this orange it measures **4.07:1 and fails**. Use `#1A2340`
(4.58) or `#111827` (5.25).

**Semantic fix, separate from contrast.** `Busy` moves to amber, which also retires the
`Busy` ≡ `Rejected` collision. Sharing amber with `Upcoming` is deliberate — both mean "not
available to you right now". Red is reserved for terminal negative states (`Rejected`). This is
the direct answer to cheesy's "ECC-608 seems unusable / on maintenance".

**Slide talking points — corrected:**
- Navy and white pairings pass comfortably (13.7–15.5:1); `#111827` body text at 17.74:1
- Orange clears 3:1 as an icon / border / accent colour. It is **not** used for body text
- **Every** text pair in the file needs 4.5:1 — the largest text style below Display is 16px, so no pair qualifies for the large-text exemption. Say this plainly if asked; it is the honest answer and it holds up
- 6 of 10 badge variants failed, including the two most-used positive states
- Worst pair in the file was white on `#FFD60A` at 1.41:1
- Fix is 6 fill swaps plus one label colour. If it has not landed by exam day, present it on Future Work instead of defending the old number

### Pending (before exam — deadline 2026-10-19)

- ✅ Prototype dead ends verified — all 15 Chonnanok/Mawin screens have NAVIGATE reactions (on inner Screen frames); core task flow works end-to-end (2026-10-06)
- ⚠️ AI Use Log: export as PDF, append as the last page of `GX_FinalReport.pdf`
- ✅ **Badge contrast fixed 2026-10-09** — 7 of 10 variants recoloured, applied live. CTA label
  deliberately left white; reasoning and the two caveats are in
  [[uxui-final-audit#Criterion 4 — Accessibility (5 pts)]]. **Say 3.38:1 for the button if asked,
  never 4.58:1.**
- ⚠️ **The badge recolour did not reach the screens on its own.** The `Status Badge` component set
  was correctly recoloured weeks ago, but every live instance kept an override holding the old
  value — so all 33 live badges still rendered `#059669`/`#DC2626`/`#D97706`/`#E8622D`/`#9CA3AF`
  until 2026-10-09. Repaired instance-by-instance, plus 33 in the RT device matrix. Re-verified:
  0 mismatches on live screens. **General rule this took two passes to learn: in this file, a
  component-set edit changes nothing on screen until the instances are dealt with too.**
  See [[uxui-usability-test#Improvement tracker]] row 46.
- ✅ **Attendee control rebuilt 2026-10-09** — the 2-variant Slider is gone from Booking Details
  (empty + filled) and Edit Booking, replaced by `Attendee Preset` chips bounded by room capacity.
  The fake `capacity-warning` label was deleted from all 5 copies, and ECC-603's capacity was
  normalised to 40 across Home, Search Results, Room Detail and the booking flow.
- ✅ **Palette resolved** from the live file: orange `#E8622D`, navy `#1B2A5B`. See
  [[#Contrast — verified numbers]].
- ℹ️ `assets/ut/2026-10-10-prefix/after/08-room-detail-available.png` and `09-sort-sheet.png` predate the badge recolour,
  so the UT deck and the live prototype differ slightly in badge colour. They still document their
  own improvements accurately. Not treated as a blocker.

### Remaining Figma fixes — resume list

Open items from the 2026-10-09 fix round, roughly highest value first. Detail and owner for each
is in [[uxui-usability-test#Improvement tracker]] (rows 24–35, 37–41).

> **A second fix round ran 2026-10-10** against a teammate's fresh bug list —
> 13 Figma fixes plus component-set and prototype-link repairs. That list, what
> was changed, and a verification audit of every item live in
> [[uxui-prototype-buglist-2026-10-10]]. Read that note before re-checking
> anything below; several rows here were re-verified there.

| # | Fix | Where | Owner |
|---|---|---|---|
| 1 | ~~Microsoft sign-in opens a live OAuth session~~ — **this was wrong**, see below. Fixed 2026-10-09 | `Authentication.png` | Napaul ✅ |
| 2 | ~~Sort By sheet + Notifications trap the user~~ — **fixed, and the scope was five overlays, not two.** Every overlay trigger restored `NAVIGATE → OVERLAY`; see [[uxui-usability-test#Improvement tracker]] row 43 | Overlays | Napaul ✅ |
| 3 | ~~Confirm Booking dialog — Back does not return~~ — **fixed by the same change.** `Go Back` carried `CLOSE`, which is a no-op outside an overlay; restoring `OVERLAY` makes it live | Overlays | Napaul ✅ |
| 4 | **Busy / Unavailable vocabulary** — ECC-608 reads `Busy` in Search, `Unavailable` in Room Detail, and the "Busy until 15:00" time is dropped on the detail screen | Search → Room Detail | Chonchanok |
| 5 | **Book Now gating differs by tab** — works on an Unavailable room from Details, dead on Reviews | Room Detail ×4 | Chonchanok — **re-checked 2026-10-10: the Details tab is now greyed out (properly disabled), but both Review screens still render Book Now as a full-colour `#E8622D` CTA with no reaction.** Intent unresolved: this row says "fix the dead Reviews button", while the team separately reports the booking option was *deliberately* disabled on both tabs. Decide which, then either mute the Review CTA or wire it. See [[uxui-prototype-buglist-2026-10-10#Verification audit — 2026-10-10]] |
| 6 | **Reviews submittable on rejected and cancelled bookings** | Booking Details | Mawin |
| 7 | **Booking History empty state** — the only empty state actually missing. `Search Results - Empty` already exists | Booking History | Mawin |
| 8 | ~~`+` control overlaps the booking details area~~ — **already gone.** The `+` was the attendee stepper, removed by the `Attendee Preset` rebuild ([[uxui-usability-test#Improvement tracker]] row 36). A page-wide scan finds only two other `+`-ish elements — the Upload Documents row icon (correctly inside its own 370px card, checked at 2×) and two "Add to Calendar" labels — neither overlapping anything | S7 | Napaul ✅ |
| 9 | **Booking History scroll position not reset** on entry from Review / Upcoming | Booking History | Mawin |
| 10 | ~~Stepper connector line renders ahead of the current section~~ — **fixed on all 6 live steppers.** The file was internally consistent, not off-by-one; flipped from convention A to convention B, plus the 1px orange nubs are gone. Full reasoning in [[uxui-usability-test#Improvement tracker]] row 44. **Row 45 (label drift) is also fixed — steppers only**, to two colours; see row 45a. The full-file palette call in item 13 is still open and this does not pre-empt it | Booking Details | Napaul ✅ |
| 11 | **Slideshow: drag vs tap inconsistent; drags behind the room card** | Room Detail | Chonchanok |
| 12 | **Home profile avatar does not route to Profile** | Home | Chonchanok |
| 13 | **Consolidate the two navies and two greens** (`#1B2A5B`+`#1A2340`, `#059669`+`#34C759`). **Scope grew 2026-10-09** — the stepper labels alone add `#111827` and `#000000`, so the file really carries **four** dark text colours, not two. One decision fixes items 13 and 45 together | Components | design system |

### Grid export limitation — 2026-10-10

Layout grids never reach an export. The plugin's `exportAsync` and the REST image endpoint both
return the design without them, verified by pixel measurement on 2026-10-10. The "set
`visible: true` for export" step in [[uxui-exam-task-split]] does not achieve what it claims. A
screen that must show the grid needs either a plugin drawn overlay or the reconstruction method in
`~/Code/ut-export/`, which matches Figma's own rendering to the pixel. Separately, the seven frames
in `Napaul / User / Booking Flow` now carry `layoutGrids.visible: true`, which changes nothing in an
export. See [[uxui-usability-test#Status — 2026-10-10]] for the measurement detail.

### Figma node index

File **`UX/UI 2026 — KMITL-BApp`**, key `bhuuET1PKmzZSGMkVr2de7`. Pages: `Wireframe` `0:1` ·
`Components` `4054:84` · `Screens` `4054:85`.

**Components page** — sections `Lucide Icon Library (hidden)` · `UI Components` ·
`Icons — Used in Screens` · `Design Tokens` · `Sort Direction`.

| Thing | Node |
|---|---|
| Section: Buttons & Actions | `4498:9366` |
| `Button` set (12 variants) | child of `4498:9366` |
| Section: Status & Progress | `4498:9369` |
| `Status Badge` set (10 variants) | child of `4498:9369` |
| `Chip` set (23px → 28px) | `4498:10045` |
| `Filter Select` set (reverted, no chevron) | `4293:9732` |
| `Capacity Select` set (new, has chevron) | `4848:9915` |
| `Attendee Preset` set (new) | `4848:9805` |
| `Slider` set (the 2-variant one) | `4293:8483` |
| `Lucide / chevron-down` icon | `4647:10569` |

**Screens page** — key screens: `Home` `4673:10496` · `Search Results` `4673:10451` ·
`Room Detail - Available` `4673:10466` · `Filter` `4673:10441` · `Booking Details - Empty`
`4673:10425` · `Booking Details - Filled` `4673:10426` · `Edit Booking` `4673:10431` ·
`Booking History` `4673:10433`-range · RT device matrix section `4781:7939`.

> **File has no paint styles and no variables** — every colour is a raw fill. Read fills off
> nodes directly. Plugin API notes: use the `…Async` getters (`getNodeByIdAsync`,
> `getLocalPaintStylesAsync`) — the sync ones throw under `documentAccess: dynamic-page`. Text
> nodes can have `figma.mixed` as `fills`, which is not an array — guard with `Array.isArray`
> before `.find`. Instances reject `appendChild` from a foreign component; make a new component
> instead. A script that throws mid-way still applied the mutations before the throw — verify
> state, don't blindly re-run.

> **Reaction writes — three traps, all hit on 2026-10-09.** Use `node.setReactionsAsync([...])`;
> the plain `reactions` setter throws `Cannot call with documentAccess: dynamic-page`. The write
> payload must contain **only** `trigger` and `actions` — reading a reaction back also returns a
> legacy read-only `action` (singular) alias alongside `actions`, and passing that object
> straight back is rejected as `Reaction at index 0 was invalid`. Most importantly: **a `NAVIGATE`
> destination must be a direct child of a section or of the page.** A frame nested inside another
> frame is refused with *"destinations must be a different top-level frame on the same page"*.
> This file's older reactions (e.g. the original `SSO Microsoft`) point at inner `Screen` frames
> and still exist in the file, but **new writes to that same destination fail** — so "it already
> works elsewhere in the file" is not evidence the shape is writable. Navigate to the section
> child (`Home` `4673:10496`), not its `Screen`.

> **`Frame 14` `4777:7085` is a hidden workbench, not an orphan.** 9161×905 at (477, −1259),
> `visible: false`, overlapping no section. It holds scratch copies of several screens including
> a second Sign In whose SSO buttons still point at the inner `Screen` destination. Harmless
> while hidden — but if it is ever unhidden, note its SSO behaviour differs from the live screen.

### Decisions log

[[uxui-decisions-log]] — every design decision with its reasoning, illustrated with 54 project
images in `assets/decision/`. Written as the source for `GX_FinalReport.pdf`. Start there when
preparing an answer to an examiner's question about *why* a screen looks the way it does.

### Exam task split

[[uxui-exam-task-split]] — who does what: Nuker (book), Name/Chonchanok (browse), Noey/Mawin
(track). Carries the shared grid standard, the 93-frame touch-target audit broken down by owner,
each member's open fixes, and the list of UT evidence each can draw on.

### Still outstanding outside Figma

- ⚠️ **Draft the 2nd persona** (student). The group exam section requires two; only "New" exists in [[uxui-week4-user-journey-map]].
- ⚠️ **AI Use Log** — export as PDF, append as the last page of `GX_FinalReport.pdf`.
- ⚠️ **Deliverables not yet built:** `GX_FinalReport.pdf`, `GX_FinalPresentation.pdf`. Slide outline in [[uxui-final-audit]].
- ⚠️ Building the fixes above will add rows to [[uxui-usability-test]] and pairs to `assets/ut/` — capture before/after for each, as rows 36–41 do.

---

*See also: [[uxui-facility-booking-project]] · [[uxui-prototype-buglist-2026-10-10]] · [[uxui-project-state]]*
