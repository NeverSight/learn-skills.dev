---
name: google
description: Personal assistant for Google Workspace using gog CLI. Search Gmail, manage Calendar, organize Drive, update Sheets, track Tasks, and lookup Contacts. Use when triaging email, scheduling meetings, finding availability, searching documents, managing tasks, or any Google service interaction from the terminal.
---

# Google Personal Assistant

A comprehensive skill for managing Google Workspace services via the `gog` CLI. Designed for Personal Assistant and Chief of Staff workflows with emphasis on efficient searching, filtering, and querying.

## When to Use This Skill

- Triaging and processing email inbox
- Scheduling meetings and managing calendar events
- Finding availability across multiple calendars
- Searching and organizing Google Drive documents
- Managing task lists and to-dos
- Looking up and managing contacts
- Reading/writing data in Google Sheets
- Exporting Docs, Slides, or Sheets
- Setting focus time or out-of-office status

## Prerequisites

Ensure `gog` is installed and authenticated:

```bash
# Check installation
gog version

# Check authentication status
gog auth status

# Verify account access
gog people me

# Add a new account if needed
gog auth add your@email.com --services=all
```

## Quick Start

### Gmail

```bash
# Search unread emails
gog gmail search "is:unread" --max=20

# Search from specific sender
gog gmail search "from:boss@company.com newer_than:7d"

# Send an email
gog gmail send --to="recipient@example.com" --subject="Subject" --body="Message body"

# Reply to a thread
gog gmail send --reply-to-message-id=MESSAGE_ID --body="Reply text"

# Get message details
gog gmail get MESSAGE_ID
```

### Calendar

```bash
# View today's events
gog calendar events --today

# View this week
gog calendar events --week

# Create an event with Google Meet
gog calendar create primary \
  --summary="Team Sync" \
  --from="2026-01-15T14:00:00-08:00" \
  --to="2026-01-15T15:00:00-08:00" \
  --attendees="person1@example.com,person2@example.com" \
  --with-meet

# Check availability
gog calendar freebusy "person1@example.com,person2@example.com" \
  --from="2026-01-15T09:00:00Z" --to="2026-01-15T17:00:00Z"

# Find scheduling conflicts
gog calendar conflicts --week
```

### Drive

```bash
# List files in root
gog drive ls

# Search for documents
gog drive search "quarterly report"

# Download a file
gog drive download FILE_ID

# Upload a file
gog drive upload /path/to/file.pdf --parent=FOLDER_ID

# Get shareable URL
gog drive url FILE_ID
```

### Tasks

```bash
# List task lists
gog tasks lists list

# View tasks in default list
gog tasks list @default

# Add a task
gog tasks add @default --title="Review report" --due="2026-01-15"

# Mark task complete
gog tasks done @default TASK_ID
```

### Sheets

```bash
# Read a range
gog sheets get SPREADSHEET_ID "Sheet1!A1:D10"

# Update values
gog sheets update SPREADSHEET_ID "Sheet1!A1" "Value1" "Value2"

# Append a row
gog sheets append SPREADSHEET_ID "Sheet1!A:D" "Col1" "Col2" "Col3" "Col4"
```

## Gmail Search Syntax

Gmail search is powerful. Here are the essential operators:

### Sender & Recipient

| Operator | Example | Description |
|----------|---------|-------------|
| `from:` | `from:boss@company.com` | Emails from sender |
| `to:` | `to:team@company.com` | Emails sent to recipient |
| `cc:` | `cc:manager@company.com` | CC'd recipient |
| `bcc:` | `bcc:archive@company.com` | BCC'd recipient |

### Status & Labels

| Operator | Example | Description |
|----------|---------|-------------|
| `is:unread` | `is:unread` | Unread messages |
| `is:read` | `is:read` | Read messages |
| `is:starred` | `is:starred` | Starred messages |
| `is:important` | `is:important` | Marked important |
| `is:snoozed` | `is:snoozed` | Snoozed messages |
| `label:` | `label:work` | Has specific label |
| `in:inbox` | `in:inbox` | In inbox |
| `in:sent` | `in:sent` | In sent folder |
| `in:drafts` | `in:drafts` | In drafts |
| `in:trash` | `in:trash` | In trash |
| `in:spam` | `in:spam` | In spam |
| `in:anywhere` | `in:anywhere` | All mail including spam/trash |

### Content & Subject

