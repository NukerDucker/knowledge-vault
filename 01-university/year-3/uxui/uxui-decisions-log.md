---
title: KMITL B-App — Design Decisions Log
tags:
  - university
  - group-work
  - project
status: active
subject: uxui
course: 01276545
feature: 01-university/year-3/uxui/assets/decision/information-architecture/G2_UserStory-1.png
thumbnail: thumbnails/resized/688c40ab71446a2ac60c39829ba9f4ae_86cf658e.webp
---

# KMITL B-App — Design Decisions Log

Every decision made on this project, why it was made, and what it cost. Written to feed
`GX_FinalReport.pdf` and to answer the examiner's random question about any single screen.

**Group 2 · Mookrata** — Napaul Intharasing (67011178) · Mawin Pengsuk (67011163) ·
Chonchanok Nitipornsri (67011106)

Images live in `assets/decision/`, copied from `~/Documents/University/Year-3/UXUI/`.
Source notes: [[uxui-week3-market-comparison]] → [[uxui-week9-sitemap]], plus
[[uxui-final-audit]] and [[uxui-usability-test]].

---

## 1 · The decision that governs every other one

> **The problem.** Two users, one failure point.
>
> - **Student:** submits a booking via LINE, then cannot tell whether staff have read it.
>   Messages sit unread for days; by the time it is clear the activity cannot proceed, it is
>   too late to rearrange.
> - **Professor:** wants live room availability from his desk. No shared calendar exists, so he
>   walks the ECC building reading door notice boards — and double-bookings still happen anyway.
>
> Both POVs fail at the same place: **no visibility into room state or booking progress.**

That sentence is the filter. **Every feature must trace to a POV or an HMW.** Anything that
could not was cut — including AI room suggestion and a loyalty system, both of which were
generated during Crazy 8s and then killed. Being able to say *why something was cut* is
stronger evidence of a decision process than the feature list itself.

**Decision — build live availability + status notification first.** Not because they are the
most interesting, but because two independent frameworks agreed they must come first:

| Framework | What it says | Verdict |
|---|---|---|
| Kano | These are **Basics** — the product is broken without them | Ship first |
| Hooked | The **Variable Reward** step cannot exist without live data | Ship first |

> When two models disagree you have a judgement call. When they agree, you have a decision.

That is the single most quotable line in the project, and it is the answer to *"why did you build
this first?"*

---

## 2 · Information architecture

### 2.1 User story map — the backbone

Four activities across the top, stories hanging beneath. Full detail in
[[uxui-week8-user-story-mapping]].

**Log in → Browse & Check Rooms → Book a Room → Track Room Status**

| Activity | Steps and stories |
|---|---|
| **Log in** | Enter student ID · enter password · press log in |
| **Browse & Check Rooms** | *Browse rooms* — view list, filter. *Filter search* — floor, room type, date, time, capacity. *Search by name* — for users who already know the room. *Check availability* — out of order, free, occupied. *View room detail* — capacity, equipment, photos |
| **Book a Room** | *Select room & date* — room, date, time slot. *Enter details* — purpose, attendee count, attach activity form. *Submit* — conflict check, submit, tracking confirmation |
| **Track Room Status** | *Track approval* — pending, approved, rejected, rejection reason. *Get notified* — status change, auto-release alert |

**The submitted story map** — `G2_UserStory.pdf`, five pages:

![User story map page 1](assets/decision/information-architecture/G2_UserStory-1.png)

![User story map page 2](assets/decision/information-architecture/G2_UserStory-2.png)

![User story map page 3](assets/decision/information-architecture/G2_UserStory-3.png)

![User story map page 4](assets/decision/information-architecture/G2_UserStory-4.png)

![User story map page 5](assets/decision/information-architecture/G2_UserStory-5.png)

**Why the backbone is those four and not something else:** they are the four steps of the
critical user journey named in Week 8 — *check availability → submit request → track status →
(staff) approve & manage*. The map is the journey, written at story granularity.

**Deliberately deferred to a later release:** biometric login · favourite rooms · campus map view ·
recurring booking · auto-fill from history · calendar export · similar-room suggestion after
rejection. These are the *bottom* slice of the map — the discipline is that they are visible and
postponed, not invisible and forgotten.

### 2.2 Sitemap — the navigation model

