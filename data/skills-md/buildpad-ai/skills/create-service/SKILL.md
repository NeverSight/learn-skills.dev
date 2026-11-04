---
name: create-service
description: Create and manage DaaS custom services for reusable code shared between extensions and cron jobs. Define utility libraries, API wrappers, validators, and formatters that can be injected via `services.custom('name')`. Use when the user needs shared logic across hooks/crons, wants to avoid code duplication, or needs testable service modules.
argument-hint: "[service name] [purpose: helpers|validators|api-wrapper|formatter|custom]"
---

# Create Custom Service

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

Define reusable service modules that can be shared between Runtime Extensions and Cron Jobs. Custom services eliminate code duplication and provide a testable, modular architecture.

## Overview

Custom services are stored in the database (`daas_custom_services`) and compiled at runtime. They are accessible via `services.custom('serviceName')` in both extensions and cron jobs.

**Key properties:**

| Property     | Description                                              |
| ------------ | -------------------------------------------------------- |
| Name         | Unique identifier (`snake_case`, e.g., `data_helpers`). Must start with lowercase letter, only lowercase letters, digits, underscores, hyphens. CamelCase names are **rejected** by the DB constraint. |
| Code         | JS module that returns an object with methods            |
| Status       | `active` / `inactive` / `draft` / `error`                |
| Tests        | Embedded test cases (run in live environment)            |
| Dependencies | Names of other services this depends on                  |
| Timeout      | Max execution time in ms (default 5,000)                 |

## Setup Steps

<!-- buildpad-backend: supabase -->
### 1. Create a Custom Service (Draft First)

Always create services as `draft` initially, add tests, verify, then activate.

```json
{
  "name": "mcp_daas_services",
  "arguments": {
    "action": "create",
    "name": "date_helpers",
    "description": "Date formatting and calculation utilities",
    "code": "return {\n  formatDate(date) {\n    return new Date(date).toISOString().slice(0, 10);\n  },\n  daysAgo(days) {\n    return new Date(Date.now() - days * 86400000).toISOString();\n  },\n  isExpired(dateStr, maxDays) {\n    const date = new Date(dateStr);\n    const diff = Date.now() - date.getTime();\n    return diff > maxDays * 86400000;\n  }\n};",
    "status": "draft",
    "tests": [
      {
        "name": "formatDate returns YYYY-MM-DD",
        "code": "const svc = await api.instance();\nconst result = svc.formatDate('2025-01-15T10:30:00Z');\nassert.equal(result, '2025-01-15');"
      },
      {
        "name": "isExpired returns true for old dates",
        "code": "const svc = await api.instance();\nconst oldDate = new Date(Date.now() - 100 * 86400000).toISOString();\nassert.ok(svc.isExpired(oldDate, 30));"
      }
    ],
    "dependencies": [],
    "timeout_ms": 5000
  }
}
```

### 2. Run Tests

```json
{
  "name": "mcp_daas_services",
  "arguments": {
    "action": "run_tests",
    "id": "<service-id>"
  }
}
```

### 3. Activate When Tests Pass

```json
{
  "name": "mcp_daas_services",
  "arguments": {
    "action": "activate",
    "id": "<service-id>"
  }
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### 1. Create a Custom Service (Draft First)

Always create services as `draft` initially, add tests, verify, then activate. On an Engine project create a service in the Studio's Custom Services module, or through the Engine's REST API from a server-side script or route with an administrator's access token (a user whose role holds `create` on `daas_custom_services` may create one too), or with the Engine's MCP tool `services`, which is listed and served to an administrator only. An omitted `status` is stored as `draft`.

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

```bash
curl -X POST "$ENGINE_URL/api/services" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "date_helpers",
    "description": "Date formatting and calculation utilities",
    "code": "return {\n  formatDate(date) {\n    return new Date(date).toISOString().slice(0, 10);\n  },\n  daysAgo(days) {\n    return new Date(Date.now() - days * 86400000).toISOString();\n  },\n  isExpired(dateStr, maxDays) {\n    const date = new Date(dateStr);\n    const diff = Date.now() - date.getTime();\n    return diff > maxDays * 86400000;\n  }\n};",
    "status": "draft",
    "tests": [
      {
        "name": "formatDate returns YYYY-MM-DD",
        "code": "const svc = await api.instance();\nconst result = svc.formatDate(\"2025-01-15T10:30:00Z\");\nassert.equal(result, \"2025-01-15\");"
      },
      {
        "name": "isExpired returns true for old dates",
        "code": "const svc = await api.instance();\nconst oldDate = new Date(Date.now() - 100 * 86400000).toISOString();\nassert.ok(svc.isExpired(oldDate, 30));"
      }
    ],
    "dependencies": [],
    "timeout_ms": 5000
  }'
