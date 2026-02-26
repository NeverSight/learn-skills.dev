---
name: tui-review
description: Critically review terminal user interfaces for UX quality, responsiveness, visual design, and interactivity. Use when asked to "review my TUI", "test my TUI UX", "audit my terminal UI", "check TUI responsiveness", "review TUI keybindings", "check interactivity", or any request to evaluate the user experience quality of a ratatui/crossterm/ncurses-based terminal application. Launches the TUI in tmux, systematically tests 10 dimensions (responsiveness, input conflicts, visual clarity, navigation, feedback loops, error states, layout, keyboard design, permission flows, visual design & color), and produces a graded report with screenshots and specific findings. Benchmarks against Claude Code, OpenCode, and Codex — the three best-in-class AI terminal UIs.
---

# TUI Review

Critically review terminal UIs by running them live in tmux, taking screenshots at key states, and testing against 10 UX dimensions. Benchmarks against Claude Code, OpenCode, and Codex.

**Gold standard**: Every keypress produces visible change within 100ms. Every state has a designed appearance. Color communicates meaning. No dead keys, no blank screens, no stuck states.

## Style Opinion: Borders

Flag excessive border usage. Many TUIs wrap the entire screen in box-drawing borders (`╭╮╰╯│─`) — this wastes precious terminal real estate and adds visual noise. Borders should be used **sparingly and purposefully**:

- **Good**: Borders to separate distinct regions (input area vs conversation), to frame a modal/dialog that overlays content, or to visually group related controls.
- **Bad**: A full outer border around the entire TUI (eats 2 columns + 2 rows for zero information gain), borders around every panel when whitespace/divider lines would suffice, nested borders creating a "box in a box" effect.

**What the best TUIs actually do**: Claude Code uses horizontal rule lines (`────`) to separate the input area — no outer border. OpenCode uses `┃` left-margin lines for message attribution — not a full box. Codex uses bordered boxes only for the header info panel and status panel — the conversation area itself is borderless. The pattern: **content-heavy areas are borderless; chrome-heavy areas (headers, dialogs) get borders.**

Flag any TUI that wraps the full screen in a border as a WARNING.

## Process

1. Launch TUI in tmux
2. Take **initial screenshot** — first impression matters
3. Discover the UI (find help, navigation, input areas)
4. Test each of the 10 dimensions, **screenshotting each key state**
5. Take **resize screenshots** at 80x24, 120x30, 160x40, 200x50
6. **Visually review** all screenshots using the Read tool
7. Produce graded report with screenshots and findings

## Setup

### CRITICAL: Enable True-Color in tmux (RGB colors)

**Ratatui/crossterm TUIs use RGB colors** (`Color::Rgb(r,g,b)`). By default, tmux does NOT pass these through, causing `capture-pane -e` to strip all color escape codes. You MUST enable true-color support BEFORE launching the TUI:

```bash
# Enable true-color (Tc) for ALL terminal types — run ONCE per tmux server
tmux set-option -g default-terminal "xterm-256color"
tmux set-option -ga terminal-overrides ",*:Tc"
```

**Without this fix**: `capture-pane -e` returns zero ANSI escape codes — the TUI appears monochrome in captures even though it renders colorful in a real terminal. This is because tmux's internal cell storage doesn't preserve RGB attributes unless Tc is enabled.

**Verification**: After setting the override and launching a ratatui TUI, check:
```bash
tmux capture-pane -t $SESSION -e -p | hexdump -C | grep '1b 5b 33 38 3b 32'
# Should show: |.[38;2;R;G;Bm| sequences (RGB foreground color codes)
# If empty: Tc override is not working
```

### Screenshot Method

Use `capture-pane -e` (with escape codes) piped to `freeze` for color PNG screenshots:

```bash
# Take a color screenshot
tmux capture-pane -t $SESSION -e -p | freeze --language ansi --output /tmp/screenshot.png

# IMPORTANT: freeze may hang — always run with a timeout
tmux capture-pane -t $SESSION -e -p | freeze --language ansi --output /tmp/screenshot.png &
PID=$!
sleep 6
kill $PID 2>/dev/null
```

### Full Setup

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_helpers.sh
TMUX_TEST_WIDTH=140
TMUX_TEST_HEIGHT=40
TMUX_TEST_POLL_INTERVAL=0.1
TMUX_SCREENSHOT_DIR="/tmp/tui-review-screenshots"
mkdir -p "$TMUX_SCREENSHOT_DIR"

