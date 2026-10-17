---
name: tanstack-start-server-routes
description: >-
  Use when building server routes or server functions with TanStack Start —
  file-based API routes, createServerFn, request handlers, or porting Supabase
  Edge Function logic into a TanStack Start app. Not for Vite-only SPAs (use
  edge-functions-and-webhooks) or Next.js route handlers.
---

# TanStack Start server routes and server functions

[TanStack Start](https://tanstack.com/start) gives you SSR + file-based **server routes** and isomorphic **server functions** in the same app as your TanStack Router + Query frontend. Use it when you want a single deploy unit instead of "SPA + Supabase Edge Functions".

If the project is plain **Vite + React**, stay on Supabase Edge Functions — see [`edge-functions-and-webhooks`](../edge-functions-and-webhooks/). This skill applies when the project is (or is moving to) TanStack Start.

Companion skills: [`tanstack-router-data-loaders`](../tanstack-router-data-loaders/), [`tanstack-query-alternative`](../tanstack-query-alternative/), [`server-input-validation`](../server-input-validation/), [`api-error-handling`](../api-error-handling/), [`rate-limiting-edge`](../rate-limiting-edge/).

## When to use each primitive

| Need | Use |
|------|-----|
| Endpoint at a stable URL (third-party webhooks, OAuth callbacks, downloads) | **Server route** (`api.*.ts`) |
| Backend logic called from React (mutations, server-only reads) | **Server function** (`createServerFn`) |
| Initial data for a route on SSR | **Loader** (see `tanstack-router-data-loaders`) |
| Periodic background work | **pg_cron** (see `pg-cron-scheduled-jobs`) |

Rule of thumb: **server functions for client-driven work, server routes for external integrations.**

---

## Server routes (file-based HTTP handlers)

```
app/routes/
  api.stripe-webhook.ts
  api.health.ts
  api.users.$id.ts
```

```ts
// app/routes/api.health.ts
import { createAPIFileRoute } from "@tanstack/start/api";

export const APIRoute = createAPIFileRoute("/api/health")({
  GET: () => Response.json({ ok: true, t: Date.now() }),
});
```

Path params from the file name:

```ts
// app/routes/api.users.$id.ts
export const APIRoute = createAPIFileRoute("/api/users/$id")({
  GET: async ({ params }) => {
    const user = await db.user.findUnique({ where: { id: params.id } });
    if (!user) return new Response("Not found", { status: 404 });
    return Response.json(user);
  },
});
```

Use for: webhooks, OAuth callbacks, RSS feeds, sitemaps, robots.txt, image proxies.

---

## Server functions (`createServerFn`)

Server functions are isomorphic: you import them in React components but the body only runs on the server. They auto-serialize input/output and integrate with TanStack Query.

```ts
// app/server/projects.ts
import { createServerFn } from "@tanstack/start";
import { z } from "zod";
import { getUserFromRequest } from "~/server/auth";

const createProjectSchema = z.object({
  name: z.string().min(1).max(80),
  organization_id: z.string().uuid(),
});

export const createProject = createServerFn(
  { method: "POST" },
  async (raw: unknown) => {
    const input = createProjectSchema.parse(raw);
    const user = await getUserFromRequest();
    if (!user) throw new HttpError(401, "unauthorized");

    const allowed = await canCreateProject(user.id, input.organization_id);
    if (!allowed) throw new HttpError(403, "forbidden");

    const project = await db.project.create({
      data: { ...input, owner_id: user.id },
    });
    return project;
  },
);
```

In React (wired through TanStack Query):

```tsx
const create = useMutation({
  mutationFn: (vars: { name: string; organization_id: string }) => createProject(vars),
  onSuccess: () => qc.invalidateQueries({ queryKey: ["projects"] }),
});
```

See [`tanstack-mutations-and-invalidation`](../tanstack-mutations-and-invalidation/) for invalidation patterns.

---

## Auth and authorization

Server functions and routes both run on the server, so:

- Read auth from request context (`getEvent`, cookies, or your auth library — Supabase, Lucia, Clerk).
- Authorize **after** input validation.
- Never trust IDs in the payload for ownership — re-check membership via the authenticated user.

```ts
async function getUserFromRequest() {
  const event = getEvent();
  const token = getCookie(event, "sb-access-token");
  if (!token) return null;
  const { data, error } = await supabase.auth.getUser(token);
  if (error || !data.user) return null;
  return data.user;
}
```

---

## Input validation and error shape

Always validate (`server-input-validation`) and return a consistent error JSON (`api-error-handling`):

```ts
class HttpError extends Error {
  constructor(public status: number, public code: string, message?: string) {
    super(message ?? code);
  }
}

function jsonError(e: HttpError) {
  return Response.json({ error: e.code, message: e.message }, { status: e.status });
}
```

Server routes should `try/catch` and surface `HttpError` as JSON; server functions throw and Start serializes the error to the client (your hook gets a typed error).

---

## Webhook routes (Stripe, GitHub, Linear)

```ts
// app/routes/api.stripe-webhook.ts
import { createAPIFileRoute } from "@tanstack/start/api";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-11-20.acacia",
});

export const APIRoute = createAPIFileRoute("/api/stripe-webhook")({
  POST: async ({ request }) => {
    const body = await request.text();
    const sig = request.headers.get("stripe-signature")!;
    let event: Stripe.Event;
    try {
      event = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
    } catch {
      return new Response("Bad signature", { status: 400 });
    }
    // see stripe-payment-webhooks for full handler + idempotency
    return Response.json({ received: true });
  },
});
```

Node runtime supports the sync `constructEvent`; the Deno `constructEventAsync` form from [`stripe-payment-webhooks`](../stripe-payment-webhooks/) is only needed on Supabase Edge.

---

## File layout

```
app/
  routes/
    __root.tsx
    index.tsx
    projects.$id.tsx           # page routes
    api.health.ts              # API routes
    api.stripe-webhook.ts
  server/
    auth.ts
    db.ts
    projects.ts                # createServerFn
  components/
  lib/
```

Keep server-only modules under `app/server/` so it's obvious what is *not* shipped to the client.

---

## Deployment notes

- **Node target**: Vercel, Render, Fly, your own Node. Has full Node API.
- **Edge target**: Cloudflare, Vercel Edge. Constrained APIs (no `fs`, no native Node libs).
- Choose the target before you write server code — switching later may force rewrites.

Set env vars via the host. Never check `.env` into git.

---

## Avoid

- Calling `createServerFn` from a server route handler (wasteful indirection — just call the function body directly).
- Using server functions for third-party webhooks (the URL must be stable; use `api.*.ts` routes).
- Mixing Supabase Edge Functions and TanStack Start server routes for the same purpose. Pick one server.
- Returning HTML from API routes; return JSON with status codes (`api-error-handling`).
- Sharing module-level mutable state between requests in the server runtime.

## Checklist

- [ ] Server routes only for stable URLs (webhooks, files, integrations).
- [ ] Server functions validate input (Zod) and authorize the caller.
- [ ] Errors returned as consistent JSON (`api-error-handling`).
- [ ] Server-only code lives under `app/server/`.
- [ ] Webhook signatures verified before any side effect.
