---
name: tui-clone
description: Explore and analyze TUI applications to document their features for cloning. Use when asked to reverse-engineer, analyze, document, or understand a terminal UI like Claude Code, OpenCode, Codex, lazygit, or any ratatui/ncurses-based application. Launches the target TUI in tmux, systematically explores all views and keybindings, captures ASCII diagrams of each screen, and writes findings incrementally to a markdown file (survives context compaction).
---

# TUI Clone

Explore terminal user interfaces systematically to produce clone-ready documentation.

**Key principle**: Write findings to file immediately as discovered. This survives context compaction.

## Output File

All findings go to: `tui-analysis-[app-name]-[timestamp].md`

The timestamp ensures multiple sessions don't clobber each other.

## Process

### 1. Setup and Initialize Output File

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_helpers.sh
TMUX_TEST_WIDTH=140
TMUX_TEST_HEIGHT=40

APP_NAME="lazygit"  # Set to target app
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_FILE="tui-analysis-${APP_NAME}-${TIMESTAMP}.md"

# Initialize output file with header
cat > "$OUTPUT_FILE" << 'EOF'
# [App Name] TUI Analysis

## Overview
- Purpose: [TODO]
- Technology stack: [TODO]
- Target users: [TODO]

## Screen Catalog
EOF

echo "Output file: $OUTPUT_FILE"
```

### 2. Launch Target and Capture Initial View

```bash
SESSION="tui-analysis"
tmux_start "$SESSION" "$APP_NAME"
tmux_wait_for "$SESSION" "<ready-indicator>" 30

# Immediately write initial view to file
{
    echo ""
    echo "### Initial View"
    echo "- Entry: Launch command"
    echo '```'
    tmux_capture "$SESSION"
    echo '```'
} >> "$OUTPUT_FILE"

echo "Wrote initial view to $OUTPUT_FILE"
```

### 3. Write Screen Function

Use this helper to append each discovered screen:

```bash
write_screen() {
    local name="$1"
    local entry="$2"
    local session="$3"

    {
        echo ""
        echo "### $name"
        echo "- Entry: $entry"
        echo '```'
        tmux_capture "$session"
        echo '```'
    } >> "$OUTPUT_FILE"

    echo "Wrote screen '$name' to $OUTPUT_FILE"
}
```

### 4. Explore and Write Immediately

As you discover each screen, write it immediately:

```bash
# Check for help screen
tmux_send "$SESSION" "?"
if tmux_wait_for "$SESSION" "help\|Help\|Keybindings" 3; then
    write_screen "Help Screen" "Press ?" "$SESSION"
fi
tmux_send "$SESSION" Escape

# Explore numbered tabs
for i in 1 2 3 4 5; do
    tmux_send "$SESSION" "$i"
    sleep 0.3
    # Check if view changed meaningfully
    write_screen "Tab $i View" "Press $i" "$SESSION"
done
```

### 5. Write Keybindings Section

After exploring, append keybindings:

```bash
{
    echo ""
    echo "## Keybindings"
    echo ""
    echo "| Key | Context | Action |"
    echo "|-----|---------|--------|"
    echo "| ? | Global | Show help |"
    echo "| q | Global | Quit |"
    echo "| j/k | List | Navigate up/down |"
    # Add more as discovered
} >> "$OUTPUT_FILE"
```

### 6. Write Implementation Notes

At the end, append analysis:

```bash
{
    echo ""
    echo "## Implementation Notes"
    echo ""
    echo "### Patterns Identified"
    echo "- [List patterns observed]"
    echo ""
    echo "### Recommended Tech Stack"
    echo "- [Your recommendations]"
    echo ""
    echo "### Complexity Assessment"
    echo "- [Your assessment]"
} >> "$OUTPUT_FILE"
```

## Example Session: Analyzing lazygit

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_helpers.sh
TMUX_TEST_WIDTH=140
TMUX_TEST_HEIGHT=40

APP_NAME="lazygit"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_FILE="tui-analysis-${APP_NAME}-${TIMESTAMP}.md"
SESSION="analyze-${APP_NAME}"

# Initialize output file
cat > "$OUTPUT_FILE" << EOF
# $APP_NAME TUI Analysis

## Overview
- Purpose: Git TUI client
- Technology stack: Go + gocui/tcell
- Target users: Developers who prefer terminal git workflow

## Screen Catalog
EOF

# Launch and capture initial view
tmux_start "$SESSION" "$APP_NAME"
tmux_wait_for "$SESSION" "Status" 15

{
    echo ""
    echo "### Main View"
    echo "- Entry: Launch command"
    echo '```'
    tmux_capture "$SESSION"
    echo '```'
} >> "$OUTPUT_FILE"
echo "Wrote: Main View"

# Check for help
tmux_send "$SESSION" "?"
if tmux_wait_for "$SESSION" "Keybindings" 5; then
    {
        echo ""
        echo "### Help Screen"
        echo "- Entry: Press ?"
        echo '```'
        tmux_capture "$SESSION"
        echo '```'
    } >> "$OUTPUT_FILE"
    echo "Wrote: Help Screen"
fi
tmux_send "$SESSION" Escape

# Explore numbered panels
for i in 1 2 3 4 5; do
    tmux_send "$SESSION" "$i"
    sleep 0.3
    {
        echo ""
        echo "### Panel $i"
        echo "- Entry: Press $i"
        echo '```'
        tmux_capture "$SESSION"
        echo '```'
    } >> "$OUTPUT_FILE"
    echo "Wrote: Panel $i"
done

# Cleanup
tmux_send "$SESSION" q
tmux_wait_exit "$SESSION" 5

