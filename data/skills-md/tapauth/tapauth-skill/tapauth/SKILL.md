---
name: tapauth
description: >-
  OAuth token broker for AI agents. Get access tokens for Google, GitHub, Slack, Linear, Notion,
  Vercel, Sentry, Asana, Dropbox, Figma, and 20+ providers with two API calls. Use when your agent
  needs OAuth authentication, API tokens, user authorization, or access to third-party services.
  Handles the full OAuth flow — redirect URL, consent screen, token exchange, refresh — so your
  agent doesn't have to. Works with Claude Code, Cursor, Codex, OpenClaw, and any coding agent
  that needs authenticated API access.
license: MIT
compatibility: Requires curl or any HTTP client. Works with Claude Code, Cursor, OpenClaw, Codex, GitHub Copilot, and any agent with HTTP access.
metadata:
  author: tapauth
  version: "1.0"
  website: https://tapauth.ai
  docs: https://tapauth.ai/docs
---

# TapAuth — OAuth Token Broker for AI Agents

TapAuth lets your agent get OAuth tokens from users without handling credentials directly.
The user approves in their browser. You get a scoped token. That's it.

## The Flow (3 steps)

### Step 1: Create a Grant

```bash
curl -X POST https://tapauth.ai/api/grants \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "github",
    "scopes": ["repo", "read:user"],
    "agent_name": "My Agent"
  }'
```

Response:
```json
{
  "id": "grant_abc123",
  "grant_secret": "gs_live_xxxx",
  "approval_url": "https://tapauth.ai/approve/grant_abc123",
  "status": "pending",
  "expires_at": "2026-02-14T16:10:00Z"
}
```

**Important:** Save `grant_secret` — you need it to retrieve the token. It's only returned once.

### Step 2: User Approves

Show the user the `approval_url`. They'll see:
- Which agent is requesting access
- Which provider and scopes
- Options: approve with full scopes, read-only, or time-limited (1hr/24hr/7d/forever)

The approval URL expires after **10 minutes**. Create a new grant if it expires.

### Step 3: Retrieve the Token

Poll until the user approves:

```bash
curl -X POST https://tapauth.ai/api/grants/grant_abc123/token \
  -H "Content-Type: application/json" \
  -d '{"grant_secret": "gs_live_xxxx"}'
```

| Status | HTTP | Meaning |
|--------|------|---------|
| `pending` | 202 | User hasn't approved yet. Poll again in 2-5 seconds. |
| `approved` | 200 | Token returned in response body. |
| `denied` | 410 | User denied the request. |
| `revoked` | 410 | User revoked access after approving. |
| `link_expired` | 410 | Approval URL expired (10 min). Create a new grant. |

On 200, the response includes:
```json
{
  "access_token": "gho_xxxx",
  "token_type": "bearer",
  "scope": "repo,read:user",
  "provider": "github"
}
```

## Quick Reference

| What | Endpoint | Method |
|------|----------|--------|
| Create grant | `/api/grants` | POST |
| Get token | `/api/grants/{id}/token` | POST |

No API key needed. No signup needed. The user's approval is the only gate.

## Supported Providers

See the `references/` directory for provider-specific scopes, examples, and gotchas:

- **GitHub** → `references/github.md` — repos, issues, PRs, user data
- **Google** → `references/google.md` — Gmail, Drive, Calendar, Sheets, Docs, Contacts (all scopes)
- **Gmail** → `references/gmail.md` — read, send, manage emails (uses `google` provider)
- **Google Drive** → `references/google_drive.md` — focused Drive-only access
- **Google Contacts** → `references/google_contacts.md` — view and manage contacts
- **Google Sheets** → `references/google_sheets.md` — read and write spreadsheets
- **Google Docs** → `references/google_docs.md` — read and write documents
- **Linear** → `references/linear.md` — issues, projects, teams
- **Vercel** → `references/vercel.md` — deployments, projects, env vars, domains
- **Notion** → `references/notion.md` — pages, databases, search
- **Slack** → `references/slack.md` — channels, messages, users, files
- **Sentry** → `references/sentry.md` — error tracking, projects, organizations
- **Asana** → `references/asana.md` — tasks, projects, workspaces

> **Tip:** The focused Google providers (`google_drive`, `google_sheets`, etc.) show simpler consent screens.
> Use them when you only need one Google service. Use `google` when you need multiple services.

## Helper Script

For a complete grant-creation + polling flow, use the bundled script:

```bash
./scripts/tapauth.sh github "repo,read:user" "My Agent"
```

It creates the grant, prints the approval URL, polls for the token, and outputs it when ready.

## Common Patterns

### Ask the user to approve, then proceed
```
1. Create grant for the provider/scopes you need
2. Tell the user: "Please approve access at: {approval_url}"
3. Poll /api/grants/{id}/token every 3 seconds
4. Once approved, use the token for API calls
```

### Handle expiry gracefully
If you get `link_expired` (410), just create a new grant and ask the user again.
If you get `revoked`, the user withdrew access — don't retry.

### Scope selection
Request the minimum scopes you need. Users see exactly what you're asking for
and can approve with reduced permissions. Less scope = more trust = higher approval rate.
