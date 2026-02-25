---
name: grove-doctor
description: Use when something in the Grove setup is not working as expected, or when a user asks to diagnose or troubleshoot their Grove installation
---

I'm using the grove-doctor skill to run a series of diagnostic checks on this Grove setup.

## Workflow

Run each check in order. Collect all results and print the full report at the end.

### Check 1: Platform

```bash
diskutil info / | grep "File System"
```

- PASS if output contains `APFS`
- WARN if macOS but not APFS
- FAIL if not macOS

### Check 2: CLI installed

```bash
command -v grove
```

- PASS if a path is returned
- FAIL if the command is not found. Fix: follow the installation instructions at https://github.com/chrisbanes/grove

### Check 3: CLI version

```bash
grove version
```

- PASS — record the version string for the report
- FAIL if the command errors. Fix: reinstall the CLI

### Check 4: Grove initialized

```bash
test -f .grove/config.json
```

- PASS if the file exists
- FAIL if not found. Fix: run the `grove:grove-config` skill to initialize Grove in this repository

### Check 5: Golden copy health

```bash
git status --porcelain
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
```

- PASS if `git status --porcelain` produces no output (clean)
- WARN if there are uncommitted changes — report the count of dirty files. Suggestion: commit or stash changes before creating workspaces
- Record branch name and short commit hash in the report regardless

### Check 6: Workspace directory

Read `workspaceDir` from `.grove/config.json`. Then:

```bash
test -d <workspaceDir> && test -w <workspaceDir>
df -h <workspaceDir>
```

- PASS if the directory exists, is writable, and has available disk space
- WARN if free space is under 5 GB
- FAIL if the directory does not exist or is not writable. Fix: `mkdir -p <workspaceDir>` or adjust permissions

### Check 7: Hooks

```bash
test -x .grove/hooks/post-clone
```

- PASS if the file exists and is executable
- FAIL if missing or not executable. Fix: `chmod +x .grove/hooks/post-clone`

### Check 8: Active workspaces

```bash
grove list --json
```

- PASS — report the count of active workspaces
- Flag any workspaces whose `created_at` is more than 7 days ago as potentially stale
- FAIL if the command errors

## Output Format

After all checks, print the report:

```
Grove Doctor Report:
  [PASS] Platform: macOS (APFS)
  [PASS] CLI: grove v0.1.0
  [PASS] Initialized: .grove/config.json found
  [WARN] Golden copy: 3 uncommitted changes
  [PASS] Workspace dir: /tmp/grove/myproject (12GB free)
  [FAIL] Hooks: .grove/hooks/post-clone not executable
         Fix: chmod +x .grove/hooks/post-clone
  [PASS] Workspaces: 2 active
```

For every FAIL, include a Fix line with a specific command or actionable suggestion. For every WARN, include a Suggestion line.

## Quick Reference

| Check | Command |
|---|---|
| Platform | `diskutil info / | grep "File System"` |
| CLI installed | `command -v grove` |
| CLI version | `grove version` |
| Initialized | `test -f .grove/config.json` |
| Golden copy | `git status --porcelain` |
| Workspace dir | `df -h <workspaceDir>` |
| Hooks | `test -x .grove/hooks/post-clone` |
| Workspaces | `grove list --json` |

## Common Mistakes

- **Running grove-doctor outside a git repo** — checks 4 and 5 will produce misleading results. Always run from the repository root.
- **Reporting only failures** — always print the full checklist including PASSes so the user can see what is healthy.
- **Skipping the fix command** — every FAIL must include a concrete remediation step, not just a description of the problem.

## Red Flags

- Multiple FAILs starting from Check 2 — the CLI is not installed; later checks are meaningless. Stop early and fix the CLI first.
- Golden copy is on a detached HEAD — workspaces created from it will have no branch context.
- Workspace directory is on a non-APFS volume — CoW clones will not work; Grove requires APFS.

## Integration

- **Standalone** — invoked manually when things go wrong; not called by other skills automatically
