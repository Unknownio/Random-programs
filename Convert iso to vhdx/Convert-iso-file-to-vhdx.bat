@echo off
echo First and foremost you will need to install something
echo 1.You will need to Open Powershell As admin after you do that 
echo ---
echo 1.1 Yeah i get its in red, because the terminal is black and at the moment i thought the red was pretty cool so yeah
color 0C
echo ----
echo 2.You will need to type: install-module -Name Convert-WindowsImage
echo ------
echo it will ask you to accept the requset to download Nuget( because is Important part of the process)
echo Then it will ask you if you trust the repository just press: y
echo -----
echo 3.Now you will need to go to the location of the iso file, you will need to just type: cd [path]
echo ----
echo 4.Finall step: 
echo Just type: Convert-WindowsImage -SourcePath "THE NAME OF THE ISO FILE.iso" -PassThru -DiskLayout "Windowstogo"
echo ---
PAUSE