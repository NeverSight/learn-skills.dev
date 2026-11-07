---
name: hooks-extensions
description: DaaS runtime extensions (hooks) and utilities API reference. Covers filter hooks (validation, transformation before save), action hooks (audit logging, notifications after save), and utility endpoints. Use DaaS extensions instead of implementing backend logic in Next.js API routes. Automatically loaded as background context.
user-invokable: false
---

# Hooks & Extensions Reference

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

<!-- buildpad-backend: supabase -->
## Runtime Extensions

DaaS runtime extensions (hooks) run server-side on data events. They replace custom backend logic in Next.js API routes.

### Extension Types

| Type     | When             | Use For                                                | Blocking?        |
| -------- | ---------------- | ------------------------------------------------------ | ---------------- |
| `filter` | Before operation | Validation, data transformation, auto-populate fields  | Yes — can reject |
| `action` | After operation  | Audit logging, notifications, sync to external systems | No — async       |

### Creating Extensions via MCP

Use **top-level parameters** (not wrapped in a `data` object):

```json
// Filter hook — validate before save
{
  "name": "mcp_daas_extensions",
  "arguments": {
    "action": "create",
    "name": "Validate Title Length",
    "event": "articles.items.create",
    "type": "filter",
    "code": "if (!payload.title || payload.title.length < 3) { throw new Error('Title too short'); } return payload;",
    "status": "active"
  }
}

// Action hook — audit logging (async, non-blocking)
{
  "name": "mcp_daas_extensions",
  "arguments": {
    "action": "create",
    "name": "Audit Logger",
    "event": "items.create",
    "type": "action",
    "code": "console.log('Created:', meta.collection, meta.key); await services.items(meta.collection).createOne({ action: 'create', collection: meta.collection, item_id: meta.key, payload_keys: Object.keys(meta.payload || {}) });",
    "status": "active"
  }
}
```

### `mcp_daas_extensions` Actions

| Action       | Parameters                                             | Purpose                        |
| ------------ | ------------------------------------------------------ | ------------------------------ |
| `list`       | `event?`, `status?`, `type?`                           | List all extensions            |
| `read`       | `id`                                                   | Read extension details         |
| `create`     | `name`, `event`, `type`, `code`, `status?`, `sort?`, `timeout_ms?` | Create an extension |
| `update`     | `id`, `name?`, `event?`, `type?`, `code?`, `status?`, `sort?`, `timeout_ms?` | Update an extension |
| `delete`     | `id`                                                   | Delete an extension            |
| `activate`   | `id`                                                   | Set status to active           |
| `deactivate` | `id`                                                   | Set status to inactive         |
| `clone`      | `id`, `name?`                                          | Clone an extension             |

> **Note:** All parameters are top-level in `arguments` — do NOT wrap them in a `data` object.
> The `delete` action requires the platform setting `mcp_allow_deletes = true` (env: `MCP_ALLOW_DELETES=true`). Without it, delete returns "Delete operations are disabled".

### Event Names

- `items.create` / `items.update` / `items.delete` — All collections
- `[collection].items.create` — Specific collection
- `auth.login` / `auth.logout` — Auth events
- System collections also emit events: `daas_cron_jobs.items.*`, `daas_custom_services.items.*`, `daas_extensions.items.*`, `daas_scope_types.items.*`, `daas_scope_items.items.*`, `daas_scope_collection_config.items.*`, `daas_access.items.*`, `daas_user_roles.items.*`, `daas_settings.items.*`, `daas_folders.items.*`, `daas_users.items.*`, `daas_roles.items.*`

### Built-in Platform Hooks

The following hooks are **hardcoded in the platform** (not runtime extensions). They fire automatically and cannot be disabled or overridden via the extensions API.

| Hook | Event | Purpose |
|---|---|---|
| Role-scope read | `daas_roles.items.read` | Computes the `assignable` boolean on each role based on the current scope context and `scope_config.allowed_scopes` |
| Role-scope validate | `daas_users.items.create`, `daas_users.items.update` | Validates role assignments against `scope_config`. Throws `ROLE_SCOPE_MISMATCH` or `ROLE_SCOPE_LOCKED` if the assignment violates scope restrictions |

> These hooks are implemented in `lib/hooks/role-scope.ts`. Do **not** create runtime extensions for the same events expecting to replicate or override this behavior.