# CRITICAL: Enable true-color BEFORE starting any TUI session
tmux set-option -g default-terminal "xterm-256color"
tmux set-option -ga terminal-overrides ",*:Tc"

SESSION="tui-review"
# Launch with COLORTERM=truecolor to help crossterm detect color support
tmux new-session -d -s "$SESSION" -x $TMUX_TEST_WIDTH -y $TMUX_TEST_HEIGHT \
  "COLORTERM=truecolor <command>"
sleep 4  # Wait for TUI to render

# Take first color screenshot
tmux capture-pane -t "$SESSION" -e -p | \
  freeze --language ansi --output "$TMUX_SCREENSHOT_DIR/01-initial.png" &
PID=$!; sleep 6; kill $PID 2>/dev/null

# Visually inspect it
# Use Read tool on the PNG path
```

**Requires**: `freeze` (`brew install charmbracelet/tap/freeze`) for PNG screenshots.

## Screenshot Protocol

Take screenshots at these moments during the review. Use the **Read tool** to visually inspect each PNG.

| # | State | Label | What to Look For |
|---|-------|-------|-----------------|
| 1 | Initial load | `01-initial` | First impression, layout, color usage |
| 2 | Help/shortcuts overlay | `02-help` | Discoverability, overlay design |
| 3 | Command palette / slash menu | `03-commands` | Dropdown styling, selection highlight |
| 4 | During processing/streaming | `04-processing` | Loading indicator, streaming text |
| 5 | Completed response | `05-response` | Message formatting, tool output |
| 6 | Error state | `06-error` | Error visibility, color distinction |
| 7 | Dialog/modal open | `07-dialog` | Modal design, backdrop |
| 8 | Permission/confirmation flow | `08-permission` | Diff preview, action options |
| 9-12 | Resize: 80x24, 120x30, 160x40, 200x50 | `09-resize-WxH` | Layout adaptation |

```bash
# Helper function for color screenshots (use instead of tmux_screenshot for ratatui TUIs)
take_color_screenshot() {
  local session="$1" label="$2"
  local outfile="$TMUX_SCREENSHOT_DIR/${label}.png"
  tmux capture-pane -t "$session" -e -p | \
    freeze --language ansi --output "$outfile" &
  local pid=$!
  sleep 6
  kill $pid 2>/dev/null
  echo "$outfile"
}

# Example: screenshot after opening help
tmux send-keys -t "$SESSION" "?"
sleep 1
take_color_screenshot "$SESSION" "02-help"

# Example: resize screenshots
for size in "80x24" "120x30" "160x40" "200x50"; do
  IFS='x' read -r w h <<< "$size"
  tmux resize-window -t "$SESSION" -x "$w" -y "$h"
  sleep 0.5
  take_color_screenshot "$SESSION" "09-resize-${size}"
done

