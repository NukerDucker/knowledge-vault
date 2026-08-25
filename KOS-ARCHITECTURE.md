---
title: Knowledge Operating System — Architecture
tags: [meta, kos, architecture]
status: draft
created: 2026-08-25
---

# Knowledge Operating System — Architecture

Design document. Parts 1–8, 12, 13.
Companion: `KOS-MANUAL.md` (Parts 9, 10, 11, 14).

**Assumption stated once:** `~/KnowledgeVault/` is the canonical KOS root. `~/Documents/University/` is a legacy file store to be reshaped, not replaced.

**Nothing in this document has been executed.** No file was created, moved, renamed, or deleted to produce it, apart from this file and the manual.

---

> ### Revision 2 — what your actual requirements changed
>
> The first draft answered a brief that turned out not to be yours. Your real requirements are three: **one app**, **university access must be fast**, and **the tracker must never need a manual sync.** Three recommendations invert as a result.
>
> | First draft | Revised | Why |
> |---|---|---|
> | Five stores; Notion owns status | **Four stores; Notion dropped** | You want one app. At 131 notes the status/knowledge separation was solving a problem you do not have |
> | `assignments-tracker.md` moves to Notion | **Stays here, and becomes generated** | You want it current without asking. Derived beats relocated |
> | New top level: `10-areas/20-projects/30-library/90-archive` | **Deferred.** `01-university/` stays at the top | It is your dominant use case and you want it one click away. The graduation argument is real but it can wait |
>
> Unchanged: the drift finding (Part 0), `check.sh`, naming rules, one README per project, the AI context hierarchy, the refusal of Dataview.
>
> The mechanism that answers *"never make me ask"* is not a better rule. It is **deleting the manual step** — the tracker stops being a file you maintain and becomes a view generated from the notes. Part 1 has the details.

---

## Part 0 — What I Found, and Why It Changes the Design

You asked me to inspect deeply before proposing. I did. The finding reframes the whole project.

I took the three concrete paths named in your existing governing document, `VAULT-GUIDE.md`, and checked whether they exist on disk:

| Path named in `VAULT-GUIDE.md` | On disk? |
|---|---|
| `06-nacl-kmitl/` | **Missing** |
| `01-university/internship/` | **Missing** |
| `03-ai/projects/nacl-nextpath-x/` | **Missing** |

Three out of three. The guide was last updated 2026-08-11 — two weeks and roughly 34 commits ago. `VAULT-GUIDE.md` also lists a folder called `rome-wasnt-build-in-a-day/`, a name that has never existed on disk; the actual folder is `rome-pathfinding/`.

Look at *how* each one failed, because the pattern matters more than the count:

- **`01-university/internship/` is missing, but `04-archive/agoda-internship/` exists.** This is not carelessness. An archival operation ran correctly and nothing updated the documents pointing at the old location. That is a **lifecycle bug**, and it is the reason Part 3 makes de-referencing a mandatory step of archiving rather than a nicety.
- **`06-nacl-kmitl/` appears in *both* `VAULT-GUIDE.md` and `BRIDGE.md`.** The same fact was written in two governing documents, so there were two places to forget. This is the direct argument against your own prescribed four-document read order.
- **`03-ai/projects/nacl-nextpath-x/`** drifted through a rename that no document followed.

### The conclusion you should take from this

Your vault is small — 131 Markdown files, about 133,000 words. It is nowhere near the scale where structure fails. And yet **the rules layer has already rotted while the content layer is fine.**

That inverts the usual assumption. The thing that breaks a knowledge system over five to ten years is not a bad folder tree. It is **governance documents that describe a system which no longer exists.** Once the map is wrong, you stop trusting it; once you stop trusting it, you stop filing correctly; then the content layer rots too. You are currently at step one of that sequence.

So the single governing principle of this design is:

> **Every rule must be either machine-checkable or not written down.**

A rule nobody can verify is a rule that will be wrong within a month and misleading within a year. Concretely this means: one governing file instead of four, and a script that fails loudly when the file disagrees with the disk. That script is worth more than any folder structure I could design for you.

### Three live contradictions the architecture has to settle

These are already active in your system. Each is verifiable. Each needs a decision, and I make one for each below.

**1. `assignments-tracker.md` versus "Operational State Stays Separate."**
Your project `CLAUDE.md` mandates updating `01-university/assignments-tracker.md` on every status change and forbids committing a status change without syncing it. Your KOS instructions say live status belongs in your tracking tool, not in knowledge files. Both rules are currently active, and your recent commits do exactly what `CLAUDE.md` says. One of these has to die. *(Decision in Part 1.)*

**2. "Never put raw work files here" versus what is actually on disk.**
399 PNG files live inside the vault, and `slide-06-lp-diagram.html` sits in your vault root. The rule as written is already unenforced, which means it will not survive five years — an unenforced rule is worse than no rule, because it teaches you that rules here are decorative.

What makes this the *right* kind of violation is that both cases are correct and the rule is what is wrong: the PNGs are annotated screenshots their notes are meaningless without, and the HTML file is embedded live via `![[slide-06-lp-diagram.html]]` in `rome-pathfinding.md`. You were filing well and breaking the rule to do it. *(Replacement rule in Part 4.)*

**3. Binary assets in git.**
The vault is a git repository with 34 commits and carries roughly 400 images. Over a ten-year horizon this is a real durability question, and you asked me to surface exactly this kind of thing. *(Handled in Part 3, Asset Durability.)*

One more, smaller: `02-programming/guides/system-design-notes/` is a vendored external repository living inside your vault, complete with its own `.gitignore`. It is reference material you did not write. It should be marked as such or moved out — otherwise in three years you will not remember which parts are your notes and which are someone else's book summary.

---

## Part 1 — The Knowledge Operating System

### The core problem

You have four tools and a pile of files. Right now the boundaries between them are described by intent ("Obsidian is for knowledge") rather than by a test you can apply in two seconds while holding a file you need to put somewhere. Intent-based boundaries fail because every document feels like it could go anywhere.

The fix is to give each store **one question it answers**, and to make those questions mutually exclusive.

### The four stores

Note that there are four, not three. Your file store holds 47,373 files. Pretending it is not part of the system is how `slide-06-lp-diagram.html` ended up in your vault root.

| Store | Answers the question | Time character | Source of truth for |
|---|---|---|---|
| **Obsidian** | *What do I know, what is due, what did I decide?* | Durable — accumulates | **Everything textual.** Understanding, decisions, reasoning, lessons, **and status** |
| **Code repos (VS Code)** | *How does it actually work?* | Versioned with code | **Implementation.** Source, plus docs that must change when code changes |
| **Files (`~/Documents`, `~/Code`)** | *What did I produce or receive?* | Static artifacts | **Deliverables.** PDFs, slides, DOCX, datasets, submissions |
| **Claude** | *What does all of this mean together?* | Stateless — nothing persists | **Nothing.** Never a source of truth |

**Obsidian is the one app.** VS Code stays only because you cannot write and run code in a note editor, and Files stays only because binaries are not text. Neither is a knowledge store competing with Obsidian; they are the two things Obsidian genuinely cannot be.

**What dropping Notion costs, stated honestly.** You lose the clean separation between things that expire (deadlines, status) and things that accumulate (understanding). That separation is genuinely valuable at scale, because expiring data churns and churning data pollutes durable notes. At 131 notes and one degree programme, it is solving a problem you do not have — and it costs you a second app to open, a second place to look, and a sync you have to remember. Revisit if you ever run a team or a business from this vault. Until then, one app wins.

### The two-second filing test

When a new thing appears, ask in this order and stop at the first yes:

1. **Is it a binary file I produced or received?** → Files (`~/Documents/`).
2. **Does it have to change whenever the code changes?** → Beside the code (`~/Code/`).
3. **Will I want to reread this in six months?** → Obsidian.
4. **None of the above** → delete it. Not the inbox — delete it.

Three questions and a default. Option 4 matters more than it looks: most captured things are not worth keeping, and a system that assumes everything deserves a home is a system that fills with sediment.

Note what is *absent* from this test — there is no "does it have a deadline" branch any more. Deadlines are a **field on a note**, not a category of thing. That is the whole simplification.

### Claude's position, and why it holds nothing

Claude is a **reasoning layer with no persistence**. It reads from the other four stores, thinks, and writes results back into one of them. It never becomes the place a fact lives.

This is not a limitation to work around. It is the property that makes the whole system durable. Every fact stays in a plain file you own, on a disk you control, readable without any AI. If Claude disappeared tomorrow, or its pricing changed, or a model was deprecated, your knowledge would be untouched. Design decisions that make Claude cheaper and smarter (Part 7) are optimizations *on top of* a system that works without it — never dependencies.

The practical rule: **Claude may propose a change to any store; only you commit it.** Your File Change Authority rule already says this. It is correct and it should stay.

