---
name: myworkdayjobs
description: "Myworkdayjobs (myworkdayjobs.com) for agents: Search jobs by keyword, location and category on the DBS Careers job search page; Read dbs.wd3.myworkdayjobs.com/en-US/DBS_Careers — through Unbrowse's scoped MCP for myworkdayjobs.com (unofficial), which replays myworkdayjobs.com's own first-party API (no browser, verified results). Use when the user wants anything from myworkdayjobs.com, e.g. search jobs by keyword, location and category on the dbs careers job search page."
---

# Unbrowse for Myworkdayjobs (myworkdayjobs.com)

Myworkdayjobs as tools for your agent. Unofficial: not affiliated with or endorsed by myworkdayjobs.com. Unbrowse compiled these from myworkdayjobs.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no myworkdayjobs.com API key.

## Connect the myworkdayjobs.com MCP

This server is a tool scope holding only myworkdayjobs.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on myworkdayjobs.com.

```sh
claude mcp add --transport http myworkdayjobs https://unbrowse.ai/mcp/myworkdayjobs.com
codex mcp add myworkdayjobs --url https://unbrowse.ai/mcp/myworkdayjobs.com && codex mcp login myworkdayjobs
```

```json
{"mcpServers":{"myworkdayjobs":{"url":"https://unbrowse.ai/mcp/myworkdayjobs.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch myworkdayjobs.com some other way and present it as this skill's result.

## Tools

### `dbs_wd3_myworkdayjobs_com__render_page` — Search jobs by keyword, location and category on the DBS Careers job search page

Search jobs by keyword, location and category on the DBS Careers job search page. Inputs: keyword. Returns the page's title, readable text and links. Read-only on dbs.wd3.myworkdayjobs.com.

- `keyword` (string, required) — keyword — what to search for on dbs.wd3.myworkdayjobs.com
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"keyword":"<keyword>"}
```

### `dbs_wd3_myworkdayjobs_com__read_page` — Read dbs.wd3.myworkdayjobs.com/en-US/DBS_Careers

Read dbs.wd3.myworkdayjobs.com/en-US/DBS_Careers. No inputs. Returns the page's title, readable text and links. Read-only on dbs.wd3.myworkdayjobs.com.

- `jobFamily` (string) — optional, e.g. "7c4ba0705e5d017ad85cd065f22cd410"
- `locationCountry` (string) — optional, e.g. "80938777cac5440fab50d729f9634969"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"jobFamily":"7c4ba0705e5d017ad85cd065f22cd410","locationCountry":"80938777cac5440fab50d729f9634969"}
```

Always there too: `unbrowse.run` (a task on myworkdayjobs.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on myworkdayjobs.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on myworkdayjobs.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off myworkdayjobs.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills myworkdayjobs.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/dbs.wd3.myworkdayjobs.com/call/dbs_wd3_myworkdayjobs_com__render_page \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"keyword":"<keyword>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/dbs.wd3.myworkdayjobs.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
