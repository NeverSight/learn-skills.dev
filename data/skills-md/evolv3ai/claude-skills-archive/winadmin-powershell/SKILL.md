---
name: winadmin-powershell
description: |
  Administer Windows 11 systems with PowerShell 7.x. Includes command translations from bash/Linux, package manager usage (winget, scoop, npm, chocolatey), PATH configuration, and environment management for multi-device setups.

  Use when: setting up Windows admin environments, writing PowerShell automation scripts, translating bash commands to PowerShell, configuring PATH and environment variables, or troubleshooting "command not found", "Get-Content not recognized", "winget not working" errors.
source: plugin
---

# WinAdmin PowerShell

- NEVER store live `.env` files or credentials inside any skill folder.
- `.env.template` files belong only in `templates/` within a skill.
- Store live secrets in `~/.admin/.env` (or another non-skill location you control) and reference them from there.


**Status**: Production Ready
**Last Updated**: 2025-12-06
**Dependencies**: PowerShell 7.x, Windows 11
**Latest Versions**: PowerShell 7.5.x, winget 1.x

---

## Quick Start (5 Minutes)

### 1. Verify PowerShell Version

```powershell
$PSVersionTable.PSVersion
# Should show 7.x (NOT 5.1)
```

**If PowerShell 7 not installed:**
```powershell
winget install Microsoft.PowerShell
```

### 2. Set Up Environment File

Create `.env` in your admin directory (never inside a skill folder):

```powershell
# Create .env from template (store outside the skill)
$adminRoot = if ($env:ADMIN_ROOT) { $env:ADMIN_ROOT } else { Join-Path $HOME ".admin" }
Copy-Item "templates/.env.template" (Join-Path $adminRoot ".env")
# Edit with your device-specific values
notepad (Join-Path $adminRoot ".env")
```

### 3. Verify Environment

```powershell
# Run verification script
.\scripts\Verify-ShellEnvironment.ps1
```

---

## Critical Rules

### Always Do

- Use PowerShell 7.x (`pwsh.exe`), not Windows PowerShell 5.1 (`powershell.exe`)
- Use PowerShell cmdlets, not bash/Linux commands
- Use full paths with `Test-Path` before file operations
- Set PATH in Windows Registry for persistence (not just profile)
- Use `${env:VARIABLE}` syntax for environment variables

### Never Do

- Use bash commands (`cat`, `ls`, `grep`, `echo`, `export`)
- Use relative paths without verification
- Modify system PATH without backup
- Run scripts without execution policy check
- Create multiple config files (update existing ones)

---

## Bash to PowerShell Translation

| Bash Command | PowerShell Equivalent | Notes |
|--------------|----------------------|-------|
| `cat file.txt` | `Get-Content file.txt` | Or `gc` alias |
| `cat file.txt \| head -20` | `Get-Content file.txt -Head 20` | Built-in parameter |
| `cat file.txt \| tail -20` | `Get-Content file.txt -Tail 20` | Built-in parameter |
| `ls` | `Get-ChildItem` | Or `dir`, `gci` aliases |
| `ls -la` | `Get-ChildItem -Force` | Shows hidden files |
| `grep "pattern" file` | `Select-String "pattern" file` | Or `sls` alias |
| `grep -r "pattern" .` | `Get-ChildItem -Recurse \| Select-String "pattern"` | Recursive search |
| `echo "text"` | `Write-Output "text"` | Or `Write-Host` for display |
| `echo "text" > file` | `Set-Content file -Value "text"` | Overwrites file |
| `echo "text" >> file` | `Add-Content file -Value "text"` | Appends to file |
| `export VAR=value` | `$env:VAR = "value"` | Session only |
| `export VAR=value` (permanent) | `[Environment]::SetEnvironmentVariable("VAR", "value", "User")` | Persists |
| `test -f file` | `Test-Path file -PathType Leaf` | Check file exists |
| `test -d dir` | `Test-Path dir -PathType Container` | Check dir exists |
| `mkdir -p dir/sub` | `New-Item -ItemType Directory -Path dir/sub -Force` | Creates parents |
| `rm file` | `Remove-Item file` | Delete file |
| `rm -rf dir` | `Remove-Item dir -Recurse -Force` | Delete directory |
| `cp src dst` | `Copy-Item src dst` | Copy file |
| `mv src dst` | `Move-Item src dst` | Move/rename |
| `pwd` | `Get-Location` | Or `$PWD` variable |
| `cd dir` | `Set-Location dir` | Or `cd` alias works |
| `which cmd` | `Get-Command cmd` | Find command location |
| `ps aux` | `Get-Process` | List processes |
| `kill PID` | `Stop-Process -Id PID` | Kill process |
| `curl URL` | `Invoke-WebRequest URL` | Or `Invoke-RestMethod` for APIs |
| `wget URL -O file` | `Invoke-WebRequest URL -OutFile file` | Download file |
| `jq` | `ConvertFrom-Json` / `ConvertTo-Json` | JSON handling |
| `sed 's/old/new/g'` | `(Get-Content file) -replace 'old','new'` | Text replacement |
| `awk` | `Select-Object`, `ForEach-Object` | Data processing |
| `source file.sh` | `. .\file.ps1` | Dot-source script |