Full tree in [[uxui-week9-sitemap]]. Three surfaces: **Shared Auth**, **Student/Professor**, and
**Facility Staff**.

Five navigation decisions were made here, and each one has a reason:

| # | Decision | Why |
|---|---|---|
| 1 | **Room Detail is one shared page**, staff seeing extra controls | The room is the same object to everyone; only the actions differ. Duplicating the page would duplicate every future room change |
| 2 | **Notifications is top-level, not inside Profile** | HMW 2 is *notify users automatically so they never need to message staff*. A core promise cannot be buried two taps deep |
| 3 | **Bookmark lives in Room Detail, not Booking** | Users save a room *before* they commit to it. Putting save inside the booking flow only offers it to people who have already decided |
| 4 | **Edit Booking is restricted to Pending** | Once staff have approved, changing the request invalidates the approval. Must be annotated on the slide — an examiner will ask |
| 5 | **Home/Dashboard is the entry node** | Every comparison app checked lacks one. It is a differentiator, not a convention we followed |

**The submitted sitemap** — `G2_Sitemap.pdf`, three pages:

![Sitemap page 1](assets/decision/information-architecture/G2_Sitemap-1.png)

![Sitemap page 2](assets/decision/information-architecture/G2_Sitemap-2.png)

![Sitemap page 3](assets/decision/information-architecture/G2_Sitemap-3.png)

### 2.3 Wireflow

**The submitted wireflow** — `G2_Wireflow.pdf`, five pages. Page 1 is the cover, which is why all
three members and the group name are on it.

![Wireflow page 1 — cover](assets/decision/information-architecture/G2_Wireflow-1.png)

![Wireflow page 2](assets/decision/information-architecture/G2_Wireflow-2.png)

![Wireflow page 3](assets/decision/information-architecture/G2_Wireflow-3.png)

![Wireflow page 4](assets/decision/information-architecture/G2_Wireflow-4.png)

![Wireflow page 5](assets/decision/information-architecture/G2_Wireflow-5.png)

### 2.4 Role division — and why the speaking order follows it

| Member | Task | Screens | Pages |
|---|---|---|---|
| **Chonchanok** (67011106) | Home · Search Flow · Room Info | 9 | Home · ECC room list · Search Results · Search Results - Empty · Filters · Room Detail ×4 · Map |
| **Napaul** (67011178) | Authentication · Booking Flow · Overlays | 16 | Sign In · Sign Up · Forgot Password · Reset Password · Select Date · Booking Details (empty/filled) · Upload Docs ×2 · Review · Confirmation · 5 overlays |
| **Mawin** (67011163) | Booking History · Booking Details · Profile | 6 | History Past · History Upcoming · Detail Approved · Detail Completed · Edit Booking · My Profile |

**Total 31 screens.** Minimum was 5 per member, ≥3 full-function, ≥2 core.

**The split is by user task, not by screen count** — Chonchanok *finds* a room, Napaul *books* it,
Mawin *tracks* it. That is why the presentation order is Chonchanok → Napaul → Mawin. The exam
says speaking order follows the flow, not student number, and this split makes that free: the
examiners see the user journey run continuously instead of jumping between members.

### 2.5 Research artefacts behind these decisions

The earlier deliverable that the story map, sitemap and wireflow were built on. It is listed after
the outputs rather than before them because it explains *how* the structure was agreed, not *what*
it is — but if an examiner asks "why is Notifications top-level?", the answer starts here.

**Card sorting** — `G2_CardSorting.pdf`, nine pages. This is where the grouping that became the
sitemap's branches was decided, by participants rather than by the team:

![Card sorting page 1](assets/decision/information-architecture/G2_CardSorting-1.png)

![Card sorting page 2](assets/decision/information-architecture/G2_CardSorting-2.png)

![Card sorting page 3](assets/decision/information-architecture/G2_CardSorting-3.png)

![Card sorting page 4](assets/decision/information-architecture/G2_CardSorting-4.png)

![Card sorting page 5](assets/decision/information-architecture/G2_CardSorting-5.png)

![Card sorting page 6](assets/decision/information-architecture/G2_CardSorting-6.png)

![Card sorting page 7](assets/decision/information-architecture/G2_CardSorting-7.png)

![Card sorting page 8](assets/decision/information-architecture/G2_CardSorting-8.png)

