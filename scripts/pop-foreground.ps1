$p = Get-Process blender -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle } | Select-Object -First 1
if ($p) {
    $wshell = New-Object -ComObject WScript.Shell
    $wshell.AppActivate($p.Id)
    Write-Host "FOREGROUND_POP_SUCCESS: $($p.MainWindowTitle)"
}