### What must never be duplicated

Duplication is the mechanism by which every knowledge system dies. Two copies of a fact drift, and once they disagree you trust neither. Your `06-nacl-kmitl/` entry, written into two documents and stale in both, is exactly this failure in miniature.

| Fact | Lives in exactly one place | Everywhere else it is |
|---|---|---|
| Assignment deadline & status | **The assignment note's frontmatter** | generated, or a link |
| What an assignment asks for | The assignment note body | a link |
| The submitted PDF | Files | a path reference |
| Why a technical choice was made | Obsidian decision entry | a link |
| How a function works | The code, or a doc next to it | a link |
| Folder rules | `_meta/KOS.md` | nothing — nowhere else states them |

The enforcement rule is one line, and it is the most important sentence in this document:

> **If a fact appears in two files, one of them is wrong. You just don't know which yet.**

### The one exception: generated views

A derived tracker duplicates `due` and `status` by design, so state the exception explicitly or future-you will "fix" it:

> **A generated view is exempt — one source, one derived view, regenerated and never hand-edited.**
>
> Generated regions are fenced with `<!-- BEGIN GENERATED -->` / `<!-- END GENERATED -->`. Inside the fence, edits are overwritten. Outside it, nothing is ever touched.

This is not a loophole. The rule against duplication exists because two *independently maintained* copies drift. A copy that is mechanically reproduced from its source cannot drift — it can only be stale, and staleness is visible and fixable by re-running one command. That is a categorically different failure mode, and a much better one.

### Decision on contradiction #1 — the assignments tracker

**`assignments-tracker.md` stays exactly where it is, and stops being a file you maintain.**

Your complaint is precise and it is not about location: *"I don't want to have to tell you to update tracker."* Moving it to Notion would not fix that — it would just move the manual step into a different app. The problem is that a manual step exists at all.

Today the tracker is kept true by three separate pieces of discipline: a rule in `CLAUDE.md` saying always sync it, a `Stop` hook reminding you to sync it, and you remembering to check. Three mechanisms, all of them made of memory, all of them enforcing something that a script does in half a second.

**The fix is to delete the manual step, not relocate it.**

> **Each assignment note's frontmatter is the source of truth. The tracker is a generated view of it.**

```yaml
---
title: "UX/UI: UI Hunt — Unusual Screens"
tags: [university, uxui]
status: submitted
due: 2026-09-07
points: 6
subject: uxui
---
```

`_meta/sync-tracker.sh` reads that frontmatter across every assignment note and rewrites the tracker's tables between `<!-- BEGIN GENERATED -->` markers. A `SessionStart` hook runs it automatically. You never sync anything; you edit the note you were editing anyway, and the tracker is already correct next time you open it.

**Why `SessionStart` and not an on-edit hook.** You do most of your editing inside Obsidian, and Claude Code hooks cannot see those edits — a `PostToolUse` hook only fires when *Claude* writes a file, which would leave the majority of your changes unsynced and the promise quietly broken. `SessionStart` fires once per session and picks up everything that changed since last time, whoever changed it.

**The honest limit.** The tracker is regenerated when a Claude session starts. If you edit a note in Obsidian and look at the tracker thirty seconds later without starting a session, it is stale until next time. The fix for that is running one command by hand, not building a file-watcher — a background daemon to save you thirty seconds of staleness is exactly the kind of automation Part 12 tells you to refuse.

**What this deletes:**
- The Assignment Tracker Rule in `CLAUDE.md` — not because status moved away, but because nothing needs syncing.
- The assignment half of the `Stop` hook reminder — once sync is automatic, a message telling you to do it by hand is instructing you to duplicate a machine. Leaving two mechanisms with different assumptions is precisely how the Part 0 drift happened.

**The prerequisite, and it is real work.** Your frontmatter is not uniform today. `uxui-ui-hunt.md` has `due: 2026-09-07`; `rtw-resume-assignment.md` and `rome-pathfinding.md` state their due dates in body prose. `status:` currently ranges over `active`, `archived`, and `submitted` with no controlled vocabulary. Nothing derived works until this is uniform, which is why normalization is its own milestone with its own validation.

**Status vocabulary.** Part 3 proposes `active | stable | archived`. Assignments need one more, because `submitted` is real, already in use, and means something the others do not — done by you, not yet graded:

```
active → submitted → graded → archived
```

Non-assignment notes keep `active | stable | archived`. Two vocabularies is one more than ideal, but collapsing `submitted` into `stable` would throw away the distinction you most want to see at a glance.

**Cost of being wrong:** near zero. The generated tables are reproducible from the notes at any time, and everything outside the markers is never touched.

---

## Part 2 — Folder Architecture

### Diagnosis of the current tree

Your top level is:

```
00-inbox/  01-university/  02-programming/  03-ai/  04-archive/
```

These are four different *kinds* of category wearing the same numbering:

- `00-inbox` and `04-archive` are **lifecycle states**.
- `01-university` is a **life phase**.
- `02-programming` is a **topic**.
- `03-ai` is a **tool**.

Mixing four incompatible axes at the top level is precisely why filing requires thought. A note about an AI university project written in Python has four valid homes, so you have to decide every time — which is the decision fatigue you asked me to remove.

Each axis also fails on its own timeline:

- **`01-university` expires.** You graduate in a year or two. Then a top-level folder holds a closed chapter, and the vault's most prominent structure describes your past.
- **`02-programming` mixes lifecycles.** `guides/` is durable reference that never ends; `projects/` is per-project material that finishes. Two different retirement schedules in one folder means neither can be retired cleanly.
- **`03-ai` is the worst of the four, and it is the most urgent.** It categorizes by the tool used to produce the work. Within two years essentially all of your work will be AI-assisted. A category that will match everything is a category that means nothing, and `03-ai` is on track to quietly absorb the vault.

### The principle

> **The top level should use exactly one axis, and it should be the axis that never changes: lifecycle.**

Topic changes. Tools change — `03-ai` is proof. Life phase changes. But "is this still live?" is a question that will still make sense in 2036.

### Decision: keep your top level. Fix only what is broken.

You want university one click away, and `01-university/` at the top of the sidebar is the fastest possible version of that. A restructure would move it down a level and buy you nothing you can feel this year.

So the recommendation is **surgical, not architectural**:

```
_meta/            NEW — the governing document, templates, check script, sync script
00-inbox/         unchanged
01-university/    unchanged — your dominant use case, stays at the top
02-programming/   unchanged
03-ai/            DELETED — see below
04-archive/       unchanged
HOME.md           NEW — the dashboard you open into
```

**One folder dies. One folder is added. Everything else stays put.**

`03-ai/` is the only genuinely broken category, and the argument against it does not depend on any of the rest: it classifies by *the tool used to produce the work*. Within two years essentially everything you do will be AI-assisted, and a category that matches everything means nothing. It is already misleading — `casestudy01-os` and `modular-synth` are coursework whose session logs live there purely because Claude helped write them.

Its contents move to a rule **you already documented in `VAULT-GUIDE.md`** for non-AI projects — a `-log.md` sibling in the subject folder:

| From | To |
|---|---|
| `03-ai/projects/rome-pathfinding/` | `01-university/year-3/ai/rome-pathfinding-log.md` (+ `romania.json`, `rome-assignment.md` alongside) |
| `03-ai/projects/casestudy01-os/` | `01-university/year-3/os/casestudy01-log.md` |
| `03-ai/projects/modular-synth/` | `01-university/year-3/mcu/mcu-stm32-log.md` |
| `03-ai/projects/drunkbill/` | `02-programming/projects/drunkbill-log.md` |

Four mechanical moves. After them, the AI/non-AI distinction disappears from the vault entirely, and every project's log sits next to the note it belongs to — which is also fewer clicks from university material, not more.

### What was deferred, and when to revisit

The first draft proposed replacing the top level with `10-areas/ 20-projects/ 30-library/ 90-archive/` — one axis, lifecycle, so that graduating would retire university in a single move. **That argument is still correct and it is now deferred.** The reasoning for deferring:

- The cost is paid today (a session of moves, every path table rewritten) and the benefit arrives at graduation.
- It makes your most-used folder one level deeper, against an explicit requirement.
- Doing it later is not much harder. Obsidian resolves `[[wikilinks]]` by name, so the expensive part is the same at 131 notes or 400.

**Revisit when either is true:** you graduate, or the vault passes roughly 1,000 notes. Whichever comes first, reread the deferred design in the Part 2 sections below — the diagnosis of the four-axis problem is unchanged and will be waiting.

Until then, the rules that follow — when to create a folder, when not to, the depth limit — apply to your existing structure exactly as written.

### The deferred design, for reference

```
_meta/            the governing document, templates, and the check script
00-inbox/         capture only — target state is empty
10-areas/         ongoing responsibilities with no end date
20-projects/      work with a definition of done
30-library/       durable reference not owned by any one project
90-archive/       finished, superseded, or retired
```

