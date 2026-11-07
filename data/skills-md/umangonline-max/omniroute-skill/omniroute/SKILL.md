---
name: omniroute
description: Control and integrate with the user's OmniRoute instance (self-hosted AI gateway/router). Use whenever the user asks about OmniRoute, routing AI traffic, providers, models, API keys, combos, quotas, usage, cost, compression, MCP tools, or wants an agent (claude, codex, openclaw, hermes, opencode, etc.) pointed at OmniRoute or managed through it. Gives any agent full read/modify control over the gateway on the user's behalf via CLI + REST + MCP surfaces.
---

# OmniRoute Control Skill

> OmniRoute = self-hosted AI gateway: one endpoint in front of ~290 providers, with auto-fallback routing, combos, compression, quota/cost tracking, MCP/A2A servers, and per-agent CLI integrations.
> This skill lets ANY agent (a) integrate its own traffic through the gateway and (b) inspect/modify the gateway on the user's behalf.

## 0. Locate the instance FIRST (do not assume anything)

Run these until one works — every recipe below depends on knowing where the server lives:

```bash
omniroute health 2>/dev/null || echo "no omniroute CLI"
curl -s http://localhost:20128/api/monitoring/health   # default port
curl -s http://localhost:20128/api/settings | head -c 200
```

- Server: default `http://localhost:20128` (dashboard + API same port). Overrides: `OMNIROUTE_BASE_URL`, `OMNIROUTE_API_KEY` env vars, `omniroute` CLI contexts (`omniroute contexts list`).
- CLI: `omniroute` (JSON output with `--output json`). If missing: `npm install -g omniroute`.
- Data dir: `~/.omniroute/` (SQLite `storage.sqlite` + backups).
- Auth: local calls to `/api/*` are trusted (requireLogin=false). If `OMNIROUTE_API_KEY` env is set it grants `manage` scope. Management routes ignore URL-borne keys.
- Version-sensitive: run `omniroute health` and note the version — if a recipe 404s, check `omniroute --help`/`omniroute api --help` for renamed commands rather than assuming the skill is wrong.

## 1. Surface ranking (use in this order)

1. **CLI** — `omniroute <subcommand>` (works in any agent with a shell; auto-discovers server)
2. **REST** — `curl http://<host>:<port>/api/...` (for anything the CLI lacks: settings PATCH, provider CRUD, combos)
3. **MCP** — streamable-http at `<host>:<port>/api/mcp/stream` (100+ tools; for agents with MCP clients). NOTE: `omniroute mcp call` may return 404 when the stdio MCP server is not running (transport is streamable-http); use `omniroute mcp tools list`/`mcp info <tool>` for discovery instead.

## 2. Discover state FIRST (always before changing anything)

```bash
omniroute health            # component health
omniroute status            # full status dashboard
omniroute models            # model catalog (provider-qualified ids)
omniroute providers list    # configured connections + status
omniroute providers status  # key health (age, expiry, cooldown)
omniroute keys list         # gateway API keys
omniroute combo list        # routing combos
omniroute quota             # per-provider quota %
omniroute usage analytics   # requests/tokens/cost, time-windowed
omniroute cost              # cost by provider/model/combo/key
curl -s http://localhost:20128/api/models/catalog | jq .catalog   # grouped by provider
curl -s http://localhost:20128/api/monitoring/health | jq .        # health JSON
```

## 3. Integrate an agent with OmniRoute

### 3a. Auto-generated per-agent config (recommended)
`omniroute setup-opencode | setup-codex | setup-claude | setup-cline | setup-kilo | setup-continue | setup-cursor | setup-roo | setup-crush | setup-goose | setup-aider | setup-qwen`
Each writes that agent's config from the live model catalog (e.g. `setup-opencode` writes the provider into `~/.config/opencode/opencode.json`). Run with `--help` for flags; supports `--base-url`/`--api-key` for remote instances.

