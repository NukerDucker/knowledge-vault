---
title: "KMITL B-App — Build Handoff (report + presentation)"
tags:
  - university
  - project
  - reference
status: active
subject: uxui
course: 01276545
updated: 2026-10-11
---

# Build Handoff — `GX_FinalPrototype.pdf` + `GX_FinalPresentation.pdf`

**Audience: a Claude session with the `docx` and `pptx` skills.** This file is the complete brief.
The Figma work it depends on is already done and logged in [[uxui-figma-changelog-2026-10-11]] —
read that first; it is the authority for every "what changed and why" claim.

Deadline **2026-10-19**. Grading: Part 1 = 5 pts (Design Rationale 2 · Presentation Flow 1.5 · AI
Transparency 1.5), Part 2 = 20 pts (Criterion 1 Screen Elements & Real Data, 2 Consistency & Design
System, 3 Defined User Flow, 4 Usability & Accessibility).

---

## 1 · Deliverables

| # | Artifact | Source | Output |
|---|---|---|---|
| 1 | **`GX_FinalPrototype.pdf`** — the report | new note `01-university/year-3/uxui/uxui-final-report.md` → export script | `~/Documents/University/Year-3/UXUI/GX_FinalPrototype.pdf` |
| 2 | **`GX_FinalPresentation.pdf`** — exam deck | fix the `.pptx` built from the Canva export | `~/Documents/University/Year-3/UXUI/GX_FinalPresentation.pdf` + the `.pptx` |

Export pipeline: `~/Code/ut-export/export.py` (markdown → print-quality PDF, same one used for the UT
submission). **Caution:** its `MD` constant is hardcoded to `uxui-ut-submission.md` — parameterise it
(env var or arg) before use; do not overwrite the UT source.

Deck flow agreed with the user: Claude fixes the **pptx** → user imports into Canva → user adjusts
**alignment/decoration only**. So the pptx must be content-complete and style-simple: plain text
boxes, simple rectangles, no grouped art, no exotic shapes.

## 2 · Hard rules

1. **Measured numbers only.** Every contrast ratio comes from the table in the changelog (computed
   from live hexes). Claiming untested numbers = Red-level AI use = deducted.
2. **No theory without an artefact.** Each named model must explain something concrete in this
   project; one line of theory + one screen where it shows.
3. **Screens carry `Member / Student` captions** in the PDF (brief: name + user type under every
   frame, in Figma and the PDF). Captions already renamed in Figma; carry them into the PDF.
4. **AI Use Log** is 1 page at the end of the report AND a presentation slide (rubric puts it in
   Part 1; brief wants the page). Same content, reconciled — see §7.
5. **UT data stays real.** Five real participants (Putt, Mind, Nhow, ching ching, cheesy). Cite only
   what `uxui-usability-test.md` records. Fabricating results is Red-level.
6. Slides answer in the order **Problem (UX) → Solution (UI) → Demo**.

## 3 · Live design system fingerprint (read from the live file 2026-10-11)

| Token | Value | Use |
|---|---|---|
| Orange/500 | `#E8622D` | CTAs, active nav, selected states |
| Navy/500 | `#1B2A5B` | headings, body, labels **(the old `#1A2340` is gone — never quote it)** |
| Neutral/0 · 50 · 100 · 300 · 400 · 900 | `#FFFFFF` `#F5F7FA` `#E5E7EB` `#9CA3AF` `#6B7280` `#111827` | surfaces, text, disabled |
| Status fills | Green `#047857` · Amber `#B45309` · Rust `#C2410C` · Grey `#4B5563` · Red `#DC2626` · Slate `#6B7280` | Available/Approved · Upcoming/Busy · Partial/Under Review · Cancelled · Rejected · Unavailable/Completed |
| Font | Inter | Display 32 Bold · H1 28 Bold · H2 24 SemiBold · H3 20 SemiBold · Body Large 16 · Body Medium 14 · Body Small 12 · Caption 11 · Label 12 |
| Semantic tokens | `Text/Primary` navy · `Text/Secondary` `#6B7280` · `Text/Hint` `#6B7280` (raised 2026-10-11) · `Text/Disabled` `#9CA3AF` · `Text/OnPrimary` white | collections `_Color – Primitive`, `Color – Semantic` |
| Grid | columns, 8px gutter, 16px offset, orange @10% | present on all 34 screens |

Typography rationale for the slides/report: Inter chosen for neutral, highly legible UI letterforms
across weights — one family covers 9 roles, so the file needs no second font; the scale is a modular
ladder (32/28/24/20/16/14/12/11) mapping heading/body/label usage (Jakob's Law: users spend most of
their time in *other* apps with system-ish sans-serifs; Inter reads as native there).

## 4 · Measured contrast table (use verbatim)

