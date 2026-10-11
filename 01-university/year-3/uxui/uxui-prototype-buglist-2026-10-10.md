---
title: "UX/UI Prototype Bug List — 2026-10-10"
tags:
  - university
status: active
subject: uxui
course: 01276545
updated: 2026-10-11
---

# Prototype Bug List — 2026-10-10

Teammate report against the live prototype. File `UX/UI 2026 — KMITL-BApp`, key
`bhuuET1PKmzZSGMkVr2de7`.

Related: [[uxui-facility-booking-project]] · [[uxui-usability-test]] ·
[[uxui-exam-task-split]]

## New

**Functionality**

- Can't select attendees count
- Attendees for ECC-603 is fixed to 20 people, task 1/2 requires 40
- Can't use Map from in ECC-603 room details, from Home or Search; other
  busy/unavailable rooms can

**Visuals**

- Checkmark in Booking Details from after booking or using Booking History is
  brokenly large
- Rebooking for ECC-603 after successful booking has date bubble and review
  bubble on, process works fine

**Details**

- Can press booking stage bubble to later stages, does nothing, doesn't draw
  lines when pressed, works fine after continuing through process
- Edges in Booking History are rough
- ECC-603 in Booking Details after booking is ECC-601, 20 from 40 people
- Bookings → ECC-603 → Edit → attendees fixed to 20, mismatch from task 40
- Clickable file upload buttons in booking from Booking Details or during
  booking, clicking collapses Booking Summary
- Bookings → any booking → booking pencil button purpose

## Unfixed

**Functionality**

- Can submit review for rejected/cancelled booking
- Can't book room with ongoing session

**Visuals**

- Booking History scrollbar not reset after viewing booking and going back to
  Booking History

## Fixes applied

### 2026-10-10 — session 1

