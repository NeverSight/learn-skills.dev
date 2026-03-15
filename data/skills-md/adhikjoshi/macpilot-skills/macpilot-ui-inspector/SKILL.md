---
name: macpilot-ui-inspector
description: Inspect and interact with macOS UI elements using MacPilot accessibility APIs. Find buttons, text fields, labels, and other elements by role, label, or position, then click, read, or modify them.
---

# MacPilot UI Inspector

Use MacPilot's accessibility (AX) commands to inspect, find, and interact with UI elements in any macOS application. This skill enables precise programmatic control of app interfaces.

## When to Use

Use this skill when the user asks to:
- Find a specific button, text field, checkbox, or UI element in an app
- Read the value or state of a UI control
- Click a button or interact with a control by its label
- Inspect the full UI hierarchy/accessibility tree of an app
- Set values in text fields or toggle checkboxes programmatically
- Discover what keyboard shortcuts an app supports
- Identify elements at specific screen coordinates

## Commands

### List UI Elements
```bash
macpilot ui list --app "Safari" --json                    # All elements
macpilot ui list --app "Safari" --role AXButton --json    # Only buttons
macpilot ui list --app "Safari" --depth 5 --json          # Deeper scan
macpilot ui list --app "Safari" --hierarchy --json        # With hierarchy
```

### Find Elements by Text
```bash
macpilot ui find "Save" --app "TextEdit" --json           # Find by label
macpilot ui find "Save" --role AXButton --json            # Filter by role
macpilot ui find "Save" --exact --json                    # Exact match only
```

### Find Element with Coordinates
```bash
macpilot ui find-text "Submit" --app "Safari" --json
# Returns: position {x, y}, size {w, h} - use for clicking
```

### Click UI Element by Label
```bash
macpilot ui click "Save" --app "TextEdit" --json
macpilot ui click "Cancel" --role AXButton --json
```

### Get/Set Values
```bash
macpilot ui get-value "Search" --app "Safari" --json          # Read field value
macpilot ui set-value "Search" "query text" --app "Safari"    # Set field value
macpilot ui set-value "Dark Mode" "1" --role AXCheckBox       # Toggle checkbox
```

### Set Focus
```bash
macpilot ui set-focus "Search" --app "Safari" --json    # Focus an element
```

### Scroll Within Elements
```bash
macpilot ui scroll "content" down 5 --app "Safari"     # Scroll element
```

### Inspect Element Attributes
```bash
macpilot ui attributes "Save" --app "TextEdit" --json   # All AX attributes
```

### Elements at Coordinates
```bash
macpilot ui elements-at 500 300 --json                  # What's at x=500 y=300
macpilot ui elements-at 500 300 --radius 50 --json      # Search wider area
```

### Accessibility Tree
```bash
macpilot ui tree --app "Finder" --json                  # Full AX tree
macpilot ui tree --app "Finder" --depth 3 --json        # Limit depth
```

### Keyboard Shortcuts
```bash
macpilot ui shortcuts --app "Safari" --json             # All shortcuts
macpilot ui shortcuts --app "Safari" --menu File --json # Menu-specific
```

### Wait for Elements
```bash
macpilot wait element "Download Complete" --app "Safari" --timeout 30 --json
```

## Common AX Roles

| Role | Description |
|------|-------------|
| `AXButton` | Buttons (push, toggle) |
| `AXTextField` | Text input fields |
| `AXTextArea` | Multi-line text areas |
| `AXStaticText` | Labels and display text |
| `AXCheckBox` | Checkboxes and toggles |
| `AXRadioButton` | Radio buttons |
| `AXPopUpButton` | Dropdown menus |
| `AXComboBox` | Combo boxes |
| `AXTable` | Tables and lists |
| `AXRow` | Table/list rows |
| `AXMenuItem` | Menu items |
| `AXToolbar` | Toolbars |
| `AXScrollArea` | Scrollable regions |
| `AXWindow` | Windows |
| `AXSheet` | Modal sheets |
| `AXImage` | Images |
| `AXLink` | Hyperlinks |
| `AXGroup` | Generic container |

## Workflow Patterns

### Pattern 1: Find and Click
```bash
# Always focus app first
macpilot app focus "Safari"
# Find the element to verify it exists
macpilot ui find "Downloads" --app "Safari" --role AXButton --json
# Click it
macpilot ui click "Downloads" --app "Safari"
```

### Pattern 2: Read Form State
```bash
macpilot app focus "System Settings"
macpilot ui get-value "Computer Name" --app "System Settings" --json
```

### Pattern 3: Fill a Form
```bash
macpilot app focus "MyApp"
macpilot ui set-value "Name" "John Doe" --app "MyApp"
macpilot ui set-value "Email" "john@example.com" --app "MyApp"
macpilot ui click "Submit" --app "MyApp"
```

### Pattern 4: Explore Unknown UI
```bash
# Start with a broad scan
macpilot ui tree --app "SomeApp" --depth 2 --json
# Narrow down to specific elements
macpilot ui list --app "SomeApp" --role AXButton --json
# Inspect a specific element
macpilot ui attributes "Settings" --app "SomeApp" --json
```

### Pattern 5: Click by Coordinates (Fallback)
```bash
# When label-based clicking fails, find coordinates first
macpilot ui find-text "Submit" --app "MyApp" --json
# Use returned x,y to click
macpilot click 450 320
```

## Tips

- Always call `macpilot app focus` before any UI interaction
- Use `--json` output for reliable parsing of element properties
- When `ui click` fails, fall back to `ui find-text` + `macpilot click x y`
- Use `ui tree --depth 2` first to understand app structure before deep scans
- AX permission must be granted to MacPilot.app in System Settings
- The `--role` filter significantly speeds up element searches in complex apps
