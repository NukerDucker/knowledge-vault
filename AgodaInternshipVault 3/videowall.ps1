$taskName   = "VideoWall Biweekly Restart"
$scriptPath = "C:\Scripts\restart_videowall.ps1"

$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
	$answer = Read-Host "Task '$taskName' already exists. Remove it and create a new one? (y/n)"
	if ($answer -ne "y") {
		Write-Output "Left existing task '$taskName' as is."
		return
	}
	Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
	Remove-Item $scriptPath -ErrorAction SilentlyContinue
	Write-Output "Removed existing task '$taskName'."
}

$validDays = "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
do {
	$dayNum = Read-Host "Day of week for restart, 1=Monday .. 7=Sunday (default 5=Friday)"
	if ([string]::IsNullOrWhiteSpace($dayNum)) { $dayNum = "5" }
} while ($dayNum -notmatch '^[1-7]$')
$dayOfWeek = $validDays[[int]$dayNum - 1]

if (!(Test-Path "C:\Scripts")) { New-Item -ItemType Directory -Path "C:\Scripts" | Out-Null }

@'
$logFile = "C:\VideoWallLogs\restart_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

if (!(Test-Path "C:\VideoWallLogs")) { New-Item -ItemType Directory -Path "C:\VideoWallLogs" }

Write-Output "[$timestamp] Starting biweekly restart..." | Tee-Object -FilePath $logFile -Append

if ((Get-Item $logFile -ErrorAction SilentlyContinue).Length -gt 1MB) { Remove-Item $logFile }

Write-Output "[$timestamp] Initiating system reboot..." | Tee-Object -FilePath $logFile -Append
Restart-Computer -Force
'@ | Set-Content -Path $scriptPath

$action    = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger   = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $dayOfWeek -WeeksInterval 2 -At 12:00PM
$settings  = New-ScheduledTaskSettingsSet
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force
Write-Output "Started: created $scriptPath and registered task '$taskName' for every other $dayOfWeek at 12:00 PM."