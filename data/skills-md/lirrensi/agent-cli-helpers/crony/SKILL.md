---
name: crony
description: >
  Manage cron jobs with natural language scheduling. Use this skill when the user wants
  to schedule tasks to run later or recurring, manage scheduled jobs, view job logs,
  or run jobs on-demand. Supports both one-off and recurring schedules with natural
  language syntax like "in 5m", "every 1h", "every monday".
---

# Crony Skill

Manage cron jobs with natural language scheduling and inspect computed upcoming run times.

## Installation Check

```bash
crony --help
```

If not installed:
```bash
uv tool install agentcli-helpers
```

## Usage

### Add a Job
```bash
crony add <name> <schedule> <command>
```

### List Jobs
```bash
crony list
crony list --sync
crony list --json
```

`crony list` shows a `Next Run` column for one-off and recurring jobs. `crony list --json` includes a computed `next_run` field for each job.

### Remove Job
```bash
crony rm <name>
```

### Run Job Now
```bash
crony run <name>
```

### View Logs
```bash
crony logs <name>
```

## Schedule Formats

### One-off Jobs
```bash
crony add backup "in 5m" "python --version"
crony add report "at 15:30" "python send_report.py"
crony add deploy "on 2026-03-10" "python deploy.py"
```

### Recurring Jobs
```bash
crony add ping "every 1h" "python --version"
crony add cleanup "every 24h" "python cleanup.py"
crony add weekly "every monday" "python weekly_report.py"
crony add weekday "every weekday" "python daily_check.py"
```

### Interval Syntax
- `in 5m`, `in 1h`, `in 2d` - Relative one-off
- `at 15:30`, `at "2026-03-10 10:00"` - Absolute one-off
- `every 1h`, `every 30m`, `every 24h` - Interval recurring
- `every monday`, `every weekday`, `every weekend` - Day-based recurring

## Examples

```bash
# Health check every hour
crony add health "every 1h" "python --version"

# Daily backup
crony add backup "every 24h" "python backup.py"

# Weekly report
crony add report "every friday" "python generate_report.py"

# One-time reminder
crony add remind "in 30m" "python --version"

# Inspect upcoming run times
crony list
crony list --json
```

## Platform Support

Jobs are registered with the native OS scheduler:
- **Linux/macOS**: Uses `crontab`
- **Windows**: Uses Task Scheduler

Job metadata is stored in `~/.crony/jobs.json` for easy management.
