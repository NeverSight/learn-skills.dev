---
name: encourage
description: "Add item to encouraged list (prioritizes work on matching topics). TRIGGERS - ru encourage, add encouraged, prioritize topic, encourage work."
allowed-tools: Bash, AskUserQuestion
argument-hint: "<phrase> | --list | --clear | --remove"
model: haiku
---

# RU: Encourage

Add items to the encouraged list during an active loop session.
Encouraged items get priority in opportunity discovery and override forbidden patterns.

**Runtime configurable**: Works with or without active loop. Changes apply on next iteration.

## Usage

- `/ru:encourage test coverage` - Add "test coverage" to encouraged list
- `/ru:encourage --list` - Show current encouraged items
- `/ru:encourage --clear` - Clear all encouraged items
- `/ru:encourage --remove <phrase>` - Remove item matching phrase (fuzzy)

## Execution

```bash
/usr/bin/env bash << 'RALPH_ENCOURAGE_SCRIPT'
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
        echo "Current encouraged items:"
        jq -r '.guidance.encouraged[]?' "$CONFIG_FILE" | while read -r item; do
            echo "  + $item"
        done
        COUNT=$(jq -r '.guidance.encouraged | length' "$CONFIG_FILE")
        echo ""
        echo "Total: $COUNT items"
        ;;
    "--clear"|"-c")
        jq '.guidance.encouraged = []' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo "Cleared all encouraged items"
        ;;
    --remove\ *)
        PHRASE="${ARGS#--remove }"
        MATCH=$(jq -r --arg phrase "$PHRASE" \
            '.guidance.encouraged[] | select(. | ascii_downcase | contains($phrase | ascii_downcase))' \
            "$CONFIG_FILE" | head -1)
        if [[ -z "$MATCH" ]]; then
            echo "No encouraged item matches: $PHRASE"
            exit 1
        fi
        TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        jq --arg match "$MATCH" --arg ts "$TS" \
            '.guidance.encouraged |= map(select(. != $match)) | .guidance.timestamp = $ts' \
            "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo "Removed from encouraged list: $MATCH"
        ;;
    "")
        echo "Usage: /ru:encourage <phrase> | --list | --clear | --remove <phrase>"
        echo ""
        echo "Current encouraged items:"
        jq -r '.guidance.encouraged[]?' "$CONFIG_FILE" | while read -r item; do
            echo "  + $item"
        done
        ;;
    *)
        TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        jq --arg item "$ARGS" --arg ts "$TS" \
            '.guidance.encouraged = ((.guidance.encouraged // []) + [$item] | unique) | .guidance.timestamp = $ts' \
            "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
        echo "Added to encouraged list: $ARGS"
        echo ""
        echo "Current encouraged items:"
        jq -r '.guidance.encouraged[]?' "$CONFIG_FILE" | while read -r item; do
            echo "  + $item"
        done
        ;;
esac
RALPH_ENCOURAGE_SCRIPT
```

Run the bash script above to manage encouraged items.

## How It Works

1. **Config file**: Changes are written to `.claude/ru-config.json`
2. **Next iteration applies**: The Stop hook reads config fresh on each iteration
3. **Priority override**: Encouraged items override forbidden patterns
4. **Template rendering**: Encouraged items appear in the `## USER GUIDANCE` section

## Troubleshooting

| Issue                  | Cause                    | Solution                             |
| ---------------------- | ------------------------ | ------------------------------------ |
| jq error on add        | Config file malformed    | Run `/ru:config reset` to recreate   |
| Item not appearing     | Typo or different casing | Use `--list` to verify exact text    |
| Encouraged not applied | RU not running           | Start with `/ru:start`               |
| Remove by phrase fails | No match found           | Use `--list` to see exact item names |
| Config file not found  | .claude dir missing      | Create with `mkdir -p .claude`       |
