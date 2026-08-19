---
title: Grading Score Audit Trail
tags: [nextpath-x, schema, grading, audit]
component: nextpath-x-api
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Grading Score Audit Trail

Related: [[../01-architecture/02-backend-architecture]].

## Table: `grading_score_audits`

Model: `studentanswer.GradingScoreAudit` (`internal/domain/studentanswer/model.go`).

| Column | Type | Notes |
|---|---|---|
| `id` | `uuid` primary key | `default: gen_random_uuid()` |
| `answer_id` | `uuid`, not null, indexed (composite `idx_grading_score_audits_answer_created` with `created_at`) | FK → `student_answers(id)` CASCADE |
| `attempt_id` | `uuid`, not null, indexed | FK → `exam_attempts(id)` CASCADE |
| `question_id` | `uuid`, not null, indexed | FK → `questions(id)` CASCADE |
| `student_user_id` | `uuid`, not null, indexed | FK → `users(id)` CASCADE |
| `edited_by_user_id` | `uuid`, not null, indexed | FK → `users(id)` CASCADE |
| `edited_by_role` | `string`, not null | Role of the editor at time of edit (`grader`/`admin`) |
| `old_score` / `new_score` | `float64` | |
| `old_feedback` / `new_feedback` | `string` | |
| `created_at` | `time.Time`, not null, indexed (composite with `answer_id`) | |

All 5 foreign keys added via `internal/database/automigrate.go`'s `addForeignKeys` pass (GORM `AutoMigrate` doesn't create FKs for raw-ID-only fields) — see [[../04-adrs/0002-schemaless-automigrate-no-versioned-migrations]].

## Write path

Confirmed via `~/KnowledgeVault/05-ai/projects/nacl-nextpath-x/session-state.md`, 2026-06-02 entry:

> "API added dedicated `grading_score_audits` table... Manual score edits now log old/new score/feedback, answer/attempt/question/student ids, and authenticated grader/admin user id/role in the same transaction as score update and attempt recompute."

I.e. the audit row is written atomically with the score update itself and the attempt's recomputed total — a grading edit and its audit record cannot diverge (no window where one exists without the other).

## Read path

`GET /api/student-answers/:id/score-audits?limit=20&cursor=...` (grader/admin only) — cursor pagination sorted `created_at DESC, id DESC` (the composite secondary sort on `id` makes pagination stable when multiple audit rows share the same `created_at`).

## Needs verification

- [ ] Exact handler/service method names for the score-audits read endpoint — the route and sort order are confirmed via `session-state.md`, but the source file wasn't opened directly in this pass.
