---
name: postgrest-rls
description: Configure Row-Level Security (RLS) with PostgREST in a Postgres project. Use when the user wants to set up user-scoped data access, JWT auth with PostgREST, per-user data isolation, or wants a backend to proxy requests to PostgREST with forwarded JWTs. Triggers on terms like "RLS", "row-level security", "PostgREST auth", "multi-tenant Postgres", "user isolation in Postgres".
---

# PostgREST + RLS Setup

This skill is a playbook for wiring up authenticated, per-user data access in a stack with **Postgres + PostgREST + (optionally) a Node backend**. It covers the full chain: roles → JWT → views → RLS policies → backend integration.

## When to Use

- User wants to restrict data access per user/tenant in Postgres.
- User is adding PostgREST and needs auth.
- User has a backend that should forward a user's JWT to PostgREST (proxy pattern).
- User hits RLS "permission denied" or "no rows returned" and needs to debug.

## Core Concepts (read first)

### The three roles PostgREST expects

| Role | Purpose | Notes |
|------|---------|-------|
| `anon` | Unauthenticated callers | Set via `PGRST_DB_ANON_ROLE`. Usually read-only or nothing. |
| `authenticated` | Logged-in users | JWT claim `role: "authenticated"` makes PostgREST `SET ROLE` to it. |
| `authenticator` | Login role for the PG connection | Has `LOGIN`, `NOINHERIT`. Can `SET ROLE` to `anon` / `authenticated`. Configured via `PGRST_DB_URI`. |

Critical: `authenticator` must be granted the other roles (`GRANT anon, authenticated TO authenticator`), and must be `NOINHERIT` so it only gets the target role's privileges after `SET ROLE`.

### JWT contract

PostgREST reads the JWT from `Authorization: Bearer <token>`. It must:
- Be signed with HS256 using the secret in `PGRST_JWT_SECRET`.
- Include a `role` claim matching a DB role (`anon` if missing).
- Any other claim is available in SQL via `current_setting('request.jwt.claims', true)::jsonb->>'claim_name'`.

Common claims: `sub` (user id), `exp`, `role`, `email`.

### How RLS is bypassed (gotchas)

`ENABLE ROW LEVEL SECURITY` applies to everyone **except**:
1. **Superusers** (e.g. `postgres` created by the Docker image).
2. Roles with `BYPASSRLS` attribute.
3. The **table owner** (unless `FORCE ROW LEVEL SECURITY` is set).

If a backend connects as superuser, its writes ignore RLS — fine for a trusted service. If it connects as a regular role, `INSERT` will fail when the policy references `auth.user_id()` and no JWT is set on the session.

## Setup Playbook

Follow these steps in order. Assume a `public` schema with existing tables and an `api` schema that PostgREST will expose.

### Step 1 — Schemas and roles

```sql
CREATE SCHEMA IF NOT EXISTS api;
CREATE SCHEMA IF NOT EXISTS auth;

CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE authenticator LOGIN PASSWORD '<strong-random>' NOINHERIT;
GRANT anon, authenticated TO authenticator;

GRANT USAGE ON SCHEMA api TO anon, authenticated;
```

### Step 2 — Users table (for email/password auth)

```sql
CREATE TABLE IF NOT EXISTS auth.users (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email         text UNIQUE NOT NULL,
  password_hash text NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now()
);
```

`auth.users` is NEVER exposed through PostgREST. Only the backend (as superuser or a privileged role) reads/writes it.

### Step 3 — Ownership column on user-scoped tables

Add `owner_id uuid REFERENCES auth.users(id)` to the **root** tenant table (the one that represents "thing that belongs to a user"). Child tables link via FK to the root, not directly to `auth.users`.

Example:
- `clients.owner_id → auth.users.id` (root)
- `pautas.client_id → clients.id` (child, no owner_id needed)
- `articles.client_id → clients.id` (child)

### Step 4 — Helper functions

```sql
CREATE OR REPLACE FUNCTION auth.user_id() RETURNS text
LANGUAGE sql STABLE AS $$
  SELECT current_setting('request.jwt.claims', true)::jsonb->>'sub'
$$;

CREATE OR REPLACE FUNCTION auth.owns_client(cid text) RETURNS boolean
LANGUAGE sql STABLE AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.clients c
    WHERE c.id = cid AND c.owner_id::text = auth.user_id()
  )
$$;
```

`STABLE` matters — lets the planner inline. The `true` in `current_setting(..., true)` makes it return NULL instead of erroring when the setting is missing (important for backend connections without a JWT).

### Step 5 — RLS on the root table

```sql
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS clients_owner_all ON public.clients;
CREATE POLICY clients_owner_all ON public.clients
  FOR ALL TO authenticated
  USING (owner_id::text = auth.user_id())
  WITH CHECK (owner_id::text = auth.user_id());

GRANT SELECT, INSERT, UPDATE, DELETE ON public.clients TO authenticated;
```

`USING` filters reads and the "before" side of updates/deletes. `WITH CHECK` validates inserts and the "after" side of updates — prevents a user from changing `owner_id` to another user.

### Step 6 — RLS on child tables (loop pattern)

```sql
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY['pautas','articles','client_categories','client_tags']
  LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format('DROP POLICY IF EXISTS %I_owner_all ON public.%I', t, t);
    EXECUTE format($f$
      CREATE POLICY %I_owner_all ON public.%I
        FOR ALL TO authenticated
        USING (auth.owns_client(client_id))
        WITH CHECK (auth.owns_client(client_id))
    $f$, t, t);
    EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON public.%I TO authenticated', t);
  END LOOP;
END $$;
```

For grandchildren (e.g. `images.article_id → articles.id`), write an explicit `EXISTS` clause that joins up to the root.