```

The answer carries the stored service under `data`. A name that breaks the naming rule, code or a test that does not compile, a missing dependency, or a `timeout_ms` outside 100-30000 is refused with `400` and the server's sentence; a name already taken is refused with `409`. Nothing is stored.

### 2. Run Tests

```bash
curl -X POST "$ENGINE_URL/api/services/<service-id>/tests" -H "Authorization: Bearer $ACCESS_TOKEN"
```

Only an administrator may run tests. Add `?test=<test name>` to run one test. The tests run live, one after another, inside the request, as the calling administrator; a `draft` service can be tested. The answer is `200` whatever the outcome: **`data.status` decides** — `passed` or `failed` — beside `passed`, `failed`, `total`, `duration_ms` and `results` (each with `name`, `status` of `passed`, `failed`, `error` or `timeout`, and `error`).

### 3. Activate When Tests Pass

```bash
curl -X PATCH "$ENGINE_URL/api/services/<service-id>" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "status": "active" }'
```

`services.custom(name)` resolves only an `active` service; any other status answers `Custom service "<name>" not found or inactive`.
<!-- /buildpad-backend -->

## Service Code Structure

Service code is a factory function body that receives `context` as its only parameter.
Common pattern: destructure `context` at the top, then `return { ... }` with methods.

<!-- buildpad-backend: supabase -->
```javascript
// Destructure context to get services, env, etc.
const { services, accountability, env } = context;

