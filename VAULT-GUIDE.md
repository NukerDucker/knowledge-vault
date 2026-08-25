---
title: Vault Structure Guide
tags: [meta, guide]
status: active
created: 2026-07-24
updated: 2026-08-25
---

# Vault Structure Guide

Single source of truth for how this vault is organized. Read this before creating new notes.

**Navigation hub:** See [[BRIDGE]] for the cross-reference map between this vault and `~/Documents/University/`.  
**Symlink:** `university-files/` in vault root → `~/Documents/University/` (excluded from Obsidian indexing).

---

## Folder Map

```
00-inbox/                         ← unprocessed captures, process weekly

01-university/
  assignments-tracker.md          ← single hub for all years/subjects
  year-1/                         ← add subject subfolders when content exists
  year-2/
  year-3/
    os/                           ← Operating Systems
    uxui/                         ← UX/UI Design
    rtw/                          ← Ready to Work
    investment-planning/          ← Investment Planning (bonds report, stock analysis)
    ai/                           ← Artificial Intelligence (Rome pathfinding)
  year-4/
  courses/                        ← semester schedule, degree/study plans
  regulations/                    ← university rules, CEI regulations
  (internship/ — archived 2026-08 → 04-archive/agoda-internship/)

02-programming/
  guides/                         ← dev reference guides
  projects/                       ← per-project vault-wiring notes


04-archive/                       ← closed / superseded, keep for reference
  agoda-internship/               ← Agoda IT internship 2026 — READ-ONLY
    _index.md
    daily-notes/                  ← daily standup logs (YYYY-MM-DD.md)
    internship-diary.md
    Internship_Diary_Complete.md
    knowledge-base/               ← Windows/Mac build guides, laptop specs
```

**Archive is read-only.** Read it freely; do not edit or reorganize it. If something in there needs updating, it is not archived — move it out first.

---

## File Naming

```
kebab-case.md
```

- All lowercase, hyphens not underscores
- Descriptive: `uxui-week3-market-comparison.md` not `UX_UI_Final.md`
- Date prefix for time-bound one-offs: `2026-07-24-meeting-notes.md`
- PDFs: keep original filename

---

## Required Frontmatter

```yaml
---
title: Note Title
tags: [tag1, tag2]
status: active   # active | draft | archived
created: 2026-07-24
updated: 2026-07-24  # add when significantly revised
---
```

---

## Where Things Go — Decision Table

| Content type | Path | Example |
|-------------|------|---------|
| Assignment tracker hub | `01-university/` | `assignments-tracker.md` |
| Assignment detail note | `01-university/year-N/<subject>/` | `uxui-week3-market-comparison.md` |
| Semester schedule | `01-university/courses/` | `semester-schedule-2026.md` |
| Degree / study plan | `01-university/courses/` | `cei-study-plan.md` |
| University regulations | `01-university/regulations/` | `cei-regulations-summary.md` |
| Internship diary / reports / forms | `04-archive/agoda-internship/` (archived, read-only) | `internship-diary.md` |
| Dev reference guide | `02-programming/guides/` | `senior-frontend-developer-guide.md` |
| Vault wiring notes (per repo) | `02-programming/projects/` | `nacl-nextpath-x.md` |
| Project session log | `01-university/year-3/<subject>/` | `<project>-log.md` |
| NACL system docs / ADRs / design specs | *(no vault folder — lives with the code)* | `~/Documents/University/Network-and-Cloud-Laboratory-KMITL/<repo>/` |
| Agoda internship daily notes | `04-archive/agoda-internship/daily-notes/` (read-only) | `2026-05-26.md` |
| Agoda KB articles | `04-archive/agoda-internship/knowledge-base/` (read-only) | `NH Laptop Spec.md` |
| Unprocessed capture | `00-inbox/` | — |
| Old / closed / superseded | `04-archive/` | — |
| University PDFs / slides / physical docs | `~/Documents/University/Year-N/<Subject>/` | `A1 Foundation knowledge.pdf` |

