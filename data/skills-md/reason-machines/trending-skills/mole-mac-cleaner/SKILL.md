---
name: mole-mac-cleaner
description: Deep clean and optimize your Mac using the Mole CLI tool
triggers:
  - clean up my Mac disk space
  - remove app leftovers on macOS
  - optimize my Mac with mole
  - uninstall apps and hidden files mac
  - free up space on mac cli
  - analyze disk usage mac terminal
  - purge node_modules and build artifacts mac
  - monitor mac system stats terminal
---

# Mole Mac Cleaner

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Mole (`mo`) is an all-in-one macOS maintenance CLI that combines deep cleaning, smart app uninstallation, disk analysis, system optimization, live monitoring, and project artifact purging into a single binary.

## Installation

```bash
# Via Homebrew (recommended)
brew install mole

# Via install script (supports version pinning)
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash

# Specific version
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash -s 1.17.0

# Latest main branch (nightly)
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash -s latest
```

## Core Commands

```bash
mo                    # Interactive menu (arrow keys or vim h/j/k/l)
mo clean              # Deep system cache + browser + dev tool cleanup
mo uninstall          # Remove apps plus all hidden remnants
mo optimize           # Rebuild caches, reset network, refresh Finder/Dock
mo analyze            # Visual disk space explorer
mo status             # Live real-time system health dashboard
mo purge              # Remove project build artifacts (node_modules, target, dist)
mo installer          # Find and remove installer .dmg/.pkg files

mo touchid            # Configure Touch ID for sudo
mo completion         # Set up shell tab completion
mo update             # Update Mole
mo update --nightly   # Update to latest unreleased build (script install only)
mo remove             # Uninstall Mole itself
mo --help
mo --version
```

## Safe Preview Before Deleting

Always dry-run destructive commands first:

```bash
mo clean --dry-run
mo uninstall --dry-run
mo purge --dry-run

# Combine with debug for detailed output
mo clean --dry-run --debug
mo optimize --dry-run --debug
```

## Key Command Details

### `mo clean` — Deep Cleanup

Cleans user app caches, browser caches (Chrome, Safari, Firefox), developer tool caches (Xcode, Node.js, npm), system logs, temp files, app-specific caches (Spotify, Dropbox, Slack), and Trash.

```bash
mo clean                  # Interactive cleanup
mo clean --dry-run        # Preview what would be removed
mo clean --whitelist      # Manage protected caches (exclude from cleanup)
```

Whitelist config lives at `~/.config/mole/`. Edit it to protect paths you want to keep.

### `mo uninstall` — Smart App Removal

Finds apps, shows size and last-used date, then removes the app bundle plus all related files:
- Application Support, Caches, Preferences
- Logs, WebKit storage, Cookies
- Extensions, Plugins, Launch Daemons

```bash
mo uninstall              # Interactive multi-select list
mo uninstall --dry-run    # Preview removals
```

### `mo optimize` — System Refresh

```bash
mo optimize               # Run all optimizations
mo optimize --dry-run     # Preview
mo optimize --whitelist   # Exclude specific optimizations
```

Optimizations include:
- Rebuild system databases and clear caches
- Reset network services
- Refresh Finder and Dock
- Clean diagnostic and crash logs
- Remove swap files and restart dynamic pager
- Rebuild launch services and Spotlight index

### `mo analyze` — Disk Explorer

```bash
mo analyze                # Analyze home directory (skips /Volumes by default)
mo analyze ~/Downloads    # Analyze specific path
mo analyze /Volumes       # Include external drives explicitly

# Machine-readable output for scripting
mo analyze --json ~/Documents
```

**JSON output example:**
```json
{
  "path": "/Users/you/Documents",
  "entries": [
    { "name": "Library", "path": "...", "size": 80939438080, "is_dir": true }
  ],
  "total_size": 168393441280,
  "total_files": 42187
}
```

**Navigator shortcuts inside `mo analyze`:**
| Key | Action |
|-----|--------|
| `↑↓` or `j/k` | Navigate list |
| `←→` or `h/l` | Go back / Enter directory |
| `O` | Open in Finder |
| `F` | Reveal in Finder |
| `⌫` | Move to Trash (via Finder, safer than direct delete) |
| `L` | Show large files |
| `Q` | Quit |

### `mo status` — Live Dashboard

```bash
mo status                 # Real-time CPU, GPU, memory, disk, network, processes
mo status --json          # JSON output for scripting
mo status | jq '.health_score'   # Auto-detects pipe → outputs JSON
```

