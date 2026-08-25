---
title: KOS — Vault Governing Document
tags: [meta, kos]
status: active
updated: 2026-08-25
---

# KOS — Vault Governing Document

**The single source of truth for how this vault is organized.**

Read this before creating notes or moving anything. If this document and the disk
disagree, one of them is wrong — run `bash _meta/check.sh` to find out which.

> **This is the only governing document.** `VAULT-GUIDE.md` and `BRIDGE.md` were
> retired on 2026-08-26; everything still true from them lives here. Two copies of
> a rule is a design that needs perfect discipline forever, and that is exactly
> how the August drift happened.

Design reasoning: `KOS-ARCHITECTURE.md`. Day-to-day usage: `KOS-MANUAL.md`.
Rules for Claude: `_meta/CLAUDE.md`.

---

## The governing principle

> **Every rule here must be machine-checkable, or it should not be written down.**

In August 2026 this vault's guide named three folders that did not exist. The
content was fine; the *rules layer* had rotted. A rule nobody can verify is wrong
within a month and misleading within a year.

That is why `_meta/check.sh` exists, and why it matters more than any rule below.

---

## Stores

| Store | Holds | Source of truth for |
|---|---|---|
| **This vault** | notes, briefs, logs, decisions, and status | everything textual |
| **`~/Documents/University/`** | PDFs, slides, DOCX, submissions | deliverables |
| **Code repos** | source, plus docs that version with the code | implementation |
| **Claude** | nothing | never a source of truth |

**Filing test** — first yes wins:

1. Binary file I produced or received? → `~/Documents/`
2. Must change when the code changes? → beside the code
3. Want to reread it in six months? → here
4. None of the above? → delete it

There is no "does it have a deadline" branch. A deadline is a `due:` field on a
note, not a category of thing.

---

## Folder map

```
_meta/                            rules, templates, check.sh
  KOS.md                          this file
  CLAUDE.md                       agent reference card
  check.sh                        governance checker

00-inbox/                         undecided captures — cleared every 2 weeks

01-university/
  assignments-tracker.md          hub for all deadlines and status
  courses/                        semester schedule, degree/study plans
  regulations/                    university rules, CEI regulations
  year-3/
    ai/                           Artificial Intelligence
      assets/                     embedded diagrams and sources
    mcu/                          Microcontroller Interfacing
    os/                           Operating Systems
    rtw/                          Ready to Work
    uxui/                         UX/UI Design
    investment-planning/          Investment Planning

02-programming/
  guides/                         dev reference guides
  projects/                       per-project vault-wiring notes

04-archive/                       closed / superseded. READ-ONLY.
  agoda-internship/               Agoda IT internship 2026
  nacl-nextpath-x/                NACL NextPath-X system docs
```

### Archive is read-only

Read it freely. **Do not edit or reorganize it.** If something in there needs
updating, it is not archived — move it out first.

That includes leaving upstream conventions alone. Renaming files inside a closed
chapter is churn against material that will never be edited again.

---

## Where things go

| Content | Path |
|---|---|
| Assignment note | `01-university/year-3/<subject>/` |
| Assignment tracker | `01-university/assignments-tracker.md` |
| Semester schedule, study plan | `01-university/courses/` |
| University regulations | `01-university/regulations/` |
| Diagram or screenshot a note embeds | `<subject>/assets/` |
| Dev reference guide | `02-programming/guides/` |
| Personal project note | `02-programming/projects/` |
| Session log | `<subject>/<project>-log.md`, beside its reference note |
| Unprocessed capture | `00-inbox/` |
| Closed / superseded | `04-archive/` |
| PDFs, slides, submissions | `~/Documents/University/Year-N/<Subject>/` |

**Inputs vs outputs.** If the note would be unreadable without the file, it is an
input and lives in the vault beside the note. If it is something you produced and
handed to someone, it is an output and lives in `~/Documents/`.

Worked example: `01-university/year-3/ai/assets/slide-06-lp-diagram.html` is an
input — `rome-pathfinding.md` embeds it. The exported PNG is an output and lives
in `~/Documents/`.

---

## Naming

`kebab-case-descriptive.md` — lowercase, hyphens, no spaces.

