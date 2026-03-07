---
name: daemon-stop
description: Stop the asciinema chunker daemon. TRIGGERS - stop daemon, pause chunker, disable backup.
allowed-tools: Bash
argument-hint: ""
model: haiku
disable-model-invocation: true
---

# /asciinema-tools:daemon-stop

Stop the asciinema chunker daemon via launchd.

## Execution

### Check if Running

```bash
/usr/bin/env bash << 'CHECK_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"

if ! [[ -f "$PLIST_PATH" ]]; then
  echo "Daemon not installed."
  exit 0
fi

if ! launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
  echo "Daemon not running."
  exit 0
fi

echo "RUNNING"
CHECK_EOF
```

### Stop Daemon

```bash
/usr/bin/env bash << 'STOP_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"

if launchctl unload "$PLIST_PATH"; then
  echo "Daemon stopped"

  # Verify
  sleep 1
  if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
    echo "WARNING: Daemon may still be running"
  else
    echo "Confirmed: Daemon is no longer running"
  fi
else
  echo "ERROR: Failed to stop daemon"
  exit 1
fi
STOP_EOF
```

## Output

On success:

```
Daemon stopped
Confirmed: Daemon is no longer running
```

## Notes

- Stopping the daemon does NOT delete credentials from Keychain
- To restart: `/asciinema-tools:daemon-start`
- The daemon will NOT auto-start on next login until started again

## Troubleshooting

| Issue                   | Cause                    | Solution                                         |
| ----------------------- | ------------------------ | ------------------------------------------------ |
| Failed to stop daemon   | Launchd error            | Try `launchctl unload -F <plist-path>`           |
| Daemon still running    | Multiple instances       | Kill manually: `pkill -f asciinema-chunker`      |
| Can't find plist        | Setup not run            | Run `/asciinema-tools:daemon-setup` first        |
| Recordings not stopping | asciinema rec is running | Exit recording shell first (Ctrl-D or type exit) |
