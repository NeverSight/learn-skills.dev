---
name: keep-codex-fast-maintenance
description: Backup-first skill for inspecting, archiving, and maintaining local Codex state to keep it fast, clean, and recoverable.
triggers:
  - keep codex fast
  - codex feels slow after heavy use
  - clean up codex local state
  - archive old codex chats
  - codex maintenance plan
  - rotate codex logs
  - prune stale codex worktrees
  - inspect codex session size
---

# Keep Codex Fast

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A backup-first maintenance skill for local Codex state. When Codex starts feeling heavy after weeks of chats, terminals, logs, worktrees, and project history, this skill gives you a safe, inspectable workflow to reduce drag without losing context.

**Core rule:** Make handoffs first. Archive, don't delete. Apply changes only when you are ready.

---

## Installation

Ask Codex directly:

```text
Install the keep-codex-fast skill from https://github.com/vibeforge1111/keep-codex-fast
```

Or clone manually into your Codex skills directory:

```bash
git clone https://github.com/vibeforge1111/keep-codex-fast keep-codex-fast
```

---

## Mental Model

| Layer | Purpose |
|---|---|
| Chats | Execution context |
| Handoff docs | Memory and continuity |
| Archives | History, not deletion |
| Fresh threads | Speed |

**Never delete. Always archive.** The script moves state into archive folders and writes backup/restore artifacts before applying any change.

---

## CLI — Key Commands

All commands run from the project root. The script is read-only by default.

### 1. Inspect Only (Safe, No Writes)

```bash
python scripts/keep_codex_fast.py
```

Reports: active session size, archived session size, extended path candidates, old session candidates, worktree candidates, log size, top Node/dev processes. **Nothing is mutated.**

### 2. Detailed Report (Raw IDs, Titles, Paths)

```bash
python scripts/keep_codex_fast.py --details
```

Shows thread IDs, chat titles, file paths, and process paths. Use when you need to identify specific sessions or worktrees before archiving.

### 3. Backup Only (No Move/Archive)

```bash
python scripts/keep_codex_fast.py --backup-only
```

Creates backup artifacts of current Codex state without moving or modifying anything. Run this before any apply step as an extra safety net.

> ⚠️ Backup folders contain private local Codex metadata. Keep them on your machine. Do not publish or share without reviewing contents.

### 4. Apply Maintenance

```bash
python scripts/keep_codex_fast.py --apply --archive-older-than-days 10 --worktree-older-than-days 7
```

Archives old non-pinned sessions, moves stale worktrees, rotates large `logs_2.sqlite*` files, prunes dead/temp project references in `config.toml`, and normalizes Windows `\\?\C:\...` path mismatches in SQLite text fields.

### 5. Wait for Codex to Exit Before Applying

```bash
python scripts/keep_codex_fast.py --apply --wait-for-codex-exit
```

Holds until no Codex process is detected, then applies maintenance. Use this when you want to queue a cleanup but need Codex to close first.

---

## Workflow: Step-by-Step

### Step 1 — Inspect First

```text
Use $keep-codex-fast to inspect my Codex local state and recommend a safe maintenance plan.
```

Review the report. Note which sessions are large, which worktrees are stale, and which logs are heavy.

### Step 2 — Create Handoff Docs for Active Chats

For every active repo chat you may want to continue later, run this inside that chat:

```text
Create a comprehensive handoff document for this repo/session before I archive Codex history.

Include:
- repo/path and branch
- current goal
- what we already completed
- files touched or investigated
- commands/tests already run
- known errors, warnings, or failing checks
- open decisions
- constraints, user preferences, and do-not-touch areas
- the next 3-7 concrete steps

Also include a reactivation prompt I can paste into a fresh Codex chat so it can continue from this handoff without relying on the old chat context.

Save the handoff in a sensible repo-local place like docs/codex-handoffs/YYYY-MM-DD-topic.md unless this repo already has a better handoff location.
```

A handoff captures: what you were doing, what changed, what files matter, what commands ran, what is still broken or undecided, and what to do next.

### Step 3 — Apply Safe Maintenance

After handoffs exist for all chats you care about:

```text
Use $keep-codex-fast to apply safe Codex maintenance.

Before changing anything, confirm that important active repo chats have handoff docs or do not need them.

Then back up first, archive instead of deleting, move stale worktrees, rotate large logs, prune dead config references, and verify the result.

If Codex is currently running, do not mutate local state. Tell me to close Codex first.
```

---

## What the Script Can Change

| Target | Action |
|---|---|
| Old non-pinned active sessions | Archived, not deleted |
| Stale worktrees | Moved out of hot path |
| Large `logs_2.sqlite*` files | Rotated |
| Dead/temp project entries in `config.toml` | Pruned |
| Windows `\\?\C:\...` path mismatches in SQLite | Normalized |

---

## Recurring Maintenance Reminder

Set up a weekly or biweekly reminder that **reports only** — never auto-applies:

