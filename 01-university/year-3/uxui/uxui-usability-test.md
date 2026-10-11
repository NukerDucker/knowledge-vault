---
title: "UX/UI Usability Test & UI Improvement — Individual"
tags:
  - university
  - individual
status: submitted
subject: uxui
course: 01276545
due: 2026-10-12
points: 10
updated: 2026-10-09
---

# Usability Test & UI Improvement

**Individual task** · 10 points · Due 2026-10-12 23:59  
**Napaul's scope:** Screens 6–10 (booking flow: Select Date & Time → Booking Details → Upload Document → Review Booking → Booking Submitted)  
Parent project: [[uxui-facility-booking-project]]

---

## Status — 2026-10-11

**Submitted.** Handed in on Google Classroom 2026-10-11.

- `KMITL-BApp_Napaul_UT_submission.pdf` and `.docx`, exported 13:39 —
  `~/Documents/University/Year-3/UXUI/Usability_Test/Napaul/`.
- `KMITL-BApp_Napaul_screens_with-grid.pdf` and `KMITL-BApp_Napaul_screens_no-grid.pdf`,
  exported 12:32, same folder.
- Images were regenerated from the post-fix file state on 2026-10-11 and live in
  `assets/ut/2026-10-11/` — `with-grid/` (7), `no-grid/` (7), `s6-s10-pairs/` (5 annotated).
  That is the batch the submission was built from. The pre-fix set is preserved at
  `assets/ut/2026-10-10-prefix/` and is **not** what was submitted.
- [[uxui-ut-submission]] holds the document text; its prose went through `napaul-voice` R1–R10
  and `ai-check` returned **Likely Human, Medium confidence**.
- Pipeline: `~/Code/ut-export/export.py` (markdown to PDF), `annotate.py` (difference boxes).
  A plain Figma export drops the layout grid — always use the pipeline.

Project-wide status lives in [[uxui-project-state]]. This note carries the reasoning and the
evidence.

**Verified while building**

- Figma renders layout grids in **no** export path. The plugin's `exportAsync` and the REST image
  endpoint both return a flat render, measured pixel by pixel. The grid in section 3 is therefore a
  reconstruction, checked against the 2026-10-06 export: 16px margins, four columns of 86.5px, 8px
  gutters, `#EE621D` at ten percent.
- The seven booking flow frames carried `layoutGrids.visible: false` and now read true. No effect on
  any export, but it is the file state.
- S6–S10 is 5 screens but 7 frames. Booking Details and Upload Documents each carry Empty and
  Filled, so "every page" in requirements 3–5 means seven.
- A stale 18-page submission PDF was removed to Trash rather than deleted.

**Fix batch — 2026-10-10, 16:06–17:54**

Sixteen fixes landed before the regeneration. Full list with node ids in
[[uxui-prototype-buglist-2026-10-10]]. Every image in `assets/ut/2026-10-11/` postdates this
batch.

- **In scope** (S6–S10): Booking Details fields now fill on click (Activity name, Additional
  note, Purpose dropdown); the attendee count is selectable and set to 40; Review Booking shows
  ECC-603 rather than ECC-601; the stepper is no longer clickable; and 81 prototype links were
  repointed off nested frames.
- **Out of scope — other members' submissions:** the oversized badge, the Map wiring, room-card
  routing, and the room-naming pass.

**Open**

- Figma view access is not confirmed — the submitted link is worthless to a marker without it.
- The cheesy re-run decision. Scoring him needs the ECC-608 status changed on Chonchanok's screens
  and a 60 seat variant of the booking flow built in `Napaul / User / Booking Flow`.

---

## What to submit (PDF)

1. Brief profile of 5 test participants (pseudonyms)
2. Feedback summary per participant (short)
3. All UI screens with **grid + pattern design shown**
4. Every page captured with grid setting visible
5. **Separate PDF** — each page alone, no grid
6. Before/after comparison with improvements highlighted (≥5 points; one screen can have multiple)
7. Brief written explanation of each improvement
8. Updated Figma link (view mode)

**Format:** no cover/abstract needed. Portrait or landscape OK. Sections captured in parts if too small.  
**Note:** if <5 improvement points found, include designs for the future as alternatives.

---

## Group 2 — Testing Setup

**Project:** Campus facility booking app for KMITL students and staff.

**Flow to test:** Find room → Check description/availability → Select Date/Time → Book

**Testing objective:** Test whether users can find an available room and complete booking successfully.

**Hypothesis:** We expect users will complete the booking flow easily and understand the information shown on each page.

**Personas:** University students · University staff

**Scenario:**
> "Imagine you've been tasked to book a room for a Junior Orientation event — needs to handle a certain number of people, have all the necessities, on a specific date."

**Info given to participant before start:**
- You want to book a room for a club activity.
- It should handle no more than 60 people including staff.
- It should have simple tools: TVs, 2 microphones.

**Task 1:** "Find and book ECC811 in ECC building"  
Success = user successfully books a room

**Task 2 (optional):** "Search and filter rooms"  
Success = user finds a room fitting the criteria

**Prototype link:** https://www.figma.com/proto/bhuuET1PKmzZSGMkVr2de7/UX-UI-2026-%E2%80%94-KMITL-BApp?node-id=4054-85&t=V9J0ZywXhtL6KiI3-1  
**Figma design link:** https://www.figma.com/design/bhuuET1PKmzZSGMkVr2de7/UX-UI-2026-%E2%80%94-KMITL-BApp?node-id=4054-85&t=V9J0ZywXhtL6KiI3-1

---

## Roles (Group 2)

| Role | Person |
|------|--------|
| Moderator (stays, runs test) | Napaul Intharasing 67011178 |
| Note-taker / Observer (stays, records) | Nmae (TBC full name + ID) |
| Participant (goes to test other group) | TBC |

**Note:** Only 2 groups in class — G2 (in-class, 3 people) + an outside group (3 people). The 3-group sections in the UT groupwork deck are the course template, not this class.

**Checklist before testing:** prototype link works · tasks are printed/ready · note template is open

---

## UT Schedule

| Round | Time | G1 tested by | G2 tested by | G3 tested by |
|-------|------|-------------|-------------|-------------|
| Round 1 | 10:40–11:10 | G3 | G1 | G2 |
| Round 2 | 11:15–11:45 | G2 | G3 | G1 |

→ **G2 as moderator/note-taker stays put both rounds.** Participants go out: Round 1 to test G1, Round 2 to test G3.

---

## How to run the test (moderator steps)

1. **Introduce + set expectations** — "We are testing the design, not you. No right or wrong answers." Ask them to **Think Aloud** — say whatever they're thinking.
2. **Introduce scenario** — give context, do NOT explain how to use it or where to click.
3. **Pre-test interview** — background: similar apps used? related experience?
4. **Run tasks + observe** — let participant go alone. May ask:
   - "What are you thinking about or looking for right now?"
   - "Why did you choose to do it this way?"
   - "What do you expect to happen next?"
   - "Is there anything you feel unsure or worried about?"
   - **Do NOT give hints, answers, or teach.**
