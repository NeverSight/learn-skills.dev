---
name: stop
description: "Disable autonomous loop mode immediately. TRIGGERS - ru stop, stop autonomous, disable loop, end autonomous mode."
allowed-tools: Bash
argument-hint: ""
model: haiku
disable-model-invocation: true
---

# RU: Stop

**EXECUTE IMMEDIATELY**: Use the Bash tool to run the following script.

```bash
/usr/bin/env bash << 'RALPH_UNIVERSAL_STOP'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "Stopping RU loop..."

# Set state to stopped
STATE_FILE="$PROJECT_DIR/.claude/ru-state.json"
if [[ -d "$PROJECT_DIR/.claude" ]]; then
    echo '{"state": "stopped"}' > "$STATE_FILE"
fi

# Create kill switch for redundancy
touch "$PROJECT_DIR/.claude/STOP_LOOP"

# Update config if exists
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"
if [[ -f "$CONFIG_FILE" ]]; then
    jq '.state = "stopped"' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

# Clean up markers
rm -f "$PROJECT_DIR/.claude/ru-start-timestamp"

# Create global stop signal
echo '{"state": "stopped", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' > "$HOME/.claude/ru-global-stop.json"

echo ""
echo "RU: STOPPED"
echo "Project: $PROJECT_DIR"
RALPH_UNIVERSAL_STOP
```

After execution, confirm the loop has been stopped.

## Troubleshooting

| Issue                   | Cause                 | Solution                             |
| ----------------------- | --------------------- | ------------------------------------ |
| Loop continues running  | Hook still active     | Wait for current iteration to finish |
| State file not created  | .claude dir missing   | Create with `mkdir -p .claude`       |
| jq error                | Config file malformed | Delete and recreate config file      |
| Permission denied       | File not writable     | Check directory permissions          |
| Global stop not working | Different project dir | Ensure CLAUDE_PROJECT_DIR is correct |
