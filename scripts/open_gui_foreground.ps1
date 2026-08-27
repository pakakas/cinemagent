$csharp = @"
using System;
using System.Runtime.InteropServices;
public class Win32Window {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool SwitchToThisWindow(IntPtr hWnd, bool fAltTab);
}
"@
Add-Type -TypeDefinition $csharp -ErrorAction SilentlyContinue

Write-Host "Launching Blender GUI..."
$proc = Start-Process "C:\Users\ucing\AppData\Local\Microsoft\WindowsApps\blender-launcher.exe" -ArgumentList '"D:\videos\guray.blend" --python "f:\work\00-oss\maintenis\pakakas\blender-server\main.py"' -PassThru

for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Milliseconds 500
    $bp = Get-Process -Name "blender" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }
    if ($bp) {
        $hwnd = $bp[0].MainWindowHandle
        [Win32Window]::ShowWindow($hwnd, 9)
        [Win32Window]::SwitchToThisWindow($hwnd, $true)
        [Win32Window]::SetForegroundWindow($hwnd)
        Write-Host "Brought Blender GUI window to front successfully! HWND: $hwnd"
        exit 0
    }
}

Write-Host "Blender process started."
