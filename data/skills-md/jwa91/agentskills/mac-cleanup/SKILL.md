---
name: mac-cleanup
description: "Interactive macOS system cleanup for any dev machine. Frees disk space by pruning caches, package managers, unused apps, stale dev artifacts, and more. Discovers what's installed rather than assuming a specific setup. Always consults the user before deleting anything. Use when the user asks to: clean up their Mac, free disk space, remove unused apps, prune caches, clean developer artifacts, or any disk space maintenance task."
user_invocable: true
metadata:
  version: 0.1.0
---

# macOS Cleanup

An interactive, discovery-based macOS cleanup skill. Works on any Mac dev machine — detects installed tools, package managers, browsers, and dev directories rather than assuming a fixed setup.

## Safety Rules

These rules are non-negotiable. Follow them at all times:

1. **Never delete without approval.** Always show what will be deleted, its size, and get explicit user confirmation before executing any destructive command.
2. **Never `rm -rf` app bundles.** Use Finder via osascript to move apps to Trash:
   `osascript -e 'tell application "Finder" to delete POSIX file "/Applications/App.app"'`
3. **Never clear browser profile data** (cookies, history, passwords in ~/Library/Application Support/).
   OS-level browser caches in ~/Library/Caches/ are safe to remove like any app cache.
4. **Honor protected paths.** Ask the user for any paths that should be skipped, and never touch them.
5. **Never touch `.git` directories.** Only clean merged branches (via `git branch -d`), never remove `.git` itself.
6. **Never touch system directories.** `/System`, `/Library` (root level), `/usr`, `/bin`, `/sbin` are off-limits.
7. **Never use `sudo`** unless the user explicitly asks for elevated privileges and understands why.
8. **Keep a running tally.** Track and display cumulative space freed after each action.
9. **Default stale threshold: 90 days.** Dev artifacts not modified in 90+ days are flagged as stale. The user can override this.
10. **Confirm before bulk operations.** Never run commands like `rm -rf ~/Downloads/*` without showing item count and total size.

## Workflow

### 1. Discover & Configure

Before scanning, gather context about the system:

- Run `uname -m` to detect architecture (Apple Silicon vs Intel — determines Homebrew prefix)
- Detect the Homebrew prefix: `/opt/homebrew` (Apple Silicon) or `/usr/local` (Intel)
- Check which package managers are installed: `which brew npm pnpm yarn bun uv pip3 cargo go pyenv`
- Scan `/Applications/` for installed browsers
- Identify dev directories — check common locations: `~/developer`, `~/Developer`, `~/dev`, `~/projects`, `~/Projects`, `~/src`, `~/code`, `~/workspace`, `~/repos`
- Ask the user:
  - Are there additional dev directories to scan?
  - Should the stale threshold be something other than 90 days?

Note: The scan script's tool detection (`shutil.which()`) is authoritative — it may find tools that the shell's `which` misses due to PATH differences.

### 2. Scan

Run the scan script with the discovered configuration:

```bash
uv run .agents/skills/mac-cleanup/scripts/scan.py \
  --dev-dirs <discovered_dirs> \
  --stale-days <threshold> \
  --skip <protected_paths>
```

If `uv` is not available, fall back to `python3`.

The script runs all checks in parallel and outputs a JSON report to stdout. Read the full JSON output to understand what's on the system.

If the scan script is unavailable or fails, fall back to manual commands:

- `df -h /` — overall disk usage
- `du -sh ~/Library/Caches ~/Library/Logs ~/.cache ~/.npm ~/.Trash ~/Downloads` — quick size survey
- Check package manager caches individually (see `references/cleanup-catalog.md`)

### 3. Present Findings

Show the user a summary table grouped by category. Include:

| Category | Item | Size | Risk | Status |
|----------|------|------|------|--------|
| Package caches | Homebrew | 3.2 GB | safe | 12 stale items |
| System caches | ~/Library/Caches | 8.1 GB | moderate | Top: Xcode (4 GB) |
| Dev artifacts | node_modules (5 stale) | 2.3 GB | safe | >90 days old |
| Docker | Images + containers | 15 GB | moderate | 8 unused images |
| Trash | ~/.Trash | 1.2 GB | moderate | |
| Downloads | ~/Downloads | 4.5 GB | high | 127 items |