![Card sorting page 9](assets/decision/information-architecture/G2_CardSorting-9.png)

---

## 3 · Design system

### 3.1 Palette — and a correction worth admitting

The palette was read off the **live Figma file**, not from any document. Both palettes previously
written down in the team's own notes were wrong.

| Token | Hex | Use |
|---|---|---|
| Primary orange | **`#E8622D`** | CTAs, active nav, selected states |
| Navy | **`#1B2A5B`** | Headings, body text, labels |
| Background | `#F0F2F5` | App background |
| White | `#FFFFFF` | Cards, surfaces |

**Rule: navy is text only, never a surface.** Orange carries action; navy carries reading.

The audit note's own colour table (`#E86027` orange, `#1A2340` navy, `#2E9E5B` green, `#E8A020`
amber) is a **third, superseded palette** — do not quote it. It predates the live read.

![Buttons and actions](assets/decision/design-system/buttons-and-actions.png)

![Forms and inputs](assets/decision/design-system/forms-and-inputs.png)

![Cards](assets/decision/design-system/cards.png)

![Action bar](assets/decision/design-system/action-bar.png)

### 3.2 Status Badge — a 10-variant system, and the rule it follows

Every status communicates on **three channels at once**: colour, icon, and text. That is WCAG
1.4.1 — never colour alone — and it also means a colour-blind user loses nothing.

| Variant | Colour | Icon | Label |
|---|---|---|---|
| Upcoming | `#B45309` | calendar-clock | Upcoming |
| Available | `#047857` | circle-check | Available |
| Approved | `#047857` | badge-check | Approved |
| Busy | `#B45309` | **clock** | Busy until HH:MM |
| Rejected | `#DC2626` | circle-x | Rejected |
| Partial | `#C2410C` | circle-dashed | Partial |
| Reviewing | `#C2410C` | hourglass | Under Review |
| Unavailable | `#6B7280` | ban | Unavailable |
| Cancelled | `#4B5563` | calendar-x | Cancelled |
| Completed | `#6B7280` | check-check | Completed |

![Status and progress components](assets/decision/design-system/status-and-progress.png)

**Two decisions inside this table are worth defending, because both were contested:**

1. **Busy changed from a red cross to an amber clock.** A tester read the red ⊗ as *"broken"* —
   and it was also identical to Rejected, so two unrelated meanings shared one visual. Busy now
   says *when*, which is the information the user actually came for.
2. **Four colour collisions remain by design** — Busy≡Upcoming (amber), Available≡Approved,
   Partial≡Reviewing, Unavailable≡Completed. These pairs never appear in the same context, so the
   icon and label separate them. Unifying the colours would need four more hues and would make the
   palette harder to read, not easier.

### 3.3 Component decisions worth naming

- **Chip** raised from 23px to 28px — it was one pixel under the WCAG 2.5.8 minimum target of 24px.
- **Attendee Preset** replaced a slider — see §6.2.
- **Capacity Select** was cloned rather than added to `Filter Select` — see §6.3, which is a
  cautionary tale.

---

## 4 · Prototype evolution — the evidence

These captures are the *before* state: the 30 September milestone and the earlier `s6`–`s15` set.
They are the honest baseline for every improvement claimed in the tracker.

### 4.1 The 30 September milestone

![Home](assets/decision/prototype-evolution/30sep-01-home.png)

![Search results](assets/decision/prototype-evolution/30sep-02-search-results.png)

![Filter](assets/decision/prototype-evolution/30sep-03-filter.png)

![Room detail](assets/decision/prototype-evolution/30sep-04-room-detail.png)

![Map](assets/decision/prototype-evolution/30sep-05-map.png)

![Select date and time](assets/decision/prototype-evolution/30sep-06-select-date-time.png)

![Booking details](assets/decision/prototype-evolution/30sep-07-booking-details.png)

![Upload documents](assets/decision/prototype-evolution/30sep-08-upload-documents.png)

![Review booking](assets/decision/prototype-evolution/30sep-09-review-booking.png)

![Booking submitted](assets/decision/prototype-evolution/30sep-10-booking-submitted.png)

![Booking history past](assets/decision/prototype-evolution/30sep-11-booking-history-past.png)

