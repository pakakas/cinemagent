$batPath = "f:\work\00-oss\maintenis\start-blank-video.bat"
$action = New-ScheduledTaskAction -Execute $batPath
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -TaskName "LaunchBlankVideoGUI" -Action $action -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName "LaunchBlankVideoGUI"
Write-Host "BLANK_VIDEO_TASK_LAUNCHED_SUCCESS"
