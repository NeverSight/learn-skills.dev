---
name: granola-auth
description: Authenticate with Granola and save OAuth tokens to .env
allowed-tools: Bash
---

Authenticate with Granola. Try to silently refresh the existing token first;
only open the browser for a full OAuth flow if refresh fails or no token exists.

> **Note:** `install.sh` replaces the paths below with absolute paths on your
> machine when it writes this file to `~/.claude/skills/granola-auth/SKILL.md`.
> Do not use this file directly — run `bash install.sh` instead.

## Step 1 — Try refresh first

Run:

```
node /path/to/granola-skill/refresh.js
```

- If it exits 0: tokens are valid (or were refreshed). Report the new expiry and stop.
- If it exits non-zero: proceed to Step 2.

## Step 2 — Full OAuth flow (browser)

Run:

```
node /path/to/granola-skill/auth.js
```

This will:
1. Discover the Granola OAuth endpoints automatically
2. Register a temporary OAuth client via Dynamic Client Registration
3. Open the browser to log in with Google via Granola
4. Capture the OAuth callback on localhost:3334
5. Exchange the authorization code for access + refresh tokens
6. Save all tokens to a `.env` file in the current working directory
7. Prompt the user to configure MCP for Claude Code, Cursor, or both

After either step succeeds, display the contents of `.env` (mask token values
to show only first + last 6 chars), confirm the path where it was written, and
report which MCP config files were updated.

If Step 2 fails, show the full error output and suggest:
- Checking that port 3334 is not in use (`lsof -i :3334`)
- Ensuring Node.js 22+ is installed (`node --version`)
- Verifying internet connectivity to mcp.granola.ai
