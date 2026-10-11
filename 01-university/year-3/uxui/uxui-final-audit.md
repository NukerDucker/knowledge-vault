---
title: "KMITL B-App — Final Prototype Audit & Presentation Plan"
tags:
  - university
  - group-work
  - project
status: active
subject: uxui
course: 01276545
---

# KMITL B-App — Final Audit & Presentation Plan

**Date:** 2026-10-07 · **Submission:** 07_10_2026 folder · **Group:** Napaul / Chonchanok / Mawin

---

## Screen Inventory (07_10_2026)

| Member | File | Screens | Role |
|---|---|---|---|
| Napaul | Authentication.png | 4 | Login, Sign Up, Reset Password ×2 |
| Napaul | Booking Flow.png | 7 | Select Date, Booking Details (empty+filled+error), Upload Docs ×2, Review, Confirmation |
| Napaul | Overlays.png | 5 | Notifications, Sort By sheet, Confirm Booking dialog, Cancel dialog, Confirm Edit dialog |
| Chonchanok | Home.png | 1 | Home dashboard |
| Chonchanok | Search Flow.png | 3 | ECC Building room list, Search Results, Filters |
| Chonchanok | Room Info.png | 5 | Room Detail (Details tab, Available), Room Detail (Reviews tab, Available), Room Detail (Details, Unavailable), Room Detail (Reviews, Unavailable), Map |
| Mawin | Booking History.png | 2 | Booking History Past, Booking History Upcoming |
| Mawin | Booking Details.png | 3 | Booking Detail (Approved), Booking Detail (Completed), Edit Booking |
| Mawin | Profile.png | 1 | My Profile |

**Totals:** Napaul 16, Chonchanok 9, Mawin 6 — all meet ≥5 minimum ✅

---

## Rubric Audit

### Criterion 1 — Frame Labeling & Screen Quota (5 pts)

- ✅ All frames labeled "Member / User" format
- ✅ All members ≥5 screens
- ✅ ≥3 full-function screens each
- ✅ ≥2 core screens each (Booking Details + Review / Room Detail + Search / Booking Detail + Edit)
- ✅ Data realism: real room photos, real IDs, real names, specific dates
- ✅ No Lorem ipsum

### Criterion 2 — Design System (5 pts)

- ✅ Orange **`#E8622D`** + navy **`#1B2A5B`** across all 3 members — read from the live file
  2026-10-09. Both hexes quoted in earlier versions of this note were wrong
- ✅ Bottom nav identical on all screens
- ✅ Status badge system consistent — colour + icon + text, all 10 variants
- ✅ Card and button styles match
- ✅ Components page exists in Figma (shared Design System)
- ✅ **Two components added 2026-10-09:** `Attendee Preset` (capacity-bounded attendee chips) and
  `Capacity Select`. Both are component sets with Default/Selected states
- ⚠️ **Two navies and two greens remain in the file** — `#1B2A5B` + `#1A2340`, and `#059669` +
  iOS `#34C759`. Low visual impact, but an examiner reading raw fills would catch it. Worth
  consolidating if time allows, and worth a one-line mention on the Future Work slide either way

### Criterion 3 — User Flow & Happy Path (5 pts)

Happy path confirmed:
```
Login → Home → Room Detail → Book Now → Select Date → Booking Details → Upload Docs → Review → Submit → Confirmation → View Booking Detail
```

Dead ends resolved:
- Filter → back to same search result ✅
- HM Building → ECC search result (prototype scope) ✅
- Request Edit/Cancel → back to edit page ✅
- All confirmation dialogs wired ✅

### Criterion 4 — Accessibility (5 pts)

