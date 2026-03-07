---
name: daemon-logs
description: View asciinema chunker daemon logs. TRIGGERS - daemon logs, chunker logs, backup logs.
allowed-tools: Bash
argument-hint: "[-n lines] [--follow] [--errors]"
model: haiku
---

# /asciinema-tools:daemon-logs

View logs from the asciinema chunker daemon.

## Arguments

| Argument   | Description                        |
| ---------- | ---------------------------------- |
| `-n N`     | Show last N lines (default: 50)    |
| `--follow` | Follow log output (like `tail -f`) |
| `--errors` | Show only ERROR lines              |

## Execution

### Default: Show Recent Logs

```bash
/usr/bin/env bash << 'LOGS_EOF'
LOG_FILE="$HOME/.asciinema/logs/chunker.log"
LAUNCHD_STDOUT="$HOME/.asciinema/logs/launchd-stdout.log"
LAUNCHD_STDERR="$HOME/.asciinema/logs/launchd-stderr.log"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "No daemon logs found."
  echo ""
  echo "Log locations:"
  echo "  Daemon log: $LOG_FILE"
  echo "  launchd stdout: $LAUNCHD_STDOUT"
  echo "  launchd stderr: $LAUNCHD_STDERR"
  exit 0
fi

echo "=== Daemon Log (last 50 lines) ==="
echo "File: $LOG_FILE"
echo ""
tail -50 "$LOG_FILE"
LOGS_EOF
```

### With --follow: Stream Logs

```bash
/usr/bin/env bash << 'FOLLOW_EOF'
LOG_FILE="$HOME/.asciinema/logs/chunker.log"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "No daemon logs found. Start the daemon first."
  exit 1
fi

echo "=== Following Daemon Log (Ctrl+C to stop) ==="
echo "File: $LOG_FILE"
echo ""
tail -f "$LOG_FILE"
FOLLOW_EOF
```

### With --errors: Show Only Errors

```bash
/usr/bin/env bash << 'ERRORS_EOF'
LOG_FILE="$HOME/.asciinema/logs/chunker.log"

if [[ ! -f "$LOG_FILE" ]]; then
  echo "No daemon logs found."
  exit 0
fi

echo "=== Error Log Entries ==="
echo ""
grep -E "ERROR|WARN|FAIL" "$LOG_FILE" | tail -30 || echo "(no errors found)"
ERRORS_EOF
```

## Log Format

```
[2025-12-26 15:30:00] === Daemon started (PID: 12345) ===
[2025-12-26 15:30:00] Config: idle=30s, zstd=3, active_dir=/Users/user/.asciinema/active
[2025-12-26 15:30:00] Credentials loaded (Pushover: enabled)
[2025-12-26 15:30:00] SSH caches cleared
[2025-12-26 15:30:02] Idle detected (35s) for workspace_2025-12-26.cast, creating chunk...
[2025-12-26 15:30:03] Pushed: chunk_20251226_153002.cast.zst to https://github.com/...
```

## Additional Log Files

| File                                   | Content         |
| -------------------------------------- | --------------- |
| `~/.asciinema/logs/chunker.log`        | Main daemon log |
| `~/.asciinema/logs/launchd-stdout.log` | launchd stdout  |
| `~/.asciinema/logs/launchd-stderr.log` | launchd stderr  |

## Examples

```bash
# View recent logs
/asciinema-tools:daemon-logs

# Follow logs in real-time
/asciinema-tools:daemon-logs --follow

# Show only errors
/asciinema-tools:daemon-logs --errors
```

## Troubleshooting

| Issue             | Cause                | Solution                            |
| ----------------- | -------------------- | ----------------------------------- |
| No logs found     | Daemon never started | Run `/asciinema-tools:daemon-start` |
| Empty log file    | Daemon just started  | Wait a few seconds, check again     |
| Logs not updating | Daemon crashed       | Check `/daemon-status`, restart     |
| Permission denied | Wrong file owner     | Check `ls -la ~/.asciinema/logs/`   |
