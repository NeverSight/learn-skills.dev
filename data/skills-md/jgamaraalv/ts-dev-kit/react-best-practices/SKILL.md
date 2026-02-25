---
name: react-best-practices
description: "React and Next.js performance patterns. Use when writing, reviewing, or optimizing React components."
---

# React & Next.js Performance Patterns

Performance optimization guide for React and Next.js applications, based on Vercel Engineering practices. 8 categories organized by impact.

## Table of Contents

- [When to Apply](#when-to-apply)
- [Quick Reference](#quick-reference)
  - [Async Patterns (CRITICAL)](#1-async-patterns-critical)
  - [Bundle Optimization (CRITICAL)](#2-bundle-optimization-critical)
  - [Server-Side Performance (HIGH)](#3-server-side-performance-high)
  - [Client-Side Patterns (MEDIUM-HIGH)](#4-client-side-patterns-medium-high)
  - [Re-render Optimization (MEDIUM)](#5-re-render-optimization-medium)
  - [Rendering Performance (MEDIUM)](#6-rendering-performance-medium)
  - [JavaScript Performance (LOW-MEDIUM)](#7-javascript-performance-low-medium)
  - [Advanced Patterns (LOW)](#8-advanced-patterns-low)

## When to Apply

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Optimizing bundle size or load times

## Quick Reference

### 1. Async Patterns (CRITICAL)

[references/async-patterns.md](references/async-patterns.md)

- Prevent waterfall chains in API routes -- start promises early, await late
- Defer await until needed -- move await into branches that use it
- Dependency-based parallelization -- `Promise.all()` with `.then()` chaining
- Strategic Suspense boundaries -- stream content with `<Suspense>`

### 2. Bundle Optimization (CRITICAL)

[references/bundle-optimization.md](references/bundle-optimization.md)

- Avoid barrel file imports -- import directly from source files
- Conditional module loading -- load only when feature is activated
- Defer non-critical third-party libraries -- load after hydration
- Dynamic imports for heavy components -- `next/dynamic` with `ssr: false`
- Preload on user intent -- preload on hover/focus

### 3. Server-Side Performance (HIGH)

[references/server-performance.md](references/server-performance.md)

- `after()` for non-blocking operations -- logging, analytics after response
- Authenticate Server Actions -- treat as public endpoints
- Cross-request LRU caching -- share data across sequential requests
- `React.cache()` deduplication -- per-request with primitive args
- Avoid duplicate RSC serialization -- transform in client, not server
- Parallel fetching via composition -- restructure component tree
- Minimize serialization at boundaries -- pass only needed fields

### 4. Client-Side Patterns (MEDIUM-HIGH)

[references/client-patterns.md](references/client-patterns.md)

- Deduplicate global event listeners -- `useSWRSubscription`
- Version and minimize localStorage -- schema versioning, try-catch
- Passive event listeners -- `{ passive: true }` for scroll performance
- SWR for automatic deduplication -- caching and revalidation

### 5. Re-render Optimization (MEDIUM)

[references/rerender-optimization.md](references/rerender-optimization.md)

- Defer state reads to usage point -- read in callbacks, not render
- Narrow effect dependencies -- use primitives, not objects
- Derive state during render -- no state + effect for computed values
- Functional setState -- stable callbacks, no stale closures
- Hoist default non-primitive props -- stable defaults for `memo()`
- Extract to memoized components -- skip computation with early returns
- Interaction logic in event handlers -- not state + effect
- useRef for transient values -- avoid re-render on frequent updates

### 6. Rendering Performance (MEDIUM)

[references/rendering-performance.md](references/rendering-performance.md)

- Animate SVG wrapper -- hardware-accelerated CSS on `<div>`, not `<svg>`
- CSS `content-visibility: auto` -- defer off-screen rendering
- Hoist static JSX -- extract constants outside components
- Prevent hydration mismatch -- inline script for client-only data
- `useTransition` over manual loading states -- built-in pending state

### 7. JavaScript Performance (LOW-MEDIUM)

[references/js-performance.md](references/js-performance.md)

- Avoid layout thrashing -- batch DOM reads and writes
- Cache repeated function calls -- module-level Map
- Cache storage API calls -- in-memory cache for localStorage/cookies
- Build index Maps for lookups -- O(1) instead of O(n) `.find()`
- Loop for min/max -- O(n) instead of O(n log n) sort

### 8. Advanced Patterns (LOW)

[references/advanced-patterns.md](references/advanced-patterns.md)

- Store event handlers in refs -- stable effect subscriptions
- Initialize app once per load -- module-level guard
