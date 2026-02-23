---
name: hydration-guardian
description: >
  Ensures zero-mismatch integrity between server-rendered HTML and client-side
  React trees. Use when debugging hydration errors, fixing text content
  mismatches, handling browser extension DOM pollution, implementing selective
  hydration with Suspense, using the React 19 use() hook for deterministic
  server-to-client data bridges, or applying Next.js use cache for data drift
  prevention. Use for hydration mismatch, SSR, hydrateRoot, suppressHydrationWarning,
  onRecoverableError, two-pass rendering.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://react.dev/reference/react-dom/client/hydrateRoot'
---

# Hydration Guardian

## Overview

Ensures zero-mismatch integrity between server-rendered HTML and client-side React trees. Covers hydration error diagnosis, selective hydration via Suspense boundaries, deterministic data bridges with the React 19 `use()` hook, `'use cache'` for eliminating data drift, two-pass rendering for client-only content, React 19's single-diff hydration error reporting for pinpointing exact mismatches, and automated validation of rendered DOM state.

**When to use:** Debugging hydration mismatch errors, fixing text content mismatches, handling browser extension DOM pollution, implementing deterministic data bridges, optimizing SSR/client hydration performance, setting up error monitoring with `onRecoverableError`.

**When NOT to use:** Client-only React applications without SSR, static sites without hydration, API-only backends.

## Quick Reference

| Pattern              | Approach                                   | Key Points                                                 |
| -------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| Selective hydration  | `<Suspense fallback={...}>` boundary       | Hydrates independently; prioritizes user interaction       |
| Deterministic bridge | `use(serverPromise)` instead of useEffect  | Seamless server-to-client data transition (React 19)       |
| Cache directive      | `'use cache'` in data fetchers             | Share exact server result with client during hydration     |
| Two-pass rendering   | `useState` + `useEffect` for client-only   | First render matches server; second adds client content    |
| Client-only skip     | `next/dynamic` with `ssr: false`           | Exclude component from server render entirely              |
| Error monitoring     | `onRecoverableError` on `hydrateRoot`      | Detect and report silent hydration recovery                |
| Error reporting      | React 19 single-diff error format          | Pinpoints exact mismatch location with unified diff output |
| Error callbacks      | `onUncaughtError`, `onCaughtError`         | Granular error handling on `createRoot`/`hydrateRoot`      |
| Date/time safety     | UTC normalization or server-synced context | Prevent locale-dependent hydration mismatches              |
| Extension resilience | Test with common browser extensions active | Detect DOM pollution from translators, dark-mode tools     |

## Hydration Error Diagnosis

| Error Message                        | Likely Cause                                    | Corrective Action                                         |
| ------------------------------------ | ----------------------------------------------- | --------------------------------------------------------- |
| `Text content did not match`         | Non-deterministic render (dates, random values) | Use two-pass rendering or `suppressHydrationWarning`      |
| `Expected server HTML to contain`    | Client renders content server did not           | Move client-only code to `useEffect` or dynamic import    |
| `Hydration failed`                   | Invalid HTML nesting (`<p>` inside `<p>`)       | Fix HTML structure; browsers auto-correct causing drift   |
| `Extra attributes from server`       | Server-only attributes not on client            | Ensure attribute parity or use `suppressHydrationWarning` |
| `There was an error while hydrating` | Extension-modified DOM or major mismatch        | Check for browser extensions; verify HTML validity        |

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Using `suppressHydrationWarning` on container elements      | Fix the root cause; suppress only on leaf elements with unavoidable differences |
| Accessing `window` or `document` in the render body         | Wrap client-only code in `useEffect` or use `next/dynamic` with `ssr: false`    |
| Using `Math.random()` or `new Date()` without stable seeds  | Use UTC normalization, server-cached values, or two-pass rendering              |
| Ignoring silent hydration recovery in production            | Configure `onRecoverableError` on `hydrateRoot` to log and monitor              |
| Using `dangerouslySetInnerHTML` with server/client mismatch | Ensure identical content or use a dedicated `key` change to force remount       |
| Checking `typeof window !== 'undefined'` in render          | Use two-pass rendering; the check runs on server too (it returns false)         |
| Nesting `<p>` inside `<p>` or `<div>` inside `<p>`          | Fix invalid HTML nesting; browsers correct it causing server/client drift       |

## Delegation

- **Scan rendered pages for hidden hydration warnings**: Use `Explore` agent with Chrome DevTools to run the hydration audit script
- **Fix hydration mismatches across multiple routes**: Use `Task` agent to isolate, correct, and verify each affected component
- **Design hydration-safe architecture for new features**: Use `Plan` agent to select between Suspense boundaries, two-pass rendering, and cache patterns

## References

- [Common Mismatches](references/common-mismatches.md) -- causes, diagnosis, and fixes for hydration mismatch errors including dates, locales, HTML nesting, and browser extensions
- [Selective Hydration](references/selective-hydration.md) -- Suspense-based selective hydration, streaming SSR, two-pass rendering, and client-only components
- [Use Cache Patterns](references/use-cache-patterns.md) -- data drift prevention, Next.js use cache directive, React 19 use() hook, deterministic data bridges
- [Validation Techniques](references/validation-techniques.md) -- automated DOM verification, mutation monitoring, onRecoverableError, and production hydration monitoring
