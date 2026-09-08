---
title: Week 9 — Sitemap & App Comparison
tags:
  - uxui
  - assignment
  - group-work
  - sitemap
  - information-architecture
status: in-progress
created: 2026-09-08
updated: 2026-09-08
due: TBA
points: TBA
type: group-work
team: G2
subject: uxui
---

# Week 9 — Sitemap & App Comparison

**App:** RoomIQ — KMITL Campus Facility Booking System
**Team:** Mookrata (Group 2) — Napaul Intharasing (67011178), Mawin Pengsuk (67011163), Chonchanok Nitipornsri (67011106)
Project hub → [[uxui-facility-booking-project]]

---

## Sitemap

### Shared
```
Auth
  ├── Login with KMITL SSO
  ├── Forgot Password
  └── Reset Password
```

### Student / Professor
```
Home / Dashboard
  ├── Upcoming booking card
  ├── Quick availability strip (today)
  └── Notification badge

Search
  ├── Search by name
  └── Filter Panel
      ├── Floor
      ├── Room type (Lecture / Lab / Meeting room)
      ├── Date
      ├── Time
      └── Capacity

Room Detail
  ├── Room information (photos · equipment · capacity)
  ├── Live availability calendar
  └── Book This Room (CTA)
      └── Bookmark / Favourite (save room)

Booking
  ├── Select date and time
  ├── Enter booking details
  │   ├── Purpose / activity name
  │   ├── Attendee count
  │   └── Upload document (activity form)
  ├── Submit Booking
  ├── Edit Booking (Pending only)
  └── Cancel Booking

Status Tracking
  ├── Status Updates
  │   ├── Pending
  │   ├── Approved
  │   └── Rejected
  │       └── Rejection reason
  ├── Notifications
  │   ├── Status-change alerts
  │   └── Auto-release alerts
  └── History (past bookings)

Profile / Settings
  ├── Account Info
  ├── Notification Preferences
  └── Logout
```

### Facility Staff
```
Staff Dashboard
  ├── Pending approvals count
  └── Today's room schedule overview

Manage Bookings
  ├── Pending list
  ├── All bookings (filterable)
  └── Booking Detail
      ├── Approve
      └── Reject (+ rejection reason → triggers notification)

Manage Rooms
  ├── Room list
  └── Room Detail (staff view)
      ├── Mark out of order / restore
      └── View current + upcoming schedule

Profile / Settings
  ├── Account Info
  └── Logout
```

---

## Design decisions

- **Room Detail is shared** — same page; staff sees extra controls
- **Notifications** is top-level, not buried in Profile (core feature per HMW 2)
- **Bookmark** lives in Room Detail, not Booking — users save before they commit
- **Edit Booking** restricted to Pending state only — must be annotated on slide
- **Home/Dashboard** is the entry node — all three apps compared below lack one

---

## App Comparison

### Prompt used
`"room booking web app with live availability and approval workflow"` (Skedda)
`"university campus room booking system students"` (LibCal)
`"Google Calendar room booking features university"` (Google Calendar)

---

### 1. Skedda (skedda.com) — web app

**Why chosen:** Direct domain match. Space/room booking with live availability grid — closest to RoomIQ's core loop.

| Feature | Skedda | RoomIQ |
|---|---|---|
| Live availability grid | ✅ | ✅ |
| Filter by space type | ✅ | ✅ |
| Booking form | ✅ | ✅ + document upload |
| Staff approval workflow | ❌ (self-serve) | ✅ |
| Rejection reason | ❌ | ✅ |
| Status-change notifications | ❌ | ✅ |

**What's similar:** Browse → Book flow, live availability concept.
**What's different:** Skedda stops at booking confirmation. RoomIQ adds the full approval lifecycle — the gap the POV identified.

---

### 2. LibCal by Springshare — web app

**Why chosen:** University context. Used by academic libraries worldwide for student space booking — same user group.

| Feature | LibCal | RoomIQ |
|---|---|---|
| Room list + time slot picker | ✅ | ✅ |
| Email confirmation | ✅ | ✅ + in-app push |
| Staff approval workflow | ❌ (auto-approve) | ✅ |
| Live availability calendar | ❌ | ✅ |
| Rejection handling | ❌ | ✅ |
| Document upload | ❌ | ✅ |

**What's similar:** Academic use case, student room search flow.
**What's different:** LibCal designed for low-friction library seats — no approval chain needed. KMITL activity rooms require staff authorisation, which LibCal cannot model.

---

### 3. Google Calendar Room Booking (Google Workspace) — web + app

**Why chosen:** Most familiar reference for professors. Understanding what GCal lacks explains why a dedicated system is needed.

| Feature | Google Calendar | RoomIQ |
|---|---|---|
| Calendar / availability view | ✅ | ✅ |
| Room resource booking | ✅ (invite-based) | ✅ (request-based) |
| Staff approval workflow | ❌ | ✅ |
| Document upload | ❌ | ✅ |
| Status tracking (Pending/Approved/Rejected) | ❌ | ✅ |
| Rejection reason | ❌ | ✅ |
| Targeted in-app notifications | ❌ (email only) | ✅ |

**What's similar:** Calendar view of availability, familiar scheduling mental model.
**What's different:** GCal handles peer scheduling, not hierarchical request-approval. The moment a student needs staff sign-off, GCal breaks — which is exactly KMITL's problem.

---

## Key insight (use in slide rationale)

All three apps cover **Browse → Book**. None cover **Request → Approval → Notify** properly. That gap is RoomIQ's entire reason to exist and traces directly to HMW 1 + 2.

---

## Final Prototype — Page Count Rules

**Count:** App 5–8 screens per member · Web 3–5 pages per member
3 members → **15–24 screens total**

### Counting rules

| Rule | RoomIQ application |
|---|---|
| Sign in + sign up = 1 page | Auth node = 1 screen |
| Pop-up = 0.5 (max 2 counted = 1 page) | Rejection reason, cancel confirm → pop-ups |
| One user type per pair | Each member picks Student OR Staff |
| Link only one option through to completion | Book flow: one room type, one time slot — no branches |
| First page shows all related functions | Home/Dashboard must surface full nav |
| Must be usable start-to-finish | Browse → Book → Track = one complete linked flow |

### Member split

⬜ Not decided yet — assign user type + flow per member before starting prototypes.

Suggested split (pending team agreement):

| Member | User type | Screens | Flow |
|---|---|---|---|
| Napaul (67011178) | TBA | 5–8 | TBA |
| Mawin (67011163) | TBA | 5–8 | TBA |
| Chonchanok (67011106) | TBA | 5–8 | TBA |

### AI policy (applies to this project)

**Acceptable:** brainstorming, grouping/summarising data, mock data drafts, checking flow completeness
**Not acceptable:** generating user research in place of real data, concluding insights without verifying with real users, using generated UX/UI as-is

---

## Status

- ✅ Sitemap drafted (student/prof + staff)
- ✅ App comparison (3 apps)
- ✅ Prototype page-count rules
- ⬜ Member split (decide with team)
- ⬜ Card sorting
- ⬜ Final slide layout

---

*Project hub → [[uxui-facility-booking-project]]*
