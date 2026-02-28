---
name: sapiom-agent-builder
description: Build and deploy autonomous agents — scripts that run on a schedule,
  call LLMs, scrape the web, store data, and act without user intervention. Use when
  user says "build me an agent", "create a bot", "automate X on a schedule",
  "monitor this page", "summarize X every day", "alert me when Y changes",
  or wants to deploy code that runs autonomously via Sapiom.
  Do NOT use for one-off API calls or deploying existing scripts — use sapiom-deploy instead.
---

# Sapiom Agent Builder

Build and deploy autonomous agents powered by `@sapiom/fetch` SDK and Sapiom service gateways.

## When to Use

- User says "build me an agent that..."
- User wants to "automate X on a schedule"
- User wants a "bot that checks/monitors/scrapes/summarizes"
- User wants to "alert me when X changes"
- User wants to deploy code that runs autonomously

> Already have a working script and just want to deploy it? Use the **sapiom-deploy** skill instead.

## Process

### Phase 1: Parse Intent

Determine from the user's request:

1. **What should the agent do?** — Monitor a website? Summarize content? Research a topic?
2. **How often?** — Every 5 min, hourly, daily, weekly? On-demand?
3. **What output?** — Log to console? Send a webhook? Store results?

Pick a **compute pattern**:

| Pattern | When to Use | Deploy |
|---------|------------|--------|
| **Scheduled job** | Runs periodically on a cron schedule | `POST /v1/jobs` with `schedule` param |
| **Batch job** | Processes N items in parallel on demand | `POST /v1/jobs` (no schedule), trigger via `/executions` |
| **Orchestrator + workers** | Periodic task that fans out per-item work | Scheduled job triggers batch job executions |
| **Sandbox** | Long-running service, exposed ports, persistent filesystem | `POST /v1/sandboxes` |

For agents that iterate over a list of items, consider the **orchestrator + workers** pattern: a lightweight scheduled job handles scraping and diffing, then triggers a separately deployed batch job with new items as task payloads. This processes items in parallel instead of sequentially.

> Full deploy API details: `references/deploy.md`

Map the intent to a **service pattern**:

| Pattern | Description | Services |
|---------|------------|----------|
| **Monitor + Alert** | Watch a page, alert on changes | Firecrawl + OpenRouter |
| **Research + Report** | Search web, read pages, summarize | Linkup + Firecrawl + OpenRouter |
| **Collect + Store** | Scrape data, store for retrieval | Firecrawl + Upstash Vector |
| **Search + Answer** | Query stored data, generate answers | Upstash Vector + OpenRouter |
| **Watch + Notify** | Check URL, send webhook on condition | Firecrawl + QStash |
| **Collect + Persist** | Scrape data, store in SQL database | Firecrawl + Neon Postgres |
| **Track + Report** | Maintain state across runs, report trends | Neon Postgres + OpenRouter |

### Phase 2: Select Capabilities

Read the reference for each service the agent needs. **Only read what you need.** For each service, ask: does the agent actually need this, or is it just nice-to-have? Extra service calls add cost, latency, and failure points — and if a service returns low-quality data, downstream LLM analysis will be wrong too.

| Service | Reference File | When Needed |
|---------|---------------|-------------|
| LLM inference | `references/llm-inference.md` | Agent needs to reason, summarize, classify |
| Web scraping | `references/web-scraping.md` | Agent needs page content |
| Web search | `references/web-search.md` | Agent needs to find URLs |
| Vector storage | `references/vector-storage.md` | Agent needs semantic search / RAG |
| Text search | `references/text-search.md` | Agent needs keyword search |
| Redis cache | `references/redis-cache.md` | Agent needs caching, rate limiting, ephemeral state |
| Message queue | `references/message-queue.md` | Agent needs webhooks / delayed tasks |
| Postgres database | `references/database.md` | Agent needs structured storage / state across runs |
| Deployment | `references/deploy.md` | Always needed (final step) |
| All services | `references/capabilities.md` | Quick overview / comparison |

### Phase 3: Get API Key

The user needs a Sapiom API key. Two options:

1. **MCP tool** (if `sapiom_create_transaction_api_key` is available):
   ```
   Tool: sapiom_create_transaction_api_key
   Parameters: { name: "{agent-name}-key", description: "API key for {agent-name}" }
   ```
   The plain key is shown **only once** — save it immediately.

2. **Manual** (if no MCP tool): Direct user to https://app.sapiom.ai/settings to create an API key.

If the user already has a key, skip this step.

### Phase 4: Write the Script

Start from the appropriate template:

| Template | When |
|----------|------|
| `templates/basic-cron.js` | Simple scrape/fetch agent |
| `templates/llm-agent.js` | Agent that calls an LLM |

Read the template, then adapt it:

1. Copy the SDK setup pattern (same for all agents)
2. Add gateway calls from the reference docs
3. Wire the steps together: gather → process → act
4. Add error handling:
   - Every `safeFetch` call should check `res.ok` and include the response body in the error: `throw new Error(\`... HTTP ${res.status}: ${await res.text()}\`)`
   - If the agent iterates over a list of items, wrap per-item work in try/catch so one failure doesn't abort the entire batch. Log the error and continue.

**Script requirements for deployment:**
- Entry point: `index.js`
- Must have `package.json` with `@sapiom/fetch` in dependencies
- Must have `scripts.start: "node index.js"`
- Agent reads `SAPIOM_API_KEY` from `process.env`
- Keep it simple — one file, no build step
- **Batch job workers** use `const { blStartJob } = require("@blaxel/core")` and call `blStartJob(myFunction)` where `myFunction(args)` receives each task's payload. Add `@blaxel/core` to dependencies. Scheduled jobs and standalone scripts use a normal `main()` function.

