---
title: "ADR-0003: Rich Text Stored as an Opaque TEXT Column"
tags: [nextpath-x, adr, database, rich-text]
component: full-stack
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# ADR-0003: Rich Text Stored as an Opaque TEXT Column

Related: [[../05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format]], [[../03-incident-playbooks/00-rich-text-parsing-failures]].

## Context

Exam-paper prompts, choices, and descriptions can contain rich formatting (bold, lists, images, math, code) authored via a Tiptap editor on the frontend. That content has to be persisted somewhere in Postgres.

## Decision

`question.Content`, `questionchoice.Content`, `exampaper.Description` are plain Go `string` fields (`internal/domain/{question,questionchoice,exampaper}/model.go`), which GORM maps to Postgres `TEXT` columns — no `JSONB` type, no `CHECK` constraint. The rich-text JSON shape (`{"kind":"rich-text","version":1,"doc":<RichTextNode>}`) is entirely an **application-level convention**, produced by `serializeRichText` and consumed by `parseRichText` in `nacl-nextpath-x-web/src/shared/lib/rich-text.tsx` — the database has no awareness that these columns hold structured data at all.

> [!warning] Rationale not confirmed in code
> No comment in the Go models, GORM tags, or `automigrate.go` explains *why* TEXT was chosen over `JSONB`. The following consequences/tradeoffs are this note's own analysis, not a documented project decision — treat them as "per project owner" reasoning to be confirmed, not fact.

## Consequences

- **Positive (inferred)**: the backend stays entirely agnostic to the rich-text document format. The Go API never parses, validates, or transforms the content — it's a pass-through blob. If the frontend's editor/schema changes (e.g. a Tiptap major version bump changing node shapes), no backend code or migration is required.
- **Positive (inferred)**: existing plain-text values (pre-dating the rich-text editor, or written by scripts/imports) remain valid `TEXT` — no migration needed to "upgrade" old rows; they're just handled via the fallback path documented in [[../05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format]] and [[../03-incident-playbooks/00-rich-text-parsing-failures]].
- **Risk (inferred)**: nothing in Postgres enforces the JSON shape. A malformed write (bad migration, manual `UPDATE`, an admin-save-path bug) is invisible until render time on the frontend — this is the entire premise of [[../03-incident-playbooks/00-rich-text-parsing-failures]]. A `JSONB` column with a `CHECK` constraint validating top-level shape (`kind`/`version` keys at minimum) would catch some of this class of bug at write time instead of read time.
- **Risk (inferred)**: `TEXT` gives up Postgres-side JSON querying/indexing (e.g. `jsonb_path_query` to find all questions containing an image node) — not currently used, but would require a column type change (and thus a real migration, see [[0002-schemaless-automigrate-no-versioned-migrations]]) to add later.

## Alternatives considered (inferred, not confirmed as actually discussed)

- **`JSONB` column with a `CHECK` constraint**: would validate `{"kind":"rich-text","version":<n>,...}` shape at write time and enable server-side JSON queries. Not adopted (or at least not currently in place) — plausibly because the schema-validation logic (which node/mark types are legal) genuinely lives in the frontend renderer (`rich-text.tsx`) and duplicating even a shallow version in a DB constraint adds a second place to keep in sync with editor changes.
- **A dedicated versioned migration table for content format changes**: not adopted, consistent with [[0002-schemaless-automigrate-no-versioned-migrations]]'s broader no-versioned-migrations approach.

## Needs verification

- [ ] Confirm with the project owner whether TEXT-vs-JSONB was an explicit choice or simply never revisited since the columns were first added as plain strings.
