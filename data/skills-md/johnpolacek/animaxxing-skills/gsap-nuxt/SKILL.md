---
name: gsap-nuxt
description: "Build or review Nuxt 3/4 animation: GSAP pageTransition and layoutTransition hooks, component enter/exit, scroll effects, keepalive, and cleanup. Use for interrupted navigation, missing done callbacks, or choosing Vue CSS and View Transitions, even when GSAP is unnamed. Also covers hidden-content recovery and first-load performance. Not for plain Vue or isolated GSAP API questions."
license: MIT
metadata:
  short-description: GSAP page and component lifecycles in Nuxt
---

# GSAP Nuxt

**mount → initial state → intro → settled → outro → end state → unmount**

Mount and unmount belong to Vue; animation owns the five phases between them. During a Nuxt page leave, the component is torn down while its root element remains until `done`. The transition hooks (`css: false`) must own the outro independently of component cleanup.

Keep the requested look and existing project conventions. Add GSAP/plugins only as needed; do not replace the chosen animation library unless asked.

This skill decides when motion runs. For what moves, and for a feel such as premium or playful, also load the `animaxxing` skill when it is installed: its recipes and its guide to finding the vibe plug into this lifecycle.

## Start with the project

Read repository instructions, existing animation, layouts, navigation, CSS, accessibility conventions, and checks. Then:

1. Confirm Nuxt with a `pages/` directory. If the project is plain Vue with Vue Router and no Nuxt, say this skill does not cover it and use `gsap-frameworks`.
2. Read the installed Nuxt, Vue, and Vue Router versions from `node_modules`. Prefer the installed types and their JSDoc (`node_modules/@nuxt/schema`, `node_modules/nuxt/dist`, `node_modules/@vue/runtime-core/dist`, `node_modules/vue-router/dist`) and that version's docs over memory. Version gates: `onPrehydrate` (3.12), `useRuntimeHook` (3.14), the `app/` source directory (4), view transition types (4.4), `prefetch` in the `<NuxtLink custom>` slot (4.5).
3. Read `nuxt.config`: `ssr`, `srcDir`, `app.pageTransition`, `app.layoutTransition`, `app.keepalive`, `experimental.viewTransition`, `future.compatibilityVersion`. Nuxt 4 puts `pages/`, `layouts/`, `middleware/`, `plugins/`, `composables/`, `app.vue`, and `router.options.ts` under `app/`; Nuxt 3 keeps them at the root. `~/` resolves to the source directory in both.

## Choose the engine

Use Vue Transition CSS for simple page fades/slides, `experimental.viewTransition` for snapshot morphs, and GSAP JavaScript hooks for live-DOM outros, sequencing, interruption, or controlled overlap. Use one engine per element and do not run Vue hooks and a view transition on the same navigation. See [View Transitions](references/navigation.md#view-transitions).

## Read only what you need

- Invisible entrances, failed initialization, indexing, and first-load performance: [Initialization and recovery](references/initialization.md), plus the [framework integration](references/motion-system.md#initialization-and-recovery).
- The hooks, `done`, modes, what dies when the leave starts, first load, layouts, direction, interruptions: [Page transitions](references/page-transitions.md).
- Page keys, keepalive, Nuxt app hooks, scroll and focus, outro before navigation, back and forward, View Transitions, SSR and first paint: [Navigation](references/navigation.md).
- The five phases, GSAP setup, Vue lifecycle, show and hide, layout stability, scroll, text, plugins: [Lifecycle implementation](references/motion-system.md).
- Lenis, ScrollSmoother, or eased page scrolling across routes: [Smooth scrolling](references/smooth-scroll.md), plus the [hook mapping](references/navigation.md#scroll-and-focus).
- Curtains, first-visit preloaders, and shared-element morphs: [Transition archetypes](references/transition-archetypes.md), plus the [app.vue integration](references/navigation.md#curtains-and-preloaders) and [shared elements](references/navigation.md#outro-before-navigation).
- Touch, viewport changes, and device budgets: [Devices and input](references/devices.md).
- Before calling work done: [Verification](references/verification.md).

Install the [official GSAP skills](https://github.com/greensock/gsap-skills) alongside this repository. Load `gsap-core` for API details and `gsap-frameworks` for component setup only as needed.

## Rules

- Preserve invisible intros on successful setup; recover the current incoming owner on failure. Follow the initialization contract before adding hiding rules.
- GSAP runs only on the client. Guard with `import.meta.client`, `onMounted`, or `<ClientOnly>`. Scope selectors. Clean up every tween, trigger, split, and listener.
- Reserve final geometry with normal CSS and a stable wrapper; overlap outgoing/incoming content without doubling layout space. Pages and layouts need a single root element or the transition does not run.
- Mount, then set initial values, then paint. `onBeforeEnter` runs before the incoming root is inserted and `onEnter` right after, before the browser paints. Successful initialization never flashes settled content before the intro.
- Clear temporary styles at settled. Use `will-change` only while animating; this overrides `gsap-performance`'s static hint.
- Use capability queries for device tiers. Touch states release; controls work without hover.
- Always call `done`: from `onComplete`, from `onInterrupt`, and synchronously under reduced motion. A leave that never calls `done` leaves the old page in the DOM forever.
- The page component is unmounted, or deactivated under keepalive, when the leave starts, not when it ends. Its context revert and `onUnmounted` run while the outro plays. Build the outro in `onLeave` against `el`, in a context the hooks own.
- Keep outgoing pages and components in the DOM through outro and end state. Vue does this as long as `done` waits.
- The outro cannot start before the incoming page has resolved. Design the wait: the old page stays on screen and interactive.
- Under keepalive, a page lifecycle runs again on reactivation against DOM that already holds settled values. Never assume a fresh node.
- Back and forward run the same hooks as a click. Detect history navigation yourself and give it a quieter path. Never fake an outro that did not happen.
- Never use `appear` on a server-rendered page: Vue's SSR wraps the child of `<Transition appear>` in `<template>`, so the page is blank until hydration and without JavaScript.
- Keep native link behavior, focus, scroll, and no-JavaScript readability.
- Reduced motion reaches the same settled state and still calls `done` and every completion callback.
- Define interruption and rapid-click behavior; completion must release navigation waits exactly once.
- Verify in a real browser when practical. Use a production build for route, config, dependency, or release changes.