### Hook Context Variables

**Common to all hooks:**

| Variable   | Type    | Description                                                     |
| ---------- | ------- | --------------------------------------------------------------- |
| `services` | object  | Full services object (see table below)                          |
| `context`  | object  | Supabase client (circular reference — do NOT JSON.stringify)    |
| `console`  | object  | `log`, `warn`, `error` — captured in logs                      |
| `JSON`     | object  | `parse`, `stringify`                                            |
| `Date`     | class   | Standard Date constructor                                       |
| `Math`     | object  | Standard Math object                                            |

**Filter hooks — additional variables:**

| Variable  | Type   | Description                                                    |
| --------- | ------ | -------------------------------------------------------------- |
| `payload` | object | The data being written (modify and `return payload`)           |
| `meta`    | object | `{ event, collection }` — event metadata (no payload or key)  |

**Action hooks — additional variables:**

| Variable | Type   | Description                                                                |
| -------- | ------ | -------------------------------------------------------------------------- |
| `meta`   | object | `{ event, payload, key, collection }` — full event data                   |

In action hooks, access event data via `meta`:
- `meta.payload` — The data that was written
- `meta.key` / `meta.keys` — The ID(s) of the created/updated/deleted item(s)
- `meta.collection` — The collection name
- `meta.event` — The event name string (e.g., `"articles.items.create"`)

**NOT available (despite Directus conventions):**
- ❌ `event` — Use `meta.event`
- ❌ `collection` — Use `meta.collection`
- ❌ `key` / `keys` — Use `meta.key` or `meta.keys`
- ❌ `accountability` — Not injected into sandbox

### `services` Object Members

All service factory calls accept an optional `{ elevated: true }` option (see below).

| Member                              | Type     | Purpose                                                |
| ----------------------------------- | -------- | ------------------------------------------------------ |
| `services.items(coll, [opts])`      | async fn | CRUD + aggregate on any collection (17 methods)        |
| `services.collections([opts])`      | async fn | Collection management                                  |
| `services.fields([opts])`           | async fn | Field management                                       |
| `services.files([opts])`            | async fn | File upload, import, download, metadata                |
| `services.versions([opts])`         | async fn | Content versioning — create, save, promote             |
| `services.relations([opts])`        | async fn | Relation management                                    |
| `services.mail()`                   | async fn | Send emails via SMTP (`send()`, `verify()`)            |
| `services.mail(options)`            | async fn | Send email directly (shorthand)                        |
| `services.custom(name, [opts])`      | async fn | Load a reusable custom service (see [Custom Services](../create-service/SKILL.md)) |
| `services.fetch(url)`               | function | Domain-restricted HTTP fetch                           |
| `services.supabase`                 | object   | Raw Supabase client (service role, bypasses RLS)       |
| `services.env`                      | object   | Runtime whitelisted env vars. Always includes `NODE_ENV` and `NEXT_PUBLIC_SITE_URL`. Additional keys configured via `RUNTIME_ENV_WHITELIST_EXTENSION` or `EXTENSION_PUBLIC_*` deployment env vars. Use `services.env.KEY` or `context.services.env.KEY` (equivalent in extensions). `context.env` does NOT exist. |

> **All factory calls are async** — always `await` them. See [Services API reference](references/services-api.instructions.md) for complete method signatures.

### Elevated Permissions

By default, service calls enforce the **triggering user's own permission policies**. Pass `{ elevated: true }` to bypass permission checks while keeping the original user in the audit trail (`user_created`/`user_updated` fields and `daas_activity` log).

Use this when the extension must perform an operation the user is not directly allowed to do — e.g. writing to a field locked by their policy.

```js
// Normal — user's own permissions enforced
const svc = await services.items('orders');

// Elevated — permission checks skipped, user still in audit trail
const svc = await services.items('orders', { elevated: true });
// Same flag works on every service factory:
// services.fields({ elevated: true })
// services.files({ elevated: true })
// services.versions({ elevated: true })
// services.relations({ elevated: true })
// services.collections({ elevated: true })
// services.custom('name', { elevated: true })  ← propagates admin acc into the nested service

// Example: action hook writing to a protected status log (orders.items.create)
const log = await services.items('order_status_log', { elevated: true });
await log.createOne({ order_id: meta.key, status: 'pending', note: 'auto-created' });
```

