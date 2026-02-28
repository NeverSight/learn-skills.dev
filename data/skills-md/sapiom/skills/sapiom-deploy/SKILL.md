---
name: sapiom-deploy
description: Deploy and run code on Sapiom — scheduled jobs, batch execution,
  sandboxes. Use when user says "deploy this", "ship it", "run this on a schedule",
  "put this on a cron", "run these tasks in parallel", "spin up a server",
  "I need a dev environment", or already has a script and wants it running in the cloud.
---

# Sapiom Deploy

Deploy and run code via Sapiom. ZIP your code, POST it, done.

## When to Use

- User says "deploy this" / "ship it" / "put this in the cloud"
- User wants to run a script on a schedule
- User wants to process N items in parallel
- User wants a persistent environment with ports/filesystem
- User already has working code and wants it deployed

> Building an agent from scratch? Use the **sapiom-agent-builder** skill instead — it handles the full workflow from intent to deploy.

## Deploy Patterns (pick one)

| Pattern | What It Does | When to Use | Reference |
|---------|-------------|-------------|-----------|
| Scheduled job | Runs on cron | Periodic tasks (monitoring, scraping, reports) | `references/jobs.md` |
| Batch job | N parallel tasks on demand | Process a list of items in parallel | `references/jobs.md` |
| Orchestrator + workers | Scheduled job fans out to batch | Periodic task that processes N items | `references/patterns.md` |
| Sandbox | Persistent instance with ports + filesystem | Dev environments, servers, long-running processes | `references/sandboxes.md` |

## Quick Decision

- "Run X every hour" → Scheduled job
- "Process these 50 items" → Batch job
- "Every hour, check for new items, process each" → Orchestrator + workers
- "Spin up a server" / "I need a dev environment" → Sandbox

## Setup (same for all patterns)

```js
const { createFetch } = require("@sapiom/fetch");
const safeFetch = createFetch({
  apiKey: process.env.SAPIOM_API_KEY,
});
const GATEWAY = "https://blaxel.services.sapiom.ai";
```

## Example: Deploy a Script on a Schedule

User says: "Deploy this script to run every 2 hours"

**Steps:**
1. Read `references/jobs.md` for the full API
2. ZIP `index.js` + `package.json` (files at ZIP root, not in a subdirectory)
3. `POST /v1/jobs?name=my-job&schedule=0 */2 * * *` with ZIP body
4. Response returns `{ status: "deployed" }` — deploy is synchronous, no polling

**Result:** Job runs every 2 hours. Check status with `GET /v1/jobs/my-job`.

## Example: Fan Out to Parallel Workers

User says: "Process these 100 URLs in parallel"

**Steps:**
1. Deploy worker code as a batch job (no schedule): `POST /v1/jobs?name=my-worker` with ZIP body
2. Trigger execution: `POST /v1/jobs/my-worker/executions` with `{ tasks: [{ url: "..." }, ...] }`
3. Each task runs in parallel, receives its payload via `blStartJob(async (args) => { ... })`

**Result:** 100 tasks run concurrently. Check progress with `GET /v1/jobs/my-worker/executions/{id}`.

## Troubleshooting

### Deploy returns 502
**Cause:** Bad `package.json` — missing `main`, `scripts.start`, or invalid JSON.
**Fix:** Ensure `package.json` has `"main": "index.js"` and `"scripts": { "start": "node index.js" }`.

### Deploy returns 402
**Cause:** Missing or invalid `SAPIOM_API_KEY`.
**Fix:** Ensure the API key is valid and passed via the `@sapiom/fetch` SDK.

### Job deploys but fails at runtime
**Cause:** Code works locally but crashes in the cloud — usually missing env vars.
**Fix:** Pass `SAPIOM_API_KEY` and any other env vars via the `envs` field in the JSON deploy body.

### ZIP files not found by builder
**Cause:** Files nested in a subdirectory inside the ZIP (e.g., `my-project/index.js` instead of `index.js`).
**Fix:** ZIP from inside the directory: `cd my-project && zip -r ../deploy.zip .`

### Job name conflict
**Cause:** A job with that name already exists.
**Fix:** Use `PUT /v1/jobs/{name}` to update, or `DELETE` then recreate.

## References

- `references/jobs.md` — Jobs API (create, deploy, execute, manage)
- `references/sandboxes.md` — Sandboxes API (create, filesystem, processes, ports)
- `references/patterns.md` — Orchestrator + workers pattern with concrete example
