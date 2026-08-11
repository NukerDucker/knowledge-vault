# NextPath → Camellya Booking Sync — Design

**Date:** 2026-07-07
**Status:** Approved, pending spec review

## Goal

Let a student book an interview slot in **NextPath-X** and have that candidate
appear in **Camellya** (day + time slot) so interviewers can score them.
Two separate apps, two separate databases, connected by a one-way **pull**.

## Scope

**In scope:** the booking → scoring data bridge (pull + reconcile), the
Camellya `Candidate` remodel, and one widened NextPath endpoint.

**Out of scope:** SSO / Authentik / OIDC. Camellya SSO is **already
implemented** (commit `b1b94bf`; see `camellya-api/docs/NACLAUTH.md`): Google +
Authentik both seed a **local Camellya JWT** (cookie or `Authorization: Bearer`),
provisioning an `Interviewer` from a `@kmitl.ac.th` email. NextPath still uses
Google + local JWT (SSO is only a seam comment so far). Neither app's login is
touched by this work. Also out of scope: student onboarding.

## Settled decisions

| Decision | Choice |
|---|---|
| Integration shape | Keep both apps + both DBs; integrate (no merge, no shared login) |
| Slot / schedule owner | NextPath owns `interview_slots` + `interview_bookings` |
| Sync direction | Pull — Camellya fetches from NextPath |
| Sync trigger | Manual admin button ("Sync bookings"). No ticker (YAGNI). |
| Auth for pull | **Long-lived service JWT** — one-time out-of-band minted NextPath admin JWT (`Role:"admin"`, ~10y exp, HS256 + `JWT_SECRET`), held in Camellya config, sent as Bearer |
| Candidate fields | Remodel Camellya `Candidate` to mirror NextPath's field shape |
| Names | Keep both Thai and English (like NextPath) |
| Slot capacity | One candidate per slot (`max_capacity` = 1 in practice) |
| Parallel rooms | No — single track. `Round` unique key stays `(day, start_time)`. |

## Data flow

```
NextPath (admin creates slots; student books)
   │  GET /api/interview-bookings?event_id=N   (Bearer service-admin token)
   ▼
Camellya sync service
   │  for each BOOKED row  → upsert Day → upsert Round → upsert Candidate
   │  for each CANCELLED   → unlink Candidate from its Round
   ▼
Camellya interviewers score the candidate (existing UI)
```

Trigger: admin clicks **Sync bookings** in the Camellya admin UI.

## Field map (NextPath → Camellya Candidate)

| Camellya `Candidate` | NextPath source |
|---|---|
| `name_th` / `last_name_th` / `nickname_th` | `User.name_th` / `last_name_th` / `nickname_th` |
| `name_en` / `last_name_en` / `nickname_en` | `User.name_en` / `last_name_en` / `nickname_en` |
| `student_id` | `User.student_id` |
| `email` | `User.email` |
| `year` | `User.year` |
| `faculty` | `User.Faculty.Name` (resolved) |
| `department` | `User.Department.Name` (resolved) |
| `major` | `User.Major.Name` (resolved) |
| `exam_score` | `ExamAttempt.Score` for the student's attempt in that event |
| Day / Round | booking `date` / `start_time` / `end_time` |

`exam_score` = the student's earned total (`ExamAttempt.Score`) — the same
number the NextPath admin/grader pages render.

## Changes by repo

### NextPath-X API (one endpoint, widened — no new routes)

`GET /api/interview-bookings?event_id=N` already returns `AdminBookingRow`.
Widen that row + its query to also return, per booked student:
`nickname_th`, `name_en`, `last_name_en`, `nickname_en`, `year`,
`faculty`, `department`, `major`, `exam_score`.

- Join `users` → faculty/department/major names.
- Join the student's `ExamAttempt.Score` for the requested event (0 / null if
  no attempt).
- Still one endpoint, one query, ~a dozen added fields on the DTO.
- Admin-gated as today. Camellya authenticates with a long-lived service JWT
  (see below). **No change to NextPath's auth code** — the token is minted
  out-of-band, because NextPath's login path hardcodes a 24h expiry
  (`auth/service.go:239`) and has no API-key mechanism.

