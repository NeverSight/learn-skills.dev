---
name: dingtalk-workspace-cli
description: Use DingTalk Workspace CLI (dws) to manage DingTalk contacts, calendar, todos, attendance, approvals, and more from the command line or AI agent workflows.
triggers:
  - use dingtalk from the command line
  - automate dingtalk with dws
  - search dingtalk contacts
  - create dingtalk todo or calendar event
  - integrate dingtalk with AI agent
  - send dingtalk message via CLI
  - manage dingtalk workspace programmatically
  - dws command help
---

# DingTalk Workspace CLI (dws)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`dws` is an officially open-sourced cross-platform CLI tool from DingTalk that unifies DingTalk's full product suite into a single binary. It is designed for both human users and AI agent workflows. Every response is structured JSON, and built-in Agent Skills let LLMs use DingTalk out of the box.

---

## Installation

### One-liner (recommended)

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.ps1 | iex
```

The installer:
- Auto-detects OS and architecture
- Downloads a pre-compiled binary to `~/.local/bin`
- Installs Agent Skills to `~/.agents/skills/dws`

Add to PATH if needed:
```bash
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc to persist
```

### Build from source

```bash
git clone https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli.git
cd dingtalk-workspace-cli
make build
./dws version
```

---

## Prerequisites & Setup

### 1. Create a DingTalk app

Go to [DingTalk Open Platform](https://open-dev.dingtalk.com/fe/app?hash=%23%2Fcorp%2Fapp#/corp/app), create an enterprise internal app, and note the **Client ID (AppKey)** and **Client Secret (AppSecret)**.

### 2. Configure redirect URL

In the app's **Security Settings**, add `http://127.0.0.1` as a redirect URL.

### 3. Publish the app

Go to **App Release → Version Management** and publish the app so it is active.

### 4. Whitelist (beta)

During the co-creation phase, join the DingTalk DWS group and provide your Client ID and enterprise admin confirmation to be whitelisted.

### 5. Authenticate

```bash
# Via CLI flags
dws auth login --client-id $DWS_CLIENT_ID --client-secret $DWS_CLIENT_SECRET

# Or set env vars first, then login
export DWS_CLIENT_ID=your-app-key
export DWS_CLIENT_SECRET=your-app-secret
dws auth login
```

Tokens are stored encrypted with **PBKDF2 (600,000 iterations) + AES-256-GCM**, keyed to your device MAC address.

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `DWS_CLIENT_ID` | OAuth Client ID (DingTalk AppKey) |
| `DWS_CLIENT_SECRET` | OAuth Client Secret (DingTalk AppSecret) |
| `DWS_CONFIG_DIR` | Override default config directory |
| `DWS_SERVERS_URL` | Custom server registry endpoint |
| `DWS_TRUSTED_DOMAINS` | Comma-separated domains for bearer token (default: `*.dingtalk.com`) |
| `DWS_ALLOW_HTTP_ENDPOINTS` | Set to `1` to allow HTTP on loopback (dev only) |

---

## Key Commands

### Authentication

```bash
dws auth login                        # Authenticate via OAuth device flow
dws auth logout                       # Remove stored credentials
dws auth status                       # Show current auth status
```

### Contacts

```bash
# Search users
dws contact user search --keyword "Alice"

# List departments
dws contact department list

# Get user details
dws contact user get --user-id <userId>
```

### Calendar

```bash
# List events
dws calendar event list

# Create an event
dws calendar event create \
  --title "Q2 Planning" \
  --start "2026-04-01T10:00:00+08:00" \
  --end "2026-04-01T11:00:00+08:00" \
  --attendees "<userId1>,<userId2>"

# Check room availability
dws calendar room list
```

### Todo

```bash
# List tasks
dws todo task list

# Create a task
dws todo task create \
  --title "Prepare quarterly report" \
  --executors "<userId>"

# Complete a task
dws todo task complete --task-id <taskId>
```

### Chat

```bash
# List groups
dws chat group list

# Send a message via webhook
dws chat webhook send \
  --url $DINGTALK_WEBHOOK_URL \
  --content "Deployment succeeded ✅"

# Send robot message
dws chat robot send \
  --group-id <groupId> \
  --content "Hello from dws"
```

### Attendance

```bash
# Get attendance records
dws attendance record list --user-id <userId> --date "2026-03-01"

# List shift schedules
dws attendance shift list
```

### Approval

```bash
# List approval templates
dws approval template list

# Submit an approval instance
dws approval instance create \
  --process-code <processCode> \
  --form-values '{"key":"value"}'

# Query approval instances
dws approval instance list --status RUNNING
```

### DING Messages

```bash
# Send a DING message
dws ding send --receiver-ids "<userId>" --content "Urgent: please review PR"

# Recall a DING message
dws ding recall --ding-id <dingId>
```

### AI Table (aitable)

```bash
# List tables
dws aitable table list --space-id <spaceId>

# Query records
dws aitable record list --table-id <tableId>
```

### Developer Docs

```bash
# Search DingTalk open platform docs
dws devdoc search --keyword "webhook"
```

### Workbench

```bash
# List workbench apps
dws workbench app list
```

---

## Output Formats

All commands support `-f` / `--format`:

```bash
# Human-readable table (default)
dws contact user search --keyword "Alice" -f table

# Structured JSON (for agents and piping)
dws contact user search --keyword "Alice" -f json

# Raw API response
dws contact user search --keyword "Alice" -f raw
```

Save output to a file:
```bash
dws contact user search --keyword "Alice" -f json -o results.json
```

---

## Dry Run

