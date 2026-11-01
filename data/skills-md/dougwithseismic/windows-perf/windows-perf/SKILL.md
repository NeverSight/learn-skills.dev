---
name: windows-perf
description: "Optimize Windows 11 for performance, privacy, and developer productivity. Use this skill whenever the user wants to speed up Windows, remove bloatware, debloat their machine, tune Windows for development, clean up junk apps, optimize GPU/network/memory settings, disable telemetry, or generally make their Windows machine faster. Also trigger when users mention slow builds, Windows bloat, startup optimization, or anything about making Windows less annoying. Even if they just say 'my PC feels slow' or 'clean this machine up' on a Windows system - this skill applies."
---

# Windows Performance Optimizer

A comprehensive Windows 11 optimization skill that covers power plans, services, network, privacy, UI speed, bloatware removal, gaming/GPU, memory/disk, developer tools, Defender exclusions, and more.

## Quick Reference

The full optimization script lives at `windows-perf.ps1` in the project root (or can be found via the repo at github.com/withseismic/windows-perf). If the script is available locally, prefer running it. If not, execute the optimizations inline using the module reference below.

## Workflow

### Step 1: System Reconnaissance

Before doing anything, gather the machine's specs. This determines which optimizations are safe and relevant.

```powershell
# Run all of these to understand what we're working with
Get-ComputerInfo | Select-Object CsName, OsName, OsBuildNumber, OsArchitecture
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_VideoController | Where-Object { $_.Name -notmatch "Microsoft" } | Select-Object Name, DriverVersion
[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, HealthStatus
powercfg /getactivescheme
```

Also check elevation — many optimizations require admin:
```powershell
([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
```

If not admin, warn the user upfront: "I can apply user-level tweaks (UI, Explorer, privacy, taskbar, input, dark mode) but power plans, services, DNS, Defender exclusions, memory/disk, and scheduled tasks need admin. Want me to create an elevated script for those?"

### Step 2: Present Options

Use AskUserQuestion to let the user pick what to optimize. Present the categories with descriptions so they can make an informed choice. The categories are:

| Module | What it does | Needs Admin |
|---|---|---|
| power | Ultimate Performance plan, core parking off, idle states off | Yes |
| services | Disable telemetry, Superfetch, Search indexer, etc. (10 services) | Yes |
| network | Cloudflare DNS, Nagle off, TCP tuning, RSS, throttling off | Yes |
| privacy | Telemetry zero, ads off, Bing removed, Copilot blocked, Edge nags killed | Partial |
| ui | Zero menu delay, faster shutdown, reduced animations | Partial |
| explorer | File extensions, hidden files, classic right-click, full paths | No |
| taskbar | Remove Widgets, Task View, Chat, Copilot, Search box | No |
| gaming | HW GPU scheduling, Game Mode, DVR off, NVIDIA max perf, TDR | Partial |
| memory | Pagefile, TRIM, NTFS, hibernation off, large cache, compression off | Yes |
| bloatware | Remove 30+ junk apps, block reinstall, deprovision | Partial |
| onedrive | Full OneDrive removal | No |
| developer | Git config, dev mode, long paths, UTF-8, NTFS 8.3 off, NODE_OPTIONS | Partial |
| defender | Defender exclusions for dev folders/processes (huge build speed boost) | Yes |
| input | Mouse acceleration off, Sticky/Filter/Toggle Keys prompts off | No |
| misc | Dark mode, clipboard history, background apps off, lock screen off | Partial |
| tasks | Disable telemetry/CEIP/diagnostic scheduled tasks | Yes |
| wsl | WSL2 memory/CPU/swap optimization | No |

Also ask about DNS preference (Cloudflare 1.1.1.1, Google 8.8.8.8, Quad9 9.9.9.9, or keep current).

Offer a "Send it - do everything" option for users who just want the full treatment.

### Step 3: Execute

