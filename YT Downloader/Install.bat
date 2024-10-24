@echo off
echo "Press Any Key"
call ./read-me.bat
echo Download will start 3, 2, 1, Now!!

rem Open PowerShell and run the scripts
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "./Packages/install-scoop.ps1"
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "./Packages/Install-node.js.ps1"

rem Update scoop and install packages
powershell.exe -ExecutionPolicy Bypass -Command "scoop update; scoop install nodejs; scoop update python"

rem Install npm packages
powershell.exe -ExecutionPolicy Bypass -Command "npm install"

PAUSE
