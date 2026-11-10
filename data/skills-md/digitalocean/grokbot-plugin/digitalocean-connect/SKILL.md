---
name: digitalocean-connect
description: >-
  Connect the DigitalOcean MCP server, choose OAuth or a scoped token, and fix
  401, 403, and 429 errors. Use for "connect DigitalOcean", "DO auth error",
  "token", or "permission denied".
---
# Connect DigitalOcean MCP

This plugin ships a **single hosted MCP server** — **DigitalOcean MCP** at
`https://mcp.digitalocean.com/mcp`. It fronts every first-party DigitalOcean
service, so you connect **once** and reach all of them.

DigitalOcean MCP exposes three meta-tools (a discovery-to-run flow):

- `find_tools` — natural-language search that returns candidate tools by their
  qualified `service/tool` name.
- `retrieve_schema` — full input/output schema for one qualified tool name.
- `invoke_tool` — runs a tool by its qualified name with matching `arguments`.

Approval tiers still apply: the plugin hook unwraps the `invoke_tool` target
(for example `droplets/droplet-delete`) and enforces the tier maps.

## Default auth (v1)

- **OAuth** on first use — a single browser sign-in for DigitalOcean MCP. No
  per-service grants and no long-lived credentials stored in config.
- **Never ask for or accept a Personal Access Token (PAT) or API token in chat.**
  If the user pastes a token, tell them to **revoke it immediately** in the
  DigitalOcean control panel and authenticate through **Customize → MCP** OAuth
  instead.
- Configure an optional PAT only in the MCP server settings UI or local MCP
  config (`mcp.json` / Cursor MCP settings) as an `Authorization: Bearer` header,
  never in prompts, skills output, or committed files.
- **Database connection strings** (URI, password, CA material): never echo them,
  never write them to workspace files unless the user explicitly asks for a
  local copy in a named file.

## Connect workflow

DigitalOcean MCP is a single server, so there is nothing to connect per service.

1. In Cursor: **Customize → MCP** — enable the **digitalocean** server and
   complete OAuth when prompted.
1. Confirm the connection with a read-only discovery call (`find_tools`) or a
   Tier 1 read (for example `invoke_tool` → `droplets/droplet-list`) before any
   write.
1. The same OAuth grant covers accounts, droplets, apps, databases, networking,
   insights, docs, and the other services it fronts.

The public documentation MCP (`docs`) tools require no sign-in; they are reached
through the same DigitalOcean MCP connection.

## Errors

| Symptom | Likely cause                  | What to do                                                       |
| ------- | ----------------------------- | ---------------------------------------------------------------- |
| 401     | Missing or expired OAuth      | Re-authenticate the **digitalocean** server in Customize → MCP   |
| 403     | Insufficient scopes           | Reconnect with broader OAuth scopes — **not** chat-pasted tokens |
| 429     | Rate limit (5000/hr, 250/min) | Back off; honor `Retry-After`; reduce polling                    |

**App Platform + private GitHub** is separate from MCP OAuth. Signing in to
DigitalOcean MCP does not install the DigitalOcean GitHub app or grant repo
access. If `apps-create-app-from-spec` / `apps-update` return `GitHub user not authenticated`, use **digitalocean-app-platform** (user steps at
[Create an app](https://cloud.digitalocean.com/apps/new)), then retry the deploy call.

Public OAuth clients use **1-hour** access tokens and **single-use** refresh tokens.
Persist the latest refresh token only in MCP server configuration if the user runs
a custom client (not the default hosted flow).

## Scoped token (break-glass only)

Do **not** solicit PATs. If the user already configured a PAT in MCP settings
outside chat:

- Recommend **Read Only** (`api:read`) for inventory and troubleshooting.
- Require explicit opt-in before **write** scopes.
- Never echo the token in chat or logs.

See `skills/digitalocean-connect/references/scope-bundles.md` for suggested scope sets per skill.
