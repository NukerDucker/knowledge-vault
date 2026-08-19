---
title: Full-Stack Data Flow
tags: [nextpath-x, architecture, data-flow]
component: full-stack
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Full-Stack Data Flow

Related: [[00-stack-overview]], [[02-backend-architecture]], [[../04-adrs/0001-decouple-global-settings-and-session-registration-status-from-timeline-display]], [[../05-schema-and-data-quirks/02-exam-access-token-exchange-flow]].

## Timeline display vs. access gating (condensed — full ADR: [[../04-adrs/0001-decouple-global-settings-and-session-registration-status-from-timeline-display]])

Three separate mechanisms, easy to conflate, deliberately decoupled:

| Mechanism | Field | Model | Effect |
|---|---|---|---|
| Timeline display | `IsActive` | `event.Event` | **Display-only.** Grepped across all of `internal/` (excluding `_test.go`): only referenced in `event/handler.go` and `event/dto.go`. No authorization or registration-gating code reads it. |
| Per-session registration gate | `RegistrationStatus` (`OPEN`/`CLOSED`) | `examsession.ExamSession` | Actually gates `examregistration.Service.Register` — `session.EffectiveRegistrationStatus() != examsession.RegistrationStatusOpen` → `ErrSessionNotOpen`. |
| Global window gate | `TheorySetting.RegistrationMode/OpenAt/CloseAt`, `PortfolioSetting.SubmissionMode/OpenAt/CloseAt` | `settings.TheorySetting`, `settings.PortfolioSetting` | `examregistration.Service.Register` additionally calls `settings.NewService(s.settingsRepo).GetTheory(ctx)` and checks `setting.IsRegistrationOpen(time.Now())`. `portfolio.Service.Submit` calls `s.isSubmissionOpen(ctx)` (backed by `PortfolioSetting`) before accepting a file. |

Confirmed intentional (not accidental) via `~/KnowledgeVault/05-ai/projects/nacl-nextpath-x/session-state.md`, 2026-05-24 entries (quoted):

> "Portfolio availability/result publication is now global settings, detached from timeline events. Use public `GET /api/settings/portfolio` and admin `PUT /api/settings/portfolio`..."
> "Timeline `/api/events` is display-only for dynamic timeline; do not use events to decide whether portfolio upload is open or portfolio results are visible."

Frontend contract note (`nacl-nextpath-x-web/CLAUDE.md`) confirms the session-level knob is a distinct admin action: `PATCH /api/exam-sessions/:id/registration-status` (`OPEN`/`CLOSED`) is separate from `PATCH /api/exam-sessions/:id/exam-status` (`WAITING`/`STARTED`/`FINISHED`) — registration and exam-runtime state are two different admin toggles on the same session.

## Exam-access token flow (condensed — full detail: [[../05-schema-and-data-quirks/02-exam-access-token-exchange-flow]])

```
Admin check-in (POST /api/admin/exam-registrations/:id/check-in)
  → sets IsCheckedIn, ExamCodeHash, ExamCodeIssuedAt, ExamCodeExpiresAt on ExamRegistration
  → plaintext code shown once in the response

Student POST /api/exam-access/exchange { code }   [requires login session cookie]
  → examaccess.Service.ExchangeCode: hash code, lockout check, look up registration by hash,
    verify reg.UserID == authenticated userID
  → issueToken: check-in status, exam-mode-for-year policy, code expiry, session status,
    attempt-not-already-submitted
  → mints short-lived exam_access JWT (expires at session.RuntimeDeadline() + SubmitGrace)

exam_access JWT (Bearer) → gates /api/exam-attempts/*, /api/student-answers/* (examOnly routes)
```

## Portfolio submission flow (overview)

`POST /api/portfolios` (protected, JWT user id — not client-supplied `user_id`) → `portfolio.Service.Submit` → gated by `PortfolioSetting` window (`isSubmissionOpen`) + `policy.CanSubmitPortfolio(u.Year)` (year-1 only) + one-submission-per-user (`ErrAlreadySubmitted`). Result publication is a separate global flag (`PortfolioSetting.ResultPublishedAt`), also decoupled from the timeline — same pattern as registration above.

## Needs verification

- [ ] Full admin portfolio-review flow (status transitions beyond `PENDING`) — not traced in this pass, out of scope for this note.
