---
name: crnd
description: Schedule and manage cron jobs, one-time scheduled tasks, and recurring jobs using the crnd CLI. Use when the user wants to set up cronjobs, scheduled jobs, one-time tasks, recurring/repetitive jobs, automate tasks at specific times, or manage background processes. Triggers include requests like "run this every day at 2am", "schedule a backup", "set up a recurring task", "run this once tomorrow", or "create a cron job".
---

# crnd

Local cron daemon with text-first output, no prompts, real OS processes. Use `--json` for machine-readable output.

## Installation

```sh
bunx crnd
# or
brew install ysm-dev/crnd/crnd
```

## Quick Reference

| Task                           | Command                                               |
| ------------------------------ | ----------------------------------------------------- |
| Create cron job                | `crnd schedule -n NAME -s "CRON" -- command args`     |
| Create one-time job (relative) | `crnd schedule -n NAME -i DURATION -- command`        |
| Create one-time job (absolute) | `crnd schedule -n NAME -a "ISO_TIMESTAMP" -- command` |
| List all jobs                  | `crnd list`                                           |
| Job status                     | `crnd status -n NAME`                                 |
| Run immediately                | `crnd run-once -n NAME`                               |
| View logs                      | `crnd logs -n NAME`                                   |
| Stream logs                    | `crnd logs -n NAME -s`                                |
| Pause job                      | `crnd pause -n NAME`                                  |
| Resume job                     | `crnd resume -n NAME`                                 |
| Stop gracefully                | `crnd stop -n NAME`                                   |
| Kill immediately               | `crnd kill -n NAME`                                   |
| Delete job                     | `crnd delete -n NAME -f`                              |
| Run history                    | `crnd runs -n NAME`                                   |
| Check setup                    | `crnd doctor`                                         |

All commands default to text output; use `--json` for machine-readable output.

## Scheduling Jobs

### Cron Jobs (Recurring)

```sh
# Daily at 2am UTC
crnd schedule -n backup -s "0 2 * * *" -- rsync -a ~/docs ~/backup

# Every hour
crnd schedule -n healthcheck -s "0 * * * *" -- curl http://localhost:8080/health

# Weekdays at 9am in specific timezone
crnd schedule -n standup-reminder -s "0 9 * * 1-5" -z "America/New_York" -- notify "Standup in 15 minutes"

# Every 5 minutes
crnd schedule -n monitor -s "*/5 * * * *" -- ./check-system.sh
```

### One-Time Jobs (Relative Time)

```sh
# Run in 10 minutes
crnd schedule -n reminder -i 10m -- say "Time to stretch!"

# Run in 2 hours
crnd schedule -n deploy -i 2h -- ./deploy.sh

# Run tomorrow (24 hours from now)
crnd schedule -n backup -i 1d -- rsync -a ~/docs ~/backup
```

Relative time formats: `30s`, `5m`, `2h`, `1d`, `1w`, `1y`

### One-Time Jobs (Absolute Time)

```sh
# Run at specific time
crnd schedule -n deploy -a "2026-02-01T10:00:00Z" -- ./deploy.sh

# Future reminder with timezone offset
crnd schedule -n reminder -a "2026-03-15T14:30:00-05:00" -- notify "Meeting starts now"
```

### Natural Language to Flags

| User says           | Flag | Example value           |
| ------------------- | ---- | ----------------------- |
| "in 5 minutes"      | `-i` | `5m`                    |
| "in 2 hours"        | `-i` | `2h`                    |
| "tomorrow"          | `-i` | `1d`                    |
| "in a week"         | `-i` | `1w`                    |
| "tomorrow at 9am"   | `-a` | `"2026-02-04T09:00:00"` |
| "every day at 8am"  | `-s` | `"0 8 * * *"`           |
| "weekdays at 9am"   | `-s` | `"0 9 * * 1-5"`         |
| "every Monday 10am" | `-s` | `"0 10 * * 1"`          |
| "every hour"        | `-s` | `"0 * * * *"`           |

### Cron Expression Format

5-field standard: `minute hour day-of-month month day-of-week`

| Field        | Values      | Special         |
| ------------ | ----------- | --------------- |
| Minute       | 0-59        | `*` `/` `,` `-` |
| Hour         | 0-23        | `*` `/` `,` `-` |
| Day of Month | 1-31        | `*` `/` `,` `-` |
| Month        | 1-12        | `*` `/` `,` `-` |
| Day of Week  | 0-6 (Sun=0) | `*` `/` `,` `-` |

Common patterns:

- `0 * * * *` - every hour
- `*/15 * * * *` - every 15 minutes
- `0 2 * * *` - daily at 2am
- `0 0 * * 0` - weekly on Sunday midnight
- `0 9 * * 1-5` - weekdays at 9am
- `0 0 1 * *` - monthly on the 1st

## Managing Jobs

### Monitoring

```sh
# List all jobs
crnd list
crnd list --json

# Job details
crnd status -n backup

# Run history
crnd runs -n backup

# View latest logs
crnd logs -n backup

# Stream logs in real-time
crnd logs -n backup -s

# Tail recent logs
crnd logs -n backup -t
```

### Control

```sh
# Trigger immediate run
crnd run-once -n backup

# Pause scheduling (job won't run until resumed)
crnd pause -n backup

# Resume scheduling
crnd resume -n backup

# Stop running process gracefully (SIGTERM)
crnd stop -n backup

# Kill running process immediately (SIGKILL)
crnd kill -n backup

# Delete job entirely
crnd delete -n backup -f
```

### Import/Export

```sh
# Export all jobs to TOML
crnd export > jobs.toml

# Import jobs from file
crnd import -f jobs.toml
```

## Daemon Management

```sh
# Start daemon
crnd daemon start

# Stop daemon
crnd daemon stop

# Daemon status
crnd daemon status

# Install autostart (runs on login)
crnd daemon install

# Uninstall autostart
crnd daemon uninstall

# Check setup
crnd doctor
```

## jobs.toml Format

Jobs are stored in `~/.config/crnd/jobs.toml` (Linux/macOS) or `%APPDATA%\crnd\jobs.toml` (Windows). Edit directly; daemon watches for changes.

```toml
[jobs.backup]
command = ["rsync", "-a", "/src", "/dst"]
schedule = "0 2 * * *"
timezone = "UTC"
timeout_ms = 600000

[jobs.deploy]
command = ["./deploy.sh"]
run_at = "2026-02-01T10:00:00Z"
```

## Common Workflows

### Set up a daily backup

```sh
crnd daemon start
crnd schedule -n daily-backup -s "0 3 * * *" -z "UTC" -- rsync -av ~/important ~/backup
crnd run-once -n daily-backup  # test it works
crnd daemon install  # autostart on login
```

### Schedule a one-time deployment

```sh
crnd schedule -n prod-deploy -a "2026-02-15T02:00:00Z" -- ./deploy.sh production
crnd status -n prod-deploy  # verify scheduled time
```

### Monitor a recurring job

```sh
crnd runs -n backup  # check run history
crnd logs -n backup  # view latest output
crnd status -n backup  # see next scheduled run
```

### Pause during maintenance

```sh
crnd pause -n backup
# ... do maintenance ...
crnd resume -n backup
```
