---
title: "UX/UI: Sign In / Sign Up Self-Checklist (Student Version)"
tags:
  - university
  - uxui
  - individual
  - figma
status: submitted
created: 2026-08-25
updated: 2026-08-26
subject: uxui
---

# UX/UI — Sign In / Sign Up Self-Checklist

> [!info] Status
> **Submitted 2026-08-26.** Design + clickable prototype complete in Figma.
> Deadline and points still **TBA** — add `due:` and `points:` to the frontmatter
> when known and the tracker will pick it up automatically.

## Assignment

Design Sign In and Sign Up pages that satisfy a self-check list before submission.

**Sign In**
- Email/Username and Password fields
- Sign In button clear and noticeable
- Forgot password link
- Link to Sign Up page
- Error or validation messages

**Sign Up**
- Email, Password, Confirm Password fields
- Password requirements shown
- Password and Confirm Password match
- Terms & Privacy checkbox
- Link back to Sign In

## Product Context

Framed as the login flow for a **KMITL room / facility booking app** — same product family as the Week 5–6 facility booking work ([[uxui-week5-pov-hmw]], [[uxui-week6-hooked-kano]]). Avoids a context-free template login and lets the fields carry real meaning:

- Sign In accepts **Student ID or Email** (`67011178`) — how KMITL students actually identify themselves.
- Sign Up gates on **@kmitl.ac.th** with helper text — campus identity is what makes a person eligible to book a room.
- Terms wording is booking-specific: "I agree to the Booking Terms and Privacy Policy".

## Design Spec

| | |
|---|---|
| Figma file | https://www.figma.com/design/AbdHj7iltcgiZslPoiFC9P |
| Frame | iPhone 17 — 402 × 874 pt |
| Sign In node | `4:2` |
| Sign Up node | `5:2` |
| Booking Home node | `18:2` (prototype destination stub) |
| Forgot Password node | `18:29` (prototype destination stub) |
| Typeface | Inter — Regular / Medium / Semi Bold / Bold |

**Palette**

| Token | Hex | Use |
|---|---|---|
| Orange | `#E8622D` | Primary button, links, logo tile, checkbox |
| Navy ink | `#1B2A5B` | Headings, labels, home indicator |
| Muted | `#6B7280` | Body text, placeholders, helper text |
| Border | `#D3D7DE` | Input outlines (default) |
| Error | `#DC2626` | Failed-validation border + message |
| Success | `#17994F` | Met requirements, password-match state |

**Layout rules**

- Full auto-layout, no absolute positioning inside frames.
- 24 pt side padding; status bar 9:41 row on top, home indicator bar (134 × 5) at bottom.
- Content column is `SPACE_BETWEEN` — form group top, cross-link footer pinned to bottom.
- Inputs 10 pt radius, 15/16 pt vertical padding; primary buttons ≥ 48 pt tall for tap targets.

## Prototype

Flow starting point: **Sign In (`4:2`)** — `page.flowStartingPoints = [{ nodeId: '4:2', name: 'Sign In / Sign Up Flow' }]`. Press play from any frame and it opens on Sign In.

| Hotspot | Node | Destination | Transition |
|---|---|---|---|
| Footer "Sign up" | `4:30` | Sign Up `5:2` | Push ← 300 ms |
| Footer "Sign in" | `5:41` | Sign In `4:2` | Push → 300 ms |
| Sign In button | `4:26` | Booking Home `18:2` | Push ← 300 ms |
| Create Account button | `5:37` | Booking Home `18:2` | Push ← 300 ms |
| "Forgot password?" | `4:25` | Forgot Password `18:29` | Push ← 300 ms |
| "← Back" | `18:35` | Sign In `4:2` | Push → 300 ms |
| Footer "Sign in" (reset screen) | `18:47` | Sign In `4:2` | Push → 300 ms |

All triggers are `ON_CLICK` with `navigation: 'NAVIGATE'`. Verified by reading `node.reactions` back after the write — a screenshot cannot show whether a reaction landed.

**Two stub destinations** were added so the primary CTAs go somewhere instead of dead-ending:

- **Booking Home (`18:2`)** — greeting, three available-room cards, "Book a Room" CTA. Deliberately shallow; it exists to prove the auth flow terminates in the product.
- **Forgot Password (`18:29`)** — email field, "Send Reset Link", back link. Same reason.

Neither stub is graded content. The "Book a Room" CTA on Booking Home is intentionally unwired — the flow ends there.

**Scope note:** the two graded frames (`4:2`, `5:2`) still render their live error/success states, so the prototype opens on a screen that already shows "⚠ Incorrect password". That is a deliberate trade — the validation states are the checklist items and have to be visible statically. A fuller prototype would duplicate both screens into resting variants and wire button-click → error state.

## Checklist Coverage

| Required item | Where it lives |
|---|---|
| Email/Username + Password | Sign In fields 1–2 |
| Clear Sign In button | Full-width orange primary |
| Forgot password link | Right-aligned under password |
| Link to Sign Up | Footer — "New to KMITL Booking? **Sign up**" |
| Error / validation message | Password shown in error state: red border + "⚠ Incorrect password. Please try again." |
| Email + Password + Confirm | Sign Up fields 1–3 |
| Password requirements shown | Live list under password: ✓ 8+ characters, ✓ 1 uppercase, ○ 1 number |
| Password / Confirm match | Green border + "✓ Passwords match" |
| Terms & Privacy checkbox | Checked orange checkbox row |
| Link back to Sign In | Footer — "Already have an account? **Sign in**" |

Both screens deliberately render a **live validation state** rather than an empty resting form — the error and success states are the graded items, so they have to be visible in the static frame.

## Files

**Exports:** `~/Documents/University/Year-3/UXUI/signin-signup-assets/`
- `signin-iphone17.png` — 402 × 874
- `signup-iphone17.png` — 402 × 874

Booking Home and Forgot Password stubs are not exported — they are prototype scaffolding, not submission screens.

An earlier 440 px web-card iteration of both screens is kept on the same Figma canvas (nodes `1:2`, `2:2`) for comparison.

## Build Notes

Frames were generated through the Figma MCP plugin API, not drawn by hand. Two things that bit:

- Setting `layoutMode` on a frame **after** `resize()` makes it re-hug its content — the 56 × 56 logo tile collapsed to the width of the letter "K". Fix: set `primaryAxisSizingMode` / `counterAxisSizingMode` to `FIXED`, then resize.
- `layoutSizingHorizontal = 'FILL'` only works once the node is already a child of an auto-layout parent, so `appendChild` has to come first.

## Open

- [ ] Confirm whether the brief wants clickable navigation only or a graded state demo — if the latter, add resting-state duplicates of `4:2` / `5:2`
- [ ] Confirm deadline + point value, then add `due:`/`points:` to frontmatter (the tracker row generates itself)
- [x] Export final submission PDF — submitted 2026-08-26
