---
name: feishu-calendar
description: Manage Feishu calendar with automatic user authorization. Create, read, update, and delete calendar events. List upcoming events, check availability, and manage your calendar programmatically with automatic token refresh.
---

# Feishu Calendar

Manage your Feishu calendar with automatic user authorization. Create, update, delete, and query calendar events.

## Quick Start

### Create an Event

```bash
bash scripts/create_event.sh "Event Title" "2026-02-01 10:00:00" "2026-02-01 11:00:00" "Description"
```

Returns event ID and link.

### List Today's Events

```bash
bash scripts/list_events.sh
```

### Get Event Details

```bash
bash scripts/get_event.sh <event_id>
```

### Update an Event

```bash
bash scripts/update_event.sh <event_id> "New Title" "2026-02-01 14:00:00" "2026-02-01 15:00:00"
```

### Delete an Event

```bash
bash scripts/delete_event.sh <event_id>
```

## Setup

### Prerequisites

- User must authorize with Feishu OAuth (one-time)
- Credentials stored at `~/.feishu-credentials.json`
- Required permissions: `calendar:calendar calendar:event offline_access`

### Verify Setup

```bash
bash scripts/verify_setup.sh
```

## Scripts

| Script | Purpose |
|--------|---------|
| `create_event.sh` | Create a new calendar event |
| `list_events.sh` | List events (today or date range) |
| `get_event.sh` | Get event details |
| `update_event.sh` | Update event title/time |
| `delete_event.sh` | Delete an event |
| `verify_setup.sh` | Check credentials and permissions |

## Important Notes

### Event Ownership

- Events are created in **your personal calendar**
- You own all events created through this Skill
- Automatic token refresh keeps events accessible long-term
- Your identity: `ou_1f553aa193ea382ef8239c16dee55fed`

### DateTime Format

All scripts use ISO 8601 format with time zone support:
- Format: `YYYY-MM-DD HH:MM:SS` (assumes your local time)
- Example: `2026-02-01 14:30:00`

### Event IDs

- Event IDs are used for updates and deletions
- Returned when creating events
- Can also be retrieved via `list_events.sh`

## Examples

### Create a meeting

```bash
bash scripts/create_event.sh \
  "Team Sync" \
  "2026-02-01 10:00:00" \
  "2026-02-01 11:00:00" \
  "Weekly team synchronization meeting"
```

### List all events this week

```bash
bash scripts/list_events.sh "2026-01-31" "2026-02-07"
```

### Update an event

```bash
bash scripts/update_event.sh "event_id_here" \
  "Updated Title" \
  "2026-02-02 15:00:00" \
  "2026-02-02 16:00:00"
```

## Troubleshooting

### "Permission denied" error

Run `verify_setup.sh` to check credentials and permissions.

### Event not found

Verify the event ID is correct. Use `list_events.sh` to find event IDs.

### Token errors

The Skill automatically refreshes tokens. If you see authorization errors, re-authorize through the OAuth flow.

## References

- [Feishu Calendar API Documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/calendar-v4/calendar/introduction)
- [Event Management](references/event-api.md) - Event creation, update, and deletion details
