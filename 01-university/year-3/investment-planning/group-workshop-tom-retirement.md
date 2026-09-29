---
title: Group Workshop — Tom Retirement Portfolio
tags: [investment-planning, group-work, portfolio, retirement]
status: active
updated: 2026-09-24
due: 2026-10-08
points: 20
subject: investment-planning
---

# Group Workshop — Tom Retirement Portfolio

**Course:** 96643026 Investment Planning  
**Weight:** 20% of total score  
**NotebookLM:** https://notebooklm.google.com/notebook/d8650ac2-a3fe-40a7-86f8-9b999836e3e0

## Deliverables & Deadlines

| Item | Due | Format |
|---|---|---|
| First draft | 2026-09-24 (TODAY) | Submit to MS Teams → Investment Planning Workshop folder |
| Final draft | 2026-10-01 | PPT + PDF ≥70% done; presentation order randomized this day |
| Presentation + Final report | 2026-10-08 | 15 min present + 5 min Q&A |

**Submit:** PPT file + PDF report (5 content pages; max 9 pages including cover/intro/TOC/references)  
**Presenters:** 2 representatives per group  
**Q&A:** answer 1 question from another group + 1 from lecturer

---

## Tom's Case

- Age 30, expat in Thailand
- Savings: ฿200,000 lump sum
- Monthly contribution: ฿5,000/month until retirement
- Retire at 60 (30 years accumulation)
- Live to 90 (30 years payout)
- Retirement spend: ฿30,000/month

---

## Q1 — Minimum Required Rate of Return

Two-phase TVM. Solve for monthly rate `r` iteratively.

**Phase 2 — PV needed at retirement:**
```
N = 360 (30yr × 12)
PMT = 30,000
FV = 0
Solve → PV₆₀
```

**Phase 1 — What savings grow to:**
```
N = 360
PV = -200,000
PMT = -5,000
Solve → FV₃₀
```

Constraint: FV₃₀ = PV₆₀ → solve for `r` (no closed form, iterate numerically)

**Formula:**
$$200{,}000(1+i)^{360} + 5{,}000\frac{(1+i)^{360}-1}{i} = 30{,}000\frac{1-(1+i)^{-360}}{i}$$

**Core equations:**

$$FV_{60} = PV_{60}$$

$$200{,}000(1+i)^{360} + 5{,}000\frac{(1+i)^{360}-1}{i} = 30{,}000(1+i)\frac{1-(1+i)^{-360}}{i}$$

Where:

$$FV_{60} = P_0(1+i)^n + C\frac{(1+i)^n - 1}{i}$$

$$PV_{60} = W(1+i)\frac{1-(1+i)^{-n}}{i}$$

**Answer: i* = 0.4440% per month → 5.4606% effective per year**

Solved via Excel Goal Seek: Set gap cell (FV−PV) = 0, By Changing monthly rate cell.  
At i* = 0.4440%: FV@60 ≈ ฿5,408,558 | PV@60 ≈ ฿5,385,564 (gap < ฿23,000 ≈ 0.4%)

Include Excel Goal Seek screenshot + payout table (annual balance age 60→90) as submission evidence.

---

## Q2 — Risk Assessment Score 35

Score 35/100 = **High Risk — Level 4** (30–36 per SEC/course risk framework from W11 slides).  
Level 4 permits aggressive equity allocation; 30-year horizon reinforces this posture.

**SEC risk framework from lectures (W11 Portfolio Management):**
- Level 1 (< 15): Low Risk
- Level 2 (15–21): Moderate-Low Risk
- Level 3 (22–29): Moderate-High Risk
- **Level 4 (30–36): High Risk ← Tom is here (score 35)**
- Level 5 (≥ 37): Very High Risk

**Suggested allocation (3-Basket technique from lectures):**

| Basket               | Asset Type              | %   | Notes                                                             |
| -------------------- | ----------------------- | --- | ----------------------------------------------------------------- |
| Low risk (10-20%)    | Money Market / Cash     | 10% | Emergency/liquidity reserve (Krungsri Kept cited in lectures)     |
| Medium risk (60-80%) | Fixed Income            | 45% | Core stability; UGIS-N + PTT Debentures                           |
| High risk (10-30%)   | Equities + Alternatives | 45% | Growth over 30yr; KKP GNP + B-INNOTECH + LHTPROP + DIF + SCBGOLDH |

