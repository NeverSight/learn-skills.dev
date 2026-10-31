---
name: install-missing-tool
description: Use when a shell command is not found during task execution, or a required tool is missing from the agent's environment
---

# Install Missing Tool

**Core rule: never install software automatically. Always ask user permission first.**

When a command fails with "command not found", "not recognized", or similar, the agent MUST attempt to install the missing tool through a package manager — but ONLY after explicit user approval.

## When to Use

- Shell returns `command not found` / `not recognized` / `no such file or directory` for a needed command
- A script or tool requires a dependency that is not installed
- Task execution is blocked by a missing utility

**NOT needed for:** Python/Node.js imports within a project (those go in `requirements.txt`, `package.json`, etc.).

## Procedure

### 1. Identify the missing tool

Run the failing command or check the error message to identify the exact binary name needed.

### 2. Map the tool to a package name

Use the table below to find the correct package. If the tool is not listed, search for it with the preferred package manager (`brew search <tool>`, `apt search <tool>`, etc.).

| Command | Homebrew | apt (Debian/Ubuntu) | dnf (Fedora/RHEL) | pacman (Arch) | winget (Windows) |
|---------|----------|---------------------|-------------------|---------------|------------------|
| `jq` | jq | jq | jq | jq | jqlang.jq |
| `fzf` | fzf | fzf | fzf | fzf | junegunn.fzf |
| `rg` (ripgrep) | ripgrep | ripgrep | ripgrep | ripgrep | BurntSushi.ripgrep |
| `fd` | fd | fd-find | fd-find | fd | sharkdp.fd |
| `bat` | bat | bat | bat | bat | sharkdp.bat |
| `tree` | tree | tree | tree | tree | GNUWin32.Tree |
| `httpie` | httpie | httpie | httpie | httpie | httpie.httpie |
| `curl` | curl | curl | curl | curl | curl.curl |
| `wget` | wget | wget | wget | wget | GNU.Wget |
| `tmux` | tmux | tmux | tmux | tmux | tmux.tmux |
| `neofetch` | neofetch | neofetch | neofetch | neofetch | — |
| `htop` | htop | htop | htop | htop | — |
| `yq` | yq | yq | yq | yq | — |
| `diff-so-fancy` | diff-so-fancy | — | — | — | — |
| `shellcheck` | shellcheck | shellcheck | ShellCheck | shellcheck | — |
| `pandoc` | pandoc | pandoc | pandoc | pandoc | — |

**Language-specific tools:**

| Tool | Package / Command |
|------|-------------------|
| Python packages | `uv tool install <package>` (preferred) or `uv add <package>` for project-local |
| Node.js packages | `npm install -g <package>` |
| Rust tools | `cargo install <package>` |
| Go tools | `go install <package>@latest` |

### 3. Determine the available package manager

Check in order of preference:

1. **Homebrew** (`brew --version`) — macOS and Linux
2. **OS native:**
   - Debian/Ubuntu: `dpkg --version` → `apt` / `apt-get`
   - Fedora/RHEL/CentOS: `rpm --version` → `dnf` or `yum`
   - Arch/Manjaro: `pacman --version` → `pacman`
   - openSUSE: `zypper --version` → `zypper`
   - Alpine: `apk --version` → `apk`
   - Windows: `winget --version` → `winget`, or `choco --version` → `chocolatey`
3. **Language-specific:** `uv --version`, `npm --version`, `cargo --version`, `go version`

### 4. Ask user permission

**This step is mandatory and has no exceptions.**

Present the user with:
- The tool name and package manager
- The exact command that will be run
- Whether it requires elevated privileges (`sudo`, admin rights)

```
I need to install `<tool>` to continue. The command is:
  brew install <package>

This requires user privileges. May I proceed?
```

If `sudo` is required:
- Ask the user to run the command themselves, OR
- Ask if they want to provide their password for you to run it

**NEVER run installation commands without explicit approval. Not even for "obvious" tools. Not even with `--yes` flags.**

### 5. Install the tool

Run the installation command after user approval:

```bash
# Homebrew (macOS/Linux)
brew install <package>

# apt (Debian/Ubuntu) — requires sudo
sudo apt install -y <package>

# dnf (Fedora/RHEL) — requires sudo
sudo dnf install -y <package>

# pacman (Arch) — requires sudo
sudo pacman -S <package>

# apk (Alpine) — requires root
apk add <package>

# winget (Windows)
winget install <package>

# chocolatey (Windows, admin)
choco install <package> -y

# Python tools — uv preferred over pip
uv tool install <package>        # global tool (e.g. uv tool install ruff)
uv add <package>                 # project-local dependency

# Node.js tools
npm install -g <package>

# Rust tools
cargo install <package>

# Go tools
go install <package>@latest
```

### 6. Verify installation

After installation, verify the tool is available:

```bash
<tool> --version
# or
which <tool>
```

If verification fails, check for PATH issues or installation errors.

## Fallback: Custom Script

Only if no package manager can provide the tool:

1. Explain to the user that no package was found
2. Propose a custom installation script (download + extract + PATH setup)
3. Ask for explicit permission before running any download or script
4. Never run downloaded scripts without user review

## Pitfalls

- **Auto-installing:** NEVER install without asking. Always ask first.
- **Pip over uv:** Python tool installations MUST prefer `uv` over `pip`. `uv tool install` for global tools, `uv add` for project dependencies. Only fall back to `pip install` if `uv` is unavailable.
- **Wrong package name:** The binary name and package name often differ (`fd-find` vs `fd`, `ripgrep` vs `rg`). Always verify the package name first.
- **Sudo without asking:** If installation requires `sudo`, the user MUST either run it themselves or explicitly authorize you to run it.
- **Silent failures:** Some package managers fail silently or install to a non-PATH location. Always verify with `which` or `<tool> --version`.
- **Partial installs:** If an install is interrupted, re-run the install command — package managers handle this gracefully.

## Verification

After installing any tool:

```bash
which <tool> && <tool> --version
```

- The tool path is in the user's `$PATH`
- The version command returns output (no errors)
- The tool is usable in the same shell session
