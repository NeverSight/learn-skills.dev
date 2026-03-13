---
name: google-workspace
description: >
  Manage Google Workspace via the `gws` CLI — Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin,
  Tasks, Meet, Slides, Forms, Contacts, and every other Workspace API. Use when: (1) listing,
  uploading, downloading, or sharing files on Google Drive, (2) reading, sending, labeling, or
  filtering Gmail messages, (3) creating, updating, or querying Google Calendar events,
  (4) reading or writing Google Sheets data, (5) creating or editing Google Docs,
  (6) sending Google Chat messages, (7) managing Google Tasks, (8) any other Google Workspace
  operation. Wraps the official `gws` CLI which dynamically discovers all Workspace APIs.
  Outputs structured JSON suitable for agent pipelines.
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    install:
      - id: gws
        kind: node
        package: "@googleworkspace/cli"
        bins: ["gws"]
        label: "Install Google Workspace CLI (npm)"
---

# Google Workspace Skill

Operate all Google Workspace services through the `gws` CLI from OpenClaw.

## Prerequisites

- Node.js 18+
- A Google Cloud project with OAuth credentials
- `gws` CLI installed: `npm install -g @googleworkspace/cli`

## Authentication

### First-time setup (machine with browser)

```bash
gws auth setup        # creates GCP project, enables APIs, logs in
gws auth login -s drive,gmail,sheets,calendar   # pick services you need
```

### Headless server (no browser)

Complete auth on a machine with a browser, then export:

```bash
gws auth export --unmasked > credentials.json
```

> **Security notes:**
> - Set file permissions: `chmod 600 credentials.json`
> - Do not commit credential files to git — add `credentials.json` to your `.gitignore`
> - For production environments, prefer using a service account instead of user credentials

On the headless server:

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
```

### Service account

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/service-account.json
```

### Pre-obtained token

```bash
export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)
```

**Priority:** Token env > Credentials file env > `gws auth login` store > plaintext file.

## Command Pattern

```bash
gws <service> <resource> <method> [--params '{}'] [--json '{}'] [flags]
```

All responses are **structured JSON**. Use `jq` for extraction.

### Global Flags

| Flag | Purpose |
|------|---------|
| `--dry-run` | Preview request without executing |
| `--page-all` | Stream all pages as NDJSON |
| `--fields 'a,b'` | Select response fields |
| `--output table` | Table output for humans |

### Discover commands

```bash
gws --help              # list all services
gws drive --help        # list resources in a service
gws drive files --help  # list methods on a resource
gws schema drive.files.list  # full request/response schema
```

## Common Operations

### Drive

```bash
# List recent files
gws drive files list --params '{"pageSize": 10}'

# Search files
gws drive files list --params '{"q": "name contains '\''report'\''", "pageSize": 20}'

# Upload a file
gws drive +upload ./report.pdf

# Download a file
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' > output.pdf

# Create a folder
gws drive files create --json '{"name": "Project", "mimeType": "application/vnd.google-apps.folder"}'

# Share a file
gws drive permissions create \
  --params '{"fileId": "FILE_ID"}' \
  --json '{"role": "reader", "type": "user", "emailAddress": "user@example.com"}'

# List all pages
gws drive files list --params '{"pageSize": 100}' --page-all | jq -r '.files[].name'
```

### Gmail

```bash
# List inbox messages
gws gmail users-messages list --params '{"userId": "me", "maxResults": 10}'

# Read a message
gws gmail users-messages get --params '{"userId": "me", "id": "MSG_ID"}'

# Send an email
gws gmail users-messages send \
  --params '{"userId": "me"}' \
  --json '{"raw": "BASE64_ENCODED_EMAIL"}'

# Search messages
gws gmail users-messages list --params '{"userId": "me", "q": "from:boss@company.com is:unread"}'

# List labels
gws gmail users-labels list --params '{"userId": "me"}'

# Create a filter
gws gmail users-settings-filters create \
  --params '{"userId": "me"}' \
  --json '{"criteria": {"from": "noreply@example.com"}, "action": {"addLabelIds": ["LABEL_ID"], "removeLabelIds": ["INBOX"]}}'
```

