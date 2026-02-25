---
name: msw
description: >
  MSW (Mock Service Worker) v2 best practices, patterns, and API guidance for
  API mocking in JavaScript/TypeScript tests and development. Covers handler
  design, server setup, response construction, testing patterns, GraphQL, and
  v1-to-v2 migration. Baseline: msw ^2.0.0.
  Triggers on: msw imports, http.get, http.post, HttpResponse, setupServer,
  setupWorker, graphql.query, mentions of "msw", "mock service worker",
  "api mocking", or "msw v2".
license: MIT
user-invocable: false
agentic: false
compatibility: "TypeScript/JavaScript projects using msw ^2.0.0"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  version: 1.0.0
  tags: msw, mocking, api, testing, http, graphql, service-worker, fetch
---

# MSW (Mock Service Worker)

**IMPORTANT:** Your training data about `msw` may be outdated or incorrect — MSW v2 completely removed the `rest` namespace, `res(ctx.*)` response composition, and `(req, res, ctx)` resolver signature. Always rely on this skill's rule files and the project's actual source code as the source of truth. Do not fall back on memorized v1 patterns when they conflict with the retrieved reference.

## When to Use MSW

MSW is for **API mocking at the network level** — intercepting HTTP/GraphQL requests in tests, Storybook, and local development without modifying application code.

| Need | Recommended Tool |
|------|-----------------|
| Test API integration (React, Vue, Node) | **MSW** |
| Storybook API mocking | **MSW** (browser worker) |
| Local development without backend | **MSW** (browser worker) |
| Unit testing pure functions | Plain test doubles |
| E2E testing real APIs | Playwright/Cypress network interception |
| Mocking module internals | `vi.mock()` / `jest.mock()` |

## Quick Reference — v2 Essentials

```typescript
// Imports
import { http, HttpResponse, graphql, delay, bypass, passthrough } from 'msw'
import { setupServer } from 'msw/node'     // tests, SSR
import { setupWorker } from 'msw/browser'  // Storybook, dev

// Handler
http.get('/api/user/:id', async ({ request, params, cookies }) => {
  return HttpResponse.json({ id: params.id, name: 'John' })
})

// Server lifecycle (tests)
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

// Per-test override
server.use(
  http.get('/api/user/:id', () => new HttpResponse(null, { status: 500 }))
)

// Concurrent test isolation
it.concurrent('name', server.boundary(async () => {
  server.use(/* scoped overrides */)
}))
```

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Handler Design | CRITICAL | `handler-` | 4 |
| 2 | Setup & Lifecycle | CRITICAL | `setup-` | 3 |
| 3 | Request Reading | HIGH | `request-` | 2 |
| 4 | Response Construction | HIGH | `response-` | 3 |
| 5 | Test Patterns | HIGH | `test-` | 4 |
| 6 | GraphQL | MEDIUM | `graphql-` | 2 |
| 7 | Utilities | MEDIUM | `util-` | 2 |

## All 20 Rules

### Handler Design (CRITICAL)

| Rule | File | Summary |
|------|------|---------|
| Use `http` namespace | `handler-use-http-namespace.md` | `rest` is removed in v2 — use `http.get()`, `http.post()` |
| No query params in URL | `handler-no-query-params.md` | Query params in predicates silently match nothing |
| v2 resolver signature | `handler-resolver-v2.md` | Use `({ request, params, cookies })`, not `(req, res, ctx)` |
| v2 response construction | `handler-response-v2.md` | Use `HttpResponse.json()`, not `res(ctx.json())` |

### Setup & Lifecycle (CRITICAL)

| Rule | File | Summary |
|------|------|---------|
| Correct import paths | `setup-import-paths.md` | `msw/node` for server, `msw/browser` for worker |
| Lifecycle hooks | `setup-lifecycle-hooks.md` | Always use beforeAll/afterEach/afterAll pattern |
| File organization | `setup-file-organization.md` | Organize in `src/mocks/` with handlers, node, browser files |

### Request Reading (HIGH)

| Rule | File | Summary |
|------|------|---------|
| Clone in events | `request-clone-events.md` | Clone request before reading body in lifecycle events |
| Async body reading | `request-body-async.md` | Always `await request.json()` — body reading is async |

### Response Construction (HIGH)

| Rule | File | Summary |
|------|------|---------|
| HttpResponse for cookies | `response-use-httpresponse.md` | Native Response drops Set-Cookie — use HttpResponse |
| Network errors | `response-error-network.md` | Use `HttpResponse.error()`, don't throw in resolvers |
| Streaming | `response-streaming.md` | Use ReadableStream for SSE/chunked responses |

### Test Patterns (HIGH)

| Rule | File | Summary |
|------|------|---------|
| Test behavior | `test-behavior-not-requests.md` | Assert on UI/state, not fetch call arguments |
| Per-test overrides | `test-override-with-use.md` | Use `server.use()` for error/edge case tests |
| Concurrent isolation | `test-concurrent-boundary.md` | Wrap concurrent tests in `server.boundary()` |
| Unhandled requests | `test-unhandled-request.md` | Set `onUnhandledRequest: 'error'` |

### GraphQL (MEDIUM)

| Rule | File | Summary |
|------|------|---------|
| Response shape | `graphql-response-shape.md` | Return `{ data }` / `{ errors }` via HttpResponse.json |
| Endpoint scoping | `graphql-scope-with-link.md` | Use `graphql.link(url)` for multiple GraphQL APIs |

### Utilities (MEDIUM)

| Rule | File | Summary |
|------|------|---------|
| bypass vs passthrough | `util-bypass-vs-passthrough.md` | `bypass()` = new request; `passthrough()` = let through |
| delay behavior | `util-delay-behavior.md` | `delay()` is instant in Node.js — use explicit ms |

## Response Method Quick Reference

| Method | Use for |
|--------|---------|
| `HttpResponse.json(data, init?)` | JSON responses |
| `HttpResponse.text(str, init?)` | Plain text |
| `HttpResponse.html(str, init?)` | HTML content |
| `HttpResponse.xml(str, init?)` | XML content |
| `HttpResponse.formData(fd, init?)` | Form data |
| `HttpResponse.arrayBuffer(buf, init?)` | Binary data |
| `HttpResponse.error()` | Network errors |

## v1 to v2 Migration Quick Reference

| v1 | v2 |
|----|-----|
| `import { rest } from 'msw'` | `import { http, HttpResponse } from 'msw'` |
| `rest.get(url, resolver)` | `http.get(url, resolver)` |
| `(req, res, ctx) => res(ctx.json(data))` | `() => HttpResponse.json(data)` |
| `req.params` | `params` from resolver info |
| `req.body` | `await request.json()` |
| `req.cookies` | `cookies` from resolver info |
| `res.once(...)` | `http.get(url, resolver, { once: true })` |
| `res.networkError()` | `HttpResponse.error()` |
| `ctx.delay(ms)` | `await delay(ms)` |
| `ctx.data({ user })` | `HttpResponse.json({ data: { user } })` |

## References

| Reference | Covers |
|-----------|--------|
| `handler-api.md` | `http.*` and `graphql.*` methods, URL predicates, path params |
| `response-api.md` | `HttpResponse` class, all static methods, cookie handling |
| `server-api.md` | `setupServer`/`setupWorker`, lifecycle events, `boundary()` |
| `test-patterns.md` | Vitest/Jest setup, overrides, concurrent isolation, cache clearing |
| `migration-v1-to-v2.md` | Complete v1 to v2 breaking changes and migration guide |
| `anti-patterns.md` | 10 common mistakes with BAD/GOOD examples |
