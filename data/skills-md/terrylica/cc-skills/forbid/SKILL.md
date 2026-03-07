---
name: forbid
description: "Add item to forbidden list (blocks work on matching topics). TRIGGERS - ru forbid, block topic, add forbidden, prevent work."
allowed-tools: Bash, AskUserQuestion
argument-hint: "<phrase> | --list | --clear | --remove"
model: haiku
---

# RU: Forbid

Add items to the forbidden list during an active loop session.
Forbidden items are blocked from opportunity discovery.

**Runtime configurable**: Works with or without active loop. Changes apply on next iteration.

## Usage

- `/ru:forbid documentation updates` - Add "documentation updates" to forbidden list
- `/ru:forbid --list` - Show current forbidden items
- `/ru:forbid --clear` - Clear all forbidden items
- `/ru:forbid --remove <phrase>` - Remove item matching phrase (fuzzy)

## Execution

```bash
/usr/bin/env bash << 'RALPH_FORBID_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"

# Get arguments
ARGS="${ARGUMENTS:-}"

# Ensure config file exists with guidance structure
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo '{"guidance": {"forbidden": [], "encouraged": []}}' > "$CONFIG_FILE"
fi

# Ensure guidance structure exists
if ! jq -e '.guidance' "$CONFIG_FILE" >/dev/null 2>&1; then
    jq '. + {guidance: {forbidden: [], encouraged: []}}' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

# Handle commands
case "$ARGS" in
    "--list"|"-l")
        echo "Current forbidden items:"
        jq -r '.guidance.forbidden[]?' "$CONFIG_FILE" | while read -r item; do
            echo "  ✗ $item"
        done
        COUNT=$(jq -r '.guidance.forbidden | length' "$CONFIG_FILE")
        echo ""
        echo "Total: $COUNT items"
        ;;
    "--clear"|"-c")
        jq '.guidance.forbidden = []' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo "Cleared all forbidden items"
        ;;
    --remove\ *)
        PHRASE="${ARGS#--remove }"
        MATCH=$(jq -r --arg phrase "$PHRASE" \
            '.guidance.forbidden[] | select(. | ascii_downcase | contains($phrase | ascii_downcase))' \
            "$CONFIG_FILE" | head -1)
        if [[ -z "$MATCH" ]]; then
            echo "No forbidden item matches: $PHRASE"
            exit 1
        fi
        TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        jq --arg match "$MATCH" --arg ts "$TS" \
            '.guidance.forbidden |= map(select(. != $match)) | .guidance.timestamp = $ts' \
            "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo "Removed from forbidden list: $MATCH"
        ;;
    "")
        echo "Usage: /ru:forbid <phrase> | --list | --clear | --remove <phrase>"
        echo ""
        echo "Current forbidden items:"
        jq -r '.guidance.forbidden[]?' "$CONFIG_FILE" | while read -r item; do
            echo "  ✗ $item"
        done
        ;;
    *)
        TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        jq --arg item "$ARGS" --arg ts "$TS" \
            '.guidance.forbidden = ((.guidance.forbidden // []) + [$item] | unique) | .guidance.timestamp = $ts' \
            "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo "Added to forbidden list: $ARGS"
        echo ""
        echo "Current forbidden items:"
        jq -r '.guidance.forbidden[]?' "$CONFIG_FILE" | while read -r item; do
            echo "  ✗ $item"
        done
        ;;
esac
RALPH_FORBID_SCRIPT
```

Run the bash script above to manage forbidden items.

## How It Works

1. **Config file**: Changes are written to `.claude/ru-config.json`
2. **Next iteration applies**: The Stop hook reads config fresh on each iteration
3. **Template rendering**: Forbidden items appear in the `## USER GUIDANCE` section

## Troubleshooting

| Issue                  | Cause                    | Solution                             |
| ---------------------- | ------------------------ | ------------------------------------ |
| jq error on add        | Config file malformed    | Run `/ru:config reset` to recreate   |
| Item not appearing     | Typo or different casing | Use `--list` to verify exact text    |
| Forbidden not enforced | RU not running           | Start with `/ru:start`               |
| Remove by phrase fails | No match found           | Use `--list` to see exact item names |
| Config file not found  | .claude dir missing      | Create with `mkdir -p .claude`       |
