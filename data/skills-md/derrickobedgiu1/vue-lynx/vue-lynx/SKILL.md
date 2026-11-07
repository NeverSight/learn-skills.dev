---
name: vue-lynx
description: "How to build native Lynx applications using Vue 3 with the vue-lynx custom renderer. Covers the dual-thread architecture, Lynx-native elements (<view>, <text>, <image>), the Lynx event system (:bindtap, :catchtap), Main Thread Script for performance-critical interactions, and ecosystem integration (Vue Router, Pinia, TanStack Query, Tailwind CSS). Use this skill whenever the user is building, debugging, or asking about Vue Lynx apps, converting Vue web code to Lynx, setting up a vue-lynx project, writing vue-lynx tests, or working with any Lynx-native UI. Also trigger when the user mentions lynx.config.ts, rspeedy, LynxExplorer, or imports from 'vue-lynx'."
---

# Vue Lynx

Vue Lynx is a Vue 3 custom renderer for [Lynx](https://vue.lynxjs.org). It lets you build native Lynx applications using Vue's Composition API, single-file components, and reactivity system. If you know Vue 3, you mostly know Vue Lynx — the differences are in elements, events, and the dual-thread runtime.

## The Three Things That Change from Vue Web

### 1. Import from `vue-lynx`

Vue Lynx re-exports the full Vue 3 API surface, so swap your import source:

```ts
import { ref, computed, onMounted, watch, nextTick } from 'vue-lynx'
```

### 2. Use Lynx elements instead of HTML

Lynx renders natively, not in a browser. There are no `<div>`, `<span>`, or `<img>` tags:

| HTML | Vue Lynx | Notes |
|------|----------|-------|
| `<div>` | `<view>` | General container |
| `<span>` | `<text>` | Text content (see caveat below) |
| `<img>` | `<image>` | Image element |
| scrollable `<div>` | `<scroll-view>` | Needs `scroll-orientation="vertical"` or `"horizontal"` |
| `<ul>` / `<li>` | `<list>` + `<list-item>` | Virtualized, lazy-loaded |
| `<input>` | `<input>` | `v-model` not yet supported (see workaround below) |

**Text wrapping caveat:** Lynx does not support bare text nodes inside `<view>`. All visible text needs a `<text>` wrapper, otherwise it silently won't render:

```vue
<!-- Won't render the text -->
<view>Hello</view>

<!-- Correct -->
<view><text>Hello</text></view>
```

### 3. Use Lynx events instead of DOM events

Lynx has its own event system. The most common change: `@click` becomes `:bindtap`.

| Pattern | Syntax | Propagation |
|---------|--------|-------------|
| Bubbling handler | `:bindtap="handler"` | Propagates up |
| Non-bubbling handler | `:catchtap="handler"` | Stops at this element |
| Capture phase | `:capture-bindtap="handler"` | Fires during capture, propagates |
| Capture + stop | `:capture-catchtap="handler"` | Fires during capture, stops |

Available event names: `tap`, `longtap`, `longpress`, `touchstart`, `touchmove`, `touchend`, `touchcancel`, `scroll`, `scrollend`, `focus`, `blur`, `layoutchange`, `transitionend`, `animationend`.

## Dual-Thread Architecture

Vue runs on a **background thread** while native rendering happens on the **main thread**. Changes flow as batched **ops** to the main thread; user interactions flow back as **events**. This keeps the UI responsive — Vue reconciliation never blocks rendering.

```
Background Thread (JS)              Main Thread (Native)
┌───────────────────────┐           ┌──────────────────────┐
│ Vue 3 runtime         │   ops     │ Native elements      │
│ Reactivity, components│ ────────> │ Layout & rendering   │
│ Lifecycle, your code  │           │ MTS handlers         │
│                       │ <──────── │ User events          │
└───────────────────────┘  events   └──────────────────────┘
```

**What this means in practice:**

- `onMounted()` fires when the component tree is built on the background thread. Native elements may not exist yet on the main thread. If you need to query native elements (layout, measurements), wrap in `nextTick()`:

```vue
<script setup lang="ts">
import { onMounted, nextTick } from 'vue-lynx'

onMounted(() => {
  nextTick(() => {
    // Native elements are now fully materialized
    lynx.createSelectorQuery()
      .select('.target')
      .invoke({ method: 'boundingClientRect', success: (res) => console.log(res) })
      .exec()
  })
})
</script>
```

If your `onMounted` only sets up reactive state, timers, or data fetching, `nextTick` isn't needed — those don't touch native elements.

- `nextTick()` resolves after a full cross-thread round trip (ops flushed, main thread applied), not just Vue's scheduler. Same mental model as Vue web's nextTick, extended across threads.

- There's no `document` or `window`. Libraries that depend on browser globals need adaptation. Lynx provides its own APIs via the `lynx` global object.

## Vue Feature Compatibility

Almost all of Vue 3's API surface works identically because Vue Lynx uses `@vue/runtime-core` directly:

**Works as expected:** `ref`, `reactive`, `computed`, `watch`, `watchEffect`, `provide`/`inject`, `defineComponent`, `<script setup>`, props, emits, `defineModel`, slots (default/named/scoped), `v-if`/`v-else`/`v-for`/`v-show`, `<style>`, `<style module>`, imported CSS files, `Suspense`, `defineAsyncComponent`, Options API.

**Experimental:** `<Transition>` and `<TransitionGroup>` work but need an explicit `:duration` prop (the background thread can't call `getComputedStyle()` to auto-detect duration).

**Not available:**
- `<KeepAlive>` — no native storage container equivalent
- `<Teleport>` — no `querySelector` for string targets across threads
- `<style scoped>` / `v-bind()` in CSS — not yet implemented
- `v-model` on native `<input>` — Lynx inputs use synchronous main-thread APIs that the background thread can't reach. Use the manual pattern:

```vue
<input :value="text" @input="(e) => text = e.detail.value" />
```

## Project Setup

Scaffold a new project:

```bash
npm create vue-lynx@latest
cd my-app && npm install && npm run dev
```

The build config lives in `lynx.config.ts`:

```ts
import { defineConfig } from '@lynx-js/rspeedy'
import { pluginVueLynx } from 'vue-lynx/plugin'

export default defineConfig({
  plugins: [
    pluginVueLynx({
      optionsApi: false,               // tree-shakes Options API (~9 kB savings)
      enableCSSSelector: true,         // default
      enableCSSInheritance: false,     // enable for CSS variables
      enableCSSInlineVariables: false,  // enable for --* in :style bindings
    }),
  ],
})
```

Entry point — no selector needed, it mounts to the Lynx page root:

```ts
import { createApp } from 'vue-lynx'
import App from './App.vue'
createApp(App).mount()
```

## Common Patterns

**Scroll view:**
```vue
<scroll-view scroll-orientation="vertical" style="height: 500px">
  <view v-for="item in items" :key="item.id">
    <text>{{ item.name }}</text>
  </view>
</scroll-view>
```

**Virtualized list** (for large datasets — Lynx handles lazy rendering):
```vue
<list scroll-orientation="vertical" style="height: 500px">
  <list-item v-for="item in items" :key="item.id" :item-key="item.id">
    <text>{{ item.name }}</text>
  </list-item>
</list>
```

**Dynamic styling** (workaround for missing `v-bind()` in CSS):
```vue
<script setup>
import { ref, computed } from 'vue-lynx'
const color = ref('#1565c0')
const style = computed(() => ({ color: color.value }))
</script>
<template>
  <text :style="style">Dynamic color</text>
</template>
```

## Deeper Topics

For more detailed guidance on specific areas, read the relevant reference file:

- **Performance-critical interactions** (scroll animations, touch gestures, eliminating cross-thread delay): Read `references/main-thread-script.md`
- **Ecosystem libraries** (Vue Router, Pinia, TanStack Query, Tailwind CSS setup and patterns): Read `references/ecosystem.md`
- **Testing** (vitest setup, dual-thread test environment, fireEvent, waitForUpdate): Read `references/testing.md`
