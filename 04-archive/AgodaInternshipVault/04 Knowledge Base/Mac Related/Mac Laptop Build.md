> Related: [[NH Laptop Spec]] | [[Return Laptop]] | [[Troubleshoot Of MacBook]]

## Which Build Method to Use?

> Source: [Build Mac Laptop](https://agoda.atlassian.net/wiki/spaces/Desktop/pages/316342575) *(last updated 2022-10-04 — may be outdated)*

| In Apple Business Manager (ABM)? | Apple Silicon / T2 Chip? | Personal/Contract Mac? | Method |
| :---: | :---: | :---: | --- |
| No | No | No | [User Initiated Enrollment](https://agoda.atlassian.net/wiki/display/Desktop/User+Initiated+Enrollment) |
| No | Yes | No | 1. [Add Mac into ABM](https://agoda.atlassian.net/wiki/display/Desktop/How+to+add+Mac+into+ABM) → 2. [JAMF Connect (DEP)](https://agoda.atlassian.net/wiki/display/Desktop/How+to+Setup+your+Mac+with+JAMF+Connect) |
| Yes | — | No | [JAMF Connect (DEP) — Automated Enrollment](https://agoda.atlassian.net/wiki/display/Desktop/How+to+Setup+your+Mac+with+JAMF+Connect) |
| — | — | Yes | [Onboard Personal/Contractor Mac to JAMF](https://agoda.atlassian.net/wiki/pages/viewpage.action?pageId=316343482) |

To identify chip type: [Apple Silicon models](https://support.apple.com/HT211814) · [T2 Chip models](https://support.apple.com/HT208862)

## DEP / JAMF Connect Build Steps (Primary Method)

> Source: [How to Setup your Mac with JAMF Connect](https://agoda.atlassian.net/wiki/spaces/Desktop/pages/316343401)

1. If new laptop — connect the HDD and reinstall the OS; no need to wipe the disk
2. If reinstalling — hold the power button to enter recovery mode, reinstall OS from the dedicated HDD
3. Click **Set As Wiped** in TARS (check Assets tab; if not there, check Loans)
   - Device will be auto-removed from JAMF Pro
   - If still showing in JAMF Pro, remove it manually and notify Trainers
4. Enroll MacBook to the user — verify the following are installed:
   - `agoda-hkgsubprod-CA`
   - `agoda-sgpsubcorp-CA`
   - Applications: Microsoft Products, Okta Verify
   - User's Certificate
5. Wait for all applications and policies to install
6. **Once done: assign device and update status in Kace**

> **Note:** No need to enable Location Services — set local time manually instead.

[[Troubleshoot Of MacBook]]
