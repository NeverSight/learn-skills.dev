---
name: instancez
description: Use when building, changing, or deploying an instancez backend - editing instancez.yaml (tables, RLS, auth, storage, rpc, functions), running the inz CLI, or debugging why a query is denied. instancez is a single-binary Supabase-compatible backend defined by one YAML file.
---

# Building with instancez

instancez turns one file, `instancez.yaml`, into a full backend: Postgres CRUD, auth, storage, SQL RPC, and Node.js functions. Clients talk to it with `@supabase/supabase-js` (or any Supabase client library) unchanged. There are no migration files: on every run the migrator diffs the YAML against the live database and applies the delta, including drops.

## Workflow

If `inz` is not installed: `curl -fsSL https://get.instancez.ai | sh` (macOS/Linux) or `irm https://get.instancez.ai/windows | iex` (PowerShell).

```sh
inz init                # scaffold instancez.yaml + .development.env.example
inz validate            # check YAML syntax and references, no DB needed
inz dev --embedded-pg   # dev server on :8080 with a built-in Postgres 16
```

Edit `instancez.yaml`, save, and `inz dev` re-applies the schema automatically. Always run `inz validate` after editing the YAML; it catches bad types, bad references, and missing function files without touching a database.

Without `--embedded-pg`, `inz dev` needs `INSTANCEZ_DATABASE_URL` set to a superuser DSN. API keys land in `.development.env` on first run (`INSTANCEZ_PUBLISHABLE_KEY`, `INSTANCEZ_SECRET_KEY`). `inz doctor` diagnoses a dev setup that won't boot.

Client-side, the app is a normal Supabase app. Point any Supabase client library at the server and the whole surface works: PostgREST-style queries with filters and embeds, auth, storage, RPC, functions.

```js
import { createClient } from '@supabase/supabase-js'
const supabase = createClient('http://localhost:8080', process.env.INSTANCEZ_PUBLISHABLE_KEY)
const { data, error } = await supabase.from('todos').select('*').eq('status', 'pending')
```

The secret key takes the `service_role` path (bypasses RLS); keep it server-side only.

Other commands: `inz serve` (production, no hot reload, dashboard off by default), `inz bundle` (build a tar.gz of config + functions for deploys), `inz cloud deploy` (push to a managed project; `--new` creates one).

## instancez.yaml at a glance

Top-level keys:

```yaml
version: 1
project:
  name: my-app
server:        # port, cors, timeouts, max_body_size (all optional)
providers:     # storage backend (local | s3), email provider
auth:          # jwt expiry, refresh tokens, signup toggles, oauth
tables:        # your schema + RLS policies
storage:       # buckets + RLS policies
rpc:           # Postgres stored procedures at /rest/v1/rpc/<name>
functions:     # Node.js handlers at /functions/v1/<name>
```

`rpc:` is SQL running inside Postgres. `functions:` is JavaScript running in Node workers. Don't mix them up.

## Tables

```yaml
tables:
  posts:
    rls_enabled: true
    fields:
      - name: id
        type: bigserial          # or: uuid with default: uuid_v7()
        primary_key: true
      - name: user_id
        foreign_key:
          references: auth.users.id   # table.column or schema.table.column; type inferred: uuid for auth.users.id, bigint otherwise
          on_delete: cascade          # cascade | restrict (default) | set_null
      - name: title
        type: text
        required: true               # NOT NULL
      - name: status
        type: text
        required: true
        enum: [draft, published]     # enum only works on text/varchar/char
        default: draft
      - name: score
        type: integer
        min: 0                       # min/max/check/pattern become CHECK constraints
        max: 100
      - name: created_at
        type: timestamptz
        required: true
        default: now()               # a literal, or one of: now(), uuid_v7(), uuid_v4(), current_date, current_time
      - name: updated_at
        type: timestamptz
        auto_updated_at: true        # set to now() on every update (timestamp types only)
      # immutable: true on any field rejects updates that change it (400, all roles)
    indexes:
      - columns: [user_id, created_at]
      - columns: [title]
        unique: true
        where: "status = 'published'"   # partial index
      - columns: [search]
        method: gin                     # btree (default) | hash | gin | gist | brin | spgist
    rls:
      - operations: [select]
        using: "true"
```

