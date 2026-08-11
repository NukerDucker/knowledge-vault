> Related: [[NH Laptop Spec]] | [[Return Laptop]] | [[PPID]]

## Autopilot Group Tags

Assign the correct group tag **before** pre-provisioning. This determines which software gets auto-installed.

| Department                           | Group Tag             | Extra Software            |
| ------------------------------------ | --------------------- | ------------------------- |
| CEG                                  | `Autopilot-Azure-CEG` | Genesys                   |
| IT                                   | `Autopilot-Azure-IT`  | Slack, local admin rights |
| All others (People, Marketing, etc.) | `Autopilot-Azure`     | —                         |

## Pre-Provisioning Steps

> Source: [How to build with Autopilot Pre-provisioning](https://agoda.atlassian.net/wiki/spaces/Desktop/pages/316343403) *(last updated 2026-03-16 — verify if anything changed)*

**Requirements:** Machine must already be enrolled in Autopilot. Must be connected to **LAN** (Wi-Fi not supported for pre-provisioning).

Pre-provisioning reduces setup time from ~40 min → 10–15 min.

1. If reusing a machine: reset Windows and delete the Intune account (keep the Azure AD / Autopilot entry)
2. Assign the correct group tag (see table above)
3. Connect to LAN
4. Boot the machine — at the OOBE screen, press **Windows key × 5** to open the Pre-provisioning menu
5. Select **"Pre-provision with Windows Autopilot"** → click Next
6. Verify: Organization = `agoda.onmicrosoft.com`, Deployment profile = `Autopilot Azure Joined`
7. Click **Next** and wait for completion
8. Click **Reseal** → machine shuts down
9. Pack and assign to staff (see: Assigning assets to staff on Confluence)

## Peripherals Package

| Employee Type | Package Contents |
| ------------- | ---------------- |
| IT | Laptop, Charger |
| Non-IT | Laptop, Charger |
| Non-IT CEG | Laptop, Charger, Headset |

> **Keyboard & Mouse (Wireless):**
> - **Intern** — item is on loan; update keyboard and mouse on **Kace** for return when they leave
> - **Regular / Temp / Full-time** — given away permanently; no Kace update needed

## New Hire Delivery

- Workplace delivers laptop to **CEN 16 Conference Room** every **Monday at 08:30**
- Desktop Support attends onsite to complete enrollment
- User setup checklist:
  - [ ] Windows Hello (PIN / Fingerprint / Face)
  - [ ] Okta Fastpass

## File Transfer Notes

- **Cursor IDE data** — if the user wants to migrate Cursor settings/extensions/state to a new machine, copy both:
  - `C:\Users\<username>\AppData\Roaming\Cursor` — settings, keybindings, extensions
  - `C:\Users\<username>\.cursor` — user-level config and workspace data

## New Hire List

New joiners are announced on SharePoint by the Onboarding team:
[Desktop Support - New Hire List (BKK)](https://agoda.sharepoint.com/sites/IT-Support/Lists/New%20Hire%20List%20For%20Desktop%20BKK%20Team/AllItems.aspx)
