---
name: vue
description: >-
  Modern Vue 3 conventions for writing, reviewing, refactoring, or migrating Vue:
  `<script setup>` and the Composition API, `defineProps` / `defineEmits` /
  `defineModel`, `ref` vs `reactive` and reactivity-loss caveats, composables for
  shared logic, `provide` / `inject` and Pinia within the state tiers, templates
  and keyed lists, `<Suspense>` and async components, the Nuxt server boundary,
  and testing by role. Builds on `core-typescript` and `architecture-and-design`.
  Use it when the user mentions Vue, Nuxt, `script setup`, Composition API, `ref`,
  `reactive`, `computed`, `watch`, composables, Pinia, `defineModel`, `v-model`,
  `provide`/`inject`, or hydration mismatch.
license: CC-BY-4.0
metadata:
  author: danielteles
  version: "1.0"
---

# Vue Conventions — Framework Skill

Vue-specific rules for modern Vue 3: single-file components with `<script setup>`, the Composition
API, composables, Pinia, and SSR with Nuxt. It gives the Vue form of rules that `core-typescript`
and `architecture-and-design` set in general terms.

> **Builds on.** `core-typescript` (language rules) and `architecture-and-design` (design), plus
> `accessibility` for UI work. Load a sibling only when the task turns on its layer; if it is not
> loaded, apply that layer from general knowledge and do not block.

This SKILL.md is self-sufficient: the **Ruleset** below is the complete, enforceable list. Each
`references/<topic>.md` holds that group's reasoning and `❌ / ✅` code, and
`references/worked-example.md` a full review pass; open them for depth when your runtime allows.

---

## How to Use This Skill

Pick the mode that matches the task. Do the steps in order.

| Mode | Steps |
|---|---|
| **Generate** — write a new component or composable | 1. `<script setup lang="ts">`, typed `defineProps` / `defineEmits`, `defineModel` for two-way (`components`). 2. `ref` for state, `computed` for derived; do not destructure a `reactive` (`reactivity`). 3. Pull shared stateful logic into a `useX` composable that returns refs (`composables`). 4. Key every `v-for` on a stable id (`templates`). 5. Run the Ruleset as a checklist. Fix each fail before you hand off. |
| **Review** — check a pull request or a diff | 1. Run the Ruleset against the diff. 2. Write one finding per fail, in the Output Format below. 3. Order the findings: `must-fix` first, then `consider`. 4. If nothing fails, say so in one line. Do not invent findings. |
| **Migrate** — Options API or Vue 2 to modern Vue 3 | 1. Move one component at a time to `<script setup>`; `data` → `ref`, `computed` stays, `methods` → functions, `watch` → `watch`/`watchEffect`. 2. Extract `mixins` into composables. 3. Replace the event bus and Vuex with `provide`/`inject` or Pinia (`state`). 4. One component per commit; keep the tests green. |

### Output Format

Write one finding per line:

```
<severity> · <topic> · <file>:<line> — <what is wrong>. <the fix as an action>.
```

- `<severity>` is `must-fix` (breaks a rule in this skill, the compiler, or a lint rule) or `consider` (safe, but a rule prefers another form).
- `<topic>` is a Ruleset topic slug (`components`, `reactivity`, `composables`, `templates`, `state`, `forms`, `rendering`, `server`, `testing`).

### Rules for Every Mode

- Name the Ruleset topic when you enforce a rule.
- Prefer the current API: `<script setup>` over `defineComponent`, `defineModel` over a manual `modelValue` prop plus `update:modelValue` event, Composition API
  over Options API in new code.
- Consistency within a file wins. When a file is entirely Options API, match it and note the gap rather than half-converting it.

---

## Ruleset

### components → `references/components.md`

- [ ] `<script setup lang="ts">` for a new component; no Options API and no `export default defineComponent({ ... })` with an options object.
- [ ] `defineProps` and `defineEmits` are typed with a type argument, not a runtime object; `defineModel` for two-way binding instead of a `modelValue` prop
      plus an `update:modelValue` emit.
