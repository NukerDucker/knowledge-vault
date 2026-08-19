---
title: Frontend Architecture
tags: [nextpath-x, architecture, frontend, nextjs]
component: nextpath-x-web
criticality: medium
status: active
created: 2026-07-16
updated: 2026-07-16
last_reviewed: 2026-07-16
---

# Frontend Architecture

Related: [[00-stack-overview]], [[03-full-stack-data-flow]].

> [!info] New ground
> No prior audit ever covered `nacl-nextpath-x-web` — the deleted `obsidian-map/` (see [[../00-system-map/README]]) was API-only even before it was removed. This note is the first architectural record of the frontend in this vault.

## App Router structure

`src/app/` (verified against the live tree, not just `nacl-nextpath-x-web/CLAUDE.md`'s repo map):

| Route group | Purpose |
|---|---|
| `(landing)/` | Public marketing/landing sections |
| `apply/`, `application/`, `pdpa/` | Applicant entry flow |
| `portfolio/`, `theory/` | Applicant portfolio upload, theory exam session selection |
| `exam/[sessionId]/` | Digital exam client (session-scoped) |
| `exam-preview/` | Exam preview mode (separate from live exam) |
| `blueprint/` | Applicant blueprint page |
| `auth/`, `auth/callback` | Google OAuth entry/callback |
| `grading/`, `grading/written`, `grading/submissions` | Grader answer review, written-answer scoring, submission list |
| `admin/{dashboard,exam-rounds,exam-papers,portfolios,users,examinees,timeline,check-in,interview,audit-logs,clock}` | Admin area, one route per management surface |

Evidence: `find nacl-nextpath-x-web/src/app -maxdepth 2 -type d`, 2026-07-16.

## Feature modules (`src/features/`)

`admin`, `application`, `apply`, `auth`, `blueprint`, `exam`, `grading`, `landing`, `pdpa`, `portfolio`, `theory` — one folder per domain, each holding its own components/types/API-client/data-source files. Example depth (`src/features/exam/`): `ExamClient.tsx`, `ExamPage.tsx`, `ExamQuestionPage.tsx`, `ExamPreviewClient.tsx`, `exam.data-source.ts`, `exam.types.ts`, `exam.constants.ts`, `exam.utils.ts`, `exam-weights.ts`, `useSessionClock.ts`, `useTabSwitchGuard.ts`, plus `.test.ts(x)` siblings for several of these (Vitest).

## Shared layer (`src/shared/`)

| Folder | Purpose |
|---|---|
| `lib/api/` | `client.ts` (`apiFetch`/`apiList`/`apiData`, `ApiClientError`, `COOKIE_SESSION_MARKER`), `config.ts` (`getApiUrl`) |
| `lib/rich-text.tsx` | Tiptap-JSON renderer — see [[../05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format]] and [[../03-incident-playbooks/00-rich-text-parsing-failures]] |
| `lib/auth/`, `lib/dates/`, `lib/theory/`, `lib/admission/`, `lib/users/` | Domain helper libs |
| `components/`, `components/ui/`, `components/reui/` | Shared components, shadcn/ui primitives, reui components |
| `hooks/` | Shared React hooks |
| `config/` | App-level config |

## Auth session model (frontend side)

`COOKIE_SESSION_MARKER = "cookie-session"` (`src/shared/lib/api/client.ts`) is a **non-secret sentinel**, not a credential: the real session JWT lives only in an HttpOnly cookie sent via `credentials: "include"`. Components use the marker as a "logged in?" boolean without ever holding the JWT client-side. Exam-access tokens are a separate, real bearer token sent explicitly — see [[../05-schema-and-data-quirks/02-exam-access-token-exchange-flow]].

## Security headers (`next.config.ts`)

`output: "standalone"`. Every response gets `Content-Security-Policy` (`frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `upgrade-insecure-requests` — intentionally omits `script-src`/`style-src`/`default-src` so it doesn't break Next.js inline runtime scripts or KaTeX/Tiptap inline styles), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (camera/mic/geolocation denied), HSTS. Marked `ponytail: tighten to a nonce-based script-src once a CSP test pass is budgeted` in source — i.e. a known, accepted gap, not an oversight.

`images.remotePatterns` allow-lists `lh3.googleusercontent.com` (Google avatar images) plus, when `NEXT_PUBLIC_API_URL` is set, `<that host>/api/exam-assets/**`. `localhost`/`127.0.0.1` patterns are added only outside `NODE_ENV=production`.

## Rich-text editing

Tiptap 3.25 (`@tiptap/core`, `@tiptap/react`, `@tiptap/starter-kit`, plus extensions for tables/task-lists/math/highlight/color/superscript-subscript/text-align/typography) is the editor used by admins to author exam-paper prompts/choices/descriptions (`src/features/admin/exam-papers/RichTextEditor.tsx` per `nacl-nextpath-x-web/CLAUDE.md`). Rendering back to read-only HTML on the applicant/exam side goes through `src/shared/lib/rich-text.tsx` — see [[../05-schema-and-data-quirks/00-exam-content-schema-and-rich-text-format]].

## Needs verification

- [ ] Whether `src/features/admin/exam-papers/RichTextEditor.tsx` exists exactly at that path — cited from `nacl-nextpath-x-web/CLAUDE.md`, not directly opened during this audit pass.
