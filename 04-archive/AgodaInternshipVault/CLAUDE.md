# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About This Vault

This is an **Obsidian knowledge vault** used during an IT internship at Agoda. It stores IT support procedures, device provisioning guides, task tracking, and project notes — not application source code.

## Vault Structure

```
00 Inbox/          — Unsorted notes
01 Daily Notes/    — Daily standup/focus logs (YYYY-MM-DD.md)
03 Tasks/          — Weekly task tracking tables
04 Knowledge Base/ — Reference guides (Windows, Mac, general)
05 Meetings/       — Meeting notes
06 Projects/       — Ongoing project documentation
07 Templates/      — Note templates
08 Reference/      — Scripts and external reference material
99 Archive/        — Deprecated notes
```

## Key Knowledge Base Notes

- **`04 Knowledge Base/NH Laptop Spec.md`** — Laptop model assignments by employee type (Regular/Temp/Intern, IT vs non-IT)
- **`04 Knowledge Base/Windows Related/Windows Laptop Build.md`** — Full Autopilot pre-provisioning steps, group tag assignments by department, peripherals, new hire delivery process
- **`04 Knowledge Base/Windows Related/PPID.md`** — PowerShell one-liner to retrieve device PPID from WMI
- **`04 Knowledge Base/Mac Related/Mac Laptop Build.md`** — Decision table for which Mac enrollment method to use (DEP/JAMF Connect, User Initiated, ABM), plus full DEP build steps
- **`04 Knowledge Base/Mac Related/Troubleshoot Of MacBook.md`** — Mac troubleshooting table (Okta password sync, Agoda network, printer, Kace check-in)
- **`04 Knowledge Base/Return Laptop.md`** — Full laptop return process (TARS update, wipe, storage) and escalation timeline for unreturned devices

## Active Projects

- **WallKeeper** (`06 Projects/WallKeeper.md`) — Biweekly PowerShell restart script for Grafana video wall NUC machines running MagicSign; scheduled via Windows Task Scheduler every other Friday at 12:00 PM. Logs to `C:\VideoWallLogs\restart_log.txt`.
- **Keep Alive** (`06 Projects/Project Keep Alive/`) — Monitoring NUC/device uptime and network connectivity (Uptime Kuma / Proxmox); alive refresh every 1 hour.

## Task Tracking

- **New Hire Laptop Tracker** — `03 Tasks/NH Laptop Tracker - YYYY-MM.md` — Monthly tracker for new hire laptop preparation. Rows grouped by start date. Columns: Device Serial | Name | Email | Dept | Device Type | Device Model | Accessories | Status | Agoda ID | Role | Location | Notes.
- **Laptop Replacement** — `03 Tasks/Replacement - [Name].md` — One note per replacement request. Includes old/new device serials, checklist for file transfer (Loan tab in TARS if needed), enrollment, and Kace update.

## TARS Workflow Notes

- **Loan tab** — Managed by Technical Support. Use when user needs extra time to transfer files before returning old device.
- **Assets tab / Set As Received** — Managed by Assets Team after IT Support hands over the laptop.
- **Wipe ticket** — Auto-raised by TARS 2 weeks after Set As Received. Assigned to Technical Support to wipe and mark Set As Wiped.

## Reference

- **`08 Reference/claude_code_setup_win.ps1`** — Creates `~/.claude.json` with a GenAI personal token as `ANTHROPIC_AUTH_TOKEN`. Run once on a new Windows machine to configure Claude Code.

## Obsidian Conventions

- Internal links use `[[Note Name]]` syntax
- Daily notes follow the filename format `YYYY-MM-DD.md`
- Task tables use Markdown table format with status columns
- Confluence sources are cited with a link and last-updated date — treat older pages as potentially outdated and verify against current practice
