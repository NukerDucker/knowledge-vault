# CLAUDE.md

An Obsidian knowledge vault. No build system, no tests, no CI. Markdown with
YAML frontmatter.

## Read this instead

**→ `_meta/CLAUDE.md`** — the rules, under 100 lines. That is the whole read order.

Everything else is reference. Do not load it unless asked:

| File | What |
|---|---|
| `_meta/KOS.md` | the governing document — folders, naming, governance |
| `_meta/check.sh` | governance checker. `bash _meta/check.sh` |
| `_meta/sync-tracker.py` | regenerates the tracker and `HOME.md` from frontmatter |
| `_meta/templates/` | note templates |
| `KOS-ARCHITECTURE.md` | why the system is shaped this way |
| `KOS-MANUAL.md` | how to operate it |
| `HOME.md` | dashboard — what is due |

## The three rules worth repeating here

**File change authority.** Propose, then wait. Do not create, rename, move, or
delete any file without explicit approval for that specific change. Reading is
always fine.

**Never hand-edit the tracker.** `01-university/assignments-tracker.md` is
generated. Edit the assignment note's `status:` / `due:` / `points:` instead —
that is the entire action. Rows outside the `GENERATED` markers are
hand-maintained; leave them alone.

**Archiving is two steps.** Move to `04-archive/`, then sweep every reference to
the old location. Skipping step 2 is what broke this vault's docs in August 2026.

---

*`VAULT-GUIDE.md` and `BRIDGE.md` were retired 2026-08-26 — their content lives
in `_meta/KOS.md`. One copy of a rule needs no discipline; two copies need it
forever.*
