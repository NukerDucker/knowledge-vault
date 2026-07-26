---
title: Deployment and CI
tags: [nextpath-x, operations, ci, deployment]
component: full-stack
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Deployment and CI

Related: [[00-local-dev-quickstart]].

Both repos have their own GitHub Actions workflows (`.github/workflows/`), independent of each other. No shared/orchestrating pipeline at the `nacl-nextpath-x/` parent level (it isn't a git repo, so it can't have one).

## API: `nacl-nextpath-x-api/.github/workflows/api-ci.yml`

Triggers: push to `dev`/`staging`, PRs targeting `main`. Job `test`:

1. Checkout, `actions/setup-go@v5` (`go-version-file: go.mod`).
2. `go mod download` → `go vet ./...` → `go test ./...` → `go build ./...`.
3. `docker build -t nextpath-api-ci:${{ github.sha }} .`
4. Writes a CI-only `.env` (test secrets, `APP_ENV=test`, `DB_NAME=nextpath_test`).
5. `docker compose -p nextpath-api-ci config` (validates compose file) then `up -d --build --remove-orphans`.
6. Polls `GET http://localhost:8080/health` up to 40× / 3s apart; fails the job and dumps `docker compose logs --tail=200` if it never goes healthy.
7. `if: always()` teardown: `docker compose -p nextpath-api-ci down -v --remove-orphans`.

Job `publish-image` (needs `test`, only on push to `staging`): builds and pushes `ghcr.io/network-and-cloud-laboratory-kmitl/nacl-nextpath-x-api:{sha,staging-latest}` to GHCR.

## API: `nacl-nextpath-x-api/.github/workflows/api-staging-deploy.yml`

Triggers: `workflow_run` completion of "API CI" on `staging` (success only), or manual `workflow_dispatch`. Runs on a **self-hosted** runner (`self-hosted, linux, nextpath-x-api-staging`) — i.e. an actual staging VM, not a GitHub-hosted runner. Steps: checkout the deployed SHA → write a `.env` from GitHub Environment secrets (`environment: staging`) → GHCR login → `docker compose -p nextpath-api pull` + `up -d --no-build --remove-orphans` (deploys the image `publish-image` pushed, does not rebuild) → poll `GET http://localhost:${APP_PORT}/health` up to 20× → `docker image prune -f` on success, diagnostics dump on failure.

## Web: `nacl-nextpath-x-web/.github/workflows/web-ci.yml`

Triggers: push to `dev`/`staging`, PRs targeting `main`. Job `test` (20 min timeout), env `NEXT_PUBLIC_API_URL=http://localhost:8080`, `NEXT_PUBLIC_USE_MOCK_DATA=true`: Bun setup (`oven-sh/setup-bun@v2`), Bun-install-cache + `.next/cache` caching keyed on `bun.lock`/`package.json`/`next.config.ts`/`tsconfig.json`/`src/**/*`.

## Web: `nacl-nextpath-x-web/.github/workflows/web-staging-deploy.yml`

Exists; not opened in this pass — mirror structure to the API's staging-deploy workflow is likely but unconfirmed.

## Needs verification

- [ ] Full step list of `web-ci.yml` past the cache-setup steps (lint/test/build steps not read in this pass).
- [ ] Full content of `web-staging-deploy.yml` — not opened.
- [ ] Whether `NEXT_PUBLIC_USE_MOCK_DATA` is a real, still-used env var in the web app source, or a CI-only leftover — it doesn't appear in `nacl-nextpath-x-web/.env.example` (see [[01-environment-variables]]) and `nacl-nextpath-x-web/CLAUDE.md`'s Data Policy section says production must not use mock/hardcoded fallback data, so this flag's actual runtime effect (if any) is unconfirmed.
