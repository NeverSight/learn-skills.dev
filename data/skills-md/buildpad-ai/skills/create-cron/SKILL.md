---
name: create-cron
description: Create and manage DaaS cron jobs for scheduled background tasks. Sets up recurring jobs with cron expressions, sandboxed JS code, timezone support, execution history, and overlap protection. Use when the user needs scheduled tasks, recurring jobs, background processing, or timed automation.
argument-hint: "[job name] [schedule: every-minute|hourly|daily|weekly|monthly|custom]"
---

# Create Cron Job

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

Set up scheduled background tasks using the DaaS cron system. Cron jobs run recurring logic — archive stale records, send digests, sync external systems — without deploying new code.

## Overview

<!-- buildpad-backend: supabase -->
Cron jobs are stored in the database (`daas_cron_jobs`) and executed at runtime using the same JavaScript sandbox as [Runtime Extensions](../hooks-extensions/SKILL.md). They are managed via REST API or MCP.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Cron jobs are stored in the Engine (`daas_cron_jobs`) and executed by the Engine's runtime, the same runtime as [Runtime Extensions](../hooks-extensions/SKILL.md). They are managed in the Studio's Cron module, through the Engine's REST API (`<Engine_URL>/api/cron`) with an administrator's session, or through the Engine's MCP tool `cron`, which is listed and served to an administrator only (see [Cron REST Routes](#cron-rest-routes)).

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

On an Engine project an active cron job fires at its scheduled time. A job can also be run by hand at any time (`POST /api/cron/:id/run`).
<!-- /buildpad-backend -->

**Key properties:**

| Property    | Description                                           |
| ----------- | ----------------------------------------------------- |
| Schedule    | Standard 5-field cron expression (`min hour dom mon dow`) |
| Timezone    | IANA timezone string (default `UTC`)                  |
| Code        | JS snippet (same sandbox as runtime extensions)       |
| Status      | `active` / `inactive`                                 |
| Timeout     | Max execution time in ms (default 30,000)             |
| History     | Every run is recorded in `daas_cron_history`          |

## Setup Steps

<!-- buildpad-backend: supabase -->
### 1. Create a Cron Job (Inactive First)

Always create jobs as `inactive` initially, test them, then activate.

```json
{
  "name": "mcp_daas_cron",
  "arguments": {
    "action": "create",
    "name": "Nightly Cleanup",
    "description": "Archive stale sessions every night at midnight",
    "schedule": "0 0 * * *",
    "timezone": "Asia/Singapore",
    "code": "const items = await services.items('sessions');\nconst cutoff = new Date(Date.now() - 24 * 3600_000).toISOString();\nconst stale = await items.readByQuery({ filter: { updated_at: { _lt: cutoff }, status: { _eq: 'pending' } }, limit: 500 });\nfor (const session of stale) { await items.deleteOne(session.id); }\nconsole.log(`Cleaned up ${stale.length} stale sessions`);",
    "status": "inactive",
    "timeout_ms": 60000
  }
}
```

### 2. Test with Manual Trigger

```json
{
  "name": "mcp_daas_cron",
  "arguments": {
    "action": "run_now",
    "id": "<job-id>"
  }
}
```

### 3. Check Execution History

```json
{
  "name": "mcp_daas_cron",
  "arguments": {
    "action": "history",
    "id": "<job-id>",
    "limit": 5
  }
}
```

### 4. Activate When Satisfied