- [ ] Prop defaults use reactive props destructure (`const { size = 'md' } = defineProps<Props>()`, Vue 3.5), not `withDefaults`.
- [ ] One component per `.vue` file, `PascalCase` name matching the file; a `name` is set (or inferred) for the devtools and `<KeepAlive>`.
- [ ] `defineOptions` for component options that are not props (e.g. `inheritAttrs: false`), not a second `<script>` block where avoidable.
- [ ] Caller-supplied content comes through named and scoped slots; the slot-vs-prop decision is `component-api-design`, slots-vs-config.
- [ ] `<style scoped>` (or CSS Modules); a child-piercing rule uses `:deep()` deliberately, never an unscoped global leak from a component file.

### reactivity → `references/reactivity.md`

- [ ] `ref` is the default for state; `reactive` only for a genuinely object-shaped local group, and it is never destructured or reassigned (that drops
      reactivity — use `toRefs` / `toRef`).
- [ ] `.value` in script; no `.value` on a top-level ref in a template.
- [ ] `computed` is pure — no side effect, no async, no mutation of another ref inside it.
- [ ] `watch` lists its source explicitly and does the minimum; `watchEffect` only when the dependencies are truly dynamic; neither is used to derive a value
      that `computed` can (`state`).
- [ ] `shallowRef` / `shallowReactive` for a large or externally-owned structure; a deep `watch` is a deliberate, commented choice.
- [ ] Exposed reactive state that callers must not mutate is wrapped in `readonly()`.

### composables → `references/composables.md`

- [ ] Shared stateful logic is a `useX()` composable in its own file that returns refs / computeds (and functions), not a mixin and not a renderless component.
- [ ] A composable that takes reactive input accepts a ref or a getter and reads it with `toValue()`.
- [ ] Lifecycle hooks and `watch` inside a composable are registered synchronously at call time (no `await` before them).
- [ ] The composable has no module-scope mutable state unless it is a deliberate singleton — that state is shared across every caller and leaks across requests
      in SSR (`server`).
- [ ] It returns a plain object of named values, not a single `reactive` bag.

### templates → `references/templates.md`

- [ ] Every `v-for` has a `:key` bound to a stable domain id — never the array index for a list that can reorder, grow, or shrink.
- [ ] `v-if` and `v-for` are never on the same element; the `v-if` moves to a `<template>` wrapper or into a `computed` filtered list.
- [ ] No non-trivial expression in a binding — anything past a property read or one call goes into a `computed`.
- [ ] `v-html` is used only on sanitized or trusted content (`architecture-and-design`, security).
- [ ] Element choice and accessible names follow `accessibility`; `useId()` supplies a stable label / `aria-*` id across server and client.
- [ ] `v-once` / `v-memo` appear only on a list row or subtree measured to be a render cost, not by default.

### state → `references/state.md`

- [ ] State is local (`ref` in the component) until a second component needs it; then `provide` / `inject` with a typed `InjectionKey`, and only then a store.
- [ ] Pinia is the store for cross-view client state, sized against the `architecture-and-design` state tiers — reach for it when a composable plus `provide`
      would not scale, not by default.
- [ ] A Pinia store is defined with the setup syntax and is written through its actions (or one `$patch`); a component never assigns store state directly
      or reassigns `store.$state`.
- [ ] Server data (fetch, cache, revalidate) is not held in Pinia or a `ref` — it uses a query cache (TanStack Query, or Nuxt `useAsyncData` / `useFetch`) keyed
      by its inputs (`architecture-and-design`, state-and-data).
- [ ] URL-owned state — filters, tab, pagination, page — lives in the route query, not a store (`architecture-and-design`, state-and-data).

### forms → `references/forms.md`

- [ ] `v-model` (with `.lazy` / `.number` / `.trim` where they fit) or `defineModel` for a custom field component; a native input is not needlessly wrapped in
      reactive plumbing.
- [ ] Validation runs off the same schema the server validates with (VeeValidate + a schema, or a resolver), and the server re-validates
      (`architecture-and-design`, forms).
- [ ] Field error state and messages are derived (`computed`) from the validation result, not copied into separate refs that can drift.
- [ ] Entered values survive a failed submit; each error maps back to its field; the submit button is not the only feedback for a blocked save.
- [ ] A field the current step does not use is removed from the payload or explicitly disabled, not just hidden with `v-if`.