Simplified view:

| Asset Type | % |
|---|---|
| Fixed Income | 45% |
| Equities | 25% |
| Real Estate / Infrastructure | 15% |
| Gold | 10% |
| Cash / Money Market | 5% |

Justify: Level 4 (High Risk) permits higher equity allocation; 30-year horizon supports full use of this latitude; inflation risk requires REITs + gold in alternatives basket; money market 5% provides liquidity buffer.

---

## Q3 — Portfolio Construction (4 types, max 2 assets each)

**Theme: "Tom's Global Diversified Retirement Portfolio"** — global ETF approach suited to Tom as an expat; accessible via Interactive Brokers or Saxo Bank Thailand; all iShares UCITS ETFs with deep liquidity and public data.

*4 asset types per course taxonomy (เงินฝาก / ตราสารหนี้ / ตราสารทุน / สินทรัพย์ทางเลือก); max 2 assets each*

| # | Asset Type (Course Taxonomy) | Assets | Tickers | Weight | Role |
|---|---|---|---|---|---|
| 1 | **Deposits / เงินฝาก** | Krungsri Kept (digital savings, 1.50% p.a.) | **Krungsri Kept** | 5% | Liquidity buffer; THB-denominated; near-zero risk; lecturer's W11 sample asset |
| 2 | **Equities / ตราสารทุน** | iShares Core MSCI World UCITS ETF (Acc) + iShares MSCI Emerging Markets UCITS ETF | **IWDA** (IE00B4L5Y983) + **EIMI** | 40% | Core global growth — developed (32%) + emerging markets (8%); 30yr compounding engine |
| 3 | **Fixed Income / ตราสารหนี้** | iShares Core Global Aggregate Bond (USD-hedged) + Krungsri Monthly Fixed Income | **AGGU** + **KFMTFI** | 38% | Ballast (28% AGGU global IG bonds) + THB anchor (10% KFMTFI local currency match) |
| 4 | **Alternatives / สินทรัพย์ทางเลือก** | iShares Global REIT ETF + iShares Physical Gold ETC | **REET** + **IGLN** | 17% | Inflation hedge (REET 10%) + crash hedge / gold (IGLN 7%) |

**Portfolio allocation summary:**

| Asset Type | Assets | Weight | Expected Return | Contribution |
|---|---|---|---|---|
| Deposits | Krungsri Kept | 5% | ~1.5% | 0.08% |
| Equities | IWDA + EIMI | 40% | ~9.5% | 3.80% |
| Fixed Income | AGGU + KFMTFI | 38% | ~3.5% | 1.33% |
| Alternatives | REET + IGLN | 17% | ~5.0% | 0.85% |
| **Weighted portfolio return** | | **100%** | | **~6.06%** ✓ > i* 5.46% |

