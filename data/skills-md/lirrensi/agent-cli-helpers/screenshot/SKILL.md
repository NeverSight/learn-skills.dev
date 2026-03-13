---
name: screenshot
description: >
  Take screenshots from the terminal using the screenshot CLI tool.
  Use this skill when the user wants to capture the screen or a region,
  save screenshots to files, or integrate screenshot capture into scripts.
  Supports cross-platform (Windows/macOS/Linux) with automatic fallback to native tools.
---

# Screenshot Skill

Take screenshots from the terminal.

## Installation Check

```bash
screenshot --help
```

If not installed:
```bash
uv tool install agentcli-helpers
```

## Usage

### Auto-named Screenshot
```bash
screenshot
# Outputs: C:\Users\...\Temp\agentcli_screenshots\screenshot_20260305_160405.png
```

### Named Screenshot
```bash
screenshot output.png
screenshot /path/to/screenshot.png
```

## Output

The command outputs the path to the saved screenshot, making it easy to use in scripts:

```bash
# Capture and open
screenshot | xargs open

# Capture and send
screenshot | xargs curl -F "image=@-" http://api/upload

# Capture with timestamp
SCREENSHOT=$(screenshot)
echo "Saved to: $SCREENSHOT"
```

## Examples

```bash
# Quick capture
screenshot

# Save to specific location
screenshot ~/Desktop/bug_report.png

# In a script
screenshot "/tmp/screenshot_$(date +%s).png"

# Capture and notify
notify "Screenshot" "$(screenshot)"
```

## Platform Support

Uses the `mss` library for cross-platform screenshots:
- **Windows**: Direct screen capture
- **macOS**: Direct screen capture
- **Linux**: Direct screen capture (X11/Wayland)

If `mss` is not available, falls back to native tools:
- **Linux**: gnome-screenshot, scrot, import, flameshot
- **macOS**: screencapture
- **Windows**: PowerShell with .NET
