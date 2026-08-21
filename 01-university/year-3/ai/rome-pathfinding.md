---
title: Rome Pathfinding — AI Assignment
tags: [university, year-3, ai, project, assignment]
status: active
created: 2026-08-06
---

# Rome Pathfinding (AI Assignment)

Repo: `~/Documents/University/Year-3/AI/rome-pathfinding` → `github.com/NukerDucker/rome-pathfinding`
Due: **2026-10-13** | Submission: YouTube video + Vercel URL + GitHub link

*Session log and git state → [[session-state]]*

---

## Assignment brief

- **Deliverables:** Web app URL, GitHub link (embedded in app), 10–15 min YouTube demo
- **Grading:** Creativity (heuristic + UX/UI) > Completeness > Presentation
- **Rule:** Present ONE best algorithm. Multiple algos = no creativity credit. Road block feature = zero score impact.

## Stack

- **Vite 8 + React 19 + TypeScript ~6.0** → Vercel
- Package manager: **bun** — `bun dev`
- React Compiler enabled (`babel-plugin-react-compiler`)
- Pure client-side SPA, no SSR

## Grading priorities (from prof)

1. **Creative heuristic function** — the core mark
2. **UX/UI presentation quality**
3. **Presentation delivery**

---

## Heuristic rules

- **Data source:** ONLY page 2 of assignment PDF. Nothing external.
- **Allowed:** pixel coordinates, protractor degrees, road km — anything derivable from PDF.
- **Banned:** GPS data. **Straight-line distance (SLD) in any form.**
- **Must be custom.**

### What counts as SLD (banned) vs what's allowed

| Method | Verdict |
|--------|---------|
| Measure SLD from map image | ❌ banned |
| Real-world SLD + terrain adjustment | ❌ banned (still SLD) |
| SLD from any external source | ❌ banned |
| Road km from PDF | ✅ allowed |
| Dijkstra precomputed road distances | ✅ allowed |
| Pixel coords for vector decomposition | ✅ allowed |

*Clarified 2026-08-19 — other groups asked prof directly.*

---

## Current heuristic: Combined LP+ALT (`heuristic.ts`)

`h = max(hLP, hALT)` — max of admissibles = admissible and tighter.

### LP Vector-Decomposition (`heuristic_table.ts`)

- h(a,b) = min Σ αᵢ·kmᵢ s.t. Σ αᵢ·vecᵢ = chord_AB
- Solved offline with scipy/HiGHS; uses pixel coords + road km only
- Mean h/road: **0.729** — admissible on all 190 pairs

![[slide-06-lp-diagram.html]]

**File:** `~/Documents/University/Year-3/AI/rome-pathfinding/slides/slide-06-lp-diagram.png` | Source HTML: `~/KnowledgeVault/slide-06-lp-diagram.html`

### ALT — Landmarks + Triangle Inequality (`alt.ts`)

- h(n, goal) = max_L |d(L,n) − d(L,goal)|
- Three presets: **lm2** (Eforie, Oradea), **lm4** (+ Neamt, Giurgiu), **lm8** (+ Timisoara, Vaslui, Drobeta, Hirsova)
- Selectable in UI — `setALTPreset()` in `heuristic.ts`
- Admissible by triangle inequality — Waze/Google Maps technique
- Dijkstra precomputed at module load (8 × 20 nodes, negligible cost)

#### Degree-1 "backdoor" landmarks — exact h for specific goals

When landmark L is degree-1 (only one edge), and goal = L's only neighbor:

```
d(L, n) = edge_km + d(neighbor, n)   for all n
|d(L,n) − d(L,goal)| = d(goal, n)   ← exact true distance
```

Romania backdoors:

| Landmark | Backdoor to | In preset |
|---|---|---|
| Giurgiu (degree-1→Bucharest) | exact h for goal=Bucharest | lm4+ |
| Eforie (degree-1→Hirsova) | exact h for goal=Hirsova | lm2+ (all) |
| Neamt (degree-1→Iasi) | exact h for goal=Iasi | lm4+ |

![[slide-08-base.png]]

Consequence: landmark count effect is **invisible** for queries where goal has a backdoor landmark already in scope. e.g. Arad→Bucharest (Giurgiu, lm4), Oradea→Hirsova (Eforie, lm2) all show same generated count at lm2/lm4/lm8.
**To demo Eforie backdoor: use goal=Hirsova, not goal=Eforie.**

#### How to choose landmarks

**1. Farthest-first (best general method)**
Each next landmark = node farthest from all existing landmarks (max min-dist). Spreads maximally. Used by Waze/Google Maps.

**2. Geographic extremes (our approach)**
Pick nodes at compass corners — far N/S/E/W. Works on spatially embedded graphs.