return {
  // Optional: called once per instantiation
  async init(ctx) {
    // Setup code here (ctx is the same context object)
  },
  
  // Sync helper methods
  formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
    }).format(amount);
  },
  
  // Async methods that use DaaS services
  async getActiveUsers() {
    const users = await services.items('users');
    const { data } = await users.readByQuery({
      filter: { status: { _eq: 'active' } },
      limit: -1,
    });
    return data;
  },
  
  // Methods that call external APIs
  async fetchExternalData(endpoint) {
    const response = await services.fetch(`https://api.example.com/${endpoint}`);
    return response.json();
  }
};
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```javascript
// Destructure context to get services, env, etc.
const { services, accountability, env } = context;

return {
  // Optional: awaited before a caller gets the object
  async init(ctx) {
    // Setup code here (ctx is the same context object)
  },
  
  // Sync helper methods. The Engine's runtime has no Intl: format by hand.
  formatCurrency(amount, currency = 'USD') {
    const [whole, cents] = Math.abs(amount).toFixed(2).split('.');
    const grouped = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return `${amount < 0 ? '-' : ''}${currency} ${grouped}.${cents}`;
  },
  
  // Async methods that use the Engine's services
  async getActiveUsers() {
    const users = services.items('users');
    // readByQuery returns the array itself; limit is capped at 1000
    return users.readByQuery({
      filter: { status: { _eq: 'active' } },
      limit: 1000,
    });
  },
  
  // Methods that call external APIs (the host must be allowed by the Engine's operator)
  async fetchExternalData(endpoint) {
    const response = await services.fetch(`https://api.example.com/${endpoint}`);
    return response.json();
  }
};
```

`console` is not in scope in a service body on an Engine project: return what should be recorded, or let the caller log it.
<!-- /buildpad-backend -->

## Available Context

Service code receives **one parameter**: `context`. Destructure it to access:

```javascript
const { services, accountability, env } = context;
```

<!-- buildpad-backend: supabase -->
| `context` Property       | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| `context.services.items(coll)` | ItemsService factory (17 methods)                |
| `context.services.collections()` | CollectionsService factory                     |
| `context.services.fields()` | FieldsService factory                               |
| `context.services.files()` | FilesService factory                                 |
| `context.services.versions()` | VersionService factory                            |
| `context.services.relations()` | RelationsService factory                         |
| `context.services.mail()` | MailService factory (`send()`, `verify()`)            |
| `context.services.custom(name)` | Get another custom service                      |
| `context.services.fetch(url)` | Safe HTTP fetch (domain-restricted)                |
| `context.services.supabase` | Raw Supabase client (service role, bypasses RLS)    |
| `context.accountability` | Current user context (`{ user, role, admin, app }`)    |
| `context.env`            | Whitelisted environment variables (`NODE_ENV`, `NEXT_PUBLIC_SITE_URL`) |

> See [Services API reference](../hooks-extensions/references/services-api.instructions.md) for complete method signatures of all services.

> **Important:** `services`, `accountability`, and `env` are NOT top-level variables.
> You must access them via `context.*` or destructure `const { services } = context;`.

> **Background user context:** When a custom service is invoked without a real user (e.g., from a cron job or another service), `context.accountability.user` is the System Service UUID (`00000000-0000-0000-0000-000000000000`). Audit fields (`user-created`, `user-updated`) will reflect this system user. `readByQuery()` returns `Item[]` directly — do not destructure with `const { data } = ...`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
| `context` Property       | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| `context.services.items(coll, opts?)` | Nine methods: `readByQuery`, `readOne`, `readMany`, `createOne`, `createMany`, `updateOne`, `updateMany`, `deleteOne`, `deleteMany` |
| `context.services.collections()` | Read only: `readAll`, `readOne`                  |
| `context.services.fields()` | Read only: `readAll`, `readOne`                       |
| `context.services.files()` | File metadata only: `readByQuery`, `readOne`           |
| `context.services.versions()` | `readAll`, `readOne`, `promote`                     |
| `context.services.relations()` | Read only: `readAll`, `readOne`                    |
| `context.services.mail()` | `send(options)` and `verify()`; `services.mail(options)` sends directly and returns `{ success, ... }` |
| `context.services.custom(name, opts?)` | Another active custom service; `await` it   |
| `context.services.fetch(url, init?)` | HTTP to the hosts the Engine's operator allows |
| `context.services.cron` | `trigger`, `list`, `get` for cron jobs                    |
| `context.accountability` | The caller: `{ user, admin, role, app }`; `user` is always the real caller |
| `context.env`            | Only the variables the Engine's operator names; empty by default (the same object as `context.services.env`) |

There is no Supabase service, no SQL and no `console` in a custom service on an Engine project.

On an Engine project stored code (hooks, cron jobs, custom services) runs in the Engine's runtime, which provides only what the Engine runtime table of the [hooks-extensions skill](../hooks-extensions/SKILL.md) lists; for each interface it lacks, the table says what replaces it.

> **Important:** `services`, `accountability`, and `env` are NOT top-level variables.
> You must access them via `context.*` or destructure `const { services } = context;`.

> **Background user context:** When a custom service is called from a cron job, `context.accountability.user` is the Engine's system account (`00000000-0000-0000-0000-000000000000`), which holds the Administrator policy. From a hook it is the user whose request fired the hook. `services.custom(name, { elevated: true })` makes the service's calls pass every permission check while every audit row still names the caller. `readByQuery()` returns `Item[]` directly — do not destructure with `const { data } = ...`.
<!-- /buildpad-backend -->

## Using Services in Extensions

**Filter hook** (payload and meta available directly):
```javascript
// In a filter hook:
const helpers = await services.custom('date_helpers');
const validator = await services.custom('order_validator');

// Use the service methods — payload is a direct variable
const formatted = helpers.formatDate(payload.created_at);
const isValid = await validator.validateOrder(payload);

