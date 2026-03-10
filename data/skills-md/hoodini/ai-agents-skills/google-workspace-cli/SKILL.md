---
name: google-workspace-cli
description: Interact with all Google Workspace APIs via the gws CLI. Use when managing Drive files, sending/reading Gmail, creating Calendar events, reading/writing Sheets/Docs/Slides, managing Chat spaces, contacts, Admin users/groups, Vault eDiscovery, Classroom, Apps Script, Workspace Events, or configuring the gws MCP server. Triggers on Google Workspace, gws, Drive, Gmail, Calendar, Sheets, Docs, Slides, Chat, Tasks, Meet, Forms, Keep, Admin, People, Vault, Classroom, Apps Script, Cloud Identity, Alert Center, Groups Settings, Licensing, Reseller, Model Armor, gws CLI, gws mcp, Google API, Workspace automation, npx skills add.
---

# Google Workspace CLI (`gws`)

One CLI for **all** of Google Workspace — Drive, Gmail, Calendar, Sheets, Docs, Slides, Chat, Tasks, Admin, Meet, Forms, Keep, and every other Workspace API. Built for humans and AI agents. Structured JSON output. 100+ agent skills included.

> **Note:** This is not an officially supported Google product.

> **Important:** This project is under active development. Expect breaking changes as we march toward v1.0.

**Repository:** https://github.com/googleworkspace/cli

## How It Works

`gws` does NOT ship a static list of commands. It reads Google's own [Discovery Service](https://developers.google.com/discovery) at runtime and builds its entire command surface dynamically. When Google adds a new API endpoint or method, `gws` picks it up automatically — zero updates needed.

## Prerequisites

