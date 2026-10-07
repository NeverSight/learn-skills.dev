---
name: udemy
description: "Udemy (udemy.com) for agents: Read a udemy.com page by name — through Unbrowse's scoped MCP for udemy.com (unofficial), which replays udemy.com's own first-party API (no browser, verified results). Use when the user wants anything from udemy.com, e.g. read a udemy.com page by name."
---

# Unbrowse for Udemy (udemy.com)

Udemy as tools for your agent. Unofficial: not affiliated with or endorsed by udemy.com. Unbrowse compiled these from udemy.com's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no udemy.com API key.

## Connect the udemy.com MCP

This server is a tool scope holding only udemy.com: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on udemy.com.

```sh
claude mcp add --transport http udemy https://unbrowse.ai/mcp/udemy.com
codex mcp add udemy --url https://unbrowse.ai/mcp/udemy.com && codex mcp login udemy
```

```json
{"mcpServers":{"udemy":{"url":"https://unbrowse.ai/mcp/udemy.com"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch udemy.com some other way and present it as this skill's result.

## Tools

### `udemy_com__read_course_by_name` — Read a udemy.com page by name

Read a udemy.com page by name. Inputs: name. Returns the page's title, readable text and links. Read-only on udemy.com.

- `name` (string, required)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"name":"<name>"}
```

Always there too: `unbrowse.run` (a task on udemy.com in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on udemy.com), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on udemy.com → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off udemy.com is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills udemy.com's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/udemy.com/call/udemy_com__read_course_by_name \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"name":"<name>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/udemy.com/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
