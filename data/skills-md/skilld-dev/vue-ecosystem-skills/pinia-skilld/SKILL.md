---
name: pinia-skilld
description: "Use when writing, debugging, or refactoring code that imports \"pinia\", the Vue 3 store library. Covers pinia 4.x: option and setup stores, state, getters, actions, subscriptions, plugins, SSR hydration, testing, Options API map helpers, and v4 nostics diagnostics. Provides version-correct API usage and migration notes from v2 and v3."
---

# pinia@4.0.3

Source citations use package-relative paths from the prepared pinia 4.0.3 source: `package.json`, `README.md`, `dist/pinia.js` (runtime), `dist/pinia.d.ts` (types). Other citations are official documentation URLs.

## Requirements

- Vue `^3.5.11` peer [package.json:62]. Vue 2 is unsupported since v3.
- `@vue/devtools-api` `^8.1.5` is a required, non-optional peer [package.json:60-68]. Install it alongside pinia: `npm install pinia @vue/devtools-api` [README.md:108-111], v4.0.0 release notes.
- TypeScript `>=5.6.0` optional peer [package.json:69-71].
- ESM-only package: `"type": "module"`, single export `.` to `dist/pinia.js` [package.json:42,47-50]. v4 removed CJS resolution; a require() fallback breaks.
- `@pinia/nuxt` 1.x and `@pinia/testing` 2.x are the companion versions for pinia 4 (https://github.com/vuejs/pinia/releases).

## Install and setup

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.mount('#app')
```

From [README.md:119-130]. In dev on the client, `createPinia()` registers the devtools plugin itself [dist/pinia.js:832,847].

## Define a store

Two syntaxes. The id is a unique string, first argument in both [dist/pinia.d.ts:645,653].

```ts
import { defineStore } from 'pinia'

// Option store: state/getters/actions
export const useCounterStore = defineStore('counter', {
  state: () => ({ count: 0 }),
  getters: {
    doubleCount: (state) => state.count * 2,
  },
  actions: {
    increment() {
      this.count++
    },
  },
})

// Setup store: refs are state, computed are getters, functions are actions
export const useTodos = defineStore('todos', () => {
  const todos = ref<Todo[]>([])
  const done = computed(() => todos.value.filter((t) => t.done))
  function add(todo: Todo) {
    todos.value.push(todo)
  }
  return { todos, done, add }
})
```

Rules for setup stores [dist/pinia.js:1178-1202]:
- `ref()` and `reactive()` become state.
- `computed()` becomes a getter.
- Functions become actions, wrapped automatically for `$onAction`.
- Return every state property. Pinia only picks up returned state, so private state breaks SSR hydration and devtools.

The setup function receives helpers: `defineStore('id', ({ action }) => { ... })` [dist/pinia.js:1177, dist/pinia.d.ts:628-638]. `action(fn, name?)` makes a helper function trackable by `$onAction` when called within the store. Rarely needed; intended for advanced cases like Pinia Colada.

## Use a store

Call `useStore()` inside `setup()` (or any composable). Every call returns the same store instance.

```ts
const counter = useCounterStore()

counter.count++            // direct state mutation
counter.doubleCount        // getter
counter.increment()        // action

const { count, doubleCount } = storeToRefs(counter) // refs for destructuring
```

`storeToRefs()` converts state and getters to refs. It ignores actions and non-reactive properties [dist/pinia.js:1475-1489]. Destructure with it, never plain `toRefs()` or `...store`, when you need reactivity.

Common operations:
- Group changes into one devtools entry with `store.$patch(obj)` or `$patch(fn)`. The function form must be synchronous [dist/pinia.d.ts:219-225] and suits array, Map, and Set edits [dist/pinia.js:964-975].
- `$reset()` exists only on option stores. On a setup store it throws in dev [dist/pinia.js:1085-1087]; implement your own `$reset` in the returned object.
- Assigning `store.$state = {...}` does not replace state; it calls `$patch` internally [dist/pinia.js:1207-1216].
- Declare every state key in `state()` (or return it from setup), even when the initial value is `undefined`. New keys added later are not reactive.
- Outside a component, pass the pinia instance: `useStore(pinia)`. On the server this is mandatory; skipping it risks cross-request state pollution [dist/pinia.js:37-39].

Details: [stores](./references/stores.md), [subscriptions](./references/subscriptions.md).

## Version notes and migration

v4.0.0, technically breaking only (https://github.com/vuejs/pinia/releases/tag/v4.0.0):
- ESM-only distribution.
- `@vue/devtools-api` upgraded to v8 and now a required install.
- Errors and dev warnings refactored onto Nostics diagnostics, codes `PINIA_R1001` to `PINIA_R1007` [dist/pinia.js:18-56]. See [diagnostics](./references/diagnostics.md).
- `piniaSymbol` is now part of the public exports [dist/pinia.js:1491].
- `storeToRefs()` skips nullish values gracefully; `$subscribe()` ignores a duplicate callback instead of stacking a second watcher.

Still relevant from v3.0.0 (https://pinia.vuejs.org/cookbook/migration-v2-v3.html):
- `defineStore({ id: 'x', ... })` object-only signature removed. Use `defineStore('x', { ... })`.
- `PiniaStorePlugin` type removed. Use `PiniaPlugin`.
- Vue 2 support dropped. Vue 2 users stay on pinia v2.

## Reference files

- [API surface](./references/api.md): every public export with signatures and type helpers.
- [Stores](./references/stores.md): state, getters, actions, typing, composing stores, HMR.
- [Subscriptions](./references/subscriptions.md): `$subscribe`, `$onAction`, `MutationType`, detached and flush options.
- [Plugins](./references/plugins.md): `pinia.use()`, context, typing extensions, new state and options.
- [SSR](./references/ssr.md): hydration, `skipHydrate`, per-request pinia, Nuxt.
- [Testing](./references/testing.md): `setActivePinia`, `@pinia/testing` 2.x usage.
- [Options API](./references/options-api.md): map helpers without `setup()`.
- [Diagnostics](./references/diagnostics.md): dev-only `PINIA_R100x` catalog with fixes.

Official docs: https://pinia.vuejs.org
