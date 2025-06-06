@echo off
echo Installing Scoop, Node.js, Python, and pip...

:: Install Scoop
echo Checking for Scoop...
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command ^
  "if (-Not (Get-Command scoop -ErrorAction SilentlyContinue)) { Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh'); } else { Write-Host 'Scoop is already installed.'; }"

:: Check if Scoop is installed successfully
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command ^
  "if (-Not (Get-Command scoop -ErrorAction SilentlyContinue)) { echo 'Scoop installation failed.'; exit 1; }"

:: Install Node.js using Scoop
echo Installing Node.js...
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command ^
  "if (Get-Command scoop -ErrorAction SilentlyContinue) { scoop install nodejs; }"

:: Check if Node.js is installed successfully
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command ^
  "if (-Not (Get-Command node -ErrorAction SilentlyContinue)) { echo 'Node.js installation failed.'; exit 1; } else { echo 'Node.js installed successfully!'; }"

:: Install Python (with pip) using Scoop if not installed
echo Checking for Python...
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command ^
  "if (-Not (Get-Command python -ErrorAction SilentlyContinue)) { exit 1 } else { exit 0 }"
if errorlevel 1 (
  echo Python not found. Installing Python via Scoop...
  powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "scoop install python"
) else (
  echo Python is already installed.
)

:: Check if pip is installed
echo Checking for pip...
powershell.exe -ExecutionPolicy Bypass -NoProfile -Command ^
  "try { python -m pip --version; exit 0 } catch { exit 1 }"
if errorlevel 1 (
  echo pip not found. Installing pip...
  powershell.exe -ExecutionPolicy Bypass -NoProfile -Command "python -m ensurepip --upgrade"
) else (
  echo pip is already installed.
)

:: Install node modules
npm i || exit /b 1

:: Install/update yt-dlp via pip
pip install -U yt-dlp || exit /b 1

echo Successfully Installed!

pause
