---
title: Stack Overview
tags: [nextpath-x, architecture, stack]
component: full-stack
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Stack Overview

Related: [[00-system-map/README]], [[01-frontend-architecture]], [[02-backend-architecture]], [[03-full-stack-data-flow]].

> [!info] Thin index note
> Backend depth lives in [[02-backend-architecture]] (routes, auth, layers, DB models — condensed but self-contained). Frontend depth lives in [[01-frontend-architecture]]. A prior deep backend/security audit (`obsidian-map/`) existed here and was deleted 2026-07-16 at the project owner's request because it no longer reflected `origin/main` — see [[../00-system-map/README]] for the full note. This file stays a thin index so it doesn't become a second copy of either detail note.

## Repos

| Repo | Path | Stack | Evidence |
|---|---|---|---|
| `nacl-nextpath-x-api` | `nacl-nextpath-x/nacl-nextpath-x-api` | Go 1.21+, Gin, GORM, PostgreSQL 15, MinIO/S3, JWT | `go.mod`, `docker-compose.yml` |
| `nacl-nextpath-x-web` | `nacl-nextpath-x/nacl-nextpath-x-web` | Next.js 16.2.6, Bun, React, Tailwind, Tiptap 3.25 (rich-text editor), Vitest | `package.json` |

## Backend (`nacl-nextpath-x-api`)

20 domains under `internal/domain/`: `auth`, `event`, `examaccess`, `examasset`, `examattempt`, `exampaper`, `examregistration`, `examsession`, `grading`, `interview`, `paperquestion`, `policy`, `portfolio`, `question`, `questioncategory`, `questionchoice`, `settings`, `studentanswer`, `systemlog`, `user`. Full boot sequence, middleware order, route-group table, auth model, and data model summary: [[02-backend-architecture]].

## Frontend (`nacl-nextpath-x-web`)

App-router Next.js app under `src/app`, feature modules under `src/features/{landing,portfolio,theory,exam,admin,grading,apply,auth,application,blueprint,pdpa}`, shared helpers under `src/shared/{components,lib,hooks}`. Full detail: [[01-frontend-architecture]].

Evidence: `nacl-nextpath-x-web/CLAUDE.md` repo map (confirmed against actual `src/` tree during this audit).

## Cross-cutting: full-stack data flow

Settings vs. timeline vs. registration-status decoupling, and the exam-access token exchange, span both repos. See [[03-full-stack-data-flow]] and [[../04-adrs/0001-decouple-global-settings-and-session-registration-status-from-timeline-display]].

## Needs verification

- [ ] Whether `nacl-nextpath-x-web/docker-compose.yml` is actually used anywhere (no reference found in root `README.md` quick-start, which uses `bun run dev` directly for local frontend). Treated as a production-image build path only, per project owner's original description of the quick-start commands.