Six entries. Five you file into.

**`_meta/`** — the rules and the tools that enforce them. Leading underscore sorts it above the numbers and marks it as "about the vault, not in the vault." One governing file lives here, plus templates and `check.sh`. Currently `VAULT-GUIDE.md`, `BRIDGE.md`, and `CLAUDE.md` are loose in the root; consolidating them here is Milestone 1.

**`00-inbox/`** — the only place you are allowed to put something without deciding. Its health metric is *emptiness*: anything older than two weeks gets deleted, not filed. An inbox that accumulates is a second archive with a misleading name.

**`10-areas/`** — responsibilities that are ongoing and have no completion state. `university/`, `career/`, `health/`. Areas are the only folders that may be nested by sub-responsibility (`university/year-3/uxui/`), because that nesting reflects real institutional structure rather than an organizational preference.

Crucially, **an area retires as a single move.** When you graduate, `10-areas/university/` becomes `90-archive/university/`. One operation. Compare that to today, where "university" is entangled across `01-university`, `03-ai/projects/`, and `02-programming/` — retiring it would be a restructure, so you will never do it, so it will sit at the top level forever.

**`20-projects/`** — anything with a definition of done. One folder per project. **The reason project material is not filed under its area is that projects and areas retire on completely different clocks:** a project finishes in weeks, an area lasts years. Keeping them separate means archiving a project never disturbs an area, and retiring an area never orphans a project.

**`30-library/`** — durable reference material you did not produce as part of any project: book notes, article summaries, technical guides, papers. It grows monotonically and is never archived, because reference does not expire — it just gets consulted less. `02-programming/guides/` and `system-design-notes/` belong here.

**`90-archive/`** — done, superseded, retired. `90` rather than `04` because it should sort last forever, with room for `40`–`80` above it. Archive is **read-only by convention**: you may read it, you may not edit it. If something in the archive needs updating, it is not archived — move it back out. This single rule prevents the archive from becoming a shadow working directory.

### When to create a new folder

Three conditions, all required:

1. **Five or more notes already exist** that would live in it. Not four. Not "I expect five."
2. **They share a retirement date.** A folder is a unit of archival; if its contents will not be archived together, it is a tag, not a folder.
3. **The name will still make sense in five years.**

Until all three hold, keep notes flat in the parent. A flat folder of thirty files is searchable in half a second. A five-level tree with two files per leaf is not searchable by any means, including by you.

### When NOT to create a folder

- **Never for one note.** A single note in its own folder is a note that is hard to find and a folder that is hard to delete.
- **Never named after a tool.** `03-ai/` is the object lesson. Also: no `notion/`, no `claude/`, no `vscode/`.
- **Never named after a format.** No `pdfs/`, no `images/`, no `videos/`. Format is not a subject; you will never think "I need something, and it was a PDF."
- **Never named after a year at the top level.** Years belong inside areas where an institution imposes them (`university/year-3/`), never as an organizing principle of their own.
- **Never to separate "important" from "unimportant."** You cannot predict this, and the judgment inverts over time.

### Depth limit

**Maximum three levels below the top.** `20-projects/rome-pathfinding/assets/diagram.png` is at the limit and is fine. Anything deeper means you are encoding in the path what should be in the note.

Reason: every level of depth is a decision on the way in and a guess on the way out. Search handles retrieval; folders only need to handle *filing* and *archiving*.

### How this scales

**At 300 notes** — structure unchanged. `30-library/` starts to feel large; leave it flat and use search.

**At 1,000 notes** — `30-library/` gets internal splits, but only where a subtopic has fifteen-plus notes. `10-areas/` gains an area or two as life changes. The top level does not move.

**At 5,000 notes** — still the same top level. Folders have stopped being how you find things (search and links do that) and are now purely how you *archive* things. This is the intended end state: **folders are a retirement mechanism, not a retrieval mechanism.** Design them for the day you want a whole chapter gone, because retrieval was solved by full-text search a long time ago.

**The stress test:** in 2032 you are five years into a career, university long finished. Under the current tree, `01-university` still sits at the top of your sidebar, and every AI-assisted project of your career has piled into `03-ai`. Under the proposed tree, `10-areas/university/` moved to `90-archive/` on graduation day in one drag, and `20-projects/` holds career work with the same shape it has today. Nothing was restructured. That is the whole argument.

### Migration cost of the deferred version, honestly

It is a real rename of your top level and it will churn every hand-written path in `BRIDGE.md`. Obsidian updates `[[wikilinks]]` automatically on folder moves — they are name-based, not path-based — so the genuinely manual work is only the path tables in the governing docs and the `**File:**` references. One focused session, not a project, whenever you decide to do it.

**You are taking the smaller change instead**, which is the `03-ai` fix alone. That was always a legitimate choice rather than a compromise: it removes the one category that is actively wrong and leaves the ones that are merely imperfect.

### Easy access — `HOME.md`

Fast access is not really a folder problem, and it is worth being clear about why. Obsidian's `Cmd+O` already opens any note in under two seconds from anywhere, no matter how it is filed. What a top-level folder actually buys you is *the sidebar being right when you glance at it* — which is real, and is why `01-university/` stays where it is.

What genuinely speeds up a daily start is a single note you open into:

```markdown
# HOME

## This week
<!-- BEGIN GENERATED --> ← next 5 assignments by due date, from frontmatter
<!-- END GENERATED -->

## Subjects
[[uxui-week7-crazy8s-storyboard]] · [[os-case-study-1]] · [[rome-pathfinding]] · …

## Links
[[assignments-tracker]] · [[KOS]]
```

The same `sync-tracker.py` writes the generated block, so what is due is on screen without you maintaining anything.

**How to make it the thing you land on:** bookmark it (`Cmd+O` → `HOME` → star it) and pin its tab. Obsidian has **no core "startup note" setting** — it reopens whatever tabs were last open, so a pinned `HOME` tab is what actually makes it the landing page. A community plugin can force it, but that is a dependency for a problem a pinned tab already solves.

No plugin required, and the file is plain Markdown, so Claude can read the same dashboard you do.

---

## Part 3 — Knowledge Governance

This is the part that determines whether the system is alive in five years. Structure is easy; keeping structure true is the hard problem, and the drift evidence in Part 0 shows it is already the failing one.

### Folder philosophy

**Folders answer "when does this die?" Tags and links answer "what is this about?"**

Once folders carry only lifecycle, filing becomes mechanical — is it live, is it reference, is it finished — and topic can live in frontmatter where multiple values are allowed and nothing has to be chosen exclusively.

### Document ownership

**Every note has exactly one owner folder, and one owner: you.** No note is co-owned by two folders.

When a note plausibly fits two places, **the more permanent one wins.** A note about the Rome pathfinding algorithm could sit in `20-projects/rome-pathfinding/` or `30-library/`. If the insight outlives the project, it goes to the library and the project links to it. Rule of thumb: *would this note still be worth reading if the project were cancelled tomorrow?* Yes → library. No → project.

This resolves nearly every hard filing case, and it resolves them the same way every time, which is what makes it a default rather than a decision.

### Note granularity

**One note = one thing you would search for by name.**

Too fine (a note per session, a note per paragraph) produces hundreds of fragments with no individual meaning. Too coarse (one note per course) produces documents you scroll rather than read, and — importantly for Part 7 — documents Claude must ingest entirely to answer a narrow question.

Practical bounds: **under 200 words, it is a section of another note. Over 2,000 words, it is probably two notes.** These are prompts to look, not laws.

The test that actually works: *would I ever link to this specific thing from somewhere else?* If yes, it is a note. If it only ever makes sense inside a larger document, it is a heading.

### Lifecycle management

Three states, in frontmatter:

```yaml
status: active     # being worked on now
status: stable     # finished and true — the normal resting state
status: archived   # in 90-archive/, read-only
```

Drop `draft`. It is indistinguishable from `active` in practice, and a state nobody can define is a state that ends up meaning "I forgot about this."

**`stable` is the state most notes should be in**, and this matters more than it sounds. A finished note is not dead — it is *done and correct*, and it is what makes knowledge compound. The `updated:` field applies only to `active` notes; on `stable` notes it creates date churn with no information, which is why your own guide already tells you to omit it on reference notes. That instinct was right; this just names it.

### Archival strategy

Archiving has **two steps, and skipping the second is the bug that killed `01-university/internship/`:**

1. Move the folder or note to `90-archive/`.
2. **Sweep every reference to its old location.** Search the vault for the old path and the old name. Update or remove each hit.

Step 2 is not optional and it is not "nice hygiene." It is what separates an archive from a set of broken links. The reason it gets skipped is that nobody remembers to do it, which is why `check.sh` (below) verifies it automatically and loudly.

