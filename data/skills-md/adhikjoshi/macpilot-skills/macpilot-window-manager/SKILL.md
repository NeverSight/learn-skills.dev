---
name: macpilot-window-manager
description: Manage macOS windows with MacPilot. List, move, resize, snap, minimize, fullscreen, and arrange application windows. Supports multi-display and Spaces.
---

# MacPilot Window Manager

Use MacPilot to control application windows on macOS - list, move, resize, snap to positions, minimize, fullscreen, and manage across Spaces and displays.

## When to Use

Use this skill when:
- You need to arrange or organize application windows
- You need to move/resize windows to specific positions
- You need to snap windows to screen halves or corners
- You need to list what windows are open
- You need to focus or bring a specific window to front
- You need to manage windows across multiple Spaces/desktops
- You need to save and restore window layouts

## Window Commands

### List Windows
```bash
macpilot window list --json                        # All visible windows
macpilot window list --app "Safari" --json         # Windows for specific app
macpilot window list --all-spaces --json           # Include all Spaces
```

### Focus Window
```bash
macpilot window focus "Safari" --json                          # Focus app's main window
macpilot window focus "Safari" --title "GitHub" --json         # Focus by title substring
```

### New Window
```bash
macpilot window new "Safari" --json                # Open new window in app
```

### Move Window
```bash
macpilot window move "Safari" 100 50 --json        # Move to x=100, y=50
```

### Resize Window
```bash
macpilot window resize "Safari" 1200 800 --json    # Set width=1200, height=800
```

### Close Window
```bash
macpilot window close --app "Safari" --json        # Close frontmost window
```

### Minimize / Fullscreen
```bash
macpilot window minimize "Safari" --json           # Minimize to Dock
macpilot window fullscreen "Safari" --json         # Toggle fullscreen
```

### Snap to Position
```bash
macpilot window snap "Safari" left --json          # Left half of screen
macpilot window snap "Safari" right --json         # Right half of screen
macpilot window snap "Safari" top-left --json      # Top-left quarter
macpilot window snap "Safari" top-right --json     # Top-right quarter
macpilot window snap "Safari" bottom-left --json   # Bottom-left quarter
macpilot window snap "Safari" bottom-right --json  # Bottom-right quarter
macpilot window snap "Safari" center --json        # Center of screen
macpilot window snap "Safari" maximize --json      # Fill entire screen
```

### Save / Restore Layout
```bash
macpilot window restore --save --json              # Save all window positions
macpilot window restore --json                     # Restore saved positions
macpilot window restore --save --app "Safari"      # Save specific app only
```

## Spaces / Desktops

```bash
macpilot space list --json                         # List all Spaces
macpilot space switch left --json                  # Switch to left Space
macpilot space switch right --json                 # Switch to right Space
macpilot space switch 2 --json                     # Switch to Space 2
macpilot space bring --app "Slack" --json          # Bring app to current Space
```

## Workflow Patterns

### Side-by-Side Layout
```bash
macpilot window snap "Safari" left
macpilot window snap "VS Code" right
```

### Quarter Layout (4 Apps)
```bash
macpilot window snap "Safari" top-left
macpilot window snap "Terminal" top-right
macpilot window snap "Finder" bottom-left
macpilot window snap "Notes" bottom-right
```

### Presentation Setup
```bash
# Maximize the presentation app
macpilot window snap "Keynote" maximize
# Or go fullscreen
macpilot window fullscreen "Keynote"
```

### Dev Environment Layout
```bash
# Editor on left 60%, terminal on right 40%
macpilot window move "VS Code" 0 25
macpilot window resize "VS Code" 1152 775
macpilot window move "Terminal" 1152 25
macpilot window resize "Terminal" 768 775
```

### Collect All Windows
```bash
# Bring scattered windows back to current Space
macpilot space bring --app "Safari"
macpilot space bring --app "Terminal"
macpilot space bring --app "Finder"
```

### Save and Restore Workspace
```bash
# Before a meeting - save your layout
macpilot window restore --save

# After the meeting - restore it
macpilot window restore
```

## Tips

- Use `window list --json` to see current positions/sizes before rearranging
- The `snap` command uses the display where the window currently resides
- `window focus` is preferred over `app focus` when multiple windows exist
- Use `display-info --json` to get screen dimensions for precise positioning
- Coordinates use top-left origin (0,0 is top-left of primary display)
- On multi-monitor setups, secondary displays may have negative x coordinates (left of primary) or x > primary width (right of primary)
