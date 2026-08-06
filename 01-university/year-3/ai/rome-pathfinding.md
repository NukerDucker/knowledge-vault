---
title: Rome Pathfinding — AI Assignment
tags: [university, year-3, ai, project]
status: active
created: 2026-08-06
---

# Rome Pathfinding (AI Assignment)

Repo: `~/Documents/University/Year-3/AI/rome-pathfinding`
Due: **2026-10-13**

## Stack

- **Vite 8 + React 19 + TypeScript ~6.0** → Vercel
- Package manager: **bun** — `bun dev`
- React Compiler enabled (`babel-plugin-react-compiler`)
- Pure client-side SPA, no SSR

**Why:** React over Svelte for familiarity under deadline; Vite for fast dev; Vercel for zero-config deploy with stable grader URL.

## Grading priorities (from prof)

Where the marks live — the **creativity** the prof looks for:
1. **Creative heuristic function** — the core
2. **UX/UI presentation quality**
3. **Presentation delivery**

**NOT** the creativity prof cares about:
- **Multiple search algorithms** — allowed, but no creativity credit. Prof said **present ONE best, not all 6**. Extras can go in but don't move score.
- **Road block feature** — optional, **zero score impact**.

Prof cares most about the **core**: heuristic + presentation.

## Heuristic rules (custom heuristic, A*/greedy phase)

- **Data source:** ONLY data on **page 2 of assignment PDF**. Nothing external.
- **Allowed:** anything derivable from that PDF — pixel coordinates, protractor/angle degrees, etc.
- **Banned:** GPS data, and **straight-line distance (SLD) as heuristic**. SLD may not even be used to *derive* another value.
- **Must be a CUSTOM heuristic.**
- Does NOT affect BFS (uninformed, no heuristic).

## Team status (2026-08-06)

| Who         | Task                    | Status                                            |
| ----------- | ----------------------- | ------------------------------------------------- |
| bento       | Custom algo (heuristic) | Done — behavior issue, discussing with prof today |
| cheesy      | Bidirectional search    | Done                                              |
| mind        | Uniform cost search     | Done                                              |
| putt + nhow | Visual map adjustments  | In progress                                       |

## Planned viz

Dual animated step-by-step search viz, live metrics ticker, speed slider.

---

## Code status (read from repo, 2026-08-06)

Branch `main`, 5 commits. Latest: *Add algorithm comparison panel (time, memory, path cost)*.
**Uncommitted:** modified `App.tsx`, `greedy.ts`, `heuristic.ts`, `search.ts`; untracked `_core.ts`, `astar.ts`, `bench.ts` (A* + heuristic engine + benchmark not committed yet).

This local checkout = **bento (kk)'s work** (arc-heuristic branch content, uncommitted locally). All teammate work lives on **remote branches — none merged to `main` yet** (main frozen since first panel build).

Remote: `github.com/NukerDucker/rome-pathfinding`

### Remote branches (not yet merged)
| Branch | Owner | Contents | New files |
|--------|-------|----------|-----------|
| `arc-heuristic` | bento (kk) | Arc/Bento heuristic + A* + greedy, hi-res 4000×2250 coords, arc viz | `astar.ts`, `heuristic.ts` |
| `bidirectionalucs` | cheesy | Bidirectional UCS/Dijkstra module | `biucs.ts` |
| `uniform-cost-search` | mind | UCS + path cost side panel | `ucs.ts` |
| `frontend-refinements` | putt + nhow | Map redesign, ring markers on select, slider readouts, random-city dice button | — |

### Integration — DONE on `integrate` branch (2026-08-06)

All 4 remote branches combined into `integrate` (off `main`, **not merged to main, not pushed** — awaiting review).

**Coordinate conflict resolution — DECOUPLE:** heuristic keeps its 4000×2250 geometry via a private `HCOORDS` const embedded in `heuristic.ts`; `romania.ts` uses frontend-refinements' 600×450 map coords. Heuristic reads `HCOORDS` for x/y, `ROMANIA` for edges/km only. No heuristic retuning, no map rescaling.

**File provenance:**
| File | Source |
|------|--------|
| App.tsx, App.css, index.css, romania.ts | frontend-refinements (+ arc overlay, footnotes) |
| heuristic.ts, astar.ts | arc-heuristic (+ HCOORDS decouple) |
| ucs.ts | uniform-cost-search |
| biucs.ts | bidirectionalucs (13 type-only fixes, no logic change; lockfile dropped) |
| bfs/dfs/greedy.ts | main |

**Registry:** 6 algos wired — BFS, DFS, Greedy (Bento), A* (Bento), UCS, Bidirectional UCS.

**Arc overlay:** heuristic viz re-expressed in 600×450 map coords (`mapArcGeometry` in App.tsx), shown for greedy + astar.

**Verified:** `tsc -b` clean, `bun run build` clean, A* Arad→Bucharest = 418 (Arad·Sibiu·Rimnicu Vilcea·Pitesti·Bucharest). All 6 algos run; ucs/biucs/astar optimal 418, bfs/dfs 450.

`integrate` log: c6b27b7 map redesign → 0ed4d9e algo files → 3e4aa70 union registry → df6974e footnotes+arc overlay.

**Next:** review `integrate`, then merge to `main`. Note: `heuristic.ts` still exports unused `arcGeometry` in HCOORDS space (dead, harmless). A* admissible-but-inconsistent reopening still a prof discussion.

### Algorithms wired in UI (`search.ts` → `ALGORITHMS`)
| Key | Label | Optimal | Complete |
|-----|-------|---------|----------|
| bfs | BFS | Yes* (equal step costs) | Yes* |
| dfs | DFS | No | Yes* (visited set) |
| greedy | Greedy (Bento) | No | No* |
| astar | A* (Bento) | Yes* | Yes* |

### Bento heuristic (`_core.ts` + `heuristic.ts`)
- **Friction-weighted chord length** — chord between map pixel coords × per-region "friction" (km/px). Pixel coords are legal per heuristic rules; **no SLD, no GPS**.
- Direct-edge pairs return exact km; others = friction-sum (3 samples along chord) × chord / 3.
- Friction grid: **200×112 cells**, 20px each, sampled within 150px of road edges; floor = slowest road on map (`GLOBAL_MIN_FRIC`, derived from data so it can't drift).
- **Admissible on all 190 city pairs** (self-checked via Floyd-Warshall ground truth).
- **NOT consistent** — 59 triples violate triangle inequality.

### ⚠ The behavior issue for prof
A* uses an **admissible-but-inconsistent** heuristic. Because it's not consistent, the closed set is unsafe: `astar.ts` **reopens** nodes (removes from closed, re-expands) when a strictly lower `g` is found. Goal-test on pop (not on generation) to keep optimality. This reopening behavior — correct but non-standard vs textbook A* — is the thing to confirm with the prof.

### Self-checks (run at module load)
- `heuristic.ts`: asserts `romania.ts` ↔ `_core.ts` graph stay in sync + heuristic admissible on all pairs.
- `astar.ts`: asserts Arad→Bucharest = **418** via Arad·Sibiu·Rimnicu Vilcea·Pitesti·Bucharest.
- `bench.ts`: compares Dijkstra vs SLD vs Bento — nodes expanded, timing, admissibility (`deno run bench.ts`).

### UI
React SPA, shadcn/ui + lucide-react. Step-by-step search visualizer with frontier/visited highlight, algorithm comparison panel (time / memory / path cost), speed slider, play/pause/step.
