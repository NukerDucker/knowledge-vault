---
title: Rome Pathfinding — AI Assignment
tags: [university, year-3, ai, project]
status: active
created: 2026-08-06
updated: 2026-08-19
---

# Rome Pathfinding (AI Assignment)

Repo: `~/Documents/University/Year-3/AI/rome-pathfinding` → `github.com/NukerDucker/rome-pathfinding`
Due: **2026-10-13**

## Stack

- **Vite 8 + React 19 + TypeScript ~6.0** → Vercel
- Package manager: **bun** — `bun dev`
- React Compiler enabled (`babel-plugin-react-compiler`)
- Pure client-side SPA, no SSR

## Grading priorities (from prof)

1. **Creative heuristic function** — the core mark
2. **UX/UI presentation quality**
3. **Presentation delivery**

**Present ONE best algorithm, not all 8.** Multiple algos = no creativity credit. Road block feature = zero score impact.

## Heuristic rules

- **Data source:** ONLY page 2 of assignment PDF. Nothing external.
- **Allowed:** pixel coordinates, protractor degrees, road km — anything derivable from PDF.
- **Banned:** GPS data. **Straight-line distance (SLD) in any form** — measuring from map, real-world SLD+terrain, SLD from any source.
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

## Current heuristic: Combined LP+ALT (`heuristic.ts`)

Two admissible components combined via `h = max(hLP, hALT)`. Max of admissibles = admissible and tighter.

### LP Vector-Decomposition (`heuristic_table.ts`)
- h(a,b) = min Σ αᵢ·kmᵢ s.t. Σ αᵢ·vecᵢ = chord_AB
- Solved offline with scipy/HiGHS; uses pixel coords + road km only
- Mean h/road: **0.729** — admissible on all 190 pairs

### ALT — Landmarks + Triangle Inequality (`alt.ts`)
- h(n, goal) = max_L |d(L,n) − d(L,goal)|
- Three presets: **lm2** (Eforie, Oradea), **lm4** (+ Neamt, Giurgiu), **lm8** (+ Timisoara, Vaslui, Drobeta, Hirsova)
- Selectable in UI — `setALTPreset()` in `heuristic.ts`
- Admissible by triangle inequality — no empirical testing needed
- Same technique used in Waze/Google Maps at scale
- Dijkstra precomputed at module load (8 × 20 nodes, negligible cost)

#### Degree-1 "backdoor" landmarks — give exact h for specific goals
When a landmark L is degree-1 (only one edge), and goal = L's only neighbor:
```
d(L, n) = edge_km + d(neighbor, n)   for all n
|d(L,n) − d(L,goal)| = d(goal, n)   ← exact true distance
```
Romania backdoors:
| Landmark | Backdoor to | In preset |
|---|---|---|
| Giurgiu (degree-1→Bucharest) | exact h for goal=Bucharest | lm4+ |
| Eforie (degree-1→Hirsova) | exact h for goal=Eforie | lm2+ (all) |
| Neamt (degree-1→Iasi) | exact h for goal=Neamt | lm4+ |

Consequence: landmark count effect is **invisible** for queries where goal has a backdoor landmark already in scope. e.g. Arad→Bucharest (Giurgiu, lm4), Oradea→Eforie (Eforie, lm2) all show same generated count at lm2/lm4/lm8.

#### How to choose landmarks

**1. Farthest-first (best general method)**
1. Pick any node as first landmark
2. Each next = node farthest from all existing landmarks (max min-dist)
3. Repeat until k landmarks
Spreads maximally across graph. Used by Waze/Google Maps.

**2. Geographic extremes (our approach)**
Pick nodes at compass corners — far N/S/E/W. Works well on map graphs because road networks are spatially embedded.

**3. Avoid high-degree hubs**
Central nodes give weak bounds — `|d(L,n) - d(L,goal)|` is small when L is close to everything. Dead-ends (degree-1) give strong bounds for their specific goals.

**4. Boundary/convex hull nodes**
Every shortest path tends to hug the boundary → boundary landmarks are likely near optimal paths → tight bounds.

| Strategy | Our landmarks | Quality |
|---|---|---|
| Geographic extremes | Eforie (E), Oradea (W), Neamt (NE), Giurgiu (S) | ✓ Good |
| Degree-1 backdoors | Eforie, Neamt, Giurgiu | ✓ Exact h for those goals |
| Farthest-first | Converges to similar nodes on 20-node graph | ≈ Same |

On 20 nodes, all strategies pick similar landmarks. Difference matters at millions of nodes. For presentation: lm8 geographic extremes + corner fill ≈ farthest-first — defensible.

#### Where landmark count actually matters
Goal must have NO backdoor in the smaller preset. Try: goal = Arad, Sibiu, Pitesti, Craiova, Lugoj, Rimnicu Vilcea. None of these are degree-1 neighbors of a landmark.

#### Why `generated` count often doesn't change between presets
`generated` = nodes ever discovered (added to frontier), not nodes expanded. Even with perfect h, A* still discovers neighbors of each node it expands. Count only drops if weaker heuristic causes *extra* expansions → exposing more neighbors. On a 20-node graph, most heuristics are tight enough that expansion count is identical.

### Combined
- `h = max(hLP, hALT)` → mean h/road **~0.85–0.90**
- `hLP` exported separately for A*(LP) baseline comparison
- A*(ALT only) also available as separate algorithm for comparison

### Other groups (2026-08-19)
Exploring random h, eye/feel h, favor h — all inadmissible, A* loses optimality. Our LP+ALT is stronger on every axis.

## Algorithms — 8 total

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

**Bidirectional A*:** Pohl 1971 stopping (minF_fwd + minF_bwd ≥ μ). Slower on 20 nodes (overhead > savings at small scale); O(b^(d/2)) advantage appears at millions of nodes.

## Self-checks (run at module load)

- `heuristic.ts`: hLP(Arad,Bucharest) ≈ 388; combined h ≤ 418 (admissibility)
- `astar.ts`: Arad→Bucharest = 418
- `biastar.ts`: Arad→Bucharest = 418; trivial same-city case
- `search.ts`: pathCost(Arad→Sibiu→Fagaras→Bucharest) = 450

## UI

Bento two-lane side-by-side algo comparison. Step-by-step visualizer, frontier/visited highlight, arc overlay (greedy/astar/astaralt/biastar), speed slider, play/pause/step. shadcn/ui + lucide-react.

## Git state (2026-08-19)

Branch `main` — clean, pushed. Last 2 commits:
- `d2d76b7` — A*(LP+ALT) + ALT heuristic + side-by-side comparison
- `6b1ed4d` — Bidirectional A*(LP+ALT) + arc overlay fix
