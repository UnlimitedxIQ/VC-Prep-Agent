# Restart VC Thesis Bot
Write-Host "Stopping existing bot instances..."

# Find and stop python processes running bot.py
Get-Process python -ErrorAction SilentlyContinue | ForEach-Object {
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
        if ($cmdLine -like "*bot.py*") {
            Stop-Process -Id $_.Id -Force
            Write-Host "Stopped process $($_.Id)"
        }
    } catch {}
}

Start-Sleep 2

# Start the bot
Write-Host "Starting bot..."
Start-Process -FilePath "python" -ArgumentList "C:\Users\bryso\GPTOSS_AGENTFILES\Agents\TelegramVCBot\bot.py" -WindowStyle Normal
Write-Host "Bot started!"
