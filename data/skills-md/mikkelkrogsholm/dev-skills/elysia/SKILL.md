---
name: elysia
description: "Elysia — Bun-native web framework with end-to-end type safety and Eden Treaty typed client. Use when building with Elysia or asking about its routing, plugins, lifecycle hooks, validation, Eden Treaty, WebSocket, SSE, or integration with Bun. Fetch live documentation for up-to-date details."
---

# Elysia

> **CRITICAL: Your training data for Elysia is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://elysiajs.com/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume an API exists — verify against current docs.

Elysia is a Bun-native web framework designed for end-to-end type safety. Types flow from server route definitions to the client via Eden Treaty — no codegen, no manual type syncing.
## Key Capabilities

Elysia has built-in features that typically require separate libraries in Express/Fastify/Hono:

- **End-to-end type safety**: Eden Treaty generates a fully typed client from route definitions — no tRPC, no OpenAPI codegen, no manual type files
- **Schema validation**: Built-in `t.Object()`, `t.String()`, etc. (TypeBox) for request/response validation — no Zod middleware needed
- **WebSocket**: First-class WS support with typed message schemas — no `ws` or `socket.io`
- **Server-Sent Events**: Native SSE support via streaming responses — no `eventsource` polyfill
- **Swagger/OpenAPI**: Auto-generated from route schemas via `@elysiajs/swagger` — no manual spec writing
- **Static files**: `@elysiajs/static` serves files with caching headers — no `serve-static`
- **CORS**: `@elysiajs/cors` with typed config — no `cors` package
- **Bearer auth**: `@elysiajs/bearer` extracts and validates tokens — no custom middleware
- **File uploads**: Native `t.File()` and `t.Files()` validators for multipart handling

## Best Practices

**Use `.group()` for route organization, not separate Elysia instances.** Groups share the parent's type context and lifecycle hooks. Creating separate `new Elysia()` instances and merging with `.use()` works, but loses the type-level connection that makes Eden Treaty useful across route boundaries.

**Eden Treaty requires exporting the app type, not the app.** The client needs `typeof app`, not the runtime instance. A common mistake:

```ts
// server
const app = new Elysia()
  .get('/users', () => getUsers())
  .listen(3000)

export type App = typeof app  // ← this is what Eden needs

// client
import type { App } from '../api'
import { treaty } from '@elysiajs/eden'
const api = treaty<App>('localhost:3000')
const { data } = await api.users.get()  // fully typed
```

**Lifecycle hooks run in a specific order.** The chain is: `onRequest` → `onParse` → `onTransform` → `onBeforeHandle` → handler → `onAfterHandle` → `onMapResponse` → `onAfterResponse`. Auth guards belong in `onBeforeHandle`, not `onRequest` — putting them in `onRequest` runs before body parsing, so you can't read the request body for auth decisions.

**`derive` and `resolve` add typed context.** Use `derive` to add request-scoped values (runs on every request) and `resolve` for values that depend on validation (runs after schema validation). Both inject into the handler's typed context automatically — no manual type annotations needed.

**Schema validation doubles as documentation.** Every `t.Object()` schema on a route is automatically reflected in the Swagger UI. Adding `t.String({ description: 'User ID' })` improves both validation errors and API docs simultaneously.

**Error handling uses `error()` helper, not thrown exceptions.** Return `error(404, 'Not found')` instead of `throw new Error()`. The `error()` helper preserves type safety in the response type — thrown exceptions lose type information and bypass `onAfterHandle`.
