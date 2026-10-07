---
name: airbnb
description: "Airbnb (airbnb.com) for agents: Airbnb search: stays in a location; Search stays — through Unbrowse's scoped MCP for airbnb.com (unofficial), which replays airbnb.com's own first-party API (no browser, verified results). Use when the user wants anything from airbnb.com, e.g. airbnb search: stays in a location."
---

# Unbrowse for Airbnb (airbnb.com)

Airbnb as tools for your agent. Unofficial: not affiliated with or endorsed by airbnb.com. Unbrowse compiled these from airbnb.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no airbnb.com API key.

## Connect the airbnb.com MCP

This server is a tool scope holding only airbnb.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on airbnb.com.

```sh
claude mcp add --transport http airbnb https://unbrowse.ai/mcp/airbnb.com
codex mcp add airbnb --url https://unbrowse.ai/mcp/airbnb.com && codex mcp login airbnb
```

```json
{"mcpServers":{"airbnb":{"url":"https://unbrowse.ai/mcp/airbnb.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch airbnb.com some other way and present it as this skill's result.

## Tools

### `airbnb_com__get_s_homes` — Airbnb search: stays in a location

Airbnb search: stays in a location. Inputs: location. Returns the page's title, readable text and links. Read-only on airbnb.com.

- `location` (string, required) — location (typed during “search”)
- `checkin` (string) — optional, e.g. "2026-11-10"
- `checkout` (string) — optional, e.g. "2026-11-14"
- `adults` (integer) — optional, e.g. "2"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.
- 3 more of the site's own parameters (locale, paging and the like), sent as recorded

```json
{"location":"<location>"}
```

### `airbnb_com__read_page` — Search stays

Search stays. Inputs: query. Returns the page's title, readable text and links. Read-only on airbnb.com.

- `query` (string, required)
- `adults` (integer) — optional, e.g. 2
- `tab_id` (string) — optional, e.g. "home_tab"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

Always there too: `unbrowse.run` (a task on airbnb.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on airbnb.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on airbnb.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off airbnb.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills airbnb.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/airbnb.com/call/airbnb_com__get_s_homes \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"location":"<location>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/airbnb.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
