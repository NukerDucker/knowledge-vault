---
title: "UX/UI Project: KMITL Campus Facility Booking System"
tags:
  - university
  - group-work
  - project
status: active
due: 2026-10-19
subject: uxui
course: 01276545
---

# KMITL Campus Facility Booking System

**What:** a campus room-booking system for KMITL — the design project behind every UX/UI weekly deliverable.
**Why:** UX/UI Design coursework (01276545, Tue). Group 2 · Napaul Intharasing (67011178).
**Where:** files → `~/Documents/University/Year-3/UXUI/` · NotebookLM id `ab79df06-a734-46f4-a9a8-f97f4d753982` (14 sources)
**Constraint:** every feature must trace to a POV or an HMW. Untraceable ideas (AI room suggestion, loyalty points) were cut for exactly that reason.

The design project that Weeks 3–7 all build on. Each week's note holds that
week's deliverable; this note holds the through-line — the reasoning that
carries across weeks and would otherwise be lost between them.

**NotebookLM:** "UX/UI Design CEI — Year 3 Project"
id `ab79df06-a734-46f4-a9a8-f97f4d753982` · 14 sources

---

## The problem

Two users, one failure point.

- **Student:** submits a booking via LINE, then cannot tell whether staff have
  read it. Messages sit unread for days; by the time it is clear the activity
  cannot proceed, it is too late to rearrange.
- **Professor:** wants live room availability from his desk. No shared calendar
  exists, so he walks the ECC building reading door notice boards — and
  double-bookings still happen anyway.

Both POVs fail at the same place: **no visibility into room state or booking
progress.** Every design decision below traces back to that sentence.

---

## The spine — how each week connects

| Week | Deliverable | What it contributed | Note |
|---|---|---|---|
| 3 | Market comparison | Competitor baseline | [[uxui-week3-market-comparison]] |
| 4 | User journey map | Where the journey breaks | [[uxui-week4-user-journey-map]] |
| 5 | POV + HMW | The two POVs, and HMW 1 + 2 as the winners | [[uxui-week5-pov-hmw]] |
| 6 | Hooked + Kano | Why those two ship first | [[uxui-week6-hooked-kano]] |
| 7 | Crazy 8s + storyboard | What they look like | [[uxui-week7-crazy8s-storyboard]] |
| 8 | User story mapping | Scoping topic + activities/steps/details map | [[uxui-week8-user-story-mapping]] |
| 9 | Sitemap + app comparison | IA structure for student/prof/staff + 3-app benchmark | [[uxui-week9-sitemap]] |
| ~10 | Wireframe & Wireflow | 15 screens combined on one Figma page, snake wireflow | see below |
| ~11 | UI Prototype + Usability Test | Hi-fi prototype → UT with 5 participants → improve | [[uxui-usability-test]] |

### The HMW shortlist (Week 5)

1. **Make live room availability visible to everyone in one shared place** *(both)*
2. **Notify users automatically at every approval stage so they never message staff** *(both)*
3. Surface estimated approval time upfront so students can plan *(student)*
4. Replace LINE as submission channel so messages cannot be left unread *(both)*
5. Auto-release a room the moment a booking is cancelled *(both)*

**Top two: HMW 1 + 2.** Every other HMW subsumes into them — 3 is a refinement
of 2, 4 is a consequence of 1 + 2, 5 is a refinement of 1.

---

## The central argument

This is the answer to the Essential Question, and the single most reusable
paragraph in the project:

> We build **live availability + status notification** first. Both POVs fail at
> the same point — no visibility into room state or booking progress. These are
> Kano **Basics** (the product is broken without them) and simultaneously the
> Hooked **Variable Reward** (every return is triggered by a genuine status
> update). That makes the loop both ethical and sticky.

Two frameworks, same conclusion, reached independently:

- **Per Kano:** basics ship first or nothing else matters.
- **Per Hooked:** the reward step cannot exist without live data.

When two models disagree you have a judgement call. When they agree, you have a
decision — which is why this argument is the thing worth keeping.

---

## Build order

1. **Basics** — booking recorded · live availability · status notifications · approval workflow
2. **Performance** — approval-time estimate · auto-release · booking history · room detail
3. **Delight** — calendar export · "similar rooms free now" after a rejection

Calendar export sits in Delight but does real structural work: it feeds the
Hooked **investment** step, which becomes the **external trigger** for the next
booking. It closes the loop.

**Cut:** AI room suggestion, loyalty/points. Neither traces to a POV or an HMW,
and untraceable features are how scope dies.

---

## Ethics position

The Hooked loop runs across a **single booking lifecycle (1–3 days)** — it is
deliberately not a daily-habit product. Users return because they need
information, not because the app manufactured urgency.

The nearest dark pattern is notification pressure: pushing users to open the app
when nothing meaningful has changed. The mitigation is in the design —
notifications fire only on real state changes (status update, slot freed,
deadline), and can be disabled entirely.

---

## Submission filenames

| Week | File |
|---|---|
| 6 | `TeamNumber_Hooked_Kano.pdf` |
| 7 | `GroupNumber_Crazy8s_Storyboard.pdf` |
| ~10 | Wireframe & Wireflow (Figma) |

---

## Wireframe & Wireflow (Week ~10)

**Figma file:** "UX/UI 2026 — Wirefame (Copy)" (working copy)  
**Status (2026-09-23):** ✅ Complete. All 15 screens on one Figma page (Nuker), snake wireflow layout.

**15 screens — 3 members × 5 each:**

| # | Screen | Member |
|---|---|---|
| 1 | Home | Name |
| 2 | Search Result | Name |
| 3 | Filter Search | Name |
| 4 | Room Detail | Name |
| 5 | Room Map | Name |
| 6 | Select Date & Time | Nuker |
| 7 | Booking Details | Nuker |
| 8 | Upload Document | Nuker |
| 9 | Review Booking | Nuker |
| 10 | Booking Submitted | Nuker |
| 11 | My Bookings (Past) | Noey |
| 12 | Booking Detail | Noey |
| 13 | Edit Booking | Noey |
| 14 | My Bookings (Upcoming) | Noey |
| 15 | Me (Profile) | Noey |

**Layout:** Snake/Z wireflow — row 1 left→right (1–5), row 2 right→left (6–10, connects from 5 via vertical drop on right, wraps left), row 3 left→right (11–15, connects from 10 via vertical drop on left). Flow arrows: ▶ ◀ ▼. Row labels with member names.

**Submission:** PDF export from Figma. Assignment says capture in sections if too small to read.

**Next step:** Hi-fi prototype → [[uxui-usability-test]] (UT with 5 participants, due 2026-10-05)

---

## Hi-fi Prototype — Final Submission (2026-10-06)

The full prototype specification — screens, node ids, and build order — now lives in
[[uxui-prototype-reference]]. It describes the 2026-10-06 file state and was superseded in part by
the 2026-10-10 fix batch ([[uxui-prototype-buglist-2026-10-10]]).

Project-wide status: [[uxui-project-state]].

---

## Grading traps (Week 7, from the brief)

Each of these is −0.5:

- One Crazy 8s sheet for the whole team — every member needs their own
- A critique note that says "no comments"
- User stories written as specs rather than as stories
- A storyboard that ends without resolution

---

*Weekly deliverables and their status live in each week's note. This note holds
only what spans weeks.*
