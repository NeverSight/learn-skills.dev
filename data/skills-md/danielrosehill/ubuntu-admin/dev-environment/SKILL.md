---
name: dev-environment
description: Inventory and set up a developer environment on Ubuntu — Python (system python3 vs uv, pipx, pyenv, venv and conda detection; never pip into the system interpreter), Node.js (nvm/fnm vs apt/snap, version check), Java and other SDKs via SDKMAN, other toolchains on PATH, and git global configuration (identity, default branch, pull strategy, global gitignore) plus gh authentication. Use when asked "what Python environments do I have", "set up pyenv / uv", "which node version", "install npm", "what SDKs are installed", "check my git config", "set up a global gitignore". Works on the local machine or a remote host over SSH.
---

# Developer environment

Find what runtimes exist and who manages them, then fill gaps without breaking the system interpreter.

## Target

Local by default. Remote: `ssh <host> '<cmd>'`. Version managers are per-user and initialised from `~/.bashrc` — over SSH run them via `ssh <host> 'bash -lic "<cmd>"'` so the shell init loads.

## 1. Inventory

```bash
# Python
command -v python3; python3 --version; ls /usr/bin/python3.* 2>/dev/null
for t in uv pipx pyenv conda mamba micromamba poetry; do command -v $t >/dev/null && echo "$t: $($t --version 2>&1 | head -1)"; done
ls -d ~/.pyenv ~/miniconda3 ~/anaconda3 ~/miniforge3 ~/.local/share/uv 2>/dev/null
conda env list 2>/dev/null
pipx list --short 2>/dev/null

# Node
command -v node && node --version; command -v npm && npm --version
ls -d ~/.nvm ~/.local/share/fnm 2>/dev/null; snap list node 2>/dev/null; dpkg -l nodejs 2>/dev/null | tail -1

# JVM and other SDKs
[ -s ~/.sdkman/bin/sdkman-init.sh ] && bash -lc 'sdk current'
for t in java javac go rustc cargo dotnet ruby php gcc clang cmake; do command -v $t >/dev/null && echo "$t: $($t --version 2>&1 | head -1)"; done
update-alternatives --list java 2>/dev/null

# Anything else that looks like an SDK
ls /opt ~/.local/opt ~/sdk 2>/dev/null
```

Report which manager owns each runtime and flag conflicts (e.g. conda's `base` auto-activating and shadowing system `python3`; apt `nodejs` and nvm both on PATH).

## 2. Python rules

- **Never** `sudo pip install` or `pip install --user` against system Python. Ubuntu 23.04+ enforces this (PEP 668 "externally-managed-environment") — do not bypass with `--break-system-packages`.
- CLI apps → `pipx install <tool>` or `uv tool install <tool>`.
- Projects → `uv venv && uv pip install -r requirements.txt` (or `uv sync` with pyproject), or `python3 -m venv .venv` (`sudo apt-get install python3-venv`).
- Other Python versions → `uv python install 3.12` (simplest) or pyenv:

```bash
sudo apt-get install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
curl -fsSL https://pyenv.run | bash      # then add the init lines it prints to ~/.bashrc
pyenv install 3.12 && pyenv global system   # keep system as default unless asked otherwise
```

- Conda: if present, suggest `conda config --set auto_activate_base false` so it doesn't hijack every shell.

## 3. Node

```bash
# per-user, multiple versions (recommended for development)
curl -fsSL https://fnm.vercel.app/install | bash      # or nvm: https://github.com/nvm-sh/nvm#installing-and-updating
fnm install --lts && fnm default lts-latest
# system-wide single version: Ubuntu archive (often old) — sudo apt-get install nodejs npm
# or the snap: sudo snap install node --classic --channel=<major>/stable
```

Global npm packages with a version manager need no sudo; with apt nodejs set `npm config set prefix ~/.local` instead of `sudo npm -g`.

## 4. JVM via SDKMAN

```bash
sdk list java | head -40; sdk install java <identifier>; sdk default java <identifier>
sdk install gradle; sdk install maven
```

`apt install default-jdk` is fine when one system JDK is enough.

## 5. Git and GitHub

```bash
git --version
git config --global --list --show-origin
git config --global user.name "<name>"
git config --global user.email "<email>"
git config --global init.defaultBranch main
git config --global pull.rebase false        # or true / ff only — ask
git config --global core.editor "<editor>"
git config --global core.excludesFile ~/.gitignore_global
```

A minimal global gitignore (create only if `core.excludesFile` is unset):

```
.DS_Store
*.swp
*~
.idea/
.vscode/
__pycache__/
*.pyc
.venv/
node_modules/
.env
.env.local
```

gh: `gh auth status`; if unauthenticated, `gh auth login && gh auth setup-git` (install via `packages-cli-tools`).

## Desktop vs server

- **Desktop**: multiple versions via per-user managers are normal.
- **Server**: prefer one runtime from apt (patched by unattended-upgrades) or a container; per-user managers under service accounts complicate systemd units (absolute paths needed).

## Confirm before

- Installing or removing a runtime or version manager, and editing `~/.bashrc` init blocks.
- Changing global git settings that already have a value.
- Removing conda/pyenv/nvm installs or environments.

## Report

Table of runtimes (language, version, path, manager), conflicts found, git identity and key settings, gh auth state, and changes made.

## Related

- `packages-cli-tools` — gh, pipx, uv, SDKMAN installs.
- `shell-config` — PATH order and shell init files.
- `docker-setup` — containerised toolchains.