Preview the MCP tool call without executing it:

```bash
dws todo task list --dry-run
dws calendar event create --title "Test" --dry-run
```

---

## Shell Completion

```bash
# Bash
dws completion bash > /etc/bash_completion.d/dws

# Zsh
dws completion zsh > "${fpath[1]}/_dws"

# Fish
dws completion fish > ~/.config/fish/completions/dws.fish
```

---

## Exit Codes

| Code | Category | Meaning |
|---|---|---|
| 0 | Success | Command completed successfully |
| 1 | API | MCP tool call or upstream API failure |
| 2 | Auth | Authentication or authorization failure |
| 3 | Validation | Bad input flags or schema mismatch |
| 4 | Discovery | Service discovery or cache failure |
| 5 | Internal | Unexpected internal error |

When using `-f json`, errors include structured fields: `category`, `reason`, `hint`, `actions`.

---

## Common Patterns

### Scripting: find a user then create a todo assigned to them

```bash
#!/bin/bash
set -euo pipefail

# Search for user and extract userId
USER_ID=$(dws contact user search --keyword "Alice" -f json | \
  jq -r '.data[0].userId')

echo "Found user: $USER_ID"

# Create a todo assigned to that user
dws todo task create \
  --title "Review design doc" \
  --executors "$USER_ID" \
  -f json
```

### Scripting: send a daily standup reminder

```bash
#!/bin/bash
dws ding send \
  --receiver-ids "$TEAM_USER_IDS" \
  --content "🕘 Daily standup in 5 minutes — please join!" \
  -f json
```

### CI/CD: post build status to a DingTalk group

```bash
#!/bin/bash
STATUS=${1:-"unknown"}
EMOJI=$([[ "$STATUS" == "success" ]] && echo "✅" || echo "❌")

dws chat webhook send \
  --url "$DINGTALK_WEBHOOK_URL" \
  --content "$EMOJI Build #$BUILD_NUMBER $STATUS — $BUILD_URL"
```

### Using dws in a Go project

```go
package main

import (
    "os/exec"
    "encoding/json"
    "fmt"
)

type SearchResult struct {
    Data []struct {
        UserID string `json:"userId"`
        Name   string `json:"name"`
    } `json:"data"`
}

func searchDingTalkUser(keyword string) (*SearchResult, error) {
    cmd := exec.Command("dws", "contact", "user", "search",
        "--keyword", keyword,
        "-f", "json",
    )
    out, err := cmd.Output()
    if err != nil {
        return nil, fmt.Errorf("dws error: %w", err)
    }
    var result SearchResult
    if err := json.Unmarshal(out, &result); err != nil {
        return nil, err
    }
    return &result, nil
}

func main() {
    result, err := searchDingTalkUser("Alice")
    if err != nil {
        panic(err)
    }
    for _, u := range result.Data {
        fmt.Printf("User: %s (%s)\n", u.Name, u.UserID)
    }
}
```

---

## AI Agent Integration

`dws` installs Agent Skills automatically. Most AI coding agents (Claude Code, Cursor, Windsurf, etc.) auto-discover skills in `.agents/skills/`.

### Install skills for a specific project

```bash
# Install to current working directory (project-scoped)
curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install-skills.sh | sh
```

Skills are placed at `./.agents/skills/dws/` — commit these to your repo so all collaborators and agents get DingTalk capabilities automatically.

### Typical agent prompts that trigger dws

- "Find the user ID for Alice in DingTalk"
- "Create a todo assigned to Bob for reviewing the PR"
- "List my calendar events for tomorrow"
- "Send a DING message to the team leads"
- "Check attendance records for user X this month"

---

## Architecture Overview

`dws` uses a **discovery-driven pipeline** — no product commands are hardcoded:

```
Market Registry → Discovery → IR (normalized catalog) → CLI (Cobra) → Transport (MCP JSON-RPC)
       ↓               ↓
  mcp.dingtalk.com   Disk cache (TTL + stale-fallback for offline use)
```

1. **Market** — fetches MCP service registry from `mcp.dingtalk.com`
2. **Discovery** — resolves service capabilities, cached to disk with TTL and stale fallback
3. **IR** — normalizes services into a unified product/tool catalog
4. **CLI** — mounts catalog onto a Cobra command tree, maps flags to MCP input params
5. **Transport** — executes MCP JSON-RPC calls with retry, auth injection, and response size limits

---

## Development

```bash
make build                       # Build binary
make test                        # Run unit tests
make lint                        # Format + lint
make package                     # Build all release artifacts locally (goreleaser snapshot)
make release                     # Build and release via goreleaser
```

---

## Troubleshooting

**`dws: command not found`**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Auth errors (exit code 2)**
- Verify `DWS_CLIENT_ID` and `DWS_CLIENT_SECRET` are correct
- Confirm the app is published and the redirect URL `http://127.0.0.1` is configured
- Confirm your enterprise is whitelisted (required during beta)

**Discovery failures (exit code 4)**
- `dws` caches service discovery; if the cache is stale, delete it:
  ```bash
  rm -rf "${DWS_CONFIG_DIR:-$HOME/.config/dws}/cache"
  ```
- Set `DWS_SERVERS_URL` if using a custom registry

**API errors (exit code 1)**
```bash
# Get structured error details
dws todo task list -f json
# Response includes: category, reason, hint, actions
```

**Inspect raw requests**
```bash
dws contact user search --keyword "Alice" -f raw
```

**Allow HTTP for local dev/testing**
```bash
export DWS_ALLOW_HTTP_ENDPOINTS=1
```