| Pair | Ratio | Verdict |
|---|---|---|
| Navy `#1B2A5B` on white | 13.74:1 | AAA |
| White on `#047857` Available/Approved | 5.48:1 | AA |
| White on `#C2410C` Partial/Under Review | 5.18:1 | AA |
| White on `#B45309` Upcoming/Busy | 5.02:1 | AA |
| White on `#4B5563` Cancelled | 7.56:1 | AAA |
| White on `#DC2626` Rejected | 4.83:1 | AA |
| `#6B7280` on white (secondary/hint) | 4.83:1 | AA |
| White on orange CTA `#E8622D` — **all button labels 16px Semi Bold** | 3.38:1 | ⚠️ deliberate, defended |
| White on orange, small controls (chips/tiles, ≤14px) | 3.38:1 | ⚠️ deliberate, defended |
| Navy `#1B2A5B` on orange (fallback, unused) | 4.07:1 | fails normal text |
| `#9CA3AF` on white (disabled only) | 2.54:1 | exempt |

The white-on-orange position covers button labels AND small controls, and must be stated with both
caveats: the uxmovement argument's evidence is preference surveys, and its low-ratio allowance is
justified via large text — which 16px SemiBold is not. The support is (a) a ratio is an
approximation, (b) five real participants raised no legibility issue. **Never claim 4.58:1 for the
button; that was the old navy. Never claim a large-text exemption for the button label — an earlier
18.66px Bold experiment was reverted for type-scale consistency.**

## 5 · Report structure — with theory anchors

| Section | Content (source) | Theory to cite |
|---|---|---|
| Cover + group member page | project, Group 2 Mookrata, who built what: Napaul 16 screens · Chonchanok 10 · Mawin 8 | — |
| 1 Background & problem | LINE submission fails silently; professor walks ECC reading door boards, still double-booked. Two users, one failure point: no visibility | Double Diamond; Design Thinking Empathize→Define |
| 2 UX process W3→W11 | market comparison → journey map → POV/HMW → Hooked+Kano → Crazy 8s/storyboard → story map → sitemap/card sorting → wireflow → hi-fi → UT (`uxui-facility-booking-project` spine table) | Design Thinking stages; affinity mapping; card sorting |
| 3 Research findings | real quotes, empathy map, journey emotional dip — satisfaction 1/5 at Stage 4 (Wait) | Customer Journey Mapping (emotional curve); IDEO HMW framing |
| 4 Design rationale | live availability + status notification = Kano **Basic** AND Hooked **Variable Reward**; build order Basics → Performance → Delight; cut AI-suggestion & loyalty (untraceable); ethics: single lifecycle, notifications only on real state changes | Kano Model; Hooked (Trigger→Action→Variable Reward→Investment) |
| 5 IA & flow | sitemap (student/staff), story map, 4-step wizard, role split browse/book/track | Miller's Law (chunking); Hick's Law (single-select sort, presets); Progressive Disclosure |
| 6 Design system | palette, Inter scale, tokens, 10-variant badge system with the rule **stroke = fill** | Jakob's Law; Gestalt similarity + common region; Von Restorff (status emphasis) |
| 7 Accessibility | §4 table; the badge story (component fixed ≠ instances fixed — 29 stale overrides swept 2026-10-11); uniform button typography (16 SemiBold across all variants + auth buttons, replacing three mismatched sizes); touch targets (21 back-buttons moved to 44pt Header Bars; day cells 24×24 = WCAG 2.5.8 AA floor, below Apple 44 — stated, not hidden); colour+icon+text; CTA contrast position stated with measured 3.38:1 | WCAG 2.2 AA: 1.4.3, 1.4.11, 1.4.1, 2.5.8; POUR; Fitts's Law |
| 8 Prototype completeness | 34 screens; happy path Login→Home→Room Detail→Book Now→Select Date→Details→Upload→Review→Submit→Confirmation→Detail; empty states (Search zero-result, Booking History ×2); error states (capacity inline); overlays; **0 broken links** (full reaction sweep, 2026-10-11) | Nielsen #1 visibility of system status, #5 error prevention, #9 help users recover |
| 9 Usability test & iteration | 5 participants, think-aloud, findings per person, improvement tracker, before/after pairs (`assets/ut/2026-10-11/`); regressions found (Mind contradicted three tracker rows) | Think-aloud protocol; Nielsen severity rating |
| 10 Positioning | vs BU (status, no discovery) · RMUTL (discovery, onboarding wall) · Calendly (availability, no approval) · Skedda · LibCal · Google Calendar | Competitive analysis |
| 11 Conclusion + future work | shipped vs deferred: auto-reopen cancelled slots, push notifications | — |
| Part B per member | Chonchanok (browse, 10 frames) → Napaul (book, 16) → Mawin (track, 8): counted-page math under the brief's rules, own decisions, a11y numbers, UT findings, before/after | Nielsen heuristics per screen family |
| Appendix | AI Use Log (rubric columns `# · Tool · Used for (page/section) · Level · What you changed + why · Member`) | — |

