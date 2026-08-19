---
title: Vault Maintenance Log
tags: [vault, maintenance, hooks, claude]
status: active
created: 2026-08-16
---

# Vault Maintenance Log

Running log of structural changes to the KnowledgeVault itself — hooks, settings, conventions, folder changes.

---

## 2026-08-16

### Added RTW resume assignment note
- Created `01-university/year-3/rtw/rtw-resume-assignment.md`
- Due: 2026-08-27 (MS Teams submit by Aug 25)
- Requirements: photo, job position, summary, education, work experience, activities, skills (tech + soft), language skills (English TOEIC, Thai native)
- Rubric: 4pts — no late submission, all sections, appropriate language level

### Added Stop hook for auto session-note reminders
- Created `.claude/settings.json` (project-level) with `Stop` + `asyncRewake` hook
- Hook script: `~/.claude/hooks/vault-stop-reminder.sh`
- Behavior: when Claude stops in this vault, hook wakes Claude with reminder to update/create dated vault session notes
- Mirrors nacl-nextpath-x `session-end.sh` pattern

### TODOs
- None unresolved