**When to archive:**
- A project: when it is done and you have stopped referring to it — not on the day it ships. Give it a month.
- An area: when the responsibility genuinely ends (graduation, job change).
- A note: essentially never on its own. Notes archive with their container.

**Never archive:** decision logs and lessons learned. These are the highest-value, lowest-volume content you own, and their whole purpose is to be found years later by someone who has forgotten the context. They live in `30-library/` and stay live permanently.

### Deletion rules

Deletion is a feature. A system that only accumulates becomes a landfill you are afraid to look at.

**Delete freely:**
- Inbox captures older than two weeks. If it mattered, you would have filed it.
- Duplicates — keep the one with more links pointing at it.
- Superseded drafts, once the final version exists and is committed to git.
- Scratch and temporary notes, immediately after use.
- Any note that is only a link to something you can find in three seconds anyway.

**Never delete:**
- Decisions and their reasoning.
- Lessons learned.
- Anything a currently-live note links to. Fix the link first, or you have manufactured the exact problem Part 0 documents.

**The safety net:** the vault is in git. Deletion is recoverable, which means you can delete decisively rather than hoarding out of anxiety. This is a genuine and underrated benefit of version-controlling a vault, and it is worth using deliberately.

### Duplication prevention

One mechanism, applied consistently: **when you notice the same fact in two files, delete one and replace it with a link, in that moment.** Not later, not on a list. The window in which you know which copy is correct is short.

The recurring temptation is to copy a fact "for convenience" so a note reads standalone. Resist it. A `[[wikilink]]` is one click and it can never go stale.

The structural version of this rule is why Part 2 puts all rules in one file. Your `06-nacl-kmitl/` entry existed in two governing documents and was stale in both — not because you were careless, but because two copies is a design that requires perfect discipline forever. Designs that require perfect discipline fail. One copy needs no discipline at all.

### Asset durability — decision on contradiction #3

**Recommendation: keep images in git. Accept the ceiling, and watch it.**

Reasoning. The images are meaningful *with* their notes — an annotated screenshot is worthless separated from the note that annotates it. Versioning them together is correct, and separating them to protect repository size would trade a real benefit for a hypothetical problem.

The honest ceiling: git stores every version of every binary forever, so repeatedly-edited images grow the history permanently. At roughly 400 images your repository is comfortably fine. The failure point is around 2 GB of `.git`, where clones and pushes turn slow.

The mitigation is one line in the monthly review:

```
du -sh .git
```

Under 2 GB: do nothing. Over 2 GB: revisit, and the answer at that point is almost certainly "stop committing screenshots you re-export weekly," not "adopt Git LFS." Do not adopt LFS now. It adds a tool, a config, and a failure mode to solve a problem you do not have.

Two habits keep you far from the ceiling: screenshot as PNG at actual size rather than Retina 2x, and never commit an image you intend to re-export repeatedly.

### Review routines

The system needs three loops at three timescales. Keep them short enough that you actually run them — a 90-minute monthly review is a review you will skip twice and then abandon.

**Weekly — 10 minutes**
- Empty `00-inbox/` to zero. File or delete; there is no third option.
- Move any project finished this week to `status: stable`.

**Monthly — 30 minutes**
- Run `_meta/check.sh`. Fix what it reports. This is the single highest-value maintenance action in the system.
- Archive projects finished over a month ago, including the de-reference sweep.
- Check `du -sh .git`.

**Yearly — 2 hours**
- Read `_meta/KOS.md` end to end. Does it describe the system you actually have? Where it does not, decide which is wrong — the document or the vault — and fix that one.
- Retire any area whose responsibility has ended.
- Delete an entire folder of things you have not opened in a year. Doing this on purpose, once a year, is what keeps a ten-year vault from becoming a museum.

### Maintenance schedule at a glance

| Cadence | Time | Actions | Success looks like |
|---|---|---|---|
| Weekly | 10 min | Inbox to zero; mark finished work `stable` | Inbox empty |
| Monthly | 30 min | `check.sh`; archive + de-reference; `du -sh .git` | Zero check errors |
| Yearly | 2 hr | Reread `KOS.md`; retire an area; delete a folder | The doc matches the disk |

**Total: about 15 hours per year.** If it costs more than that, the system is too complex and the correct response is to simplify the system rather than to try harder.

### The mechanism that makes all of this hold

Everything above is conventional advice, and conventional advice is what your `VAULT-GUIDE.md` already contained before it went stale. The difference in this design is a single script:

```
_meta/check.sh
```

It verifies, in a few seconds:

1. **Every path mentioned in `_meta/KOS.md` exists on disk.** This is the exact check that would have caught all three of the Part 0 failures the day they happened.
2. **Every `[[wikilink]]` resolves** to a real note.
3. **Every `.md` file has valid frontmatter** with `title`, `tags`, and `status`.
4. **No note in `90-archive/` is linked to from outside the archive** — catching incomplete de-reference sweeps.
5. **`00-inbox/` has nothing older than two weeks.**

Run it monthly, and after any restructuring. It is perhaps fifty lines of shell and it is the difference between a governance document and a governance *system*. Everything else in this part is advice; this is enforcement.

The design rule it embodies is worth restating, because it should govern every rule you add in future years:

> **A rule that cannot be checked will be wrong within a month. Write checkable rules, or write none.**

---

## Part 4 — Document Classification

One table. It is the whole answer. Find the row, use the path, do not deliberate.

> **Path notation.** The table and the parts after it are written in the deferred Part 2 vocabulary, because the *reasoning* is the same either way and rewriting thirty rows twice would be churn. Translate as you read:
>
> | Written as | Your vault today |
> |---|---|
> | `10-areas/university/…` | `01-university/…` |
> | `20-projects/<name>/` | `01-university/year-3/<subject>/` for coursework · `02-programming/projects/` for personal projects |
> | `30-library/…` | `02-programming/guides/` |
> | `90-archive/…` | `04-archive/…` |
>
> Everything else — the *why*, the metadata, the AI guidance — applies unchanged.

### The master table

| What it is | Where it goes | Why | Useful metadata | How Claude should use it |
|---|---|---|---|---|
| **Active project** | `20-projects/<name>/` | Has a definition of done; archives as a unit | `status: active`, `tags` | Read `README.md` first, nothing else unless asked |
| **Completed project** | `90-archive/<name>/` after a month | Done and no longer consulted | `status: archived` | Ignore unless explicitly named |
| **Documentation (how something works)** | Next to the code, in the repo | Must version with the code | — | Read from the repo, never from the vault |
| **Documentation (why it exists)** | `20-projects/<name>/README.md` | Outlives any given implementation | `status` | Primary entry point |
| **Meeting notes** | `10-areas/<area>/meetings/YYYY-MM-DD-topic.md` | Belongs to an ongoing responsibility, not a project | `date`, attendees | Skip by default — decisions get extracted out |
| **Decision log** | `README.md` section, or `decisions.md` past five entries | Highest-value content you own; must be findable years later | `date` per entry | **Always read.** Cheapest possible context |
| **Changelog** | The code repo (git handles it) | Git log already is one | — | Read from git, not the vault |
| **Lessons learned** | `30-library/lessons/<topic>.md` | Outlives the project that produced it; never archived | `tags` | Read when starting similar work |
| **Book notes** | `30-library/books/<author>-<title>.md` | Durable reference, never expires | `author`, `year`, `tags` | Read on request only |
| **Article / blog summary** | `30-library/articles/<topic>.md` | Same, and often ends up merged into a topic note | `source` URL, `tags` | On request only |
| **Research paper (the PDF)** | `~/Documents/Papers/` | Binary artifact | — | Never — read your note about it |
| **Research paper (your notes)** | `30-library/papers/<author>-<year>.md` | Your understanding is the durable part | `authors`, `year`, `doi` | On request |
| **Study notes** | `10-areas/university/year-N/<subject>/` | Belongs to an ongoing responsibility, retires with it | `status`, `tags` | On request |
| **Personal journal** *(only if you keep one — you currently do not)* | `10-areas/personal/journal/YYYY-MM-DD.md` | Ongoing, private, dated by nature | `date` | **Never.** Excluded from AI context by convention |
| **Career documents (notes)** | `10-areas/career/` | Ongoing responsibility for decades | `status` | On request |
| **Resume (the PDF/DOCX)** | `~/Documents/Career/` | Deliverable | — | Never |
| **Resume (content & history)** | `10-areas/career/resume-content.md` | The source you regenerate exports from | `updated` | On request — good Claude task |
| **Portfolio** | Its own repo in `~/Code/` | It is a website, not a note | — | From the repo |
| **Screenshots supporting a note** | `<note-folder>/assets/` | The note is unreadable without them | — | Never read directly |
| **Screenshots that are deliverables** | `~/Documents/<project>/` | Output, not input | — | Never |
| **Images (decorative)** | Delete them | They are not knowledge | — | — |
| **PDFs you received** | `~/Documents/<area>/` | Binary artifact you did not write | — | Never — read the vault note |
| **PDFs you produced** | `~/Documents/<area>/` | Deliverable | — | Never |
| **Downloads** | `~/Downloads/`, cleared weekly | Not a storage location | — | Never |
| **Miscellaneous** | `00-inbox/`, then filed or deleted in ≤2 weeks | The only legitimate "I don't know" | — | Never |

