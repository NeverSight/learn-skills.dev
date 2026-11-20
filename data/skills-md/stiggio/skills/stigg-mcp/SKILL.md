---
name: stigg-mcp
description: SETUP skill — use when connecting an AI client to the Stigg MCP server at https://mcp.stigg.io, or when picking between the Stigg CLI and the Stigg MCP server. Covers Claude Code, Claude Desktop, ChatGPT, Cursor, VS Code, Windsurf, Codex, Continue.dev, and any MCP-compatible client. Triggers include "set up Stigg MCP", "install Stigg MCP", "connect Stigg to Claude", "connect Stigg to Cursor", "add Stigg MCP server", "stigg mcp add", "/mcp doesn't show stigg", "Stigg MCP not connecting", "X-API-KEY header for Stigg MCP", "@stigg/typescript-mcp", "stdio bridge for Stigg", "Stigg CLI vs MCP", "Stigg HTTP transport", or any first-time Stigg-with-an-agent setup. Skip for using the Stigg MCP after it's already connected — operational work belongs to the relevant pillar (entitlements, credits, pricing-modeling, subscriptions, widgets).
---

# Stigg MCP — Connect Once, Use Everywhere

The **Stigg MCP server** at `https://mcp.stigg.io` exposes a Stigg environment to any MCP-compatible AI client. The agent can then provision customers, manage subscriptions, check entitlements, and report usage — in natural language — without writing API calls.

