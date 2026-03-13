---
name: desktop-notifications
description: >
  Send desktop notifications from the terminal. Use this skill when the user wants
  to display system notifications, pipe command output to notifications, or get
  alerts after long-running operations complete. Supports cross-platform (Windows
  Toast, macOS osascript, Linux notify-send).
---

# Notify Skill

Send desktop notifications from the terminal.

## Installation Check

```bash
notify --help
```

If not installed:
```bash
uv tool install agentcli-helpers
```

## Usage

### Basic Notification
```bash
notify "Title" "Body message"
```

### Pipe Input
```bash
echo "Status update" | notify "Progress"
cat log.txt | notify "Logs"
```

### In Scripts
```bash
# After long operation
long_operation && notify "Done" "Operation completed successfully"
```

## Examples

```bash
# Simple alert
notify "Build Complete" "All tests passed!"

# With pipe
curl -s http://api/status | notify "API Status"

# Chain with other commands
find . -name "*.py" | wc -l | notify "File Count"
```

## Platform Support

- **Windows**: Uses Windows Toast notifications
- **macOS**: Uses osascript for native notifications
- **Linux**: Uses notify-send (libnotify)