### 3b. Manual: point any OpenAI-compatible agent at the gateway
- Base URL: `http://<host>:<port>/v1` (chat completions, responses, embeddings, images, audio, moderations, rerank)
- Model ids: anything in `omniroute models` — e.g. `auto/best-coding`, `combo/<name>`, `<provider>/<model>`
- Auth: gateway API key from `omniroute keys` (or `OMNIROUTE_API_KEY` env)
- Anthropic-compatible surface: `claude/<model>` aliases when enabled; `claude/` prefix models route via Claude Code provider
- Per-request control headers: `X-Route-Model` (force model), `x-omniroute-compression` (override), `X-OmniRoute-Budget`, `X-OmniRoute-Mode`, `idempotency-key`/`x-request-id` (5s dedup window)

### 3c. MCP integration (for MCP-capable agents)
Client config: type `remote`, url `<host>:<port>/api/mcp/stream` (OpenCode/Claude use this). Protocol: POST `initialize` first, server returns `Mcp-Session-Id` header — ALL subsequent calls MUST include it or you get 400 `Mcp-Session-Id header is required`. Sessions idle out in ~5min. Discovery: `omniroute mcp tools list`, `omniroute mcp info <tool>`.

## 4. Control operations (read → modify → verify)

### Settings
```bash
curl -s http://localhost:20128/api/settings            # GET all settings (flat KV)
curl -s -X PATCH http://localhost:20128/api/settings \
  -H 'Content-Type: application/json' -d '{"debugMode":false}'
```
- PATCH is WHITELISTED (zod schema ~85 fields). Unknown keys are SILENTLY dropped (e.g. `comboAutoPromoteEnabled` is not writable in current builds — hardcoded `false`). Verify by re-GETting.
- Concurrency: send `expectedRevision` in body or `If-Match: <revision>` header; mismatch → 409 `SETTINGS_REVISION_CONFLICT`.
- Compression is a separate endpoint with its own strict schema:
```bash
curl -s http://localhost:20128/api/settings/compression                      # GET
curl -s -X PUT http://localhost:20128/api/settings/compression \
  -H 'Content-Type: application/json' \
  -d '{"enabled":true,"defaultMode":"stacked","autoTriggerMode":"standard","autoTriggerTokens":2000,
       "engines":{"caveman":{"enabled":true,"level":"standard"},"rtk":{"enabled":true,"level":"standard"}}}'
```
  Enums are strict (caveman intensity: `lite|full|ultra`; autoTriggerMode: `off|lite|standard|aggressive|ultra|rtk|codex-responses|omniglyph|stacked`). Known-good optimized config: stacked, caveman full on user+system roles, rtk standard on tool results+code blocks, system prompt preserved.

### Providers (connections)
```bash
curl -s http://localhost:20128/api/providers                                     # list
curl -s -X POST http://localhost:20128/api/providers -H 'Content-Type: application/json' \
  -d '{"provider":"openai-compatible-chat","name":"myconn",
       "apiKey":"sk-...","providerSpecificData":{"baseUrl":"https://x.com/v1","prefix":"x","apiType":"chat"}}'
curl -s -X PATCH http://localhost:20128/api/providers/<id> -d '{"isActive":false}'
curl -s -X DELETE http://localhost:20128/api/providers/<id>                      # irreversible — confirm first
curl -s -X POST http://localhost:20128/api/providers/<id>/test                   # test connection
curl -s "http://localhost:20128/api/providers/<id>/models?refresh=true"          # LIVE model fetch (no cache)
```
- Live model discovery works for ANY connection via `GET /api/providers/{id}/models` (`source: api|cache`). Custom openai-compatible connections must set `providerSpecificData.baseUrl` for fetch to work.
- `POST /api/providers/import` CREATES a new connection (fields: `entries[].provider|name|apiKey`) — it does NOT import models. Don't use it to refresh models.
- `testStatus`/`errorCode`/`lastError` on connections reflect last test; `auth_failed`/`upstream_auth_error` = bad key.
- Registry providers may have hardcoded `passthroughModels: false` — static catalog only, but the `/models` endpoint still does live fetch. Don't try to enable passthroughModels per-connection; it's a registry-level field, not a per-connection setting.
- Rate limiting per connection: `rateLimitProtection`, `rateLimitOverrides {rpm,tpm,tpd,minTime,maxConcurrent}`, `quotaWindowThresholds`.

