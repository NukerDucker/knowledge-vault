---
title: Knowledge Operating System — User Manual
tags: [meta, kos, manual]
status: draft
created: 2026-08-25
---

# Knowledge Operating System — User Manual

Parts 9, 10, 11, 14. Companion to `KOS-ARCHITECTURE.md` (Parts 1–8, 12, 13).

**This document assumes you have forgotten everything**, because in six months you will have. Keep it in the vault — it is the one file that explains the others.

**Read this first if you are returning after a break:** skip to *Part 14 → Onboarding Guide for Future You*. It is six short paragraphs and will get you working again in five minutes.

---

## Part 9 — Learning Roadmap

### What this teaches, and what it deliberately does not

Obsidian has hundreds of features. You need about eight. VS Code has thousands. You need about six. Everything below exists because the system in `KOS-ARCHITECTURE.md` requires it — nothing is here because it is a neat feature.

Your stated level has a useful contradiction in it: intermediate with the applications, but new to Markdown, plugins, and Git. That is a common and specific profile — comfortable navigating a GUI, not yet comfortable with the mechanics underneath. So the stages below move quickly through interface navigation and slowly through the mechanical parts, which is the opposite of most tutorials.

Five stages. Each takes an evening. **Do not skip ahead** — each one uses what the previous built.

---

### Stage 1 — Markdown, and only the parts you need
*One evening. The foundation for everything else.*

**What to learn**

Six pieces of syntax. This is genuinely the complete list for this system:

```markdown
# Heading 1
## Heading 2

**bold**

- bullet
- bullet

- [ ] unchecked task
- [x] checked task

[[link-to-another-note]]

| column | column |
|--------|--------|
| cell   | cell   |
```

Plus frontmatter — the block at the very top of a file, between three-dash lines:

```yaml
---
title: My Note
tags: [university]
status: active
---
```

**Why it matters**

Markdown is why this system will still work in 2036. It is plain text. Every editor ever written can open it. No company can discontinue it, change its pricing, or lock your notes behind a subscription. This is the single most important property of the whole design, and it costs you one evening of learning.

Frontmatter matters specifically because it is the part machines read. Obsidian uses it for search. `check.sh` validates it. Claude uses `status` to know whether a note is live.

**Hands-on, with your own files**

1. Open `01-university/year-3/uxui/uxui-ui-hunt.md` in Obsidian.
2. Toggle between edit and preview mode (`Cmd+E`). Watch how the raw text becomes formatted.
3. Find the frontmatter at the top. Find a `[[wikilink]]`. Find a table.
4. Create a new note. Type the six pieces of syntax above. Preview it.
5. Delete the note. It was practice.

**Common mistakes**

- **Frontmatter not at the very top.** It must be line 1. One blank line above it and it becomes literal text.
- **Using `*` for bullets sometimes and `-` other times.** Both work; pick `-` and never think about it again.
- **Spaces in filenames.** They break shell commands, URLs, and scripts. Hyphens only.

**Expected outcome:** you can read any note in your vault as raw text and know what it will look like rendered.

---

### Stage 2 — Obsidian as a tool, not a hobby
*One evening.*

**What to learn**

Five things:

1. **Quick switcher** — `Cmd+O`. Type part of a filename, hit enter. **This is how you open notes.** Not the sidebar.
2. **Search** — `Cmd+Shift+F`. Full-text across the vault.
3. **Wikilinks** — type `[[`, start typing, pick from the list. Obsidian creates the link and keeps it working when files move.
4. **Backlinks panel** — shows every note linking *to* the current one. This is the feature that makes a vault more than a folder.
5. **Templates** (core plugin) — insert a pre-written structure into a new note.

**Why it matters**

The habit shift here is the whole point of the stage: **stop navigating by folder.** Folders are for archiving (Architecture Part 2). Retrieval is `Cmd+O` and `Cmd+Shift+F`. Once that clicks, the folder structure stops mattering day-to-day, which is exactly why it can afford to be as simple as it is.

Backlinks are the compounding mechanism. When you open a note in two years and see six other notes linking to it, you have context you never deliberately created.

**Hands-on**

