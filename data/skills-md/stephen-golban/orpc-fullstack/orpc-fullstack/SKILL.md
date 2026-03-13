---
name: orpc-fullstack
description: >-
  oRPC (v1.12+) typesafe API layer for TypeScript. Covers contract-first
  development, procedure definition, middleware, routers, context, error
  handling, Hono integration, TanStack Query, event iterators, plugins, file
  uploads, WebSocket adapter, and best practices. Use when building or modifying
  API procedures, data fetching hooks, server handlers, or real-time features.
  Triggers on tasks involving oRPC, typesafe APIs, RPC procedures, or server
  route handlers.
license: MIT
metadata:
  author: stephen-golban
  version: "2.0.0"
---

# oRPC — Typesafe APIs Made Simple

oRPC combines RPC with OpenAPI for end-to-end type-safe APIs (v1.12+). It supports Zod, Valibot, Arktype, or any Standard Schema library.

## When to Apply

Reference these guidelines when:

- Creating or modifying API procedures (contracts, routers, handlers)
- Setting up middleware (auth, authorization guards, logging)
- Integrating oRPC with Hono or other server frameworks
- Building data fetching hooks with TanStack Query
- Implementing real-time features with event iterators / SSE
- Configuring client links (fetch, WebSocket, batch, retry)
- Handling errors (server-side ORPCError, client-side typed errors)

## Core Concepts

| Concept | Import | Purpose |
|---|---|---|
| Contract | `oc` from `@orpc/contract` | Define API shape without handlers |
| Procedure | `os` from `@orpc/server` | Function with validation + middleware + DI |
| Router | Plain object | Compose procedures into a tree |
| Middleware | `os.middleware()` | Intercept, inject context, guard access |
| Handler | `OpenAPIHandler` / `RPCHandler` | Serve procedures over HTTP/WS |
| Client | `createORPCClient` + link | Type-safe client from contract/router |
| TanStack Query | `createTanstackQueryUtils` | React hooks for queries/mutations |

## Project Structure

Organize by **domain modules** with paired contract + router files:

```
src/
  index.ts                    # Hono app + handler setup
  middlewares/
    auth-middleware.ts         # Session validation -> injects user
  modules/
    contract.ts               # Root barrel: all contracts
    router.ts                 # Root barrel: all routers
    health/
      health.contract.ts
      health.router.ts
    user/
      user.contract.ts
      user.router.ts
```

Root barrels compose modules: `export default { health, user }`.

## Contract-First Development

Contracts define API shape. Routers implement them with TypeScript enforcement.

```ts
// Contract — define shape
import { oc } from "@orpc/contract";
import { z } from "zod/v4";

const userContract = oc
  .route({ tags: ["user"] })
  .errors({ UNAUTHORIZED: {} });

const searchUser = userContract
  .route({ method: "POST", path: "/user/search" })
  .input(z.object({ query: z.string() }))
  .output(z.array(userSchema));

export default { searchUser };
```

```ts
// Router — implement contract
import { implement } from "@orpc/server";
import contract from "./user.contract";

const router = implement(contract).$context<{ headers: Headers }>();

const searchUser = router.searchUser
  .use(authMiddleware)
  .handler(async ({ input, context }) => { /* ... */ });

export default { searchUser };
```

## Procedures

```ts
import { os } from "@orpc/server";

const example = os
  .use(aMiddleware)                         // Middleware
  .input(z.object({ name: z.string() }))   // Validate input
  .output(z.object({ id: z.number() }))    // Validate output (recommended)
  .handler(async ({ input, context }) => {  // Handler
    return { id: 1 };
  });
```

- `.handler` is the only required step
- Specifying `.output` improves TypeScript inference speed
- Create reusable bases: `const protectedProcedure = os.$context<Ctx>().use(authMiddleware)`

## Middleware

Auth middleware injects user into context:

```ts
export const authMiddleware = os
  .$context<{ headers: Headers }>()
  .middleware(async ({ context, next }) => {
    const session = await auth.api.getSession({ headers: context.headers });
    if (!session) throw new ORPCError("UNAUTHORIZED");
    return next({ context: { ...context, user: session.user } });
  });
```

Input-aware middleware for authorization guards:

```ts
export const membershipGuard = os
  .$context<{ user: User }>()
  .middleware(async ({ context, next }, input: { uuid: string }) => {
    // Check membership using input.uuid + context.user.id
    if (!member) throw new ORPCError("FORBIDDEN");
    return next();
  });
```

Stack middleware left-to-right: `.use(auth).use(guard).handler(...)`.

Built-ins: `onStart`, `onSuccess`, `onError`, `onFinish`, `dedupeMiddleware`.

## Error Handling

```ts
// Server — throw errors
throw new ORPCError("NOT_FOUND");
throw new ORPCError("BAD_REQUEST", { message: "Invalid input" });

// Contract-defined typed errors
const contract = oc.errors({
  RATE_LIMITED: { data: z.object({ retryAfter: z.number() }) },
});

// Handler uses typed factory
const proc = implement(contract).handler(async ({ errors }) => {
  throw errors.RATE_LIMITED({ data: { retryAfter: 60 } });
});

// Client — handle errors
const [error, data] = await safe(client.doSomething({ id: "123" }));
if (isDefinedError(error)) { /* typed from contract */ }
```

## Hono Integration

```ts
import { OpenAPIHandler } from "@orpc/openapi/fetch";
import { Hono } from "hono";

const handler = new OpenAPIHandler(router, { /* plugins, interceptors */ });

const app = new Hono()
  .basePath("/api")
  .use("/rpc/*", async (c, next) => {
    const { matched, response } = await handler.handle(c.req.raw, {
      prefix: "/api/rpc",
      context: { headers: c.req.raw.headers },
    });
    if (matched) return c.newResponse(response.body, response);
    await next();
  });
```

## TanStack Query

```ts
import { createTanstackQueryUtils } from "@orpc/tanstack-query";
const orpc = createTanstackQueryUtils(client);

// Queries
useQuery(orpc.user.search.queryOptions({ input: { query } }));

// Mutations
useMutation(orpc.vehicle.add.mutationOptions());

// Infinite queries
useInfiniteQuery(orpc.feed.list.infiniteOptions({
  input: (pageParam) => ({ cursor: pageParam, limit: 20 }),
  initialPageParam: undefined,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
}));

// Keys for invalidation
orpc.vehicle.key()                           // All vehicle queries
queryClient.invalidateQueries({ queryKey: orpc.vehicle.key() });
```

## Event Iterator (SSE / Streaming)

```ts
// Server — async generator
const live = os
  .output(eventIterator(z.object({ message: z.string() })))
  .handler(async function* ({ signal }) {
    for await (const payload of publisher.subscribe("topic", { signal })) {
      yield payload;
    }
  });

// Client — consume
for await (const event of await client.live()) {
  console.log(event.message);
}
```

Use `EventPublisher` for typed pub/sub between handlers.

## Client Setup

```ts
import { RPCLink } from "@orpc/client/fetch";
import { createORPCClient } from "@orpc/client";

const link = new RPCLink({
  url: "http://localhost:3000/api/rpc",
  headers: () => ({ Authorization: `Bearer ${getToken()}` }),
});

export const client = createORPCClient(link);
```

WebSocket: `import { RPCLink } from "@orpc/client/websocket"`.

## Detailed Reference

For comprehensive examples, advanced patterns, and full API coverage see:

- [Full Reference](references/REFERENCE.md) — Complete documentation with detailed code examples covering contracts, routers, middleware, server handlers, client setup, TanStack Query, event iterators, plugins, file uploads, WebSocket, AI SDK integration, and metadata.
