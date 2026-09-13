---
name: cloud-weaver-computer-setup
description: >
  This skill should be used when the user asks to "set up my computer",
  "install dev tools", "set up my environment", or when the pre-flight check
  reports NEEDS_COMPUTER_SETUP. It detects the OS, tries install methods in
  order of reliability, and falls back gracefully. Works on Linux, macOS,
  Windows (native or WSL), and locked-down corporate machines.
---

# Computer Setup

CloudWeaver v2 needs three tools locally — everything else runs in GitHub
Actions. The skill detects the OS and tries install methods from most
convenient to most universally compatible.

**Required tools:** `gh` (GitHub CLI) · `ssh` (OpenSSH client) · `python3`

`git` and `jq` are **not** required: provisioning and deployment run in CI,
and `jq` is built into `gh` via `--jq`.

---

## Step 1 — Detect OS and available tools

```python
import platform, shutil, os

system  = platform.system()   # "Linux", "Darwin", "Windows"
is_wsl  = system == "Linux" and os.path.exists("/proc/version") and \
          "microsoft" in open("/proc/version").read().lower()
has_bash = shutil.which("bash") is not None
has_pwsh = shutil.which("pwsh") or shutil.which("powershell")
has_npx  = shutil.which("npx")  is not None
has_curl = shutil.which("curl") is not None

missing = [t for t in ["gh", "ssh", "python3"] if not shutil.which(t)]
print(f"OS: {system}{'  (WSL)' if is_wsl else ''}")
print(f"Missing: {missing or 'none'}")
```

If nothing is missing, skip to Step 3.

---

## Step 2 — Install missing tools

Try the tiers in order — stop at the first that works.

### Tier 1 — bash (Linux · macOS · WSL · Git Bash)

```bash
curl -fsSL https://cloudweaver.fagnerlopes.dev/install.sh | bash
```

**When to use:** `bash` is available (`has_bash = True`).

### Tier 2 — PowerShell (Windows without WSL)

```powershell
irm https://cloudweaver.fagnerlopes.dev/install.ps1 | iex
```

**When to use:** no bash, but PowerShell is available (`has_pwsh = True`).
If execution policy blocks it, ask the user to run first:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Tier 3 — Python (any OS with Python 3)

```bash
curl -fsSL https://cloudweaver.fagnerlopes.dev/install.py | python3
```

**When to use:** no bash, no PowerShell — but Python 3 and curl exist.
On Windows without curl, download manually:
```powershell
Invoke-WebRequest -Uri https://cloudweaver.fagnerlopes.dev/install.py -OutFile install.py
python3 install.py
```

### Tier 4 — npx (any OS with Node 18+)

```bash
npx -y skills install fagnerlopes/cloud-weaver
```

**When to use:** always available as last resort — Node 18+ is a hard
prerequisite for the workshop. No curl, no bash, no PowerShell needed.

---

### Per-tool install (if the script approach fails)

If the platform scripts can't install `gh`, `ssh`, or `python3`, guide the
user to install each manually:

#### `gh` (GitHub CLI)
| Platform | Command |
|----------|---------|
| Linux / WSL | `sudo apt install gh` (after adding the [official repo](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)) |
| macOS | `brew install gh` |
| Windows | `winget install --id GitHub.cli` or download from https://cli.github.com |

#### `ssh` (OpenSSH client)
| Platform | Notes |
|----------|-------|
| Linux / WSL | `sudo apt install openssh-client` |
| macOS | Built-in — no install needed |
| Windows 10+ | Built-in: **Settings → Apps → Optional features → OpenSSH Client** |

#### `python3`
| Platform | Command |
|----------|---------|
| Linux / WSL | `sudo apt install python3` |
| macOS | `brew install python` |
| Windows | `winget install --id Python.Python.3` or https://python.org |

---

## Step 3 — GitHub authentication

```bash
gh auth status
```

If not authenticated, ask the user to run in their terminal:

```bash
gh auth login
```

---

## Step 4 — Re-run the pre-flight

After all tools are confirmed, re-run `cloud-weaver-pre-flight-check`.

---

## Bundled Resources

This skill has no bundled scripts — all steps run inline.
