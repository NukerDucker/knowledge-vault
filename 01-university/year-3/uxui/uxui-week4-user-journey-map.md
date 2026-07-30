---
title: "UX/UI Wk4: User Journey Map"
tags:
  - university
  - uxui
  - group-work
status: active
created: 2026-07-24
---

# UX/UI Week 4 — User Journey Map

> [!warning] Deadline
> **August 3, 2026 at 11:59 PM** · Group

## Task

Build a user journey map for the **Week 3 persona** and identify design opportunities within your project domain.

## Grading Criteria

- Stages and emotion curves
- Touchpoints/pains alignment
- Identified design opportunities

## Persona

**"New"** · 34 · University Professor, Computer Engineering, EEC building.
Books labs/classrooms for his own courses and endorses student requests.
See [[uxui-week3-market-comparison]] for the market gap this journey feeds.

## Draft journey — 5 stages

Scenario: New needs a lab for a make-up class next week, and a student group has
asked him to endorse their room request the same week.

| | 1 · Realise need | 2 · Find availability | 3 · Submit request | 4 · Wait | 5 · Use / outcome |
|---|---|---|---|---|---|
| **Doing** | Decides date + room type; asks which room is free | Walks to the room door to read the paper notice; calls admin | Fills paper form; messages person in charge on LINE; goes in person | Checks LINE repeatedly; asks around; re-sends message | Arrives at room; sometimes finds another group already inside |
| **Thinking** | "This should take five minutes" | "Why do I have to walk here to find this out?" | "Am I even sending this to the right person?" | "Was it approved? Did they see it?" | "The system said booked but class was cancelled" |
| **Feeling** | Neutral | Annoyed | Uncertain | Anxious → resigned | Frustrated / distrustful |
| **Emotion** | 3/5 | 2/5 | 2/5 | 1/5 ← **lowest** | 1/5 |
| **Touchpoints** | colleagues, memory | paper notice on door, phone call to admin | paper form, LINE, admin office counter | LINE (unread), admin office | physical room, occupying group |
| **Pains** | no single place to start | availability is offline and physical | wrong-person risk; form gets lost | no status, no ETA, messages left on read | double-booking; cancelled slots never reopen |

**Emotion curve:** starts neutral, dips at stage 2, collapses through stage 4
(the wait), and does not recover at stage 5 — the outcome confirms the distrust
rather than resolving it. Two troughs, not one.

## Design opportunities (per stage)

| Stage | Opportunity |
|-------|-------------|
| 2 · Find availability | Live room calendar as the entry point — never render an unavailable slot (Calendly model). Kills the walk-to-the-door touchpoint entirely. |
| 3 · Submit request | Request created *from* the calendar slot, routed automatically to the correct approver. Removes the "who do I send this to" failure. |
| 4 · Wait | Visible status timeline + estimated approval time, pushed not polled. Directly answers Insight 1 and 3 from Week 3. |
| 5 · Use | Conflict detection at booking time; auto-reopen cancelled class slots so freed rooms return to the pool. |

> **Biggest opportunity:** stage 4. Deepest emotional trough, and the one no
> comparison product solves well — BU tracks status but does not push it,
> RMUTL does not surface approval at all.

## Gaps to fix before submitting

- Empathy map **FEELS** column in `67011178_Persona.pdf` duplicates the DOES text — fix at source.
- "Circle one gap where SAYS and FEELS disagree" not marked. Proposed: he *says* the process is too slow, but *feels* he cannot trust the data — trust, not speed, is the real gap.
- Emotion values above are inferred from quotes, not scored by participants. Either validate with interviewees or label them as inferred on the slide.

## Status

- [x] Week 3 persona confirmed ("New")
- [x] Journey stages mapped (5 stages)
- [x] Emotion curve drafted
- [x] Touchpoints and pains identified
- [x] Design opportunities listed
- [ ] Emotion values validated with participants (or labelled inferred)
- [ ] Rendered as visual map (Figma/Slides)
- [ ] Submitted

---

*See also: [[assignments-tracker]]*
