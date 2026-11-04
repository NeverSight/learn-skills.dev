---
name: daas-platform
description: Core DaaS architecture, REST API, authentication, files, MCP tools, environment configuration, and Next.js App Router patterns, for Engine projects and Supabase projects. Automatically loaded as background context for all DaaS development tasks.
user-invokable: false
---

# DaaS Platform Reference

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
## Two-Tier Architecture

```
Frontend App  →  DaaS Backend (DaaS)  →  Supabase (PostgreSQL)
(Next.js)        (DaaS-compatible REST API)           (Database)
```

- Frontend connects to DaaS backend for ALL data operations
- Frontend uses Supabase ONLY for authentication (via proxy routes)
- Never query Supabase directly from frontend code

## Technology Stack

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript 5.x
- **UI**: Mantine v8 + Buildpad components (Copy & Own)
- **Backend**: DaaS (DaaS-compatible REST API)
- **Auth**: Supabase Auth via server-side proxy routes
- **Testing**: Playwright (E2E) + Vitest (unit)
- **Design**: Token-based theming with CSS custom properties (`--ds-*`)

## Environment Variables (`.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_BUILDPAD_DAAS_URL=http://localhost:3000
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Architecture

```
Frontend App  →  Buildpad Engine  →  the Engine's own database
(Next.js)        (DaaS-compatible REST API, sign-in, files)
```

- Frontend connects to the Engine for ALL data operations, sign-in and files
- The Engine has its own database: there is no Supabase project behind it, and no frontend code queries a database directly
- The frontend keeps the Supabase client for sign-in only; it is pointed at the Engine

## Technology Stack

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript 5.x
- **UI**: Mantine v8 + Buildpad components (Copy & Own)
- **Backend**: the Buildpad Engine (DaaS-compatible REST API, with its own database and file storage)
- **Auth**: the Engine's password sign-in, through the Supabase client and server-side proxy routes
- **Testing**: Playwright (E2E) + Vitest (unit)
- **Design**: Token-based theming with CSS custom properties (`--ds-*`)