1. `Cmd+O`, type `ui-hunt`, enter. Time yourself — under two seconds.
2. `Cmd+Shift+F`, search `Kano`. See every note mentioning it.
3. Open `assignments-tracker.md`. Look at the backlinks panel (right sidebar). Those are your assignment notes finding their hub automatically.
4. In any note, type `[[` and link to another real note. Follow it. Come back. Check the backlinks panel on the target — your new link is there.
5. Settings → Core plugins → enable **Templates**. Set the folder to `_meta/templates` (the setting can point at a folder that does not exist yet).

**Common mistakes**

- **Living in the file explorer sidebar.** It is a comfort habit and it stops scaling around 200 notes.
- **Making links "for completeness."** Link when one note genuinely helps you understand another. A vault where everything links to everything carries the same information as one where nothing does.
- **Installing plugins to solve problems you have not hit yet.** See Part 10.

**Expected outcome:** you open notes without touching the sidebar, and you have linked two notes yourself.

---

### Stage 3 — Git, but only four commands
*One evening. The stage people skip and then regret.*

**What to learn**

Git is what makes deletion safe, and safe deletion is what keeps the vault from becoming a landfill. You need four commands and one concept.

**The concept:** git takes a snapshot of every file whenever you tell it to. Every snapshot is permanent. You can return to any of them. Nothing is ever really lost.

**The four commands** — run them in Terminal, from the vault folder:

```bash
git status                    # what changed since the last snapshot
git add -A                    # stage everything for the next snapshot
git commit -m "what I did"    # take the snapshot
git log --oneline             # list past snapshots
```

And the one you will need in an emergency:

```bash
git checkout <filename>       # undo all changes to that file since the last snapshot
```

**Why it matters**

The deletion rules in the architecture tell you to delete freely — superseded drafts, stale captures, entire folders you have not opened in a year. That advice is only reasonable because git makes it reversible. Without git you will hoard, and a hoarded vault stops being searchable.

Obsidian Git (already installed) commits automatically on a timer, so you get this benefit without doing anything. But you need to understand what it is doing, because the day something goes wrong, the automatic tool will not help you and the four commands will.

**Hands-on**

1. Open Terminal. Type `cd ~/KnowledgeVault`, enter.
2. `git status` — see what has changed.
3. `git log --oneline` — see your existing commits. Each one is a restorable snapshot.
4. Now the important exercise, and do it exactly: **delete a note you do not care about.** Then `git status` (it shows as deleted), then `git checkout <filename>`, then look — the file is back.
5. Make a small edit somewhere, then `git add -A` and `git commit -m "practice commit"`.

Step 4 is the whole stage. Do it until deleting something stops feeling risky, because that feeling is what the rest of the system depends on.

**Common mistakes**

- **Committing with a message like "update".** Six months later `git log` is a wall of "update" and useless. Write what changed.
- **Fearing `git checkout`.** It only discards *uncommitted* changes. Anything committed is safe forever.
- **Trying to learn branching, merging, or rebasing.** You will not need them for a personal vault. Ever.

**Expected outcome:** you have deleted a file and restored it. Deletion no longer feels dangerous.

---

### Stage 4 — VS Code for the four things it is for
*One evening.*

**What to learn**

1. **Open a folder** — `File → Open Folder`. One repo per window.
2. **Quick open** — `Cmd+P`, type a filename. The same muscle as Obsidian's `Cmd+O`.
3. **Search across files** — `Cmd+Shift+F`.
4. **Integrated terminal** — `` Ctrl+` ``. This is where your four git commands live.
5. **Source Control panel** — the branch icon in the left bar. Visual `git status` and `git commit`.
6. **The command palette** — `Cmd+Shift+P`. Every feature by name. When you do not know how to do something, this is where you look, and it means you never need to memorize menus.

**Why it matters**

VS Code is your *code* workspace, per Architecture Part 8. It is not a second Markdown editor — Obsidian handles notes, VS Code handles repos. Keeping that boundary is what stops your notes and your code from bleeding into each other.

The Source Control panel is worth learning specifically because it shows you the diff before you commit. Seeing exactly what changed before you record it is a habit that prevents a whole class of mistakes.

**Hands-on**

1. Open VS Code. `File → Open Folder` → `~/Documents/University/drunkbill`.
2. `Cmd+P`, type part of a filename. Open it.
3. `` Ctrl+` `` to open the terminal. Type `git status`.
4. Click the Source Control icon. Compare what it shows against the terminal output — it is the same information.
5. `Cmd+Shift+P`, type "theme", change your color theme. That is the palette working.

**Common mistakes**