**3. Avoid high-degree hubs**
Central nodes give weak bounds. Dead-ends (degree-1) give exact bounds for specific goals.

**4. Boundary/convex hull nodes**
Shortest paths hug the boundary → boundary landmarks near optimal paths → tight bounds.

![[slide-10-landmarks.png]]

| Strategy | Our landmarks | Quality |
|---|---|---|
| Geographic extremes | Eforie (E), Oradea (W), Neamt (NE), Giurgiu (S) | ✓ Good |
| Degree-1 backdoors | Eforie, Neamt, Giurgiu | ✓ Exact h for those goals |
| Farthest-first | Converges to similar nodes on 20-node graph | ≈ Same |

On 20 nodes, all strategies pick similar landmarks. For presentation: lm8 geographic extremes + corner fill ≈ farthest-first — defensible.

#### Where landmark count actually matters

Goal must have NO backdoor in smaller preset. Try: goal = Arad, Sibiu, Pitesti, Craiova, Lugoj, Rimnicu Vilcea.

#### Why `generated` count often doesn't change between presets

`generated` = nodes ever discovered (added to frontier). Even perfect h discovers neighbors of each expanded node. Count only drops if weaker h causes extra expansions. On 20 nodes most heuristics are tight enough.

### Combined performance

- `h = max(hLP, hALT)` → mean h/road **0.986** (380 directed pairs)
- ALT lm8 alone: **0.985**
- LP alone: **0.729**
- Combined buys +0.001 over ALT alone — tightness is not the justification for keeping LP

**Why keep LP (Q&A answer):** LP is an independent bound from vector decomposition + offline LP — different data and method from landmark distances + triangle inequality. `max(hLP, hALT)` means admissibility never rests solely on landmark choice.

**Other groups (2026-08-19):** random h, eye/feel h, favor h — all inadmissible, A* loses optimality.

---

## Algorithms

| Key | Label | Heuristic | Optimal | Complete |
|-----|-------|-----------|---------|----------|
| bfs | BFS | — | Yes* | Yes |
| dfs | DFS | — | No | No* |
| greedy | Greedy | LP+ALT | No | No* |
| astar | A* (LP) | LP only | Yes | Yes |
| astaralt | A* (LP+ALT) | combined | Yes | Yes |
| astaraltonly | A* (ALT only) | ALT only (active preset) | Yes | Yes |
| biastar | Bidir. A* (LP+ALT) | combined | Yes | Yes |
| ucs | UCS | — | Yes | Yes |
| biucs | Bidirectional UCS | — | Yes | Yes |

**Bidirectional A*:** Pohl 1971 stopping (minF_fwd + minF_bwd ≥ μ). Slower on 20 nodes (overhead > savings); O(b^(d/2)) advantage at millions of nodes.

## Self-checks (run at module load)

- `heuristic.ts`: hLP(Arad,Bucharest) ≈ 388; combined h ≤ 418
- `astar.ts`: Arad→Bucharest = 418
- `biastar.ts`: Arad→Bucharest = 418; trivial same-city case
- `search.ts`: pathCost(Arad→Sibiu→Fagaras→Bucharest) = 450

---

## UI

Bento two-lane side-by-side algo comparison. Step-by-step visualizer, frontier/visited highlight, arc overlay, speed slider, play/pause/step. shadcn/ui + lucide-react.

**H-value heatmap** (`showHeatmap` toggle): normalizes `hALTOnly(city, goal)` across all 20 cities; hue = norm×240 (0=red near goal, 240=blue far). Rendered in separate `<g>` BEFORE node groups (CSS specificity issue). Legend: frosted-glass pill top-right both lanes.

**Click-to-landmark** (`pickLandmarkMode`): click city → `customLandmarks: NodeId[]` → `setCustomLandmarks()` → `makeHALTArbitrary()`. `ALL_CITY_DIST` precomputed for any city. Dashed gold ring on selected.

**Toolbar:** 4 groups — Legend | Overlays | Playback | Speed. CSS spacing tokens `--sp-1`–`--sp-6`.

![[slide-13-heatmap.png]]

**Conclusions slide:** QR code to deployed app — stays up during Q&A.

---

## Slide image plan

Five evidence slides ranked by impact:

1. **Slide 13 (UI heatmap)** ✅ `slide-13-heatmap.png`
2. **Slide 8 (backdoor landmarks)** ✅ `slide-08-base.png`
3. **Slide 6 (LP decomposition)** ✅ `slide-06-lp-diagram.html` → PNG in Documents/University
4. **Slide 10 (landmark selection)** ✅ `slide-10-landmarks.png`
5. **Slide 2 (motivation)** — PDF page-2 map, cited directly under image

**Do not add:** photos of Rome/roads, stock network imagery, AI-generated images.

---

*See also: [[session-state]] — session log, git state, dated progress*