---

## Package Managers

### winget (Preferred for Windows Apps)

```powershell
# Search for package
winget search "package-name"

# Install package
winget install Package.Name

# Install specific version
winget install Package.Name --version 1.2.3

# List installed packages
winget list

# Upgrade package
winget upgrade Package.Name

# Upgrade all packages
winget upgrade --all

# Uninstall package
winget uninstall Package.Name
```

### scoop (Developer Tools)

```powershell
# Install scoop (if not installed)
irm get.scoop.sh | iex

# Add buckets (repositories)
scoop bucket add extras
scoop bucket add versions

# Install package
scoop install git

# List installed
scoop list

# Update package
scoop update git

# Update all
scoop update *

# Uninstall
scoop uninstall git
```

### npm (Node.js Packages)

```powershell
# Install globally
npm install -g package-name

# List global packages
npm list -g --depth=0

# Update global package
npm update -g package-name

# Uninstall global
npm uninstall -g package-name
```

### chocolatey (Alternative)

```powershell
# Install chocolatey (admin required)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install package
choco install package-name -y

# List installed
choco list --local-only

# Upgrade
choco upgrade package-name -y
```

---

## PATH Configuration

### Check Current PATH

```powershell
# View full PATH
$env:PATH -split ';'

# Check if path exists in PATH
$env:PATH -split ';' | Where-Object { $_ -like "*npm*" }

# Check User vs Machine PATH separately
[Environment]::GetEnvironmentVariable('PATH', 'User') -split ';'
[Environment]::GetEnvironmentVariable('PATH', 'Machine') -split ';'
```

### Add to PATH (Permanent)

```powershell
# Add to User PATH (no admin required)
$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
$newPath = "C:\new\path"
if ($currentPath -notlike "*$newPath*") {
    [Environment]::SetEnvironmentVariable('PATH', "$newPath;$currentPath", 'User')
    Write-Host "Added $newPath to User PATH"
}

# Refresh current session
$env:PATH = [Environment]::GetEnvironmentVariable('PATH', 'User') + ";" + [Environment]::GetEnvironmentVariable('PATH', 'Machine')
```

### Common PATH Entries

```powershell
# npm global packages
C:\Users\${env:USERNAME}\AppData\Roaming\npm

# Scoop apps
C:\Users\${env:USERNAME}\scoop\shims

# Python (winget install)
C:\Users\${env:USERNAME}\AppData\Local\Programs\Python\Python3xx

# Git
C:\Program Files\Git\cmd
```

---

## Environment Variables

### Session Variables (Temporary)

```powershell
# Set variable
$env:MY_VAR = "value"

# Read variable
$env:MY_VAR

# Remove variable
Remove-Item Env:\MY_VAR
```

### Permanent Variables

```powershell
# Set User variable (persists across sessions)
[Environment]::SetEnvironmentVariable("MY_VAR", "value", "User")

# Set Machine variable (requires admin)
[Environment]::SetEnvironmentVariable("MY_VAR", "value", "Machine")

# Read from specific scope
[Environment]::GetEnvironmentVariable("MY_VAR", "User")

# Remove permanent variable
[Environment]::SetEnvironmentVariable("MY_VAR", $null, "User")
```

