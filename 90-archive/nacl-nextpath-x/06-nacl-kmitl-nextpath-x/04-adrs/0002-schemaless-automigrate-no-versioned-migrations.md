---
title: "ADR-0002: Schema via GORM AutoMigrate, No Versioned Migration Tool"
tags: [nextpath-x, adr, database, migrations]
component: nextpath-x-api
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# ADR-0002: Schema via GORM AutoMigrate, No Versioned Migration Tool

Related: [[../01-architecture/02-backend-architecture]], [[../02-operations-and-seeding/02-seeding-and-migrations]].

## Context

The API needs a way to keep the Postgres schema in sync with 24 GORM model structs across 20 domains as they evolve. No `golang-migrate`/`goose`/`atlas`-style versioned migration files exist anywhere in `nacl-nextpath-x-api`. A loose `database_er_diagram.txt` (DBML-style sketch) exists at the repo root but is a snapshot, not a migration source — confirmed present in this pass (`test -f` succeeded, first lines show a `users` table DBML block), but its currency relative to the live schema is unconfirmed (it is hand-maintained prose, not generated from the models).

## Decision

Schema management is entirely `db.AutoMigrate(gormDB)` (`internal/database/automigrate.go`), invoked on every single API boot (`cmd/api/main.go` step 3, before any request is served). Source comment states the intent explicitly:

> "It runs on every API startup and is safe to call repeatedly: GORM only creates missing tables/columns/indexes, it never drops or renames anything, so there is no separate migration step to run before deploys."

`AutoMigrate` is additive-only by GORM's own design (create-if-missing for tables/columns/indexes; never drops or renames). Where a genuinely breaking schema change was needed, the fix was hand-written idempotent SQL run *before* `AutoMigrate`, directly in `automigrate.go`'s function body — e.g. two `DROP INDEX IF EXISTS` statements removing now-obsolete global-uniqueness indexes on `departments`/`majors` (superseded by composite per-faculty indexes on the model structs), and a guarded `DO $$ ... ALTER TABLE portfolio_submissions DROP CONSTRAINT IF EXISTS fk_portfolio_submissions_event_id ... END $$` dropping a foreign key that became optional. Foreign keys in general are added in a *second* pass, `addForeignKeys`, because GORM's `AutoMigrate` skips FK creation when a model stores only a raw ID column without an explicit association field — each constraint is added via an idempotent `DO $$ IF NOT EXISTS ... END $$` block with an inline cleanup statement (`DELETE`/`UPDATE`) to remove orphaned rows first.

## Consequences

- **Positive**: zero-friction deploys — there is no separate "run migrations" step to forget; every boot self-heals additive schema drift.
- **Positive**: the two "breaking change" precedents in `automigrate.go` (index drop, FK drop) show the team has an established, working pattern for the rare case AutoMigrate can't handle: hand-written idempotent SQL guarded by `IF EXISTS`/`DO $$ IF NOT EXISTS`, run before the AutoMigrate call.
- **Risk — schema drift has no detector**: nothing in CI or at boot verifies the *live* schema actually matches what the current model structs would produce beyond what AutoMigrate itself applies. A manually-applied `ALTER TABLE` on a shared environment (staging/prod) that AutoMigrate doesn't know to reconcile (e.g. a column type change, which AutoMigrate also won't apply automatically) can silently diverge from what local dev / other environments see.
- **Risk — no rollback primitive**: because there's no migration history table, there's no equivalent of "roll back to migration N." Recovering from a bad deploy means either a new forward-fixing boot-time SQL block (matching the existing pattern) or a manual DB intervention.
- **Neutral**: `database_er_diagram.txt` existing as a hand-maintained sketch alongside AutoMigrate is a minor documentation-drift risk (two descriptions of the schema, only one of which is authoritative) but isn't itself a runtime risk.

## Alternatives considered

- **`golang-migrate` or `goose`**: versioned `.sql`/`.go` migration files, explicit up/down, a migration-history table. Not adopted. Would give rollback capability and an audit trail of schema changes, at the cost of an explicit deploy step (forgettable) and double-maintaining schema intent (model structs + migration files).
- **Atlas (declarative schema-as-code)**: diffs the desired schema against live state and generates migrations automatically. Not adopted — likely a larger tooling/CI investment than the two ad-hoc breaking-change precedents in `automigrate.go` have needed so far.

## Needs verification

- [ ] Whether `database_er_diagram.txt` is still referenced anywhere (docs, onboarding) as authoritative, or is genuinely just a stale sketch — not fully cross-checked against the live model structs in this pass beyond its opening `users` table block.
- [ ] Whether staging/prod have ever needed a manual out-of-band schema fix that `automigrate.go` doesn't reflect — not something visible from the repo alone.