# Visually inspect a screenshot (CRITICAL — actually look at it)
# Use the Read tool on the PNG path
```

**IMPORTANT**: After taking each screenshot, use the **Read tool** to view the PNG file. This is what makes the review "visual" — you are literally looking at the rendered TUI and assessing color, layout, contrast, and design quality.

**NOTE on tmux_screenshot vs take_color_screenshot**: The `tmux_screenshot` helper from `tmux_helpers.sh` may not preserve RGB colors from ratatui/crossterm TUIs. For any TUI built with ratatui, crossterm, or similar Rust terminal frameworks, use the `take_color_screenshot` function above which pipes `capture-pane -e` through freeze with `--language ansi` to preserve all RGB color information.

## The 10 Dimensions

Read [references/heuristics.md](references/heuristics.md) for detailed test procedures, pass/fail criteria, and best-in-class examples for each dimension.

1. **Responsiveness** - Every keypress produces visible change within 100ms
2. **Input Mode Integrity** - Trigger characters don't hijack mid-sentence text input
3. **Visual Feedback** - Every app state has a distinct visual indicator
4. **Navigation & Escape** - Escape always goes back, never get stuck
5. **Feedback Loops** - Submit triggers: clear, echo, loading, stream, completion
6. **Error & Empty States** - Every state has a designed appearance, no blank screens
7. **Layout & Resize** - Usable at 80x24, scales to 200x50+
8. **Keyboard Design** - All features keyboard-reachable, shortcuts discoverable
9. **Permission Flows** - Destructive actions show preview, require confirmation
10. **Visual Design & Color** - Color communicates meaning, sufficient contrast, consistent palette

## Visual Review Checklist

When reviewing screenshots with the Read tool, evaluate:

### Color
- [ ] **Semantic color**: Status colors (green=success, red=error, yellow=warning) used consistently
- [ ] **Color richness**: Not monochrome — uses color to create visual hierarchy
- [ ] **Contrast**: Text readable against background (no light-gray-on-dark-gray)
- [ ] **Consistency**: Same element type uses same color everywhere
- [ ] **Restraint**: Not a rainbow — limited palette with purpose

### Layout
- [ ] **Density**: Information-dense without feeling cluttered
- [ ] **Alignment**: Elements align to a grid, no ragged edges
- [ ] **Whitespace**: Breathing room between sections
- [ ] **Proportions**: Input area, content area, and status bar are well-sized

### Typography
- [ ] **Hierarchy**: Headers/titles are visually distinct (bold, color, or size)
- [ ] **Readability**: Line lengths reasonable (not 200-char lines)
- [ ] **Symbols**: Unicode symbols (●, ◐, ✓, ✗) used for status, not ASCII

### Polish
- [ ] **No artifacts**: No stray characters, broken box-drawing, or rendering glitches
- [ ] **Consistent borders**: Border style (thin/thick/double) is consistent
- [ ] **Professional feel**: Would this look good in a demo or conference talk?

## Color Assertions (Programmatic)

Use these alongside visual review for automated checks:

```bash
# Check that the pane uses color (not monochrome)
tmux_assert_not_monochrome "$SESSION" "TUI uses color"

# Check that at least 4 distinct colors are used (visual hierarchy)
tmux_assert_min_colors "$SESSION" 4 "sufficient color variety"

# Check specific semantic colors
tmux_assert_text_color "$SESSION" "READY" "32" "READY is green"
tmux_assert_text_color "$SESSION" "ERROR" "31" "ERROR is red"
tmux_assert_has_color "$SESSION" "33" "yellow/warning color present"
```

## Report Format

```markdown
# TUI Review: [App Name]

**Overall Grade**: [A/B/C/D/F]
**Tested at**: [terminal size] | **Binary**: [path] | **Date**: [date]
**Screenshots**: [directory path]

## Summary
[2-3 sentence verdict]

## Screenshots

### Initial State
![initial](screenshots/01-initial.png)
[Visual observations: layout, color palette, first impression]

### Key States
![help](screenshots/02-help.png)
[Visual observations for each captured state]

### Resize Behavior
![80x24](screenshots/09-resize-80x24.png) ![200x50](screenshots/09-resize-200x50.png)
[How the layout adapts]

## Scores

| # | Dimension | Grade | Issues |
|---|-----------|-------|--------|
| 1 | Responsiveness | | |
| 2 | Input Integrity | | |
| 3 | Visual Feedback | | |
| 4 | Navigation | | |
| 5 | Feedback Loops | | |
| 6 | Error States | | |
| 7 | Layout | | |
| 8 | Keyboard Design | | |
| 9 | Permission Flows | | |
| 10 | Visual Design & Color | | |

## Findings

### CRITICAL (must fix)
- [finding with file:line if known]

### WARNING (should fix)
- [finding]

### INFO (nice to have)
- [finding]

## vs Best-in-Class
[How this TUI compares to Claude Code/OpenCode/Codex patterns]
```

**Grading**: A = no issues. B = minor polish needed. C = noticeable UX friction. D = broken workflows. F = unusable.

## Quick Start for Unknown TUIs

When reviewing a TUI you haven't seen before:

1. Launch and wait for ready
2. **Screenshot the initial state** and visually review it
3. Press `?` then `F1` to find help — screenshot if found
4. Try `/` for command palette — screenshot if found
5. Try `Tab`, arrow keys, `j`/`k` for navigation
6. Try `Escape` from every state you reach
7. Type text to find input areas
8. Submit a message and screenshot the processing + response states
9. **Take resize screenshots** at all 4 sizes
10. Run color assertions (monochrome check, min colors, semantic colors)
11. **Visually review ALL screenshots** using Read tool
12. Then run the remaining dimension tests
