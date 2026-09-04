#!/usr/bin/env python3
"""Emit assignment due dates as an .ics calendar, from note frontmatter.

Same contract as sync-tracker.py: the note is the source of truth, this only
generates a derived view. Import _meta/assignments.ics once into Google
Calendar; re-running and re-importing updates events in place because each
event's UID is derived from the note filename.

Usage:
    python3 _meta/sync-calendar.py            # write _meta/assignments.ics
    python3 _meta/sync-calendar.py --check    # report only, writes nothing

Exit codes: 0 written/no change, 1 changes pending (--check), 2 error.
"""

import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICS = ROOT / "_meta/assignments.ics"
SKIP_DIRS = {".git", ".obsidian", "node_modules", "04-archive", "_meta"}
DONE = {"submitted"}


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


def due_notes():
    """Unsubmitted notes carrying a real (non-TBA) ISO due date."""
    found = []
    for p in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        fm = frontmatter(p)
        if not fm or not fm.get("due"):
            continue
        if fm.get("status", "active") in DONE:
            continue
        try:
            day = datetime.date.fromisoformat(fm["due"])
        except ValueError:
            continue  # TBA and malformed dates have no place on a calendar
        found.append(
            {
                "uid": f"{p.stem}@knowledgevault",
                "title": fm.get("title", p.stem),
                "subject": fm.get("subject", "—"),
                "points": (fm.get("points") or "").strip() or None,
                "day": day,
            }
        )
    return found


def esc(s):
    """RFC 5545 text escaping."""
    return str(s).replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")


def render(rows):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//KnowledgeVault//sync-calendar//EN",
        "CALSCALE:GREGORIAN",
    ]
    for r in rows:
        v = r.get("points")
        # points is a raw count ("20") or a course weight ("15%") — both appear in frontmatter.
        pts = "" if v in (None, "null", "—") else f" ({v})" if v.endswith("%") else f" ({v} pts)"
        out += [
            "BEGIN:VEVENT",
            f"UID:{r['uid']}",
            f"DTSTAMP:{now}",
            f"DTSTART;VALUE=DATE:{r['day']:%Y%m%d}",
            f"DTEND;VALUE=DATE:{r['day'] + datetime.timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{esc(r['subject'].upper())}: {esc(r['title'])}{esc(pts)}",
            "BEGIN:VALARM",
            "TRIGGER:-P1D",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{esc(r['title'])} due tomorrow",
            "END:VALARM",
            "END:VEVENT",
        ]
    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def main():
    check = "--check" in sys.argv
    rows = sorted(due_notes(), key=lambda r: r["day"])
    body = render(rows)
    # DTSTAMP changes every run; compare everything else so --check is honest.
    strip = lambda t: "\r\n".join(l for l in t.splitlines() if not l.startswith("DTSTAMP:"))
    old = ICS.read_text(encoding="utf-8") if ICS.exists() else ""
    if strip(old) == strip(body):
        print(f"{len(rows)} events, no change")
        return 0
    if check:
        print(f"{len(rows)} events, {ICS.name} is stale")
        return 1
    ICS.write_text(body, encoding="utf-8")
    print(f"wrote {ICS.relative_to(ROOT)} — {len(rows)} events")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
