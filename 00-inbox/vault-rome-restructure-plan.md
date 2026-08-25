---
title: Vault Rome Restructure Plan
tags: [meta, inbox]
status: stable
---

# Vault Rome Restructure + Gitignore Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Embed slide images in rome-pathfinding.md, restructure it into a stable-content note, establish Reference/Session split as vault-wide rule, add Obsidian .gitignore.

**Architecture:** Three concerns — file org (images), note structure (split year-3 content from 03-ai session log), meta (VAULT-GUIDE rule + .gitignore). Each task is independent; execute in order.

**Tech Stack:** Markdown, Obsidian wikilinks, git

---

## File Map

| Action | File |
|--------|------|
| Move | `slide-08-base.png` → `01-university/year-3/ai/` |
| Move | `slide-10-landmarks.png` → `01-university/year-3/ai/` |
| Move | `slide-13-heatmap.png` → `01-university/year-3/ai/` |
| Leave | `slide-06-lp-diagram.html` — stays in vault root (source asset) |
| Rewrite | `01-university/year-3/ai/rome-pathfinding.md` |
| Create | `03-ai/projects/rome-pathfinding/session-state.md` |
| Modify | `VAULT-GUIDE.md` — add Reference/Session Split section |
| Modify | `CLAUDE.md` — update 03-ai row + add split rule |
| Create | `.gitignore` |

---

### Task 1: Move slide images to correct vault location

**Why:** Images in vault root are orphaned. PNGs are academic assets (not "raw work files" like PDFs/PPTX), so they live alongside their note in `01-university/year-3/ai/`. This enables clean `![[image.png]]` Obsidian embeds.

- [ ] **Step 1: Move three PNGs**

```bash
mv /Users/nukerducker/KnowledgeVault/slide-08-base.png \
   /Users/nukerducker/KnowledgeVault/01-university/year-3/ai/
mv /Users/nukerducker/KnowledgeVault/slide-10-landmarks.png \
   /Users/nukerducker/KnowledgeVault/01-university/year-3/ai/
mv /Users/nukerducker/KnowledgeVault/slide-13-heatmap.png \
   /Users/nukerducker/KnowledgeVault/01-university/year-3/ai/
```

- [ ] **Step 2: Verify**

```bash
ls /Users/nukerducker/KnowledgeVault/01-university/year-3/ai/
# Expected: rome-pathfinding.md  slide-08-base.png  slide-10-landmarks.png  slide-13-heatmap.png
```

- [ ] **Step 3: Commit**

```bash
cd /Users/nukerducker/KnowledgeVault
git add -A
git commit -m "vault: move slide PNGs to 01-university/year-3/ai/"
```

---

### Task 2: Rewrite rome-pathfinding.md — stable content note

**Why:** Current note mixes stable reference content with session churn (`updated:`, git state, dated notes). This rewrite removes churn, embeds slide images, adds session-log pointer.

**Remove from this note:** `updated:` frontmatter, `## Git state` section, dated session entries.
**Add:** `![[image.png]]` embeds under relevant sections, `*See also: [[rome-pathfinding-log]]*` footer.

- [ ] **Step 1: Write the rewritten note**

Full replacement for `01-university/year-3/ai/rome-pathfinding.md`:

```markdown
---
title: Rome Pathfinding — AI Assignment
tags: [university, year-3, ai, project, assignment]
status: active
created: 2026-08-06
---

# Rome Pathfinding (AI Assignment)

Repo: `~/Code/rome-pathfinding` → `github.com/NukerDucker/rome-pathfinding`
Due: **2026-10-13** | Submission: YouTube video + Vercel URL + GitHub link

*Session log and git state → [[rome-pathfinding-log]]*

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

**File:** `~/Code/rome-pathfinding/slides/slide-06-lp-diagram.png (not yet exported)` | Source HTML: `01-university/year-3/ai/assets/slide-06-lp-diagram.html`

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
Central nodes give weak bounds. Dead-ends (degree-1) give exact bounds for their specific goals.

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

Goal must have NO backdoor in the smaller preset. Try: goal = Arad, Sibiu, Pitesti, Craiova, Lugoj, Rimnicu Vilcea.

#### Why `generated` count often doesn't change between presets

`generated` = nodes ever discovered (added to frontier). Even perfect h still discovers neighbors of each expanded node. Count only drops if weaker h causes extra expansions → exposing more neighbors. On 20 nodes most heuristics are tight enough.

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

*See also: [[rome-pathfinding-log]] — session log, git state, dated progress*
```

- [ ] **Step 2: Commit**

```bash
cd /Users/nukerducker/KnowledgeVault
git add 01-university/year-3/ai/rome-pathfinding.md
git commit -m "vault: restructure rome-pathfinding.md — stable content + image embeds"
```

---

### Task 3: Create 03-ai session-state.md for rome

**Why:** Session log, git state, and dated updates belong in 03-ai — not in the year-3 content note. Existing `rome-assignment.md` = keep (assignment brief). `rome-conversation.md` = superseded; archive manually after this.

- [ ] **Step 1: Create session-state.md**

Write `03-ai/projects/rome-pathfinding/session-state.md`:

```markdown
---
title: Rome Pathfinding — Session State
tags: [ai, project, session-log]
status: active
created: 2026-08-06
updated: 2026-08-21
---

# Rome Pathfinding — Session Log

*Reference note → [[rome-pathfinding]]*
Repo: `~/Code/rome-pathfinding`

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
- Slide images moved from vault root to `01-university/year-3/ai/`
- rome-pathfinding.md restructured: stable content note + image embeds + session-state split

### 2026-08-20

- Viz enhancements shipped: heatmap, click-to-landmark, toolbar refactor
- Slide 6 LP diagram built as SVG/HTML → PNG screenshot at `~/Code/rome-pathfinding/slides/slide-06-lp-diagram.png (not yet exported)`
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
```

