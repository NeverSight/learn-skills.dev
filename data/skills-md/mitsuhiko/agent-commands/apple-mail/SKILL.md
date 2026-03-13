---
name: apple-mail
description: "Search, read, and extract attachments from Apple Mail's local storage. Query emails by sender, recipient, subject, body, date, mailbox, and flags. Read raw RFC822 messages and extract file attachments."
---

# Apple Mail Skill

Search, read, and extract attachments from Apple Mail's local storage on macOS.

## Tool

`apple-mail.sh` — a bash script that queries the Apple Mail SQLite envelope
index and reads `.emlx` files from disk. **Read-only** — it never modifies
mail data.

## Quick Reference

```bash
TOOL=~/Development/agent-stuff/skills/apple-mail/apple-mail.sh

# Search emails
$TOOL search --from "peter@" --subject "dinner" --limit 5
$TOOL search --after 2026-02-01 --has-attachment
$TOOL search --body "invoice" --mailbox "INBOX" --unread
$TOOL search --to "armin@" --before 2025-12-31

# Show message metadata, recipients, attachments, and summary
$TOOL info 783660

# Read the raw RFC822 email (headers + body)
$TOOL read 783660

# Extract attachments to a temp directory (prints the path)
$TOOL attachment 783660                          # all attachments
$TOOL attachment 783660 "Rechnung.pdf"           # specific file

# List all mailboxes with counts
$TOOL mailboxes
```

## Search Options

| Flag | Description |
|------|-------------|
| `--from <addr>` | Sender address substring |
| `--to <addr>` | Recipient address substring |
| `--subject <text>` | Subject substring |
| `--body <text>` | Body/summary text substring |
| `--mailbox <name>` | Mailbox URL substring (e.g. `INBOX`, `Sent`, `Trash`) |
| `--after <YYYY-MM-DD>` | Received after date |
| `--before <YYYY-MM-DD>` | Received before date |
| `--unread` | Only unread messages |
| `--flagged` | Only flagged messages |
| `--has-attachment` | Only messages with attachments |
| `--limit <n>` | Max results (default: 20) |

## Output Format

- `search` returns pipe-delimited table with header row:
  `id|sender|sender_name|subject|received|status|flagged|mailbox|attachments`
- `info` returns structured metadata sections
- `read` outputs raw RFC822 email to stdout
- `attachment` prints the temp directory path to stdout, file listing to stderr

## Notes

- Message IDs are Apple Mail internal ROWIDs (integers), shown in the `id` column
- `.partial.emlx` files contain headers only (body not downloaded); `read` warns about this
- Attachments are copied to a temp directory under `/tmp/`; clean up when done
- The `body` search queries the `summaries` table (Apple Mail's plaintext preview), not the full email body
- Mailbox URLs are percent-encoded (e.g., `%5BGmail%5D` = `[Gmail]`, `%20` = space)
- Deleted messages are excluded from search by default