if (!isValid) {
  throw new Error('Invalid order data');
}

return payload; // MUST return payload in filter hooks
```

**Action hook** (event data is in `meta`, not direct variables):
```javascript
// In an action hook:
const logger = await services.custom('audit_logger');

// Access event data via meta — NOT direct variables
const entry = logger.buildAuditEntry(
  'create',
  meta.collection,  // NOT collection (undefined)
  meta.key,         // NOT key (undefined)
  { payload: meta.payload }
);
const items = await services.items('audit_logs');
await items.createOne(entry);
```

## Using Services in Cron Jobs

<!-- buildpad-backend: supabase -->
```javascript
// In cron job code — only services and context available
const syncService = await services.custom('external_sync');
const dateHelpers = await services.custom('date_helpers');

const cutoff = dateHelpers.daysAgo(7);
const result = await syncService.syncRecordsSince(cutoff);

console.log(`Synced ${result.count} records`);

// Can also use services.supabase directly
const { data } = await services.supabase.from('my_table').select('*');
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```javascript
// In cron job code — only services and context available
const syncService = await services.custom('external_sync');
const dateHelpers = await services.custom('date_helpers');

const cutoff = dateHelpers.daysAgo(7);
const result = await syncService.syncRecordsSince(cutoff);

console.log(`Synced ${result.count} records`);

// Read data through services.items: the Engine has no Supabase service
const rows = await services.items('my_table').readByQuery({ limit: 100 });
```
<!-- /buildpad-backend -->

> **Note:** In cron jobs, only `services`, `context`, `console`, `JSON`, `Date`, and `Math` are available. Variables like `payload`, `meta`, `event`, and `accountability` are **undefined**.

## Test Structure

Tests run in the live environment (no mocking). Test function signature: `(api, assert, context, console)`.

| Variable | Description |
| -------- | ----------- |
| `api.instance()` | Get a fresh instance of the service |
| `api.call(method, ...args)` | Call a service method directly |
| `api.cleanup(fn)` | Register async cleanup function (runs after all tests) |
| `api.services` | Direct access to services object |
| `assert.equal(a, b)` | Strict equality |
| `assert.notEqual(a, b)` | Not equal |
| `assert.deepEqual(a, b)` | Deep object equality |
| `assert.ok(value)` | Truthy assertion |
| `assert.truthy(value)` / `assert.falsy(value)` | Truthiness checks |
| `assert.isString(v)` / `assert.isNumber(v)` / `assert.isArray(v)` / `assert.isObject(v)` | Type checks |
| `assert.hasProperty(obj, key)` | Property existence |
| `assert.includes(arr, item)` | Array contains |
| `assert.hasLength(arr, n)` | Array length |
| `assert.throws(fn, expectedError?)` | Expect sync throw |
| `assert.rejects(promise, expectedError?)` | Expect async rejection |
| `context` | Same `{ services, accountability, env }` as service code |
| `console.log()` | Output captured in results |

### Test Example

```json
{
  "name": "validateOrder rejects empty items",
  "code": "const svc = await api.instance();\nconst result = await svc.validateOrder({ items: [] });\nassert.equal(result.valid, false);\nassert.ok(result.errors.includes('Order must have items'));"
}
```

## Dependencies

Services can depend on other services:

```json
{
  "name": "order_processor",
  "dependencies": ["date_helpers", "email_service"],
  "code": "const { services } = context;\nconst dateHelpers = await services.custom('date_helpers');\nconst emailService = await services.custom('email_service');\n\nreturn {\n  async processOrder(order) {\n    const due = dateHelpers.daysFromNow(30);\n    await emailService.sendOrderConfirmation(order, due);\n    return { processed: true, dueDate: due };\n  }\n};"
}
```

- Dependencies are loaded before the dependent service
- Circular dependencies are rejected
- Deleting a service fails if others depend on it

<!-- buildpad-backend: supabase -->
## MCP Actions