| Operator | Example | Description |
|----------|---------|-------------|
| `subject:` | `subject:urgent` | Subject contains word |
| `"exact phrase"` | `"quarterly report"` | Exact phrase match |
| `has:attachment` | `has:attachment` | Has any attachment |
| `filename:` | `filename:pdf` | Attachment filename/type |
| `filename:` | `filename:report.xlsx` | Specific filename |

### Date & Time

| Operator | Example | Description |
|----------|---------|-------------|
| `newer_than:` | `newer_than:7d` | Within last N days |
| `older_than:` | `older_than:1y` | Older than N years |
| `after:` | `after:2026/01/01` | After specific date |
| `before:` | `before:2026/12/31` | Before specific date |

Units for newer_than/older_than: `d` (day), `m` (month), `y` (year)

### Size

| Operator | Example | Description |
|----------|---------|-------------|
| `larger:` | `larger:5M` | Larger than size |
| `smaller:` | `smaller:100K` | Smaller than size |

Units: `K` (KB), `M` (MB)

### Categories

| Operator | Example | Description |
|----------|---------|-------------|
| `category:primary` | `category:primary` | Primary inbox |
| `category:social` | `category:social` | Social category |
| `category:promotions` | `category:promotions` | Promotions |
| `category:updates` | `category:updates` | Updates |
| `category:forums` | `category:forums` | Forums |

### Boolean Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `AND` (or space) | `from:alice subject:report` | Both conditions |
| `OR` | `from:alice OR from:bob` | Either condition |
| `-` (NOT) | `-category:promotions` | Exclude condition |
| `()` | `(from:alice OR from:bob) is:unread` | Grouping |
| `{}` | `{from:alice from:bob}` | OR shorthand |

### Example Queries

```bash
# Unread from VIPs this week
gog gmail search "is:unread from:(boss@company.com OR ceo@company.com) newer_than:7d"

# Large attachments
gog gmail search "has:attachment larger:10M"

# Urgent subjects excluding promotions
gog gmail search "subject:(urgent OR asap OR EOD) -category:promotions is:unread"

# Contracts from legal team
gog gmail search "from:legal@company.com subject:contract has:attachment filename:pdf"

# All messages in a thread (use thread ID from search results)
gog gmail thread get THREAD_ID
```

See [references/gmail-search-syntax.md](references/gmail-search-syntax.md) for complete operator reference.

## Drive Search Syntax

Drive search uses a query language for precise file finding:

### Basic Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `name contains` | `name contains 'report'` | Filename contains |
| `fullText contains` | `fullText contains 'budget'` | Content search |
| `mimeType =` | `mimeType = 'application/pdf'` | File type |

### Date Filters

| Operator | Example | Description |
|----------|---------|-------------|
| `modifiedTime >` | `modifiedTime > '2026-01-01'` | Modified after |
| `modifiedTime <` | `modifiedTime < '2026-01-01'` | Modified before |
| `createdTime >` | `createdTime > '2026-01-01'` | Created after |
| `viewedByMeTime >` | `viewedByMeTime > '2026-01-01'` | Viewed after |

### Ownership & Sharing

| Operator | Example | Description |
|----------|---------|-------------|
| `'email' in owners` | `'me' in owners` | Owned by user |
| `'email' in writers` | `'user@example.com' in writers` | User can edit |
| `'email' in readers` | `'user@example.com' in readers` | User can view |
| `sharedWithMe` | `sharedWithMe` | Shared with you |

### Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `starred` | `starred` | Starred files |
| `trashed = false` | `trashed = false` | Not in trash |
| `'folderId' in parents` | `'FOLDER_ID' in parents` | In specific folder |

### Common MIME Types

| Type | MIME Type |
|------|-----------|
| Google Doc | `application/vnd.google-apps.document` |
| Google Sheet | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Google Form | `application/vnd.google-apps.form` |
| Folder | `application/vnd.google-apps.folder` |
| PDF | `application/pdf` |
| Word | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Excel | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

### Boolean Operators

- `and` - Both conditions must match
- `or` - Either condition matches
- `not` - Negate condition

### Example Queries

