---
name: workleap-react-best-practices
description: React performance optimization guidelines for Single Page Applications (SPA) at Workleap. Use when writing, reviewing, or refactoring React SPA code to ensure optimal performance patterns. Triggers on tasks involving React components, state management, bundle optimization, re-render prevention, rendering performance, or JavaScript performance improvements. Covers async waterfall elimination, bundle size reduction, re-render optimization, rendering efficiency, JS micro-optimizations, and advanced React patterns. Does NOT cover server-side rendering (SSR), Next.js, or server components.
metadata:
  version: 1.0
---

# Workleap React Best Practices

Performance optimization guide for React Single Page Applications (SPA), tailored for Workleap's SPA-first architecture.

## When to Apply

Reference these guidelines when:
- Writing new React components
- Reviewing code for performance issues
- Refactoring existing React code
- Optimizing bundle size or load times
- Debugging unnecessary re-renders

## Rule Categories by Priority

| Priority | Category | Impact | Reference |
|----------|----------|--------|-----------|
| 1 | Eliminating Waterfalls | CRITICAL | [async-rules.md](references/async-rules.md) |
| 2 | Bundle Size Optimization | CRITICAL | [bundle-rules.md](references/bundle-rules.md) |
| 3 | Re-render Optimization | MEDIUM | [rerender-rules.md](references/rerender-rules.md) |
| 4 | Rendering Performance | MEDIUM | [rendering-rules.md](references/rendering-rules.md) |
| 5 | JavaScript Performance | LOW-MEDIUM | [js-rules.md](references/js-rules.md) |
| 6 | Advanced Patterns | LOW | [advanced-rules.md](references/advanced-rules.md) |

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)

Waterfalls are the #1 performance killer. Each sequential await adds full network latency.

- **Defer Await Until Needed** - Move await into branches where actually used
- **Promise.all() for Independent Operations** - Run independent async operations concurrently
- **Dependency-Based Parallelization** - Use promise chaining for partial dependencies
- **Prevent Waterfall Chains** - Start promises early, await late

Read [references/async-rules.md](references/async-rules.md) for detailed rules and code examples.

### 2. Bundle Size Optimization (CRITICAL)

Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

- **Route-Based Code Splitting** - Lazy-load each route so users only download code they visit
- **Avoid Barrel File Imports** - Import directly from source files, not barrel re-exports
- **React.lazy for Heavy Components** - Lazy-load large components not needed on initial render
- **Conditional Module Loading** - Load modules only when feature is activated
- **Preload on User Intent** - Preload heavy bundles on hover/focus

Read [references/bundle-rules.md](references/bundle-rules.md) for detailed rules and code examples.

### 3. Re-render Optimization (MEDIUM)

Reducing unnecessary re-renders minimizes wasted computation and improves UI responsiveness.

- **Defer State Reads** - Don't subscribe to state only used in callbacks
- **Extract to Memoized Components** - Enable early returns before computation
- **Hoist Default Non-primitive Props** - Extract default values to constants for stable memo
- **Narrow Effect Dependencies** - Use primitive dependencies in effects
- **Subscribe to Derived State** - Subscribe to derived booleans, not raw values
- **Calculate Derived State During Render** - Derive state during render, not effects
- **Functional setState** - Use functional setState for stable callbacks
- **Lazy State Initialization** - Pass function to useState for expensive values
- **Skip useMemo for Simple Expressions** - Avoid memo for simple primitives
- **Put Logic in Event Handlers** - Put interaction logic in event handlers, not effects
- **Transitions for Non-Urgent Updates** - Use startTransition for non-urgent updates
- **useRef for Transient Values** - Use refs for transient frequent values

Read [references/rerender-rules.md](references/rerender-rules.md) for detailed rules and code examples.

### 4. Rendering Performance (MEDIUM)

Optimizing the rendering process reduces the work the browser needs to do.

- **Animate SVG Wrapper** - Animate div wrapper, not SVG element
- **CSS content-visibility** - Use content-visibility for long lists
- **Hoist Static JSX** - Extract static JSX outside components
- **Optimize SVG Precision** - Reduce SVG coordinate precision
- **Activity Component (Experimental)** - Use Activity for show/hide with state preservation
- **Explicit Conditional Rendering** - Use ternary, not && for conditionals
- **useTransition for Loading** - Prefer useTransition over manual loading state

Read [references/rendering-rules.md](references/rendering-rules.md) for detailed rules and code examples.

### 5. JavaScript Performance (LOW-MEDIUM)

Micro-optimizations for hot paths that can add up to meaningful improvements.

- **Avoid Layout Thrashing** - Batch DOM writes, avoid interleaved reads
- **Build Index Maps** - Use Map for repeated lookups
- **Cache Property Access** - Cache object properties in loops
- **Cache Function Results** - Cache repeated function calls in module-level Map
- **Cache Storage API Calls** - Cache localStorage/sessionStorage reads
- **Combine Array Iterations** - Combine multiple filter/map into one loop
- **Early Length Check** - Check array length before expensive comparison
- **Early Return** - Return early from functions
- **Hoist RegExp** - Hoist RegExp creation outside loops
- **Loop for Min/Max** - Use loop instead of sort for min/max
- **Set/Map Lookups** - Use Set/Map for O(1) lookups
- **toSorted() Immutability** - Use toSorted() to prevent mutation bugs

Read [references/js-rules.md](references/js-rules.md) for detailed rules and code examples.

### 6. Advanced Patterns (LOW)

Advanced patterns for specific cases that require careful implementation.

- **Event Handler Refs** - Store event handlers in refs for stable subscriptions
- **Initialize Once** - Initialize app once per load, not per mount
- **Stable Callback Refs** - Stable callback refs for effects without re-runs

Read [references/advanced-rules.md](references/advanced-rules.md) for detailed rules and code examples.
