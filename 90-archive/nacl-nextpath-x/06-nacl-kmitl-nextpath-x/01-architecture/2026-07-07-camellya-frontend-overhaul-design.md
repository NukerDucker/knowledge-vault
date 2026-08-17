# Camellya Frontend Overhaul — Design Spec
**Date:** 2026-07-07  
**Branch:** audit  
**Stack:** Next.js 15, React 19, shadcn/ui (new-york), Tailwind CSS v3, TanStack Table v8, Recharts

---

## 1. Goal

Rebuild the interviewer-facing web app from its current broken/patched state into a clean, secure, responsive tool. Interviewers use it during in-person sessions to find candidates quickly, score per question, and leave comments. Design stays dark-themed, improves on the current layout rather than replacing it wholesale.

Primary user flow: **open app → find candidate → score + comment (auto-saves) → done.**

---

## 2. Architecture

### 2.1 Route Structure (new, kebab-case, RESTful)

| New Route | Old Route | Notes |
|---|---|---|
| `/` | `/` | Login — Google OAuth only |
| `/candidates` | `/candidate_table` | Interviewer candidate list |
| `/candidates/[id]/score` | `/scoring/[id]` | Interviewer scoring form |
| `/admin/candidates` | `/admin/candidate_table` | Admin candidate list |
| `/admin/candidates/cards` | `/admin/candidate_card` | Admin card/radar view |
| `/admin/candidates/[id]/score` | `/admin/scoring/[id]` | Admin scoring view |
| `/admin/roles` | `/admin/role` | Assign primary interviewers |
| `/admin/schedule` | `/admin/date_rounds` | Manage days + rounds |
| `/admin/questions` | `/admin/edit_question` | CRUD categories + questions |
| `/unauthorized` | `/unauthorized` + `/403` | Single error page |

`/admin/edit_candidate` removed — CRUD handled via modal in `/admin/candidates`.

### 2.2 Shared Layout

**`Shell` component** (`src/components/Shell.tsx`):
- Wraps all authenticated pages
- Renders `<NavBar>` + `<main>` content area
- NavBar reads `user`, `isAdmin` from `AuthProvider` context — no extra API fetch

**`NavBar`** (`src/components/NavBar.tsx`):
- Shows: app name, interviewer name + role badge (Primary/Secondary/Admin), logout dropdown
- Logo navigates to `/candidates` (interviewer) or `/admin/candidates` (admin)
- Current date/time via `Intl.DateTimeFormat` (1s interval, same as now)
- Stops independently fetching `/interviewers/current` — reads from context

**`AdminSidebar`** (`src/components/AdminSidebar.tsx`):
- Rendered inside all `/admin/*` pages alongside content
- Desktop: fixed left sidebar (collapsible)
- Tablet (iPad): collapsed to icon-only sidebar
- Mobile: hidden, toggled via shadcn `Sheet` drawer
- Links: Candidates (table), Candidates (cards), Roles, Schedule, Questions

### 2.3 Shared Library

**`src/lib/api.ts`** — single source for all API calls:
```ts
const API = process.env.NEXT_PUBLIC_API_URL

export async function apiRequest(
  path: string,
  opts?: RequestInit,
  retry = true
): Promise<Response> {
  const res = await fetch(`${API}${path}`, { credentials: 'include', ...opts })
  if (res.status === 401 && retry) {
    const refreshed = await fetch(`${API}/auth/refresh`, { credentials: 'include' })
    if (refreshed.ok) return apiRequest(path, opts, false)
    window.location.href = '/'
  }
  return res
}
```
Replaces 11 copy-pasted `getAPI()` and 6 copy-pasted `authenticatedRequest`.

**`src/types/index.ts`** — all shared interfaces:
- `CandidateDetail`, `Category`, `Question`, `ExistingScore`, `AuthUser`, `InterviewerRole`, `Day`, `Round`, `WeightedScoreResult`

**`src/lib/errors.ts`** — keep existing `errMsg` / `errStatus`.

---

## 3. Pages

### 3.1 Login (`/`)

- Centered `Card` (shadcn), dark background, app name + subtitle
- Single "Sign in with Google" `Button`
- OAuth error from `?error=` query param shown via sonner `toast.error` (remove `alert()`)
- Remove all commented-out username/password code

### 3.2 Interviewer Candidate List (`/candidates`)