- **Opening `~/Documents/University/` as a folder.** 47,373 files. Search becomes useless and the window takes forever to index. Open one repo.
- **Editing vault notes in VS Code.** Wikilinks do not resolve, the backlinks panel does not exist, and you lose the reason Obsidian is in the stack.
- **Installing twenty extensions on day one.** See Part 10.

**Expected outcome:** you open one repo, find a file, and run `git status` inside VS Code.

---

### Stage 5 — Running the system
*Ongoing. This is where it becomes habit rather than knowledge.*

**What to learn**

The three loops:

- Weekly: 10 minutes, inbox to zero.
- Monthly: 30 minutes, run `check.sh`, archive finished projects.
- Yearly: 2 hours, reread the governing doc, retire an area.

Plus the two-second filing test — the only thing you use every single day:

1. Binary file? → Files
2. Changes with code? → Beside the code
3. Want it in six months? → Obsidian
4. None? → Delete

**Why it matters**

Everything until now was design. This is operation. A well-designed system with no maintenance loop decays exactly like a badly-designed one, just more slowly — and your `VAULT-GUIDE.md` is the proof, because it was well designed and went stale in two weeks anyway.

**Hands-on**

1. Do one full weekly review this week. Time it. If it takes more than fifteen minutes, something is wrong with the system rather than with you — write down what took the time.
2. After Phase 1, run `bash _meta/check.sh` and fix whatever it reports.
3. At the end of one real work session, ask: *did anything here change how I think or work?* If yes, write one line in the project's Decisions section. If no, skip it — a forced reflection is worth nothing.

**Common mistakes**

- **Skipping the weekly review twice, then abandoning it.** Missing one is fine. The recovery move is to do a ten-minute version, not a catch-up marathon.
- **Reorganizing instead of reviewing.** The review is for filing and archiving. Restructuring is a yearly activity, and doing it monthly means the structure is never stable enough to trust.

**Expected outcome:** you have run one weekly review and one monthly review, and the inbox has been empty at least once.

---

## Part 10 — Plugins and Extensions

The governing rule: **every plugin is a dependency that can break, get abandoned, or change behavior in an update.** A plugin has to earn that risk. Most do not.

### Obsidian — the complete list

| Plugin | Status | Why | When you use it | Downside |
|---|---|---|---|---|
| **Templates** (core) | **Essential** | Makes project structure automatic instead of remembered | Every new project or note | None — ships with Obsidian |
| **Obsidian Git** (community) | **Essential** — installed | Automatic backup and undo. The safety net the deletion rules depend on | Continuously, in the background | Needs git installed; occasional auth prompts |
| **Backlinks** (core) | **Essential** | Shows what links here. The compounding mechanism | Every time you open an old note | None |
| **Quick switcher** (core) | **Essential** | `Cmd+O`. How you open notes | Constantly | None |
| **Search** (core) | **Essential** | Full-text. How you find things | Constantly | None |
| **Outline** (core) | Optional | Heading navigation in long notes | Notes over 1,000 words | None |
| **Kanban** (community) | **Remove** — installed | Board view of tasks | You do not use it | Stores boards in a bespoke Markdown format other tools cannot read |
| **Obsidian Bases** | **Do not use** | — | — | Same flaw as Dataview: the view is computed at render time and does not exist in the file |
| **LaTeX Suite** (community) | Keep if you use it | Math notation shortcuts | Only if you write equations | None if you actually use it; dead weight otherwise |
| **Dataview** | **Do not install** | — | — | Content exists only at render time — invisible to Claude, invisible to every other editor, and a hard dependency on one plugin. See Architecture Part 7 |
| **Templater** | **Do not install** | — | — | More powerful than core Templates and needs a scripting language you would have to learn and maintain |

**Four core plugins, two community plugins.** That is the whole recommendation.

**On Kanban:** you have it installed and there is no board in the vault. It is a good plugin doing nothing, and its boards store data in a format only it can read — so if you ever do start one, you have quietly acquired a dependency. Remove it. Your "what's next" view is `HOME.md`, which is plain Markdown and generated.

**On Dataview and Bases together:** both compute their output when you look at the page. Neither writes anything into the file. That is exactly why the tracker is generated by a *script* instead — the script writes real Markdown rows that live in the file, so Claude reads the same table you do, and so does GitHub, and so does whatever editor you use in 2036.

**On LaTeX Suite:** genuinely useful for equation-heavy notes, useless otherwise. You installed it; only you know which. If you have not used it in three months, remove it.

