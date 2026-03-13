---
name: zd
description: >
  Manage Zendesk support tickets via the `zd` CLI. Use when the user asks about
  Zendesk tickets, support tickets, customer issues, helpdesk operations, or
  ticket triage. Covers listing, searching, creating, updating, and deleting
  tickets, plus authentication setup and Zendesk search queries. Triggers on
  tasks involving "zendesk", "zd", "support ticket", "ticket queue", "helpdesk",
  or "customer support".
license: MIT
metadata:
  author: johanviberg
  version: "1.0.0"
---

# zd — Zendesk CLI

A command-line interface for Zendesk's ticketing REST API, designed for both human users and AI agents.

## Prerequisites: authentication check

Before running any ticket command, verify authentication:

```bash
zd auth status -o json
```

**If exit code 0**: authenticated, proceed with commands.

**If exit code 3 (auth error)**: set up credentials using one of these methods:

### Option A: environment variables (preferred for agents)

```bash
export ZENDESK_SUBDOMAIN="yourcompany"
export ZENDESK_EMAIL="agent@yourcompany.com"
export ZENDESK_API_TOKEN="your-api-token"
```

Or for OAuth:

```bash
export ZENDESK_SUBDOMAIN="yourcompany"
export ZENDESK_OAUTH_TOKEN="your-oauth-token"
```

### Option B: interactive login (for humans)

```bash
# Token auth (non-interactive)
zd auth login --method token --subdomain yourcompany --email agent@co.com --api-token TOKEN

# OAuth (opens browser)
zd auth login --subdomain yourcompany --client-id ID --client-secret SECRET
```

Auth resolution order: env vars > stored credentials file by profile.

## Dynamic command discovery

For the most up-to-date command info, use the CLI's self-describing capabilities:

```bash
# List all commands with flags, types, and defaults
zd commands -o json

# Get JSON Schema for a specific command (for tool calling)
zd schema --command "tickets create"
```

These are always accurate. For a static fallback, see [reference/commands.md](reference/commands.md).

## Core operations

### List tickets

```bash
zd tickets list -o json --limit 25
zd tickets list -o json --status open --sort updated_at --sort-order desc
zd tickets list -o json --assignee 12345 --group 67890

# Sideload users to get requester/assignee names
zd tickets list -o json --include users
zd tickets list -o json --include users --fields id,subject,requester_name,assignee_name
```

### Show a ticket

```bash
zd tickets show 12345 -o json
zd tickets show 12345 -o json --include users
zd tickets show 12345 -o json --include users --fields id,subject,requester_name,requester_email
```

### Create a ticket

```bash
zd tickets create -o json \
  --subject "Password reset not working" \
  --comment "User reports password reset emails are not arriving" \
  --priority high \
  --tags billing,urgent
```

With idempotency (safe for retries):

```bash
zd tickets create -o json \
  --subject "Deploy issue #42" \
  --comment "Deployment failed" \
  --idempotency-key "deploy-42" \
  --if-exists skip
```

### Update a ticket

```bash
zd tickets update 12345 -o json --status solved --comment "Fixed in v2.1"
zd tickets update 12345 -o json --add-tags escalated --priority urgent
zd tickets update 12345 -o json --comment "Internal note" --public=false
zd tickets update 12345 -o json --comment "Looping in team" --cc alice@co.com,bob@co.com
```

### Delete a ticket (two-step safety)

```bash
# Step 1: dry run — returns confirmation ID
zd tickets delete 12345 -o json --dry-run

# Step 2: confirm with the ID from step 1
zd tickets delete 12345 -o json --confirm CONFIRMATION_ID
```

Or skip confirmation:

```bash
zd tickets delete 12345 -o json --yes
```

### Search tickets

```bash
zd tickets search "status:open priority:high" -o json
zd tickets search "tags:vip assignee:jane created>2024-01-01" -o json
zd tickets search "status:open OR status:pending" -o json --sort-by updated_at

# Sideload users
zd tickets search "status:open" -o json --include users
```

For large result sets (>1000):

```bash
zd tickets search "status:closed" -o json --export
```

For the full search syntax reference, see [reference/search-syntax.md](reference/search-syntax.md).

### List ticket comments

```bash
zd tickets comments 12345 -o json
zd tickets comments 12345 -o json --sort-order desc --limit 50
zd tickets comments 12345 -o json --include users
```

### List Help Center articles

```bash
zd articles list -o json
zd articles list -o json --limit 50 --sort-by updated_at
```

### Show an article

```bash
zd articles show 360001234567 -o json
```

### Search Help Center articles

```bash
zd articles search "password reset" -o json
zd articles search "billing FAQ" -o json --limit 10
```

## Output handling

### Formats

| Flag | Format | Use case |
|------|--------|----------|
| `-o json` | JSON | Structured parsing, single objects or arrays |
| `-o ndjson` | Newline-delimited JSON | Streaming, piping to `jq`, bulk processing |
| `-o text` | Table (default) | Human-readable display |

### Field projection

Limit output to specific fields:

```bash
zd tickets list -o json --fields id,status,subject,updated_at
```

### Sideloading users

Use `--include users` on `list`, `show`, or `search` to resolve `requester_id` and `assignee_id` into names and emails. The output is enriched with `requester_name`, `requester_email`, `assignee_name`, and `assignee_email` fields:

```bash
zd tickets show 12345 -o json --include users --fields id,subject,requester_name,assignee_name
```

### Pagination

List and search commands return a page at a time. When more results exist, use the cursor from stderr:

```bash
zd tickets list -o json --cursor "eyJhZnRlciI6..."
```

### Error output

Errors always go to stderr. When using `-o json`, errors are structured:

```json
{"code": "not_found", "message": "Ticket 99999 not found", "exitCode": 5}
```

## Error handling

| Exit code | Meaning | Recovery |
|-----------|---------|----------|
| 0 | Success | — |
| 1 | General error | Check stderr message |
| 2 | Argument error | Fix flags or arguments |
| 3 | Auth error | Run `zd auth login` or set env vars |
| 4 | Rate limited | Auto-retried 3x; wait for `retryAfter` seconds |
| 5 | Not found | Verify ticket ID exists |

For detailed error handling, see [reference/error-handling.md](reference/error-handling.md).

## Common workflows

For multi-step recipes including bulk operations, triage, reporting, and paginated iteration, see [reference/workflows.md](reference/workflows.md).

## Agent best practices

When using `zd` from an AI agent or automated pipeline:

- **Always use** `--non-interactive -o json` to prevent prompts and get parseable output
- **Parse stdout** for data, **stderr** for diagnostics and pagination cursors
- **Use `--trace-id`** to correlate API requests with agent actions
- **Use `--profile`** when operating across multiple Zendesk accounts
- **Use `--idempotency-key`** on creates to make operations safely retryable
- **Use `--dry-run` then `--confirm`** for deletes to prevent accidental data loss
- **Prefer token auth** via env vars — OAuth requires a browser
- **Use `--fields`** to minimize response size when you only need specific data
- **Use `--include users`** to resolve requester/assignee IDs into names without extra API calls
- **Use `--demo`** to explore commands without authentication — generates synthetic data locally
