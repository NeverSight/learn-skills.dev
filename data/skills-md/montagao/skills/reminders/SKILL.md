---
name: reminders
description: Internal helper for creating and managing reminders/notifications.
user-invocable: false
---

# reminders (internal)

Create recurring or one-time reminders that send messages to a channel.

## Input contract (JSON)

### Create recurring reminder
{
  "action": "create_recurring",
  "name": "Daily plan",
  "schedule": "Every day at 07:30",
  "timezone": "Australia/Melbourne",
  "deliver": { "channel": "telegram", "to": "..." },
  "message": "/plan",
  "suppressIf": "HEARTBEAT_OK (optional)"
}

### Create one-time reminder
{
  "action": "create_once",
  "name": "...",
  "runAt": "YYYY-MM-DDTHH:mm",
  "timezone": "Australia/Melbourne",
  "deliver": { "channel": "telegram", "to": "..." },
  "message": "..."
}

### List reminders
{ "action": "list" }

### Update reminder
{
  "action": "update",
  "id": "...",
  "patch": { "schedule": "...", "message": "...", "deliver": {...} }
}

### Delete reminder
{ "action": "delete", "id": "..." }

## Behavior
- Never asks user questions.
- Returns JSON only.
- If `suppressIf` is provided, do not deliver when output is exactly that string.

## Output
{ "ok": true, "action": "create_recurring", "id": "..." }