### VS Code — the complete list

| Extension | Status | Why | Downside |
|---|---|---|---|
| **GitLens** | Recommended | Shows who changed each line and when, inline. Makes git legible while you are learning it | Verbose by default — turn off inline blame if it is noisy |
| **Prettier** | Recommended | Auto-formats code on save. Ends all formatting decisions permanently | Occasionally fights a project with its own config |
| **ESLint** | If you write JS/TS | Catches errors as you type | Needs project-level config |
| **Language pack for what you write** | As needed | Python, Rust, Go — install when you write that language | None |
| **Live Server** | If you write HTML | Auto-refreshing local preview | None |
| **Themes and icon packs** | Free | Pure preference, zero risk | None |

**Deliberately not recommended:** AI autocomplete extensions. You have Claude Code, which fits how you work better, and running both means two AI systems with different context making different assumptions in the same file.

### The rule for anything you find later

> **Install a plugin only after you have hit the problem it solves at least three times.**

Not once — three times. Once is a novelty. Three times is a pattern, and by then you will know exactly what you need it to do, which means you will pick the right plugin instead of the most popular one.

---

## Part 11 — Migration Strategy

Seven phases, mapping to the milestones in Architecture Part 13. **Each phase leaves the system working.** You can stop after any phase and be better off than before it.

### The sequencing principle

The order is not arbitrary and it is not negotiable. Each phase builds the thing the next phase needs to be verified:

```
Phase 0  fix the map              ─┐
Phase 1  build the map-checker     ├─ truth before automation
Phase 2  normalize frontmatter    ─┘
Phase 3  generate the tracker      ← the "never ask me again" phase
Phase 4  delete 03-ai/
Phase 5  add context blocks        ← the AI savings land here
Phase 6  separate code
Phase 7  delete the old map
```

Phases 2 and 3 are the ones you actually asked for. Phases 0 and 1 exist because a generator built on inconsistent data quietly produces wrong output, and you would not notice for weeks.

Restructuring before you can verify structure is how you end up with a clean-looking vault full of broken links you find eight months later.

### Phase 0 — Fix the map *(20 minutes)*

**Value on its own:** your governing documents stop lying to you. Worth an evening even if you do nothing else, because right now they will send you to three folders that do not exist.

**Do:** Milestone 0 — correct the stale paths in `VAULT-GUIDE.md` and `BRIDGE.md`, decide where `slide-06-lp-diagram.html` goes.
**Validate:** open `VAULT-GUIDE.md`, check every path it names actually exists.
**Stop here if:** you want to test whether the rest is worth it. This phase is complete on its own.

### Phase 1 — Build the checker *(1 evening)*

**Value on its own:** you gain the ability to detect drift automatically, forever. This phase changes the long-term outcome more than any other.

**Do:** Milestone 1. Create `_meta/`, write `KOS.md`, `CLAUDE.md`, and `check.sh`.
**Validate:** `bash _meta/check.sh` runs clean against your *current, unchanged* structure.
**Critical:** if the checker reports errors on the current vault that you know are false, fix the checker before moving on. A checker you learn to ignore is worse than none.

### Phase 2 — Normalize frontmatter *(1–2 hours)*

**Value on its own:** every assignment note states its own due date, points, and status in a fixed place. Even with no script, you can search and sort by them.

**Do:** Milestone 2. Add `due`, `points`, `subject`, `status` to every assignment note.
**Validate:** `check.sh` gains a sixth check — every assignment note has all four fields, and `status` is one of `active | submitted | graded | archived`.
**Delegate:** Sonnet drafts; **you confirm the dates.** A wrong `due` is worse than a missing one.

### Phase 3 — Generate the tracker *(1 evening)*

**Value on its own:** **this is the phase you asked for.** The tracker updates itself; you never sync anything again.

**Do:** Milestone 3. Write `sync-tracker.sh`, add the `<!-- BEGIN GENERATED -->` markers, wire the `SessionStart` hook, create `HOME.md`, delete the sync rule from `CLAUDE.md`, trim the `Stop` hook reminder.

**⚠️ Validate this one carefully — it can delete data.** Your tracker has rows with no backing note (*"Unit 5: IKAIGI"*, *"RTW Class — prep for Sep 10"*, *"Case Study 1 — Group Registration"*), and `os-case-study-1.md` + `os-case-study-1-2.md` produce three rows between them. A naive regenerate destroys those.

