---
name: gsap-nextjs
description: "Build or review Next.js App Router animation: GSAP page transitions, component enter/exit, scroll effects, interrupted motion, and cleanup. Use even when GSAP is unnamed, including choosing React View Transitions. Also covers loading flashes, data-ready entrances, layout stability, hidden-content recovery, and first-load performance. Not for Pages Router, other routers, or isolated GSAP API questions."
license: MIT
metadata:
  short-description: GSAP page and component lifecycles in Next.js
---

# GSAP Next.js

**mount → initial state → intro → settled → outro → end state → unmount**

Mount and unmount belong to React; animation owns the five phases between them. With `cacheComponents`, treat route hide as unmount and re-show as mount on preserved DOM.

Keep the requested look and existing project conventions. Add GSAP/plugins only as needed; do not replace the chosen animation library unless asked.

This skill decides when motion runs. For what moves, and for a feel such as premium or playful, also load the `animaxxing` skill when it is installed: its recipes and its guide to finding the vibe plug into this lifecycle.

## Start with the project

Read repository instructions, existing animation, layouts, navigation, CSS, accessibility conventions, and checks. Then:

1. Confirm the App Router. If the project uses the Pages Router, use version-matched Pages Router guidance instead of this skill.
2. Read the installed Next.js version. Prefer its bundled docs in `node_modules/next/dist/docs/` over memory. Version gates: `onNavigate` and `useLinkStatus` (15.3), `<ViewTransition>` and `transitionTypes` (16.2), `<Activity>` route preservation when `cacheComponents` is enabled (16.0, opt-in).
3. Check the Next config for `cacheComponents`. It changes how long routes live.

## Choose the engine

Use React `<ViewTransition>` for shared-element morphs, page crossfades, and Suspense swaps when supported by the installed Next.js version. Use GSAP for live-DOM outros that gate navigation, interruptible sequences, split text, or scroll-linked motion. One engine per element; see [combining engines](references/app-router-navigation.md#combining-with-view-transitions).

## Read only what you need

- Invisible entrances, failed initialization, indexing, and first-load performance: [Initialization and recovery](references/initialization.md), plus the [framework integration](references/motion-system.md#initialization-and-recovery).
- Loading/auth flashes and shifting async sections: [Data readiness](references/initialization.md#data-readiness-and-layout-stability), plus [React data integration](references/motion-system.md#data-ready-entrances).
- Page intros and outros, transition-aware links, back and forward, focus, route swaps: [App Router navigation](references/app-router-navigation.md).
- The five phases, GSAP setup, React lifecycle, show and hide, layout stability, scroll, text, plugins: [Lifecycle implementation](references/motion-system.md).
- Lenis, ScrollSmoother, or eased page scrolling across routes: [Smooth scrolling](references/smooth-scroll.md), plus the [App Router integration](references/app-router-navigation.md#smooth-scrolling).
- Curtains, first-visit preloaders, and shared-element morphs: [Transition archetypes](references/transition-archetypes.md), plus [where they live in the App Router](references/app-router-navigation.md#curtains-and-preloaders).
- Touch, viewport changes, and device budgets: [Devices and input](references/devices.md).
- Tauri, Electron, or Wails desktop shells: [Desktop webviews](references/desktop-webviews.md).
- Before calling work done: [Verification](references/verification.md).

Install the [official GSAP skills](https://github.com/greensock/gsap-skills) alongside this repository. Load `gsap-core` for API details and `gsap-react` for component setup only as needed.

## Rules

- Preserve invisible intros on successful setup; recover the current incoming owner on failure. Follow the initialization contract before adding hiding rules.
- GSAP runs only on the client. Scope selectors. Clean up every tween, trigger, split, and listener.
- Reserve final geometry with normal CSS and a stable wrapper; overlap outgoing/incoming content without doubling layout space.
- Reveal each owner when its structural data is ready; unresolved auth or queries must not masquerade as guest or empty content.
- Mount, then set initial values, then paint. Successful initialization never flashes settled content before the intro.
- Clear temporary styles at settled. Use `will-change` only while animating; this overrides `gsap-performance`'s static hint.
- Use capability queries for device tiers. Touch states release; controls work without hover.
- Keep outgoing pages and components mounted and visible through outro and end state. Unmount, or let the router hide, only after the end callback.
- Under `cacheComponents`, a page lifecycle runs again on re-show against DOM that already holds settled values. Never assume a fresh node.
- Back and forward never run an outro. Give them an intro-only path.
- Keep native link behavior, focus, scroll, and no-JavaScript readability.
- Reduced motion reaches the same settled state and still fires every completion callback.
- Define interruption and rapid-click behavior; completion must release navigation waits exactly once.
- Verify in a real browser when practical. Use a production build for route, config, dependency, or release changes.
