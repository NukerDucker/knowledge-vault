---
title: Backend Architecture
tags: [nextpath-x, architecture, backend, go, gin]
component: nextpath-x-api
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Backend Architecture

Related: [[00-stack-overview]], [[01-frontend-architecture]], [[03-full-stack-data-flow]].

> [!info] Replaces a deleted prior audit
> An earlier `obsidian-map/` folder (in this vault and loose next to the repo checkout) had a deep backend/security audit, but it was produced from an older checkout and the project owner confirmed on 2026-07-16 it no longer reflects `origin/main` and should not be trusted — it was deleted. This note re-documents backend architecture directly from the current source instead of trusting that prior audit. It is intentionally a condensed reference (route table + layer shape + auth model), not a full security re-audit — a fresh audit is a separate task if wanted.

## Boot sequence (`cmd/api/main.go`)

1. `config.MustLoad()` — env vars, prod validation (fail-fast on missing `JWT_SECRET`/short secret in prod).
2. `db.NewPostgresGorm(cfg)` — GORM Postgres connection.
3. `db.AutoMigrate(gormDB)` — see [[../04-adrs/0002-schemaless-automigrate-no-versioned-migrations]].
4. `bootstrap.SeedAcademicData(ctx, gormDB)` — idempotent upsert of KMITL faculty/department/major reference data.
5. `storage.NewS3Service(...)` — MinIO/S3 client init.
6. Manual repo → service → handler wiring for all 20 domains (`server.Handlers` struct).
7. `server.New(cfg, h, authSvc)` — builds the Gin engine and route tree.
8. `srv.ListenAndServe()` with graceful shutdown on `SIGINT`/`SIGTERM` (30s drain, so in-flight exam submits/uploads finish).

Evidence: `cmd/api/main.go`.

## Layer shape

Per `internal/domain/<name>/`: `routes.go -> handler.go -> service.go -> repository.go -> repository_gorm.go -> model.go`. Handlers are manually constructed and wired in `main.go` (no DI framework).

Domains (20): `auth`, `event`, `examaccess`, `examasset`, `examattempt`, `exampaper`, `examregistration`, `examsession`, `grading`, `interview`, `paperquestion`, `policy`, `portfolio`, `question`, `questioncategory`, `questionchoice`, `settings`, `studentanswer`, `systemlog`, `user`, `user/data`.

## Global middleware order (`internal/server/server.go`, `server.New`)

Order matters — "fail-fast top-down" per source comment:

1. `middleware.CORS(cfg)`
2. `middleware.CSRFProtect(cfg)`
3. `middleware.RequestSizeLimit(cfg.MaxRequestSize, cfg.MaxUploadSize)`
4. `middleware.Sanitizer()`
5. `gin.Logger()`
6. `middleware.Recover()`

Middleware source files: `internal/middleware/{auth,cors,csrf,ratelimit,recover,requestsize,sanitizer}.go`, each with a `_test.go` sibling.

## Route groups and their gates

| Group | Middleware | Registers |
|---|---|---|
| `publicAPI` (`/api`) | `RateLimiter(RateLimitGlobal)` — IP-based | `/auth/*`, `/auth/session`, `event` public, `examsession` public, `settings` public, `examasset` public; `/dev/*` only when `APP_ENV != prod` |
| `examOnly` (`/api`) | `ExamAccessRequired(authSvc)` + `UserRateLimiter(RateLimitExam)` | `studentanswer` auth routes (answer autosave — high per-user limit, ~150 questions can burst) |
| `examOnlyAttempts` (`/api`) | above + `UserRateLimiter(RateLimitStrict)` | `examattempt` exam-access routes (start/resume/submit) |
| `protected` (`/api`) | `AuthRequired(authSvc)` + `UserRateLimiter(RateLimitGlobal)` | `user`, `portfolio`, `interview`, `examregistration`, `examaccess` (exchange — **requires login session**, code alone is not enough), `data` |
| `examAttemptGroup` (`/api/exam-attempts`) | above + `UserRateLimiter(RateLimitStrict)` | `examattempt` general routes |
| `grader` (`protected` + `RequireRole("grader","admin")`) | | `studentanswer` grader routes, `grading` |
| `admin` (`protected` + `RequireRole("admin")`) | | `examregistration` admin/room, `user` admin, `event` admin, `examsession` admin, `portfolio` admin, `interview` admin, `examasset`, `exampaper`, `settings` admin, `question`, `questioncategory`, `questionchoice`, `paperquestion`, `systemlog`, `data` admin |