> **Run the script in dry-run first and diff against the current tracker. If any row disappears, stop and fix the markers before letting it write.**

Then: change a `status`, start a new session, confirm the table updated. Edit a note in Obsidian, start a session, confirm the same. Run three times and confirm hand-written rows outside the markers survive.

**Rollback:** `git checkout 01-university/assignments-tracker.md`, remove the hook block from `.claude/settings.json`.

### Phase 4 — Delete `03-ai/` *(30 minutes)*

**Value on its own:** the one broken folder is gone, and each project's log sits next to the note it belongs to.

**Do:** Milestone 4 — four file moves.
**Validate:** `check.sh` clean; each log links back to its reference note.
**Leave `04-archive/agoda-internship/` completely alone.**

### Phase 5 — Context blocks *(1 evening, then ongoing)*

**Value on its own:** **this is where AI cost drops.** Everything before was structure and automation; this is the phase you feel in every session.

**Do:** Milestone 5.
**Validate:** the cold-start test. New Claude session, hand it one note, ask "what's the next action?" A correct answer with no follow-up means the block works.
**Ongoing:** every new project gets its block on day one. Not later — day one, or it never happens.

### Phase 6 — Separate code *(2 hours)*

**Value on its own:** VS Code gets fast, and your code survives graduation.

**Do:** Milestone 6.
**Validate:** each repo opens and `git status` works. `check.sh` clean. No vault note points at a moved path.

### Phase 7 — Retire the old documents *(30 minutes)*

**Value on its own:** one governing document. The duplication that caused the original drift is structurally gone.

**Do:** Milestone 7.
**Validate:** `check.sh` clean, nothing links to the deleted files.

### If you only do part of it

| Time available | Do | You get |
|---|---|---|
| One evening | Phase 0 + 1 | Honest documents and automated drift detection |
| One weekend | Phases 0–3 | **Plus the self-updating tracker — your actual ask** |
| Two weekends | Phases 0–5 | Plus a clean folder tree and much cheaper AI sessions |
| Everything | Phases 0–7 | The full system |

**If you only have a weekend, do 0 through 3.** That is the whole "never make me ask again" outcome. Phases 4–7 are cleanup and can wait indefinitely.

---

## Part 14 — User Manual

*Everything below is written to be read cold, with no memory of this conversation.*

---

### Installation

**What you need**

| Tool | Purpose | Cost |
|---|---|---|
| Obsidian | Read and write notes | Free |
| Git | Backup and undo | Free, comes with macOS |
| VS Code | Write code | Free |
| Claude Code | Reasoning layer | Claude Pro |

**Setup, once**

1. Install Obsidian from obsidian.md.
2. Open Obsidian → "Open folder as vault" → select `~/KnowledgeVault`.
3. Verify git works: open Terminal, `cd ~/KnowledgeVault`, `git status`. If it prints a status, you are done.
4. Install VS Code from code.visualstudio.com.
5. In Obsidian, Settings → Core plugins → enable **Templates**, set the template folder to `_meta/templates`.
6. Open `HOME.md`, bookmark it, and pin its tab. Obsidian reopens the tabs you
   left open, so a pinned `HOME` tab is what makes it your landing page — there
   is no core "startup note" setting.

**Verify the whole setup**

```bash
cd ~/KnowledgeVault
git status              # prints a status
bash _meta/check.sh     # prints zero errors
```

If both work, the system is live.

---

### The folders, and what each one means

| Folder | Holds | Filing question | Retires when |
|---|---|---|---|
| `_meta/` | The rules, templates, `check.sh` | *Is this about the vault itself?* | Never |
| `00-inbox/` | Things you have not decided about | *Do I not know yet?* | Emptied weekly |
| `01-university/` | All coursework, by year and subject | *Is this for a class?* | You graduate |
| `02-programming/` | Dev guides and personal project notes | *Is this code-related and not coursework?* | Per project |
| `04-archive/` | Finished, superseded, retired | *Is this done?* | It is the end state |
| `HOME.md` | Your dashboard — what's due, subject links | — | Never |

**The one thing to remember:** folders mean *when does this die*, not *what is this about*. Topic lives in tags and links.

**Archive is read-only.** If something in `04-archive/` needs editing, it is not archived — move it out first.

**There is no `03-ai/`** — it was deleted in Phase 4. Session logs live as `<project>-log.md` next to the note they belong to.

