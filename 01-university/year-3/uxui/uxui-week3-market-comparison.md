---
title: "UX/UI Wk3: Market Comparison"
tags:
  - university
  - uxui
  - group-work
status: submitted
created: 2026-07-24
due: 2026-08-03
points: 10
subject: uxui
---

# UX/UI Week 3 — Market Comparison

> [!warning] Deadline
> **August 3, 2026 at 11:59 PM** · Group · 10 points
> Submit: `GroupNo_MarketComparison.pdf` (one member submits)

## Rubric

| Criterion | Max | Notes |
|-----------|-----|-------|
| Market Comparison | 2 | 3 products, ≥1 adjacent, each with flow/strengths/gaps |
| UX Analysis | 2 | Explain WHY, not just describe |
| Opportunity & Persona | 2 | Gap → persona pain point → differentiation |
| UI Comparison & Design Analysis | 2 | 3+ screens, screenshots, layout/nav/color/components analysis |
| Presentation & Evidence | 2 | Organized, annotations, references |

---

## Part 1: Market Comparison

Compare **3 real products** solving the same user job as your project topic.

**Requirements:**
- ≥ 1 **Adjacent Product** (different domain, similar job)
- Each product must include:
  - Core User Flow
  - UX Strengths
  - UX Gaps (limitations/weaknesses)
- Conclude with **1 Design Opportunity** — gap none currently address, tied to Persona's pain point

> [!danger] Adjacent product missing
> The three products researched so far (BU, RMUTL, SNRU) are all Thai university
> room-booking systems — **same domain**. Rubric requires ≥1 adjacent product
> (different domain, same user job: reserve a time-boxed space).
> **Action:** drop one of BU/SNRU, replace with an adjacent product.
> Candidates: **Calendly** (time-slot booking, conflict-blocking calendar),
> **Skedda** (commercial desk/room booking), **OpenTable** (table reservation),
> **Agoda/Airbnb** (availability-first booking UI).
> Recommended: **Calendly** — solves the exact pain New has (never shows an
> unavailable slot), so the contrast is sharp.

### Products

#### Product 1: BU Meeting Room Reservation
- **Link:** https://meetingroom.bu.ac.th/Manual/20180103_User_V3.pdf
- **Core User Flow:** Log in → Verify permission → Create request form → Select room + time → Save draft → Submit → Track status in "My Request"
- **UX Strengths:** Structured online request form; draft saving lets users pause a long form; explicit status tracking via "My Request" gives users a place to self-serve check.
- **UX Gaps:** No real-time availability calendar in the documented flow — users pick a room *then* find out if it's free. No automatic notifications, so status must be pulled, never pushed.
- **Takeaway:** Solves *status transparency*, not *discovery*.

#### Product 2: RMUTL Room Booking
- **Link:** https://booking.rmutl.ac.th/room/detail/
- **Core User Flow:** Sign up → Search room → Check availability → Select time → Add participants → Confirm → Participants accept → Room permitted
- **UX Strengths:** Availability-first — search surfaces schedule, capacity and equipment before commitment, so users self-filter. Closest of the three to what New asks for.
- **UX Gaps:** Every participant must register and separately confirm. A booking stalls on the slowest member — high onboarding friction for a one-off student activity.
- **Takeaway:** Best availability view, worst onboarding.

#### Product 3 (Adjacent): Calendly — *verify by hands-on walkthrough before submitting*
- **Link:** https://calendly.com
- **Core User Flow:** Open link → See only free slots → Pick slot → Enter details → Instant confirmation → Calendar invite sent both ways
- **UX Strengths:** Unavailable time is never rendered — conflicts are structurally impossible rather than validated after the fact. Zero-account booking for the guest. Confirmation is immediate and pushed, not polled.
- **UX Gaps:** No approval workflow (nobody endorses a request) and no concept of a shared physical resource or its equipment, so it cannot model "lecturer approves student's lab request".
- **Takeaway:** Proves availability-first booking works; lacks the institutional approval layer a university needs.

> *Backup:* SNRU Room Booking, already researched — colour-coded statuses, editable pending requests, email notices; weakness is a paper approval step plus manual status updates. Cite as supporting evidence, or swap back in if Calendly research falls through.
> Link: https://roombooking.snru.ac.th/roombooking.pdf

### Design Opportunity

> **Gap:** Every product digitises the *request*. None digitises *availability and approval together*. University systems have approval but no live availability; commercial tools have live availability but no approval.
> **Connected to persona pain point:** New walks to room doors to read paper notices and still gets double-booked — both are availability failures, not form failures. His students' paper forms get lost because approval lives outside the system.
> **How our design differentiates:** Lead with a conflict-blocking calendar as the entry point (Calendly's model), then layer institutional approval on top (the university model) — plus auto-reopen of cancelled class slots, which no product does.

---

## Part 2: UI Comparison & Design Analysis

Compare ≥ 3 corresponding screens (same function) across the 3 products.

**Possible screens:** Home, Product Listing, Product Detail, Search, Checkout/Payment, Profile

### Screens chosen — capture these three

Pick the *same function* across all 3 products so the comparison is like-for-like.
Recommended function set (each maps to a criterion argued in Part 1):

| # | Function | BU | RMUTL | Calendly |
|---|----------|----|-------|----------|
| 1 | **Availability / room search** | (weak — document the absence) | room detail + schedule | slot picker |
| 2 | **Request / booking submission** | request form | select time + add participants | details form |
| 3 | **Status tracking** | "My Request" list | booking permitted state | confirmation + calendar invite |

**Screenshot 1 — Availability**
- Screenshot: (attach)
- Layout / component placement:
- Navigation:
- Colour & buttons:
- **WHY designed this way:**

**Screenshot 2 — Submission**
- Screenshot: (attach)
- Layout / component placement:
- Navigation:
- Colour & buttons:
- **WHY designed this way:**

**Screenshot 3 — Status**
- Screenshot: (attach)
- Layout / component placement:
- Navigation:
- Colour & buttons:
- **WHY designed this way:**

### Synthesis (deck slide 14)

- **Similarities:** all three are form-first after entry; all require an account somewhere in the flow; all treat the approving human as the bottleneck.
- **Differences:** RMUTL surfaces schedule data; BU surfaces status; Calendly surfaces neither because it removes the need for both.
- **Implication for our design:** lead with the calendar, not the form. Approval becomes a state on a booking that already exists, not a gate before one can be made.

**Each screen analysis must include:**
- Main functions and notable features
- Key strengths / unique characteristics
- Common elements across products
- Screenshots with explanations
- Layout, component placement, navigation, colors, buttons, interaction design
- **WHY** the interface was designed that way (not just what it looks like)
- References (links to each app/site)

> [!tip] Key Grading Note
> Don't describe — **explain why**. Analyze rationale, not just appearance.

---

## Status

- [ ] Group agrees on project topic
- [ ] 3 products selected (incl. 1 adjacent)
- [ ] Part 1 drafted — all 3 products with flow/strengths/gaps
- [ ] Design opportunity written + linked to persona
- [ ] Part 2 screens selected (≥3)
- [ ] Screenshots captured with annotations
- [ ] Layout/nav/color/component analysis written
- [ ] References listed for every product
- [ ] PDF compiled as `GroupNo_MarketComparison.pdf`
- [ ] Submitted

---

*See also: [[assignments-tracker]]*
