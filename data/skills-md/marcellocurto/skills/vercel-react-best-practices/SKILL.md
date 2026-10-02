---
name: vercel-react-best-practices
description: Apply Vercel's React and Next.js performance guidance when writing or reviewing code.
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React Best Practices

Repository-maintained React and Next.js guidance adapted from Vercel's rules. Use it to address a concrete performance mechanism in the requested work, not to apply every listed pattern across an application.

## Establish relevance before optimizing

Identify the affected path, realistic workload, and avoidable cost: a dependency waterfall, repeated request, excessive bundle, expensive render, or hot computation. Support that mechanism with code and usage evidence or a representative trace/profile. A rule match or an impact label alone does not justify a change.

Preserve the user's scope, existing architecture, and correctness contracts. Prefer an existing facility or direct code change before adding a library, cache, or abstraction. Leave already-adequate code alone when the proposed optimization has no meaningful expected benefit. Correctness and security obligations do not depend on proving a performance gain.

Measure before and after when making a performance claim, using comparable workloads and conditions. If measurement is unavailable, explain the supported mechanism and label the benefit as expected or unverified. Do not turn example timings, percentages, or impact ratings into measured results for the user's application.

## Dependencies and cache ownership

SWR, `better-all`, LRU caches, and memoization are conditional options. Reuse the project's data-fetching, scheduling, or caching facilities when they meet the need. Add a dependency only when a demonstrated requirement justifies its maintenance and runtime cost; an example import is not an instruction to install it.

Before adding a cache, establish repeated work, suitable key identity, the owner and lifetime, acceptable staleness, invalidation, memory bounds, and any user or tenant isolation required by the data. Choose the narrowest useful scope. Do not cache mutable or authorization-dependent results without preserving those contracts.

## When to Apply

Reference these guidelines when:
- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing code for performance issues
- Refactoring existing React/Next.js code
- Optimizing bundle size or load times

## Rule Categories by Priority

These ratings are relative priorities for investigation under applicable conditions. Numerical gains in rules are illustrative or source-specific, not guarantees or measurements of the current application. In review, assess severity from demonstrated impact rather than copying a rule's rating.

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

- `async-cheap-condition-before-await` - Check cheap sync conditions before awaiting flags or remote values
- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Express real dependencies directly; consider better-all when it earns its place
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-analyzable-paths` - Prefer statically analyzable import and file-system paths to avoid broad bundles and traces
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

### 3. Server-Side Performance (HIGH)

- `server-auth-actions` - Authenticate server actions like API routes
- `server-cache-react` - Consider React.cache() for repeated work within a supported server render
- `server-cache-lru` - Consider bounded cross-request caching when freshness and isolation allow reuse
- `server-dedup-props` - Avoid duplicate serialization in RSC props
- `server-hoist-static-io` - Hoist static I/O (fonts, logos) to module level
- `server-no-shared-module-state` - Avoid module-level mutable request state in RSC/SSR
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-parallel-nested-fetching` - Chain nested fetches per item in Promise.all
- `server-after-nonblocking` - Use after() for non-blocking operations

### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Reuse request deduplication; consider SWR when it fits the project's data layer
- `client-event-listeners` - Deduplicate global event listeners
- `client-passive-event-listeners` - Use passive listeners for scroll
- `client-localstorage-schema` - Version and minimize localStorage data

### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-memo-with-default-value` - Hoist default non-primitive props
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-derived-state-no-effect` - Derive state during render, not effects
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-simple-expression-in-memo` - Avoid memo for simple primitives
- `rerender-split-combined-hooks` - Split hooks with independent dependencies
- `rerender-move-effect-to-event` - Put interaction logic in event handlers
- `rerender-transitions` - Use startTransition for non-urgent updates
- `rerender-use-deferred-value` - Defer expensive renders to keep input responsive
- `rerender-use-ref-transient-values` - Use refs for transient frequent values
- `rerender-no-inline-components` - Don't define components inside components

### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-hydration-suppress-warning` - Suppress expected mismatches
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals
- `rendering-usetransition-loading` - Prefer useTransition for loading state
- `rendering-resource-hints` - Use React DOM resource hints for preloading
- `rendering-script-defer-async` - Use defer or async on script tags

### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache costly repeated computation only with suitable keys and lifetime
- `js-cache-storage` - Cache hot storage reads only with a reliable invalidation policy
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability
- `js-flatmap-filter` - Use flatMap to map and filter in one pass
- `js-request-idle-callback` - Defer non-critical work to browser idle time

### 8. Advanced Patterns (LOW)

- `advanced-effect-event-deps` - Don't put `useEffectEvent` results in effect deps
- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-init-once` - Initialize app once per app load
- `advanced-use-latest` - useLatest for stable callback refs

## How to Use

Use the index to select the rules relevant to the identified mechanism. Read those individual files and their applicable examples; load additional rules only when a concrete dependency or unresolved question requires them. Do not read the entire compiled guide by default.

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

Interpret example labels within their stated workload and assumptions. Preserve framework/version compatibility and actual error, ordering, caching, and ownership contracts when adapting an example.

## Compiled Reference

`rules/` contains the canonical guidance. `AGENTS.md` is a compiled reference for deliberate full-guide reading, not the runtime entry point. When maintaining a rule, synchronize its compiled section and any affected index or metadata in the same change; see this skill's `README.md` for maintenance details.
