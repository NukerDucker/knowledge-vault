---
title: Romania Video — Production Log
tags: [ai, project]
status: active
course: 01276342
created: 2026-10-01
updated: 2026-10-01
---

# Romania Video — Production Log

*Assignment note → [[rome-pathfinding]]*
*Narration script → [[rome-video-script]]*

---

## 2026-10-01 — Manim animation rendered

### Repo
`~/Code/romania-video` — cloned from `github.com/ttithipan/romania-video`  
Setup: `uv` venv, `manim==0.21.0`, `scipy>=1.17`

### What was built
28-chapter Manim animation explaining the pathfinding algorithms, polished for DaVinci Resolve import.

#### Visual improvements over original
- `MovingCameraScene`: camera zooms on Giurgiu (ch_09 landmark reveal), Sibiu/Pitesti fork (ch_25 stopping problem)
- **UCS trace (ch_02):** live g cost labels on nodes (cyan waiting → purple settled), frontier panel top-5 sorted by g
- **A* trace (ch_18):** live g (purple) + f (green) labels per node, frontier panel sorted by f
- Chapter counter removed from top-left
- All `say()` captions trimmed to 2–6 words (narration is voiceover in DaVinci)

#### Chapter structure
| ch | method | content |
|----|--------|---------|
| 00 | journey | cold open, Arad→Bucharest problem |
| 01 | routes | two routes comparison (3 roads vs 4) |
| 02 | ucs | UCS live trace with g labels + frontier |
| 03 | ucsproof | UCS optimality proof |
| 04 | waste | UCS exploring wrong direction |
| 05 | astar | A* intro (g + h = f) |
| 06 | optimism | admissibility bars |
| 07 | lp | LP heuristic concept |
| 08 | lpproof | LP lower bound proof |
| 09 | landmark | landmark heuristic + camera zoom |
| 10 | triangle | triangle inequality |
| 11 | combine | LP+ALT max combination |
| 12 | ensemble | max justified on real pair |
| 13 | admissible | admissibility scatter plot (380 pairs) |
| 14 | tightness | tightness bars (mean h/d) |
| 15 | landmarks | lm2/lm4/lm8 comparison |
| 16 | exact | exact estimates table (Giurgiu degree-1) |
| 17 | consistency | consistency property |
| 18 | guided | A* live trace with g/f labels |
| 19 | breadth | expansion bar chart (6 algorithms) |
| 20 | coverage | per-city coverage (goal: Bucharest) |
| 21 | saving | scatter plot: UCS vs A* (352/380 below diagonal) |
| 22 | optimality | optimality table (380/380 vs 319/380 greedy) |
| 23 | guarantee | optimality proof bars |
| 24 | bidirectional | bidirectional A* trace (cyan/gold) |
| 25 | meeting | stopping problem + camera zoom |
| 26 | stop | bidirectional stopping condition |
| 27 | metrics | final comparison metrics + outro |

### Output
- **28 clips:** `media/chapters/ch_00.mp4` → `ch_27.mp4`, 1080p60, silent
- **Narration timestamps:** `narration.md` in repo (regenerated on full render)
- **Timeline JSON:** `timeline.json` in repo
- **Render script:** `render_chapters.sh` — rerenders all chapters anytime

### DaVinci editing notes
Each chapter method in `film.py` has a `# EDIT ch_NN —` comment with:
- Narration timing hints
- Cut point suggestions
- Music/sfx cue recommendations
- Which chapters can be cut if running long

### Remaining video tasks
- [ ] Record or generate narration (script: `rome-video-script.md`)
- [ ] Screen-record web app demo after UI rework freeze (friends' work)
- [ ] DaVinci edit: sequence clips, add audio, cold open, music, sfx, end card
- [ ] Export → upload YouTube (unlisted first for review)
- [ ] Submit via Google Form before 09:00, 2026-10-13

### Timing check
- Silent animation: ~9 min (under 10 min floor)
- Narration script: ~2,318 words ≈ 15.5 min at 150 wpm (over 15 min cap)
- **Action needed:** cut ~5 min of narration or speed narration to ~160–170 wpm
- Stats chapters easiest to cut: ch_13–ch_17, ch_20–ch_22 (pick ~4 of the 9)
