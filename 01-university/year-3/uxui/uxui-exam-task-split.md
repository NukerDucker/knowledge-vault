---
title: "KMITL B-App — Exam Task Split (Nuker / Name / Noey)"
tags:
  - university
  - group-work
  - project
status: active
subject: uxui
course: 01276545
---

# Exam Task Split — who does what

**Group 2 · Mookrata** · 3 members · **Deadline 2026-10-19**

| Nickname | Full name | ID | Task | Screens | Figma sections |
|---|---|---|---|---|---|
| **Nuker** | Napaul Intharasing | 67011178 | **Book** | 16 | `Napaul / User / Authentication` · `Booking Flow` · `Overlays` |
| **Name** | Chonchanok Nitipornsri | 67011106 | **Browse** | 9 | `Chonnanok / User / Home` · `Search Flow` · `Room Info` |
| **Noey** | Mawin Pengsuk | 67011163 | **Track** | 6 | `Mawin / User / Booking History` · `Booking Details` · `Profile` |

Speaking order follows the flow: **Name → Nuker → Noey**. The examiners see the user journey
run continuously, which is what the brief asks for.

There is no fourth member. The `67011138` ID in the Week 7 Crazy 8s table is not part of this group.

Related: [[uxui-facility-booking-project]] · [[uxui-decisions-log]] · [[uxui-usability-test]] ·
[[uxui-final-audit]]

---

## 0 · The shared standard everyone must adopt

### Grid — and this is currently a scoring gap

The UT assignment requires *"show all UI screens for the task you are responsible for, including
how you set the grid and pattern design"* and *"capture every page with a grid setting."*

**Only 10 of 52 frames have a layout grid, and all 10 are Nuker's.** Name's and Noey's screens have
**zero** — so neither can currently produce the required grid captures at all.

The standard to apply, copied from Nuker's frames so the whole file matches (this is also
Criterion 2, Consistency & Design System, which is a **group** score):

| Property | Value |
|---|---|
| Pattern | **COLUMNS** |
| Count | **4** |
| Gutter | **8** |
| Margin / offset | **16** |
| Alignment | **STRETCH** |
| Colour | `#EE621D` @ 10% |

Two things to do on **every** screen: apply that grid, and set `visible: true` before exporting.
Nuker's are currently `visible: false`, so even his captures would show no grid today.

### Touch targets — 93 live frames fail the rubric

The rubric requires **≥44×44pt iOS / 48×48dp Android, measured from the tappable Frame**. Not
WCAG 2.5.8's 24px. The notes previously recorded 24px pills and 28px chips as passing; against this
rubric they are roughly half the minimum.

| Owner | Live tappable frames under 44 |
|---|---|
| **Name** | 37 |
| **Noey** | 25 |
| **Nuker** | 22 |

**Exempt** per the rubric: inline links (`Forgot password?`, `Sign in`, `Sign up`, `Back`,
`To Sign In/Up`) and standard OS components (status bar, home indicator). That clears 9 of Nuker's.

**Fix strategy — two different jobs:**

1. **Wrap, do not grow.** Put a tappable icon inside a transparent 44×44 frame that carries the
   reaction. Fixes `chevron-left` (24×24, 26 instances), `Notification Bell` (36×36),
   `Action 1`/`Action 2` (22×22), `Lucide` (24×24), `minus` (16×16). **Zero visual change**, and it
   is exactly what "measured from the tappable Frame" invites.
2. **Grow the control.** `Filter Select` 23px · `Sort Direction` 23px · `Filter Label` 22px ·
   `Sort by ↓` 17px · `Chip` 28px · `Time Select` 32px · `Details`/`Reviews` tabs 32px ·
   `Date Time Filter` 41px. These have no wrapper option — the row heights change.

Item 1 is cheap and buys points in every individual section. Do it first.

---

## 1 · Nuker (Napaul) — Book · 16 screens

**Screens:** Sign In · Sign Up · Forgot Password · Reset Password · Select Date & Time ·
Booking Details - Empty · Booking Details - Filled · Upload Documents - Empty ·
Upload Documents - Uploaded · Review Booking · Booking Submitted · Notification · Sort Sheet ·
Confirm Sheet · Cancel Sheet · Action Confirm Sheet

