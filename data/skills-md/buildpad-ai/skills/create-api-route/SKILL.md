---
name: create-api-route
description: Generate a server-side Next.js API route. On an Engine project, routes that forward the signed-in user's session to the Engine (items, workflow transition, users me, files, permissions, versions) plus the sign-in routes. On a Supabase project, Supabase auth routes (login, logout, callback, session) that manage Supabase SSR cookies and run server-side — do NOT use this skill there to create proxy routes for DaaS data, the UI calls DaaS directly using Authorization Bearer tokens instead. Use when the user needs a new auth endpoint or a server-side route.
argument-hint: "[route type: login|logout|callback|user]"
---

# Create API Route

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
Generate a server-side Supabase auth route. These routes manage HTTP-only cookies for Supabase SSR sessions.

> **Important:** Only create auth routes here. Data routes (items, fields, files, etc.) are NOT needed — the UI calls DaaS directly using `Authorization: Bearer <supabase-jwt>`. CORS is handled by DaaS via `CORS_ORIGINS` env var.

## Auth Routes Only

```
app/api/auth/
├── login/route.ts      # POST — Supabase signInWithPassword
├── logout/route.ts     # POST — Supabase signOut
├── callback/route.ts   # GET  — OAuth/magic-link code exchange
└── user/route.ts       # GET  — Current user from server-side session
```

## Route Template

```typescript
import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

type RouteParams = { params: Promise<{ collection: string }> };

export async function GET(request: NextRequest, { params }: RouteParams) {
  const { collection } = await params;
  const supabase = await createClient();
  const { searchParams } = new URL(request.url);

  // Parse query parameters
  const limit = parseInt(searchParams.get("limit") || "100");
  const offset = parseInt(searchParams.get("offset") || "0");
  const sort = searchParams.get("sort");
  const filter = searchParams.get("filter");

  let query = supabase.from(collection).select("*", { count: "exact" });
  query = query.range(offset, offset + limit - 1);
  if (sort)
    query = query.order(sort.replace("-", ""), {
      ascending: !sort.startsWith("-"),
    });

  const { data, error, count } = await query;
  if (error)
    return NextResponse.json(
      { errors: [{ message: error.message }] },
      { status: 500 },
    );
  return NextResponse.json({
    data,
    meta: { total_count: count, filter_count: count },
  });
}
```

## Query Parameters

- `fields` — Comma-separated field names or `*`
- `filter` — JSON filter object `{ "status": { "_eq": "published" } }`
- `sort` — Sort field(s) with `-` prefix for descending
- `limit`, `offset` — Pagination
- `aggregate` — Aggregate functions: `aggregate[count]=id` or `aggregate={"count":["id"]}`
- `groupBy` — Group aggregate results by field(s)

When an `aggregate` parameter is present, the GET handler returns computed values instead of individual items. Supported operations: `count`, `countDistinct`, `countAll`, `sum`, `sumDistinct`, `avg`, `avgDistinct`, `min`, `max`. Response format: `{ data: [{ count: { id: 42 } }] }` (no pagination meta).

> **⚠️ Field Name Verification:** Before using any field name in `sort`, `fields`, or `filter` parameters, verify it exists in the DaaS schema using `mcp_daas_schema` or `mcp_daas_fields`. Using a non-existent field (e.g., `sort=-date_created` when the actual column is `created_at`) causes DaaS to return a **500 error** with no helpful message. Never assume field names — always check the schema first.

## Authentication

All routes must check auth:

```typescript
const supabase = await createClient();
const {
  data: { user },
} = await supabase.auth.getUser();
if (!user)
  return NextResponse.json(
    { errors: [{ message: "Unauthorized" }] },
    { status: 401 },
  );
```

## Input Validation (Zod)

```typescript
import { z } from "zod";
const schema = z.object({
  name: z.string().min(1).max(255),
  status: z.enum(["draft", "published"]),
});
const validated = schema.parse(body);
```

## Required Tests

Create `tests/api/[collection].spec.ts` with:

- GET all items (200) + query parameters
- POST create with valid data (201) + invalid data (400)
- GET single item (200) + non-existent (404)
- PATCH update (200) + non-existent (404)
- DELETE item (200/204) + non-existent (404)

## References

- [API route patterns](references/api-routes.instructions.md)
- [API authorization](references/api-authorization.instructions.md)
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Generate a server-side Next.js route for an Engine project. Every data route here is a **forwarder**: it takes the signed-in user's access token from the session, sends the request on to the same path under `<Engine_URL>/api/...`, and passes the Engine's status and body (`{ data: ... }` or `{ errors: [...] }`) back unchanged. The Engine checks the user's roles, policies, permissions and scope on every request, so a route checks no permission itself and builds no query of its own.

On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

> **Important:** Create a route here when the application needs a same-origin path: the Buildpad components and hooks call relative `/api/...` paths. Each route forwards; none re-implements what the Engine does. Every template, with the helper `forwardToEngine()` they share, is in [Engine API routes](references/engine-api-routes.instructions.md).