- **Node.js 18+** — for `npm install` (or download a pre-built binary from [GitHub Releases](https://github.com/googleworkspace/cli/releases))
- **A Google Cloud project** — required for OAuth credentials. You can create one via the [Google Cloud Console](https://console.cloud.google.com/), with the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install), or with the `gws auth setup` command.
- **A Google account** with access to Google Workspace

## Installation

```bash
# Install globally via npm (recommended — bundles native binaries, no Rust needed)
npm install -g @googleworkspace/cli

# Verify installation
gws --version
```

Alternative installation methods:
```bash
# From GitHub Releases (pre-built binaries)
# Download from: https://github.com/googleworkspace/cli/releases

# Build from source (requires Rust toolchain)
cargo install --git https://github.com/googleworkspace/cli --locked

# Nix flake
nix run github:googleworkspace/cli
```

## Quick Start

```bash
gws auth setup     # walks you through Google Cloud project config
gws auth login     # subsequent OAuth login
gws drive files list --params '{"pageSize": 5}'
```

## Authentication

### Which setup should I use?

| I have… | Use |
|:--------|:----|
| `gcloud` installed and authenticated | `gws auth setup` (fastest — one command) |
| A GCP project but no `gcloud` | Manual OAuth setup in Cloud Console |
| An existing OAuth access token | `GOOGLE_WORKSPACE_CLI_TOKEN` env var |
| Existing credentials JSON (service account or exported) | `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` env var |

### Quick Setup (recommended — requires gcloud CLI)

```bash
gws auth setup       # one-time: creates a Cloud project, enables APIs, logs you in
gws auth login       # subsequent logins with scope selection
```

> Credentials are encrypted at rest (AES-256-GCM) with the key stored in your OS keyring.

### Scoped Login (for unverified/testing OAuth apps, limited to ~25 scopes)

> **Warning:** Unverified (testing-mode) apps are limited to ~25 OAuth scopes. The `recommended` scope preset includes 85+ scopes and **will fail** for unverified apps (especially for `@gmail.com` accounts). Choose individual services instead:

```bash
# Select only the services you need to stay under the scope limit
gws auth login -s drive,gmail,sheets
gws auth login --scopes drive,gmail,calendar,docs,chat
```

### Multiple Accounts

```bash
gws auth login --account work@corp.com
gws auth login --account personal@gmail.com

gws auth list                                    # list registered accounts
gws auth default work@corp.com                   # set the default

gws --account personal@gmail.com drive files list  # one-off override
export GOOGLE_WORKSPACE_CLI_ACCOUNT=personal@gmail.com  # env var override
```

Credentials are stored per-account as `credentials.<b64-email>.enc` in `~/.config/gws/`, with an `accounts.json` registry tracking defaults.

### Manual OAuth Setup (no gcloud)

Use this when `gws auth setup` cannot automate project/client creation, or when you want explicit control.

1. Open Google Cloud Console in the target project:
   - OAuth consent screen: `https://console.cloud.google.com/apis/credentials/consent?project=<PROJECT_ID>`
   - Credentials: `https://console.cloud.google.com/apis/credentials?project=<PROJECT_ID>`
2. Configure OAuth branding/audience if prompted — App type: **External** (testing mode is fine)
3. Add your account under **Test users**
4. Create an OAuth client — Type: **Desktop app**
5. Download the client JSON → save to `~/.config/gws/client_secret.json`

> **Important:** You must add yourself as a test user. In the OAuth consent screen, click **Test users → Add users** and enter your Google account email. Without this, login will fail with a generic "Access blocked" error.

Then run:
```bash
gws auth login
```

### Headless / CI

```bash
# On a machine with a browser:
gws auth export --unmasked > credentials.json

# On the headless machine:
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
gws drive files list   # just works
```

### Service Account (server-to-server)

```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/service-account.json
gws drive files list

# For Domain-Wide Delegation:
export GOOGLE_WORKSPACE_CLI_IMPERSONATED_USER=admin@example.com
```

### Pre-obtained Access Token

```bash
export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)
```

### Browser-Assisted Auth (for AI agents)

Agents can complete OAuth with browser automation:

- **Human flow:** Run `gws auth login`, open the printed URL, approve scopes.
- **Agent-assisted flow:** The agent opens the URL, selects the account, handles consent prompts, and returns control once the localhost callback succeeds.

If consent shows "Google hasn't verified this app" (testing mode), click **Continue**. If scope checkboxes appear, select required scopes (or **Select all**) before continuing.

### Auth Precedence

| Priority | Method | Source |
|:---------|:-------|:-------|
| 1 | Access token | `GOOGLE_WORKSPACE_CLI_TOKEN` |
| 2 | Credentials file | `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` |
| 3 | Per-account encrypted credentials | `gws auth login --account EMAIL` |
| 4 | Plaintext credentials | `~/.config/gws/credentials.json` |

Account resolution: `--account` flag > `GOOGLE_WORKSPACE_CLI_ACCOUNT` env var > default in `accounts.json`.

> All environment variables can also live in a `.env` file in your project root.

## Command Structure

The universal pattern for ALL gws commands:

```
gws <service> <resource> <method> [--params '{ JSON }'] [--json '{ JSON }'] [flags]
```

### Global Flags

| Flag | Description |
|:-----|:------------|
| `--help` | Show help for any service, resource, or method |
| `--params '{ JSON }'` | URL/query parameters as JSON |
| `--json '{ JSON }'` | Request body as JSON |
| `--dry-run` | Preview the HTTP request without executing |
| `--page-all` | Auto-paginate, one JSON line per page (NDJSON) |
| `--page-limit <N>` | Max pages to fetch (default: 10) |
| `--page-delay <MS>` | Delay between pages (default: 100ms) |
| `--upload <path>` | Multipart file upload |
| `--account <email>` | Use a specific authenticated account |
| `--sanitize <template>` | Model Armor response sanitization |

### Introspecting Schemas

```bash
# See the full request/response schema for any method
gws schema drive.files.list
gws schema gmail.users.messages.send
gws schema calendar.events.insert
```

## Core Services — Commands & Examples

### Google Drive

```bash
# List files (paginated)
gws drive files list --params '{"pageSize": 10}'

# List ALL files (auto-paginate as NDJSON)
gws drive files list --params '{"pageSize": 100}' --page-all

# Search for files
gws drive files list --params '{"q": "name contains '\''report'\'' and mimeType = '\''application/pdf'\''", "pageSize": 20}'

# Get file metadata
gws drive files get --params '{"fileId": "FILE_ID"}'

# Upload a file
gws drive files create --json '{"name": "report.pdf", "parents": ["FOLDER_ID"]}' --upload ./report.pdf

# Create a folder
gws drive files create --json '{"name": "Project Docs", "mimeType": "application/vnd.google-apps.folder"}'

# Move a file to a folder
gws drive files update --params '{"fileId": "FILE_ID", "addParents": "FOLDER_ID", "removeParents": "OLD_PARENT_ID"}'

# Share a file
gws drive permissions create --params '{"fileId": "FILE_ID"}' --json '{"role": "writer", "type": "user", "emailAddress": "user@example.com"}'

# Download a file (export Google Docs as PDF)
gws drive files export --params '{"fileId": "FILE_ID", "mimeType": "application/pdf"}'

# Delete a file
gws drive files delete --params '{"fileId": "FILE_ID"}'

# List shared drives
gws drive drives list --params '{"pageSize": 10}'

# Create a shared drive
gws drive drives create --params '{"requestId": "unique-id"}' --json '{"name": "Team Drive"}'
```

### Gmail

```bash
# List messages in inbox
gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'

# Search messages
gws gmail users messages list --params '{"userId": "me", "q": "from:boss@company.com is:unread", "maxResults": 20}'

# Get a specific message
gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID"}'

# Send an email
gws gmail users messages send --params '{"userId": "me"}' --json '{
  "raw": "<BASE64_ENCODED_RFC2822_MESSAGE>"
}'

# List labels
gws gmail users labels list --params '{"userId": "me"}'

# Create a label
gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "Important/Projects"}'

# Modify message labels
gws gmail users messages modify --params '{"userId": "me", "id": "MESSAGE_ID"}' --json '{"addLabelIds": ["LABEL_ID"], "removeLabelIds": ["INBOX"]}'

# Trash a message
gws gmail users messages trash --params '{"userId": "me", "id": "MESSAGE_ID"}'

# List drafts
gws gmail users drafts list --params '{"userId": "me"}'

# Create a draft
gws gmail users drafts create --params '{"userId": "me"}' --json '{
  "message": {"raw": "<BASE64_ENCODED_RFC2822_MESSAGE>"}
}'

# Set vacation auto-reply
gws gmail users settings updateVacation --params '{"userId": "me"}' --json '{
  "enableAutoReply": true,
  "responseSubject": "Out of Office",
  "responseBodyPlainText": "I am out of office until March 10.",
  "restrictToContacts": false,
  "restrictToDomain": false
}'
```

### Google Calendar

```bash
# List upcoming events
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-03-05T00:00:00Z", "maxResults": 10, "singleEvents": true, "orderBy": "startTime"}'

# Get a specific event
gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'

# Create an event
gws calendar events insert --params '{"calendarId": "primary"}' --json '{
  "summary": "Team Standup",
  "description": "Daily standup meeting",
  "start": {"dateTime": "2026-03-06T09:00:00-05:00", "timeZone": "America/New_York"},
  "end": {"dateTime": "2026-03-06T09:30:00-05:00", "timeZone": "America/New_York"},
  "attendees": [{"email": "alice@example.com"}, {"email": "bob@example.com"}]
}'

# Update an event
gws calendar events update --params '{"calendarId": "primary", "eventId": "EVENT_ID"}' --json '{
  "summary": "Updated Standup",
  "start": {"dateTime": "2026-03-06T10:00:00-05:00"},
  "end": {"dateTime": "2026-03-06T10:30:00-05:00"}
}'

# Delete an event
gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'

# List calendars
gws calendar calendarList list

# Check free/busy
gws calendar freebusy query --json '{
  "timeMin": "2026-03-06T08:00:00Z",
  "timeMax": "2026-03-06T18:00:00Z",
  "items": [{"id": "alice@example.com"}, {"id": "bob@example.com"}]
}'

# Create a recurring event
gws calendar events insert --params '{"calendarId": "primary"}' --json '{
  "summary": "Weekly Review",
  "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=FR"],
  "start": {"dateTime": "2026-03-06T16:00:00-05:00", "timeZone": "America/New_York"},
  "end": {"dateTime": "2026-03-06T17:00:00-05:00", "timeZone": "America/New_York"}
}'
```

### Google Sheets

**Important:** Sheets ranges use `!` which bash interprets as history expansion. Always wrap values in single quotes.

```bash
# Create a spreadsheet
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'

# Read cells
gws sheets spreadsheets values get --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1:C10"}'

# Write cells
gws sheets spreadsheets values update --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' --json '{"values": [["Name", "Score"], ["Alice", 95], ["Bob", 87]]}'

# Append rows
gws sheets spreadsheets values append --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1", "valueInputOption": "USER_ENTERED"}' --json '{"values": [["Charlie", 92]]}'

# Get spreadsheet metadata
gws sheets spreadsheets get --params '{"spreadsheetId": "SPREADSHEET_ID"}'

# Clear a range
gws sheets spreadsheets values clear --params '{"spreadsheetId": "SPREADSHEET_ID", "range": "Sheet1!A1:C10"}'

# Batch update (add sheet, format cells, etc.)
gws sheets spreadsheets batchUpdate --params '{"spreadsheetId": "SPREADSHEET_ID"}' --json '{
  "requests": [
    {"addSheet": {"properties": {"title": "March Data"}}},
    {"repeatCell": {
      "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
      "cell": {"userEnteredFormat": {"textFormat": {"bold": true}}},
      "fields": "userEnteredFormat.textFormat.bold"
    }}
  ]
}'
```

### Google Docs

```bash
# Create a document
gws docs documents create --json '{"title": "Meeting Notes"}'

# Get document content
gws docs documents get --params '{"documentId": "DOC_ID"}'

# Update document (insert text)
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --json '{
  "requests": [
    {"insertText": {"location": {"index": 1}, "text": "Hello, World!\n"}}
  ]
}'
```

### Google Slides

```bash
# Create a presentation
gws slides presentations create --json '{"title": "Q1 Review"}'

# Get presentation
gws slides presentations get --params '{"presentationId": "PRES_ID"}'

# Add a slide
gws slides presentations batchUpdate --params '{"presentationId": "PRES_ID"}' --json '{
  "requests": [
    {"createSlide": {"slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"}}}
  ]
}'
```

### Google Chat

```bash
# List spaces
gws chat spaces list

# Send a message to a space
gws chat spaces messages create --params '{"parent": "spaces/SPACE_ID"}' --json '{"text": "Deploy complete."}'

# Get a message
gws chat spaces messages get --params '{"name": "spaces/SPACE_ID/messages/MSG_ID"}'

# List messages in a space
gws chat spaces messages list --params '{"parent": "spaces/SPACE_ID", "pageSize": 25}'

# Create a space
gws chat spaces create --json '{"displayName": "Project Alpha", "spaceType": "SPACE"}'
```

### Google Tasks

```bash
# List task lists
gws tasks tasklists list

# Create a task list
gws tasks tasklists insert --json '{"title": "Sprint 42"}'

# List tasks in a list
gws tasks tasks list --params '{"tasklist": "TASKLIST_ID"}'

# Create a task
gws tasks tasks insert --params '{"tasklist": "TASKLIST_ID"}' --json '{"title": "Review PR #123", "due": "2026-03-07T00:00:00Z"}'

# Complete a task
gws tasks tasks update --params '{"tasklist": "TASKLIST_ID", "task": "TASK_ID"}' --json '{"status": "completed"}'
```

### Google Meet

```bash
# Create a meeting space
gws meet spaces create --json '{}'

# Get meeting space info
gws meet spaces get --params '{"name": "spaces/SPACE_ID"}'
```

### Google Forms

```bash
# Create a form
gws forms forms create --json '{"info": {"title": "Feedback Survey"}}'

# Get form
gws forms forms get --params '{"formId": "FORM_ID"}'

# List responses
gws forms forms responses list --params '{"formId": "FORM_ID"}'
```

### Google Admin (Directory)

```bash
# List users
gws admin users list --params '{"domain": "example.com", "maxResults": 100}'

# Get a user
gws admin users get --params '{"userKey": "user@example.com"}'

# Create a user
gws admin users insert --json '{
  "primaryEmail": "newuser@example.com",
  "name": {"givenName": "Jane", "familyName": "Doe"},
  "password": "TempP@ssw0rd!"
}'

# List groups
gws admin groups list --params '{"domain": "example.com"}'

# Add member to group
gws admin members insert --params '{"groupKey": "group@example.com"}' --json '{"email": "user@example.com", "role": "MEMBER"}'
```

### Google Keep

```bash
# List notes
gws keep notes list

# Get a note
gws keep notes get --params '{"name": "notes/NOTE_ID"}'
```

### Google People (Contacts & Profiles)

```bash
# List contacts
gws people people connections list --params '{"resourceName": "people/me", "personFields": "names,emailAddresses,phoneNumbers", "pageSize": 50}'

# Get a specific contact
gws people people get --params '{"resourceName": "people/PERSON_ID", "personFields": "names,emailAddresses,organizations"}'

# Search contacts
gws people people searchContacts --params '{"query": "Alice", "readMask": "names,emailAddresses"}'

# Create a contact
gws people people createContact --json '{
  "names": [{"givenName": "Jane", "familyName": "Smith"}],
  "emailAddresses": [{"value": "jane@example.com"}],
  "phoneNumbers": [{"value": "+1-555-0100"}]
}'

# List directory (domain contacts)
gws people people listDirectoryPeople --params '{"readMask": "names,emailAddresses", "sources": ["DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"], "pageSize": 100}'
```

### Google Workspace Events

```bash
# Create a subscription to watch for changes
gws events subscriptions create --json '{
  "targetResource": "//calendar.googleapis.com/calendars/primary",
  "eventTypes": ["google.workspace.calendar.event.v1.created"],
  "notificationEndpoint": {"pubsubTopic": "projects/PROJECT/topics/TOPIC"},
  "payloadOptions": {"includeResource": true}
}'

# List subscriptions
gws events subscriptions list

# Delete a subscription
gws events subscriptions delete --params '{"name": "subscriptions/SUB_ID"}'
```

### Google Vault (eDiscovery)

```bash
# List matters
gws vault matters list

# Create a matter
gws vault matters create --json '{"name": "Investigation Q1", "description": "Q1 compliance audit"}'

# Create a hold
gws vault matters holds create --params '{"matterId": "MATTER_ID"}' --json '{
  "name": "Email Hold",
  "corpus": "MAIL",
  "accounts": [{"accountId": "user@example.com"}]
}'
```

### Google Classroom

```bash
# List courses
gws classroom courses list

# Create a course
gws classroom courses create --json '{"name": "CS101", "section": "Fall 2026", "ownerId": "me"}'

# List students in a course
gws classroom courses students list --params '{"courseId": "COURSE_ID"}'

# Create coursework
gws classroom courses courseWork create --params '{"courseId": "COURSE_ID"}' --json '{
  "title": "Assignment 1",
  "workType": "ASSIGNMENT",
  "dueDate": {"year": 2026, "month": 3, "day": 15}
}'
```

### Admin Reports (Audit Logs)

```bash
# List admin activities
gws admin-reports activities list --params '{"userKey": "all", "applicationName": "admin", "maxResults": 50}'

# List login activities
gws admin-reports activities list --params '{"userKey": "all", "applicationName": "login", "maxResults": 50}'

# List Drive audit logs
gws admin-reports activities list --params '{"userKey": "all", "applicationName": "drive", "maxResults": 50}'
```

### Alert Center (Security Alerts)

```bash
# List alerts
gws alertcenter alerts list

# Get alert details
gws alertcenter alerts get --params '{"alertId": "ALERT_ID"}'
```

### Cloud Identity

```bash
# List groups
gws cloudidentity groups list --params '{"parent": "customers/CUSTOMER_ID"}'

# Search groups
gws cloudidentity groups search --params '{"query": "parent == \"customers/CUSTOMER_ID\""}'

# List memberships
gws cloudidentity groups memberships list --params '{"parent": "groups/GROUP_ID"}'
```

### Groups Settings

```bash
# Get group settings
gws groupssettings groups get --params '{"groupUniqueId": "group@example.com"}'

# Update group settings
gws groupssettings groups update --params '{"groupUniqueId": "group@example.com"}' --json '{
  "whoCanPostMessage": "ALL_MEMBERS_CAN_POST",
  "messageModerationLevel": "MODERATE_NONE"
}'
```

### Licensing

```bash
# List license assignments
gws licensing licenseAssignments listForProduct --params '{"productId": "Google-Apps", "customerId": "CUSTOMER_ID"}'

# Assign a license
gws licensing licenseAssignments insert --params '{"productId": "Google-Apps", "skuId": "SKU_ID"}' --json '{"userId": "user@example.com"}'
```

### Reseller

```bash
# List subscriptions
gws reseller subscriptions list --params '{"customerId": "CUSTOMER_ID"}'

# Get a subscription
gws reseller subscriptions get --params '{"customerId": "CUSTOMER_ID", "subscriptionId": "SUB_ID"}'
```

### Apps Script

```bash
# List projects
gws apps-script projects list

# Get project content
gws apps-script projects getContent --params '{"scriptId": "SCRIPT_ID"}'

# Deploy a project
gws apps-script projects deployments create --params '{"scriptId": "SCRIPT_ID"}' --json '{"versionNumber": 1}'

# Run a function
gws apps-script scripts run --params '{"scriptId": "SCRIPT_ID"}' --json '{"function": "myFunction", "parameters": []}'
```

## Workflow Helpers (Shortcut Commands)

`gws` ships higher-level helper commands for the most common multi-step operations:

```bash
# --- Drive ---
# Upload a file to Drive with automatic metadata
gws drive-upload ./report.pdf

# --- Sheets ---
# Append a row to a sheet
gws sheets-append --spreadsheet-id ID --range 'Sheet1!A1' --values '[["Name", "Score"]]'

# Read sheet values
gws sheets-read --spreadsheet-id ID --range 'Sheet1!A1:C10'

# --- Gmail ---
# Send an email (simplified)
gws gmail-send --to user@example.com --subject "Hello" --body "Hi there"

# Triage inbox — show unread summary (sender, subject, date)
gws gmail-triage

# Watch for new emails and stream them as NDJSON
gws gmail-watch

# --- Calendar ---
# Show upcoming calendar agenda across all calendars
gws calendar-agenda

# Insert a calendar event quickly
gws calendar-insert --summary "Lunch" --start "2026-03-06T12:00:00" --end "2026-03-06T13:00:00"

# --- Docs ---
# Append text to a Google Doc
gws docs-write --document-id DOC_ID --text "New paragraph here"

# --- Chat ---
# Send a Chat message to a space
gws chat-send --space "spaces/SPACE_ID" --text "Hello team!"

# --- Apps Script ---
# Upload local files to an Apps Script project
gws apps-script-push --script-id SCRIPT_ID --source ./src

# --- Workspace Events ---
# Subscribe to Workspace events and stream them as NDJSON
gws events-subscribe --target "//calendar.googleapis.com/calendars/primary" --event-types "google.workspace.calendar.event.v1.created"

# Renew/reactivate Workspace Events subscriptions
gws events-renew --subscription-id SUB_ID

# --- Model Armor ---
# Sanitize a user prompt through a Model Armor template
gws modelarmor-sanitize-prompt --template "projects/P/locations/L/templates/T" --text "user input here"

# Sanitize a model response through a Model Armor template
gws modelarmor-sanitize-response --template "projects/P/locations/L/templates/T" --text "model output here"

# Create a new Model Armor template
gws modelarmor-create-template --project PROJECT --location LOCATION --template-id my-template

# --- Cross-service Workflows ---
# Today's standup report (meetings + open tasks)
gws workflow-standup-report

# Meeting prep (agenda, attendees, linked docs)
gws workflow-meeting-prep

# Convert email to task
gws workflow-email-to-task --message-id MSG_ID

# Weekly digest (meetings + unread count)
gws workflow-weekly-digest

# Announce a Drive file in a Chat space
gws workflow-file-announce --file-id FILE_ID --space "spaces/SPACE_ID"
```

## Installing gws Skills Into Your Agent Project

The gws repo ships 100+ SKILL.md files you can install directly into your agent's skills directory:

```bash
# Install ALL gws skills at once
npx skills add https://github.com/googleworkspace/cli

# Or pick only what you need
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-drive
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-gmail
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-calendar
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-sheets
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-docs
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-chat
```

<details>
<summary>OpenClaw setup</summary>

```bash
# Symlink all skills (stays in sync with repo)
ln -s $(pwd)/skills/gws-* ~/.openclaw/skills/

# Or copy specific skills
cp -r skills/gws-drive skills/gws-gmail ~/.openclaw/skills/
```

The `gws-shared` skill includes an `install` block so OpenClaw auto-installs the CLI via `npm` if `gws` isn't on PATH.

</details>

This places SKILL.md files into your project's `.github/skills/` (Copilot), `.claude/skills/` (Claude Code), or equivalent directory, giving your agent deep per-service knowledge.

## Personas (Role-Based Skill Bundles)

The gws repo includes 10 pre-built persona bundles that combine multiple services for common roles:

| Persona | Description | Services Used |
|:--------|:------------|:--------------|
| `persona-exec-assistant` | Manage an executive's schedule, inbox, and communications | Calendar, Gmail, Chat, Tasks |
| `persona-project-manager` | Coordinate projects — track tasks, schedule meetings, share docs | Tasks, Calendar, Drive, Chat |
| `persona-hr-coordinator` | Handle HR workflows — onboarding, announcements, employee comms | Admin, Gmail, Calendar, Docs |
| `persona-sales-ops` | Manage sales workflows — track deals, schedule calls, client comms | Sheets, Gmail, Calendar, Chat |
| `persona-it-admin` | Administer IT — manage users, monitor security, configure Workspace | Admin, Alert Center, Cloud Identity |
| `persona-content-creator` | Create, organize, and distribute content across Workspace | Docs, Slides, Drive, Gmail |
| `persona-customer-support` | Manage customer support — track tickets, respond, escalate issues | Gmail, Sheets, Chat, Tasks |
| `persona-event-coordinator` | Plan and manage events — scheduling, invitations, and logistics | Calendar, Gmail, Drive, Chat |
| `persona-team-lead` | Lead a team — run standups, coordinate tasks, communicate | Calendar, Tasks, Chat, Gmail |
| `persona-researcher` | Organize research — manage references, notes, collaboration | Drive, Docs, Keep, Sheets |

Install a persona:
```bash
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/persona-exec-assistant
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/persona-it-admin
```

## Recipes (Multi-Step Task Sequences)

The gws repo ships 50 curated recipes — multi-step task sequences with real commands. Key recipes:

| Recipe | What It Does |
|:-------|:-------------|
| `recipe-audit-external-sharing` | Find and review Drive files shared outside the org |
| `recipe-label-and-archive-emails` | Apply Gmail labels to matching messages and archive them |
| `recipe-send-personalized-emails` | Read from Sheets, send personalized Gmail to each row |
| `recipe-draft-email-from-doc` | Read a Google Doc and use it as Gmail body |
| `recipe-organize-drive-folder` | Create folder structure and move files into place |
| `recipe-share-folder-with-team` | Share a Drive folder with collaborators |
| `recipe-email-drive-link` | Share a file and email the link |
| `recipe-create-doc-from-template` | Copy a Docs template, fill content, share |
| `recipe-create-expense-tracker` | Set up Sheets for expense tracking |
| `recipe-block-focus-time` | Create recurring focus time on Calendar |
| `recipe-reschedule-meeting` | Move event and notify attendees |
| `recipe-search-and-export-emails` | Find matching Gmail messages and export |
| `recipe-create-gmail-filter` | Auto-label/star incoming messages |
| `recipe-cancel-and-notify` | Delete event and send cancellation email |
| `recipe-find-free-time` | Query free/busy for multiple users |
| `recipe-bulk-download-folder` | Download all files from a Drive folder |
| `recipe-find-large-files` | Identify large Drive files consuming storage |
| `recipe-create-shared-drive` | Create Shared Drive and add members |
| `recipe-transfer-file-ownership` | Transfer Drive file ownership between users |
| `recipe-post-mortem-setup` | Create Doc, schedule Calendar review, notify via Chat |
| `recipe-save-email-attachments` | Save Gmail attachments to Drive |
| `recipe-send-team-announcement` | Announce via Gmail and Chat simultaneously |
| `recipe-create-feedback-form` | Create Form and share via Gmail |
| `recipe-sync-contacts-to-sheet` | Export contacts directory to Sheets |
| `recipe-create-events-from-sheet` | Read Sheets data and create Calendar events |
| `recipe-generate-report-from-sheet` | Read Sheets data and create Docs report |
| `recipe-save-email-to-doc` | Archive Gmail message body into a Doc |
| `recipe-batch-reply-to-emails` | Find matching emails and send standard reply |
| `recipe-batch-rename-files` | Rename Drive files to consistent naming |
| `recipe-create-vacation-responder` | Enable Gmail out-of-office auto-reply |
| `recipe-triage-security-alerts` | Review Workspace security alerts |
| `recipe-deploy-apps-script` | Push local files to Apps Script project |
| `recipe-create-meet-space` | Create Meet space and share join link |
| `recipe-create-presentation` | Create Slides presentation with initial slides |
| `recipe-create-classroom-course` | Create Classroom course and invite students |

Install recipes:
```bash
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/recipe-send-personalized-emails
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/recipe-audit-external-sharing
```

Full list: https://github.com/googleworkspace/cli/blob/main/docs/skills.md

## MCP Server Integration

`gws mcp` starts a [Model Context Protocol](https://modelcontextprotocol.io/) server over stdio, exposing Google Workspace APIs as structured tools for any MCP-compatible client.

```bash
# Start MCP server for specific services
gws mcp -s drive                  # Drive only
gws mcp -s drive,gmail,calendar   # multiple services
gws mcp -s all                    # all services (many tools!)

# Include workflow and helper tools
gws mcp -s drive,gmail -w -e

# Compact tool mode — reduces context window usage for LLMs
gws mcp -s drive,gmail --compact
```

### MCP Client Configuration

**VS Code / Copilot (`settings.json` or `.vscode/mcp.json`):**
```json
{
  "mcpServers": {
    "gws": {
      "command": "gws",
      "args": ["mcp", "-s", "drive,gmail,calendar,sheets,docs"]
    }
  }
}
```

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "gws": {
      "command": "gws",
      "args": ["mcp", "-s", "drive,gmail,calendar,sheets,docs"]
    }
  }
}
```

**Cursor (`.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "gws": {
      "command": "gws",
      "args": ["mcp", "-s", "drive,gmail,calendar"]
    }
  }
}
```

**Gemini CLI Extension:**
```bash
gws auth setup
gemini extensions install https://github.com/googleworkspace/cli
```

Installing the Gemini extension gives your Gemini CLI agent direct access to all `gws` commands and skills. The extension automatically inherits your terminal credentials.

> **Tip:** Each service adds roughly 10–80 tools. Keep the list to what you actually need to stay under your client's tool limit (typically 50–100 tools). Use `--compact` flag to reduce context window usage.

### MCP Flags

| Flag | Description |
|:-----|:------------|
| `-s, --services <list>` | Comma-separated services to expose, or `all` |
| `-w, --workflows` | Also expose workflow tools |
| `-e, --helpers` | Also expose helper tools |
| `--compact` | Compact tool mode — reduces tool descriptions to save context window |

## Advanced Usage

### Dry Run (preview requests without executing)

```bash
gws drive files list --params '{"pageSize": 5}' --dry-run
```

### Pagination

```bash
# Auto-paginate everything as NDJSON
gws drive files list --params '{"pageSize": 100}' --page-all

