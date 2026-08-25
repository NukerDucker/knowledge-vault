---
title: DrunkBill — Session State
tags: [programming, project]
status: active
---

# DrunkBill — session state

**Repo:** `~/Documents/University/drunkbill` (Svelte 5 runes + TS + Vite + Tailwind 4, Bun)
**What it is:** static client-only Thai-Baht bill splitter. Integer-satang money model, largest-remainder split, localStorage persistence with `parseBill` trust boundary. See repo `CLAUDE.md` for architecture invariants.

## 2026-07-22 — Receipt UI + drunk-proof layout

**Goal (user intent):** receipt look, but *only for the summary*; minimize scrolling ("least scroll as much as possible") — adding items past 3 forced page scroll, bad when drunk. Plus: `Select all` for who-contributes, and see who eats what + how many divide per item.

**Shipped (commit `c8d8477`):**
- **Layout:** `App.svelte` now `h-screen overflow-hidden`, 3-column grid (People+Charges | Items | Summary). Only the middle `ItemList` scrolls internally (`overflow-y-auto`, `min-h-0`); page never grows, summary always visible. Add-item button pinned above the scroll region.
- **Receipt aesthetic reserved for Summary column only** — `.paper`, `.paper-edge` (scalloped torn edge via CSS mask), `.rule`, `.receipt-h` in `src/app.css`. Working panels stay normal `bg-card` surfaces.
- **ItemCard** rewritten compact: inline underline name input, small qty×price, tappable assignee **chips** (filled = selected) instead of checkboxes, `Select all`/`Clear all` button, inline per-person breakdown list + `÷ N` divide count.
- **Store:** added `BillStore.setAllAssignees(itemId, on)` in `bill.svelte.ts`. No schema/`BILL_VERSION` change.

**Verified:** `bun run check` 0 errors, `bun run test` 27/27, `bun run build` clean.

**Open / follow-ups:**
- User then asked to move the per-item "who eats what" breakdown into a **per-person dropdown under each name in the Summary** (in progress).
- No browser visual QA yet — check mobile width (chip wrap, item scroll).
- `toKhunThong` still the `ponytail:` stub (unconfirmed LINE-bot syntax).
