---
name: daemon-start
description: Start the asciinema chunker daemon. TRIGGERS - start daemon, resume chunker, enable backup.
allowed-tools: Bash
argument-hint: ""
model: haiku
disable-model-invocation: true
---

# /asciinema-tools:daemon-start

Start the asciinema chunker daemon via launchd.

## Execution

### Check if Already Running

```bash
/usr/bin/env bash << 'CHECK_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"

if ! [[ -f "$PLIST_PATH" ]]; then
  echo "ERROR: Daemon not installed. Run /asciinema-tools:daemon-setup first."
  exit 1
fi

if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
  echo "ALREADY_RUNNING"
  cat ~/.asciinema/health.json 2>/dev/null | jq -r '"Status: \(.status) | PID: \(.pid) | Last push: \(.last_push)"' || true
  exit 0
fi

echo "NOT_RUNNING"
CHECK_EOF
```

### Start Daemon

```bash
/usr/bin/env bash << 'START_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"

if launchctl load "$PLIST_PATH"; then
  echo "Daemon started"
  sleep 2

  if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
    echo ""
    echo "Status:"
    cat ~/.asciinema/health.json 2>/dev/null | jq . || echo "Waiting for health file..."
  else
    echo "WARNING: Daemon may not have started correctly. Check logs:"
    echo "  /asciinema-tools:daemon-logs"
  fi
else
  echo "ERROR: Failed to start daemon"
  exit 1
fi
START_EOF
```

## Output

On success:

```
Daemon started

Status:
{
  "status": "ok",
  "message": "Monitoring ~/.asciinema/active",
  "pid": 12345,
  ...
}
```

## Troubleshooting

| Issue                  | Cause                       | Solution                                  |
| ---------------------- | --------------------------- | ----------------------------------------- |
| Daemon not installed   | Setup not run               | Run `/asciinema-tools:daemon-setup` first |
| Failed to start daemon | Launchd configuration error | Check `launchctl error` and re-run setup  |
| Health file missing    | Daemon still initializing   | Wait 5 seconds, check `/daemon-status`    |
| Daemon keeps stopping  | Script error or credentials | Check `/asciinema-tools:daemon-logs`      |