Rules the migrator enforces:

- Every table needs a field with `primary_key: true`. Nothing is auto-added, not `id`, not `created_at`. Mark two or more fields for a composite key (a junction table keyed on both FKs also enables many-to-many embeds like `posts?select=*,tags(*)`). Key columns can't change once the table exists.
- `type` comes from a fixed allowlist of standard Postgres types (serials, integers, text/varchar/char, boolean, numeric, date/time, uuid, jsonb, bytea, inet, and similar). Custom types like `citext` or `hstore` fail validation. `[]` array suffixes work.
- Names are lowercase snake_case, starting with a letter, no SQL keywords.
- The `auth` and `storage` schemas are reserved. User profile data goes in a regular table with a FK to `auth.users.id`, never in `schema: auth`.
- Removing a table or column from the YAML drops it on the next run, with no confirmation. Warn the user before deleting anything from the YAML of a project with real data.

## RLS

RLS is the only authorization layer. There is no HTTP-level RBAC and no role table: the middleware validates the JWT, picks one of three Postgres roles, and Postgres policies decide everything else.

| Request credential | Role | RLS |
|---|---|---|
| Publishable key only | `anon` | enforced |
| Publishable key + user JWT | `authenticated` | enforced |
| Secret key | `service_role` | bypassed |

Each policy entry has `operations` (exactly one of select/insert/update/delete, or all four together; other combinations are rejected), `using` (which existing rows the operation may touch), and `with_check` (what a written row may look like).

```yaml
rls:
  # public read, owner write
  - operations: [select]
    using: "true"
  - operations: [insert]
    with_check: "auth.uid() = user_id"
  - operations: [update]
    using: "auth.uid() = user_id"      # set using explicitly on update policies;
    with_check: "auth.uid() = user_id" # with_check alone matches zero rows
  - operations: [delete]
    using: "auth.uid() = user_id"
```

Helpers available inside policy expressions: `auth.uid()` (uuid, NULL for anon and service_role), `auth.role()`, `auth.email()`, `auth.jwt()`, `auth.is_authenticated()`.

Set `rls_enabled` on every table. `rls_enabled: true` with no policies is deny-all for the publishable key, which is the safe default for new tables. Add policies to open specific access. `rls_enabled: false` exposes every row to every role and should only be used for deliberately public tables. `false` combined with policies is rejected. A table with policies but none matching a request returns empty results or silent write failures rather than errors; when a query "returns nothing" under the publishable key, suspect RLS before suspecting the query.

## Auth

```yaml
auth:
  jwt_expiry: 1h
  refresh_tokens: true      # without this, supabase-js reports session: null even on successful sign-in
  refresh_token_expiry: 7d
  allow_signup: true
  allow_anonymous: false    # anonymous sign-in is off by default; true enables signInAnonymously()
  redirect_urls:            # frontend origins OAuth/magic-link flows may land on
    - https://myapp.example.com
  oauth:
    google:
      client_id: YOUR_CLIENT_ID
      client_secret: ${INSTANCEZ_ENV_GOOGLE_CLIENT_SECRET}
      redirect_url: https://api.myapp.example.com/auth/v1/callback/google
```

All keys are optional. Clients use the normal Supabase auth API: `supabase.auth.signUp()`, `signInWithPassword()`, `signInWithOtp()` (needs an `auth.email` block and an email provider), `signInWithOAuth()`.

## Storage

```yaml
storage:
  avatars:
    public: true            # anyone can download via /object/public; list/sign/update/delete still need rls
    max_size: 5MB
    types: [image/*]
    rls:
      - operations: [insert]
        with_check: "auth.is_authenticated()"
```

