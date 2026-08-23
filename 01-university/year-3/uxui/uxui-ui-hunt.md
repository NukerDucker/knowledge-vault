---
title: "UX/UI: UI Hunt — Unusual Screens"
tags:
  - university
  - uxui
  - individual
status: active
created: 2026-07-24
updated: 2026-08-23
due: 2026-09-07
---

# UX/UI — UI Hunt: Capture UI Screens That Feel "Unusual"

> [!info] Deadline
> **September 7, 2026 at 11:59 PM** · Individual · 6 points

## Objective

Collect UI screens that feel unusual, confusing, difficult to use, or make users pause. Analyzed **twice**:
1. Now — personal observation
2. Later — after UI Design Principles lesson

## Requirements

- ≥ 3 screenshots (we have 4)
- From **different types of products**
- Sources: websites, mobile apps, desktop apps, games

## Rubric

| Criterion | Pts | Notes |
|-----------|-----|-------|
| Quality of UI Examples | 1.0 | Diverse, clear, sufficient context incl. multi-step flow |
| Analysis Using UI Design Principles | 3.0 | Correct principle ID + usability impact explanation |
| Design Improvement Proposal | 1.5 | Practical redesign, supported by principles |
| Communication & Presentation | 0.5 | Organized, clear screenshots, good explanations |

---

## Screenshots

### Site 1 — กรมสรรพากร (rd.go.th) · Thai Government

**URL:** https://www.rd.go.th/landing.html  
**Screen:** Homepage / Service Navigation  
**Screenshots:** `ss_rd_go_th.png`, `ss_rd_landing.png`

**Observation:**  
The homepage presents dozens of navigation icons at identical visual weight, with no clear primary action. Finding e-filing (ยื่นแบบภาษี) requires scanning through an undifferentiated icon grid. Labels use formal legal Thai jargon that is not self-explanatory to first-time users.

**Principle violated:** Hick's Law — too many choices of equal visual weight slow decision-making. Visual Hierarchy — no focal point guides the eye to the most common task. Recognition over Recall — icon labels are not self-descriptive without prior knowledge.

**Improvement proposal:** Group services into 3–5 top tasks ("ยื่นภาษี", "ขอคืนภาษี", "ตรวจสอบสิทธิ์") as large prominent CTAs above the fold. Relegate less-used links to a secondary menu. Replace jargon labels with plain-language descriptions.

---

### Site 2 — สำนักงานประกันสังคม (sso.go.th) · Thai Government

**URL:** https://www.sso.go.th/  
**Screen:** Homepage  
**Screenshots:** `ss_sso_go_th.png`, `ss_sso_home_full.png`

**Observation:**  
The page mixes three unrelated visual styles simultaneously — a hero banner carousel, a grid of icon shortcuts, and a news feed column — with no clear reading path. The same service (e.g., สิทธิประโยชน์) appears under multiple menu categories with different labels, confusing users about which path leads to the same destination.

**Principle violated:** Consistency — different UI patterns appear on the same page with no unified design language. Miller's Law — navigation dropdowns contain far more than 7±2 items. F-pattern reading — content layout ignores how eyes naturally scan.

**Improvement proposal:** Consolidate navigation to maximum 6 top-level categories. Use a single card pattern consistently for all service shortcuts. Add a prominent search bar as the primary interaction mode.

---

### Site 3 — Amazon.com · E-commerce (International)

**URL:** https://www.amazon.com/s?k=laptop  
**Screen:** Search results page  
**Screenshots:** `ss_amazon.png`, `ss_amazon_search.png`

**Observation:**  
The first 3–4 result cards are marked "Sponsored" but styled identically to organic results — only a small grey tag differentiates them. Within each card, multiple competing badges ("Best Seller", "Amazon's Choice", "#1 Most Gifted", "Limited time deal") simultaneously fight for attention, creating decision paralysis.

**Principle violated:** Transparency / Dark Pattern — paid ads are disguised as organic results. Cognitive Load — excessive information per card exceeds processing capacity. Signal-to-noise ratio — promotional labels drown out actual product specifications.

**Improvement proposal:** Differentiate sponsored results with a visible colored border. Limit to one badge per card. Increase white space between result cards to support comparison.

---

### Site 4 — Booking.com · Travel Booking (International)

**URL:** https://www.booking.com/searchresults.html?ss=Bangkok  
**Screen:** Hotel search results (Bangkok, 1 night)  
**Screenshots:** `ss_booking.png`, `ss_booking_results.png`

**Observation:**  
Search results show urgency messages in red/orange ("Only 2 rooms left at this price!", "In high demand — booked 12 times in the last 24 hours") creating artificial time pressure. Prices displayed exclude taxes and fees, which only appear at final checkout — significantly higher than first shown.

**Principle violated:** Dark Patterns — false scarcity and urgency manipulation exploit loss aversion. Transparency — hiding the full price until checkout violates honest disclosure. User Autonomy — manufactured anxiety undermines rational comparison.

**Improvement proposal:** Display full price including taxes on results page. Replace urgency badges with neutral factual availability info. Remove countdown timers where no real deadline exists.

---

## Status

- [x] ≥3 screenshots collected (4 sites: 2 Thai gov + 2 international)
- [x] Observations written for each
- [x] Principles identified for each
- [x] Improvements written for each
- [ ] DOCX assembled → submit as `67011178_UIHunt.pdf`

**Screenshot files:** `hooked-assets/ss_rd_go_th.png`, `ss_rd_landing.png`, `ss_sso_go_th.png`, `ss_sso_home_full.png`, `ss_amazon.png`, `ss_amazon_search.png`, `ss_booking.png`, `ss_booking_results.png`

---

*See also: [[assignments-tracker]] · [[uxui-hooked-individual]]*