**Open fixes** — all from [[uxui-facility-booking-project#Remaining Figma fixes — resume list]]:
- Overlays and stepper are **done**. `+` overlap was already gone.

**To do:**
- [ ] **Touch targets** — 22 live under 44. Worst: `chevron-left` 24×24 (26 instances), `Lucide`
      24×24, `Time Select` 112×32. Wrap-first strategy.
- [ ] **Grid** — already present on the 7 booking-flow frames; still set `visible: true` for export.
      Add to the 4 Authentication screens and the 5 overlays, which have none.
- [ ] **Page quota check** — overlays count as 0.5 each, max 2 counted = **1 page of quota**. Make
      sure the 11 non-overlay screens are all full-function, so the quota is met without them.

**Individual a11y slide — the numbers you own:**
- Navy `#1B2A5B` on white **13.7–15.5:1** ✅ · green `#047857` **5.48:1** ✅ · amber `#B45309`
  **5.02:1** ✅ · `#4B5563` **7.56:1** ✅
- **CTA white-on-orange `#E8622D` = 3.38:1** — state it as a decision, not a pass. Navy would give
  4.58:1. The justification is in [[uxui-decisions-log]] §5.2, including the two caveats.
- **Consider fixing it instead:** 3.38:1 *passes* as large text (≥18pt / 24px regular, or
  14pt / 18.66px bold). Bumping the CTA label to 18.66px bold converts a fail into a pass with no
  colour change. That is a cleaner answer than defending 3.38:1.

**States to show:** Booking Details empty · capacity inline error · Confirm / Cancel / Confirm-Edit
dialogs.

---

## 2 · Name (Chonchanok) — Browse · 9 screens

**Screens:** Home · Search Results · Search Results - Empty · Filter · Room Detail - Available ·
Room Detail - Review · Room Detail - Unavailable · Room Detail - Unavailable Review · Map

**Open fixes:**
- [ ] **`Book Now` gating differs by tab** — works on an Unavailable room from the Details tab,
      dead on Reviews. **This is a Dead End**: −1 to Criterion 1 per the rubric.
- [ ] **Home profile avatar does not route to Profile.** **Also a Dead End**: −1.
      *Two dead ends is the maximum −2.* Fix both.
- [ ] **Slideshow** — drag vs tap inconsistent, and drags land behind the room card.
- [x] Busy / Unavailable vocabulary — **fixed**, Room Detail now reads `Busy until 15:00`.

**To do:**
- [ ] **Touch targets — 37 live under 44, the worst of the three.** `Filter Select` 23px,
      `Filter Label` 22px, `Sort Direction` 23px, `Sort by ↓` 17px, `Details`/`Reviews` 32px,
      `Notification Bell` 36×36.
- [ ] **Grid — none of her 9 screens has one.** Apply the shared grid, then make it visible.
- [ ] **`Search Results - Empty`** already exists ✅ — this is her empty state for the exam.

**Individual a11y slide:** the map floor pills are **24px** and the tabs **32px** — both fail the
44 requirement. Say the measured number and what you changed. Do not quote WCAG 2.5.8's 24px floor
as a pass; this rubric is stricter.

**UT material available:** `assets/ut/2026-10-10-prefix/after/08-room-detail-available.png`, `09-sort-sheet.png`,
`10-map.png` (before + after). Tracker rows 13 (Nhow — 0px clearance under the Book Now bar),
14 (Nhow — sort had no asc/desc), 15 (Putt — bare numerals 1–7 on the map → `1F`–`7F`).

---

## 3 · Noey (Mawin) — Track · 6 screens

**Screens:** Booking History - Past · Booking History - Upcoming · Booking Detail - Approved ·
Booking Detail - Completed · Edit Booking · Profile

⚠️ **6 screens is exactly the minimum.** The rubric adds that *"supporting screens count for no more
than 2 pages of the quota"* — so at least 4 of his 6 must be full-function, with ≥2 core. There is
no room for a screen that doesn't pull its weight.

**Open fixes:**
- [ ] **Booking History empty state is missing.** The exam explicitly asks for the empty state of
      your task. This is the only genuinely missing empty state in the file.
- [ ] **Reviews submittable on rejected and cancelled bookings** — a completed-only action is
      available on states where it makes no sense.
- [ ] **Booking History scroll position not reset** on entry from Review / Upcoming — the list
      lands scrolled, pushing a past booking out of view.

**To do:**
- [ ] **Touch targets — 25 live under 44.** `Action 1`/`Action 2` 22×22, `Time Select` 32px,
      `Date Time Filter` 41px.
- [ ] **Grid — none of his 6 screens has one.** Apply the shared grid, then make it visible.

**Individual a11y slide:** his screens carry the widest spread of badge variants — Approved,
Completed, Cancelled, Rejected. All are now corrected and verified. The before/after is
`assets/ut/2026-10-10-prefix/after/17-badge-colour-propagation.png`.

**UT material available:** `assets/ut/2026-10-10-prefix/after/06-booking-detail-approved.png`,
`07-booking-history-upcoming.png` (before + after). Tracker rows 17–22.

---

## 4 · What Nuker has that Name and Noey can use for their UT

The Usability Testing assignment is a **separate individual submission worth 10 points** — not the
exam deck. It needs its own PDF, and two versions of the screen captures (with grid, without grid).
Everything below is shared evidence they are entitled to draw on.

### 4.1 The five participants — already meets the "5 profiles" requirement

| Pseudonym | Age | Where |
|---|---|---|
| Putt | 20 | [[uxui-usability-test]] |
| Mind | 22 | [[uxui-usability-test]] |
| Nhow | 20 | [[uxui-usability-test]] |
| ching ching | 20 | [[uxui-usability-test]] |
| cheesy | 20 | [[uxui-usability-test]] |

Each has a profile, raw observations, quotes, and a per-participant improvement table. The test was
run as a group, so all three members may cite the same five people — but each should quote the
findings **about their own screens**.

### 4.2 Findings that belong to Name

- **Nhow** — 0px clearance between Booking Rules and the sticky Book Now bar, already 1px clipped on
  *Unavailable*. Fixed: bottom padding 0 → 104.
- **Nhow** — sort offered no ascending/descending choice. Fixed: new `Sort Direction` component.
- **Putt** — map floor selector showed bare numerals 1–7. Fixed: `1F`–`7F`.
- **cheesy** — *"Cannot get out of Sort By — the search background behind the popup is gone."*
  Root cause was the `OVERLAY → NAVIGATE` rewrite; fixed.
- **cheesy** — the same room read `Busy` in Search then `Unavailable` in Room Detail. Fixed.

### 4.3 Findings that belong to Noey

- **Mind** — "Request Edit" carried a `CLOSE` action, so confirming did nothing.
- Both cancel buttons were visually identical — *Keep Booking* and *Request Cancellation* were
  indistinguishable.
- Profile dead links.
- The badge contrast failures land hardest on his screens — Approved, Pending, Completed,
  Cancelled all failed AA before the fix.

### 4.4 Findings that belong to Nuker

- **Putt** — the confirmation screen didn't read as a confirmation.
- **Mind** — the attendee slider drag was swallowed by a `destinationId: null` reaction.
- **cheesy** — the slider reached only 1 or 80; a 60-person booking was unsettable.
- **cheesy** — a fake capacity warning asserted "Exceeds room capacity (40 seats)" regardless of
  input, including at 1 attendee.

### 4.5 Shared assets and methods

- **`assets/ut/2026-10-10-prefix/`** — 19 before/after pairs. `08`, `09`, `10` are Name's; `06`, `07` are Noey's;
  `01`–`05` and `11`–`19` are shared or Nuker's. Each pair is numbered and referenced from the
  tracker.
- **The improvement tracker** — 48 rows in [[uxui-usability-test#Improvement tracker]], each citing
  its before/after export. **The UT assignment asks for 5 improvement points; there are 48.** Each
  member can pull 5–8 rows about their own screens straight out of it, with evidence already
  attached.
- **The verified contrast table** — every badge variant measured with the WCAG relative-luminance
  formula, not estimated. All three can cite the same numbers for their own screens.
- **The touch-target audit** — 93 live frames under 44, split by owner. That is both the to-do list
  and the a11y slide evidence.
- **The method** — scenarios and tasks as run, so each member's UT report describes the same study
  consistently.

### 4.6 What is NOT available and must be produced per member

- **Grid captures.** Nobody can produce these until the shared grid is applied and made visible.
  This is the single biggest UT gap and it blocks all three.
- **Per-member before/after framed on their own screens.** The tracker has the rows; the
  *highlighted* "improved point" callouts are per-member work.
- **Individual profile text.** The participant profiles exist; each member must write the summary
  of what *that participant said about their screens*.

---

## 5 · Blockers, in order

| # | Blocker | Owner | Blocks |
|---|---|---|---|
| 1 | Apply shared grid + `visible: true` to all screens | Name, Noey (Nuker: visibility only) | Both UT PDFs, for all three |
| 2 | Two Dead Ends on Name's screens | Name | −2 to her Criterion 1 |
| 3 | Booking History empty state | Noey | Exam slide 4, UT |
| 4 | Touch targets — wrap-first pass | all three | Criterion 4, individual |
| 5 | `GX_FinalReport.pdf` + `GX_FinalPresentation.pdf` | all three | Submission |
| 6 | Reconcile the two AI Use Log tables (3-row vs 1-row) | Nuker | Report, 1.5 pts |

---

## 6 · Group chat message to send — Thai

**Context for whoever reads this later:** neither of the other two has worked on the UXUI project.
Nuker did the design, the prototype and the usability testing himself. It is too late for them to
do the real work, so this message hands them the **real** findings about their own screens and asks
them to write up and present it.

**The honesty line is not decorative.** The grading rubric lists *fabricating usability test results
or user quotes* as **Red — not allowed**. The data is genuine — five real participants, real
observations — so citing it is fine. A member claiming they ran the sessions is not. The message
says so explicitly, which protects all three.

**Register:** กู / มึง, at Nuker's request. Nicknames — **เนม = Chonchanok**, **เนย = Mawin**.

```
เฮ้ยสองคน — สอบ 19 ต.ค. ใกล้แล้ว มาเคลียร์กันให้จบ

พูดตรง ๆ ก่อน เพราะมันกระทบคะแนนของมึง ไม่ใช่ของกู

กูเขียน Figma เสร็จหมดแล้ว — ทุกหน้าจอ ทุกการแก้ ดีไซน์ซิสเต็ม
โปรโตไทป์ทั้งอัน และกูเป็นคนรัน usability test เองทั้งหมด
ผู้ทดสอบ 5 คน กูบันทึกการแก้ไว้ 48 จุด พร้อมภาพ before/after
ข้อมูลทั้งหมดของโปรเจกต์นี้อยู่กับกู

กูจะไม่แกล้งทำเป็นอย่างอื่น และมึงก็ไม่ควรทำเหมือนกัน
เพราะเกณฑ์ให้คะแนนถือว่าการกุผลการทดสอบเป็นความผิดร้ายแรง
สิ่งที่กูทำได้คือส่งผลทดสอบจริงที่เกี่ยวกับหน้าจอของมึงให้
แล้วมึงเขียนกับนำเสนอเอง

--- สิ่งที่กูจะส่งให้แต่ละคน ---
ชุดข้อมูลที่บอกว่าผู้ทดสอบ 5 คนเจออะไรบนหน้าจอของมึง อะไรพัง
และภาพ before/after ของการแก้บนหน้าที่มึงดูแล
ทั้งหมดเป็นของจริง จากการทดสอบจริงที่กูทำ

หน้าที่มึง: เขียนใหม่ด้วยคำของตัวเอง และอธิบายปากเปล่าได้
ถ้าอาจารย์ถามว่าใครรันเทส ให้บอกว่าเป็นการทดสอบของกลุ่มครั้งเดียว
และกูรัน — อย่าอ้างว่ารันเอง

--- เนม (Chonchanok) ---
หน้าจอ: Home, Search Results, Search Results-Empty, Filter,
Room Detail x4, Map

ชุดข้อมูลของมึงมี: ผู้ทดสอบเจอช่องว่าง 0px ใต้แถบ Book Now,
การ sort ไม่มีตัวเลือกมากไปน้อย, และเลขชั้นบนแผนที่แสดงเป็น
ตัวเลขล้วนแทนที่จะเป็น 1F-7F

ยังมีสองจุดที่พังอยู่ แต่ละจุดหักคะแนนมึง 1 คะแนน:
  - "Book Now" กดได้บน Room Detail แท็บ Details
    แต่กดไม่ได้บนแท็บ Reviews
  - รูปโปรไฟล์บน Home กดแล้วไม่ไปหน้า Profile

--- เนย (Mawin) ---
หน้าจอ: Booking History Past/Upcoming, Booking Detail
Approved/Completed, Edit Booking, Profile

ชุดข้อมูลของมึงมี: "Request Edit" กดยืนยันแล้วไม่มีอะไรเกิดขึ้น
และปุ่มยกเลิกสองปุ่มหน้าตาเหมือนกัน

Booking History ยังไม่มี empty state และข้อสอบถามเรื่องนี้ตรง ๆ
นี่คือหน้าจอเดียวที่มึงต้องเพิ่ม

--- ทั้งสองคน ---
1. สไลด์นำเสนอคนละ 6 สไลด์ กูทำเด็คให้ แต่เนื้อหาเกี่ยวกับ
   หน้าจอของมึงต้องมาจากมึงเอง ส่งมา:
   - งานของมึง หนึ่งบรรทัด
   - จะเดโมหน้าจอไหน ตั้งแต่ต้นจนจบ
   - 2 อย่างที่เปลี่ยนไปหลังทดสอบ
2. เดโมสด 5 นาที คลิกไล่ flow ของตัวเองใน Figma ไม่ต้องดูโน้ต
   ต้องคลิกได้โดยไม่หลง
3. PDF Usability Testing — ส่งแยก 10 คะแนน เป็นของแต่ละคน
   ใช้ชุดข้อมูลที่กูส่งให้

--- กำหนดส่ง ---
เนื้อหาสไลด์กับ flow เดโม ภายในวันศุกร์
ถ้ามาส่งวันก่อนสอบ กูช่วยแก้อะไรไม่ได้ และทุกคนโดนหักคะแนน

ทุกคนจะโดนถามคำถามสุ่ม 1 ข้อ เรื่องการตัดสินใจดีไซน์บนหน้าของตัวเอง
เพราะฉะนั้นต้องรู้จริงว่าทำไมหน้าจอถึงเป็นแบบนั้น
กูจะส่งสรุปหนึ่งหน้าให้แต่ละคน จะได้ไม่ต้องเริ่มจากศูนย์

ถ้าการแก้ Figma ข้างบนหนักเกินไป บอกกูภายในวันศุกร์ กูทำให้เอง
```

---

## 7 · Slide plans — rubric-aligned

Written 2026-10-09 against the **Final Prototype Rubric** and the accessibility guide. This
supersedes the deck plan in [[uxui-final-audit]] where the two differ; the differences are noted.

### 7.1 Group section — 10 min · max 12 slides · Part 1 = 5 points

Part 1 grades **the explanation, not the Figma file**. Its three criteria drive the structure:

| # | Slide | Scores |
|---|---|---|
| 1 | Title — KMITL B-App · Group 2 Mookrata · 3 members | — |
| 2 | Background + **Problem Statement** + target users | Presentation Flow |
| 3 | **Persona 1 "New"** — pain points only | Design Rationale |
| 4 | **Persona 2 student** — pain points only | Design Rationale |
| 5 | **Pain → Feature → where it sits in the UI** | Presentation Flow |
| 6 | Site Map / overall user flow | Presentation Flow |
| 7 | Role division + why speaking order follows the flow | Presentation Flow |
| 8 | **Design System: palette AND typography, with tested contrast ratios** | **Design Rationale — 2 pts** |
| 9 | **AI Use Log** (or "No AI used") | **AI Transparency — 1.5 pts** |
| 10 | Standout vs BU / RMUTL / Calendly / Skedda / LibCal / Google Calendar | Design Rationale |
| 11 | Conclusion | — |
| 12 | Future Work | — |

**Two changes from the earlier plan in [[uxui-final-audit]]:**

1. **Slide 8 must cover typography too.** The rubric says *"Explains the Color Palette and
   Typography choices, linked to the user and branding, with evidence such as tested Contrast
   Ratios."* The old plan named only colours. Typography with no explanation risks falling to
   *"1 — Partly explained"*.
2. **Slide 9 is the AI Use Log** — worth **1.5 points** on its own, and the old plan dropped it as
   a "report requirement". The rubric places it in the presentation.

⚠️ The rubric's Presentation Flow criterion reads *"Problem (UX) → Solution (UI) → Demo"*. The
brief puts the live demo in the individual section. Keep a **60-second group-level flow run-through**
as insurance so the sequence is visibly complete either way.

**Contrast numbers to put on slide 8** — all measured, not estimated:

| Pair | Ratio | Verdict |
|---|---|---|
| Navy `#1B2A5B` on white | 13.7–15.5:1 | ✅ |
| White on `#047857` (Available, Approved) | 5.48:1 | ✅ |
| White on `#C2410C` (Partial, Under Review) | 5.18:1 | ✅ |
| White on `#B45309` (Upcoming, Busy) | 5.02:1 | ✅ |
| White on `#4B5563` (Cancelled) | 7.56:1 | ✅ |
| White on `#DC2626` (Rejected) | 4.83:1 | ✅ |
| **White on orange CTA `#E8622D`** | **3.38:1** | ⚠️ deliberate — see §7.4 |

### 7.2 Individual sections — 5 min each · max 6 slides each

| # | Slide | Note |
|---|---|---|
| 1 | My task + all my screens | Name every screen |
| 2 | Live Figma demo, start → end | |
| 3 | **Usability & Accessibility** — contrast, labels, **touch targets** | Cite the 44×44pt requirement and give measured numbers |
| 4 | Confirmation / error prevention — **or** the empty & error state | The exam asks for one |
| 5 | UT summary — who, what broke, what changed | One slide, brief |
| 6 | Before/After evidence | Also required for any Yellow-level AI use |

### 7.3 Usability Testing deck — separate submission · 10 points · individual

This is **not** the exam deck and should not be folded into it. Eight requirements from the UT
brief, so roughly:

| Slide | Covers |
|---|---|
| 1 | Objectives + hypotheses, scenarios, roles |
| 2 | **5 participant profiles** (pseudonyms) |
| 3–5 | Per-participant feedback summaries |
| 6 | All my screens **with grid shown** |
| 7 | Pattern / grid setup explained |
| 8–9 | **Before/After with the improved points highlighted** |
| 10 | Reasons and details for each improvement |
| 11 | Final Figma link |

Required as **two PDFs** — every page *with* grid, and every page *without* grid.

### 7.4 The white-on-orange CTA — decide before the exam

`#E8622D` with a white label is **3.38:1**. AA for normal text needs 4.5:1, so this **fails** and an
examiner reading the rubric can see it.

Two honest options:

- **Defend it.** Say 3.38:1, say navy would give 4.58:1, and give the perception argument. Full
  reasoning and the two caveats are in [[uxui-decisions-log]] §5.2. **Never claim 4.58:1.**
- **Fix it.** 3.38:1 *passes* as large text — ≥18pt/24px regular, or **14pt / 18.66px bold**. Bumping
  the CTA label to 18.66px bold converts a fail into a pass with **no colour change**. This is the
  cleaner answer and costs one text-style edit.

The second option is strictly better if there is time. It turns a defensible position into a passing
one.

---

## 8 · Resume point

Everything below is on disk and survives a cleared session.

| Where | What |
|---|---|
| [[uxui-exam-task-split]] §0 | Shared grid spec, touch-target audit by owner |
| [[uxui-exam-task-split]] §1–3 | Per-member open fixes |
| [[uxui-exam-task-split]] §4 | UT evidence each member may draw on |
| [[uxui-exam-task-split]] §6 | Thai group-chat message, ready to send |
| [[uxui-decisions-log]] | Every design decision with reasoning, 58 images |
| [[uxui-usability-test]] | Rows 42–48, 45a — this session's fixes with before/after |
| [[uxui-facility-booking-project]] | Node index, API gotchas, resume list |
| `assets/ut/2026-10-10-prefix/` | 19 before/after pairs |
| `assets/decision/` | 75 images, 4 folders |

**Open work, in priority order:**

1. Grid — apply the shared spec to Name's 9 and Noey's 6, and set `visible: true` on all 31.
   **Blocks both UT PDFs.**
2. Chonchanok's two Dead Ends — the full −2 cap on her Criterion 1.
3. Booking History empty state (Mawin).
4. Touch targets — 93 frames; wrap-first pass.
5. `GX_FinalReport.pdf` and `GX_FinalPresentation.pdf` — not started.
6. Reconcile the two AI Use Log tables (3-row vs 1-row).
7. **Unknown:** the presentation-slot sign-up file. Nuker still needs to send it over.

---

*Hub → [[uxui-facility-booking-project]] · Reasoning → [[uxui-decisions-log]] · Evidence →
[[uxui-usability-test]] · Deck plan → [[uxui-final-audit]]*