---

## Document Storage Rule

Physical university files (PDFs, PPTX/slides, Word docs) go in `~/Documents/University/` mirroring the vault year/subject structure. The vault note for that subject includes a `**File:**` path so Obsidian notes link to their source documents.

Example mapping:
```
Vault note:  01-university/year-3/rtw/rtw-a2-labour-law.md
Source file: ~/Documents/University/Year-3/Ready To Work/A2 Labour law.pdf
```

When AI summaries are generated (via NotebookLM or similar), embed the summary in the vault note under a `## Knowledge` or `## Summary` section.

---

## Hub + Spoke Pattern

**Hub notes** aggregate and link out via `[[wikilink]]`.  
**Spoke notes** link back at the bottom: `*See also: [[hub-note]]*`

Example:
- Hub: `assignments-tracker.md` → links to each assignment file
- Spoke: `uxui-ui-hunt.md` → ends with `*See also: [[assignments-tracker]]*`

---

## Reference / Session Split

For projects with ongoing AI-assisted work (3+ Claude sessions), split across two notes:

| Note type | Location | Contains | `updated:` field |
|-----------|----------|----------|-----------------|
| **Reference note** | `01-university/year-N/subject/<topic>.md` | Stable facts: stack, design, technical content, assignment brief | Omit — only changes when facts change |
| **Session log** | `<subject>/<project>-log.md` | Rolling session entries, git state, open tasks, dated progress | Keep — tracks last session |

**Linking:**
- Reference note footer: `*See also: [[<project>-log]] — session log, git state, dated progress*`
- Session log header: `*Reference note → [[<topic>]]*`

**Trigger:** Any note edited across 3+ Claude sessions should be split. Churn (dated entries, git state) belongs in the session log, not the reference note.

**All projects** use a `-log.md` sibling in the subject folder. The AI / non-AI distinction is gone: everything is AI-assisted now, so it never divided anything.

**New projects:** create `<project>-log.md` beside the reference note from day one if the project will span multiple sessions.

Active example: `01-university/year-3/ai/rome-pathfinding.md` ↔ `01-university/year-3/ai/rome-pathfinding-log.md`

---

## Tag Conventions

| Tag | Use |
|-----|-----|
| `university` | Coursework, academic notes |
| `assignment` | Active assignment with a deadline |
| `kmitl` | KMITL institutional |
| `nacl` | NACL lab work |
| `ai` | AI projects |
| `homelab` | Home lab infrastructure |
| `fitness` | Fitness tracking |
| `meta` | Vault structure and guides |

---

## Inbox Processing Rule

Clear `00-inbox/` weekly:
1. File into the correct folder with proper frontmatter
2. Or delete if no longer relevant

---

## Adding a New Top-Level Folder

Only create a new numbered folder when content genuinely doesn't fit anywhere existing.

**Rules:**
1. Use the next sequential number after the highest non-archive folder (currently `02-programming` → `03` is free, `04` is archive; insert new folder at `05+`).
2. Name pattern: `NN-kebab-case/` — all lowercase, hyphens only.
3. Add a row to the **Folder Map** and **Where Things Go** table in this file before creating the folder.
4. Add a color group entry in `.obsidian/graph.json` so the new folder gets a distinct colour in the graph.
5. Add a row to `BRIDGE.md` if the folder cross-references `~/Documents/University/`.
6. Update `CLAUDE.md` (project root) folder convention table.

**Number reservation:**
| Slot | Purpose |
|------|---------|
| `00` | Inbox — fixed |
| `01` | University — fixed |
| `02` | Programming — fixed |
| `03` | free (was AI projects, retired 2026-08-25) |
| `04` | Archive — fixed |
| `05+` | Future expansion |

---

## What NOT to Track Here

- Source code (lives in the actual repo)
- AI session context files (`.ai/`, `.claude/` inside child repos — gitignored there)
- Temporary scratch notes (delete after use)
