---
name: cloudwerk-routing
description: File-based routing conventions for Cloudwerk, a full-stack framework for Cloudflare Workers. Use when creating pages, API routes, layouts, middleware, or error boundaries. Triggers on tasks involving route files (page.tsx, route.ts, layout.tsx, middleware.ts, error.tsx, not-found.tsx), dynamic segments ([id], [...slug]), route groups ((group)), loaders, actions, or data loading patterns.
license: MIT
metadata:
  author: squirrelsoft
  version: "0.1.0"
---

# Cloudwerk Routing

File-based routing conventions for Cloudwerk. The `app/` directory structure maps directly to URL patterns, with special filenames determining behavior.

## When to Apply

Reference these guidelines when:
- Creating new pages or API routes in a Cloudwerk app
- Adding layouts that wrap multiple pages
- Implementing middleware for auth, rate limiting, or request processing
- Using dynamic route segments (`[id]`, `[...slug]`)
- Loading data with `loader()` or handling mutations with `action()`
- Adding error or not-found boundaries

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Route Files | CRITICAL | `files-` |
| 2 | Dynamic Parameters | HIGH | `params-` |
| 3 | Data Loading | HIGH | `data-` |

## Quick Reference

### 1. Route Files (CRITICAL)

- `files-page-component` - page.tsx conventions for rendering UI
- `files-api-route` - route.ts conventions for API endpoints
- `files-layout` - layout.tsx conventions for shared UI wrappers
- `files-middleware` - middleware.ts conventions for request processing
- `files-error-boundary` - error.tsx conventions for error handling
- `files-not-found-boundary` - not-found.tsx conventions for 404 pages

### 2. Dynamic Parameters (HIGH)

- `params-dynamic-segments` - [id] syntax for single dynamic segments
- `params-catch-all` - [...slug] syntax for catch-all routes
- `params-route-groups` - (group) syntax for layout grouping without URL impact

### 3. Data Loading (HIGH)

- `data-loader` - loader() function for server-side data fetching
- `data-action` - action() function for form submissions and mutations
- `data-error-control-flow` - NotFoundError/RedirectError for flow control
- `data-context-api` - getContext(), get(), set() for request-scoped data

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/files-page-component.md
rules/data-loader.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
