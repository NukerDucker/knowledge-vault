---
title: Course Registry
tags: [university, kmitl]
status: active
created: 2026-10-11
updated: 2026-10-11
---

# Course Registry

**Single authority for `code ↔ course ↔ vault folder`.** Every assignment note's
`course:` frontmatter resolves against this table; `_meta/check.sh` enforces it. Room,
time and exam data live in [[semester-schedule-2026]] and are not repeated here.

KMITL Computer Engineering (International), student 67011178.

## Current term — AY 1/2026, Year 3

| Code | Official name | Short | Vault folder | Credits | Section |
|---|---|---|---|---|---|
| `01276342` | Artificial Intelligence | AI | `01-university/year-3/ai/` | 3(3-0-6) | 901 |
| `01276314` | Microcontroller Interfacing | MCU | `01-university/year-3/mcu/` | 4(3-3-8) | 901 + 1901 (lab) |
| `01276324` | Operating Systems | OS | `01-university/year-3/os/` | 3(3-0-6) | 901 |
| `01276521` | Practice of System Administration | SysAdmin | `01-university/year-3/sysadmin/` | 3(3-0-6) | 901 |
| `01276545` | User Experience and User Interface Design | UX/UI | `01-university/year-3/uxui/` | 3(3-0-6) | 901 |
| `96642162` | Ready to Work | RTW | `01-university/year-3/rtw/` | 3(3-0-6) | 101 |
| `96643026` | Investment Planning | — | `01-university/year-3/investment-planning/` | 3(3-0-6) | 101 |

**Total: 28 credits for the term** — 22 from the seven taught courses above, plus 6 transferred
Practice credits (below). Only Microcontroller Interfacing is a 4-credit course; its lab (1901)
carries no separate credits. Reconciles with [[cei-study-plan]] Year 3 Sem 1.

## Transferred practice credits

Not taught courses — no timetable slot, no vault folder, no `subject:` key. Earned through
practice work and counted toward the term. These are the internship credits.

| Code | Title | Credits |
|---|---|---|
| `0100655` | Practice Under Personal & Professional Skills 1 | 1 |
| `0100656` | Practice Under Personal & Professional Skills 2 | 2 |
| `0100657` | Practice Under Personal & Professional Skills 3 | 3 |

## Subject key

The `subject:` frontmatter field is the **folder key**, never the code. The `course:` field is
the **registrar code**. Both are required on assignment notes.

| `subject:` | `course:` |
|---|---|
| `ai` | `01276342` |
| `mcu` | `01276314` |
| `os` | `01276324` |
| `sysadmin` | `01276521` |
| `uxui` | `01276545` |
| `rtw` | `96642162` |
| `investment-planning` | `96643026` |

## Not courses

| Folder | What it is |
|---|---|
| `01-university/nacl/` | NACL work — a company engagement, not a registered course. No code |

## Electives

Practice of System Administration and UX/UI Design are CE electives. Intro to Data Analytics
(`01276551`) is **not enrolled** — it appears on CEI-wide lists but not on the registration
system. Ignore it.

## Open

| Item | Detail |
|---|---|
| Next term | No AY 2/2026 rows yet. Add them here when registration opens; do not delete this term's rows |

---

*See also: [[semester-schedule-2026]] · [[cei-study-plan]] · [[assignments-tracker]]*