```json
{
  "name": "mcp_daas_cron",
  "arguments": {
    "action": "activate",
    "id": "<job-id>"
  }
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### 1. Create a Cron Job (Inactive First)

Always create jobs as `inactive` initially, test them, then activate. Create one in the Studio's Cron module, or send the request below from a server-side script or route with an administrator's access token (the Engine also lets a user whose role holds `create` on `daas_cron_jobs` do it). An omitted `status` is stored as `inactive`.

```bash
curl -X POST "$ENGINE_URL/api/cron" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nightly Cleanup",
    "description": "Archive stale sessions every night at midnight",
    "schedule": "0 0 * * *",
    "timezone": "Asia/Singapore",
    "code": "const items = services.items(\"sessions\");\nconst cutoff = new Date(Date.now() - 24 * 3600000).toISOString();\nconst stale = await items.readByQuery({ filter: { updated_at: { _lt: cutoff }, status: { _eq: \"pending\" } }, limit: 500 });\nfor (const session of stale) { await items.deleteOne(session.id); }\nconsole.log(`Cleaned up ${stale.length} stale sessions`);",
    "status": "inactive",
    "timeout_ms": 60000
  }'
```

`$ACCESS_TOKEN` is the access token of a signed-in administrator, never the token in the project's MCP configuration. The answer is `201` with the stored job under `data`. A schedule that is not a cron expression, an unknown timezone, or code that does not compile is refused with `400` and the server's sentence, and nothing is stored.

### 2. Test with Manual Trigger

```bash
curl -X POST "$ENGINE_URL/api/cron/<job-id>/run" -H "Authorization: Bearer $ACCESS_TOKEN"
```

The answer comes when the run has ended: `{ "data": { "historyId": "<uuid>", "message": "Cron job Nightly Cleanup triggered manually" } }`. An empty `historyId` means the job was already running and nothing ran. A run whose code failed still answers `200`; its outcome is the status of the history row. Running a job needs `update` on `daas_cron_jobs`.

### 3. Check Execution History

```bash
curl "$ENGINE_URL/api/cron/<job-id>/history?limit=5" -H "Authorization: Bearer $ACCESS_TOKEN"
```

Each row carries `status` (`running`, `success`, `error` or `timeout`), `error`, `duration_ms`, `triggered_by` (`schedule`, `manual` or `extension`) and `logs`, one entry per console call, each in the form `[<time>] [INFO|WARN|ERROR] <message>`.

### 4. Activate When Satisfied

```bash
curl -X PATCH "$ENGINE_URL/api/cron/<job-id>" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "status": "active" }'
```

On an Engine project an active cron job fires at its scheduled time. Activating the job starts its scheduled runs; to run it once at another time, run it by hand as in step 2 (or from the Studio's Cron module).
<!-- /buildpad-backend -->

## Cron Expressions

Standard 5-field syntax: `min hour dom mon dow`

| Expression      | Meaning              |
| --------------- | -------------------- |
| `* * * * *`     | Every minute         |
| `0 * * * *`     | Every hour           |
| `0 9 * * 1-5`   | Weekdays at 09:00    |
| `0 0 * * *`     | Daily at midnight    |
| `0 0 1 * *`     | Monthly (1st)        |
| `*/15 * * * *`  | Every 15 minutes     |
| `0 */6 * * *`   | Every 6 hours        |
| `30 2 * * 0`    | Sundays at 02:30     |

## Code Sandbox

Cron code runs in the same sandboxed environment as runtime extensions.

<!-- buildpad-backend: supabase -->
### Available Context Variables

| Variable   | Available | Description                                                    |
| ---------- | --------- | -------------------------------------------------------------- |
| `context`  | ✅        | `{ jobId, jobName, triggeredBy, runId, scheduledAt }`          |
| `services` | ✅        | Full services object (12 members — see table below)            |
| `console`  | ✅        | Captured output (appears in history `logs[]`)                  |
| `JSON`     | ✅        | Standard JSON object                                           |
| `Date`     | ✅        | Standard Date object                                           |
| `Math`     | ✅        | Standard Math object                                           |

**NOT available in cron jobs** (these are extension-only):
- ❌ `payload` — Not applicable
- ❌ `meta` — Not applicable
- ❌ `event` — Not applicable
- ❌ `accountability` — Not injected

Cron jobs access data exclusively through `services.*` calls.

### Background Process User Context

Cron jobs run as the **System Service** user (`00000000-0000-0000-0000-000000000000`). This means:

- `user-created` and `user-updated` special fields are auto-set to the system user UUID
- Audit log entries (`daas_activity`) attribute mutations to this system user
- Permission checks are bypassed (admin-level access)
- The system user cannot log in interactively — it exists only in `daas_users`, not in `auth.users`

> **Important:** `readByQuery()` returns `Item[]` directly — **not** `{ data: Item[] }`. The `{ data }` wrapper only exists in REST API responses. Do not destructure with `const { data } = await items.readByQuery(...)`.

### Available Services

| Service                        | Access                                                      |
| ------------------------------ | ----------------------------------------------------------- |
| `services.items(collection)`   | Full ItemsService (readByQuery, createOne, updateOne…)      |
| `services.collections()`       | CollectionsService                                          |
| `services.fields()`            | FieldsService                                               |
| `services.files()`             | FilesService                                                |
| `services.versions()`          | VersionService                                              |
| `services.relations()`         | RelationsService                                            |
| `services.mail()`              | MailService instance (`send()`, `verify()`)                 |
| `services.mail(options)`       | Send email directly (shorthand, returns `SendMailResult`)   |
| `services.fetch(url, opts)`    | Domain-restricted HTTP fetch (same `safeFetch` as extensions) |
| `services.custom(name)`        | Get a custom reusable service module (see [Custom Services](../create-service/SKILL.md)) |
| `services.supabase`            | Raw Supabase client (service role, bypasses RLS)            |
| `services.env`                 | Whitelisted environment variables (`NODE_ENV`, `NEXT_PUBLIC_SITE_URL`) |

### `mcp_daas_cron` Actions

| Action     | Parameters                                                                 | Purpose                        |
| ---------- | -------------------------------------------------------------------------- | ------------------------------ |
| `list`     | —                                                                          | List all cron jobs             |
| `read`     | `id`                                                                       | Read job details               |
| `create`   | `name`, `code`, `schedule`, `description?`, `timezone?`, `status?`, `timeout_ms?` | Create a cron job     |
| `update`   | `id`, `name?`, `code?`, `schedule?`, `status?`, `timeout_ms?`, …          | Update a cron job              |
| `delete`   | `id`                                                                       | Delete a cron job              |
| `run_now`  | `id`                                                                       | Manually trigger job immediately |
| `activate` | `id`                                                                       | Set status to active           |
| `deactivate` | `id`                                                                     | Set status to inactive         |
| `history`  | `id`, `limit?`                                                             | View run history with logs     |
| `clone`    | `id`, `name?`                                                              | Clone a cron job               |

### Blocked Globals

`setTimeout`, `setInterval`, `require`, `import`, `eval`, `Function` constructor.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Available Context Variables

| Variable   | Available | Description                                                    |
| ---------- | --------- | -------------------------------------------------------------- |
| `context`  | ✅        | `{ jobId, jobName, triggeredBy, runId, scheduledAt }`; `runId` is the id of this run's history row, `scheduledAt` an ISO-8601 string in UTC |
| `services` | ✅        | The Engine's services (see the table below)                     |
| `console`  | ✅        | Captured output (appears in the history row's `logs`)           |
| `JSON`     | ✅        | Standard JSON object                                           |
| `Date`     | ✅        | Standard Date object                                           |
| `Math`     | ✅        | Standard Math object                                           |

**NOT available in cron jobs** (these are extension-only):
- ❌ `payload` — Not applicable
- ❌ `meta` — Not applicable
- ❌ `event` — Not applicable
- ❌ `accountability` — Not injected

Cron jobs access data exclusively through `services.*` calls. The code is the body of an async function in strict mode: `await` and `return` work at the top level, and assigning to an undeclared name is a `ReferenceError`.

### Background Process User Context

On an Engine project a cron job runs as the Engine's system account (`00000000-0000-0000-0000-000000000000`), whether the schedule, a manual run or other stored code started it. This means:

- The system account holds the Administrator policy, so its `services.items` calls pass every permission check; `{ elevated: true }` changes nothing for it
- `user_created` and `user_updated` fields, where a collection has them, are set to the system account's id
- Every write is recorded in the activity log under the system account, with the user agent `daas-automation-runtime/cron`
- The system account cannot sign in

> **Important:** `readByQuery()` returns `Item[]` directly — **not** `{ data: Item[] }`. The `{ data }` wrapper only exists in REST API responses. Do not destructure with `const { data } = await items.readByQuery(...)`.

### Available Services

| Service                        | Access                                                      |
| ------------------------------ | ----------------------------------------------------------- |
| `services.items(collection, opts?)` | Nine methods: `readByQuery`, `readOne`, `readMany`, `createOne`, `createMany`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany` |
| `services.collections()`       | Read only: `readAll`, `readOne`                             |
| `services.fields()`            | Read only: `readAll`, `readOne`                             |
| `services.relations()`         | Read only: `readAll`, `readOne`                             |
| `services.files()`             | File metadata only: `readByQuery`, `readOne`                |
| `services.versions()`          | `readAll`, `readOne`, `promote`                             |
| `services.mail(options)`       | Send email; returns `{ success, ... }` and does not throw when mail cannot be sent |
| `services.mail()`              | An object with `send(options)` and `verify()`               |
| `services.fetch(url, init?)`   | HTTP to the hosts the Engine's operator allows             |
| `services.custom(name, opts?)` | A custom service module; `await` it (see [Custom Services](../create-service/SKILL.md)) |
| `services.cron`                | `trigger(idOrName)`, `list(status?)`, `get(idOrName)`       |
| `services.env`                 | Only the variables the Engine's operator names; empty by default |

