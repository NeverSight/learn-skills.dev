---
name: vue-router-skilld
description: ALWAYS use when writing code that imports "vue-router", "vue-router/vite", "vue-router/auto-routes", or "vue-router/experimental". Consult for debugging, best practices, or modifying vue-router, vue router, router, file-based routing, typed routes, data loaders.
license: MIT
---

# vuejs/router `vue-router@5.3.1`

Prepared source: `vue-router@5.3.1`, ESM package (`"type": "module"`, package.json:2,20).
Peers: `vue ^3.5.34 || ^4.0.0`; optional `vite ^7.3.0 || ^8.0.0`, `pinia ^3.0.4 || ^4.0.2`, `@pinia/colada >=0.21.2` (package.json:173-193).
Docs: https://router.vuejs.org

## Import map

| Import | Use for |
|---|---|
| `vue-router` | `createRouter`, `createWebHistory`, `createWebHashHistory`, `createMemoryHistory`, `RouterLink`, `RouterView`, `useRouter`, `useRoute`, `useLink`, `onBeforeRouteLeave`, `onBeforeRouteUpdate`, `isNavigationFailure`, `NavigationFailureType`, `START_LOCATION`, `parseQuery`, `stringifyQuery` (dist/vue-router.d.ts:6) |
| `vue-router/vite` | Vite plugin, file-based routing (package.json:104) |
| `vue-router/unplugin/{vite,webpack,rollup,esbuild,rolldown}` | same plugin for other bundlers (dist/unplugin/) |
| `vue-router/unplugin` | `VueRouterAutoImports`, `createRoutesContext`, `EditableTreeNode`, plugin `Options` (dist/unplugin/index.d.mts:62) |
| `vue-router/auto-routes` | generated `routes` array + `handleHotUpdate(router)` (vue-router-auto-routes.d.mts:6,28) |
| `vue-router/auto-resolver` | generated `resolver` for `experimental_createRouter` + `handleHotUpdate` (vue-router-auto-resolver.d.mts:15,21) |
| `vue-router/experimental` | data loaders, `reroute`, `miss`, `definePage`, `defineParamParser`, `PARAM_PARSER_INT`/`PARAM_PARSER_BOOL`, `experimental_createRouter`, `useIsDataLoading` (dist/experimental/index.d.ts:7) |
| `vue-router/experimental/pinia-colada` | `defineColadaLoader` (package.json:77) |
| `vue-router/volar/sfc-route-blocks`, `vue-router/volar/sfc-typed-router` | Volar plugins: `<route>` blocks, per-file typed `useRoute()` (package.json:115-121) |