---

### Naming rules

**Default, covering roughly 95% of cases:**

```
kebab-case-descriptive-name.md
```

Lowercase. Hyphens. Words you would type into search.

**Three exceptions:**

1. **Dates** — only when the note *is* an event: `2026-08-25-standup.md`. Never on a topic.
2. **Version numbers** — never in the vault (git holds versions). Only on exported files: `67011178_Report1_v2.pdf`.
3. **Received PDFs** — keep the original filename so you can match it to its source.

**When you hesitate:** lowercase, hyphens, describe the thing, no date, no version.

---

### Daily workflow

**When something new appears** — run the two-second test:

1. Binary file (PDF, image, deck)? → **Files** (`~/Documents/`)
2. Changes whenever the code changes? → **Beside the code** (`~/Code/<repo>/`)
3. Want to reread it in six months? → **Obsidian**
4. None of the above? → **Delete it.** Not the inbox. Delete.

There is no "does it have a deadline" branch. A deadline is a `due:` field on a note, not a category of thing.

**When you cannot decide:** `00-inbox/`. That is what it is for. But it gets resolved within two weeks or it gets deleted.

**When you start your day:** open `HOME.md`. What is due is already on screen — it regenerated when the last Claude session started.

**When you start work on something:**

```
Cmd+O → type the name → read the top of the note
```

**When an assignment's state changes** — you submit it, the due date moves, points are announced:

> **Edit the note's frontmatter. That is the entire action.**
> ```yaml
> status: submitted
> due: 2026-09-07
> points: 6
> ```
> The tracker and `HOME.md` regenerate on their own. Do not edit the tracker. Do not tell Claude to sync anything. There is no second step.

**When you work with Claude:**

```
✅  "Read 01-university/year-3/ai/rome-pathfinding.md. What's the next action?"
❌  "Look at my vault and tell me about <name>."
```

Name the file. Ask a specific question. This is roughly a fifty-fold cost difference and it produces better answers.

**When you finish a work session:**

Ask one question: *did anything here change how I think or work?*
- Yes → one line in the project's `## Decisions` section, with today's date.
- No → skip it. A forced reflection is worth nothing.

---

### Weekly maintenance — 10 minutes

Same day each week. Friday afternoon works well.

1. **Empty `00-inbox/` to zero.** Each item: file it or delete it. There is no third option. Anything older than two weeks: delete without reading.
2. **Mark finished work `stable`.** Any project that finished this week: change `status: active` to `status: stable` in its frontmatter.
3. **Commit.** `git add -A && git commit -m "weekly review"`

**Success:** inbox is empty.

**If you missed a week:** do the ten-minute version anyway. Do not attempt a catch-up marathon — that is how reviews get abandoned.

---

### Monthly review — 30 minutes

First weekend of the month.

1. **Run the checker.**
   ```bash
   cd ~/KnowledgeVault && bash _meta/check.sh
   ```
   Fix everything it reports. This is the single most valuable thirty minutes in the system.

2. **Archive finished projects.** Anything done for over a month:
   - Move the lessons to `02-programming/guides/lessons-<topic>.md` **first**
   - Move the project folder to `04-archive/`
   - **Search the vault for the old path and fix every reference.** This step is the one that gets skipped and it is the one that breaks things.

3. **Check repository size.**
   ```bash
   du -sh .git
   ```
   Under 2 GB: nothing to do. Over: stop committing frequently re-exported images.

4. **Commit.**

**Success:** `check.sh` reports zero errors.

---

### Yearly review — 2 hours

Pick a date. January works; so does your birthday.

1. **Read `_meta/KOS.md` end to end.** Does it describe the vault you actually have? Where it does not, decide which one is wrong — the document or the vault — and fix that one. Do not fix both; that is how you get two half-truths.
2. **Graduated, or past ~1,000 notes?** Reread Architecture Part 2. That is the trigger to do the deferred restructure — the diagnosis will still be true and the move will still be cheap.
3. **Delete a folder** of things you have not opened in a year. On purpose. This is what keeps a ten-year vault from becoming a museum.
4. **Review the tag list.** Merge anything used fewer than three times.
5. **Review plugins.** Anything unused in six months: remove it.

**Success:** the document matches the disk.

---

### Migration guide

If you are reading this before migrating, follow Part 11 in order. The short version:

