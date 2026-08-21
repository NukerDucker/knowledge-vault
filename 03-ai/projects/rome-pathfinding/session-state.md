---
title: Rome Pathfinding — Session State
tags: [ai, project, session-log]
status: active
created: 2026-08-06
updated: 2026-08-21
---

# Rome Pathfinding — Session Log

*Reference note → [[rome-pathfinding]]*
Repo: `~/Documents/University/Year-3/AI/rome-pathfinding`

---

## Git state

Branch `main` — clean, pushed.

| Commit | Description |
|--------|-------------|
| `46713d1` | toolbar spacing, heatmap legend both lanes, landmark CLS fix |
| `91eda39` | heatmap legend → map overlay (top-right) |
| `640a6fc` | CLS fix, spacing tokens, alignment, font-weight, dead code |
| `6b1ed4d` | Bidirectional A*(LP+ALT) + arc overlay fix |

---

## Open tasks

- [ ] Slide 2 (motivation) — cite PDF page-2 map directly under image
- [ ] Record 10–15 min YouTube demo (due before Oct 13 2026)
- [ ] Final deploy to Vercel, embed GitHub link in app

---

## Session log

### 2026-08-21

- Backdoor table corrected: Eforie→Hirsova, Neamt→Iasi (was: goal=L trivial case — mismatch with derivation)
- LP defence reframed: independence argument ("two bounds from different data"), not "+0.001 tighter"
- Demo query for Eforie backdoor: goal=Hirsova, not goal=Eforie
- Slide images moved from vault root → `01-university/year-3/ai/`
- `rome-pathfinding.md` restructured: stable content note + image embeds + session-state split
- Vault-wide Reference/Session Split rule established

### 2026-08-20

- Viz enhancements shipped: heatmap, click-to-landmark, toolbar refactor
- Slide 6 LP diagram built as SVG/HTML → PNG screenshot at `~/Documents/University/Year-3/AI/rome-pathfinding/slides/slide-06-lp-diagram.png`
- ALT save/restore: `saveALTState()` / `restoreALTState()` in `heuristic.ts`
- CSS fixes: SVG `width="2800" height="1900"` CLS fix; font-weight 650→600; dead `.arc-toggle-btn` deleted

### 2026-08-19

- Other groups confirmed: random/feel/favor h all inadmissible → A* loses optimality
- Prof clarification: SLD banned in all forms; road km + pixel coords allowed
- Combined heuristic stats final: LP 0.729, ALT lm8 0.985, combined 0.986 (380 directed pairs)

### 2026-08-06 (project start)

- Stack decision: Vite 8 + React 19 + TS + bun
- LP heuristic implemented via scipy/HiGHS offline solve
- ALT with lm2/lm4/lm8 presets implemented
