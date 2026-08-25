#!/usr/bin/env bash
# _meta/check.sh — vault governance checker.
#
# Verifies that the governing docs describe the vault that actually exists.
# Run monthly, and after any restructuring. Zero errors = the map is true.
#
# Exit 0 = clean. Exit 1 = errors found.
# Warnings never fail the run; they are work to schedule, not breakage.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

# Byte collation. Without this, [A-Z] matches lowercase in most locales
# and every file in the vault looks like a naming violation.
export LC_ALL=C

ERRORS=0
WARNS=0
err()   { printf '  \033[31mERROR\033[0m  %s\n' "$*"; ERRORS=$((ERRORS + 1)); }
warn()  { printf '  \033[33mwarn \033[0m  %s\n' "$*"; WARNS=$((WARNS + 1)); }
head2() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# All vault markdown. Prunes .git/.obsidian and never follows the
# university-files symlink — that way lies 47,000 files in ~/Documents.
vault_md() {
  find . \( -name .git -o -name .obsidian -o -name node_modules \) -prune -o \
       -type f -name '*.md' -print
}
vault_files() {
  find . \( -name .git -o -name .obsidian -o -name node_modules \) -prune -o \
       -type f -print
}

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Content you did not write. Vendored reference material keeps its upstream
# conventions; holding it to vault rules is noise, and noise gets ignored.
is_vendored() {
  case "$1" in
    ./02-programming/guides/system-design-notes/*) return 0 ;;
    *) return 1 ;;
  esac
}
# Root governing docs use SHOUTING.md by deliberate convention.
is_root_doc() {
  case "$1" in
    ./CLAUDE.md|./BRIDGE.md|./VAULT-GUIDE.md|./KOS-*.md|./MEMORY.md) return 0 ;;
    ./_meta/*) return 0 ;;
    *) return 1 ;;
  esac
}

# ---------------------------------------------------------------- 1. paths
# Every vault path named in the governing docs must exist.
# Placeholders (year-N, <name>, NN) are documentation, not paths — skip them.
head2 "1. Paths named in governing docs resolve"
GOVERNING=""
for g in _meta/KOS.md VAULT-GUIDE.md BRIDGE.md; do
  [ -f "$g" ] && GOVERNING="$GOVERNING $g"
done

# shellcheck disable=SC2086
grep -ohE '`(0[0-9]-[a-z0-9-]+|_meta)[a-zA-Z0-9/._ -]*`' $GOVERNING 2>/dev/null \
  | tr -d '`' | sed 's|/$||' | sort -u > "$TMP/paths"

while read -r p; do
  [ -z "$p" ] && continue
  case "$p" in *year-N*|*'<'*|*NN*|*'...'*) continue ;; esac
  [ -e "$p" ] || err "path named in governing docs does not exist: $p"
done < "$TMP/paths"
[ "$ERRORS" -eq 0 ] && echo "  all named paths exist"

# ------------------------------------------------------------ 2. wikilinks
# Every [[target]] must resolve to a real file.
head2 "2. Wikilinks resolve"
vault_files | while read -r f; do
  b=$(basename "$f"); echo "$b"; echo "${b%.md}"
done | sort -u > "$TMP/index"

# Strip fenced code blocks and inline `code` spans first: docs are full of
# [[wikilink]] and [[topic]] written as *examples*, and those are not links.
# 04-archive/ is skipped entirely — it is read-only, and its internal
# relative links point at files that moved with it.
strip_code() {
  awk '/^[[:space:]]*```/{f=!f; next} !f' "$1" | sed 's/`[^`]*`//g'
}

vault_md | while read -r f; do
  case "$f" in ./04-archive/*) continue ;; esac
  strip_code "$f" | grep -oE '\[\[[^]|#]+\]\]' 2>/dev/null \
  | sed 's/^\[\[//; s/\]\]$//' | sort -u \
  | while read -r link; do
      [ -z "$link" ] && continue
      case "$link" in *'<'*|*'>'*) continue ;; esac   # <placeholder>
      if grep -qxF "$link" "$TMP/index"; then continue; fi
      # Path-style link: accept if the basename resolves, warn otherwise.
      case "$link" in
        */*) base=${link##*/}
             if grep -qxF "$base" "$TMP/index"; then
               echo "WARN|$f|$link|path-style link, basename resolves"
             else
               echo "ERR|$f|$link|"
             fi ;;
        *)   echo "ERR|$f|$link|" ;;
      esac
    done
done | sort -u > "$TMP/links"

LINK_ISSUES=0
while IFS='|' read -r kind file link note; do
  [ -z "$kind" ] && continue
  if [ "$kind" = "ERR" ]; then
    err "broken wikilink [[$link]] in $file"; LINK_ISSUES=1
  else
    warn "[[$link]] in $file — $note"; LINK_ISSUES=1
  fi
