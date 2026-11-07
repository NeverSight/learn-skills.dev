---
name: add-context-gateway
description: Put the MCP servers an existing agent uses behind one Redis Iris Context Gateway with redis-iris, so the agent connects to one MCP endpoint with one agent key instead of configuring each server and its secret. Asks whether the Gateway is in Redis Cloud or self-managed, then five questions (which MCP servers and secrets the agent has today, how many tools it sees, which read-only tools may be cached, which tools return large results, whether the framework speaks MCP itself). Self-managed, it provisions the Gateway and its Upstreams from the terminal with `iris context-gateway` and sets cache and compression policies. In Redis Cloud the developer creates them in the console. Then it points the agent at the Gateway in any framework and verifies it with `tools list` and `tools call`. Use when the agent configures several MCP servers one by one, carries one secret per server, loads too many tool schemas into the prompt, or the user asks for Context Gateway, one MCP endpoint, tool caching, or result handles.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Add Context Gateway

One MCP endpoint and one agent key in place of every MCP server the agent configures today. The Gateway holds each Upstream's secret, namespaces tool names so they never collide, can expose a large catalog as `search_tools` and `run_tool` instead of every schema, caches read-only tools you opt in, and can hand a large result back as a handle. The agent keeps its tools; only where it reaches them changes. Ask first, provision, then repoint.

## 1. Discover

Read the project:

- Find every MCP server the agent configures: `.mcp.json`, `.cursor/mcp.json`, `McpToolset`, `MCPServerStreamableHttp`, `MultiServerMCPClient`, `stdio_client`, or a hand-written MCP client. Note each endpoint and where its secret comes from.
- Find where tools are handed to the model and where the turn runs.
- Identify the framework from imports, and whether it has its own MCP client.
- Note stdio-only servers: an Upstream is an HTTP MCP endpoint (`streamable-http`). A stdio server has to be served over HTTP first, or stays outside the Gateway.

First ask where the Gateway runs:

- **Redis Cloud (console).** The developer creates the Gateway and its Upstreams in the console, and the CLI only talks to the Gateway's MCP endpoint (step 3, "In Redis Cloud"). Cloud keeps the Gateway's cache and compression off, so skip questions 3 and 4.
- **Self-managed** (on-prem, or the local Compose stack). The CLI provisions everything (step 3).

Then ask the developer these five questions, nothing more. A shrug takes the default.

