---
name: trpc
description: |
  tRPC v11 end-to-end type-safe APIs for TypeScript. Covers router and procedure definitions, input validation with Zod, middleware and context, subscriptions, error handling with TRPCError, React client hooks via @trpc/react-query, server-side callers with createCallerFactory, adapter setup (standalone, Express, Fastify, Hono), and testing patterns.

  Use when building tRPC routers, defining procedures, setting up middleware, configuring adapters, integrating tRPC with React, handling errors, implementing subscriptions, or testing tRPC procedures.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://trpc.io/docs'
user-invocable: false
---

# tRPC

## Overview

tRPC enables end-to-end type-safe APIs by sharing TypeScript types between server and client without code generation or schemas. The server defines procedures (queries, mutations, subscriptions) in a router, and the client infers all types from the exported `AppRouter` type.

**When to use:** TypeScript full-stack apps needing type-safe API layers, monorepos sharing types, real-time subscriptions, rapid API iteration without OpenAPI/GraphQL overhead.

**When NOT to use:** Public APIs consumed by non-TypeScript clients (use REST/GraphQL), polyglot backends, projects requiring OpenAPI spec generation as primary output.

## Quick Reference

| Pattern               | API                                        | Key Points                                              |
| --------------------- | ------------------------------------------ | ------------------------------------------------------- |
| Initialize            | `initTRPC.context<Ctx>().create()`         | Single entry point, configure once                      |
| Router                | `t.router({ ... })`                        | Nest routers with `t.mergeRouters()`                    |
| Query                 | `t.procedure.input(schema).query(fn)`      | Read operations, cached by clients                      |
| Mutation              | `t.procedure.input(schema).mutation(fn)`   | Write operations                                        |
| Subscription          | `t.procedure.subscription(fn)`             | Real-time via WebSocket or SSE                          |
| Middleware            | `t.middleware(fn)`                         | Chain with `.use()`, extend context via `next({ ctx })` |
| Standalone middleware | `experimental_standaloneMiddleware<{}>()`  | Reusable with explicit type constraints                 |
| Context               | `createContext({ req, res })`              | Per-request, passed to all procedures                   |
| Server caller         | `t.createCallerFactory(router)`            | Type-safe server-side procedure calls                   |
| Error                 | `throw new TRPCError({ code, message })`   | Mapped to HTTP status codes                             |
| Error formatter       | `initTRPC.create({ errorFormatter })`      | Customize error shape, expose Zod errors                |
| Input validation      | `.input(zodSchema)`                        | Multiple `.input()` calls merge (intersection)          |
| Output validation     | `.output(zodSchema)`                       | Strip extra fields from responses                       |
| React hooks           | `trpc.useQuery()` / `trpc.useMutation()`   | Built on @tanstack/react-query                          |
| React utils           | `trpc.useUtils()`                          | Invalidate, prefetch, setData on cache                  |
| Suspense query        | `trpc.useSuspenseQuery()`                  | Suspense-compatible data fetching                       |
| React subscription    | `trpc.useSubscription(input, opts)`        | `onData` callback for real-time events                  |
| Vanilla client        | `createTRPCClient<AppRouter>({ links })`   | No React dependency                                     |
| Batch link            | `httpBatchLink({ url })`                   | Batches requests in single HTTP call                    |
| Stream link           | `httpBatchStreamLink({ url })`             | Streams responses as they resolve                       |
| WS link               | `wsLink({ client: wsClient })`             | WebSocket transport for subscriptions                   |
| Split link            | `splitLink({ condition, true, false })`    | Route operations to different transports                |
| Logger link           | `loggerLink()`                             | Debug request/response in development                   |
| Data transformer      | `initTRPC.create({ transformer })`         | Serialize Dates, Maps, Sets (superjson)                 |
| Fetch adapter         | `fetchRequestHandler({ endpoint, req })`   | Cloudflare Workers, Deno, Bun, Next.js                  |
| Procedure chaining    | `publicProcedure.use(auth).use(rateLimit)` | Build reusable procedure bases                          |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------ |
| Exporting the full `t` object                       | Export only `t.router`, `t.procedure`, `t.middleware`, `t.createCallerFactory` |
| Creating context inside procedure                   | Create context in adapter setup, flows through automatically                   |
| Using `any` for context type                        | Define context type with `initTRPC.context<MyContext>().create()`              |
| Catching errors in procedures                       | Let errors propagate; use `onError` in adapter or error formatter              |
| Importing server code on client                     | Import only `type AppRouter`, never runtime server code                        |
| Using `createCaller` in production request handlers | Use `createCallerFactory` for type-safe reusable callers                       |
| Defining input without validation                   | Always validate with Zod, Valibot, or ArkType schemas                          |
| Nesting routers incorrectly                         | Use dot notation in keys or `t.mergeRouters()`, not deep nesting               |
| Different transformers on client/server             | Both sides must use the same transformer (e.g., superjson)                     |
| Creating QueryClient inside component render        | Create once outside component or use useState initializer                      |
| Manual TypeScript generics on hooks                 | Type the router procedures; let inference propagate to client                  |
| Not passing `signal` to fetch in queryFn            | tRPC React handles abort signals automatically                                 |

## Installation

```bash
pnpm add @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

For subscriptions, add `ws` (server) and configure `wsLink` (client). For SSE-based subscriptions, use `httpBatchStreamLink` instead.

## Delegation

- **Procedure discovery**: Use `Explore` agent
- **Router architecture review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `tanstack-query` skill is available, delegate query/mutation caching, invalidation, and optimistic update patterns to it.
> If the `zod-validation` skill is available, delegate input schema design and validation patterns to it.
> If the `drizzle-orm` skill is available, delegate database query patterns within procedures to it.
> If the `vitest-testing` skill is available, delegate test runner configuration and assertion patterns to it.
> If the `hono` skill is available, delegate Hono framework routing and middleware patterns to it.

## References

- [Router and procedure definitions](references/router-procedures.md)
- [Middleware and context patterns](references/middleware-context.md)
- [Error handling and formatting](references/error-handling.md)
- [React client integration with @trpc/react-query](references/react-integration.md)
- [Server-side callers and vanilla client](references/server-callers.md)
- [Adapter setup for standalone, Express, Fastify, and Hono](references/adapter-setup.md)
- [Subscriptions and real-time patterns](references/subscriptions.md)
- [Testing tRPC procedures](references/testing-patterns.md)
