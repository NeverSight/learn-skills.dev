---
name: wikimedia
description: "Wikimedia (wikimedia.org) for agents: Search commons — through Unbrowse's scoped MCP for wikimedia.org (unofficial), which replays wikimedia.org's own first-party API (no browser, verified results). Use when the user wants anything from wikimedia.org, e.g. search commons."
---

# Unbrowse for Wikimedia (wikimedia.org)

Wikimedia as tools for your agent. Unofficial: not affiliated with or endorsed by wikimedia.org. Unbrowse compiled these from wikimedia.org's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no wikimedia.org API key.

## Connect the wikimedia.org MCP

This server is a tool scope holding only wikimedia.org: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on wikimedia.org.

```sh
claude mcp add --transport http wikimedia https://unbrowse.ai/mcp/wikimedia.org
codex mcp add wikimedia --url https://unbrowse.ai/mcp/wikimedia.org && codex mcp login wikimedia
```

```json
{"mcpServers":{"wikimedia":{"url":"https://unbrowse.ai/mcp/wikimedia.org"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch wikimedia.org some other way and present it as this skill's result.

## Tools

### `commons_wikimedia_org__render_page` — Search commons

Search commons. Inputs: query. Returns the page's title, readable text and links. Read-only on commons.wikimedia.org.

- `query` (string, required) — query — what to search for on commons.wikimedia.org
- `title` (string) — optional, e.g. "Special:MediaSearch"
- `type` (string) — optional, e.g. "image"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"query":"<query>"}
```

Always there too: `unbrowse.run` (a task on wikimedia.org in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on wikimedia.org), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on wikimedia.org → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off wikimedia.org is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills wikimedia.org's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/commons.wikimedia.org/call/commons_wikimedia_org__render_page \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"query":"<query>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/commons.wikimedia.org/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