**If windows-perf.ps1 exists locally**, run it with the appropriate flags:
```powershell
# Everything
.\windows-perf.ps1

# Specific modules
.\windows-perf.ps1 -Only power,network,privacy

# Skip specific modules
.\windows-perf.ps1 -Skip bloatware,onedrive

# Interactive (prompts before each)
.\windows-perf.ps1 -Interactive

# Preview only
.\windows-perf.ps1 -DryRun
```

If admin is needed, launch elevated:
```powershell
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File .\windows-perf.ps1" -Verb RunAs
```

**If the script is NOT available**, execute optimizations inline using the module details below. Apply user-level changes directly. For admin changes, write a .ps1 script and launch it elevated.

### Step 4: Verify

After applying changes, verify key optimizations took effect:
```powershell
powercfg /getactivescheme  # Should show Ultimate Performance
Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses } | Select-Object InterfaceAlias, ServerAddresses
Get-Service DiagTrack,SysMain,WSearch | Select-Object Name, Status, StartType
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" -Name "HwSchMode" -ErrorAction SilentlyContinue
Test-Path "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
```

Report a summary table showing what was applied, what was skipped (no admin), and what failed.

Always end with: "Restart required for full effect" — pagefile, GPU scheduling, classic context menu, services, memory compression, and code page changes need a reboot.

---

## Module Reference (for inline execution)

When the script isn't available, here are the exact commands for each module. Use Set-ItemProperty for registry changes, creating parent keys with New-Item -Force when they don't exist.

### Power
```powershell
# Unlock and activate Ultimate Performance
powercfg /duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
$guid = (powercfg /list | Select-String "Ultimate Performance").ToString() -replace '.*(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}).*', '$1'
powercfg /setactive $guid
# USB suspend off, PCI-E power mgmt off, CPU 100%, no sleep, core parking off
powercfg /setacvalueindex $guid 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setacvalueindex $guid 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0
powercfg /setacvalueindex $guid 54533251-82be-4824-96c1-47b60b740d00 893dee8e-2bef-41e0-89c6-b55d0929964c 100
powercfg /setacvalueindex $guid 54533251-82be-4824-96c1-47b60b740d00 bc5038f7-23e0-4960-96da-33abaf5935ec 100
powercfg /setacvalueindex $guid 54533251-82be-4824-96c1-47b60b740d00 0cc5b647-c1df-4637-891a-dec35c318583 100
powercfg /setactive $guid
```

### Services (admin)
Disable: DiagTrack, dmwappushservice, SysMain, WSearch, MapsBroker, lfsvc, RetailDemo, WerSvc, Fax, wisvc
```powershell
$svcs = @('DiagTrack','dmwappushservice','SysMain','WSearch','MapsBroker','lfsvc','RetailDemo','WerSvc','Fax','wisvc')
foreach ($s in $svcs) { Stop-Service $s -Force -EA SilentlyContinue; Set-Service $s -StartupType Disabled -EA SilentlyContinue }
```

### Network (admin)
```powershell
# DNS (Cloudflare)
$adapter = Get-NetAdapter | Where-Object { $_.Status -eq "Up" -and $_.InterfaceDescription -notmatch "Virtual|Loopback" } | Select-Object -First 1
Set-DnsClientServerAddress -InterfaceIndex $adapter.InterfaceIndex -ServerAddresses @("1.1.1.1","1.0.0.1")
# Nagle off
Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" | ForEach-Object {
    Set-ItemProperty $_.PSPath -Name "TcpAckFrequency" -Value 1 -Type DWord -EA SilentlyContinue
    Set-ItemProperty $_.PSPath -Name "TCPNoDelay" -Value 1 -Type DWord -EA SilentlyContinue
}
# TCP tuning
netsh int tcp set global autotuninglevel=normal; netsh int tcp set global rss=enabled
netsh int tcp set global dca=enabled; netsh int tcp set global timestamps=disabled
# Network throttling off
Set-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" -Name "NetworkThrottlingIndex" -Value 0xFFFFFFFF -Type DWord
# P2P delivery off
New-Item "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" -Force | Out-Null
Set-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" -Name "DODownloadMode" -Value 0 -Type DWord
```

