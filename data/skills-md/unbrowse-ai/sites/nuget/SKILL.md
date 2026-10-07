---
name: nuget
description: "Nuget (nuget.org) for agents: Search nuget; Search nuget.org — through Unbrowse's scoped MCP for nuget.org (unofficial), which replays nuget.org's own first-party API (no browser, verified results). Use when the user wants anything from nuget.org, e.g. search nuget."
---

# Unbrowse for Nuget (nuget.org)

Nuget as tools for your agent. Unofficial: not affiliated with or endorsed by nuget.org. Unbrowse compiled these from nuget.org's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no nuget.org API key.

## Connect the nuget.org MCP

This server is a tool scope holding only nuget.org: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on nuget.org.

```sh
claude mcp add --transport http nuget https://unbrowse.ai/mcp/nuget.org
codex mcp add nuget --url https://unbrowse.ai/mcp/nuget.org && codex mcp login nuget
```

```json
{"mcpServers":{"nuget":{"url":"https://unbrowse.ai/mcp/nuget.org"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch nuget.org some other way and present it as this skill's result.

## Tools

### `nuget_org__get_packages` — Search nuget

Search nuget. Inputs: query. Returns the page's title, readable text and links. Read-only on nuget.org.

- `query` (string, required) — query (typed during “fill Enter packages to search”)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

### `nuget_org__get_search` — Search nuget.org

Search nuget.org with its own search (published OpenSearch description) and read the results page as title, text and links. One first-party HTTP request, no browser. Inputs: query. Returns the page's title, readable text and links. Read-only on nuget.org.

- `query` (string, required) — query — what to search for on nuget.org
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"choices"}
```

Always there too: `unbrowse.run` (a task on nuget.org in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on nuget.org), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on nuget.org → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off nuget.org is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills nuget.org's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/nuget.org/call/nuget_org__get_packages \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/nuget.org/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