| Phase | Time | Do | Validate |
|---|---|---|---|
| 0 | 20 min | Fix stale paths in `VAULT-GUIDE.md` / `BRIDGE.md` | Every named path exists |
| 1 | 1 evening | Create `_meta/`, `KOS.md`, `CLAUDE.md`, `check.sh` | `check.sh` clean on the *current* structure |
| 2 | 1–2 hr | Add `due`/`points`/`subject`/`status` to assignment notes | All four fields present; `status` from the fixed list |
| 3 | 1 evening | `sync-tracker.sh` + `SessionStart` hook + `HOME.md` | **Dry-run diff loses zero rows**, then round-trip test |
| 4 | 30 min | Delete `03-ai/`, logs become subject-folder siblings | `check.sh` clean, logs link back |
| 5 | 1 evening | Context blocks on active notes | Cold-start Claude test passes |
| 6 | 2 hr | Move repos to `~/Code/` | Each repo opens, `git status` works |
| 7 | 30 min | Delete `VAULT-GUIDE.md`, `BRIDGE.md` | Nothing links to them |

**Rules:** one phase per session. `git status` clean before starting. Phase 3's dry-run is not optional.

---

### Troubleshooting

**A `[[wikilink]]` is broken (shows as unresolved)**
The target was renamed, moved outside the vault, or deleted. `Cmd+Shift+F` the old name to find where it went. If it was deleted, remove the link — a link to nothing is worse than no link.

**`check.sh` reports errors after I moved things**
Expected. Fix them now while you remember what you moved. Every hour you wait makes them harder to diagnose.

**Obsidian is slow**
Almost always a plugin. Settings → Community plugins → disable all → restart → re-enable one at a time. It will be a plugin doing work on every keystroke.

**I cannot find a note**
`Cmd+Shift+F` and search the *content*, not the filename. You remember what you wrote, not what you named it. This works better than you expect and is why the folder structure can afford to be simple.

**Git says "nothing to commit" but I changed files**
You are in the wrong folder. `cd ~/KnowledgeVault` first.

**Git conflict after editing on two machines**
The file has both versions in it, marked with `<<<<<<<` and `>>>>>>>`. Open it, delete the markers and the version you do not want, save, commit. Not an emergency.

**I deleted something important**
```bash
git log --oneline              # find the commit before the deletion
git checkout <commit> -- <file>
```
Nothing committed is ever lost.

**Claude keeps misunderstanding my project**
The README is missing a constraint. Add the negative facts — what is *banned*, what was already tried and failed. Those prevent more wasted work than any amount of description.

**Claude sessions feel expensive**
You are pointing at folders instead of files. Name the specific file. See *Daily workflow*.

**I have not done a review in two months**
Do one ten-minute weekly review. Delete anything in the inbox older than two weeks without reading it. Then run `check.sh`. Do not attempt to catch up on eight weeks — the system is designed so that only the current state matters.

---

### FAQ

**Where does a note go if it fits two folders?**
The more permanent one. Ask: *would this still be worth reading if the project were cancelled?* Yes → `02-programming/guides/`. No → the subject folder it belongs to.

**The tracker looks wrong / out of date.**
Run `bash _meta/sync-tracker.sh`. It regenerates from the notes. If a row is still wrong, the *note's* frontmatter is wrong — fix it there, never in the tracker.

**Can I just edit the tracker directly?**
Only outside the `<!-- BEGIN GENERATED -->` markers. Anything inside gets overwritten on the next run. If you find yourself wanting to edit inside, the note's frontmatter is what actually needs changing.

**Why is there still a hand-written row in the tracker?**
Some things have no note — a class session, a peer-eval deadline. Those live outside the markers and are maintained by hand. That is intentional; the alternative is creating stub notes to satisfy a script.

**Why did we drop Notion?**
You wanted one app. At this size the split between "status" and "knowledge" was costing you a second place to look and a sync to remember, and buying very little. Revisit if you ever run a team from this vault.

**When do I make a new folder?**
Three conditions, all required: five-plus notes already exist for it, they will be archived together, and the name will make sense in five years.

**Should I delete or archive?**
Archive things you finished and might reference. Delete things that are superseded, duplicated, or were never important. Git makes deletion reversible, so lean toward deleting.

**Do I need `updated:` in frontmatter?**
Only on `status: active` notes. On stable notes it is date churn with no information.