### Privacy
Key registry paths — set all values to 0 (DWord) unless noted:
- `HKCU:\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager` — SilentInstalledAppsEnabled, ContentDeliveryAllowed, all SubscribedContent-* keys
- `HKCU:\Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo` — Enabled
- `HKCU:\Software\Microsoft\Windows\CurrentVersion\Search` — BingSearchEnabled, CortanaConsent
- `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection` — AllowTelemetry, MaxTelemetryAllowed (admin)
- `HKLM:\SOFTWARE\Policies\Microsoft\Windows\System` — EnableActivityFeed, PublishUserActivities, UploadUserActivities (admin)
- `HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot` — TurnOffWindowsCopilot=1 (admin)
- `HKLM:\SOFTWARE\Policies\Microsoft\Edge` — HideFirstRunExperience=1, DefaultBrowserSettingEnabled=0, HubsSidebarEnabled=0 (admin)

### UI Speed
```powershell
Set-ItemProperty "HKCU:\Control Panel\Desktop" -Name "MenuShowDelay" -Value "0" -Type String
Set-ItemProperty "HKCU:\Control Panel\Desktop\WindowMetrics" -Name "MinAnimate" -Value "0" -Type String
Set-ItemProperty "HKCU:\Control Panel\Desktop" -Name "WaitToKillAppTimeout" -Value "2000" -Type String
Set-ItemProperty "HKCU:\Control Panel\Desktop" -Name "HungAppTimeout" -Value "1000" -Type String
Set-ItemProperty "HKCU:\Control Panel\Desktop" -Name "AutoEndTasks" -Value "1" -Type String
# Keep ClearType on
Set-ItemProperty "HKCU:\Control Panel\Desktop" -Name "FontSmoothing" -Value "2" -Type String
```

### Explorer
```powershell
$adv = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
Set-ItemProperty $adv -Name "HideFileExt" -Value 0; Set-ItemProperty $adv -Name "Hidden" -Value 1
Set-ItemProperty $adv -Name "LaunchTo" -Value 1  # This PC
# Classic right-click
$ctx = "HKCU:\Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
New-Item $ctx -Force | Out-Null; Set-ItemProperty $ctx -Name "(Default)" -Value "" -Type String
```

### Bloatware
```powershell
$apps = @("Microsoft.Copilot","Microsoft.YourPhone","Clipchamp.Clipchamp","Microsoft.BingNews","Microsoft.BingWeather","Microsoft.BingSearch","Microsoft.WindowsFeedbackHub","Microsoft.People","Microsoft.MicrosoftSolitaireCollection","Microsoft.MixedReality.Portal","Microsoft.Microsoft3DViewer","Microsoft.SkypeApp","Microsoft.ZuneMusic","Microsoft.ZuneVideo","Microsoft.Todos","MicrosoftCorporationII.QuickAssist","Microsoft.MicrosoftOfficeHub","Microsoft.Office.OneNote","Microsoft.WindowsMaps","Microsoft.Edge.GameAssist","MSTeams","MicrosoftWindows.CrossDevice","Microsoft.GetHelp","Microsoft.WindowsAlarms","Microsoft.OutlookForWindows","MicrosoftWindows.Client.WebExperience","Microsoft.WidgetsPlatformRuntime")
foreach ($a in $apps) { Get-AppxPackage -Name $a -EA SilentlyContinue | Remove-AppxPackage -EA SilentlyContinue }
```

### Defender Exclusions (admin — biggest build speed win)
```powershell
$paths = @("$env:USERPROFILE\source","$env:USERPROFILE\projects","$env:USERPROFILE\repos","$env:USERPROFILE\.cargo","$env:USERPROFILE\.rustup","$env:USERPROFILE\AppData\Local\Temp","C:\dev","D:\dev","E:\dev")
$procs = @("node.exe","cargo.exe","rustc.exe","go.exe","python.exe","dotnet.exe","git.exe","Code.exe","pwsh.exe")
foreach ($p in $paths) { if (Test-Path $p) { Add-MpPreference -ExclusionPath $p -EA SilentlyContinue } }
foreach ($p in $procs) { Add-MpPreference -ExclusionProcess $p -EA SilentlyContinue }
```

