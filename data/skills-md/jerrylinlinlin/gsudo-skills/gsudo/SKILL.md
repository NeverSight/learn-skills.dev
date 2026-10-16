---
name: gsudo
description: >-
  Cheatsheet for gsudo — a sudo for Windows — to run commands elevated (as admin) or elevate the
  current shell in-place, without a separate admin window. Use it for essentially any gsudo /
  "sudo on Windows" task: elevating the current CMD / PowerShell / WSL / Git-Bash shell, cutting
  UAC popups with the credentials cache, running as System / TrustedInstaller / another user / a
  chosen integrity level, elevating in a new window, the PowerShell `gsudo { ScriptBlock }` /
  `Invoke-gsudo` / `$using:` syntax, scripts that self-elevate, detecting elevation with
  `gsudo status`, dropping privileges with `-i`, and tuning via `gsudo config`. Trigger on
  phrasings like "run as admin from the terminal", "elevate this command", "sudo on Windows",
  "gsudo", "run as SYSTEM / TrustedInstaller", "fewer UAC prompts", "make a script self-elevate",
  or "am I running elevated". Assumes gsudo is installed and on PATH. Covers CMD / PowerShell /
  WSL / Git-Bash / MSYS2.
---

# gsudo — Cheatsheet

A dense command reference for **gsudo**, a `sudo` for Windows: it runs a single command elevated, or
re-launches your current shell elevated, **in the same console window** (no context-switch to a
separate admin window), with one UAC popup per elevation — or none while a credentials-cache session
is active. This is a cheatsheet, not a fixed procedure: jump to the section you need and copy the
snippet.

## Install the dependency

Install gsudo with WinGet, open a new terminal, and verify it:

```powershell
winget install --id gerardog.gsudo --exact
gsudo --version
```

Assumes `gsudo` is already installed and on `PATH` (verified default install:
`C:\Program Files\gsudo\Current\gsudo.exe`). Examples are written for **PowerShell**; CMD / WSL /
Git-Bash variants are noted where they differ.

