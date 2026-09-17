---
title: House Samyan QR Ticket Generator
tags: [work, house-samyan, tools, programming]
status: stable
---

# House Samyan QR Tool

Web tool for generating QR-coded tickets for House Samyan cinema staff.
Code lives at `~/Code/hs-qr`. Staff open the deployed URL — no install.

**Use case:** Customer can't open ticket but remembers seat → staff finds movie/showtime → selects seat on map → enters ticket ID from booking system → generates QR to let them in.

## Deploy

```bash
cd ~/Code/hs-qr/worker
npx wrangler deploy
```

Share the `hsqr.*.workers.dev` URL with staff.

## How to use

1. **Pick a Movie** — browse poster grid (Now Showing / Coming Soon tabs), click movie card
2. **Choose Showtime** — click a showtime row; seat map loads automatically
3. **Select Your Seat** — click seat on map or type e.g. `K11`; badge shows Available / Sold / Suspended; click same seat again to deselect
4. **Enter Ticket Number** — enter from booking system
5. **Your QR Code** — renders instantly; Print button available

Bottom nav: Back / Confirm Seat / Generate QR / Next Ticket — contextual per step.

## Stack

- Cloudflare Worker (`worker/worker.js`) — single file: HTML + CSS + JS + API proxy
- Routes: `GET /` → web app · `GET /movies` → scraped movie list (5-min cache) · `GET /movie/{id}` → showtimes · `POST /seats` → seat map
- QR payload: `base64("ticket{ticket_id}{showtimes_seat_id}-{ticket_id}")`

## Seat status

| Badge | Meaning |
|---|---|
| ✓ Available | Can select |
| ● Sold | Already sold online — can still override |
| ✕ Suspended | Blocked, cannot select |

## Known quirks

- `caches.default` is no-op under `wrangler dev` (local mode) — movie cache only works on deployed worker
- Template literal gotcha: regex `\d` inside the HTML template literal must be written as `\\d` or V8 strips the backslash

## Related

- [[house-samyan-shift-codes]] — shift scheduling reference
