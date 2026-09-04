#!/usr/bin/env python3
"""Regenerate the assignment tracker and HOME dashboard from note frontmatter.

The note is the source of truth. This script only ever writes between
  <!-- BEGIN GENERATED: name -->  ...  <!-- END GENERATED: name -->
markers. Everything outside a marker block is left byte-for-byte alone, which
is what lets hand-written rows (class sessions, peer evals — things with no
backing note) coexist with generated ones.

Usage:
    python3 _meta/sync-tracker.py --check   # diff only, writes nothing
    python3 _meta/sync-tracker.py           # write

Exit codes: 0 no change or written, 1 changes pending (--check), 2 error.
"""

import re
import sys
import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACKER = ROOT / "01-university/assignments-tracker.md"
HOME = ROOT / "HOME.md"
SKIP_DIRS = {".git", ".obsidian", "node_modules", "04-archive", "_meta"}

DONE = {"submitted"}
LIVE = {"active", "draft"}
ICON = {"active": "🔄", "draft": "🔄", "submitted": "✅"}


def frontmatter(path):
    """Return the note's frontmatter as a dict, or None if it has none."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if km:
            out[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return out


def assignments():
    """Every note carrying a due: field."""
    found = []
    for p in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        fm = frontmatter(p)
        if not fm or not fm.get("due"):
            continue
        found.append(
            {
                "note": p.stem,
                "title": fm.get("title", p.stem),
                "due": fm["due"],
                "points": fm.get("points", "—"),
                "subject": fm.get("subject", "—"),
                "status": fm.get("status", "active"),
            }
        )
    return found


def sort_key(a):
    """TBA sorts last: it is a real state, not a missing value."""
    return (1, "") if a["due"] == "TBA" else (0, a["due"])


def table(rows):
    if not rows:
        return "_None._"
    out = [
        "| Due | Assignment | Subject | Points | Status |",
        "| --- | ---------- | ------- | ------ | ------ |",
    ]
    for a in rows:
        icon = ICON.get(a["status"], "⬜")
        out.append(
            f"| {a['due']} | [[{a['note']}\\|{a['title']}]] | {a['subject']} "
            f"| {a['points']} | {icon} {a['status']} |"
        )
    return "\n".join(out)


def upcoming_block(rows, limit=None):
    live = sorted([a for a in rows if a["status"] in LIVE], key=sort_key)
    return table(live[:limit] if limit else live)


def completed_block(rows):
    done = sorted([a for a in rows if a["status"] in DONE], key=sort_key, reverse=True)
    return table(done)


def replace_block(text, name, body):
    """Swap the contents of one marker block. Raises if the block is absent."""
    begin = f"<!-- BEGIN GENERATED: {name} -->"
    end = f"<!-- END GENERATED: {name} -->"
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise KeyError(f"marker block '{name}' not found")
    stamp = datetime.date.today().isoformat()
    new = (
        f"{begin}\n<!-- regenerated {stamp} — do not edit by hand -->\n\n"
        f"{body}\n\n{end}"
    )
    return pattern.sub(lambda _: new, text)


def apply(path, blocks):
    """Return (old, new) for a file after substituting every named block."""
    old = path.read_text(encoding="utf-8")
    new = old
    for name, body in blocks.items():
        new = replace_block(new, name, body)
    return old, new


def main():
    check = "--check" in sys.argv
    rows = assignments()
    if not rows:
        print("no assignment notes found — refusing to write", file=sys.stderr)
        return 2

    targets = [
        (TRACKER, {"upcoming": upcoming_block(rows),
                   "completed": completed_block(rows)}),
    ]
    if HOME.exists():
        targets.append((HOME, {"due-next": upcoming_block(rows, limit=5)}))

    changed = False
    for path, blocks in targets:
        if not path.exists():
            print(f"missing: {path}", file=sys.stderr)
            return 2
        try:
            old, new = apply(path, blocks)
        except KeyError as e:
            print(f"{path.name}: {e}", file=sys.stderr)
            return 2
        if old == new:
            print(f"  unchanged  {path.relative_to(ROOT)}")
            continue
        changed = True
        if check:
            print(f"  WOULD EDIT {path.relative_to(ROOT)}")
        else:
            path.write_text(new, encoding="utf-8")
            print(f"  written    {path.relative_to(ROOT)}")

    live = len([a for a in rows if a["status"] in LIVE])
    done = len([a for a in rows if a["status"] in DONE])
    print(f"  {len(rows)} assignment notes — {live} live, {done} done")
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