echo "Analysis complete: $OUTPUT_FILE"
```

## Resuming After Compaction

If context compacts mid-session, find and read the output file to see progress:

```bash
ls -la tui-analysis-*.md  # Find the current session's file
cat tui-analysis-lazygit-20260203-141523.md  # Read it
```

Then continue appending new discoveries to the same file. The timestamp in the filename helps identify which session you're continuing.

## Additional Analysis Dimensions

Beyond screens and keybindings, capture these for a complete clone spec:

### 7. Color/Style Analysis

Capture with ANSI codes to understand the color palette:

```bash
{
    echo ""
    echo "## Color Palette"
    echo ""
    echo "Raw ANSI capture:"
    echo '```ansi'
    tmux_capture_ansi "$SESSION"
    echo '```'
} >> "$OUTPUT_FILE"
```

### 8. Component Inventory

Document reusable UI components observed:

```bash
{
    echo ""
    echo "## Component Inventory"
    echo ""
    echo "| Component | Description | Observed In |"
    echo "|-----------|-------------|-------------|"
    echo "| List | Scrollable item list with selection | Main view, File picker |"
    echo "| Modal | Centered overlay dialog | Commit message, Confirmation |"
    echo "| Tabs | Numbered panel switcher | Top bar |"
    echo "| Status bar | Bottom info line | All views |"
    echo "| Progress | Loading/sync indicator | Push/pull operations |"
    echo "| Input | Text entry field | Search, Commit message |"
} >> "$OUTPUT_FILE"
```

### 9. Responsive Behavior

Test terminal resize handling:

```bash
# Resize terminal and capture
tmux resize-pane -t "$SESSION" -x 80 -y 24
sleep 0.5
{
    echo ""
    echo "### Compact Layout (80x24)"
    echo '```'
    tmux_capture "$SESSION"
    echo '```'
} >> "$OUTPUT_FILE"

tmux resize-pane -t "$SESSION" -x 200 -y 50
sleep 0.5
{
    echo ""
    echo "### Wide Layout (200x50)"
    echo '```'
    tmux_capture "$SESSION"
    echo '```'
} >> "$OUTPUT_FILE"
```

### 10. State Transitions

Document view change triggers:

```bash
{
    echo ""
    echo "## State Transitions"
    echo ""
    echo "| From | Trigger | To |"
    echo "|------|---------|-----|"
    echo "| Main | Enter on file | Diff view |"
    echo "| Main | c | Commit dialog |"
    echo "| Any | Escape | Previous view |"
    echo "| Any | q | Exit confirmation |"
} >> "$OUTPUT_FILE"
```

### 11. Error/Loading States

Look for and document:
- Error messages (try invalid operations)
- Loading spinners
- Empty states
- Confirmation dialogs

### 12. Data Structures

Document what data types the UI displays:
- Lists (single select, multi-select)
- Trees (expandable/collapsible)
- Tables (columns, sorting)
- Text views (scrollable, line numbers)
- Diffs (side-by-side, unified)

## ASCII Diagram Guidelines

When documenting layouts, use box-drawing characters:

```
┌─────────────────────────────────────────┐
│ Header / Title Bar                      │
├────────────────┬────────────────────────┤
│ Sidebar        │ Main Content           │
│                │                        │
│ - Item 1       │  Details here          │
│ > Item 2 *     │                        │
│ - Item 3       │                        │
├────────────────┴────────────────────────┤
│ Status Bar / Footer                     │
└─────────────────────────────────────────┘
```

Use these conventions:
- `>` for selected item
- `*` for active/focused
- `[Button]` for clickable
- `[x]` / `[ ]` for checkboxes
- `( )` / `(*)` for radio buttons
- `│` `─` `┌` `┐` `└` `┘` `├` `┤` `┬` `┴` `┼` for borders

## Known TUI Commands

| TUI | Launch Command | Ready Text |
|-----|----------------|------------|
| Claude Code | `claude` | `>` or prompt |
| OpenCode | `opencode` | Session or prompt |
| Codex | `codex` | Ready indicator |
| lazygit | `lazygit` | Status |
| lazydocker | `lazydocker` | Containers |
| htop | `htop` | CPU |
| btop | `btop` | CPU |
| k9s | `k9s` | Pods |

## Deliverable Checklist

The output file `tui-analysis-[app-name]-[timestamp].md` should contain:

- [ ] **Overview** - Purpose, tech stack, target users
- [ ] **Screen Catalog** - ASCII diagram + entry path for each view
- [ ] **Keybindings** - Complete table with context
- [ ] **State Transitions** - View change triggers
- [ ] **Component Inventory** - Reusable UI elements
- [ ] **Color Palette** - ANSI capture for styling
- [ ] **Responsive Behavior** - Compact/wide layout captures
- [ ] **Error/Loading States** - Edge case UI
- [ ] **Data Structures** - Lists, trees, tables observed
- [ ] **Implementation Notes** - Tech recommendations, complexity

## Quick Reference: What Makes a Good Clone Spec

| Dimension | Question to Answer |
|-----------|-------------------|
| Layout | How is the screen divided? Panels, sidebars, modals? |
| Navigation | How do users move between views? Keys, menus, tabs? |
| Selection | Single-select? Multi-select? How is selection shown? |
| Input | Text fields? How do they behave? Validation? |
| Feedback | Loading states? Success/error messages? Progress? |
| Scrolling | What scrolls? How is scroll position indicated? |
| Focus | What can be focused? How is focus shown? |
| Shortcuts | Global vs context-specific? Discoverable? |
| Theming | Hard-coded colors or configurable? |
| Resize | Fixed layout or responsive? Minimum size? |