### Calendar

```bash
# List upcoming events
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-01-01T00:00:00Z", "maxResults": 10, "orderBy": "startTime", "singleEvents": true}'

# Create an event
gws calendar events insert \
  --params '{"calendarId": "primary"}' \
  --json '{"summary": "Team Sync", "start": {"dateTime": "2026-03-07T10:00:00+08:00"}, "end": {"dateTime": "2026-03-07T11:00:00+08:00"}, "attendees": [{"email": "user@example.com"}]}'

# Delete an event
gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'

# Find free/busy slots
gws calendar freebusy query \
  --json '{"timeMin": "2026-03-07T00:00:00Z", "timeMax": "2026-03-07T23:59:59Z", "items": [{"id": "user@example.com"}]}'
```

### Sheets

```bash
# Create a spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'

# Read cell values
gws sheets spreadsheets-values get --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1:D10"}'

# Write values
gws sheets spreadsheets-values update \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["Name", "Amount"], ["Rent", "2000"]]}'

# Append a row
gws sheets spreadsheets-values append \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' \
  --json '{"values": [["New Item", "500"]]}'
```

### Docs

```bash
# Create a document
gws docs documents create --json '{"title": "Meeting Notes"}'

# Get document content
gws docs documents get --params '{"documentId": "DOC_ID"}'

# Insert text (batchUpdate)
gws docs documents batchUpdate \
  --params '{"documentId": "DOC_ID"}' \
  --json '{"requests": [{"insertText": {"location": {"index": 1}, "text": "Hello World\n"}}]}'
```

### Chat

```bash
# List spaces
gws chat spaces list

# Send a message
gws chat spaces messages create \
  --params '{"parent": "spaces/SPACE_ID"}' \
  --json '{"text": "Deploy complete ✅"}'
```

### Tasks

```bash
# List task lists
gws tasks tasklists list

# List tasks
gws tasks tasks list --params '{"tasklist": "TASKLIST_ID"}'

# Create a task
gws tasks tasks insert \
  --params '{"tasklist": "TASKLIST_ID"}' \
  --json '{"title": "Review PR", "due": "2026-03-10T00:00:00Z"}'
```

### Admin (Directory)

```bash
# List users
gws admin users list --params '{"domain": "example.com"}'

# Get user details
gws admin users get --params '{"userKey": "user@example.com"}'
```

## Workflow Patterns

### Pipeline: Find → Process → Act

```bash
# Find unread emails from boss, extract subjects
gws gmail users-messages list --params '{"userId": "me", "q": "from:boss is:unread"}' \
  | jq -r '.messages[].id' \
  | while read id; do
      gws gmail users-messages get --params "{\"userId\": \"me\", \"id\": \"$id\"}" \
        | jq -r '.payload.headers[] | select(.name=="Subject") | .value'
    done
```

### Dry-run first

Always use `--dry-run` before destructive operations:

```bash
gws drive files delete --params '{"fileId": "FILE_ID"}' --dry-run
```

## Tips

- Use `gws schema <method>` to discover exact parameter names and types.
- All commands accept `--params` for URL/query parameters and `--json` for request body.
- Pipe through `jq` for field extraction in agent pipelines.
- Use `--page-all` for full result sets with automatic pagination.
- Credentials are encrypted at rest (AES-256-GCM) with OS keyring.

## Recipes

For 50+ ready-made workflow recipes (label & archive emails, organize Drive folders, schedule meetings, etc.), see the [official recipe library](https://github.com/googleworkspace/cli/tree/main/skills).

## Disclaimer

The `gws` CLI is **not an officially supported Google product**. It is a community/experimental tool. Use at your own discretion, and refer to the [upstream repository](https://github.com/googleworkspace/cli) for license and support details.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `gws: command not found` | `npm install -g @googleworkspace/cli` |
| Auth fails / scope error | `gws auth login -s drive,gmail` (pick specific services) |
| "Access blocked" on login | Add yourself as test user in GCP OAuth consent screen |
| Headless server | Export creds from a desktop, set `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` |
| Rate limited | Add delays between calls, reduce `pageSize` |
