---
name: gmail-inbox
description: Manage emails across multiple Gmail accounts with unified tooling. Use when user asks to check email, read inbox, label emails, archive messages, or manage Gmail across accounts.
---

# Gmail Inbox Management

## Goal
Check and manage emails across multiple Gmail accounts using unified tooling.

## Scripts
- `./scripts/gmail_unified.py` - Check and manage inboxes
- `./scripts/gmail_multi_auth.py` - Authenticate accounts
- `./scripts/gmail_bulk_label.py` - Bulk labeling
- `./scripts/gmail_create_filters.py` - Create filters
- `./scripts/gmail_auth.py` - Auth helper

## Quick Reference

```bash
# Check unread across all accounts
python3 ./scripts/gmail_unified.py --query "is:unread" --limit 50

# Check specific account only
python3 ./scripts/gmail_unified.py --query "is:unread" --account yourcompany

# List registered accounts
python3 ./scripts/gmail_unified.py --accounts

# Label and archive emails
python3 ./scripts/gmail_unified.py --query "from:notifications@" --label "Notifications" --archive

# Mark as read
python3 ./scripts/gmail_unified.py --query "from:noreply@" --mark-read

# Dry run (preview)
python3 ./scripts/gmail_unified.py --query "subject:invoice" --label "Invoices" --dry-run
```

## Account Registry

| Account | Email | Credentials | Token |
|---------|-------|-------------|-------|
| youruser | you@example.com | credentials.json | token_youruser.json |
| yourcompany | you@yourdomain.com | credentials_yourcompany.json | token_yourcompany.json |

## Troubleshooting Auth Errors

**"Token file not found"**
```bash
python3 ./scripts/gmail_multi_auth.py --account yourcompany --email you@yourdomain.com
```

**"invalid_scope: Bad Request"**
```bash
rm token_youruser.json
python3 ./scripts/gmail_multi_auth.py --account youruser --email you@example.com
```

**"Failed to authenticate"**
Check that credentials.json exists in root directory.

## Required Scopes
- `gmail.modify` - Read/write emails
- `gmail.labels` - Create/manage labels
- `gmail.settings.basic` - Manage settings
- `spreadsheets` - Google Sheets access
- `drive` - Google Drive access

## Credentials Location
All credential files should be in the workspace root:
- `credentials.json` / `credentials_yourcompany.json` - OAuth client configs
- `token_*.json` - Auth tokens (auto-generated)
- `gmail_accounts.json` - Account registry

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | No | Gmail search query (e.g., 'is:unread') |
| `account` | string | No | Specific account name from registry |
| `limit` | integer | No | Max emails to fetch (default: 50) |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `emails` | array | List of email objects with subject, from, date, snippet |

### Credentials
| Name | Source |
|------|--------|
| `credentials.json` | file |
| `token_*.json` | file (auto-generated) |

### Composable With
Skills that chain well with this one: `gmail-label`, `instantly-autoreply`

### Cost
Free (Gmail API)
