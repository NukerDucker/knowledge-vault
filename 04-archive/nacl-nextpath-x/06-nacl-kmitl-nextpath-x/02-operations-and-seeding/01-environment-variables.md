---
title: Environment Variables
tags: [nextpath-x, operations, env-vars, config]
component: full-stack
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Environment Variables

Related: [[00-local-dev-quickstart]], [[../01-architecture/02-backend-architecture]].

Transcribed from `nacl-nextpath-x-api/.env.example` and `nacl-nextpath-x-web/.env.example` verbatim, 2026-07-16.

## `nacl-nextpath-x-api/.env.example`

All runtime unless noted. Defaults shown are the `.env.example` values, not necessarily `config.go`'s fallback if the var is absent entirely (see `internal/config/config.go` for those).

| Var | Default | Notes |
|---|---|---|
| `APP_ENV` | `dev` | `dev` = lax cookies over http, dev token endpoint, relaxed CORS. `prod` = Secure+SameSite=None cookies (HTTPS only), CSRF + strict CORS, dev token endpoint disabled. Serving prod over plain http breaks login (browser drops the Secure cookie). `config.go`'s `normalizeAppEnv` collapses any non-dev-alias value (including typos, "production", "staging") to `prod` — fail-closed by design (SEC-007 in source comment). |
| `APP_PORT` | `8080` | |
| `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` / `DB_SSLMODE` / `DB_TIMEZONE` | `localhost` / `5432` / `postgres` / `postgres` / `myapi` / `disable` / `UTC` | |
| `PGADMIN_DEFAULT_EMAIL` / `PGADMIN_DEFAULT_PASSWORD` / `PGADMIN_PORT` | (empty) / (empty) / `5050` | |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | (empty) | Google OAuth app credentials |
| `GOOGLE_REDIRECT_URL` | `http://localhost:8080/api/auth/google/callback` | prod: `https://<api-domain>/api/auth/google/callback`, also register in Google console |
| `FRONTEND_URL` | `http://localhost:3000` | |
| `JWT_SECRET` | `change_me_to_a_random_32_char_string` | **Prod requires ≥32 bytes or boot fails** (`config.go`). Generate: `openssl rand -base64 48`. Rotating invalidates every issued cookie (forces re-login). |
| `JWT_EXPIRY_HOURS` | `24` | |
| `S3_REGION` / `S3_BUCKET` / `S3_ACCESS_KEY_ID` / `S3_SECRET_ACCESS_KEY` / `S3_ENDPOINT` / `S3_PUBLIC_URL` | `us-east-1` / `test-bucket` / `minioadmin` / `minioadmin` / `http://localhost:9000` / `http://localhost:9000/test-bucket` | |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | prod: web origin(s), https, comma-separated. **Authoritative for both CORS and the CSRF Origin allowlist** — a wrong value blocks every admin write. |
| `RATE_LIMIT_GLOBAL` | `100` | |
| `RATE_LIMIT_STRICT` | `10` | Per-IP limit on `/auth`. Event-day note in source: shared school NAT collapses many students to one IP — raise (e.g. 100) so a whole room can log in, then lower afterward. |
| `RATE_LIMIT_EXAM` | `300` | Per-user limit on exam answer autosave (~150 questions can burst quickly). |
| `MAX_REQUEST_SIZE` | `10485760` (10 MB) | JSON body cap; multipart uploads use `MAX_UPLOAD_SIZE` instead. |
| `MAX_UPLOAD_SIZE` | `52428800` (50 MB) | |
| `DB_MAX_OPEN_CONNS` | `100` | Postgres `max_connections` must exceed this — compose sets `200`. |
| `INTERVIEW_CANCEL_CUTOFF_HOURS` | `24` | |

## `nacl-nextpath-x-web/.env.example`

| Var | Default | Build-time or runtime | Notes |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8080` | **Build time** | Next.js inlines `NEXT_PUBLIC_*` vars into the client bundle at `next build`. Source comment: "Required in production builds (build throws if unset)." Prod value must be `https://` so the Secure session cookie round-trips, and must match the API's `CORS_ALLOWED_ORIGINS` / OAuth redirect. |
| `WEB_PORT` | `3000` | Runtime | Only consumed by `nacl-nextpath-x-web/docker-compose.yml` (production-image path, not local `bun run dev` — see [[00-local-dev-quickstart]]). |

## Cross-cutting risk

Three separate places must agree on the web origin or auth silently breaks: `GOOGLE_REDIRECT_URL` (api), `CORS_ALLOWED_ORIGINS` (api), `NEXT_PUBLIC_API_URL` (web, must point back at the api). A mismatch on any one manifests as either a blocked OAuth callback, a CORS-rejected admin write, or a browser silently dropping the Secure cookie — none of these throw a helpful error at the point of misconfiguration.
