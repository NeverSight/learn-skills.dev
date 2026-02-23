---
name: react-performance
description: |
  React performance optimization patterns including memoization, code splitting, bundle size reduction, re-render elimination, and profiling. Covers React Compiler automatic optimization, manual memo/useMemo/useCallback targeting, React.lazy with Suspense, barrel file avoidance, content-visibility for large lists, startTransition for non-urgent updates, and React DevTools profiling.

  Use when optimizing React app performance, reducing bundle size, eliminating unnecessary re-renders, debugging slow components, code splitting, or profiling rendering bottlenecks. Use for performance audit, bundle analysis, re-render diagnosis, lazy loading, virtualization.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://react.dev/learn/react-compiler'
---

# React Performance

## Overview

Dedicated performance optimization skill for React applications. Covers the full spectrum from build-time optimizations (code splitting, barrel file avoidance) through runtime techniques (memoization, transitions, content-visibility) to diagnostic tooling (React DevTools Profiler, bundle analyzers).

**When to use:** Reducing Time to Interactive, shrinking bundle size, eliminating re-renders, profiling slow components, optimizing large lists, lazy loading heavy dependencies, auditing React app performance.

**When NOT to use:** General React component patterns (use `react-patterns` skill), framework-specific optimizations like Next.js caching (use framework skill), non-React performance (network, database, CDN).

## Quick Reference

| Category    | Technique                    | Key Points                                                                            |
| ----------- | ---------------------------- | ------------------------------------------------------------------------------------- |
| Compiler    | React Compiler               | Automatic memoization at build time; eliminates manual memo/useMemo/useCallback       |
| Memoization | `React.memo(Component)`      | Wrap components receiving stable primitive props from frequently re-rendering parents |
| Memoization | `useMemo(fn, deps)`          | Expensive computations only: sorting, filtering, Set/Map construction                 |
| Memoization | `useCallback(fn, deps)`      | Only when passed to memoized children; use functional setState for stable refs        |
| Splitting   | `React.lazy(() => import())` | Lazy-load heavy components with `<Suspense>` fallback                                 |
| Splitting   | Preload on intent            | Trigger `import()` on hover/focus for perceived speed                                 |
| Bundle      | Direct imports               | Avoid barrel files; import from specific paths to reduce module count                 |
| Bundle      | Defer third-party            | Load analytics, logging after hydration                                               |
| Re-renders  | `startTransition`            | Mark non-urgent updates (search, scroll tracking) as interruptible                    |
| Re-renders  | Functional setState          | `setState(prev => ...)` eliminates state dependencies from callbacks                  |
| Re-renders  | Derived state                | Subscribe to booleans, not continuous values; compute during render                   |
| Re-renders  | Defer state reads            | Read dynamic state (searchParams) inside callbacks, not at render                     |
| Rendering   | `content-visibility: auto`   | Skip layout/paint for off-screen items in long lists                                  |
| Rendering   | Hoist static JSX             | Extract constant elements outside component functions                                 |
| Profiling   | React DevTools Profiler      | Record renders, identify slow components, flamegraph analysis                         |
| Profiling   | Bundle analyzer              | Visualize chunk sizes, find oversized dependencies                                    |

## Common Mistakes

| Mistake                                                            | Correct Pattern                                                                             |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Wrapping everything in useMemo/useCallback                         | Trust React Compiler first; only memoize expensive computations or memoized-child callbacks |
| Memoizing cheap operations like `value * 2`                        | Skip memo for simple primitives; overhead exceeds recomputation cost                        |
| Importing from barrel files (`lucide-react`, `@mui/material`)      | Import directly from specific paths or use `optimizePackageImports`                         |
| Loading analytics/tracking in the initial bundle                   | Defer with lazy + mounted state to load after hydration                                     |
| Subscribing to continuous values (window width) for boolean checks | Use `useMediaQuery` or derived boolean to re-render only on threshold change                |
| Referencing state in useCallback dependency array                  | Use functional setState `setState(prev => ...)` for stable callbacks                        |
| Using `useEffect` to derive state from props                       | Compute derived values during render; effects add an extra render cycle                     |
| Creating new object literals as props on every render              | Hoist static objects outside component; use useMemo for dynamic objects                     |
| Profiling in development mode                                      | Always profile production builds; dev mode includes extra warnings that skew results        |

## Delegation

- **Profile and diagnose performance bottlenecks**: Use `Explore` agent to run React DevTools Profiler, analyze bundle composition, and trace re-render cascades
- **Apply performance optimizations to existing code**: Use `Task` agent to implement code splitting, add memoization boundaries, and optimize rendering
- **Plan performance improvement strategy**: Use `Plan` agent to prioritize optimizations by impact (waterfalls > bundle > re-renders) and create an optimization roadmap

> If the `react-patterns` skill is available, delegate general component architecture and React 19 API questions to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill react-patterns`

## References

- [Rendering optimization: memo, useMemo, useCallback, compiler, re-render elimination](references/rendering-optimization.md)
- [Code splitting: React.lazy, Suspense, dynamic imports, bundle optimization](references/code-splitting.md)
- [Profiling and debugging: DevTools, performance measurement, common bottlenecks](references/profiling-and-debugging.md)
