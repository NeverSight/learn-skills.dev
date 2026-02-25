---
name: eve-job-debugging
description: Monitor and debug Eve jobs with CLI follow, logs, wait, and diagnose commands. Use when work is stuck, failing, or you need fast status.
---

# Eve Job Debugging

## CLI-Only Debugging

> **Debug via the Eve CLI exclusively.** This replicates the client experience — clients don't have kubectl or host access.

Every debugging capability must be available through the CLI. If you find yourself needing system tools to diagnose a job issue, that's a gap in our CLI that should be fixed.

## Monitor

- `eve job follow <id>` to stream logs.
- `eve job wait <id> --timeout 300 --json` to wait on completion.
- `eve job result <id> --format text` for the latest result.

## Diagnose

- `eve job diagnose <id>` for timeline and error summary.
- `eve job show <id> --verbose` for attempts and phase.
- `eve job dep list <id>` for dependency blocks.

## System health

- `eve system health` to confirm the API is reachable.