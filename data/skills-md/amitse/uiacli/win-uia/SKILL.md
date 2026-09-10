---
name: win-uia
description: "Automate any Windows desktop application — list windows, inspect UI trees, click buttons, type text, take screenshots, and run action batches. Use when the user mentions automating a Windows app, clicking buttons, UI automation, desktop control, screen interaction, Windows GUI, calculator, notepad, paint, controlling a desktop app, or computer use on Windows."
---

# Windows Desktop Automation with UIA CLI

Control any Windows desktop application from the terminal using `uia.exe`. All output is JSON.

## Prerequisites

UIA CLI must be installed. If `uia windows` fails, install it first:

```powershell
irm https://raw.githubusercontent.com/amitse/uiacli/master/install.ps1 | iex
```

## Core Workflow

### 1. Discover what's on screen

```bash
uia windows                        # List all open windows (title, handle, bounds)
uia state                          # Full snapshot: windows, focus, cursor, screens
```

### 2. Inspect a window's UI tree

```bash
uia tree Calculator --depth 3      # Nested JSON of all UI elements
uia find Calculator --name Equals  # Find specific elements by name/type/id
uia focused                        # What element has keyboard focus right now
```

### 3. Interact with elements

```bash
uia click --window Calculator --name Five         # Click by element name
uia click --x 500 --y 300                         # Click by screen coordinates
uia type --window Notepad --text "Hello world"    # Type text
uia key --window Calculator --combo ctrl+c        # Send key combo
uia focus Calculator                               # Bring window to foreground
```

### 4. Take screenshots

```bash
uia screenshot --window Calculator  # Capture window to PNG, returns file path
```

### 5. Launch apps

```bash
uia launch calc.exe                # Launch Calculator
uia launch notepad.exe             # Launch Notepad
uia launch mspaint.exe             # Launch Paint
```

### 6. Clipboard

```bash
uia clipboard get                  # Read clipboard text
uia clipboard set "copied text"   # Write to clipboard
```

## Action Batching (Key Pattern)

Always batch multiple actions into one call to avoid per-command overhead. Write a JSON file and pass it to `uia batch`:

```json
{
  "window": "Calculator",
  "actions": [
    {"type": "click", "element": {"name": "Two"}},
    {"type": "click", "element": {"name": "Five"}},
    {"type": "click", "element": {"name": "Multiply by"}},
    {"type": "click", "element": {"name": "Two"}},
    {"type": "click", "element": {"name": "Five"}},
    {"type": "click", "element": {"name": "Equals"}},
    {"type": "read", "element": {"automationId": "CalculatorResults"}}
  ],
  "verbose": true
}
```

```bash
uia batch actions.json --verbose   # Execute with overlay visuals
```

### Supported action types

| Type | Description | Key fields |
|------|-------------|------------|
| `click` | Click element or coords | `element`, `x`, `y` |
| `rightclick` | Right-click | `element`, `x`, `y` |
| `doubleclick` | Double-click | `element`, `x`, `y` |
| `type` | Type text | `text`, `element` |
| `key` | Key combo | `combo` (e.g., `ctrl+a`) |
| `read` | Read element value | `element` → returns `value` |
| `wait` | Wait for element | `element`, `timeoutMs` |
| `scroll` | Scroll | `element`, `clicks` (+down, -up) |
| `select` | Select dropdown item | `element`, `value` |
| `toggle` | Toggle checkbox/switch | `element` |
| `drag` | Drag from/to | `x`, `y`, `toX`, `toY` |
| `freehand` | Draw path | `points` array of `{x, y}` |
| `screenshot` | Mid-batch screenshot | (captures current state) |

### Element queries

Target elements using any combination of:
- `name` — visible text or accessible name
- `controlType` — Button, Edit, Text, CheckBox, ComboBox, etc.
- `automationId` — developer-assigned stable ID

Example: `{"name": "Five", "controlType": "Button"}`

## Important Patterns

### Window handles for stability
Window titles change (e.g., browser tabs). Capture the `handle` from `uia windows` and use it for all subsequent commands instead of the title.

### Apps with poor UIA trees (Paint, modern UWP)
Some apps don't expose internal controls in the UIA tree. For these:
1. `uia screenshot <window>` — see the visual layout
2. `uia tree <window> --depth 4` — see what UIA exposes
3. If elements are missing, fall back to coordinate-based clicks using bounds from the screenshot

### Verify after acting
After clicking or typing, read the result or take a screenshot to confirm the action worked. If it didn't, adjust coordinates by ±5px and retry.

## Output Format

All output is JSON:

```json
{"ok": true, "data": { ... }}
{"ok": false, "error": {"code": "WINDOW_NOT_FOUND", "message": "...", "hint": "..."}}
```

Exit codes: 0=success, 1=action failed, 2=setup error, 3=timeout.

## Server Management

The server auto-starts on first command. You rarely need these:

```bash
uia serve --background   # Start manually
uia stop                 # Stop the server
```