`/health` is unauthenticated, ungated. `/swagger/*any` is registered only when `APP_ENV != "prod"`.

## Auth model (`internal/domain/auth/service.go`)

Two distinct JWTs, both HMAC-signed with `JWT_SECRET`:

| Token | Claims (`auth.Claims`) | Issued by | Verified by | Scope |
|---|---|---|---|---|
| Session JWT | includes `Role` (`student`/`grader`/`admin`) | `signJWT` after Google OAuth (`ExchangeAndLogin`) or `DevToken` (non-prod) | `ParseJWT`, `middleware.AuthRequired` / `RequireRole` | Full authenticated API surface, HttpOnly cookie |
| Exam-access JWT (`ExamAccessClaims`) | user/registration/session/attempt scoped | `SignExamAccess` (called from `examaccess.Service.issueToken`) | `ParseExamAccessJWT`, `middleware.ExamAccessRequired` | Only `examOnly`/`examOnlyAttempts` routes, short-lived (session runtime deadline + submit grace) |

Login is Google OAuth restricted to the `@kmitl.ac.th` domain (per `nacl-nextpath-x-web/CLAUDE.md` and the `// @kmitl.ac.th domain check is the primary bot gate` comment in `server.go`'s `authGroup` setup). Dev-only shortcuts (`auth.RegisterDevRoutes`, `examaccess.RegisterDevRoutes`) are compiled into every build but only *registered* when `cfg.AppEnv != "prod"` — `examaccess.Service.DevAccess` additionally hard-checks `s.appEnv == "prod"` and returns `ErrDevDisabled` even if somehow reached.

Full exam-access token issuance flow (registration → check-in → code exchange → token): [[../05-schema-and-data-quirks/02-exam-access-token-exchange-flow]].

## Data model summary

GORM `AutoMigrate` model list (`internal/database/automigrate.go`) — 21 tables in migration order: `faculties`, `departments`, `majors` (reference data, seeded), `users`, `events`, `portfolio_submissions`, `exam_papers`, `question_categories`, `questions`, `question_choices`, `paper_questions`, `exam_sessions`, `exam_registrations`, `exam_attempts`, `student_answers`, `student_answer_choices`, `grading_score_audits`, `interview_slots`, `interview_bookings`, `system_logs`, `landing_cta_settings`, `portfolio_settings`, `theory_settings`, `interview_settings`. Foreign keys are added in a separate idempotent `addForeignKeys` pass (GORM `AutoMigrate` skips FKs when a model only stores a raw ID column) — see [[../04-adrs/0002-schemaless-automigrate-no-versioned-migrations]] for why there's no separate migration tool.

Key relationships relevant to exam flow: `Event 1—N ExamSession`, `ExamSession 1—N ExamRegistration`, `ExamRegistration 1—1 ExamAttempt` (per user+session), `ExamAttempt 1—N StudentAnswer`, `StudentAnswer 1—N GradingScoreAudit`. Detail: [[../05-schema-and-data-quirks/01-grading-score-audit-trail]].

## Needs verification

- [ ] Whether `internal/middleware/auth.go` implements `ExamAccessRequired`/`AuthRequired`/`RequireRole` exactly as named here — confirmed via `server.go` call sites, not by opening `auth.go` directly in this pass.
- [ ] Exact CSRF enforcement mechanics (`middleware.CSRFProtect`) — not opened in this pass; `CORS_ALLOWED_ORIGINS` is documented as authoritative for both CORS and the CSRF origin allowlist per `.env.example` comments only.