## Environment Variables (`.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>
NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>
NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key
NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>
```

On an Engine project the environment is: `NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>`, `NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>`, `NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key` (a fixed value that is not a secret; the Engine does not read it, the Supabase client needs one), and `NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>`. There is no service-role key on an Engine project: add none.

On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

**How a request is authenticated.** On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

On an Engine project the Supabase client is kept for sign-in only. Password sign-in, session refresh, reading the signed-in user and sign-out work through it, and its default sign-out ends the user's sessions on every device. An account that holds no role in the project's tenant is refused at password sign-in. XAppHub sign-in also works through it while the project's XAppHub connector is connected: the application's server gives the ID token from XAppHub to `signInWithIdToken` with the provider `my-apps`, and ends the session of an account that holds no role yet (the `add-external-oauth` skill). Not available on an Engine project: sign-up; OAuth sign-in with any provider other than XAppHub; magic link and one-time code; password recovery; changing a password, an email or a profile through the Supabase client; the Supabase client's code exchange; and the Supabase administration API. The Platform's password-less handoff opens the Studio; it is not a way for an application to sign a user in.

The sign-in route, the tenant header, the error codes and the multi-factor routes are in the [DaaS API reference](references/daas-api.instructions.md).
<!-- /buildpad-backend -->

Always read `.env.local` to get actual configured values before making API calls.

## REST API Pattern

```
GET    /api/items/:collection          # List items
POST   /api/items/:collection          # Create item
GET    /api/items/:collection/:id      # Get item
PATCH  /api/items/:collection/:id      # Update item
DELETE /api/items/:collection/:id      # Delete item
GET    /api/fields/:collection         # Get field schema
GET    /api/relations                  # Get relations
```

<!-- buildpad-backend: supabase -->
### Query Parameters

- `fields`: `*` or comma-separated field names
- `filter`: `{ "status": { "_eq": "published" } }`
- `sort`: Field name, `-` prefix for descending
- `limit`, `offset`: Pagination
- `aggregate`: Aggregate functions — `{ "count": ["id"], "sum": ["amount"] }` or bracket notation `aggregate[count]=id`
- `groupBy`: Group aggregate results — comma-separated field names

### Aggregate Functions

Perform calculations on collection data without fetching individual items:

```
GET /api/items/:collection?aggregate[count]=id&groupBy=status
GET /api/items/:collection?aggregate={"count":["*"],"sum":["amount"]}&filter={"status":{"_eq":"completed"}}
```

**Supported operations:** `count`, `countDistinct`, `countAll`, `sum`, `sumDistinct`, `avg`, `avgDistinct`, `min`, `max`

**Response format** (nested, permission-aware):

```json
{
  "data": [
    { "status": "completed", "count": { "id": 42 }, "sum": { "amount": 12500 } }
  ]
}
```

Aggregate queries respect collection-level read permissions and item-level RLS filters.

### Filter Operators

`_eq`, `_neq`, `_lt`, `_lte`, `_gt`, `_gte`, `_in`, `_nin`, `_contains`, `_icontains`, `_starts_with`, `_ends_with`, `_null`, `_nnull`, `_and`, `_or`

## DaaS MCP Tools

| Tool                   | Purpose                                               |
| ---------------------- | ----------------------------------------------------- |
| `mcp_daas_items`       | CRUD + aggregate on collection items                  |
| `mcp_daas_schema`      | Read collection/field schema (no `action` param!)     |
| `mcp_daas_collections` | Manage tables (admin)                                 |
| `mcp_daas_fields`      | Manage columns — `data` accepts object OR array       |
| `mcp_daas_relations`   | Foreign key relationships                             |
| `mcp_daas_files`       | File management                                       |
| `mcp_daas_users`       | User profiles                                         |
| `mcp_daas_roles`       | Role definitions (CRUD — create/read/update/delete)   |
| `mcp_daas_permissions` | Permission rules (CRUD — create/read/update/delete)   |
| `mcp_daas_extensions`  | Runtime hooks (admin)                                 |
| `mcp_daas_cron`        | Scheduled background jobs (admin)                     |
| `mcp_daas_services`    | Reusable custom service modules shared between extensions and cron jobs (admin) |
| `mcp_daas_scope`       | Hierarchical scope management — types, items, collection configs, scoped role assignments (admin) |

### MCP Action Quick Reference

**`mcp_daas_services`** — Custom Services:

| Action       | Key Parameters                        | Purpose                                 |
| ------------ | ------------------------------------- | --------------------------------------- |
| `list`       | `status?`                             | List all services                       |
| `read`       | `id`                                  | Read service details                    |
| `create`     | `name`, `code`, `tests[]?`, `status?` | Create a service (`snake_case` names!)  |
| `update`     | `id`, `code?`, `tests[]?`, `status?`  | Update service (auto-increments version)|
| `delete`     | `id`                                  | Delete service (fails if dependents)    |
| `run_tests`  | `id`                                  | Run all built-in tests                  |
| `run_test`   | `id`, `test`                          | Run a single test by name               |
| `activate`   | `id`                                  | Set status to active                    |
| `deactivate` | `id`                                  | Set status to inactive                  |

**`mcp_daas_cron`** — Cron Jobs:

| Action       | Key Parameters                          | Purpose                        |
| ------------ | --------------------------------------- | ------------------------------ |
| `list`       | —                                       | List all cron jobs             |
| `read`       | `id`                                    | Read job details               |
| `create`     | `name`, `code`, `schedule`, `status?`   | Create a cron job              |
| `update`     | `id`, `code?`, `schedule?`, `status?`   | Update a cron job              |
| `delete`     | `id`                                    | Delete a cron job              |
| `run_now`    | `id`                                    | Manually trigger immediately   |
| `activate`   | `id`                                    | Set status to active           |
| `deactivate` | `id`                                    | Set status to inactive         |
| `history`    | `id`, `limit?`                          | View run history with logs     |
| `clone`      | `id`, `name?`                           | Clone a cron job               |

**`mcp_daas_extensions`** — Runtime Extensions:

| Action       | Key Parameters                             | Purpose                    |
| ------------ | ------------------------------------------ | -------------------------- |
| `list`       | `event?`, `status?`, `type?`               | List all extensions        |
| `read`       | `id`                                       | Read extension details     |
| `create`     | `name`, `event`, `type`, `code`, `status?` | Create an extension        |
| `update`     | `id`, `code?`, `name?`, `status?`          | Update an extension        |
| `delete`     | `id`                                       | Delete an extension        |
| `activate`   | `id`                                       | Set status to active       |
| `deactivate` | `id`                                       | Set status to inactive     |
| `clone`      | `id`, `name?`                              | Clone an extension         |

> **All MCP tools** use top-level parameters in `arguments` — do NOT wrap in a `data` object.
>
> **Delete restriction (expected, not a bug):** The `delete` action on most tools is blocked by default — this is an intentional safety gate, not an error condition to work around. The platform setting `mcp_allow_deletes` (env: `MCP_ALLOW_DELETES`) must be `true` for delete to work. RBAC tools (`roles`, `policies`, `permissions`, `access`) are exempt from this restriction.
>
> If a delete call errors with `"Delete operations are disabled"`, **do not** retry, switch tools, use raw SQL, or attempt any other workaround. Tell the user this is expected and that they need to enable it in the DaaS Admin dashboard under Settings → AI (`mcp_allow_deletes`), then stop.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Query Parameters

- `fields`: `*` or comma-separated field names; dot notation (`author.name`) expands a relation
- `filter`: `{ "status": { "_eq": "published" } }`
- `sort`: Field name, `-` prefix for descending
- `limit`, `offset`, `page`: Pagination. `limit` defaults to 25; on an Engine project it is capped at 1000, and a larger value is served as 1000
- `search`: Full-text search
- `aggregate`: Aggregate functions — `{ "count": ["id"], "sum": ["amount"] }` or bracket notation `aggregate[count]=id`
- `groupBy`: Group aggregate results — comma-separated field names

On an Engine project the query parameters `deep`, `meta` and `version` are ignored: the Engine answers as if they were not sent. Filter on a related field inside `filter` instead of `deep`, read the counts from the `meta` of a list answer (`total_count`, `filter_count`, `total`), and read a content version through `/api/versions` instead of `version`.

### Aggregate Functions

Perform calculations on collection data without fetching individual items:

```
GET /api/items/:collection?aggregate[count]=id&groupBy=status
GET /api/items/:collection?aggregate={"count":["*"],"sum":["amount"]}&filter={"status":{"_eq":"completed"}}
```

**Supported operations:** `count`, `countDistinct`, `countAll`, `sum`, `sumDistinct`, `avg`, `avgDistinct`, `min`, `max`

**Response format** (nested, permission-aware):

```json
{
  "data": [
    { "status": "completed", "count": { "id": 42 }, "sum": { "amount": 12500 } }
  ]
}
```

Aggregate queries respect the caller's read permission on the collection, including the item filter of that permission.

### Filter Operators

`_eq`, `_neq`, `_lt`, `_lte`, `_gt`, `_gte`, `_in`, `_nin`, `_contains`, `_icontains`, `_starts_with`, `_ends_with`, `_null`, `_nnull`, `_and`, `_or`

The Engine also accepts `_ncontains`, `_nicontains`, `_istarts_with`, `_nstarts_with`, `_nistarts_with`, `_iends_with`, `_nends_with`, `_niends_with`, `_between`, `_nbetween`, `_empty`, `_nempty` and `_regex`.

## DaaS MCP Tools

On an Engine project the MCP server is the Engine's own, at `<Engine_URL>/api/mcp`. It serves these tools:

| Tool                     | Purpose                                                                 |
| ------------------------ | ----------------------------------------------------------------------- |
| `mcp_daas_system-prompt` | Operating context for the assistant — read it before the first tool call |
| `mcp_daas_items`         | CRUD + aggregate on collection items (refuses the Engine's own tables)  |
| `mcp_daas_schema`        | Read collection/field schema (no `action` param!)                       |
| `mcp_daas_collections`   | Manage collections (admin)                                              |
| `mcp_daas_fields`        | Manage fields (admin) — keeps name, type and `meta`, not the `schema` block |
| `mcp_daas_relations`     | Foreign key relationships (admin)                                       |
| `mcp_daas_files`         | File metadata: read, edit, delete, import from a URL                    |
| `mcp_daas_folders`       | Folders                                                                 |
| `mcp_daas_users`         | User profiles                                                           |
| `mcp_daas_roles`         | Role definitions (CRUD — create/read/update/delete)                     |
| `mcp_daas_policies`      | Policies (CRUD — create/read/update/delete)                             |
| `mcp_daas_permissions`   | Permission rules (CRUD — create/read/update/delete)                     |
| `mcp_daas_access`        | Attach a policy to a role or a user, read or revoke the attachment (admin) |
| `mcp_daas_scope`         | Assign a role to a user at a scope (`action: "assign_user_role"`), or register a collection as tenanted (`action: "create_config"`) (admin) |

The Engine also serves one tool per operation, for clients that already call them: `daas_read_items`, `daas_create_item`, `daas_update_item`, `daas_delete_item`, `daas_list_collections`, `daas_get_schema`, `daas_create_collection`, `daas_list_files`, `daas_list_workflows` and `daas_trigger_transition`. Prefer the tools in the table.

The `items` tool refuses the Engine's own tables `daas_users`, `daas_roles`, `daas_policies`, `daas_permissions`, `daas_access`, `daas_activity`, `daas_sessions` and `daas_settings`: use the dedicated tool, or the REST API for the activity (`GET /api/activity`).

On an Engine project collections, fields, relations, roles, policies and permissions are created through the Engine's API (`/api/collections`, `/api/fields/:collection`, `/api/relations`, `/api/roles`, `/api/policies`, `/api/access`, `/api/permissions`) or its MCP tools `collections`, `fields`, `relations`, `roles`, `policies`, `access` and `permissions`. Access is roles, policies and permissions: a permission belongs to a policy, and a policy is attached to a role or a user. The MCP `collections` and `fields` tools keep a field's name, type and `meta` but not its `schema` block (default, not-null, length): set those through `POST /api/fields/:collection` with an administrator's session.

### Stored code and settings on the Engine's MCP server

On an Engine project the MCP server serves the tools `cron`, `services`, `extensions`, `cors-settings`, `smtp-settings` and `module_access_keys` to an administrator only: they are listed and served when the project's MCP configuration carries an administrator's token, and a worker's token sees none of them. Each takes an `action` argument, and a change takes effect as the REST write of the same body does. A `delete` is refused while the project's MCP deletes are off. If `tools/list` does not list them, the project's Engine is older than 0.1.0-dev.4: use the REST routes in the table. There is still no MCP tool for the application log or for a file's content.

| Task                  | MCP tool (administrators only)                                                                 | Without the tool                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Cron jobs             | `cron`: `list`, `read`, `create`, `update`, `delete`, `activate`, `deactivate`, `clone`, `run_now`, `history` | The Studio's Cron module, or `POST <Engine_URL>/api/cron` with an administrator's session (`GET`/`PATCH`/`DELETE /api/cron/:id`, `POST /api/cron/:id/run`, `POST /api/cron/:id/clone`, `GET /api/cron/:id/history`). See [create-cron](../create-cron/SKILL.md) |
| Custom services       | `services`: `list`, `read`, `create`, `update`, `delete`, `run_tests`, `activate`, `deactivate` | The Studio, or `POST <Engine_URL>/api/services` with an administrator's session (`GET`/`PATCH`/`DELETE /api/services/:id`, tests through `POST /api/services/:id/tests`). See [create-service](../create-service/SKILL.md) |
| Hooks                 | `extensions`: `list`, `read`, `create`, `update`, `delete`, `activate`, `deactivate`, `clone` | The Studio, or `POST <Engine_URL>/api/extensions` with an administrator's session (`GET`/`PATCH`/`DELETE /api/extensions/:id`, `POST /api/extensions/:id/activate`, `/deactivate`, `/clone`). See [hooks-extensions](../hooks-extensions/SKILL.md) |
| Module access keys    | `module_access_keys`: `create`, `read`, `update`, `delete`                                     | The `items` tool on the collection `daas_module_access_keys` (the `grant-module-access` skill)              |
| Cross-origin settings | `cors-settings` exists: change nothing through it                                              | Change nothing: see the cross-origin rule below                                                            |
| Mail settings         | `smtp-settings`: `get`, `update`, `test`                                                       | `GET`/`PATCH <Engine_URL>/api/settings/smtp` with an administrator's session                               |

On an Engine project an active cron job fires at its scheduled time. The `cron` tool's `run_now`, or `POST /api/cron/:id/run`, runs a job by hand at any time.

> **All MCP tools** take their parameters at the top level of `arguments` (`action`, `collection`, `keys`, `query`, `data`) — do NOT wrap them in a `data` object. `data` holds only the field values of a create or an update.
>
> **Delete restriction (expected, not a bug):** The `delete` action is blocked while the project setting `mcp_allow_deletes` is off — this is an intentional safety gate, not an error condition to work around. The RBAC tools (`roles`, `policies`, `permissions`, `access`) are exempt from this restriction.
>
> If a delete call errors with `"Delete operations are disabled in project settings (mcp_allow_deletes)."`, **do not** retry, switch tools, call the REST API, or attempt any other workaround. Tell the user this is expected and that an administrator needs to turn on `mcp_allow_deletes` in the Studio's settings, then stop.
>
> The token in the project's MCP configuration is accepted only on `/api/mcp`. Never send it to the data API.
<!-- /buildpad-backend -->

### MCP Pitfalls

<!-- buildpad-backend: supabase -->
- `schema` tool has NO `action` parameter — just use `keys`
- `permissions`, `roles`, and `policies` all support full CRUD via their own dedicated MCP tools — do NOT use the `items` tool for these collections
- For `permissions` create: the `data.action` field is the **permission action** (`"create"`/`"read"`/`"update"`/`"delete"`/`"share"`), which is different from the top-level `action` parameter (`"create"`) — pass them both explicitly
- `fields.delete` uses `fields: []` (array), not `field` (string)
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- `schema` tool has NO `action` parameter — just use `keys`
- `permissions`, `roles`, and `policies` all support full CRUD via their own dedicated MCP tools, and `access` attaches a policy to a role or a user — do NOT use the `items` tool for these collections (it refuses them)
- For `permissions` create: the `data.action` field is the **permission action** (`"create"`/`"read"`/`"update"`/`"delete"`/`"share"`), which is different from the top-level `action` parameter (`"create"`) — pass them both explicitly
- `fields` delete takes `collection` and `keys: [...]` (the names of the fields to drop), not `field` (string)
<!-- /buildpad-backend -->

### Schema Verification Rule (CRITICAL)

<!-- buildpad-backend: supabase -->
**Always verify field names against the actual DaaS schema before writing queries, sort parameters, or filter expressions.** Do NOT assume field names — they may differ from common conventions (e.g., `created_at` vs `date_created`). Using a non-existent field in `sort`, `fields`, or `filter` causes the DaaS backend to return a **500 error** with no helpful message.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
**Always verify field names against the actual schema before writing queries, sort parameters, or filter expressions.** Do NOT assume field names — they may differ from common conventions (e.g., `created_at` vs `date_created`). On an Engine project a `sort`, `fields`, `filter`, `groupBy` or `aggregate` that names a field the collection does not have is refused with **400** and the code `INVALID_QUERY`, and the message names the field.
<!-- /buildpad-backend -->

Before writing any API route or page that queries a collection:

1. Use `mcp_daas_schema` (with `keys: ["collection_name"]`) or `mcp_daas_fields` to get the actual field names
2. Use only the field names returned by the schema in `sort`, `fields`, and `filter` parameters
3. Pay special attention to audit/timestamp columns — names vary between DaaS instances (e.g., `created_at` vs `date_created` vs `date_created`)

## Backend-First Rule

**Before implementing ANY server-side feature**, check the [Built-in DaaS Features reference](references/builtin-features.instructions.md). If DaaS provides it natively, use it — do NOT rebuild it in Next.js. This is the most common source of agent errors: building custom implementations of features that DaaS already provides.

<!-- buildpad-backend: supabase -->
| Pattern                        | DaaS Feature                                        | DO NOT Build                                         |
| ------------------------------ | --------------------------------------------------- | ---------------------------------------------------- |
| State machine / approvals      | DaaS Workflows (`create-workflow` skill)             | Custom status fields, manual state logic             |
| Audit / change tracking        | **Automatic** — `daas_activity` + `GET /api/activity`| Custom audit tables, logging hooks                   |
| Validation before save         | Runtime Extensions (filter hooks)                    | Next.js API middleware validation                    |
| Side effects after save        | Runtime Extensions (action hooks)                    | Custom webhook dispatchers                           |
| Scheduled tasks                | DaaS Cron Jobs (`mcp_daas_cron`)                     | `setInterval`, Next.js cron, external schedulers     |
| Shared reusable code           | DaaS Custom Services (`services.custom()`)           | Shared utility files for server-side logic           |
| Auto timestamps                | Special fields: `date-created`, `date-updated`       | Manual `new Date()` in API routes                    |
| Auto user tracking             | Special fields: `user-created`, `user-updated`       | Manual `req.user.id` assignment                      |
| Permissions / access control   | DaaS Permission system (RBAC)                        | Custom permission tables, `isAdmin` fields           |
| Content versioning / drafts    | DaaS Versions API (`POST /api/versions`)             | Custom version/draft tables                          |
| File upload / storage          | DaaS Files API (`POST /api/files`)                   | Custom upload endpoints, storage logic               |
| Multi-tenancy / scoping        | DaaS Scope system (`manage-scope` skill)             | Custom `tenant_id` columns, manual filtering         |
| Data import/export             | `POST /api/utils/import`, `GET /api/utils/export`   | Custom CSV parsers, import routes                    |
| Hashing / random tokens        | `POST /api/utils/hash/*`, `/random/string`           | Custom bcrypt/crypto code                            |
| Third-party integrations (Stripe API calls, Get Feedback widget, etc.) | Connect via the Buildpad platform's Connectors page; credential(s) arrive as whitelisted env var(s) — check `get_project_detail`'s `connectors[]` for the exact name(s), base URL, and auth header style (base URL may itself be one of the env vars for a self-hosted provider like Chocolate Factory or Get Feedback). **Always check that provider's `references/<key>.instructions.md` (in the `create-service` skill's `references/` folder) first** — it tells you the actual integration shape, which is NOT always a backend API call: most providers are called from a custom service via raw `services.fetch`; one that ships an official SDK (e.g. Chocolate Factory) is called from a server-side Next.js API route instead, since custom services can't import npm packages; and one that ships a client-side embeddable widget (e.g. Get Feedback — a floating button dropped into the root layout via a single `<script>` tag) needs no backend code at all. For local dev, `connectors[]` also carries `envVars` (actual decrypted values) to populate `.env.local` — and since connecting a provider does NOT push anything to the deployed Amplify app, also push that same `envVars` map with `amplify_set_env_vars` + `amplify_redeploy` (see `amplify-env-vars` skill) once the feature is built | Hardcoding API keys, inventing your own env var name, asking the user to paste a key into code, building a connector-dependent feature without pushing its env var(s) to Amplify (works locally, silently missing once deployed), asking the user what a named capability means before checking whether it's already a connected provider |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
| Pattern                        | Engine Feature                                       | DO NOT Build                                         |
| ------------------------------ | ---------------------------------------------------- | ---------------------------------------------------- |
| State machine / approvals      | Workflows (`create-workflow` skill)                  | Custom status fields, manual state logic             |
| Audit / change tracking        | **Automatic** — `daas_activity` + `GET /api/activity` | Custom audit tables, logging hooks                   |
| Validation before save         | Hooks: filter hooks ([hooks-extensions](../hooks-extensions/SKILL.md)) | Next.js API middleware validation |
| Side effects after save        | Hooks: action hooks ([hooks-extensions](../hooks-extensions/SKILL.md)) | Custom webhook dispatchers        |
| Scheduled tasks                | Cron jobs ([create-cron](../create-cron/SKILL.md)) | `setInterval`, Next.js cron, external schedulers |
| Shared reusable code           | Custom services (`services.custom()`, `create-service` skill) | Shared utility files for server-side logic  |
| Auto timestamps                | Special fields: `date-created`, `date-updated`       | Manual `new Date()` in API routes                    |
| Auto user tracking             | Special fields: `user-created`, `user-updated`       | Manual `req.user.id` assignment                      |
| Permissions / access control   | Roles, policies and permissions (`create-rbac` skill) | Custom permission tables, `isAdmin` fields          |
| Content versioning / drafts    | Versions API (`POST /api/versions`)                  | Custom version/draft tables                          |
| File upload / storage          | Files API (`POST /api/files`)                        | Custom upload endpoints, storage logic               |
| Multi-tenancy / scoping        | Scope system below the project's tenant (`manage-scope` skill) | Custom `tenant_id` columns, manual filtering |
| Data import/export             | `POST /api/utils/import/:collection`, `GET /api/utils/export/:collection` (administrators) | Custom CSV parsers, import routes |
| Hashing / random tokens        | `POST /api/utils/hash/generate`, `GET /api/utils/random/string` | Custom bcrypt/crypto code                 |
| Third-party integrations (Stripe API calls, Get Feedback widget, etc.) | Connect via the Buildpad platform's Connectors page; credential(s) arrive as env var(s) — check `get_project_detail`'s `connectors[]` for the exact name(s), base URL, and auth header style (base URL may itself be one of the env vars for a self-hosted provider like Chocolate Factory or Get Feedback). **Always check that provider's `references/<key>.instructions.md` in the `create-service` skill first** — it tells you the actual integration shape, which is NOT always a backend API call: most providers are called from a custom service via raw `services.fetch`; one that ships an official SDK (e.g. Chocolate Factory) is called from a server-side Next.js API route instead, since custom services can't import npm packages; and one that ships a client-side embeddable widget (e.g. Get Feedback — a floating button dropped into the root layout via a single `<script>` tag) needs no backend code at all. On an Engine project a custom service reads a key through `services.env` only when the Engine's operator has named that key, and reaches a host through `services.fetch` only when the operator has allowed that host (the Engine runtime table in the [Built-in DaaS features reference](references/builtin-features.instructions.md)): ask the operator, never assume either. For local dev, `connectors[]` also carries `envVars` (actual decrypted values) to populate `.env.local` — and since connecting a provider does NOT push anything to the deployed Amplify app, also push that same `envVars` map with `amplify_set_env_vars` + `amplify_redeploy` (see `amplify-env-vars` skill) once the feature is built | Hardcoding API keys, inventing your own env var name, asking the user to paste a key into code, building a connector-dependent feature without pushing its env var(s) to Amplify (works locally, silently missing once deployed), asking the user what a named capability means before checking whether it's already a connected provider |

On an Engine project files are stored and served by the Engine: `/api/files`, `/api/folders`, `/api/files/signed-url`, and file content at `/api/files/assets/:id` (with a session or a signed token). A file shown in a browser, a public one included, is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read: an `<img>` element or a link sends no `X-Tenant-Id`. Set no storage bucket option: the Engine stores files on its own disk or in S3.
<!-- /buildpad-backend -->

**Before asking a clarifying question about a named feature or capability** (e.g. "feedback widget", "chat", "payments", "analytics"), check `get_project_detail`'s `connectors[]` first. If it matches a connected provider, its `references/<key>.instructions.md` already answers "what is this and how do I add it" — no need to ask the user to disambiguate something the platform already knows.

## References

- [DaaS API reference](references/daas-api.instructions.md)
- [DaaS MCP tools](references/daas-mcp-tools.instructions.md)
- [Next.js patterns](references/nextjs.instructions.md)
- [Built-in DaaS features](references/builtin-features.instructions.md) — DO NOT rebuild these

---

## Provider Architecture Rules (Learned from Production)

<!-- buildpad-backend: supabase -->
### Rule: DaaSProvider MUST be in `(authenticated)/layout.tsx`, NEVER in root layout (Bug 22)

Next.js root layouts never unmount during client-side navigation. If `DaaSProviderWrapper` is in `app/layout.tsx`, it stays alive across logout → `/login` → re-login, delivering a stale null token and causing 401 on every DaaS call after the second login. Fix: place it in `app/(authenticated)/layout.tsx` so it fully unmounts when the user navigates to `/login`.

### Rule: DaaSProviderWrapper must use `onAuthStateChange`, NOT `getSession`, pass `token` as sync prop, and gate `ready` on non-null token (Bug 19 + Bug 27)

`supabase.auth.getSession()` from `createBrowserClient` can return `{ session: null }` before the async storage adapter finishes reading cookies. Use `onAuthStateChange` which fires `INITIAL_SESSION` only after cookie parsing is complete.

Two additional requirements:
1. Pass `token: tokenState` as a **sync prop** to `DaaSProvider` — without it `effectiveToken` is `null` on first render, so `setGlobalDaaSConfig` sets a null-token config and child components get 401.
2. Only set `ready = true` when `tok` is non-null — `INITIAL_SESSION` can fire with `session = null` when the access token is expired and Supabase is performing a silent refresh. Setting `ready` unconditionally causes children to mount without auth.
3. Make `useMemo` deps include `tokenState` so `DaaSProvider` re-renders when the token refreshes.

```tsx
const [tokenState, setTokenState] = useState<string | null>(null);
const tokenRef = useRef<string | null>(null);

useEffect(() => {
  const { data: { subscription } } = supabase.auth.onAuthStateChange(
    (_event, session) => {
      const tok = session?.access_token ?? null;
      tokenRef.current = tok;
      setTokenState(tok);
      if (tok) setReady(true); // only gate-open when token is present
    }
  );
  return () => subscription.unsubscribe();
}, [supabase]);

const config = useMemo(() => ({
  url: process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL ?? '',
  token: tokenState ?? undefined,   // sync prop for first render
  getToken: async () => tokenRef.current,
  // ...
}), [tokenState]);                  // re-create when token refreshes

if (!ready) return null;
```

### Rule: DaaSProvider must NOT clear `globalDaaSConfig` on unmount (Bug 27)

React 18+ StrictMode (on by default in Next.js dev) double-invokes effects: **mount → cleanup → mount**. If `DaaSProvider` runs `setGlobalDaaSConfig(null)` in an effect cleanup, the cleanup fires between the two mounts. Child components (`CollectionList`, `VForm`) that re-mount in the second pass call `getApiHeadersAsync()` during the null window → **401 on every hard reload in dev, and intermittently in production**.

The render body already calls `setGlobalDaaSConfig(resolvedConfig)` synchronously on every mount, so the next mount overwrites the config. Do **not** add any cleanup that nulls out `globalDaaSConfig`.

### Rule: `DaaSConfig` must include `getHeaders` for scope forwarding (Bug 16)

Buildpad components call DaaS **directly** from the browser — they do NOT go through the Next.js proxy. Without `getHeaders`, the `X-Resource-Uri` header is never sent on direct calls, and DaaS falls back to root scope where the user has no role → 403.

```tsx
getHeaders: async () => {
  const raw = document.cookie
    .split('; ')
    .find(r => r.startsWith('daas_resource_uri='))
    ?.split('=')[1];
  return raw ? { 'X-Resource-Uri': decodeURIComponent(raw) } : {};
},
```

### Rule: CORS must use explicit origins + allow `X-Resource-Uri` header (Bugs 17 + 25)

The DaaS default `cors_origins: ["*"]` is **incompatible** with Buildpad’s `credentials: 'include'` — the browser blocks every preflight. Also, `X-Resource-Uri` is not in the default `cors_allowed_headers`, so even after fixing origins the header is blocked. Always run this at project creation:

```json
{
  "cors_origins": ["http://localhost:3000", "http://localhost:3001", "<amplifyUrl>"],
  "cors_allow_credentials": true,
  "cors_allowed_headers": ["Content-Type","Authorization","Origin","X-Requested-With","Accept","X-Resource-Uri"],
  "cors_max_age": 0
}
```

### Rule: Any context that calls DaaS on mount must wait for scope to be ready (Bug 26)

If a context provider fetches from DaaS (e.g. `/api/policies/me`) and lives inside `ScopeProvider`, the first fetch will have no scope cookie yet and will get 401. The `.catch()` handler will set state to empty/false and the effect will never re-run if `scopeLoading` is not in deps.

Pattern — always consume `useScope()` and guard + react to scope changes:

```tsx
const { resourceUri, isLoading: scopeLoading } = useScope();

useEffect(() => {
  if (scopeLoading) return; // wait for scope cookie to be set
  // ... fetch from DaaS
}, [version, resourceUri, scopeLoading]); // re-fetch when tenant switches
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Rule: DaaSProvider MUST be in `(authenticated)/layout.tsx`, NEVER in root layout (Bug 22)

Next.js root layouts never unmount during client-side navigation. If `DaaSProviderWrapper` is in `app/layout.tsx`, it stays alive across logout → `/login` → re-login, delivering a stale null token and causing 401 on every Engine call after the second login. Fix: place it in `app/(authenticated)/layout.tsx` so it fully unmounts when the user navigates to `/login`.

### Rule: DaaSProviderWrapper must use `onAuthStateChange`, NOT `getSession`, pass `token` as sync prop, and gate `ready` on non-null token (Bug 19 + Bug 27)

On an Engine project the Supabase client in the browser is kept for sign-in only: it holds the session the Engine issued, and the wrapper reads the access token from it. `supabase.auth.getSession()` from `createBrowserClient` can return `{ session: null }` before the async storage adapter finishes reading cookies. Use `onAuthStateChange` which fires `INITIAL_SESSION` only after cookie parsing is complete. The token is then sent to the Engine as `Authorization: Bearer`: the Engine accepts no cookie session on its data API.

Two additional requirements:
1. Pass `token: tokenState` as a **sync prop** to `DaaSProvider` — without it `effectiveToken` is `null` on first render, so `setGlobalDaaSConfig` sets a null-token config and child components get 401.
2. Only set `ready = true` when `tok` is non-null — `INITIAL_SESSION` can fire with `session = null` when the access token is expired and the client is performing a silent refresh. Setting `ready` unconditionally causes children to mount without auth.
3. Make `useMemo` deps include `tokenState` so `DaaSProvider` re-renders when the token refreshes.

```tsx
const [tokenState, setTokenState] = useState<string | null>(null);
const tokenRef = useRef<string | null>(null);

useEffect(() => {
  const { data: { subscription } } = supabase.auth.onAuthStateChange(
    (_event, session) => {
      const tok = session?.access_token ?? null;
      tokenRef.current = tok;
      setTokenState(tok);
      if (tok) setReady(true); // only gate-open when token is present
    }
  );
  return () => subscription.unsubscribe();
}, [supabase]);

const config = useMemo(() => ({
  url: process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL ?? '',   // the Engine_URL
  token: tokenState ?? undefined,   // sync prop for first render
  getToken: async () => tokenRef.current,
  // ...
}), [tokenState]);                  // re-create when token refreshes

if (!ready) return null;
```

### Rule: DaaSProvider must NOT clear `globalDaaSConfig` on unmount (Bug 27)

React 18+ StrictMode (on by default in Next.js dev) double-invokes effects: **mount → cleanup → mount**. If `DaaSProvider` runs `setGlobalDaaSConfig(null)` in an effect cleanup, the cleanup fires between the two mounts. Child components (`CollectionList`, `VForm`) that re-mount in the second pass call `getApiHeadersAsync()` during the null window → **401 on every hard reload in dev, and intermittently in production**.

The render body already calls `setGlobalDaaSConfig(resolvedConfig)` synchronously on every mount, so the next mount overwrites the config. Do **not** add any cleanup that nulls out `globalDaaSConfig`.

### Rule: `DaaSConfig` must include `getHeaders` for scope forwarding (Bug 16)

Buildpad components call the Engine **directly** from the browser, with the user's access token — they do NOT go through the Next.js proxy. Without `getHeaders`, the `X-Resource-Uri` header is never sent on direct calls, and the Engine cannot act at the scope the user selected.

```tsx
getHeaders: async () => {
  const raw = document.cookie
    .split('; ')
    .find(r => r.startsWith('daas_resource_uri='))
    ?.split('=')[1];
  return raw ? { 'X-Resource-Uri': decodeURIComponent(raw) } : {};
},
```

The `daas_resource_uri` cookie belongs to the application's own origin: a call to the Engine carries no cookie, so the `X-Resource-Uri` header is what names the scope.

### Rule: Leave the Engine's cross-origin settings as they are

On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere. Buildpad components send the user's access token as `Authorization: Bearer`, never a cookie, and the Engine's default allowed headers include `X-Resource-Uri`, so nothing needs configuring at project creation.

### Rule: Any context that calls the Engine on mount must wait for scope to be ready (Bug 26)

If a context provider fetches from the Engine (e.g. `/api/policies/me`) and lives inside `ScopeProvider`, the first fetch runs before the scope cookie is set and is not made at the user's scope. The `.catch()` handler will set state to empty/false and the effect will never re-run if `scopeLoading` is not in deps.

Pattern — always consume `useScope()` and guard + react to scope changes:

```tsx
const { resourceUri, isLoading: scopeLoading } = useScope();

useEffect(() => {
  if (scopeLoading) return; // wait for scope cookie to be set
  // ... fetch from the Engine
}, [version, resourceUri, scopeLoading]); // re-fetch when the scope switches
```
<!-- /buildpad-backend -->
