---
name: taste-gsap
description: |
  GSAP implementation craft for agent-built sites: timeline architecture, gsap.context and matchMedia, ScrollTrigger pin and scrub hygiene, SplitText discipline, transform-only animation, refresh-after-fonts, and full prefers-reduced-motion gating. The 90% of award-tier motion is structure, not effects — this is that 90%. Use whenever generating GSAP animation code. Stack on the design-taste core skill and taste-motion.
triggers:
  - "gsap"
  - "scrolltrigger"
  - "scroll animation"
  - "pinned section"
  - "scrub"
  - "splittext"
  - "smooth scroll"
  - "web animation"
  - "scrolltrigger"
  - "site of the day"
---

# taste-gsap

> GSAP is a scalpel, not a glitter gun. One clean pinned section beats nine parallax layers — and survives a code review.

## 1. ARCHITECTURE (The Non-Negotiable Shell)

- Wrap every page's animations in a single `gsap.context(() => { ... }, rootElement)` — it scopes selectors and gives you instant teardown.
- Gate everything through `gsap.matchMedia()`:
  - `(prefers-reduced-motion: no-preference)` — all animation lives here. Reduced-motion users get the static, complete page.
  - `(min-width: 768px)` — heavy effects (pins, scrubs, per-character splits) desktop-only; small screens get fades or nothing.
- The matchMedia callback returns a cleanup function; on SPAs, call `ctx.revert()` on unmount.
- One timeline per section, named by section; never one giant global timeline with 40 tweens.
- Lenis (free, not ScrollSmoother): `new Lenis({ duration: ~1.1, anchors: true })`, pipe it to ScrollTrigger with `lenis.on("scroll", ScrollTrigger.update)` + `gsap.ticker.add(t => lenis.raf(t * 1000))` + `gsap.ticker.lagSmoothing(0)`. `lenis.stop()` during the preloader, `lenis.start()` after. Never smooth-scroll under reduced motion.

## 2. PIN & SCRUB HYGIENE (Where Agents Fail Loudest)

- **Max two pinned sections per page.** Every pin costs the scroll thread. Two is the budget; one is the norm.
- Pins: `pin: true, pinSpacing: true` (default — keep it), `start: "top top"`, `end: "+=200%"` to `"+=300%"`. Longer ends = slower scrub = more jank on mobile.
- Horizontal galleries (the signature Awwwards move): pin the *section*, translate the *track* (`x` only, never `left`), `end: () => "+=" + (track.scrollWidth - innerWidth)` so the distance recalculates on resize, `scrub: 1`, desktop-only. Native `overflow-x` + scroll-snap must remain as the no-JS / reduced-motion fallback.
- Drag carousels (Magma-school): `Draggable.create(track, { type: "x", inertia: true, bounds: () => ({ minX: -(track.scrollWidth - wrap.offsetWidth), maxX: 0 }) })` — bounds as a *function* so it recalibrates on resize. `edgeResistance` ~0.9, native `overflow-x` + snap as the no-JS fallback, and a cursor/UI hint that the strip is draggable.
- `scrub: 0.6`–`1` on heavy sections; `scrub: true` only on trivial tweens. A scrubbed tween without smoothing fights the scroll.
- Never pin inside another pin; never start a second pin before the first's spacer ends. `ScrollTrigger.refresh()` after fonts/images (`window.load` + `document.fonts.ready`) or everything misaligns.
- Test pins at 768px width before shipping — pinned sections that trap mobile users are a bug, not a feature (this is why pins live in the `(min-width: 768px)` gate).
- `invalidateOnRefresh: true` on refresh-dependent triggers so re-layouts don't drift.

## 3. WHAT TO ANIMATE (Transform and Opacity Only)

- Animate `x`, `y`, `scale`, `rotation`, `opacity` — never `top/left/width/height/margin/filter` (layout thrash = jank).
- Text reveals: line-level splits (`overflow: hidden` wrapper + `yPercent: 110` → 0) by default. Character-level only for hero headlines, and only inside the desktop gate.
- No `will-change` spam — set it on the animated element's wrapper while animating, remove after (or let GSAP manage it). Every `will-change` is a memory promise.
- Keep 60fps honesty: no 200-element stagger in one frame, no scrubbing 40 DOM properties. Batch with `gsap.utils.toArray` and stagger — one tween, many targets, cheap.

## 4. REVEAL PATTERNS (The Professional's Defaults)

- **From-states stay in code, not CSS:** elements start visible in CSS; `gsap.from(...)` with `immediateRender: true` inside the matchMedia gate hides them only when JS + motion are active. If GSAP never loads, the page is complete — this is the safety contract.
- Standard reveal: `opacity: 0, y: 40, duration: 0.9, ease: "power3.out"`, trigger `top 82%`, `once: true` for content sections.
- Hero intro: a `gsap.timeline()` on load — 80–120ms stagger between elements, `ease: "expo.out"` or `power4.out`, total under 1.4s. The page is a story with a first line, not a slideshow.
- Count-ups: tween a proxy object (`gsap.to(obj, { v: target })`), write `el.textContent` in `onUpdate`, `snap` optional. `once: true` on the trigger.

## 5. THE FULL STACK OF SINS (Each Is a Fail)

- Scroll-jacking the wheel without a smooth-scroll layer (Lenis) and then not testing it — native scroll is a feature.
- Animations that trigger before the content exists (missing `ScrollTrigger.refresh()`).
- Infinite marquees that aren't paused under reduced motion — kill them in CSS with `@media (prefers-reduced-motion: reduce)` too, not just in JS.
- Autoplaying anything: hero video, accordions, carousels that move without input. Awwwards confidence is stillness between moments.
- A page whose "wow" depends on animation: if the still screenshot is boring, the animation is makeup, not design.

## 6. CHECKLIST (Fail the Animation If…)

- [ ] No `gsap.context` + `matchMedia` gating (reduced-motion users see animation).
- [ ] More than two pinned sections, or a pin under 768px.
- [ ] Any animated layout property (`top/left/width/height`).
- [ ] No `ScrollTrigger.refresh()` after fonts/images.
- [ ] Per-character splits outside the desktop gate.
- [ ] Marquee or autoplay without a reduced-motion kill switch.
- [ ] The still frame (no JS) isn't a complete, beautiful page.
- [ ] Any animation that exists for its own sake — every move serves the story or dies.
