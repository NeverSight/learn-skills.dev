---
name: config
description: "View or modify loop configuration. TRIGGERS - ru config, loop settings, show config, ru configuration."
allowed-tools: Bash
argument-hint: "[show|reset|set <key>=<value>]"
model: haiku
---

# RU: Config

View or modify the loop configuration.

## Arguments

- `show` (default): Display current configuration
- `reset`: Reset to defaults (removes project config)
- `set <key>=<value>`: Set a specific config value

## Execution

```bash
/usr/bin/env bash << 'RU_CONFIG_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"
STATE_FILE="$PROJECT_DIR/.claude/ru-state.json"
ARGS="${ARGUMENTS:-show}"

case "$ARGS" in
    "show"|"")
        echo "=== RU Configuration ==="
        echo ""
        echo "--- State ---"
        if [[ -f "$STATE_FILE" ]]; then
            echo "State: $(jq -r '.state // "stopped"' "$STATE_FILE")"
        else
            echo "State: stopped (no state file)"
        fi
        echo ""
        echo "--- Config ---"
        if [[ -f "$CONFIG_FILE" ]]; then
            cat "$CONFIG_FILE" | python3 -m json.tool
        else
            echo "(using defaults - no project config)"
        fi
        ;;
    "reset")
        rm -f "$CONFIG_FILE" "$STATE_FILE"
        echo "Config reset to defaults."
        ;;
    set\ *)
        KEY_VALUE="${ARGS#set }"
        KEY=$(echo "$KEY_VALUE" | cut -d= -f1)
        VALUE=$(echo "$KEY_VALUE" | cut -d= -f2-)

        if [[ -z "$KEY" || -z "$VALUE" ]]; then
            echo "Usage: /ru:config set <key>=<value>"
            exit 1
        fi

        if [[ ! -f "$CONFIG_FILE" ]]; then
            echo '{}' > "$CONFIG_FILE"
        fi

        JQ_PATH=".$KEY"
        if [[ "$VALUE" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            jq "$JQ_PATH = $VALUE" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        elif [[ "$VALUE" == "true" || "$VALUE" == "false" ]]; then
            jq "$JQ_PATH = $VALUE" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        else
            jq "$JQ_PATH = \"$VALUE\"" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        fi
        echo "Set $KEY = $VALUE"
        ;;
    *)
        echo "Usage: /ru:config [show|reset|set <key>=<value>]"
        ;;
esac
RU_CONFIG_SCRIPT
```

Run the bash script above to manage configuration.

## Troubleshooting

| Issue                 | Cause                   | Solution                                |
| --------------------- | ----------------------- | --------------------------------------- |
| Config file not found | .claude dir missing     | Create with `mkdir -p .claude`          |
| jq error on set       | Invalid value syntax    | Check value type (number, string, bool) |
| python3 not found     | python3 not in PATH     | Install Python 3 or use `jq .` instead  |
| Reset removes state   | Intentional behavior    | State file is also removed on reset     |
| Changes not applying  | Using wrong config file | Check PROJECT_DIR matches your cwd      |