> **Cron jobs** always run as the system account (`admin: true`). Permission checks are already bypassed — `{ elevated: true }` is not needed in cron code.

> **Custom services** inherit the calling context's accountability. Pass `{ elevated: true }` when *calling* `services.custom('name', { elevated: true })` to give the nested service admin-level accountability — permission checks inside the custom service are bypassed while the triggering user is still recorded in the audit trail. You can also use `{ elevated: true }` on any `context.services` factory call *within* the custom service itself.

### Correct Code Examples

**Filter hook — validate and transform:**
```js
// payload and meta are available directly
const helper = await services.custom('my_validator');
const check = helper.validatePayload(payload, ['name', 'email']);
if (!check.valid) {
  throw new Error('Missing: ' + check.missing.join(', '));
}
payload.name = payload.name.trim().toUpperCase();
return payload; // MUST return payload
```

**Action hook — audit logging:**
```js
// In action hooks, all event data is in meta (not direct variables)
const helper = await services.custom('audit_logger');
const audit = helper.buildAuditEntry(
  'create',
  meta.collection,    // NOT collection (undefined)
  meta.key,           // NOT key (undefined)
  { payload_keys: Object.keys(meta.payload || {}) }
);
const items = await services.items('audit_logs');
await items.createOne(audit);
```

## Performance: Extensions vs API Routes

| Approach              | Request Flow                               | User Waits For    |
| --------------------- | ------------------------------------------ | ----------------- |
| API Route (❌)        | Request → DaaS → Audit → Response          | Operation + Audit |
| Action Extension (✅) | Request → DaaS → Response → (async: Audit) | Operation only    |

## Special Fields (Auto-Populated)

Instead of hooks for timestamps/user tracking, use special fields:

| Field Type   | `meta.special` Value | Purpose                |
| ------------ | -------------------- | ---------------------- |
| UUID PK      | `["uuid"]`           | Auto-generate UUID     |
| Created date | `["date-created"]`   | Auto-set on create     |
| Updated date | `["date-updated"]`   | Auto-set on update     |
| Created by   | `["user-created"]`   | Auto-set creating user |
| Updated by   | `["user-updated"]`   | Auto-set updating user |

## References

- [Hooks & extensions guide](references/hooks-extensions.instructions.md)
- [Services API reference](references/services-api.instructions.md) — complete method signatures for all built-in services
- [Utilities API](references/utilities-api.instructions.md)
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Runtime Extensions

On an Engine project runtime extensions (hooks) are JavaScript stored in the Engine (`daas_extensions`) and run by the Engine on item events. They replace custom backend logic in Next.js API routes.

On an Engine project stored code (hooks, cron jobs, custom services) runs in the Engine's runtime, which provides only what the table [Engine runtime](#engine-runtime) lists; for each interface it lacks, the table says what replaces it.

### Extension Types

| Type     | When             | Use For                                                | Blocking?        |
| -------- | ---------------- | ------------------------------------------------------ | ---------------- |
| `filter` | Before operation | Validation, data transformation, auto-populate fields  | Yes — can reject |
| `action` | After the commit | Audit logging, notifications, sync to external systems | No — its own run |

### Creating Extensions

On an Engine project create and change extensions in the Studio's Extensions module, or through the Engine's REST API `/api/extensions` with an administrator's access token. Only an administrator may create, change, activate, deactivate, clone or delete an extension. An administrator's agent can also use the Engine's MCP tool `extensions`, which is listed and served to an administrator only: its `action` is `list`, `read`, `create`, `update`, `delete`, `activate`, `deactivate` or `clone`, the extension's fields (`name`, `event`, `type`, `code`, `sort`, `status`, `timeout_ms`) and `id` stand at the top level of `arguments`, and a `delete` is refused while the project's MCP deletes are off. If the tool is not listed, the project's Engine is older than 0.1.0-dev.4: use the Studio or the REST API.

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

```bash
# Filter hook — validate before save (stored inactive; activate it after the check below)
curl -X POST "$ENGINE_URL/api/extensions" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Validate Title Length",
    "event": "articles.items.create",
    "type": "filter",
    "code": "if (!payload.title || payload.title.length < 3) { throw new HookError(\"Title too short\", 422, \"VALIDATION_FAILED\"); } return payload;"
  }'

# Activate it
curl -X POST "$ENGINE_URL/api/extensions/<extension-id>/activate" -H "Authorization: Bearer $ACCESS_TOKEN"
```

