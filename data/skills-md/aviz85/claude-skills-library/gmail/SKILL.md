---
name: gmail
description: "Gmail automation via Google Apps Script. Use for: send emails, read inbox, create drafts, search messages."
version: "1.0.0"
author: aviz85
tags:
  - gmail
  - email
  - google
  - automation
setup: "./SETUP.md"
setup_complete: false
---

# Gmail Integration

> **First time?** If `setup_complete: false` above, run `./SETUP.md` first, then set `setup_complete: true`.

Full Gmail automation via Google Apps Script API: send, read inbox, create drafts, mark as read.

## Workflow

1. **Read inbox** - Get unread emails with optional filters
2. **Send email** - Send with HTML support, CC/BCC
3. **Create drafts** - Save for review before sending
4. **Mark as read** - Update email status

## API Actions

| Action | Description | Required Params | Optional |
|--------|-------------|-----------------|----------|
| `send` | Send email | `to`, `subject`, `body` | `html`, `cc`, `bcc`, `name` |
| `inbox` | Read inbox | - | `maxResults`, `query`, `hours` |
| `draft` | Create draft | `to`, `subject`, `body` | `html`, `replyTo` |
| `markRead` | Mark as read | `messageId` | - |

## Examples

```bash
# Send email
curl -sL "$URL?token=$TOKEN&action=send&to=user@example.com&subject=Hello&body=Message"

# Get last 10 unread emails from last 6 hours
curl -sL "$URL?token=$TOKEN&action=inbox&maxResults=10&hours=6"

# Search for specific emails
curl -sL "$URL?token=$TOKEN&action=inbox&query=from:important@client.com"

# Create draft
curl -sL "$URL?token=$TOKEN&action=draft&to=user@example.com&subject=Follow%20Up&body=Draft"

# Mark email as read
curl -sL "$URL?token=$TOKEN&action=markRead&messageId=MESSAGE_ID"
```

## Response Format

**Send:**
```json
{
  "success": true,
  "email": { "to": "user@example.com", "subject": "Hello", "cc": null, "bcc": null }
}
```

**Inbox:**
```json
{
  "success": true,
  "count": 5,
  "emails": [
    {
      "id": "message_id",
      "threadId": "thread_id",
      "from": "sender@example.com",
      "subject": "Email Subject",
      "date": "2026-01-14T08:30:00Z",
      "snippet": "First 200 chars...",
      "body": "Full email body",
      "isUnread": true,
      "labels": ["INBOX", "UNREAD"]
    }
  ]
}
```

## Important Notes

- **No emojis** in subject/body - URL encoding breaks them
- Default inbox query: `is:unread` with time filter
- `hours` param defaults to 24

## Integration

Works with other skills:
- **whatsapp** - Forward important emails as messages
- **calendar** - Create events from email content
