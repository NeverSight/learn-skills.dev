---
name: outlook-automation
description: >
  Automates reading, searching, drafting, and sending emails AND calendar events
  in Classic Outlook on Windows using local COM automation. Use this skill when
  the user asks to process Outlook emails, create drafts, send messages, save
  attachments, manage calendar events, create meetings, or respond to invitations
  from the authenticated Outlook session on their Windows Devbox. Requires
  Classic Outlook (not New Outlook) to be running.
---

# Outlook Automation

This skill enables email and calendar automation through Classic Outlook on Windows using the `outlookctl` CLI tool.

## How to Run Commands

Run all commands using this pattern from any directory:

```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli <command> [options]
```

For convenience, define this alias at the start of your session:
```bash
alias outlookctl='uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli'
```

## Quick Start

Before using any commands, verify the environment:

```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli doctor
```

## Available Commands

### Email Commands

| Command | Description |
|---------|-------------|
| `doctor` | Validate environment and prerequisites |
| `list` | List messages from a folder |
| `get` | Get a single message by ID |
| `search` | Search messages with filters |
| `draft` | Create a draft message (supports --reply-all) |
| `send` | Send a draft or new message |
| `move` | Move message to another folder |
| `delete` | Delete a message (soft or permanent) |
| `mark-read` | Mark message as read/unread |
| `forward` | Create a forward draft |
| `attachments save` | Save attachments to disk |

### Calendar Commands

| Command | Description |
|---------|-------------|
| `calendar calendars` | List all available calendars (including subscribed ICS) |
| `calendar list` | List calendar events (default: next 7 days, use --all for all calendars) |
| `calendar get` | Get event details by ID |
| `calendar create` | Create an event or meeting (draft by default) |
| `calendar send` | Send meeting invitations |
| `calendar respond` | Accept, decline, or tentatively respond to a meeting |
| `calendar update` | Update event subject, time, location, etc. |
| `calendar delete` | Delete/cancel an event (sends cancellations if needed) |

**Tip:** Use `--calendar "Name"` to access non-default calendars (e.g., `--calendar "Family"`).

## Safety Rules

**CRITICAL: Follow these rules when handling email and calendar operations:**

### Email Safety
1. **Never auto-send emails** - Always create drafts first and get explicit user confirmation before sending
2. **Draft-first workflow** - Use `draft` to create drafts, show the user a preview, then send only after approval
3. **Explicit confirmation required** - The send command requires `--confirm-send YES` flag
4. **Metadata by default** - Body content is only retrieved when explicitly requested

### Calendar Safety
1. **Meetings are drafts by default** - When creating a meeting with attendees, invitations are NOT sent automatically
2. **Explicit send required** - Use `calendar send --confirm-send YES` to send meeting invitations
3. **Show preview first** - Always show the user meeting details before sending invitations
4. **Responding is safe** - Accepting/declining meetings does not require extra confirmation

## Workflows

### Reading and Searching Email

To list recent emails:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli list --count 10
```

To search for specific emails:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli search --from "sender@example.com" --since 2025-01-01
```

To get full message content (only when user asks):
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli get --id "<entry_id>" --store "<store_id>" --include-body
```

### Creating and Sending Email (Draft-First)

**Step 1: Create a draft**
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli draft --to "recipient@example.com" --subject "Subject" --body-text "Message body"
```

**Step 2: Show user the preview** (subject, recipients, body summary)

**Step 3: Only after user confirms, send the draft**
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli send --draft-id "<entry_id>" --draft-store "<store_id>" --confirm-send YES
```

### Replying to Messages

```bash
# Create reply draft
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli draft --to "recipient@example.com" --subject "Re: Original" --body-text "Reply text" --reply-to-id "<entry_id>" --reply-to-store "<store_id>"
```

### Saving Attachments

```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli attachments save --id "<entry_id>" --store "<store_id>" --dest "./attachments"
```

## Calendar Workflows

### Viewing Calendar Events

To list upcoming events (next 7 days by default):
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar list
```

To list events for a specific date range:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar list --start "2025-01-20" --days 14
```

To view a shared calendar:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar list --calendar "colleague@example.com"
```

To get full event details:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar get --id "<entry_id>" --store "<store_id>" --include-body
```

### Creating Events (Personal Appointments)

For events without attendees (no invitations needed):
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar create --subject "Focus Time" --start "2025-01-20 14:00" --duration 120
```

### Creating Meetings (Draft-First Workflow)

**Step 1: Create the meeting (saved as draft, no invitations sent)**
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar create \
  --subject "Team Sync" \
  --start "2025-01-20 10:00" \
  --duration 60 \
  --location "Conference Room A" \
  --attendees "alice@example.com,bob@example.com" \
  --body "Agenda:\n1. Project updates\n2. Next steps"
```

**Step 2: Show user the meeting preview** (subject, time, attendees, location)

**Step 3: Only after user confirms, send the invitations**
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar send --id "<entry_id>" --store "<store_id>" --confirm-send YES
```

### Creating Meetings with Teams Link

To include a Teams meeting URL in the body:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar create \
  --subject "Virtual Meeting" \
  --start "2025-01-20 15:00" \
  --duration 30 \
  --attendees "team@example.com" \
  --teams-url "https://teams.microsoft.com/l/meetup-join/..."
```

Note: The Teams URL is embedded in the meeting body. For full Teams integration (automatic link generation), create the meeting in Outlook manually.

### Creating Recurring Events

Weekly standup every Monday and Wednesday:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar create \
  --subject "Daily Standup" \
  --start "2025-01-20 09:00" \
  --duration 15 \
  --recurrence "weekly:monday,wednesday:until:2025-12-31"
```

### Responding to Meeting Invitations

To accept a meeting:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar respond --id "<entry_id>" --store "<store_id>" --response accept
```

To decline a meeting:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar respond --id "<entry_id>" --store "<store_id>" --response decline
```

To tentatively accept:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar respond --id "<entry_id>" --store "<store_id>" --response tentative
```

To respond without notifying the organizer:
```bash
uv run --project "C:/Users/GordonMickel/work/outlookctl" python -m outlookctl.cli calendar respond --id "<entry_id>" --store "<store_id>" --response accept --no-response
```

## Output Format

All commands output JSON with a consistent structure. Key fields:

- `version`: Schema version (currently "1.0")
- `success`: Boolean for operation result
- Message IDs include `entry_id` and `store_id` for stable references

## Reference Documentation

For detailed information, see:
- [CLI Reference](reference/cli.md) - Complete command options
- [JSON Schema](reference/json-schema.md) - Output format details
- [Security](reference/security.md) - Data handling and safety
- [Troubleshooting](reference/troubleshooting.md) - Common issues

## Requirements

- Windows with Classic Outlook running
- uv installed and in PATH
- outlookctl project at: `C:/Users/GordonMickel/work/outlookctl`

## Error Handling

If commands fail, check:
1. Classic Outlook is running (not New Outlook)
2. `doctor` command passes all checks
3. Message IDs are valid and not expired
