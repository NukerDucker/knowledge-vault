## Get Device PPID

Used when a claimed laptop is still connected to another tenant and you need to identify it by PPID.

Run in PowerShell:

```powershell
(Get-CimInstance -ClassName Win32_BaseBoard).SerialNumber.Split('/')[2].Substring(0,2)+(Get-CimInstance -ClassName Win32_BaseBoard).Product+(Get-CimInstance -ClassName Win32_BaseBoard).SerialNumber.Split('/')[2].Substring(2)
```
