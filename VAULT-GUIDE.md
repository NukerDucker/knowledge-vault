---
title: Vault Structure Guide
tags: [meta, guide]
status: active
created: 2026-07-24
updated: 2026-08-11
---

# Vault Structure Guide

Single source of truth for how this vault is organized. Read this before creating new notes.

---

## Folder Map

```
00-inbox/                         ← unprocessed captures, process weekly

01-university/
  assignments-tracker.md          ← single hub for all years/subjects
  year-1/                         ← add subject subfolders when content exists
  year-2/
  year-3/
    os/                           ← Operating Systems
    uxui/                         ← UX/UI Design
    rtw/                          ← Ready to Work
    investment-planning/          ← Investment Planning (bonds report, stock analysis)
    ai/                           ← Artificial Intelligence (Rome pathfinding)
  year-4/
  courses/                        ← semester schedule, degree/study plans
  internship/
    internship-diary.md           ← general internship diary / leave forms
    agoda/                        ← Agoda IT internship sub-vault (2026)
  regulations/                    ← university rules, CEI regulations

02-homelab/                       ← hardware, network configs, self-hosting

03-programming/
  guides/                         ← dev reference guides
  projects/                       ← per-project vault-wiring notes

04-fitness/                       ← workout logs, PRs, plans

05-ai/
  projects/<name>/                ← session-state.md + edit-log.md per project
    nacl-nextpath-x/              ← NACL NextPath X session state + edit log
    rome-wasnt-build-in-a-day/   ← AI Rome pathfinding project
    casestudy01-os/               ← OS case study session notes
    drunkbill/                    ← Drunkbill project

06-nacl-kmitl/
  lab-setup/                      ← physical lab: layouts, power, TOR docs
  nextpath-x/                     ← system docs, ADRs, architecture, playbooks
    00-system-map/
    01-architecture/              ← design specs, integration designs
    02-operations-and-seeding/
    03-incident-playbooks/
    04-adrs/
    05-schema-and-data-quirks/

01-university/internship/agoda/   ← Agoda IT internship 2026 (own Obsidian sub-vault)
  01 Daily Notes/                 ← daily standup logs (YYYY-MM-DD.md)
  03 Tasks/                       ← laptop tracker, replacement tasks
  04 Knowledge Base/              ← Windows/Mac build guides, TARS procedures
  06 Projects/
    WallKeeper/                   ← Grafana video wall NUC restart script + keepalive design
    Project Keep Alive/           ← NUC uptime monitoring (Uptime Kuma / Proxmox)
  07 Templates/                   ← task/note templates
  08 Reference/                   ← scripts, external references
  99 Archive/                     ← deprecated notes
  CLAUDE.md                       ← Agoda vault–specific guidance

90-archive/                       ← closed / superseded, keep for reference
```

---

## File Naming

```
kebab-case.md
```

- All lowercase, hyphens not underscores
- Descriptive: `uxui-week3-market-comparison.md` not `UX_UI_Final.md`
- Date prefix for time-bound one-offs: `2026-07-24-meeting-notes.md`
- PDFs: keep original filename

---

## Required Frontmatter

```yaml
---
title: Note Title
tags: [tag1, tag2]
status: active   # active | draft | archived
created: 2026-07-24
updated: 2026-07-24  # add when significantly revised
---
```

---

## Where Things Go — Decision Table

| Content type | Path | Example |
|-------------|------|---------|
| Assignment tracker hub | `01-university/` | `assignments-tracker.md` |
| Assignment detail note | `01-university/year-N/<subject>/` | `uxui-week3-market-comparison.md` |
| Semester schedule | `01-university/courses/` | `semester-schedule-2026.md` |
| Degree / study plan | `01-university/courses/` | `cei-study-plan.md` |
| University regulations | `01-university/regulations/` | `cei-regulations-summary.md` |
| Internship diary / reports / forms | `01-university/internship/` | `internship-diary.md` |
| Dev reference guide | `03-programming/guides/` | `senior-frontend-developer-guide.md` |
| Vault wiring notes (per repo) | `03-programming/projects/` | `nacl-nextpath-x.md` |
| AI project session state | `05-ai/projects/<name>/` | `session-state.md` |
| Physical lab docs, layouts | `06-nacl-kmitl/lab-setup/` | `601-lab-layout.png` |
| System docs, ADRs, architecture | `06-nacl-kmitl/nextpath-x/` | `01-architecture/` |
| NACL design specs / integration docs | `06-nacl-kmitl/nextpath-x/01-architecture/` | `2026-07-07-camellya-frontend-overhaul-design.md` |
| Agoda internship daily notes | `01-university/internship/agoda/01 Daily Notes/` | `2026-05-26.md` |
| Agoda internship project docs | `01-university/internship/agoda/06 Projects/<name>/` | `WallKeeper/` |
| Agoda KB articles | `01-university/internship/agoda/04 Knowledge Base/` | `NH Laptop Spec.md` |
| Unprocessed capture | `00-inbox/` | — |
| Old / closed / superseded | `90-archive/` | — |
| University PDFs / slides / physical docs | `~/Documents/University/Year-N/<Subject>/` | `A1 Foundation knowledge.pdf` |

---

## Document Storage Rule

Physical university files (PDFs, PPTX/slides, Word docs) go in `~/Documents/University/` mirroring the vault year/subject structure. The vault note for that subject includes a `**File:**` path so Obsidian notes link to their source documents.

Example mapping:
```
Vault note:  01-university/year-3/rtw/rtw-a2-labour-law.md
Source file: ~/Documents/University/Year-3/Ready To Work/A2 Labour law.pdf
```

When AI summaries are generated (via NotebookLM or similar), embed the summary in the vault note under a `## Knowledge` or `## Summary` section.

---

## Hub + Spoke Pattern

**Hub notes** aggregate and link out via `[[wikilink]]`.  
**Spoke notes** link back at the bottom: `*See also: [[hub-note]]*`

Example:
- Hub: `assignments-tracker.md` → links to each assignment file
- Spoke: `uxui-ui-hunt.md` → ends with `*See also: [[assignments-tracker]]*`

---

## Tag Conventions

| Tag | Use |
|-----|-----|
| `university` | Coursework, academic notes |
| `assignment` | Active assignment with a deadline |
| `kmitl` | KMITL institutional |
| `nacl` | NACL lab work |
| `ai` | AI projects |
| `homelab` | Home lab infrastructure |
| `fitness` | Fitness tracking |
| `meta` | Vault structure and guides |

---

## Inbox Processing Rule

Clear `00-inbox/` weekly:
1. File into the correct folder with proper frontmatter
2. Or delete if no longer relevant

---

## What NOT to Track Here

- Source code (lives in the actual repo)
- AI session context files (`.ai/`, `.claude/` inside child repos — gitignored there)
- Temporary scratch notes (delete after use)
