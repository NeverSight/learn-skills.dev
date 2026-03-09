---
name: ci-monitor
description: Monitor GitHub Actions CI/CD runs after pushing. Auto-load after any `jj git push` or `git push` command. Also use when checking CI status or watching a pipeline. Auto-detects branch, deduplicates monitors, reports pass/fail with failed logs.
---

# CI Monitor

Watch GitHub Actions CI runs after a push. Auto-detects repo and branch, deduplicates concurrent monitors, reports results.

## Usage

Run the script in the background after pushing:

```bash
uv run ~/.claude/skills/ci-monitor/ci-monitor.py
```

With explicit branch:

```bash
uv run ~/.claude/skills/ci-monitor/ci-monitor.py --branch my-feature
```

## How to Invoke from Claude

After a push, run as a background Bash command:

```bash
uv run ~/.claude/skills/ci-monitor/ci-monitor.py --branch <branch-name>
```

Use `run_in_background: true` so it doesn't block the conversation. Tell the user: "CI monitor running in background — you'll be notified when it completes."

## Features

- **Auto-detects branch**: jj bookmarks first, falls back to git
- **Deduplicates**: sentinel file at `/tmp/{repo}-ci-monitor` prevents double-watching
- **Polls for run**: waits up to 60s for a CI run to appear on the branch
- **Watches until done**: uses `gh run watch --exit-status`
- **Reports failure logs**: on failure, fetches `gh run view --log-failed` (last 3000 chars)
- **Cleans up**: always removes sentinel, even on error

## Exit Codes

- `0` — CI passed (or no run found)
- `1` — CI failed (logs printed)

## Requirements

- `gh` CLI authenticated
- GitHub Actions workflows in the repo