Sort by size (largest first). Flag risk levels:
- **safe** — always reclaimable, rebuilds automatically
- **moderate** — reclaimable but may need re-download or rebuild time
- **high** — potential data loss, needs careful review

### 4. Clean Up Interactively

Before starting, ask the user if there are paths that should be protected/skipped during cleanup.

Walk through categories from safest to riskiest. For each:

1. Show exactly what will be deleted and its size
2. Show the command that will run
3. Get user approval
4. Execute the command
5. Report space freed

Consult `references/cleanup-catalog.md` for the correct detection, cleanup command, and dry-run command for each category.

**Order of operations (safest first):**

1. Package manager caches (brew, npm, pnpm, yarn, bun, uv, pip, cargo, go)
2. System logs (`~/Library/Logs`)
3. Stale dev artifacts (node_modules, .venv, build dirs older than threshold)
4. Python bytecode caches (`__pycache__`, `.pytest_cache`, etc.)
5. Merged git branches
6. System caches (`~/Library/Caches` — per-subdirectory, with breakdown)
7. Docker (show `docker system df`, ask about aggressiveness level)
8. Homebrew — unused formulae/casks (list installed as a table with `| App | Size | Description |` using `brew info --json` for descriptions and sizes, ask which are unused)
9. Trash
10. Downloads (show largest files, never bulk-delete without review)
11. Application uninstall (if user wants — quit first, use Finder, clean support files)

**App uninstall procedure:**

1. Get bundle ID: `mdls -name kMDItemCFBundleIdentifier /Applications/AppName.app`
2. Quit the app if running
3. Move to Trash via Finder: `osascript -e 'tell application "Finder" to delete POSIX file "/Applications/AppName.app"'`
4. Clean support files in these locations (use the bundle ID):
   - `~/Library/Application Support/<AppName>`
   - `~/Library/Caches/<bundleid>`
   - `~/Library/Preferences/<bundleid>.plist`
   - `~/Library/HTTPStorages/<bundleid>`
   - `~/Library/Logs/<AppName>`
   - `~/Library/Containers/<bundleid>`
   - `~/Library/Group Containers/<bundleid>`
   - `~/Library/Saved Application State/<bundleid>.savedState`
   - `~/Library/WebKit/<bundleid>`

### 5. Report

After all cleanup actions are complete, show:

- **Before/after disk comparison:** free space before vs after
- **Actions taken:** list every action with space freed
- **Total space freed:** cumulative sum
- **Declined items:** what was skipped and why, with suggestions for future cleanup
- **Maintenance tips:** suggest scheduling periodic cleanup for categories that grow back

## Edge Cases

- **Docker not running:** Docker images/containers can use 10+ GB. Ask the user:
  "Docker is installed but not running. Want to start Docker Desktop to check for reclaimable space?"
  If yes: `open -a Docker`, wait for daemon readiness (poll `docker info` up to 30s).
  If no: flag prominently in report: "Docker skipped (not running) — restart and re-run to check."
- **No dev directories found:** Skip dev artifact scan. Ask the user if they have dev work in a non-standard location.
- **Intel Mac:** Use `/usr/local` for Homebrew prefix. All other commands work the same.
- **Command failures:** Log the error, skip that category, continue with the rest. Report all errors at the end.
- **Nothing to clean:** Report that the system is already in good shape. Show current disk usage.
- **Scan script missing:** Fall back to manual `du`/`df` commands as described in Step 2.
- **Large ML caches:** `~/.cache/huggingface` or similar can be huge. Flag these specifically and warn about re-download costs.

## Anti-Patterns

Do NOT do any of the following:

- **`rm -rf /`** or any variation targeting the root filesystem
- **Delete `.git` directories** — only clean merged branches
- **Use `sudo` by default** — only when the user explicitly requests it and for a specific reason
- **Bulk-delete `~/Library/Application Support`** — this contains critical app data. Only remove entries for apps the user has confirmed they uninstalled.
- **Run recursive finds on huge system directories** like `~/Library/Application Support` or `~/Library/Containers` — these can be enormous and slow. Only check specific subdirectories.
- **Delete Xcode derived data without warning** — it can be very large but takes time to rebuild. Always flag the size and rebuild cost.
- **Clear browser caches programmatically** — this can corrupt browser state. Always direct users to browser settings.
- **Force-prune Docker volumes** — these may contain database data. Always show volume names and get explicit approval.
