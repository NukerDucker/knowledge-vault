---
inclusion: always
---

# Vault rules

Same rules as Claude. Read `_meta/CLAUDE.md` — under 100 lines, the whole read
order. Everything else is reference; do not load it unless asked.

## Three rules worth repeating

**File change authority.** Propose, then wait. Do not create, rename, move, or
delete any file without explicit approval for that specific change. Reading is
always fine.

**Never hand-edit the tracker.** `01-university/assignments-tracker.md` is
generated. Edit the assignment note's `status:` / `due:` / `points:` instead.
Rows outside the `GENERATED` markers are hand-maintained; leave them alone.

**Archiving is two steps.** Move to `04-archive/`, then sweep every reference to
the old location. Skipping step 2 is what broke this vault's docs in August 2026.