done < "$TMP/links"
[ "$LINK_ISSUES" -eq 0 ] && echo "  all wikilinks resolve"

# --------------------------------------------------------- 3. frontmatter
# Every live note needs a frontmatter block with title, tags, status.
# Missing block = error. Missing field = warning (work to schedule).
head2 "3. Frontmatter present and valid"
VALID_STATUS="active|stable|submitted|graded|archived|draft"
FM_ISSUES=0
while read -r f; do
  # CLAUDE.md is agent config, not a note — no frontmatter expected.
  case "$f" in ./04-archive/*|./.claude/*|./CLAUDE.md|*/CLAUDE.md) continue ;; esac
  is_vendored "$f" && continue
  if [ "$(head -n1 "$f")" != "---" ]; then
    err "no frontmatter block: $f"; FM_ISSUES=1; continue
  fi
  fm=$(awk 'NR>1{if($0=="---")exit; print}' "$f")
  for field in title tags status; do
    printf '%s\n' "$fm" | grep -qE "^${field}:" || { warn "missing '${field}:' — $f"; FM_ISSUES=1; }
  done
  st=$(printf '%s\n' "$fm" | grep -E '^status:' | head -1 \
       | sed 's/^status:[[:space:]]*//' | tr -d '"' | awk '{print $1}')
  if [ -n "$st" ] && ! printf '%s' "$st" | grep -qE "^(${VALID_STATUS})$"; then
    warn "status '${st}' not in {${VALID_STATUS}} — $f"; FM_ISSUES=1
  fi
done < <(vault_md)
[ "$FM_ISSUES" -eq 0 ] && echo "  all notes have valid frontmatter"

# ------------------------------------------------------ 4. archive linkage
# Nothing outside 04-archive/ should link into it.
# This is the check that would have caught the 2026-08 internship drift.
head2 "4. No live note links into 04-archive/"
ARCH_ISSUES=0
if [ -d 04-archive ]; then
  find 04-archive -type f -name '*.md' -exec basename {} .md \; | sort -u > "$TMP/arch"
  while read -r name; do
    [ -z "$name" ] && continue
    # Skip ambiguous basenames: if a LIVE note shares the name (session-state.md
    # exists in several project folders), a [[link]] to it is almost certainly
    # aimed at the live one, and flagging it is noise.
    live_twin=$(find . \( -name .git -o -name .obsidian -o -name 04-archive \) -prune -o \
                     -type f -name "${name}.md" -print 2>/dev/null | head -1)
    [ -n "$live_twin" ] && continue
    hits=$(grep -rlF "[[$name]]" --include='*.md' . 2>/dev/null \
           | grep -v '^./04-archive/' | grep -v '^./_meta/' | grep -v '^./KOS-')
    if [ -n "$hits" ]; then
      err "archived [[$name]] still linked from: $(printf '%s' "$hits" | tr '\n' ' ')"
      ARCH_ISSUES=1
    fi
  done < "$TMP/arch"
fi
[ "$ARCH_ISSUES" -eq 0 ] && echo "  archive is not linked from live notes"

# ----------------------------------------------------------- 5. inbox age
# 00-inbox/ is a staging area, not storage. Two weeks is the limit.
head2 "5. Inbox is fresh (nothing older than 14 days)"
if [ -d 00-inbox ]; then
  stale=$(find 00-inbox -type f -name '*.md' -mtime +14 2>/dev/null)
  if [ -n "$stale" ]; then
    while read -r f; do warn "inbox item older than 14 days: $f"; done <<< "$stale"
  else
    echo "  inbox is clear"
  fi
fi

# ------------------------------------------------------------ 6. filenames
# Naming rule: kebab-case, no spaces, no uppercase. Archive is exempt.
head2 "6. Filenames follow the naming rule"
NAME_ISSUES=0
while read -r f; do
  case "$f" in ./04-archive/*) continue ;; esac
  is_vendored "$f" && continue
  is_root_doc "$f" && continue
  b=$(basename "$f")
  case "$b" in
    *' '*)   warn "space in filename: $f";     NAME_ISSUES=1 ;;
    *[A-Z]*) warn "uppercase in filename: $f"; NAME_ISSUES=1 ;;
  esac
done < <(vault_md)
[ "$NAME_ISSUES" -eq 0 ] && echo "  all filenames follow the rule"

# ---------------------------------------------------------------- summary
head2 "Summary"
echo "  errors:   $ERRORS"
echo "  warnings: $WARNS"
if [ "$ERRORS" -gt 0 ]; then
  printf '\n  The map disagrees with the disk. Fix the errors, or fix the doc.\n'
  exit 1
fi
echo "  Vault is consistent with its governing docs."
exit 0
