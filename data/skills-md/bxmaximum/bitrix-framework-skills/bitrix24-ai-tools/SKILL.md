---
name: bitrix24-ai-tools
description: 'AI tooling for Bitrix24 development: official docs MCP b24-dev-mcp (bitrix-search, bitrix-method-details) and Alaio Vibecode (keys, /v1/me, vibecodeconnector on-premise). Use when an agent writes REST calls, sets up MCP or builds a Vibecode app.'
---

# Bitrix24 AI tools

Baseline: Bitrix24 cloud; on-premise via `vibecodeconnector` · Verified: b24restdocs 2026-09-30, vibecodeconnector 26.200.100 (main 26.800.0)

| Goal | Use |
| --- | --- |
| Write or change REST calls in your own code | MCP `b24-dev-mcp` + `bitrix24-rest-api` |
| Have an agent build and host an app on the platform | Alaio Vibecode |
| Agent-ready starters | b24gosdk `llms.txt`; `github.com/bitrix24/b24-ai-starter` (Nuxt 3 + PHP/Python/Node, OAuth, Docker) |

No `llms.txt` is documented for the REST docs themselves. Vibecode (platform) ≠ Vibe (start page, `landing.repowidget.*`) ≠ Vibe+ (cloud plan line).

## Docs MCP `b24-dev-mcp`

`https://mcp-dev.bitrix24.com/mcp`: Streamable HTTP (no `/sse`), no auth. It serves docs only: no portal data, no method calls. The client must accept `application/json` and `text/event-stream` (otherwise 406).

| Tool | Call when |
| --- | --- |
| `bitrix-search` | first; returns exact names. `doc_type`: `method`, `event`, `other`, `app_development_docs`; `limit` |
| `bitrix-method-details` | before writing a call: params, required fields, response, errors, samples (`field`, `filter` narrow it) |
| `bitrix-event-details` | writing an event handler: payload |
| `bitrix-article-details` | concepts: auth, limits, batch, pagination |
| `bitrix-app-development-doc-details` | app install, placements, app types |

Setup:

```bash
claude mcp add --transport http b24-dev-mcp https://mcp-dev.bitrix24.com/mcp
codex mcp add b24-dev-mcp --url https://mcp-dev.bitrix24.com/mcp
```

Cursor `.cursor/mcp.json`: `{"mcpServers": {"b24-dev-mcp": {"url": "https://mcp-dev.bitrix24.com/mcp", "timeout": 30000}}}`. VS Code `.vscode/mcp.json`: `{"servers": {"b24-dev-mcp": {"url": "https://mcp-dev.bitrix24.com/mcp", "type": "http"}}}`. Smoke test: ask for `crm.item.add` params; the answer must name `entityTypeId` and `fields`.

Rules:

1. Before adding or changing a REST call: `bitrix-search`, then `bitrix-method-details` on the exact name. Take param names and case, required fields, filter syntax and scope from the result, not from memory.
2. `not found` means an inexact name: search again, never guess.
3. The docs describe the cloud. Whether a method exists on a given box: `method.get` on that portal.
4. Never send webhook URLs, tokens, keys or customer data to the MCP.

## Alaio Vibecode

A platform where an agent builds Bitrix24 apps through Vibecode's own API. Entry point: give the agent a key and `GET https://vibecode.bitrix24.com/v1/me`, which returns objects, key permissions and instructions.

Keys (shown once):

- `vibe_api_…`: personal, acts as one user like a webhook; cannot embed in the UI.
- `vibe_app_…`: app with OAuth, users act with their own rights; required for placements and event delivery.
- `vibe_live_…`: management only (keys, portals), no data access.
- Mode `READWRITE` (default) or `READONLY` (writes return 403 `WRITE_BLOCKED_READONLY_KEY`).

Compared with REST, the API converts field names and filters, pages internally up to 5 000 items (REST: 50), batches and retries transient errors. Extras: Black Hole servers (hosting behind a tunnel, sleep after 60 min idle), event subscriptions with redelivery, OpenAI-compatible models (`/v1/models`, `/v1/embeddings`), search (`/v1/search`), storage, source versions.

Limits: 300 req/min per key; `/v1/search` 60/min; AI router 600/min per key and 1 500/min per user. 429 carries the retry time; the effective limit is in `X-RateLimit-Limit`.

Cost: paid Bitrix24 plan plus Vibe+ subscription. Servers, metered models, search and agents are billed in Vibe credits (1 Ꝟ = 1 USD); an exhausted budget returns 402.

Security: keep the key in the project's env only. A leaked key: create a new one, disable the old. Team members use their own keys, never a shared one.

Pick Vibecode for fast internal tools, bots and AI features without your own hosting. Pick a plain REST app (`bitrix24-rest-api`) for own infrastructure, Marketplace distribution, custom token storage or a box without a Vibecode connection.

## On-premise: module `vibecodeconnector`

- Version 26.200.100, beta: the installer requires accepting beta terms. Needs `rest` with REST enabled; uses `im` and `socialservices`. Connect one installation per license key.
- Module settings → Connect registers the box with Vibecode (`vibecode.bitrix24.com`; `vibecode.bitrix24.tech` for CIS or unknown license regions) and stores the pairing key.
- Vibecode then POSTs to the module's actions with `Authorization: Bearer <JWT>` (`CheckIncomingJwt`). The box must be reachable from Vibecode. An API key is issued as an inbound webhook of the user, an app key as a personal app installed on the box.
- Option `permission_source`: `vibecode` bypasses the portal's webhook and app creation restrictions, `portal` applies them. RU/BY licenses also need a Marketplace subscription (`SUBSCRIPTION_REQUIRED`).
- Uninstall only after Disconnect. After connecting, users add the box in Vibecode ("Connect self-hosted Bitrix24") and work as in the cloud.

## Checklist

- [ ] Every new or changed REST call was checked with `bitrix-method-details` (or the method page), not written from memory.
- [ ] No webhook URL, token or Vibecode key in the repo, prompts, screenshots or MCP requests.
- [ ] Vibecode key has minimal permissions; `READONLY` where the app does not write.
- [ ] Generated app reviewed: permissions, data it changes, error handling, who can open it.
