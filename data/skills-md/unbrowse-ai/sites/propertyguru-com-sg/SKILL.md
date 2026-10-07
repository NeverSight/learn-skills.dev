---
name: propertyguru-com-sg
description: "Propertyguru (propertyguru.com.sg) for agents: PropertyGuru property listings for sale; PropertyGuru agent's active listings; Read a propertyguru.com.sg slug page — through Unbrowse's scoped MCP for propertyguru.com.sg (unofficial), which replays propertyguru.com.sg's own first-party API (no browser, verified results). Use when the user wants anything from propertyguru.com.sg, e.g. propertyguru property listings for sale."
---

# Unbrowse for Propertyguru (propertyguru.com.sg)

Propertyguru as tools for your agent. Unofficial: not affiliated with or endorsed by propertyguru.com.sg. Unbrowse compiled these from propertyguru.com.sg's own requests: each call replays the site's first-party API server-side and returns a verified result. No scraping of rendered pages, no browser on your side, no propertyguru.com.sg API key.

## Connect the propertyguru.com.sg MCP

This server is a tool scope holding only propertyguru.com.sg: its compiled tools plus the Unbrowse tools that run them, so the agent's tool list stays small and every call stays on propertyguru.com.sg.

```sh
claude mcp add --transport http propertyguru-com-sg https://unbrowse.ai/mcp/propertyguru.com.sg
codex mcp add propertyguru-com-sg --url https://unbrowse.ai/mcp/propertyguru.com.sg && codex mcp login propertyguru-com-sg
```

```json
{"mcpServers":{"propertyguru-com-sg":{"url":"https://unbrowse.ai/mcp/propertyguru.com.sg"}}}
```

The first connect signs in to Unbrowse with OAuth (free tier, only verified results count). For scripts, send `Authorization: Bearer $UNBROWSE_API_KEY` (key from https://unbrowse.ai/app/keys; keep it in a secret manager, never in config you commit).

If none of the tools below are in this session's tool list, the server is not connected or not signed in: say so and stop. Do not fetch propertyguru.com.sg some other way and present it as this skill's result.

## Tools

### `propertyguru_com_sg__get_property_for_sale` — PropertyGuru property listings for sale

PropertyGuru property listings for sale. Inputs: propertyTypeCode. Returns the page's title, readable text and links. Read-only on propertyguru.com.sg.

- `propertyTypeCode` (string, required)
- `propertyTypeGroup` (string) — optional, e.g. "N"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"propertyTypeCode":"<propertyTypeCode>"}
```

### `propertyguru_com_sg__get_agent_profile_active_listings` — PropertyGuru agent's active listings

PropertyGuru agent's active listings. Inputs: agent_id; limit; page. Returns isSuccess, data, timestamp, path. Read-only on propertyguru.com.sg.

- `agent_id` (integer, required) — agent id
- `limit` (integer, required)
- `page` (integer, required)
- `marketplace` (string) — optional, e.g. "pg"
- `sort` (string) — optional, e.g. "date"
- `order` (string) — optional, e.g. "desc"
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.
- 1 more of the site's own parameters (locale, paging and the like), sent as recorded

```json
{"agent_id":"<agent_id>","limit":"<limit>","page":"<page>"}
```

### `propertyguru_com_sg__read_page` — Read a propertyguru.com.sg slug page

Read a propertyguru.com.sg slug page. Inputs: slug. Returns the page's title, readable text and links. Read-only on propertyguru.com.sg.

- `slug` (string, required)
- `select` (array) — Keep only these parts of the result: dots walk keys, [] maps over a list, a final {a,b} keeps several keys (e.g. "results[].{title,url}"). Unmatched paths come back in selectMissing.

```json
{"slug":"<slug>"}
```

Always there too: `unbrowse.run` (a task on propertyguru.com.sg in plain words), `unbrowse.inspect`, `unbrowse.resume`, `unbrowse.scrape` and `unbrowse.map` (any page on propertyguru.com.sg), and the recorded cloud browser `unbrowse.browse.open` → `unbrowse.browse.act` → `unbrowse.browse.finish`. Hosts that reject dotted names show them with `_` (`unbrowse_run`).

## How to call

1. Pick the tool whose title matches the job and pass its inputs. Leave the site's recorded parameters out unless the user asked for something they control.
2. Read `status`. `succeeded` carries the verified `result`. `input_required` is not a failure: answer the open fields with `unbrowse.resume {runId, answers}` on the same run.
3. No tool fits: `unbrowse.run {task}`. It fails with `no_capability` when nothing is compiled for that yet: do it once with `unbrowse.browse.open` on propertyguru.com.sg → `unbrowse.browse.act` → `unbrowse.browse.finish`, which compiles a new tool this server lists next time. Anything off propertyguru.com.sg is refused here (`not_in_scope`): use the general Unbrowse server for that.
4. Signing in: never ask the user for a password. `unbrowse.browse.act` with `action: "autofill"` fills propertyguru.com.sg's login from their Unbrowse password manager.
5. Report only what a `succeeded` result says. `outcome_unknown` means a change may have happened: check before retrying. Posting, buying, sending or deleting needs the user's go-ahead.

## Without MCP

Every tool is also a REST call:

```sh
curl -s https://unbrowse.ai/api/v1/sites/propertyguru.com.sg/call/propertyguru_com_sg__get_property_for_sale \
  -H "authorization: Bearer $UNBROWSE_API_KEY" -H "content-type: application/json" \
  -d '{"propertyTypeCode":"<propertyTypeCode>"}'
```

OpenAPI: https://unbrowse.ai/api/v1/sites/propertyguru.com.sg/openapi.json. Every other site: the general Unbrowse skill (https://github.com/unbrowse-ai/unbrowse) and https://unbrowse.ai/mcp.
