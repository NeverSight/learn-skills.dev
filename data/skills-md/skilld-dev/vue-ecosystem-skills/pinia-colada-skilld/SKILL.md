---
name: pinia-colada-skilld
description: Data fetching layer for Vue built on Pinia. Use when writing, debugging, or reviewing code that imports @pinia/colada (pinia colada), including useQuery, useMutation, useInfiniteQuery, defineQuery, query cache invalidation, optimistic updates, plugins, SSR, or migrating from older versions. Provides current 1.4.x APIs, patterns, and migration rules.
---

# @pinia/colada 1.4.5

The smart data fetching layer for Vue.js, built on Pinia. Queries read and cache
data (`useQuery`), mutations write data (`useMutation`), everything lives in
Pinia stores (`useQueryCache`, `useMutationCache`).

- Docs: https://pinia-colada.esm.dev
- API types: `dist/index.d.mts` in the prepared package source
- Runtime exports: `dist/index.mjs:1487`
- Peers: `vue ^3.5.41`, `pinia ^2.2.6 || ^3.0.0 || ^4.0.2` (pinia 4 allowed since 1.4.1, `package.json:91-94`)
- Bundled codemods: `codemods/rules/*.yaml` in the package

## Setup

```sh
npm install pinia @pinia/colada
```

```ts
import { createPinia } from 'pinia'
import { PiniaColada } from '@pinia/colada'

const app = createApp(App)
app.use(createPinia())
// install after pinia; the options object is required for correct typing
app.use(PiniaColada, {
  queryOptions: { staleTime: 60_000 },
  plugins: [],
})
```

Global options go under `queryOptions` / `mutationOptions` (`dist/index.d.mts:1601-1618`).

## Mental model

- A query is identified by its `key`: a JSON-serializable array
  (`EntryKey`, `dist/index.d.mts:119`). Keys are hierarchical: `{ key: ['todos'] }`
  also matches `['todos', { filter: 'done' }]` when filtering.