### Keys (gateway API keys)
```bash
omniroute keys list                     # id, scopes, status
curl -s -X POST http://localhost:20128/api/keys -d '{"name":"newkey","scopes":["manage"]}'
curl -s -X DELETE http://localhost:20128/api/keys/<id>
omniroute keys revoke <id>              # soft revoke (keeps audit)
omniroute keys regenerate <id>          # NEW value, old invalid
```
- Key model: `sk-<machineId>-<id>-<crc8>`; scopes include `manage`, `self:usage`, `self:account-quota`; per-key model allow/deny lists, budgets, expiry, `no_log`.
- Secret is stored encrypted (AES-256-GCM); reveal requires `ALLOW_API_KEY_REVEAL`. Rotating a key breaks whatever uses it — confirm with the user first.

### Combos (routing policies)
```bash
omniroute combo list
omniroute combo create <name> --strategy priority      # CLI creates empty combo (name + strategy only)
curl -s http://localhost:20128/api/combos               # full configs
curl -s -X POST http://localhost:20128/api/combos -H 'Content-Type: application/json' \
  -d '{"name":"mycombo","models":["provider/model1","provider/model2"],"strategy":"priority"}'
curl -s -X PATCH http://localhost:20128/api/combos/<id> -d '{"strategy":"weighted","models":[...]}'
omniroute combo switch <name>          # activate
```
- Combo fields: `name, model(s), strategy, nodes[{connectionId, weight, priority}], isActive, endpoint`.
- Strategies: `priority | weighted | round-robin | context-relay | fill-first | p2c | random | least-used | cost-optimized | reset-aware | reset-window | headroom | strict-random | auto | lkgp | context-optimized | cache-optimized | fusion | pipeline` (+internal `quota-share`).
- `auto/*` models are virtual combos (no DB row): `auto/best-coding`, `auto/best-fast`, `auto/best-reasoning`, `auto/best-vision`, `auto/best-chat`, `auto/pro-*`, `auto/<family>`, `auto/<category>:<tier>`; resolve at request time from live candidates. `auto/best-free` = free-tier filter.
- Global fallback: `settings.globalFallbackModel` retries once on 502/503.
- On failure, combos return `ComboDiagnostics {poolSize, attempted, excluded, attemptOrder, terminalReason, recovery}` — use `omniroute simulate --explain` to preview routing before touching config.

### Resilience
```bash
omniroute resilience status | breakers | cooldowns | lockouts
curl -s http://localhost:20128/api/resilience
curl -s -X POST http://localhost:20128/api/resilience/reset   # clear breaker/cooldown state (safe, in-memory)
```
Defaults: backoff steps 1→2→5→10→20min; apikey breaker threshold 12 failures/30s reset; cooldown-aware wait budget 5min; daily quota locks until next 00:00. `rate_limited_until` is persisted per connection (survives restart).

### Cache / compression / quota / usage
```bash
omniroute cache status | clear
curl -s http://localhost:20128/api/cache/stats
curl -s http://localhost:20128/api/settings/compression          # pipeline state
curl -s http://localhost:20128/api/usage/analytics              # requests/tokens/success
curl -s http://localhost:20128/api/usage/budget                 # budget config
curl -s http://localhost:20128/api/quota/pools                  # quota pools
```
- Semantic cache keyed on model+messages hash; `X-OmniRoute-No-Cache` bypasses; invalidation via `/api/cache` (by signature or model).
- Budget: daily/weekly/monthly USD limits per API key; `checkBudget` denies when projected > limit. Set via `omniroute usage budget`.
- Prompt-cache affinity: `promptCacheAffinityEnabled` + `sessionAffinityTtlMs` (e.g. 300000) keep multi-turn sessions on one provider to maximize cache hits.

### Chat / test requests
```bash
omniroute chat "hello" -m auto/best-fast           # one-shot
omniroute stream "explain" -m auto/best-coding     # SSE with inspection
omniroute simulate "..." -m auto/best-coding --explain   # dry-run, no upstream call
curl -s -X POST http://localhost:20128/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"auto/best-fast","messages":[{"role":"user","content":"hi"}]}'
```
Routing is transparent: responses carry `X-OmniRoute-*` headers (route class, connection used). `omniroute logs` shows per-request routing decisions.

## 5. Safety protocol (MANDATORY)

