---
name: macpilot-automation
description: Core macOS automation skill using MacPilot CLI. Enables Claude Code to control apps, type text, click elements, run shell commands, and automate workflows on macOS via the `macpilot` command.
---

# MacPilot Automation

Use the `macpilot` CLI tool to automate macOS. MacPilot provides 100+ commands for mouse, keyboard, app, window, UI, clipboard, dialog, shell, and system control. All commands support `--json` for structured output.

## When to Use

Use this skill when the user asks to:
- Automate macOS tasks (open apps, click buttons, type text, navigate menus)
- Control mouse and keyboard programmatically
- Interact with running applications via accessibility APIs
- Chain multiple automation steps into workflows
- Run shell commands or interact with Terminal
- Manage clipboard, notifications, audio, display settings

## Prerequisites

MacPilot must be installed at `/Applications/MacPilot.app` with a symlink at `/usr/local/bin/macpilot` or `~/bin/macpilot`. The app requires Accessibility permission in System Settings > Privacy & Security > Accessibility.

## Core Commands Reference

### Mouse Control
```bash
macpilot click <x> <y>              # Left click at coordinates
macpilot doubleclick <x> <y>        # Double click
macpilot rightclick <x> <y>         # Right click
macpilot move <x> <y>               # Move cursor
macpilot drag <x1> <y1> <x2> <y2>  # Drag from point to point
macpilot scroll <up|down|left|right> [amount]  # Scroll (default: 3)
macpilot mouse-position --json      # Get current cursor position
```

### Keyboard Control
```bash
macpilot keyboard type "Hello World"           # Type text
macpilot keyboard key cmd+c                    # Press shortcut
macpilot keyboard key enter                    # Press single key
macpilot chain "type:hello" "key:tab" "type:world"  # Chain actions
```
Modifier keys: `cmd`, `shift`, `alt`, `ctrl`, `fn`
Special keys: `enter`, `tab`, `space`, `escape`, `delete`, `f1`-`f12`, `up`, `down`, `left`, `right`

### App Management
```bash
macpilot app open "Safari"          # Open/launch app
macpilot app focus "Safari"         # Bring app to front
macpilot app frontmost --json       # Get frontmost app
macpilot app list --json            # List running apps
macpilot app quit "Safari"          # Quit app
macpilot app quit "Safari" --force  # Force quit
macpilot app hide "Safari"          # Hide app
```

### Menu Interaction
```bash
macpilot menu click File Open --app Safari      # Click menu item
macpilot menu list --app Safari --json           # List all menus
macpilot menu list --app Safari --menu File      # List specific menu
```

### Clipboard
```bash
macpilot clipboard get --json              # Read clipboard text
macpilot clipboard set "text"              # Set clipboard text
macpilot clipboard image photo.png         # Copy image to clipboard
macpilot clipboard info --json             # Content type, size, preview
macpilot clipboard types --json            # List all UTI types
macpilot clipboard clear --json            # Clear clipboard
macpilot clipboard paste --json            # Simulate Cmd+V
macpilot clipboard copy file.txt --json    # Copy file(s) to clipboard
macpilot clipboard save /tmp/out.png       # Save clipboard content to file

# Clipboard history (background daemon, max 50 items)
macpilot clipboard history start --json    # Start tracking
macpilot clipboard history stop --json     # Stop tracking
macpilot clipboard history list --json     # Show history
macpilot clipboard history search "text"   # Search history
macpilot clipboard history clear --json    # Delete history
```

### Shell Commands
```bash
macpilot shell run "ls -la"                # Run command, get output
macpilot shell interactive "top"           # Open in Terminal
macpilot shell type "git status"           # Type into active terminal
macpilot shell paste "long command here"   # Paste via clipboard
```

### System Controls
```bash
macpilot audio volume get --json           # Get volume (0-100)
macpilot audio volume set 50               # Set volume
macpilot audio volume mute                 # Mute
macpilot display brightness set 75         # Set brightness
macpilot appearance dark                   # Dark mode
macpilot appearance light                  # Light mode
macpilot notification send "Title" "Body"  # System notification
macpilot notification list --json          # List visible notifications
macpilot notification click --title "match" # Click notification by title
macpilot notification dismiss --json       # Dismiss top notification
macpilot notification dismiss --all        # Dismiss all notifications
macpilot system info --json                # System info
macpilot network wifi-name --json          # Wi-Fi name
macpilot network ip --json                 # IP address
```

### Waiting & Synchronization
```bash
macpilot wait seconds 2                          # Sleep 2 seconds
macpilot wait element "Save" --app TextEdit       # Wait for UI element
macpilot wait window "Untitled" --timeout 10      # Wait for window
macpilot watch events --duration 5 --json         # Monitor events
```

### Spaces & Dock
```bash
macpilot space list --json                  # List spaces
macpilot space switch right                 # Switch space
macpilot dock hide                          # Auto-hide dock
macpilot dock show                          # Always show dock
```

## Critical Patterns

1. **Always focus the app before interacting**: `macpilot app focus "AppName"` must come before clicking, typing, or menu operations. The first click after focus may be consumed by window activation - click the app's content area first, then click the target.

2. **Use `--json` for parsing**: Always add `--json` when you need to parse output programmatically.

3. **Use `ui find-text` for coordinates**: When you need to click a specific element, first find its coordinates with `macpilot ui find-text "label" --app AppName --json`, then click at the returned position.

4. **Chain for complex sequences**: Use `macpilot chain` for multi-step keyboard workflows instead of multiple separate commands.

5. **AX value set over keyboard**: Setting text field values via `macpilot ui set-value` is more reliable than keyboard typing when focus is uncertain.

6. **Wait for elements**: Use `macpilot wait element` before interacting with UI elements that may not have appeared yet.

## Example Workflows

### Open a URL in Safari
```bash
macpilot app open Safari
macpilot wait window Safari --timeout 5
macpilot app focus Safari
macpilot keyboard key cmd+l
macpilot keyboard type "https://example.com"
macpilot keyboard key enter
```

### Copy text from one app to another
```bash
macpilot app focus "TextEdit"
macpilot keyboard key cmd+a
macpilot keyboard key cmd+c
macpilot app focus "Notes"
macpilot keyboard key cmd+v
```

### Create a new file in TextEdit
```bash
macpilot app open TextEdit
macpilot wait window TextEdit --timeout 5
macpilot keyboard type "Hello from MacPilot!"
macpilot keyboard key cmd+s
macpilot wait seconds 1
macpilot dialog navigate "/Users/me/Desktop"
macpilot dialog set-field "myfile.txt"
macpilot dialog click-button "Save"
```
