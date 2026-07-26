---
title: NACL NextPath X Session State
tags: [ai, project, nextpath-x, session-memory]
status: active
created: 2026-05-23
updated: 2026-07-24
---
# NACL NextPath X Session State

## Purpose
Local source of truth for new coding sessions. Read this before broad codebase scans. Keep concise and update after meaningful work.

## Repo Layout
- Parent folder is not a git repo.
- `nacl-nextpath-x-web`: Next.js frontend repo on `dev`, currently behind `origin/dev` by 3 commits at setup time.
- `nacl-nextpath-x-api`: Go/Gin backend repo on `dev`, currently behind `origin/dev` by 6 commits at setup time.
- Local session memory belongs here in `~/KnowledgeVault` or parent `.ai/`, not inside child repos.

## Current Safety Rules
- Before commit/push, run `git status --short` in both child repos.
- Do not stage or commit `.ai/`, `.claude/`, `.codex/`, `session-state.md`, or `KnowledgeVault/**` in child repos.
- Existing tracked AI docs are allowed: web `AGENTS.md`, web `CLAUDE.md`, API `CLAUDE.md`.
- Preserve user changes. Never reset or revert unrelated work.
- Use `rtk` for high-output terminal commands.

## Web App State
- Framework: Next.js frontend, package scripts use Bun.
- Main folders:
  - `src/app`: route wrappers, layouts, loading/error/not-found, globals.
  - `src/features/landing`: public landing sections.
  - `src/features/portfolio`: applicant portfolio page/upload flow.
  - `src/features/theory`: applicant theory exam session selection.
  - `src/features/exam`: exam client container, screens, data source, types.
  - `src/features/admin`: admin dashboard, portfolio review, timeline, users.
  - `src/shared/components`: shared UI/components.
  - `src/shared/lib`: API/auth/date/user/data-source helpers.
- Commands: `bun run dev`, `bun run lint`, `bun run build`.
- Production data must come from API/DB. Production requires `NEXT_PUBLIC_API_URL`; no mock/hardcoded/localhost fallback.

## API State
- Backend: Go REST API with Gin, GORM, PostgreSQL, MinIO/S3.
- Entry points: `cmd/api/main.go`, `internal/server/server.go`, `internal/config/config.go`.
- Domain pattern under `internal/domain/<name>/`: model, repository interface, GORM repository, service, handler, routes.
- Auth: Google OAuth restricted to KMITL domain plus JWT roles `student`, `grader`, `admin`.
- Security priority high. Middleware order: CORS, request size, rate limit, sanitizer, logger, recover.
- Commands: `go run ./cmd/api/main.go`, `go build -o main ./cmd/api/main.go`, `go vet ./...`, `go test -race ./...`, `docker compose up --build`.
- Tests currently sparse/absent; new Go tests should be table-driven with subtests.

## Frontend/Backend Contract Notes
- 2026-05-24: Portfolio availability/result publication is now global settings, detached from timeline events. Use public `GET /api/settings/portfolio` and admin `PUT /api/settings/portfolio` with `submission_mode`, optional schedule fields, and `result_published`.
- 2026-05-24: Timeline `/api/events` is display-only for dynamic timeline; do not use events to decide whether portfolio upload is open or portfolio results are visible.
- 2026-05-24: Portfolio responses include computed `result_published` from global portfolio setting `result_published_at`.
- 2026-05-24: Student-owned requests hardened: portfolio submit and exam registration now use JWT user id, not client-supplied `user_id`; portfolio/registration detail and cancel enforce owner-or-admin. 2026-06-04: students can `DELETE /api/portfolios/mine` to remove their current portfolio before re-uploading; submit rejects existing submissions.
- 2026-05-24: Frontend normalized `/api/portfolios/mine` direct-object responses via `apiData`; Swagger docs generated under API `docs/` and imported by `cmd/api/main.go`.
- Backend has `/api/events`, `/api/exam-sessions/by-event/:event_id`, `/api/exam-attempts/session/:session_id/start`.
- Student exam payload must include session metadata, ordered questions, and choices without correctness fields.
- Do not expose `is_correct`, `correct_keywords`, scoring keys, or admin grading fields to students.
- Attempt start should use JWT user id from auth context, not client-supplied `user_id`.
- Backend should persist randomized question order per attempt and support answer upsert for MCQ, checkbox, short, and long answers.

## CI Guard State
- No CI guard is installed. User requested guard removal.
- Rely on local checks before commit/push: run `git status --short` in both child repos and do not stage local memory paths.

## 2026-05-30 Admin Grading Mock
- Web refactored frontend-only `/admin/grading` mock to match admin users/portfolio/exam-room styling: compact controls, table-style attempt list, rounded-xl admin cards.
- Mock data now isolated in `src/features/admin/grading/grading.mock.ts`; types in `grading.types.ts`; pure helpers in `grading.utils.ts`.
- Mock content updated with realistic exam rounds, Thai student records, network/Linux/system-design questions, rubrics, and varied answers/scores.
- Grading overview now follows Figma workflow while keeping admin visual tokens; anonymous mode now masks student names, IDs, and detail personal fields.
- No API code changed. Validation: `bun run lint` passes with pre-existing ProfilePanel warnings; `bun run build` passes and includes `/admin/grading`.

## 2026-06-01 Merge origin/dev into feat/access-token
- API merge commit `9934fd1` resolved `origin/dev` into `feat/access-token`.
- Kept `origin/dev` grading/auto-grading model with `student_answer_choices`, `is_graded`, grading routes and tests.
- Preserved exam access-token checks for start/resume, submit, and student answer save/list; answer writes block after submit.
- Validation: `rtk go test ./...` passed (49 tests/28 packages).

## 2026-06-01 Admin Written Grading Mock Refresh
- Web implemented frontend-only `/admin/grading` written-answer grading mock for exam-paper selection (`ข้อสอบชุดที่ 1`, `ข้อสอบชุดที่ 2`, `จิตวิทยา`) and question-level student scoring.
- Uses shadcn Select/Card/Badge/Input/Button plus sticky bottom save; shell follows admin `min-h-screen` + `max-w-7xl px-6 py-8` and relies on root dotted body background; mock data lives in `src/features/admin/grading/grading.mock.ts`; local diagram asset at `public/assets/mock/network-topology.svg`.
- Validation: `rtk bun run lint` passes with pre-existing ProfilePanel warnings; `rtk bun run build` passes and includes `/admin/grading`.

## 2026-06-02 Grading Backend Connection + Score Audit
- API added dedicated `grading_score_audits` table via `studentanswer.GradingScoreAudit` AutoMigrate. Manual score edits now log old/new score/feedback, answer/attempt/question/student ids, and authenticated grader/admin user id/role in the same transaction as score update and attempt recompute.
- API added grader/admin `GET /api/student-answers/:id/score-audits?limit=20&cursor=...` with cursor pagination sorted by `created_at DESC, id DESC`.
- Web added backend grading API helpers, `/grader/grading` real sessions/attempts table with round/status/search filters and offset pagination, and `/grader/grading/user/[id]` backend detail loading/score save/score audit history.
- Validation: `rtk go test ./...`, `rtk bun run test`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-02 Web Route Rename
- Web hard-replaced short route names: `/apply`, `/application`, `/pdpa`, `/admin/portfolios`, `/admin/exam-rounds`, `/admin/exam-rounds/[sessionId]`, `/admin/exam-papers`, `/admin/check-in`, `/grading`, `/grading/written`, `/grading/submissions/[submissionId]`, and exam question `/exam/[sessionId]/q/[questionNo]`.
- Kept `/blueprint`, `/theory`, `/portfolio`, `/exam`, `/auth/callback`, and admin dashboard/users/timeline.
- Added `src/shared/lib/routes.ts` route constants and tests; updated nav, auth onboarding redirect, landing CTA defaults, admin links, exam router navigation, and grading links. Follow-up commit renamed frontend feature modules to match routes: apply, application, pdpa, admin portfolios/exam-rounds/exam-papers/check-in, and grading.
- Removed stale inactive admin grading compatibility guard/tests. Backend APIs unchanged; grading still calls backend attempt ids internally while UI route uses submission wording. `/admin/exam-papers` lists `/api/exam-papers`; `/admin/exam-rounds` handles scheduled rounds/sessions.
- Added admin route shield guard matching grading access-denied card; all `/admin/*` pages now require admin role.
- Validation: `rtk bun run test`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-04 Application Penguin Success Dialog
- Web replaced student `/application`, `/portfolio`, and `/theory` success toasts for portfolio submit and exam registration with a shared Radix dialog using existing penguin assets. `/portfolio` also loads `/api/portfolios/mine`, shows the uploaded file card like `/application`, and requires deleting the current file before choosing a replacement.
- Error/info/cancel/profile toasts unchanged. Validation: `rtk bun run test`, `rtk bun run lint` (pre-existing DataTable warning), `rtk bun run build` passed.

## 2026-06-04 Admin Exam Registration Auto Sync
- Web Admin Dashboard exam registration card now has `เปิด/ปิดอัตโนมัติ` next to manual open/close. It bulk-syncs every loaded exam session `registration_status` to `OPEN` so all rounds/sessions become available at once.
- No API schema change. Validation: `rtk bun run test`, `rtk bun run lint` (pre-existing DataTable warning), `rtk bun run build` passed.

## Update Rule
ALWAYS update this file — at session START (record what is being picked up / current
intent) and after meaningful work. Not optional, every session touches it.
Update with:
- changed subsystem and intent,
- new commands/tests that matter,
- new contracts or pitfalls,
- current unresolved TODOs.
Keep it compact. Remove stale details.