1. **Read before write**: always GET current state, then PATCH only what's needed. Re-GET to verify. Settings PATCH silently drops unknown keys — never assume a change applied.
2. **Never delete** providers/connections/keys/combos without explicit user confirmation (`DELETE` is irreversible; keys deletion cascades budgets).
3. **Never rotate/revoke** an API key that's actively used by other agents unless the user says so.
4. **Don't reveal plaintext secrets** (`omniroute keys reveal`, `omniroute auth`) unless explicitly requested; prefer masked/redacted output.
5. **Spend awareness**: before enabling anything that increases usage (auto-promote, new combos, warming pools, auto-refresh), check current quota/budget.
6. **Prefer dry-runs**: `omniroute simulate --explain`, `providers validate`, agent-skills `/generate` with `dryRun:true`.
7. If a change is reverted or a request conflicts, restore prior values and re-verify before trying something else.

## 6. Troubleshooting quick ref

| Symptom | Cause / fix |
|---|---|
| `omniroute mcp call` / `mcp restart` → 404 | stdio MCP server not running (transport=streamable-http). Use `mcp tools list`, REST, or curl the stream endpoint. |
| MCP 400 `Mcp-Session-Id header is required` | Session handshake: POST `initialize` first, reuse returned session id on all calls. |
| Model missing from catalog | Registry `passthroughModels:false` → run `GET /api/providers/<id>/models?refresh=true` (live fetch works anyway). |
| PATCH setting didn't stick | Key not in PATCH whitelist (e.g. `comboAutoPromoteEnabled`, `mcpEnforceScopes`, `call_log_pipeline_enabled`) — hardcoded in this build, not a config. |
| Connection `testStatus: error` | `errorCode`/`lastError` say why: `auth_failed`/`upstream_auth_error` = bad key; `upstream_unavailable` = endpoint down. |
| Duplicate connections | Created via `POST /api/providers/import` (it creates connections, not models). Delete the dup by id. |
| 429/cooldowns | `omniroute resilience cooldowns`; `rate_limited_until` is persisted — clears on success or reset. |
| Routing surprises | `omniroute simulate --explain` or MCP `omniroute_explain_route <requestId>`; combo diagnostics in error body. |

## 7. MCP tool cheat sheet (100+ tools, key ones)

`omniroute_list_models_catalog`, `omniroute_get_health`, `omniroute_check_quota`, `omniroute_simulate_route`, `omniroute_best_combo_for_task`, `omniroute_route_request` (chat through routing), `omniroute_cost_report`, `omniroute_explain_route`, `omniroute_set_routing_strategy`, `omniroute_set_resilience_profile`, `omniroute_cache_stats/flush`, `omniroute_compression_status/configure`, `omniroute_set_compression_engine`, `omniroute_memory_search/add`, `omniroute_skills_list/enable/execute`, `omniroute_agent_skills_*`, `plugin_*`, `omniroute_web_search/fetch`, `notion_*`, `obsidian_*`, `local_corpus_search/read`, `gamification_*`. Discovery: `omniroute mcp tools list`.

## 8. Installing this skill into other agents

- Codex: `ln -s ~/.agents/skills/omniroute ~/.codex/skills/omniroute`
- Hermes: `ln -s ~/.agents/skills/omniroute ~/.hermes/skills/omniroute` (uses SKILL.md + optional DESCRIPTION.md)
- Claude Code: `ln -s ~/.agents/skills/omniroute ~/.claude/skills/omniroute` (mkdir ~/.claude/skills first)
- OpenClaw: copy as an extension (`~/.openclaw/extensions/omniroute/` with `openclaw.plugin.json`) or point OpenClaw's skills dir at this folder
- OpenCode: already loads from `~/.agents/skills/`
- Or just run the repo's `install.sh` — it detects installed agents and copies into all of the above.

## 9. Known build limitations (don't fight them)

- `comboAutoPromoteEnabled`: not in settings PATCH schema in current builds (stays `false`).
- MCP scope enforcement (`scopesEnforced`): stdio-only env var (`OMNIROUTE_MCP_ENFORCE_SCOPES`), not API-toggable.
- `call_log_pipeline_enabled`: internal DB KV, no API route.
- `passthroughModels`: registry-hardcoded per provider type.
- CLI `mcp call`/`mcp restart`: require the stdio server; streamable-http is the default active transport in recent versions.