- Role badge + welcome header (name, year, primary/secondary)
- `PieChartDonutWithText` — "% Interviewed" stat, top-right or above table
- Prominent search bar (shadcn `Command` or controlled `Input`) — filter by name/nickname/student ID
- TanStack Table with columns: Name, Student ID, Program, Year, Interview Time, Scored badge
  - "Scored" badge: green if interviewer has submitted scores for this candidate, muted if not
- Row click → navigate to `/candidates/[id]/score`
- Date filter (by day) — `Select` component
- Responsive: table scrolls horizontally on mobile, columns hide gracefully

### 3.3 Interviewer Scoring Form (`/candidates/[id]/score`)

- Back button → `/candidates`
- Candidate header: name, nickname, student ID, program, year, exam score badge
- Interviewer's own role badge (Primary/Secondary) shown prominently
- **Score section:** per-question, grouped by category. Each question has 1–5 button group (shadcn `Button` variants, not dropdowns). Selected score highlighted.
- **Comment section:** shadcn `Textarea` for overall comment
- **Auto-save:** debounced 1.5s after any score or comment change
  - Sticky bottom bar shows: `Saving...` | `Saved ✓` | `Failed, retrying...`
  - Each category saves independently via `POST /scores/submit` (upsert)
  - Comment saves via `POST /candidates/:id/comments` (upsert)
  - On 3 consecutive failures: persistent `toast.error` + manual Save button fallback
- **Score summary card** (shown to all, primary sees weighted breakdown):
  - Own average per category
  - If primary: weighted score summary using current weighting method
- On mount: load existing scores + comment, populate form

### 3.4 Admin Candidate List (`/admin/candidates`)

- `AdminSidebar` + `Shell`
- Same table as interviewer view + extra admin columns: all interviewers' average, weighted score
- Row actions (shadcn `DropdownMenu`): View scores, Edit candidate, Delete candidate
- Edit/Create candidate via shadcn `Dialog` (modal) — replaces `/admin/edit_candidate` page
- `ScoreDetailsDialog` — repurpose the existing component (currently dead) to show all interviewer scores per candidate

### 3.5 Admin Candidate Cards (`/admin/candidates/cards`)

- `AdminSidebar` + `Shell`
- Full candidate detail card (implement the currently-empty shell):
  - Candidate info header
  - `RadarChart` (recharts) showing weighted scores by category
  - Comments list from all interviewers
  - Overall comment field (`GET /candidates/:id/overall-comment`, `POST /admin/scores/overall-comment`)
- Weighting method selector (`WeightingMethodSelector`) — one instance, lifted to page level
- Preference manager (like/maybe/no) — localStorage, keep as-is

### 3.6 Admin Scoring View (`/admin/candidates/[id]/score`)

- Same as interviewer scoring form
- Additionally:
  - All interviewers' comments listed below, each with delete button (`DELETE /admin/comments/:commentId`)
  - Overall comment field (`POST /admin/scores/overall-comment`)
  - Day-level interviewer stats panel (`GET /days/:dayId/interviewer-stats`)

### 3.7 Admin Roles (`/admin/roles`)

- `AdminSidebar` + `Shell`
- Assign primary interviewers per day — current logic kept, UX cleaned up
- Day selector → shows assigned primaries → add/remove

### 3.8 Admin Schedule (`/admin/schedule`)

- `AdminSidebar` + `Shell`
- Manage interview days + rounds
- Remove 404-fallback hack for `GET /days/:dayId/rounds` — API to add this endpoint
- Add book/unbook UI for rounds (`POST /admin/rounds/:id/book`, `POST /admin/rounds/:id/unbook`)
- Available rounds view using `GET /admin/rounds/available`

### 3.9 Admin Questions (`/admin/questions`)

- `AdminSidebar` + `Shell`
- CRUD categories + questions in one page
- Add missing edit question (`PUT /admin/questions/:id`) — currently only create/delete exists
- Category accordion → questions list per category

---

## 4. shadcn Components

Install in this order:

```bash
# Fix components.json first, then:
npx shadcn@latest add button input label card textarea badge select checkbox
npx shadcn@latest add dialog sheet dropdown-menu alert scroll-area avatar separator tabs
npx shadcn@latest add table command
# External:
npm install sonner
```

Replace/fix:
- `dialog.tsx` — replace DIY with proper shadcn Radix dialog
- `avatar.tsx` — replace stub with real shadcn Avatar
- `button.tsx` + `input.tsx` — reinstall (remove `tw-` prefix bug)
- `labels.tsx` → split into `label.tsx` + `textarea.tsx`

