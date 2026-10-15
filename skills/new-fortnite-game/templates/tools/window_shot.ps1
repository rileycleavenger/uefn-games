<#
.SYNOPSIS
  Captures a window (by title substring) to a PNG, exactly as shown on screen: HUD, widgets and camera
  lens effects included, which HighResShot leaves out. For the Fortnite client window ("Fortnite") during a UEFN session. Reads pixels only (PrintWindow); sends no input. Untested on the Fortnite client (Easy Anti-Cheat): if the image is black, ask the human for a screenshot.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\window_shot.ps1 -Title "Fortnite" -Out shots\client.png
#>
param([Parameter(Mandatory = $true)][string]$Title, [string]$Out = "")
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $Out) { $Out = Join-Path $Repo ("shots/window-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".png") }
Add-Type -AssemblyName System.Drawing
if (-not ("FnShot" -as [type])) {
    Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public class FnShot {
  public delegate bool P(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(P p, IntPtr l);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint flags);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  public static IntPtr Find(string part) { IntPtr found = IntPtr.Zero; EnumWindows((h, l) => { var s = new StringBuilder(512);
    GetWindowText(h, s, 512); if (found == IntPtr.Zero && IsWindowVisible(h) && s.ToString().Contains(part) && !s.ToString().Contains("Unreal Editor")) found = h; return true; }, IntPtr.Zero); return found; }
}
"@
}
[void][FnShot]::SetProcessDPIAware()  # real pixel sizes under Windows display scaling
$H = [FnShot]::Find($Title)
if ($H -eq [IntPtr]::Zero) { throw "no visible window with '$Title' in its title" }
$R = New-Object FnShot+RECT
[void][FnShot]::GetWindowRect($H, [ref]$R)
$Bmp = New-Object System.Drawing.Bitmap ($R.R - $R.L), ($R.B - $R.T)
$G = [System.Drawing.Graphics]::FromImage($Bmp)
$Dc = $G.GetHdc()
[void][FnShot]::PrintWindow($H, $Dc, 2)  # PW_RENDERFULLCONTENT: works for D3D windows behind others
$G.ReleaseHdc($Dc)
New-Item -ItemType Directory -Force -Path (Split-Path $Out) | Out-Null
$Bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$G.Dispose(); $Bmp.Dispose()
Write-Host "saved $Out"
