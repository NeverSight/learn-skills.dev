---
name: authenticate
description: Sign in to the Finance District agent wallet. Use when you or the user want to log in, sign in, connect, set up, or configure the wallet, or when any wallet operation fails with authentication or "not authenticated" errors. This skill is a prerequisite before sending tokens, swapping, checking balances, or any other wallet operation.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx setup*)", "Bash(fdx status*)", "Bash(fdx logout*)"]
---

# Authenticating with the Finance District Agent Wallet

When the wallet is not signed in (detected via `fdx status` or when wallet operations fail with authentication errors), use the `fdx` CLI to authenticate via OAuth 2.1.

Authentication requires a browser — the agent guides the human through the flow, but the human must complete the browser-based authorization step.

## Checking Authentication Status

```bash
fdx status
```

Displays the MCP server URL, token state, expiry, and whether a refresh token is available.

## Authentication Flow

FDX supports two OAuth flows depending on the environment:

### Browser Flow (default)

Use when the human has a browser available on the same machine:

```bash
fdx setup
```

This will:

1. Register a client with the MCP server
2. Print an authorization URL
3. Start a local callback server on port 6260
4. Wait for the human to complete browser authorization
5. Exchange the authorization code for tokens

**Tell your human:** "Please open the URL in your browser and authorize the wallet. I'll wait for the callback."

### Device Flow

Use when the human cannot open a browser on the same machine (e.g. remote server, headless environment):

```bash
fdx setup --device
```

This will:

1. Register a device client with the MCP server
2. Display a verification URL and a user code
3. Poll for authorization completion

**Tell your human:** "Please go to the verification URL on any device, enter the code shown, and authorize. I'll wait here."

## Logging Out

```bash
fdx logout
```

Removes stored credentials. The human will need to run `fdx setup` again to re-authenticate.

## Example Session

```bash
# Check current status
fdx status

# If not authenticated, start login
fdx setup

# Human completes browser authorization...

# Confirm authentication succeeded
fdx status
```

## Token Lifecycle

- Tokens auto-refresh on subsequent `fdx call` commands if a refresh token is available
- If the token is expired and no refresh token exists, the human must run `fdx setup` again
- Token state is stored locally (default: `~/.fdx/auth.json`)

## Environment Variables

| Variable           | Description           | Default                                |
| ------------------ | --------------------- | -------------------------------------- |
| `FDX_MCP_SERVER`   | MCP server URL        | `https://mcp.fd.xyz`                   |
| `FDX_REDIRECT_URI` | OAuth callback URI    | `http://localhost:6260/oauth/callback` |
| `FDX_STORE_PATH`   | Token store file path | `~/.fdx/auth.json`                     |

## Error Handling

- "not authenticated" — Run `fdx setup` to authenticate
- "token expired" with refresh token — Will auto-refresh on next call; no action needed
- "token expired" without refresh token — Run `fdx setup` again
- "OAuth state mismatch" — Possible CSRF; restart with `fdx setup`
- "Callback server error" — Port 6260 may be in use; try `--device` flow instead
