---
title: "Week 7 — Crazy 8s & Storyboarding"
tags: [uxui, assignment, group-work, ideation, storyboard]
status: draft
created: 2026-08-11
due: 2026-08-24
points: 5
type: group-work
submit: GroupNumber_Crazy8s_Storyboard.pdf
---

# Week 7 Assignment — Crazy 8s & Storyboarding

**Due:** Aug 24, 11:59 PM · 5 pts · Group work · One member submits

---

## Learning Outcomes

- Pick a worthy problem from Week 6 feature order
- Generate wide range of ideas via Crazy 8s before deciding
- Narrow to one concept using criteria, not loudest voice
- Tell concept as storyboard (context + action + user-felt outcome)
- Convert storyboard to checkable user stories
- Write acceptance criteria (done = done, not vague)
- Revise after critique with reasons

---

## 4-Part Submission

### Part 1 — HMW + Why

- Open Week 6 feature order → pick one item with room for multiple designs
- Write as "How might we…" question + one-line reason why
- May reuse Week 5 HMW if it still fits

> **HMW:** How might we keep every user informed of room status — before, during, and after booking — without them having to ask?
> **Why:** Merges HMW 1 (live availability) + HMW 2 (automated notifications). Both personas fail at the same root: no proactive status signal — Prof. New walks to check doors, students chase staff on LINE. Combined HMW covers discovery (what's free) and approval progress (where is my request) in one design space. Rank 1 + 2 in build order, both Kano Basics. Still allows multiple design directions: push vs. pull, map vs. feed, ambient display vs. on-demand query.

---

### Part 2 — Crazy 8s (every member)

- Each person fills **own** 8 boxes (paper photo ok)
- Collect all sheets into single team file
- ⚠️ One sheet for whole team = half marks

#### Crazy 8s — Idea Bank (generated from Week 6 context, use as inspiration for individual sheets)

> Each team member picks 8 boxes from different angles. Do NOT all draw the same thing.

| Box | Concept | What it looks like |
|-----|---------|-------------------|
| 1 | **Map-First Floor Plan** | Interactive campus floor plan. Each room = colored circle: 🟢 Free / 🔴 Busy / 🟡 Pending. Tap → timeslots + book. |
| 2 | **Status Board (Airport-Style)** | All rooms as rows, next 4 hours as columns. Blocks fill in like a departure board. Glance and go — no interaction needed. |
| 3 | **Calendar Grid** | Rooms = columns, time = rows (Google Calendar style). Gray = booked, white = free. Filter by capacity / equipment. |
| 4 | **Scrollable List + Live Badges** | List sorted by "soonest free." Each row: room name, capacity icon, badge (Free Now / Free at 3pm / Fully booked). |
| 5 | **LINE-Bot / Chatbot** | Type "free room 2–4pm Thursday, 30 pax." Bot replies with 3 options + one-tap confirm. Meets users in LINE. |
| 6 | **Approval Timeline (Package-Tracker)** | After submit → step tracker: Submitted → Staff Review → Dept Head → Approved. Like Grab order tracking. Status visible without messaging anyone. |
| 7 | **Room Info Card** | Each room has a detail page: photo, capacity, equipment, live status, next free slot. Tap from map or list. All info in one place — no asking staff what's inside. |
| 8 | **Subscription + Push Alert** | Follow specific rooms. When a booking is cancelled → instant push: "ECC-301 free 2–4pm. Tap to grab it." |

#### Member tracking

| Member | ID | Sheet included? | 8 boxes? |
|--------|----|----------------|---------|
| Norpoom | 67011138 | ✅ | ✅ |
| Teammate 2 | — | ✅ | ✅ |
| Teammate 3 | — | ⬜ pending | — |

#### Sheet summaries

**67011138 Norpoom (Image #3)**
1. Map-First Floor Plan — interactive campus map, rooms labeled (L01–L05, etc.)
2. Status Board — list: ECC 601 Booked 12:00 / ECC 607 Available / ECC 403 Available
3. Calendar Grid — ECC 601 time grid
4. Scrollable Lists — ECC 603 free now / ECC 604 free 5pm / ECC 605 Booked
5. Chatbot — conversational query interface
6. Approval Timeline — step tracker nodes
7. Room Info — detail card with management widget
8. Push Alert — notification UI

**Teammate 2 (Image #2)**
1. Calendar showing available dates — August month view, dates highlighted
2. Interactive map showing available rooms — EN-01/02/03 floor layout
3. Booking Progress — EN-01: Pending → Complete step flow
4. Notify user when status changes — lock screen push notification
5. Document upload — EN-01 card with upload button
6. Recommend new room if rejected — EN-05 with available time shown
7. Upcoming booking reminder — lock screen "today booking" notification
8. Cancel booking — EN-01 card with ⊗ Cancel button

---

### Part 3 — Chosen Concept + Storyboard

**Concept name (≤5 words):** See It. Book It. Track It.

**How it answers the HMW:** Combines map-first live availability (HMW1) with approval timeline tracking (HMW2). User sees what's free without walking anywhere, books in-app, then watches approval progress without messaging anyone.

**Selection method:** Silent vote → discussion

#### Storyboard (6–8 frames)

| Frame | Scene | What's shown |
|-------|-------|-------------|
| 1 | **[BEFORE APP] Student at dorm** | Club activity next week. Needs to book a room. Sends LINE message to staff. Two days pass — no reply. Anxious, can't tell members if activity is on. |
| 2 | **Opens app → Floor Plan** | Campus floor plan loads. ECC building. Rooms colored 🟢🔴🟡. Sees free slots without asking anyone. |
| 3 | **Taps ECC-301 → Room Info Card** | Card: capacity 40, projector ✓, AC ✓, "Free Sat 1–4pm". Exactly what the club needs. One tap to proceed. |
| 4 | **Selects slot → Conflict check** | Picks Sat 1–4pm. No clash. "Slot available." Submits request — takes 30 seconds total. |
| 5 | **Approval Timeline appears** | Step tracker: `Submitted ✓ → Staff Review ⏳ → Dept Head → Approved`. Student bookmarks it. No follow-up LINE needed. |
| 6 | **Push notification arrives** | "ECC-301 approved for Sat 1–4pm 🎉" Student sees it in class. Immediately messages club group: "We're confirmed." |
| 7 | **[AFTER APP] Saturday arrives** | Student and club members walk to ECC-301. Door unlocked, room as booked. No last-minute "wait for staff" moment. |
| 8 | **[AFTER APP] Outcome felt** | Activity runs. Members present. Whiteboard covered in plans. Student relaxed — knew 3 days in advance. No LINE chase. |

---

### Part 4 — Critique Note

| | |
|--|--|
| **What other team flagged** | |
| **What we changed** | |
| **What we kept + why** | |

---

### Part 5 — User Stories + Acceptance Criteria (5–8 stories)

Formula: *As a [who] I want to [do what] so that [I get what]*

| # | User Story | Acceptance Criterion |
|---|-----------|---------------------|
| 1 | As a **student**, I want to see which rooms are available right now on a map, so that I can find a free room without walking around campus or asking staff. | Done when: student opens app and sees a floor plan with each room colored by live status (Free / Pending / Booked) updated in real time. |
| 2 | As a **student**, I want to view a room's details before booking — including capacity, equipment, and any restrictions — so that I can confirm the room fits my event before committing. | Done when: tapping any room shows a detail card with at minimum: capacity (number of people), equipment list, and current availability. |
| 3 | As a **student**, I want to submit my booking request and upload the required documents in the app, so that I don't need to deliver physical paperwork or send files on LINE. | Done when: student can attach a document file during booking submission and receive a confirmation that the request was received. |
| 4 | As a **student**, I want to track my booking's approval progress step by step, so that I always know where my request stands without messaging anyone. | Done when: student sees a live step tracker (Submitted → Staff Review → Dept Head → Approved/Rejected) that updates automatically at each stage. |
| 5 | As a **student**, I want to receive a push notification when my booking is approved or rejected, so that I can inform my group immediately without checking the app repeatedly. | Done when: student's phone receives a notification within 5 minutes of a status change, showing the room name, result, and time slot. |
| 6 | As a **student**, I want the app to suggest an available alternative room when my request is rejected, so that I can re-book quickly without starting the search from scratch. | Done when: rejection screen shows at least one alternative room with matching capacity that has a free slot on the same date. |
| 7 | As a **student**, I want to cancel a booking I no longer need, so that the room becomes available for others immediately. | Done when: student can cancel a pending or approved booking from the booking detail screen, and the room status updates to Free within 1 minute. |

⚠️ Write user goals, NOT technical specs ("the system must have a button" = half marks)

---

## Rubric

| Criterion | Full (1.0) | Half (0.5) |
|-----------|-----------|-----------|
| 1. Problem choice + idea range | HMW links to Week 6; everyone did 8 boxes; ideas genuinely different | < 8 boxes, same-shape ideas, or one sheet for whole team |
| 2. Concept selection with criteria | Silent vote first; concept named; explains why it answers HMW | No reasoning linked to HMW |
| 3. Storyboard tells a story | 6–8 frames; starts before app, ends after; context + action + felt outcome | App screens only, or no resolution shown |
| 4. Revision after critique | All 3 lines done; change visible in storyboard; kept items have reasons | "No comments" or notes written but nothing changed |
| 5. User stories well-formed | 5–8 stories; As a/I want/so that; user goals not implementation | < 5 stories, or written as specs |

---

## Gemini Image Prompts

### Storyboard (8-panel, updated 2026-08-11)

Reflects actual Crazy 8s sketches. Key differences vs. first draft: Panel 4 = doc upload, Panel 6 gap = rejection→suggest alternative, Panel 7 = day-of reminder, Panel 8 gap = cancel.

```
Create a UX storyboard infographic in a clean flat-illustration style.

OVERALL LAYOUT:
- White background, 8 panels in 2 rows of 4
- Each panel: white card, light gray border, rounded corners
- Top of each panel: teal numbered circle (①②③…) + bold navy panel title
- Inside panel: flat cartoon illustration of a person + a UI phone/screen mockup
- Below illustration: 1–2 sentence narrative caption in small gray text
- Below each panel card: a pink sticky-note card with a "?" icon and a design question
- Character style: rounded, friendly, simple flat cartoon — Google illustration style

COLOR PALETTE:
- Navy blue (#1a2e4a) for main titles
- Teal (#2a9d8f) for numbered circles and accents
- Pink/blush (#fce4ec) for sticky-note question cards
- Light gray (#f5f5f5) for panel backgrounds
- White for card fills

HEADER:
Title (bold navy, large): "KMITL FACILITY BOOKING — STORYBOARD"
Subtitle (teal): "How a student books a room without chasing anyone on LINE."
Scenario line: "Scenario: A 3rd-year engineering student needs to book a club activity room."

PANEL 1 — "Before: Waiting on LINE"
Illustration: Student at desk, anxious. Phone shows LINE chat sent 2 days ago — double gray tick, unread. Wall calendar with activity date circled in red.
Caption: "He messaged staff on LINE 2 days ago. Still no reply. Can't confirm with club members."
Pink question: "Should the app replace LINE entirely, or notify staff inside LINE?"

PANEL 2 — "Opens App: Floor Plan"
Illustration: Student holds phone, relaxed. Screen shows campus building floor plan — rooms labeled EN-01, EN-02, EN-03 as colored rectangles: green (free), red (busy), yellow (pending).
Caption: "He opens the app. Every room's live status visible on the floor plan instantly."
Pink question: "Should rooms be sorted by floor, by availability, or nearest first?"

PANEL 3 — "Taps Room: Info Card"
Illustration: Phone screen close-up. Card pops up: room name ECC-301, person icon + "40 pax", projector ✓, AC ✓, green badge "Free Sat 1–4pm". Finger tapping "Book This Slot".
Caption: "He taps a free room. Capacity, equipment, and live slot — one card, one tap."
Pink question: "What if his preferred room is taken? Does the app suggest alternatives like EN-05?"

PANEL 4 — "Submit + Upload Doc"
Illustration: Student on phone. Screen shows booking form: time slot selected (Sat 1–4pm, green checkmark "No conflict"), plus a document upload section with a file icon and "Upload activity proposal" button. Submit button at bottom.
Caption: "He picks the slot, attaches the required document, and submits — 1 minute total."
Pink question: "Which documents are required? Should templates be provided in-app?"

PANEL 5 — "Approval Timeline"
Illustration: Student sitting calmly, phone in lap. Screen shows horizontal step tracker: Submitted ✓ → Staff Review (spinner) → Dept Head → Approved. First node checked, second has loading spinner.
Caption: "A live tracker appears — he knows exactly where his request sits. No messages sent."
Pink question: "Should he get notified at every step, or only on final decision?"

PANEL 6 — "Push: Approved!"
Illustration: Student in class, phone buzzes. Lock screen: "📅 ECC-301 approved for Sat 1–4pm ✓". Student smiles, types to club group chat.
Caption: "Notification arrives. He tells the club immediately: we're confirmed."
Pink question: "If rejected, does the app instantly show available alternatives like EN-05?"

PANEL 7 — "Day-of Reminder"
Illustration: Student's phone lock screen, morning of Saturday. Notification: "09:58 — Today's booking: ECC-301, 1–4pm. Tap to view details." Student glances at phone, grabs bag.
Caption: "A reminder fires on the day. He doesn't need to remember — the app does."
Pink question: "Should he be able to cancel from this reminder notification directly?"

PANEL 8 — "After: Activity Runs"
Illustration: Wide panel. Club activity in full swing — 5 students around a table, whiteboard with diagrams, projector on. Small inset: old LINE chat still unread, greyed out with a light X over it.
Caption: "Activity runs. Confirmed 3 days early. He never needed LINE."
Pink question: "Should the app collect feedback or auto-release the room if he cancels?"

FOOTER:
Yellow rounded box with lightbulb icon:
"Key Takeaway: The student always knew the status — no walking, no LINE chasing, no guessing."
```

### User Stories — 3 Core Cards (2026-08-11)

```
Create a user story infographic in clean flat illustration style, white background.

LAYOUT: 3 cards side by side in one row. Same format as food delivery user story examples.
Each card has two zones:
- TOP ZONE (white): colored numbered circle top-left + "User Story" label. Small flat cartoon illustration of a student with a phone. Below: story text.
- BOTTOM ZONE (soft green background): trophy icon + "Acceptance Criteria" in bold green + 1 bullet point.

CARD 1 — green numbered circle ①
Illustration: student holding phone, map with colored room boxes visible on screen.
Story text:
"As a student,
I want to see a real-time map of available rooms with clear dates and times,
so that I can find a free room instantly without asking anyone."
Acceptance Criteria: The student can see a live floor plan where each room shows its current status (Free / Pending / Booked) and available time slots, updated in real time.

CARD 2 — orange numbered circle ②
Illustration: student tapping a room card on phone showing details.
Story text:
"As a student,
I want to view room details — equipment, size, capacity, and restrictions — before booking,
so that I can confirm the room fits my event's needs."
Acceptance Criteria: Tapping a room opens a detail card showing capacity (number of people), equipment list, room size, and any usage restrictions.

CARD 3 — blue numbered circle ③
Illustration: student sitting calmly, phone shows step tracker: Submitted ✓ → Review → Approved.
Story text:
"As a student,
I want to submit documents online and check my booking status at any time,
so that I never need to follow up with staff or send files on LINE."
Acceptance Criteria: Student can attach a required document during submission and view a live approval step tracker (Submitted → Staff Review → Dept Head → Approved/Rejected) at any time.

FOOTER: light yellow rounded banner with lightbulb icon.
Text: "Key Takeaway: Good user stories answer Who – What – Why and have clear acceptance criteria."

STYLE: Google flat illustration style. Friendly, clean. Color palette: teal, orange, blue card accents. White cards, light gray page background.
```

---

## Related

- [[uxui-week5-pov-hmw]] — POV + HMW from week 5
- [[uxui-week6-hooked-kano]] — Feature order (Kano model output)
