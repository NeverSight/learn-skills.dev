---
name: gsap-vanilla
description: "Build or review animation on plain HTML/CSS/JavaScript sites: GSAP page intros/outros, component show/hide, scroll effects, cross-document View Transitions, bfcache, and fetch/swap navigation with Swup, Barba, or Taxi. Use for first-paint flashes or interrupted navigation, even when GSAP is unnamed. Also covers hidden-content recovery and first-load performance. Not for component frameworks or isolated GSAP API questions."
license: MIT
metadata:
  short-description: GSAP page and component lifecycles on plain HTML sites
---

# GSAP Vanilla

**mount → initial state → intro → settled → outro → end state → unmount**

On full document loads, the browser owns mount and unmount; animation owns the five phases between them. On same-document swaps, the router owns node replacement and persistent resources need explicit cleanup.

Keep the requested look and existing project conventions. Add GSAP/plugins only as needed; do not replace the chosen animation library unless asked.

This skill decides when motion runs. For what moves, and for a feel such as premium or playful, also load the `animaxxing` skill when it is installed: its recipes and its guide to finding the vibe plug into this lifecycle.

## Start with the project

Read repository instructions, existing animation, layouts, navigation, CSS, accessibility conventions, and checks. Then:

1. Find out how pages are produced: hand-written HTML, a static generator with no client framework, a bundler such as Vite with no UI framework, or a transition library such as Swup, Barba, or Taxi. If a component framework renders the pages, say this skill does not cover it and use that framework's skill.
2. Find out how GSAP loads: npm import, import map, or script tag. Keep it.
3. Find out how scripts run: inline, `defer`, or `type="module"`. This decides when the DOM exists and whether the page can paint before the script runs.
4. Check the target browsers. Cross-document View Transitions, `pageswap` and `pagereveal`, the Navigation API, and `blocking="render"` are not everywhere. Read installed transition-library docs/types and feature-detect browser APIs instead of trusting memory, and make sure the site works with all of them missing.

## Pick a navigation model

Identify the navigation model before writing lifecycle code. Assign one owner per navigation; a same-document router may still need a full-load fallback.

- **Full document loads.** Every link replaces the document. The outro plays before the link is followed; the intro plays when the new page loads. This is the default and needs no router.
- **Full document loads with cross-document View Transitions.** The browser snapshots the old page and animates to the new one. GSAP fills in what a snapshot pair cannot do.
- **Same-document navigation.** Script fetches the next page and swaps content in place, so chrome, state, and timelines survive. Use a maintained library unless the project already owns a router or has a reason to. See [Same-document navigation](references/spa-navigation.md).

## Choose the engine

Use cross-document View Transitions for snapshot morphs or page crossfades, with an instant-swap fallback. Use GSAP for live-DOM outros that gate navigation, interruptible sequences, split text, or scroll-linked motion. One engine per element; see [combining engines](references/cross-document-navigation.md#combining-with-gsap).

## Read only what you need

- Invisible entrances, failed initialization, indexing, and first-load performance: [Initialization and recovery](references/initialization.md), plus the [framework integration](references/motion-system.md#initialization-and-recovery).
- First paint, script timing, fonts, navigation type, prerendering, the bfcache, hidden tabs, and leaving a page with an outro: [Page load and unload](references/page-load.md).
- `@view-transition`, `pageswap`, `pagereveal`, types, render blocking, and handing off between the browser and GSAP: [Cross-document navigation](references/cross-document-navigation.md).
- Fetch and swap routers, link interception, history, scroll, focus, script re-execution, and when to use a library: [Same-document navigation](references/spa-navigation.md).
- The five phases, GSAP setup, contexts, show and hide, layout stability, scroll, text, plugins: [Lifecycle implementation](references/motion-system.md).
- Lenis, ScrollSmoother, or eased page scrolling across documents and swaps: [Smooth scrolling](references/smooth-scroll.md), plus [per-document scrollers](references/page-load.md#smooth-scrolling) and [one scroller under a swap router](references/spa-navigation.md#smooth-scrolling-curtains-and-shared-elements).
- Curtains, first-visit preloaders, and shared-element morphs: [Transition archetypes](references/transition-archetypes.md), plus the [full-document](references/page-load.md#curtains-and-preloaders) and [same-document](references/spa-navigation.md#smooth-scrolling-curtains-and-shared-elements) integration.
- Touch, viewport changes, and device budgets: [Devices and input](references/devices.md).
- Before calling work done: [Verification](references/verification.md).

Install the [official GSAP skills](https://github.com/greensock/gsap-skills) alongside this repository. Load `gsap-core` for API details and the relevant plugin skill only as needed.

## Rules

- Preserve invisible intros on successful setup; recover the current incoming owner on failure. Follow the initialization contract before adding hiding rules.
- GSAP runs after the DOM it targets exists. Scope selectors with `gsap.context` to the page or component root. Clean up every tween, trigger, split, and listener when its owner goes away.
- Reserve final geometry with normal CSS and a stable wrapper; overlap outgoing/incoming content without doubling layout space.
- Set initial values before first paint, then reveal. Successful initialization never flashes settled content before the intro, and never a blank page without JavaScript.
- Clear temporary styles at settled. Use `will-change` only while animating; this overrides `gsap-performance`'s static hint.
- Use capability queries for device tiers. Touch states release; controls work without hover.
- Keep outgoing content in the DOM and visible through outro and end state. Follow the link, remove the node, or swap only from the end callback.
- Back and forward never run an outro. A fresh document reached by history gets an intro-only path, and a bfcache restore gets no intro at all.
- A prerendered page sets initial state at once and waits for activation before it animates.
- Keep native link behavior, focus, scroll restoration, and no-JavaScript readability.
- Never add `unload` or `beforeunload` listeners for animation. They disable the bfcache. Use `pagehide`.
- Reduced motion reaches the same settled state and still fires every completion callback.
- Define interruption and rapid-click behavior; completion must release navigation waits exactly once.
- Verify in a real browser when practical, including reload, back, forward, and a click from a background tab.
