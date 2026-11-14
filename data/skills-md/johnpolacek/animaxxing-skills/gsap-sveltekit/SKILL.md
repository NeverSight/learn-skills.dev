---
name: gsap-sveltekit
description: "Build or review SvelteKit animation on Svelte 5: GSAP page transitions, component enter/exit, scroll effects, route reuse, and cleanup. Use for interrupted navigation or choosing GSAP, Svelte transitions, or View Transitions, even when GSAP is unnamed. Also covers hidden-content recovery and first-load performance. Not for plain Svelte or isolated GSAP API questions."
license: MIT
metadata:
  short-description: GSAP page and component lifecycles in SvelteKit
---

# GSAP SvelteKit

**mount → initial state → intro → settled → outro → end state → unmount**

Mount and unmount belong to Svelte; animation owns the five phases between them. SvelteKit reuses pages on parameter changes and preserves shared layouts, so a new page lifecycle need not mean a new node.

Keep the requested look and existing project conventions. Add GSAP/plugins only as needed; do not replace the chosen animation library unless asked.

This skill decides when motion runs. For what moves, and for a feel such as premium or playful, also load the `animaxxing` skill when it is installed: its recipes and its guide to finding the vibe plug into this lifecycle.

## Start with the project

Read repository instructions, existing animation, layouts, navigation, CSS, accessibility conventions, and checks. Then:

1. Confirm SvelteKit with Svelte 5 in runes mode. Plain Svelte without SvelteKit routing belongs to `gsap-frameworks`. For Svelte 4 or legacy mode, say so and map `$effect` advice onto `onMount` and `onDestroy`.
2. Read the installed `@sveltejs/kit` and `svelte` versions. Prefer their bundled types over memory: `node_modules/@sveltejs/kit/types/index.d.ts` documents every navigation object, and `node_modules/svelte/types/index.d.ts` the runes and lifecycle exports. Version gates: `onNavigate` (1.24), `$app/state` (2.12; use `$app/stores` before), `to.scroll` on navigation targets (2.51), `prefersReducedMotion` in `svelte/motion` (5.7), `{@attach}` (5.29).
3. Check `svelte.config.js`, page options (`ssr`, `csr`, `prerender`), `data-sveltekit-preload-data` on `body` in `src/app.html`, and links marked `data-sveltekit-reload`. A page with `csr = false` has no client router and no navigation hooks; a reload link is a full document load. Treat both as plain documents.

## Choose the engine

Use Svelte `transition:` / `in:` / `out:` for simple block motion and `{#key}` swaps that only need DOM retention through an outro. Use View Transitions from `onNavigate` for snapshot morphs or page crossfades. Use GSAP for live-DOM navigation holds, interruptible sequences, split text, or scroll-linked motion. One engine per element; see [combining engines](references/page-lifetime.md#combining-engines).

## Read only what you need

- Invisible entrances, failed initialization, indexing, and first-load performance: [Initialization and recovery](references/initialization.md), plus the [framework integration](references/motion-system.md#initialization-and-recovery).
- Navigation hooks and their order, outro before navigation, the lock, back and forward, scroll, focus, links, preloading, View Transitions: [SvelteKit navigation](references/sveltekit-navigation.md).
- Page reuse versus remount, layouts, `{#key}` versus `afterNavigate`, the Svelte 5 lifecycle, Svelte transitions beside GSAP, shallow-routed modals, SSR: [Page lifetime](references/page-lifetime.md).
- The five phases, GSAP setup, contexts, show and hide, layout stability, scroll, text, plugins: [Lifecycle implementation](references/motion-system.md).
- Lenis, ScrollSmoother, or eased page scrolling across routes: [Smooth scrolling](references/smooth-scroll.md), plus the [hook mapping](references/sveltekit-navigation.md#settled-state-focus-and-scroll).
- Curtains, first-visit preloaders, and shared-element morphs: [Transition archetypes](references/transition-archetypes.md), plus the [layout integration](references/sveltekit-navigation.md#curtains-preloaders-and-shared-elements).
- Touch, viewport changes, and device budgets: [Devices and input](references/devices.md).
- Tauri, Electron, or Wails desktop shells: [Desktop webviews](references/desktop-webviews.md).
- Before calling work done: [Verification](references/verification.md).

Install the [official GSAP skills](https://github.com/greensock/gsap-skills) alongside this repository. Load `gsap-core` for API details and `gsap-frameworks` for component setup only as needed.

## Rules

- Preserve invisible intros on successful setup; recover the current incoming owner on failure. Follow the initialization contract before adding hiding rules.
- GSAP runs only in the browser. `onMount` and `$effect` never run on the server; module-level code needs a `browser` guard. Scope selectors with `gsap.context` to a `bind:this` root. Clean up every tween, trigger, split, and listener in the effect teardown or the `onMount` return.
- Reserve final geometry with normal CSS and a stable wrapper; overlap outgoing/incoming content without doubling layout space.
- Mount, then set initial values, then paint. Successful initialization never flashes settled content before the intro. Server HTML paints before hydration, so hide intro targets only under a root attribute set by an inline script, only during the initial phase, with a no-JavaScript path.
- Clear temporary styles at settled. Use `will-change` only while animating; this overrides `gsap-performance`'s static hint.
- Use capability queries for device tiers. Touch states release; controls work without hover.
- Keep outgoing pages mounted and visible through outro and end state. Hold the navigation with `beforeNavigate` and re-issue it from the end callback, or return the outro's promise from `onNavigate`. The URL changes before `onNavigate` runs, so only the first keeps it unchanged during the outro.
- A navigation to the same route with new params updates the page in place. Run the lifecycle again from `afterNavigate` against DOM that already holds settled values, or remount with `{#key}`.
- Back and forward arrive as `popstate` through the same hooks. Never run an outro for them. Give them an intro-only path after scroll restoration.
- Do not read `page`, `data`, or `navigating` inside the effect that builds GSAP setup unless it should rebuild on every navigation.
- One engine per element. An `out:` directive on a node GSAP also animates fights it, and the block stays in the DOM until the directive finishes.
- Keep native link behavior, `data-sveltekit-*` options, focus, scroll, and no-JavaScript readability.
- Reduced motion reaches the same settled state and still fires every completion callback. Svelte transitions ignore CSS reduced-motion rules; zero them from `prefersReducedMotion`.
- Define interruption and rapid-click behavior; completion must release navigation waits exactly once.
- Verify in a real browser when practical. Use a production build for route, config, dependency, or release changes.
