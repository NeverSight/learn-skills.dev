---
name: wikipedia
description: "Wikipedia (wikipedia.org) for agents: Search wikipedia; Read a Wikipedia article — through Unbrowse's scoped MCP for wikipedia.org (unofficial), which replays wikipedia.org's own first-party API (no browser, verified results). Use when the user wants anything from wikipedia.org, e.g. search wikipedia."
---

# Unbrowse for Wikipedia (wikipedia.org)

Wikipedia as tools for your agent. Unofficial: not affiliated with or endorsed by wikipedia.org. Unbrowse compiled these from wikipedia.org's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no wikipedia.org API key.

## Connect the wikipedia.org MCP

This server is a tool scope holding only wikipedia.org: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on wikipedia.org.

```sh
claude mcp add --transport http wikipedia https://unbrowse.ai/mcp/wikipedia.org
codex mcp add wikipedia --url https://unbrowse.ai/mcp/wikipedia.org && codex mcp login wikipedia
```

```json
{"mcpServers":{"wikipedia":{"url":"https://unbrowse.ai/mcp/wikipedia.org"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch wikipedia.org some other way and present it as this skill's result.

## Tools

### `en_wikipedia_org__render_page` — Search wikipedia

Search wikipedia. Inputs: query. Returns the page's title, readable text and links. Read-only on en.wikipedia.org.

- `query` (string, required) — query — what to search for on en.wikipedia.org
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

### `simple_wikipedia_org__read_page` — Read a Wikipedia article

Read a Wikipedia article. Inputs: title (optional). Returns the page's title, readable text and links. Read-only on simple.wikipedia.org.

- `title` (string)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"title":"Virtual_private_network"}
```

Always there too: `unbrowse.run` (a task on wikipedia.org in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on wikipedia.org), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on wikipedia.org → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off wikipedia.org is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills wikipedia.org's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/en.wikipedia.org/call/en_wikipedia_org__render_page \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/en.wikipedia.org/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
