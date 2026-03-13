---
name: google-calendar
description: Google Calendar API for scheduling. Use when user mentions "calendar",
  "calendar.google.com", shares a calendar link, "schedule meeting", "check availability",
  or "when am I free".
vm0_secrets:
  - GOOGLE_CALENDAR_TOKEN
---

# Google Calendar API

Manage calendars and events via Google's Calendar REST API.

> Official docs: https://developers.google.com/workspace/calendar/api/v3/reference

---

## When to Use

Use this skill when you need to:

- List and manage calendars
- Create, update, and delete calendar events
- Search and filter events by time range
- Manage event attendees and send invitations
- Set up event reminders
- Check free/busy availability
- Handle recurring events
- Quick-add events using natural language

---

## Prerequisites

Go to [vm0.ai](https://vm0.ai) **Settings → Connectors** and connect **Google Calendar**. vm0 will automatically inject the required `GOOGLE_CALENDAR_TOKEN` environment variable.

---

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

> **Placeholders:** Values in `{curly-braces}` like `{event-id}` are placeholders. Replace them with actual values when executing.

---

## How to Use

Base URL: `https://www.googleapis.com/calendar/v3`

---

## Calendar List

### List All Calendars

Get all calendars the user has access to:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/users/me/calendarList" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.items[]? | {id, summary, primary, accessRole}'
```

### Get Calendar Details

Get metadata for a specific calendar:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/{calendar-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '{id, summary, description, timeZone}'
```

For primary calendar, use `primary` as the calendar ID:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/primary" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '{id, summary, description, timeZone}'
```

---

## Events

### List Events

List upcoming events from the primary calendar:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?maxResults=10&orderBy=startTime&singleEvents=true&timeMin=$(date -u +%Y-%m-%dT%H:%M:%SZ)" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.items[]? | {id, summary, start, end}'
```

### List Events with Time Filter

Get events within a specific date range:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=2024-01-01T00:00:00Z&timeMax=2024-12-31T23:59:59Z&singleEvents=true&orderBy=startTime" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.items[]? | {id, summary, start, end}'
```

### Search Events

Search events by query string:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?q=meeting&singleEvents=true" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.items[]? | {id, summary, start, end}'
```

### Get Event Details

Get full details for a specific event:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.'
```

### Create Event

Create a new event. Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Team Meeting",
  "description": "Weekly sync-up meeting",
  "location": "Conference Room A",
  "start": {
    "dateTime": "2024-03-15T10:00:00",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2024-03-15T11:00:00",
    "timeZone": "America/New_York"
  },
  "attendees": [
    {
      "email": "colleague@example.com"
    }
  ],
  "reminders": {
    "useDefault": false,
    "overrides": [
      {
        "method": "email",
        "minutes": 30
      },
      {
        "method": "popup",
        "minutes": 10
      }
    ]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, htmlLink}'
```

### Create All-Day Event

Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Company Holiday",
  "start": {
    "date": "2024-07-04"
  },
  "end": {
    "date": "2024-07-05"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, htmlLink}'
```

### Quick Add Event

Create event from natural language text:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events/quickAdd?text=Lunch%20with%20Sarah%20tomorrow%20at%2012pm" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.error // {id, summary, start, end}'
```

### Update Event

Update an existing event. Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Updated Team Meeting",
  "description": "Updated description",
  "start": {
    "dateTime": "2024-03-15T14:00:00",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2024-03-15T15:00:00",
    "timeZone": "America/New_York"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, updated}'
```

### Patch Event

Partially update an event (only specified fields). Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Updated Title Only"
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, updated}'
```

### Delete Event

Delete an event:

```bash
bash -c 'curl -s -X DELETE "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"'
```

Send deletion notifications to attendees:

```bash
bash -c 'curl -s -X DELETE "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}?sendUpdates=all" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"'
```

---

## Attendees

### Set Attendees on Event

> **Note:** PATCH replaces the entire attendees array — always include all intended attendees in the list, not just the ones you're adding.

Write the full attendees list to `/tmp/calendar_request.json`:

```json
{
  "attendees": [
    {
      "email": "attendee1@example.com",
      "optional": false
    },
    {
      "email": "attendee2@example.com",
      "optional": true
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}?sendUpdates=all" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, attendees}'
```

### Remove Attendee from Event

Patch the event with the updated attendees list (omit the attendee you want to remove). Write to `/tmp/calendar_request.json`:

```json
{
  "attendees": [
    {
      "email": "remaining@example.com"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}?sendUpdates=all" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, attendees}'
```

---

## Reminders

### Set Custom Reminders

Update event with custom reminders. Write to `/tmp/calendar_request.json`:

```json
{
  "reminders": {
    "useDefault": false,
    "overrides": [
      {
        "method": "email",
        "minutes": 1440
      },
      {
        "method": "popup",
        "minutes": 30
      }
    ]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, reminders}'
```

### Use Default Reminders

Write to `/tmp/calendar_request.json`:

```json
{
  "reminders": {
    "useDefault": true
  }
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, reminders}'
```

---

## Recurring Events

### Create Recurring Event

Create an event with recurrence rule. Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Weekly Team Standup",
  "start": {
    "dateTime": "2024-03-15T09:00:00",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2024-03-15T09:30:00",
    "timeZone": "America/New_York"
  },
  "recurrence": [
    "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;COUNT=20"
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, recurrence, htmlLink}'
```

Common recurrence patterns:
- Daily: `RRULE:FREQ=DAILY`
- Weekly on specific days: `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR`
- Monthly on same day: `RRULE:FREQ=MONTHLY;BYMONTHDAY=15`
- Until specific date: `RRULE:FREQ=WEEKLY;UNTIL=20241231T235959Z`
- Limited occurrences: `RRULE:FREQ=DAILY;COUNT=10`

### List Recurring Event Instances

Get all instances of a recurring event:

```bash
bash -c 'curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events/{recurring-event-id}/instances?timeMin=2024-01-01T00:00:00Z&timeMax=2024-12-31T23:59:59Z" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"' | jq '.items[]? | {id, summary, start, end, recurringEventId}'
```

---

## Free/Busy Information

### Query Free/Busy

Check availability for one or more calendars. Write to `/tmp/calendar_request.json`:

```json
{
  "timeMin": "2024-03-15T00:00:00Z",
  "timeMax": "2024-03-15T23:59:59Z",
  "items": [
    {
      "id": "primary"
    },
    {
      "id": "colleague@example.com"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/calendar/v3/freeBusy" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // .calendars'
```

---

## Secondary Calendars

### Create Secondary Calendar

Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Project Alpha Calendar",
  "description": "Calendar for Project Alpha events",
  "timeZone": "America/New_York"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, description}'
```

### Update Calendar Properties

Write to `/tmp/calendar_request.json`:

```json
{
  "summary": "Updated Calendar Name",
  "description": "Updated description"
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/{calendar-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, description}'
```

### Delete Secondary Calendar

```bash
bash -c 'curl -s -X DELETE "https://www.googleapis.com/calendar/v3/calendars/{calendar-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN"'
```

---

## Event Colors

### Set Event Color

Update event color using colorId (1-11). Write to `/tmp/calendar_request.json`:

```json
{
  "colorId": "5"
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/{event-id}" --header "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" --header "Content-Type: application/json" -d @/tmp/calendar_request.json' | jq '.error // {id, summary, colorId}'
```

Available color IDs:
- 1: Lavender
- 2: Sage
- 3: Grape
- 4: Flamingo
- 5: Banana
- 6: Tangerine
- 7: Peacock
- 8: Graphite
- 9: Blueberry
- 10: Basil
- 11: Tomato

---

## Common Query Parameters

| Parameter | Type | Purpose |
|-----------|------|---------|
| `timeMin` | datetime | Lower bound for event end time (RFC3339) |
| `timeMax` | datetime | Upper bound for event start time (RFC3339) |
| `maxResults` | integer | Max events per page (default 250, max 2500) |
| `orderBy` | string | Sort by `startTime` or `updated` |
| `singleEvents` | boolean | Expand recurring events into instances |
| `q` | string | Free text search query |
| `sendUpdates` | string | Send notifications: `all`, `externalOnly`, `none` |

---

## Guidelines

1. **Primary Calendar**: Use `primary` as the calendar ID for the user's primary calendar
2. **Date Format**: Use RFC3339 format for dates (`2024-03-15T10:00:00Z` or with timezone `2024-03-15T10:00:00-04:00`)
3. **All-Day Events**: Use `date` field instead of `dateTime` for all-day events
4. **Notifications**: Use `sendUpdates` parameter to control whether attendees receive email notifications
5. **Patch vs Update**: Use PATCH for partial updates (more efficient), PUT for full replacement. Note: PATCH on `attendees` replaces the entire array — always include all intended attendees
6. **Time Zones**: Always specify time zones explicitly to avoid ambiguity
7. **Recurring Events**: To modify all instances, update the recurring event master; to modify single instance, update the specific instance ID

---

## API Reference

- REST Reference: https://developers.google.com/workspace/calendar/api/v3/reference
- Events Reference: https://developers.google.com/workspace/calendar/api/v3/reference/events
- OAuth Scopes: https://developers.google.com/workspace/calendar/api/auth
- OAuth Playground: https://developers.google.com/oauthplayground/
- Recurrence Rules: https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5