| Case | Rule |
|---|---|
| Notes | `kebab-case`, describe the thing |
| Events (meetings, daily notes) | `YYYY-MM-DD-topic.md` |
| Topics | **never** dated — a dated topic note fragments your knowledge |
| Versions | never in the vault (git holds them); only on exports |
| Received PDFs | keep the original filename |
| Produced PDFs | whatever the recipient requires |
| Images | `<note-name>-<what-it-shows>.png` |
| Folders | same convention; plural for collections |

Exempt: root docs (`CLAUDE.md`, `HOME.md`, `KOS-*.md`) use uppercase by
deliberate convention.

---

## Frontmatter

```yaml
---
title: Human Readable Title
tags: [topic]
status: active | stable | submitted | graded | archived
---
```

`updated:` only on `active` notes. On finished notes it is date churn.

Assignment notes additionally carry `due:` (ISO date or `TBA`), `points:`, and
`subject:`. **These are the source of truth for the tracker.**

### Status vocabulary

| Status | Meaning |
|---|---|
| `active` | being worked on now |
| `stable` | finished and true — the normal resting state for notes |
| `submitted` | handed in, not yet graded *(assignments only)* |
| `graded` | returned with a mark *(assignments only)* |
| `archived` | in `04-archive/`, read-only |

---

## Assignments

**The note's frontmatter is the source of truth. The tracker is a view of it.**

When something changes — submitted, date moved, points announced — edit the
note's frontmatter. That is the entire action. Never hand-sync the tracker.

`_meta/sync-tracker.py` regenerates the tracker and `HOME.md` from frontmatter.
It runs automatically on SessionStart; run it by hand with
`python3 _meta/sync-tracker.py`, or `--check` to diff without writing.

It only writes between `<!-- BEGIN GENERATED: name -->` markers. Rows with no
backing note — class sessions, peer-eval deadlines — live outside the markers in
a hand-maintained table and are never touched.

**Staleness is the known limit.** Edit a note in Obsidian and the tracker is out
of date until the next session starts, or until you run the script. That is a
visible, one-command fix; a file-watcher would be more machinery than the
problem deserves.

---

## Governance rules

**Ownership.** Every note has exactly one owner folder. When two fit, the more
permanent one wins: *would this still be worth reading if the project were
cancelled?* Yes → guides. No → the project's folder.

**Granularity.** One note = one thing you would search for by name. Under ~200
words it is a section of something else; over ~2,000 it is probably two notes.

**Duplication.** If a fact appears in two files, one is wrong. Link instead.
Exception: generated views inside `<!-- BEGIN GENERATED -->` markers — one source,
one derived view, regenerated and never hand-edited.

**Archiving is two steps.** Move to `04-archive/`, **then sweep every reference to
the old location.** Step 2 is what separates an archive from a set of broken
links, and skipping it is exactly what broke this vault's docs in August 2026.

**Deletion.** Delete inbox items older than two weeks, superseded drafts,
duplicates, and scratch notes. Never delete decisions, lessons, or anything a live
note links to. Git makes deletion reversible — use that.

**New folders** need all three: five-plus notes already exist for it, they will be
archived together, and the name will still make sense in five years. Never create
a folder for one note, or one named after a tool, a format, or a year.

**Depth limit:** three levels below the top.

---

## Hub and spoke

**Hub notes** aggregate and link out. **Spoke notes** link back at the bottom.

- Hub: `assignments-tracker.md` → every assignment · `HOME.md` → everything
- Spoke: `uxui-ui-hunt.md` ends with `*See also: [[assignments-tracker]]*`
- Project hub: `uxui-facility-booking-project.md` ↔ weeks 3–7

A hub earns its place when 5+ notes share a thread that none of them owns.

---

## Reference / session split

Once a project has run across 3+ sessions, split it in two:

| Note | Holds | `updated:` |
|---|---|---|
| **Reference** — `<subject>/<topic>.md` | stable facts: stack, design, brief | omit |
| **Log** — `<subject>/<topic>-log.md` | dated entries, git state, open tasks | keep |

Link both ways: reference footer `*See also: [[<topic>-log]]*`, log header
`*Reference note → [[<topic>]]*`.

**Why:** dated churn inside a reference note forces a re-read to work out what is
still true. Splitting keeps the durable half durable. This applies to every
project — there is no AI / non-AI distinction, because everything is
AI-assisted now.

---

## Tags

Cross-cutting topics only. If a tag matches exactly one folder, delete it — the
folder already says it. Keep the list under twenty, and merge anything used
fewer than three times at the yearly review.