5. **Post-test interview** — see template below.
6. **Record + summarize** — what they said, did, asked, hesitated on, got stuck on → findings → improve.

---

## Remote test kit (async — LINE)

For the 4 participants who can't be tested in person. Send verbatim; their reply
fills the profile + post-test fields directly.

**Recruit 5–6, need 4** (Putt is #1 of 5).

**Limitation to record honestly:** async means no Think-Aloud and no observation
of hesitation — only what they report. Put "not observed" in any field they
don't answer. Do not fill gaps by inference; that distinction is what makes the
section defensible.

**Message to send:**

> Hey — could you help me test a room-booking app for ~10 min? It's for a class
> assignment, and we're testing the *design*, not you. No wrong answers.
>
> Link: https://www.figma.com/proto/bhuuET1PKmzZSGMkVr2de7/UX-UI-2026-%E2%80%94-KMITL-BApp?node-id=4054-85&t=V9J0ZywXhtL6KiI3-1
> (opens in view mode, works on your phone)
>
> Imagine you've been asked to book a room for a club activity. It needs to fit
> no more than 60 people including staff, it should have a TV and 2 microphones,
> on a specific date.
>
> Please try to:
> 1. Find and book room **ECC811** in the ECC building
> 2. Search and filter rooms to find one that fits
>
> Screenshot anywhere you get stuck. Then answer these — typing them back is
> fine, no need to be formal:
>
> 1. Nickname
> 2. Age
> 3. Used a room-booking app before? Which?
> 4. Related experience (booking anything online)?
> 5. Task 1 — done / done but messy / couldn't finish
> 6. Task 2 — same
> 7. Rate 1–5 (1 = very hard, 5 = very easy). Why that score?
> 8. What was easy to understand?
> 9. Where did you get stuck or confused?
> 10. Anything you expected to find but couldn't?
> 11. If you could change one thing, what would it be?
>
> Thanks — this genuinely helps.

Q11 is the money question: it's where your ≥5 improvement points come from on
the user side, and it's the one people answer fastest.

---

## Note-taker template (per participant × 5)

### During test

**Profile:**
- Nickname / group:
- Age:
- Used similar product before? Which?:
- Related experience:

**Task result:**
- Task 1: ✓ Success / ! Success with difficulty / ✗ Not completed
- Task 2: ✓ Success / ! Success with difficulty / ✗ Not completed

**Observations:** *(what they did, hesitated on, clicked)*

**Quotes:** *(exact words)*

### Post-test interview

**Experience score:** _ / 5 (1 = very hard, 5 = very easy)  
**Why this score:**  
**What was easy to understand:**  
**Where did they get stuck / confused:**  
**What would they like improved:**  
**Anything expected but couldn't find:**  
**If they could change one thing:**

---

## Napaul's 5 screens to test + improve

| # | Screen | What to watch for |
|---|--------|------------------|
| 6 | Select Date & Time | Do users understand the calendar + time slot UI? |
| 7 | Booking Details | Is purpose/participant count input clear? |
| 8 | Upload Document | Is the 2-doc requirement (proposal + list) obvious? |
| 9 | Review Booking | Do users read the summary before submitting? |
| 10 | Booking Submitted | Do they understand "Under Review" status? |

**Minimum 5 improvement points** across these screens (before/after for each).

---

## Participant log (fill during UT)

| # | Nickname | Age | Prior exp | Task 1 | Task 2 | Score |
|---|----------|-----|-----------|--------|--------|-------|
| 1 | Putt | 20 | Never (hotels closest) | — | — | 4 /5 |
| 2 | Mind | 22 | Yes — KMITL UAPP | Frequent event organiser | — | — | 3 /5 |
| 3 | Nhow | 20 | Never | None | — | — | 4 /5 |
| 4 | ching ching | 20 | — | Blocked — could not type in any field | — | 2 /5 (pre-fix build — blocking bugs) |
| 5 | cheesy | 20 | — | ✗ ECC-608 reads Busy in search, Unavailable when opened | ! Stuck on attendee slider | not scored, both tasks blocked |

**Participant sourcing.** Putt and Mind are **external to the class** — neither is enrolled
in UX/UI 2026 and neither is on this team. Nhow is **cross-group**: enrolled, but from
another group's team. None of the three had seen the design before, so their reactions are
first-impression, not informed review. That is stronger evidence than classmates testing
each other's work, and worth stating explicitly in the submission.

**Participants 4 and 5** (ching ching, 20 · cheesy, 20) were run later, against the
`08_10_2026` build. Both are **external**. Unlike 1–3 they were asked to *stress* the
prototype rather than walk the happy path, so their findings are failure-mode evidence:
they enumerate what breaks under real use, not what reads well.

> **Stated scope limit.** Figma does not carry state between pages, so complaints that
> depend on state persistence — text fields not accepting typing, a summary screen showing
> default values instead of the user's selections — are **out of scope** and are not logged
> as defects. They are properties of a Figma prototype, not of the design. Every finding
> below this line is independent of that limitation.

---

## Participant 1 — Putt (20)

*Moderator interview notes. Task-result fields not captured — see gap below.*

**Profile**
- Nickname: Putt
- Age: 20
- Used a booking app before? Never
- Related experience: closest thing is hotels

**Task result — NOT RECORDED.** Task 1 / Task 2 status (✓ / ! / ✗) was never written down. Only the post-test interview exists.

**Observations**
- Completed the booking steps without reported hesitation — no friction on the flow itself.
- On the confirmation screen, paused: unsure whether it was a fresh page or the "Booked" page, thought the booking might not have gone through, looked for something else to press to reveal the details.

**Quotes**
- "It is very clear, easy to read, easy to navigate"
- "Steps to booking a room was straightforward as it is structured like most Hotel booking apps, no hassle at all."
- "i wasnt sure if i was looking at a fresh page or the 'booked' page. I thought It didn't go through or i had to press something else to see the booked details."
- "unlabeled building sections (only number is shown) and summary screens are the main grudges"

**Post-test**
- Experience score: **4 / 5** — verbally qualified as "more realistically, 4.5". Logged as 4.
- Why this score: clear, easy to read, easy to navigate, above average overall. Deductions for unlabeled map sidebar sections and the summary/booked screens.
- Easy to understand: the booking steps — structured like hotel booking apps, no hassle.
- Stuck / confused: the Booked page. Unsure whether it was a fresh page or the confirmation; wanted a large clear "Booked" label.
- Expected but couldn't find: "Not really, everything presented was expected of a booking app."
- One change: label the map-page sidebar building sections with real names instead of 1, 2, 3, 4.

**Improvement points contributed**

| Screen | Issue | Improvement |
|--------|-------|-------------|
| Booking Submitted (S10) | Confirmation doesn't announce itself — reads as a new or blank page | Large explicit "Booked" heading + booking reference on the confirmation screen |
| Map page (outside S6–S10) | Sidebar building selectors are bare numbers | Replace numerals with building names |

---

**Feedback summary (submission text)** — the version used in [[uxui-ut-submission]].

Putt had never used a booking application before, and his closest experience comes from
hotel websites. His run produced only the post-test interview, because the task fields
were left empty during the session, and the confirmation screen gave him the most
trouble of anything he saw. It did not announce itself, so he read it as a new page or
an empty one and could not tell whether the booking had actually gone through. He also
found the building selector on the map unreadable, since it showed bare numbers from 1
to 7 with no labels attached to them. Both problems were corrected after the round. The
confirmation screen now opens with a large heading and the booking reference printed
underneath, and the floor pills read 1F through 7F.

---

## Participant 2 — Mind (22)

*External to the class. Not enrolled in UX/UI 2026, not on this team.*

**Profile**
- Nickname: Mind
- Age: 22
- Used a booking app before? Yes — **KMITL UAPP**
- Related experience: organises events regularly; booking rooms and venues is routine

**This is the most valuable participant on the list.** Mind is the only one with prior
experience of the actual comparator product, so their report is the only one that can
distinguish "this is hard" from "this differs from UAPP".

**Post-test**
- Experience score: **3 / 5**
- Why this score: "the overall flow between pages felt smooth and was easy to follow, but some features didn't work as expected, which made it difficult to complete the booking process."
- Easy to understand: the booking flow itself. Moving page to page felt smooth and natural. Praised the Next button being in a consistent bottom position, bright orange, with clear context.
- Stuck / confused: **four separate failures**, below.
- Expected but couldn't find: not every interactive button works — "If it does not function, better not add it or make it grey colour or something so I know it is not working just yet."
- One change: make every interactive element behave as expected, especially the Booking Details fields and the attendee slider, and prevent selecting more attendees than the room holds.

**Findings → disposition**

| # | Screen | Issue | Disposition |
|---|--------|-------|-------------|
| M1 | Booking Details (S7) | Couldn't type into Activity Name, Purpose, or Additional Notes | **Cannot fix.** Figma prototypes have no text input. Report as a tool limitation, not a design defect |
| M2 | Booking Details (S7) | Slider allowed 80 attendees on a 40-seat room; couldn't slide back down | **Partly fixed.** A dangling reaction with a null destination was firing first and swallowing the drag — removed. Real toggle restored. Capacity clamping is impossible: the component has only two states and Figma has no conditional logic |
| M3 | Action Confirm Sheet | "Request Edit" does nothing | **Fixed** — was a `CLOSE` reaction. Now navigates to Booking Detail - Approved (tracker row 17) |
| M4 | Cancel Sheet | "Request Cancellation" does nothing | **Fixed** — both buttons now have their own reaction instead of sharing one from the wrapping row (tracker row 18) |
| M5 | Back arrow | "Not working sometimes, or needs to click repeatedly" | **Addressed by removal.** `BACK` pops navigation history, so arriving via an overlay left nothing to pop and the first tap looked dead. Converting the six overlays to `NAVIGATE` (tracker row 19) removes those history states, and Profile's chevron had a literal duplicate `BACK` reaction (row 22) |
| M6 | All | Grey out non-functional controls | **Adopted.** Edit Profile, Settings and the header pencil are now greyed via the Button component's `State=Disabled` variant (tracker row 20) |

**The M1 honesty call.** Mind is right that the fields look editable and aren't. Three
options, and the deck should name the one chosen: (a) state it as a Figma limitation;
(b) grey the fields so they read as inactive; (c) tap a field to advance to
`Booking Details - Filled`. (c) demos well but is a small lie — a grader will try to type.
Recommend (a) stated plainly, because the finding is about the *tool*, not the design.

### Regression warning — Mind contradicts three rows of the tracker

Tracker rows 3, 4 and 5 claim improvements that the running prototype **does not deliver**.
Mind falsified all three by using it:

- Row 4 claims *"Capacity validation surfaces inline: Exceeds room capacity (40 seats)"*. Mind picked 80 on a 40-seat room with no objection from the UI.
- Row 5 lists the slider as an *improvement* over a −/20/+ stepper. The slider was the broken control.
- Row 3 claims *"Labels bound to the right fields"*. Mind couldn't enter text in any of them.

Those rows were built from a **visual diff**. Mind is the first behavioural evidence on
this project, and it disagrees with the visuals. Either fix the behaviour or soften the
claims — a grader who opens the prototype and then reads row 4 finds a false claim.

---

**Feedback summary (submission text)**

Mind books rooms and venues regularly through the KMITL UAPP, which gave her the
strongest basis for comparison of anyone in the round. Her session produced six
findings. The fields on the booking form look editable but cannot be typed into, which
is a limit of the Figma prototype rather than a design defect, and the attendee control
jumped to 80 on a room that seats 40 and then refused to move back down. The Request
Edit and Request Cancellation actions did nothing when she pressed them, and the back
arrow sometimes needed several taps before it responded. She also suggested that
controls which do not work should be greyed out, so that they read as inactive instead
of broken. Five of the six were fixed or addressed, and her suggestion was adopted
through the disabled variant of the button component.

---

## Participant 3 — Nhow (20)

*Cross-group. Enrolled in UX/UI 2026, but from another group's team.*

**Profile**
- Nickname: Nhow
- Age: 20
- Used a booking app before? Never
- Related experience: none

**Post-test**
- Experience score: **4 / 5** — reason given, verbatim: "easy to use and the steps were clear".
- Easy to understand: "the buttons are clear and easy to see, so I know what to do next."
- Stuck / confused: "I did not get stuck. Everything worked fine."
- Expected but couldn't find: no
- One change: "add a high-to-low and low-to-high choice to Sort by, and I think adding an Apply button to Sort would be nice."

**Findings → disposition**

| # | Screen | Issue | Disposition |
|---|--------|-------|-------------|
| N1 | Room Detail (all 4 variants) | Book Now bar covers part of the Booking Rules section | **Fixed** — see tracker row 13 |
| N2 | Sort Sheet | No ascending / descending choice | **Fixed** — see tracker row 14 |
| N3 | Sort Sheet | Wants an Apply button | **Declined, with reasoning.** Options already use radio buttons, so apply-on-tap is unambiguous. Airbnb, Booking.com and Agoda all apply a single-select sort immediately and close the sheet; Apply belongs to multi-criteria *filtering*. Adding it makes sort feel slower than it is |

**Read this result sceptically.** Nhow scores the build 4 / 5 and reports zero friction, but
Mind — on the same build — hit four dead controls. That is not tester variance; it is a **coverage gap**.
Neither run walked the edit/cancel path, and Nhow never attempted to type in a field.
"Everything worked fine" should never be printed without the path actually tested beside
it, or it reads as a polite soft rating. The task script needs "enter an activity name"
and "edit this booking" added as explicit steps.

---

**Feedback summary (submission text)**

Nhow reported no friction at all and completed the flow without hesitation, which is
worth reading with some care, because the same build produced hard failures for two
other participants. His two structural findings both held up under checking. The sticky
Book Now bar sat flush against the Booking Rules section with no clearance at all, and
it was already clipped by a single pixel on the unavailable variant of the room page.
The sort sheet also offered no choice between ascending and descending order. He asked
for an Apply button on the sort sheet as well, and that request was declined with
reasoning, since a single-select list applies on tap and the multi-step confirmation
belongs to filtering instead.

---

## Participant 4 — ching ching (20)

*External. Run against the `08_10_2026` build. Feedback given in Thai; paraphrased below with
her own framing kept where it carries meaning.*

**Profile**
- Nickname: ching ching
- Age: 20
- Task scoring: **not attempted.** She stopped to interrogate the prototype's fidelity before
  completing a task — see the quote below.
- Experience score: **2 / 5** — the lowest of the five, and the one that maps straight onto the
  defect list. Deductions for what blocked her: no field accepts typing, the two sign-in buttons
  behave differently, and the attendee selector moves only between 1 and 80. Scored against the
  build she ran, before the fix pass.

**The finding that outranks her list.** She could not tell whether the prototype was meant to
be interactive or was a static design showcase: *"is this supposed to work, or is it just
showing the design? If it's just design, then it all looks fine."* A first-time user could not
infer the intended fidelity from the artifact. Everything she reports below follows from that
uncertainty, so it is logged as its own finding, not folded into the bug list.

**Observations**
- Sign Up — cannot type in any field; Create Account does not respond
- Login — cannot type username or password
- Sign in with Google — does not respond
- Sign in with Microsoft — **opens a live OAuth session into a real account**
- Booking — the `+` control covers part of the booking details
- Booking Details — cannot type into the data fields
- Booking Review — summary shows the values set in the design, not the ones she selected
- Attendee count — selector moves only between **1 and 80**, nothing in between

**Scope decision.** The typing, summary and Google-button findings are Figma prototype
limits — out of scope per the stated limit above, except that the **Google / Microsoft
behaviour is inconsistent** and the Microsoft button is a live-demo hazard. Those two are
logged as defects (tracker rows 31).

---

**Feedback summary (submission text)**

ching ching stopped before the tasks and questioned the fidelity of the prototype
instead, because she could not enter text in any field and could not tell whether the
prototype was meant to be interactive at all. That ambiguity is the finding which
outranks everything else she said. Her typing and summary observations resolve to
prototype limits that Figma imposes, so they are recorded as a tool constraint rather
than a design fault. The asymmetry she surfaced between the two sign-in buttons was
real, and it was fixed afterwards.

---

## Participant 5 — cheesy (20)

*External. Run against the `08_10_2026` build. Ran the full path twice — same results both
times, so these reproduce.*

**Profile**
- Nickname: cheesy
- Age: 20
- Task 1 (book for 60 people) — **failed.** Target room ECC-608 shows as busy in Search
  Results but as unavailable when opened.
- Task 2 (ECC-603) — **blocked.** Could not set an attendee count, so could not proceed.

**The conceptual finding.** *"You do need to book the room and submit a proposal and stuff,
but if a room is available, then you can walk in without booking?"* The prototype never states
the rule connecting *availability* to *permission*. Then, on a room occupied right now:
*"maybe a DND sign instead of a cross — it makes ECC-608 seem unusable or on maintenance. Or a
clock with a yellow colour."* He is describing a semantic error, not a styling preference: red
cross means **out of service**, and an occupied room is not out of service. Logged as tracker
row 25.

**Observations — functionality**
- Attendee slider snaps between 1 and 80 only
- Tried to trigger the over-capacity error deliberately; could not get back to a valid state
  afterwards — and from then on *normal* runs reported exceeding capacity at 1 attendee
- Back in the confirm-booking step does not go back
- Reviews can be submitted on **rejected** and **cancelled** bookings
- A busy room is treated as unavailable (ECC-608)
- Book Now on an unavailable room still works from the **Details** tab, but is dead on the
  **Reviews** tab. On available rooms both tabs work

**Observations — smaller**
- ECC-SIIE-E12 slideshow: sometimes it slides, sometimes it needs a tap; behaviour is not
  consistent between positions
- The slideshow can be dragged while behind the room card
- Booking History does not reset scroll — arriving from Review or Upcoming lands the list
  scrolled down, so a past booking appears pushed away
- Booking Details: the connector line between the date / details bubbles renders ahead of the
  current section

**Suggestions**
- Home profile avatar should route to Profile — he inferred the dropdown cannot be a page of
  its own, so the avatar is the natural entry
- **Cannot get out of Sort By** — the search background behind the popup is gone
- **Cannot get out of Notifications**

**Improvement points contributed**

| Screen | Issue | Improvement |
|--------|-------|-------------|
| Attendee slider (S7) | Two values only — 1 or 80 | Discrete capacity presets or a numeric stepper (tracker row 23) |
| Search → Room Detail | Same room reads Busy then Unavailable | One status vocabulary (tracker row 24) |
| Status Badge — Busy | Red cross reads as broken | Amber clock / DND sign (tracker row 25) |
| Sort By, Notifications | No exit affordance | Restore backdrop + close (tracker row 28) |

---

**Feedback summary (submission text)**

cheesy ran the full booking path twice and reproduced his results on both passes, so
his findings are stable rather than incidental. He failed the task of booking for 60
people. Room ECC-608 reads as busy in the search results but as unavailable when the
room is opened, which means one real state carries two different words, and he then
became stuck on the attendee control. He reported that a red cross badge reads as
broken, since the busy state used the same red and the same icon as rejected, and that
the sort sheet and the notification sheet both left him with no way out. This pass
produced change log entries 23 through 28 and drove five of the six fixes explained in
the submission.

---

**Experience score: not given.** He was ready to score both tasks and neither could be completed, so no rating was recorded. Task 1, the booking for 60 people, was blocked by the ECC-608 status wording, since the room reads as busy in Search Results and as unavailable when opened. Task 2 on ECC-603 was blocked by the attendee control, which snapped between 1 and 80 and would not move back down, after which even a booking for one person reported that it exceeded the room capacity and a page refresh did not clear it. Source, his written feedback after the session, 2026-10-10.

---

## Improvement tracker

Two sources, and the distinction matters. **Rows 1–12** come from a visual diff of the six
prototype versions on disk. **Rows 13–22** come from usability testing — real people using
the prototype — and are the stronger evidence, because three of the earlier rows turned out
to claim improvements the running prototype did not actually deliver (see the regression
warning under Participant 2).

Every row cites its before/after export, so each claim can be re-checked against the files
rather than taken on trust — with the caveat about rows 1–12 noted below.

**Version chain:** `old/` → `1-10-2026/UX/` → `2-10-2026/UX/` → `Final_Prototype_6_10_2026/` → `07_10_2026/` → `08_10_2026/`

| # | Screen | Issue in the earlier version | Improvement | Before → After |
|---|--------|------------------------------|-------------|----------------|
| 1 | S6 | Stepper was 4 unlabelled dots — no way to tell how many steps remained | Numbered, labelled stepper: 1 Date · 2 Details · 3 Docs · 4 Review | `old/s6.png` → `08_10_2026/Napaul/User/Booking Flow.png` (frame 1) |
| 2 | S6 | Room card was a flat orange swatch — no photo, no status, no capacity | Photo thumbnail + status/category/capacity chips (Available · Co-working · 40 Seats) | `old/s6.png` → `1-10-2026/UX/6 · SELECT DATE & TIME.png` |
| 3 | S7 | Labels didn't match their fields — "NUMBER OF PARTICIPANTS" carried the placeholder "Enter Activity Name"; label sat outside its card; purpose dropdown overlapped the card below | Labels bound to the right fields: "Number of attendees" above the stepper, "Enter participant count" in the count field | `old/s7.png` → `old/s7-fixed.png` |
| 4 | S7 | Attendee count had no relationship to room capacity — an impossible number looked fine | Capacity validation surfaces inline: "Exceeds room capacity (40 seats)" | `old/s7.png` → `08_10_2026/Napaul/User/Booking Flow.png` (frame 3) |
| 5 | S7 | Attendee count was a −/20/+ stepper — slow for large numbers | Slider control with an orange value bubble | `old/s7.png` → `2-10-2026/UX/7 · BOOKING DETAILS.png` |
| 6 | S8 | Submit CTA was clipped to a 7px sliver under the nav bar — effectively unreachable | CTA fully visible, relabelled "Continue to review" | `1-10-2026/UX/8 · UPLOAD DOCUMENTS.png` → `2-10-2026/UX/8 · UPLOAD DOCUMENTS.png` |
| 7 | S9 | Room status chip read "Upcoming" on a booking still under review — wrong word for that state | Chip corrected to "Available" (green) | `1-10-2026/UX/9 · REVIEW BOOKING.png` → `2-10-2026/UX/9 · REVIEW BOOKING.png` |
| 8 | S9 | Summary opened with Room/Date/Time — the user's own activity was buried | Activity-first row order: Activity Name, Room, Date, Time, Purpose, Attendees | `old/s9.png` → `1-10-2026/UX/9 · REVIEW BOOKING.png` |
| 9 | S9 | Attachments showed placeholder text "Attachment title / Description · 5.4 MB" twice | Real filenames: `proposal.pdf · 5.4 MB`, `participants.pdf · 1.2 MB` | `old/s9.png` → `1-10-2026/UX/9 · REVIEW BOOKING.png` |
| 10 | S10 | Zero approval visibility — a static "Under Review" pill, no sense of what happens next | 3-node approval tracker added: 1 Submitted · 2 Reviewing · 3 Approved | `old/s10.png` → `1-10-2026/UX/10 · BOOKING SUBMITTED.png` |
| 11 | S10 | Confirmation screen didn't read as a confirmation (matches Putt's finding) | Headline "You're all set!" + confetti; "Back to home" promoted from underlined text to an outlined button | `1-10-2026/UX/10 · BOOKING SUBMITTED.png` → `08_10_2026/Napaul/User/Booking Flow.png` (frame 7) |
| 12 | S6–S10 | Bottom nav stayed live inside a linear 4-step wizard, inviting exits mid-flow | Nav removed from every flow screen; CTA height 42px → 55px for touch target | `1-10-2026/UX/6,7,9,10` → `2-10-2026/UX/6,7,9,10` |
| 13 | Room Detail (all 4 variants) | Booking Rules section sat flush against the sticky Book Now bar — 0px clearance, and already 1px clipped on *Unavailable*. Reported by Nhow | `Content` bottom padding 0 → 104: 24px clearance above the bar, 90–105px of scroll headroom | `assets/ut/2026-10-10-prefix/before/08-room-detail-available.png` → `assets/ut/2026-10-10-prefix/after/08-room-detail-available.png` |
| 14 | Sort Sheet | Sort options had no ascending / descending choice. Requested by Nhow | New `Sort Direction` component — two chips wired both ways with `CHANGE_TO`, so it toggles in the prototype. Sheet 296 → 335px | `assets/ut/2026-10-10-prefix/before/09-sort-sheet.png` → `assets/ut/2026-10-10-prefix/after/09-sort-sheet.png` |
| 15 | Map (floor selector) | Sidebar showed bare numerals 1–7, unreadable at a glance. Reported by Putt | Labels → `1F`–`7F` (`B` unchanged). Fits the existing 24px pill, zero relayout | `assets/ut/2026-10-10-prefix/before/10-map.png` → `assets/ut/2026-10-10-prefix/after/10-map.png` |
| 16 | Slider (Booking Details) | A dangling reaction with `destinationId: null` was firing before the working one and swallowing the drag — the control could not be moved back down. Reported by Mind | Dangling reaction removed; `ON_CLICK` added alongside `ON_DRAG` on both states, since drag inside a scroll region is unreliable on touch | component-level fix; inherited by all 10 instances |