```bash
# Recent docs mentioning Q4
gog drive search "fullText contains 'Q4' and modifiedTime > '2026-01-01'"

# All spreadsheets shared with me
gog drive search "sharedWithMe and mimeType = 'application/vnd.google-apps.spreadsheet'"

# PDFs I own
gog drive search "'me' in owners and mimeType = 'application/pdf'"

# Files modified this week
gog drive search "modifiedTime > '2026-01-03'"

# Documents in specific folder
gog drive ls --parent=FOLDER_ID

# Starred presentations
gog drive search "starred and mimeType = 'application/vnd.google-apps.presentation'"
```

See [references/drive-search-syntax.md](references/drive-search-syntax.md) for complete query reference.

## PA/CoS Workflows

### Morning Inbox Triage

```bash
# 1. Check unread counts by label
gog gmail labels list --json | jq '.[] | select(.messagesUnread > 0) | {name, unread: .messagesUnread}'

# 2. Review unread from priority senders
gog gmail search "is:unread from:(boss@company.com OR vip@client.com)" --max=20

# 3. Check for urgent subjects
gog gmail search "is:unread subject:(urgent OR asap OR EOD OR \"action required\")" --max=10

# 4. Review threads needing response (excludes noise)
gog gmail search "is:unread in:inbox -category:updates -category:promotions -category:social" --max=30

# 5. Check for emails with attachments requiring action
gog gmail search "is:unread has:attachment newer_than:2d" --max=15
```

### Schedule a Meeting

```bash
# 1. Find availability for attendees
gog calendar freebusy "person1@company.com,person2@company.com" \
  --from="2026-01-15T09:00:00-08:00" \
  --to="2026-01-15T17:00:00-08:00"

# 2. Check your own conflicts
gog calendar conflicts --days=7

# 3. Create the meeting
gog calendar create primary \
  --summary="Project Kickoff" \
  --from="2026-01-15T14:00:00-08:00" \
  --to="2026-01-15T15:00:00-08:00" \
  --attendees="person1@company.com,person2@company.com" \
  --description="Agenda:\n1. Project overview\n2. Timeline review\n3. Action items" \
  --location="Conference Room A" \
  --with-meet \
  --reminder="popup:15m"

# 4. Send follow-up email with details
gog gmail send \
  --to="person1@company.com,person2@company.com" \
  --subject="Meeting Scheduled: Project Kickoff - Jan 15 at 2pm" \
  --body="Hi team,

I've scheduled our project kickoff meeting for Wednesday, January 15th at 2:00 PM.

Location: Conference Room A (Google Meet link in calendar invite)

Agenda:
1. Project overview
2. Timeline review
3. Action items

Please let me know if you have any conflicts.

Best regards"
```

### Weekly Calendar Prep

```bash
# 1. View the week ahead
gog calendar events --week

# 2. Check all calendars for the week
gog calendar events --week --all

# 3. Find and resolve conflicts
gog calendar conflicts --week

# 4. Check team availability (for group)
gog calendar team engineering@company.com --week

# 5. Block focus time
gog calendar focus-time \
  --from="2026-01-16T09:00:00-08:00" \
  --to="2026-01-16T12:00:00-08:00"

# 6. Set out of office (if needed)
gog calendar out-of-office \
  --from="2026-01-20" \
  --to="2026-01-21" \
  --summary="Out of office - personal day"

# 7. Set working location
gog calendar working-location \
  --from="2026-01-17" \
  --to="2026-01-17" \
  --type="home"
```

### Document Search & Organization

```bash
# Find all docs from a project
gog drive search "fullText contains 'Project Alpha'"

# List recent docs you created
gog drive search "'me' in owners and modifiedTime > '2026-01-01'" --max=50

# Find docs shared by specific person
gog drive search "'colleague@company.com' in writers"

# Find presentation decks
gog drive search "mimeType = 'application/vnd.google-apps.presentation' and modifiedTime > '2025-10-01'"

# Download a doc as PDF
gog docs export DOC_ID --format=pdf --output="./report.pdf"

# Read doc contents (plain text for quick review)
gog docs cat DOC_ID

# Export spreadsheet as Excel
gog sheets export SPREADSHEET_ID --format=xlsx --output="./data.xlsx"

# Get shareable link
gog drive url FILE_ID
gog drive share FILE_ID --role=reader --type=anyone
```

### Daily Task Management