![Booking history upcoming](assets/decision/prototype-evolution/30sep-11-booking-history-upcoming.png)

![Booking detail](assets/decision/prototype-evolution/30sep-12-booking-detail.png)

![Edit booking](assets/decision/prototype-evolution/30sep-13-edit-booking.png)

### 4.2 The earlier `s6`–`s15` set — the true "before"

![s6](assets/decision/prototype-evolution/s6.png)

![s7](assets/decision/prototype-evolution/s7.png)

![s7 fixed](assets/decision/prototype-evolution/s7-fixed.png)

![s8](assets/decision/prototype-evolution/s8.png)

![s9](assets/decision/prototype-evolution/s9.png)

![s10](assets/decision/prototype-evolution/s10.png)

![s11](assets/decision/prototype-evolution/s11.png)

![s12](assets/decision/prototype-evolution/s12.png)

![s13](assets/decision/prototype-evolution/s13.png)

![s14](assets/decision/prototype-evolution/s14.png)

![s15](assets/decision/prototype-evolution/s15.png)

**What changed across these generations, and why** — the full itemised list is
[[uxui-usability-test#Improvement tracker]], 48 rows. The recurring themes:

- **A four-dot stepper** became numbered and labelled. Four unlabelled dots cannot tell you how
  many steps remain, which is the only thing a stepper is for.
- **A flat orange room swatch** became a photo card with status, category and capacity chips.
  A swatch is not data.
- **A clipped CTA** — a 7px sliver under the nav bar — was made fully visible and relabelled
  "Continue to review". An unreachable button is not a button.
- **A static "Under Review" pill** became a four-node approval tracker:
  Submitted → Reviewing → Approved. This is HMW 2 made visible.

### 4.3 Device walkthroughs — the booking flow end to end

Seven exports on device mockups, showing the flow in context rather than as isolated frames. Read
them as a sequence, not as a device test.

**These captures predate the attendee-control rebuild — and that is exactly why they are worth
keeping.** The Booking Details screen still shows the old slider frozen at **80**, with the
hardcoded *"Exceeds room capacity (40 seats)"* warning directly beneath it. That is the precise bug
a usability tester hit, sitting in the team's own export rather than only in a write-up. Compare
against §6.2, where the control was replaced.

![Device walkthrough 1](assets/decision/flow-walkthroughs/device-frame-15.png)

![Device walkthrough 2](assets/decision/flow-walkthroughs/device-frame-16.png)

![Device walkthrough 3](assets/decision/flow-walkthroughs/device-frame-17.png)

![Device walkthrough 4](assets/decision/flow-walkthroughs/device-frame-18.png)

![Device walkthrough 5](assets/decision/flow-walkthroughs/device-frame-19.png)

![Device walkthrough 6](assets/decision/flow-walkthroughs/device-frame-20.png)

![Device walkthrough reference frame](assets/decision/flow-walkthroughs/device-iphone-17-pro.png)

**A separate finding, about the Figma file rather than about these images:** the responsive device
matrix section inside Figma had every frame at **402px** regardless of its 375 / 360 / 393 label —
the outer frames were `HUG` and the inner ones `FIXED`, so nothing was actually being tested. A
responsive matrix that renders every device identically is worse than no matrix, because it looks
like evidence. Fixed to `FILL` and re-verified by resizing to 360 and screenshotting Home.

### 4.4 Intermediate working states

Successive states of the same screens, kept for completeness rather than as separate findings.

![s11](assets/decision/prototype-evolution/s11b.png)

![s11 final](assets/decision/prototype-evolution/s11f.png)

![s12](assets/decision/prototype-evolution/s12.png)

![s12 variant](assets/decision/prototype-evolution/s12b.png)

![s12 final](assets/decision/prototype-evolution/s12f.png)

![s12 new](assets/decision/prototype-evolution/s12-new.png)

![s13](assets/decision/prototype-evolution/s13.png)

![s13 variant](assets/decision/prototype-evolution/s13b.png)

![s13 final](assets/decision/prototype-evolution/s13f.png)

![s13 new](assets/decision/prototype-evolution/s13-new.png)

![s14](assets/decision/prototype-evolution/s14.png)

![s14 variant](assets/decision/prototype-evolution/s14b.png)

![s14 final](assets/decision/prototype-evolution/s14f.png)

![s15](assets/decision/prototype-evolution/s15.png)

![s15 variant](assets/decision/prototype-evolution/s15b.png)

![s15 final](assets/decision/prototype-evolution/s15f.png)

![s15 new](assets/decision/prototype-evolution/s15-new.png)

![Booking detail alternate](assets/decision/prototype-evolution/30sep-12-booking-detail-1.png)

---

## 5 · Accessibility and contrast

### 5.1 The numbers, measured not estimated

Computed with the WCAG 2.x relative-luminance formula, read from the live file.

| Pair | Ratio | Verdict |
|---|---|---|
| Navy `#1B2A5B` on white | 13.7–15.5:1 | ✅ far past AA |
| White on `#047857` (Available, Approved) | 5.48:1 | ✅ |
| White on `#C2410C` (Partial, Under Review) | 5.18:1 | ✅ |
| White on `#B45309` (Upcoming, Busy) | 5.02:1 | ✅ |
| White on `#4B5563` (Cancelled) | 7.56:1 | ✅ |
| White on `#DC2626` (Rejected) | 4.83:1 | ✅ |
| `#848B96` on white (285 uses) | 3.43:1 | ❌ |
| **White on orange CTA `#E8622D`** | **3.38:1** | ⚠️ **deliberate** |

**Six of ten badge variants originally failed AA** — including Available and Approved, the two
most-used states. All six were corrected.

### 5.2 The white-on-orange decision — the one to be ready to defend

The CTA label is **white at 3.38:1**, which fails AA for normal text. This is a decision, not an
oversight. Navy `#1A2340` would give 4.58:1 and pass.

**Why white was kept:** after reviewing [The Myths of Color Contrast
Accessibility](https://uxmovement.com/buttons/the-myths-of-color-contrast-accessibility/), on the
grounds that contrast ratio is an approximation and white on a saturated hue reads better than the
maths suggests, because white carries no hue or saturation of its own. Five usability participants,
none of whom raised button legibility, is the supporting evidence.

**Two caveats to state rather than have discovered:**
- The article's flagship example is white-vs-black on **blue**, and its evidence is preference
  surveys, not reading-performance testing.
- Its lower-ratio allowance is justified via **large text** (18pt / 14pt bold). Our button labels
  are **14px Medium** — not large text. So the position rests on the perception argument, not on
  the large-text exemption.

**If challenged: say 3.38:1. Never claim 4.58:1.**

### 5.3 The accessibility fix that had not actually landed

The badge recolour was recorded as done — "6 fill swaps, propagates to all 31 screens". It did not
propagate. The component set was recoloured correctly, but every live instance carried an override
holding the old colour, and seven of ten variants also kept a 1px stroke in the old colour, so each
badge wore a halo of its former colour.

**All 33 live badges were still rendering the old values.** Repaired instance by instance, plus 33
in the responsive matrix. Verified afterwards: 65 badges, 0 mismatches.

> **The lesson, and it is the most transferable one on this project:** in this file, a
> component-set edit changes nothing on screen until the instances are dealt with too. "I updated
> the component" is not evidence. Check what renders.

### 5.4 Other accessibility decisions

- **Map floor pills are 24px** — meets the WCAG 2.5.8 AA floor exactly, under the 44px comfort
  target. Say both numbers; the honest version scores better than the flattering one.
- **CTA height 42px → 55px** for touch.
- **Form errors** use a warning icon plus descriptive text, never a red border alone.
- **Chip and Filter Select** raised 23px → 28px, clearing the 24px minimum.

---

## 6 · Screen-level decisions

### 6.1 Empty and error states

- `Search Results - Empty` — filters matching nothing, copy offering to clear them.
- `Booking History` empty state — no bookings yet, copy routing to Home to start one.
- **Capacity error** — "Exceeds room capacity (40 seats)", inline.

**A fake error was found and deleted.** A `capacity-warning` label was a plain text layer,
permanently visible, hardcoded onto the filled screen. It asserted "Exceeds room capacity (40
seats)" regardless of the value entered — which is why a tester got the error while entering
*1 attendee*. It was never computed from anything. **A validation message that cannot be false is
not validation.** Removed from all five copies.

### 6.2 The attendee control — why a slider was replaced, not fixed

The original control was a slider that only reached **two values, 1 or 80**. Root cause: it is a
**2-variant Figma component**, and a Figma prototype has no variables or logic — the only way to
show a new value is to swap to a different variant.

| Control | Variants needed | Covers |
|---|---|---|
| Slider, continuous 1–40 | **40** | exact seat counts |
| Slider, stepped 5/10/…/40 | 8 | coarse only, still snaps |
| Numeric stepper | 2 buttons + **40 readouts** | the number still needs a variant per value |
| **`Attendee Preset` chips** | **4** | every value that matters |

So the slider was not broken — it was *fake*. Replacing it with capacity-bounded chips (10 / 20 /
30 / 40) does three things at once:

1. **An over-capacity booking becomes unreachable rather than rejected.** Error prevention, not
   error messaging — which is exactly what the exam asks for on the individual slide.
2. **Target size** — a chip is one 28px tap; a drag handle is a precision task.
3. **Exact input** — people book for a group size, and group sizes are round.

**The honest counter-argument:** a real app should allow free numeric entry, because 23 is a real
number. That is why the **Filter** capacity control kept a Min/Max range instead — a range wants
continuous ends, so presets were the wrong shape there. Different control, different job. Knowing
which is which is the actual design decision.

### 6.3 The regression that taught the real lesson

Adding a disclosure chevron to the shared `Filter Select` component also chevroned **Room Type**
and **Facility Equipments**, because both are instances of it. Both rows grew and lost density.

Reverted, and a separate `Capacity Select` was cloned so the chevron applies to capacity only.

> **Check who else uses a component before changing it.** This is recorded as tracker row 41
> deliberately rather than hidden — a documented regression caught by screenshot is stronger
> evidence of process than a clean-looking history.

### 6.4 Content and data realism

Real room photographs, real student IDs (`67011178`), real names, specific dates, real file names
(`proposal.pdf · 5.4 MB`). **No Lorem ipsum anywhere.** Placeholder text like
"Attachment title / Description · 5.4 MB" was replaced with real filenames.

**One data integrity fix:** room ECC-603 carried **three different capacities** — `Cap: 15` on the
Home card, `30 Seats` in Search Results, `40 Seats` in Room Detail and the booking flow.
Normalised to **40** everywhere. A room has one capacity.

### 6.5 One status vocabulary

The same room state was called **`Busy until 15:00`** in Search but **`Unavailable`** in Room
Detail — two different words, two different badge variants, two different colours, for one
condition. Worse, the detail screen dropped the time entirely, so the user lost the only piece of
information that mattered.

**Decision: `Busy until HH:MM` wins.** It answers *when*, which is the question. `Unavailable` is
reserved for genuinely not-bookable states. Room Detail now matches Search.

---

## 7 · Interaction and prototype decisions

### 7.1 Overlays are overlays

An earlier rewrite changed every overlay trigger from `OVERLAY` to `NAVIGATE`. Because each overlay
frame is a **transparent wrapper whose scrim lives on an inner child**, `NAVIGATE` presented the
frame with nothing behind it — a tester reported *"the search background behind the popup is
gone"*. `CLOSE` also became a no-op, since there was no longer an overlay to close, which is why
every sheet trapped the user with no way out.

**Six callers restored to `OVERLAY`**, and the Confirm Sheet was given the dismiss it had never had.

### 7.2 The stepper — and how a convention gets settled

A tester reported *"the connector line renders ahead of the current section"*. Investigation showed
the file was **internally consistent**, not off-by-one: it used convention A — *N* filled segments
on step *N*. So the segment leaving the current step was filled on purpose.

It was changed to convention B (*N−1* filled) because **step 1 settles it**: under A the first
screen is wrong twice over — its label is navy *and* its outgoing segment is filled. Under B it is
correct on every element. The tiebreaker is not taste, it is which reading leaves fewer
contradictions.

A second, unambiguous defect was found in the same pass: every "empty" segment carried a **1px
orange nub** — the author's zero-width placeholder, plainly visible at 4× zoom.

---

## 8 · Competitive positioning

Three products compared in Week 3, plus three more benchmarked in Week 9.

| Product | What it does well | What it lacks |
|---|---|---|
| **BU** Meeting Room Reservation | Structured request form, draft saving, explicit "My Request" status tracking | No real-time availability — you pick a room *then* learn if it's free. Nothing is pushed |
| **RMUTL** Room Booking | Availability-first — schedule, capacity and equipment shown before commitment | Every participant must register and separately confirm. A booking stalls on the slowest member |
| **Calendly** *(adjacent)* | Unavailable time is never rendered, so conflicts are structurally impossible. Zero-account booking | No approval workflow, no concept of a shared physical resource |
| **Skedda** | Direct domain match, live availability grid | No approval workflow, no rejection reason, no status notifications |
| **LibCal** | University context, same user group | Auto-approve — no approval workflow, no live calendar, no document upload |
| **Google Calendar** | The most familiar reference for professors | No approval workflow, no document upload, no status tracking, email notifications only |

> **Key insight:** all of them cover **Browse → Book**. None cover **Request → Approval → Notify**
> properly. That gap is the entire reason this product exists, and it traces directly to HMW 1 + 2.

**The single design opportunity, in one sentence:** every product digitises the *request*; none
digitises *availability and approval together*. University systems have approval but no live
availability; commercial tools have live availability but no approval.

---

## 9 · Open decisions and known debts

State these before an examiner finds them.

| # | Debt | Status |
|---|---|---|
| 1 | **Palette consolidation.** The file carries more dark text colours than intended — `#1B2A5B`, `#1A2340`, `#111827`, `#000000`. The steppers were unified to two; the rest of the file was not | Open — Future Work slide |
| 2 | **`Booking Status Badge`** is a second, navy (`#1B2A5B`) badge family whose component set reports errors. Not an accessibility problem; a naming one | Noted, untouched |
| 3 | **Second persona** — the exam requires two. "New" (professor, 34) exists; the student persona is written in the report from Week 5/7 research material | See §10 |
| 4 | **Facility Staff surface** exists in the sitemap but has no screens. Prototype scope is the student/professor journey | Scope decision |
| 5 | **`#848B96` on white at 3.43:1** across 285 uses — secondary/muted text | Open |
| 6 | **Emotion scores in the journey map are inferred from quotes, not scored by participants** | Label as inferred |
| 7 | **App name** — Figma uses "KMITL B-App", Week 8/9 notes say "RoomIQ" (a placeholder) | Pick one |

---

## 10 · Persona 2 — the student

Persona 1 is **"New"**, 34, University Professor, Computer Engineering, EEC building — he books
labs and classrooms for his own courses and endorses student requests. His journey map is in
[[uxui-week4-user-journey-map]].

Persona 2 is drawn from the student material that already existed across Weeks 5–8: the Week 5
empathy map and POV statement, the Week 7 user cases, and the Week 8 scoping work.

> **POV:** *A 3rd-year engineering student needs a way to track booking status in real time because
> staff leave LINE messages unread for days, leaving them unable to confirm whether their activity
> can proceed until it's too late to replicate.*

**Empathy map (Week 5, student-voiced):**

| | |
|---|---|
| **Says** | "Messaged staff, got left on read." · "Why paper form?" · "Room shows booked even after cancellation." |
| **Does** | Waits for LINE reply · goes in person · submits a physical form · contacts staff via LINE |
| **Thinks** | Wants a centralised ecosystem · transparent booking status online · self-serve room availability |
| **Feels** | Frustrated by limited slots and conflicts · uncertain waiting for approval · paper forms feel outdated |

> **Insight:** students need a transparent reservation process to feel confident throughout the
> booking journey.

**User cases (Week 7):** the club leader who sent a LINE message two days ago and still cannot tell
her members whether the activity is on · the final-year student whose preferred slots are gone by
the time staff reply · the professor who walks the building to check equipment he cannot verify
without asking.

**The two personas fail at the same point** — one walks to a door, the other refreshes a chat. Both
are visibility failures, not form failures. That is why one design answers both.

---

## 11 · AI use

Full log and declaration: [[uxui-facility-booking-project]]. Summary — all entries **Green level**
(AI as research and reference tool), no Before/After slides required.

Two versions of this table exist in the team's notes and they disagree in size (a 3-row version and
a 1-row version). **Reconcile before submitting** — the report needs exactly one.

---

*Project hub → [[uxui-facility-booking-project]] · Audit and presentation plan →
[[uxui-final-audit]] · Defects and fixes → [[uxui-usability-test]]*
