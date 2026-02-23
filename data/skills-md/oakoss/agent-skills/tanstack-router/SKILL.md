---
name: tanstack-router
description: 'Type-safe, file-based React routing with route loaders, search params validation, code splitting, preloading, navigation, route context, and TanStack Query integration. Use when setting up file-based routing, adding search params validation, implementing route loaders, code splitting routes, configuring virtual file routes, protecting routes with auth guards, or fixing type registration errors. Use for router setup, navigation patterns, URL state management, data loading.'
license: MIT
metadata:
  author: oakoss
  version: '1.3'
  source: 'https://tanstack.com/router/latest/docs'
---

# TanStack Router

Type-safe, file-based routing for React with route-level data loading, search params validation, code splitting, and TanStack Query integration.

**Package:** `@tanstack/react-router` | **Plugin:** `@tanstack/router-plugin`

## Quick Reference

| Pattern                           | Usage                                   |
| --------------------------------- | --------------------------------------- |
| `createFileRoute('/path')`        | Define file-based route                 |
| `createRootRouteWithContext<T>()` | Root route with typed context           |
| `createLazyFileRoute('/path')`    | Code-split route component              |
| `zodValidator(schema)`            | Search params validation                |
| `Route.useLoaderData()`           | Access loader data in component         |
| `Route.useParams()`               | Type-safe route params                  |
| `Route.useSearch()`               | Type-safe search params                 |
| `useNavigate()`                   | Programmatic navigation                 |
| `useBlocker()`                    | Block navigation (dirty forms)          |
| `notFound()`                      | Throw 404 from loader                   |
| `getRouteApi('/path')`            | Type-safe hooks in split files          |
| `stripSearchParams(defaults)`     | Clean default values from URLs          |
| `retainSearchParams(['key'])`     | Preserve params across navs             |
| `useAwaited({ promise })`         | Suspend until deferred promise resolves |
| `useCanGoBack()`                  | Check if router can go back safely      |

## Data Loading

| Method               | Returns | Throws | Use Case                                         |
| -------------------- | ------- | ------ | ------------------------------------------------ |
| `ensureQueryData`    | Data    | Yes    | Route loaders (recommended)                      |
| `prefetchQuery`      | void    | No     | Background prefetching                           |
| `fetchQuery`         | Data    | Yes    | Immediate data need                              |
| `defer()` (optional) | Promise | No     | Stream non-critical data (promises auto-handled) |

## Preloading

| Strategy     | Behavior                  | Use Case                    |
| ------------ | ------------------------- | --------------------------- |
| `'intent'`   | Preload on hover/focus    | Default for most links      |
| `'render'`   | Preload when Link mounts  | Critical next pages         |
| `'viewport'` | Preload when Link in view | Below-fold content          |
| `false`      | No preloading             | Heavy, rarely-visited pages |

## File Organization

| File                 | Purpose                      |
| -------------------- | ---------------------------- |
| `__root.tsx`         | Root route with `<Outlet />` |
| `index.tsx`          | Index route for `/`          |
| `posts.$postId.tsx`  | Dynamic param route          |
| `_authenticated.tsx` | Pathless layout (auth guard) |
| `dashboard.lazy.tsx` | Code-split component         |

## Common Mistakes

| Mistake                           | Fix                                                   |
| --------------------------------- | ----------------------------------------------------- |
| Missing router type registration  | Add `declare module` with `Register` interface        |
| `useParams()` without `from`      | Always pass `from: '/route/path'` for exact types     |
| `useNavigate()` for regular links | Use `<Link>` for `<a>` tags, a11y, preloading         |
| `prefetchQuery` in loaders        | Use `ensureQueryData` (returns data, throws errors)   |
| Fetching in `useEffect`           | Use route loaders (prevents waterfalls)               |
| Sequential fetches in loader      | Use `Promise.all` for parallel requests               |
| Missing leading slash             | Always `'/about'` not `'about'`                       |
| TanStackRouterVite after react()  | Plugin MUST come before `react()` in Vite config      |
| `strict: false` params unparsed   | Use strict mode or manually parse after navigation    |
| Pathless route notFoundComponent  | Define `notFoundComponent` on child routes instead    |
| Aborted loader undefined error    | Guard `errorComponent` with `if (!error) return null` |
| No `loaderDeps` declared          | Declare deps so loader only re-runs when they change  |

## Delegation

- **TanStack Query patterns** — data fetching, caching, mutations: use `tanstack-query` skill
- **TanStack Start** — server functions, SSR, server-side auth: use `tanstack-start` skill
- **TanStack Table** — table rendering with router search params: use `tanstack-table` skill
- **Router + Query integration** — loader data flow, preloading: see [Loader Data Flow Patterns](references/loader-query-patterns.md)

> If the `tanstack-devtools` skill is available, delegate router state debugging and route tree inspection to it.

## References

- [Setup](references/setup.md) — installation, Vite config, file structure, app setup, router default options
- [Type Safety](references/type-safety.md) — register router, `from` param, `strict: false`, type utilities, getRouteApi
- [Data Loading](references/data-loading.md) — route loaders, Query integration, parallel loading, streaming, deferred data, abort signal, loaderDeps
- [Search Params](references/search-params.md) — validation, strip/retain middleware, fine-grained subscriptions, debounce, custom serializers
- [Navigation](references/navigation.md) — Link, active styling, relative navigation, hash, route masks, blocker, scroll restoration
- [Auth and Context](references/auth-and-context.md) — beforeLoad, context inheritance, pathless layouts, dependency injection, error handling
- [Code Splitting](references/code-splitting.md) — lazy routes, auto splitting, preloading strategies, programmatic preloading
- [Virtual File Routes](references/virtual-routes.md) — rootRoute, route, index, layout, physical builders, mixing file-based and code-based routing
- [Known Issues](references/known-issues.md) — 20 documented issues with fixes, anti-patterns
- [Loader+Query Patterns](references/loader-query-patterns.md) — ensureQueryData in loaders, parallel loading, critical vs non-critical data, search-param-dependent loaders