```bash
# 1. List all task lists
gog tasks lists list

# 2. View all tasks in default list
gog tasks list @default

# 3. View tasks due today
gog tasks list @default --due-max="$(date -u +%Y-%m-%dT23:59:59Z)"

# 4. Add a new task with due date
gog tasks add @default \
  --title="Review Q4 financials" \
  --due="2026-01-15" \
  --notes="Check revenue projections and expense reports"

# 5. Complete a task
gog tasks done @default TASK_ID

# 6. Reopen a completed task
gog tasks undo @default TASK_ID

# 7. Delete a task
gog tasks delete @default TASK_ID

# 8. Clear all completed tasks
gog tasks clear @default
```

### Contact Lookup

```bash
# Search for a contact
gog contacts search "John Smith"

# List all contacts
gog contacts list --max=100

# Get contact details
gog contacts get RESOURCE_NAME

# Create a new contact
gog contacts create \
  --given="Jane" \
  --family="Doe" \
  --email="jane.doe@example.com" \
  --phone="+1-555-123-4567"

# Search directory (Workspace)
gog contacts directory search "engineering"
```

See [references/common-workflows.md](references/common-workflows.md) for more workflow recipes.

## Command Reference

### Gmail Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `gmail search <query>` | Search threads | `--max`, `--oldest`, `--page` |
| `gmail get <messageId>` | Get message content | `--format=full\|metadata\|raw` |
| `gmail send` | Send email | `--to`, `--cc`, `--bcc`, `--subject`, `--body`, `--attach` |
| `gmail thread get <id>` | Get full thread | - |
| `gmail thread modify <id>` | Modify thread labels | `--add-labels`, `--remove-labels` |
| `gmail labels list` | List all labels | - |
| `gmail labels get <name>` | Get label details | - |
| `gmail labels modify <ids>` | Bulk modify labels | `--add`, `--remove` |
| `gmail attachment <msgId> <attId>` | Download attachment | - |
| `gmail url <threadId>` | Get Gmail web URL | - |
| `gmail batch delete <ids>` | Bulk delete | - |
| `gmail drafts list` | List drafts | - |
| `gmail drafts create` | Create draft | Same flags as send |

### Calendar Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `calendar calendars` | List calendars | - |
| `calendar events [calId]` | List events | `--from`, `--to`, `--today`, `--week`, `--all` |
| `calendar event <calId> <eventId>` | Get event details | - |
| `calendar create <calId>` | Create event | `--summary`, `--from`, `--to`, `--attendees`, `--with-meet` |
| `calendar update <calId> <eventId>` | Update event | Same as create |
| `calendar delete <calId> <eventId>` | Delete event | - |
| `calendar freebusy <calendars>` | Check availability | `--from`, `--to` |
| `calendar conflicts` | Find conflicts | `--week`, `--days` |
| `calendar search <query>` | Search events | - |
| `calendar respond <calId> <eventId>` | RSVP | `--status=accepted\|declined\|tentative` |
| `calendar focus-time` | Create focus block | `--from`, `--to` |
| `calendar out-of-office` | Set OOO | `--from`, `--to` |
| `calendar working-location` | Set work location | `--from`, `--to`, `--type` |
| `calendar team <groupEmail>` | View team calendars | - |

### Drive Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `drive ls` | List files | `--parent` |
| `drive search <query>` | Full-text search | `--max` |
| `drive get <fileId>` | Get file metadata | - |
| `drive download <fileId>` | Download file | `--output` |
| `drive upload <path>` | Upload file | `--name`, `--parent` |
| `drive mkdir <name>` | Create folder | `--parent` |
| `drive delete <fileId>` | Delete (trash) | - |
| `drive move <fileId>` | Move file | `--parent` |
| `drive rename <fileId> <name>` | Rename file | - |
| `drive share <fileId>` | Share file | `--role`, `--type`, `--email` |
| `drive unshare <fileId> <permId>` | Remove permission | - |
| `drive permissions <fileId>` | List permissions | - |
| `drive url <fileId>` | Get web URL | - |
| `drive copy <fileId> <name>` | Copy file | - |

### Sheets Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `sheets get <id> <range>` | Read values | - |
| `sheets update <id> <range> [vals]` | Update values | `--input=RAW\|USER_ENTERED` |
| `sheets append <id> <range> [vals]` | Append row | `--input` |
| `sheets clear <id> <range>` | Clear values | - |
| `sheets metadata <id>` | Get spreadsheet info | - |
| `sheets create <title>` | Create spreadsheet | - |
| `sheets copy <id> <title>` | Copy spreadsheet | - |
| `sheets export <id>` | Export | `--format=pdf\|xlsx\|csv` |