### Decision on contradiction #2 — the work-files rule

Your current rule — *"Never put raw work files here"* — is violated on disk today by `slide-06-lp-diagram.html` and 399 PNGs. A rule already broken at 131 notes will not hold at 1,000. The problem is that the rule is drawn along the wrong line: it separates by **file type**, when the meaningful distinction is **role**.

Replacement rule, with the exception encoded rather than left implicit:

> **Inputs live with the note. Outputs live in Files.**
>
> Test: *if this file vanished, would the note become unreadable?*
> **Yes → vault** (`<note-folder>/assets/`). It is an input — an annotated screenshot, a diagram the note explains.
> **No → Files.** It is an output — the PDF you submitted, the deck you presented, the DOCX you emailed.

This legitimizes your 399 PNGs, which were always correct: annotated UI screenshots that their notes are meaningless without. It also legitimizes `slide-06-lp-diagram.html`, which is embedded live by `rome-pathfinding.md` — the note renders the diagram from it, so it is an input, and it belongs in the vault. Its only defect is sitting in the **root** rather than next to the note that embeds it. It excludes the exported `slide-06-lp-diagram.png`, which is already correctly in `~/Documents/`.

That pairing — HTML source in the vault, exported PNG in Documents — is the rule working exactly as intended, and you arrived at it before the rule existed.

**Why this version survives.** The old rule required you to feel guilty every time you did the right thing, and guilt is not an enforcement mechanism. The new rule matches what you were already doing correctly, which means following it costs nothing.

### Metadata standard

Three required fields, and stop there:

```yaml
---
title: Human Readable Title
tags: [topic, topic]
status: active | stable | archived
---
```

Add `created:` if you want it. Add `updated:` **only on `active` notes** — on stable notes it is churn, as your own guide already recognized.

**Why so few.** Every required field is a small tax on every note forever, and fields you do not query are pure cost. You are not running Dataview queries over `author` and `year` on 131 notes; you are searching. Add a field the day you have a concrete need to filter by it, and not before.

### Tags

Tags are for **cross-cutting topics only** — things that appear across multiple folders. If a tag matches exactly one folder, delete it: the folder already says it.

Keep the tag list under twenty. Review it yearly and merge anything used fewer than three times. A tag used twice is a typo waiting to happen; an unbounded tag vocabulary is a second, worse folder structure with no rules.

---

## Part 5 — Naming Convention

The goal is that you never think about naming. One default, three narrow exceptions.

### The default

```
kebab-case-descriptive-name.md
```

Lowercase. Hyphens. Words a future you would actually type into search.

- ✅ `rome-pathfinding-heuristic-design.md`
- ❌ `Rome Pathfinding Heuristic Design.md` (spaces break shell commands and URLs)
- ❌ `rome_pathfinding.md` (underscores are harder to type and visually merge with link underlines)
- ❌ `RomePathfinding.md` (case-sensitivity differs between macOS and Linux — a real portability bug)
- ❌ `notes.md`, `final.md`, `stuff.md` (meaningless at scale, and you will have thirty of them)

**Front-load the distinguishing word.** `uxui-week3-market-comparison.md` sorts and scans well because the varying part comes last. This is why your existing UX/UI naming works and should be kept.

### The three exceptions

**1. Dates — only when the note *is* a point in time.**

```
2026-08-25-standup.md          ✅ a meeting on a specific day
2026-08-25-rome-pathfinding.md ❌ a topic, not an event
```

Always `YYYY-MM-DD`, always as a prefix, because it sorts chronologically as text.

The test: *does this note describe a moment, or a subject?* Moments get dates — daily notes, meetings, incident reports. Subjects never do, because a dated subject note fragments your knowledge into one note per time you thought about it, which is the single most common way a vault becomes unusable.

**2. Version numbers — never in the vault. Only on exported deliverables.**

```
Vault:  investment-report.md              ✅ git holds every version
Vault:  investment-report-v2-final.md     ❌ never
Files:  67011178_Report1_v2.pdf           ✅ exports are immutable and need distinct names
```

The vault is version-controlled; a version number in a filename there is a second, worse version control system running in parallel. Deliverables are not version-controlled, so their versions belong in the name.

**3. Folder names — same convention, but nouns, and plural for collections.**

```
20-projects/rome-pathfinding/     ✅
30-library/books/                 ✅ plural, it holds many
_meta/                            ✅ underscore marks meta
```

### Everything else

| Kind | Rule | Example |
|---|---|---|
| Markdown | kebab-case, descriptive | `bond-valuation-method.md` |
| PDFs you received | keep the original name | `A2 Labour law.pdf` |
| PDFs you produced | whatever the recipient requires | `67011178_UIHunt.pdf` |
| Images | `<note-name>-<what-it-shows>.png` | `ui-hunt-booking-hotel-list.png` |
| Meeting notes | `YYYY-MM-DD-topic.md` | `2026-08-25-advisor-sync.md` |
| Decision entries | not files — dated headings | `## 2026-08-25 — Chose A* over Dijkstra` |
| References | `<author>-<title>.md` | `kleppmann-designing-data-intensive.md` |

Note the deliberate asymmetry on PDFs: received files keep their original name so you can match them against the source they came from; produced files follow whatever the recipient demands. Your vault note carries the human-readable name; the file carries whatever its context requires. Neither needs to compromise.

### How to stay consistent for years

Consistency comes from having **one default and few exceptions**, not from discipline. You have one default here. When you hesitate, the answer is always: lowercase, hyphens, describe the thing, no date, no version.

`check.sh` flags files with spaces or uppercase in the name. That is the only enforcement needed, and it costs nothing.

---

## Part 6 — Project Documentation Standard

### Pushing back on the nine-file list

You asked for nine documents per project: README, Context, Current Status, Decisions, Lessons Learned, References, Assets, Changelog, Next Actions.

**I recommend against it, and the reasoning is the same principle driving the rest of this design.** Nine files across thirty projects is 270 files, and the overwhelming majority would be empty or one line long. Empty files are worse than absent ones: they cost a create decision, they clutter search results, they make Claude read nine files to learn what one would have told it, and — most damagingly — they make starting a new project feel like paperwork. A standard that makes starting expensive is a standard you will start skipping, which is how you end up with projects that have no documentation at all.

Two of the nine also duplicate something that already exists. **Current Status** is a `status:` field in frontmatter, which the tracker already generates from — a prose status file would be a third copy that goes stale first. **Changelog** is what `git log` is, and maintaining a parallel one by hand guarantees the two disagree.

### What I recommend instead

**One file. Sections earn promotion to files by growing.**

```
20-projects/<name>/
  README.md        ← always. Usually the only file.
```

`README.md` contains, in this order:

```markdown
---
title: Project Name
tags: [topic]
status: active
---

# Project Name

**What:** one sentence.
**Why:** one sentence.
**Where:** code → ~/Code/<repo> · files → ~/Documents/<path>
## Context
Three to five sentences. What problem, what constraints, what has been tried.

## Decisions
### 2026-08-25 — Chose X over Y
Because Z. Rejected Y because W.

## Next Actions
- [ ] the next concrete thing

## References
- [[related-note]]
- external link
```

That is Context, Decisions, References, and Next Actions as **sections**, plus the pointer block that replaces a separate Assets file.

### Promotion triggers

A section becomes its own file when — and only when — it crosses a threshold:

| Section | Becomes a file when | Filename |
|---|---|---|
| Decisions | more than 5 entries | `decisions.md` |
| Work log | more than 3 sessions | `log.md` |
| Assets | more than 2 images | `assets/` folder |
| Lessons learned | the project ends | `30-library/lessons/<topic>.md` |

Everything starts as a heading. The file appears when the content demands it, which means every file that exists has earned its existence.

Note that **Lessons Learned deliberately leaves the project folder** when the project ends. This is the single highest-value move in the standard. Lessons are the part of a project that outlives it, and burying them in a folder destined for `90-archive/` guarantees you will never read them again — which defeats the entire purpose of writing them down. They go to `30-library/lessons/`, which is never archived.

### The purpose of each element

