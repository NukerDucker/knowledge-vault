---
title: Seeding and Migrations
tags: [nextpath-x, operations, seeding, database]
component: nextpath-x-api
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Seeding and Migrations

Related: [[../01-architecture/02-backend-architecture]], [[../04-adrs/0002-schemaless-automigrate-no-versioned-migrations]].

## Schema: AutoMigrate, no versioned migration tool

Schema is entirely GORM `AutoMigrate` (`internal/database/automigrate.go`), run on every boot (`cmd/api/main.go` step 3). No `golang-migrate`/`goose`/`atlas`-style migration files exist in the repo. Full rationale: [[../04-adrs/0002-schemaless-automigrate-no-versioned-migrations]].

## Academic reference data seeding

`bootstrap.SeedAcademicData(ctx, gormDB)` runs on every boot, including production (`cmd/api/main.go` step 4, source comment: "this is real reference data, not mock fixtures"). Implementation (`internal/bootstrap/seed.go`):

- Embeds `internal/bootstrap/data/kmitl_seed.json` at compile time via `//go:embed`.
- Upserts `Faculty`, `Department`, `Major` rows keyed by `id` (`clause.OnConflict{Columns: [id], DoUpdates: [name]}`) — idempotent, safe to run repeatedly.
- Regenerate the snapshot with `scripts/fetch_kmitl_seed.py`.

## `scripts/fetch_kmitl_seed.py`

Python 3 script, run manually (not part of any automated pipeline found in this pass): `python3 scripts/fetch_kmitl_seed.py`. Fetches faculty/department/curriculum data from the KMITL Registrar API (`https://api.reg.kmitl.ac.th/{faculty,department,curriculum}/...`), trims to the fields the app needs, writes `internal/bootstrap/data/kmitl_seed.json` (the file `seed.go` embeds). This is the only way the seed snapshot changes — editing the JSON by hand works too but drifts from the registrar source of truth.

## No test-data seeder found

No fixture/demo-data seed script was found for exam papers, questions, users, or sessions in this pass — `SeedAcademicData` only covers faculty/department/major reference data. Populating exam content for local dev currently means using the admin UI (`/admin/exam-papers`) or the API directly.

## Needs verification

- [ ] Whether a CI-only or dev-only seed path exists elsewhere in the repo (e.g. a `Makefile` target, a `scripts/` helper) beyond what was found in this pass.
