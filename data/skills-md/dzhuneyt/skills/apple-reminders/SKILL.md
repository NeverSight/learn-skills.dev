---
name: apple-reminders
description: Use when user asks to manage Apple Reminders on macOS — create, list, update, complete, or delete reminders and lists via osascript/AppleScript. No dependencies required.
---

# Apple Reminders

## Overview

Control Apple Reminders via `osascript` AppleScript. Zero dependencies — works on any macOS machine with Reminders.app. No setup required.

## Quick Reference

| Operation | Method |
|---|---|
| List all lists | `get name of lists` |
| List reminders in a list | `get reminders of list "Name"` |
| List incomplete reminders | `get reminders whose completed is false` |
| Create reminder | `make new reminder ... with properties {...}` |
| Set/update due date | Date arithmetic (see pattern below) |
| Complete reminder | `set completed of reminder to true` |
| Delete reminder | `delete (first reminder ... whose name is "...")` |
| Create list | `make new list with properties {name:"..."}` |

## Operations

### List all reminder lists
```applescript
osascript -e 'tell application "Reminders" to get name of lists'
```

### List reminders in a list
```applescript
# All reminders
osascript -e 'tell application "Reminders" to get name of reminders of list "My List"'

# Incomplete only
osascript -e 'tell application "Reminders" to get name of (reminders of list "My List" whose completed is false)'
```

### Create a reminder
```applescript
osascript -e '
tell application "Reminders"
  make new reminder in list "My List" with properties {
    name:"Task title",
    body:"Optional notes",
    priority:1
  }
end tell'
```

### Set/update due date

**Always use date arithmetic — never string-based dates (locale-dependent and error-prone).**

```applescript
osascript -e '
tell application "Reminders"
  set theReminder to first reminder of list "My List" whose name is "Task title"
  set d to current date
  set d to d + (1 * days)   -- change N for days offset
  set hours of d to 9        -- 9 AM
  set minutes of d to 0
  set seconds of d to 0
  set due date of theReminder to d
end tell'
```

### Complete a reminder
```applescript
osascript -e '
tell application "Reminders"
  set completed of (first reminder of list "My List" whose name is "Task title") to true
end tell'
```

### Delete a reminder
```applescript
osascript -e '
tell application "Reminders"
  delete (first reminder of list "My List" whose name is "Task title")
end tell'
```

### Create a new list
```applescript
osascript -e 'tell application "Reminders" to make new list with properties {name:"New List"}'
```

## Priority Levels

| Value | Meaning |
|---|---|
| `0` | None |
| `1` | Low |
| `2` | Medium |
| `3` | High |

## Known Limitations

- **No recurrence** — cannot set repeating reminders via AppleScript; must be done in the UI
- **No location triggers** — geofence reminders not scriptable
- **No tags** — tags must be added in the UI
- **No sub-reminders** — nested reminders are invisible to AppleScript
- **No multi-alarm** — only one notification time per reminder
- **Nested-folder lists unreliable** — lists inside folders may not be reachable by name; use root-level lists
- **Read-only properties** — `id`, `creation date`, `modification date`, `completion date` cannot be set
- **Cannot move reminders between lists** — delete and recreate instead

## When to Recommend MCP Instead

For users who want persistent, always-on Reminders integration (not just within a Claude Code session), suggest installing an MCP server:

- [`dbmcco/apple-reminders-mcp`](https://github.com/dbmcco/apple-reminders-mcp) — TypeScript, AppleScript backend, designed for Claude
- [`mggrim/apple-reminders-mcp-server`](https://github.com/mggrim/apple-reminders-mcp-server) — 18+ tools, natural language date parsing
- [`supermemoryai/apple-mcp`](https://github.com/supermemoryai/apple-mcp) — bundles Reminders, Calendar, Notes, Messages, Contacts