> **Note on กองทุนธนาบัตร:** not named in course materials. Concept = Thai T-bill fund (ultra-short gov't debt, maturity <1yr). If prof specifies a particular fund, substitute it in row 1. Krungsri Kept is the lecturer's W11 sample; it is a deposit product, not a fund — both are valid เงินฝาก/ตลาดเงิน tier assets.

**How Tom buys:** Interactive Brokers or Saxo Bank Thailand — both accessible to expats with passport + work permit. KFMTFI purchasable via KAsset app (Thai brokerage). All ETFs have public price history on iShares website + Bloomberg.

**Currency note:** IWDA/EIMI/REET/IGLN priced in USD; KFMTFI in THB. Currency mismatch at payout is a risk — mitigated by KFMTFI (12% THB anchor) and long horizon allowing FX averaging.

---

## Fundamental Analysis Requirements

- Use ≥5 years historical data for each asset (price chart, return, volatility)
- For equities: P/E, EPS trend, dividend yield, sector outlook
- For bonds: credit rating, duration, yield curve position
- For REITs: occupancy rate, dividend yield, NAV
- For gold: macro drivers (USD, inflation), 5-yr price trend

---

## Risk Analysis

| Risk | Assets affected | Scenario | Mitigation |
|---|---|---|---|
| Equity drawdown | IWDA + EIMI | 30–40% drop in a crash year | 30yr horizon absorbs recovery; AGGU + IGLN buffer losses |
| Interest rate rise | AGGU | Bond price falls ~7% per 1% rate increase | KFMTFI short-duration offsets; hold to maturity recovers value |
| Currency (USD to THB) | IWDA + EIMI + REET + IGLN | THB strengthens, lower baht value at payout | KFMTFI 12% THB anchor; long horizon averages out FX cycles |
| Inflation | AGGU + KFMTFI | Fixed returns lose real value over 30 years | REET passes rent increases; IGLN preserves real value |
| Liquidity | REET | REITs sell off fast in a credit crunch | NYSE/LSE-listed, high daily volume, no lock-up |
| Broker/custody | All | Broker insolvency | SIPC-insured up to $500k; assets held separately from broker |

---

## Report Structure (5 content pages)

1. **Tom's Profile + Required Rate of Return** — TVM calc, payout table
2. **Risk Assessment Interpretation** — score 35 breakdown, allocation rationale
3. **Asset Selection** — 4 types × 2 assets, why each, how to buy in Thailand
4. **Fundamental Analysis** — 5-yr historical data, valuation per asset
5. **Risk Analysis + Portfolio Summary** — donut chart + summary table

---

## Session Fixes Applied (2026-09-25)

**FIXED docx:** `~/Downloads/Investment Planning First Report FIXED.docx`

| Fix | Status |
|---|---|
| Risk score 35 = Level 4 High Risk (not Moderate) | ✓ done in docx |
| IWDA "56 yrs" → MSCI World ~56yr; IWDA launched 2009 (~17 yrs) | ✓ done in docx |
| "inflation-adjusted ฿30,000" → nominal (inflation note added) | ✓ done in docx |
| Surplus "end of 60 year" → "at retirement (age 60)" | ✓ done in docx |
| KFMTFI ticker added to asset table | ✓ done in docx |
| Key Assumptions block + annuity-due (1+i) explanation | ✓ done in docx |
| Weighted return derivation table (6.06% > i* 5.46%) | ✓ done in docx |
| Payout table age 60–90 from Excel (฿5.4M → ฿0) | ✓ done in docx |
| Donut chart | ⬜ manual in Word |
| §6 asset table → Deposits/Equities/FI/Alternatives layout | ⬜ manual in Word |
| 3-basket mapping fix (Krungsri Kept = low-risk) | ⬜ manual in Word |
| Deepen §7 fundamental analysis | ⬜ pending |
| Humanize AI-flagged prose (§3, §5, §9) | ⬜ pending |

**Final draft due: 2026-10-01**

---

## Donut Chart Settings (Word for Mac)

- Insert → Chart → Doughnut → OK
- Data: Krungsri Kept 5, IWDA 32, EIMI 8, AGGU 28, KFMTFI 10, REET 10, IGLN 7
- Hole size: Format Data Series → 75%
- Labels: Category Name ✓ + Percentage ✓ + Show Leader Lines ✓, Separator: New Line
- Label position: Word Mac has no Outside End option — drag each label manually outside slice; leader line auto-draws
- Colors same type = same hue, different shade:
  - Deposits: `#90A4AE`
  - IWDA: `#1565C0` / EIMI: `#64B5F6`
  - AGGU: `#2E7D32` / KFMTFI: `#81C784`
  - REET: `#F9A825`
  - IGLN: `#8D1A1A`
- Delete auto legend → manual text box with 5 colored squares (Deposits/Equities/Fixed Income/Alternatives)
- Center text box: `6.06%` bold 28pt + `expected return` gray 11pt, no border/fill
- Slice borders: white, 2pt (Format Data Series → Border)

---

## NotebookLM

**Notebook:** https://notebooklm.google.com/notebook/d8650ac2-a3fe-40a7-86f8-9b999836e3e0  
**Sources added:** Group Workshop.pdf (official brief), all lecture slides

**Key confirmed facts from NotebookLM:**
- Risk score scale: Level 4 = 30–36 = High Risk (NOT moderate)
- Course taxonomy: เงินฝาก / ตราสารหนี้ / ตราสารทุน / สินทรัพย์ทางเลือก
- กองทุนธนาบัตร NOT in course materials — Krungsri Kept is lecturer's W11 sample
- Brief requires exactly 4 asset types, max 2 each
- Payout table + weighted return derivation required by rubric

---

## Scoring Criteria

**Report:** content (assumptions, fundamentals, risk, theory from lectures), format  
**Presentation:** content, time (±1 min), visuals, explanation clarity, Q&A ability
