---
name: composio-calendar
description: |
  Google Calendar via Composio API. Use when:
  (1) Creating calendar events with correct durations
  (2) Finding/searching events
  (3) Updating or deleting events
  (4) Finding free time slots
  CRITICAL: CREATE and UPDATE use DIFFERENT duration parameters. This skill prevents the common 30-minute default bug.
---

# Google Calendar via Composio

## Critical: CREATE vs UPDATE Parameters

**This is the most common bug.** CREATE and UPDATE use different parameters for event duration:

| Action | Duration Method | Example |
|--------|----------------|---------|
| `GOOGLECALENDAR_CREATE_EVENT` | `event_duration_hour` + `event_duration_minutes` | `{"event_duration_hour": 2, "event_duration_minutes": 0}` |
| `GOOGLECALENDAR_UPDATE_EVENT` | `end_datetime` | `{"end_datetime": "2026-02-24T21:00:00"}` |
| `GOOGLECALENDAR_PATCH_EVENT` | `end_datetime` | `{"end_datetime": "2026-02-24T21:00:00"}` |

**If you pass `end_datetime` to CREATE, it is IGNORED and the event defaults to 30 minutes.**

## Environment

```bash
COMPOSIO_API_KEY      # API key
COMPOSIO_USER_ID      # Entity ID (required for all requests)
COMPOSIO_CONNECTIONS  # JSON with .googlecalendar connection ID
```

## Core Pattern

```bash
CONNECTION_ID=$(echo $COMPOSIO_CONNECTIONS | jq -r '.googlecalendar')

curl -s "https://backend.composio.dev/api/v3/tools/execute/ACTION_NAME" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {}
  }' | jq '.data'
```

## Creating Events

```bash
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLECALENDAR_CREATE_EVENT" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "title": "Work Block: API Docs",
      "start_datetime": "2026-02-24T09:00:00",
      "event_duration_hour": 2,
      "event_duration_minutes": 0,
      "timezone": "America/Los_Angeles",
      "description": "Focus time for API documentation",
      "calendar_id": "primary"
    }
  }' | jq
```

**Duration rules:**
- `event_duration_minutes`: 0-59 ONLY. Never use 60+.
- For 90 minutes: `event_duration_hour: 1, event_duration_minutes: 30`
- For 2 hours: `event_duration_hour: 2, event_duration_minutes: 0`

**Defaults:**
- `calendar_id`: "primary" if omitted
- `create_meeting_room`: true (adds Google Meet link)
- `timezone`: UTC if omitted

## Finding Events

```bash
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLECALENDAR_FIND_EVENT" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "text_query": "API Docs",
      "time_min": "2026-02-24T00:00:00Z",
      "time_max": "2026-02-25T00:00:00Z",
      "calendar_id": "primary"
    }
  }' | jq
```

Use `GOOGLECALENDAR_FIND_EVENT` to get `event_id` before updating or deleting.

## Updating Events

Use PATCH for partial updates (preferred), UPDATE for full replacement:

```bash
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLECALENDAR_PATCH_EVENT" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "event_id": "abc123",
      "calendar_id": "primary",
      "end_datetime": "2026-02-24T11:00:00"
    }
  }' | jq
```

**Note:** UPDATE replaces the entire event; unspecified fields may be cleared.

## Deleting Events

```bash
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLECALENDAR_DELETE_EVENT" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "event_id": "abc123",
      "calendar_id": "primary"
    }
  }' | jq
```

## Finding Free Slots

```bash
curl -s "https://backend.composio.dev/api/v3/tools/execute/GOOGLECALENDAR_FREE_BUSY" \
  -H "x-api-key: $COMPOSIO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "connected_account_id": "'$CONNECTION_ID'",
    "entity_id": "'$COMPOSIO_USER_ID'",
    "arguments": {
      "time_min": "2026-02-24T09:00:00Z",
      "time_max": "2026-02-24T18:00:00Z"
    }
  }' | jq
```

## Common Patterns

### Scheduling Multiple Work Blocks

When creating multiple events in sequence:
1. Calculate each `start_datetime` explicitly
2. Use `event_duration_hour` + `event_duration_minutes` for each
3. Account for breaks between blocks

Example: 3 two-hour blocks with 30-min breaks:
- Block 1: 9:00-11:00 (`start: 09:00, duration: 2h`)
- Block 2: 11:30-13:30 (`start: 11:30, duration: 2h`)
- Block 3: 14:00-16:00 (`start: 14:00, duration: 2h`)

### Fixing Duration After Creation

If events were created with wrong duration:
1. Find events: `GOOGLECALENDAR_FIND_EVENT`
2. Patch each: `GOOGLECALENDAR_PATCH_EVENT` with correct `end_datetime`

## Datetime Formats

- ISO 8601: `YYYY-MM-DDTHH:MM:SS` (e.g., `2026-02-24T09:00:00`)
- With timezone: `2026-02-24T09:00:00-08:00` or use `timezone` param
- **Natural language NOT supported**: "tomorrow", "next Monday" will be rejected

## All Actions

See [references/actions.md](references/actions.md) for complete API reference.

## Discover Actions

```bash
curl -s "https://backend.composio.dev/api/v2/actions?apps=googlecalendar" \
  -H "x-api-key: $COMPOSIO_API_KEY" | jq '.items[] | {name, description}'
```
