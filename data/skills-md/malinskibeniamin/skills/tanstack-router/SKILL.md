---
name: tanstack-router
description: Apply TanStack Router patterns for Query ownership and typed search. Use when changing routes, loaders, navigation, route trees, or search parameters.
paths:
  - "**/routes/**/*.tsx"
  - "**/routes/**/*.ts"
---

Run `/tanstack-intent` first for installed Router/Query API syntax. This skill owns local URL/data policy. See [REFERENCE.md](REFERENCE.md) for shapes and [SETUP.md](SETUP.md) for install.

## Router + Query

Router loaders start server fetches after navigation intent; Query owns cache/refetch/invalidation/GC; components observe with `useQuery`/`useSuspenseQuery`.

Route-known inputs use one pipeline: `validateSearch` -> `loaderDeps` -> one `queryOptions` builder -> loader and observer. Return only query-driving fields. Components use `useLoaderDeps`, not parallel search reads. Share route-context options only when installed Intent guidance supports it.

- Critical data: await `ensureQueryData`, observe with `useSuspenseQuery`.
- Deferred route data: start in loader, observe with `useQuery` plus loading/empty/error.
- Interaction-only data may start in components.
- Query loaders use `defaultPreloadStaleTime: 0` and `createRootRouteWithContext`.

## Navigation lifetimes

- Superseded navigation cannot publish; shared loader/Query work may remain useful.
- `beforeLoad` is replay-safe auth, redirect, or context construction. No observable side effects or ordinary fetches.
- Direct loader requests forward `abortController.signal`; Query functions forward Query's signal. Never cancel shared work on each navigation.
- Throw `redirect(...)`; never imperatively navigate from guards/loaders.
- `onResolved` owns analytics/non-DOM cleanup; `onRendered` owns focus, scroll, measurement after commit.
- Use Router pending UI/timing, not custom navigation timers.

## Route rules

- Scope `useParams`, `useSearch`, `useLoaderData`, `useRouteContext` with `{ from }` or route API; reject `strict: false`.
- Query-backed components read Query, not `Route.useLoaderData`.
- Route files export config only; reusable components live elsewhere.
- Use router navigation, not `window.location`.
- `react-router-dom`, `URLSearchParams`, and nuqs are migration debt.
- Regenerate route tree after changes.

## Search

`validateSearch` owns typing. URL holds shareable tabs/filters/sort/page; storage holds personal density/page size/collapse. Validate enums/dates/bounded numbers; clamp stale pages. Merge prior search and use `replace: true` within a section so Back exits it.

## Done

Types prove scope; loader and observer share options/inputs; Query has an active observer and all visible states; rapid/preloaded navigation cannot publish stale UI or duplicate app work; tests assert rendered landmarks after URL changes; history semantics and malformed/stale/shared URLs pass; route tree, tests, typecheck, lint pass.
