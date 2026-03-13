---
name: gmail
description: Access and operate Gmail directly from scripts. Supports multiple accounts (link, list, unlink). Read inbox, search emails, read threads, reply with HTML/attachments/CC/BCC, send emails, manage labels, and manage drafts. On first use, runs an OAuth2 auth flow. Use when the user wants to read, search, reply, send, label, draft emails, or manage multiple Gmail accounts.
---

# Gmail

All scripts in `~/.cursor/skills/gmail/scripts/`. Run from anywhere.

## Account Management

```bash
# List linked accounts
node accounts.mjs --list

# Link an account (runs browser OAuth flow)
node accounts.mjs --link                      # links as "default"
node accounts.mjs --link --account=work       # links as named account

# Unlink an account
node accounts.mjs --unlink --account=work
```

Account storage:
```
~/.cursor/skills/gmail/
├── credentials.json              # shared OAuth2 client (one for all accounts)
└── accounts/
    ├── default/
    │   ├── token.json            # access + refresh tokens  ← SENSITIVE
    │   └── profile.json          # cached email address
    └── work/
        ├── token.json
        └── profile.json
```

**All scripts accept `--account=<name>` (default: `default`)**

## One-Time Setup

```bash
# 1. Get credentials.json from Google Cloud Console:
#    console.cloud.google.com → Gmail API → Credentials → OAuth Client ID → Desktop App → Download JSON
mv ~/Downloads/client_secret_*.json ~/.cursor/skills/gmail/credentials.json

# 2. Link your first account
node ~/.cursor/skills/gmail/scripts/accounts.mjs --link
```

## Scripts

### list.mjs
```bash
node list.mjs [--account=work] [--max=50] [--label=UNREAD] [--next-page=<token>]
```

### search.mjs
```bash
node search.mjs --query="from:stripe" [--account=work] [--max=20] [--next-page=<token>]
# Gmail query syntax: from: to: subject: is:unread has:attachment after:2026/03/01
```

### read.mjs
```bash
node read.mjs --id=<messageId> [--account=work]          # single message
node read.mjs --id=<threadId> --thread [--account=work]  # full thread
node read.mjs --id=<messageId> --raw                     # show raw HTML
```

### reply.mjs
```bash
node reply.mjs --message-id=<id> --body="Text" [--account=work]
node reply.mjs --message-id=<id> --html="<b>Hi</b>"
node reply.mjs --message-id=<id> --body="Hi" --cc="c@d.com" --bcc="e@f.com"
node reply.mjs --message-id=<id> --body="See attached" --attachments="/path/a.pdf"
```

### send.mjs
```bash
node send.mjs --to="a@b.com" --subject="Hi" --body="Text" [--account=work]
node send.mjs --to="a@b.com" --subject="Hi" --html="<h1>Hello</h1>"
node send.mjs --to="a@b.com" --subject="Hi" --body="Hi" --cc="c@d.com" --bcc="e@f.com"
node send.mjs --to="a@b.com" --subject="Files" --body="See attached" --attachments="/path/a.pdf,/path/b.png"
```

### label.mjs
```bash
node label.mjs --list [--account=work]
node label.mjs --id=<messageId> --mark-read [--account=work]
node label.mjs --id=<messageId> --mark-unread
node label.mjs --id=<messageId> --archive
node label.mjs --id=<messageId> --trash
node label.mjs --id=<messageId> --star / --unstar
node label.mjs --id=<messageId> --add-label=IMPORTANT
node label.mjs --id=<messageId> --remove-label=SPAM
```

### draft.mjs
```bash
node draft.mjs --list [--account=work]
node draft.mjs --create --to="a@b.com" --subject="Hi" --body="Text"
node draft.mjs --create --reply-to=<messageId> --body="Reply"   # To: auto-filled
node draft.mjs --read --id=<draftId>
node draft.mjs --send --id=<draftId>
node draft.mjs --delete --id=<draftId>
```

## Abuse Report Workflow

```bash
node search.mjs --query="from:namecheap subject:abuse"
node read.mjs --id=<messageId> --thread
node reply.mjs --message-id=<id> --body="Dear Namecheap Legal & Abuse Team,

Thank you for your message regarding ticket <TICKET-ID>.

We have completed our investigation and taken the following actions:

1. The account in question has been permanently suspended.
2. The reported URL (hxxp:// <PROJECT-ID> [.] sites [.] blink [.] new/) has been deactivated and now returns an HTTP 410 response.
3. All content and deployments associated with this account have been removed.

Our platform has a strict Acceptable Use Policy and we act promptly on all reports.
The blink.new domain is fully compliant with your Terms of Service.

Please let us know if anything further is needed to close this case.

Best regards,
Kai Feng
CEO, Blink.new
support@blink.new"
```

## Cloud Setup

```bash
echo "GMAIL_CREDENTIALS=$(base64 -i ~/.cursor/skills/gmail/credentials.json)"
echo "GMAIL_TOKEN=$(base64 -i ~/.cursor/skills/gmail/accounts/default/token.json)"
```
Set as secrets in your cloud container. Scripts auto-detect env vars over files (default account only).

## Security

- `credentials.json` and `token.json` files are gitignored — never leave your machine
- To revoke access: https://myaccount.google.com/permissions → find your app → Revoke