| Method   | Path                              | Purpose                                  |
| -------- | --------------------------------- | ---------------------------------------- |
| `GET`    | `/api/extensions`                 | List (`event`, `type`, `status`, `search`); needs `read` on `daas_extensions` |
| `GET`    | `/api/extensions/:id`             | Read one; needs `read` on `daas_extensions` |
| `POST`   | `/api/extensions`                 | Create (`201`); an omitted `status` is `inactive` |
| `PATCH`  | `/api/extensions/:id`             | Update the fields sent                   |
| `DELETE` | `/api/extensions/:id`             | Delete                                   |
| `POST`   | `/api/extensions/:id/activate`    | Set status to active                     |
| `POST`   | `/api/extensions/:id/deactivate`  | Set status to inactive                   |
| `POST`   | `/api/extensions/:id/clone`       | Copy (`{ "name": "<new name>" }` optional) |

The fields are `name`, `description`, `event`, `type` (`filter` or `action`), `sort`, `code`, `status`, `timeout_ms` (default 5000) and `memory_limit_mb` (stored, not enforced). Code that does not compile is refused with `400` and nothing is stored. A change is live in every process of the Engine before the request answers.

**There is no test route.** To check a hook: create it inactive, activate it, write a scratch item to the collection it handles (through the Items API or the Studio), read the answer and the hook's console lines in the Engine's log (`GET /api/logs`, for an administrator or a holder of `system:logs`), then delete the scratch item. Deactivate the hook at once if it refuses writes it should not.

Full guide: [Engine hooks guide](references/engine-hooks.instructions.md).

### Event Names

- `items.create` / `items.update` / `items.delete` / `items.read` / `items.query` — All collections
- `[collection].items.create` (and `.update`, `.delete`, `.read`, `.query`) — One collection
- `versions.create` — A content version was created (action only)
- A workflow command's `event_name` — after a transition commits (action only); see [create-workflow](../create-workflow/SKILL.md)
- One `event` may list several names separated by commas

On an Engine project events are emitted by item writes and reads through the Items API, the MCP `items` tool and `services.items` in stored code. The Engine's administration routes (users, roles, policies, cron jobs, custom services, extensions, settings, scope, files) emit no event, and there are no sign-in or sign-out events.

### Built-in Engine Checks

The Engine checks role assignments against a role's scope settings itself (`ROLE_SCOPE_MISMATCH`, `ROLE_SCOPE_LOCKED`), in its own code. Do **not** create runtime extensions to replicate or override that check.

### Hook Context Variables

**Common to all hooks:**

| Variable   | Type    | Description                                                     |
| ---------- | ------- | --------------------------------------------------------------- |
| `services` | object  | The Engine's services (see table below)                         |
| `context`  | object  | `{ accountability, resourceUri, services }`                     |
| `console`  | object  | `log`, `info`, `debug`, `warn`, `error` — captured in the Engine's log |
| `JSON`     | object  | `parse`, `stringify`                                            |
| `Date`     | class   | Standard Date constructor                                       |
| `Math`     | object  | Standard Math object                                            |
| `HookError`| class   | `new HookError(message, statusCode = 400, code = "HOOK_VALIDATION_FAILED")` |

`context.accountability` is `{ user, role, roles, admin, app }` for the caller whose request fired the hook (the system account when there is none). `context.resourceUri` is the caller's tenant scope.

**Filter hooks — additional variables:**

| Variable  | Type   | Description                                                    |
| --------- | ------ | -------------------------------------------------------------- |
| `payload` | any    | The data being written (or the rows read, or the parsed query); return a replacement or nothing |
| `meta`    | object | `{ event, collection }`, plus `keys` on update and delete      |

**Action hooks — additional variables:**

| Variable | Type   | Description                                                                |
| -------- | ------ | -------------------------------------------------------------------------- |
| `meta`   | object | `{ event, collection }` plus: `key` and `payload` on create; `keys` and `payload` on update; `keys` on delete |

