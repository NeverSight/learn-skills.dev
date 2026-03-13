---
name: use-sapiom
description: Access 97 cloud-service tools via Sapiom MCP server — scrape websites,
  run code in sandboxes, store data (Redis/Vector/Postgres), search the web, call
  LLMs, generate images and audio, send messages, and manage agent governance.
  Use when user says "use sapiom", "scrape this page", "search the web",
  "run this code in the cloud", "store data", "generate an image",
  "create a database", "set up a message queue", or needs any paid cloud
  service without vendor account setup.
  Do NOT use when sapiom-deploy or sapiom-agent-builder skills are loaded
  (those are more specific).
---

# Sapiom

97 cloud-service tools via one MCP server. Scrape, compute, store, search, generate — pay per use, no vendor accounts.

## Quick Setup — MCP Server (Recommended)

```bash
# Claude Code CLI
claude mcp add sapiom --transport http https://api.sapiom.ai/v1/mcp
```

```json
{
  "mcpServers": {
    "sapiom": {
      "type": "http",
      "url": "https://api.sapiom.ai/v1/mcp"
    }
  }
}
```

Browser auth is used automatically. To use an API key instead, add `--header "Authorization:Bearer YOUR_KEY"` or set the `headers` field. Get a key at https://app.sapiom.ai/settings.

## When to Use

- **Scrape & extract** web content, crawl sites, take screenshots
- **Run code** in cloud sandboxes (Node, Python, Go, Rust) with file I/O and process management
- **Store data** in Redis, Vector DB, Search Index, or ephemeral Postgres
- **Search the web** with Linkup (fast) or You.com (thorough)
- **Generate media** — images (Fal.ai), speech (ElevenLabs), sound effects
- **Send messages** via queues, schedules, and pub/sub

> Building an agent? Use **sapiom-agent-builder**. Just deploying code? Use **sapiom-deploy**.

## Available Tools

### Getting Started (2)

| Tool | Description |
|------|-------------|
| `sapiom_status` | Check MCP session auth and tenant context |
| `tool_discover` | Find the right tool by keyword (free) |

### Scraping & Browser (9) — [details](references/scraping.md)

| Tool | Description |
|------|-------------|
| `sapiom_fetch` | Fetch clean main content from a URL as markdown |
| `sapiom_screenshot` | Capture a webpage screenshot (PNG URL) |
| `sapiom_scrape` | Advanced scrape with format options and selectors |
| `sapiom_crawl` | Crawl an entire website (async, returns job ID) |
| `sapiom_crawl_status` | Check crawl job status and get results |
| `sapiom_map` | Discover all URLs on a site (fast sitemap) |
| `sapiom_extract` | Extract structured data with prompt + schema |
| `sapiom_extract_status` | Check extract job status and get results |
| `sapiom_site_search` | Search within a specific website's content |

### Compute (31) — [details](references/compute.md)

| Tool | Description |
|------|-------------|
| `sapiom_run` | Run code snippet in the cloud (Node/Python/Go/Rust) |
| `sapiom_run_list` | List recent code runs |
| `sapiom_run_get` | Get run result by ID |
| `sapiom_sandbox_create` | Create a persistent cloud sandbox |
| `sapiom_sandbox_list` | List active sandboxes |
| `sapiom_sandbox_get` | Get sandbox details |
| `sapiom_sandbox_delete` | Delete a sandbox |
| `sapiom_sandbox_extend` | Extend sandbox lifetime |
| `sapiom_sandbox_exec` | Execute a command in a sandbox |
| `sapiom_sandbox_deploy` | Deploy sandbox as a persistent service |
| `sapiom_sandbox_write_file` | Write a file to a sandbox |
| `sapiom_sandbox_read_file` | Read a file from a sandbox |
| `sapiom_sandbox_list_files` | List files in a sandbox directory |
| `sapiom_sandbox_delete_file` | Delete a file from a sandbox |
| `sapiom_sandbox_process_logs` | Get process stdout/stderr logs |
| `sapiom_sandbox_process_list` | List running processes in a sandbox |
| `sapiom_sandbox_process_get` | Get process details by PID |
| `sapiom_sandbox_process_stop` | Gracefully stop a process |
| `sapiom_sandbox_process_kill` | Force-kill a process |
| `sapiom_sandbox_preview_create` | Create a public preview URL for a port |
| `sapiom_sandbox_preview_list` | List active preview URLs |
| `sapiom_sandbox_preview_delete` | Delete a preview URL |
| `sapiom_sandbox_ports` | List open ports in a sandbox |
| `sapiom_job_deploy` | Deploy a scheduled/triggered job |
| `sapiom_job_list` | List deployed jobs |
| `sapiom_job_get` | Get job details |
| `sapiom_job_update` | Update job config |
| `sapiom_job_delete` | Delete a job |
| `sapiom_job_trigger` | Manually trigger a job execution |
| `sapiom_job_list_executions` | List job execution history |
| `sapiom_job_get_execution` | Get execution result by ID |

