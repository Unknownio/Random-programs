@echo off
echo Installing Scoop and Node.js...

:: Install Scoop
echo Checking for Scoop...
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "if (-Not (Get-Command scoop -ErrorAction SilentlyContinue)) { Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh'); } else { Write-Host 'Scoop is already installed.'; }"

:: Check if Scoop is installed successfully
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "if (-Not (Get-Command scoop -ErrorAction SilentlyContinue)) { echo 'Scoop installation failed.'; exit 1; }"

:: Install Node.js using Scoop
echo Installing Node.js...
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "if (Get-Command scoop -ErrorAction SilentlyContinue) { scoop install nodejs; }"

:: Check if Node.js is installed successfully
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "if (-Not (Get-Command node -ErrorAction SilentlyContinue)) { echo 'Node.js installation failed.'; exit 1; } else { echo 'Node.js installed successfully!'; }"

PAUSE
