---
name: redfin
description: "Redfin (redfin.com) for agents: Redfin search: homes for sale in a region — through Unbrowse's scoped MCP for redfin.com (unofficial), which replays redfin.com's own first-party API (no browser, verified results). Use when the user wants anything from redfin.com, e.g. redfin search: homes for sale in a region."
---

# Unbrowse for Redfin (redfin.com)

Redfin as tools for your agent. Unofficial: not affiliated with or endorsed by redfin.com. Unbrowse compiled these from redfin.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no redfin.com API key.

## Connect the redfin.com MCP

This server is a tool scope holding only redfin.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on redfin.com.

```sh
claude mcp add --transport http redfin https://unbrowse.ai/mcp/redfin.com
codex mcp add redfin --url https://unbrowse.ai/mcp/redfin.com && codex mcp login redfin
```

```json
{"mcpServers":{"redfin":{"url":"https://unbrowse.ai/mcp/redfin.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch redfin.com some other way and present it as this skill's result.

## Tools

### `redfin_com__get_stingray_gis` — Redfin search: homes for sale in a region

Redfin search: homes for sale in a region. Inputs: market; region_id; region_type. Returns text. Read-only on redfin.com.

- `market` (string, required) — market (typed during “search”)
- `region_id` (integer, required) — region id (typed during “search”)
- `region_type` (integer, required) — region type (typed during “search”)
- `al` (integer) — optional, e.g. "1"
- `include_nearby_homes` (string) — optional, e.g. "false"
- `num_homes` (integer) — optional, e.g. "50"
- `ord` (string) — optional, e.g. "redfin-recommended-asc"
- `page_number` (integer) — optional, e.g. "1"
- `sf` (string) — optional, e.g. "1,2,3,5,6,7"
- `start` (integer) — optional, e.g. "0"
- `status` (integer) — optional, e.g. "9"
- `uipt` (string) — optional, e.g. "1,2,3,4,5,6,7,8"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"market":"<market>","region_id":"<region_id>","region_type":"<region_type>"}
```

Always there too: `unbrowse.run` (a task on redfin.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on redfin.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on redfin.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off redfin.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills redfin.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/redfin.com/call/redfin_com__get_stingray_gis \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"market":"<market>","region_id":"<region_id>","region_type":"<region_type>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/redfin.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
