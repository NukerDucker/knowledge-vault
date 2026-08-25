# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Assignment Tracker Rule

**Never hand-edit `01-university/assignments-tracker.md`.** It is generated.

The assignment note's frontmatter is the source of truth. When status changes,
edit `status:` / `due:` / `points:` in the note — that is the entire action.
`_meta/sync-tracker.py` regenerates the tracker and `HOME.md` on SessionStart.

Rows with no backing note (class sessions, peer-eval deadlines) live *outside*
the `<!-- BEGIN GENERATED -->` markers and are hand-maintained. Leave them alone.

*(Replaced 2026-08-25. The old rule required syncing the tracker by hand on every
status change, which is a manual step this vault no longer has.)*

## What This Is

An Obsidian knowledge vault. No build system, no tests, no CI. All files are Markdown with YAML frontmatter.

---

## Two-Vault System

This vault and `~/Documents/University/` work as a pair. Each has a strict role:

| | `~/KnowledgeVault/` (here) | `~/Documents/University/` |
|---|---|---|
| **Role** | Markdown notes & tracking | Work files |
| **Contains** | `.md` notes, assignment briefs, session state, project logs | PDFs, PPTX, Word docs, source code, submission files |
| **Examples** | `01-university/year-3/uxui/uxui-week7-crazy8s-storyboard.md` | lab slides, `.pdf` submissions (repos live in `~/Code/`) |

**Rule:** Never put raw work files here. Never put markdown notes in Documents/University.  
Vault notes reference their source files with a `**File:**` path pointing to `~/Documents/University/`.

### Key Documents/University paths cross-referenced from vault notes

| What | Documents path |
|------|---------------|
| Rome pathfinding app | `~/Code/rome-pathfinding/` (moved out of Documents 2026-08-26) |
| Agoda internship files | `~/Documents/University/Internship/` |
| Year-3 UX/UI slides + PDFs | `~/Documents/University/Year-3/` |
| Investment Planning report doc | `~/Documents/University/Year-3/` |

---

## Folder Convention

Numbered prefixes control sidebar order in Obsidian:

| Folder | Purpose |
|--------|---------|
| `00-inbox` | Unprocessed captures |
| `01-university` | Academic notes, assignments, internship docs, regulations |
| `01-university/year-3/os/` | Operating Systems coursework |
| `01-university/year-3/uxui/` | UX/UI Design coursework |
| `01-university/year-3/rtw/` | Ready to Work coursework |
| `01-university/year-3/investment-planning/` | Investment Planning (bonds report, stock analysis) |
| `01-university/year-3/ai/` | Artificial Intelligence (Rome pathfinding) |
| `02-programming` | Dev project notes and vault wiring docs |
| `04-archive/agoda-internship/` | Agoda IT internship 2026 — archived, read-only |
| `04-archive` | Retired notes |

See `VAULT-GUIDE.md` for full filing rules, naming conventions, and tag taxonomy.

## Note Frontmatter

Standard format used across the vault:

```yaml
---
title: Note Title
tags: [tag1, tag2]
status: active   # or draft, archived
created: 2026-05-15
updated: 2026-06-01  # optional — omit on reference notes, keep on session logs
---
```

---

## Reference / Session Split Rule

When a project is worked on across 3+ Claude sessions, split into two notes:

- **`01-university/year-N/subject/topic.md`** — stable facts only (stack, design, technical content). Omit `updated:` to avoid date churn.
- **`<subject>/<project>-log.md`** — rolling session log, git state, open tasks, dated entries. Keep `updated:`.

**Linking rule:**
- Reference note footer: `*See also: [[<project>-log]] — session log, git state, dated progress*`
- Session log header: `*Reference note → [[topic]]*`

**New projects:** create `<project>-log.md` beside the reference note from session 1.


Active example: `01-university/year-3/ai/rome-pathfinding.md` ↔ `01-university/year-3/ai/rome-pathfinding-log.md`

Full rule in `VAULT-GUIDE.md` → Reference / Session Split section.

