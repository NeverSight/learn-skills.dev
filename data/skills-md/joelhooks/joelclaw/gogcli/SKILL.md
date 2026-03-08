---
name: gogcli
description: "Google Workspace CLI for agents. Use gog to access Gmail, Calendar, Drive, Contacts, Tasks, Sheets, Docs, Slides, Forms, Chat, and more. Triggers on: 'check my email', 'what's on my calendar', 'search gmail', 'list calendar events', 'send email', 'check tasks', 'search drive', 'list contacts', 'create event', 'upload to drive', 'read spreadsheet', or any Google Workspace task."
---

# gogcli — Google Workspace in the Terminal

`gog` is a fast, JSON-first CLI for the full Google Workspace suite. Always use `--json` for structured output when parsing results.

## Environment

```bash
export GOG_ACCOUNT=joelhooks@gmail.com
export GOG_KEYRING_PASSWORD=$(secrets lease gog_keyring_password )
```

Both vars are **required** for every `gog` command. Lease the keyring password from agent-secrets before use.

## Quick Reference

### Gmail

```bash
# Search (default: threads)
gog gmail search 'newer_than:1d' --max 10 --json
gog gmail search 'is:unread' --max 20 --json
gog gmail search 'from:someone@example.com newer_than:7d' --max 10 --json

# Message-level search with bodies
gog gmail messages search 'is:unread' --max 5 --include-body --json

# Read thread
gog gmail thread get <threadId> --json

# Send
gog gmail send --to user@example.com --subject "Subject" --body "Body text"
gog gmail send --to user@example.com --subject "Hi" --body-html "<p>Hello</p>"

# Labels
gog gmail labels list --json
gog gmail thread modify <threadId> --add STARRED --remove INBOX
```

### Calendar

```bash
# Today / this week
gog calendar events primary --today --json
gog calendar events primary --week --json
gog calendar events primary --tomorrow --json
gog calendar events primary --days 7 --json

# All calendars
gog calendar events --all --today --json

# Search
gog calendar search "meeting" --today --json

# Create event
gog calendar create primary \
  --summary "Meeting" \
  --from 2025-01-15T10:00:00Z \
  --to 2025-01-15T11:00:00Z \
  --attendees "alice@example.com"

# Check availability
gog calendar freebusy --calendars "primary" \
  --from 2025-01-15T00:00:00Z --to 2025-01-16T00:00:00Z --json

# List calendars
gog calendar calendars --json
```

### Drive

```bash
gog drive ls --max 20 --json
gog drive search "invoice" --max 20 --json
gog drive upload ./file.pdf --parent <folderId>
gog drive download <fileId> --out ./file.pdf
gog drive mkdir "New Folder"
```

### Tasks

```bash
gog tasks lists --json
gog tasks list <tasklistId> --max 50 --json
gog tasks add <tasklistId> --title "New task"
gog tasks done <tasklistId> <taskId>
```

### Contacts

```bash
gog contacts search "Name" --max 10 --json
gog contacts list --max 50 --json
```

### Sheets

```bash
gog sheets metadata <spreadsheetId> --json
gog sheets get <spreadsheetId> 'Sheet1!A1:B10' --json
gog sheets update <spreadsheetId> 'A1' 'val1|val2,val3|val4'
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data'
```

### Docs / Slides

```bash
gog docs cat <docId>                           # Read doc as text
gog docs export <docId> --format pdf --out doc.pdf
gog slides export <presentationId> --format pdf --out deck.pdf
```

### Chat (Workspace only)

```bash
gog chat spaces list --json
gog chat messages list spaces/<spaceId> --max 10 --json
gog chat dm send user@company.com --text "message"
```

## Output Modes

| Flag | Use |
|------|-----|
| `--json` | Structured JSON to stdout (always prefer for parsing) |
| `--plain` | Stable TSV (tabs, no colors) |
| (none) | Human-readable table |

Errors/progress go to stderr. Pipe `--json` output through `jq` for filtering.

## Patterns

### Batch Gmail search → summarize

```bash
gog gmail messages search 'is:unread newer_than:1d' --max 20 --include-body --json | jq '.messages[] | {from, subject, body}'
```

### Find next free slot

```bash
gog calendar freebusy --calendars "primary" --from today --to tomorrow --json
```

### Today's agenda

```bash
gog calendar events primary --today --json | jq '.events[] | {summary, start: .start.dateTime, end: .end.dateTime}'
```

## Auth Setup (one-time)

If `gog` returns auth errors:

```bash
export GOG_KEYRING_PASSWORD=$(secrets lease gog_keyring_password )
gog auth add joelhooks@gmail.com --services user
# Complete OAuth in browser, then verify:
gog auth list --check
```

## Troubleshooting

- **"Secret not found"**: Keyring password not set. Export `GOG_KEYRING_PASSWORD`.
- **"No auth for gmail"**: Need `gog auth add <email> --services gmail` (or `user` for all).
- **403 insufficient scopes**: Re-auth with `--force-consent` to add missing scopes.
- **Keychain locked**: This system uses `file` backend. Set `GOG_KEYRING_PASSWORD` env var.
