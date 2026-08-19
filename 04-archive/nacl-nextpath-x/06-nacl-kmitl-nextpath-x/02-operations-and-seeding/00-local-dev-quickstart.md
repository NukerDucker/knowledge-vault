---
title: Local Dev Quickstart
tags: [nextpath-x, operations, local-dev]
component: full-stack
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Local Dev Quickstart

Related: [[../00-system-map/README]], [[01-environment-variables]].

## Two-terminal setup

```bash
cd ~/Documents/University/Network-and-Cloud-Laboratory-KMITL/nacl-nextpath-x

# Terminal 1 — API
cd nacl-nextpath-x-api
cp .env.example .env
# edit .env — see [[01-environment-variables]]
docker compose up --build

# Terminal 2 — Web
cd nacl-nextpath-x-web
cp .env.example .env
bun install
bun run dev
```

## API `docker-compose.yml` services

| Service | Image | Purpose | Port(s) |
|---|---|---|---|
| `app` | built from `Dockerfile` | Go API | `${APP_PORT}` → `8080` by default |
| `postgres` | `postgres:15-alpine` | Primary DB, `max_connections=200` (headroom above `DB_MAX_OPEN_CONNS=100` for pgAdmin/psql) | `5432` |
| `pgadmin` | `dpage/pgadmin4:latest` | DB admin UI | `${PGADMIN_PORT}` → `5050` |
| `minio` | `minio/minio:latest` | S3-compatible object storage | `9000` (S3 API), `9001` (console) |
| `minio-init` | `minio/mc:latest` | One-shot: creates the bucket, sets `portfolios`/`exam-assets` prefixes to anonymous-download | none (runs once, exits) |

Evidence: `nacl-nextpath-x-api/docker-compose.yml`.

## Default ports (cross-checked against root `README.md`)

| Service | URL |
|---|---|
| Web | `http://localhost:3000` |
| API | `http://localhost:8080` |
| Swagger UI | `http://localhost:8080/swagger/index.html` (non-prod only — `server.go` registers it only when `APP_ENV != "prod"`) |
| PostgreSQL | `localhost:5432` |
| pgAdmin | `http://localhost:5050` |
| MinIO API | `http://localhost:9000` |
| MinIO Console | `http://localhost:9001` |

## Health check

`GET /health` on the API is unauthenticated and ungated (`server.go`), returns `{"status": "ok"}`. Used by CI's Docker Compose smoke test and the staging deploy's post-deploy check — see [[03-deployment-and-ci]].

## `nacl-nextpath-x-web/docker-compose.yml` — not the local dev path

This file exists but bakes `NEXT_PUBLIC_API_URL` in at Docker build time via `args:` and runs `next start` in a production image. Local frontend development uses `bun run dev` directly, not this compose file — confirmed against root `README.md`'s quick-start, which never invokes it.

## Needs verification

- [ ] Whether `nacl-nextpath-x-web/docker-compose.yml` is used anywhere (e.g. a staging/prod deploy script) — not traced in this pass.
