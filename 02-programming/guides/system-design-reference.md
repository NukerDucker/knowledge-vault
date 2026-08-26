---
title: System Design Interview — Reference
tags: [programming, system-design, reference, vendored]
status: stable
created: 2026-08-26
---

# System Design Interview — Reference

**What:** 28 chapter summaries of *System Design Interview: An Insider's Guide* (Alex Xu, Vol 1 + Vol 2).
**Why:** worked examples of software design — how real systems get scoped, estimated, and staged.
**Where:** `02-programming/guides/system-design-notes/`
**Stack:** Markdown + PNG diagrams. No build step.
**Constraint:** **vendored — not your writing.** Keeps upstream conventions (`README.md` per chapter, Title Case), exempt from vault naming and frontmatter rules, skipped by `check.sh`. Edit only to repair broken links.

This note is the vault-side door into that tree. The tree itself has no
frontmatter and 29 files all named `README.md`, so it cannot be linked by
wikilink — every link below is a relative markdown link instead.

---

## How to use it

Chapters 1–3 are the method; 4–28 are worked examples applying it. Read the
method first, then whichever system resembles the problem in front of you.

| Chapter | Read it for |
|---|---|
| [1 — Scaling](./system-design-notes/01-scaling/README.md) | single server → millions of users, one step at a time |
| [2 — Back-of-the-envelope](./system-design-notes/02-back-of-the-envelope-estimation/README.md) | sizing a system before designing it |
| [3 — Framework](./system-design-notes/03-system-design-framework/README.md) | the four-step interview method |

## Worked designs

**Fundamentals**

- [4 — Rate Limiter](./system-design-notes/04-rate-limiter/README.md)
- [5 — Consistent Hashing](./system-design-notes/05-consistent-hashing/README.md)
- [6 — Key-Value Store](./system-design-notes/06-key-value-store/README.md)
- [7 — Unique ID Generator](./system-design-notes/07-unique-id-generator/README.md)
- [8 — URL Shortener](./system-design-notes/08-url-shortener/README.md)
- [9 — Web Crawler](./system-design-notes/09-web-crawler/README.md)

**Consumer products**

- [10 — Notification System](./system-design-notes/10-notification-system/README.md)
- [11 — News Feed System](./system-design-notes/11-news-feed-system/README.md)
- [12 — Chat System](./system-design-notes/12-chat-system/README.md)
- [13 — Search Autocomplete](./system-design-notes/13-search-autocomplete/README.md)
- [14 — YouTube](./system-design-notes/14-youtube/README.md)
- [15 — Google Drive](./system-design-notes/15-google-drive/README.md)

**Location and mapping**

- [16 — Proximity Service](./system-design-notes/16-proximity-service/README.md)
- [17 — Nearby Friends](./system-design-notes/17-nearby-friends/README.md)
- [18 — Google Maps](./system-design-notes/18-google-maps/README.md)

**Infrastructure**

- [19 — Distributed Message Queue](./system-design-notes/19-distributed-message-queue/README.md)
- [20 — Metrics Monitoring and Alerting](./system-design-notes/20-metrics-monitoring-and-alerting-system/README.md)
- [21 — Ad Click Event Aggregation](./system-design-notes/21-ad-click-event-aggregation/README.md)
- [23 — Distributed Email Service](./system-design-notes/23-distributed-email-service/README.md)
- [24 — S3-like Object Storage](./system-design-notes/24-s3-like-object-storage/README.md)

**Transactional**

- [22 — Hotel Reservation System](./system-design-notes/22-hotel-reservation-system/README.md)
- [25 — Real-time Gaming Leaderboard](./system-design-notes/25-real-time-gaming-leaderboard/README.md)
- [26 — Payment System](./system-design-notes/26-payment-system/README.md)
- [27 — Digital Wallet](./system-design-notes/27-digital-wallet/README.md)
- [28 — Stock Exchange](./system-design-notes/28-stock-exchange/README.md)

## Source

- Book: [System Design Interview, Vol 1 + Vol 2 2nd Ed](https://www.goodreads.com/book/show/54109255-system-design-interview-an-insider-s-guide)
- Course: [bytebytego.com](https://bytebytego.com/courses/system-design-interview)
- Upstream index with the external reading list: [`system-design-notes/README.md`](./system-design-notes/README.md)

---

*See also: [[senior-frontend-developer-guide]]*