Avoid:
- `vue-router/auto` — deprecated, will be removed (vue-router-auto.d.ts:1).
- `vue-router/experimental` in CJS builds — ESM-only since v5.1.0 (https://github.com/vuejs/router/releases/tag/v5.1.0).

## Quick start (classic routes)

```ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./pages/Home.vue') },
    { path: '/users/:id', component: () => import('./pages/User.vue'), props: true },
  ],
})
app.use(router)
```

In components: `useRoute()` / `useRouter()` from `vue-router`; `<RouterLink to="...">` and `<RouterView>` are globally registered by `app.use(router)`.

## Quick start (file-based routing)

```ts
// vite.config.ts
import VueRouter from 'vue-router/vite'
import Vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [VueRouter(), Vue()], // Vue plugin MUST come after VueRouter
})
```

```ts
import { createRouter, createWebHistory } from 'vue-router'
import { routes, handleHotUpdate } from 'vue-router/auto-routes'

const router = createRouter({ history: createWebHistory(), routes })
if (import.meta.hot) handleHotUpdate(router)
```

Pages live in `src/pages` by default. Start the dev server once to generate `typed-router.d.ts`, add it to `tsconfig.json` `include` with `"moduleResolution": "Bundler"`. Details, naming conventions, and plugin options: [references/file-based-routing.md](./references/file-based-routing.md).

## Core rules

- Return values from navigation guards, never call `next()`. `next` is deprecated (runtime warning since v5.0.3) and will be removed (dist/index-D7ja2BKs.d.ts:362-393, https://github.com/vuejs/router/releases/tag/v5.0.3).
  ```ts
  router.beforeEach(to => {
    if (to.meta.requiresAuth && !isAuthenticated) return { name: 'login' }
    // return nothing, true, false, or a route location
  })
  ```
- In data loaders, redirect with `reroute(to)`; `new NavigationResult(to)` is deprecated and logs a warning (dist/experimental/index.js:1106-1111).
- `router.currentRoute` is a `ShallowRef<RouteLocationNormalizedLoaded>` — read it as `router.currentRoute.value` (dist/index-D7ja2BKs.d.ts:1433).
- `router.onReady()` does not exist (removed in v4); use `await router.isReady()`.
- `scrollBehavior` returns `{ top, left }` (v4 renamed `x`/`y` to `left`/`top`).
- Detect failed navigations: `const failure = await router.push(...)`; check with `isNavigationFailure(failure, NavigationFailureType.aborted)`.
- `route.meta` merges non-recursively from all matched records; read `to.meta.requiresAuth` directly instead of scanning `to.matched`. Type `meta` via `RouteMeta` module augmentation.
- Use `router.beforeResolve` (not `beforeEach`) for work that needs async components resolved.
- Use `inject()` inside guards to reach Pinia stores (supported since Vue 3.3).
- Decouple components from the router with route `props: true` or `props: route => ({ ... })`; pass query values this way to keep components testable.
- Watch narrow sources (`() => route.params.id`), never the whole `route` object.

Full core API notes: [references/core-api.md](./references/core-api.md).

## Typed routes

Enable by using the file-based routing plugin (types are generated automatically), or augment manually:

```ts
declare module 'vue-router' {
  interface TypesConfig {
    RouteNamedMap: RouteNamedMap
  }
}
```

Typed `push('/users/:id', { params: { id: 42 } })`, typed `useRoute()`, per-file typing via Volar plugin `vue-router/volar/sfc-typed-router`. Param parsers (`int`, `bool`, custom in `src/params/`) give typed, validated params; `definePage({ params: { query: { page: { parser: 'int', default: 1 } } } })` declares query params. Details: [references/typed-routes.md](./references/typed-routes.md).

## Data loaders (experimental)

```ts
// src/pages/users/[id].vue
import { defineBasicLoader } from 'vue-router/experimental'
import { reroute } from 'vue-router/experimental'

export const useUserData = defineBasicLoader(async (to) => {
  if (!to.params.id) reroute('/') // reroute throws: stops the loader immediately
  return fetchUser(to.params.id)
})
```

Install `DataLoaderPlugin` **before** the router: `app.use(DataLoaderPlugin, { router })`. Non-blocking loaders: `defineBasicLoader(loader, { lazy: true })`; errors then land in `error`, not in `router.onError`. Details: [references/data-loaders.md](./references/data-loaders.md).

## Version notes (5.0.x → 5.3.1)

- v5.0.7: `RouteNamedMap` is wired through the generated `typed-router.d.ts` (https://github.com/vuejs/router/releases/tag/v5.0.7); param parser folders gained `include`/`exclude`.
- v5.1.0: typed `definePage` `params.path`, `defineParamParserRaw`, strict default typing, `TypesConfig` global `Router` override, experimental export is ESM-only (https://github.com/vuejs/router/releases/tag/v5.1.0).
- v5.2.0: added diagnostics for common mistakes; allows pinia 4 (https://github.com/vuejs/router/releases/tag/v5.2.0).
- v5.3.0: scroll skips when `history.scrollRestoration` says so; duplicate `definePage()` reported instead of crashing; `EditableTreeNode.name` accepts `false` to unset (https://github.com/vuejs/router/releases/tag/v5.3.0).
- v5.3.1: fixes `isActive` with non-string params (https://github.com/vuejs/router/releases/tag/v5.3.1).

Migration from v3/v4, or from `unplugin-vue-router`: [references/migration.md](./references/migration.md).

## References

- [core-api.md](./references/core-api.md) — router creation, histories, guards, failures, scroll, RouterLink/RouterView.
- [file-based-routing.md](./references/file-based-routing.md) — plugin setup, file naming, `definePage`, `<route>` blocks, `extendRoute`, options.
- [typed-routes.md](./references/typed-routes.md) — `TypesConfig`, generated types, param parsers, `experimental_createRouter`.
- [data-loaders.md](./references/data-loaders.md) — `defineBasicLoader`, `defineColadaLoader`, `reroute`, lazy loaders, SSR notes.
- [migration.md](./references/migration.md) — v3→v4 and v4→v5 changes, deprecations in the v5 line.
