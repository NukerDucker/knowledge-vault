> Related: [[Mac Laptop Build]] | [[Windows Laptop Build]] | [[NH Laptop Spec]]

## Loan Tab (Temporary Hold)

If the user needs extra time to transfer files before returning the old device:

1. **Technical Support** adds the device to the **Loan** tab in TARS
2. User completes file transfer (OneDrive sync recommended)
3. User returns the laptop → Technical Support removes it from Loan
4. Continue with the normal return process below

> The Loan tab is managed by Technical Support — separate from the Assets tab which is managed by the Assets Team.

---

## Normal Return Process

> Source: [Return Laptop](https://agoda.atlassian.net/wiki/spaces/Desktop/pages/316343218) *(last updated 2025-06-20)*

1. User returns laptop to **IT Support**
2. **IT Support** hands the laptop to the **Assets Team**:
   - Bangkok → hand to Assets Team directly
   - Outside Bangkok → put in local storage
3. **Assets Team** updates TARS:
   - Resigned staff → "Leavers" → **Set As Received** (auto-disables in AAD)
   - Not in TARS + resigned → check Workday for termination info; if missing, email manager + Data-Management Team
   - Returned/replaced/spare → Assets tab → **Set As Received**
4. **Assets Team** verifies status/owner in Kace and deactivates the computer account
5. After **2 weeks** — TARS automatically raises a wipe ticket assigned to **Technical Support**
6. **Technical Support** wipes the machine (Windows Reset or macOS Erase) and marks **Set As Wiped** in TARS (auto-deletes from Intune/JAMF)

> If AAD/Intune/Jamf can't be updated automatically, a ticket is raised and assigned to Assets Team to manually disable/delete in AD, AAD, Intune, or Jamf.

## Laptop Not Returned (Escalation Timeline)

| Day after last day | Action |
| :---: | --- |
| 1 | Contact via personal email + phone (see Workday); lock laptop; escalate to manager |
| 2 | 2nd reminder |
| 3 | 3rd reminder |
| 4 | Escalate to local POP/ER team |
| 7 | Escalate to Wanida |

Wanida handles write-off with confirmation from POP team + manager. Some countries require a Police Certificate for write-off.

Log all contact attempts with dates in the TARS ticket for audit trail.
