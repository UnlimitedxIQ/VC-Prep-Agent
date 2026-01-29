$startup = [Environment]::GetFolderPath('Startup')
$source = "C:\Users\bryso\GPTOSS_AGENTFILES\start_bot.bat"
Copy-Item $source -Destination $startup -Force
Write-Host "Bot added to Windows Startup folder!"
Write-Host "Location: $startup\start_bot.bat"
Write-Host ""
Write-Host "The bot will now start automatically when you log in."
