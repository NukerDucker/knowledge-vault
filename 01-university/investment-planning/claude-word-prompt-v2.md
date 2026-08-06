# Claude in Word — Correction Prompt (v2)

> Paste everything below the horizontal line into Claude in Word.
> Select your entire document first, then paste this prompt.

---

You are editing a Thai corporate bond investment analysis report for an Investment Planning university course (KMITL, course 96643026). Make only the specific corrections listed below. Do not rewrite sections not mentioned. Preserve all existing analysis, citations, and structure unless told to change it.

---

## CORRECTION 1 — Fix SAWAD data throughout entire document

The previous version used SAWAD No. 2/2026 (3-year, 2.95%). The correct offering from the assignment brief is SAWAD Term 1 (2-year, 3.60%).

Find and replace ALL instances of the following throughout the entire document:

| Find | Replace with |
|------|-------------|
| 2.95% | 3.60% |
| 3-year (when referring to SAWAD) | 2-year |
| 3 years (when referring to SAWAD tenor) | 2 years |
| SAWAD No. 2/2026 | SAWAD Term 1 (2-year secured bond) |
| Tranche 1 | Term 1 |

After replacing, verify: every mention of SAWAD coupon rate should now read 3.60%, every SAWAD tenor should read 2 years.

---

## CORRECTION 2 — Replace Table 1 rows with corrected data

Find Table 1 (Candidate Debenture Screening Overview). Replace the entire table content with the following rows. Keep the same table title and footnotes, but update the footnote excess return example to match SAWAD's new +2.60%.

New rows:

| Issuer | Credit Rating (Agency) | Outlook | Coupon Rate | Tenor | Excess Return vs. Deposit¹ | Default Prob.² | Decision |
|--------|------------------------|---------|-------------|-------|---------------------------|----------------|---------|
| SAWAD (Term 1, 2-year secured bond) | A-(tha) — Fitch | Stable | 3.60% p.a. | 2 yr | +2.60% | 0.334% | Selected |
| BTS Group (Jan 2025 2-yr tranche) | BBB+ — TRIS | Negative | 4.30% p.a. | 2 yr | +3.30% | 0.582% | Selected |
| Jaymart Group (JMART26OA) | BBB+ / BBB — TRIS | Stable | 5.50–5.80% p.a. | 3 yr | +4.65% (mid) | — | Eliminated |
| Thai AirAsia (TAA) | BBB− — TRIS | Stable | 5.50% p.a. (institutional only) | 3 yr | — | — | Eliminated |
| Mudman PCL (MUD) | BB− — TRIS | Negative | 7.35% p.a. | 2 yr | +6.35% (nominal) | 2.483% | Eliminated |
| MQDC / DTGO | BBB+ — TRIS | Stable | 6.90–7.20% p.a. | ~2–3 yr | +5.90–6.20% | — | Eliminated |

Update footnote 1 to read:
"¹ Excess return = coupon rate − 1.0% (Bank of Thailand policy rate, 2026). SAWAD example: 3.60% − 1.0% = +2.60%."

---

## CORRECTION 3 — Replace Table 2 with corrected numbers

Find Table 2 (Investment Outcome — Present Value to Future Value at Maturity). Replace the entire table content:

Introductory sentence (replace existing):
"Table 2 projects the future value of each debenture position at maturity using simple interest mechanics consistent with fixed-coupon bond structure, gross of withholding tax (Investment Planning Course, 2026)."

New table rows:

| Issuer | Allocation (THB) | Coupon Rate | Tenor | Total Coupon Income (THB) | Future Value at Maturity (THB) |
|--------|-----------------|-------------|-------|--------------------------|-------------------------------|
| SAWAD Term 1 (2-year secured bond) | 600,000 | 3.60% p.a. | 2 years | 43,200 | 643,200 |
| BTS Group (2-year tranche, 4.30%) | 400,000 | 4.30% p.a. | 2 years | 34,400 | 434,400 |
| Portfolio Total | 1,000,000 | — | — | 77,600 | 1,077,600 |

Table footnote (replace existing):
"Coupon income is subject to 15% withholding tax (Investment Planning Course, 2026). Net after-tax coupon income: 77,600 × 0.85 = 65,960 THB → after-tax portfolio value: 1,065,960 THB."

---

## CORRECTION 4 — Fix summary sentence after Table 2

Find the sentence beginning "A principal of 1,000,000 Baht deployed across both debentures..." Replace it entirely with:

"A principal of 1,000,000 Baht deployed across both debentures and held to maturity returns 1,077,600 Baht gross (1,065,960 Baht net of withholding tax), representing a blended portfolio yield of 3.88% — nearly four times the 1.0% available from bank deposits during the same period (Bank of Thailand, 2026)."

---

## CORRECTION 5 — Fix all other blended yield / FV figures in body text

Find and replace ALL remaining instances throughout the document (body text, Introduction, Conclusion, anywhere):

| Find | Replace with |
|------|-------------|
| 3.49% | 3.88% |
| 3.43% | 3.88% |
| 1,087,500 | 1,077,600 |
| 1,074,375 | 1,065,960 |
| 87,500 | 77,600 |
| 74,375 | 65,960 |
| 53,100 | 43,200 |
| 653,100 | 643,200 |

---

## CORRECTION 6 — Remove stale reference

In the References section, find and delete this entry:

"Srisawad Corporation Public Company Limited. (2026). Draft prospectus — Unsubordinated and guaranteed debentures No. 2/2026. Securities and Exchange Commission Thailand. https://www.sec.or.th/"

Replace it with:

"Srisawad Corporation Public Company Limited. (2025). SAWAD secured bond offerings — Term 1 (2-year) and Term 3 (9-year) [Bond advertisement]. Thai Bond Market Association. https://www.thaibma.or.th/"

---

## CORRECTION 7 — Fix SAWAD excess return in elimination paragraph

In the paragraph discussing the screening and eliminated candidates, if SAWAD's excess return is mentioned as +1.95%, change to +2.60%.

---

## STYLE RULES

- Match existing writing style, font, and paragraph formatting exactly
- Table style: match existing tables
- Do not add new chapters or headings
- Do not remove any existing analysis or content beyond what is specified above
- Make only the listed changes — nothing else
