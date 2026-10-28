---
name: setup
description: Connect and authenticate the UptimeRobot MCP server (OAuth via mcp-remote), OR diagnose why `uptimerobot:*` MCP tools aren't visible in the current session. Invoke this skill any time you cannot see UptimeRobot tools, before telling the user the MCP is misconfigured — Step 0 detects the most common case (server already connected, tools loaded after session start) and resolves it without re-authenticating. Also invoke on `-31001` auth errors or first-time setup.
tags: [setup, auth, oauth, configuration, onboarding]
---

# Setup UptimeRobot

The UptimeRobot MCP server authenticates with **OAuth**. The plugin registers a
small `mcp-remote` launcher that proxies to `https://mcp.uptimerobot.com/mcp`;
on first connection it opens a browser where the user logs into UptimeRobot and
authorizes access. There is no API key to paste — tokens are cached locally by
`mcp-remote`.

Invoke this skill when:
- Any UptimeRobot tool returns `-31001 user_not_found` (the OAuth grant is missing, expired, or revoked).
- The MCP server fails to connect or returns an authentication error.
- The user reports that UptimeRobot tools aren't working.
- The user explicitly asks to connect or reconfigure UptimeRobot.

---

## Step 0 — Check whether setup is already done

**Always run this step first.** It prevents the most common failure mode: looping
the user through setup every session even though the MCP server is already
configured and connected. The MCP connection sometimes finishes after the
assistant's tool list is captured, so the absence of UptimeRobot tools at session
start is *not* proof the server is unconfigured.

Run:

```bash
claude mcp list 2>&1 | grep -i uptimerobot
```

Interpret the output:

- **A line containing `uptimerobot` and `✓ Connected`**: configuration already works and the OAuth grant is valid. Do **not** re-authenticate. Tell the user:

  > Your UptimeRobot MCP server is already configured and connected (`claude mcp list` shows ✓). The tools aren't showing up in this session — that usually means the MCP connection finished after my tool list was captured.
  >
  > **To unblock this session:** fully quit Claude Code (close the terminal, not just `/exit`) and relaunch. The tools will be available from the start.

  Then **stop this skill**. Do not proceed.

- **A line containing `uptimerobot` and `✗ Failed to connect`**: the server is registered but the OAuth grant is stale/expired, or the launcher couldn't start. Go to **Step 3 (Re-authenticate)**.

- **No `uptimerobot` line at all**: the server hasn't been registered yet. Go to **Step 1**.

- **Multiple `uptimerobot` entries** (e.g. `claude.ai UptimeRobot` plus a plain `uptimerobot`): only the plain `uptimerobot` (the `mcp-remote` launcher) matters for this skill. The `claude.ai`-prefixed one is a separate cloud MCP server unrelated to this plugin.

---

## Step 1 — Register the server (manual / dev path only)

If the user installed this plugin from the marketplace (Claude Code) or via the
Cursor plugin, the server auto-registers from `.mcp.json` / `mcp.json` — skip to
Step 2.

For a manual / scripted setup, register the `mcp-remote` launcher:

```bash
claude mcp add uptimerobot -- npx -y mcp-remote@latest https://mcp.uptimerobot.com/mcp
```

If it fails because the server already exists in some scope, remove it from each
scope the error lists, then re-add:

```bash
claude mcp remove uptimerobot -s local
claude mcp remove uptimerobot -s user   # only if the error mentioned user scope
claude mcp add uptimerobot -- npx -y mcp-remote@latest https://mcp.uptimerobot.com/mcp
```

---

## Step 2 — Authenticate (OAuth browser flow)

The first time the server connects, `mcp-remote` opens your default browser to log
into UptimeRobot and authorize access. Tell the user:

> I've registered the UptimeRobot MCP server. The next time it connects it will
> open a browser asking you to log into UptimeRobot and authorize access — there's
> no API key to paste. After you approve, fully quit Claude Code (close the
> terminal) and relaunch so the tools load at session start.
>
> If a browser window doesn't open automatically, copy the authorization URL that
> `mcp-remote` prints in the terminal and open it manually.