> **Correction 2026-10-09.** This section previously claimed "white on orange buttons ~4.7:1 ✅ AA".
> That number was wrong — no orange in either palette reaches 4.7:1. Measured: 3.39:1 and 3.42:1.
> The old WCAG table also claimed the green badge passes AA; it does not.
> Verified numbers live in [[uxui-facility-booking-project#Contrast — verified numbers]].

**Passing now:**
- ✅ Status badges carry icon **and** text — never colour alone (WCAG 1.4.1)
- ✅ Form errors: warning icon + descriptive text, not a red border alone
- ✅ Navy / white pairings: 13.74–15.46:1, well past AA
- ✅ Orange as icon / border / accent: clears the 3:1 UI threshold

**Measured from the live file 2026-10-09** — fill census + component inspection, not estimates.
Live orange is `#E8622D`; **nobody's vault palette had it right.**

Failing — all normal-size text (largest style below Display is 16px, so **no pair qualifies for
the large-text exemption**; the 3:1 allowance covers non-text marks only):

| Pair | Ratio | Verdict |
|---|---|---|
| White on orange CTA label `#E8622D` | 3.38:1 | ❌ needs 4.5:1 |
| White on **Available** / **Approved** `#059669` | 3.77:1 | ❌ needs 4.5:1 |
| White on **Partial** / **Under Review** `#E8622D` | 3.38:1 | ❌ needs 4.5:1 |
| White on **Upcoming** `#D97706` | 3.19:1 | ❌ needs 4.5:1 |
| White on **Cancelled** `#9CA3AF` | 2.54:1 | ❌ needs 4.5:1 |
| `#848B96` on white (285 uses) | 3.43:1 | ❌ needs 4.5:1 |

**6 of 10 badge variants failed — including `Available` and `Approved`, the two most-used states.**

**Fix — Option A, 6 fill swaps + 1 label colour.** ⚠️ **Corrected 2026-10-09:** this was recorded as
"propagates to all 31 screens". **It did not.** The component set was recoloured but every live
instance kept an override carrying the old colour, so all 33 live badges still rendered the old
values. Repaired instance-by-instance — see [[uxui-usability-test#Improvement tracker]] row 46.
Verified after the repair: 0 mismatches on live screens. **Do not claim this fix on the strength of
the component set alone — the instances are where it either lands or does not.**

⚠️ **And the stroke was missed entirely.** Seven of ten variants kept a 1px stroke in the *old*
colour, so every recoloured badge rendered with a halo of its previous colour. The three variants
whose stroke matched were exactly the three whose fill never changed — which is what proves the
convention is `stroke = fill`. Repaired on the component set and on 62 instances. Final sweep:
65 badges, 0 mismatches. See row 47.

Option A was chosen over a tinted-bg pattern because text colour and layout stay untouched and all badges keep uniform white text.

| Variant(s) | Now | → | After |
|---|---|---|---|
| Available, Approved | `#059669` | **`#047857`** | 5.48:1 ✅ |
| Partial, Under Review | `#E8622D` | **`#C2410C`** | 5.18:1 ✅ |
| Upcoming | `#D97706` | **`#B45309`** | 5.02:1 ✅ |
| Cancelled | `#9CA3AF` | **`#4B5563`** | 7.56:1 ✅ |
| Busy | `#DC2626` | **`#B45309`** | 5.02:1 ✅ |
| Rejected | `#DC2626` | unchanged | 4.83:1 ✅ |
| Unavailable, Completed | `#6B7280` | unchanged | 4.83:1 ✅ |
| CTA label | white | **kept white — deliberate** | 3.38:1 ⚠️ |

**The CTA label stays white — this is a decision, not an oversight.** Navy `#1A2340` would give
4.58:1, but white-on-orange was kept after reviewing the argument in
[The Myths of Color Contrast Accessibility](https://uxmovement.com/buttons/the-myths-of-color-contrast-accessibility/):
contrast ratios are an approximation, and white on a saturated hue reads better than the math
suggests because white carries no hue or saturation. The article's own recommendation is to pair
ratios with user testing — and five usability participants, none of whom raised button
legibility, is that evidence.

**Two honest caveats to state if asked, rather than discovered:**
- The article's flagship example is white-vs-black on *blue*, and its evidence is preference
  surveys, not reading-performance testing.
- Its lower-ratio allowance is justified via large text (18pt / 14pt bold). Our button labels are
  **14px Medium** — *not* large text. So the position rests on the perception argument, not on the
  large-text exemption.
- If challenged, do **not** claim 4.58:1 for the button. Say 3.38:1, say why white was kept, and
  cite the participant evidence.

Because the label stayed white, the **34 Button instances, 17 standalone buttons and 39 Stepper
labels still carrying white text are now correct** and need no sweeping. Only badges were changed.

Colour + icon + text retained — the non-colour requirement is unaffected.
Fix detail and full measured table: [[uxui-facility-booking-project#Contrast — verified numbers]].

⚠️ **Apply after 2026-10-12.** `assets/ut/2026-10-10-prefix/after/08-room-detail-available.png` and `09-sort-sheet.png`
show badges; recolouring first makes the UT before/after pairs stale before that submission.

---

## Presentation Plan — exam-aligned (deadline 2026-10-19)

**Group = 3 members.** Group section 10 min (≤12 slides). Individual 5 min each (≤6 slides each).
Figma stays editable until the deadline, frozen after — so the contrast fix is live, not just a talking point.

**Speaking order follows the flow, not student number:** Chonchanok (browse) → Napaul (book) → Mawin (track).
That way the examiners see the user journey continuously.

### Group section — 10 min · 11 slides

| # | Slide | Covers |
|---|---|---|
| 1 | Title | KMITL B-App · Group 2 · 3 members |
| 2 | Problem statement + target users | 2 user types — student, staff |
| 3 | Persona 1 — "New", professor, 34 | Walks ECC to read door notices, still double-booked |
| 4 | Persona 2 — student | LINE request sits unread; no status signal |
| 5 | **Pain → feature map** | Which pain became which function, and where it sits in the UI |
| 6 | Sitemap / overall user flow | Week 9 sitemap |
| 7 | Role division | Chonchanok browse · Napaul book · Mawin track |
| 8 | Design system | Colours, fonts, key components |
| 9 | What makes us stand out | vs BU (status, no discovery) · RMUTL (discovery, onboarding wall) · Calendly (availability, no approval) |
| 10 | Conclusion | |
| 11 | Future work | Contrast fix shipped · auto-reopen cancelled slots · push notifications |

**Dropped from the earlier plan:**
- The 4-minute live demo — that is an **individual** requirement, not a group one.
- The AI Use Log slide — that is a **report** requirement, 1 page at the end of `GX_FinalReport.pdf`.

Do not re-walk the UX process. Only pain → feature → UI.

### Individual sections — 5 min each · 6 slides each

Shared skeleton:

| # | Slide |
|---|---|
| 1 | My task + all my screens |
| 2 | Live Figma demo, start → end of my task |
| 3 | Usability & accessibility — real contrast numbers, labels, touch targets |
| 4 | Confirmation / error prevention + empty & error state |
| 5 | UT summary — who, what broke, what changed |
| 6 | Before/After evidence |

#### Chonchanok — 9 screens — *find a room*

`Home.png` (Home dashboard) · `Search Flow.png` (ECC room list, Search Results, Filters) · `Room Info.png` (Room Detail Details/Reviews × Available/Unavailable, Map)

- **Demo:** Home → ECC list → Filters → Results → Room Detail (both tabs, both states) → Map
- **A11y:** Available/Unavailable chips are colour + text ✅. Map floor pills are **24px** — meets the WCAG 2.5.8 AA floor (24), under the 44px comfort target. Say both numbers; the honest version scores.
- **States:** Unavailable variant suppresses Book Now ✅ · **no zero-results empty state** → build
- **UT:** Nhow → 0px clearance under the sticky Book Now bar (fixed, padding 0→104) · Putt → bare numerals 1–7 on the map (now 1F–7F) · Nhow → sort had no asc/desc (new Sort Direction component)
- **Before/After:** tracker rows 13, 14, 15

#### Napaul — 16 screens — *complete a booking*

`Authentication.png` (4) · `Booking Flow.png` (7, S6–S10) · `Overlays.png` (5 — including Sort By sheet)

- **Demo:** Login → Home → ECC603 → Book Now → S6 → S7 → S8 → S9 → confirm sheet → S10
- **A11y:** corrected contrast table ([[#Criterion 4 — Accessibility (5 pts)]]) · CTA 42px → 55px for touch · bottom nav removed mid-wizard
- **States:** capacity inline error "Exceeds room capacity (40 seats)" · empty Booking Details · confirm booking / cancel / confirm-edit dialogs
- **UT:** Putt → confirmation didn't read as a confirmation · Mind → slider drag swallowed by a `destinationId: null` reaction
- **Before/After:** tracker rows 1–12 + 16

#### Mawin — 6 screens — *track and manage a booking*

`Booking History.png` (Past, Upcoming) · `Booking Details.png` (Approved, Completed, Edit Booking) · `Profile.png`

- **Demo:** Bookings tab → Upcoming → Detail Approved → Edit Booking → Cancel sheet → History
- **A11y: his screens carry every failing badge** — Approved / Pending / Completed / Cancelled. Green 3.41, amber 2.22. The colour fix lands mostly in this section.
- **States:** Cancel sheet (Keep vs Request were indistinguishable — both inherited one `CLOSE`) · Edit confirm ✅ · **no empty booking-history state** → build
- **UT:** Mind → "Request Edit" carried `CLOSE`, so confirming did nothing; both cancel buttons identical; Profile dead links
- **Before/After:** tracker rows 17–22

### Build before the deck — 2 frames

| # | Screen | State | Owner |
|---|---|---|---|
| 1 | Search Results | Zero-results empty state (filters match nothing), copy offers "clear filters" | Chonchanok |
| 2 | Booking History | Empty state (no bookings yet), copy routes to Home to start one | Mawin |

Both are direct exam asks — "the empty state and error state of your task" — and are cheap.
Build them so every member answers slide 4 with a real screen rather than a dialog substitute.

### Contrast fix — timing

Apply the two component edits in [[#Criterion 4 — Accessibility (5 pts)]] **after 2026-10-12**,
so the UT before/after pairs stay valid for that submission.

---

## AI Use Log (report — 1 page, last page of `GX_FinalReport.pdf`)

| # | Tool | Used for | Level | What changed + why | Member |
|---|---|---|---|---|---|
| 1 | Claude | Researched component naming conventions, identified where to source UI components, recommended icon choices for Components page | Green | Used AI suggestions as reference only; final component selection, naming, and icon decisions made by team | Napaul |

**Note:** Green-level = AI as research/reference tool. No Before/After slides required.
If no AI beyond the above, the brief's alternative is the single line "No AI used."

---

## Color Reference

| Token | Hex | Usage |
|---|---|---|
| Primary Orange | #E86027 | CTAs, active nav, selected states |
| Navy | #1A2340 | Headings, body text, labels |
| Green | #2E9E5B | Approved badge |
| Red | #E03535 | Rejected badge, errors |
| Yellow/Amber | #E8A020 | Pending badge |
| Grey | #8C8C8C | Cancelled badge, inactive |

---

*Hub → [[uxui-facility-booking-project]] · Status → [[uxui-project-state]] · Evidence → [[uxui-usability-test]]*