On an Engine project stored code (hooks, cron jobs, custom services) runs in the Engine's runtime, which provides only what the table [Engine runtime](#engine-runtime) lists; for each interface it lacks, the table says what replaces it.

### Engine runtime

What a cron job's code has on the Engine, and what replaces what it lacks.

| Interface taught on a Supabase project | On the Engine | Replacement |
|---|---|---|
| The Supabase service in stored code (`services.supabase`) | Refused permanently: `501 RUNTIME_SUPABASE_UNAVAILABLE` | `services.items(collection)`, with `{ elevated: true }` where a hook or custom service must act as an administrator |
| SQL functions, remote procedure calls and raw SQL from stored code | No path | `services.items` calls, or a custom service built on them |
| `services.items(c)` methods | Nine: `readByQuery`, `readOne`, `readMany`, `createOne`, `createMany`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany`; `readByQuery` returns the array itself | Read `result`, not `result.data`; loop over `updateOne`/`deleteOne` where a query-wide update or delete was used |
| Query keys | `fields`, `filter`, `sort`, `limit`, `page`, `offset`, `search`; any other key is refused. Without `limit` a read returns 25 rows; `limit` is capped at 1000 | Drop the key; set `limit` |
| Filters across relations | One relation deep (`{ "comments.status": { _eq: "published" } }` or `{ comments: { _has: true } }`); a path through two relations, `_some` and `_none` are refused | Read the related collection first |
| Schema services | Read only: `readAll`, `readOne` | Change structure through the Engine's API (see [create-collection](../create-collection/SKILL.md)) |
| `services.files` | Metadata only: `readByQuery`, `readOne` | Upload and download through the application and `/api/files` |
| `services.mail` | Options `to`, `subject`, `html`, `text`, `replyTo`; returns `{ success, ... }` and does not throw when mail cannot be sent; a wrong option throws `400 INVALID_PAYLOAD` | Check `success` |
| `services.env` | Empty unless the Engine's operator names keys (`RUNTIME_ENV_WHITELIST_CRON`, `RUNTIME_ENV_WHITELIST_GLOBAL`) or sets prefixed variables (`CRON_PUBLIC_<KEY>`, `RUNTIME_PUBLIC_<KEY>`); `NODE_ENV` and `NEXT_PUBLIC_SITE_URL` are not exposed | Ask the operator to name the key; never assume one |
| `services.fetch` | Only hosts in the operator's `EXTENSION_ALLOWED_DOMAINS` (and their subdomains); an empty list allows `localhost` only; responses over 8 MiB are refused | Ask the operator to allow the host |
| `fetch`, `process`, `require`, `import`, `setTimeout`, `setInterval`, `eval`, `Function` | Do not exist: using one is a `ReferenceError` | `services.fetch`; no timers |
| `Intl` (for example `Intl.NumberFormat`) | Not in the runtime's globals | Format numbers and dates by hand |
| `console.table`, `console.trace` | Do not exist; `log`, `info`, `debug`, `warn`, `error` only | `console.log` |
| A run's memory | `memory_limit_mb` is stored and shown but not enforced | Keep batches small; `timeout_ms` is the only bound |
| Filesystem extensions, `/api/ext/*` endpoints | None | Stored hooks, cron jobs, custom services |

### Cron REST Routes

On an Engine project cron jobs are managed through these routes, the Studio's Cron module, or the Engine's MCP tool `cron`. The tool is listed and served to an administrator only, so the agent can use it when the project's MCP configuration carries an administrator's token. Its `action` is `list`, `read`, `create`, `update`, `delete`, `activate`, `deactivate`, `clone`, `run_now` or `history`; the job's fields (`name`, `schedule`, `timezone`, `code`, `status`, `timeout_ms`) and `id` stand at the top level of `arguments`, and a change takes effect as the route's write of the same body does. A `delete` is refused while the project's MCP deletes are off. If the tool is not listed, the project's Engine is older than 0.1.0-dev.4: use these routes.

| Method   | Path                     | Needs on `daas_cron_jobs` | Purpose                          |
| -------- | ------------------------ | ------------------------- | -------------------------------- |
| `GET`    | `/api/cron`              | `read`                    | List jobs (`search`, `status`, `page`, `limit`) |
| `POST`   | `/api/cron`              | `create`                  | Create a job                     |
| `GET`    | `/api/cron/:id`          | `read`                    | Read one job                     |
| `PATCH`  | `/api/cron/:id`          | `update`                  | Update the fields sent; `status` activates or deactivates |
| `DELETE` | `/api/cron/:id`          | `delete`                  | Delete a job and its history     |
| `POST`   | `/api/cron/:id/run`      | `update`                  | Run the job now                  |
| `POST`   | `/api/cron/:id/clone`    | `create` and `read`       | Copy a job (optional body `{ "name": "<new name>" }`); the copy is inactive |
| `GET`    | `/api/cron/:id/history`  | `read`                    | Runs of one job, newest first    |
| `GET`    | `/api/cron/history`      | `read`                    | Runs of every job, newest first  |

An administrator passes every check. A grant on `daas_cron_history` opens nothing.

### Blocked Globals

`setTimeout`, `setInterval`, `require`, `import`, `eval`, `Function` constructor, `fetch`, `process`, and the file system.
<!-- /buildpad-backend -->

## Common Patterns

### Data Cleanup

```javascript
// Archive items older than 30 days
const items = await services.items('temp_uploads');
const cutoff = new Date(Date.now() - 30 * 24 * 3600_000).toISOString();
const expired = await items.readByQuery({
  filter: { created_at: { _lt: cutoff } },
  limit: 1000,
});
for (const item of expired) {
  await items.deleteOne(item.id);
}
console.log(`Archived ${expired.length} expired uploads`);
```

### Digest / Report Generation

```javascript
// Daily summary of new items
const items = await services.items('orders');
const yesterday = new Date(Date.now() - 24 * 3600_000).toISOString();
const newOrders = await items.readByQuery({
  filter: { created_at: { _gte: yesterday } },
  fields: ['id', 'total', 'status'],
});
const total = newOrders.reduce((sum, o) => sum + (o.total || 0), 0);
console.log(`Daily report: ${newOrders.length} orders, total: $${total}`);
```

### External Sync

<!-- buildpad-backend: supabase -->
```javascript
// Sync contacts to external CRM every 6 hours
const items = await services.items('contacts');
const unsynced = await items.readByQuery({
  filter: { synced: { _eq: false } },
  limit: 100,
});
for (const contact of unsynced) {
  // Process sync logic with services.supabase if needed
  await items.updateOne(contact.id, { synced: true, synced_at: new Date().toISOString() });
}
console.log(`Synced ${unsynced.length} contacts`);
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```javascript
// Sync contacts to an external CRM every 6 hours
const items = services.items('contacts');
const unsynced = await items.readByQuery({
  filter: { synced: { _eq: false } },
  limit: 100,
});
for (const contact of unsynced) {
  // Send the contact with services.fetch to a host the Engine's operator allows
  await items.updateOne(contact.id, { synced: true, synced_at: new Date().toISOString() });
}
console.log(`Synced ${unsynced.length} contacts`);
```
<!-- /buildpad-backend -->

### Status Escalation

```javascript
// Auto-escalate unresolved tickets after 48 hours
const items = await services.items('tickets');
const cutoff = new Date(Date.now() - 48 * 3600_000).toISOString();
const overdue = await items.readByQuery({
  filter: {
    _and: [
      { status: { _eq: 'open' } },
      { created_at: { _lt: cutoff } },
      { priority: { _neq: 'critical' } }
    ]
  },
  limit: 200,
});
for (const ticket of overdue) {
  await items.updateOne(ticket.id, { priority: 'critical', escalated_at: new Date().toISOString() });
}
console.log(`Escalated ${overdue.length} overdue tickets`);
```

<!-- buildpad-backend: supabase -->
## Next.js API Proxy Routes

> **Need an admin UI for cron jobs?** Do not hand-build pages over these routes. The Cron Jobs module ([add-cron](../add-cron/SKILL.md), `npx @buildpad/cli@latest add cron-routes`) ships the jobs list, the job editor and the run history, and calls DaaS directly from the browser — it needs explicit DaaS CORS origins, and none of the proxy routes below. The routes below are for an app's own server-side or custom calls.

All cron API calls from the browser must go through Next.js proxy routes (Rule 4: No CORS).

### Proxy Route Pattern

```typescript
// app/api/cron/route.ts
import { NextRequest } from 'next/server';
import { proxyToDaaS } from '@/lib/proxy';

export async function GET(request: NextRequest) {
  return proxyToDaaS(request, '/api/cron');
}

export async function POST(request: NextRequest) {
  return proxyToDaaS(request, '/api/cron');
}
```

```typescript
// app/api/cron/[id]/route.ts
import { NextRequest } from 'next/server';
import { proxyToDaaS } from '@/lib/proxy';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return proxyToDaaS(request, `/api/cron/${id}`);
}

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return proxyToDaaS(request, `/api/cron/${id}`);
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return proxyToDaaS(request, `/api/cron/${id}`);
}
```

```typescript
// app/api/cron/[id]/run/route.ts
import { NextRequest } from 'next/server';
import { proxyToDaaS } from '@/lib/proxy';

export async function POST(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return proxyToDaaS(request, `/api/cron/${id}/run`);
}
```

```typescript
// app/api/cron/[id]/history/route.ts
import { NextRequest } from 'next/server';
import { proxyToDaaS } from '@/lib/proxy';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return proxyToDaaS(request, `/api/cron/${id}/history`);
}
```

## Environment Variables

| Variable                  | Default | Description                      |
| ------------------------- | ------- | -------------------------------- |
| `CRON_ENABLED`            | `true`  | Set `false` to disable all jobs  |
| `CRON_HISTORY_RETENTION`  | `100`   | History rows kept per job        |

## Overlap Protection

If a job takes longer than its schedule interval, the next tick is automatically skipped. The DB `running` flag prevents concurrent runs of the same job.

## History Retention

Default: **100 rows per job** (configurable via `CRON_HISTORY_RETENTION`). Old rows are pruned automatically after each run.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Next.js API Proxy Routes

> **Need an admin UI for cron jobs?** Do not hand-build pages over these routes. The Cron Jobs module ([add-cron](../add-cron/SKILL.md), `npx @buildpad/cli@latest add cron-routes`) ships the jobs list, the job editor and the run history, and calls the Engine directly from the browser with the user's access token — it needs no cross-origin setting and none of the routes below. The routes below are for an app's own server-side or custom calls.

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

### Proxy Route Pattern

Each route forwards the signed-in user's `Authorization` header to the Engine and passes the Engine's status and `{ errors: [...] }` body through unchanged.

```typescript
// lib/engine-forward.ts
import { NextRequest, NextResponse } from 'next/server';
import { getAuthHeaders, getDaasUrl } from '@/lib/api/auth-headers';

export async function forwardToEngine(request: NextRequest, path: string) {
  const headers = await getAuthHeaders();
  const body = ['GET', 'HEAD'].includes(request.method) ? undefined : await request.text();
  const response = await fetch(`${getDaasUrl()}${path}${request.nextUrl.search}`, {
    method: request.method,
    headers: { ...headers, 'Content-Type': 'application/json' },
    body,
    cache: 'no-store',
  });
  const text = await response.text();
  return new NextResponse(text || null, {
    status: response.status,
    headers: { 'Content-Type': response.headers.get('content-type') ?? 'application/json' },
  });
}
```

```typescript
// app/api/cron/route.ts
import { NextRequest } from 'next/server';
import { forwardToEngine } from '@/lib/engine-forward';

export async function GET(request: NextRequest) {
  return forwardToEngine(request, '/api/cron');
}

export async function POST(request: NextRequest) {
  return forwardToEngine(request, '/api/cron');
}
```

```typescript
// app/api/cron/[id]/route.ts
import { NextRequest } from 'next/server';
import { forwardToEngine } from '@/lib/engine-forward';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return forwardToEngine(request, `/api/cron/${id}`);
}

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return forwardToEngine(request, `/api/cron/${id}`);
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return forwardToEngine(request, `/api/cron/${id}`);
}
```

```typescript
// app/api/cron/[id]/run/route.ts
import { NextRequest } from 'next/server';
import { forwardToEngine } from '@/lib/engine-forward';

export async function POST(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return forwardToEngine(request, `/api/cron/${id}/run`);
}
```

```typescript
// app/api/cron/[id]/history/route.ts
import { NextRequest } from 'next/server';
import { forwardToEngine } from '@/lib/engine-forward';

export async function GET(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return forwardToEngine(request, `/api/cron/${id}/history`);
}
```

## Environment Variables

These are settings of the Engine, made by its operator, not variables of the application:

| Variable                   | Default | Description                                         |
| -------------------------- | ------- | --------------------------------------------------- |
| `CRON_ENABLED`             | `true`  | `false` stops scheduled runs; manual runs still work |
| `CRON_HISTORY_RETENTION`   | `100`   | History rows kept per job                           |
| `CRON_STALE_LOCK_GRACE_MS` | `30000` | Added to a job's `timeout_ms` before a lock left by a stopped process is taken over |

## Overlap Protection

A job never runs twice at once. A run takes the job's lock first; a run that finds the lock held is skipped, and a manual run then answers an empty `historyId`. A lock left by a process that stopped mid-run is taken over once `timeout_ms` plus `CRON_STALE_LOCK_GRACE_MS` has passed.

## History Retention

Default: **100 rows per job** (`CRON_HISTORY_RETENTION`, set by the Engine's operator). Older rows of that job are removed after each run.
<!-- /buildpad-backend -->

## References

- [Cron expressions & sandbox](references/cron-sandbox.instructions.md)
<!-- buildpad-backend: supabase -->
- [Cron MCP tool](references/cron-mcp.instructions.md)
<!-- /buildpad-backend -->
- [Cron API routes](references/cron-api.instructions.md)

````
