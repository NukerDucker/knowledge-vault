# NUC Training Summary

Source: `NUC Training.pdf` — Desktop Team / Global Delivery Support Team (2024)

---

## What is NUC?

**NUC (Next Unit of Computing)** is a mini-computer attached to office TVs to display:
- **Grafana dashboards** — real-time team monitoring
- **Signage** — internal communications (e.g. CEG, IT dept announcements)

Remote access:
- **Users** → Rustdesk (VNC)
- **GSD team** → TeamViewer

---

## How to Build a NUC

### 1. Prepare Hardware

| Option | Pros | Cons |
|---|---|---|
| Intel NUC | Small, mounts behind TV | Performance/heating issues |
| Dell OptiPlex | Higher performance, reliable | Larger size |

> Recommend: **Dell OptiPlex** as the next-gen NUC standard.

**OS:** Windows 10 LTSC, patch version **21H2**
- Check version: `Win+R` → `winver`
- After install: press `Ctrl+Shift+F3` to skip OOBE → Audit mode → run Windows Update

### 2. Assign Autopilot Profile

Run in PowerShell (as admin) in Audit mode:
```powershell
Set-ExecutionPolicy bypass
Install-Script -name Get-WindowsAutopilotInfo -force
Get-WindowsAutopilotInfo -Output C:\temp\Autopilot.csv
```
- Login with Okta when prompted
- Open Sysprep (`C:\Windows\System32\Sysprep\sysprep.exe`) → exit Audit mode → back to OOBE
- In Intune → Autopilot → **Import** the CSV → wait 10–15 min
- Assign group tag: **`Autopilot-NUC`**

### 3. Enroll Machine

- At OOBE, log in with **`gsduser@agoda.com`** (OTP from 1Password)
- Wait for device setup to complete and Desktop to appear

### 4. Check Policy & Apps

- In Intune → device Properties → **Change Primary User** from `gsduser` to `IT-Dataview`
- Sign out of gsduser → machine auto-logs in as IT-Dataview
- Go to **Settings → Accounts → Access work or school → Sync**
- After sync, rename device using pattern:
  - Multi-floor: `DV-XXXYYY07-15` (Site + Building + Floor + NUC#)
  - Single-floor: `DV-XXX-15` (Site + NUC#)

---

## MagicSign

**MagicSign** is digital signage software used to push media to NUC displays — functions like a notice board/billboard for internal communications.

### Install Steps
1. Download installer, run via PowerShell
2. Software auto-starts after install
3. Select device name → bind to MagicSign server
4. Run **MagicSign Engine** to start media playback

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Script fails to add machine to Agoda tenant (Unauthorized) | Intune role not active | Activate **Intune-Role-GSD-L1-L2** in Azure admin → retry |
| Login with `it-dataview` at OOBE fails | Account has 5-machine limit | Use **`gsduser@agoda.com`** instead |
