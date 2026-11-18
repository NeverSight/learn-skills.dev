---
name: google-calendar
description: Create, list, and manage Google Calendar events. Use when asked to schedule meetings, check calendar, create events, or manage appointments. For pre-meeting intelligence briefings, see meeting-prep.
---

# Google Calendar

Create, list, find, and manage events in Google Calendar. Connect your Google account to schedule meetings, check availability, and manage your calendar programmatically.

## Requirements

- Install the `orth` CLI
- Connect your Google Calendar at https://orthogonal.com/dashboard/integrations
- OAuth connection must be active (HTTP 428 response means not connected)

## Actions

### Create Event

Schedule a new calendar event with attendees and settings.

```bash
orth run google-calendar /create-event --body '{
  "start_datetime": "2024-03-15T14:00:00",
  "summary": "Team Meeting",
  "description": "Weekly team sync",
  "event_duration_hour": 1
}'
```

**Parameters:**
- `start_datetime` (required) - Event start time in "YYYY-MM-DDTHH:MM:SS" format (NO timezone)
- `summary` - Event title/summary
- `description` - Event description/details
- `location` - Event location or meeting room
- `timezone` - IANA timezone (e.g., "America/New_York")
- `attendees` - Array of attendee email addresses
- `event_duration_hour` - Duration in hours
- `event_duration_minutes` - Duration in minutes (0-59 only)
- `recurrence` - Recurrence rule (RRULE format)
- `visibility` - Event visibility (default, public, private)
- `calendar_id` - Specific calendar to create event in
- `send_updates` - Send email invitations (true/false)
- `transparency` - Show as busy/free (opaque/transparent)
- `exclude_organizer` - Exclude organizer from attendee list (true/false)
- `guests_can_modify` - Allow guests to modify event (true/false)
- `create_meeting_room` - Create Google Meet room (requires paid Workspace)
- `eventType` - Event type classification
- `guestsCanInviteOthers` - Allow guests to invite others (true/false)
- `guestsCanSeeOtherGuests` - Allow guests to see other attendees (true/false)

### List Events

Retrieve events from your calendar within a time range.

```bash
orth run google-calendar /list-events --body '{
  "calendarId": "primary",
  "timeMin": "2024-03-01T00:00:00Z",
  "maxResults": 10
}'
```

**Parameters:**
- `calendarId` (required) - Calendar ID to query ("primary" for main calendar)
- `timeMin` - Start time filter (RFC3339 format)
- `timeMax` - End time filter (RFC3339 format)
- `q` - Text search query
- `orderBy` - Sort order (startTime, updated)
- `maxResults` - Maximum events to return
- `pageToken` - Token for pagination
- `singleEvents` - Expand recurring events (true/false)
- `showDeleted` - Include deleted events (true/false)
- `timeZone` - Timezone for results
- `eventTypes` - Filter by event types
- `updatedMin` - Only events updated after this time
- `maxAttendees` - Maximum attendees to return per event
- `syncToken` - Sync token for incremental sync
- `showHiddenInvitations` - Include hidden invitations (true/false)

### Find Event

Search for specific events by query and filters.

```bash
orth run google-calendar /find-event --body '{
  "query": "team meeting",
  "timeMin": "2024-03-01T00:00:00Z"
}'
```

**Parameters:**
- `query` - Search query text
- `timeMin` - Search start time (RFC3339 format)
- `timeMax` - Search end time (RFC3339 format)
- `calendar_id` - Specific calendar to search
- `order_by` - Sort results (startTime, updated)
- `max_results` - Maximum results to return
- `single_events` - Expand recurring events (true/false)
- `show_deleted` - Include deleted events (true/false)
- `event_types` - Filter by event types
- `page_token` - Token for pagination
- `updated_min` - Only events updated after this time

### Delete Event

Remove an event from your calendar.

```bash
orth run google-calendar /delete-event --body '{
  "event_id": "EVENT_ID_HERE"
}'
```

**Parameters:**
- `event_id` (required) - Google Calendar event ID to delete
- `calendar_id` - Calendar containing the event (defaults to primary)

## Usage Examples

**Schedule a 1-hour meeting:**
```bash
orth run google-calendar /create-event -b '{"start_datetime":"2024-03-15T14:00:00","summary":"Client Call","event_duration_hour":1,"attendees":["client@company.com"]}'
```

**Create recurring weekly meeting:**
```bash
orth run google-calendar /create-event -b '{"start_datetime":"2024-03-15T10:00:00","summary":"Weekly Standup","event_duration_minutes":30,"recurrence":"RRULE:FREQ=WEEKLY;BYDAY=FR"}'
```

**Check today's events:**
```bash
orth run google-calendar /list-events -b '{"calendarId":"primary","timeMin":"2024-03-15T00:00:00Z","timeMax":"2024-03-15T23:59:59Z"}'
```

**Search for meetings:**
```bash
orth run google-calendar /find-event -b '{"query":"team meeting","timeMin":"2024-03-01T00:00:00Z"}'
```

**Cancel an event:**
```bash
orth run google-calendar /delete-event -b '{"event_id":"abc123def456ghi789"}'
```

## Error Handling

- **HTTP 428** - Google Calendar integration not connected. Visit https://orthogonal.com/dashboard/integrations to connect your account
- **400 Bad Request** - Invalid datetime format or missing required parameters
- **403 Forbidden** - Insufficient calendar permissions
- **404 Not Found** - Event or calendar does not exist
- **409 Conflict** - Event conflicts with existing event
- **429 Rate Limited** - Too many requests, wait before retrying

## Tips

- Use "primary" as calendarId for your main calendar
- DateTime format must be "YYYY-MM-DDTHH:MM:SS" without timezone
- Set timezone separately using the timezone parameter
- Duration can be specified in hours and/or minutes
- Recurring events use RRULE syntax (e.g., "RRULE:FREQ=WEEKLY")
- Use timeMin/timeMax in RFC3339 format for filtering
- Google Meet rooms require paid Google Workspace
- Event IDs are returned from create/list operations

## Related Skills

- **meeting-prep** — automated pre-meeting briefings using calendar events
- **discovery-debrief** — structured debrief after meetings