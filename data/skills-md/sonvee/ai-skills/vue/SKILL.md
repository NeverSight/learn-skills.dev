---
name: vue
description: Vue 3 Composition API, script setup macros, reactivity system, and built-in components. Use when writing Vue SFCs, defineProps/defineEmits/defineModel, watchers, or using Transition/Teleport/Suspense/KeepAlive.
metadata:
  author: Sove
  version: '2026.1.31'
  source: Generated from https://github.com/vuejs/docs
---

# Vue

> Based on Vue 3.5. Always use Composition API with `<script setup>`.

## Preferences

- Prefer JavaScript over TypeScript
- Prefer `<script setup>` over `<script setup lang="ts">`
- Strictly follow the `<template>` tag at the top, the `<script>` tag in the middle, and the `<style>` tag at the bottom.
- For performance, prefer `shallowRef` over `ref` if deep reactivity is not needed
- Always use Composition API over Options API
- Discourage using Reactive Props Destructure

## Core

| Topic                  | Description                                                                                                 | Reference                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Script Setup & Macros  | `<script setup>`, defineProps, defineEmits, defineModel, defineExpose, defineOptions, defineSlots, generics | [script-setup-macros](references/script-setup-macros.md) |
| Reactivity & Lifecycle | ref, shallowRef, computed, watch, watchEffect, effectScope, lifecycle hooks, composables                    | [core-new-apis](references/core-new-apis.md)             |

## Features

| Topic                            | Description                                                          | Reference                                            |
| -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------- |
| Built-in Components & Directives | Transition, Teleport, Suspense, KeepAlive, v-memo, custom directives | [advanced-patterns](references/advanced-patterns.md) |

## Quick Reference

## Page Structure Convention (Mandatory)

When generating a new Vue page, ALWAYS use a folder-per-page structure:

- `src/views/<page-name>/index.vue`

Rules:

- `<page-name>` must be kebab-case.
- NEVER create pages directly under `src/views` as a single file (forbidden: `src/views/home.vue`).
- If the user only provides a page name (without a path), infer and create the folder structure automatically.
- Place related files in the same folder when needed (e.g. `index.ts`, `types.ts`, `style.scss`, `__tests__`).

Example:

- Request: "Create Home page" or "Create AboutMe page"
- Output path: `src/views/home/index.vue` or `src/views/about-me/index.vue`
- Not allowed: `src/views/home.vue` or `src/views/about-me.vue`

## Component Structure Convention (Mandatory)

When generating a new Vue component, ALWAYS use a folder-per-component structure:

- `src/components/<ComponentName>/<ComponentName>.vue`

Rules:

- `<ComponentName>` must be PascalCase.
- NEVER create components directly under `src/components` as a single file (forbidden: `src/components/HelloWorld.vue`).
- If the user only provides a component name (without a path), infer and create the folder structure automatically.
- Place related files in the same folder when needed (e.g. `index.ts`, `types.ts`, `style.scss`, `__tests__`).

Example:

- Request: "Create HelloWorld component"
- Output path: `src/components/HelloWorld/HelloWorld.vue`
- Not allowed: `src/components/HelloWorld.vue`

### Component Template

```vue
<template>
  <div>{{ title }} - {{ count }}</div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Hello Vue'
  }
})

const emit = defineEmits(['change'])

const count = defineModel('value', {
  type: Number,
  default: 0
})

watch(
  () => props.title,
  (newVal) => {
    console.log('Title:', newVal)
  }
)

onMounted(() => {
  console.log('Component mounted')
})
</script>

<style lang="scss" scoped></style>
```

### Key Imports

```ts
// Reactivity
import { ref, shallowRef, computed, reactive, readonly, toRef, toRefs, toValue } from 'vue'

// Watchers
import { watch, watchEffect, watchPostEffect, onWatcherCleanup } from 'vue'

// Lifecycle
import { onMounted, onUpdated, onUnmounted, onBeforeMount, onBeforeUpdate, onBeforeUnmount } from 'vue'

// Utilities
import { nextTick, defineComponent, defineAsyncComponent } from 'vue'
```