### Data (23) — [details](references/data.md)

| Tool | Description |
|------|-------------|
| `sapiom_redis_create` | Create a serverless Redis database |
| `sapiom_redis_create_fixed` | Create a fixed-size Redis database |
| `sapiom_redis_list` | List Redis databases |
| `sapiom_redis_delete` | Delete a Redis database |
| `sapiom_redis_update` | Rename a Redis database |
| `sapiom_redis_command` | Execute any Redis command |
| `sapiom_vector_create` | Create a vector index |
| `sapiom_vector_list` | List vector indexes |
| `sapiom_vector_delete` | Delete a vector index |
| `sapiom_vector_update` | Update vector index settings |
| `sapiom_vector_upsert` | Upsert vectors with metadata |
| `sapiom_vector_query` | Query vectors by similarity |
| `sapiom_searchindex_create` | Create a full-text search index |
| `sapiom_searchindex_list` | List search indexes |
| `sapiom_searchindex_delete` | Delete a search index |
| `sapiom_searchindex_update` | Update search index schema |
| `sapiom_searchindex_upsert` | Upsert documents into search index |
| `sapiom_searchindex_query` | Query a search index |
| `sapiom_database_create` | Provision an ephemeral Neon Postgres database |
| `sapiom_database_price` | Get Postgres price estimate (free) |
| `sapiom_database_list` | List active Postgres databases |
| `sapiom_database_get` | Get Postgres database details + connection URI |
| `sapiom_database_delete` | Delete a Postgres database |

### Messaging (16) — [details](references/messaging.md)

| Tool | Description |
|------|-------------|
| `sapiom_message_publish` | Publish a message to a URL endpoint |
| `sapiom_message_enqueue` | Enqueue a message to a named queue |
| `sapiom_message_batch` | Send multiple messages in one call |
| `sapiom_message_get` | Get message delivery status |
| `sapiom_message_cancel` | Cancel a pending message |
| `sapiom_schedule_create` | Create a recurring schedule (cron) |
| `sapiom_schedule_list` | List schedules |
| `sapiom_schedule_get` | Get schedule details |
| `sapiom_schedule_delete` | Delete a schedule |
| `sapiom_schedule_pause` | Pause a schedule |
| `sapiom_schedule_resume` | Resume a paused schedule |
| `sapiom_queue_list` | List message queues |
| `sapiom_queue_get` | Get queue details |
| `sapiom_queue_delete` | Delete a queue |
| `sapiom_queue_pause` | Pause a queue |
| `sapiom_queue_resume` | Resume a paused queue |

### Search (2) — [details](references/search.md)

| Tool | Description |
|------|-------------|
| `sapiom_search` | Web search via Linkup — AI-synthesised answer with sources |
| `sapiom_deep_search` | Web search via You.com — formatted web + news results |

### AI Models (2) — [details](references/ai-models.md)

| Tool | Description |
|------|-------------|
| `sapiom_chat` | Send a prompt to any LLM via OpenRouter |
| `sapiom_list_models` | List available LLM models and pricing |

### Audio (3) — [details](references/audio.md)

| Tool | Description |
|------|-------------|
| `sapiom_text_to_speech` | Convert text to speech (ElevenLabs) |
| `sapiom_sound_effects` | Generate sound effects from description |
| `sapiom_list_voices` | List available ElevenLabs voices (free) |

### Images (1) — [details](references/images.md)

| Tool | Description |
|------|-------------|
| `sapiom_generate_image` | Generate images from text prompt (Fal.ai FLUX) |

### Verify (2) — [details](references/verify.md)

| Tool | Description |
|------|-------------|
| `sapiom_verify_send` | Send a verification code via SMS |
| `sapiom_verify_check` | Check a 6-digit verification code |

### Governance (6) — [details](references/governance.md)

