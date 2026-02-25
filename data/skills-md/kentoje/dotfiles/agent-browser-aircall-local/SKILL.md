---
name: agent-browser-aircall-local
description: >
  Open a headless browser authenticated with Aircall staging credentials for localhost development
---

# Agent Browser - Aircall Local Development

Opens an `agent-browser` instance authenticated with Aircall staging credentials for localhost development.

## Usage

Use this skill when you need to browse a localhost app (`http://localhost:<PORT>`) authenticated against the Aircall staging environment.

**User provides:**

- `PORT` - The localhost port (e.g., `3000`, `5173`)
- `TARGET_PATH` - The path to navigate to after auth (e.g., `/playground`, `/...`)

## Steps to Execute

### 1. Load the agent-browser CLI reference

Always start by running `agent-browser --help` to get the full, up-to-date CLI reference:

```bash
agent-browser --help
```

This ensures you have the latest commands and options available.

### 2. Retrieve Fresh Staging Token

Depending on which agent runtime you are in, use the appropriate tool:

**Claude Code** — call the MCP tool:

```
mcp__aircall-personal-tools__aircall_staging_auth_token
```

**OpenCode** — call the tool:

```
AircallStagingAuthToken
```

Both tools take no arguments and return a JSON object:

```json
{ "accessToken": "eyJhbG...", "refreshToken": "eyJhbG..." }
```

Extract both `accessToken` and `refreshToken` from the response.

### 3. Navigate to SSO callback with token

Build the SSO callback URL and open it in the browser:

```bash
agent-browser --session aircall-local open "http://localhost:<PORT>/sso/callback?token=<ACCESS_TOKEN>&refresh_token=<REFRESH_TOKEN>&redirect=<TARGET_PATH>"
```

**Parameters:**

| Param              | Source                      |
| ------------------ | --------------------------- |
| `<PORT>`           | User-provided localhost port |
| `<ACCESS_TOKEN>`   | `accessToken` from step 2   |
| `<REFRESH_TOKEN>`  | `refreshToken` from step 2  |
| `<TARGET_PATH>`    | User-provided target path (URL-encoded if needed) |

**What the app does:**

1. Reads `token` and `refresh_token` from the query parameters
2. Stores them locally (cookie/localStorage)
3. Redirects to `<TARGET_PATH>` — the user is now authenticated

### 4. Take Snapshot of Page

After navigation completes, get an interactive snapshot to see the page state:

```bash
agent-browser --session aircall-local snapshot -i
```

This returns interactive elements with refs (`@e1`, `@e2`, etc.) for further interaction.

### 5. Interact with Page Elements

Use the refs from the snapshot to interact:

```bash
# Click an element
agent-browser --session aircall-local click @e1

# Fill a text field
agent-browser --session aircall-local fill @e2 "some text"

# Take screenshot
agent-browser --session aircall-local screenshot /tmp/screenshot.png
```

**Always re-snapshot after page changes** to get updated refs:

```bash
agent-browser --session aircall-local snapshot -i
```

## Complete Example Flow

```bash
# 1. Run --help to load CLI reference
agent-browser --help

# 2. Get token (via the appropriate tool for your runtime — see step 2)

# 3. Open browser with auth
agent-browser --session aircall-local open "http://localhost:3000/sso/callback?token=eyJhbG...&refresh_token=eyJhbG...&redirect=/playground"

# 4. Get interactive snapshot
agent-browser --session aircall-local snapshot -i

# 5. Interact based on snapshot refs
agent-browser --session aircall-local click @e5
agent-browser --session aircall-local snapshot -i  # Re-snapshot after click

# 6. Fill form fields
agent-browser --session aircall-local fill @e3 "test input"

# 7. Take screenshot for verification
agent-browser --session aircall-local screenshot /tmp/result.png
```

## Session Management

| Command                                       | Description                  |
| --------------------------------------------- | ---------------------------- |
| `--session aircall-local`                     | Use isolated browser context |
| `agent-browser --session aircall-local close` | Close browser session        |
| `agent-browser sessions`                      | List active sessions         |

## Browser Modes

- **Headless** (default): No visible browser window
- **Headed**: Add `--headed` flag to see the browser

```bash
agent-browser --session aircall-local --headed open "http://localhost:3000/sso/callback?token=..."
```

## Troubleshooting

### Token Expired

Re-run the appropriate token tool for your runtime (see step 2) to get a fresh token.

### Page Not Loading

1. Verify the localhost server is running on the specified port
2. Check the snapshot for any error messages
3. Take a screenshot: `agent-browser --session aircall-local screenshot /tmp/debug.png`

### Element Not Found

1. Re-snapshot to get current page state
2. Use `snapshot -i -c` for more compact output
3. Verify the element exists in the snapshot before interacting

## Technical Details

- **SSO Route**: `/sso/callback`
- **Query Params**: `token`, `refresh_token`, `redirect`
- **Session Name**: `aircall-local`
- **Auth Endpoint**: `https://id.aircall-staging.com/auth/v1/users/session`
