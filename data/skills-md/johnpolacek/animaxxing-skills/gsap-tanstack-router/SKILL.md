---
name: gsap-tanstack-router
description: "Build or review TanStack Router for React and TanStack Start animation: GSAP page transitions, component enter/exit, scroll effects, useBlocker, pending UI, route reuse, and cleanup. Use even when GSAP is unnamed, including choosing viewTransition. Also covers hidden-content recovery and first-load performance. Not for Solid, other routers, React without routing, or isolated GSAP API questions."
license: MIT
metadata:
  short-description: GSAP page and component lifecycles in TanStack Router
---

# GSAP TanStack Router

**mount → initial state → intro → settled → outro → end state → unmount**

Mount and unmount belong to React; animation owns the five phases between them. TanStack Router preserves shared layouts and can reuse routes on parameter changes; pending UI and loaders also affect when the new page appears.

Keep the requested look and existing project conventions. Add GSAP/plugins only as needed; do not replace the chosen animation library unless asked.

This skill decides when motion runs. For what moves, and for a feel such as premium or playful, also load the `animaxxing` skill when it is installed: its recipes and its guide to finding the vibe plug into this lifecycle.

## Start with the project

Read repository instructions, existing animation, layouts, navigation, CSS, accessibility conventions, and checks. Then:

1. Confirm `@tanstack/react-router`. Next.js belongs to `gsap-nextjs`, React Router to `gsap-react-router`, React without a router to `gsap-react`. Solid Router is out of scope.
2. Read the installed `@tanstack/react-router` version and, when present, `@tanstack/react-start`. Prefer their bundled types over memory: `node_modules/@tanstack/router-core/dist/esm/router.d.ts` for `RouterOptions`, `RouterState`, and `RouterEvents`, `node_modules/@tanstack/react-router/dist/esm/useBlocker.d.ts` for the blocker, `node_modules/@tanstack/history/dist/esm/index.d.ts` for history actions. The TanStack/router repository's `docs/router/` and `docs/start/` are the source of truth. The loading architecture changed during the 1.16x and 1.17x releases; `RouterState.isTransitioning` is gone from router-core 1.171.2x, and `useBlocker` is still marked experimental.
3. Tell file-based routes (`createFileRoute`, `routeTree.gen.ts`, `__root.tsx`) from code-based routes (`createRoute`, `createRootRoute`). The lifecycle is the same; only where route options live differs.
4. Tell TanStack Start (SSR, a root document shell with `HeadContent` and `Scripts`) from a client-only Vite app (`RouterProvider` rendered into a div). Client-only apps paint nothing before React, so they need no pre-paint rule. Check `ssr` per route, `defaultSsr`, `spa.enabled`, and prerendering.
5. Read the router options: `defaultPreload`, `defaultPendingComponent`, `defaultPendingMs`, `defaultPendingMinMs`, `defaultViewTransition`, `scrollRestoration`, `defaultStaleTime`, `defaultRemountDeps`. Each changes when pages mount and what the user sees while they load.

## Choose the engine

Use `defaultViewTransition` or Link/`navigate` `viewTransition` for snapshot morphs or page crossfades. Use GSAP for live-DOM outros that gate navigation, interruptible sequences, split text, or scroll-linked motion. One engine per element; see [combining engines](references/tanstack-navigation.md#combining-with-view-transitions).

## Read only what you need

- Invisible entrances, failed initialization, indexing, and first-load performance: [Initialization and recovery](references/initialization.md), plus the [framework integration](references/motion-system.md#initialization-and-recovery).
- Router APIs and the order of one navigation, outro before navigation with `useBlocker` or an intercepted Link, the lock, back and forward, pending UI, the swap gap, scroll, focus, View Transitions: [TanStack navigation](references/tanstack-navigation.md).
- Route reuse versus `remountDeps`, layouts and `Outlet`, the React lifecycle for GSAP, conditional content, TanStack Start SSR and hydration, deferred data: [Route lifetime](references/route-lifetime.md).
- The five phases, GSAP setup, show and hide, layout stability, scroll, text, plugins: [Lifecycle implementation](references/motion-system.md).
- Lenis, ScrollSmoother, or eased page scrolling across routes: [Smooth scrolling](references/smooth-scroll.md), plus the [TanStack integration](references/tanstack-navigation.md#smooth-scrolling).
- Curtains, first-visit preloaders, and shared-element morphs: [Transition archetypes](references/transition-archetypes.md), plus [where they live under TanStack Router](references/tanstack-navigation.md#curtains-preloaders-and-shared-elements).
- Touch, viewport changes, and device budgets: [Devices and input](references/devices.md).
- Tauri, Electron, or Wails desktop shells: [Desktop webviews](references/desktop-webviews.md).
- Before calling work done: [Verification](references/verification.md).

Install the [official GSAP skills](https://github.com/greensock/gsap-skills) alongside this repository. Load `gsap-core` for API details and `gsap-react` for component setup only as needed.

## Rules

- Preserve invisible intros on successful setup; recover the current incoming owner on failure. Follow the initialization contract before adding hiding rules.
- GSAP runs only on the client. `useGSAP` never runs on the server; keep GSAP calls out of module scope in files Start renders on the server. Scope selectors. Clean up every tween, trigger, split, and listener.
- Reserve final geometry with normal CSS and a stable wrapper; overlap outgoing/incoming content without doubling layout space.
- Mount, then set initial values, then paint. Successful initialization never flashes settled content before the intro. Under Start, server HTML paints before hydration, so hide intro targets only under a root attribute set by a `ScriptOnce` inline script, only during the initial phase, with a no-JavaScript path.
- Clear temporary styles at settled. Use `will-change` only while animating; this overrides `gsap-performance`'s static hint.
- Use capability queries for device tiers. Touch states release; controls work without hover.
- Keep outgoing pages mounted and visible through outro and end state. The router swaps only after every blocker allows the navigation and the loaders finish; resolve the blocker from the end callback.
- No router event fires before the URL changes. `onBeforeNavigate` runs after the history commit; only a blocker runs before it.
- A navigation to the same route with new params reuses the component. Run the lifecycle again against DOM that already holds settled values, keyed on the params, or set `remountDeps`.
- Back and forward arrive with `action` `BACK`, `FORWARD`, or `GO`. Never run an outro for them; the URL has already moved when the blocker runs. Give them an intro-only path after scroll restoration.
- `useLocation` moves to the destination when loading starts, before the new page mounts. Do not key route content on it; key on the presented matches or on `resolvedLocation`.
- Keep native link behavior, preloading, `activeProps`, focus, scroll, and no-JavaScript readability.
- Reduced motion reaches the same settled state and still fires every completion callback, including the one that lets the blocked navigation proceed.
- Define interruption and rapid-click behavior; completion must release navigation waits exactly once.
- Verify in a real browser when practical. Use a production build for route, config, dependency, or release changes.
