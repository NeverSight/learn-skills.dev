---
name: onemap-gov-sg
description: "Onemap (onemap.gov.sg) for agents: Read ss search on www.onemap.gov.sg — through Unbrowse's scoped MCP for onemap.gov.sg (unofficial), which replays onemap.gov.sg's own first-party API (no browser, verified results). Use when the user wants anything from onemap.gov.sg, e.g. read ss search on www.onemap.gov.sg."
---

# Unbrowse for Onemap (onemap.gov.sg)

Onemap as tools for your agent. Unofficial: not affiliated with or endorsed by onemap.gov.sg. Unbrowse compiled these from onemap.gov.sg's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no onemap.gov.sg API key.

## Connect the onemap.gov.sg MCP

This server is a tool scope holding only onemap.gov.sg: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on onemap.gov.sg.

```sh
claude mcp add --transport http onemap-gov-sg https://unbrowse.ai/mcp/onemap.gov.sg
codex mcp add onemap-gov-sg --url https://unbrowse.ai/mcp/onemap.gov.sg && codex mcp login onemap-gov-sg
```

```json
{"mcpServers":{"onemap-gov-sg":{"url":"https://unbrowse.ai/mcp/onemap.gov.sg"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch onemap.gov.sg some other way and present it as this skill's result.

## Tools

### `onemap_gov_sg__get_ss_search` — Read ss search on www.onemap.gov.sg

Read ss search on www.onemap.gov.sg. Inputs: search. Returns found, totalNumPages, pageNum, results. Read-only on onemap.gov.sg.

- `search` (string, required) — search (typed during “fill Search...”)
- `returnGeom` (string) — optional, e.g. "Y"
- `getAddrDetails` (string) — optional, e.g. "Y"
- `pageNum` (integer) — optional, e.g. "1"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"search":"<search>"}
```

Always there too: `unbrowse.run` (a task on onemap.gov.sg in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on onemap.gov.sg), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on onemap.gov.sg → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off onemap.gov.sg is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills onemap.gov.sg's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/onemap.gov.sg/call/onemap_gov_sg__get_ss_search \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"search":"<search>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/onemap.gov.sg/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