# Limit pages
gws drive files list --params '{"pageSize": 100}' --page-all --page-limit 5

# Delay between pages (rate limiting)
gws drive files list --params '{"pageSize": 100}' --page-all --page-delay 200
```

### Piping & Processing Output

All output is structured JSON. Pipe to `jq` for processing:

```bash
# Get just file names
gws drive files list --params '{"pageSize": 100}' --page-all | jq -r '.files[].name'

# Get unread email subjects
gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 5}' | jq '.messages[].id'

# Count events this week
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-03-02T00:00:00Z", "timeMax": "2026-03-08T00:00:00Z", "singleEvents": true}' | jq '.items | length'
```

### Multipart Uploads

```bash
gws drive files create --json '{"name": "report.pdf"}' --upload ./report.pdf
```

### Model Armor (Response Sanitization)

Scan API responses for prompt injection before they reach your agent:

```bash
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}' \
  --sanitize "projects/P/locations/L/templates/T"
```

| Environment Variable | Description |
|:---------------------|:------------|
| `GOOGLE_WORKSPACE_CLI_SANITIZE_TEMPLATE` | Default Model Armor template |
| `GOOGLE_WORKSPACE_CLI_SANITIZE_MODE` | `warn` (default) or `block` |

## Agent Decision Guide

Use this table to decide which `gws` command to run based on what the user is asking:

| User Intent | Service | Example Command |
|:------------|:--------|:----------------|
| List, search, upload, download, share files | `drive` | `gws drive files list` |
| Create folders, manage permissions | `drive` | `gws drive files create`, `gws drive permissions create` |
| Read, send, search, label emails | `gmail` | `gws gmail users messages list/send` |
| Create drafts, manage filters | `gmail` | `gws gmail users drafts create` |
| View, create, update, delete calendar events | `calendar` | `gws calendar events list/insert/update/delete` |
| Check availability / free-busy | `calendar` | `gws calendar freebusy query` |
| Read, write, append spreadsheet data | `sheets` | `gws sheets spreadsheets values get/update/append` |
| Create spreadsheets, format cells | `sheets` | `gws sheets spreadsheets create/batchUpdate` |
| Create, read, edit documents | `docs` | `gws docs documents create/get/batchUpdate` |
| Create, edit presentations | `slides` | `gws slides presentations create/batchUpdate` |
| Send messages, manage chat spaces | `chat` | `gws chat spaces messages create` |
| Manage tasks and to-do lists | `tasks` | `gws tasks tasks list/insert/update` |
| Create meeting links | `meet` | `gws meet spaces create` |
| Create forms, read responses | `forms` | `gws forms forms create`, `gws forms forms responses list` |
| Manage contacts and profiles | `people` | `gws people people connections list` |
| Manage users, groups, devices | `admin` | `gws admin users list`, `gws admin groups list` |
| Manage notes | `keep` | `gws keep notes list` |
| Run/deploy Apps Script projects | `apps-script` | `gws apps-script projects list` |
| Audit logs and usage reports | `admin-reports` | `gws admin-reports activities list` |
| Manage security alerts | `alertcenter` | `gws alertcenter alerts list` |
| Manage identity and groups | `cloudidentity` | `gws cloudidentity groups list` |
| Subscribe to Workspace events | `events` | `gws events subscriptions create` |
| Manage Google Vault (eDiscovery) | `vault` | `gws vault matters list` |
| Manage Workspace licenses | `licensing` | `gws licensing licenseAssignments list` |
| Manage Google Classroom | `classroom` | `gws classroom courses list` |
| Configure Google Groups settings | `groupssettings` | `gws groupssettings groups get/update` |
| Manage Workspace subscriptions | `reseller` | `gws reseller subscriptions list` |
| Sanitize content for safety | `modelarmor` | `gws modelarmor-sanitize-prompt` |

## Environment Variables Reference

| Variable | Description |
|:---------|:------------|
| `GOOGLE_WORKSPACE_CLI_TOKEN` | Pre-obtained OAuth access token |
| `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` | Path to credentials JSON (service account or exported) |
| `GOOGLE_WORKSPACE_CLI_ACCOUNT` | Default account email |
| `GOOGLE_WORKSPACE_CLI_IMPERSONATED_USER` | User to impersonate (domain-wide delegation) |
| `GOOGLE_WORKSPACE_CLI_SANITIZE_TEMPLATE` | Default Model Armor template |
| `GOOGLE_WORKSPACE_CLI_SANITIZE_MODE` | `warn` or `block` |

## Troubleshooting

| Error | Fix |
|:------|:----|
| "Access blocked" or 403 during login | Add yourself as a test user in OAuth consent screen |
| "Google hasn't verified this app" | Click Advanced → Continue (safe for personal use) |
| Too many scopes error | Use `gws auth login -s drive,gmail,sheets` to select fewer services |
| `gcloud` CLI not found | Install gcloud or set up OAuth manually in Cloud Console |
| `redirect_uri_mismatch` | Re-create OAuth client as Desktop app type |
| `accessNotConfigured` | See detailed fix below |
| Stale credentials | Run `gws auth login` to re-authenticate |

### API not enabled — `accessNotConfigured`

If a required Google API is not enabled for your GCP project, you will see a 403 error:

```json
{
  "error": {
    "code": 403,
    "message": "Gmail API has not been used in project 549352339482 ...",
    "reason": "accessNotConfigured",
    "enable_url": "https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=549352339482"
  }
}
```

`gws` also prints an actionable hint to stderr:

```
💡 API not enabled for your GCP project.
   Enable it at: https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=549352339482
   After enabling, wait a few seconds and retry your command.
```

**Steps to fix:**
1. Click the `enable_url` link (or copy it from the JSON `enable_url` field).
2. In the GCP Console, click **Enable**.
3. Wait ~10 seconds, then retry your `gws` command.

> **Tip:** You can also run `gws auth setup` which walks you through enabling all required APIs for your project automatically.

## Architecture

`gws` uses a two-phase parsing strategy:

1. Read `argv[1]` to identify the service (e.g. `drive`)
2. Fetch the service's Discovery Document (cached 24 hours)
3. Build a `clap::Command` tree from the document's resources and methods
4. Re-parse the remaining arguments
5. Authenticate, build the HTTP request, execute

All output — success, errors, download metadata — is structured JSON. This means every response is directly parseable by agents without any text extraction.

## Resources

- **GitHub Repo**: https://github.com/googleworkspace/cli
- **npm Package**: https://www.npmjs.com/package/@googleworkspace/cli
- **Skills Index (100+ skills)**: https://github.com/googleworkspace/cli/blob/main/docs/skills.md
- **Google Discovery API**: https://developers.google.com/discovery
- **Google Workspace APIs**: https://developers.google.com/workspace
- **Releases & Binaries**: https://github.com/googleworkspace/cli/releases

## License

Apache-2.0