All `alert()` calls replaced with `toast` (sonner).

---

## 5. Auth & Security

### 5.1 OAuth Flow

1. User clicks "Sign in with Google" → redirects to `${API}/login`
2. Backend owns full OAuth dance (PKCE with Google — backend responsibility)
3. Google → backend `/callback` → backend sets cookie → redirects to `${FRONTEND}/auth/loading`
4. `AuthProvider` calls `GET /auth/verify` → cookie sent automatically (never JS-accessible)
5. Context stores decoded user in memory only

### 5.2 Token Strategy

- **Access token:** short-lived (15–60 min), HttpOnly + Secure + SameSite=Strict cookie
- **Refresh token:** longer-lived (8–24h), HttpOnly cookie
- `apiRequest` in `api.ts` handles 401 → calls `GET /auth/refresh` → retries once → if refresh fails, redirect to `/`
- Backend requirements: PKCE, cookie flags, signature validation, expiry check on `/auth/verify`

### 5.3 Security Headers (`next.config.ts`)

```ts
headers: [
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Content-Security-Policy', value: "default-src 'self'; connect-src 'self' <API_ORIGIN_SET_AT_BUILD>; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'" },
]
```

### 5.4 Middleware (`middleware.ts`)

- Check cookie presence → missing: redirect `/`
- Decode JWT payload, check `exp` → expired: redirect `/` (UX gate, not security boundary — API enforces real auth)
- Check `isAdmin` for `/admin/*` → redirect `/unauthorized` if false
- Add comment: "JWT decode here is UX-only. API validates signature."

### 5.5 Logout

- `POST /auth/logout` clears HttpOnly cookie server-side
- Context cleared, redirect to `/`
- No localStorage/sessionStorage to clean (tokens never stored there)

---

## 6. Auto-Save

Applies to `/candidates/[id]/score` and `/admin/candidates/[id]/score`.

- Debounce: 1.5s after last score or comment change
- Score changes: `POST /scores/submit` per category (upsert — safe to repeat)
- Comment changes: `POST /candidates/:id/comments` (upsert)
- Sticky bottom bar states: `Saving...` → `Saved ✓` (3s then fade) → `Failed, retrying...`
- Retry: up to 3 attempts, then persistent `toast.error` + manual Save button fallback
- On mount: load existing scores + comment → populate form
- No unsaved-changes navigation warning needed

---

## 7. Responsive Breakpoints

| Breakpoint | Layout |
|---|---|
| `< 768px` (mobile) | Stack layout, AdminSidebar as Sheet drawer, score buttons full-width, table horizontal scroll |
| `768–1024px` (iPad) | AdminSidebar icon-only collapsed, table scrollable, scoring form single-column |
| `> 1024px` (laptop) | Full layout, AdminSidebar expanded, table multi-column |

---

## 8. Cleanup (delete before implementing)

**Frontend files to delete:**
- `src/components/ScoreDetailsDialog.tsx` — repurpose, don't delete; wire into admin candidates table
- `src/data/candidate-data.ts`
- `src/components/table.tsx`
- `src/lib/export.ts`
- `src/components/scoring/ScoringLayout.tsx`
- `src/app/edit_candidate/` (whole directory)
- `src/app/403/`

**npm deps to remove:**
- `react-icons`
- `fix`
- `@radix-ui/react-tooltip` (if tooltip component still not used after overhaul)

**Tailwind config fixes:**
- `tailwind.config.ts`: fix CSS variable syntax `"(var(--x))"` → `"hsl(var(--x))"`
- `components.json`: fix `tailwind.config.js` → `tailwind.config.ts`, fix CSS path to `src/app/styles/globals.css`
- `globals.css`: fix `--destructive` to a red value (e.g. `0 84% 60%` in HSL)

---

## 9. What Is Not Changing

- API endpoints (except adding `GET /days/:dayId/rounds` on backend)
- Dark theme color palette
- TanStack Table for data tables
- Recharts for radar chart + pie chart
- Google OAuth-only login
- Role system (primary/secondary/admin) logic
- localStorage preferences for candidate cards

---

## 10. Out of Scope

- Google Sheets export (API has it, no UI — defer)
- `POST /scoring/simulate` UI — defer
- `GET /candidates/weighted-scores` collection view — defer
- Light mode toggle
