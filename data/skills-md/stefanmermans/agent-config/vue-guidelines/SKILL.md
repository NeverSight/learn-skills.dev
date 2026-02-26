---
name: vue-guidelines
description: Essential guidelines for Vue.js development. Always follow these rules when working with Vue project.
---

# Vue Guidelines

This document outlines best practices for building robust, maintainable, and modern Vue.js applications using the Composition API and TypeScript.

## 1. General Principles

- **Composition API**: Always use the Composition API with `<script setup lang="ts">`.
- **Single File Components (SFC)**: Keep template, script, and style in one file.
- **Structure**: Order blocks as `<script setup>`, `<template>`, `<style>`.
- **Naming**: Use PascalCase for component filenames (e.g., `MyComponent.vue`).

## 2. TypeScript Integration

- **Strict Typing**: Enable strict mode in `tsconfig.json`. Avoid `any`.
- **Props**: Use `defineProps` with type-only declarations for better inference.

    ```vue
    <script setup lang="ts">
    interface Props {
      msg: string
      count?: number
    }
    
    // withDefaults is optional but recommended for default values
    const props = withDefaults(defineProps<Props>(), {
      count: 0
    })
    </script>
    ```

- **Emits**: Use `defineEmits` with type-only declarations.

    ```vue
    <script setup lang="ts">
    const emit = defineEmits<{
      (e: 'update', value: number): void
      (e: 'close'): void
    }>()
    </script>
    ```

## 3. Reactivity Fundamentals

- **ref vs reactive**: Prefer `ref` for most cases, especially for primitives and when you need to replace the entire object. Use `reactive` sparingly for grouped state where structure matters.
- **Unwrapping**: Remember `.value` is required in `<script>` but unwrapped in `<template>`.
- **Destructuring**: Be careful destructuring `reactive` objects; use `toRefs` to maintain reactivity.

    ```ts
    const state = reactive({ count: 0 })
    const { count } = toRefs(state) // count is now a Ref
    ```

## 4. Component Patterns

- **Composables**: Extract logic into reusable composables (use... functions). Start with `use`.

    ```ts
    // useCounter.ts
    export function useCounter() {
      const count = ref(0)
      const increment = () => count.value++
      return { count, increment }
    }
    ```

- **Slots**: Use slots for flexible content injection. Named slots for multiple insertion points.
- **Provide/Inject**: Use for deep prop drilling, but prefer explicit props for direct parent-child communication. Key injection symbols to avoid collisions.
- **Splitting components**: Split components into smaller, focused components to improve maintainability and reusability. A components should't do too many things at once. Also if you feel the need to start adding comments for structure you should probably split the component into smaller ones instead of adding comments.

## 5. State Management

- **Pinia**: Use Pinia for global state. It's the official recommendation over Vuex.
- **Setup Stores**: Prefer "Setup Stores" (function style) in Pinia for consistency with Composition API.

    ```ts
    export const useUserStore = defineStore('user', () => {
      const user = ref(null)
      const isLoggedIn = computed(() => !!user.value)
      function login() { /* ... */ }
      
      return { user, isLoggedIn, login }
    })
    ```

## 6. Performance

- **v-memo**: Use `v-memo` for optimization of large lists or complex sub-trees.
- **v-once**: Use for static content that never changes.
- **Lazy Loading**: Use `defineAsyncComponent` for route components or heavy distinct sections.
- **Computed Stability**: Ensure computed properties are side-effect free and stable.

## 7. Style Guide

- **Scoped Styles**: Always use `<style scoped>`.
- **CSS Variables**: Use CSS variables for theming to allow dynamic changes.
- **BEM/Utility**: Follow BEM or a utility interaction pattern (like Tailwind) consistent with the project.
