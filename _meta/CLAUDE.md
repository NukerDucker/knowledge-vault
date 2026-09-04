# Vault rules for Claude

Reference card. Under 100 lines by design — this loads every session.
Full reasoning lives in `KOS-ARCHITECTURE.md`; do not read it unless asked.

## Read order

This file. That is the whole read order. Nothing else is required before acting.

## What lives where

| Store | Holds | Source of truth for |
|---|---|---|
| This vault | notes, briefs, logs, decisions, **and status** | everything textual |
| `~/Documents/University/` | PDFs, slides, DOCX, submissions | deliverables |
| Code repos | source + docs that version with code | implementation |
| Claude | nothing | never a source of truth |

## Folders

```
_meta/            rules, templates, check.sh
00-inbox/         undecided captures — cleared every 2 weeks
01-university/    coursework, by year/subject
02-programming/   dev guides + personal project notes
04-archive/       closed. READ-ONLY. Never edit, never reorganize.
```

Folders answer *when does this die*, not *what is this about*.
Topic lives in tags and links.

## File change authority

**Propose, then wait.** Do not create, rename, move, or delete any file without
explicit approval for that specific change. Before touching the filesystem answer:
what file, what exact change, did they approve it. No approval, no operation.

Reading is always fine.

## Naming

`kebab-case-descriptive.md` — lowercase, hyphens, no spaces.

- Date prefix `YYYY-MM-DD-` **only** when the note *is* an event (meeting, daily
  note). Never on a topic.
- No version numbers in the vault. Git holds versions. Exported files in
  `~/Documents/` may carry them.
- Received PDFs keep their original filename.

## Frontmatter

```yaml
---
title: Human Readable Title
tags: [topic]
status: active | stable | submitted | archived
---
```

`updated:` only on `active` notes. On finished notes it is date churn.

Assignment notes additionally carry:

```yaml
due: 2026-09-07     # ISO, or TBA
points: 6           # omit if ungraded
subject: uxui       # matches the subject folder
```

## Assignments — do not sync anything by hand

The assignment note's frontmatter is the source of truth.
`assignments-tracker.md` is a **generated view** of it.

- Status changed? Edit the note's frontmatter. That is the entire action.
- Never hand-edit anything between `<!-- BEGIN GENERATED -->` markers.
- Never ask the user to sync the tracker, and never sync it by hand yourself.

Generator: `python3 _meta/sync-tracker.py` (runs automatically on SessionStart).
Rows with no backing note live *outside* the markers and are hand-maintained —
leave them alone.

## Archiving is two steps

1. Move to `04-archive/`.
2. **Sweep every reference to the old location and fix it.**

Step 2 is not optional. Skipping it is what broke this vault's docs in 2026-08.

## Duplication

If a fact appears in two files, one is wrong. Link instead of copying.

Exception: generated views inside `<!-- BEGIN GENERATED -->` markers.
One source, one derived view, regenerated and never hand-edited.

## Context economy

Read the narrowest thing that answers the question. Never explore the whole
vault. Never read `04-archive/` unless named. Never read
`02-programming/guides/system-design-notes/` — vendored reference material, not
the user's writing.

## Checking

`bash _meta/check.sh` — verifies docs match disk. Run after any restructuring.
Exit 0 clean, exit 1 errors.