| # | Item from list | Node(s) | Change | How verified |
|---|---|---|---|---|
| 1 | *Attendees for ECC-603 is fixed to 20, task 1/2 requires 40* | `4848:9818`, `4848:9827` (chip `20` → Default)<br>`4848:9822`, `4848:9831` (chip `40` → Selected) | Moved the `Selected` state from the 20 chip to the 40 chip on Booking Details - Filled and Edit Booking | Screenshot: `40` renders selected. File scan: no `20 people` left on Screens |
| 2 | *ECC-603 in Booking Details after booking is ECC-601* | `I4489:8037;4464:7082`<br>`I4651:8446;4464:7082` | `ECC-601` → `ECC-603` | Scan of Screens page: zero `ECC-601` remaining |
| 3 | *20 from 40 people* (post-booking screens + Review Booking) | `I4489:8072;4464:7082`<br>`I4651:8450;4464:7082` | `20 people` → `40 people` | Same scan |
| 4 | *Checkmark in Booking Details is brokenly large* | `I4364:10386;4336:17775;4336:14585` | `resetOverrides()`. The icon had been overridden to `layoutSizingHorizontal=FILL` inside a HUG parent — the badge ballooned to **79×75** and its label was deleted. Now **79×24** with its `Upcoming` label restored | Screenshot: badge sits inline, no longer covering the room card. Shrinking it also revealed the previously-hidden `Edit booking` button |
| 5 | *Bookings → any booking → booking pencil button purpose* | `I4364:10383;4409:10397` | Wired `ON_CLICK → NODE 4673:10431 NAVIGATE` (Edit Booking) | Reaction read back; destination resolves to `Edit Booking`, parent type `SECTION` |
| 6 | *Can press booking stage bubble to later stages, does nothing, doesn't draw lines* | 6 × `Stepper State` bubbles inside the `Stepper` variants (`4205:11133`, `4205:11116`, `4205:10580`, `4205:11042`, `4205:9935`, `4205:9805`) + 1 stray on `Stepper State/State=Default` (`4205:9611`) | Cleared every `ON_CLICK → CHANGE_TO State=Active` reaction. The stepper is now a pure progress indicator and the half-lit state is unreachable | All 8 stepper instances re-scanned: **0 reactions** remaining |
| 7 | *Can't select attendees count* | New component set `Attendee Selector` (`4900:11231`), 5 variants `Count=None/10/20/30/40`; swapped onto `4900:11249` (Filled), `4900:11258` (Empty), `4900:11267` (Edit Booking) | Rebuilt the chip row as one variant-driven component, replacing the three raw `Preset Row` frames | Each variant verified to light exactly its own chip; screens verified by screenshot and by reading back the selected chip |
| 8 | *File upload buttons collapse Booking Summary* | `4336:15073`, `4249:17076` (Booking Summary Dropdown), `4336:14835`, `4336:14952` (Room Summary Dropdown) | The `CHANGE_TO` sat on the **variant root**, so any click inside the 368×416 instance — including on a file row — fired the accordion toggle. Moved the reaction onto the 344×32 `Dropdown Header` in all four variants | Live instance `4528:7618` reads root reactions **0**, header → Expanded. Three file-upload entries were also dead-coded per the earlier sweep |
| 9 | *Can't use Map from ECC-603 room details* | `I4550:23433;4550:23385` (Available), `I4550:23475;4550:23427` (Review) | Both `Moleculs - Navbar` frames had **zero reactions** while their Unavailable counterparts navigated to `4859:5846`. Wired both to the canonical Map | Cross-check of all four Room Detail screens: every Map-labelled navbar now resolves to `4859:5846` |
| 10 | *Rebooking shows date + review bubbles already on* | — | **Resolved by fix 6.** The only way to light arbitrary bubbles was clicking them; with the stepper reactions stripped, no component state can produce that combination | All 8 steppers audited: each shows a consistent cumulative fill (1 / 1-2 / 1-2-3 / 1-2-3-4) |
| 11 | *Can't select attendees count* — click wiring | 20 chip reactions across the 5 `Attendee Selector` variants; live on `4900:11249`, `4900:11258`, `4900:11267` | Each chip fires `ON_CLICK → CHANGE_TO` the variant in which **that** chip is selected, so the click changes the enclosing `Attendee Selector` instance, not just the chip. See correction below — the earlier "not expressible" conclusion was wrong | Booking Details - Empty has all four chips wired (any choice reachable); Filled and Edit Booking have 10/20/30 wired with 40 already selected. Clicking a selected chip is a deliberate no-op |
| 12 | *`4059:155` nested `NAVIGATE` destination* | **81 reactions** across every Screens-page flow | Swept the whole file, not just `4059:155`. Every `NAVIGATE` whose destination was a frame nested inside another frame was repointed to its top-level ancestor on the same page | Re-scan after the write: **0 nested destinations remain**; 81 fixed, 0 failed |
| 13 | Booking Details fields should fill on click | `4489:8943`, `4489:9030` (Text Input, Empty) → `4896:11011`; `4197:7109` (Select) → `4507:10436` | Added a `Value` TEXT property to the `Text Input` set, bound **only** in the `State=Filled` variant so the Empty state keeps its own placeholder. Clicking either field changes it to `State=Filled` carrying that field's text; the Purpose dropdown changes to `State=Default` carrying `Education` | All three read back with the right property, placeholder text while Empty, and the correct reaction. The four already-placed Filled instances were re-set explicitly because the new property's default (`Junior Orientation`) would otherwise have overwritten both note fields |
| 14 | Room cards should open the matching room state | `4585:4648` — **superseded by 15** | First treated as a genuine card: corrected its Floor `0` → `6` and repointed it from Unavailable to Available. It was subsequently identified as a malformed stray and removed entirely (fix 15) | The sweep run during fix 14 still stands and is the useful result: **no other card carries Floor 0**, and **zero routing mismatches** exist. Routing was already correct everywhere — ECC-604/605/606 and ECC-501/608/609 (Busy) → Unavailable; ECC-603 and the Home cards (Available) → Available |
| 15 | Search Results - Empty page data | Removed stray `4585:4648` | That card was **malformed**, not a design choice: **287×114** against 370×116 for every real card, a plain `FRAME` rather than an instance of `Cards/Room Card`, its chevron `visible: false` and positioned *outside* its own bounds, no `image 1` rectangle, and it sat at y=2910 mostly **behind the bottom nav**. It also duplicated ECC-603, already the first card | After removal: **4 cards, all 370×116, zero duplicate rooms**, matching the page's own "4 rooms found" header. No empty stray frames left; screenshot confirms |