**JSON output example:**
```json
{
  "host": "MacBook-Pro",
  "health_score": 92,
  "cpu": { "usage": 45.2, "logical_cpu": 8 },
  "memory": { "total": 25769803776, "used": 15049334784, "used_percent": 58.4 },
  "disks": [],
  "uptime": "3d 12h 45m"
}
```

Shortcuts inside `mo status`: `k` toggles the cat mascot, `q` quits.

### `mo purge` — Project Artifact Cleanup

Scans for `node_modules`, `target`, `build`, `dist`, `venv`, and similar directories. Projects newer than 7 days are unselected by default.

```bash
mo purge                  # Interactive multi-select
mo purge --dry-run        # Preview
mo purge --paths          # Configure custom scan directories
```

**Configure custom scan paths** (`~/.config/mole/purge_paths`):
```
~/Documents/MyProjects
~/Work/ClientA
~/Work/ClientB
```

When this file exists, Mole uses only those paths. Otherwise it defaults to `~/Projects`, `~/GitHub`, `~/dev`.

> Install `fd` for faster scanning: `brew install fd`

### `mo installer` — Installer File Cleanup

```bash
mo installer              # Find .dmg/.pkg files in Downloads, Desktop, Homebrew cache, iCloud, Mail
mo installer --dry-run    # Preview removals
```

## Configuration Files

All config lives in `~/.config/mole/`:

| File | Purpose |
|------|---------|
| `purge_paths` | Custom directories for `mo purge` to scan |
| `operations.log` | Log of all file operations |

**Disable operation logging:**
```bash
export MO_NO_OPLOG=1
mo clean
```

## Shell Tab Completion

```bash
mo completion             # Interactive setup for bash/zsh/fish
```

## Touch ID for sudo

```bash
mo touchid                # Enable Touch ID authentication for sudo commands
mo touchid enable --dry-run
```

## Scripting & Automation Patterns

### Check disk health in a script

```bash
#!/bin/bash
health=$(mo status --json | jq -r '.health_score')
if [ "$health" -lt 70 ]; then
  echo "Health score low: $health — running cleanup"
  mo clean --dry-run  # swap to `mo clean` when ready
fi
```

### Get largest directories as JSON and process with jq

```bash
mo analyze --json ~/Downloads | jq '.entries | sort_by(-.size) | .[0:5] | .[] | {name, size_gb: (.size / 1073741824 | . * 100 | round / 100)}'
```

### Automated project purge in CI teardown

```bash
#!/bin/bash
# Non-interactive purge of build artifacts after CI
MO_NO_OPLOG=1 mo purge --dry-run   # always preview first in scripts
```

### Raycast / Alfred quick launchers

```bash
curl -fsSL https://raw.githubusercontent.com/tw93/mole/main/install.sh | bash
# Then bind `mo clean`, `mo status`, `mo analyze` as script commands in Raycast
```

## Safety Boundaries

- `mo analyze` moves files to Trash via Finder (recoverable) instead of direct deletion — prefer it for ad hoc cleanup
- `clean`, `uninstall`, `purge`, `installer`, and `remove` are **permanently destructive** — always `--dry-run` first
- Mole validates paths and enforces protected-directory rules; it skips or refuses high-risk operations
- Operation log: `~/.config/mole/operations.log` — disable with `MO_NO_OPLOG=1`
- Review [SECURITY.md](https://github.com/tw93/Mole/blob/main/SECURITY.md) and [SECURITY_AUDIT.md](https://github.com/tw93/Mole/blob/main/SECURITY_AUDIT.md) before using in automated pipelines

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `mo: command not found` | Run `brew install mole` or re-run install script; check `$PATH` |
| Purge scan is slow | Install `fd`: `brew install fd` |
| External drives not appearing in analyze | Run `mo analyze /Volumes` explicitly |
| Want to protect a cache from being cleaned | Run `mo clean --whitelist` to add it |
| Need to exclude an optimization step | Run `mo optimize --whitelist` |
| Script getting interactive prompts | Use `--dry-run` flag; check for `MO_NO_OPLOG=1` env var |
| Nightly update not working | Nightly updates (`--nightly`) only work with script install, not Homebrew |

## Update & Remove

```bash
mo update                 # Update to latest stable
mo update --nightly       # Update to latest main (script install only)
mo remove                 # Uninstall Mole completely
mo remove --dry-run       # Preview what remove would delete
```
