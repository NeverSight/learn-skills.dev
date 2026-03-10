---
name: ekctl
description: macOS calendar and reminder management via CLI using EventKit. Use when the user wants to list calendars, view events, create events, add reminders, mark reminders complete, or manage calendar aliases. Triggers on requests like "show my calendar", "add an event", "create a reminder", "what's on my schedule", "list my reminders", or any calendar/reminder management task.
---

# ekctl

CLI tool for managing macOS Calendar events and Reminders using EventKit.

## Installation

```bash
brew tap schappim/ekctl
brew install ekctl
```

Requires macOS 13.0 (Ventura) or later. Grant Calendar and Reminders permissions when prompted.

## Quick Reference

```bash
# List all calendars and reminder lists
ekctl list calendars

# List events (requires --from and --to in ISO8601)
ekctl list events --calendar <ID|alias> --from 2026-02-01T00:00:00Z --to 2026-02-07T23:59:59Z

# List reminders
ekctl list reminders --list <ID|alias>
ekctl list reminders --list <ID|alias> --completed false

# Add event
ekctl add event --calendar <ID|alias> --title "Meeting" --start 2026-02-03T09:00:00Z --end 2026-02-03T10:00:00Z
ekctl add event --calendar <ID|alias> --title "Vacation" --start 2026-02-10T00:00:00Z --end 2026-02-12T00:00:00Z --all-day

# Add reminder
ekctl add reminder --list <ID|alias> --title "Call mom"
ekctl add reminder --list <ID|alias> --title "Pay bills" --due 2026-02-05T17:00:00Z --priority 1

# Complete a reminder
ekctl complete reminder <reminder-id>

# Delete
ekctl delete event <event-id>
ekctl delete reminder <reminder-id>

# Aliases (use names instead of UUIDs)
ekctl alias set work "CALENDAR-UUID-HERE"
ekctl alias list
ekctl alias remove work
```

## Workflow

1. **First run**: List calendars to get IDs: `ekctl list calendars`
2. **Set aliases** for frequently used calendars: `ekctl alias set work <id>`
3. **Use aliases** in commands: `ekctl list events --calendar work --from ... --to ...`

## Quick Reminder Workflow

Adding a reminder requires a list ID. Here's the fastest path:

```bash
# 1. Find reminder lists (look for "type": "reminder")
ekctl list calendars

# 2. Add reminder with the list ID
ekctl add reminder --list "<LIST-ID>" --title "Do the thing" --due "2026-02-17T09:00:00Z"
```

**Choosing between multiple lists**: Users often have multiple "Reminders" lists from different sources (iCloud, Exchange, etc.). Prefer **iCloud** for personal reminders as it syncs across Apple devices.

**Pro tip**: Set an alias for your default reminder list to skip the lookup:
```bash
ekctl alias set reminders "YOUR-ICLOUD-REMINDERS-UUID"
# Then use: ekctl add reminder --list reminders --title "..."
```

## Required Parameters

These parameters are **mandatory** (not optional):

| Command | Required |
|---------|----------|
| `add reminder` | `--list`, `--title` |
| `add event` | `--calendar`, `--title`, `--start`, `--end` |
| `list events` | `--calendar`, `--from`, `--to` |
| `list reminders` | `--list` |

## ISO8601 Date Format

All dates **MUST** include the Z suffix: `YYYY-MM-DDTHH:MM:SSZ`

⚠️ **Common mistake**: Dates without `Z` will fail silently or error.

```bash
# ❌ WRONG - these will fail
--due "2026-02-17"
--due "2026-02-17T09:00:00"

# ✅ CORRECT - always include Z
--due "2026-02-17T09:00:00Z"
```

Examples:
- `2026-02-03T09:00:00Z` - 9 AM UTC on Feb 3, 2026
- `2026-02-03T00:00:00Z` - Midnight UTC on Feb 3, 2026

## Priority Values (Reminders)

- `0` - None
- `1` - High
- `5` - Medium
- `9` - Low

## Output

All commands return JSON with `"status": "success"` or `"status": "error"`.

## Time Management Best Practices

Follow these rules when helping users manage their calendar:

### Finding Available Slots

- **Check ALL calendars** when looking for free time—list calendars first, then query events from each one for the relevant time range
- **Look at the full week** when suggesting times, not just the requested day
- **Avoid fragmented gaps**—don't suggest a 30-min slot between two meetings; prefer contiguous free blocks
- **Respect working hours**—default to 9 AM - 6 PM unless the user specifies otherwise
- **Protect lunch**—avoid scheduling over 12 PM - 1 PM unless explicitly requested

### Scheduling Events

- **Add buffer time**—leave 10-15 minutes between meetings for context switching
- **Default to shorter durations**—suggest 30 minutes for meetings unless the user specifies longer
- **Group meetings together**—when suggesting times, prefer slots adjacent to existing meetings to preserve larger focus blocks
- **Morning for focus, afternoon for meetings**—when the user has flexibility, suggest meetings in the afternoon to protect morning deep work time

### Reminders

- **Set appropriate lead times** based on task type:
  - Video/phone calls: 5 minutes before
  - In-person meetings: 15-30 minutes before (account for travel)
  - Deadlines/tasks: 1 day before
- **Include travel time** for in-person meetings—ask about location and add buffer accordingly

### Weekly Review

When asked about schedule or availability:
- Summarize the week's commitments
- Highlight unusually busy days
- Note large free blocks available for deep work