| 16 | Room naming + screen title inconsistency | Three text nodes on Search Results - Empty (`I4585:4593;4336:14098`, `I4528:5816;4336:14258;4336:14098`, `I4585:4554;4336:14098`); title `I4349:10006;4190:5713` | Applied the plain `ECC-###` convention: `Co-working (ECC-606)` → `ECC-606`, `(ECC-605)` → `ECC-605`, `(ECC-604)` → `ECC-604`. Title corrected from singular `Search Result` to `Search Results` | Re-scan: no parenthesised room names remain anywhere, and all **35** room-name texts on the Screens page now use plain `ECC-###`. Screen title reads `Search Results` |

> **How this one was nearly mis-diagnosed.** Fix 14 treated the same node as a
> genuine card and "corrected" its floor and destination. It is in fact an
> invisible-in-practice stray: at 0.43× in a whole-section export it does not
> read as a card at all, and exporting it **alone renders blank**. The tell was
> the size (287 wide against 370) and the hidden, out-of-bounds chevron. When a
> node's data looks wrong, check whether it is *the right kind of node* before
> correcting its content.

> **Trap worth remembering.** Binding a TEXT property to a node that instances
> already override silently resets those instances to the property's **default**.
> Adding `Value` with default `Junior Orientation` would have turned every
> "Please arrange chairs in rows." note into "Junior Orientation" on Booking
> Details - Filled and Edit Booking. Always re-set existing instances in the same
> operation that introduces the property.

Items 2 and 3 needed care: all four text nodes resolve to a single shared master
`4489:3655` (`List Items / Base`) that carries **no** room text of its own — the
values are per-instance overrides. Fixing at instance level reaches every screen
that reuses those list items.

Item 4 is the same failure class the vault already documents for the badge
recolour: *a component-set edit changes nothing on screen until the instances are
dealt with too*. Here the rot was an instance-level `FILL` sizing override.

Note on destinations: `NAVIGATE` requires the target to be a **direct child of a
section or of the page**, and each action needs `transition` plus the reset flags.
`Edit Booking` (child of section `4434:13590`) satisfies both.

### Reviewed and deliberately not changed

- *Edges in Booking History are rough* — investigated and explained. The
  `Content` frame `4249:13667` is 402×573 and clips at y=6886, exactly where the
  `Nav Bar` `4645:9650` begins, which is correct. The artifact is that the third
  card `4336:17848` spans y6735–6927, so it is sliced **41px from its bottom,
  through the "Research Presentation" text row**, where every other card shows a
  16px rounded bottom. Options were to move the cut into a gap, show the card
  fully under the nav, or drop the third card. **Decision: leave it** — it reads
  as a normal mid-scroll list.

### Correction — the attendee chips *are* wireable

An earlier version of this note recorded that per-chip single-select was
**impossible** because `CHANGE_TO` is host-scoped. **That was wrong**, and the
error was mine, not Figma's.

The original hotspot attempt set `rect.fills = []`. A rectangle with no fill has
no hit area, so it is not a valid prototype source — and Figma's error message
said exactly that (*"the source may not be a valid prototype source"*), but the
message lists three possible causes and I read it as the destination being
unreachable. Two subsequent tests settled it:

