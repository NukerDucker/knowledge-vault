$ConfigFile = "$env:USERPROFILE\.claude.json"

if (Test-Path $ConfigFile) {
  $overwrite = Read-Host "Config file already exists at $ConfigFile. Overwrite? (y/n)"
  if ($overwrite -ne "y" -and $overwrite -ne "Y") {
    Write-Host "Aborted. Existing config kept."
    exit
  }
}

$Token = Read-Host "Enter your GenAI personal token"

# Build config as array of lines for Windows line endings
$ConfigLines = @(
  '{'
  '  "numStartups": 1,'
  '  "installMethod": "unknown",'
  '  "autoUpdates": true,'
  '  "env": {'
  "    `"ANTHROPIC_AUTH_TOKEN`": `"$Token`""
  '  }'
  '}'
)

# Join lines with Windows line endings
$ConfigContent = $ConfigLines -join "`r`n"

# Write as UTF-8 without BOM (works in all PowerShell versions)
[System.IO.File]::WriteAllText($ConfigFile, $ConfigContent, [System.Text.Encoding]::UTF8)

Write-Host "Claude Code config created at $ConfigFile"