---
name: status
description: "Show current loop state. TRIGGERS - ru status, loop status, autonomous status, check ru state."
allowed-tools: Bash
argument-hint: ""
model: haiku
---

# RU: Status

```bash
/usr/bin/env bash << 'RALPH_UNIVERSAL_STATUS'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "========================================"
echo "  RALPH UNIVERSAL STATUS"
echo "========================================"
echo ""

STATE_FILE="$PROJECT_DIR/.claude/ru-state.json"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"

if [[ ! -f "$STATE_FILE" ]]; then
    echo "State: NOT STARTED"
    echo "       Run /ru:start to begin"
    exit 0
fi

STATE=$(jq -r '.state // "unknown"' "$STATE_FILE" 2>/dev/null || echo "unknown")
echo "State: $STATE"
echo "Project: $PROJECT_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
    echo ""
    echo "Configuration:"
    jq -r '.loop_limits | "  Time: \(.min_hours)h - \(.max_hours)h\n  Iterations: \(.min_iterations) - \(.max_iterations)"' "$CONFIG_FILE" 2>/dev/null || echo "  (unable to read config)"
fi

if [[ -f "$PROJECT_DIR/.claude/ru-start-timestamp" ]]; then
    START_TS=$(cat "$PROJECT_DIR/.claude/ru-start-timestamp")
    NOW_TS=$(date +%s)
    ELAPSED_SECS=$((NOW_TS - START_TS))
    ELAPSED_MINS=$((ELAPSED_SECS / 60))
    echo ""
    echo "Elapsed: ${ELAPSED_MINS} minutes"
fi
RALPH_UNIVERSAL_STATUS
```

## Examples

```bash
# Check if loop is running
/ru:status

# Quick check from terminal
cat .claude/ru-state.json 2>/dev/null | jq -r '.state' || echo "not started"
```

## Troubleshooting

| Issue            | Cause                  | Solution                          |
| ---------------- | ---------------------- | --------------------------------- |
| NOT STARTED      | Loop never initialized | Run `/ru:start`                   |
| State: unknown   | Corrupted state file   | Delete `.claude/ru-state.json`    |
| No configuration | Config file missing    | Run `/ru:wizard` for guided setup |
| jq not found     | jq not installed       | `brew install jq`                 |