| Ask | If the answer is | Configure |
|---|---|---|
| Which MCP servers does the agent use, and where do their secrets live? | A list of HTTP endpoints | One Upstream each: `upstream add --name NAME --endpoint URL` with `--bearer-secret env:VAR` or `--header NAME --header-secret env:VAR` |
| | A Redis database the agent should query | A Context Surface Upstream: `--kind context-surface --surface-database-id ID --data-model FILE` (self-managed, the ID can be left out and defaults from the deployment config. In Redis Cloud the console's Create Context Surface asks for the database). Write the data model first: see "Write the data model" |
| How many tools does the agent see in total? | Tens (default) | `--tool-exposure-mode full`: every tool, namespaced |
| | Hundreds, or schemas crowd the prompt | `--tool-exposure-mode search`: the model sees `search_tools` and `run_tool` |
| Which read-only tools return the same answer for the same arguments? | Lookups, searches, reference data | A Gateway with a database and `cache` enabled (see "Gateway switches and database"), then `policy set UPSTREAM TOOL --cache-ttl DURATION` per tool |
| | None, or not sure | No cache policies |
| Which tools return results too large to read whole? | Exports, list endpoints, logs | A Gateway with a `noeviction` database and `compression` enabled (see "Gateway switches and database"). Then the deployment's handle defaults, or `--compression-ttl DURATION` per tool, and `--compression-capture never` for a tool that must always return whole |
| Does the framework connect to MCP servers itself? | Yes: Claude Code, Cursor, ADK, OpenAI Agents SDK, LangChain MCP adapters | Point its MCP client at the Gateway URL and key |
| | No, or the agent wants plain function tools | The SDK: `gateway.model_tools()` or `gateway.hooks()` |

## 2. Get current facts from MCP

Do this before writing code. Never guess framework APIs from memory.

- Framework docs: query an available docs MCP (Context7, or the framework's own) for the installed version's MCP client: how it takes a streamable HTTP URL and an `Authorization` header.
- Redis docs: if the Redis docs MCP is connected, use it for Context Gateway concepts (Upstreams, exposure modes, cache, handles).
- No MCP available: read the installed package source in the virtualenv. Say so in the report.

## 3. Provision

### Install the CLI

```
pip install redis-iris
```

It needs Python 3.11 or later. On LangGraph, install `redis-iris[langgraph]`. If `tools call crm__lookup_customer` fails with `tool_not_found` on a search-mode Gateway while a Gateway ID is set (`--gateway-id` or `IRIS_CONTEXT_GATEWAY_ID`), the installed release splits tool names at the first `.`: upgrade redis-iris, or run `tools call` with `IRIS_CONTEXT_GATEWAY_URL` set and no Gateway ID, so the CLI resolves the name through `search_tools`.

### In Redis Cloud

Redis Cloud has no API for Gateway setup yet. The control plane takes only the console session, so a `cloud` profile refuses `service`, `upstream` and `policy` commands with `cloud_unsupported`, and the agent can't provision. The developer does it in the console:

1. **Iris → Context Gateway**: create the Gateway, or open an existing one.
2. On the Gateway, **Upstreams**: **Add MCP server** for each HTTP server from question 1, or **Create Context Surface** for a Redis database (write the data model first: see "Write the data model").
3. On the connect step, copy the MCP endpoint and create an agent key.
4. Put them in `IRIS_CONTEXT_GATEWAY_URL` and `IRIS_CONTEXT_GATEWAY_API_KEY` in the agent's environment or its `.env`. The developer sets them, never the agent: don't ask for the key in chat, and never echo, `cat` or `grep` the env file.

Add both names to `.env.example` with empty values, and never commit `.env`. Then skip the rest of this step and go to step 4. Cloud keeps cache and compression off, so there are no policies or handles to set up.

### Self-managed

Let the person export `IRIS_CONTEXT_GATEWAY_SERVICE_URL`, `IRIS_CONTEXT_GATEWAY_SERVICE_TOKEN`, `IRIS_IDENTITY_URL` and `IRIS_IDENTITY_TOKEN`. For the local Compose stack, `--local` after the command (`service list --local`) supplies the service URL and token, but not the Identity URL, so `IRIS_IDENTITY_URL` is still needed for `create`.

**Identity tokens.** Each product chart can run its own Identity Service. Then set the product's own `IRIS_CONTEXT_GATEWAY_IDENTITY_TOKEN` (and `IRIS_CONTEXT_GATEWAY_IDENTITY_URL`, or the profile's `identity_url`), and leave `IRIS_IDENTITY_URL` unset: it overrides every product's `identity_url` in the profile. On a suite with one shared Identity Service, `IRIS_IDENTITY_TOKEN` and `IRIS_IDENTITY_URL` cover every product. The CLI takes the token from `--identity-token`, then `IRIS_CONTEXT_GATEWAY_IDENTITY_TOKEN`, then `IRIS_IDENTITY_TOKEN`, then the product's service token, which only works when the two are the same secret.

```
iris --json --no-input context-gateway service list
iris --json --no-input context-gateway service create --name support --tool-exposure-mode full --write-env .env
set -a; . ./.env; set +a; iris --json --no-input context-gateway service check <gatewayId from the result>
```

The Gateway CLI reads `IRIS_CONTEXT_GATEWAY_API_KEY` from the environment only, never from `.env`, so `service check`, `tools` and `handle` fail with `configuration_error` until the key is in the command's environment. Load the file inside the same shell command, as above (or `uv run --env-file .env iris ...`), so the key never reaches your output.

### Gateway switches and database

Each Gateway has two switches, `cache` and `compression`, each `ENABLED` or `DISABLED`. `service show gw_0123456789abcdef0123456789abcdef` prints both. A `--cache-ttl` policy is refused with a 400 while the Gateway's `cache` is `DISABLED`, so enable `cache` first. A compression policy is stored but does nothing while `compression` is off. Both features also need the operator's deployment switches (`cache.enabled` and `compression.enabled` in the data plane config, off by default).

| Create | `cache` and `compression` |
|---|---|
| With a database: `--database-id ID`, or the on-prem default `defaultDatabases.gatewayDb` | Both `ENABLED` |
| Without one | Both `DISABLED`. Sending `ENABLED` with no database is a 400 on that field |
| With a database that can't take compression (below, or unreachable), and `compression` omitted | `cache` `ENABLED`, `compression` stored `DISABLED` |

| Feature | Works only when |
|---|---|
| Caching | Gateway `cache` is `ENABLED`, the tool is cacheable (not marked `readOnlyHint: false` or `destructiveHint: true`; a tool with no hints counts, so opt in only tools you know are read-only), and it has a `--cache-ttl` policy |
| Compression | Gateway `compression` is `ENABLED`, and the tool's policy is not `--compression-capture never` |

`service create` and `service update` accept `--cache enabled|disabled` and `--compression enabled|disabled` in either case and send uppercase API values. Omitted flags leave the server defaults or existing values unchanged. Adding a database later does not enable either feature, so enable them explicitly:

```
iris --json --no-input context-gateway service update gw_0123456789abcdef0123456789abcdef --database-id gateway-db --cache enabled --compression enabled
```

To detach the database, pass `--clear-database --cache disabled --compression disabled` in one update. A stale `--expected-revision` returns 412 `revision_conflict`. Read the resource again before deciding whether to retry.

Database requirements:

- **Compression** needs a Gateway database with `maxmemory-policy noeviction` and the JSON module. Enabling it (create, update, or a `databaseId` change while it stays enabled) on another policy is a 400 with an `errors[]` entry pointing to `/compression`, with a reason such as `database lru-db uses allkeys-lru, compression needs noeviction`. When you send `compression enabled`, an unreachable database is a 503: retry. A create that omits `compression` on an unsuitable or unreachable database is not refused: it stores `compression` `DISABLED`, so read it back with `service show`.
- **Cache only** works on any Gateway database. Handles and cache entries share it, so give it room under `maxmemory`. On a cache-only database with an evicting policy, Redis evicts entries and the share limits below don't apply.
- **Each side has its own share of `maxmemory`.** Handles stop at `compression.max_memory_share` (default 0.5) and the cache at `cache.max_memory_share` (default 0.4), at most 0.95 together, so neither takes the other's room. Both also stop above 90% of `maxmemory`, but that's only a backstop for what the shares miss.
- **When the handle share is full**, an automatic capture returns the result whole, and an explicit `run_tool_as_handle` answers a tool error: `handle storage is full, release handles or narrow the query`. A full cache share just skips the write and returns the result. Releasing handles frees their share at once, and expired ones free it within about 10 s.
- **Size the Gateway database for its TTLs.** Handles and cache entries stay until their TTL ends (15 minutes for handles by default), so each share needs room for `creates per second x TTL x stored size`. Don't estimate the stored size from the result size. Measure it: `service diagnose --metrics-url` shows the cache and compression counters, and a rising `skipped_low_memory` or `out_of_memory` outcome means that side is full. Lower `--compression-ttl` or `--cache-ttl`, or raise `maxmemory` or the operator's share, if it doesn't fit.
- **On-prem**, the databases come from the deployment config, never from the CLI: `shared.config.databases` registers each ID, `databaseConnections` supplies the URLs, and `defaultDatabases.gatewayDb` and `defaultDatabases.surfaceDb` pick the defaults. Ask the operator when an ID is missing. With compression on, keep the Gateway database and the Surface database on separate Redis instances: `noeviction` would otherwise apply to customer data.

`service diagnose gw_0123456789abcdef0123456789abcdef` reports the Gateway's database (`no Gateway database` means every call bypasses the cache), each Upstream's catalog and the cache policies. Add `--metrics-url` for the cache and compression counters, where a rising `eviction_policy`, `skipped_low_memory` or `out_of_memory` outcome means handles are not being held.

### Run the CLI as an agent

1. Always put `--json --no-input` before the product name. You get one JSON value on stdout, errors as one JSON value on stderr, and no prompts.
2. Read before you write. `service create` has no `--dry-run`, so run `service list` first: it proves the service URL and token, and a `configuration_error`, `unauthenticated` or `forbidden` there means hand off (step 4) before anything is created.
3. Always deliver keys with `--write-env PATH` (or `--write PATH` on `service key`). Never run `create` or `key` with `--json` and no file: that prints the key into your transcript.
4. On `configuration_error`, `unauthenticated` or `forbidden`, stop. Tell the person which variable to set (the message, or `details.env`) and link `details.obtain` when present. Never ask for a secret in chat, pass one on the command line, or echo, `cat` or `grep` an env file.
5. Upstream secrets go in by reference only: `env:NAME`, `file:PATH` or `-`. Ask the person to export the variable; never write the secret yourself.
6. On `resource_exists`, ask whether to `--reuse` `details.gatewayId` or pick another name. Never delete to retry. If `create` fails with `details.created: true`, re-run with `--reuse --write-env`.

Every error is one JSON value on stderr with `error.code`; credential errors also carry `details.env` and `details.obtain`, never the value. Stop on the first failure and relay it:

| `error.code` | Who acts | Action |
|---|---|---|
| `credential_required` | person | Set the variable in `details.env` in the agent's shell. See "Identity tokens" above. |
| `unauthenticated` | person | The token from `details.source` was refused: it expired or belongs to another deployment. Issue a new one. |
| `forbidden` | person | The token is valid but lacks the role or tenant. Use a token with the right role for that product. |
| `configuration_error` | person or agent | A URL is missing, such as `url`. Add it to the profile. |
| `invalid_request` | agent | HTTP 400. Fix the request the message names. |
| `resource_exists` | person | Decide: re-run with `--reuse` to adopt `details.gatewayId`, or choose another name. |
| `unavailable` | person | The hop is unreachable. Check the URL, the ingress and the service's pods. |
| `check_failed` | person | `details.hop` and `details.cause` name the broken hop. Fix it and re-run the check. |
| `cloud_unsupported` | person | The profile is `kind = "cloud"`. Follow `details.steps` in the console. |
| `input_error`, `usage_error` | agent | Fix the command. A destructive command under `--no-input` needs `--yes` from a person. |

`--write-env .env` writes `IRIS_CONTEXT_GATEWAY_URL` (the Gateway's MCP endpoint), `IRIS_CONTEXT_GATEWAY_ID` and `IRIS_CONTEXT_GATEWAY_API_KEY`. Add the same three names to `.env.example` with empty values. Never commit `.env`.

Add the Upstreams (question 1). `IRIS_CONTEXT_GATEWAY_ID` is not a secret; pass `--gateway-id` with the `gatewayId` `create` printed (`gw_` and 32 hex characters):

```
iris --json --no-input context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef upstream add --name CRM --endpoint https://crm.example.com/mcp --bearer-secret env:CRM_TOKEN
iris --json --no-input context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef upstream add --name Tickets --endpoint https://tickets.example.com/mcp --header X-Api-Key --header-secret env:TICKETS_KEY
iris --json --no-input context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef upstream tools crm
```

An `upstream add` that prints `initialCatalogFailure` still created the Upstream: 422 means the Upstream refused the credentials (fix with `upstream update`, then `upstream refresh`), 424 means discovery failed (check the control plane can reach the endpoint), 408 means it timed out. For a `--kind context-surface` Upstream, 422 means the Surface database refused the control plane's login and 424 means tool generation failed (for example a Redis `NOPERM`): both are fixed in the deployment config, then `upstream refresh`.

### Write the data model

A Context Surface Upstream takes a data model: JSON that says which records the agent can read and how they are indexed. The Gateway generates the tools from it, so write it before `upstream add --kind context-surface`.

| Level | Members |
|---|---|
| Model | `title`, `description`, `entities[]` |
| Entity | `name`, `description`, `redis_key_template` (for example `order:{id}`, default `<Name>:{id}`), `relationships[]`, `fields[]`, optional `document_type` |
| Field | `name`, `type`, `description`, `is_key_component`, `redis_indices[]`, optional `allowed_values` for a tag |
| Relationship | `name`, `target` (an entity), `description`, `source_field` (a field of this entity) |

Rules:

- Every `{placeholder}` in the key template is a field with `is_key_component: true`. A key field takes no index. The text before the first placeholder (`order:`) must be a literal that ends in `:`, `_`, `-`, `/` or `.`: it is the index prefix.
- Field `type` is `str`, `int`, `float`, `bool`, `list[str]`, `list[float]`, `geo`, `timestamp` or `object`. `object` can't be indexed.
- Records are stored as RedisJSON by default. `"document_type": "hash"` stores an entity as a Hash: no `object` fields, `list[float]` only with a vector index, and key fields must be scalar.
- The Gateway refuses `acl_field_mappings` with a 400, so leave it out: every agent key with access to the Gateway reads every record of the Surface. The example file in the iris repo carries it, so don't copy that one.

Pick an index by how the agent asks:

| Index | Field types | Use it for | Generated tool |
|---|---|---|---|
| `tag` | `str`, `bool`, `list[str]` | Exact filters: status, IDs, categories. `allowed_values` lists the legal values | `filter_<entity>` |
| `text` | `str` | Full text over names, descriptions, notes. `weight` ranks fields, `no_stem` turns stemming off | `search_<entity>_by_text` |
| `numeric` | `int`, `float`, `timestamp` | Ranges and sorting. Sortable unless you set `sortable: false`; `list_` needs a sortable field, and a `timestamp` can't be `sortable: false` | `filter_<entity>`, `list_<entity>`, `summarize_<entity>` |
| `vector` | `list[float]` | Meaning-based search. Needs `vector_dim` and `distance_metric` (`cosine`, `euclidean`, `dot_product`), and an embedding service on the data plane. Redis Cloud can't embed queries yet, so these tools fail there today | `search_<entity>_by_<field>_semantic` when `source_field` names the text field it embeds, else `_similarity`. Also `search_<entity>_by_<field>_hybrid` (text and vector ranked together) when that text field has a `text` index and the Surface Redis supports native hybrid search over RESP3 |
| `geo` | `geo` | Records within a radius | `find_<entity>_near_<field>` |

An entity whose key template has one placeholder also gets `get_<entity>_by_id`, and `count_<entity>` counts records. Across entities, the set tools `intersect_results`, `union_results`, `except_results` and `expand_results` combine filters and follow relationships. Each tool is read-only and appears as `<namespace>__<tool>`, for example `orders__search_order_by_text`. A tool only exists when the model has the field it needs: no `text` index, no text search.

A minimal orders model:

```json
{
  "title": "Orders",
  "description": "Customer orders",
  "entities": [
    {
      "name": "Order",
      "description": "A customer order",
      "redis_key_template": "order:{id}",
      "relationships": [],
      "fields": [
        {"name": "id", "type": "str", "description": "Order ID", "is_key_component": true, "redis_indices": []},
        {"name": "status", "type": "str", "description": "open, shipped or cancelled", "redis_indices": [{"type": "tag"}]},
        {"name": "notes", "type": "str", "description": "Free-text order notes", "redis_indices": [{"type": "text", "weight": 1.0}]},
        {"name": "total", "type": "float", "description": "Order total in dollars", "redis_indices": [{"type": "numeric", "sortable": true}]}
      ]
    }
  ]
}
```

Save it as `orders.json`, and add it with `--surface-database-id ID --data-model orders.json`. Records live at `order:<id>` as JSON documents with those field names. After `upstream add`, `upstream tools orders` lists what was generated. Search results can be partial until Redis finishes indexing existing keys (`FT.INFO <index>`, `percent_indexed` reaches 1). A data model change (`upstream update`) reindexes, so do it when the database has room.

Set policies (questions 3 and 4). `upstream tools` says which tools are cacheable; only those take `--cache-ttl`:

```
iris --json --no-input context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef policy set crm search_customers --cache-ttl 5m
iris --json --no-input context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef policy set crm export_orders --compression-ttl 1h
```

### Rotate keys and secrets

- New agent key: `service key gw_0123456789abcdef0123456789abcdef --write .env` mints one and upserts it into the file. Restart the agent so it reads the new value.
- A second developer on the same Gateway: `service env gw_0123456789abcdef0123456789abcdef --write .env` writes the URL and ID without minting a key, then `service key` gives them their own.
- New Upstream secret: have the person export the new value, then `upstream update crm --bearer-secret env:CRM_TOKEN` (or `--header-secret`) and `upstream refresh crm`.

Full reference: `iris context-gateway <command> --help` (for example `iris context-gateway upstream add --help`).

## 4. Repoint the agent

**MCP-native frameworks** (question 5, yes). Replace each server entry with one Gateway entry. `connect` writes it with the key read from a variable at run time, never printed. In Redis Cloud, run `connect` with a `cloud` profile and no `--gateway-id`: it takes the endpoint from `IRIS_CONTEXT_GATEWAY_URL`.

```
iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef connect --client claude-code --write .mcp.json
iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef connect --client cursor --write .cursor/mcp.json
iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef connect --client adk > gateway_tools.py
iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef connect --client json
```

For another MCP client (OpenAI Agents SDK, LangChain MCP adapters), use the `json` output: the URL, `streamable-http`, and an `Authorization: Bearer` header with the value of `IRIS_CONTEXT_GATEWAY_API_KEY`. Confirm the client's parameter names in step 2. A `.env` file doesn't reach a running client: the variable must be in the environment the client starts in.

**SDK tools** (question 5, no):

```python
from redis_iris import ContextGateway

gateway = ContextGateway.from_env()
tools = gateway.model_tools()  # framework-free Tool objects, one per Gateway tool
```

TypeScript agents: see the [`@redis-iris/context-gateway` API](https://www.npmjs.com/package/@redis-iris/context-gateway).

On LangGraph, `langchain_tools(gateway.hooks())` from `redis_iris.integrations.langgraph` gives LangChain tools for a `ToolNode`. With Agent Memory or Agent Playbooks also wired, stack them so the model gets every product's tools from one place:

```python
from redis_iris.hooks import stack
from redis_iris.integrations.langgraph import attach, langchain_tools

hooks = stack(memory.hooks(), playbook.disclosure(), gateway.hooks())
graph.add_node("tools", ToolNode(langchain_tools(hooks)))
app = attach(hooks, graph).compile()
```

`gateway.call("crm__lookup_customer", id="cust-1042")` calls a tool directly (`result.data`, `result.is_error`), and `gateway.call_as_handle(...)` keeps a large result on the Gateway as a `Handle`. The reads are on the gateway: `gateway.page(handle, limit=5)`, `gateway.query(handle, ...)`, `count`, `aggregate`, `describe` and `gateway.release(handle)`. Async twins: `atools`, `acall`, `apage` and so on.

Then remove what the Gateway replaced: each per-server MCP entry, each per-server secret from the agent's environment (the Gateway holds them now), and any hand-written namespacing or tool filtering.

Tool names change to `namespace__tool`, for example `crm__lookup_customer`. Update any prompt text or code that names a tool.

In search mode the model never sees those names in `tools/list`. It calls `search_tools` with a `query` (and an optional `limit`, default 5), gets back full MCP tool definitions, and runs one with `run_tool`: `tool` holds the `upstreamId` and `originalName` from the match, and `toolArgs` the arguments. Prompt text should describe the task a tool does, not name the tool. Code that calls a tool by name keeps working through the SDK and CLI, which resolve `namespace__tool` for you.

### Handles from the agent's side

With Gateway `compression` enabled, `tools/list` adds seven tools, in both exposure modes: `run_tool_as_handle`, `describe_result`, `count_results`, `page_results`, `query_results`, `aggregate_results` and `release_results`. A tool result over 32 KiB then comes back as a small stub holding a handle (`h_` and 32 hex digits) with a preview and the next step, in place of the full payload. In full mode, a tool that declares an `outputSchema` returns whole. A tool with `--compression-capture never` returns whole, and `run_tool_as_handle` on it is a tool error telling the agent to call the tool directly. Tell the agent in its prompt to read a handle with the tools below and never to ask for the whole payload again.

| The agent wants | Call |
|---|---|
| A big result held for several follow-ups, whatever its size | `run_tool_as_handle` (full mode `name` and `toolArgs`, search mode `tool` with `upstreamId` and `originalName`, and `toolArgs`) |
| The shape, size, fields and expiry of a handle | `describe_result` |
| How many items, or how many per value of one field | `count_results` with `jsonpath` or `groupBy` |
| A sum, min, max or average of numbers | `aggregate_results` with a `jsonpath` |
| Only the items that match a condition | `query_results` with a JSONPath such as `$[?@.status=="open"]`, paged |
| To read items in order, or a text result by bytes | `page_results` with `offset` and `limit` |
| To free the memory early | `release_results` |

When `run_tool_as_handle` answers `handle storage is full, release handles or narrow the query`, the agent should call `release_results` on handles it no longer needs, then retry with a narrower query or call the tool directly.

A handle expires after the deployment's TTL (15 minutes by default) or the tool's `--compression-ttl`, and a read never extends it. An expired, released or another key's handle is a Gateway refusal with reason `unknown_handle`, which the CLI's `handle` commands report as `handle_not_found` (exit 1): call the tool again for a new one. A partial handle (one page of a longer answer) says so in its `completeness` and `warning`. To fetch the next page, call `run_tool_as_handle` again with the paging arguments. A Context Surface capture reads every page itself, up to the deployment limits (10,000 rows), so one large Surface query can fill handle storage (known issue MOD-20735). With compression `DISABLED`, the seven tools are gone from `tools/list`. From the SDK, `gateway.call_as_handle(...)` returns a `Handle`, and `redis_context_gateway.mcp.HANDLE_TOOLS` lists the seven names.

## 5. Verify

Checks 1, 3, 4, 6 and 7 need the agent key in the command's environment: run them as `set -a; . ./.env; set +a; iris ...` in one shell command, never by printing the file.

In Redis Cloud, run 3, 4, 8 and 9 without `--gateway-id`: the `tools` commands use `IRIS_CONTEXT_GATEWAY_URL` and the agent key. The other checks call the control plane or need cache and handles, which cloud doesn't offer.

1. `iris context-gateway service check gw_0123456789abcdef0123456789abcdef` passes every step: token, Gateway, Identity Service, agent key, and one `tools/list` with the agent key.
2. `iris --json context-gateway service show gw_0123456789abcdef0123456789abcdef` shows `cache` and `compression` as the questions need: `ENABLED` for each feature in use, and `databaseBinding` present. A `DISABLED` the agent didn't choose means the database was missing or refused compression (step 3, "Gateway switches and database").
3. `iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef tools list` shows every Upstream's tools namespaced (full mode), or `search_tools` and `run_tool` (search mode). With compression enabled it also lists the seven handle tools.
4. `iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef tools call crm__lookup_customer --arg id=42` returns what the server returned directly.
5. `iris context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef policy list crm` shows the cache and compression policies from questions 3 and 4.
6. Cache hit: with a cache-policy tool, run the same `iris --json context-gateway --gateway-id gw_0123456789abcdef0123456789abcdef tools call crm__search_customers --arg query=acme` twice. The second result's `_meta["com.redis.context-gateway/invocation"]` carries `"cache": {"status": "hit", ...}`, and the first has no `cache` entry.
7. Handle round trip: `tools call crm__export_orders --as-handle` prints a stub with `h_...`, then `handle describe h_...`, `handle page h_... --limit 5` and `handle release h_...` each answer. A second `handle describe` on the released handle exits 1 with `handle_not_found`.
8. Run the agent once on a task that uses a Gateway tool, and show the call went through the Gateway (the namespaced name in the trace or log).
9. Unset `IRIS_CONTEXT_GATEWAY_API_KEY` and confirm the SDK raises `ConfigurationError` naming it, or the MCP client reports an auth failure.

`iris context-gateway service diagnose gw_0123456789abcdef0123456789abcdef` explains a failing Upstream, cache or handle setup, and a missing Gateway database.

## 6. Report

List where the Gateway runs (Redis Cloud or self-managed), the five answers, each Upstream added (name, namespace, endpoint, secret variable name, never the value), the exposure mode, each policy set, the Gateway `cache` and `compression` values and the database behind them, the data model written, files changed, the client configuration written, env vars added and removed, verification output, and anything you could not confirm over MCP.
