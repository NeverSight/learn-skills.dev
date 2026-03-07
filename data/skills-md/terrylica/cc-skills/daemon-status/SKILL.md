---
name: daemon-status
description: Check asciinema status - daemon, running processes, and unhandled .cast files. TRIGGERS - daemon status, check backup, chunker health, recording status, unhandled files.
allowed-tools: Bash
argument-hint: "[--verbose] [--files-only] [--processes-only]"
model: haiku
---

# /asciinema-tools:daemon-status

Check comprehensive asciinema status including daemon, running processes, and unhandled .cast files.

## Execution

### Collect Status Information

```bash
/usr/bin/env bash << 'STATUS_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"
HEALTH_FILE="$HOME/.asciinema/health.json"
LOG_FILE="$HOME/.asciinema/logs/chunker.log"
RECORDINGS_DIR="$HOME/asciinema_recordings"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  asciinema Status Overview                                     ║"
echo "╠════════════════════════════════════════════════════════════════╣"

# ========== RUNNING PROCESSES ==========
echo "║  RUNNING PROCESSES                                             ║"
echo "╠────────────────────────────────────────────────────────────────╣"

PROCS=$(ps aux | grep -E "asciinema rec" | grep -v grep)
if [[ -n "$PROCS" ]]; then
  PROC_COUNT=$(echo "$PROCS" | wc -l | tr -d ' ')
  printf "║  Active asciinema rec: %-38s ║\n" "$PROC_COUNT process(es)"
  echo "$PROCS" | while read -r line; do
    PID=$(echo "$line" | awk '{print $2}')
    # Extract .cast file path from command
    CAST_FILE=$(echo "$line" | grep -oE '[^ ]+\.cast' | head -1)
    if [[ -n "$CAST_FILE" ]]; then
      BASENAME=$(basename "$CAST_FILE")
      SIZE=$(ls -lh "$CAST_FILE" 2>/dev/null | awk '{print $5}' || echo "?")
      printf "║    PID %-6s %-35s %5s ║\n" "$PID" "${BASENAME:0:35}" "$SIZE"
    else
      printf "║    PID %-6s (no file detected)                          ║\n" "$PID"
    fi
  done
else
  echo "║  Active asciinema rec: None                                    ║"
fi

echo "╠════════════════════════════════════════════════════════════════╣"

# ========== DAEMON STATUS ==========
echo "║  CHUNKER DAEMON                                                ║"
echo "╠────────────────────────────────────────────────────────────────╣"

if [[ -f "$PLIST_PATH" ]]; then
  echo "║  Installed: Yes                                                ║"
  if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
    echo "║  Running: Yes                                                  ║"
  else
    echo "║  Running: No                                                   ║"
  fi

  if [[ -f "$HEALTH_FILE" ]]; then
    STATUS=$(jq -r '.status // "unknown"' "$HEALTH_FILE")
    LAST_PUSH=$(jq -r '.last_push // "never"' "$HEALTH_FILE")
    CHUNKS=$(jq -r '.chunks_pushed // 0' "$HEALTH_FILE")
    printf "║  Health: %-52s ║\n" "$STATUS"
    printf "║  Last push: %-49s ║\n" "$LAST_PUSH"
    printf "║  Chunks pushed: %-44s ║\n" "$CHUNKS"
  fi
else
  echo "║  Installed: No - run /asciinema-tools:daemon-setup             ║"
fi

echo "╠════════════════════════════════════════════════════════════════╣"

# ========== UNHANDLED .CAST FILES ==========
echo "║  UNHANDLED .CAST FILES (not on orphan branch)                  ║"
echo "╠────────────────────────────────────────────────────────────────╣"

# Find .cast files in common locations
UNHANDLED=()
while IFS= read -r -d '' file; do
  UNHANDLED+=("$file")
done < <(find ~/eon -name "*.cast" -size +1M -mtime -30 -print0 2>/dev/null)

# Also check tmp directories
while IFS= read -r -d '' file; do
  UNHANDLED+=("$file")
done < <(find /tmp -maxdepth 2 -name "*.cast" -size +1M -print0 2>/dev/null)

if [[ ${#UNHANDLED[@]} -gt 0 ]]; then
  printf "║  Found: %-53s ║\n" "${#UNHANDLED[@]} file(s) need attention"
  for file in "${UNHANDLED[@]:0:5}"; do
    BASENAME=$(basename "$file")
    SIZE=$(ls -lh "$file" 2>/dev/null | awk '{print $5}')
    MTIME=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || stat -c "%y" "$file" 2>/dev/null | cut -d' ' -f1)
    printf "║    %-40s %5s  %s ║\n" "${BASENAME:0:40}" "$SIZE" "$MTIME"
  done
  if [[ ${#UNHANDLED[@]} -gt 5 ]]; then
    printf "║    ... and %d more                                          ║\n" "$((${#UNHANDLED[@]} - 5))"
  fi
  echo "║                                                                ║"
  echo "║  → Run /asciinema-tools:finalize to process these files        ║"
else
  echo "║  No unhandled .cast files found                                ║"
fi

echo "╠════════════════════════════════════════════════════════════════╣"

# ========== CREDENTIALS ==========
echo "║  CREDENTIALS                                                   ║"
echo "╠────────────────────────────────────────────────────────────────╣"

if security find-generic-password -s "asciinema-github-pat" -a "$USER" -w &>/dev/null 2>&1; then
  echo "║  GitHub PAT: ✓ Configured                                      ║"
else
  echo "║  GitHub PAT: ✗ Not configured                                  ║"
fi

if security find-generic-password -s "asciinema-pushover-app" -a "$USER" -w &>/dev/null 2>&1; then
  echo "║  Pushover: ✓ Configured                                        ║"
else
  echo "║  Pushover: ○ Not configured (optional)                         ║"
fi

echo "╚════════════════════════════════════════════════════════════════╝"

# Recent log entries
if [[ -f "$LOG_FILE" ]]; then
  echo ""
  echo "Recent daemon logs:"
  echo "-------------------"
  tail -5 "$LOG_FILE"
fi
STATUS_EOF
```