> **Status:** the Stigg MCP server is currently in **public beta**. Re-confirm via [docs.stigg.io](https://docs.stigg.io/api-and-sdks/mcp-server) before relying on edge behavior.

## Before You Start

Per the umbrella `stigg` skill: **search first**. If the user already has the Mintlify Stigg docs MCP available (`search_stigg`), use it to confirm the latest install command. Re-fetch [the MCP-server docs page](https://docs.stigg.io/api-and-sdks/mcp-server) when in doubt.

## The 3-Step Setup

### Step 0 — You need a Stigg account

If you don't already have one: sign up at [app.stigg.io](https://app.stigg.io). New accounts come with a default sandbox environment. Production environments are on the Scale plan.

If your agent runs the install command before Step 0 is done, the smoke test will fail with `401 Unauthenticated`.

### Step 1 — Get an API key

1. In the Stigg app, go to **Integrations → API keys**.
2. Pick the environment (sandbox / staging / production). **Default to sandbox for AI-assisted dev.**
3. Either copy the **Full access** key or click **+ Add scoped key** (Scale plan) and grant only the permissions the agent needs. Treat the key like a password.

> **For better isolation, create a dedicated scoped key per AI client** (e.g., "Claude Code – Dev", "Cursor – Staging").

### Step 2 — Configure the client (snippets per AI client)

#### Claude Code (HTTP transport — preferred)

```bash
claude mcp add stigg \
  --header "X-API-KEY: <YOUR_API_KEY>" \
  --transport http https://mcp.stigg.io
```

Then start a new Claude Code session and run `/mcp` to confirm `stigg` is connected and its tools are listed.

#### Claude Desktop

Edit:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add under `mcpServers`:

```json
{
  "mcpServers": {
    "stigg": {
      "url": "https://mcp.stigg.io",
      "headers": {
        "X-API-KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

Restart Claude Desktop.

#### ChatGPT

**Settings → Connectors**, add a new MCP server:

| Field | Value |
|---|---|
| Server URL | `https://mcp.stigg.io` |
| Connection | API Key (header) |
| Header name | `X-API-KEY` |
| Header value | `<YOUR_API_KEY>` |

#### Cursor / VS Code / Windsurf / Codex / generic clients (stdio bridge)

These clients use the local stdio bridge `@stigg/typescript-mcp` (run via `npx`). Edit the relevant config file (`~/.cursor/mcp.json` for Cursor; **MCP: Open User Configuration** in VS Code; the equivalent for Windsurf/Codex), and add:

```json
{
  "mcpServers": {
    "stigg_typescript_api": {
      "command": "npx",
      "args": ["-y", "@stigg/typescript-mcp"],
      "env": {
        "STIGG_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

Restart the client. For any client that supports HTTP transport natively, prefer the `mcp.stigg.io` HTTP form (same shape as the Claude Desktop snippet).

> The **canonical, always-current** install matrix lives at [docs.stigg.io/api-and-sdks/mcp-server](https://docs.stigg.io/api-and-sdks/mcp-server). Refresh from there if a snippet here doesn't work.

## Smoke Test

After install, confirm:

1. **Tool listing.** In Claude Code: `/mcp` — `stigg` should appear with its tools.
2. **Search docs.** Ask: *"Search Stigg docs for 'create a customer'."* If the agent invokes `search_docs` (or equivalent) and returns a doc snippet, transport is alive.
3. **No-op read.** Ask: *"List the first 3 customers in this Stigg environment."* This exercises a read against the live env. Expected on a fresh sandbox: an empty list — *that's a pass.*

If any step fails, the most common causes are: wrong header name (`X-API-KEY`, not `Authorization`), key from a different environment than expected, or the client wasn't restarted after editing the config.

## When NOT to Use This Skill

Don't load this skill — go straight to a different one — when:

- You're writing **production hot paths** (gating, per-request usage reports). The MCP is non-deterministic by design; use the Node SDK instead — see `stigg-api`.
- The user **explicitly asks for the CLI**, or the task is unambiguously a deterministic shell workflow (CI, scheduled cron, runbooks). Use the **Stigg CLI** (`brew install stiggio/tools/stigg` — https://github.com/stiggio/stigg-cli) — see `references/cli-vs-mcp.md`. Otherwise default to the MCP server even for one-off ops.
- The user's question is about the **REST or GraphQL API itself**, not the MCP server — see `stigg-api`.

The MCP server fits when you're inside an AI assistant doing modeling, exploration, or one-off ops. It doesn't fit unattended automation or production hot paths.

## Security — Read This Before Connecting Production

- **Default to sandbox.** AI agents can take destructive, hard-to-reverse actions based on natural-language instructions that may be misinterpreted. Develop and test against sandbox first.
- **One scoped key per AI client.** Don't reuse the full-access key everywhere. If a key leaks, blast radius = its scoped permissions only.
- **Keys are environment-bound.** A sandbox key cannot touch production data, and vice versa.
- **Never commit keys.** Treat them like passwords.
- **Rotate periodically** from **Settings → API keys**. Stigg supports zero-downtime rotation with a configurable grace period.
- **The agent acts on your behalf.** There is no separate agent identity. The MCP server forwards API calls using your key, scoped to its permissions.

## Multi-Environment

Each `mcpServers` entry is per-environment. To switch, configure separate entries (`stigg-sandbox`, `stigg-production`) with separate keys. **This is error-prone** — the agent may not know which to target. Prefer running with a single environment per session and only adding the key for the environment you intend the agent to operate on.

## What the Agent Can Do Once Connected

A non-exhaustive map (full surface continues to grow — re-check the docs page):

- **Catalog:** create / update / archive / list plans, features, add-ons; publish and archive packages.
- **Customers & subscriptions:** provision customers, provision/preview/cancel subscriptions (including scheduled and trial), grant promotional entitlements.
- **Entitlements & usage:** check entitlements, report usage measurements, report metering events.

A current, terse tool listing is in `references/mcp-tools.md`. **Do not memorize this list — re-fetch from the live docs when in doubt.**

## Common Mistakes

| Mistake | Fix |
|---|---|
| Used `Authorization: Bearer` header | The Stigg MCP wants `X-API-KEY`. |
| `/mcp` doesn't show `stigg` | Forgot to restart the client after editing config. |
| 401 Unauthenticated on every call | Key is for a different environment, expired, or revoked. |
| Agent acted on production by mistake | Only the sandbox key should be in the config during dev. Remove the prod entry. |
| Picked the MCP for a CI script | Use the CLI for CI. The MCP is non-deterministic by design. |
| Embedded the key in a checked-in config | Use env vars or your client's secret store. Rotate the leaked key immediately. |
| Misread an `execute` `isError: true` from a TypeScript typecheck rejection as an account/permission failure | `execute` runs sandboxed TypeScript — a typecheck error means your snippet doesn't compile, not that the API or key is wrong. Fix the TS and re-run. |
