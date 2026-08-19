# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An Obsidian knowledge vault. No build system, no tests, no CI. All files are Markdown with YAML frontmatter.

---

## Two-Vault System

This vault and `~/Documents/University/` work as a pair. Each has a strict role:

| | `~/KnowledgeVault/` (here) | `~/Documents/University/` |
|---|---|---|
| **Role** | Markdown notes & tracking | Work files |
| **Contains** | `.md` notes, assignment briefs, session state, project logs | PDFs, PPTX, Word docs, source code, submission files |
| **Examples** | `01-university/year-3/uxui/uxui-week7-crazy8s-storyboard.md` | `Year-3/AI/rome-pathfinding/` repo, lab slides, `.pdf` submissions |

**Rule:** Never put raw work files here. Never put markdown notes in Documents/University.  
Vault notes reference their source files with a `**File:**` path pointing to `~/Documents/University/`.

### Key Documents/University paths cross-referenced from vault notes

| What | Documents path |
|------|---------------|
| Rome pathfinding app | `~/Documents/University/Year-3/AI/rome-pathfinding/` |
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
| `03-ai` | AI project plans and session state (nacl-nextpath-x, rome, etc.) |
| `01-university/internship/agoda/` | Agoda IT internship 2026 (own Obsidian sub-vault) |
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
updated: 2026-06-01  # optional
---
```