- `status` is the data status: `'pending' | 'success' | 'error'`.
  `asyncStatus` is the operation status: `'idle' | 'loading'`. They are separate
  on purpose (https://pinia-colada.esm.dev/guide/queries.md).
- Defaults: `staleTime: 5000`, `gcTime: 300_000`, `refetchOnMount`,
  `refetchOnWindowFocus`, `refetchOnReconnect`, `enabled: true`
  (`dist/index.mjs:92-97`). Mutation `gcTime` default is `60_000`
  (`dist/index.d.mts:1379`).

## Core patterns

### Basic query

```vue
<script setup lang="ts">
import { useQuery } from '@pinia/colada'

const { state, asyncStatus } = useQuery({
  key: ['todos'],
  query: () => fetch('/api/todos').then(res => res.json()),
})
</script>

<template>
  <div v-if="state.status === 'pending'">Loading...</div>
  <div v-else-if="state.status === 'error'">{{ state.error.message }}</div>
  <ul v-else>
    <li v-for="todo in state.data" :key="todo.id">{{ todo.text }}</li>
  </ul>
</template>
```

Use the grouped `state` object for type narrowing in templates. TypeScript
cannot narrow separate `data` / `error` refs from `status`
(https://pinia-colada.esm.dev/guide/queries.md).

### Reactive keys: pass a getter

Everything the `query` function reads (route params, refs) must be in the `key`.
Pass `key` as a getter so the query refetches when dependencies change:

```ts
const { data } = useQuery({
  key: () => ['contacts', route.params.id as string],
  query: () => fetch(`/api/contacts/${route.params.id}`).then(r => r.json()),
})
```

### Guard queries with `enabled`

Prevent invalid fetches when a required param is absent (common in stores and
global queries):

```ts
useQuery({
  key: () => ['decks', route.params.deckId],
  query: () => fetchDeck(route.params.deckId as string),
  enabled: () => 'deckId' in route.params,
})
```

### Type-safe shared options: `defineQueryOptions`

```ts
export const todoOptions = defineQueryOptions((id: string) => ({
  key: ['todos', id],
  query: () => fetchTodo(id),
}))

// single-function form; the returned key is tagged so queryCache infers TData
const { data } = useQuery(() => todoOptions(route.params.id as string))
const todo = queryCache.getQueryData(todoOptions('1').key) // typed
```

`useQuery` accepts options or a getter returning options
(`dist/index.d.mts:733`). Since 1.0 the two-parameter form
`useQuery(options, paramsGetter)` is removed; see
[references/migration.md](./references/migration.md).

### Shared query state: `defineQuery`

Wrap queries used by multiple components so refs are created once, like a tiny
Pinia store. The setup function must be synchronous:

```ts
export const useFilteredTodos = defineQuery(() => {
  const search = ref('')
  const query = useQuery({
    key: () => ['todos', { search: search.value }],
    query: () => fetchTodos(search.value),
  })
  return { ...query, search }
})
```

Details: [references/queries.md](./references/queries.md).

### Mutation + invalidation

```ts
const queryCache = useQueryCache()

const { mutate, isLoading } = useMutation({
  mutation: (text: string) => createTodo(text),
  async onSettled() {
    await queryCache.invalidateQueries({ key: ['todos'] })
  },
})
```

- `mutate(vars)` never rejects; use it in templates and event handlers.
- `mutateAsync(vars)` returns a promise and rejects on failure.
- Put `onMutate` before `mutation` in the options object so its returned
  context is inferred in later hooks (`dist/index.d.mts:1410-1433`).
- Optimistic updates: write to the cache in `onMutate`, roll back in `onError`
  only if the cache still holds your optimistic value. Full pattern in
  [references/mutations.md](./references/mutations.md).

### Queries have no `onSuccess`/`onError`

This is intentional: a query can have many watchers. Use `watch(data, ...)`,
or global hooks via `PiniaColadaQueryHooksPlugin`
(https://pinia-colada.esm.dev/plugins/official/query-hooks.md).

## Version-critical rules (1.x)

- `useQuery(setup, paramsGetter)` and `useQueryState(setup, paramsGetter)` were
  removed in 1.0.0. Migrate with the shipped codemod:
  `ast-grep scan -r node_modules/@pinia/colada/codemods/rules/migration-0-21-to-1-0.yaml -i src`
  (https://github.com/posva/pinia-colada/blob/main/CHANGELOG.md).
- `useQueryState(key)` reads query state without fetching; the key is the only
  argument (`dist/index.d.mts:920-926`).
- `initialData` changes query state to `success`; `placeholderData` does not
  change the cache (`dist/index.d.mts:558-600`).
- To reset an entry's state manually use `queryCache.setEntryState(entry, state)`;
  setting data to `undefined` via `setQueryData()` no longer resets state.
- Infinite query data is `{ pages, pageParams }`; use `setInfiniteQueryData()`
  (added 1.2.0), not `setQueryData()`, to prime infinite entries.
- Devtools are a separate package: `@pinia/colada-devtools`.
- Nuxt: install the `@pinia/colada-nuxt` module; it handles SSR serialization
  automatically.

## References

- [queries.md](./references/queries.md): `useQuery` API, options, return values,
  `useQueryState`, `defineQuery`, `defineQueryOptions`, key factories
- [mutations.md](./references/mutations.md): `useMutation` API, hooks and
  context, optimistic updates, `defineMutation`, `defineMutationOptions`
- [infinite-queries.md](./references/infinite-queries.md): `useInfiniteQuery`,
  `defineInfiniteQueryOptions`, `setInfiniteQueryData`, `maxPages`
- [query-cache.md](./references/query-cache.md): cache stores, invalidation,
  filters, manual cache writes, error codes
- [plugins.md](./references/plugins.md): plugin API, `PiniaColadaQueryHooksPlugin`,
  `TypesConfig` augmentation, official plugin packages
- [ssr.md](./references/ssr.md): serialization and hydration, lazy queries,
  `PiniaColadaSSRNoGc`
- [migration.md](./references/migration.md): 0.x to 1.x changes and codemods
