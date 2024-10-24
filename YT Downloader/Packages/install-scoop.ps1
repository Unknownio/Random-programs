# Import the required module
Import-Module Microsoft.PowerShell.Security

# Set execution policy to allow script execution
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Download and install Scoop
Invoke-WebRequest -UseBasicP "get.scoop.sh" | Invoke-Expression