**Minting the service token (one-time, manual):** sign a JWT with
`{UserID:<service-user>, Role:"admin", exp:+~10y}` using HS256 + NextPath's
`JWT_SECRET` (same recipe as the frontend's `generate-test-tokens.js`). Store
in Camellya secrets as `NEXTPATH_SERVICE_TOKEN`; never commit. Re-mint if
NextPath rotates `JWT_SECRET` or changes claim shape (e.g. when it adopts SSO).

### Camellya API

1. **Remodel `Candidate`** (`models/models.go`) to the NextPath-shaped fields
   above. Replaces flat `Firstname/Lastname/Nickname/Program/Major`. Adds
   `faculty`, `department`, English name variants, `year`. DB migration under
   `migrations/`.
2. **`internal/integration/nextpath/client.go`** — HTTP client that calls the
   NextPath roster endpoint with the long-lived service JWT as a Bearer header.
   New config keys (mirroring Camellya's existing env-config pattern in
   `internal/config/config.go`): `NEXTPATH_BASE_URL`, `NEXTPATH_SERVICE_TOKEN`,
   `NEXTPATH_EVENT_ID`.
3. **`internal/service/sync/`** — reconcile logic:
   - `BOOKED` row → upsert `Day` by `date`; upsert `Round` by
     `(day, start_time)`, `DurationMinutes` from `end_time − start_time`;
     upsert `Candidate` by `student_id`; set `Candidate.DayID/RoundID` and
     `Round.StudentID`.
   - `CANCELLED` row → unlink the candidate from its round (clear
     `Round.StudentID`, `Candidate.DayID/RoundID`).
   - Upserts keyed on natural keys (`student_id`, `date`, `start_time`) so the
     sync is idempotent — safe to press repeatedly.
4. **One admin route + handler** (e.g. `POST /admin/sync/bookings`) that runs
   the sync service. Admin-only.

### Camellya frontend

- **"Sync bookings"** button on the admin schedule/candidates page → calls the
  sync route, shows a result summary (added / updated / unlinked).
- Adjust candidate/score/edit-candidate screens that read the renamed fields
  (`Firstname` → `name_th`, etc.); surface `faculty`/`department`.

## Idempotency & reconciliation

- Every upsert uses a natural key, so re-syncing is safe and non-duplicating.
- Cancellations are the reason pull needs reconciliation: a student who cancels
  in NextPath flips to `CANCELLED`; the next sync unlinks them in Camellya.
- Scores already recorded against an unlinked round are retained, not deleted
  (a cancel shouldn't destroy interviewer work). Only the candidate↔round link
  is cleared.

## Explicitly skipped (YAGNI — add when needed)

- **Scheduled/automatic sync** — manual button only. A ticker is a ~10-line add
  later if same-day lag becomes a problem.
- **Push/webhook** — pull chosen to avoid building authenticated inbound. If
  real-time cancellation handling is ever required, revisit.
- **Parallel-room support** — `Round` stays keyed on `(day, start_time)`. If
  two rooms ever run at the same time, add `location` to the key (small
  migration).
- **Shared identity / SSO between the apps** — separate user tables; only
  candidate *data* crosses the boundary.

## Risks

- **Single-track assumption:** if NextPath ever books two slots at the same
  `start_time` on one day, the second candidate collides on Camellya's unique
  `(day, start_time)` index and silently fails to sync. Mitigation is known
  (add `location` to the key). Flagged, deliberately deferred.
- **exam_score absence:** students with no submitted attempt sync with
  `exam_score = 0`. Acceptable — editable in Camellya's edit-candidate screen.
- **Service token blast radius:** the pull uses a ~10-year admin JWT. If it
  leaks, it grants full NextPath admin access until `JWT_SECRET` is rotated —
  and rotation invalidates every user's session. Keep it in secrets, never in
  git (same policy as Camellya's existing Google creds). Acceptable trade for a
  single-event tool; revisit if this becomes long-lived infrastructure.
- **Token breaks on NextPath auth changes:** when NextPath adopts SSO or
  rotates `JWT_SECRET`, the service token stops working and must be re-minted.
  Sync failing = an admin sees an error on the button; no data corruption.
