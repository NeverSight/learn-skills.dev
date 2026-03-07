---
name: audit-now
description: "Force immediate validation round. TRIGGERS - ru audit, force validation, audit now, run audit."
allowed-tools: Bash
argument-hint: "[round-number 1-5]"
model: haiku
---

# RU: Audit Now

Force the loop to enter validation mode on the next iteration.

## Usage

- `/ru:audit-now` - Start validation from round 1
- `/ru:audit-now 4` - Start from round 4 (Adversarial Probing)

## Execution

```bash
/usr/bin/env bash << 'RU_AUDIT_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"
STATE_FILE="$PROJECT_DIR/.claude/ru-state.json"
ROUND="${ARGUMENTS:-1}"

# Validate round number
if ! [[ "$ROUND" =~ ^[1-5]$ ]]; then
    echo "Error: Round must be 1-5"
    echo ""
    echo "Validation Rounds:"
    echo "  1: Critical Issues"
    echo "  2: Verification"
    echo "  3: Documentation"
    echo "  4: Adversarial Probing"
    echo "  5: Cross-Period Robustness"
    exit 1
fi

# Ensure config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo '{}' > "$CONFIG_FILE"
fi

# Check if loop is running
CURRENT_STATE="stopped"
if [[ -f "$STATE_FILE" ]]; then
    CURRENT_STATE=$(jq -r '.state // "stopped"' "$STATE_FILE" 2>/dev/null || echo "stopped")
fi

if [[ "$CURRENT_STATE" != "running" ]]; then
    echo "Warning: Loop not running (state: $CURRENT_STATE)"
fi

# Set force validation flag
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq --argjson round "$ROUND" --arg ts "$TIMESTAMP" \
    '.force_validation = {enabled: true, round: $round, timestamp: $ts}' \
    "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

echo "Force validation enabled - starting round $ROUND on next iteration"
RU_AUDIT_SCRIPT
```

Run the bash script above to force validation mode.

## Troubleshooting

| Issue                   | Cause                 | Solution                         |
| ----------------------- | --------------------- | -------------------------------- |
| Round must be 1-5       | Invalid round number  | Use a number between 1 and 5     |
| Loop not running        | RU not started        | Run `/ru:start` first            |
| Config file not found   | .claude dir missing   | Create with `mkdir -p .claude`   |
| Validation not starting | Config not read yet   | Wait for next iteration to apply |
| jq error                | Config file malformed | Run `/ru:config reset`           |