Then confirm connectivity with Step 4.

---

## Step 3 — Re-authenticate (fix a stale or revoked grant)

Use this when a tool returns `-31001`, when `claude mcp list` shows
`✗ Failed to connect`, or when the user revoked access. Clear the cached
`mcp-remote` tokens so the next connection re-runs the OAuth flow:

```bash
rm -rf ~/.mcp-auth
```

Then tell the user:

> I've cleared the cached UptimeRobot authorization. Fully quit Claude Code and
> relaunch — the next connection will reopen the browser so you can log in and
> re-authorize.

Then confirm connectivity with Step 4.

---

## Step 4 — Validate connectivity

Run `claude mcp list 2>&1 | grep uptimerobot` and confirm a line shows
`✓ Connected`.

If yes, tell the user:

> Connected! The authorization is cached locally and persists across sessions and
> projects.
>
> **Important:** to use the UptimeRobot tools in this session, fully quit Claude
> Code (close the terminal) and relaunch. The server is connected now, but its
> tools are loaded at session start.

Then optionally call `list-monitors` once tools are available in a fresh session —
but do not block this skill on that.

---

## Step 5 — Handle validation failures

**`claude mcp list` still shows `✗ Failed`:**
1. Confirm the browser flow completed — `mcp-remote` needs the user to finish authorizing in the browser. Re-run Step 3 to force a fresh attempt.
2. Confirm `node`/`npx` is installed and on `PATH` (`npx --version`). `mcp-remote` runs via `npx`; without Node it can't start.
3. If the authorization page errored, have the user retry; if it persists, the account may lack access — see the access-denied note below.

**`-31002 access_denied` when the user later runs a write operation:**
The authorized account doesn't have write permission for that action. Tell the user
to authorize with an account that has write access, then re-run Step 3 to
re-authenticate.

**MCP server not reachable (network error):**
Tell the user:
> The UptimeRobot MCP server at `https://mcp.uptimerobot.com/mcp` isn't reachable right now. Check your internet connection and try again. If the issue persists, visit [uptimerobot.com/status](https://uptimerobot.com/status).

---

## Why am I being asked again?

If the user reports they've connected before but the skill keeps re-running every
session, the cause is almost always one of these:

1. **MCP connection lag**: tools aren't in the assistant's tool list at session start because the MCP handshake hadn't completed yet. **Fix**: Step 0 detects this case and stops the skill from re-prompting.

2. **Expired or revoked OAuth grant**: the cached token expired or access was revoked in the dashboard. **Fix**: re-authenticate via Step 3.

---

## Notes

- **Cursor users:** the project's `mcp.json` registers the same `mcp-remote`
  launcher. Reload Cursor and complete the OAuth browser flow when prompted — no
  `UPTIMEROBOT_API_KEY` env var is needed.
- **Marketplace / plugin install path:** the server auto-registers from
  `.mcp.json` (Claude Code) or `mcp.json` (Cursor). Users only need to complete
  the OAuth browser flow on first connection — no `claude mcp add` required. This
  skill's Step 1 only applies to the manual/dev path.

### Advanced — headless / CI (no browser)

The OAuth browser flow can't run in a headless environment (CI, dev-containers).
There, skip `mcp-remote` and connect over plain HTTP with a Main API key from the
dashboard (**Integrations & API**) instead:

```json
{
  "mcpServers": {
    "uptimerobot": {
      "type": "http",
      "url": "https://mcp.uptimerobot.com/mcp",
      "headers": { "Authorization": "Bearer <MAIN_API_KEY>" }
    }
  }
}
```

Use a Main key for read/write; a Read-only key blocks write tools (`-31002`). This
is the only place the API-key path is needed — the default interactive flow is
OAuth.

## Related

- `manage-monitors` — list and control monitors once connected.
- `errors` — full error code reference.
