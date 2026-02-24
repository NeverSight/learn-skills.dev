---
name: m365
description: Use this skill when the user asks about Microsoft 365 email or calendar - reading, searching, sending Outlook emails, viewing calendar events, scheduling meetings, or managing M365 data.
---

# Microsoft 365 via CLI for Microsoft 365

This skill uses the `m365` CLI (CLI for Microsoft 365) to interact with Outlook email and calendar via the Microsoft Graph API. It works cross-platform (macOS, Linux, Windows).

## Connection Check

Before doing anything, run these two commands in parallel:

```bash
m365 status --output json
m365 connection list --output json
```

If the active connection already has `"authType": "secret"`, proceed to the task.

If the active connection has a different auth type (e.g. `deviceCode`), check `connection list` for an inactive connection with `"authType": "secret"`. If one exists, activate it:

```bash
m365 connection use --name "<connection-name>"
```

Only if no `secret` connection exists at all, read `./setup.md` (relative to this file) and follow the setup steps.

All commands that target a user's mailbox require `--userName <upn>` (built-in commands) or the user principal name in the Graph API URL. Ask the user for their UPN (e.g. `user@company.com`) if not known.

## Important Notes

- ALWAYS confirm with the user before any write action (send email, create/delete event).
- The CLI has built-in commands for email but NOT for calendar events. Use `m365 request` with Graph API URLs for calendar operations.
- Use `--output json` for machine-readable output. Use `--query` (JMESPath) to filter fields.
- Every command supports `-h` / `--help`. Use `m365 <command group> --help` to discover commands.

## Email

### List messages

```bash
m365 outlook message list --folderName inbox --userName <upn> --output json

# With date range (endTime must be in the past)
m365 outlook message list --folderName inbox --userName <upn> \
  --startTime "2026-02-01T00:00:00Z" --endTime "2026-02-15T00:00:00Z" --output json

# Compact output with JMESPath
m365 outlook message list --folderName inbox --userName <upn> --output json \
  --query "[].{subject:subject,from:from.emailAddress.address,received:receivedDateTime,isRead:isRead}"
```

Folder names: `inbox`, `drafts`, `sentitems`, `deleteditems`, `junkemail`, `archive`. You can also use `--folderId`.

### Read a specific message

```bash
m365 outlook message get --id <message-id> --userName <upn> --output json
```

### Search emails (via Graph API)

The built-in `message list` does not support search. Use `m365 request` with `$search` or `$filter`:

```bash
# Full-text search (subject, body, sender, etc.)
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/messages?\$search=%22keyword%22&\$select=subject,from,receivedDateTime&\$top=10" --method get --output json

# Filter by sender
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/messages?\$filter=from/emailAddress/address eq 'someone@example.com'&\$select=subject,receivedDateTime&\$top=10" --method get --output json
```

Note: `$search` and `$orderby` cannot be combined. Results from `$search` are ranked by relevance.

### List mail folders

```bash
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/mailFolders?\$select=displayName,id,totalItemCount,unreadItemCount" --method get --output json
```

### Send email

```bash
# Plain text
m365 outlook mail send --subject "Subject" --to "recipient@example.com" \
  --sender "<upn>" --bodyContents "Message body" --output json

# HTML with multiple recipients
m365 outlook mail send --subject "Subject" --to "a@example.com,b@example.com" \
  --cc "c@example.com" --sender "<upn>" \
  --bodyContents "<p>HTML body</p>" --bodyContentType HTML --output json

# With attachment (max 3 MB per attachment)
m365 outlook mail send --subject "Subject" --to "recipient@example.com" \
  --sender "<upn>" --bodyContents "See attached." \
  --attachment "/path/to/file.pdf" --output json

# Send from shared mailbox
m365 outlook mail send --subject "Subject" --to "recipient@example.com" \
  --mailbox "shared@company.com" --sender "<upn>" \
  --bodyContents "Sent from shared mailbox" --output json
```

### Reply to email (via Graph API)

The CLI has no built-in reply command. Use `m365 request` with the Graph API reply endpoint:

```bash
# Reply to sender only (plain text comment)
cat > /tmp/m365_reply.json << 'EOF'
{
  "comment": "Thanks, that works for me!"
}
EOF

m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/messages/<message-id>/reply" \
  --method post --body @/tmp/m365_reply.json --content-type "application/json"

# Reply all
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/messages/<message-id>/replyAll" \
  --method post --body @/tmp/m365_reply.json --content-type "application/json"

# Reply with HTML body and additional recipients
cat > /tmp/m365_reply.json << 'EOF'
{
  "message": {
    "toRecipients": [
      {"emailAddress": {"address": "extra@example.com", "name": "Extra Recipient"}}
    ]
  },
  "comment": "<p>Replying with <b>HTML</b> content.</p>"
}
EOF

m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/messages/<message-id>/reply" \
  --method post --body @/tmp/m365_reply.json --content-type "application/json"
```

The Graph API handles threading, quoting the original message, and setting recipients automatically. Use `comment` for the reply text. Optionally include a `message` object to add/override recipients. Returns `202 Accepted` with no body on success. Requires `Mail.Send` permission.

### Move / archive messages

```bash
m365 outlook message move --id <message-id> \
  --sourceFolderName inbox --targetFolderName archive --output json
```

## Calendar

Calendar operations use `m365 request` with Microsoft Graph API endpoints. For POST/PUT/PATCH requests, write the JSON body to a temp file and pass it with `--body @/path/to/file.json --content-type "application/json"`.

### List calendars

```bash
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/calendars?\$select=name,id,canEdit,isDefaultCalendar" --method get --output json
```

### List upcoming events (calendar view)

Use `calendarView` for events in a date range (expands recurring events):

```bash
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/calendarView?\$select=subject,start,end,location,organizer,isAllDay&startDateTime=2026-02-17T00:00:00Z&endDateTime=2026-02-24T00:00:00Z&\$orderby=start/dateTime" --method get --output json
```

### Get event details (with attendees)

```bash
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/events/<event-id>?\$select=subject,start,end,location,organizer,attendees,body,onlineMeeting" --method get --output json
```

### Search events

```bash
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/events?\$filter=contains(subject,'keyword')&\$select=subject,start,end&\$top=10" --method get --output json
```

### Create event

Write the event JSON to a temp file, then POST:

```bash
cat > /tmp/m365_event.json << 'EOF'
{
  "subject": "Meeting Title",
  "start": {"dateTime": "2026-03-01T14:00:00", "timeZone": "Europe/Berlin"},
  "end": {"dateTime": "2026-03-01T15:00:00", "timeZone": "Europe/Berlin"},
  "location": {"displayName": "Conference Room"},
  "attendees": [
    {"emailAddress": {"address": "attendee@example.com", "name": "Name"}, "type": "required"}
  ],
  "body": {"contentType": "text", "content": "Agenda: ..."}
}
EOF

m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/events" \
  --method post --body @/tmp/m365_event.json --content-type "application/json" --output json
```

### Delete event

```bash
m365 request --url "https://graph.microsoft.com/v1.0/users/<upn>/events/<event-id>" \
  --method delete
```

## Tips

- Paginated results include `@odata.nextLink`. Fetch the next page by passing that URL to `m365 request`.
- Use `--query` (JMESPath) to extract specific fields: `--query "[].{subject:subject,from:from.emailAddress.address}"`.
- For Graph API requests, use `\$` to escape `$` in shell.
- `$top` limits results: `$top=5` returns at most 5 items.
- Graph API datetimes are UTC. Specify `timeZone` in event start/end for local times.