In action hooks, access event data via `meta`:
- `meta.payload` — The data that was written (create and update)
- `meta.key` — The ID of the created item (create only)
- `meta.keys` — The IDs of the updated or deleted items; a batch emits once with every key
- `meta.collection` — The collection name
- `meta.event` — The event name that matched (e.g., `"articles.items.create"`)

**NOT available:**
- ❌ `event` — Use `meta.event`
- ❌ `collection` — Use `meta.collection`
- ❌ `key` / `keys` — Use `meta.key` or `meta.keys`
- ❌ `accountability` — Use `context.accountability`

### `services` Object Members

| Member                              | Purpose                                                |
| ----------------------------------- | ------------------------------------------------------ |
| `services.items(coll, [opts])`      | Nine methods: `readByQuery`, `readOne`, `readMany`, `createOne`, `createMany`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany` |
| `services.collections([opts])`      | Read only: `readAll`, `readOne`                        |
| `services.fields([opts])`           | Read only: `readAll`, `readOne`                        |
| `services.relations([opts])`        | Read only: `readAll`, `readOne`                        |
| `services.files([opts])`            | File metadata only: `readByQuery`, `readOne`           |
| `services.versions([opts])`         | `readAll`, `readOne`, `promote`                        |
| `services.mail()`                   | `send(options)`, `verify()`                            |
| `services.mail(options)`            | Send email directly; returns `{ success, ... }`        |
| `services.custom(name, [opts])`     | An active custom service; `await` it (see [Custom Services](../create-service/SKILL.md)) |
| `services.cron`                     | `trigger(idOrName)`, `list(status?)`, `get(idOrName)`  |
| `services.fetch(url, [init])`       | HTTP to the hosts the Engine's operator allows         |
| `services.env`                      | Only the variables the Engine's operator names (`RUNTIME_ENV_WHITELIST_EXTENSION`, `RUNTIME_ENV_WHITELIST_GLOBAL`, `EXTENSION_PUBLIC_*`, `RUNTIME_PUBLIC_*`); empty by default |

Every signature: [Engine services API](references/engine-services-api.instructions.md).

### Elevated Permissions

By default `services.items` calls in a hook are checked against the **grants of the caller who fired the hook**. Pass `{ elevated: true }` to evaluate them as an administrator while the audit trail (`user_created`/`user_updated` and the activity log) still names the caller. A filter runs before the caller's grant is applied to the payload, so a filter cannot write a column the caller may not.

```js
// Elevated — checked as an administrator, caller still in the audit trail (orders.items.create, action)
const log = services.items('order_status_log', { elevated: true });
await log.createOne({ order_id: meta.key, status: 'pending', note: 'auto-created' });

