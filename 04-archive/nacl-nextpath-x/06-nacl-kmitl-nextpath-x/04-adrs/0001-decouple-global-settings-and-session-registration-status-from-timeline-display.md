---
title: "ADR-0001: Decouple Global Settings and Session Registration-Status from Timeline Display"
tags: [nextpath-x, adr, security, settings, timeline]
component: full-stack
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# ADR-0001: Decouple Global Settings and Session Registration-Status from Timeline Display

Related: [[../01-architecture/03-full-stack-data-flow]], [[../01-architecture/02-backend-architecture]].

## Context

NextPath X shows applicants a public timeline (`event.Event`, `GET /api/events`) of portfolio/exam/interview rounds with a `Name`, `Type`, `StartTime`/`EndTime`, and an `IsActive` flag. It's tempting — and was apparently an earlier design, per the "decouple... detached from timeline events" language in the session log below — to use that same timeline to decide whether an action is actually allowed (can I submit my portfolio right now? can I register for this exam session right now?).

Three separate mechanisms exist in the current codebase for "is X open":

1. `Event.IsActive` (`internal/domain/event/model.go`) — a boolean on the timeline event.
2. `ExamSession.RegistrationStatus` (`OPEN`/`CLOSED`, `internal/domain/examsession/model.go`) — per-session, admin-toggled.
3. `TheorySetting`/`PortfolioSetting` (`internal/domain/settings/model.go`) — global windows (`RegistrationOpenAt`/`CloseAt`, `SubmissionOpenAt`/`CloseAt`) plus a `RegistrationMode`/`SubmissionMode` switch.

## Decision

**Timeline events are display-only.** `Event.IsActive` is never read by any authorization or eligibility-gating code. Confirmed by grep across all of `internal/` (excluding `_test.go`) for `IsActive`: every hit is in `internal/domain/event/handler.go` or `internal/domain/event/dto.go` — request/response plumbing for the admin timeline CRUD UI. Nothing in `examregistration`, `portfolio`, `examaccess`, or `middleware` reads it.

**Actual access control lives in two other places, and they are also separate from each other:**

- Session-level: `examregistration.Service.Register` (`internal/domain/examregistration/service.go`) checks `session.EffectiveRegistrationStatus() != examsession.RegistrationStatusOpen` and returns `ErrSessionNotOpen` if closed. This is a per-`ExamSession` admin toggle (`PATCH /api/exam-sessions/:id/registration-status`), independent of that same session's `ExamStatus` (`WAITING`/`STARTED`/`FINISHED`, toggled via a *different* endpoint, `PATCH /api/exam-sessions/:id/exam-status`).
- Global-window level: the same `Register` method also calls `settings.NewService(s.settingsRepo).GetTheory(ctx)` and checks `setting.IsRegistrationOpen(time.Now())` — a site-wide window independent of any individual session. `portfolio.Service.Submit` (`internal/domain/portfolio/service.go`) does the analogous check via `PortfolioSetting` (`isSubmissionOpen`).

This is confirmed as a deliberate change, not an oversight, by dated entries in `~/KnowledgeVault/05-ai/projects/nacl-nextpath-x/session-state.md` (2026-05-24, quoted verbatim):

> "Portfolio availability/result publication is now global settings, detached from timeline events. Use public `GET /api/settings/portfolio` and admin `PUT /api/settings/portfolio` with `submission_mode`, optional schedule fields, and `result_published`."
>
> "Timeline `/api/events` is display-only for dynamic timeline; do not use events to decide whether portfolio upload is open or portfolio results are visible."

The task brief that requested this ADR referred to the session-level field as "per-session `registration_status`" — that framing is accurate once the owning model is identified: it's the `RegistrationStatus` field on `ExamSession`, not a field on `ExamRegistration` (which instead has `IsCheckedIn`/`Status` for the individual registrant's own state — see [[../05-schema-and-data-quirks/02-exam-access-token-exchange-flow]]).

## Consequences

- **Positive**: admins can build/preview a timeline (including future/inactive events) without accidentally opening registration or submission windows early — the two concerns can't cross-contaminate by construction.
- **Positive**: a single global window (settings) plus a per-session override (registration status) gives fine control: e.g. globally open theory registration but keep one overflow room's session closed.
- **Risk**: this split is easy to reintroduce a bug against. Any new frontend or backend code that needs to answer "is this open?" must consult `ExamSession.RegistrationStatus` / the relevant `*Setting`, never `Event.IsActive` — there is no compiler-enforced boundary preventing a future handler from reading the wrong field. A frontend developer unfamiliar with this ADR could plausibly wire a UI element to `event.is_active` and ship a real access-control bug that looks correct in casual testing (the timeline dot and the actual gate usually agree, since admins update both together by convention, not by enforcement).
- **Neutral**: three independent toggles (event active flag, session registration status, session exam status, plus the global setting) is more moving parts than a single source of truth, but matches the real-world need (site-wide policy vs. per-room exception vs. purely cosmetic timeline).

## Alternatives considered

- **Single source of truth on `Event`**: derive registration-open/closed and submission-open/closed directly from `Event.IsActive` and `Event.StartTime`/`EndTime`. Rejected (per the session-log evidence above) — doesn't support "timeline shows the round but registration/submission has its own independent schedule," which the product needed (e.g. announcing a round before its registration window opens).
- **Merge session-level and global-level gates into one field**: e.g. only `ExamSession.RegistrationStatus`, no global `TheorySetting` window. Not adopted — the global setting lets admins close registration site-wide in one action instead of toggling every session individually (useful for an emergency freeze).

## Needs verification

- [ ] Whether any admin-facing UI copy or documentation (outside code) still implies the timeline flag gates access — not checked in this pass, would be a docs/UX bug rather than a code bug if so.