| Action        | Description                          |
| ------------- | ------------------------------------ |
| `list`        | List all services (filter by status) |
| `read`        | Get service by ID                    |
| `create`      | Create new service                   |
| `update`      | Update service                       |
| `delete`      | Delete service (if no dependents)    |
| `run_tests`   | Run all embedded tests               |
| `run_test`    | Run single test by name              |
| `activate`    | Set status to active                 |
| `deactivate`  | Set status to inactive               |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## REST Routes

On an Engine project custom services are managed in the Studio's Custom Services module or through these routes, decided by the caller's grant on `daas_custom_services` (an administrator passes every check), or through the Engine's MCP tool `services` (administrators only).

| Method   | Path                      | Needs                     | Description                          |
| -------- | ------------------------- | ------------------------- | ------------------------------------ |
| `GET`    | `/api/services`           | `read`                    | List services (`search`, `status`)   |
| `POST`   | `/api/services`           | `create`                  | Create a service                     |
| `GET`    | `/api/services/:id`       | `read`                    | Get a service                        |
| `PATCH`  | `/api/services/:id`       | `update`                  | Update the fields sent; `status` activates or deactivates |
| `DELETE` | `/api/services/:id`       | `delete`                  | Delete a service; `409` while others depend on it |
| `POST`   | `/api/services/:id/tests` | administrator only        | Run all tests, or one with `?test=<name>` |
<!-- /buildpad-backend -->

## Common Patterns

### API Wrapper

This env var → auth header → `services.fetch` pattern applies to most connected third-party providers, not just Stripe — but not all: a provider that ships an official SDK (e.g. Chocolate Factory) can't be called this way, since custom services run sandboxed JS with no `import`/`require` support — that provider is called from a server-side Next.js API route instead. Before writing the call: confirm the provider is connected and get its exact `envVarNames`, `apiBaseUrl`, and `authHeaderStyle` from `get_project_detail`'s `connectors[]` — do not assume an env var name. Note `apiBaseUrl` may be absent for a self-hosted provider (e.g. Chocolate Factory); in that case the base URL is itself one of the connector's env vars, per that provider's `references/<key>.instructions.md`. Always check `references/<provider-key>.instructions.md` if one exists (e.g. `references/stripe.instructions.md`) first — it covers both the request/response shape *and* which execution context (custom service vs. API route) that provider actually needs.

<!-- buildpad-backend: supabase -->
**Local dev:** `connectors[]` entries also include `envVars` (env var name → actual decrypted value) alongside `envVarNames`. These are real secrets, not just names — use them to populate `.env.local` when a feature that reads a connector's env var(s) needs to run locally (`pnpm dev`), then restart the dev server (Next.js only reads `.env.local` at process start). Don't print these values to logs, commit them, or write them anywhere other than `.env.local`.

**Deploying:** connecting a provider on the Connectors page only stores its credential in Buildpad — it does **not** push anything to the deployed app's Amplify environment. The first time a feature actually reads a connector's env var(s), also push that same `envVars` map with `amplify_set_env_vars` (see the `amplify-env-vars` skill) and follow with `amplify_redeploy`, or the deployed app will have the code but no value to read — it'll work locally (from `.env.local`) and silently fail once deployed.

```javascript
const { services, env } = context;

return {
  baseUrl: 'https://api.stripe.com/v1',
  
  async createCustomer(email, name) {
    const response = await services.fetch(`${this.baseUrl}/customers`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ email, name }),
    });
    return response.json();
  },
  
  async getCustomer(customerId) {
    const response = await services.fetch(`${this.baseUrl}/customers/${customerId}`, {
      headers: { 'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}` },
    });
    return response.json();
  }
};
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
**The key must reach the Engine, not only the application.** On an Engine project a custom service runs inside the Engine, so it reads `env.<KEY>` from the Engine's environment, never from the application's `.env.local` or its Amplify environment. `services.env` is empty unless the Engine's operator names the key (for example `RUNTIME_ENV_WHITELIST_CUSTOM_SERVICE=STRIPE_SECRET_KEY`, with `STRIPE_SECRET_KEY` set in the Engine's environment). `services.fetch` reaches a host only when the operator lists it in `EXTENSION_ALLOWED_DOMAINS` (for Stripe, `api.stripe.com`). Ask the operator for both before you write the service, and never assume either. A provider key the application itself uses (in a server-side API route) still goes to `.env.local` for local dev and to Amplify with `amplify_set_env_vars` and `amplify_redeploy` (see the `amplify-env-vars` skill) for the deployed app. These are real secrets: don't print them to logs, commit them, or write them anywhere else.