- **README** — the single entry point. Both you in six months and Claude on a cold start read this first and often only this. Its first fifteen lines are optimized for exactly that in Part 7.
- **What / Why** — orientation in two seconds. The most common failure of an old project folder is that you cannot remember what it was for.
- **Where** — three pointers replacing an Assets file. Solves the "where did I put the code" problem permanently.
- **Context** — what a competent person needs to know before touching this. The constraints matter more than the description; constraints are what you forget.
- **Decisions** — dated entries with reasoning. **This is the highest-value content in any project.** Not what you chose — *why*, and what you rejected. Six months later the "what" is visible in the code; only the "why" is gone. When you reconsider a decision, this is what tells you whether the original reason still holds.
- **Next Actions** — the trailhead. One item is enough. This is not a full task list; it is the note that lets you resume without re-reading everything.
- **References** — links out. Keeps the README short by pointing rather than including.

### Non-AI projects and session logs

Your existing Reference/Session Split rule solves a real problem: session churn polluting stable reference notes. Keep the principle, simplify the mechanism.

Under this structure, `log.md` sits next to `README.md` in the same project folder, and the trigger is "more than three sessions" rather than "is it AI-assisted." The AI/non-AI distinction disappears entirely, which also removes the last reason `03-ai/` needs to exist.

---

## Part 7 — AI Optimization

The goal: Claude understands a project from the smallest possible number of tokens, and you never have to re-explain context you already wrote down.

### The core misunderstanding to fix first

The instinct is "give Claude everything so it has full context." This is wrong in both directions at once: it costs far more, *and* it produces worse answers, because the signal you care about gets diluted across thousands of tokens of things you did not care about.

Retrieval quality degrades with irrelevant context. A focused 500-token README produces better output than a 30,000-token folder dump, and costs about 1.5% as much.

**The rule that follows: never say "read my vault." Always name a file.**

### The context hierarchy

Four levels. Give Claude the lowest level that answers the question, and stop.

| Level | What | Size | When |
|---|---|---|---|
| **L0** | `_meta/CLAUDE.md` — the rules | ~100 lines | Always, automatically loaded |
| **L1** | `20-projects/<name>/README.md` | ~50 lines | Any question about that project |
| **L2** | A specific note | ~200 lines | When L1 says the answer is in it |
| **L3** | Code or source files | large | Only when actually editing code |

Most sessions need L0 + L1. That is roughly 150 lines — about 2,000 tokens — and it is enough for Claude to know what the project is, what was decided, what is next, and where everything lives.

The concrete comparison: pointing Claude at `20-projects/rome-pathfinding/README.md` costs about 700 tokens. Letting it explore `03-ai/projects/rome-pathfinding/` plus the reference note plus the conversation log costs roughly 35,000. **Same answer, fifty times the cost.** Over a year of daily use that difference is the entire value of the optimization.

### The context block

The first fifteen lines of every project README are a fixed-shape block Claude can rely on:

```markdown
---
title: Rome Pathfinding
tags: [ai, university]
status: active
---

# Rome Pathfinding

**What:** A* pathfinding over Romanian cities, React + TS frontend.
**Why:** AI coursework, due 2026-10-13.
**Where:** code → ~/Code/rome-pathfinding · files → ~/Documents/...**Stack:** Vite 8, React 19, TypeScript, bun.
**Constraint:** custom heuristic only — straight-line distance and GPS are banned.
```

Everything Claude needs to avoid a wrong assumption is here. That `Constraint` line alone prevents an entire category of wasted session — and note that it currently lives in your Claude memory rather than in the project, which means it is invisible to any session that does not load that memory.

**Consistent shape is the point.** Because every README has the same first lines, Claude knows where to look without being told, and you never have to explain your conventions in a prompt.

### Documentation strategy for AI readability

Six habits, all of which also make documents better for humans:

1. **Front-load conclusions.** Answer first, reasoning after. Claude reading the top of a file should already have the answer.
2. **Tables over prose** for anything with repeated structure. Denser, unambiguous, and parsed reliably.
3. **Stable headings.** Headings are addresses. Once `## Decisions` exists, it never gets renamed to `## Design Choices` — renaming breaks every instruction that referenced it.
4. **State constraints explicitly**, including the negative ones. "GPS is banned" prevents more wasted work than three paragraphs of description.
5. **Absolute paths in pointers.** `~/Code/rome-pathfinding` is actionable; "the repo" is not.
6. **No rendered-only content.** Which brings us to the most consequential recommendation in this part.

### Why Dataview is excluded

Dataview is the most popular Obsidian plugin and it is the wrong choice for an AI-friendly, portable, ten-year vault.

A Dataview query is stored in the file as a query. The results exist only in Obsidian's renderer, at render time. Which means:

- **Claude reading the file sees the query, not the data.** Your carefully-built index page is, to every tool other than Obsidian, an empty page.
- **The file is no longer portable.** Open it in any other Markdown editor, or on GitHub, or in five years in whatever replaces Obsidian, and the content is gone.
- **You have acquired a hard dependency on one plugin** for content you cannot read without it.

This directly contradicts your stated priorities of portable Markdown, local-first ownership, and AI friendliness — three of your top eight.

The alternative is a plain Markdown index you maintain by hand or generate with a script. It is readable by everything, forever. At your scale, hand-maintained is honestly fine.

### Reusable context files

**`_meta/CLAUDE.md`** — the machine-readable rules, loaded automatically in every session. Keep it under 100 lines. It should contain: folder meanings, naming rule, where things go, file-change authority, and the read order. It should *not* contain: anything that changes weekly, anything duplicated from `KOS.md`, or long explanations of reasoning. It is a reference card, not a document.

**Your existing four-document read order should collapse to one.** Requiring Claude to read a system overview, a constitution, an architecture doc, and an operating-instructions doc before acting means four files to keep synchronized, which is four opportunities for the `06-nacl-kmitl` failure. It also spends real tokens on every single session before any work starts.

One file: `_meta/CLAUDE.md`. Under 100 lines. Verified by `check.sh`.

### How to give Claude only what it needs

A practical progression:

```
❌  "Look at my vault and tell me about the Rome project."
    → explores dozens of files, ~35,000 tokens

⚠️  "Read 20-projects/rome-pathfinding/ and tell me about it."
    → reads the whole folder, ~8,000 tokens

✅  "Read 20-projects/rome-pathfinding/README.md. What's the next action?"
    → ~700 tokens
```

Rules of thumb:

- **Name the file.** Always.
- **Ask a specific question.** "Tell me about X" invites exhaustive reading; "what's the next action for X" does not.
- **Let Claude ask for more.** A good README tells it which note holds the detail. Requesting one more named file is much cheaper than pre-loading five.
- **Start a new session per project.** Context carried between unrelated projects is pure cost — every subsequent message pays for it again.
- **If you ever keep a journal, never point at it.** `10-areas/personal/` would be out of scope by convention. You have no such folder today; this is a rule waiting for a case, not a description of one.

### The compounding effect

Every hour spent making a README good is repaid on every future session that reads it instead of re-deriving the same context. This is what "knowledge compounds" means operationally: not that you accumulate more notes, but that the cost of picking work back up keeps falling.

---

## Part 8 — VS Code Architecture

### The finding

`~/Documents/University/` contains **47,373 files** and includes these as top-level or near-top-level entries:

```
drunkbill/                                    (has .git, .vscode, src/)
timetable-website/
Network-and-Cloud-Laboratory-KMITL/nacl-nextpath-x/
Network-and-Cloud-Laboratory-KMITL/nacl-website/
Network-and-Cloud-Laboratory-KMITL/nacl-camellya/
```

These are software repositories living inside a documents folder, next to `Room C`, `TA`, `_Archive`, and lecture PDFs.

This is a category error with practical consequences: code gets backed up by document-sync tools that do not understand `node_modules`, `Cmd+P` in VS Code searches thousands of irrelevant PDFs, git repositories are nested inside a tree that is not itself a repository, and — the one that will actually bite — **when university ends and you archive `Documents/University/`, you will archive your code with it.**

### The fix

Three roots, one purpose each:

```
~/Code/            every git repository, one folder per repo, flat
~/Documents/       documents only — PDFs, slides, DOCX, deliverables
~/KnowledgeVault/  notes
```

`~/Code/` is **flat**. No `~/Code/university/`, no `~/Code/work/`. Repos are independent units with independent lifecycles; grouping them by origin means moving them when their origin changes, which is exactly the churn Part 2 is designed to avoid. Twenty to fifty flat repos is entirely navigable.

**What moves:** `drunkbill`, `timetable-website`, `nacl-nextpath-x`, `nacl-website`, `nacl-camellya`, and `rome-pathfinding`.
**What stays:** lecture PDFs, slides, submitted deliverables, `UniversityRules`, `Academic-PDF`, `Room C`, `TA`, `_Archive`, `Internship`.

**Migration risk:** the vault contains `**File:**` pointers and `university-files/` symlink references to these repos. Moving them breaks those references until updated. This is why the move is its own milestone with its own validation step, and why `check.sh` should exist before the move rather than after.

### The workspace layout

