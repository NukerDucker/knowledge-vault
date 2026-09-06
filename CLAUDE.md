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

<!-- FABLIZE:BEGIN — run Opus like Fable (always-on router). Verified procedures only. Install/update: fablize setup.sh -->
## Operating mode (always on — auto-route by task signal)

Apply what the task signals; with no signal, baseline only. Read each pack only when needed. Routing: smallest matching discipline only, overlap only when genuinely multi-category, mimic observable behavior only.

- **[always]** Lead with the outcome · stay within the requested scope (no incidental refactors) · ground completion claims in this session's tool results · confirm before destructive or hard-to-reverse actions.
- **[2+ sequential stories]** Run `python3 /Users/nukerducker/.claude/plugins/cache/fablize/fablize/2.1.1/scripts/goals.py`: create → next → checkpoint (with evidence) → final verification gate (no completion without `--verify-cmd` and `--verify-evidence`). Run from the repo root; state in `./.fablize/` (resume with `status`). Skip for single-step tasks.
- **[debugging / test failure / unknown cause / review]** Follow `/Users/nukerducker/.claude/plugins/cache/fablize/fablize/2.1.1/packs/investigation-protocol.txt`: reproduce first → 3+ competing hypotheses → evidence per hypothesis → full causal chain → verify before/after → report rejected hypotheses.
- **[render/executable artifact: HTML, SVG, game, UI, chart]** Follow `/Users/nukerducker/.claude/plugins/cache/fablize/fablize/2.1.1/packs/verification-grounding-pack.txt` grounding loop: run it in the real renderer → observe the output → fix what you see → re-run. A static check is not observation.
- **[hard or ambiguous task]** Adaptive thinking scales with difficulty automatically. To go higher, recommend `/effort xhigh` to the user. Depth (capability) cannot be raised: if stuck 2+ times or out-of-spec discovery is needed, report the limit honestly and escalate.
<!-- FABLIZE:END -->