### Docs Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `docs cat <docId>` | Print as plain text | - |
| `docs export <docId>` | Export document | `--format=pdf\|docx\|txt` |
| `docs info <docId>` | Get metadata | - |
| `docs create <title>` | Create document | - |
| `docs copy <docId> <title>` | Copy document | - |

### Slides Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `slides export <id>` | Export presentation | `--format=pdf\|pptx` |
| `slides info <id>` | Get metadata | - |
| `slides create <title>` | Create presentation | - |
| `slides copy <id> <title>` | Copy presentation | - |

### Tasks Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `tasks lists list` | List task lists | - |
| `tasks list <listId>` | List tasks | `--due-min`, `--due-max`, `--show-completed` |
| `tasks add <listId>` | Add task | `--title`, `--due`, `--notes` |
| `tasks update <listId> <taskId>` | Update task | Same as add |
| `tasks done <listId> <taskId>` | Mark complete | - |
| `tasks undo <listId> <taskId>` | Mark incomplete | - |
| `tasks delete <listId> <taskId>` | Delete task | - |
| `tasks clear <listId>` | Clear completed | - |

### Contacts Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `contacts search <query>` | Search contacts | - |
| `contacts list` | List all contacts | `--max` |
| `contacts get <resourceName>` | Get contact | - |
| `contacts create` | Create contact | `--given`, `--family`, `--email`, `--phone` |
| `contacts update <resourceName>` | Update contact | Same as create |
| `contacts delete <resourceName>` | Delete contact | - |
| `contacts directory search` | Search directory | - |

### Groups Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `groups list` | List your groups | - |
| `groups members <groupEmail>` | List group members | - |

### People Commands

| Command | Description | Key Flags |
|---------|-------------|-----------|
| `people me` | Show your profile | - |

## Global Flags

All `gog` commands support these flags:

| Flag | Description |
|------|-------------|
| `--json` | Output JSON (best for scripting/piping to jq) |
| `--plain` | TSV output, no colors (for scripts/parsing) |
| `--account=EMAIL` | Use specific account (multi-account support) |
| `--force` | Skip confirmation prompts |
| `--no-input` | Never prompt, fail instead (CI/automation) |
| `--verbose` | Detailed logging for debugging |
| `--color=<auto\|always\|never>` | Control color output |

### Multi-Account Usage

```bash
# Use specific account for a command
gog gmail search "is:unread" --account=work@company.com

# List available accounts
gog auth list
```

### JSON Output for Scripting

```bash
# Get unread count for inbox
gog gmail labels get INBOX --json | jq '.messagesUnread'

# Extract event IDs from today
gog calendar events --today --json | jq '.[].id'

# List file IDs from search
gog drive search "budget" --json | jq '.[].id'

# Process email subjects
gog gmail search "is:unread" --json | jq '.[].snippet'
```

## Best Practices

### Efficient Searching

1. **Start narrow, then broaden** - Begin with specific queries, add filters if too many results
2. **Use date filters** - `newer_than:` reduces noise dramatically
3. **Combine operators** - `is:unread from:boss newer_than:7d` is better than browsing
4. **Use `--max`** - Limit results when exploring: `--max=10`

### Calendar Management

1. **Always check freebusy** before scheduling meetings with others
2. **Use `--with-meet`** for remote meetings to auto-create video link
3. **Set reminders** - `--reminder="popup:15m"` for important meetings
4. **Block focus time** proactively to protect deep work

### Drive Organization

1. **Use folder IDs** - Store frequently-used folder IDs for quick access
2. **Search by content** - `fullText contains` finds docs even if filename is unclear
3. **Filter by MIME type** - Narrow to specific doc types
4. **Export early** - Download important docs as PDF for offline access

### Automation Tips

1. **Use `--json`** for scripting - Parse with jq
2. **Use `--plain`** for simple scripts - Tab-separated, no colors
3. **Use `--no-input`** in CI - Prevents hangs on prompts
4. **Store IDs** - Calendar, folder, and task list IDs for reuse

## Reference Files

- [Gmail Search Syntax](references/gmail-search-syntax.md) - Complete query operator reference
- [Drive Search Syntax](references/drive-search-syntax.md) - Complete Drive query reference
- [Calendar Scheduling](references/calendar-scheduling.md) - Event creation, time formats, RRULE
- [Common Workflows](references/common-workflows.md) - Extended PA/CoS workflow recipes