## 2026-06-01 Admin Individual Grading Mock
- Web added mock-only nested admin grading routes: `/admin/grading` landing, `/admin/grading/written` written overview, `/admin/grading/user/[id]` individual full-exam grading detail.
- Individual mock data stays in `src/features/admin/grading/grading.mock.ts`; helper tests added for attempt lookup/filtering/score clamping.
- Validation: `rtk bun run test`, `rtk bun run lint` (passes with pre-existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-01 Individual Grading Read-Only Scores
- Web updated `/admin/grading/user/[id]` individual mock grading to show auto-computed/read-only scores instead of editable score inputs and removed stale score clamp helper/test.
- Individual mock attempt now uses realistic network/Linux/cloud/security questions, answer selections, computed total 14/20, and category score cards.
- Validation: `rtk bun run test`, `rtk bun run lint` (passes with existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-01 Individual Grading Written Edit
- Web changed `/admin/grading/user/[id]` so only written questions have editable scores; auto-scored choice questions remain read-only.
- Edited written questions show `แก้ไขแล้ว`; floating save island appears with edited count and clears after mock save. Total score previews written-score deltas.
- Validation: `rtk bun run test`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-01 Grader Role Grading Routes
- Web added dev grader test account `kanda.grader@kmitl.ac.th` and TestAccountSwitcher grader icon.
- Grading mock pages are now available under primary grader routes: `/grader/grading`, `/grader/grading/written`, `/grader/grading/user/[id]`; admin routes remain compatibility aliases.
- Navbar shows Grading link for `grader` role only; admin menu remains dashboard/users.
- Validation: `rtk bun run test`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-01 Grader Route Guard
- Web wrapped `/grader/grading*` pages with client role guard; only `grader` role renders grader pages, admin/student/anonymous see access denied.
- Added pure access test for grader-only route policy.
- Validation: `rtk bun run test`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-01 Grading Feature Rename
- Web moved grading feature files from `src/features/admin/grading` to `src/features/grader/grading` and renamed component filenames/symbols to `Grader*`.
- Admin compatibility route wrappers import grader feature components; primary grader routes unchanged.
- Validation: `rtk bun run test`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-01 Admin Exam Round Mock Merge
- Web merged `origin/feat/admin-round-management` into local `dev` as merge commit `59adde3`.
- Kept grading routes from `origin/dev`; added mock-only `/admin/exam` and `/admin/exam/[sessionId]` pages with admin nav entry.
- Fixed mock merge gates: `ExamRoundList` route prop, shared `DataTable` lint issues, portfolio `SortDir` import, navbar menu helper/test.
- Still mock-first: exam round pages use `USE_MOCK = true`; backend endpoint alignment remains future work.
- Validation: `rtk bun run test`, `rtk bunx tsc --noEmit`, `rtk bun run lint` (existing ProfilePanel warnings), `rtk bun run build`.

## 2026-06-03 Grading Exam Date UI
- Web /grading now shows selected exam date next to round dropdown using grading session start_time; no route or API changes.
- Validation: rtk bun run test, rtk bun run lint (passes with existing ProfilePanel warnings), rtk bun run build.

## 2026-06-03 Exam Registration And Manual Start
- API split exam session state into registration_status OPEN/CLOSED and exam_status WAITING/STARTED/FINISHED with started_at/finished_at; legacy status remains compatibility-only and effective status helpers preserve old OPEN/STARTED rows.
- Registration now checks registration_status; check-in/code issue remains available after registration closes; exam access/start requires checked-in token flow plus exam_status STARTED and uses started_at plus planned duration for token expiry and remaining time.
- Web added Admin Dashboard exam registration card with date/round selects and open/close buttons; Admin Check-in adds start/end exam controls; theory registration lists only open-registration sessions; exam UI maps waiting/finished errors to Thai copy.
- Validation: rtk go test ./..., rtk bun run test, rtk bun run lint (existing ProfilePanel warnings), rtk bun run build.

## 2026-06-03 Manual Exam Flow + Realistic Seeds
- API commit `07e84fa` adds split exam round state: `registration_status` for signup open/close and `exam_status` for exam runtime (`WAITING`, `STARTED`, `FINISHED`) with `started_at`/`finished_at`.
- API registration now checks `registration_status`; exam access/start/resume requires check-in and `exam_status=STARTED`; timers use `started_at + planned duration`; manual finish blocks start/resume.
- Dev seed now creates realistic 2026 KMITL-style portfolio submissions, exam event, two exam papers, categories/questions/choices, four sessions across two days/two rounds per day, registrations/check-ins, attempts, and student answers. Seed stays disabled in production.
- Web commit `9d638bc` adds dashboard exam-round registration control, `/admin/check-in` start/finish controls, open-session filtering for theory registration, realistic admin/grading/portfolio mocks, and ProfilePanel cleanup.
- ProfilePanel now edits only names/nicknames/phone. Email, student ID, faculty, department, major, and year are read-only labels; profile save sends only editable fields.
- Validation: `rtk go test ./...`, `rtk bun run test`, `rtk bun run lint`, and `rtk bun run build` passed. React Doctor advisory remains with broad/pre-existing warnings (large components/useReducer/a11y in touched files); low-risk style/Intl fixes were applied before web amend.

## 2026-06-03 Dashboard Exam Registration Simplified
- Web commit `34f987d` changes Admin Dashboard exam registration from per-date/per-round controls to portfolio-style global cards.
- `ตั้งค่าการรับสมัคร` now opens/closes registration for all loaded exam rounds at once via bulk PATCH to `/api/exam-sessions/:id/registration-status`.
- Added matching `จำนวนการรับสมัคร` card linked to `/admin/exam-rounds`; stats count total/pending/pass/fail from exam registrations, with mock fallback because current admin exam-round list still uses mock data and backend root registration list may be unavailable.
- Validation: `rtk bun run test`, `rtk bun run lint`, `rtk bun run build` passed. React Doctor advisory left one broad warning: `AdminDashboardPage` is a large component.

## 2026-06-03 Seed-Backed Admin Exam Data
- API commit `ee770ed` adds `GET /api/admin/exam-registrations` with `session_id`, `limit`, `offset`; response includes registration, nested user/session, score, and derived `PENDING|PASS|FAIL` based on latest submitted graded attempt and paper max score.
- Dev seed expanded to 12 realistic KMITL-style exam applicants across four sessions (2 days x 2 rounds), with registrations/check-ins/attempts/answers yielding dashboard demo counts: total 12, pending 2, pass 7, fail 3. Seed remains production-disabled.
- Web commit `2f2bac6` removes admin exam forced mocks and broken calls to unavailable public registration/settings/session list endpoints. `/admin/exam-rounds` and detail now read `/api/admin/exam-registrations`; detail also reads `/api/exam-sessions/:id`; check-in/action controls stay read-only there and real actions remain `/admin/check-in`.
- Dashboard exam stats now come from real admin registration API. Added simple `จัดการสอบ` panel linking `/admin/exam-rounds` and `/admin/exam-papers`; extracted dashboard subpanels to satisfy React Doctor.
- Validation: `rtk go test ./...`, `rtk bun run test`, `rtk bun run lint`, `rtk bun run build`, and `rtk bunx react-doctor --verbose --diff 34f987dc972463c8577cb387f2b956d26167159c --fail-on warning --no-score` passed.

## 2026-06-03 Merge feat/exam-page Into Web Dev
- Web `dev` fast-forwarded to merge commit `9c789d5`, combining `origin/feat/exam-page` exam UX/core changes with current `dev`.
- Added exam intro/sample UX, markdown prompt rendering deps, mock exam data source, and exam component tests.
- Preserved current backend contract: non-mock exam start/save/submit still use scoped exam-access tokens from `/api/exam-access/exchange`; dev exam access switcher restored; admin/mock bypass remains development-only.
- Validation in temp clean worktree: `rtk bun run test`, `rtk bun run lint`, `rtk bun run build` passed. React Doctor still reports broad exam screen warnings (`ExamClient`/`SampleScreen` state/effect/component-size); not fixed in merge.
- Current web checkout still has unrelated dirty grading/auth/mock-data changes; API unchanged.

## 2026-06-03 Grading Mock Removal Commit
- Web commit `888032e` removes grading mock data/assets, moves grading shared types to `src/features/grading/grading.types.ts`, points `/grading/written` at real `GradingPage`, and removes static dev JWT tokens from test accounts.
- Validation before commit: `rtk bun run test`, `rtk bun run lint`, `rtk bun run build` passed.
- Commit hook still reports React Doctor warnings; committed anyway. Web working tree clean, `dev` ahead of `origin/dev` by 17.

## 2026-06-03 Frontend Next Best Practices Pass
- Web audited all 22 App Router pages against Next.js best-practice checks: Server/Client boundaries, async params, Suspense around `useSearchParams`, image/font/route conventions, runtime selection, and error files.
- Added `src/app/global-error.tsx`, changed root metadata title to default/template form, and stopped `src/app/error.tsx` from rendering raw error messages.
- Validation: `rtk bun run lint`, `rtk bun run test` (17 files/56 tests), and `rtk bun run build` passed.

## 2026-06-04 Word-Like Exam Text Editor
- API added minimal PATCH endpoints for existing exam text fields: `/api/exam-papers/:id`, `/api/questions/:id`, and `/api/question-choices/:id`; no schema migration and sanitizer unchanged.
- Web added `/admin/exam-papers/[paperId]` rich text editor using Tiptap JSON stored inside existing string fields. Editor supports bold, italic, text color, highlight, undo/redo, and clear formatting for paper description, question prompts, and choice text.
- Student exam prompt/choice renderer now detects `{"kind":"rich-text","version":1,"doc":...}` and renders React nodes safely; legacy Markdown fallback remains; long-answer student input remains Markdown.
- Added Tiptap deps: `@tiptap/react`, `@tiptap/starter-kit`, `@tiptap/extension-text-style`, `@tiptap/extension-color`, `@tiptap/extension-highlight`.
- Validation: `rtk go test ./...`, `rtk bun run test`, `rtk bun run lint`, `rtk bun run build` passed.

## 2026-06-04 Backend Mock Exam Seed
- API dev seed now adds frontend `exam.mock-data-source` as third exam paper `SeedExamPaperMockID` (`ข้อสอบคัดเลือก`) with 5 questions, markdown prompts, MCQ/CHECKBOX choices, SHORT/LONG written questions, and paper-question ordering/scores totaling 20.
- Existing infra/ops seed papers and demo attempts are unchanged to preserve grading/dashboard demo data.
- Validation: `rtk go test ./...` passed (68 tests/28 packages).

## 2026-06-04 Exam Round Admin Cleanup
- Web commit `2a7b7fe` cleans `/admin/exam-rounds`: row body clicks navigate via router, edit/delete controls do not, `?create=1` opens create dialog, and form/delete dialogs use shadcn Field/Input/Select/Dialog/AlertDialog composition.
- Web shared `DataTable` ignores interactive child clicks when `onRowClick` is set and has regression tests. Admin check-in/dashboard/timeline touched for consistency; rich-text helper remains shared under `src/shared/lib/rich-text.tsx`.
- API commit `251707e` keeps dev seed wiring intact and adds optional `registration_status` create validation with 400 `invalid_status`; added exam session service tests.
- Validation: `rtk bun run test`, `rtk bun run lint`, `rtk bun run build`, and `rtk go test ./...` passed. Running web test in parallel with build can hit Vitest 5s timeouts; rerun alone passed.

## 2026-06-04 Exam Operational Mock Seed Removal
- API dev seed no longer inserts exam sessions, exam registrations, exam attempts, or seeded student answers/answer choices. It now deletes those known seeded operational rows on non-prod startup while keeping exam event, papers, questions, choices, and paper-question seed data.
- Web removed default fallback exam session UUIDs from `src/features/exam/exam.config.ts`; `/exam` now requires `NEXT_PUBLIC_EXAM_SESSION_ID` or a route/session id instead of relying on removed seed sessions. Result screen treats missing next-session config as last set.
- Validation: `rtk go test ./...`, `rtk bun run test`, `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-05 Admin Dashboard + Theory Auto Mode
- API added global theory registration settings under `/api/settings/theory` with `registration_mode`, optional open/close schedule, and computed `registration_open`; exam registration now requires both global theory registration open and session-level registration open.
- Web dashboard now clearly separates `รอบสะสมผลงาน` and `รอบสอบทฤษฎี`, moves portfolio result publication into the portfolio card, adds portfolio-style theory auto/force-open/force-close schedule controls, and condenses user/timeline/CTA management into buttons/dialog.
- Web restored `/admin/examinees` as a global current-backend examinee list using `/api/admin/exam-registrations?limit=500`; `/admin/exam-rounds` create/edit now uses shared `DatePickerTime`; users rows open detail dialogs with profile, portfolio, and exam registration info; timeline cards are condensed.
- Validation: `rtk go test ./...`, `rtk bun run test`, `rtk bunx tsc --noEmit`, `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-05 Timeline Active Muted State
- Web made timeline event `is_active=false` visual-only: public timeline/calendar still show the event but render it as muted gray; delete remains the only hide/remove flow.
- Landing CTA no longer uses event `is_active` to decide if exam registration is open; it follows schedule/settings only.
- Landing, portfolio, and theory public timelines show date-only ranges; round registration summary text still uses existing date-time ranges.
- Validation: `rtk bun run test`, `rtk bun run lint`, `rtk bun run build` passed.

## 2026-06-04 Exam Session Paper Source
- Web `/exam` now resolves the current user's assigned session via `GET /api/exam-registrations/mine` when no route/env session id is provided, instead of relying on hardcoded seeded IDs.
- Backend student exam start response includes `session.paper_id`; attempt start already reads `exam_sessions.paper_id` from DB and loads questions through paper-question mappings.
- Validation: `rtk go test ./...`, focused exam frontend tests, `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-04 Mock Data Trace Removal
- Web commit `336708c` and API commit `2e8f82c` remove exam mock-data flow.
- API dev seed no longer defines or inserts mock exam user/paper/question/session/registration/attempt IDs, old frontend mock exam paper data, made-up exam event rows, or cleanup-only retired mock IDs. Remaining seeded domain data in `dev_seed.go` is KMITL academic data, users, portfolio submissions tied to an existing portfolio event, and exam papers/questions/choices/paper mappings.
- Web removed the mock exam student test account; `/exam` stays DB-backed through assigned session/paper IDs.
- Targeted searches for mock-data/config identifiers are empty in both repos; non-test web `src` and API `internal` contain no `mock`/`Mock`/`MOCK` matches.
- Validation: `rtk go test ./...`, `rtk bun run lint`, `rtk bun run test`, and `rtk bun run build` passed.

## 2026-06-04 Copilot Repair Pass
- Web fixed `/admin/exam-rounds` build break by using exported `SessionRow`, wrapping `useSearchParams` route content in Suspense, normalizing form values, and renaming exam-round helper `api.tsx` to `api.ts`.
- Shared rich-text helpers moved from `src/features/exam/components/rich-text.tsx` to `src/shared/lib/rich-text.tsx`; admin editor and exam renderers import shared helper.
- API restored dev portfolio/exam seed calls so backend-backed exam/admin dev pages keep seeded data, removed empty session DTO placeholder, and validates create `registration_status`; added service tests.
- Validation: `rtk bun run test` (64 tests/21 files), `rtk bun run lint` (passes with existing `DataTable` warning), `rtk bun run build`, and `rtk go test ./...` (73 tests/28 packages) passed.

## 2026-06-04 Backend-Pulled Exam Pages
- API added non-prod `POST /api/dev/auth-token` to issue a real JWT for seeded dev users; frontend dev test-account auth now fetches that token so admin pages can call protected backend APIs.
- Dev seed now includes started mock exam session `SeedExamSessionMockID` (`74000000-0000-0000-0000-000000000005`) using `SeedExamPaperMockID`, plus dedicated `SeedStudentMockExamID` / `student_mock_exam` to avoid the unique `exam_registrations.user_id` constraint.
- Exam page default session now points at the seeded mock backend session; admin dev users no longer force frontend mock data unless `NEXT_PUBLIC_USE_MOCK_EXAM=true`.
- Fixed dev exam access so `checked_in_by` remains a valid UUID instead of `"dev"`.
- Smoke: local API returned mock paper in `/api/exam-papers`, 14 admin registrations including mock session, and exam start returned 5 backend questions.
- Validation: `rtk go test ./...` (71 tests/28 packages), `rtk bun run test` (66 tests/22 files), `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-04 Frontend Exam Mock Removed
- Web deleted `src/features/exam/exam.mock-data-source.ts` and removed the `NEXT_PUBLIC_USE_MOCK_EXAM` / `shouldUseMockExam` frontend path. Exam UI now always uses backend data source plus dev exam-access token flow.
- Backend seed remains the source of the former frontend mock exam data.
- Validation: `rtk bun run test` (64 tests/21 files), `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-04 Frontend Exam Mock Removed
- Web deleted `src/features/exam/exam.mock-data-source.ts` and removed the `NEXT_PUBLIC_USE_MOCK_EXAM` / `shouldUseMockExam` frontend path. Exam UI now always uses backend data source plus dev exam-access token flow.
- Backend seed remains the source of the former frontend mock exam data.
- Validation: `rtk bun run test` (64 tests/21 files), `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-04 Backend-Pulled Exam Pages
- API added non-prod `POST /api/dev/auth-token` to issue a real JWT for seeded dev users; frontend dev test-account auth now fetches that token so admin pages can call protected backend APIs.
- Dev seed now includes started mock exam session `SeedExamSessionMockID` (`74000000-0000-0000-0000-000000000005`) using `SeedExamPaperMockID`, plus dedicated `SeedStudentMockExamID` / `student_mock_exam` to avoid the unique `exam_registrations.user_id` constraint.
- Exam page default session now points at the seeded mock backend session; admin dev users no longer force frontend mock data unless `NEXT_PUBLIC_USE_MOCK_EXAM=true`.
- Fixed dev exam access so `checked_in_by` remains a valid UUID instead of `"dev"`.
- Smoke: local API returned mock paper in `/api/exam-papers`, 14 admin registrations including mock session, and exam start returned 5 backend questions.
- Validation: `rtk go test ./...` (71 tests/28 packages), `rtk bun run test` (66 tests/22 files), `rtk bun run lint`, and `rtk bun run build` passed.

## 2026-06-04 Backend Mock Exam Seed
- API dev seed now adds frontend `exam.mock-data-source` as third exam paper `SeedExamPaperMockID` (`ข้อสอบคัดเลือก`) with 5 questions, markdown prompts, MCQ/CHECKBOX choices, SHORT/LONG written questions, and paper-question ordering/scores totaling 20.
- Existing infra/ops seed papers and demo attempts are unchanged to preserve grading/dashboard demo data.
- Validation: `rtk go test ./...` passed (68 tests/28 packages).

## 2026-06-05 Notion-Style Exam Editor V1
- API added admin-only `POST /api/exam-assets` for rich exam editor image uploads. It reuses S3/MinIO via `UploadExamAssetFile`, accepts PNG/JPEG/WebP/GIF up to 5 MB, and returns URL/key/file metadata.
- Web replaced broken copied Tiptap template with scoped admin `ExamRichTextEditor` for `/admin/exam-papers/[paperId]`: toolbar, BubbleMenu, drag handles, emoji quick insert, math, links, alignment, code blocks, colors/highlights, and image paste/drop/upload.
- Student exam rich-text renderer now whitelists expanded nodes/marks: links, images, math, code highlighting, alignment, underline, sup/sub, tasks, dividers, and legacy Markdown fallback.
- Removed unused copied `/simple` Tiptap template tree and stale SCSS globals; all direct `@tiptap/*` deps pinned to 3.25.0.
- Validation: `rtk go test ./...`, `rtk bunx tsc --noEmit`, `rtk bun run lint`, `rtk bun run test`, `rtk bun run build` passed.

## 2026-06-05 Exam Sample Offline + Contextual Editor Menus
- Web fixed `/exam?screen=rules` and `/exam?screen=sample` to render intro/sample UI without calling exam backend first. `ExamClient` now defers `loadExam` until taking mode or direct question route, preventing rate-limit errors on sample-only pages.
- Admin exam Tiptap editor no longer renders a persistent toolbar. Selected text uses `BubbleMenu` for marks/link/color/highlight; focused empty blocks use `FloatingMenu` for block insert/format actions and image upload.
- Added `src/features/exam/ExamClient.test.tsx` coverage for offline rules/sample and taking-mode loading. Validation: `rtk bunx tsc --noEmit`, `rtk bun run test`, `rtk bun run lint`, `rtk bun run build` passed.

## 2026-06-05 Unified Exam Flow + Preview Hardening
- Web `/exam` now keeps `paper_id` backend-owned: code exchange stores `session_id` + exam access token, start attempt uses `/api/exam-attempts/session/:session_id/start`, sample final moves to `?screen=taking`, and code gate renders until both session id and exam access token exist. Empty backend question payload now shows Thai error instead of skeleton forever.
- Web added admin-only `/admin/exam-papers/[paperId]/preview`. Editor Preview stores current unsaved rich-text content in `sessionStorage`; preview route renders with student exam components and never creates attempts, saves answers, or submits.
- API sanitizer now preserves only parse-valid `{kind:"rich-text",version:1,doc:{...}}` strings; malformed rich-text-looking strings sanitize as plain text. Exam assets now validate file signatures, use UUID `exam-assets/<uuid><ext>` keys, remove MinIO anonymous download, and serve through `/api/exam-assets/{key}` capability URLs with Swagger docs.
- Web tightened rich-text image URLs to API asset URLs or HTTPS only, kept `mailto:` for links, made localhost image remotes dev-only, and removed unused deps.
- Validation: `rtk go test ./...`, `rtk gofmt -l internal/middleware/sanitizer.go internal/domain/examasset internal/storage`, `rtk rg -n "exam-assets" docs`, `rtk bun run test`, `rtk bun run lint`, `rtk bunx tsc --noEmit`, and `rtk bun run build` passed.

## 2026-06-12 Route Standardization
- API: Added `GET /api/users/me` endpoint.
- Web & API: Standardized all `/mine` endpoints (`/api/portfolios/mine`, `/api/exam-registrations/mine`, `/api/interview-bookings/mine`) to `/me`.
- Merged `feat/access-token` into `dev` on the backend.
- Validation: `go test ./...` and `bun run test` passed. Generated new Swagger docs.

## 2026-06-21 Portfolio Upload Gate + Ponytail Audit
- Web: `/portfolio` `UploadSection` now hides the entire upload area when submission not open. Reads `submission_open` from `GET /api/settings/portfolio`; closed round shows `ปิดรับสมัครหรืออยู่นอกช่วงเวลาที่กำหนด` and renders no dropzone/input/confirm. Render hoisted to `uploadBody` var (avoids nested-ternary lint + a11y S6848/S6819). Test `PortfolioContent.test.tsx` covers closed-round (4/4). Still UNCOMMITTED (separate from audit commits; unrelated WIP also dirty — never `git add -A`).
- Ran ponytail-audit (web+api), rechecked with scrutinize. Two headline backend cuts REFUTED and dropped: deleting 17 Repository interfaces and questionchoice Service — both load-bearing test seams (`fake*Repository` doubles across 17 `*_test.go`; questionchoice Service validates + read-mutate Update). KEEP. Plan: `~/.claude/plans/rosy-kindling-lighthouse.md`.
- Web dead-code removals, one commit each on `dev`: `cf176ce` drop `richTextPlainText`; `d8b9be6` remove unused `useIsMobile` hook + barrel line; `fe27a61` inline single-use `selectCurrentPortfolioEvent`; `6dbfe61` delete dead portfolio CSV export module. tsc clean, 6/6 affected tests pass.
- API boilerplate helpers in `internal/utils/response.go`, one commit each on `dev`: `73af560` add `BindJSON(c, dst) bool` → 36 inline `ShouldBindJSON+JSONError+return` sites (outliers grading `invalid_input` and user:34 custom msg left verbatim); `6107350` add `NotFoundIf(c, cond, msg) bool` → 21 nil→404 blocks (messages verbatim, no contract change). Net −33 LOC.
- B3 (generic `MapToResponses[T,R]` for ~16 `ToResponse` loops) NOT applied — marginal, idiomatic explicit loops, 16 manual edits; recommended skip. Helper sketch in plan if revisited.
- F5 (route ~15 raw `fetch` through `apiFetch`/`apiList`) still pending from plan.
- Validation each API commit: `rtk go build ./...`, `rtk go vet ./...`, `rtk go test ./...` (171 tests/29 packages) passed.

## 2026-06-21 Applicant UX Refactor + Exam-Preview
- Web-only. New `/exam-preview` practice mock: `src/app/exam-preview/page.tsx` → `src/features/exam/ExamPreviewClient.tsx` reusing `ExamFrame`/`ExamQuestionCard`/`QuestionNavigator` (real `ExamClient` untouched). 20 static questions `exam-preview.questions.ts` (answer keys local, never API). Untimed. Scored via pure `exam-preview.score.ts` (`scorePreview`, exact-match MCQ/CHECKBOX, SHORT→reviewer) + `exam-preview.score.test.ts`. `routes.examPreview` added. Blueprint "ลองทำข้อสอบ" now → `/exam-preview` (was `/exam`). Navbar hides on `/exam*` so preview is chromeless too.
- Exam images: new `src/features/exam/components/ZoomableImage.tsx` (shadcn Dialog lightbox, no new dep). Applied in `QuestionBody.tsx` + shared `rich-text.tsx` image node — removed border + alt caption (alt kept on `<Image>` for a11y/tests). `QuestionNavigator` grid now `lg:max-h-[calc(100vh-22rem)]` so ~200 buttons scroll, no layout break.
- Theory: `ContentDetailsSection` gates on `isRoundClosed` (no OPEN slot) → rose Portfolio-style `TheoryClosedCard`, registration UI hidden. Blueprint button relocated out of Navbar; user moved it into `AboutSection` (not TheoryPage). Cleaned unused TheoryPage imports.
- Application: upload session fully hidden when `!portfolioEventOpen` (rose status card instead of disabled dropzone+alert). Exam slots restyled to Theory low(≤5)/full seat pills (dropped `Badge`). `ProfileFields.Field` locked = muted bg + `Lock` icon + "(แก้ไขไม่ได้)", editable = white bg + logo border. `ApplicationProgress` component + usage deleted.
- Global: admin dashboard `hover:text-black` → `hover:bg-[#1FA9FF]/10 hover:text-[#1FA9FF]`; hero CTA `size=lg` bigger/bolder.
- DEFERRED (plan §1a): full shared `PortfolioUpload` extraction unifying Application + standalone Portfolio upload bodies NOT done (500-line extraction, risk vs context budget); only user-visible hide-when-closed + status-card parity shipped.
- Pre-existing lint warnings remain in `ApplicationRounds.tsx` (unused AlertDialog*/Field*/RadioGroup imports, dead `handleConfirmExamClick`/`showChangeConfirm`) — left per minimal-diff.
- Plan: `~/.claude/plans/context-developer-jolly-pearl.md`. Validation: `rtk bunx tsc --noEmit`, `rtk bun run lint` (0 errors), `rtk bun run test` (119 tests/35 files), `rtk bun run build` passed.

## 2026-06-22 UI Polish + Design-Token Sweep
- Web-only, `dev`. Commit `c7c1038` (+ follow-up): unify neutral chrome to semantic tokens, no redesign, palette unchanged.
- Convention now in web `CLAUDE.md` "Design Tokens": numbered Tailwind `gray-*/slate-*` → `text-foreground` / `text-muted-foreground` / `bg-muted` / `bg-accent` / `border-border` / `border-input`. Primary buttons → `<Button variant="nacl">`. KEEP custom theme tokens (`bg-logo`, `text-blue-5`, `border-blue-40`), named status colors (badges/dots/timeline), and dark panels (`bg-slate-800/900`).
- Swept admin/grading/application/apply/exam/landing/portfolio + shared shells via prefix-safe `perl` (lookbehind keeps `hover:/focus:` prefixes; dark-bg tokens excluded). Backup at `/tmp/nacl-ui-backup`.
- Primitives: `ui/table.tsx` rows `p-2`→`px-3 py-2.5`; `ui/button.tsx` base `active:scale-[0.98]` press; `globals.css` underline `#1fa9ff`→`var(--color-logo)`; `Navbar.tsx` dropped invalid `align-center` + orphan `bg-opacity`, login→`nacl` variant, removed icon `mr-2` double-spacing, fade-in skeleton. Both `app/loading.tsx` get `animate-in fade-in`.
- Fixed dup `variant` prop in `AdminCheckInPage` (left by an interrupted subagent — Sonnet hit session limit mid-run; finished with Opus).
- React Doctor: 10 `label`-without-`htmlFor` warnings in touched files are PRE-EXISTING (diffs are color-only), not regressions. Separate a11y task if wanted.
- PENDING: browser screenshot verification (not run — cost/context budget); QuestionNavigator already had `transition-colors` (no work).

## 2026-06-22 Security Hardening + Cookie-Only Auth
- Ran vibecoder-review (OWASP triage) + ecc:security-review over both repos. Codebase already hardened (JWT alg-confusion check, OAuth state CSRF, httpOnly cookies, KMITL domain lock, consistent IDOR owner-or-admin checks, per-IP rate limit, request-size cap, bluemonday deep JSON sanitizer, parameterized GORM, prod config guards, dev/swagger gated to non-prod). No SQLi/RCE/hardcoded secrets (`.env` gitignored).
- **Pass 1 — 4 gap fixes:**
  - Web `next.config.ts`: added security headers (CSP `frame-ancestors/object-src 'none'`, `base-uri/form-action 'self'`, `upgrade-insecure-requests`; X-Frame-Options DENY; X-Content-Type-Options nosniff; Referrer-Policy; Permissions-Policy; HSTS). CSP omits script/style-src so Next/KaTeX/Tiptap don't break — tighten to nonce later (flagged `ponytail:`).
  - API `storage/s3.go`: `verifyPortfolioContent` sniffs magic bytes (`http.DetectContentType`) and matches declared→sniffed family (office docs→zip); portfolio upload no longer trusts client `Content-Type` (parity with exam-asset path).
  - API `auth/handler.go`: OAuth state cookie `Secure` flag now honors prod (was hardcoded false) on set+clear.
  - Web `shared/lib/rich-text.tsx`: KaTeX fail fallback `escapeHtml(latex)` instead of raw latex into `dangerouslySetInnerHTML` (latent XSS; KaTeX itself safe `trust:false`).
- **Pass 2 — full cookie-only auth migration (chosen: unify dev to cookie):** real session JWT now lives ONLY in httpOnly+Secure cookie in every env.
  - API: `TokenFromRequest` cookie-first (Bearer = non-browser fallback); `/api/auth/session` returns `{user}` only (no JWT in body); `/api/dev/auth-token` now sets the same httpOnly cookie → dev auth path == prod.
  - API: new `middleware/csrf.go` `CSRFProtect` — prod rejects state-changing (POST/PUT/PATCH/DELETE) requests whose `Origin` ∉ `CORS_ALLOWED_ORIGINS`. This is the anti-impersonation control the cookie-only move requires (Bearer previously gave accidental CSRF immunity). `csrf_test.go` table-driven (6 cases).
  - Web: auth context holds non-secret `COOKIE_SESSION_MARKER` (exported from `api/client.ts`), never the JWT; `buildHeaders` skips the marker (cookie authenticates). All ~40 `if(!token)`/`{token}` callers UNCHANGED — marker design avoided 40-file churn. `dev-auth.ts` sends `credentials:"include"`.
  - Exam-access token (sessionStorage) LEFT as-is: short-lived, scoped to one attempt, can't impersonate beyond that exam.
- Threat outcome: XSS can't read JWT (cookie-only), JWT unforgeable (HS256+alg check), CSRF blocked (Origin), no token in body/logs.
- PROD MUST-DO: set `CORS_ALLOWED_ORIGINS` (both CORS + CSRF depend on it). Cookie is `SameSite=None` in prod (assumes cross-site web/api); if deployed same-site, switch to `SameSite=Strict` for defense-in-depth (offered to make env-configurable).
- Validation: API `rtk go build/vet`, `rtk go test -race ./...` 178 pass/29 pkg; web `rtk bunx tsc --noEmit` clean, auth/api vitest pass. 1 PRE-EXISTING failure `PortfolioContent.test.tsx` (date/registration-window, confirmed failing on clean tree — NOT from this work).
- Plan: `~/.claude/plans/reflect-on-mistakes-you-cheerful-lovelace.md`. Validation: `rtk bunx tsc --noEmit` clean, `rtk bun run lint` 0 errors (24 pre-existing warnings).

## 2026-06-23 — 2026-06-24 Commits (post-22 catch-up)
- Web (`dev`):
  - `c85dcdf` feat(admin,landing): admin sidebar nav, timeline calendar, round-info dialog.
  - `9807f24` admin papers page responsiveness.
  - `d9da495` fix(web): route authenticated API calls through `apiFetch` (cookie session).
  - `6f3c3e5` refactor(api): migrate public raw `fetch` calls to `apiFetch` helpers — closes prior plan item F5 (raw `fetch` → `apiFetch`/`apiList`).
  - `2f2b5a8` fix(grading): guard null list payloads so empty lists don't crash.
  - `43d7631` fix(apply): assign `dataRef` in effect, not during render.
  - `dee054a` style(admin): `QuestionNavigatorPanel` sticky offset.
  - `3239363` fix padding.
  - `a9f05bd` fix(admin/timeline): clarify color toggle label, fix edit dialog CLS.
- API (`dev`):
  - `34fdef4` feat: basic loadtest; `3308b75` merge PR #15 `feat/load-test`.
  - `1e070bb` fix: unit test mismatch with auth handler change.
  - `73042f6` feat(exampaper): derive `CreatedBy` from JWT, drop required body field.
  - `fd34b5b` fix(portfolio,examregistration): `GetMine` returns 200 null on no record (was error path).

## 2026-06-28 Obsidian-Map Security Findings Fixed (SEC-001..008)
- Verified the `obsidian-map/10 - Security Review Map.md` findings against live code — all real, not stale. Fixed all 8. API commit `d39ac27` (`dev`), web commit `1faa51c` (`dev`).
- API (`internal/...`):
  - SEC-001 `auth/service.go`: added `token_type` to `Claims`; `signJWT` stamps `"session"`; `ParseJWT` rejects non-session types. Exam-access tokens (same HS256 secret) can no longer reach `AuthRequired` routes. `testutil/jwt.go` MintSessionJWT now stamps the type.
  - SEC-002 `examattempt/handler.go`+`dto.go`: `Start` uses `ContextKeyUserID`, dropped body `user_id` from `StartExamRequest`. (`StartSession` already context-correct.)
  - SEC-003 `studentanswer/repository_gorm.go`: `SaveAnswer` is now update-only (no insert) → unassigned question = `ErrNotFound` (handler maps 404). Slots are pre-created at attempt Start; Submit already guarded via `validQuestionIDs`.
  - SEC-004 `examaccess/service.go`: `issueToken` enforces `ExamCodeExpiresAt` (nil/past denied, `ErrCodeExpired`).
  - SEC-005 `examattempt/repository_gorm.go`: `Submit` finalizes conditional `WHERE submit_time IS NULL` + `RowsAffected==0 → ErrAlreadySubmitted` (atomic finalize).
  - SEC-006 `examsession/repository_gorm.go`: `UpdateSeats` floors at 0 via `GREATEST(current_seats + ?, 0)`. **PARTIAL** — full delete+decrement atomicity across registration/session tables still needs a unit-of-work tx (TODO).
  - SEC-007 `config/config.go`: `normalizeAppEnv` collapses `APP_ENV` at load, fail-closed to `prod` for unknown/typo values; all `== "prod"` sites unchanged.
  - SEC-008 `interview/service.go`: `CancelBooking` checks `booking.UserID` before cutoff → `ErrNotFound`, no foreign-booking timing leak.
- Exam check-in code "disappears on reload" = NOT a bug. Code stored HMAC-hash only (correct), plaintext returned once. Web `AdminCheckInPage.tsx` now persists issued codes in **sessionStorage** keyed per session (survives reload, clears on tab close). No backend/DB change.
- TODO: (1) SEC-006 unit-of-work transaction for atomic cancel; (2) repos have NO DB test harness (fakes only) — SEC-005 RowsAffected guard + SEC-006 floor are untested at DB level; add sqlite/pg integration harness.
- Tests: `rtk go vet ./...` clean, `rtk go test -race ./...` 618 pass/30 pkg. Web `rtk bun run lint` clean (4 pre-existing warnings). Plan: `~/.claude/plans/plan-the-fix-and-snuggly-clover.md`.

## 2026-06-29 Partial-Credit Checkbox + Heal Stale Objective Scores
- API commits on `dev` since last session: `7a7785e` perf(exam) batch answer persistence on submit; `58f78bd` fix(grading) partial-credit checkbox + heal stale objective scores (this session).
- ROOT BUG (`58f78bd`): objective MCQ/CHECKBOX `score_received` persisted once at submit, never re-derived. If answer key (`is_correct`) set AFTER a student submitted, submit-time auto-grade stored 0; only the grading DETAIL view recomputed live, so the grading LIST, `is_graded`, `passed`, and the new theory threshold pass/fail all read stale zeros. Real attempt: list showed 5.5 (SHORT only) vs actual 12.5.
- Fix, all in API `internal/domain`:
  - `studentanswer.RecomputeAttemptGradeState` now re-derives objective scores from current answer key and PERSISTS `score_received` when drifted → heals on any submit or grade-save. Both callers (examattempt.Submit, UpdateScoreAndRecompute tx) are write paths.
  - grading list `score` = `COALESCE(SUM(sa.score_received),0)` (incl. manual SHORT), was cached `exam_attempts.total_score`.
  - CHECKBOX scoring all-or-nothing → PER-CHOICE PARTIAL CREDIT (admin spec image): `score = maxScore × matched / totalOptions` where a choice matches when selected-state == correct-state; blank answer (nothing selected) = not attempted = 0. One shared helper `studentanswer.CheckboxScore` used at submit + heal + detail (kills 3-way divergence that caused the bug). MCQ unchanged (single correct).
  - Added `AnswerForGrading.TotalChoices` (+ batched count query in `ListForAutoGrading`); removed dead `sameStringSet` in both pkgs; `TestCheckboxScore` encodes the spec image (5/3/4/0/2/0).
- PITFALL: stale attempts graded under old code DON'T self-heal until a grade action re-triggers `Recompute` — re-save any grade to fix. New submits auto-grade partial at submit.
- DB access for debugging: `set -a; . ./.env; set +a; PGPASSWORD=$DB_PASS psql -h $DB_HOST -U $DB_USER -d $DB_NAME` (host `10.60.2.3`).
- Validation: `rtk go build ./...`, `rtk go vet ./internal/domain/...`, `rtk go test -race ./internal/domain/{grading,studentanswer,examattempt}/...` 117 pass.

## 2026-07-02 Ponytail Audit + Dep Cuts (repo-wide)
- Ran `/ponytail-audit` both repos. Verdict: API lean (17 repo interfaces all test-mocked, keep); web had dep bloat.
- Web commit `926de8b` (staging): −5 deps (@xyflow/react, react-markdown, remark-gfm, remark-breaks, next-themes).
  - ApplicationFlow rewritten WITHOUT xyflow: nodes absolute in natural coords, canvas CSS-scaled (hand-rolled fitView: zoom=min(cw/(bw·(1+pad)), ch/(bh·(1+pad))), pad .2 desktop/.08 mobile), SVG cubic beziers with xyflow's exact control math (offset = d≥0 ? d/2 : 6.25·√-d), copied ArrowClosed marker, HTML pill labels at bezier t=.5 midpoint. Handle centers sit 3px outside node edges. Desktop nodes need `width:max-content` (mobile keeps w-80 — inline width overrode it, was bug). Pixel-diff vs xyflow: 0.8-1.0% AA-only.
  - RichTextRenderer markdown fallback → `whitespace-pre-wrap` div (legacy `**bold**` now renders literal; test updated).
  - Deleted dead `submitForm` (87 lines, exam-papers lib/api.ts), dead `shared/lib/index.ts` barrel, dead `.flow-node .react-flow__handle` CSS.
  - PITFALL: `shadcn` package is NOT just CLI — `globals.css` line 3 `@import "shadcn/tailwind.css"`. Removal breaks build. Keep as dependency.
- API commit `e1d9a5f` (dev): 4 byte-identical `*string→""` helpers collapsed into generic `utils.Deref[T]` (+ test). `go mod tidy` promoted go-sqlmock to direct.
- REJECTED findings: mongo-driver removal (gin v1.12.0's own go.mod requires it, `go mod why` misleading); shadcn dep removal (see pitfall); godotenv (real .env parsing).
- Web branch is now `staging` (not dev). User WIP left uncommitted: ExamPaperForm.tsx, AdminUsersPage.tsx, Navbar.tsx.
- Validation: web `bun run build` + vitest 135 pass (36 files); api `go vet` + `go test -race ./...` 646 pass (32 pkgs). Live check: 5 nodes/6 edges render, console clean. Screenshots in parent `.jez/screens/flow-{before,after}-{desktop,mobile}.png`.

## 2026-07-02 MCQ Negative Marking + Backend-Authoritative Exam Time (dev)
- Both repos switched staging → `dev` (api fast-forwarded to `7905e2c`). Duration flow (paper `duration_minutes` → freeze `duration_seconds` at admin start, round start/end = estimate only) already existed on dev from `e5fb341` — no change needed there.
- API (uncommitted on `dev`):
  - MCQ negative marking: new `studentanswer.MCQScore(max, correctIDs, selectedID)` — correct→max, unanswered→0, **wrong→flat −1**; attempt totals raw-summed, MAY GO NEGATIVE (user choice, no clamp). Used by all 3 scoring sites: examattempt Submit auto-grade, `objectiveScore` heal path, grading `scoreSingleChoice` (read-side mirror). Pass threshold ≥50% unchanged.
  - Server-side submit deadline: `Submit` loads session, rejects past `RuntimeDeadline()+30s grace` with new `ErrTimeExpired` → handler 409 `time_expired`; nil session → 404. Tests: `TestMCQScore`, submit −1/negative-total cases, `TestServiceSubmitRejectsAfterDeadline`; `newSubmitTestRouter`+submit service tests now need `inProgressSession()`.
- Web (uncommitted on `dev`): backend is SOLE time authority. Draft (`nacl-exam-draft:*`) no longer stores `remainingSeconds`; countdown anchored to `deadlineAtRef = Date.now()+server remaining_seconds*1000` and re-derived each tick (tab-sleep-proof); preview mode falls back to plain decrement. loadExam shows `durationSeconds` display-only.
- Time display verified correct, no changes: `combineDateTime` local→`toISOString()`, `Intl` formatters `Asia/Bangkok` 24h, RFC3339 round-trip.
- PITFALL: `bun install` needed after staging→dev switch (react-markdown etc. differ per branch).
- Web `clampWrittenScore` only gates manual SHORT/LONG input 0..max — fine with negative MCQ auto-scores.
- go-review verdict WARN → both MEDIUM findings fixed: `scoreSingleChoice` hardened (multi-correct key ≠1 → −1; multiple selections = malformed → −1; single pass, order-independent) + `TestScoreSingleChoice`. LOW (`err.Error()` to client) skipped — matches existing pattern.
- COMMITTED: api `7e2998c` feat(exam) MCQ negative marking + server-side submit deadline; web `ca29913` fix(exam) backend sole time authority. No Co-Authored-By per user pref.
- Validation final: api `go vet` clean, `go test -race ./...` 648 pass (30 pkg); web vitest 135 pass, lint 0 errors; react-doctor on diff: no issues.
- TODO: e2e smoke BLOCKED — DB `10.60.2.3` unreachable off lab network (create paper→round→start→wrong MCQ→−1 shown, reload resume = server remaining, late submit → 409 `time_expired`). Run when on lab net.

## 2026-07-03 Exam Model Cleanup (dev, uncommitted)
- API: legacy `ExamSession.Status` FULLY removed — field, `Effective*` fallbacks (now plain ""-defaults), dual-writes in Create/UpdateRegistrationStatus/service Update, `PATCH /exam-sessions/:id/status` route+handler+service+repo `UpdateStatus`, `UpdateSessionStatusRequest`, response `status` json. NO DB backfill — user chose to drop/recreate whole database (GORM AutoMigrate creates fresh schema; stale `status`/`total_score` columns don't exist on fresh DB).
- API: `ExamAttempt.TotalScore`→`Score` (json+DB column `score`). Same-word-opposite-meaning drift fixed: grading's `TotalScore`=paper max stays. Ripples: examattempt dto/repo (`Submit` update map), studentanswer `AttemptGradeState.Score` + recompute tx map, examregistration derive, grading `GetAttemptDetail` SQL `ea.score`, exampaper export SQL/`ExportRow.Score`/CSV header `score`. Ignored `SubmitExamRequest.TotalScore` deleted.
- API: exampaper Create/Update request DTOs no longer accept `total_score`/`question_count` (server-computed via `RecomputeTotalScore`/editor save). NEW: paper duration must be >0 — `ErrInvalidDuration`→400 `invalid_duration` at Create/Update/editor save; examsession `UpdateExamStatus` STARTED requires paper with duration → `ErrPaperDurationMissing`→409 `paper_duration_missing` (kills silent EndTime−StartTime fallback for new starts; `PlannedDuration()` chain itself unchanged).
- Web: exam-rounds `types.ts` dead `ExamAttemptPayload` + `attempt`/`exam_attempt` fields + `ExamSession.status` deleted (zero readers; backend never emitted attempt keys). New `shared/lib/api/exam-status-error.ts` `examStatusErrorMessage` maps `paper_duration_missing` to Thai copy in AdminCheckInPage + ExamManagementPanel.
- Kept (explorer flags REFUTED on verification): `ExamSession.ResultPublishedAt` (grading raw SQL r/w), `ExamRegistration.Status` (admin PASS/FAIL PATCH, examinees page). `SubmitGrace`/`RuntimeDeadline` timing chain untouched.
- Swagger regenerated (`go run swag@latest init -g cmd/api/main.go -o docs --parseDependency --parseInternal`; swag not installed locally).
- Validation: api `go vet` clean, `go test -race ./...` 655 pass (30 pkg); web tsc clean, vitest 135 pass, lint 0 errors, build pass. go-review verdict pending.
- PITFALL: exam CSV export header changed `total_score`→`score` (earned). Anyone parsing old exports must adjust.
- Plan: `~/.claude/plans/check-the-exam-paper-purrfect-wigderson.md`.

## 2026-07-03 Timeout Submit 401/403 Fix (dev, uncommitted)
- User re-requested duration flow + MCQ −1: BOTH already on dev (2026-07-02 entries) — no change; only the timeout submit bug was real.
- ROOT CAUSE: exam-access JWT expiry was EXACTLY `RuntimeDeadline()` (`examaccess/service.go:171`), so `ExamAccessRequired` middleware 401'd the t=0 auto-submit BEFORE the service-level 30s `submitGrace` could apply (grace was dead code). Then frontend reset to code entry; re-exchange 403'd (`ErrSessionFinished` + `ExamCodeExpiresAt` both past) = user's scenario 2.
- API fix (examattempt + examaccess): `submitGrace` → exported `SubmitGrace` (30s); token expiry, session-finished check, and code-expiry check in `issueToken` all now `+SubmitGrace`. Attempt Start unchanged (hard stop at deadline); already-submitted still rejected at exchange. Test expiry assertion updated.
- Web fix (`ExamClient.tsx`): timeout/section-timeout auto-submit rejected with 401/403 now goes straight to timeout result screen (draft kept, no code-entry reset — retry can't succeed past deadline; answers already saved per-answer). Manual submit 403 gets explicit Thai message, resetToCode=false.
- Validation: api `go vet` clean, `go test -race ./...` 648 pass (30 pkg); web vitest 135 pass, lint 0 errors. go-review verdict pending this session.
- PITFALL: GateGuard fact-forcing hook blocks FIRST Edit/Write per file per session — state importers/API/instruction facts then retry (or `ECC_GATEGUARD=off`).
- TODO: same lab-network e2e smoke as 2026-07-02 entry, now also: let timer expire → auto-submit 200; >30s past deadline → exchange 403 / submit 409.

## 2026-07-03 Session Status Clock + Admin Projector Clock Page (dev, COMMITTED by user)
- Feature: exam time box shows session status live; new fullscreen admin clock page for exam-room projector. Committed by user (squashed with their own WIP): api `2a5443d`, web `b81e1c1`.
- API (`examsession/dto.go`): `ExamSessionResponse` += `duration_seconds` (always, from `PlannedDuration()`) and `remaining_seconds` (`*int,omitempty`, ONLY when `EffectiveExamStatus()==STARTED && StartedAt != nil`, `max(int(time.Until(RuntimeDeadline()).Seconds()), 0)`) — same math as examattempt so both endpoints agree. Dead `65*60` guard removed from `examattempt.ToStudentStartResponse` (PlannedDuration guarantees positive); `SubmitGrace`/token TTL untouched. Tests: `TestToResponseFields` 7 subtests in `model_test.go`.
- Web new hook `src/features/exam/useSessionClock.ts` (3 consumers): polls public `GET /api/exam-sessions/:id`; WAITING→5s poll "ยังไม่เริ่มสอบ"; STARTED→anchor `deadlineRef=now+remaining*1000`, 1s tick + 15s re-anchor; FINISHED→"จบสอบแล้ว" stop. Cancelled guard in tick + AbortController per effect run.
- `ExamClient.tsx`: hook enabled pre-attempt only (`!attemptId`, not finished/timeout); 3 pre-attempt ExamFrame branches use `clock.timeLabel ?? "ยังไม่เริ่มสอบ"`. PITFALL/root-cause: before 6-digit code exchange NO session id exists → hook can't poll → old `formatTime(65*60)` fallback showed fake 01:05:00; static-label fallback is deliberate. Taking-phase `deadlineAtRef`/auto-submit untouched.
- `AdminExamPaperPreviewPage.tsx`: session discovery (events→EXAM event→`listExamSessionsByEvent`→filter paper_id, prefer STARTED else earliest non-FINISHED), non-fatal; clock label w/ static fallback.
- NEW `/admin/clock` (`routes.admin.clock`, sidebar NavItem "นาฬิกาห้องสอบ", lucide Clock): `src/features/admin/clock/AdminClockPage.tsx` — card-grid session picker (name/room/Thai date+time/status badge) → `fixed inset-0 z-50` fullscreen overlay, `text-[16vw] tabular-nums`, `?session=` seed param, "เปลี่ยนรอบสอบ". Under admin layout → AdminRouteGuard applies.
- Reviews: go-review (all findings fixed: nil-StartedAt guard, max() builtin go1.26, dead guard, 2 extra tests), react-review no CRITICAL/HIGH (3 MEDIUM fixed; pre-existing `submitAttempt`-dep countdown-stutter in taking-phase timer effect left as debt). Opus recheck FAILED (session limit) — Fable rechecked committed diffs instead: invariant intact, `ensureSessionInProgress` only relocated.
- Verified live in browser: WAITING code screen shows "ยังไม่เริ่มสอบ"; clock page picker + fullscreen FINISHED state render. STARTED live e2e NOT run (no admin identity; dev-token user ids not in DB — TestAccountSwitcher `admin_mali` id `2222...` returns user not found; lab-net e2e TODO).
- PITFALL: long-running `go run` API binary was STALE (predates even `status`-field removal) — restart `go run ./cmd/api` after backend changes; new fields verified via curl after restart.
- Validation: api `go vet` clean, `go test -race` 663→(post-squash exam domains 79) pass; web vitest 136 pass, lint 0 errors, build pass w/ `/admin/clock` route.

## 2026-07-04 Question Navigator Scroll Spy (web, uncommitted)
- User: grading + exam-paper question navigation "navigable and accurately". Jumps already worked (`scrollIntoView` on `#gq-*`/`#q-*` anchors); missing piece was current-question highlight.
- NEW `src/shared/hooks/useScrollSpy.ts`: IntersectionObserver over element ids, `rootMargin "0px 0px -55% 0px"` (top-45% band = current), topmost-visible wins, fallback last-element-above-viewport; re-observes on id-list change (join-key dep). Observes OUTER anchor wrappers — safe with `LazyMount` (inner content unmounted offscreen, wrapper always present).
- `GradingSubmissionPage.tsx`: spy over `visibleQuestions` → `currentId` prop to grading `QuestionNavigatorPanel`; panel cell gets `aria-current` + `ring-2 ring-logo` (edited styling kept).
- `ExamPaperForm.tsx`: spy over `draft.questions` (`q-${localId}`) → `currentId` to admin `QuestionNavigatorPanel`; same ring + `aria-current` layered over amber/emerald completeness + dirty dot.
- Exam-taking `QuestionNavigator` untouched (single-question, already correct — was the style reference).
- Validation: `rtk bun run build` pass, vitest 136 pass, lint 0 errors (fixed own set-state-in-effect error by relying on IO initial callback). No browser verify yet.
- COMMITTED web `db10e99` on dev, pushed.

## 2026-07-04 API dev: ParkinPot Commits Reverted (pushed)
- User asked to remove phakinplot's 2 latest dev commits, keep iIFortxne/NukerDucker. Chose REVERT over history rewrite (user picked; no force push); kept Archer-SN `22be2f9`.
- API dev: `d3999c4` reverts `7269128` (ensureSessionInProgress helper), `9f2ebce` reverts `c60f3b5` (MCQ −1 wrong/+2 right rescore). Both reverts clean; helper still exists via NukerDucker refactor `3c05e25`, build unaffected.
- Done in scratch worktree — local API checkout stays on `staging` (dirty: grading/studentanswer WIP + untracked `cmd/recompute-scores/`), untouched.
- Validation before push: `go build`, `go vet`, `go test -race ./...` 659 pass/30 pkg. Pushed `22be2f9..9f2ebce dev->dev`.
- NOTE: ParkinPot's MCQ scoring change is now UNDONE on dev — if −1/+2 scoring was wanted, it needs a reimplementation, not a re-merge.

## 2026-07-04 Grading Score-Heal WIP Committed + dev→staging Merge (pushed)
- Staging WIP moved to dev via stash→checkout dev→pop (clean 3-way; ParkinPot `return 2.0` vs dev `maxScore` auto-resolved). Commit `7f18535` on dev, pushed.
- WIP content: grading `Service` gains `AttemptHealer` dep (satisfied by `studentanswer.GormRepository.HealAttempt`); `GetAttemptDetail` heals stored objective scores from current answer key then reads DB verbatim — deleted grading-side `normalizeAttemptDetailScores`/`scoreSingleChoice`/`scoreMultipleChoice` duplicate scoring. Stored `student_answers.score_received`/`exam_attempts.score` = single source of truth. New one-off `cmd/recompute-scores/` backfill tool (compiled `recompute-scores` binary left untracked, NOT committed).
- Merged dev→staging `487ba99`, pushed. Staging history already had ParkinPot commits; merge brought reverts so their content is gone (`return 2.0` absent, `maxScore` back). MCQ negative marking itself (−1 wrong) predates ParkinPot (`7e2998c` NukerDucker) and REMAINS.
- Validation dev: build/vet clean, `go test -race` 660/31 pkg. Staging post-merge: 668/31 pkg. Both pushed.
- Local API checkout ends on `staging`, clean except untracked binary.

## 2026-07-05 Exam Code Ownership + Tab-Switch Anti-Cheat (committed, not pushed)
- Plan `immutable-munching-moler.md` (repo root) fully done: backend Parts 1.x were pre-committed as API `b238b28` "backend phase 1 done"; this session verified state, finished docs, ran full verification, and committed remainders.
- API `dev` commit `9666cc9`: `AdminExamRegistrationResponse.TabSwitchCount *int` (rides attempt), CLAUDE.md route table exchange PUBLIC→AUTH, DEVELOPMENT.md public list fix. `database_er_diagram.txt` already had `tab_switch_count`.
- Web `dev` commit `a65970b` (18 files): login-gated code entry card + Thai `code_owner_mismatch`/`unauthorized` messages, sessionStorage `nacl-auth-return-to` OAuth returnTo, `useTabSwitchGuard` (visibilitychange, taking-phase only), `TabSwitchWarningDialog` escalation 1–3, auto-submit on 4th + ResultScreen notice, server count via `POST /exam-attempts/:id/tab-switch` (resume-restored, draft-mirrored), admin examinees column, api client fix `payload.code ?? payload.error`.
- Contract: `/api/exam-access/exchange` now AUTH (session cookie; code owner must match → 403 `code_owner_mismatch`; mismatch does NOT count toward lockout — anti-griefing). Deploy backend+frontend together.
- Validation: `go vet` clean, `go test -race` 670/31 pkg; web lint 0 errors (47 pre-existing warnings), vitest 144/36. React-doctor hook warnings on ExamClient = pre-existing effect-chain/context patterns, not regressions.
- Both commits on local `dev`, NOT pushed. E2E curl matrix + browser tab-switch walkthrough from plan §Verification not run.

## 2026-07-05 Exam Info Popover Real Weights (uncommitted)
- Exam header "i" popover (`ExamWeightInfo`) now computes category totals + percentages from real questions instead of the 10-row placeholder in `exam-weights.ts`.
- API: `StudentExamQuestion` gains `score` (json `score`); `ToStudentStartResponse` loads `paper_questions` by paper and sets score = `paper_questions.score` if >0 else `questions.default_score`. Vet clean, examattempt tests 57 pass.
- Web: `ExamQuestion.score: number` (data-source maps `score ?? 0`); `exam-weights.ts` rewritten to `computeExamWeights(questions)` (group by category first-seen, palette cycled) + `examWeightPercent(score, total)`; `ExamWeightInfo` takes `questions` prop, returns null when total ≤ 0; `ExamFrame` optional `questions` prop passed from `ExamClient`, `ExamPreviewClient` (practice questions score: 1 each), `AdminExamPaperPreviewPage`; preview mappers map score (`assignment.score` fallback `default_score`, builder draft `question.score`).
- Validation: web lint 0 errors, build green, vitest 143/144 — the 1 fail (`SampleScreen.test.tsx` multiple /เขียนตอบ/ match) is PRE-EXISTING, confirmed on stashed clean tree.
- Changes uncommitted in both repos.

## 2026-07-05 SHORT Keyword Auto-Grading (committed, not pushed)
- Plan `i-want-autograding-with-soft-newell.md` (repo root) complete. Backend steps 1–4 were already implemented pre-session (uncommitted on API `dev`); this session added tests + frontend.
- Semantics: `ShortScore(maxScore, correctKeywords, textAnswer)` in `studentanswer/repository_gorm.go` — exact match multi-accept, keys split on `|`/`,`/newline, normalize = trim+lowercase+collapse-whitespace. Match → full score + `is_auto_graded=true`; no match or empty key → (0,false), stays in manual queue. Manual override wins everywhere and clears the auto flag. Heal pass (`RecomputeAttemptGradeState`) re-derives on keyword change and un-grades a stale auto-match.
- New column `student_answers.is_auto_graded` (AutoMigrate). Exposed via studentanswer + grading DTOs (`is_auto_graded`).
- Submit behavior note: every non-manual SHORT answer gets an `AutoGradeAnswerUpdate` (score 0/flag false on no-match) — harmless write, tests assert flags.
- Tests added: `TestShortScore` (11 cases, studentanswer/service_test.go); `TestServiceSubmitAutoGradesChoiceAnswers` extended with SHORT keyword match/no-match/no-keywords/manual-override + `wantAuto` flag assertions (examattempt/service_test.go).
- Web: `grading.api.ts` types gain `is_auto_graded`; `WrittenGradingPage.tsx` per-answer badge ตรวจด้วยมือ (green) / ตรวจอัตโนมัติ (คีย์เวิร์ด) (blue-300/50/600 raw Tailwind — theme `blue-5` is dark gray, unusable for badge bg) / รอตรวจ (orange); `QuestionFormCard.tsx` SHORT field relabeled "Accepted answers (auto-grading)" + format placeholder. GradingSubmissionPage renders no per-answer grade state — no badge added there.
- Validation: `go vet` clean, `go test -race ./...` 674/31 pkg; web lint 0 errors (47 pre-existing warnings), vitest 143/144 (same pre-existing SampleScreen fail, re-confirmed via stash).
- Post-review (ponytail + ecc:go-reviewer): heal SHORT branch consolidated to single drift-update block (−10 lines, behavior-equivalent); TestShortScore fixed (separator-only case now uses non-empty answer, added CR/CRLF cases, wrapped in t.Run subtests); Submit test wantAuto now asserted for all cases (nil guard dropped).
- Committed: API `dev` `a4e1eba` (amended) "feat(grading): keyword auto-grading for SHORT answers"; web `dev` `9573c72` "feat(grading): show auto-graded badge and keyword format hint". NOT pushed. React Doctor pre-commit flag was oxlint bunx-cache breakage, no real findings. Manual browser verification from plan §Verification not run.

## 2026-07-05 Loadtest Dropped-Submit RCA (uncommitted)
- Question answered: exam submit has NO queue — `POST /api/exam-attempts/:id/submit` fully synchronous (Gin goroutine → service.Submit → GORM → PG). Only implicit buffering = DB pool wait. Rejected request = lost; client must retry.
- Archer's bench "someone left out" root causes, both reproduced locally (k6 spike 200 VUs):
  1. `loadtest/loadtest.js` STALE vs API: (a) paper editor now requires `duration_minutes>0` → setup died; (b) submit sent login JWT as Bearer but token moved to httpOnly cookie AND submit route lives under ExamAccessRequired → 100% of submits 401'd. Fixed: added `duration_minutes:90`, submit uses `examAuth` (exam-access token), dropped dead `jwt` const.
  2. Overlay `DB_MAX_OPEN_CONNS=250` > postgres default `max_connections=100` → `FATAL: sorry, too many clients already` (53300) → 72×500 on /dev/auth-token + 28×500 on /dev/exam-access, half the VUs dead pre-submit. Fixed: overlay now 90 with comment.
- Post-fix spike run clean: http_req_failed 0.0000, 200/200 attempts submitted in DB, submit p95 483ms.
- Archer's `http_req_blocked` max 26.9s = SYN retransmit backoff (1+2+4+8+16s) → listen backlog overflow on his machine; NOT reproduced locally (run finishes ~2s). Park unless it recurs.
- Known load-sensitive bug NOT fixed (flagged only): `service.Submit` check-then-write race on `SubmitTime` (service.go:337) — no row lock, concurrent double-submit can double-run grading.
- Loadtest evidence workflow: `run.fish` writes `loadtest/last-run-summary.json` (--summary-export); Grafana dashboard JSON export contains NO data — need summary json, terminal output, panel CSV, or InfluxDB query.
- Edits uncommitted: `loadtest/loadtest.js`, `loadtest/docker-compose.loadtest.yml`. Killed user's local `api` dev process (held :8080) to run compose — restart with `go run ./cmd/api/main.go` if needed.

## 2026-07-05 Submit Load-Capacity Fixes (uncommitted)
- Goal: exam submit (80/round real, target 400 = 5x) + portfolio submit at 150-question papers. Plan `can-you-look-through-frolicking-finch.md`.
- Exam hot paths de-N+1'd:
  - Attempt start: 150 per-question `Create` INSERTs → single `CreateBatch` (new `studentanswer.Repository` method, `CreateInBatches(...,100)`); `examattempt/service.go` builds slot slice.
  - `ApplyAutoGrades` (submit auto-grade): 150 sequential UPDATEs in one tx → single `UPDATE ... FROM (VALUES ...)` with `?::uuid/::double precision/::boolean` casts.
- Config/limits: `DB_MAX_OPEN_CONNS` default 25→100 (compose postgres now `-c max_connections=200`); new `RATE_LIMIT_EXAM` (default 300/min per-user) on `/student-answers` autosave group (was RateLimitGlobal 100 → 429s at 150-question bursts).
- `MAX_UPLOAD_SIZE` was DEAD config: global `RequestSizeLimit(10MB)` 413'd any portfolio >10MB before handler. `RequestSizeLimit(maxBytes, uploadMaxBytes)` now content-type-switched: multipart → MAX_UPLOAD_SIZE (50MB), JSON → MAX_REQUEST_SIZE. New test `TestRequestSizeLimit_MultipartUsesUploadLimit`.
- `cmd/api/main.go`: `r.Run` → explicit `http.Server` (ReadHeader 10s, Read/Write 2m, Idle 60s) + SIGINT/SIGTERM graceful shutdown (30s); `r.MaxMultipartMemory = 8MB` (gin default 32MB/upload RAM → 8MB).
- Portfolio: pg 23505 in repo `Create` → `ErrAlreadySubmitted` (409, was 500 on TOCTOU dup submit); `ToResponses` settings fetched once (was N+1 per row + dup query in Submit path).
- loadtest.js default PAPER_QUESTIONS 20→150; overlay `DB_MAX_OPEN_CONNS` 90→150, `RATE_LIMIT_EXAM=50000`. Worst-case cmd: `k6 run -e VUS=400 -e PAPER_QUESTIONS=150 -e K6_SCENARIO=spike`.
- Docs: api CLAUDE.md env table + .env.example (event-day note: RATE_LIMIT_STRICT per-IP on /auth breaks shared school NAT logins — raise to ~100 for event; `SetTrustedProxies(nil)` collapses per-IP buckets behind LB, flagged not changed).
- Validation: `go vet` clean, `go test -race ./...` 688 pass / 31 pkgs. NOT run: k6 400-VU spike, 45MB upload manual check. All uncommitted on API repo.
- Known remaining (flagged, unchanged): service.Submit SubmitTime check-then-write race (double grading); rate limiter + examaccess lockout per-process (single instance assumed); frontend autosave batching (web repo).

## 2026-07-06 PDPA 2026 Policy + Editor Image Rehost (web, COMMITTED dev, merged staging)
- PdpaPage.tsx fully rewritten to mirror repo-root `นโยบาย PDPA.txt`: 10 sections TH+EN, email support@→nacl@kmitl.ac.th, effective 5 กรกฎาคม 2569 / 5 July 2026, fixes หนาที่ typo.
- Editor external-image rehost feature (was uncommitted work) confirmed complete + committed: RichTextEditor `rehostExternalImages` on onUpdate → `POST /api/exam-assets/from-url` (admin-gated, SSRF-guarded backend) → serves via `/api/exam-assets/` proxy. CSV import rehost already live on API side (`exampaper/import.go resolveImageURL` → `imagefetch` → `UploadExamAssetBytes`).
- Removed test scaffolding `images.immediate.co.uk` remotePattern from next.config.ts (restored file to HEAD, so not in commit).
- Commit `e57d32c feat(exam-papers): auto-rehost pasted external images into exam-assets` on dev (3 files: RichTextEditor.tsx, exam-paper-editor.api.ts, PdpaPage.tsx). Lint 0 errors, build green, /pdpa prerenders.
- Merged dev→staging locally: merge commit `abd00e8`, zero conflicts. NOT pushed (user chose local only).
- WARNING before pushing staging: local staging was 3 commits behind origin/staging pre-merge → now diverged from origin/staging (origin has PR #31 merge `fb89f97` not in local). Pull/merge origin/staging before push. dev is ahead of origin/dev by 1.
- API side committed: `1140d9a feat(exam-assets): add SSRF-guarded external image rehost endpoint` on api dev (9 files, new internal/imagefetch pkg). Vet + race tests green pre-commit. api dev now ahead of origin/dev by 6, not pushed.
- API dev merged into api staging: merge commit f034c0a, zero conflicts, vet + race tests green post-merge. Back on dev. Api staging ahead of origin/staging (local only). Web staging already contained web dev — no new merge needed.

## 2026-07-07 Ponytail Audit-of-Audit (report only, nothing applied)
- Audited the 2026-07-02 audit's own commits: web `926de8b`, api `e1d9a5f`.
- API verdict lean: no leftover deref helpers; `boolValue` fallback semantics ≠ Deref; bezier negative-d branch is LIVE (n1→n2 desktop edge). Keep all.
- Web findings (unapplied): shrink handlePoint+controlPoint dual switches → DIR vector table (~30 lines); delete dead `flow-node` class token (CSS rule removed in same commit, no selector left); shrink edge-label 10-prop inline style → Tailwind class. Net ~−35 lines, 0 deps.

## 2026-07-07 Admin No-Event Guidance + สีหลัก→ไฮไลต์ (web, uncommitted)
- Fixed infinite skeleton when no EXAM/INTERVIEW event exists: `ExamRoundListPage.tsx` sets `sessions=[]` (and on fetch error), `InterviewSlotListPage.tsx` sets `slots=[]`/`roster=[]` when no INTERVIEW event or on error — `isLoading={x === null}` now resolves.
- Added `<Alert>` banner on both pages when events loaded but no matching event: explains event must be created first + button linking to `routes.admin.timeline` ("ไปสร้าง event").
- Disabled create buttons when no event: "เพิ่มรอบสอบ" (`!createOrEditEventId`), SlotTab "เพิ่มวัน" (`eventId === null`).
- Reworded timeline toggle in `AdminTimelinePage.tsx`: "แสดงรอบนี้ด้วยสีหลัก" → "ไฮไลต์รอบนี้บนไทม์ไลน์" (create+edit dialogs), card title สีหลัก/สีเทา → ไฮไลต์อยู่/แสดงเป็นสีเทา, help text ปิดสีหลัก → ปิดไฮไลต์.
- Lint: 0 errors, warnings all pre-existing.

## 2026-07-07 Interview Roster 404 RCA + Interview Dedupe (web uncommitted; BE fix pending)
- RCA: `GET /api/interview-bookings?event_id=` 404 (375ns router miss) — backend never had admin booking-list endpoint; `interview/routes.go` only registers POST, GET /mine, PATCH /:id/cancel. FE `listInterviewBookings` (admin RosterTab) calls it. Fix needs new admin route+handler+repo joining bookings×slots×users → `InterviewBookingRow` (student_id, name_th, email...). NOT implemented yet — backend edit needs user go-ahead.
- Dedupe: new shared `src/features/admin/components/NoEventAlert.tsx`; used by ExamRoundListPage + InterviewSlotListPage (replaced inline Alert dupes). SlotTab: 6 label+input blocks collapsed into local `Field` helper.
- Pre-existing repo-wide dupes noted, untouched: `AdmissionEvent` type declared in 7 files; baseline `bunx tsc --noEmit` not clean (exam/grading test fixtures).
- Duplicate checkbox/button fix: DataTable auto-renders selection checkboxes + Export CSV button. Removed SlotTab manual `sel` checkbox column (now `selectedRowIds`/`onSelectedRowsChange` controlled selection) and RosterTab custom "ดาวน์โหลด CSV" button/blob code (now DataTable `exportFileName`). RosterTab rows map `id` from `booking_id` — fixed pre-existing TS error.

## 2026-07-07 Interview Admin Endpoints Added (api, uncommitted)
- User approved backend edit. Added to `internal/domain/interview/`:
  - `GET /api/interview-bookings?event_id=` (admin) — `AdminBookingRow` join bookings×slots×users (status BOOKED, ordered by date/start), handler normalises nil→[].
  - `PATCH /api/interview-slots/:id` (admin) — `UpdateSlotRequest` pointer fields; validates HH:MM range, non-blank location, max_capacity ≥ current_booked. FE edit dialog previously 404'd too (route never existed).
- go-review BLOCK findings fixed: nil-deref (UpdateSlot now applies fields to fetched slot, no re-fetch), handler tests added for both endpoints (roles, 400/404/500, empty array), repo-error propagation tests.
- Deferred from review (flagged, not done): `interview_slots.updated_at` audit column; GORM map-key constants; HH:MM string compare is pre-existing idiom.
- `go vet` clean; `go test -race ./...` 739 pass. Backend needs restart to pick up routes.

## 2026-07-07 Interview Filters + Pagination (web, committed 9e4a43c)
- SlotTab/RosterTab: date+location TableFilterGroup + searchFilter (examinees pattern), pageSize 20.
- DataTable Columns dropdown skips empty-label columns (SlotTab actions no longer blank toggle).
- Check-in page: client-side pagination 20/page, DataTable-style footer.
- Earlier commits: api ad67281 (interview endpoints), web 86b824a (no-event guidance/dedupe/reword).
- User's own edits Step2Education.tsx + launch.ts still uncommitted, untouched.

## 2026-07-07 PaperID Nullable (api, staging)
- Bug: create exam round 400 `CreateExamSessionRequest.PaperID ... required`. FE omits paper_id for paper-mode (year 2) + computer rounds with no paper yet; DTO had `binding:"required"`.
- Root: paper_id is uuid FK → exam_papers.id. Empty string fails uuid cast, sentinel fails FK → must be NULL. exam_mode already encodes paper vs computer, so nullable paper_id is the clean rep (no sentinel).
- `PaperID string` → `*string` end-to-end: model.go (`gorm:"type:uuid"`, no not-null — column already nullable, NO migration), dto.go Create (`*string`, dropped required, ToResponse `utils.Deref`). Service Create/Update: trim-empty→nil, paper-mode force nil. UpdateExamStatus: paper-duration fetch skipped for paper mode (durationSeconds stays 0).
- examattempt.Start: paper-mode → new sentinel `ErrPaperModeSession` (409 `paper_mode_session`); nil paper → `ErrPaperNotFound` (404); else deref. examregistration repo_gorm: nil-guard both paperID collect + maxScore lookup. utils: added `Ptr[T]`.
- FE ExamRoundFormDialog unchanged (`paper_id: paperId || undefined` valid once BE relaxed).
- Validation: `go vet` clean, `go test -race ./...` 744 pass/33 pkg. Committed to `staging`.

## 2026-07-07 Year→exam-mode rule corrected (yr3/4 ineligible)
- New rule (user): yr1 → computer, yr2 → paper, yr3/4/unknown → ineligible for ANY round. Was: yr2 paper else computer (yr3/4 wrongly computer-eligible).
- BE `policy/eligibility.go` `ExamModeForYear`: yr1→"computer", yr2→"paper", else→"" (ineligible). eligibility_test.go updated (yr3/4/nil→""). No enforcement caller (dead except FE mirror) — kept honest. Did NOT add `EligibleForExam` (YAGNI).
- FE mirror `shared/lib/theory/exam-mode.ts` `examModeForYear(year?): ExamMode | null` (yr1 computer, yr2 paper, else null). Consumers: `session-data-source.ts` filter `=== expectedMode` → null matches nothing → yr3/4 get [] (no filter edit needed). `TheoryContent.tsx` added amber ineligible banner for `=== null`. session-data-source.test.ts: existing test now passes year 1, added yr3 empty-list case.
- Validation: BE `go vet` clean + `go test ./...` 745 pass/33 pkg; FE theory vitest 3 pass, tsc errors present but ALL pre-existing (ExamClient.test/grading.api.test `score`/`is_auto_graded`, untouched files). Memory `year-exam-mode-rule` updated.

## 2026-07-07 BE year-eligibility enforcement (was FE-only gap)
- User greenlit closing the gap. `examregistration.Register` now enforces year↔mode server-side.
- `examregistration.NewService` signature: added `userRepo user.Repository` (now `NewService(repo, sessionRepo, userRepo, codeSecret, settingsRepos...)`). Wired real userRepo in cmd/api/main.go:124 (userRepo already existed for portfolio). userRepo nil-guarded in Register like settingsRepo — `ponytail:` comment warns prod MUST inject or check silently skips.
- Register check (after settings/open checks, before seat): fetch user → nil ErrUserNotFound; `policy.ExamModeForYear(u.Year)==""` → ErrYearNotEligible (403 `year_not_eligible`); `session.EffectiveExamMode() != mode` → ErrExamModeMismatch (403 `exam_mode_mismatch`). New sentinels + handler.go mapping.
- Test churn: 11 NewService call sites got `nil` userRepo arg (year check skipped, behavior preserved). New table test `TestServiceRegisterEnforcesYearEligibility` (8 cases: yr1/2 match ok, yr1↔paper & yr2↔computer mismatch, yr3/4/nil ineligible, unknown user) with embedded-interface `fakeUserRepo`.
- Validation: `go vet` clean, `go test -race ./...` 754 pass/33 pkg.
- GIT (user: "commit to dev push and merge into staging" → chose strict dev→staging both repos): API commits paper_id(63c75d1)+policy(cc640b7)+enforcement(3f229c9) were linear on staging = origin/dev+3; ff-promoted onto dev, pushed, merged→staging. API origin/dev=origin/staging=3f229c9. WEB theory(78d3ff3) ff-promoted dev→staging. WEB origin/dev=origin/staging=78d3ff3. No hard reset needed (topology was linear). Both repos back on local dev.

## 2026-07-08 Ponytail-audit cleanup (web, dashboard hooks + headers)
- Actioned pasted ponytail-audit findings. Delete: `features/exam/components/IntroShell.tsx` (dead, 0 callers); `features/admin/components/AdminPageHeader.tsx` (inlined).
- Extracted `features/admin/dashboard/hooks/schedule-utils.ts` — shared `Schedule` type + 12 date helpers (parseDate, formatTime, datesToSchedule, minimumScheduleStart, addDays, defaultEditableSchedule, scheduleToDate, ensureEditableSchedule, ensureFutureSchedule, datesEqual, schedulesEqual). `settingToSchedule` generalized to `scheduleFromRange(openAt, closeAt)` — only field-name diff between the two hooks. usePortfolioEvent 292→~165 lines, useTheoryRegistrationSetting 268→~140. Both hooks now thin wrappers.
- Inlined AdminPageHeader → `<h1 className="mb-6 text-3xl font-bold text-foreground">Admin</h1>` (single title-only use in AdminDashboardPage).
- SKIPPED SectionHeader inline: audit said "one caller" but called 3× in BlueprintPage — inline would triple markup. Kept. SKIPPED RoundTone/StatusTone + AdminRouteGuard (author flagged acceptable).
- Validation: `bun run lint` 0 errors (51 pre-existing warnings, none in touched files). `bunx tsc --noEmit` clean on all touched files (remaining errors pre-existing exam/grading *.test fixtures — score/is_auto_graded, untouched).

## 2026-07-10 Audit: missing FKs + broken cancel booking (PLAN ONLY, committed for cross-device)
- Audit findings: (1) GORM `constraint:` tag on scalar field is a NO-OP — `interview_bookings.slot_id` CASCADE tag never created an FK; DB has ~23 FK-shaped columns with zero constraints (only user↔faculty/department/major FKs real). (2) Cancel booking 404s from UI: BE is `PATCH /api/interview-bookings/:id/cancel` (correct, SEC-008 + cutoff + txn), FE `ApplicationPage.tsx:280` calls `DELETE /:id`.
- Plan (user-approved scope: ALL FKs repo-wide, must not break prod DB): raw SQL in `automigrate.go` post-AutoMigrate — `ADD CONSTRAINT ... NOT VALID` in DO-block (duplicate_object swallowed) + soft `VALIDATE CONSTRAINT` that logs orphan warning instead of failing boot. FE fix = one-liner to PATCH /:id/cancel. `grading_score_audits` deliberately excluded (immutable audit snapshot). Full spec table in plan doc.
- NOT IMPLEMENTED — user implements on another device. Plan committed: API branch `plan/missing-fks-cancel-booking` (pushed), file `PLAN-missing-fks-cancel-booking.md` at repo root (docs/ is gitignored swagger output). NOTE: branch cut from `main` (checkout was on main this session, not dev/staging) — doc-only, rebase irrelevant.

## 2026-07-13 Exam e2e recheck (code trace + live browser run + 100-VU load test)
- **Code trace**: token TTL invariant SOUND (exam-access JWT exp = RuntimeDeadline+SubmitGrace(30s) `examaccess/service.go:195`; submit rejects `now > deadline+30s` `examattempt/service.go:352`; boundaries consistently exclusive `After`). userRepo IS injected (main.go:137) — year↔mode enforced. `exam_registrations.user_id` global-unique = documented intent (CLAUDE.md "one exam session per student"), not bug.
- **Live browser e2e (chrome-devtools, dev stack: nextpath-pg-e2e:5433, API 8081, web 3000)**: full pass — dev-login Anong(yr1) → register → admin check-in code → exchange → rules/sample → 3-question exam (MCQ/CHECKBOX/SHORT) → per-answer autosave 201s → reload draft-restore ✓ timer re-anchor ✓ → tab-switch warning 1/3 ✓ → manual submit ✓ score=10 auto-graded. Timeout path (1-min paper, Boon): deadline auto-submit fired, landed 0.023s past deadline, accepted in grace, timeout screen ✓. Past-grace exchange correctly rejected ("รอบสอบนี้สิ้นสุดแล้ว") ✓.
- **Load (user q: "100 users submit — crash?")**: NO. `loadtest/tests/exam-flow/spike100.js` (new, spike.js@100VU), k6 burst full-flow: 100/100 iters, checks 1106/1106, 0 5xx, submit p95 153ms max 166ms, whole burst 1.2s, pg backends peak 81 (pool 80), 0 panics. Rate limits raised via env for the run (defaults back after).
- **Findings for follow-up**: (1) 🔴 deadline auto-submit path untested in vitest (now proven live but still no regression test — fake timers); (2) 🟠 SHORT/text autosave fires per keystroke, no debounce — 21 chars = 21 POSTs, can hit RATE_LIMIT_EXAM 300/min for long answers; (3) 🟡 MCQ/CHECKBOX `AutoGradeAnswerUpdate` omits IsAutoGraded → stored false despite scored (service.go:374,378 vs SHORT :386) — grader UI flag misleading; (4) 🟡 double auto-submit at timeout (one 200 one 409, FE treats 409 as success — harmless; likely dev strict-mode double timer effect, verify prod build); (5) 🟡 result screen timer shows planned duration (00:30:00) after submit — cosmetic; (6) loadtest setup 409'd on singleton EXAM event — patched `exam-flow.js` setup with list-events fallback (committed? NO — working tree only). ShortScore is exact-match (not contains) — by design, unmatched → manual queue.
- Env notes: web dev runs on 3000 (WEB_PORT=3001 in .env not applied to dev script); session create ignores paper duration until STARTED (duration_seconds derived from end-start pre-start, from paper at start); exam code expiry = deadline exactly (grace only on JWT).

## 2026-07-13 Keyword auto-grade tested + findings 1-4 fixed
- **Keyword grade live test**: SHORT " Alpha " vs keywords "alpha,beta,gamma" → normalize (trim/casefold) matched → score 5, is_auto_graded=t; MCQ correct → 5, is_auto_graded=t (new); attempt score 10, is_graded=t. ShortScore = exact-match whole answer (repository_gorm.go:684), unmatched → manual queue (unit rows cover no-match/empty-key).
- **Fix 2 (BE is_auto_graded)**: examattempt/service.go MCQ+CHECKBOX AutoGradeAnswerUpdate now `IsAutoGraded: true`; studentanswer/repository_gorm.go Recompute heal branch persists `is_auto_graded=true` when scored||flag-false (manual-graded rows still skipped first). service_test.go wantAuto flipped true for choice cases. `go vet` clean, `go test -race ./...` 750 pass/34 pkg.
- **Fix 1 (FE autosave debounce)**: ExamClient.tsx upsertAnswer — text answers (answer.text !== undefined) debounced 600ms per-question via saveTimersRef map; choice answers still immediate; clearAnswer cancels pending timer (no resurrect); unmount effect clears all timers. Draft + full-set submit still authoritative.
- **Fix 3 (double auto-submit)**: root cause = `isSubmitting` state read stale by adjacent timer ticks. Added submitInFlightRef synchronous guard: set before await, reset on attemptId-missing / timeoutPastGrace / failure paths + on attempt start (fresh/resume); left true on success intentionally.
- **Fix 4 (vitest)**: ExamClient.test.tsx new "deadline auto-submit" test — fake timers (shouldAdvanceTime), startAttempt remainingSeconds:2, advance 5s → submitAttempt called exactly once with status timeout + timeout screen. 16/16 pass. tsc: no new errors (pre-existing fixture `score` errors remain). lint 0 errors.
- Anomaly (unresolved, one-off): first POST /exam-attempts/session/:id/start after dev exam-access returned 500 "failed to fetch attempt"; immediate retry 200 resume. Watch for recurrence.
- All changes UNCOMMITTED (both repos) + loadtest spike100.js/exam-flow.js fallback from earlier.

## 2026-07-13 Fixes committed (dev, both repos)
- API dev 9da58b5 `fix(grading): mark MCQ/CHECKBOX answers auto-graded` (service.go + repository_gorm.go heal + test expectations). loadtest changes deliberately excluded per user.
- WEB dev 5789366 `fix(exam): debounce text autosave, dedupe timeout submit` + abef12a `refactor(exam): keep countdown state updater pure` — react-doctor commit hook flagged side effects (clearInterval/submitAttempt) inside setRemainingSeconds updater = true root cause of double timeout submit; tick now computes outside updater with remainingSecondsRef fallback mirror (synced at payload load + attempt start). 16/16 vitest after refactor.
- Remaining react-doctor output on features/exam = pre-existing exhaustive-deps/style warnings, out of scope.
- STILL UNCOMMITTED (API): loadtest/tests/exam-flow/spike100.js (new) + exam-flow.js singleton-event fallback. Not pushed anywhere; local dev commits only.

## 2026-07-14 Removed session exam_mode — shared seat pool per round
- **Decision (user)**: year 1 (computer) + year 2 (paper) always sit in the SAME room/round with ONE shared seat count. No per-mode rounds, no "mixed" enum (mixed variant was implemented then discarded mid-session on user pivot). Delivery mode is now purely per-student via `policy.ExamModeForYear` (BE) / `examModeForYear` (FE) — year rule stays hardcoded there.
- **API (removed)**: `ExamSession.ExamMode` field + computer/paper consts + `EffectiveExamMode()` (model/dto/service/handler); `ErrExamModeMismatch` + registration mode check (registration now checks only year eligibility); `ErrPaperModeSession` + attempt-start session-mode gate; session Create/Update mode validation + paper-clearing-on-paper-mode; UpdateExamStatus now ALWAYS requires paper duration to start. DB column `exam_mode` still exists but is ignored (no migration to drop).
- **API (added)**: `policy.ExamModeComputer/ExamModePaper` consts; `examaccess.NewService` gains `userRepo` (wired main.go, nil-guarded) — `issueToken` now denies exam-access tokens per-student: year≠computer → `ErrPaperExamOnly` (msg reworded to student-based). This is THE gate keeping year-2 out of the digital exam (attempt start sits behind exam_access JWT). New test `TestIssueForRegistrationGatesPaperModeStudents`; eligibility test rewritten mode-less. `go vet` clean, `go test -race` 752 pass/34 pkg.
- **WEB (removed)**: `normalizeExamMode`; `TheoryTimeSlot.examMode`; session `exam_mode` filter in `loadTheoryTimeSlots` (now: ineligible year → [] early-return, eligible years see ALL open rounds); `exam_mode` from admin SessionRow/ExamSession types; exam-mode Select in ExamRoundFormDialog (paper select always shown, helper text explains shared-room rule). lint 0 errors, vitest 149 pass, build pass.
- UNCOMMITTED both repos.
- Committed 2026-07-14: API dev 048d574 (14 files, loadtest still uncommitted), WEB dev 0a141b9. Not pushed.

## 2026-07-17 Full e2e recheck on `main` — register→exam→grade→threshold→announce; new threshold bug found
- Both repos are on `main` now (clean, `origin/main` in sync at session start): api `f25f7a9`, web `4a452e8`. `dev` diverged 7/9 commits from `main` but the threshold/announce files are byte-identical (`git diff main dev -- AdminExamineesPage.tsx` empty; settings domain diff empty) — confirmed dev has the same feature, not drift.
- "Rank" = admin `/admin/examinees` ใช้เกณฑ์คะแนน (apply score threshold) button, NOT a leaderboard — no ranking/percentile feature exists in either repo (grep clean). "Announcement" = ประกาศผล button → `PUT /api/settings/theory {result_published}` (global, one row, all rounds).
- **Chain register→check-in→start→answer→submit→manual-grade verified working** on `main` via curl + live browser (fresh paper/session/3 students created for this test, since `main` has no dev-seed for exam users — `internal/bootstrap/seed.go` only seeds faculty/dept/major reference data, not users/papers/sessions; TEST_ACCOUNTS UUIDs had to be inserted directly into `users` via psql to use `/api/dev/auth-token`).
- **🔴 NEW BUG — `applyThreshold` (`nacl-nextpath-x-web/src/features/admin/examinees/AdminExamineesPage.tsx:269-297`) is not usable at real scale, reproduced live:**
  1. Fires one `PATCH .../status` per qualifying row via bare `Promise.all` over ALL 500 loaded rows (not the filtered/visible subset — reads `rows` state, ignores search/filter UI). At ~200 qualifying rows it trips the backend per-IP rate limiter: 99 got 200 (persisted PASS), 101 got 429 → `Promise.all` rejects → generic "ใช้เกณฑ์คะแนนไม่สำเร็จ" toast. The optimistic `setRows` flip is never rolled back on catch, so UI and DB both end up inconsistent and the admin is told it failed when 99 rows actually changed. Any round with more than ~100 qualifying students cannot complete this action.
  2. `examregistration/dto.go:105-112` (`AdminExamRegistrationResponse.ToResponse`) pre-derives FAIL for any PENDING+graded row scoring <50% of max — before the admin sets any custom threshold. Since `applyThreshold`'s target filter is `status === "PENDING"` (reading this same derived value, not the real DB column), a custom threshold below 50% can never promote those rows. Reproduced live: test student "boon" scored 4/10 (40%), displayed status was already "ไม่ผ่าน", threshold=3 (should pass 4≥3) had no effect on her.
  - Whether threshold-apply is meant to be global (one settings row, page titled "ทุกวันและทุกรอบ") is a product question, not asserted as wrong — items 1 and 2 are bugs regardless of that answer.
- **Announcement gate verified correct**: `/theory` (standalone) shows a passed banner on `status===PASS` immediately, no publish wait (matches 2026-07-14 commit intent). `/application` interview-round eligibility correctly stays locked pre-publish (`hasPublishedExamPass = theoryResultPublished && status==="PASS"`, ApplicationPage.tsx:215-217) and unlocks live the moment `ประกาศผล` is clicked. Did not check PENDING/FAIL student's `/application` view post-publish (untested, not expected to differ).
- **Local DB side effects from this test (`nextpath-pg-e2e` docker container, port 5433) — NOT prod, but not reset**: ~99 unrelated loadtest registrations got permanently flipped to PASS by the reproduced bug; `theory_settings.result_published` is now `true` globally; test student `11111111-...` (Anong) registration is now real PASS. Left running: API on :8081 (`go run ./cmd/api`, log `/tmp/nextpath-api-e2e.log`), web dev on :3000 (`bun run dev`, log `/tmp/nextpath-web-e2e.log`), docker containers `nextpath-pg-e2e` + `nacl-nextpath-x-api-minio-1`. Next session: decide whether to reset this DB or keep as scratch.
- TODO: fix `applyThreshold` — scope to the round/filtered rows being viewed (or confirm global is intentional and fix the atomicity/rollback + rate-limit-batching instead), and reconcile the two competing PASS/FAIL derivations (dto.go 50%-cutoff preview vs. admin's real `pass_threshold` setting).

## 2026-07-18 Admin UI Overhaul START (web dev branch)
- Intent: all /admin pages — responsiveness (≥360px), a11y, UX consistency, NEW BulkActionBar + batched bulk mutations (examinees/portfolios/check-in/users), status semantics centralization, minimal toolbars, contrast token --color-logo-ink. No dark mode. Admin only, no /grader.
- Plan: ~/.claude/plans/you-are-the-most-polymorphic-thunder.md (7 phases, 12 commits). applyThreshold bug confirmed ALREADY FIXED on dev (rank-select endpoint). Go API: no changes planned.
- Baseline screenshots: scratchpad before-*.png (1440/390). Dev stack: web :3000, API :8081.

## 2026-07-19 Admin UI Overhaul DONE (web dev, 11 commits c497eae..b4e5786, not pushed)
- Commits: DataTable conversion users+check-in / sidebar md+ & FAB de-conflict / responsive grids+wraps / minimal examinees toolbar (rank-select→Popover) / BulkActionBar+runBatched bulk mutations (examinees/portfolios/check-in/users) / --color-logo-ink contrast token / a11y labels+focus+DialogTitle / confirm dialogs (paper delete, exam start/finish, regen code, role→admin, publish×2, AlertDialogAction fix) / toasts+tooltips+Thai labels / dead code −531 (EventCalendar, exam-papers QuestionCard/ChoiceRow/GuidelineRow, 13× double AdminRouteGuard) / RegistrationControlCard+ApplicantStatsCard extraction (dashboard −230) / px-4 sm:px-6 containers.
- New shared: `admin/components/BulkActionBar.tsx`, `admin/lib/batch.ts` (runBatched concurrency 5 + test), `dashboard/RegistrationControlCard.tsx`. DataTable: dual-mode selection+onRowClick (`showSelect`), `rowAriaLabel` prop.
- Verified live (chrome-devtools): users 390px scrolls w/ checkboxes; sidebar rail present at 768 (was absent 768-1024); examinees bulk bar works ("เลือก 2 รายการ"); console 0 errors. After-shots scratchpad after-*.png (session-scoped tmp).
- Validation every slice: lint 0 err (37 warn, was 46), vitest 151 pass, tsc no new errors, build green. React Doctor commit-hook noise: staged-scope warnings, diff-scope clean.
- NOT done (flagged): getStudentName/searchFilter dedupe (marginal, differing signatures); SlotTab slot create/edit UI (BE PATCH exists, FE view-only); DataTable empty/skeleton→AdminState unify; grader pages untouched per scope.

## 2026-07-19 Audit Log Upgrade DONE (api dev 7b9e16f, web dev c9ee86d, not pushed)
- User ask: audit log show who sent what + failures (CRUD). Chosen: middleware auto-log.
- API: new AuditLog middleware on protected group logs POST/PUT/PATCH/DELETE with actor, method, path, HTTP status, scrubbed JSON body (<=2KB, redacts password/token/secret/authorization/otp/cookie) into dormant details jsonb. New columns method/path/status via AutoMigrate. WriteAsync(c,...) sets dedup skip-flag; 9 named-event calls moved AFTER response write (status was always 200 before). Bug fixed: DELETE_USER logged deleted user id as actor -> FK violation meant those rows were NEVER written; now logs acting admin. /api/logs + /by-user accept limit/offset (symmetric 400 on malformed). Daily retention goroutine AUDIT_LOG_RETENTION_DAYS (default 90, 0=off). Path truncated to 255 runes. Excluded by group placement: exam autosave/tab-switch/attempts, /api/auth, /api/internal.
- Web: audit page status pill (fail>=400 red w/ code, 200-399 green, legacy em dash), METHOD /path rows (uuid/numeric segments -> :id for filter dropdown), expandable detail rows via real disclosure button (aria-expanded/aria-controls), path in search.
- Workflow: Sonnet implement -> ecc:go-review + ecc:react-reviewer -> Opus fix (10 findings: 2 Go MEDIUM status/paging, 3 React HIGH a11y, etc).
- Verified: go vet + go test -race 779 pass; bun lint 0 err/test 151/build green; live curl: 400 row password [REDACTED], 403 row student actor, limit=5 works; browser expand OK, console clean.
- NOT pushed. Named events (SUBMIT_EXAM etc) still log target-style user_id for CREATE/UPDATE_USER (commented, intentional).

## 2026-07-19 dev → staging merge (local, not pushed)
- api: staging 56dd6a1 (merge --no-ff dev); web: staging cbd38af
- Merge messages summarize feats/fixes (audit middleware+retention, camellya internal API, exam mode/seats, admin UI overhaul, exam autosave fixes)
- `git diff dev staging` empty both repos — trees identical to dev tips already verified green (go test -race 779 pass, bun lint/test/build)
- 2026-07-19: theory Read More route fix (/commingsoon → /theory) committed staging ee0b03e + cherry-picked dev a0ae19d (web repo, local)

## 2026-07-24 Exam Statistics Dashboard DONE (api+web dev, not committed)
- User ask: stats on what examinees got mostly right/wrong, graphs, cover all areas (categories). Budget-capped: Fable planned, Sonnet subagents implemented+reviewed+fixed.
- API (grading domain, additive): `GET /api/grading/sessions/:session_id/stats` — summary (attempts/graded/avg/pass_rate), per-question buckets (correct ≥max / partial / incorrect ≤0 answered / blank / pending = SHORT ungraded, excluded from rate denominators), per-category rates, 10-bucket score histogram (graded attempts only, pass = ≥50%). Two flat parameterized queries (per-attempt totals + per-answer rows) + in-memory aggregation in new `stats.go` (ponytail: SQL GROUP BY if >10k attempts). Uses `pq.order_index` NOT `sa.order_index` (shuffled per-attempt!). `stats_test.go` covers buckets incl. unanswered-SHORT→Pending precedence. go build/vet clean, grading 44/44 (-race), full suite 787 pass.
- Web: `/admin/exam-rounds/[sessionId]/stats` → `features/admin/exam-rounds/components/ExamStatsPage.tsx` + `lib/stats.api.ts`; link from ExamRoundDetailPage ("ดูสถิติผลสอบ"); `routes.admin.examRoundStats()`. NEW DEP: recharts via `shadcn add chart` (`shared/components/ui/chart.tsx`). 6 sections: stat cards, per-question stacked bar (sort: order|hardest), difficulty line chart Q1→Qn (user mid-task add), category bar, histogram w/ 50% ref line, hardest/easiest top-5 tables. dataviz palette (status scale correct/partial/incorrect + neutral grays + brand blue).
- Review fixes applied: auth-token race flashed not-found card (now gates on authLoading, not-found gated !error), aria-pressed sort toggle + role=group, aria-labels on 4 ChartContainers, dedup hardest comparator. Skipped by design: AbortController (cancelled flag suffices).
- Live-verified: API run vs e2e Postgres :5433 (nextpath-pg-e2e, load-test data 206 attempts), dev token `/api/dev/auth-token`, curl session d3a4c649: 100 attempts bucketed correctly, graded_count 0 = genuine (all SHORT pending). FE verified earlier via mocked preview route (reverted). tsc: 0 errors in new files (12 pre-existing in old test files).
- NOT done: browser test of real page against real API (only mocked preview); commit (user decides).
