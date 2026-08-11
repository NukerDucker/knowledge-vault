# Autopilot Training Summary

Source: `Autopilot Training.pdf` — Desktop Team / Global Delivery Support Team (2024)

---

## What is Windows Autopilot?

A Microsoft technology to **pre-configure new devices** so they're ready for productive use out of the box. IT uploads device IDs → configures profiles → device self-deploys when the employee logs in.

Lifecycle: Purchase → Deploy → Self Service → Ready for Business → Steady State → End of Life / Break-fix

---

## Autopilot Group Tags

| Tag                   | Used For                          |
| --------------------- | --------------------------------- |
| `Autopilot-Azure-IT`  | IT users                          |
| `Autopilot-Azure-CEG` | CEG agent users                   |
| `Autopilot-Azure-CN`  | Users in China                    |
| `Autopilot-Azure`     | All other (non-IT, non-CEG) users |
| `Autopilot-NUC`       | Dataview/NUC machines             |

---

## How to Use Intune Autopilot

1. Go to **Microsoft Intune** → Devices → Windows → Windows enrollment → **Devices** (under Windows Autopilot)
2. View all enrolled devices with serial number, manufacturer, model, group tag, and profile status
3. Click a device → set **Group tag** in the side panel → Save

---

## How to Add a Machine to Autopilot Tenant

1. Open **Windows PowerShell ISE** as Administrator
2. Click **New Script**, enter:
```powershell
Set-ExecutionPolicy bypass
Install-Script -name Get-WindowsAutopilotInfo -force
Get-WindowsAutopilotInfo -Output C:\temp\Autopilot.csv
```
3. Highlight rows 1–2 first and run (accept any pop-ups with "Yes to All")
4. Then highlight row 3 and run — this exports hardware info to `C:\temp\Autopilot.csv`
5. Copy CSV to USB → upload to Intune Autopilot page (Import) → wait 10–15 min

---

## How to Install Windows OS

### Method 1: USB Drive
1. Prepare bootable USB (≥16GB) using Rufus or Etcher with Windows image
2. Boot laptop → press **F12** → select **UEFI: Generic Flash Disk**
3. Set Time/Currency format: **English (United States)**
4. Click **Install Now** → accept license → **Custom: Install Windows Only**
5. Delete all existing partitions → select Unallocated Space → Next
6. Wait for install → region selection screen appears

### Method 2: Windows MDT (Network)
MDT = Microsoft Deployment Toolkit — automates OS deployment over network.

1. Connect laptop to **VLAN 15** via LAN cable
2. Boot → press **F12** → select **Onboard NIC (IPv4)** or **USB IPv4** (via adapter)
3. Select **Autopilot V1.8** from boot menu
4. Choose task sequence (e.g. `14 - Autopilot - Windows 10 Ent_LTSC - NUC`)
5. Wait for install → region selection screen

---

## Pre-Provisioning a Laptop

After OS install, before handing to user:

1. At region screen → press **Ctrl+Shift+F3** to enter Audit mode (Desktop)
2. Run Windows Update until **No updates available**
3. Run Sysprep to return to OOBE
4. At OOBE → press **Windows button 5 times** → select **Pre-provision with Windows Autopilot**
5. Confirm Group tag details → click **Next**
6. Wait for device setup (security policies, certs, network, apps)
7. When complete → click **Reseal** → device is ready for delivery

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Can't add Group tag to machine | Intune admin role not active | Activate **Intune-Role-GSD-L1-L2** in Microsoft Entra admin center → My Roles → Groups → Activate |
| Pre-provisioning shows "Something went wrong / No profile found" | Group tag not assigned | Assign the correct Group tag in Intune Autopilot before running pre-provisioning |
