---
name: gsap-astro
description: "Build or review Astro animation: GSAP page transitions, ClientRouter swap hooks, persisted islands, repeated setup, and cleanup. Use for missing or duplicated motion after navigation and choosing transition:animate versus GSAP. Without ClientRouter, use gsap-vanilla. Also covers hidden-content recovery and first-load performance. Not for standalone island frameworks or isolated GSAP API questions."
license: MIT
metadata:
  short-description: GSAP page and component lifecycles in Astro
---

# GSAP Astro

**mount → initial state → intro → settled → outro → end state → unmount**

Without `<ClientRouter />`, use `gsap-vanilla` for full document loads. With it, mount and unmount correspond to body swaps; module scripts, global listeners, timelines, and persisted elements can survive. Animation owns the five phases between swaps.

Keep the requested look and existing project conventions. Add GSAP/plugins only as needed; do not replace the chosen animation library unless asked.

This skill decides when motion runs. For what moves, and for a feel such as premium or playful, also load the `animaxxing` skill when it is installed: its recipes and its guide to finding the vibe plug into this lifecycle.

## Start with the project

Read repository instructions, existing animation, layouts, navigation, CSS, accessibility conventions, and checks. Then:

1. Read the installed Astro version. Read `node_modules/astro/dist/transitions/router.js`, `swap-functions.js`, and `node_modules/astro/components/ClientRouter.astro` before trusting memory; the package ships no changelog, so check the release notes for that version. Version gates: `<ClientRouter />` (5.0; `<ViewTransitions />` in 4.x, removed in 6.0), lifecycle events with `loader` and `newDocument` (3.6), form navigation (4.0), `transition:persist-props` and `data-astro-rerun` (4.5), `swapFunctions` (4.15).
2. Find where `<ClientRouter />` is: the shared head, some pages, or nowhere, and its `fallback` prop. Nowhere means `gsap-vanilla`, including CSS `@view-transition`.
3. Find which framework integrations render islands and which `client:*` directives are in use.
4. Check `astro.config` for `prefetch` and `experimental.clientPrerender`.

## Choose the engine

Use `transition:name` / `transition:animate` for snapshot morphs, fades, or slides under ClientRouter. Use GSAP for live-DOM outros that hold the swap, interruptible sequences, split text, or scroll-linked motion. One engine per element; see [combining engines](references/client-router-navigation.md#combining-with-astros-animations).

## Read only what you need

- Invisible entrances, failed initialization, indexing, and first-load performance: [Initialization and recovery](references/initialization.md), plus the [framework integration](references/motion-system.md#initialization-and-recovery).
- The router's event sequence, outro before the swap, cleanup, initial state on the incoming page, direction, back and forward, scroll, focus, prefetch, fallback browsers: [ClientRouter navigation](references/client-router-navigation.md).
- Which scripts run again, listeners that outlive pages, custom elements, islands and `client:*` directives, `transition:persist`: [Scripts and islands](references/scripts-and-islands.md).
- The five phases, GSAP setup, contexts, show and hide, layout stability, scroll, text, plugins: [Lifecycle implementation](references/motion-system.md).
- Lenis, ScrollSmoother, or eased page scrolling across swaps: [Smooth scrolling](references/smooth-scroll.md), plus the [router integration](references/client-router-navigation.md#scroll).
- Curtains, first-visit preloaders, and shared-element morphs: [Transition archetypes](references/transition-archetypes.md), plus the [event mapping](references/client-router-navigation.md#curtains-preloaders-and-shared-elements).
- Touch, viewport changes, and device budgets: [Devices and input](references/devices.md).
- Before calling work done: [Verification](references/verification.md).

Install the [official GSAP skills](https://github.com/greensock/gsap-skills) alongside this repository. Load `gsap-core` for API details and `gsap-frameworks` for component setup only as needed.

## Rules

- Preserve invisible intros on successful setup; recover the current incoming owner on failure. Follow the initialization contract before adding hiding rules.
- GSAP runs after the DOM it targets exists. Scope selectors with `gsap.context` to the page or component root. Clean up every tween, trigger, split, and listener before the swap that removes its owner.
- A module script runs once per visit, not once per page. Setup runs from `astro:page-load` and is correct when it runs again on a new body or twice on the same one.
- Listeners on `document` and `window` outlive the page. Register router listeners once, in one place, and have each handler find the current page before acting.
- Reserve final geometry with normal CSS and a stable wrapper; overlap outgoing/incoming content without doubling layout space.
- Set initial values before paint, then reveal. On first load that is the inline head script; after a swap it is `astro:before-swap` and `astro:after-swap`. Successful initialization never flashes settled content before the intro, and never a blank page without JavaScript.
- Clear temporary styles at settled. Use `will-change` only while animating; this overrides `gsap-performance`'s static hint.
- Use capability queries for device tiers. Touch states release; controls work without hover.
- The outro plays on live DOM inside `event.loader` in `astro:before-preparation`, and the router waits for it. Never animate in `astro:before-swap`: the user is looking at a snapshot.
- Back and forward get an intro-only path. A traverse fires every event, so skip the outro on `navigationType === "traverse"` on purpose.
- Keep `transition:persist` elements out of page-level cleanup and page-level intros. They cross the swap alive, timelines included.
- Keep native link behavior, the router's history, scroll restoration, and route announcement. Do not add a click interceptor beside the router for motion; the only click listener is the capture-phase guard that holds the lock while a navigation is in flight.
- Cleanup before the swap kills the page context; it does not revert it. A revert writes the intro's start values back onto a body that is still attached.
- Reduced motion reaches the same settled state and still fires every completion callback. The router already disables its own animations under `prefers-reduced-motion`.
- Use timelines for sequences. Decide up front what happens on rapid clicks and interrupted animations: the router lets a second click abort the first navigation while its outro is running, so first-click-wins needs the lock guard.
- Verify in a real browser when practical, including a page visited twice, back, forward, and a click during an outro.
