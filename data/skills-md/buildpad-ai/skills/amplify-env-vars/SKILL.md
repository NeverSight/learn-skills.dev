---
name: amplify-env-vars
description: Manage AWS Amplify environment variables for the project's main app or a microapp via Buildpad platform MCP tools (amplify_get_env_vars, amplify_set_env_vars). Use when a deployment needs env vars read, set, updated, or removed without opening the Amplify Console.
---

# Amplify Environment Variables — Agentic Management via MCP Tools

## Overview

Amplify environment variables can now be managed **directly by AI agents** using the Buildpad platform MCP tools. You no longer need to set them manually in the Amplify Console.


---

## MCP Tools for Amplify Management

All tools are project-scoped (authenticated by MCP bearer token). Use `microappId` to target a specific microapp; omit it for the project's main Amplify app.

### 1. `amplify_get_env_vars`
Returns the **key names** (not values) currently set on the Amplify app.

```json
{ "name": "amplify_get_env_vars", "arguments": { "microappId": "<uuid>" } }
```

Returns: `{ keys: string[], totalCount: number }`

### 2. `amplify_set_env_vars`
Sets, updates, or removes environment variables. The Amplify API replaces the full env var map — this tool reads current vars, merges your changes, then writes back atomically.

```json
{
  "name": "amplify_set_env_vars",
  "arguments": {
    "microappId": "<uuid>",
    "vars": { "EXTERNAL_BUCKET_NAME": "my-bucket", "EXTERNAL_BUCKET_REGION": "ap-southeast-1" },
    "removeKeys": ["OLD_VAR_NAME"]
  }
}
```

Returns: `{ updatedKeys, removedKeys, totalVarCount }`

**Does NOT trigger a redeploy.** Call `amplify_redeploy` after this.

### 3. `amplify_redeploy`
Triggers a new build on the `main` branch.

```json
{
  "name": "amplify_redeploy",
  "arguments": { "microappId": "<uuid>", "reason": "Updated EXTERNAL_BUCKET_NAME" }
}
```

Returns: `{ jobId, jobStatus }` — save the `jobId` to track progress.

**Do NOT call if a build is already PENDING or RUNNING.**

### 4. `amplify_get_status`
Gets the build job status and per-phase breakdown.

```json
{ "name": "amplify_get_status", "arguments": { "microappId": "<uuid>", "jobId": "<jobId>" } }
```

Returns: `{ status, steps[] }` — each step includes `stepName`, `status`, and a `logUrl` (pre-signed S3 URL, valid ~10 minutes) that links directly to that step's CI build log.

Note: `jobType` may be `null` for git-push-triggered builds — this is expected and not an error.

### 5. `amplify_get_build_log`
Fetches the CI build log (pnpm/next build output) for a specific job.

```json
{
  "name": "amplify_get_build_log",
  "arguments": {
    "microappId": "<uuid>",
    "jobId": "<jobId>",
    "phase": "build",
    "tailLines": 50
  }
}
```

**Response `logSource` field tells you what was returned:**
- `"ci"` — real pnpm/next CI build output (TypeScript errors, missing modules, build failures). This is the correct diagnostic data for build failures.
- `"cloudwatch"` — the CI step URL expired (~10 min window). Returned lines are Lambda execution metrics (timing/RAM), NOT pnpm output. Check the Amplify Console build history instead.
- `"none"` — no data found.

**Call this immediately after detecting a FAILED status** — the CI step `logUrl` is only valid for ~10 minutes after a build completes.

### 6. `amplify_get_access_log`
Fetches HTTP access log lines (method, path, status, latency).

```json
{
  "name": "amplify_get_access_log",
  "arguments": {
    "microappId": "<uuid>",
    "statusCodeFilter": "5xx",
    "maxLines": 50
  }
}
```

### 7. `amplify_get_compute_log`
Searches SSR/Lambda runtime logs using CloudWatch `FilterLogEvents`.

```json
{
  "name": "amplify_get_compute_log",
  "arguments": {
    "microappId": "<uuid>",
    "filter": "Error",
    "maxLines": 50
  }
}
```

**What is in Lambda compute logs:**
- `REPORT RequestId: ... Duration: 8ms Memory Used: 133MB` — Lambda execution metrics
- Your app's `console.log()` / `console.error()` output from Next.js API routes, server components, middleware
- NOT present: HTTP request paths like `GET /api/...` (use `amplify_get_access_log` for that)
- NOT present: pnpm build output (use `amplify_get_build_log` for that)

**Filter guidance (CloudWatch patterns are case-sensitive):**
- App errors: `"Error"` or `"error"` (match the casing your app uses)
- Unhandled rejections: `"UnhandledPromiseRejection"` or `"Unhandled"`
- Lambda cold starts: `"Init Duration"`
- Lambda timeouts: `"Task timed out"`
- Lambda execution summary: `"REPORT"`
- Custom app output: exact string your code logs (e.g. `"[api/items]"`)

> **`filter` is required** — omitting it risks returning thousands of REPORT/START/END lines. Zero results is expected when no app errors occurred.

> **Note:** The `amplify_get_access_log` tool requires HTTP access logging to be enabled on the Amplify app. If not enabled, it will return "Access log group not found" — this is expected.

---

## Standard Workflow: Updating Environment Variables

```
1. amplify_get_env_vars       → see what keys already exist
2. amplify_set_env_vars       → add/update/remove keys (vars + removeKeys)
3. amplify_redeploy           → trigger build (save the jobId)
4. amplify_get_status         → poll every 30–60s until SUCCEED or FAILED
5. (if FAILED) immediately:   → call amplify_get_build_log with tailLines: 50
                                 (step logUrls expire ~10 min after build)
   check logSource in response:
   - "ci" → real pnpm errors, diagnose from the output
   - "cloudwatch" → URLs expired, check Amplify Console
```

---

## Making Amplify Env Vars Available to Next.js API Routes at Runtime

Amplify env vars are available at **build time** by default. For Next.js **API routes** (server-side runtime), you must write them to `.env.production` during the build phase.

Update `amplify.yml` in the microapp repo:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - corepack enable
        - corepack pnpm install
    build:
      commands:
        - echo "EXTERNAL_BUCKET_NAME=$EXTERNAL_BUCKET_NAME" >> .env.production
        - echo "EXTERNAL_BUCKET_REGION=$EXTERNAL_BUCKET_REGION" >> .env.production
        - pnpm build
  artifacts:
    baseDirectory: .next
    files:
      - "**/*"
  cache:
    paths:
      - node_modules/**
```

Then access in API routes:
```ts
const bucket = process.env.EXTERNAL_BUCKET_NAME;
const region = process.env.EXTERNAL_BUCKET_REGION;
```

**Important:** After updating `amplify.yml`, push to `main` or call `amplify_redeploy` — the `echo` commands only take effect during a build.

---

## Security Notes

- Variable **values** are never returned by `amplify_get_env_vars` — only key names.
- All MCP tool calls are project-scoped and audit-logged on the Buildpad platform.
- Do NOT commit secrets to git. Use Amplify env vars + the `echo` pattern above.

