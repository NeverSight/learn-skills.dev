---
name: vue-component-anatomy
description: >-
  Use when writing, editing, or reviewing a single Vue 3 Single File Component
  (a `.vue` file with `<script setup lang="ts">`). Covers block order and
  template root, the compiler-macro order (defineEmits -> defineModel ->
  defineProps -> defineSlots, defineExpose last), the ordering inside `<script
  setup>` (imports -> macros -> constants -> stores -> state -> composables ->
  computed -> watch -> lifecycle -> functions), function-vs-arrow style, prop and
  emit typing, v-model via defineModel, and scoped/module styling. Triggers on
  editing any `.vue` file, on defineProps/defineEmits/defineModel/defineSlots, on
  script-setup ordering questions, and on prop typing. Feature-level splitting:
  `vue-build-feature`; Flux UI library: `flux-ui`.
---

# Vue component anatomy

How one Vue 3 Single File Component is built on the inside. This is about the
shape of a single `.vue` file: the order of its blocks, its macros, its script,
and its styles. It is deliberately library-neutral. For how a feature is split
across several components use `vue-build-feature`; for choosing UI components (if
the project uses Flux) use `flux-ui`; project-specific rules live in the repo's
`CLAUDE.md` / `AGENTS.md`.

Assume `<script setup lang="ts">` and Vue 3.5+ unless the repo says otherwise.

## 1. SFC skeleton and template root

- **Block order:** `<template>` first, then `<script setup lang="ts">`, then
  `<style>`, then an optional `<i18n>` block last. Keep it consistent across
  the codebase.
- **`<i18n>` blocks** (projects with vue-i18n SFC messages) always come after
  `<style>`. Match the format of existing components: check whether the
  codebase uses `<i18n lang="yaml">` or JSON before writing one, and use the
  same `lang` attribute everywhere.
- **Prefer a single root element** in the template: it gives predictable
  attribute fallthrough (`class`, `@click`, `v-bind="$attrs"` land on one node)
  and is required by many `<Transition>` setups. Vue 3 allows fragments
  (multiple roots), but reach for them deliberately, not by accident: with more
  than one root, `$attrs` is not auto-inherited and you must bind it explicitly.
- Render teleported/overlay children (dialogs, tooltips) inside the root, not as
  a sibling of it, so transitions and fallthrough stay intact.

## 2. Macro order (top of `<script setup>`)

Declare the compiler macros first, in this order, so the component's contract is
readable at a glance:

`defineOptions` (rare) -> `defineEmits` -> `defineModel` -> `defineProps` ->
`defineSlots`.

`defineExpose` is the exception: it goes at the very bottom of the script (after
the function declarations, see section 3), and only if a parent needs a ref
handle. It describes the outward surface, so it reads last once everything it
exposes is defined.

- Type each one; do not pass runtime option objects when a type argument says it
  better.

## 3. `<script setup>` ordering

Order the body top to bottom so state is declared before it is used:

1. **imports**
2. **macros** (emits / models / props / slots) - see section 2
3. **module constants** (`ALL_CAPS`: config values, option lists, lookup maps)
4. **stores** (`use*Store()` - shared state)
5. **reactive state** (`ref`, `reactive`, `shallowRef`, and template refs)
6. **composables** (`useRouter`, `useI18n`, other `use*` behaviour helpers)
7. **computed**
8. **watch / watchEffect**
9. **lifecycle hooks** (`onMounted`, `onUnmounted`, ...)
10. **function declarations** (event handlers and helpers)
11. **`defineExpose`** last of all, only if a parent needs a ref handle

- **Module constants go below the macros, not above them.** The macros are the
  component's public contract and read first; constants are implementation
  detail. A constant that needs `t()` or other reactive input is not a constant:
  make it a `computed` in step 7.
- **Stores sit above the reactive state, composables below it.** A store is
  shared state and reads together with the component's own state; a composable
  provides behaviour or derived data and may build on that state. Rule of thumb:
  a `use*Store()` from the store layer is a store, every other `use*` call is a
  composable.
- **Template refs use `useTemplateRef('name')`** (Vue 3.5+) and sit with the
  reactive state; the string argument matches the `ref="name"` in the template.
- **Import style (alias vs relative)** follows `vue-build-feature`: the path
  alias (`@/...`) across layers, relative paths only for same-feature siblings.
- Keep side effects (kick-off fetches, title setters) in the lifecycle step, not
  scattered between declarations.

## 4. `function` vs arrow

