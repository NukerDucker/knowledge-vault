---
title: Exam Access Token Exchange Flow
tags: [nextpath-x, schema, auth, exam-access, security]
component: nextpath-x-api
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Exam Access Token Exchange Flow

Related: [[../01-architecture/02-backend-architecture]], [[../01-architecture/03-full-stack-data-flow]], [[../04-adrs/0001-decouple-global-settings-and-session-registration-status-from-timeline-display]].

This is the core security boundary for the digital exam: turning "I'm a logged-in student with a 6-character check-in code" into a scoped, short-lived token that can submit exam answers.

## Step 1 — Admin check-in

`POST /api/admin/exam-registrations/:id/check-in` (admin only, `examregistration.RegisterAdminRoomRoutes`). Sets on `ExamRegistration`: `IsCheckedIn = true`, `CheckedInAt`, `CheckedInBy`, `ExamCodeHash` (HMAC of a generated code, `examregistration.HashExamCode`), `ExamCodeIssuedAt`, `ExamCodeExpiresAt`. The plaintext code is returned once in the response body — never stored in plaintext.

## Step 2 — Student exchanges the code

`POST /api/exam-access/exchange { code }` — registered under the `protected` route group (`middleware.AuthRequired`), i.e. **requires an authenticated login session cookie**. The code alone is never sufficient. Handler: `examaccess.Handler.ExchangeCode` (`internal/domain/examaccess/handler.go`).

```go
func (h *Handler) ExchangeCode(c *gin.Context) {
	userID := c.GetString(utils.ContextKeyUserID) // from the session JWT, not the request body
	...
	res, err := h.service.ExchangeCode(c.Request.Context(), userID, req.Code)
	...
}
```

## Step 3 — `examaccess.Service.ExchangeCode` (`internal/domain/examaccess/service.go`)

1. Trim/validate code is exactly 6 characters (`ErrInvalidCode` otherwise).
2. Hash the code (`HashExamCode`), check a per-code-hash **lockout** (`ErrTooManyExchangeAttempts` / `ErrCodeLocked`) before doing anything else.
3. Look up the registration by code hash. Not found → count as a failed attempt (`lockout.recordFailure`).
4. **Owner check**: `reg.UserID != userID` → `ErrCodeOwnerMismatch` — and this failure is **deliberately not counted toward the lockout**. Source comment, quoted:
   > "A mismatch means the code itself is correct, so it must not count toward the lockout: otherwise anyone sent a victim's code could lock the victim out of their own exam."
5. On success, calls `issueToken` and resets the lockout for that code hash.

## Step 4 — `issueToken` (same file)

Checks, in order:

1. `reg.IsCheckedIn` — false → `ErrRegistrationHold`.
2. Session lookup; nil → `ErrSessionExpired`.
3. **Exam-mode policy gate**: `policy.ExamModeForYear(u.Year) != policy.ExamModeComputer` → `ErrPaperExamOnly`. Paper-mode students never receive a digital token — the exam roster shares one room/seat pool across year groups, but only computer-mode years get exam-access tokens. Source has a `ponytail:` note flagging that `userRepo` being nil in production would silently skip this gate — must be wired in `cmd/api/main.go` (it is, per [[../01-architecture/02-backend-architecture]]).
4. **Code expiry** ("SEC-004" in source comment): `reg.ExamCodeExpiresAt == nil || !reg.ExamCodeExpiresAt.After(now)` → `ErrCodeExpired`. No grace period here — quoted: "ExamCodeExpiresAt is admin intent (set at check-in) and must stay revocable to the second, unlike the runtime deadline below."
5. **Session status** (`EffectiveExamStatus()`): `STARTED` with room left before `RuntimeDeadline() + SubmitGrace` → proceed; `STARTED` past that → `ErrSessionFinished`; `FINISHED` → `ErrSessionFinished`; anything else (`WAITING`) → `ErrSessionNotStarted`.
6. **Already submitted**: existing attempt with `SubmitTime != nil` → `ErrAttemptSubmitted`.
7. Mint the token: `authSvc.SignExamAccess(reg.UserID, reg.ID, reg.SessionID, "", expiresAt)`, where `expiresAt = session.RuntimeDeadline().Add(examattempt.SubmitGrace)`. Quoted rationale for outliving the runtime deadline: "the auto-submit fired at t=0 cannot be 401'd by middleware before the submit service's own deadline check (which honors the same grace) runs."

## HTTP error codes (from `Handler.ExchangeCode`'s switch)

| HTTP | Code | Trigger |
|---|---|---|
| 401 | `unauthorized` | No login session |
| 401 | `invalid_code` | Malformed/not-found code |
| 429 | `too_many_attempts` | Lockout threshold hit |
| 423 | `locked` | Code temporarily locked |
| 403 | `not_checked_in` | Registration not checked in |
| 403 | `paper_exam_only` | Student's year is paper-mode |
| 403 | `code_owner_mismatch` | Code belongs to a different account |
| 403 | `exam_not_started` | Session still `WAITING` |
| 403 | `exam_finished` | Session `FINISHED` or past grace |
| 403 | `expired` | Code or session expired |
| 409 | `already_submitted` | Attempt already has a `SubmitTime` |
| 500 | `internal_error` | Unhandled |

## Related: fetching your own registration

`GET /api/exam-registrations/mine` (`protected`, `examregistration.Handler.GetMine`) — a student's own registration record, used by the frontend to know whether/when to prompt for the exchange step.

## Dev-only shortcut

`POST /dev/exam-access` (public route group, registered **only** when `APP_ENV != "prod"`) calls `examaccess.Service.DevAccess`, which additionally hard-checks `s.appEnv == "prod"` internally and returns `ErrDevDisabled` even if somehow invoked — belt-and-suspenders against this ever working in production regardless of route registration.
