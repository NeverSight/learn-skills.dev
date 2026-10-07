---
name: alibaba
description: "Alibaba (alibaba.com) for agents: Search products by keyword; Search alibaba.com — through Unbrowse's scoped MCP for alibaba.com (unofficial), which replays alibaba.com's own first-party API (no browser, verified results). Use when the user wants anything from alibaba.com, e.g. search products by keyword."
---

# Unbrowse for Alibaba (alibaba.com)

Alibaba as tools for your agent. Unofficial: not affiliated with or endorsed by alibaba.com. Unbrowse compiled these from alibaba.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no alibaba.com API key.

## Connect the alibaba.com MCP

This server is a tool scope holding only alibaba.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on alibaba.com.

```sh
claude mcp add --transport http alibaba https://unbrowse.ai/mcp/alibaba.com
codex mcp add alibaba --url https://unbrowse.ai/mcp/alibaba.com && codex mcp login alibaba
```

```json
{"mcpServers":{"alibaba":{"url":"https://unbrowse.ai/mcp/alibaba.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch alibaba.com some other way and present it as this skill's result.

## Tools

### `alibaba_com__get_trade_search` — Search products by keyword

Search products by keyword. Inputs: search_keyword. Returns the page's title, readable text and links. Read-only on alibaba.com.

- `search_keyword` (string, required) — search keyword (typed during “fill Search Alibaba”)
- `tab` (string) — optional, e.g. "all"
- `has4Tab` (string) — optional, e.g. "true"
- `spm` (string) — optional, e.g. "a2700.galleryofferlist.the-new-header_fy23_pc_search_bar.searchButton"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"search_keyword":"<search_keyword>"}
```

### `alibaba_com__render_page` — Search alibaba.com

Search alibaba.com. Inputs: search_keyword. Returns the page's title, readable text and links. Read-only on alibaba.com.

- `search_keyword` (string, required) — search_keyword — what to search for on alibaba.com
- `spm` (string) — optional, e.g. "a2700.galleryofferlist.the-new-header_fy23_pc_search_bar.searchButton"
- `tab` (string) — optional, e.g. "all"
- `has4Tab` (string) — optional, e.g. "true"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"search_keyword":"<search_keyword>"}
```

Always there too: `unbrowse.run` (a task on alibaba.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on alibaba.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on alibaba.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off alibaba.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills alibaba.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/alibaba.com/call/alibaba_com__get_trade_search \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"search_keyword":"<search_keyword>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/alibaba.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
