# WallKeeper + Keep Alive — Design Spec
**Date:** 2026-06-26

---

## Context

Two complementary projects that together prevent and detect video wall NUC failures:

- **WallKeeper** — prevention: biweekly scheduled reboot of each NUC to clear accumulated state before a freeze occurs
- **Keep Alive** — detection: ping + HTTP monitoring via Uptime Kuma, with a status page showing real-time NUC health

Both are validated on a test bed (OptiPlex #2) before touching live NUCs.

---

## Hardware

| Machine | Role |
|---|---|
| OptiPlex #1 | Proxmox host → Uptime Kuma LXC (monitoring) |
| OptiPlex #2 | Test target ("fake NUC") — Windows + browser on Grafana page; also WallKeeper test bed |
| Live NUCs (1–2) | Production targets — added to monitoring after test bed validation |

---

## WallKeeper

### Behaviour

- Runs on each NUC (and OptiPlex #2 for testing) via Windows Task Scheduler
- Trigger: every 2 weeks, Friday, 12:00 PM
- Action: full machine reboot (`Restart-Computer -Force`)
- Logs a timestamped line to `C:\VideoWallLogs\restart_log.txt` before rebooting

### Script (`restart_videowall.ps1`)

```powershell
$logFile = "C:\VideoWallLogs\restart_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if (!(Test-Path "C:\VideoWallLogs")) {
    New-Item -ItemType Directory -Path "C:\VideoWallLogs"
}

Write-Output "[$timestamp] Initiating biweekly reboot..." | Tee-Object -FilePath $logFile -Append
Restart-Computer -Force
```

### Task Scheduler job settings

| Field                         | Value                                                                             |
| ----------------------------- | --------------------------------------------------------------------------------- |
| Trigger                       | Weekly, every 2 weeks, Friday, 12:00 PM                                           |
| Action                        | `powershell.exe -ExecutionPolicy Bypass -File "C:\Scripts\restart_videowall.ps1"` |
| Run As                        | SYSTEM                                                                            |
| Run whether user is logged on | Yes                                                                               |
| Hidden                        | Yes                                                                               |

### Validation on OptiPlex #2

1. Place script at `C:\Scripts\restart_videowall.ps1`
2. Create the scheduled task with above settings
3. Right-click task → Run → confirm machine reboots and log entry written
4. Check Task Scheduler history: last run result = `0x0`
5. Once passing, deploy identically to each live NUC

---

## Keep Alive

### Architecture

```
OptiPlex #1 (Proxmox)
  └── Uptime Kuma LXC (Debian, direct install, no Docker)
        ├── Ping monitor    — OptiPlex #2
        ├── HTTP monitor    — OptiPlex #2 Grafana URL
        ├── Ping monitor    — NUC #1  (added after test bed passes)
        └── HTTP monitor    — NUC #1  (added after test bed passes)

Status Page → published on internal network
```

### Monitor config (per device)

**Ping monitor**
- Type: `Ping`
- Name: e.g. `Video Wall — Floor 3 (ping)`
- Hostname: device IP
- Interval: 60s
- Retries: 2

**HTTP monitor**
- Type: `HTTP(s)`
- Name: e.g. `Video Wall — Floor 3 (grafana)`
- URL: local Grafana/MagicSign URL the device displays
- Interval: 60s
- Retries: 2

### Phases

| Phase | Deliverable | Done when |
|---|---|---|
| 1 | Proxmox on OptiPlex #1 + Uptime Kuma LXC provisioned | Kuma UI at `http://<lxc-ip>:3001` reachable |
| 2 | Ping + HTTP monitors for OptiPlex #2 | Both show green |
| 3 | Status page published | URL accessible from another machine on the network |
| 4 | Test cases validated on OptiPlex #2 | All three cases below pass |
| 5 | Same monitors added for live NUCs | Production wall covered |
| Later | Email (SMTP) alerts | Out of scope for now |

### Test cases (Phase 4)

| Test | Action | Expected result |
|---|---|---|
| Offline | Unplug OptiPlex #2 network cable | Ping monitor → Down on status page after ~2 min |
| Freeze | Kill browser on #2 (machine stays up) | HTTP monitor → Down; ping stays Up |
| Recovery | Restore network / relaunch browser | Both monitors → Up |
| WallKeeper reboot | Trigger scheduled task on #2 | Brief ping Down → Up; validates both projects together |

---

## Out of Scope (this phase)

- Email / SMTP alerts (documented in Uptime Kuma Setup.md, add after status page is stable)
- Prometheus + Grafana integration (Phase 5 in Keep Alive.md)
- Automated recovery via smart plug / PDU
- Root-cause diagnostics (crash dumps, thermal logging)