### rendering → `references/rendering.md`

- [ ] A component with a top-level `await` in `setup` is rendered inside `<Suspense>` with a fallback and an error boundary (`onErrorCaptured` or a wrapper).
- [ ] Route components and heavy below-the-fold components are code-split with `defineAsyncComponent` / the router's lazy import.
- [ ] `<KeepAlive>` is scoped to a small `:include` list, not wrapped around a whole router view by default.
- [ ] A list past a few hundred rows is virtualized; no object / array / function literal is created in the template as a child prop — it is hoisted or
      a `computed`.
- [ ] A deep `watch` over a large structure, and a `watchEffect` that re-runs too often, are replaced with a targeted `watch` on the specific field.

### server → `references/server.md`

- [ ] No `window` / `document` / `localStorage` at the top level of `setup`; it goes in `onMounted` or behind `import.meta.client` (Nuxt) /
      `!import.meta.env.SSR` (Vite SSR).
- [ ] SSR-shared state uses the framework primitive (`useState` in Nuxt), never a module-scope `ref`.
- [ ] `useAsyncData` / `useFetch` have an explicit, stable key and run the fetch once across server and client, not again on hydration.
- [ ] A hydration mismatch is fixed at its cause (non-deterministic render, `Date.now()`, random, browser-only branch), not silenced; genuinely client-only UI
      is wrapped in `<ClientOnly>`.
- [ ] Server-only modules (secrets, a DB client, `server/` code) are never imported into a component that ships to the client.

### testing → `references/testing.md`

- [ ] Components are mounted with `@testing-library/vue` (or `@vue/test-utils` `mount`, not `shallowMount`) and queried by role and accessible name, never by
      component internals or a CSS selector on `wrapper`.
- [ ] Interaction is driven by `@testing-library/user-event` (awaited), and assertions are on rendered output — not on `emitted()` call counts or `vm` state as
      a stand-in for behavior.
- [ ] No stubbed `fetch` or mocked composable stands in for data; the boundary rule (MSW) is `test-quality`, test-doubles.
- [ ] Async updates are awaited (`await nextTick()` / `flushPromises()` / `findBy*`) before the assertion.
- [ ] A composable is tested through a host component that uses it; mounting-to-test in isolation only when there is no component.
- [ ] Teleported content (modal, tooltip) is queried through `screen` / `document`, not the mounted wrapper.
- [ ] Each test also passes the `test-quality` Ruleset — asserts on rendered behavior not internals, has a meaningful assertion, is deterministic. This group is
      the Vue mechanics; `test-quality` judges the test itself.

---

## Limits

This skill is Vue framework rules. It does not cover:

- Language rules (see `core-typescript`) or framework-neutral architecture (see `architecture-and-design`).
- A meta-framework's routing, data layer, and deployment specifics beyond the SSR boundary here — Nuxt modules, Nitro, route rules, `server/` API design.
- The Options API in depth — new code uses `<script setup>`; for a legacy Options API app, migrate first (the Migrate mode above).
- Vuex (superseded by Pinia), and store internals beyond the state tiers in `architecture-and-design`.
- Vue 2, the pre-`<script setup>` Composition API `setup()` return style, and animation (`<Transition>` choreography).
- Styling is `styling-and-design-tokens`; i18n (`vue-i18n` policy) is `i18n-and-localization`; loading and interaction cost is
  `web-performance`.
- Accessibility depth — semantic elements and names are noted where they fit; the full lens is `accessibility`.

This skill decides the Vue API. It does not replace reading the component and understanding the domain.

---

## References

This skill composes with:

- **`core-typescript`** — the language base; SFCs and `<script setup>` macros do not exempt code from it.
- **`architecture-and-design`** — the design layer. On a conflict it decides the design, this skill decides the Vue API.
- **`accessibility`** — the review lens for UI; Vue's tools are semantic templates, `useId()`, and primitive libraries (Reka UI, formerly Radix Vue,
  and Headless UI).
- **`test-quality`** — judges the individual test this skill's `testing` group produces.
- **`react`** / **`angular`** — the sibling framework skills.