| Test | Result |
|---|---|
| Reaction on a **chip instance inside a variant** → sibling variant of the enclosing set | **accepted** |
| Reaction on a **rectangle with a fill** → sibling variant of the enclosing set | **accepted** |
| Reaction from variant `Count=10`, chip `10` → destination `Count=10` (itself) | rejected — a no-op, correctly refused |

The third result is the proof: `Count=10` is not a variant of the chip's own
component set (`Attendee Preset`), so Figma must be resolving the destination
against the **enclosing `Attendee Selector` instance**. Single-select works.

A variable-mode approach was also attempted and abandoned: the file's Figma plan
returns **"Limited to 1 modes only"**, so multi-mode variables are unavailable
here regardless.

### Verification audit — 2026-10-10

Re-checked every item in the **New** list against the live file, plus three items
reported as fixed from memory.

| Item | Verdict | Evidence |
|---|---|---|
| Can't select attendees count | ✅ | Empty: all four chips wired. Filled/Edit: 10/20/30 wired, 40 selected |
| Attendees 20 → 40 | ✅ | No `20 people` anywhere on the Screens page |
| Map from ECC-603 room details | ✅ | All four Room Detail screens → `4859:5846` |
| Checkmark brokenly large | ✅ | **40** badges scanned, none oversized — max height 26 (was 79×75) |
| Rebooking date + review bubbles | ✅ | Steppers consistent; the symptom is no longer reachable |
| Booking stage bubble pressable | ✅ | All 8 steppers report **0 reactions** |
| Edges in Booking History | ⚪ | Unchanged by decision — see above |
| ECC-601 → ECC-603 | ✅ | No `ECC-601` on the Screens page |
| Edit → attendees fixed at 20 | ✅ | Chip `40` selected |
| Upload buttons collapse summary | ✅ | Accordion root **0** reactions, header **1**, on both dropdowns |
| Pencil button purpose | ✅ | → `4673:10431` (Edit Booking) |

**One check initially produced a false negative.** The first Status Badge sweep
matched `/^Status Badge/` against the *variant* name, but variants are named
`Status=Upcoming`, `Status=Busy` and so on — so it could never match and returned
zero results. Re-run against the **parent component set** name, which found 40
badges and confirmed none oversized. A zero from a pattern-based check is only
evidence once the pattern is known to match something.

#### Reported fixed from memory — verified

| Claim | Verdict | Evidence |
|---|---|---|
| Attendee slider replaced with buttons | ✅ | Zero `Slider` instances anywhere in the file |
| Red cross replaced with orange clock | ✅ | Room Detail - Unavailable reads "Busy until 15:00" with an orange clock icon |
| Booking disabled on room Details *and* Reviews | ⚠️ **half true** | Disabled on Unavailable/Details (greyed). **Both Review screens still render Book Now as a full-colour orange CTA** that has no reaction |

The Review-tab finding matters: the `Room Details Bar / State=Review` variant
styles "Book Now" with `#E8622D`, identical to the available state, so the most
prominent control on the screen is a dead end that looks live. Note this
**contradicts the main project note**, whose resume-list item 5 (Chonchanok)
records the same behaviour as an *open bug to fix* rather than a deliberate
disable. Intent is unresolved — see [[uxui-facility-booking-project]].

Minor, not changed: a `Lucide / circle-x` is still used on Booking History - Past.
The decisions log specifies `calendar-x` in `#4B5563` for Cancelled.

### Still open

- *Rebooking shows date + review bubbles already on* — resolved, see fix 10.
- *Edges in Booking History are rough* — reviewed, left as-is; see above.
- *File upload buttons collapse Booking Summary* — fixed, see fix 8.
- *Can't use Map from ECC-603 room details* — fixed, see fix 9.

Everything on the **New** list has now been actioned or explicitly decided. The
**Unfixed** list at the top of this note was flagged by the reporter as
deliberately out of scope and has not been touched.

