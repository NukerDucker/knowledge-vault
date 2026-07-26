---
title: NextPath X Knowledge Vault
aliases:
  - nextpath-x
  - NextPath X MOC
tags: [nextpath-x, index, moc]
component: full-stack
criticality: high
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# NextPath X Knowledge Vault

> [!info] Read this note first
> Any human or agent returning to NextPath X starts here. It lists every folder, what it holds, and where the ground truth actually lives.

## Project summary

NACL NextPath X is the KMITL Network and Cloud Lab's full-stack admission system: applicant portfolio submission, theory exam registration/execution/grading, and interview booking. Two repos live under `~/Documents/University/Network-and-Cloud-Laboratory-KMITL/nacl-nextpath-x/`:

| Repo | Stack | Purpose |
|---|---|---|
| `nacl-nextpath-x-api` | Go 1.21+, Gin, GORM, PostgreSQL, MinIO/S3, JWT | REST API — auth, domains, storage |
| `nacl-nextpath-x-web` | Next.js 16, Bun, React, Tailwind, Tiptap | Applicant/admin/grader web app |

Evidence: root `README.md` (`~/Documents/University/Network-and-Cloud-Laboratory-KMITL/nacl-nextpath-x/README.md`).

## This vault's scope vs. what already existed

> [!warning] A prior `obsidian-map/` audit was deleted 2026-07-16
> `~/KnowledgeVault/06-nacl-kmitl/obsidian-map/` used to hold a deep, backend-only architecture/security audit of `nacl-nextpath-x-api` (routes, auth, DB models, middleware, security findings — 16 numbered notes + a `domains/` subfolder), mirrored verbatim from a loose `obsidian-map/` folder next to the repo checkout. **The project owner confirmed it no longer reflected `origin/main` and had both copies deleted mid-session** — neither was git-tracked (the repo's parent folder isn't even a git repo), so this was a plain filesystem delete, not a git operation, and nothing was lost from version control. Backend architecture is now documented directly in [[01-architecture/02-backend-architecture]], sourced fresh from the current checkout rather than trusting the deleted audit.

## Folder map

| Folder | Contents |
|---|---|
| [[00-system-map/README\|00-system-map/]] | This entrypoint note |
| `01-architecture/` | [[01-architecture/00-stack-overview\|Stack overview]], [[01-architecture/01-frontend-architecture\|Frontend architecture]], [[01-architecture/02-backend-architecture\|Backend architecture]], [[01-architecture/03-full-stack-data-flow\|Full-stack data flow]] |
| `02-operations-and-seeding/` | [[02-operations-and-seeding/00-local-dev-quickstart\|Local dev quickstart]], [[02-operations-and-seeding/01-environment-variables\|Environment variables]], [[02-operations-and-seeding/02-seeding-and-migrations\|Seeding & migrations]], [[02-operations-and-seeding/03-deployment-and-ci\|Deployment & CI]] |
| `03-incident-playbooks/` | [[03-incident-playbooks/00-rich-text-parsing-failures\|Rich-text parsing failure diagnostics]] |
| `04-adrs/` | [[04-adrs/0001-decouple-global-settings-and-session-registration-status-from-timeline-display\|ADR-0001]] settings/registration-status vs. timeline decoupling, [[04-adrs/0002-schemaless-automigrate-no-versioned-migrations\|ADR-0002]] AutoMigrate-only schema strategy, [[04-adrs/0003-richtext-stored-as-opaque-text-column\|ADR-0003]] rich-text stored as opaque TEXT |
| `05-schema-and-data-quirks/` | [[05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format\|Exam content schema & rich-text format]], [[05-schema-and-data-quirks/01-grading-score-audit-trail\|Grading score audit trail]], [[05-schema-and-data-quirks/02-exam-access-token-exchange-flow\|Exam access token exchange flow]] |

## Quick start (verified against `docker-compose.yml` / `package.json`)

Two terminals, from `~/Documents/University/Network-and-Cloud-Laboratory-KMITL/nacl-nextpath-x/`:

```bash
# Terminal 1 — API
cd nacl-nextpath-x-api
cp .env.example .env   # then edit — see environment-variables note
docker compose up --build
# API: http://localhost:8080, Swagger: http://localhost:8080/swagger/index.html
# pgAdmin: http://localhost:5050, MinIO console: http://localhost:9001

# Terminal 2 — Web
cd nacl-nextpath-x-web
cp .env.example .env   # NEXT_PUBLIC_API_URL, WEB_PORT
bun install
bun run dev
# Web: http://localhost:3000
```

Confirmed: `nacl-nextpath-x-api/docker-compose.yml` (services `app`, `postgres`, `pgadmin`, `minio`, `minio-init`); `nacl-nextpath-x-web/package.json` scripts (`dev`, `build`, `start`, `lint`, `test`). `nacl-nextpath-x-web/docker-compose.yml` exists too but is the production-image path (`NEXT_PUBLIC_API_URL` baked in at build time via `args:`) — local frontend dev uses `bun run dev`, not that compose file. Full detail: [[02-operations-and-seeding/00-local-dev-quickstart]].

## Required environment variables (at a glance)

| Var | Repo | When required | Evidence |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | web | **Build time** — `next build` throws if unset in prod | `nacl-nextpath-x-web/.env.example` |
| `JWT_SECRET` | api | Runtime; prod requires ≥32 bytes or boot fails | `internal/config/config.go` |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` / `GOOGLE_REDIRECT_URL` | api | Runtime | `.env.example` |
| `CORS_ALLOWED_ORIGINS` | api | Runtime — authoritative for CORS **and** CSRF origin allowlist | `.env.example` |
| `DB_*`, `S3_*` | api | Runtime | `.env.example` |

Full table with build-time vs. runtime distinctions: [[02-operations-and-seeding/01-environment-variables]].

## Frontmatter schema used in this folder

```yaml
---
title: string
tags: [array]
component: nextpath-x-api | nextpath-x-web | full-stack | docs
criticality: low | medium | high
status: active | draft | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
---
```

This is a superset of the vault-wide standard in root `CLAUDE.md` (`title/tags/status/created/updated`) — `component`/`criticality`/`last_reviewed` are added per-note here because ADRs and incident playbooks need them; every note keeps `created`/`updated` for vault-wide consistency. This deviation was confirmed with the project owner before writing (see conversation this note was authored in) rather than picked silently.

## Verification status

Last verified: 2026-07-16, against the checkout at `~/Documents/University/Network-and-Cloud-Laboratory-KMITL/nacl-nextpath-x/`. Every path/route/env-var cited in this folder was read directly from that checkout, not carried over from `obsidian-map/`'s prior (Windows-checkout) evidence. Items not confirmed in code are marked "Needs verification" or "per project owner" in the relevant note.