## Output Example

```
╔════════════════════════════════════════════════════════════════╗
║  asciinema Status Overview                                     ║
╠════════════════════════════════════════════════════════════════╣
║  RUNNING PROCESSES                                             ║
╠────────────────────────────────────────────────────────────────╣
║  Active asciinema rec: 2 process(es)                           ║
║    PID 41749  alpha-forge-research_2025.cast            12G    ║
║    PID 49655  alpha-forge_2025-12-23.cast              4.5G    ║
╠════════════════════════════════════════════════════════════════╣
║  CHUNKER DAEMON                                                ║
╠────────────────────────────────────────────────────────────────╣
║  Installed: Yes                                                ║
║  Running: Yes                                                  ║
║  Health: ok                                                    ║
║  Last push: 2025-12-26T15:30:00Z                               ║
║  Chunks pushed: 7                                              ║
╠════════════════════════════════════════════════════════════════╣
║  UNHANDLED .CAST FILES (not on orphan branch)                  ║
╠────────────────────────────────────────────────────────────────╣
║  Found: 3 file(s) need attention                               ║
║    alpha-forge-research.cast                 12G   2025-12-30  ║
║    alpha-forge_session.cast                 4.5G   2025-12-26  ║
║    debug-session.cast                       234M   2025-12-28  ║
║                                                                ║
║  → Run /asciinema-tools:finalize to process these files        ║
╠════════════════════════════════════════════════════════════════╣
║  CREDENTIALS                                                   ║
╠────────────────────────────────────────────────────────────────╣
║  GitHub PAT: ✓ Configured                                      ║
║  Pushover: ○ Not configured (optional)                         ║
╚════════════════════════════════════════════════════════════════╝

Recent daemon logs:
-------------------
[2025-12-26 15:30:00] Pushed: chunk_20251226_153000.cast.zst
[2025-12-26 15:25:00] Idle detected (32s) for workspace_2025-12-26.cast
```

## Troubleshooting

| Issue                | Cause                         | Solution                               |
| -------------------- | ----------------------------- | -------------------------------------- |
| jq not found         | jq not installed              | `brew install jq`                      |
| No health.json       | Daemon not running            | Run `/asciinema-tools:daemon-start`    |
| GitHub PAT not found | Keychain credential missing   | Run `/asciinema-tools:daemon-setup`    |
| Many unhandled files | Orphan branch not initialized | Run `/asciinema-tools:finalize`        |
| Status hangs         | Large find operation          | Use `--processes-only` for quick check |