**Can I edit vault notes in VS Code?**
You can, but wikilinks will not resolve and there is no backlinks panel. Use Obsidian for notes, VS Code for code.

**What if I stop using Obsidian?**
Every note is a plain `.md` file in a normal folder. Open it in anything. This is the entire reason for the design.

**Why not Dataview? Everyone uses it.**
Its results exist only inside Obsidian at render time. Claude reading the file sees a query, not data — so your index page is empty to every tool except one. It trades portability and AI readability for convenience, and those are two of your stated priorities.

**How do I know it is working?**
Three signs: the inbox is empty most weeks, `check.sh` reports zero errors, and you find old notes by searching rather than by remembering where you put them.

**How much time does this cost?**
About fifteen hours a year — ten minutes weekly, thirty monthly, two hours yearly. If it costs more, simplify the system rather than trying harder.

---

### Common mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Creating folders for one note | Feels tidy | Keep notes flat until five share a home |
| Making the folder tree deeper | Feels organized | Three levels maximum; search handles retrieval |
| Copying a fact into two notes | Convenience | Link instead. Two copies always drift |
| Skipping the de-reference step when archiving | Nobody remembers it | It is why `check.sh` exists — run it monthly |
| Writing "update" as a commit message | Faster | Six months later the log is useless |
| Pointing Claude at a folder | Feels thorough | Name the file. Fifty times cheaper |
| Installing a plugin to try it | Curiosity | Wait until you have hit the problem three times |
| Reorganizing during a weekly review | Restructuring feels productive | Review is for filing. Restructure yearly |
| Keeping every capture | Fear of losing something | Most captures are worthless. Delete at two weeks |
| Naming files with spaces or capitals | Habit from Word | Lowercase, hyphens, always |
| Dating a topic note | Feels like a record | Dates are for events. A dated topic note fragments your knowledge |

---

### Best practices

**The five that matter most:**

1. **Name the file when you talk to Claude.** Biggest single lever on cost and answer quality.
2. **Write down *why*, not *what*.** The what is visible in the code six months later. The why is gone.
3. **Delete freely.** Git makes it safe. A vault you are afraid to prune becomes a vault you stop trusting.
4. **One fact, one place.** When you see a duplicate, fix it immediately — the window where you know which copy is right is short.
5. **Run `check.sh` monthly.** It is the difference between a system and a set of good intentions.

**The habits underneath them:**

- Open notes with `Cmd+O`, never the sidebar.
- Every project gets a README on day one, not later.
- Lessons leave the project folder when the project ends.
- The inbox is emptied, not managed.
- Archive is read-only.

---

### Onboarding Guide for Future You

*Read this if you have been away for months and everything feels unfamiliar.*

**What this system is.** One app plus two things it cannot be. **Obsidian** — this vault — holds everything textual: what you know, what you decided, and what is due. **Code repos** hold how things work, because you cannot run code in a note editor. **Files** hold PDFs and slides, because binaries are not text. **Claude** holds nothing; it reads the others and reasons.

**How to find anything.** `Cmd+O` for a filename, `Cmd+Shift+F` for content. Do not browse folders — folders exist to archive things, not to find them.

**How to file anything.** Binary file → Documents. Changes with code → beside the code. Want it in six months → here. None of those → delete it.

**How to know what is due.** Open `HOME.md`. It is generated from the notes and refreshed whenever a Claude session starts. You never update it.

**When an assignment's state changes.** Edit that note's frontmatter — `status`, `due`, `points`. Nothing else. The tracker and `HOME.md` follow on their own. If you catch yourself editing the tracker, stop and edit the note instead.

**How to restart work on something.** `Cmd+O`, its name, read the top of the note. The first fifteen lines were written specifically so you would not have to reconstruct context — trust them.

**If it feels messy.** It is probably fine and you have just lost the thread. Run `bash _meta/check.sh`. If it reports zero errors, the system is intact and you only need to reread `_meta/KOS.md`. If it reports errors, fix them — they will be specific and mechanical, not conceptual.

**If you want to change something.** The design decisions and their reasoning are in `KOS-ARCHITECTURE.md`. Read the relevant part before changing a rule; most rules exist because a specific failure was observed, and the reasoning is written down so future-you can tell a considered decision from an arbitrary one. If the reasoning no longer holds, change the rule — and write down why, dated, so the next version of you gets the same courtesy.

---

*Companion document: `KOS-ARCHITECTURE.md` — Parts 1–8, 12, 13.*