## Routes

```
app/api/
├── auth/login/route.ts               # POST — password sign-in; names the project's tenant
├── auth/logout/route.ts              # POST — sign-out
├── auth/user/route.ts                # GET  — the signed-in user
├── items/[collection]/route.ts       # GET, POST, PATCH, DELETE → /api/items/:collection
├── items/[collection]/[id]/route.ts  # GET, PATCH, DELETE      → /api/items/:collection/:id
├── workflow/transition/route.ts      # POST                    → /api/workflow/transition
├── users/me/route.ts                 # GET, PATCH              → /api/users/me
├── files/route.ts                    # GET, POST               → /api/files
├── files/signed-url/route.ts         # GET, POST, DELETE       → /api/files/signed-url
├── permissions/me/route.ts           # GET                     → /api/permissions/me
├── versions/...                      # list, create, save, promote → /api/versions
└── utils/...                         # local utilities: no Engine call
```

## Route Template

```typescript
// app/api/items/[collection]/route.ts
import { type NextRequest } from "next/server";
import { forwardToEngine } from "@/lib/api/forward";

type RouteParams = { params: Promise<{ collection: string }> };

async function forward(request: NextRequest, { params }: RouteParams) {
  const { collection } = await params;
  // Sends Authorization: Bearer <access token> and any X-Resource-Uri header on,
  // and passes the Engine's status and body back unchanged.
  return forwardToEngine(request, `/api/items/${encodeURIComponent(collection)}`);
}

export const GET = forward; // list
export const POST = forward; // create
export const PATCH = forward; // update several
export const DELETE = forward; // delete several
```

`forwardToEngine()` (in `lib/api/forward.ts`) reads the token with `getAuthHeaders()` and the Engine_URL with `getDaasUrl()` from `@/lib/api/auth-headers`; see [Engine API routes](references/engine-api-routes.instructions.md) for its code.

## Query Parameters

The route passes the query string through untouched:

- `fields` — Comma-separated field names or `*`
- `filter` — JSON filter object `{ "status": { "_eq": "published" } }`
- `search` — Text search
- `sort` — Sort field(s) with `-` prefix for descending
- `limit`, `offset`, `page` — Pagination. The Engine serves at most 1000 items per request; `limit=-1` is served as 1000
- `aggregate`, `groupBy` — Aggregate functions and their grouping

> **Field Name Verification:** Before using any field name in `sort`, `fields`, `filter`, `aggregate` or `groupBy`, verify it exists with the MCP `fields` tool or `GET <Engine_URL>/api/fields/:collection`. The Engine answers a field name the collection does not have with 400.

## Answers and Errors

The route returns the Engine's answer as it came:

- Read and list: 200 with `{ data }`; a list also carries `meta`. Create: 200. Update: 200. Delete of one item: 204 with no body. Delete of several: 200 with a body.
- Errors: `{ errors: [{ message, extensions: { code } }] }` with the Engine's status — 401 `UNAUTHENTICATED` (no session), `TOKEN_EXPIRED` or `TOKEN_INVALID` (sign in again); 403 `FORBIDDEN`, or `MISSING_SCOPE` when a scoped collection is reached without `X-Resource-Uri`; 404 `NOT_FOUND`; 400 for a query or a payload the Engine refuses.
- The route adds one error of its own: 502 when the Engine cannot be reached.

## Sign-in Routes

Sign-in uses the Supabase client against the Engine_URL. The login route names the project's tenant with the header `X-Tenant-Id`; logout and the current user need no header, because a request with a session takes its tenant from the session. These sign-in routes need no callback route: the Supabase client's code exchange is not available on an Engine project. XAppHub sign-in, the only OAuth sign-in there, has its own callback route, which the CLI's `external-oauth-engine` module writes (see [add-external-oauth](../add-external-oauth/SKILL.md)). The three templates, and what sign-in can and cannot do there, are under "Sign-in Routes" in [Engine API routes](references/engine-api-routes.instructions.md).

## Input Validation (Zod)

Validate a body before forwarding it when the route accepts input of its own. The Engine validates every write as well; a route never relaxes what the Engine refuses.

```typescript
import { z } from "zod";
const schema = z.object({
  name: z.string().min(1).max(255),
  status: z.enum(["draft", "published"]),
});
const validated = schema.parse(body);
```

## Required Tests

Create `tests/api/[collection].spec.ts` with a signed-in test user, and assert the Engine's answers through the route:

- GET all items (200) + query parameters
- POST create with valid data (200) + invalid data (400)
- GET single item (200) + non-existent (404)
- PATCH update (200) + non-existent (404)
- DELETE item (204) + non-existent (404)
- Any route without a session (401), and a user without permission (403)

## References

- [Engine API routes](references/engine-api-routes.instructions.md) — every forwarder, the sign-in routes, files and signed URLs, permissions, versions and local utilities
<!-- /buildpad-backend -->