| Tool | Description |
|------|-------------|
| `sapiom_create_agent` | Register a named agent for tracking |
| `sapiom_list_agents` | List registered agents |
| `sapiom_create_spending_rule` | Create spending/usage limits |
| `sapiom_list_spending_rules` | List spending rules |
| `sapiom_create_transaction_api_key` | Create a new API key |
| `sapiom_authenticate` | Get auth flow instructions |

## Recipes

### 1. Research a Topic
`sapiom_search` (quick answer) → `sapiom_deep_search` (more results) → `sapiom_fetch` (read full articles) → `sapiom_chat` (summarize findings)

### 2. Monitor a Page for Changes
`sapiom_scrape` (get content) → `sapiom_redis_command` (store hash, compare with previous) → `sapiom_message_publish` (alert on change) → `sapiom_schedule_create` (run every hour)

### 3. Build a Knowledge Base
`sapiom_crawl` (crawl docs site) → `sapiom_crawl_status` (get pages) → `sapiom_vector_upsert` (store embeddings) → `sapiom_vector_query` (semantic search)

### 4. Run & Deploy Code
`sapiom_run` (test code snippet) → `sapiom_sandbox_create` (persistent environment) → `sapiom_sandbox_exec` (iterate) → `sapiom_job_deploy` (schedule for production)

### 5. Generate Media
`sapiom_generate_image` (create visuals) + `sapiom_text_to_speech` (narration) + `sapiom_sound_effects` (background audio)

## Tips

- `tool_discover` finds the right tool by keyword — it's free, use it when unsure
- Pass `agentName` on gateway calls for per-agent spend tracking
- `sapiom_search` (Linkup) = fast AI answer; `sapiom_deep_search` (You.com) = more raw results
- Provision resources before using them: `sapiom_redis_create`, `sapiom_vector_create`, `sapiom_database_create`
- Set spending rules via `sapiom_create_spending_rule` before deploying autonomous agents
- `sapiom_database_price` is free — always check cost before creating a Postgres DB

## SDK Access (Direct HTTP)

For direct HTTP calls without MCP, use the SDK:

```bash
npm install @sapiom/fetch
# or: npm install @sapiom/axios axios
```

```js
const { createFetch } = require("@sapiom/fetch");
const safeFetch = createFetch({ apiKey: process.env.SAPIOM_API_KEY });

const res = await safeFetch("https://linkup.services.sapiom.ai/v1/search", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ q: "quantum computing", depth: "standard", outputType: "sourcedAnswer" }),
});
```

Python/curl: use standard HTTP with `X-402-Payment` header — see reference files for gateway URLs.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 402 Payment Required | Insufficient balance or spending rule hit | Top up at app.sapiom.ai or check `sapiom_list_spending_rules` |
| MCP connection refused | Wrong URL or auth issue | Verify URL is `https://api.sapiom.ai/v1/mcp`; try browser auth or check API key |
| `tool_discover` returns nothing | Too vague query | Use specific keywords: "scrape", "redis", "image", "search" |
| Scrape returns empty | JS-rendered page needs wait time | Use `sapiom_scrape` with `waitFor: 3000` instead of `sapiom_fetch` |
| "Resource not found" | Using data tool before provisioning | Create first: `sapiom_redis_create`, `sapiom_vector_create`, etc. |
| Database URI missing | DB still provisioning | Wait a few seconds, then `sapiom_database_get` to check status |

## References

| File | Domain | Tools |
|------|--------|-------|
| [scraping.md](references/scraping.md) | Firecrawl + Anchor Browser | 9 |
| [compute.md](references/compute.md) | Sandboxes, Jobs, Runs | 31 |
| [data.md](references/data.md) | Redis, Vector, Search, Postgres | 23 |
| [messaging.md](references/messaging.md) | QStash Messages, Schedules, Queues | 16 |
| [search.md](references/search.md) | Linkup + You.com | 2 |
| [ai-models.md](references/ai-models.md) | OpenRouter Chat + Models | 2 |
| [audio.md](references/audio.md) | ElevenLabs TTS + SFX | 3 |
| [images.md](references/images.md) | Fal.ai Image Generation | 1 |
| [verify.md](references/verify.md) | Prelude Phone Verification | 2 |
| [governance.md](references/governance.md) | Agents, Rules, API Keys | 6 |

Full docs: https://docs.sapiom.ai (append `.md` to any URL for raw markdown)