| 17 | Action Confirm Sheet | "Request Edit" carried a `CLOSE` reaction — confirming an edit did nothing. Reported by Mind | Now navigates to **Booking Detail - Approved**, which is also where Edit Booking is reached from | prototype wiring — no visual delta |
| 18 | Cancel Sheet | "Keep Booking" and "Request Cancellation" were indistinguishable: neither had its own reaction, so both inherited a single `CLOSE` from the wrapping row. Reported by Mind | Keep Booking → explicit close; Request Cancellation → **Booking History - Upcoming** | prototype wiring — no visual delta |
| 19 | 6 overlay interactions | Overlay destinations were **402×912 wrapper frames** (screen 874 + attribution label) centred in an 874 viewport — 19px clipped off each edge, worse with browser chrome. This is the "confirm banner clipped off screen" seen on a real S24/S26-class phone | All six rewritten **`OVERLAY` → `NAVIGATE`**. Sheets already bake their own dim, so navigating presents them correctly with no position to get wrong | prototype wiring — no visual delta |
| 20 | Profile | **My Bookings** and **Logout** were both dead. **Edit Profile** and **Settings** were also dead, but no such screens exist anywhere in the file — they can't be wired to anything | My Bookings → Booking History - Upcoming; Logout → Sign In. Edit Profile, Settings and the header pencil **greyed out** using the Button component's own `State=Disabled` variant, so dead controls read as inactive instead of broken — Mind's own suggestion (M6) | `Mawin / User / Profile` |
| 21 | Booking Detail - Completed | Both `View Location` buttons pointed at an orphan duplicate of the Map that sat outside every section | Repointed to the canonical Map (`4673:10461`). The duplicate is now unreferenced | prototype wiring — no visual delta |
| 22 | Profile (header) | Back chevron carried **two identical** `ON_CLICK → BACK` reactions | Deduped to one | prototype wiring — no visual delta |
| 23 | Slider (Booking Details) | **Root cause found.** The control is a *2-variant component*, not a continuous slider: `Content` → `CHANGE_TO` `4293:8482`, `Marker` → `CHANGE_TO` `4293:8548`. Two variants means exactly two reachable values, so it snaps 1 ↔ 80 and a count like 60 is unsettable. Because the default lands on the high variant, capacity validation then fires on *valid* input — cheesy got "exceeds room capacity" at 1 attendee. Reported by cheesy | *Pending* | `4293:8483` (component) → all S7 instances |
| 24 | Room status (ECC-608) | Same room reads `Busy` in Search Results but `Unavailable` in Room Detail — two variants for one real state. Reported by cheesy | *Pending* — pick one vocabulary | Search Results → Room Detail |
| 25 | Status Badge — Busy | `Busy` is red `#DC2626`, identical to `Rejected`. An occupied room therefore reads as out-of-service, which is how cheesy read ECC-608. His proposed fix — DND sign or amber clock | *Pending* — Busy → amber | `Status Badge` set |
| 26 | Room Detail — Book Now gating | Works on an Unavailable room from the **Details** tab, dead on the **Reviews** tab; both work when available. Inconsistent gate. Reported by cheesy | *Pending* | Room Detail × 4 variants |
| 27 | Booking Detail — reviews | Reviews can be submitted on `Rejected` and `Cancelled` bookings. Reported by cheesy | *Pending* — gate on status | Mawin / Booking Details |
| 28 | Sort By sheet + Notifications | **Both trap the user** — no exit, backdrop gone. This is a regression from row 19: rewriting `OVERLAY → NAVIGATE` removed the clipping *and* the dismiss affordance. Reported by cheesy | **Fixed 2026-10-09** — see row 43. The scope turned out to be **five** overlays, not two | Overlays |
| 29 | Confirm Booking dialog | Back does not return to the previous step. Reported by cheesy | *Pending* | Overlays |
| 30 | Booking Details (S7) | `+` control overlaps the booking details area. Reported by ching ching | *Pending* | S7 |
| 31 | Sign In (Auth) | **Microsoft sign-in opens a live OAuth session into a real account; Google is inert.** Inconsistent affordance, and a live-demo hazard — on a projector this signs the examiner into a personal account. Reported by ching ching | *Pending* — make both inert | `Authentication.png` |
| 32 | Booking History | Scroll position not reset on entry from Review or Upcoming, so the list lands scrolled down. Reported by cheesy | *Pending* | Mawin / Booking History |
| 33 | Booking Details | Connector line between the date / details bubbles renders ahead of the current section. Reported by cheesy | *Pending* | Booking Details |
| 34 | Room Detail — slideshow | Responds to drag in some positions and tap in others; can be dragged while behind the room card. Reported by cheesy | *Pending* | Room Detail |
| 35 | Home | Profile avatar does not route to Profile. Reported by cheesy | *Pending* | Chonchanok / Home |
| 36 | Attendee count (Booking Details, Edit Booking) | Root cause from row 23: the control is a 2-variant component, so exactly two values exist and a 60-person booking is unsettable. Replaced with an **`Attendee Preset`** chip row (10 / 20 / 30 / 40) whose values come from the selected room's capacity — an over-capacity count is now unreachable rather than rejected. Reported by cheesy | **`before/11-attendees-control-booking-details-filled.png` → `after/11-attendees-control-booking-details-filled.png`** · `before/12-attendees-control-edit-booking.png` → `after/12-attendees-control-edit-booking.png` |
| 37 | Booking Details — capacity warning | `capacity-warning` (`4528:4169`) was a plain TEXT layer, permanently `visible: true`, hardcoded onto the Filled screen. It was never computed from anything — it asserted "Exceeds room capacity (40 seats)" regardless of the value entered, which is why cheesy got it at 1 attendee. Removed from all 5 copies | no visual delta — the label is deleted, not hidden |
| 38 | ECC-603 capacity | One room carried **three** capacities: `Cap: 15` (Home card), `30 Seats` (Search Results), `40 Seats` (Room Detail, booking flow, history, and the warning text). Normalised to 40 everywhere | text-only: Home card + Search Results row. **No before capture** — a single-value text fix, verified by reading the values back |
| 39 | Filter — Capacity | Same 2-variant Slider, which left capacity stuck at 1. Replaced with two `Capacity Select` dropdowns, `Min 10 ▾` / `Max 60 ▾`. A range wants two ends, so presets were the wrong shape here. Reported by cheesy | **`before/13-capacity-control-filter.png` → `after/13-capacity-control-filter.png`** |
| 40 | Chip + Filter Select | Both were **23px** tall — one pixel under the WCAG 2.5.8 minimum target of 24px. Both raised to 28 | component-level; not screen-captured |
| 41 | Filter Select — self-inflicted regression | Adding the disclosure chevron to the shared `Filter Select` component also chevroned **Room Type** and **Facility Equipments**, which are instances of it — both rows grew and lost density. Reverted to the plain component, and cloned a separate `Capacity Select` so the chevron applies to capacity only. Lesson: check who else uses a component before changing it | visible in the row-39 pair |
| 42 | Sign In — SSO buttons | **The recorded issue was wrong.** The resume list said Microsoft opened a live OAuth session. It does not, and never did — verified three ways: zero `URL`-type prototype actions across all 632 reaction-bearing nodes on the Screens page, zero real hyperlinks (`n.hyperlink`) page-wide, and direct inspection of both SSO instances. The real defect was **asymmetry**: Microsoft navigated onward, Google had **no reaction at all** — a dead button mid-demo, which is the honest version of what was observed. Both now `ON_CLICK` → `NAVIGATE` → `Home`, byte-identical reactions | behaviour-only, no pixel delta. `before/14-signin-sso-buttons.png` → `after/14-signin-sso-buttons.png` are bit-identical — recorded as the pair because the claim is about reactions, not rendering |
| 43 | All five overlays — restore `OVERLAY` | Root cause of row 28, and wider than recorded: an earlier rewrite changed every overlay trigger from `OVERLAY` to `NAVIGATE`. Because the overlay frames are **transparent wrappers** whose scrim lives on an inner `Screen` child, `NAVIGATE` presented the frame with nothing behind it — cheesy's "the search background behind the popup is gone". `CLOSE` also became a no-op, since there was no longer an overlay to close, which is why every sheet trapped. **Six live callers restored to `OVERLAY`**: S9 Review → Confirm Sheet · Edit Booking → Action Confirm · Edit Booking → Cancel Sheet · Home bell → Notification · Search Results → Sort Sheet · Search Results Empty → Sort Sheet. Also added the missing `ON_CLICK → CLOSE` to Confirm Sheet's `Screen`, which alone among the five had no dismiss at all | **no pixel delta by construction** — the frame contents are unchanged and the background only exists at runtime, so a screenshot cannot show it. Verified structurally instead: all five now report a `CLOSE` exit *and* an `OVERLAY` inbound trigger. Follows the row-37/38/40 precedent of describing rather than picturing |
| 44 | Stepper connector — all 6 live steppers | Cheesy: "the connector line between the date / details bubbles renders ahead of the current section". **Not an off-by-one** — the file was internally consistent under convention A (*N* filled segments on step *N*), which is exactly why the segment leaving the current step was already orange. Flipped to convention B (*N−1* filled). The tiebreaker was **step 1**: under A the Select Date stepper is wrong twice (its label is navy *and* its outgoing segment is filled); under B it is correct on every element. Also removed a genuine artifact — every "empty" segment carried a **1px orange nub** (the author's zero-width placeholder, plainly visible at 4× zoom), now hidden. Exactly one segment emptied per stepper | `before/15-stepper-connector.png` → `after/15-stepper-connector.png` |
| 45 | Stepper labels — colour drift | **Found while fixing row 44, left unresolved on purpose.** The six live steppers use **three** different dark text colours — `#1A2340`, `#111827`, `#000000` — none of which is the file's documented primary navy `#1B2A5B`, and they disagree on whether reached steps are orange or navy: Select Date `#1A2340, #111827×3` · Booking Details - Empty `#1A2340×2, #111827×2` · **Booking Details - Filled `#E8622D×2, #000000×2`** · Upload Documents - Empty `#1A2340×3, #111827` · **Upload Documents - Uploaded `#E8622D×3, #000000`** · Review `#1A2340×4`. The tell: the *empty* and *filled* variants of the **same step** disagree — two screens mark reached steps orange, four mark them navy | **Not fixed — needs a palette decision**, and it is the same call as the two-navies item on the resume list, so it should be made once and not here. An earlier pass of this fix wrote `#1B2A5B` onto two labels and was **reverted**: that would have introduced a *third* navy rather than resolving the two. Recorded so the drift is not rediscovered later as a surprise |
| 45a | Stepper labels — drift resolved, **steppers only** | Row 45 fixed on 2026-10-09 by the narrower of the two options: the six live steppers were unified to exactly **two** colours — `#1A2340` for a reached step, `#111827` for one not yet reached — and the whole rest of the file was left alone. This removed `#E8622D` and `#000000` from the steppers entirely. The point is that the **empty and filled variants of the same step now agree exactly**: Booking Details - Empty and - Filled both read `#1A2340, #111827, #111827, #111827`; Upload Documents - Empty and - Uploaded both read `#1A2340, #1A2340, #111827, #111827`. Before, one of each pair marked reached steps orange and the other navy | `before/19-stepper-label-colours.png` → `after/19-stepper-label-colours.png`. The full-file palette consolidation from row 45 is still open and still wants one decision — this does not pre-empt it |
| 46 | **Status Badge — the contrast recolour never propagated** | The audit records the contrast fix as "6 fill swaps, propagates to all 31 screens". **It did not propagate.** The `Status Badge` component set was recoloured correctly — I verified every variant — but each live instance carried an **instance-level fill override** still holding the old value, so **all 33 live badges rendered the old colours**: `#059669` ×17, `#DC2626` ×9, `#D97706` ×3, `#E8622D` ×1, `#9CA3AF` ×1. The only two that looked right were the variants that never changed (`#6B7280`). Found by comparing each instance's *rendered* pill fill against its variant's *component* fill — a check the recolour pass had no reason to run, which is exactly why it was missed. **Fixed 29 of 32 live instances** (3 were already correct) and **33 more in the visible RT device matrix**. Re-verified after writing: **0 mismatches remain on live screens** | `before/17-badge-colour-propagation.png` → `after/17-badge-colour-propagation.png`. Search Results: three alarming red ⊗ badges become amber. This is the fix behind cheesy's row-25 "red cross reads as broken" — the colour half of it, at least |
| 47 | **Status Badge — strokes missed, and Busy's icon** | Two further defects in the same family, found by eye at 4× rather than by any script. **(a) The stroke was never recoloured.** Seven of ten variants kept a 1px *old*-colour stroke, so every recoloured badge wore a halo of its previous colour — amber pill, bright red ring. The three variants that matched were exactly the three whose fill never changed, which is what proves the convention is `stroke = fill`. Fixed on the component set **and** on 62 instances across the live screens and the RT matrix; component-set edits alone had already proved insufficient twice in one session. **(b) Busy shared its icon with Rejected** — both `Lucide / circle-x`. That was cheesy's row 25: the colour half was row 46, the icon half was still open. `Status=Busy` swapped to `Lucide / clock`, which is what "Busy until 15:00" actually says. | `before/18-busy-badge-icon-and-stroke.png` → `after/18-busy-badge-icon-and-stroke.png`. Final sweep: **65 badges with a known variant, 0 colour mismatches.** The one hit it reported is `Rejected` at `#DC2626` — its correct value, flagged only because it shares a hex with the old Busy red |
| 48 | Two badge oddities — **noted, deliberately untouched** | **(a)** `Booking Status Badge` (`4197:6802`) is a **navy `#1B2A5B`** badge reading "Upcoming" on the Select Date booking card — the same word the amber `Upcoming` variant uses, in the primary navy instead. Its component set reports *"Component set for node has existing errors"*, so its variant cannot even be read. It is not part of the 10-variant colour system and navy/white passes contrast comfortably, so it is not an accessibility problem — it is a naming one. **(b)** The hidden `Frame 14` workbench still holds old-coloured copies throughout; invisible, and not worth touching | No capture. Recorded so neither is rediscovered as a surprise during the exam |

Rows 13–22 are the first entries in this tracker with **behavioural** evidence behind them
(a participant using the prototype), rather than a screenshot diff. They are also the first
whose cited paths actually resolve on this machine.

**Rows 36–41 are the fixes applied for those findings**, made 2026-10-09 against the live file. Rows 36, 39 and 41 carry before/after captures under `assets/ut/`; 37, 38 and 40 are structural or text-only and are described rather than pictured. Row 41 is included deliberately — it is a regression introduced while fixing row 39, caught by screenshot, and reverted. Recording it is more useful than hiding it.

**Rows 23–35 come from a deliberate stress pass** (participants 4 and 5), not a happy-path walk.
That is why they are denser and more negative than 13–22: the earlier runs were not looking for
failure modes. Two of them are **regressions caused by earlier fixes** — row 28 (from row 19's
overlay rewrite) and row 23 (from row 16's slider work). State-dependent complaints are excluded
under the scope limit stated above.

### Prototype integrity pass — rows 17–22

Rows 17–19 and 21–22 are **wiring only**: not one pixel moved, so they have no before/after
image and shouldn't get one. They were found by auditing the reaction graph rather than by
looking at screens, and every one of them was a button that did nothing or went somewhere
wrong when a participant pressed it.

Row 19 is the one worth explaining in the deck. The symptom — a confirmation banner clipped
off the bottom of the screen — looked like a layout bug and isn't one. The overlay's
destination is a 912px-tall wrapper and its position was `CENTER`, so centring it in an
874px viewport overflowed 19px at each end. The fix isn't to move the overlay; it's to stop
using overlays for full-screen sheets. **Symptom and cause were in different subsystems**,
which is why two earlier passes over the layout missed it.

**Rows 20–22 have no before/after capture.** The Profile screen wasn't in the `assets/ut/`
set, and the greying can't be reconstructed backwards. If a Profile pair is wanted for the
deck, it needs a manual "before" or the row stays text-only.

**Evidence note on rows 1–12.** Those rows cite `old/`, `1-10-2026/UX/`, `07_10_2026/`,
`08_10_2026/`. None of those paths exist in this vault or in `~` — they are not on this
machine. Either locate them (likely OneDrive; `~/Downloads/OneDrive_1_10-8-2026/` holds
`Group 2 … Group 9`) or stop citing paths that can't be opened. The tracker's claim that
every row "can be re-checked against the files rather than taken on trust" does not
currently hold. The `assets/ut/` captures were taken specifically so the newer rows do.

**Capture convention going forward.** `assets/ut/2026-10-10-prefix/before/` and `assets/ut/2026-10-10-prefix/after/` hold ten
screens each, exported from Figma at 2× (804×1748). Eight of the ten pairs are
**byte-identical** — only `09-sort-sheet` and `10-map` changed. That is the point: it
demonstrates the Row 13 fix produced zero visual regression at rest, which a
screenshot-only tracker row could never show.

Row 10 + row 11 are the strongest pairing available: a real user (Putt) named the
confirmation screen as confusing, and the tracker plus the headline change answer
it. That's evidence → change, not change alone.

### Regressions and defects — fix before submitting

Found during the same diff. These weaken the before/after story if they show up
in the "after" screenshots.

- **S6 lost a feature.** `old/s6.png` had a time-slot legend — ○ Available · ● Selected · ● Unavailable — with greyed-out unavailable slots. The newest build has plain bordered chips, no legend, no unavailable state. Either restore it or be ready to say why it went.
- **S7 board is mid-state.** `08_10_2026/Napaul/User/Booking Flow.png` frame 2 shows the Purpose dropdown with the literal placeholder text "Selected value" — a Framer/prototype artifact, not a design. Never let that into a submitted screenshot.
- **Room doesn't match the task.** The newest S6 card reads "Co-working (ECC-603) · Floor 0", but the test task is "book ECC811 in the ECC Building". `old/` correctly showed ECC811. Align the screenshots to the task or the after/before looks like a different flow.
- **07-10 and 08-10 are near-identical.** Board diffs came out at 0.0007 (Authentication), 0.0006 (Booking Flow), 0.0065 (Overlays) — the only real movement is the Notifications panel. The visible before/after is `old/` → `08_10_2026/`, **not** 07 → 08. Use `old/` as the "before".
- **`old/` has no S1–S5.** No before/after claim is possible for those screens. Out of scope here (S6–S10), but it also means you can't illustrate the map or search screens this way.

### For the deck — slide 23 (`Before & After:`) draft

Visual slide. **Three pairs**, one row, captured from the prototype at equal
scale. Three, not twelve: at slide size a phone screenshot is ~1.5" wide, so
only changes that survive thumbnail size belong here. Captions are the whole
text budget — no file paths on the slide.

Chosen because each is visible without zooming, and together they cover the
start, middle and end of the flow:

| Pair | Before | After | Caption |
|------|--------|-------|---------|
| S6 Select Date & Time | `old/s6.png` | `08_10_2026/…/Booking Flow.png` frame 1 | Unlabelled dots → numbered, labelled steps |
| S8 Upload Documents | `1-10-2026/UX/8 · UPLOAD DOCUMENTS.png` | `2-10-2026/UX/8 · UPLOAD DOCUMENTS.png` | Submit button clipped under the nav → fully visible |
| S10 Booking Submitted | `old/s10.png` | `08_10_2026/…/Booking Flow.png` frame 7 | Static status → 3-step approval tracker |

Left out deliberately: the S7 label fix is real but text-level — it needs zoom
to read, which is exactly what a slide can't ask for. It lives on slide 24.

**Title note:** the placeholder reads `Before & After:` with a dangling colon.
Drop the colon or finish the sentence.

### For the deck — slide 24 (`Improvements`) draft

**S6 · Select Date & Time**
- Stepper: 4 unlabelled dots → numbered steps (1 Date · 2 Details · 3 Docs · 4 Review)
- Room card: flat colour swatch → photo + status and capacity chips

**S7 · Booking Details**
- Labels now bind to the right fields — "Number of attendees" over the count, "Enter participant count" inside it
- Capacity enforced inline: "Exceeds room capacity (40 seats)"
- Attendee count: −/+ stepper → slider with value bubble

**S8 · Upload Documents**
- Submit CTA was clipped under the nav bar; now fully visible, reads "Continue to review"
- Additional Documents collapses behind a "+" header

**S9 · Review Booking**
- Status chip "Upcoming" → "Available" — the old word described the wrong state
- Summary opens with the activity, not the room
- Attachments show real filenames instead of placeholder text

**S10 · Booking Submitted**
- 3-step approval tracker: Submitted → Reviewing → Approved
- Headline "You're all set!" + confetti; "Back to home" is a button now, not underlined text

**Across every flow screen**
- Bottom nav removed — a linear wizard shouldn't offer exits mid-task
- CTA height 42px → 55px

Twelve points against a required five. If the slide runs long, cut S6–S8 to one
bullet each before cutting anything from S10 — that's where the user finding and
the design change actually meet.

### Deck status — 2026-10-09

Verified by reading the slide XML of the Canva export `KMITL-B App.pptx`
(30 slides). Slides 1–16 carry text. **Slides 17–30 contain zero picture
elements and only their titles** — so "Final UI holds the screenshots" is not
true of this file. Either the export is stale or the images were never placed.
Re-export from Canva before building on it; the rest of the plan depends on it.

| Slides | Section | Needs | Blocked on |
|--------|---------|-------|------------|
| 17–19 | Components | Screenshot per component + one-line description | Figma export |
| 20 | Usability Principles | Text | Draftable now |
| 21 | Accessibility & Test Iterations | Text — consolidates the contrast audit already on slides 14–15 | Draftable now |
| 22 | Feedback | Participant feedback | **the 4 testers** |
| 23 | Before & After | drafted above | paste into Canva |
| 24 | Improvements | drafted above | paste into Canva |
| 25–29 | Final UI | Images | the re-export check |
| 30 | AI Use Log | Disclosure | Napaul's own account |

**Slide 22 is the long pole.** It is the only remaining slide that depends on
other people, and the one that makes the deck defensible. Everything else can be
finished tonight.

**Slide 30 is a disclosure.** Build it from what actually happened, not from a
plausible reconstruction. An inaccurate AI-use log is worse than no slide at all.

---

## Checklist

- [ ] Hi-fi prototype built in Figma (screens 6–10, clickable)
- [ ] Grid enabled on all 5 screens
- [ ] Figma view-mode link ready
- [ ] Roles assigned in group
- [ ] Run UT Round 1 + Round 2, record notes
- [ ] Identify ≥5 improvement points from feedback
- [ ] Update UI, capture before/after screenshots
- [ ] Export PDF 1: all screens with grid
- [ ] Export PDF 2: each screen alone, no grid
- [ ] Submit Figma link (view mode)

---

*Hub → [[uxui-facility-booking-project]] · Submission document → [[uxui-ut-submission]] · Status → [[uxui-project-state]]*