- **Named handlers and helpers** are `function` declarations
  (`function onSubmit(): void { ... }`): they hoist, read cleanly in the
  template, and stack-trace with a name.
- **Arrow functions** only for inline callbacks and closures (watchers,
  `array.map`, `.filter`, event options).
- **Lifecycle bodies stay inline:** `onMounted(async () => { ... })` keeps the
  side effect where it runs. Only lift it into a named function when a second
  caller needs it (a watcher, a retry button, the template) or when the body
  grows past a handful of statements - not just to give it a name.

## 5. Props and their types

- Type props with the generic form: `defineProps<{ readonly id: number }>()`.
  Mark fields `readonly` - props are immutable.
- **Defaults:** use reactive props destructuring with defaults:
  `const { size = 'md' } = defineProps<{ size?: Size }>()`. The destructured
  bindings stay reactive; only destructure the props that need a default.
- **`type` over `interface`** for prop and data shapes. Use `interface` only
  where declaration merging is required (module augmentation, `declare global`).
- **Inline the props type** in `defineProps<{ ... }>()` when it is used only
  there. Promote it to a named, exported `type Props` only when it is reused
  elsewhere (for example passed to another generic).
- **Do not destructure props that are only read in the template** in `<script>`;
  destructure in script only when you need a default or a local binding.

## 6. Emits and models

- **Type emits:** `const emit = defineEmits<{ submit: [id: number]; cancel: [] }>()`.
- **Two-way binding is `defineModel`,** not a hand-rolled `modelValue` prop plus
  an `update:modelValue` emit: `const value = defineModel<string>()`. Named
  models: `defineModel<number>('page')` pairs with `v-model:page` on the parent.
- **Model defaults use a runtime option object** (the exception to section 2):
  `defineModel<string>({ default: '' })`. Give an array or object model a factory
  default so its value is never `undefined`:
  `defineModel<string[]>({ default: () => [] })`.
- Keep the child dumb: emit an event or write the model; let the parent own the
  decision.

## 7. Template conventions

- **`v-for` always has a stable `:key`** (an id, not the array index when the
  list reorders).
- **No heavy logic in the template.** Move anything past a simple expression into
  a `computed` or a named function.
- Bind named models with `v-model:x`; stop propagation on nested interactive
  elements (`@click.stop`) when the parent also handles the event.

## 8. Styling

- **Default to `<style module>`** (`$style.someClass`) with **camelCase** class
  names. Name classes after the component: a base class matching the component
  (`$style.tagInput`), child parts as `base + suffix` (`$style.tagInputChip`,
  `$style.tagInputField`), and state as a separate `is*` modifier on the same
  element (`.tagInput.isDisabled`). This prefix already isolates the classes, so
  scoping is largely redundant; use `<style scoped>` only if the project does.
- Toggle modifiers with an array/object binding:
  `:class="[$style.tagInput, { [$style.isDisabled]: disabled }]"`.
- **Custom / global / deep-selector CSS is a last resort.** Keep it minimal and
  leave a one-line comment explaining why the module route did not work.
- **Overriding a component library's internals** (when props, slots and design
  tokens truly cannot reach it) is done with `:local(.pane)` nested under your
  own base class. Functionally it is just a local class reference; writing
  `:local()` explicitly marks the class as foreign, deliberately reached into.
  This only resolves to the library's class when app and library share the same
  name-based CSS-modules mangling (for example both built with
  `@basmilius/vite-preset`); the one-line-comment rule above applies.
- **Theme through CSS custom properties** (design tokens), not by overriding
  internal selectors of other components. When the project has no token set, a
  standalone component can expose its own `var(--x, fallback)` properties so
  consumers can override them.

## 9. Whitespace

- **One blank line between the top-level groups** in `<script setup>` (imports,
  each macro block, constants, stores, state, composables, computed, watch,
  lifecycle)
  and between every `function` declaration.
- **No blank line between adjacent single-line declarations** in the same group
  (a run of refs or composables stays together).
- **Inside a function, one blank line separates logical steps:** after a
  guard/early-return block, and between setup and the action that follows.
- **In the template, one blank line between logically separate element groups.**
- One blank line between the `<template>`, `<script>`, `<style>`, and `<i18n>`
  blocks.

## Related skills

- **`vue-build-feature`** - splitting a feature across a view plus multiple
  components, composables, data access and a route.
- **`flux-ui`** - picking and composing components when the project uses Flux.
- The repo's **`CLAUDE.md` / `AGENTS.md`** - project-specific style, i18n and
  tooling rules that override the neutral defaults here.
