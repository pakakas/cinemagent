$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("f:\work\00-oss\maintenis\BlankVideoAgent.lnk")
$Shortcut.TargetPath = "f:\work\00-oss\maintenis\start-blank-video.bat"
$Shortcut.WorkingDirectory = "f:\work\00-oss\maintenis"
$Shortcut.IconLocation = "C:\Users\ucing\AppData\Local\Microsoft\WindowsApps\blender-launcher.exe,0"
$Shortcut.Description = "Launch Blender Blank Video Editing Project with AI Agent Server"
$Shortcut.Save()
Write-Host "SHORTCUT_CREATED_SUCCESS"
