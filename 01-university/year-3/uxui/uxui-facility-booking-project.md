---
title: "UX/UI Project: KMITL Campus Facility Booking System"
tags:
  - university
  - uxui
  - group-work
  - project
status: active
subject: uxui
---

# KMITL Campus Facility Booking System

Group 2 · Napaul Intharasing (67011178)

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
