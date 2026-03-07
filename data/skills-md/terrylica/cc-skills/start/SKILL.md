---
name: start
description: "Enable autonomous loop mode for any project. TRIGGERS - ru start, start autonomous, enable loop mode, begin autonomous work."
allowed-tools: Bash, AskUserQuestion
argument-hint: "[--poc | --production | --quick]"
disable-model-invocation: true
---

# RU: Start

Enable autonomous loop mode for **any project type**.

## Arguments

- `--poc`: Use proof-of-concept settings (5 min / 10 min limits, 10/20 iterations)
- `--production`: Use production settings (4h / 9h limits, 50/99 iterations)
- `--quick`: Skip guidance setup, use existing config

## Step 1: Mode Selection

Use AskUserQuestion:

```yaml
questions:
  - question: "Select loop configuration:"
    header: "Mode"
    multiSelect: false
    options:
      - label: "POC Mode (Recommended)"
        description: "5-10 min, 10-20 iterations - ideal for testing"
      - label: "Production Mode"
        description: "4-9 hours, 50-99 iterations - standard work"
```

## Step 2: Work Selection (unless --quick)

Present ALL work categories neutrally. Let user select which ones they want to configure:

```yaml
questions:
  - question: "Which work areas do you want to configure? (Select all relevant)"
    header: "Work Areas"
    multiSelect: true
    options:
      - label: "Bug fixes"
        description: "Fix errors, exceptions, crashes"
      - label: "Feature completion"
        description: "Finish incomplete features"
      - label: "Performance"
        description: "Speed, memory, efficiency"
      - label: "Error handling"
        description: "Edge cases, validation"
      - label: "Documentation"
        description: "README, docstrings, comments"
      - label: "Dependency upgrades"
        description: "Version bumps, lock files"
      - label: "Code formatting"
        description: "Linting, style changes"
      - label: "Test expansion"
        description: "Adding tests for existing code"
      - label: "Refactoring"
        description: "Code restructuring, DRY improvements"
      - label: "Security"
        description: "Vulnerability fixes, auth improvements"
```

## Step 3: Classify Each Selection

For EACH item selected in Step 2, ask whether to Encourage or Forbid:

```yaml
questions:
  - question: "For '[ITEM]': Should RU prioritize or avoid this?"
    header: "Classify"
    multiSelect: false
    options:
      - label: "Encourage (Prioritize)"
        description: "RU should actively seek this type of work"
      - label: "Forbid (Avoid)"
        description: "RU should not work on this unless necessary"
      - label: "Skip (No preference)"
        description: "Leave neutral, neither prioritize nor avoid"
```

Repeat for each selected item.

## Step 4: Conflict Detection

After classification, check for conflicts (same item in both encouraged AND forbidden).

If conflicts detected:

```yaml
questions:
  - question: "[ITEM] is marked both Encouraged AND Forbidden. Which takes priority?"
    header: "Conflict"
    multiSelect: false
    options:
      - label: "Encourage wins"
        description: "Prioritize this work, remove from forbidden"
      - label: "Forbid wins"
        description: "Avoid this work, remove from encouraged"
      - label: "Remove both"
        description: "Leave neutral, no guidance for this item"
```

Only proceed when all conflicts are resolved.

## Step 5: Execution

After collecting and validating guidance selections, save them and start the loop:

