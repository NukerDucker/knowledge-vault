# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An Obsidian knowledge vault. No build system, no tests, no CI. All files are Markdown with YAML frontmatter.

## Folder Convention

Numbered prefixes control sidebar order in Obsidian:

| Folder | Purpose |
|--------|---------|
| `00-inbox` | Unprocessed captures |
| `01-university` | Academic notes, assignments, internship docs, regulations |
| `02-homelab` | Home lab planning and docs |
| `03-programming` | Dev project notes and vault wiring docs |
| `04-fitness` | Personal fitness tracking |
| `05-ai` | AI project plans and session state |
| `06-nacl-kmitl` | NACL lab work — system docs, ADRs, architecture |
| `90-archive` | Retired notes |

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

## nacl-nextpath-x Session State

`05-ai/projects/nacl-nextpath-x/session-state.md` is the **primary source of truth** for the NACL NextPath X coding project. Read it before any work on that project. It contains:

- Repo layout and git branch state
- Safety rules (what never to commit)
- Web (Next.js/Bun) and API (Go/Gin) commands and architecture
- Frontend/backend contract notes with dates
- Running log of completed work per session

**Update rule:** After meaningful coding sessions on nacl-nextpath-x, append a dated section to `session-state.md` with: changed subsystem + intent, new commands/contracts/pitfalls, unresolved TODOs. Remove stale details.

## Vault ↔ Child Repo Wiring (nacl-nextpath-x)

The child repos (`nacl-nextpath-x-web`, `nacl-nextpath-x-api`) contain hook scripts that read/write this vault:

- `scripts/session-start.sh` → reads vault into `.ai/context.md` inside the child repo
- `scripts/session-end.sh` → writes session notes/state/decisions back here
- `.github/hooks/memory.json` → wires the above to sessionStart/sessionEnd events

Never commit `.ai/`, `.claude/`, `.codex/`, `session-state.md`, or `KnowledgeVault/**` from inside child repos. Existing tracked AI docs (`AGENTS.md`, `CLAUDE.md` in each repo) are allowed.