### Other work this session (same file, not from this list)

- Added `Text Input / State=Filled` variant populated with mock data; applied to
  Booking Details - Filled and Edit Booking.
- Removed 72 orphaned Nova calendar nodes and the clipped duplicate
  `AL` frame from `Date Time Filter - Visibility / State=Hide`.
- Pruned the `Button` set 18 → 4 variants after confirming all 14 had zero
  instances.
- Re-parented `Mawin / User / Profile` out of `Napaul / User / Booking Flow`.

### 2026-10-11 — session 2 (post-fix retest feedback)

Retest by Cheese and Chingchimg, S6–S10 scope.

**Reported — round 2**

- Cheese: all three tasks done, rating 5, "everything intuitive". One item — the
  map of ECC-603 reached from Home or Search doesn't allow booking the room.
- Chingchimg: rating 5 for this part. One item — picking `08:00–09:00` **and**
  `13:00–14:00` showed only `13:00 – 14:00` in the Booking Summary. She guessed a
  Figma paywall; the guess was right — see below.

**Root cause — multi-slot summary (verified)**

Two independent faults:

1. Each `Time Select` chip carried `ON_CLICK → CHANGE_TO State=Selected` on
   **itself only** — nothing reset its siblings, so every tapped chip stayed
   lit. No mutual exclusion, by construction.
2. Making the downstream summary *reflect* the pick needs a variable written at
   runtime. Probe against this file:
   `"You cannot use Set Variable actions in Reactions with your current plan."`
   Variables can be *created* here — a collection, a BOOLEAN and a STRING were
   all accepted — but not *written by a prototype action*, so no dynamic text.
   (Corroborates the earlier "Limited to 1 modes only" plan finding.)

Corollary: Booking Summary's `13:00 – 14:00` and `October 2, 2026` are
hardcoded. Any pick other than 13:00–14:00 would mismatch at step 4.

**Fixes applied**

| # | Item | Node(s) | Change | How verified |
|---|---|---|---|---|
| A | Chip multi-select | New set `Time Slots Grid` `4923:4845`, placed instance `4923:4846` (replaces frame `4060:4201`) | Rebuilt the grid as a wrapper component set; every enabled chip fires `ON_CLICK → CHANGE_TO` the wrapper variant in which **that** chip is selected — same enclosing-instance pattern as the Attendee Selector. Chip→own-variant is a self no-op and Figma refuses it, so it is skipped | Reaction read-back on the live instance: `13:00 – 14:00` → 1 action; others 0. Disabled chips untouched |
| B | Review/summary coherence | `4923:4793` (Selected=None), `4923:4827` (Selected=13-14) | Pruned the set to 2 variants and disabled `08:00–09:00` / `16:00–17:00`, so only `13:00 – 14:00` is bookable — the one slot the hardcoded summary shows. Chip hyphen normalised to the en-dash form | Instance scan: one `Default` chip, five `Disabled`; screenshot of `Select Date & Time` |

Backup frame `BACKUP / Select Date & Time` (`4923:4750`) sits right of S7 in
section `4434:13572`; delete once the present-mode click-through passes.

**Residual / by design**

- Booking Summary time + date stay static. Radio now blocks *multi*-select and
  slot pruning blocks *mismatch*; a pick-aware summary still needs `Set
  Variable` (paid) or duplicating the Details→Upload→Review chain per slot.
- Cheese's map-booking item is logged as **reported, not yet verified** against
  the file. Adjacent known issue: both `Room Details Bar / State=Review` screens
  render Book Now as a live-looking CTA with no reaction (see audit above) —
  possible same root.
- Present-mode click-through not yet run; verification so far is reaction
  read-back plus screenshot.

---

*Reference → [[uxui-prototype-reference]] · Status → [[uxui-project-state]] · Tracker → [[uxui-usability-test]]*
