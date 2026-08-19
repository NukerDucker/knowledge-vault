---
title: Exam Content Schema and Rich-Text Format
tags: [nextpath-x, schema, rich-text, database]
component: full-stack
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Exam Content Schema and Rich-Text Format

Related: [[../04-adrs/0003-richtext-stored-as-opaque-text-column]], [[../03-incident-playbooks/00-rich-text-parsing-failures]].

## DB columns holding rich-text content

All plain `string` → Postgres `TEXT`, no JSON type, no CHECK constraint:

| Column | Model | File |
|---|---|---|
| `questions.content` | `question.Question.Content` | `internal/domain/question/model.go` |
| `question_choices.content` | `questionchoice.QuestionChoice.Content` | `internal/domain/questionchoice/model.go` |
| `exam_papers.description` | `exampaper.ExamPaper.Description` | `internal/domain/exampaper/model.go` |

Why TEXT not JSONB: [[../04-adrs/0003-richtext-stored-as-opaque-text-column]].

## Rich-text JSON shape (confirmed against `nacl-nextpath-x-web/src/shared/lib/rich-text.tsx`)

```ts
type RichTextPayload = {
  kind: "rich-text";
  version: 1;
  doc: RichTextNode;
};

type RichTextNode = {
  type: string;
  text?: string;
  attrs?: Record<string, unknown>;
  marks?: { type: string; attrs?: Record<string, unknown> }[];
  content?: RichTextNode[];
};
```

Serialized via `JSON.stringify(...)` (`serializeRichText`) and stored as the raw string in the `TEXT` column. Confirms the task-brief-assumed shape `{"kind":"rich-text","version":1,"doc":...}` exactly.

## Supported node types (`renderNode`'s explicit cases)

`text`, `hardBreak`, `horizontalRule`, `image`, `emoji`, `inlineMath`, `blockMath`, `codeBlock`, `doc`, `paragraph`, `bulletList`, `orderedList`, `listItem`, `taskList`, `taskItem`, `blockquote`, `heading` (levels 1–3 only — `headingLevel` clamps anything else to 3). Any other node `type` falls through to a bare children-only render (see [[../03-incident-playbooks/00-rich-text-parsing-failures]]).

## Supported marks (`applyMarks`'s explicit cases)

`bold`, `italic`, `strike`, `code`, `underline`, `superscript`, `subscript`, `link` (href validated to `http:`/`https:`/`mailto:`), `textStyle` (color, validated hex), `highlight` (background color, validated hex).

## Legacy / invalid-value fallback behavior

- **Editor side** (`toTiptapDoc`): if `parseRichText` fails, wraps the raw string as a single-paragraph doc so the Tiptap editor can still open and edit pre-existing plain-text content.
- **Read-only render side** (`RichTextRenderer`): if `parseRichText` fails, falls back to `<div className="whitespace-pre-wrap">{text}</div>` — **plain text, not Markdown**. Markdown rendering was removed; source comment: `// ponytail: plain-text fallback for non-Tiptap content; markdown rendering dropped with react-markdown`.

## Image/link safety

`safeImageURL` only allows `https:` absolute URLs, or `http:`/relative URLs whose path starts with `/api/exam-assets/` (the API's exam-asset serving route). `safeLinkURL` only allows `http:`, `https:`, `mailto:`. Anything else silently drops the node (renders nothing, no error) — see the incident playbook for the failure-mode implications.

## Needs verification

- [ ] Whether any table/columns/rows extension is planned (currently absent from `nacl-nextpath-x-web/package.json`'s `@tiptap/*` dependencies — no `@tiptap/extension-table*` installed as of this pass).