Current: `university` `assignment` `kmitl` `nacl` `ai` `programming` `guide`
`project` `group-work` `meta` `kos` `dashboard` `tracker`

---

## Adding a top-level folder

Rare. All three conditions in Governance rules must hold, and then:

1. Take the next free number — `03` and `05`–`08` are free.
2. `NN-kebab-case/`, lowercase, hyphens only.
3. Add it to the Folder map **and** the Where-things-go table in this file first.
4. Add a colour group in `.obsidian/graph.json`.
5. Run `bash _meta/check.sh`.

| Slot | Purpose |
|---|---|
| `00` | Inbox — fixed |
| `01` | University — fixed |
| `02` | Programming — fixed |
| `03` | free (was AI projects, retired 2026-08-25) |
| `04` | Archive — fixed |
| `05`–`08` | free |

---

## What does not belong in this vault

- Source code — lives in `~/Code/<repo>/`
- Binary deliverables — PDFs, slides, DOCX in `~/Documents/`
- Agent session files (`.ai/`, `.claude/` inside child repos)
- Scratch notes — delete them after use
- Generated content that is not fenced by `GENERATED` markers

When a NotebookLM or AI summary is worth keeping, paste it into the relevant
vault note under a `## Summary` heading. Do not keep it as a separate file.

---

## Vendored content

`02-programming/guides/system-design-notes/` is an external repository, not your
writing. It keeps its upstream conventions and is exempt from the naming and
frontmatter rules. `check.sh` skips it, and Claude should not read it unless asked.

---

## Maintenance

| Cadence | Time | Do |
|---|---|---|
| Weekly | 10 min | Empty `00-inbox/` to zero; mark finished work `stable` |
| Monthly | 30 min | `bash _meta/check.sh`; archive + de-reference; `du -sh .git` |
| Yearly | 2 hr | Reread this file; retire finished areas; delete a dead folder |

Monthly is the one that matters — `check.sh` is what keeps this document true.

**Repo size ceiling:** if `.git` passes 2 GB, stop committing frequently
re-exported images. Do not adopt Git LFS before then.

---

## Cross-reference to `~/Documents/University/`

Symlink: `university-files/` → `~/Documents/University/` (excluded from indexing).

| Subject | Work files |
|---|---|
| UX/UI Design | `university-files/Year-3/UXUI/` |
| Operating Systems | `university-files/Year-3/OS/` |
| Investment Planning | `university-files/Year-3/Investment Planning/` |
| Artificial Intelligence | code at `~/Code/rome-pathfinding/` |
| Microcontroller | `university-files/Year-3/Microcon/` |
| Ready to Work | `university-files/Year-3/Ready To Work/` |

Vault notes reference work files with a `**File:**` path. `check.sh` check 8
verifies those paths still exist.

### Code

All repos live flat in `~/Code/` — moved out of `~/Documents/University/` on
2026-08-26 so that archiving university at graduation does not archive the code
with it.

| Repo | Vault note | Git |
|---|---|---|
| `~/Code/rome-pathfinding` | [[rome-pathfinding]] | yes |
| `~/Code/nacl-nextpath-x` | [[nacl-nextpath-x]] | no — project finished, left as-is |
| `~/Code/nacl-website` | *(none)* | yes |
| `~/Code/nacl-camellya` | *(none)* | no — project finished, left as-is |
| `~/Code/drunkbill` | [[drunkbill-log]] | yes |
| `~/Code/timetable-website` | *(none)* | yes |

System docs and ADRs for these live **with the code**, not in the vault. What
belongs in the vault is why the project exists and what you learned — the part
that outlives the repo.

---

## Known gaps

Tracked here rather than forgotten. Cleared as milestones land.

- `assignments-tracker.md` still has hand-written `## Details` sections that
  duplicate note content. Harmless, but they are the next duplication to remove.
- Due dates for pre-August coursework are completion dates, not deadlines — the
  originals were never recorded. Inert for submitted work.
- Top-level restructure deferred; revisit at graduation or ~1,000 notes.

**Cleared 2026-08-25:** three stale paths in the governing docs; eight notes
missing frontmatter; one broken wikilink; assignment frontmatter normalized
across 17 notes; tracker and `HOME.md` now generated. `check.sh` reports 0 errors.
