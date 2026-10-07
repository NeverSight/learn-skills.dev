---
name: alternativeto
description: "Alternativeto (alternativeto.net) for agents: Search software on AlternativeTo; Search alternativeto; Browse apps by category; Search apps and software — through Unbrowse's scoped MCP for alternativeto.net (unofficial), which replays alternativeto.net's own first-party API (no browser, verified results). Use when the user wants anything from alternativeto.net, e.g. search software on alternativeto."
---

# Unbrowse for Alternativeto (alternativeto.net)

Alternativeto as tools for your agent. Unofficial: not affiliated with or endorsed by alternativeto.net. Unbrowse compiled these from alternativeto.net's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no alternativeto.net API key.

## Connect the alternativeto.net MCP

This server is a tool scope holding only alternativeto.net: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on alternativeto.net.

```sh
claude mcp add --transport http alternativeto https://unbrowse.ai/mcp/alternativeto.net
codex mcp add alternativeto --url https://unbrowse.ai/mcp/alternativeto.net && codex mcp login alternativeto
```

```json
{"mcpServers":{"alternativeto":{"url":"https://unbrowse.ai/mcp/alternativeto.net"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch alternativeto.net some other way and present it as this skill's result.

## Tools

### `alternativeto_net__get_browse_search` — Search software on AlternativeTo

Search software on AlternativeTo. Inputs: query. Returns the page's title, readable text and links. Read-only on alternativeto.net.

- `query` (string, required) — query (typed during “fill Search”)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

### `alternativeto_net__post_indexes_queries_2` — Search alternativeto

Search alternativeto. Inputs: query. Returns results. Read-only on alternativeto.net.

- `query` (string, required) — query (typed during “fill Search”)
- `x_algolia_agent` (string) — optional, e.g. "Algolia for JavaScript (5.59.0); Lite (5.59.0); Browser"
- `x_algolia_application_id` (string) — optional, e.g. "ZIDPNS2VB0"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

### `alternativeto_net__get_items_available_filters` — Browse apps by category

Browse apps by category. No inputs. Returns platformsFilters, featureFilters, licenseFilters, originFilters. Read-only on alternativeto.net.

- `category` (string) — optional, e.g. "security"
- `excludeMetatags` (string) — optional, e.g. "nsfw-warning,legal-warning,block-as-alternative"
- `uriAsBase64` (string) — optional, e.g. "aHR0cHM6Ly9hbHRlcm5hdGl2ZXRvLm5ldC9icm93c2UvYWxsLz9jYXRlZ29yeT1zZWN1cml0eQ=="
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"category":"security","excludeMetatags":"nsfw-warning,legal-warning,block-as-alternative","uriAsBase64":"aHR0cHM6Ly9hbHRlcm5hdGl2ZXRvLm5ldC9icm93c2UvYWxsLz9jYXRlZ29yeT1zZWN1cml0eQ=="}
```

### `alternativeto_net__render_page` — Search apps and software

Search apps and software. Inputs: query. Returns the page's title, readable text and links. Read-only on alternativeto.net.

- `query` (string, required) — query — what to search for on alternativeto.net
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

### `alternativeto_net__read_page` — Read a alternativeto.net software page

Read a alternativeto.net software page. Inputs: software. Returns the page's title, readable text and links. Read-only on alternativeto.net.

- `software` (string, required)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"software":"<software>"}
```

Always there too: `unbrowse.run` (a task on alternativeto.net in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on alternativeto.net), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on alternativeto.net → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off alternativeto.net is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills alternativeto.net's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/alternativeto.net/call/alternativeto_net__get_browse_search \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/alternativeto.net/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