### Step 7 — Views in the `api` schema

PostgREST only exposes what's in the schema named by `PGRST_DB_SCHEMA`. Create views — they inherit RLS from the underlying table.

```sql
-- Pass-through view (RLS on base table filters rows)
CREATE OR REPLACE VIEW api.pautas AS SELECT * FROM public.pautas;

-- Column-filtering view (hides sensitive columns like password hashes)
CREATE OR REPLACE VIEW api.clients AS
SELECT id, name, owner_id, created_at, updated_at  -- NO password_hash
FROM public.clients;

GRANT SELECT, INSERT, UPDATE, DELETE ON api.pautas, api.clients TO authenticated;
```

Gotcha: views execute with the caller's permissions AND respect RLS of underlying tables by default in modern Postgres (`security_invoker=true` is default in PG 15+). On older versions, explicitly set `WITH (security_invoker = true)`.

### Step 8 — JWT signing (backend login)

```ts
// Backend POST /auth/login — sign HS256 with PGRST_JWT_SECRET
import { createHmac } from 'node:crypto'

function base64url(b: Buffer | string) {
  return Buffer.from(b).toString('base64')
    .replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_')
}

function signJwt(claims: Record<string, unknown>, secret: string, ttlSec = 604800) {
  const now = Math.floor(Date.now() / 1000)
  const header = base64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const body = base64url(JSON.stringify({ iat: now, exp: now + ttlSec, ...claims }))
  const sig = base64url(createHmac('sha256', secret).update(`${header}.${body}`).digest())
  return `${header}.${body}.${sig}`
}

// After verifying password:
const token = signJwt({ sub: userId, role: 'authenticated', email }, process.env.PGRST_JWT_SECRET!)
```

For passwords: use `scrypt` from `node:crypto` (no new dep) or `bcrypt`/`argon2` if available.

### Step 9 — Backend as PostgREST proxy

If a Node backend needs to call PostgREST on behalf of the user (orchestration + user data), forward the user's JWT:

```ts
const res = await fetch(`${POSTGREST_URL}/pautas?client_id=eq.${clientId}`, {
  headers: {
    'Authorization': `Bearer ${userJwt}`,
    'Content-Type': 'application/json',
  },
})
```

Hono middleware to extract + attach:
```ts
export const authContext: MiddlewareHandler = async (c, next) => {
  const header = c.req.header('Authorization')
  const jwt = header?.startsWith('Bearer ') ? header.slice(7) : null
  c.set('jwt', jwt)
  await next()
}
```

## Common Errors & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `permission denied for schema api` | Missing `GRANT USAGE ON SCHEMA api TO authenticated` | Add grant |
| `permission denied for table X` | Policy exists but no table grant | `GRANT ... ON public.X TO authenticated` |
| `new row violates row-level security policy` | INSERT missing `WITH CHECK`-passing value (often `owner_id` not set) | Set `owner_id` from JWT sub before insert |
| RLS returns 0 rows but data exists | `request.jwt.claims` not set on connection (e.g. backend using Drizzle directly) | Either use superuser connection or `SET LOCAL` the claims in a transaction |
| JWT valid but `role` not switched | Missing `GRANT authenticated TO authenticator` | Add grant, restart PostgREST |
| Backend writes fail after adding RLS | Backend role is not superuser / BYPASSRLS | Use superuser connection, OR `ALTER ROLE backend_svc BYPASSRLS`, OR switch backend to call PostgREST with a service JWT |

## Debugging checklist

1. `\du` in psql — confirm roles exist, `authenticator` has `LOGIN NOINHERIT`.
2. `SELECT rolname FROM pg_auth_members m JOIN pg_roles r ON m.roleid=r.oid WHERE m.member=(SELECT oid FROM pg_roles WHERE rolname='authenticator')` — confirm grants.
3. `SELECT * FROM pg_policies WHERE schemaname='public'` — list all policies.
4. Test JWT at jwt.io with the secret — confirm `role` claim is `authenticated`.
5. `curl -H "Authorization: Bearer $JWT" localhost:3001/clients` — bypass the backend to isolate.
6. In psql as `authenticator`, run `SET ROLE authenticated; SET request.jwt.claims = '{"sub":"<uuid>","role":"authenticated"}'; SELECT * FROM api.clients;` to simulate what PostgREST does.

## Decision: Backend proxy vs direct `SET LOCAL ROLE`

Two ways for a backend to respect RLS:

- **Proxy**: backend forwards JWT to PostgREST via HTTP. RLS lives in one place. Simpler. Extra network hop. Atomicity across backend logic + user writes impossible.
- **SET LOCAL**: backend opens a transaction, runs `SET LOCAL ROLE authenticated; SET LOCAL request.jwt.claims = '...'`, then queries with Drizzle/pg. Same connection, atomic. Requires validating JWT manually and disciplined wrapper.

Default to **proxy** unless you need atomic mixed writes.

## Files this skill typically creates or modifies

- `db/init.sql` — roles, schemas, RLS, policies, views, grants
- `backend/src/modules/auth/auth.service.ts` — register/login, JWT signing, scrypt
- `backend/src/modules/auth/auth.routes.ts` — `POST /auth/register`, `POST /auth/login`
- `backend/src/lib/auth.ts` — JWT verification middleware, `requireUser(c)` helper
- `backend/src/lib/postgrest.ts` — typed client that forwards JWT
- `docker-compose.yml` — PostgREST service with `PGRST_JWT_SECRET`, `PGRST_DB_SCHEMA=api`, `PGRST_DB_ANON_ROLE=anon`
- `.env.example` — `PGRST_JWT_SECRET` (≥32 chars)
