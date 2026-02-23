---
name: react-error-handling
description: 'React error boundaries and fallback UIs for catching rendering errors. Use when handling component crashes, displaying error states, implementing error recovery, or preventing full-page crashes. Use for ErrorBoundary, componentDidCatch, getDerivedStateFromError, error fallback, error recovery, crash handling, react-error-boundary library.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary'
---

# React Error Handling

## Overview

Error boundaries catch JavaScript errors during rendering, in lifecycle methods, and in constructors of child components. They display fallback UIs instead of crashing the entire component tree. Error boundaries can only be implemented as class components in vanilla React, but the `react-error-boundary` library provides a convenient function component wrapper.

**When to use:** Component crashes, preventing error propagation to parent routes, graceful degradation, user-facing error states, error logging and monitoring.

**When NOT to use:** Event handler errors (use try/catch), async callbacks outside rendering (setTimeout, promises without Suspense), server-side rendering errors, errors in the boundary itself.

## Quick Reference

| Pattern               | API                                                        | Key Points                                 |
| --------------------- | ---------------------------------------------------------- | ------------------------------------------ |
| Class boundary        | `getDerivedStateFromError` + `componentDidCatch`           | Manual implementation, full control        |
| Function boundary     | `<ErrorBoundary FallbackComponent={...} />`                | Uses react-error-boundary library          |
| Reset mechanism       | `resetErrorBoundary()` or `resetKeys={[dep]}`              | Auto-reset on state change or manual retry |
| Error logging         | `onError={(error, info) => log(error)}`                    | Log to analytics or monitoring service     |
| Fallback component    | `FallbackComponent={MyFallback}`                           | Receives error and resetErrorBoundary      |
| Inline fallback       | `fallback={<div>Error occurred</div>}`                     | Static JSX, no error details               |
| Render prop fallback  | `fallbackRender={({ error, reset }) => <UI />}`            | Dynamic fallback with error access         |
| Nested boundaries     | Wrap at multiple tree levels                               | Granular error isolation                   |
| Route-level boundary  | TanStack Router `errorComponent`                           | Delegate to tanstack-router skill          |
| Suspense integration  | Wrap Suspense boundaries for async errors                  | Catch errors thrown by Suspense            |
| Event handler errors  | `try/catch` in handler, not error boundary                 | Boundaries don't catch event errors        |
| useErrorBoundary hook | `const { showBoundary, resetBoundary } = useErrorBoundary` | Manually trigger boundary from child       |

## Common Mistakes

| Mistake                          | Correct Pattern                                         |
| -------------------------------- | ------------------------------------------------------- |
| Using error boundary for events  | Use try/catch in event handlers                         |
| Wrapping every single component  | Place boundaries at meaningful UI sections              |
| Not providing reset mechanism    | Include retry button or resetKeys                       |
| Showing stack traces in prod     | Only render stack in development mode                   |
| Missing onError for logging      | Always log errors to monitoring service                 |
| Catching errors in boundary self | Error boundaries only catch child component errors      |
| Using async code in getDerived   | getDerivedStateFromError must be pure, use didCatch     |
| Relying on componentDidCatch     | Use getDerivedStateFromError for state updates          |
| Not testing error boundaries     | Test with error-throwing components                     |
| Ignoring resetKeys pattern       | Use resetKeys for automatic recovery on state change    |
| Blocking Suspense fallbacks      | Error boundaries around Suspense should allow fallbacks |

## Delegation

> If the `tanstack-router` skill is available, delegate route-level error handling (errorComponent, notFoundComponent, loader errors) to it. Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-router`

- **Error monitoring setup**: Delegate to integration/observability specialists
- **Complex recovery flows**: Use `Task` agent for multi-step error recovery patterns
- **Error boundary testing**: Delegate test writing to testing specialists

## References

- [Class-based error boundaries](references/class-boundaries.md)
- [react-error-boundary library](references/react-error-boundary.md)
- [Fallback UI patterns](references/fallback-patterns.md)
- [Reset and recovery patterns](references/reset-recovery.md)
- [Error boundary placement strategies](references/boundary-placement.md)