```bash
/usr/bin/env bash << 'RU_START_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "========================================"
echo "  RU - Autonomous Loop Mode"
echo "========================================"
echo ""

# Parse arguments
ARGS="${ARGUMENTS:-}"
POC_MODE=false
PRODUCTION_MODE=false

if [[ "$ARGS" == *"--poc"* ]]; then
    POC_MODE=true
fi
if [[ "$ARGS" == *"--production"* ]]; then
    PRODUCTION_MODE=true
fi

# Set limits based on mode
if $POC_MODE; then
    MIN_HOURS=0.083
    MAX_HOURS=0.167
    MIN_ITERS=10
    MAX_ITERS=20
    MODE_NAME="POC"
else
    MIN_HOURS=4
    MAX_HOURS=9
    MIN_ITERS=50
    MAX_ITERS=99
    MODE_NAME="PRODUCTION"
fi

# Check for uv
UV_CMD=""
for loc in "$HOME/.local/share/mise/shims/uv" "$HOME/.local/bin/uv" "/opt/homebrew/bin/uv" "uv"; do
    if command -v "$loc" &>/dev/null || [[ -x "$loc" ]]; then
        UV_CMD="$loc"
        break
    fi
done

if [[ -z "$UV_CMD" ]]; then
    echo "ERROR: uv is required. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create state directory
mkdir -p "$PROJECT_DIR/.claude"

# Check current state
STATE_FILE="$PROJECT_DIR/.claude/ru-state.json"
if [[ -f "$STATE_FILE" ]]; then
    CURRENT_STATE=$(jq -r '.state // "stopped"' "$STATE_FILE" 2>/dev/null || echo "stopped")
    if [[ "$CURRENT_STATE" != "stopped" ]]; then
        echo "ERROR: Loop already in state '$CURRENT_STATE'"
        echo "       Run /ru:stop first"
        exit 1
    fi
fi

# Transition to RUNNING state
echo '{"state": "running"}' > "$STATE_FILE"
date +%s > "$PROJECT_DIR/.claude/ru-start-timestamp"

# Create/update config (preserve guidance if exists)
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"
if [[ -f "$CONFIG_FILE" ]]; then
    # Update existing config, preserve guidance
    jq --arg state "running" \
       --argjson min_hours "$MIN_HOURS" \
       --argjson max_hours "$MAX_HOURS" \
       --argjson min_iterations "$MIN_ITERS" \
       --argjson max_iterations "$MAX_ITERS" \
       '.state = $state | .loop_limits = {
           min_hours: $min_hours,
           max_hours: $max_hours,
           min_iterations: $min_iterations,
           max_iterations: $max_iterations
       }' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
else
    # Create new config
    jq -n \
        --arg state "running" \
        --argjson min_hours "$MIN_HOURS" \
        --argjson max_hours "$MAX_HOURS" \
        --argjson min_iterations "$MIN_ITERS" \
        --argjson max_iterations "$MAX_ITERS" \
        '{
            version: "1.0.0",
            state: $state,
            loop_limits: {
                min_hours: $min_hours,
                max_hours: $max_hours,
                min_iterations: $min_iterations,
                max_iterations: $max_iterations
            },
            guidance: {
                forbidden: [],
                encouraged: []
            }
        }' > "$CONFIG_FILE"
fi

echo "Mode: $MODE_NAME"
echo "Time: ${MIN_HOURS}h min / ${MAX_HOURS}h max"
echo "Iterations: ${MIN_ITERS} min / ${MAX_ITERS} max"
echo ""

# Show guidance summary
FORBIDDEN_COUNT=$(jq -r '.guidance.forbidden // [] | length' "$CONFIG_FILE" 2>/dev/null || echo "0")
ENCOURAGED_COUNT=$(jq -r '.guidance.encouraged // [] | length' "$CONFIG_FILE" 2>/dev/null || echo "0")
echo "Guidance:"
echo "  Forbidden: $FORBIDDEN_COUNT items"
echo "  Encouraged: $ENCOURAGED_COUNT items"
echo ""

echo "Project: $PROJECT_DIR"
echo "State: RUNNING"
echo ""
echo "Commands:"
echo "  /ru:stop     - Stop the loop"
echo "  /ru:status   - Check status"
echo "  /ru:forbid   - Add forbidden item"
echo "  /ru:encourage - Add encouraged item"
RU_START_SCRIPT
```

## Guidance Helper

After AskUserQuestion selections, use this to add items:

```bash
/usr/bin/env bash << 'ADD_ITEMS'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"
TYPE="${1}"      # "forbidden" or "encouraged"
ITEM="${2}"      # Item to add

if [[ -z "$TYPE" || -z "$ITEM" ]]; then
    exit 0
fi

# Ensure file exists
mkdir -p "$PROJECT_DIR/.claude"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo '{"guidance": {"forbidden": [], "encouraged": []}}' > "$CONFIG_FILE"
fi

# Ensure guidance structure exists
if ! jq -e '.guidance' "$CONFIG_FILE" >/dev/null 2>&1; then
    jq '. + {guidance: {forbidden: [], encouraged: []}}' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

# Add item
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq --arg item "$ITEM" --arg ts "$TIMESTAMP" \
    ".guidance.${TYPE} = ((.guidance.${TYPE} // []) + [\$item] | unique) | .guidance.timestamp = \$ts" \
    "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
ADD_ITEMS
```

## After Starting

The loop continues until:

- Maximum time/iterations reached
- You run `/ru:stop`
- Kill switch: `touch .claude/STOP_LOOP`

Use `/ru:wizard` for detailed guidance setup anytime.

## Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Mode Selection                                     │
│  [POC Mode] / [Production Mode]                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Work Selection (neutral, multiSelect)              │
│  [ ] Bug fixes    [ ] Features     [ ] Performance          │
│  [ ] Docs         [ ] Deps         [ ] Formatting           │
│  [ ] Tests        [ ] Refactoring  [ ] Security             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Classify Each (for each selected item)             │
│  "For 'Bug fixes': Encourage / Forbid / Skip?"              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Conflict Resolution (if any)                       │
│  "'X' is both Encouraged AND Forbidden. Which wins?"        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5: Save config + Start loop                           │
└─────────────────────────────────────────────────────────────┘
```

## Examples

```bash
# Start POC mode (quick test)
/ru:start --poc

# Start production mode (longer session)
/ru:start --production

# Start with existing config, skip setup
/ru:start --quick
```

## Troubleshooting

| Issue             | Cause                     | Solution                                           |
| ----------------- | ------------------------- | -------------------------------------------------- |
| uv not found      | uv not installed          | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Loop already in X | Previous loop not stopped | Run `/ru:stop` first                               |
| jq error          | jq not installed          | `brew install jq`                                  |
| Config preserved  | Used --quick              | Delete `.claude/ru-config.json` to reset           |
