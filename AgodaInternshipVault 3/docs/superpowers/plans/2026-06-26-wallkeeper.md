# WallKeeper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a biweekly scheduled full reboot on each video wall NUC, validated on OptiPlex #2 first.

**Architecture:** A single PowerShell script writes a timestamped log entry then reboots the machine. A Windows Task Scheduler job runs the script every other Friday at 12:00 PM as SYSTEM. The script is tested on OptiPlex #2 by manually triggering the task before deploying to live NUCs.

**Tech Stack:** PowerShell 5.1+ (built into Windows), Windows Task Scheduler

## Global Constraints

- Script path on every machine: `C:\Scripts\restart_videowall.ps1`
- Log file: `C:\VideoWallLogs\restart_log.txt`
- Scheduled task name: `WallKeeper - Biweekly Reboot`
- Task runs as: `SYSTEM`
- Trigger: Weekly, every 2 weeks, Friday, 12:00 PM
- Execution policy: `Bypass` (passed as argument, not set system-wide)

---

### Task 1: Create and deploy the restart script on OptiPlex #2

**Files:**
- Create: `C:\Scripts\restart_videowall.ps1` (on OptiPlex #2)
- Create: `C:\VideoWallLogs\` directory (created by the script itself)

**Interfaces:**
- Produces: `restart_videowall.ps1` — callable by Task Scheduler with no arguments

- [ ] **Step 1: Create the Scripts directory on OptiPlex #2**

Open PowerShell as Administrator and run:
```powershell
New-Item -ItemType Directory -Path "C:\Scripts" -Force
```
Expected: directory created (or already exists — no error either way).

- [ ] **Step 2: Write the script**

Create `C:\Scripts\restart_videowall.ps1` with this exact content:
```powershell
$logFile = "C:\VideoWallLogs\restart_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if (!(Test-Path "C:\VideoWallLogs")) {
    New-Item -ItemType Directory -Path "C:\VideoWallLogs"
}

Write-Output "[$timestamp] Initiating biweekly reboot..." | Tee-Object -FilePath $logFile -Append
Restart-Computer -Force
```

- [ ] **Step 3: Verify the script exists and is readable**

```powershell
Get-Content "C:\Scripts\restart_videowall.ps1"
```
Expected: prints the full script content with no errors.

---

### Task 2: Create the Task Scheduler job on OptiPlex #2

**Files:**
- Modify: Windows Task Scheduler (no file — configured via GUI or PowerShell)

**Interfaces:**
- Consumes: `C:\Scripts\restart_videowall.ps1` from Task 1
- Produces: Scheduled task named `WallKeeper - Biweekly Reboot`

- [ ] **Step 1: Create the scheduled task via PowerShell (run as Administrator)**

```powershell
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument '-ExecutionPolicy Bypass -NonInteractive -File "C:\Scripts\restart_videowall.ps1"'

$trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -WeeksInterval 2 `
    -DaysOfWeek Friday `
    -At "12:00PM"

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5) `
    -RunOnlyIfNetworkAvailable $false

$principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName "WallKeeper - Biweekly Reboot" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force
```
Expected: output shows `TaskName: WallKeeper - Biweekly Reboot` with `State: Ready`.

- [ ] **Step 2: Verify the task appears in Task Scheduler**

```powershell
Get-ScheduledTask -TaskName "WallKeeper - Biweekly Reboot" | Select-Object TaskName, State
```
Expected:
```
TaskName                      State
--------                      -----
WallKeeper - Biweekly Reboot  Ready
```

---

### Task 3: Validate on OptiPlex #2

**Files:**
- Read: `C:\VideoWallLogs\restart_log.txt` (created on first run)

**Interfaces:**
- Consumes: scheduled task from Task 2
- Produces: confirmed working reboot + log entry

- [ ] **Step 1: Manually trigger the task**

```powershell
Start-ScheduledTask -TaskName "WallKeeper - Biweekly Reboot"
```
Expected: machine reboots within a few seconds.

- [ ] **Step 2: After reboot — verify the log entry was written**

Open PowerShell as Administrator and run:
```powershell
Get-Content "C:\VideoWallLogs\restart_log.txt"
```
Expected output (timestamp will vary):
```
[2026-06-26 12:00:00] Initiating biweekly reboot...
```

- [ ] **Step 3: Check Task Scheduler last run result**

```powershell
(Get-ScheduledTaskInfo -TaskName "WallKeeper - Biweekly Reboot").LastTaskResult
```
Expected: `0` (means success). Any other number = error.

- [ ] **Step 4: Note result in vault**

Open `06 Projects/Project Keep Alive/WallKeeper.md` and add a test result line under the script section:
```
**Test on OptiPlex #2:** [date] — reboot confirmed, log entry written, last result = 0
```

---

### Task 4: Deploy to live NUCs

**Files:**
- Create: `C:\Scripts\restart_videowall.ps1` (on each live NUC — same content as Task 1)
- Modify: Windows Task Scheduler on each live NUC (same job as Task 2)

**Interfaces:**
- Consumes: validated script + task config from Tasks 1–3

- [ ] **Step 1: For each live NUC — copy the script**

RDP or physically access each NUC. Open PowerShell as Administrator:
```powershell
New-Item -ItemType Directory -Path "C:\Scripts" -Force
```
Then create `C:\Scripts\restart_videowall.ps1` with the same content as Task 1 Step 2.

- [ ] **Step 2: For each live NUC — create the scheduled task**

Run the same PowerShell block from Task 2 Step 1 on each NUC.

- [ ] **Step 3: For each live NUC — verify the task**

```powershell
Get-ScheduledTask -TaskName "WallKeeper - Biweekly Reboot" | Select-Object TaskName, State
```
Expected: `State: Ready` on each NUC.

- [ ] **Step 4: Update vault tracker**

In `06 Projects/Project Keep Alive/WallKeeper.md`, record each NUC it was deployed to and the deployment date.
