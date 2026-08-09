---
title: "UX/UI Wk6: Hooked + Kano — Facility Booking"
tags:
  - university
  - uxui
  - group-work
status: active
created: 2026-08-09
---

# UX/UI Week 6 — Hooked Loop + Kano Model

**Domain:** KMITL Campus Facility Booking System  
**Group:** 2 · Napaul Intharasing (67011178)

## Slide Status (as of 2026-08-09) ✅ ALL COMPLETE

| Activity | Slide | Status |
|----------|-------|--------|
| A — Hooked Loop | 9 | ✅ Done — corrected from wrong "not suitable" stub |
| B — Kano Sort | 10 | ✅ Done |
| C — Feature Order | 11 | ✅ Done |
| D — Ethics Check | 12 | ✅ Done — all 3 answers filled |

**Submit:** File → Download → PDF → rename `TeamNumber_Hooked_Kano.pdf`

## Activity A — Hooked Loop ✅ (content ready, slide wrong)

The slide currently says "not suitable" — **this is incorrect**. The actual answer:

- **Internal trigger:** Anxiety — "Did staff approve my request yet?"
- **External trigger:** Push notification — "Your booking was updated"
- **Action:** Open app → check booking status (one tap)
- **Variable reward:** Status change (Confirmed / Rejected / Pending) + available slot discovery
- **Investment:** Booking history builds → next booking pre-fills → preferred rooms surface first
- **Loop closes?** ✅ Yes — investment (history + preferences) makes the internal trigger easier to act on next time

> **Note on scope:** Loop operates within a single booking lifecycle (1–3 days), not a daily habit. User returns due to genuine information need — ethical by design.

## Activity B — Kano Sort ✅

| Tier | Features |
|------|----------|
| **Basic** | Reservations correctly recorded; automated notifications; reservation controllability (cancel etc.); live room availability |
| **Performance** | Estimated approval time; auto room release on cancellation; search + reservation history; room detail |
| **Delight** | Calendar export (→ Google Calendar); "similar rooms available" suggestion on rejection; room layout overview |

## Activity C — Feature Order ✅ (content ready)

**Rank 1 · Basic**
- Reliable reservation system
- Autonomous notification system
- Live room availability

**Rank 2 · Performance**
- Estimated reservation approval time
- Auto room release for cancelled reservations
- Search history + reservation history
- Room detail page

**Rank 3 · Delight**
- Calendar export
- Similar available rooms suggestion

**Cut list:** Loyalty system, AI room suggestion — no POV/HMW trace

## Activity D — Ethics Check ✅ (content ready, slide blank)

**Does the user genuinely gain on each pass of the loop?**  
Yes. Each return delivers real status information: Confirmed, Pending, or Rejected. Users also discover newly freed slots. No return is empty — the variable reward is the booking outcome, which is information they genuinely need.

**Where does the design come closest to a dark pattern?**  
Push notifications could pressure users to open the app when no meaningful update exists, creating anxiety rather than resolving it.

**How we fixed it / gave control back:**  
Notifications fire only on real state changes (status update, slot freed, deadline). Users can disable notifications entirely. Returning is always the user's choice — the system surfaces information, it does not manufacture urgency.

## Relationships

- [[uxui-week5-pov-hmw]] — POV + HMW that drive the feature decisions above
- [[project-uxui-week6]] — memory snapshot with full reasoning