The runtime has no `URLSearchParams`: build a form-encoded body by hand.

```javascript
const { services, env } = context;

const form = (fields) =>
  Object.entries(fields)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&');

return {
  baseUrl: 'https://api.stripe.com/v1',
  
  async createCustomer(email, name) {
    const response = await services.fetch(`${this.baseUrl}/customers`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: form({ email, name }),
    });
    return response.json();
  },
  
  async getCustomer(customerId) {
    const response = await services.fetch(`${this.baseUrl}/customers/${customerId}`, {
      headers: { 'Authorization': `Bearer ${env.STRIPE_SECRET_KEY}` },
    });
    return response.json();
  }
};
```
<!-- /buildpad-backend -->

### Validator

<!-- buildpad-backend: supabase -->
```javascript
const { services } = context;

return {
  async validateArticle(article) {
    const errors = [];
    
    if (!article.title || article.title.length < 3) {
      errors.push('Title must be at least 3 characters');
    }
    
    if (!article.content || article.content.length < 100) {
      errors.push('Content must be at least 100 characters');
    }
    
    if (article.category_id) {
      const categories = await services.items('categories');
      const category = await categories.readOne(article.category_id);
      if (!category) {
        errors.push('Invalid category');
      }
    }
    
    return { valid: errors.length === 0, errors };
  }
};
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```javascript
const { services } = context;

return {
  async validateArticle(article) {
    const errors = [];
    
    if (!article.title || article.title.length < 3) {
      errors.push('Title must be at least 3 characters');
    }
    
    if (!article.content || article.content.length < 100) {
      errors.push('Content must be at least 100 characters');
    }
    
    if (article.category_id) {
      // On the Engine readOne throws NOT_FOUND for a missing id; it never answers null
      try {
        await services.items('categories').readOne(article.category_id);
      } catch (e) {
        if (e.code !== 'NOT_FOUND') throw e;
        errors.push('Invalid category');
      }
    }
    
    return { valid: errors.length === 0, errors };
  }
};
```
<!-- /buildpad-backend -->

### Data Transformer

```javascript
// No services needed — pure helpers don't need context
return {
  toPublicFormat(user) {
    return {
      id: user.id,
      displayName: `${user.first_name} ${user.last_name}`,
      avatar: user.avatar_url || '/default-avatar.png',
      joinedAt: new Date(user.created_at).toLocaleDateString(),
    };
  },
  
  toCSVRow(record, columns) {
    return columns.map(col => {
      const val = record[col] ?? '';
      return typeof val === 'string' && val.includes(',') 
        ? `"${val}"` 
        : String(val);
    }).join(',');
  }
};
```

## Best Practices

1. **Start as draft** — Test before activating
2. **Add comprehensive tests** — Cover edge cases
3. **Keep services focused** — Single responsibility
4. **Use `snake_case` names** — e.g., `date_helpers`, `audit_logger`, `email_service`. CamelCase names are rejected.
5. **Document methods** — Use comments in code
6. **Handle errors gracefully** — Throw descriptive errors
7. **Avoid side effects in helpers** — Pure functions when possible
8. **Use dependencies** — Don't duplicate code across services

## References

- [Custom services guide](references/custom-services.instructions.md)
<!-- buildpad-backend: supabase -->
- [Services API reference](../hooks-extensions/references/services-api.instructions.md) — complete method signatures for all built-in services
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- [hooks-extensions skill](../hooks-extensions/SKILL.md) — the Engine's runtime: every built-in service, its methods, and what the runtime lacks
<!-- /buildpad-backend -->