### Load Variables from .env File

```powershell
# Load .env file into current session
function Load-EnvFile {
    param([string]$Path = ".env")

    if (Test-Path $Path) {
        Get-Content $Path | ForEach-Object {
            if ($_ -match '^([^#][^=]+)=(.*)$') {
                $name = $matches[1].Trim()
                $value = $matches[2].Trim()
                Set-Item -Path "Env:\$name" -Value $value
                Write-Host "Loaded: $name"
            }
        }
    } else {
        Write-Warning "File not found: $Path"
    }
}

# Usage
Load-EnvFile ".env"
```

---

## PowerShell Profile

### Profile Locations

```powershell
# Current user, current host (most common)
$PROFILE.CurrentUserCurrentHost
# Typically: C:\Users\<user>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1

# View all profile paths
$PROFILE | Get-Member -Type NoteProperty | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Name
        Path = $PROFILE.($_.Name)
        Exists = Test-Path $PROFILE.($_.Name)
    }
}
```

### Create/Edit Profile

```powershell
# Create profile if not exists
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

# Edit profile
notepad $PROFILE
# Or: code $PROFILE (VS Code)
```

### Recommended Profile Content

```powershell
# PowerShell Profile
# Location: $PROFILE

# === ENVIRONMENT ===
$env:COLORTERM = "truecolor"

# === PATH VERIFICATION ===
$npmPath = "$env:APPDATA\npm"
if ($env:PATH -notlike "*$npmPath*") {
    Write-Warning "npm not in PATH. Add to User PATH via Environment Variables."
}

# === FUNCTIONS ===

# Load .env file
function Load-Env {
    param([string]$Path = ".env")
    if (Test-Path $Path) {
        Get-Content $Path | ForEach-Object {
            if ($_ -match '^([^#][^=]+)=(.*)$') {
                Set-Item -Path "Env:\$($matches[1].Trim())" -Value $matches[2].Trim()
            }
        }
    }
}

# Quick navigation
function admin { Set-Location "${env:ADMIN_ROOT}" }

# === ALIASES ===
Set-Alias -Name which -Value Get-Command
Set-Alias -Name ll -Value Get-ChildItem
```

---

## Execution Policy

### Check Current Policy

```powershell
Get-ExecutionPolicy
Get-ExecutionPolicy -List  # Shows all scopes
```

### Set Execution Policy

```powershell
# For current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Options:
# - Restricted: No scripts allowed
# - AllSigned: Only signed scripts
# - RemoteSigned: Local scripts OK, downloaded must be signed
# - Unrestricted: All scripts (warning for downloaded)
# - Bypass: No restrictions, no warnings
```

### Bypass for Single Script

```powershell
powershell -ExecutionPolicy Bypass -File script.ps1
```

---

## JSON Operations

### Read JSON

```powershell
# Read and parse JSON file
$config = Get-Content "config.json" | ConvertFrom-Json

# Access properties
$config.propertyName
$config.nested.property

# Access array items
$config.items[0]
```

### Write JSON

```powershell
# Create object and save as JSON
$data = @{
    name = "value"
    nested = @{
        property = "value"
    }
    items = @("item1", "item2")
}
$data | ConvertTo-Json -Depth 10 | Set-Content "config.json"
```

### Modify JSON

```powershell
# Read, modify, save
$config = Get-Content "config.json" | ConvertFrom-Json
$config.propertyName = "new value"
$config.newProperty = "added"
$config | ConvertTo-Json -Depth 10 | Set-Content "config.json"
```

---

## Logging Function

Use this pattern for consistent logging:

```powershell
function Log-Operation {
    param(
        [ValidateSet("SUCCESS", "ERROR", "INFO", "PENDING", "WARNING")]
        [string]$Status,
        [string]$Operation,
        [string]$Details,
        [string]$LogFile = "${env:DEVICE_LOGS}"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $deviceName = $env:COMPUTERNAME
    $logEntry = "$timestamp - [$deviceName] $Status: $Operation - $Details"

    # Write to log file
    if ($LogFile -and (Test-Path (Split-Path $LogFile))) {
        Add-Content $LogFile -Value $logEntry
    }

    # Also output to console with color
    $color = switch ($Status) {
        "SUCCESS" { "Green" }
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "PENDING" { "Cyan" }
        default { "White" }
    }
    Write-Host $logEntry -ForegroundColor $color
}

# Usage
Log-Operation -Status "SUCCESS" -Operation "Install" -Details "Installed git via winget"
Log-Operation -Status "ERROR" -Operation "PATH" -Details "npm not found in PATH"
```