- **The `sudo` alias:** the installers create a `sudo` alias for gsudo — use either name. (If
  Microsoft's *Sudo for Windows* is also installed, `sudo` resolves to *it* first; see §13.)
- **Already elevated?** gsudo is a no-op passthrough — it just runs the command, no error, no UAC.
  Safe to leave `gsudo` in scripts that may already run as admin.
- **Exit codes:** gsudo returns the command's own exit code. **`999`** means *gsudo failed to
  elevate* (e.g. UAC denied). On WSL that surfaces as `231` (999 mod 256).
- **Mental model:** `gsudo {command}` re-interprets the command with a *new instance of your current
  shell* — in PowerShell `gsudo mkdir x` runs `pwsh -c "mkdir x"`, in CMD `cmd /c "mkdir x"`. The
  elevated process runs in a **separate process**, so it can't see your shell's live variables/scope.

Deeper upstream docs are copied verbatim under [`reference/`](reference/) — read them when the
cheatsheet isn't enough: [usage.md](reference/usage.md), [powershell.md](reference/powershell.md),
[credentials-cache.md](reference/credentials-cache.md), [security.md](reference/security.md),
[how-it-works.md](reference/how-it-works.md), [scripts-self-elevation.md](reference/scripts-self-elevation.md).

> Verified against **gsudo v2.6.1** on Windows 11. Every flag, config key, and `status` field below
> was confirmed against the installed binary's `gsudo help` / `gsudo config` / `gsudo status --json`.

---

## 1. The four things gsudo does

```powershell
gsudo                          # elevate the CURRENT shell, in-place, same window (Ctrl-C / `exit` to drop back)
gsudo {command} [args]         # run one command elevated, output in this console
gsudo cache on                 # start a credentials-cache session → later elevations skip the UAC popup (§4)
gsudo status                   # who am I / am I elevated / cache state (§9)
```

- `gsudo` with **no command** launches an elevated copy of your current shell in the same window. A
  red `#` in the prompt (CMD, or PowerShell with the module — §5) marks the elevated session. Type
  `exit` to return to your normal (medium-integrity) shell.
- gsudo does **not** modify your current process; it spawns a new elevated one. To "go back", end the
  elevated process (`exit`).

```powershell
gsudo notepad C:\Windows\System32\drivers\etc\hosts   # elevate a GUI/Win32 app
sudo  notepad C:\Windows\System32\drivers\etc\hosts   # same, via the built-in `sudo` alias
gsudo !!                                               # re-run your LAST command, elevated (see §5/§11)
```

`gsudo !!` works in CMD, Git-Bash, MinGW, MSYS2, Cygwin — and in PowerShell **only** if you import
the gsudo module (§5).

---

## 2. Options reference

Prepend options before the command: `gsudo [options] {command} [args]`.

| Option | Meaning |
| --- | --- |
| `-n, --new` | Run in a **new** console window; return immediately (don't wait). |
| `-w, --wait` | With `-n`, wait for the command to finish and return its exit code. |
| `--keepShell` | After the command, keep the elevated **shell** open (new-window mode). |
| `--keepWindow` | After the command, **ask for a keypress** before closing the new console. |
| `--close` | Override settings and **always close** the new window at the end. |
| `-i, --integrity {level}` | Run at a specific integrity: `Untrusted, Low, Medium, MediumPlus, High` (default), `System`. Also *lowers* privilege (§6). |
| `-u, --user {name}` | Run as another user (prompts for password). For local admins shows UAC unless `-i Medium`. |
| `-s, --system` | Run as **Local System** (`NT AUTHORITY\SYSTEM`). |
| `--ti` | Run as **TrustedInstaller** (`NT SERVICE\TrustedInstaller`). |
| `-k, --reset-timestamp` | Kill **all** cached credentials now (next elevation shows UAC). |
| `-d, --direct` | Skip shell detection — treat the command as a **CMD** command (§10, §12). |
| `--loadProfile` | When elevating PowerShell, load the user `$PROFILE` (default: `-NoProfile`). |
| `--chdir {dir}` | `cd` to `{dir}` before running the command. |
| `--copyns` | Reconnect the caller's mapped network drives in the elevated session (interactive; may prompt). |
| `--copyev` | *(deprecated)* Copy all env vars to the elevated process (not needed in default mode). |
| `--loglevel {v}` | `All, Debug, Info` (default), `Warning, Error, None`. |
| `--debug` | Verbose internal debug output — first thing to try when something misbehaves. |

**Microsoft-sudo-compatible aliases** (so muscle memory from *Sudo for Windows* works): `--inline`,
`--new-window`, `--disable-input` (= `SecurityEnforceUacIsolation`), `--preserve-env`,
`-D` / `--chdir {dir}`.

```powershell
gsudo -n -w pwsh ./Deploy.ps1        # elevate in a new window, wait for it, capture exit code
gsudo --chdir C:\Repo git pull        # elevate + run from a specific directory
```

---

## 3. Redirection, piping & scripting

gsudo is script-friendly: stdin/stdout/stderr redirect and pipe normally, and the command's exit code
propagates.

```powershell
gsudo dir | findstr /c:"bytes free" > FreeSpace.txt     # pipe/redirect the elevated command's output
echo "md C:\NewFolder" | gsudo cmd                       # feed stdin to an elevated shell
gsudo dir "C:\System Volume Information" > listing.txt   # capture elevated output to a file
```

Check whether elevation itself succeeded (exit code `999` = gsudo could not elevate):

```powershell
gsudo ./task.exe
if ($LASTEXITCODE -eq 999) { 'gsudo failed to elevate!' }
elseif ($LASTEXITCODE)     { 'Command failed!' }
else                       { 'Success!' }
```

For scripts that must **re-launch themselves** as admin, see §9 (self-elevation) —
[scripts-self-elevation.md](reference/scripts-self-elevation.md) has copy-paste CMD/PowerShell templates.

---

## 4. Credentials cache — fewer UAC popups

A cache session is just a running elevated gsudo instance that lets the **same caller process (and
its children)** elevate again without a UAC prompt. No service, no persistent daemon. It ends on
`cache off`, on `-k`, when the caller process exits, or after the idle timeout (default 5 min).

```powershell
gsudo config CacheMode Auto     # persistent setting: first elevation pops UAC + opens a cache; rest are silent
gsudo config CacheMode Explicit # (default) UAC every time, UNLESS you `gsudo cache on` first
gsudo config CacheMode Disabled # UAC every time; `cache on` throws

gsudo cache on                  # start a cache session for THIS process (one UAC popup now)
gsudo cache off                 # end this process's cache session
gsudo -k                        # end ALL cache sessions (do this before handing your PC to someone)
gsudo cache on -p 0             # allow ANY process to use the cache (default is caller pid only)
gsudo cache on -d 00:30:00      # idle timeout 30 min ( -d -1 = until logoff )
```

| CacheMode | Behavior |
| --- | --- |
| **Explicit** (default) | Every elevation shows UAC unless a session was started with `gsudo cache on`. |
| **Auto** | Unix-sudo-like: first elevation shows UAC **and** auto-starts a cache session. |
| **Disabled** | Every elevation shows UAC; starting a cache session errors out. |

> **Security note:** an active cache ≈ temporarily relaxing UAC/UIPI for the whitelisted process. A
> malicious process already running as you could inject into it and elevate silently. It's off by
> default for this reason — see [security.md](reference/security.md).

Tune with `gsudo config CacheDuration 00:05:00` (or `Infinite`). Full details:
[credentials-cache.md](reference/credentials-cache.md).

---

## 5. PowerShell — the elevation syntaxes

When the current shell is PowerShell, the command runs in a **separate elevated process** and cannot
touch your live `$variables`/scope. Pick a syntax:

### A) `gsudo { ScriptBlock }` — best performance (recommended)

```powershell
gsudo { Get-Process chrome }                              # wrap the command in { braces }
gsudo { Get-Process $args } -args "chrome"                # pass values with -args → $args[]
gsudo { echo $args[0] $args[1] } -args "Hello", "World"

# Capture output → auto-serialized back as PSObjects (transparent, but slower for huge graphs)
$svc = gsudo { Get-Service WSearch, Winmgmt }
$svc.DisplayName

# Pipeline input must be mapped explicitly with $input
Get-Process winword | gsudo { $input | Stop-Process }

# Elevate a WHOLE pipeline by putting it inside the scriptblock:
gsudo { Get-ChildItem C:\ProtectedDir | Where-Object Length -gt 1MB }
```

- If the result is **not** captured in a variable, no serialization happens → fastest (prints to console).
- `Get-Process` and other huge object graphs serialize **slowly** — capture only what you need.
- In a bare pipeline, `cmd1 | gsudo cmd2 | cmd3` elevates **only** `cmd2`.

### B) `Invoke-gsudo` — native syntax, `$using:` variables (needs the module)

```powershell
$folder = "C:\ProtectedFolder"
Invoke-gsudo { Remove-Item $using:folder }               # $using: injects the serialized value
(Invoke-gsudo { Get-ChildItem $using:folder }).LastWriteTime   # results are real PSObjects
Get-Process SpoolSv | Invoke-gsudo { Stop-Process -Force }      # accepts pipeline input
Invoke-gsudo { ... } -LoadProfile -Credential (Get-Credential)  # load $PROFILE / run as user
```

Slower than the scriptblock form (always serializes) but preserves more context (`$ErrorActionPreference`,
current location) and reads like a normal cmdlet.

### C) `gsudo 'string'` — legacy, discouraged

```powershell
$hash = gsudo "(Get-FileHash 'C:\My Secret.txt' -Algorithm md5).Hash"   # returns strings, escaping is painful
```

### The gsudo PowerShell module

Import `gsudoModule` in your `$PROFILE` for: tab auto-complete, `gsudo !!` (elevate last command),
suggestion of your last 3 commands, and helper functions.

```powershell
# Add to $PROFILE (or run this once to append it):
Write-Output "`nImport-Module gsudoModule" | Add-Content $PROFILE

# Optional red `#` elevated-prompt indicator:
Set-Alias Prompt gsudoPrompt
```

Module functions: `Test-IsProcessElevated`, `Test-IsAdminMember`, `Test-IsGsudoCacheAvailable`. Full
notes & the `$LASTEXITCODE`-999 test: [powershell.md](reference/powershell.md).

> **Elevate a CMD command from PowerShell without spinning up pwsh:** `gsudo -d dir C:\`.

---

## 6. Run as another identity / integrity level

`gsudo` isn't only "become admin" — `-i` sets an exact integrity level, and can also **drop**
privileges (run *less* trusted) from an elevated shell.

```powershell
gsudo -s cmd                       # Local SYSTEM (NT AUTHORITY\SYSTEM)
gsudo --ti cmd                     # TrustedInstaller (highest; Win10/11 only)
gsudo -u SomeUser {command}        # run as another user (prompts for password)
gsudo -u Administrator -i Medium {command}   # as a local admin WITHOUT a UAC popup (medium integrity)
gsudo -i High cmd                  # explicit High integrity (the normal "admin" level; default)

# De-elevation: from an ELEVATED shell, launch something at LOWER integrity
gsudo -i Medium explorer.exe       # restart Explorer un-elevated
gsudo -i Low  {command}            # run a risky command sandboxed at Low integrity
```

Integrity levels, low → high: `Untrusted, Low, Medium, MediumPlus, High (default), System`.

---

## 7. Elevate in a new window

Same-console elevation carries a mild risk. Elevating in a **new** console avoids it, and is
handy for fire-and-forget admin tasks.

```powershell
gsudo -n {command}                 # launch elevated in a NEW window, return immediately
gsudo -n -w {command}              # ...and WAIT for it, returning its exit code
gsudo -n --keepShell {command}     # keep the elevated shell open afterwards
gsudo -n --keepWindow {command}    # ask for a keypress before the new window closes
```

Make it the default for **all** elevations, and choose what happens when the command finishes:

```powershell
gsudo config NewWindow.Force true
gsudo config NewWindow.CloseBehaviour KeepShellOpen    # or PressKeyToClose | OsDefault (default)
```

`--close` overrides the setting and always closes the window at the end.

---

## 8. Configuration

Settings live in the registry: **user** at `HKCU\Software\gsudo`, **global** (all users, overrides
user) at `HKLM\Software\gsudo` via `--global` (writing global needs elevation).

```powershell
gsudo config                            # dump every setting + current value
gsudo config CacheMode Auto             # write a user setting
gsudo config Prompt --reset             # reset ONE setting to default
gsudo config --reset-all                # reset EVERYTHING to defaults
gsudo config PathPrecedence true --global   # write a machine-wide setting (elevates)
```

Keys that matter most (verified, v2.6.1):

| Key | Purpose |
| --- | --- |
| `CacheMode` | `Auto \| Explicit` (default) `\| Disabled` (§4). |
| `CacheDuration` | Idle lifetime `HH:MM:SS` (default `00:05:00`) or `Infinite`. |
| `NewWindow.Force` | Always elevate in a new window (= implicit `-n`) (§7). |
| `NewWindow.CloseBehaviour` | `OsDefault` (default) `\| KeepShellOpen \| PressKeyToClose`. |
| `PowerShellLoadProfile` | Load `$PROFILE` on PowerShell elevations (= `--loadProfile`). |
| `PathPrecedence` | Make gsudo win over Microsoft's `sudo` on `PATH` (§13). |
| `Prompt` / `PipedPrompt` | CMD prompt string for elevated sessions (default is the red `#`). |
| `SecurityEnforceUacIsolation` | Elevate with input closed (non-interactive, safer). |
| `LogLevel` | `All, Debug, Info` (default), `Warning, Error, None`. |
| `ForceAttachedConsole` / `ForcePipedConsole` / `ForceVTConsole` | Force an elevation mode — troubleshooting only (§12). |
| `ExceptionList` | Executables launched via `cmd /c` (default: `notepad.exe;powershell.exe;whoami.exe;vim.exe;nano.exe;`). |

---

## 9. Am I elevated? — `gsudo status` & self-elevating scripts

`gsudo status` reports user, SID, admin membership, integrity, and cache state. Query one field by
name; add `--no-output` to get **only** an exit code (boolean fields: **true → exit 0, false → exit 1**).

```powershell
gsudo status                        # human-readable summary
gsudo status --json                 # machine-readable (keys below)
gsudo status IsElevated             # prints `true` / `false`
gsudo status IsAdminMember          # is the user in the local Administrators group (S-1-5-32-544)?
```

**JSON status keys:** `CallerPid, UserName, UserSid, IsElevated, IsAdminMember, IntegrityLevelNumeric,
IntegrityLevel, CacheMode, CacheAvailable, CacheSessionsCount, CacheSessions, IsRedirected,
ConsoleProcesses`.

Prefer `gsudo status IsElevated` over `whoami`/`net session` for detecting elevation — it's
language-independent and doesn't depend on the network.

**Self-elevate a script** (re-launch elevated if it isn't already):

```powershell
# PowerShell — put at the top of your .ps1
if ((gsudo status IsElevated) -eq 'false') {
    gsudo "& '$($MyInvocation.MyCommand.Source)'" $args
    if ($LASTEXITCODE -eq 999) { Write-Error 'Failed to elevate.' }
    return
}
# ...elevated from here on...
```

```batch
:: CMD one-liner — self-elevate, then continue
@gsudo status IsElevated --no-output || (gsudo "%~f0" & exit /b)
:: ...elevated from here on...
```

More templates (full batch version, "member of Admins?" checks, no-gsudo fallback):
[scripts-self-elevation.md](reference/scripts-self-elevation.md).

---

## 10. Other shells

gsudo detects the calling shell and elevates commands **in that shell's language** — unless `-d`
forces a CMD command.

**WSL** — elevation ≠ `root`. `root` administers the WSL distro; gsudo elevates the *Windows* side
(`wsl.exe`). Use WSL's own `sudo`/`su` for root inside the distro.

```bash
gsudo                                   # elevate the default WSL shell (UAC popup)
gsudo mkdir /mnt/c/Windows/MyFolder     # elevated WSL command
gsudo -d notepad C:/Windows/System32/drivers/etc/hosts   # elevated *Windows* (CMD) command
# gsudo failure exit code 999 reads as 231 on WSL (999 mod 256)
```

**Git-Bash / MSYS2 / MinGW / Cygwin** — the process tree splits when bash invokes the gsudo wrapper,
which breaks the credentials cache. Add this to `.bashrc` to call the real exe directly:

```bash
gsudo() { WSLENV=WSL_DISTRO_NAME:USER:$WSLENV MSYS_NO_PATHCONV=1 gsudo.exe "$@"; }
```

*(The trailing `;` before `}` is intentional.)*

**CMD** — plain `gsudo {command}`; `gsudo` alone elevates the current CMD. `gsudo !!` re-runs the last
command. Also supported: Yori, Take Command, NuShell, BusyBox.

---

## 11. Windows Terminal

Two ways to get an elevated tab:

- **On demand (preferred):** in any tab, run `gsudo` to elevate the current shell in place, or prepend
  `gsudo` to specific commands. No separate elevated profile needed.
- **Dedicated elevated profile:** add/edit a WT profile and set its command to `gsudo cmd` or
  `gsudo pwsh` (or prepend `gsudo ` to the existing command line).

---

## 12. How elevation works (and forcing a mode)

gsudo launches a hidden elevated "service" instance (via `Verb=RunAs` → the UAC prompt) that brokers
the elevation over named pipes. It has four mechanisms; the default **TokenSwitch** gives native
console behavior (full speed, colors, input, redirection). You normally never pick one.

Troubleshooting only — force a mode if a specific app misbehaves:

```powershell
gsudo --attached {command}    # or: gsudo config ForceAttachedConsole true
gsudo --vt       {command}    # or: gsudo config ForceVTConsole true      (experimental)
gsudo --piped    {command}    # or: gsudo config ForcePipedConsole true   (legacy; last resort)
```

> TokenSwitch inherits the **non-elevated** environment variables. When you elevate *as another user*
> (not a local admin), gsudo falls back to Attached or Piped mode automatically. Details & trade-offs:
> [how-it-works.md](reference/how-it-works.md).

---

## 13. Coexisting with Microsoft's Sudo for Windows

If both are installed, **`sudo` runs Microsoft's** `C:\Windows\System32\sudo.exe` (that dir is earlier
on `PATH`); `gsudo` always runs gsudo. To make the `sudo` keyword resolve to gsudo:

```powershell
gsudo config PathPrecedence true      # then restart all consoles ( false reverts )
```

They otherwise run independently. gsudo also accepts Microsoft-sudo-style flags (`--inline`,
`--new-window`, `--disable-input`, `--preserve-env`, `-D/--chdir`) for an easy switch. Feature
comparison: [gsudo-vs-sudo](https://gerardog.github.io/gsudo/docs/gsudo-vs-sudo).

---

## 14. Windows Defender may block gsudo — add an exclusion

Defender (and some AVs) flag gsudo as a UAC/elevation *hacktool* and can quarantine `gsudo.exe` or
silently block the elevation. **If Defender's real-time protection is active, add gsudo's install
folder to the exclusion list** — a targeted, one-time fix (needs admin):

```powershell
$exe = (Get-Command gsudo -ErrorAction SilentlyContinue).Source
if ($exe -and (Get-MpComputerStatus -ErrorAction SilentlyContinue).RealTimeProtectionEnabled) {
    $dir = Split-Path (Split-Path $exe)     # gsudo install root, covers all versions (e.g. C:\Program Files\gsudo)
    if ((Get-MpPreference).ExclusionPath -notcontains $dir) {
        gsudo { Add-MpPreference -ExclusionPath $args[0] } -args $dir   # elevates the change
    }
}
(Get-MpPreference).ExclusionPath            # verify the folder is now listed
```

- Only the gsudo folder is excluded — Defender keeps scanning everything else.
- If gsudo is **already** quarantined (so it can't self-elevate), run
  `Add-MpPreference -ExclusionPath "<gsudo folder>"` from a manually-elevated PowerShell, then retry.
- Undo later (elevated): `Remove-MpPreference -ExclusionPath "<gsudo folder>"`.

---

## 15. Troubleshooting

- **After install/upgrade** or `Unauthorized. (Different gsudo.exe?)` → **close all consoles and open
  new ones** (refreshes `PATH`).
- **See what's happening:** `gsudo --debug {command}`.
- **PowerShell installed as a dotnet global tool** is [known-broken](https://github.com/PowerShell/PowerShell/issues/11747)
  with gsudo — reinstall pwsh via winget/choco/MSI/Store instead.
- **Network shares:** elevated sessions don't inherit the non-elevated session's mapped drives (a
  Windows behavior). Use `--copyns` to reconnect them (interactive).
- **Don't** run gsudo when your **current directory** is a mapped network drive (e.g. `Z:\> gsudo …`);
  invoking `\\server\share\gsudo {command}` is fine.
- **Requirements:** Windows 7 SP1+; some features (e.g. `--ti` TrustedInstaller) need Windows 10/11.

---

## When the cheatsheet runs out

- `gsudo help`, `gsudo config` (all keys + defaults), `gsudo status --json` — the authoritative,
  version-correct reference on this machine.
- Bundled upstream docs: [`reference/`](reference/). Online: <https://gerardog.github.io/gsudo/docs/>.