### Developer
```powershell
# Dev mode
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\AppModelUnlock" -Name "AllowDevelopmentWithoutDevLicense" -Value 1 -Type DWord
# Git optimizations
git config --global fetch.parallel 0; git config --global diff.algorithm histogram
git config --global merge.conflictstyle zdiff3; git config --global rerere.enabled true
git config --global core.fsmonitor true; git config --global core.untrackedcache true
# Long paths (admin)
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -Type DWord
# NODE_OPTIONS
[Environment]::SetEnvironmentVariable("NODE_OPTIONS", "--max-old-space-size=16384", "User")
```

### Gaming/GPU (admin)
```powershell
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" -Name "HwSchMode" -Value 2 -Type DWord
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" -Name "TdrDelay" -Value 10 -Type DWord
# NVIDIA max perf
$nv = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"
if (Test-Path $nv) { Set-ItemProperty $nv -Name "PerfLevelSrc" -Value 0x2222 -Type DWord }
# Game DVR off
Set-ItemProperty "HKCU:\System\GameConfigStore" -Name "GameDVR_Enabled" -Value 0 -Type DWord
Set-ItemProperty "HKCU:\Software\Microsoft\GameBar" -Name "AutoGameModeEnabled" -Value 1 -Type DWord
```

### Memory/Disk (admin)
```powershell
$ramGB = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
# Pagefile off for 64GB+
if ($ramGB -ge 64) {
    $cs = Get-CimInstance Win32_ComputerSystem; $cs | Set-CimInstance -Property @{AutomaticManagedPagefile=$false}
    Get-CimInstance Win32_PageFileSetting -EA SilentlyContinue | Remove-CimInstance -EA SilentlyContinue
}
fsutil behavior set disablelastaccess 1; fsutil behavior set disabledeletenotify 0
fsutil behavior set disable8dot3 1; fsutil behavior set memoryusage 2
powercfg /hibernate off
# Memory compression off for 32GB+
if ($ramGB -ge 32) { Disable-MMAgent -MemoryCompression -EA SilentlyContinue }
```

### Input
```powershell
# Mouse acceleration off
Set-ItemProperty "HKCU:\Control Panel\Mouse" -Name "MouseSpeed" -Value "0" -Type String
Set-ItemProperty "HKCU:\Control Panel\Mouse" -Name "MouseThreshold1" -Value "0" -Type String
Set-ItemProperty "HKCU:\Control Panel\Mouse" -Name "MouseThreshold2" -Value "0" -Type String
# Sticky Keys prompt off
Set-ItemProperty "HKCU:\Control Panel\Accessibility\StickyKeys" -Name "Flags" -Value "506" -Type String
Set-ItemProperty "HKCU:\Control Panel\Accessibility\Keyboard Response" -Name "Flags" -Value "122" -Type String
Set-ItemProperty "HKCU:\Control Panel\Accessibility\ToggleKeys" -Name "Flags" -Value "58" -Type String
```

### Misc
```powershell
# Dark mode
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value 0 -Type DWord
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "SystemUsesLightTheme" -Value 0 -Type DWord
# Clipboard history
New-Item "HKCU:\Software\Microsoft\Clipboard" -Force | Out-Null
Set-ItemProperty "HKCU:\Software\Microsoft\Clipboard" -Name "EnableClipboardHistory" -Value 1 -Type DWord
# Background apps off
Set-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -Name "GlobalUserDisabled" -Value 1 -Type DWord
```

### WSL2
```powershell
$ramGB = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
$wslRam = [math]::Floor($ramGB / 2)
$cpuCount = (Get-CimInstance Win32_Processor).NumberOfLogicalProcessors
@"
[wsl2]
memory=${wslRam}GB
processors=$cpuCount
swap=0
localhostForwarding=true
[experimental]
autoMemoryReclaim=dropcache
sparseVhd=true
"@ | Out-File "$env:USERPROFILE\.wslconfig" -Encoding UTF8 -Force
```
