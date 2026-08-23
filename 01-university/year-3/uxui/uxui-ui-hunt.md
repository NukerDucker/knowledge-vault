---
title: "UX/UI: UI Hunt — Unusual Screens"
tags:
  - university
  - uxui
  - individual
status: archived
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

- ≥ 3 screenshots (we have 10)
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

### Site 1 — Steam Store — Crusader Kings III · Game Platform (International)

**URL:** https://store.steampowered.com/app/1158310/Crusader_Kings_III/  
**Screen:** Game page main viewport + purchase section  
**Screenshots:** `ss_steam_main.png`, `ss_steam_purchase.png`

**Observation:**  
Arriving from a sale notification, the first visible element is a "You're not signed in" login wall with no price visible in the first viewport. The purchase section below the fold presents 4 options at 3 different discount rates (-70% base, -50% Starter bundle, -42% Collection, ฿299/mo subscription) with no recommended option highlighted. Subscription is styled identically to one-time purchases.

**Principle violated:** Hick's Law — 4 equally-weighted purchase options cause choice paralysis. Transparency — subscription payment model not visually distinguished from permanent purchases. Progressive Disclosure — price hidden behind login prompt before user can evaluate the product.

**Improvement proposal:** Show price and primary buy button above the fold without requiring login. Highlight one recommended purchase option. Visually distinguish subscription from one-time purchase options.

---

### Site 2 — กรมสรรพากร (rd.go.th) · Thai Government

**URL:** https://www.rd.go.th  
**Screen:** Homepage  
**Screenshots:** `ss_rd_main_vp.png`, `ss_rd_scroll.png`

**Observation:**  
Homepage opens with a rotating announcement banner before showing any useful content. More than 30 service icons are displayed at identical size with identical styling, regardless of how frequently they are used. The navigation bar repeats all services in dropdowns of 10–15 items, arranged by internal department categories rather than user task logic. There is no search field anywhere on the page.

**Principle violated:** Hick's Law — 30+ equally-weighted icons cause decision paralysis. Recognition over Recall — icons require prior knowledge, no search available. Progressive Disclosure — rare and common services treated identically.

**Improvement proposal:** Surface 3–5 most common tasks as large plain-language buttons above the fold. Add a prominent search input. Group remaining services by task type, not department name.

---

### Site 3 — สำนักงานประกันสังคม (sso.go.th) · Thai Government

**URL:** https://www.sso.go.th/  
**Screen:** Homepage  
**Screenshots:** `ss_sso_main_vp.png`, `ss_sso_scroll.png`

**Observation:**  
The page mixes three unrelated visual styles simultaneously — a hero banner carousel, a grid of icon shortcuts, and a news feed column — with no clear reading path. The same service (e.g., สิทธิประโยชน์) appears under multiple menu categories with different labels, confusing users about which path leads to the same destination.

**Principle violated:** Consistency — different UI patterns appear on the same page with no unified design language. Miller's Law — navigation dropdowns contain far more than 7±2 items. F-pattern reading — content layout ignores how eyes naturally scan.

**Improvement proposal:** Consolidate navigation to maximum 6 top-level categories. Use a single card pattern consistently for all service shortcuts. Add a prominent search bar as the primary interaction mode.

---

### Site 4 — Amazon.com · E-commerce (International)

**URL:** https://www.amazon.com/s?k=laptop  
**Screen:** Search results page  
**Screenshots:** `ss_amazon_search.png`, `ss_amazon_product.png`

**Observation:**  
The first 3–4 result cards are marked "Sponsored" but styled identically to organic results — only a small grey tag differentiates them. Within each card, multiple competing badges ("Best Seller", "Amazon's Choice", "#1 Most Gifted", "Limited time deal") simultaneously fight for attention, creating decision paralysis.

**Principle violated:** Transparency / Dark Pattern — paid ads are disguised as organic results. Cognitive Load — excessive information per card exceeds processing capacity. Signal-to-noise ratio — promotional labels drown out actual product specifications.

**Improvement proposal:** Differentiate sponsored results with a visible colored border. Limit to one badge per card. Increase white space between result cards to support comparison.

---

### Site 5 — Booking.com · Travel Booking (International)

**URL:** https://www.booking.com/searchresults.html?ss=Bangkok  
**Screen:** Hotel search results (Bangkok, 1 night)  
**Screenshots:** `ss_booking_results.png`, `ss_booking_hotel.png`

**Observation:**  
Search results show urgency messages in red/orange ("Only 2 rooms left at this price!", "In high demand — booked 12 times in the last 24 hours") creating artificial time pressure. Prices displayed exclude taxes and fees, which only appear at final checkout — significantly higher than first shown.

**Principle violated:** Dark Patterns — false scarcity and urgency manipulation exploit loss aversion. Transparency — hiding the full price until checkout violates honest disclosure. User Autonomy — manufactured anxiety undermines rational comparison.

**Improvement proposal:** Display full price including taxes on results page. Replace urgency badges with neutral factual availability info. Remove countdown timers where no real deadline exists.

---

## Status

- [x] ≥3 screenshots collected (5 sites: 1 game platform + 2 Thai gov + 2 international)
- [x] Observations written for each
- [x] Principles identified for each
- [x] Improvements written for each
- [x] DOCX assembled → `~/Documents/University/Year-3/UXUI/67011178_UIHunt.docx`
- [x] Export PDF → submitted as `67011178_UIHunt.pdf` Aug 23

**Assets folder:** `~/Documents/University/Year-3/UXUI/ui-hunt-assets/` (23 files: 10 originals + 10 annotated + 2 scripts + 1 preview)

| File | Description |
|---|---|
| `ss_steam_main.png` + `_ann.png` | Steam store CK3 main viewport (login wall) |
| `ss_steam_purchase.png` + `_ann.png` | Steam store purchase section (4 options) |
| `ss_rd_main_vp.png` + `_ann.png` | rd.go.th homepage (30+ equal-weight icons) |
| `ss_rd_scroll.png` + `_ann.png` | rd.go.th scrolled (icon grid continues) |
| `ss_sso_main_vp.png` + `_ann.png` | sso.go.th homepage (3 systems) |
| `ss_sso_scroll.png` + `_ann.png` | sso.go.th scrolled (news feed) |
| `ss_amazon_search.png` + `_ann.png` | Amazon laptop search results |
| `ss_amazon_product.png` + `_ann.png` | Amazon product detail page |
| `ss_booking_results.png` + `_ann.png` | Booking.com Bangkok results |
| `ss_booking_hotel.png` + `_ann.png` | Booking.com hotel room table |

---

*See also: [[assignments-tracker]] · [[uxui-hooked-individual]]*
