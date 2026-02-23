---
name: tanstack-devtools
description: 'TanStack DevTools for debugging Query, Router, and Form state in React apps. Use when setting up devtools, debugging cache state, or inspecting route trees. Use for devtools, react-query-devtools, router-devtools, form-devtools, debug, inspect, cache-viewer.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tanstack.com/devtools/latest/docs'
---

# TanStack DevTools

## Overview

TanStack DevTools provides debugging panels for inspecting Query cache state, Router route trees, and Form field state in React applications. There are two approaches: **standalone devtools** per library (`ReactQueryDevtools`, `TanStackRouterDevtools`) and the **unified TanStack Devtools** panel that combines all libraries into a single interface with plugin architecture.

**When to use:** Setting up devtools for TanStack libraries, debugging query cache behavior, inspecting route matching, monitoring form field state, or combining multiple TanStack devtools into one panel.

**When NOT to use:** Production debugging (devtools are tree-shaken in production by default), non-React frameworks without adapter support, or custom state management unrelated to TанStack libraries.

## Quick Reference

| Pattern                    | API                                       | Key Points                                          |
| -------------------------- | ----------------------------------------- | --------------------------------------------------- |
| Query devtools (floating)  | `<ReactQueryDevtools />`                  | Auto-connects to nearest QueryClient                |
| Query devtools (embedded)  | `<ReactQueryDevtoolsPanel />`             | Embed in custom layout                              |
| Router devtools (floating) | `<TanStackRouterDevtools />`              | Place in root route component                       |
| Router devtools (embedded) | `<TanStackRouterDevtoolsPanel />`         | Requires `router` prop outside provider             |
| Form devtools              | `<ReactFormDevtoolsPanel />`              | Plugin for unified devtools                         |
| Unified devtools           | `<TanStackDevtools plugins={[...]} />`    | Single panel for all TanStack libraries             |
| Vite plugin                | `devtools()` in vite config               | Source injection, enhanced logs, production removal |
| Production devtools        | `ReactQueryDevtoolsInProd`                | Opt-in for production environments                  |
| Lazy loading               | `React.lazy(() => import(...))`           | Reduce bundle size in development                   |
| Open hotkey                | `config={{ openHotkey: ['Shift', 'D'] }}` | Keyboard shortcut for unified panel                 |

## Unified Devtools Config

| Option           | Type                                                                                              | Purpose                          |
| ---------------- | ------------------------------------------------------------------------------------------------- | -------------------------------- |
| `position`       | `'top-left' \| 'top-right' \| 'bottom-left' \| 'bottom-right' \| 'middle-left' \| 'middle-right'` | Trigger button location          |
| `panelLocation`  | `'top' \| 'bottom'`                                                                               | Panel slide direction            |
| `theme`          | `'dark' \| 'light'`                                                                               | Panel color scheme               |
| `defaultOpen`    | `boolean`                                                                                         | Open panel on load               |
| `hideUntilHover` | `boolean`                                                                                         | Hide trigger until hover         |
| `openHotkey`     | `KeyboardKey[]`                                                                                   | Toggle panel shortcut            |
| `inspectHotkey`  | `KeyboardKey[]`                                                                                   | Source inspector shortcut        |
| `requireUrlFlag` | `boolean`                                                                                         | Only activate with URL parameter |

## Common Mistakes

| Mistake                                                 | Correct Pattern                                                              |
| ------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Importing devtools in production bundle                 | Standalone devtools auto-tree-shake; use `React.lazy` for code-splitting     |
| Passing `router` prop when inside RouterProvider        | Omit `router` prop; devtools auto-detect context                             |
| Using `ReactQueryDevtools` position for panel placement | `buttonPosition` controls logo position; `position` controls panel edge      |
| Mixing standalone and unified devtools                  | Choose one approach; both rendering causes duplicate panels                  |
| Rendering devtools outside QueryClientProvider          | Place `ReactQueryDevtools` inside provider or pass `client` prop             |
| Using `TanStackRouterDevtools` outside route tree       | Place in root route component or pass `router` prop explicitly               |
| Forgetting Vite plugin for unified devtools             | Add `devtools()` from `@tanstack/devtools-vite` to vite config               |
| Using unified devtools without framework adapter        | Install both `@tanstack/react-devtools` and library-specific plugin packages |

## Delegation

- **Devtools setup review**: Use `Task` agent to verify correct placement and configuration
- **Bundle size analysis**: Use `Explore` agent to check devtools are tree-shaken in production
- **Code review**: Delegate to `code-reviewer` agent

> If the `tanstack-query` skill is available, delegate query-specific debugging patterns to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-query`
>
> If the `tanstack-router` skill is available, delegate route debugging patterns to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-router`
>
> If the `tanstack-form` skill is available, delegate form state management and validation patterns to it.

## References

- [Query devtools setup, modes, and options](references/query-devtools.md)
- [Router devtools setup, route inspection, and options](references/router-devtools.md)
- [Form devtools and unified devtools patterns](references/form-devtools.md)
