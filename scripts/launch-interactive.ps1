$batPath = "f:\work\00-oss\maintenis\start-blender-agent.bat"
$action = New-ScheduledTaskAction -Execute $batPath
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
Register-ScheduledTask -TaskName "LaunchBlenderAgentGUI" -Action $action -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName "LaunchBlenderAgentGUI"
Write-Host "INTERACTIVE_TASK_LAUNCHED_SUCCESS"
