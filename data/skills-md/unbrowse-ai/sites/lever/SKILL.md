---
name: lever
description: "Lever (lever.co) for agents: Lever job board: open postings — through Unbrowse's scoped MCP for lever.co (unofficial), which replays lever.co's own first-party API (no browser, verified results). Use when the user wants anything from lever.co, e.g. lever job board: open postings."
---

# Unbrowse for Lever (lever.co)

Lever as tools for your agent. Unofficial: not affiliated with or endorsed by lever.co. Unbrowse compiled these from lever.co's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no lever.co API key.

## Connect the lever.co MCP

This server is a tool scope holding only lever.co: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on lever.co.

```sh
claude mcp add --transport http lever https://unbrowse.ai/mcp/lever.co
codex mcp add lever --url https://unbrowse.ai/mcp/lever.co && codex mcp login lever
```

```json
{"mcpServers":{"lever":{"url":"https://unbrowse.ai/mcp/lever.co"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch lever.co some other way and present it as this skill's result.

## Tools

### `api_lever_co__get_postings_ro` — Lever job board: open postings

Lever job board: open postings. Inputs: company. Returns data. Read-only on api.lever.co.

- `company` (string, required) — company (typed during “search”)
- `mode` (string) — optional, e.g. "json"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"company":"<company>"}
```

Always there too: `unbrowse.run` (a task on lever.co in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on lever.co), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on lever.co → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off lever.co is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills lever.co's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/api.lever.co/call/api_lever_co__get_postings_ro \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"company":"<company>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/api.lever.co/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