```
~/Code/
  <repo>/
    .vscode/settings.json    per-project editor settings
    README.md                what and how to run — always
    docs/                    only if the project is large
    src/
```

Open **one repo per VS Code window.** Multi-root workspaces sound efficient and produce slow search, confused extensions, and ambiguous "which project am I in" states. One window, one repo, one mental context.

### Categories you named

| Kind | Where | Note |
|---|---|---|
| **Repositories** | `~/Code/<repo>/` | Flat, one git repo each |
| **HTML projects** | `~/Code/<name>/` | A website is a repo even without a build step |
| **SQL** | `~/Code/<project>/sql/` | Versioned with what uses it |
| **Scripts** | `~/Code/scripts/` | One repo for all loose utilities |
| **Experiments** | `~/Code/scratch/` | Not a repo. Deleted monthly, no guilt |
| **Reusable components** | Inside the project that uses them | Extract to a shared repo only at the *third* use |
| **Documentation** | See below | The line that matters |

`~/Code/scratch/` deserves emphasis: having an explicit place where things are allowed to be temporary is what stops temporary things from being filed permanently "just in case." The monthly delete is the feature.

The "third use" rule for shared components is deliberate. Extracting at the second use is a coin flip; at the third you have real evidence of the abstraction's shape, and you will build the right one instead of a speculative one you refactor twice.

### Code docs versus vault notes — the test

> **If I deleted this repository tomorrow, would I want this text to survive?**
> **No → it lives beside the code.**
> **Yes → it lives in Obsidian.**

| Beside the code | In Obsidian |
|---|---|
| README — how to install and run | Why this project exists at all |
| API documentation | What I learned building it |
| ARCHITECTURE.md — how modules fit | Why I chose this architecture over the alternative |
| Inline comments | Lessons that apply to future projects |
| CONTRIBUTING, setup guides | Decisions and their reasoning |

The pattern: **mechanism lives with the code, meaning lives in the vault.** Mechanism becomes obsolete the moment the code changes and must version alongside it. Meaning survives rewrites, language changes, and the project's death — which is precisely why it must not be stored in something that dies with the project.

`ARCHITECTURE.md` is the interesting case. *How the modules fit together* is mechanism and belongs in the repo. *Why that shape rather than another* is meaning and belongs in the vault's decision log. Splitting them feels pedantic until the day you rewrite the project in a different language and want to know whether the original reasoning still applies.

---

## Part 12 — Automation Opportunities

Ordered by value-per-unit-complexity. The first two are worth doing; the next are conditional; the last group is worth actively avoiding.

### Worth doing

**1. `_meta/check.sh` — the governance checker.** *(Essential.)*
Described in Part 3. Roughly fifty lines of shell, run monthly. It is the only thing standing between this design and the fate of `VAULT-GUIDE.md`. If you implement one item from this entire document, make it this one.

**2. Obsidian Templates (core plugin, not community).** *(Essential.)*
Three templates: project README, note, meeting note. This is what makes "I always know what files a project should contain" true in practice rather than aspirationally. Core plugin means zero dependency risk and zero maintenance.

### Worth doing if you use them

**3. Obsidian Git — already installed.** *(Keep.)*
Auto-commit on a timer. Set the interval to 60 minutes or higher; more frequent commits produce a log too noisy to read, which defeats the point of having history. This is your backup and your undo, and it is already working.

**4. Claude workflows as slash commands.** *(Optional, high value once stable.)*
Two are worth defining once the structure settles:
- `/new-project <name>` — creates the folder and README from the template, with the context block pre-filled.
- `/archive <project>` — moves to `90-archive/`, then performs the de-reference sweep. **This directly automates the step that failed in Part 0**, which makes it the second-most-valuable automation after `check.sh`.

Build these *after* Milestone 4, not before. Automating a structure you are still changing means rewriting the automation.

**5. A generated index.** *(Optional.)*
A script that writes a plain-Markdown table of contents into `_meta/index.md`. Only worth it past roughly 300 notes. Plain Markdown output, so it stays readable everywhere — this is the AI-friendly replacement for a Dataview index page.

### Worth avoiding

**Dataview.** Reasoning in Part 7. Breaks portability and AI readability simultaneously.

**Templater** (the community plugin, distinct from core Templates). Powerful, scriptable, and a dependency with a learning curve. Core Templates covers everything this design needs.

**Auto-tagging, AI auto-filing, automatic note linking.** These automate the one activity that must stay yours. Filing is where you *decide what something means* — outsourcing it means accumulating files you never thought about, which is a vault with the appearance of organization and none of the substance.

**Sync services beyond git.** You have git. Adding Obsidian Sync or a cloud drive on top creates conflict-resolution problems that git already solved.

**Anything that writes to the vault without you seeing the diff.** Your File Change Authority rule is correct and should extend to automation, not just to Claude.

### The test for any future automation

> **Does this remove a decision I have to make repeatedly, or does it just remove typing?**

Removing decisions is valuable — templates remove "what sections does this need," `/archive` removes "what did I forget." Removing typing is usually a net negative, because the automation itself becomes something to maintain, understand, and eventually debug at the exact moment you needed it to just work.

---

## Part 13 — Implementation Roadmap

Seven milestones. Each is independently valuable, independently testable, and independently reversible. **Every one of them ends in a git commit, which is the rollback mechanism for all of them.**

Rules for execution:

- **One milestone per session.** Never two.
- **Approve each file operation explicitly.** File Change Authority applies throughout; Sonnet proposes, you approve, then it executes.
- **Validate before moving on.** If validation fails, roll back rather than patching forward.
- **`git status` must be clean before starting** any milestone.

---

### Milestone 0 — Reconcile the governing documents with the disk
**Do this first. It is the finding from Part 0 and it takes twenty minutes.**

**Objective:** make `VAULT-GUIDE.md`, `BRIDGE.md`, and `CLAUDE.md` describe the vault that actually exists today. No structural change — this is truth repair only.

**Actions:**
1. Remove all `06-nacl-kmitl/` references from `VAULT-GUIDE.md` and `BRIDGE.md`.
2. Correct `01-university/internship/` → `04-archive/agoda-internship/`.
3. Correct `03-ai/projects/nacl-nextpath-x/` and remove `rome-wasnt-build-in-a-day/`.
4. Decide on `slide-06-lp-diagram.html` in the vault root — **it stays in the vault** (it is embedded by `rome-pathfinding.md`); the open question is only whether it moves beside that note. Left in place pending your call.

**Validation:** every path named in either document resolves on disk. Check by hand this once; `check.sh` automates it in M1.

**Known false positive for `check.sh`:** `VAULT-GUIDE.md` documents template paths like `01-university/year-N/subject/topic.md`. These are placeholders, not real paths, and a naive checker flags them. Exclude paths containing `year-N` or `<name>` when you write the checker in M1.

**Rollback:** `git checkout VAULT-GUIDE.md BRIDGE.md`

**Why first:** everything downstream reads these documents. Restructuring on top of a false map produces a false map of a new structure.

---

### Milestone 1 — Create `_meta/` and the checker
**Objective:** one governing document plus automated enforcement, before any files move.

**Actions:**
1. Create `_meta/`.
2. Write `_meta/KOS.md` — the single governing document, merging the still-true parts of `VAULT-GUIDE.md` and `BRIDGE.md`.
3. Write `_meta/CLAUDE.md` — under 100 lines, machine-readable rules.
4. Write `_meta/check.sh` — the five checks from Part 3 (a sixth, frontmatter validity for assignments, is added in Milestone 2).
5. Leave `VAULT-GUIDE.md` and `BRIDGE.md` in place for now. Do not delete them yet.

**Validation:** `bash _meta/check.sh` runs and reports zero errors against the *current* structure.

**Rollback:** `rm -rf _meta/` — nothing else has changed.

**Why before moving anything:** the checker must exist before the migration so it can verify the migration. Building it afterward means having no way to confirm the move was clean.

---

### Milestone 2 — Normalize assignment frontmatter
**Objective:** make the notes a usable source of truth. Nothing can be generated until this is uniform.

**The problem:** three notes, three shapes. `uxui-ui-hunt.md` has `due: 2026-09-07` in frontmatter; `rtw-resume-assignment.md` and `rome-pathfinding.md` state due dates in body prose. `status:` ranges over `active`, `archived`, `submitted` with no controlled vocabulary.

**Actions:**
1. Add to every assignment note:
   ```yaml
   due: 2026-09-07      # ISO. Use `due: TBA` when genuinely unknown
   points: 6            # or omit if ungraded
   subject: uxui        # matches the subject folder name
   status: active | submitted | graded | archived
   ```
2. Leave the body prose alone. Duplication between prose and frontmatter is acceptable here and gets cleaned up naturally as you touch each note — do not do a prose rewrite pass.
3. Record the vocabulary in `_meta/KOS.md`.

