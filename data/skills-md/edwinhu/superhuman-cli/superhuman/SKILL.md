---
name: superhuman
description: This skill should be used when the user asks to "check email", "read inbox", "send email", "reply to email", "search emails", "archive email", "snooze email", "star email", "add label", "forward email", "download attachment", "switch email account", "use snippet", "search contacts", "ask ai about email", "find email about", "what did someone say about", or needs to interact with Superhuman email client. For calendar, events, and scheduling use the morgen skill instead.
allowed-tools: Bash(superhuman:*)
---

# Superhuman Email & Calendar Automation

CLI and MCP server to control [Superhuman](https://superhuman.com) email client via Chrome DevTools Protocol (CDP).

## Requirements

- [Bun](https://bun.sh) runtime
- Superhuman.app running with remote debugging enabled

## Setup

```bash
# Install dependencies (if needed)
bun install

# Start Superhuman with CDP enabled
/Applications/Superhuman.app/Contents/MacOS/Superhuman --remote-debugging-port=9400
```

### Container / Remote CDP

When running inside a Docker container or connecting to a remote host, set `CDP_HOST`:

```bash
export CDP_HOST=host.docker.internal   # Docker container → host
superhuman account auth                # Extract tokens via remote CDP
```

After initial `account auth`, most operations use cached tokens and don't need CDP. Tokens are stored at `~/.config/superhuman-cli/tokens.json` and auto-refresh via OAuth.

## CLI Usage

```bash
# Check connection status
superhuman status

# Account management
superhuman account auth
superhuman account list
superhuman account switch 2
superhuman account switch user@example.com
```

### Reading Email

```bash
# List recent inbox emails
superhuman inbox
superhuman inbox --limit 20 --json

# Search emails
superhuman search "from:john subject:meeting"
superhuman search "project update" --limit 20
superhuman search "from:anthropic" --include-done    # Search all including archived

# Read a specific thread (requires --account)
superhuman read <thread-id> --account user@gmail.com
superhuman read <thread-id> --account user@gmail.com --context 3   # Full body for last 3 only
superhuman read <thread-id> --account user@gmail.com --json
```

### Ask AI

Use Superhuman's AI to search emails, answer questions, or ask about specific threads:

```bash
# Search emails with natural language
superhuman ai "find emails about the Stanford cover letter"
superhuman ai "what did John say about the deadline?"

# Compose with AI
superhuman ai "Write an email inviting the team to a planning meeting"

# Ask about a specific thread
superhuman ai <thread-id> "summarize this thread"
superhuman ai <thread-id> "what are the action items?"
superhuman ai <thread-id> "draft a professional reply"
```

The AI automatically determines whether to search, compose, or answer based on your prompt.

### Contacts

```bash
# Search contacts by name
superhuman contact search "john"
superhuman contact search "john" --limit 5 --json

# Search contacts in a specific account (without switching UI)
superhuman contact search "john" --account user@gmail.com
```

### Multi-Account Support

The `--account` flag allows operations on any linked account without switching the Superhuman UI:

```bash
# Search contacts in a specific account
superhuman contact search "john" --account user@gmail.com

# Works with both Gmail and Microsoft/Outlook accounts
superhuman contact search "john" --account user@company.com
```

**How it works:** The CLI extracts OAuth tokens directly from Superhuman and makes API calls to Gmail or Microsoft Graph. Tokens are cached to disk with automatic background refresh when expiring.

### Token Management

```bash
# Extract and cache tokens from Superhuman (required once)
superhuman account auth

# Tokens are automatically refreshed when expiring
# If refresh fails, you'll see: "Token for user@email.com expired. Run 'superhuman account auth' to re-authenticate."
```

Tokens are stored in `~/.config/superhuman-cli/tokens.json` and automatically refreshed using OAuth refresh tokens when they expire (within 5 minutes of expiry). No CDP connection is needed for token refresh.

### Composing Email

Recipients can be specified as email addresses or contact names. Names are automatically resolved to email addresses via contact search.

```bash
# Create a draft (using email or name)
superhuman draft create --to user@example.com --subject "Hello" --body "Hi there!"
superhuman draft create --to "john" --subject "Hello" --body "Hi there!"

# List drafts (shows both provider and native Superhuman drafts)
superhuman draft list
superhuman draft list --account user@example.com

# Send an email
superhuman send --to user@example.com --subject "Quick note" --body "FYI"

# Reply to a thread
superhuman reply <thread-id> --body "Thanks!"
superhuman reply <thread-id> --body "Thanks!" --send

# Reply-all
superhuman reply-all <thread-id> --body "Thanks everyone!"

# Forward
superhuman forward <thread-id> --to colleague@example.com --body "FYI"

# Update a draft
superhuman draft update <draft-id> --body "Updated content"

# Delete drafts
superhuman draft delete <draft-id>
superhuman draft delete <draft-id1> <draft-id2>

# Send a draft by ID
superhuman send --draft <draft-id>

# Send a Superhuman draft with content
superhuman draft send <draft-id> --account=user@example.com --to=recipient@example.com --subject="Subject" --body="Body"
```

#### Draft Sources

The `draft list` command shows drafts from multiple sources with a "Source" column:

| Source | Description | Example ID |
|--------|-------------|------------|
| `native` | Superhuman-only drafts | `draft00ce4679cc58a64c` |
| `gmail` | Synced to Gmail | Gmail message ID |
| `outlook` | Synced to Outlook | Outlook message ID |

Native Superhuman drafts (IDs starting with `draft00...`) are fetched from Superhuman's backend API and only exist in Superhuman. Provider-synced drafts are fetched from Gmail/Outlook APIs and are visible in native email clients.

#### Drafts Limitation

Drafts created via `draft create` use **native Gmail/Outlook APIs**, not Superhuman's proprietary draft system. This means:

| Where | Visible? |
|-------|----------|
| Native Gmail/Outlook web | Yes |
| Native mobile apps | Yes |
| Superhuman UI | No |

This is acceptable for CLI workflows where you iterate on drafts with LLMs and send via `--send` flag. If you need to edit in Superhuman UI, open the draft in native Gmail/Outlook first.

### Managing Threads

```bash
# Archive
superhuman archive <thread-id>
superhuman archive <thread-id1> <thread-id2>

# Delete (trash)
superhuman delete <thread-id>

# Mark as read/unread
superhuman mark read <thread-id>
superhuman mark unread <thread-id>

# Star / Unstar
superhuman star add <thread-id>
superhuman star remove <thread-id>
superhuman star list

# Snooze / Unsnooze
superhuman snooze set <thread-id> --until tomorrow
superhuman snooze set <thread-id> --until next-week
superhuman snooze set <thread-id> --until "2024-02-15T14:00:00Z"
superhuman snooze cancel <thread-id>
superhuman snooze list
```

### Snippets

Reusable email templates stored in Superhuman. Snippets support template variables like `{first_name}`.

```bash
# List all snippets
superhuman snippet list
superhuman snippet list --json

# Use a snippet to create a draft (fuzzy name matching)
superhuman snippet use "zoom link" --to user@example.com

# Substitute template variables
superhuman snippet use "share recordings" --to user@example.com --vars "date=Feb 5,student_name=Jane"

# Send immediately using a snippet
superhuman snippet use "share recordings" --to user@example.com --vars "date=Feb 5" --send
```

### Labels

```bash
# List all labels
superhuman label list

# Get labels on a thread
superhuman label get <thread-id>

# Add/remove labels
superhuman label add <thread-id> --label Label_123
superhuman label remove <thread-id> --label Label_123
```

### Attachments

```bash
# List attachments in a thread
superhuman attachment list <thread-id>

# Download all attachments from a thread
superhuman attachment download <thread-id>
superhuman attachment download <thread-id> --output ./downloads

# Download specific attachment
superhuman attachment download --attachment <attachment-id> --message <message-id> --output ./file.pdf
```

### Calendar

Superhuman has built-in calendar support, but prefer `morgen` CLI for calendar operations — it supports proper calendar filtering. See the `morgen` skill.

### Options

| Option | Description |
|--------|-------------|
| `--account <email>` | Account to operate on (default: current account) |
| `--to <email\|name>` | Recipient email or name (names auto-resolved via contacts) |
| `--cc <email\|name>` | CC recipient (can be used multiple times) |
| `--bcc <email\|name>` | BCC recipient (can be used multiple times) |
| `--subject <text>` | Email subject |
| `--body <text>` | Email body (plain text, converted to HTML) |
| `--html <text>` | Email body as raw HTML |
| `--send` | Send immediately instead of saving draft (for reply/reply-all/forward/snippet) |
| `--vars <pairs>` | Template variable substitution: `"key1=val1,key2=val2"` (for snippet use) |
| `--draft <id>` | Draft ID to send (for send command) |
| `--label <id>` | Label ID (for label add/remove) |
| `--until <time>` | Snooze until time: preset or ISO datetime |
| `--output <path>` | Output path for downloads |
| `--attachment <id>` | Specific attachment ID |
| `--message <id>` | Message ID (required with --attachment) |
| `--limit <number>` | Number of results (default: 10) |
| `--include-done` | Search all emails including archived (for search) |
| `--context <number>` | Number of messages to show full body (default: all, for read) |
| `--json` | Output as JSON |
| `--port <number>` | CDP port (default: 9400) |

## Common Workflows

### Triage Inbox

```bash
superhuman inbox --limit 20
superhuman read <thread-id> --account user@gmail.com
superhuman archive <thread-id1> <thread-id2>
superhuman snooze set <thread-id> --until tomorrow
superhuman star add <thread-id>
```

### Reply to Email

For **drafting** replies (recommended — lets the user review before sending):
```bash
superhuman read <thread-id> --account user@gmail.com
superhuman reply <thread-id> --body "Thanks for the update."
```

For **sending** replies immediately:
```bash
superhuman reply <thread-id> --body "Thanks for the update." --send
```

If `superhuman reply` fails (e.g. MS Graph 400 error on Outlook accounts), use the AI approach:
```bash
superhuman ai <thread-id> "draft a professional reply saying thanks for the update"
```

### Search and Process

```bash
superhuman search "from:boss@company.com" --limit 10
superhuman search "is:unread has:attachment"
superhuman search "from:anthropic" --include-done    # Include archived
```

### Multi-Account

```bash
superhuman account list
superhuman account switch work@company.com
superhuman contact search "john" --account personal@gmail.com
```

### Snippets

```bash
superhuman snippet list
superhuman snippet use "meeting invite" --to colleague@example.com --vars "date=Feb 10" --send
```

## Snooze Presets

| Preset | When |
|--------|------|
| `tomorrow` | 9am next day |
| `next-week` | 9am next Monday |
| `weekend` | 9am Saturday |
| `evening` | 6pm today |
| ISO datetime | Exact time (e.g., `2024-02-15T14:00:00Z`) |

## Output Formats

Most commands support `--json` for structured output:

```bash
superhuman inbox --json | jq '.[] | {id, subject, from}'
```

## Troubleshooting

### Token Expired

```bash
superhuman account auth    # Re-extract tokens from Superhuman
```

Tokens auto-refresh. If refresh fails: `Token for user@email.com expired. Run 'superhuman account auth' to re-authenticate.`

### Connection Failed

1. Check if Superhuman is installed at `/Applications/Superhuman.app`
2. Launch with debugging: `/Applications/Superhuman.app/Contents/MacOS/Superhuman --remote-debugging-port=9400`
3. Verify: `superhuman status`

**From a container**: Ensure `CDP_HOST=host.docker.internal` is set and the container was started with `--add-host=host.docker.internal:host-gateway`. The CLI skips local app launch when `CDP_HOST` is non-localhost.

### Thread Not Found

Thread IDs come from inbox/search. Use `--json` to get exact IDs:

```bash
superhuman inbox --json | jq '.[0].id'
```

## How It Works

### Direct API (Primary)

Most operations use **direct Gmail API and Microsoft Graph API** calls with cached OAuth tokens:

| Operation | Gmail API | MS Graph API |
|-----------|-----------|--------------|
| List inbox | `GET /messages?q=label:INBOX` | `GET /mailFolders/Inbox/messages` |
| Search | `GET /messages?q=...` | `GET /messages?$search=...` |
| Labels | `POST /threads/{id}/modify` | `PATCH /messages/{id}` |
| Read status | Add/remove UNREAD label | `PATCH /messages/{id}` with `isRead` |
| Archive | Remove INBOX label | `POST /messages/{id}/move` |
| Star | Add STARRED label | `PATCH /messages/{id}` with `flag` |
| Attachments | `GET /messages/{id}/attachments/{id}` | `GET /messages/{id}/attachments/{id}` |
| Contacts | Google People API | MS Graph People API |
| Snippets | Superhuman backend API | Superhuman backend API |

OAuth tokens (including refresh tokens) are extracted from Superhuman and cached to disk. When tokens expire, they are automatically refreshed via OAuth endpoints without requiring CDP connection.

### CDP (Secondary)

Chrome DevTools Protocol is only needed for:

- `account auth` — One-time token extraction from `window.GoogleAccount` (also stores AI user prefix)
- `status` — Check Superhuman connection
- `search` / `inbox` (when no cached tokens) — Fallback via Superhuman's portal API

All other operations (read, reply, forward, draft, archive, delete, labels, star, snooze, attachments, contacts, snippets) use direct API with cached tokens.

### Benefits

- **Reliability**: Direct API calls don't depend on Superhuman's UI state
- **Speed**: No CDP round-trips for most operations
- **Offline from CDP**: After initial `account auth`, most operations work without CDP
- **Multi-account**: Cached tokens enable operating on any linked account

Supports both Gmail and Microsoft/Outlook accounts.