---

## Known Issues Prevention

This skill prevents **15** documented issues:

### Issue #1: Using bash commands in PowerShell
**Error**: `cat : The term 'cat' is not recognized`
**Why It Happens**: PowerShell uses different cmdlets than bash
**Prevention**: Use translation table above (`cat` -> `Get-Content`)

### Issue #2: PATH not persisting
**Error**: Commands work in one session but not another
**Why It Happens**: Setting `$env:PATH` only affects current session
**Prevention**: Use `[Environment]::SetEnvironmentVariable()` for persistence

### Issue #3: JSON depth truncation
**Error**: JSON output shows `@{...}` instead of nested values
**Why It Happens**: Default `-Depth` is 2
**Prevention**: Always use `ConvertTo-Json -Depth 10`

### Issue #4: Profile not loading
**Error**: Profile functions/aliases not available
**Why It Happens**: Wrong profile location or `-NoProfile` flag
**Prevention**: Verify `$PROFILE` path and check startup flags

### Issue #5: Script execution blocked
**Error**: `script.ps1 cannot be loaded because running scripts is disabled`
**Why It Happens**: Execution policy is Restricted
**Prevention**: Set `RemoteSigned` for current user

### Issue #6: npm global commands not found
**Error**: `npm : The term 'npm' is not recognized`
**Why It Happens**: npm path not in system PATH
**Prevention**: Add `%APPDATA%\npm` to User PATH via registry

### Issue #7: PowerShell 5.1 vs 7.x confusion
**Error**: Features not working, different behavior
**Why It Happens**: Using `powershell.exe` (5.1) instead of `pwsh.exe` (7.x)
**Prevention**: Always use `pwsh` command or verify with `$PSVersionTable`

---

## Using Bundled Resources

### Scripts (scripts/)

**Verify-ShellEnvironment.ps1** - Comprehensive environment check
```powershell
.\scripts\Verify-ShellEnvironment.ps1
```

Tests: PowerShell version, profile location, PATH configuration, tool availability

### Templates (templates/)

**profile-template.ps1** - Recommended PowerShell profile
```powershell
Copy-Item templates/profile-template.ps1 $PROFILE
```

---

## Troubleshooting

### Problem: Command not found after installation
**Solution**:
1. Check PATH: `$env:PATH -split ';' | Select-String "expected-path"`
2. Refresh session: Start new PowerShell window
3. Check registry PATH vs session PATH

### Problem: Profile changes not taking effect
**Solution**:
1. Verify profile path: `$PROFILE`
2. Dot-source to reload: `. $PROFILE`
3. Check for syntax errors: `pwsh -NoProfile -Command ". '$PROFILE'"`

### Problem: JSON losing data on save
**Solution**: Always use `-Depth 10` or higher with `ConvertTo-Json`

### Problem: Scripts from internet won't run
**Solution**:
```powershell
# Unblock single file
Unblock-File -Path script.ps1

# Or set execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Complete Setup Checklist

- [ ] PowerShell 7.x installed (`pwsh --version`)
- [ ] Execution policy set to RemoteSigned
- [ ] npm path in User PATH (registry)
- [ ] Profile created and loading
- [ ] `.env` file created from template
- [ ] Verification script passes
- [ ] Package managers working (winget, scoop, npm)

---

## Official Documentation

- **PowerShell**: https://learn.microsoft.com/en-us/powershell/
- **winget**: https://learn.microsoft.com/en-us/windows/package-manager/winget/
- **scoop**: https://scoop.sh/
- **chocolatey**: https://chocolatey.org/

---

## Package Versions (Verified 2025-12-06)

```json
{
  "tools": {
    "PowerShell": "7.5.x",
    "winget": "1.9.x",
    "scoop": "0.5.x"
  }
}
```
