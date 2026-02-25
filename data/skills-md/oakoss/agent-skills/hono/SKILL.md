---
name: hono
description: 'Hono ultrafast web framework for edge and server runtimes. Use when building APIs, middleware chains, or edge functions on Cloudflare Workers, Bun, Node.js, or Deno. Use for hono, api, routing, middleware, cloudflare-workers, edge, rpc, validator, context.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://hono.dev/docs/'
user-invocable: false
---

# Hono

## Overview

Hono is a small, ultrafast web framework built on Web Standards that runs on any JavaScript runtime including Cloudflare Workers, Bun, Deno, Node.js, Vercel, and AWS Lambda. Application code is portable across runtimes; only the entry point and adapter differ per platform.

**When to use:** Edge-first APIs, Cloudflare Workers services, multi-runtime applications, lightweight REST/RPC servers, middleware-heavy request pipelines, type-safe client-server communication.

**When NOT to use:** Full-stack SSR frameworks (use Next.js/Remix), heavy ORM-driven monoliths where Express ecosystem maturity matters, applications that need deep Node.js-only APIs without Web Standard equivalents.

## Quick Reference

| Pattern           | API                                         | Key Points                                  |
| ----------------- | ------------------------------------------- | ------------------------------------------- |
| Basic routing     | `app.get('/path', handler)`                 | Supports get, post, put, delete, patch, all |
| Path parameters   | `app.get('/user/:id', handler)`             | Access via `c.req.param('id')`              |
| Regex constraints | `app.get('/post/:id{[0-9]+}', handler)`     | Inline regex in path parameter              |
| Wildcard          | `app.get('/files/*', handler)`              | Matches any sub-path                        |
| Route grouping    | `app.route('/api', subApp)`                 | Mount sub-applications                      |
| Middleware        | `app.use(middleware())`                     | Executes in registration order              |
| Path middleware   | `app.use('/auth/*', jwt(...))`              | Scope middleware to paths                   |
| JSON response     | `c.json({ key: 'value' })`                  | Sets Content-Type automatically             |
| Text response     | `c.text('hello')`                           | Returns plain text                          |
| HTML response     | `c.html('<h1>Hi</h1>')`                     | Returns HTML content                        |
| Status + header   | `c.status(201)`, `c.header('X-Key', 'val')` | Chain before response                       |
| Redirect          | `c.redirect('/new-path', 301)`              | Default status is 302                       |
| Request body      | `c.req.json()`, `c.req.parseBody()`         | JSON or form data parsing                   |
| Query params      | `c.req.query('page')`                       | Single query parameter                      |
| Context variables | `c.set('user', data)` / `c.get('user')`     | Type-safe middleware data passing           |
| Zod validation    | `zValidator('json', schema)`                | `@hono/zod-validator` package               |
| RPC client        | `hc<AppType>(url)`                          | End-to-end type-safe API calls              |
| Error handler     | `app.onError((err, c) => ...)`              | Global error handling                       |
| Not found         | `app.notFound((c) => ...)`                  | Custom 404 handler                          |
| Environment       | `c.env.BINDING_KEY`                         | Access runtime bindings/env vars            |
| Adapter helper    | `env(c)` from `hono/adapter`                | Unified env access across runtimes          |
| WebSocket         | `upgradeWebSocket()` from runtime adapter   | WebSocket helper with RPC support           |
| Test client       | `testClient(app)` from `hono/testing`       | Type-safe testing without HTTP server       |
| JSX streaming     | `jsxRenderer({ stream: true })`             | SSR streaming with Suspense support         |

## Common Mistakes

| Mistake                                                             | Correct Pattern                                                                      |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Registering middleware after handlers                               | Register middleware before the handlers it should apply to                           |
| Using `app.route()` without chaining for RPC types                  | Chain route methods (`app.route('/a', a).route('/b', b)`) and export `typeof routes` |
| Forgetting `export default app` for edge runtimes                   | Cloudflare Workers, Bun, and Deno require the default export                         |
| Using `compress()` on Cloudflare Workers or Deno Deploy             | These platforms compress automatically; skip the middleware                          |
| Mixing Hono and middleware versions in Deno                         | Pin all `hono` imports to the same version to avoid type mismatches                  |
| Wrapping `next()` in try/catch inside middleware                    | Hono catches thrown errors and routes to `app.onError()`; `next()` never throws      |
| Defining routes with `app.get()` but exporting `typeof app` for RPC | Export the type of the chained route variable, not the app instance                  |
| Using `new Hono()` without generics for typed context               | Pass `Hono<{ Variables: MyVars }>` to enable typed `c.get()`/`c.set()`               |
| Returning `c.json()` without status for created resources           | Pass status as second argument: `c.json(data, 201)`                                  |
| Not using `createMiddleware()` for reusable middleware              | Import from `hono/factory` to preserve type inference when extracting middleware     |

## Delegation

> If the `zod` or `typescript-patterns` skill is available, delegate schema and type-level tasks to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill typescript-patterns`
>
> If a Cloudflare Workers skill is available, delegate platform-specific configuration to it.

## References

- [Route definitions, path params, groups, and method handlers](references/routing.md)
- [Built-in and custom middleware patterns](references/middleware.md)
- [Context object, request parsing, and response helpers](references/context-and-helpers.md)
- [Zod validator middleware and request validation](references/validation.md)
- [RPC client and end-to-end type safety](references/rpc-client.md)
- [Runtime adapters for Cloudflare, Bun, Node.js, Deno, and more](references/adapters.md)
- [Testing with testClient, WebSocket helper, and JSX streaming](references/testing-and-websocket.md)