```text
Use $keep-codex-fast to create a recurring Codex maintenance reminder.

Schedule it weekly if I use Codex heavily, or biweekly if that seems safer.

The reminder should:
- run the keep-codex-fast report first
- never pass --apply or run mutating maintenance automatically
- never archive, move, prune, rotate, normalize, delete, or mutate local Codex state
- remind me to create comprehensive handoff docs and reactivation prompts for active repo chats before any manual apply
- summarize active session size, archived session size, extended path candidates, old session candidates, worktree candidates, log size, and top Node/dev processes
- report heavy Node/dev processes without killing them
- tell me that manual apply should only happen after I confirm handoffs exist or are not needed and Codex is closed
```

---

## Python Integration Examples

### Check What Would Be Archived (Dry Run Pattern)

```python
import subprocess
import json

result = subprocess.run(
    ["python", "scripts/keep_codex_fast.py", "--details"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

### Trigger Backup Before Any Deploy/Migration Script

```python
import subprocess
import sys

def backup_codex_state():
    """Run before any operation that might affect Codex local state."""
    result = subprocess.run(
        ["python", "scripts/keep_codex_fast.py", "--backup-only"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[warn] Codex backup step reported issues:\n{result.stderr}")
    else:
        print("[ok] Codex state backed up.")
    return result.returncode

if __name__ == "__main__":
    sys.exit(backup_codex_state())
```

### Apply With Age Thresholds From Environment Variables

```python
import subprocess
import os

archive_days = os.environ.get("CODEX_ARCHIVE_DAYS", "14")
worktree_days = os.environ.get("CODEX_WORKTREE_DAYS", "7")

subprocess.run([
    "python", "scripts/keep_codex_fast.py",
    "--apply",
    "--archive-older-than-days", archive_days,
    "--worktree-older-than-days", worktree_days,
    "--wait-for-codex-exit",
], check=True)
```

### Wrap in a Simple Maintenance CLI

```python
#!/usr/bin/env python3
"""
maintenance.py — thin wrapper around keep_codex_fast.py for project-local use.
"""
import argparse
import subprocess
import sys

SCRIPT = "scripts/keep_codex_fast.py"

def main():
    parser = argparse.ArgumentParser(description="Codex maintenance wrapper")
    parser.add_argument("--inspect", action="store_true", help="Report only, no writes")
    parser.add_argument("--backup", action="store_true", help="Backup only, no moves")
    parser.add_argument("--apply", action="store_true", help="Apply full maintenance")
    parser.add_argument("--archive-days", type=int, default=10)
    parser.add_argument("--worktree-days", type=int, default=7)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()

    cmd = ["python", SCRIPT]

    if args.details:
        cmd.append("--details")

    if args.backup:
        cmd.append("--backup-only")
    elif args.apply:
        cmd += [
            "--apply",
            "--archive-older-than-days", str(args.archive_days),
            "--worktree-older-than-days", str(args.worktree_days),
            "--wait-for-codex-exit",
        ]
    # default: inspect only (no extra flags needed)

    result = subprocess.run(cmd, text=True)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### Script reports nothing unusual but Codex still feels slow

Run with `--details` to see raw thread IDs and process paths:

```bash
python scripts/keep_codex_fast.py --details
```

Check for heavy Node/dev processes listed in the report. The script reports them but does not kill them — review manually.

### Apply step completes but state still seems large

The apply step archives, not deletes. Check your Codex archive folder — archived sessions accumulate there over time. Periodically review the archive folder and remove old entries you no longer need.

### Windows path mismatches (`\\?\C:\...`) appearing in reports

This is a known SQLite text field issue on Windows. The `--apply` step normalizes these automatically. Run:

```bash
python scripts/keep_codex_fast.py --apply --archive-older-than-days 10 --worktree-older-than-days 7
```

### Backup folder is unexpectedly large

Backup folders snapshot Codex local metadata. If you run `--backup-only` repeatedly, old backups accumulate. Prune old backup snapshots manually — check timestamps in the backup folder and remove those older than your retention window.

### `--wait-for-codex-exit` hangs indefinitely

Codex may still be running in the background. Check for Codex processes:

```bash
# macOS/Linux
ps aux | grep -i codex

# Windows PowerShell
Get-Process | Where-Object { $_.Name -like "*codex*" }
```

Close Codex fully, then re-run the apply step.

### Pinned sessions being incorrectly flagged as archive candidates

The script should not archive pinned sessions. If you see pinned sessions in the candidate list, run inspect-only first (`--details`) and confirm before applying. Do not pass `--apply` until you have verified the candidate list.

---

## Safety Guarantees

- **Default is read-only.** No files are written, moved, or changed unless you explicitly pass `--apply` or `--backup-only`.
- **Archive, never delete.** Sessions, worktrees, and logs are moved to archive folders, not removed.
- **Backup before apply.** The script writes backup/restore artifacts before making any change.
- **Codex-running guard.** Use `--wait-for-codex-exit` or close Codex manually before applying to avoid mutating state while Codex holds file locks.
- **Reminder automation never auto-applies.** The recurring reminder prompt is explicitly scoped to report-only. It never passes `--apply`.