// Nested custom service with administrator access (strictly the boolean true)
const helper = await services.custom('my_helper', { elevated: true });
```

> **Cron jobs** run as the Engine's system account, which holds the Administrator policy: `{ elevated: true }` is not needed in cron code.

### Engine runtime

What stored code has on the Engine, and what replaces what it lacks:

| Interface taught on a Supabase project | On the Engine | Replacement |
|---|---|---|
| The Supabase service in stored code (`services.supabase`) | Refused permanently: `501 RUNTIME_SUPABASE_UNAVAILABLE` | `services.items(collection)`, with `{ elevated: true }` where the hook or service must act as an administrator |
| SQL functions, remote procedure calls and raw SQL from stored code | No path | `services.items` calls, or a custom service built on them |
| `services.items(c)` methods | Nine: `readByQuery`, `readOne`, `readMany`, `createOne`, `createMany`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany`; `readByQuery` returns the array itself | Read `result`, not `result.data`; read the keys first where a query-wide update or delete was used |
| Query keys | `fields`, `filter`, `sort`, `limit`, `page`, `offset`, `search`; any other key (`deep`, `aggregate`, `groupBy`) is refused. Without `limit` a read returns 25 rows; `limit` is capped at 1000 | Drop the key; set `limit` |
| Filters across relations | One relation deep (`{ "comments.status": { _eq: "published" } }` or `{ comments: { _has: true } }`); a path through two relations, `_some` and `_none` are refused | Read the related collection first |
| Schema services | Read only: `readAll`, `readOne` | Change structure through the Engine's API (see [create-collection](../create-collection/SKILL.md)) |
| `services.files` | Metadata only: `readByQuery`, `readOne` | Upload and download through the application and `/api/files` |
| `services.mail` | Options `to`, `subject`, `html`, `text`, `replyTo`; returns `{ success, ... }` and does not throw when mail cannot be sent | Check `success` |
| `services.env` | Empty unless the Engine's operator names keys (`RUNTIME_ENV_WHITELIST_<SCOPE>`, `RUNTIME_ENV_WHITELIST_GLOBAL`); `NODE_ENV` and `NEXT_PUBLIC_SITE_URL` are not exposed | Ask the operator to name the key; never assume one |
| `services.fetch` | Only hosts in the operator's `EXTENSION_ALLOWED_DOMAINS`; an empty list allows `localhost` only | Ask the operator to allow the host |
| `fetch`, `process`, `require`, `import`, `setTimeout`, `setInterval`, `eval`, `Function` | Do not exist: using one is a `ReferenceError` | `services.fetch`; no timers |
| `Intl`, `URLSearchParams` | Not in the runtime's globals (`context`, `services`, `console`, `JSON`, `Date`, `Math`) | Format numbers by hand; build query strings with `encodeURIComponent` |
| `console` in a custom service body | Not in scope; in hooks, cron jobs and service tests it is | Return what should be recorded |
| `console.table`, `console.trace` | Do not exist; `log`, `info`, `debug`, `warn`, `error` only | `console.log` |
| Update and delete hook payloads | `meta.keys` (array); `meta.key` only on create | Use `meta.keys` |
| Throwing from a filter hook | `new HookError(message, status, code)` is in scope | Unchanged |
| A run's memory | `memory_limit_mb` is stored and shown but not enforced | Keep work small; `timeout_ms` is the only bound |
| Filesystem extensions, `/api/ext/*` endpoints | None | Stored hooks, cron jobs, custom services |

### Correct Code Examples

**Filter hook — validate and transform:**
```js
// payload and meta are available directly
const helper = await services.custom('my_validator');
const check = helper.validatePayload(payload, ['name', 'email']);
if (!check.valid) {
  throw new HookError('Missing: ' + check.missing.join(', '), 422, 'VALIDATION_FAILED');
}
payload.name = payload.name.trim().toUpperCase();
return payload; // return the payload (returning nothing keeps it as it stands)
```

**Action hook — audit logging:**
```js
// In action hooks, all event data is in meta (not direct variables)
const helper = await services.custom('audit_logger');
const audit = helper.buildAuditEntry(
  'create',
  meta.collection,    // NOT collection (undefined)
  meta.key,           // create only; update and delete carry meta.keys
  { payload_keys: Object.keys(meta.payload || {}) }
);
await services.items('audit_logs').createOne(audit);
```

## Performance: Extensions vs API Routes

| Approach              | Request Flow                                 | User Waits For    |
| --------------------- | -------------------------------------------- | ----------------- |
| API Route (❌)        | Request → Engine → Audit → Response          | Operation + Audit |
| Action Extension (✅) | Request → Engine → Response → (after: Audit) | Operation only    |

## Special Fields (Auto-Populated)

Instead of hooks for timestamps/user tracking, use special fields:

| Field Type   | `meta.special` Value | Purpose                |
| ------------ | -------------------- | ---------------------- |
| UUID PK      | `["uuid"]`           | Auto-generate UUID     |
| Created date | `["date-created"]`   | Auto-set on create     |
| Updated date | `["date-updated"]`   | Auto-set on update     |
| Created by   | `["user-created"]`   | Auto-set creating user |
| Updated by   | `["user-updated"]`   | Auto-set updating user |

On an Engine project the Engine sets `user-created`, `user-updated` and `date-updated` on each write. `uuid` and `date-created` are filled by the field's default value, so create those fields with a default (see [create-collection](../create-collection/SKILL.md)).

## Utilities

The Engine's utility routes (`/api/utils/*`: hashing, random strings, manual sorting, import, export, cache) take a signed-in user's access token only; stored code holds no token and cannot call them. See [Engine utilities API](references/engine-utilities-api.instructions.md).

## References

- [Engine hooks guide](references/engine-hooks.instructions.md)
- [Engine services API](references/engine-services-api.instructions.md) — every built-in service and method on the Engine
- [Engine utilities API](references/engine-utilities-api.instructions.md)
<!-- /buildpad-backend -->
