---
name: macpilot-dialog-handler
description: Handle macOS file dialogs (Open, Save, Print) with MacPilot. Navigate folders, select files, set filenames, and dismiss dialogs programmatically in any application.
---

# MacPilot Dialog Handler

Use MacPilot's dialog commands to interact with native macOS file dialogs (Open, Save As, Print, etc.) that appear in any application. Navigate to folders, select files, set filenames, and confirm or cancel dialogs.

## When to Use

Use this skill when:
- A file Open or Save dialog is showing and you need to navigate it
- You need to programmatically open or save files through native dialogs
- A modal dialog (alert, confirmation) needs to be dismissed
- You need to inspect what elements a dialog contains
- You need to automate file selection workflows

## Commands

### Detect Dialogs
```bash
macpilot dialog detect --json
# Returns: whether a modal dialog/sheet is present, its type, and owning app
```

### Inspect Dialog Elements
```bash
macpilot dialog inspect --json
# Returns: all interactive elements (buttons, text fields, lists) in the dialog
macpilot dialog inspect --depth 20 --json   # Deeper inspection
```

### Navigate to Folder
```bash
macpilot dialog navigate "/Users/me/Documents" --json
# Opens the Go To Folder sheet (Cmd+Shift+G), sets the path, presses Return
# Waits for navigation to complete
```

### List Files in Dialog
```bash
macpilot dialog list-files --json
# Returns: list of files/folders visible in the current dialog location
```

### Select a File
```bash
macpilot dialog select "myfile.txt" --json            # Select file (highlight only)
macpilot dialog select "myfile.txt" --confirm --json   # Select and confirm (Open/Save)
```

### Set Text Field (Filename)
```bash
macpilot dialog set-field "output.pdf" --json              # Set filename in Save dialog
macpilot dialog set-field "query" --label "Search" --json  # Set specific labeled field
macpilot dialog set-field "text" --focused --json          # Set currently focused field
```

### Click Dialog Button
```bash
macpilot dialog click-button "Save" --json
macpilot dialog click-button "Cancel" --json
macpilot dialog click-button "Open" --json
macpilot dialog click-button "Replace" --json
```

### Wait for Dialog
```bash
macpilot dialog wait-for --timeout 30 --json         # Wait for any dialog to appear
macpilot dialog wait-for --app "Safari" --json        # Wait for dialog in specific app
```

### Click Primary Button
```bash
macpilot dialog click-primary --json                 # Click default/primary button (OK, Allow, Open, etc.)
macpilot dialog click-primary --app "Finder" --json  # In specific app
```

### Dismiss Dialogs
```bash
macpilot dialog dismiss "OK" --json           # Dismiss by clicking named button
macpilot dialog auto-dismiss --json           # Auto-dismiss with safe defaults (Cancel/OK)
```

### Trigger File Open/Save
```bash
macpilot dialog file-open "/path/to/file.txt" --json   # Trigger Open and navigate
macpilot dialog file-save "/path/to/output.pdf" --json  # Trigger Save As and navigate
```

## Complete Workflows

### Save a File to Specific Location
```bash
# 1. Trigger Save dialog (Cmd+S or Cmd+Shift+S)
macpilot app focus "TextEdit"
macpilot keyboard key cmd+shift+s

# 2. Wait for dialog to appear
macpilot wait seconds 1

# 3. Navigate to target folder
macpilot dialog navigate "/Users/me/Desktop"

# 4. Set the filename
macpilot dialog set-field "report.txt"

# 5. Click Save
macpilot dialog click-button "Save"
```

### Open a Specific File
```bash
# 1. Trigger Open dialog
macpilot app focus "TextEdit"
macpilot keyboard key cmd+o

# 2. Wait for dialog
macpilot wait seconds 1

# 3. Navigate and select
macpilot dialog navigate "/Users/me/Documents"
macpilot wait seconds 1
macpilot dialog select "readme.md" --confirm
```

### Handle "Replace Existing File" Confirmation
```bash
macpilot dialog click-button "Save"
macpilot wait seconds 0.5
# Check if a confirmation dialog appeared
macpilot dialog detect --json
# If yes, click Replace
macpilot dialog click-button "Replace"
```

### Inspect an Unknown Dialog
```bash
# First, see what dialog is present
macpilot dialog detect --json

# Then inspect all its interactive elements
macpilot dialog inspect --json

# Now you know what buttons and fields are available
```

### One-Shot File Open
```bash
# Combines triggering the open dialog, navigating, and selecting
macpilot dialog file-open "/Users/me/Documents/report.pdf"
```

## Critical Patterns

1. **Wait after triggering dialogs**: Always `macpilot wait seconds 1` after `cmd+o` or `cmd+s` to let the dialog fully appear before interacting.

2. **Navigate before selecting**: File dialogs open in the last-used directory. Always `dialog navigate` to the correct folder first.

3. **Dialog owns focus**: When a dialog is open, the dialog's owning app must be active. MacPilot's dialog commands handle this automatically by scanning all apps for dialogs.

4. **Use inspect for unknown dialogs**: If you're unsure what elements a dialog has, run `dialog inspect --json` first to see all available buttons, fields, and controls.

5. **Handle cascading dialogs**: Save operations may trigger "Replace?" or "Format?" confirmation dialogs. Always check with `dialog detect` after clicking Save.

6. **set-field vs keyboard type**: Use `dialog set-field` instead of `keyboard type` for entering filenames - it directly sets the AX value, which is more reliable than simulating keystrokes.

7. **wait-for + click-primary**: For automated workflows, use `dialog wait-for` to detect when a dialog appears, then `dialog click-primary` to accept the default action. The primary button check looks for `AXDefaultButton` first, then falls back to common labels (OK, Allow, Open, Save, Continue, Yes, Done, Confirm).