Assets: `01-university/year-3/uxui/assets/ut/2026-10-11/` (current screens + before/after) ·
`assets/decision/` (prototype evolution, sitemaps, design system) · `~/Documents/University/Year-3/UXUI/`
(exported PDFs, Components, Device Frame, Usability_Test).

## 6 · Deck spec — `GX_FinalPresentation`

Source: `~/Downloads/KMITL-B App.pdf` (30 slides, Canva, author Chonchanok). Rebuild as pptx with
these changes, keeping slide order unless stated:

1. **Slide 14 (Accessibility Audit)** — replace `Navy (#1A2340) on White: 14.18:1` with **`#1B2A5B` on white: 13.74:1**; replace `#E86027` with `#E8622D`; replace the orange line with: *"White on `#E8622D` = 3.38:1. Every button label is a uniform 16px Semi Bold, and white-on-orange is retained deliberately — a contrast ratio is an approximation, white carries no hue distortion on a saturated fill, and five usability participants raised no legibility issue."* Keep the Myths-of-Contrast slide as the supporting argument (both caveats in speaker notes). Do not claim the large-text exemption.
2. **Add evidence slide after 14** — the §4 table (post-fix badge ratios 5.48/5.18/5.02/7.56/4.83), touch targets (21 header back-buttons ≥44pt; day cells 24px meet WCAG 2.5.8 AA, below Apple's 44 comfort bar — say both), colour+icon+text rule.
3. **Palette slide** — add the six live status colours.
4. **Add 4 slides**: role division (browse/book/track + why speaking order follows the flow) · standout vs BU/RMUTL/Calendly/Skedda/LibCal/Google Calendar · conclusion · future work.
5. **Declare the split on the agenda slide**: group section ≤12 slides / 10 min; individual 5 min / ≤6 slides each with the skeleton *my task+screens · live demo · usability & accessibility numbers · confirmation/error or empty/error state · UT summary · before/after*.
6. **One theory line per rationale slide**, matching the report: Kano + Hooked (§4), Miller + Hick (§5), Jakob + Gestalt + Von Restorff (§6), WCAG + Fitts (§7), Nielsen #1/#5/#9 (§8).
7. Fix the deck's own numbers everywhere they say 14.18 or 4.58 — those are the old navy.

## 7 · AI Use Log (reconcile, then use in both artifacts)

Reconcile the recorded 3-row version ([[uxui-exam-task-split]] / [[uxui-decisions-log]]) against the
1-row version in [[uxui-final-audit]]. Truthful additions from 2026-10-11, all **Green** (research +
audit as reference; every decision made by the team):

| # | Tool | Used for (page/section) | Level | What you changed + why | Member |
|---|---|---|---|---|---|
| 1 | Claude | Component naming conventions research; where to source UI components; icon recommendations (Components page) | Green | Suggestions used as reference only; final naming, selection, icons decided by the team | Napaul |
| 2 | Claude | Figma file audit: stale badge instance overrides, duplicate navy, grey text contrast, touch targets, grid coverage | Green | Findings verified against the live file, then fixed by the team via the Desktop Bridge; all repairs logged in [[uxui-figma-changelog-2026-10-11]] | Napaul |
| 3 | ChatGPT | Mock data (room names, booking IDs, activity titles) | Green | Adjusted to real ECC building/room naming and KMITL conventions | Team |

Before/After slides are only required for Yellow-level use; none of the above is Yellow. Keep the
log to **one page**.

## 8 · Open items the prose must state honestly

1. **Dead ends: none left.** The 28 stale reactions found in the audit were repaired the same session
   (dropdown toggles retargeted to their surviving variants; dangling attachment-hover targets
   removed) — see changelog §9. The report can state "0 broken prototype links, verified by a full
   reaction sweep".
2. Day cells/chips below 44pt — WCAG 2.5.8 AA floor is 24×24 and they meet it; Apple's 44pt is the
   comfort target and the calendar grid cannot take it without redesign.
3. Layout grids are on in Figma but do not render into PNG exports — if the report needs
   grid-visible screens, export with grids enabled (the UT submission shows the with-grid mode).

## 9 · Verification before handing back

- [ ] Every ratio in report and deck appears in §4/changelog, unchanged.
- [ ] No occurrence of `#1A2340`, `#E86027`, `14.18`, `4.58`, or `18.66` in either artifact.
- [ ] Report: captions on every embedded screen; AI Log is the last page; per-member screen counts match §5.
- [ ] Deck: group section ≤12 slides; splitting declared; pptx opens clean in PowerPoint and in Canva import.
- [ ] Both PDFs land in `~/Documents/University/Year-3/UXUI/` with the exact names.

---

*Source of the Figma facts → [[uxui-figma-changelog-2026-10-11]] · Project hub → [[uxui-facility-booking-project]] · Evidence → [[uxui-usability-test]]*