- [ ] **Step 2: Commit**

```bash
cd /Users/nukerducker/KnowledgeVault
git add 03-ai/projects/rome-pathfinding/session-state.md
git commit -m "vault: add rome session-state.md in 03-ai"
```

---

### Task 4: Add Reference/Session Split rule to VAULT-GUIDE.md

**Insert location:** After `## Hub + Spoke Pattern` section, before `## Tag Conventions`.

- [ ] **Step 1: Read current VAULT-GUIDE.md to find exact insertion point**

The section immediately before `## Tag Conventions` ends with the Hub + Spoke example block ending in `*See also: [[assignments-tracker]]*`.

- [ ] **Step 2: Insert after the Hub + Spoke section**

Add this block:

```markdown
---

## Reference / Session Split

For projects with 3+ Claude sessions, split across two notes:

| Note type | Location | Contains | `updated:` field |
|-----------|----------|----------|-----------------|
| **Reference note** | `01-university/year-N/subject/<topic>.md` | Stable facts: stack, design, technical content, assignment brief | Omit — only changes when facts change |
| **Session log** | `03-ai/projects/<name>/session-state.md` | Rolling session entries, git state, open tasks, dated progress | Keep — tracks last session |

**Linking:**
- Reference note footer: `*See also: [[rome-pathfinding-log]] — session log, git state, dated progress*`
- Session log header: `*Reference note → [[<topic>]]*`

**Rule:** Any note edited across 3+ sessions should be split. Churn (dated entries, git state) belongs in the session log, not the reference note.

**Non-AI projects** (no `03-ai` presence): keep a `-log.md` sibling in the subject folder instead (e.g., `investment-planning-log.md` next to `investment-planning.md`).

Active example: `01-university/year-3/ai/rome-pathfinding.md` ↔ `03-ai/projects/rome-pathfinding/session-state.md`
```

- [ ] **Step 3: Commit**

```bash
cd /Users/nukerducker/KnowledgeVault
git add VAULT-GUIDE.md
git commit -m "vault: add Reference/Session Split rule to VAULT-GUIDE"
```

---

### Task 5: Update CLAUDE.md

**Two changes:**
1. In the Folder Convention table, update `03-ai` row
2. Add `## Reference / Session Split Rule` section after the `## Note Frontmatter` section

- [ ] **Step 1: Update 03-ai row in Folder Convention table**

Change:
```
| `03-ai` | AI project plans and session state (nacl-nextpath-x, rome, etc.) |
```
To:
```
| `03-ai` | Session log + git state for AI-assisted projects. Pair with `01-university/year-N/subject/` reference note. See Reference/Session Split rule below. |
```

- [ ] **Step 2: Add rule section after ## Note Frontmatter**

```markdown
## Reference / Session Split Rule

When a project note has been edited across 3+ Claude sessions, split it:

- `01-university/year-N/subject/topic.md` → stable facts only; omit `updated:` to avoid date churn
- `03-ai/projects/<name>/session-state.md` → session log, git state, open questions, dated entries

Linking: reference note footer links to `[[rome-pathfinding-log]]`; session log header links back to `[[topic]]`.

Active example: `rome-pathfinding.md` ↔ `03-ai/projects/rome-pathfinding/session-state.md`

See `VAULT-GUIDE.md` for full rule.
```

- [ ] **Step 3: Commit**

```bash
cd /Users/nukerducker/KnowledgeVault
git add CLAUDE.md
git commit -m "vault: document Reference/Session Split rule in CLAUDE.md"
```

---

### Task 6: Create .gitignore

**Why:** `workspace.json` changes every Obsidian open (open panes, cursor positions) — meaningless commits. `.DS_Store` is macOS noise. Track `.obsidian/` plugin/config files but ignore workspace state.

- [ ] **Step 1: Create .gitignore**

Write `/Users/nukerducker/KnowledgeVault/.gitignore`:

```gitignore
# Obsidian — workspace state (changes every open, not config)
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/.trash/

# macOS
.DS_Store
**/.DS_Store
```

- [ ] **Step 2: Remove already-tracked noise files from git index**

```bash
cd /Users/nukerducker/KnowledgeVault
git rm --cached .DS_Store 2>/dev/null || true
git rm --cached "01-university/.DS_Store" 2>/dev/null || true
git rm --cached "01-university/year-3/.DS_Store" 2>/dev/null || true
git rm --cached "03-ai/.DS_Store" 2>/dev/null || true
git rm --cached .obsidian/workspace.json 2>/dev/null || true
```

- [ ] **Step 3: Verify ignore rules work**

```bash
git check-ignore -v .DS_Store .obsidian/workspace.json
# Expected output: .gitignore:5:.DS_Store   .DS_Store
#                  .gitignore:1:.obsidian/workspace.json   .obsidian/workspace.json
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "vault: add .gitignore — ignore workspace.json, .DS_Store"
```

---

## Self-Review

**Spec coverage:**
- ✅ Images moved to `01-university/year-3/ai/` and embedded in note
- ✅ rome-pathfinding.md restructured (stable content, no date churn, no git state)
- ✅ `updated:` removed from reference note
- ✅ 03-ai session-state.md created with full session log
- ✅ Bidirectional link between reference note and session log
- ✅ Rule documented in VAULT-GUIDE.md (table + example)
- ✅ CLAUDE.md updated (table row + rule section)
- ✅ .gitignore created (workspace.json + DS_Store)

**Known follow-up (not blocking):**
- `03-ai/projects/rome-pathfinding/rome-conversation.md` — superseded by session-state.md; archive to `04-archive/` manually
- `slide-06-lp-diagram.html` in vault root — intentional source asset; leave in place