**Validation:** every `.md` under `01-university/year-3/` that describes an assignment has all four fields, and `status` is one of the four permitted values. Add this as a sixth check in `check.sh`.

**Rollback:** `git checkout 01-university/`

**Delegate to Sonnet:** yes, with review. It can read each note and propose the frontmatter; you confirm the dates, because a wrong `due` is worse than a missing one.

---

### Milestone 3 — Generate the tracker
**Objective:** the tracker updates itself. This is the milestone you actually asked for.

**Actions:**
1. Write `_meta/sync-tracker.sh` — reads frontmatter from all assignment notes, writes the Upcoming and Completed tables sorted by `due`.
2. Add `<!-- BEGIN GENERATED -->` / `<!-- END GENERATED -->` markers to `assignments-tracker.md` around the two tables only.
3. Add a `SessionStart` hook to `.claude/settings.json` that runs it.
4. Create `HOME.md` with its own generated block; point Obsidian's startup note at it.
5. Delete the Assignment Tracker Rule from `CLAUDE.md`.
6. Edit `~/.claude/hooks/vault-stop-reminder.sh` to drop the assignment-sync sentence. Keep the session-notes half.

**⚠️ The validation that blocks this milestone.** Your tracker holds rows that exist in no note:

- Upcoming: *"RTW Class — prep for Sep 10 presentation"*, *"In-class: Introduce + Summary Profile + Interview Q&A"*
- Completed: *"Unit 5: IKAIGI"*, *"Case Study 1 — Peer Eval deadline"*, *"Case Study 1 — Group Registration"*

And the mapping is not one-to-one in the other direction either: `os-case-study-1.md` and `os-case-study-1-2.md` produce **three** tracker rows between them.

A script that regenerates the whole table therefore **deletes real data on first run.** So:

> **Run the script in dry-run and diff against the current tracker. If any row disappears, stop.**

The fix is the markers, not a cleverer script: generate only what is inside the fence, leave hand-written rows outside it, and accept that some rows will always be hand-written. Do not try to make every row derivable — that ends with you creating stub notes for a class session just to satisfy a script.

**Further validation:**
- Change a `status` in a note, start a new Claude session, confirm the tracker reflects it.
- Edit a note in Obsidian, start a session, confirm the same.
- Confirm hand-written rows outside the markers survive three consecutive runs.

**Rollback:** `git checkout 01-university/assignments-tracker.md` and remove the hook block from `.claude/settings.json`.

---

### Milestone 4 — Delete `03-ai/`
**Objective:** remove the one broken category.

**Actions:**
1. `03-ai/projects/rome-pathfinding/session-state.md` → `01-university/year-3/ai/rome-pathfinding-log.md`; move `romania.json`, `rome-assignment.md`, `rome-conversation.md` alongside.
2. `03-ai/projects/casestudy01-os/session-state.md` → `01-university/year-3/os/casestudy01-log.md`
3. `03-ai/projects/modular-synth/session-state.md` → `01-university/year-3/mcu/mcu-stm32-log.md`
4. `03-ai/projects/drunkbill/session-state.md` → `02-programming/projects/drunkbill-log.md`
5. Remove the empty `03-ai/`.
6. Update the header link in each log to point at its reference note; update `_meta/KOS.md`.

**Note on `04-archive/agoda-internship/`:** leave it completely alone. **Do not normalize it.** Archive is read-only, and reorganizing a closed chapter is pure churn against material you will never edit again.

*(Correction to the first draft of this document: I described this folder as using a `NN Name/` scheme that violates the Part 5 naming rules. It does not — it was flattened to kebab-case (`daily-notes/`, `knowledge-base/`) when it was archived. Only `VAULT-GUIDE.md` still described the old scheme, which is one more instance of the same Part 0 drift.)*

**Validation:** `bash _meta/check.sh` → zero errors. Spot-check that each log's `[[wikilink]]` back to its reference note resolves.

**Rollback:** `git reset --hard HEAD` before committing.

---

### Milestone 5 — Adopt the context-block standard
**Objective:** every project and assignment note opens with the Part 7 context block.

**Actions:**
1. Create `_meta/templates/assignment.md` and `_meta/templates/project.md`.
2. Enable the core Templates plugin, pointed at `_meta/templates/`.
3. Add the context block to the top of each active project and assignment note.
4. Move the constraints currently living only in Claude memory into the notes — the Rome heuristic ban is the clearest example, and today it is invisible to any session that does not load that memory.

**Validation:** the cold-start test. Start a fresh Claude session, give it one note, ask what the next action is. A correct answer with no follow-up means the block works; a follow-up question tells you exactly what is missing.

**Rollback:** per-file `git checkout`.

**This is where the AI cost savings actually land.** Milestones 0–4 are structure and automation; this is the one that changes what a session costs.

---

### Milestone 6 — Extract code repositories
**Objective:** the Part 8 separation.

**Actions:**
1. `mkdir ~/Code`
2. Move `drunkbill`, `timetable-website`, `nacl-nextpath-x`, `nacl-website`, `nacl-camellya` out of `~/Documents/University/`.
3. Update every `**File:**` pointer in the vault that referenced them.
4. Update the `university-files/` symlink references.

**Validation:** each repo opens in VS Code and `git status` works. `bash _meta/check.sh` → zero errors. No vault note points at a moved path.

**Rollback:** move the folders back. Git history travels with them, so nothing is at risk.

**Do this after `check.sh` exists** so path breakage is detected rather than discovered months later.

---

### Milestone 7 — Retire the old governing documents
**Objective:** one governing document, as designed.

**Actions:**
1. Confirm `_meta/KOS.md` contains everything still true from `VAULT-GUIDE.md` and `BRIDGE.md`.
2. Delete both.
3. Reduce root `CLAUDE.md` to a pointer at `_meta/CLAUDE.md`.

**Validation:** `bash _meta/check.sh` → zero errors. Nothing in the vault links to the deleted files.

**Rollback:** `git checkout` restores them.

**Last, deliberately.** Deleting the old map before the new one is proven leaves you with no map at all.

---

### What to delegate to Sonnet

| Milestone | Delegate? | Why |
|---|---|---|
| M0 reconcile docs | ✅ Yes | Mechanical, verifiable |
| M1 `_meta/` + checker | ✅ Yes | Scripting — Sonnet is good at this |
| M2 normalize frontmatter | ⚠️ Draft, you confirm dates | A wrong `due` is worse than a missing one |
| M3 sync script + hook | ✅ Yes | Scripting. **You run the dry-run diff yourself** before it writes |
| M4 delete `03-ai/` | ⚠️ With approval per move | Four file moves; approve each |
| M5 context blocks | ✅ Yes, draft only | Sonnet drafts What/Where/Stack, you write the *why* |
| M6 code extraction | ⚠️ With approval | Touches repos |
| M7 retire old docs | ✅ Yes | Mechanical after validation |

Two specifics. **M3:** Sonnet can write the script, but you personally run the dry-run and confirm zero rows vanish — that is a data-loss check and it should not be delegated to the thing that wrote the code. **M5:** Sonnet can extract What, Where, and Stack from what already exists. It cannot know why you chose one approach over another, and that is the most valuable line in the note.

---

## Summary of Recommendations Against Your Original Brief

| In the brief | I recommend | Why |
|---|---|---|
| Four governing docs, fixed read order | **One** — `_meta/CLAUDE.md` | Two copies of `06-nacl-kmitl/` were both stale. One copy needs no discipline |
| Nine files per project | **One README**, sections promote to files | 270 mostly-empty files makes starting a project feel like paperwork |
| Notion keeps operational state | **Drop Notion; one app** | Your call, and correct at this scale — the separation was solving a problem you do not have |
| Tracker synced by a rule | **Tracker generated from frontmatter** | You cannot forget a step that does not exist |
| "Never put work files in the vault" | **Inputs stay, outputs leave** | Already violated on disk; the old line was drawn by file type instead of role |
| `03-ai/` as a top-level folder | **Delete the category** | Categorizing by tool; will match everything within two years |
| (unstated) plugins for power | **Refuse Dataview and Bases** | Rendered-only content is invisible to Claude and to every other tool |
| Governance by written rules | **Governance by `check.sh`** | Your existing rules were correct and went stale anyway |

### The one thing I would still argue for

Deferring the top-level restructure is your call and I have implemented it. But note what you are choosing: at graduation, retiring `01-university/` will be a restructure rather than a single move, because university material is entangled with `02-programming/` and (until M4) `03-ai/`. M4 reduces that entanglement significantly, which is most of why it is worth doing on its own.

Set yourself a trigger rather than a plan: **when you graduate, or when the vault passes ~1,000 notes, reread Part 2.** The diagnosis will still be true and the move will still be cheap.

---

*Companion document: `KOS-MANUAL.md` — Parts 9, 10, 11, 14.*
