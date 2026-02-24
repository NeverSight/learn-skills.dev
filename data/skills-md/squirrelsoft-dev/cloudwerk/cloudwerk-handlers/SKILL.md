---
name: cloudwerk-handlers
description: Handler, middleware, and component patterns for Cloudwerk applications on Cloudflare Workers. Use when writing route handlers, middleware, page/layout components, or client-side interactive components. Triggers on tasks involving CloudwerkHandler, response helpers (json, redirect), Cloudflare bindings (D1, KV, R2), middleware composition, PageProps, LayoutProps, or client directives.
license: MIT
metadata:
  author: squirrelsoft
  version: "0.1.0"
---

# Cloudwerk Handlers

Handler, middleware, and component patterns for Cloudwerk applications. Covers the signature conventions for route handlers, middleware, and page/layout components, plus how to use Cloudflare bindings and response helpers.

## When to Apply

Reference these guidelines when:
- Writing API route handlers (GET, POST, PUT, DELETE)
- Creating middleware for authentication, rate limiting, or logging
- Building page or layout components with data loading
- Accessing Cloudflare bindings (D1, KV, R2)
- Using response helpers like `json()`, `redirect()`
- Creating client-side interactive components with `'use client'`

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Handler Patterns | CRITICAL | `handler-` |
| 2 | Middleware Patterns | HIGH | `middleware-` |
| 3 | Component Patterns | HIGH | `component-` |

## Quick Reference

### 1. Handler Patterns (CRITICAL)

- `handler-signature` - CloudwerkHandler function pattern and params
- `handler-response-helpers` - json(), redirect(), notFoundResponse() helpers
- `handler-bindings` - getBinding(), DB, KV, R2 access patterns

### 2. Middleware Patterns (HIGH)

- `middleware-signature` - (request, next) => Response pattern
- `middleware-data-sharing` - set()/get() via context for passing data
- `middleware-vs-hono` - Differences from Hono middleware

### 3. Component Patterns (HIGH)

- `component-page-props` - PageProps interface and loader data
- `component-layout-props` - LayoutProps interface with children
- `component-client-directive` - 'use client' for interactive components
- `component-hono-vs-react` - class vs className and renderer differences

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/handler-signature.md
rules/middleware-signature.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
