---
name: deploy-verify
description: Deploy Cloudflare Workers and verify changes work in staging/preview. Use when asked to "deploy", "ship", "push to staging", "deploy and test", "verify deploy", or "check staging".
---

# Deploy & Verify

Deploy Cloudflare Workers to an environment and verify the changes work by inferring what to test from recent git changes.

## Workflow

```
1. Pre-deploy checks
2. Deploy to target environment
3. Infer verification plan from git diff
4. Run verification
5. Report results (pass/flag issues)
```

## Step 1: Pre-Deploy Checks

Before deploying, verify:

1. **Types pass** — `tsc --noEmit` or project equivalent
2. **Tests pass** — `npm test` / `bun test` / project equivalent
3. **No uncommitted changes** — `git status` should be clean (warn if dirty)
4. **Detect environment config** — read `wrangler.toml` / `wrangler.jsonc` for available environments

```bash
# List available environments from wrangler config
grep -E '^\[env\.' wrangler.toml | sed 's/\[env\.\(.*\)\]/\1/'
```

## Step 2: Deploy

```bash
# To a named environment (staging, preview, etc.)
wrangler deploy --env <environment>

# To production (default if no --env)
wrangler deploy
```

If the project has multiple Workers (monorepo), detect which one changed:
- Check `git diff --name-only` for paths matching Worker directories
- Only deploy the Worker(s) that changed

## Step 3: Infer Verification Plan

This is the key step. Look at what changed and determine what to verify:

```bash
# What changed since last deploy?
git diff HEAD~1 --name-only
git diff HEAD~1 --stat
git log HEAD~1..HEAD --oneline
```

**Inference rules:**

| Change type | What to verify |
|---|---|
| API route handler changed | Hit that endpoint, check response shape and status |
| Middleware changed | Test requests that flow through it |
| Auth logic changed | Test both authenticated and unauthenticated requests |
| KV/D1/R2 bindings changed | Test read/write operations on those bindings |
| Environment variables referenced | Verify secrets are set: `wrangler secret list --env <env>` |
| CORS or headers changed | Check response headers |
| Error handling changed | Test error paths |
| New route added | Hit the new route, verify 200 + correct response |
| Route removed | Verify it returns 404 |
| Static assets changed | Fetch them and verify content |

## Step 4: Run Verification

Use `curl` or `fetch` to test the deployed URL:

```bash
# Basic health check
curl -s -o /dev/null -w "%{http_code}" https://<worker-url>/

# Check specific endpoint with response body
curl -s https://<worker-url>/api/endpoint | jq .

# Check response headers
curl -sI https://<worker-url>/api/endpoint

# POST with body
curl -s -X POST https://<worker-url>/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

Also check wrangler logs for errors after hitting endpoints:

```bash
# Tail logs (run in background, hit endpoints, then check)
wrangler tail --env <environment> --format json
```

## Step 5: Report

**If all checks pass:**
```
Deploy verified:
- Environment: staging
- URL: https://my-worker-staging.example.workers.dev
- Checks passed:
  - GET /api/stories → 200, response shape correct
  - POST /api/generate → 200, returns stream
  - KV read/write → working
```

**If issues found (flag, don't rollback):**
```
Deploy issues found:
- Environment: staging
- URL: https://my-worker-staging.example.workers.dev
- PASS: GET /api/stories → 200
- FAIL: POST /api/generate → 500
  - Error in logs: "Missing AI binding"
  - Likely cause: AI binding not configured in staging env
- Action needed: Check wrangler.toml [env.staging] AI bindings
```

Do NOT automatically rollback. Flag the issues and let the user decide.

## Multi-Environment Patterns

Common setup:
```toml
# wrangler.toml
name = "my-worker"

[env.staging]
name = "my-worker-staging"
route = "staging.example.com/*"

[env.production]
name = "my-worker"
route = "example.com/*"
```

**Default flow**: Deploy to staging → verify → user promotes to production.
**Direct to prod**: Only when user explicitly asks. Still run verification after.

## Secrets

If verification fails with auth/config errors, check that secrets match between environments:

```bash
wrangler secret list --env staging
wrangler secret list --env production
```

Secrets don't copy between environments. A common gotcha after adding a new env.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| 500 after deploy | `wrangler tail --env <env>` to see error logs |
| Binding not found | Check wrangler.toml — bindings must be declared per environment |
| Secret missing | `wrangler secret put <NAME> --env <env>` |
| Old code still serving | Worker may be cached — wait 30s or check `wrangler deployments list` |
| Route not matching | Verify route patterns in wrangler.toml match the URL you're hitting |
| CORS errors | Check if the Worker sets appropriate CORS headers for the origin |