Declaring any bucket requires a `providers.storage` block (`type: local` for dev, `type: s3` for production). Bucket `rls` uses the same policy syntax as tables, applied to `storage.objects`. Clients use `supabase.storage.from('avatars').upload(...)` as usual. Signed URLs are authorized at creation time against the bucket's policies. As in Supabase, `public: true` only opens `/object/public/<bucket>/<path>` downloads; it grants no `select`, so add a `select` policy for anyone who should list, sign, update or delete. Publishable-key (guest) calls run as `anon` under those policies, so `using: "true"` admits guests; a bucket with no `rls:` gives guests nothing.

## RPC (SQL functions)

```yaml
rpc:
  team_stats:
    auth_required: true
    language: sql            # sql | plpgsql (default)
    volatility: stable       # stable/immutable also allow GET; volatile is POST-only
    set: { search_path: "" } # also statement_timeout, lock_timeout, work_mem
    args:
      - name: team_id
        type: bigint
        required: true
    returns:
      type: bigint           # a concrete Postgres type, or record, setof <table>, void
    body: |
      SELECT count(*) AS total FROM public.todos WHERE team_id = team_stats.team_id
```

Called with `supabase.rpc('team_stats', { team_id: 42 })` or `POST /rest/v1/rpc/team_stats`. Args bind as typed parameters, never string-concatenated. An optional arg takes `default: null` (or `NULL`) for `DEFAULT NULL`; other defaults are literals (use `"('null')"` for the text `null`). The body runs under the caller's role, so RLS applies inside it unless `security: definer`. A definer function should pin `set: { search_path: "" }` and schema-qualify names; `inz validate` warns otherwise.

## Code functions (Node.js)

```yaml
functions:
  charge:
    runtime: node                  # the only supported runtime; needs Node 22+ on PATH
    file: functions/charge.js
    auth_required: true            # anonymous callers get 401 before the handler runs
    timeout: 30s
    env:
      STRIPE_KEY: ${INSTANCEZ_ENV_STRIPE_KEY}   # from .env / .development.env / process env
```

```js
// functions/charge.js  (ESM)
export default async function handler(req, ctx) {
  const userId = ctx.claims?.sub;                      // null for anonymous callers
  const { data, error } = await ctx.supabase           // caller's JWT, RLS applies
    .from("orders").insert({ user_id: userId, item: req.body.item }).select().single();
  if (error) return { status: 400, body: { error: error.message } };
  return { status: 200, body: { order: data } };      // body: object -> JSON, string as-is, Buffer raw
}
```

`req` carries `method`, `path`, `query`, `headers`, parsed `body`, and `rawBody` (a Buffer, for webhook signature checks). `ctx` also has `serviceClient` (bypasses RLS; only use it for the specific step RLS blocks, on a function with `auth_required: true`), `env`, `log`, and `signal`. npm dependencies go in `functions/package.json`; commit the `package-lock.json`, since bundling runs `npm ci`.

Call from the client with `supabase.functions.invoke('charge', { body: {...} })`.

## Deploy

```sh
inz bundle --output s3://bucket/app.tar.gz        # config + functions + vendored deps in one archive
inz serve --bundle s3://bucket/app.tar.gz --migrate --watch
```

Or `inz cloud deploy` for a managed project (shows a diff and asks before writing; `--yes` for CI). Production secrets load from `.production.env`. Full deploy docs: https://instancez.github.io/deploy/docker/

## Checklist before you finish

- `inz validate` passes.
- Every table sets rls_enabled explicitly; private tables use rls_enabled: true, and every update policy sets using.
- Nothing was removed from the YAML unintentionally; removals become DROPs.
- Secrets are `${INSTANCEZ_ENV_*}` references, never literals committed to the YAML.
- Postgres stored procedures live under `rpc:`, JavaScript under `functions:`.

This file covers the common paths. For anything deeper (query operators, OAuth setup, MFA, image resizing, Kubernetes/Lambda deploys), read the docs at https://instancez.github.io/ or run `inz <command> --help`.