**If the agent uses Postgres**, always include an `agent_runs` table to track execution history. See the "Run Tracking" pattern in `references/database.md`. Every agent run should:
1. INSERT a row into `agent_runs` with status `running` at the start
2. UPDATE it to `completed` (with `items_processed` and `summary`) or `failed` (with `error`) at the end
3. Link data rows back to the run via a `run_id` foreign key

### Phase 5: Sample Run

Run the agent locally before deploying. **Expect the first run to fail** — wrong API routes, malformed responses, and bad data are normal. The goal is to catch these issues before deploying a broken agent.

1. **Install dependencies** — `npm install` in the agent directory
2. **Run the script** — `SAPIOM_API_KEY=... node index.js`
3. **Check for errors** — fix any crashes (wrong endpoints, auth failures, JSON parse errors)
4. **Re-run until the script completes without errors**

If the agent processes a list of items, the sample run will naturally cover the full set — don't artificially limit it. The point is to verify the pipeline works end-to-end with real data.

### Phase 6: Quality Check

A successful run doesn't mean the output is correct. Write a **throwaway script** that reads the agent's persisted results and checks whether the data actually makes sense.

What to check:
- **Are LLM outputs grounded?** — If the agent uses search results to inform analysis, do the search results actually relate to the query? Generic or unrelated results mean the search queries need reworking or the search step should be removed.
- **Is structured data well-formed?** — If the agent extracts JSON from LLM responses, are the fields populated with real content or hallucinated/empty values?
- **Are external API results relevant?** — Read a few records and verify that data from external services (search, scrape, enrichment) actually matches what was requested. Bad upstream data will silently produce bad downstream analysis.

If the quality check reveals issues:
1. **Fix the agent script** — adjust prompts, remove unreliable data sources, fix queries
2. **Clear stale data** — drop and recreate tables if the schema changed, or delete bad rows
3. **Re-run from Phase 5**

Repeat until the output holds up to inspection. Only then proceed to deploy.

### Phase 7: Deploy

> **STOP — Before deploying, verify:**
> 1. Phase 5 (Sample Run) completed — the script runs without errors locally
> 2. Phase 6 (Quality Check) passed — the output data is correct and makes sense
>
> If either is incomplete, go back. Deploying a broken agent wastes time — it will fail the same way in the cloud.

Read `references/deploy.md` for the full API reference. Deploy is synchronous — no polling needed.

**Quick summary:**
- **Scheduled job** (most common): ZIP + `POST /v1/jobs?name={name}&schedule={cron}`
- **Batch job**: same deploy, omit `schedule`, trigger via `POST /v1/jobs/{name}/executions`
- **Orchestrator + workers**: scheduled job triggers batch job executions

**Cron schedule selection:**

| Frequency | Cron Expression |
|-----------|----------------|
| Every 5 minutes | `*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every hour | `0 * * * *` |
| Every 2 hours | `0 */2 * * *` |
| Every 6 hours | `0 */6 * * *` |
| Daily at 9am UTC | `0 9 * * *` |
| Weekly Monday 9am | `0 9 * * 1` |

Default to **every 2 hours** (`0 */2 * * *`) unless the user specifies otherwise.

### Phase 8: Verify

After deploy completes:

1. Confirm job status is `deployed` in the response
2. Report to user: job name, cron schedule, services used
3. Remind user to set `SAPIOM_API_KEY` env var if needed

## Troubleshooting

### `safeFetch` is not a function
**Cause:** Wrong import or missing `@sapiom/fetch` dependency.
**Fix:** Ensure `package.json` has `"@sapiom/fetch": "^0.3.0"` and code uses `const { createFetch } = require("@sapiom/fetch")`.

### HTTP 402 Payment Required
**Cause:** Missing or invalid `SAPIOM_API_KEY`.
**Fix:** Check that the env var is set and the key is valid. If running locally: `SAPIOM_API_KEY=sk-... node index.js`. If deployed: pass via `envs` in the deploy body.

### Scrape returns empty/wrong content
**Cause:** Firecrawl got blocked, or the page requires JavaScript rendering.
**Fix:** Try adding `waitFor: 3000` to the scrape options. Some sites block automated requests — test the URL manually first.

### LLM returns garbage or hallucinated data
**Cause:** Input content too long, prompt too vague, or wrong model.
**Fix:** Truncate input (`.slice(0, 8000)`), be more specific in the system prompt, or switch to a more capable model (e.g., `anthropic/claude-opus-4.6`).

### Deploy returns 502
**Cause:** Bad `package.json` — missing `main`, `scripts.start`, or invalid JSON.
**Fix:** Ensure `package.json` has `"main": "index.js"` and `"scripts": { "start": "node index.js" }`.

### Agent runs but produces no output
**Cause:** Env vars missing in deployed environment.
**Fix:** Pass `SAPIOM_API_KEY` via the `envs` field when deploying. The job needs it at runtime to call other gateways.

## Checklist

- [ ] Parsed user intent (what, how often, what output, compute pattern)
- [ ] Selected capabilities (read only needed references)
- [ ] Got API key (MCP tool, manual, or user-provided)
- [ ] Wrote script from template + references
- [ ] Sample run completes without errors
- [ ] Quality checked output data for correctness
- [ ] Deployed via Sapiom (ZIP upload flow)
- [ ] Verified DEPLOYED status
- [ ] Reported results to user
