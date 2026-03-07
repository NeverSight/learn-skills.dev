---
name: wizard
description: "Interactive guidance setup with AskUserQuestion flow. TRIGGERS - ru wizard, configure guidance, setup encourage forbid, ru interactive setup."
allowed-tools: Bash, AskUserQuestion
argument-hint: "[--clear]"
---

# RU: Wizard

Interactive configuration wizard using AskUserQuestion. Presents work categories neutrally, lets user classify each as Encourage/Forbid, then resolves conflicts.

## Arguments

- `--clear`: Clear existing guidance before starting (fresh config)

## Step 1: Work Area Selection

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
      - label: "Security"
        description: "Vulnerability fixes, auth improvements"
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
      - label: "API changes"
        description: "Endpoints, contracts, interfaces"
      - label: "Database changes"
        description: "Schema, migrations, queries"
```

## Step 2: Classify Each Selection

For EACH item selected in Step 1, ask whether to Encourage or Forbid:

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

Repeat for each selected item. Track which items are classified as:

- **Encouraged**: Add to `guidance.encouraged[]`
- **Forbidden**: Add to `guidance.forbidden[]`
- **Skipped**: Do not add to either list

## Step 3: Custom Items

Ask if user wants to add custom items not in the predefined list:

```yaml
questions:
  - question: "Do you want to add custom work areas?"
    header: "Custom"
    multiSelect: false
    options:
      - label: "No, use selected items only"
        description: "Proceed with the items already configured"
      - label: "Yes, add custom items"
        description: "I'll type specific topics to configure"
```

If user selects "Yes", prompt for text input, then ask for each custom item:

- "Encourage or Forbid '[custom item]'?"

## Step 4: Conflict Detection

After all classification, check for conflicts (same item in both encouraged AND forbidden lists).

**Conflicts can occur if:**

- User accidentally selected same item in both categories
- Custom item duplicates a predefined category

If conflicts detected:

```yaml
questions:
  - question: "'[ITEM]' is marked both Encouraged AND Forbidden. Which takes priority?"
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

Repeat for each conflict until all are resolved.

## Step 5: Save Configuration

After collecting and validating all selections, run this script to save:

```bash
/usr/bin/env bash << 'RU_CONFIGURE_SAVE'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"

# Ensure config file exists with guidance structure
mkdir -p "$PROJECT_DIR/.claude"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo '{"guidance": {"forbidden": [], "encouraged": []}}' > "$CONFIG_FILE"
fi

# Ensure guidance structure exists
if ! jq -e '.guidance' "$CONFIG_FILE" >/dev/null 2>&1; then
    jq '. + {guidance: {forbidden: [], encouraged: []}}' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

echo "Configuration saved to: $CONFIG_FILE"
echo ""
echo "Current guidance:"
echo "  Forbidden: $(jq -r '.guidance.forbidden | length' "$CONFIG_FILE") items"
echo "  Encouraged: $(jq -r '.guidance.encouraged | length' "$CONFIG_FILE") items"
echo ""
jq -r '.guidance.forbidden[]' "$CONFIG_FILE" 2>/dev/null | while read item; do
    echo "  ✗ FORBID: $item"
done
jq -r '.guidance.encouraged[]' "$CONFIG_FILE" 2>/dev/null | while read item; do
    echo "  ✓ ENCOURAGE: $item"
done
echo ""
echo "To view: /ru:config show"
echo "To modify: /ru:forbid or /ru:encourage"
RU_CONFIGURE_SAVE
```

## Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Work Area Selection (neutral, multiSelect)         │
│  [ ] Bug fixes    [ ] Features     [ ] Performance          │
│  [ ] Docs         [ ] Deps         [ ] Formatting           │
│  [ ] Tests        [ ] Security     [ ] Refactoring          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Classify Each (for each selected item)             │
│  "For 'Bug fixes': Encourage / Forbid / Skip?"              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Custom Items (optional)                            │
│  "Add custom work areas?" → If yes, classify each           │
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
│  Step 5: Save config + Display summary                      │
└─────────────────────────────────────────────────────────────┘
```

## Adding Items Helper

Use this bash snippet to add items from AskUserQuestion selections:

```bash
/usr/bin/env bash << 'ADD_GUIDANCE_ITEM'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"
TYPE="${1:-forbidden}"  # "forbidden" or "encouraged"
ITEM="${2:-}"           # Item to add

if [[ -z "$ITEM" ]]; then
    exit 0
fi

# Ensure file exists
mkdir -p "$PROJECT_DIR/.claude"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo '{"guidance": {"forbidden": [], "encouraged": []}}' > "$CONFIG_FILE"
fi

# Add item with timestamp
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
jq --arg item "$ITEM" --arg ts "$TIMESTAMP" \
    ".guidance.${TYPE} = ((.guidance.${TYPE} // []) + [\$item] | unique) | .guidance.timestamp = \$ts" \
    "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
ADD_GUIDANCE_ITEM
```

## Clear Guidance Helper

Use with `--clear` argument to reset before wizard:

```bash
/usr/bin/env bash << 'CLEAR_GUIDANCE'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ru-config.json"

if [[ -f "$CONFIG_FILE" ]]; then
    TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    jq --arg ts "$TIMESTAMP" \
        '.guidance = {forbidden: [], encouraged: [], timestamp: $ts}' \
        "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    echo "Guidance cleared."
fi
CLEAR_GUIDANCE
```

## Troubleshooting

| Issue                | Cause                    | Solution                           |
| -------------------- | ------------------------ | ---------------------------------- |
| jq error             | Config file malformed    | Run `/ru:config reset` to recreate |
| No options appearing | AskUserQuestion issue    | Check that multiSelect is set      |
| Config not saved     | .claude dir missing      | Create with `mkdir -p .claude`     |
| Conflicts not shown  | Same item different case | Use exact same text for items      |
| Custom input empty   | Skipped text prompt      | Re-run wizard and enter items      |
