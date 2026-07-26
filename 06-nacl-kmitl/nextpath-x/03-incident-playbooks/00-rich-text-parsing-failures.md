---
title: Rich-Text Parsing Failure Diagnostics
tags: [nextpath-x, incident-playbook, rich-text, frontend]
component: nextpath-x-web
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Rich-Text Parsing Failure Diagnostics

Related: [[../01-architecture/01-frontend-architecture]], [[../05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format]].

> [!warning] Correction to the original framing
> This playbook was requested as "rich-text JSON parsing failures vs. legacy Markdown rendering issues." That's not the actual failure mode: `src/shared/lib/rich-text.tsx` shows Markdown rendering was **removed**, not kept as a parallel legacy path. Source comment, verbatim: `// ponytail: plain-text fallback for non-Tiptap content; markdown rendering dropped with react-markdown`. The real dichotomy is **valid rich-text JSON** (renders via `renderNode`) vs. **anything else** (falls back to raw `whitespace-pre-wrap` plain text — not Markdown). This playbook is written against that actual behavior.

## Where content lives, unenforced

`question.Content`, `questionchoice.Content`, `exampaper.Description` are plain Go `string` → Postgres `TEXT` columns (`internal/domain/{question,questionchoice,exampaper}/model.go`). Nothing in the database enforces the rich-text JSON shape — see [[../05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format]]. A bad write (manual `UPDATE`, an import script, a bug in the admin save path) can silently corrupt the format; it only surfaces at render time.

## Diagnostic runbook

| Symptom | Cause | Check | Fix |
|---|---|---|---|
| Content shows as raw JSON text (`{"kind":"rich-text",...}`) on screen | `parseRichText` returned `null` — invalid JSON, `kind !== "rich-text"`, `version !== 1`, or `doc` fails `isRichTextNode` (missing/wrong `type`, or `content` present but not an array) | Pull the raw column value (`SELECT content FROM questions WHERE id = '...'` or via pgAdmin) and validate it parses as `{kind:"rich-text",version:1,doc:{type:"doc",...}}` | If it's plain pre-editor text, that's expected — `toTiptapDoc` wraps it as a single paragraph when *opened in the editor*, but `RichTextRenderer` on the read-only side falls to the plain-text branch instead, which is why it doesn't look like rendered rich text. Re-save through the admin rich-text editor to convert it. |
| Content shows as plain text, not obviously broken, but formatting (bold/lists/etc.) is missing | Same as above — `parseRichText` failed, silently landed in the `whitespace-pre-wrap` fallback (`RichTextRenderer`, the `doc ? renderNode(...) : <div className="whitespace-pre-wrap">{text}</div>` branch) | Same as above | Same as above |
| An image or link in otherwise-working content is just... missing | `safeImageURL`/`safeLinkURL` returned `undefined` and the node rendered as `null` — no error, no placeholder | `safeImageURL` only allows `https:`, or `http:` when the path starts with `/api/exam-assets/`; `safeLinkURL` only allows `http:`/`https:`/`mailto:`. Inspect the node's `attrs.src` / `attrs.href` in the raw JSON for a disallowed scheme or malformed URL | Re-insert the image/link through the editor (which only ever produces allowed URLs), or fix the raw JSON attr |
| Math renders as raw LaTeX source instead of a formatted equation | `katex.renderToString` threw (`throwOnError: false` in `renderMath`), caught, and the raw `latex` string is HTML-escaped and shown as-is | Check `attrs.latex` on the `inlineMath`/`blockMath` node for a KaTeX syntax error | Fix the LaTeX source via the editor's math node |
| Code block shows unhighlighted plain text instead of syntax-highlighted code | `lowlight.highlight(language, code)` / `highlightAuto` threw, caught in `renderCodeBlock`, falls back to raw `code` string | Check `attrs.language` against `lowlight`'s registered `common` grammar set — an unregistered language name still attempts `highlightAuto` (shouldn't normally throw, but check for it) | Set a valid/registered language on the code block, or leave unset (defaults to `"plaintext"`) |
| A whole block or nested structure just disappears (no error, no fallback text) | Node `type` isn't in `renderNode`'s explicit `if` chain — falls to the final `return <>{children}</>` — if that node type has no `content` children of its own, nothing renders. This means a Tiptap extension whose output type isn't handled in `rich-text.tsx` | Compare the unhandled `type` value in the raw JSON against `rich-text.tsx`'s explicit cases (`text`, `hardBreak`, `horizontalRule`, `image`, `emoji`, `inlineMath`, `blockMath`, `codeBlock`, `doc`, `paragraph`, `bulletList`, `orderedList`, `listItem`, `taskList`, `taskItem`, `blockquote`, `heading`) | Add a case to `renderNode` for the missing type, or avoid that Tiptap extension in the editor until it's supported. (Checked `package.json`: no table extension is installed, so `table`/`tableRow`/`tableCell` nodes are not an expected source of this — if one shows up, it means someone hand-edited the JSON or installed an extension without updating the renderer.) |

## Fast triage query

To find rows likely to hit the fallback path (not valid `{"kind":"rich-text","version":1,...}` JSON):

```sql
SELECT id, LEFT(content, 60) AS preview
FROM questions
WHERE content !~ '^\{"kind":"rich-text","version":1'
LIMIT 50;
```

Adjust the table/column for `question_choices.content` or `exam_papers.description` as needed.

## Needs verification

- [ ] Whether the admin exam-paper editor's save path (`src/features/admin/exam-papers/exam-paper-editor.api.ts` per `nacl-nextpath-x-web/CLAUDE.md`) always writes via `serializeRichText`, or has any path that could write a raw string instead — not traced in this pass.
