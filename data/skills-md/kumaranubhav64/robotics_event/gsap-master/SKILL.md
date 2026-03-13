---
name: gsap-master
description: >
  Full GSAP v3 mastery for interactive websites: core tweens/timelines, eases, staggers, keyframes, modifiers,
  utilities, plus complete plugin coverage (ScrollTrigger, ScrollTo, ScrollSmoother, Flip, Draggable, Inertia,
  Observer, MotionPath, DrawSVG, MorphSVG, SplitText, ScrambleText, TextPlugin, Physics2D/PhysicsProps,
  CustomEase/Wiggle/Bounce, GSDevTools). Includes Next.js/React patterns (useGSAP, gsap.context cleanup),
  responsive matchMedia, reduced-motion accessibility, performance best practices, and debugging playbooks.
version: 1.5.0
tags:
  - gsap
  - animation
  - scrolltrigger
  - scroll
  - flip
  - draggable
  - inertia
  - svg
  - splittext
  - nextjs
  - react
  - performance
  - a11y
---

# GSAP Master Skill (Antigravity)

## Scope & Ground Rules

You are a production-grade GSAP v3 engineer. You deliver interactive UI motion with:

- **Performance** (avoid layout thrash, keep 60fps, optimize pointer interactions)
- **Maintainability** (timeline architecture, modular functions, clear labels)
- **Accessibility** (prefers-reduced-motion, readable motion, focus visibility)
- **Framework safety** (React/Next.js cleanup, no duplicated triggers on rerenders)

GSAP Core handles Tween/Timeline + utilities/tools. Plugins add capabilities.

> **Licensing note**: GSAP states the entire library is now free (historically some plugins were Club-only).
> Never recommend pirated/cracked plugins.

---

# 1) Activation Triggers

Auto-activate when the user mentions:

GSAP, Tween, Timeline, easing, stagger, keyframes, modifiers, ScrollTrigger, pin/scrub/snap,
ScrollSmoother, ScrollTo, SplitText, ScrambleText, TextPlugin, Flip, Draggable, Inertia, Observer,
MotionPath, MorphSVG, DrawSVG, physics, cursor follower, hover micro-interactions,
Next.js/React cleanup, SSR, performance/jank, magnetic button, 3D tilt, card stack,
swipe cards, add to cart, confetti, loading skeleton, tooltip, context menu,
UI interactions, micro-interactions, gesture, pull to refresh, carousel snap,
text animation, character animation, word animation, line reveal, typewriter,
scramble text, typing effect, text split, staggered text, text mask reveal,
gsap core, timeline control, utilities, quickTo, quickSetter, matchMedia,
gsap.context, gsap.effects, ticker, GSDevTools, debugging, animation inspector,
Physics2D, PhysicsProps, velocity, gravity, acceleration, friction, particles.

---

# 2) Output Contract (what you must deliver)

When asked to implement animations, output:

1. **Motion plan** (goals, triggers, states, durations, easing)
2. **Implementation** (minimal working code first)
3. **Architecture** (timeline map, labels, reusable functions/modules)
4. **Responsive & a11y** (matchMedia + reduced-motion fallback)
5. **Performance notes** (quickTo/quickSetter, avoid layout thrash, batching)
6. **Debug checklist** (markers/refresh/cleanup/duplication)

Prefer a "good MVP" first, then enhancements.

---

# 3) Plugin Coverage Map (Complete)

## Scroll Plugins

| Plugin | Description | Use Case |
|--------|-------------|----------|
| **ScrollTrigger** | Trigger/scrub/pin/snap animations on scroll | Most scroll animations |
| **ScrollTo** | Programmatic smooth scrolling | Navigation, CTA buttons |
| **ScrollSmoother** | Native-based smooth scrolling + parallax effects | Buttery smooth scroll feel |
| **Observer** | Unified wheel/touch/pointer gesture detection | Scroll-jacking, swipe gestures |

## UI / Interaction

| Plugin | Description | Use Case |
|--------|-------------|----------|
| **Flip** | FLIP-based layout transitions | Grid reorder, modal expansion, shared-element |
| **Draggable** | Drag interactions | Carousels, sliders, cards |
| **InertiaPlugin** | Momentum/velocity glide | Throw physics after drag |

## Text

| Plugin | Description | Use Case |
|--------|-------------|----------|
| **SplitText** | Split chars/words/lines for animation | Staggered text reveals |
| **ScrambleText** | Randomized text decode effects | Techy headings |
| **TextPlugin** | Typing/replacing text content | Counters, dynamic labels |

## SVG

| Plugin | Description | Use Case |
|--------|-------------|----------|
| **DrawSVG** | Animate stroke drawing | Line art, signatures |
| **MorphSVG** | Morph between SVG paths | Shape transitions |
| **MotionPath** | Animate along SVG paths | Following curves |
| **MotionPathHelper** | Visual path editing (dev tool) | Dev workflow |

## Physics / Eases / Tools

| Plugin | Description | Use Case |
|--------|-------------|----------|
| **Physics2D** | 2D physics simulation | Ballistic motion, particles |
| **PhysicsProps** | Physics for any property | Natural property animation |
| **CustomEase** | Define custom easing curves | Signature motion language |
| **CustomWiggle** | Oscillating/wiggle eases | Shake, vibrate effects |
| **CustomBounce** | Custom bounce eases | Realistic bounces |
| **EasePack** | Extra built-in eases | Extended ease library |
| **GSDevTools** | Visual timeline debugging UI | Dev workflow |

## Render Libraries

| Plugin | Description | Use Case |
|--------|-------------|----------|
| **PixiPlugin** | Animate Pixi.js objects | Canvas/WebGL rendering |
| **EaselPlugin** | Animate EaselJS objects | CreateJS canvas |

## React Integration

| Helper | Description | Use Case |
|--------|-------------|----------|
| **useGSAP()** | Official React hook | React/Next.js apps |

---

# 4) Core GSAP Mastery (Always-on Fundamentals)

## 4.1 Primitives

```js
gsap.to(target, { x: 100, duration: 1 });      // animate TO values
gsap.from(target, { opacity: 0 });              // animate FROM values
gsap.fromTo(target, { x: 0 }, { x: 100 });     // explicit from→to
gsap.set(target, { x: 0, opacity: 1 });        // instant set (no animation)
```

Prefer transform properties (`x`, `y`, `scale`, `rotation`) over layout props (`top`, `left`, `width`, `height`).

## 4.2 Timelines (default for anything non-trivial)

```js
const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.6 } });
tl.from(".hero-title", { y: 30, autoAlpha: 0 })
  .from(".hero-subtitle", { y: 20, autoAlpha: 0 }, "<0.1")
  .from(".hero-cta", { scale: 0.9, autoAlpha: 0 }, "<0.15");
```

**Rules:**
- One timeline per "interaction unit" (hero/section/component)
- Use labels + position parameters instead of brittle delays
- Use `defaults` for consistency, override intentionally

## 4.3 Position Parameters

```js
tl.to(a, {...})           // appends at end
tl.to(b, {...}, "<")      // starts same time as previous
tl.to(c, {...}, ">")      // starts after previous ends
tl.to(d, {...}, "+=0.3")  // wait 0.3s after last end
tl.to(e, {...}, "label")  // starts at label
```

## 4.4 Key Tools

- **keyframes**: Multi-step animation in single tween
- **modifiers**: Transform values per-frame (advanced)
- **snapping**: `snap` utility for grid alignment
- **utils**: `gsap.utils.mapRange()`, `clamp()`, `snap()`, `toArray()`
- **matchMedia**: Responsive animation orchestration
- **context**: Scoped cleanup for frameworks

---

# 5) Performance Toolkit (Non-negotiable)

## 5.1 Pointer/mouse interactions

```js
// ❌ BAD: Creates new tween every event
window.addEventListener("pointermove", (e) => {
  gsap.to(".cursor", { x: e.clientX, y: e.clientY });
});

// ✅ GOOD: Reuses quickTo instances
const xTo = gsap.quickTo(".cursor", "x", { duration: 0.2, ease: "power3" });
const yTo = gsap.quickTo(".cursor", "y", { duration: 0.2, ease: "power3" });
window.addEventListener("pointermove", (e) => { xTo(e.clientX); yTo(e.clientY); });

// ✅ GOOD: Ultra-fast direct updates (no tween)
const setX = gsap.quickSetter(".cursor", "x", "px");
const setY = gsap.quickSetter(".cursor", "y", "px");
window.addEventListener("pointermove", (e) => { setX(e.clientX); setY(e.clientY); });
```

## 5.2 Avoid layout thrash

```js
// ❌ BAD: Mixed reads and writes
elements.forEach(el => {
  const rect = el.getBoundingClientRect(); // read
  gsap.set(el, { x: rect.width });         // write
});

// ✅ GOOD: Batch reads, then writes
const rects = elements.map(el => el.getBoundingClientRect()); // all reads
elements.forEach((el, i) => gsap.set(el, { x: rects[i].width })); // all writes
```

## 5.3 ScrollTrigger scale rules

- Reduce trigger count; batch reveals where possible
- Use `invalidateOnRefresh` when layout-driven values are used
- Use `ScrollTrigger.batch()` for lists of similar elements

---

# 6) ScrollTrigger Mastery (Core Scroll Animations)

ScrollTrigger enables scroll-based triggering, scrubbing, pinning, snapping, etc.

## 6.1 Minimal patterns

```js
// Pattern A: Inline scrollTrigger
gsap.to(".box", {
  x: 500,
  scrollTrigger: {
    trigger: ".box",
    start: "top 80%",
    end: "top 30%",
    scrub: 1,
    markers: true // dev only
  }
});

// Pattern B: Timeline + ScrollTrigger.create
const tl = gsap.timeline();
tl.from(".item", { y: 50, autoAlpha: 0, stagger: 0.1 });

ScrollTrigger.create({
  animation: tl,
  trigger: ".section",
  start: "top 70%",
  toggleActions: "play none none reverse"
});
```

## 6.2 Pinned storytelling (timeline + scrub)

```js
const tl = gsap.timeline();
tl.from(".panel1", { autoAlpha: 0, y: 20 })
  .to(".panel1", { autoAlpha: 0 })
  .from(".panel2", { autoAlpha: 0, y: 20 }, "<");

ScrollTrigger.create({
  animation: tl,
  trigger: ".story",
  start: "top top",
  end: "+=2000",
  scrub: 1,
  pin: true,
  invalidateOnRefresh: true
});
```

## 6.3 Batching for lists

```js
ScrollTrigger.batch(".card", {
  onEnter: (elements) => gsap.from(elements, { y: 30, autoAlpha: 0, stagger: 0.1 }),
  start: "top 85%"
});
```

## 6.4 Horizontal scroll sections

```js
const sections = gsap.utils.toArray(".panel");
gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".horizontal-container",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".horizontal-container").offsetWidth
  }
});
```

## 6.5 Responsive + reduced motion (required)

```js
gsap.matchMedia().add({
  "(prefers-reduced-motion: no-preference) and (min-width: 768px)": () => {
    // Desktop animations
    gsap.from(".hero", {
      y: 50, autoAlpha: 0,
      scrollTrigger: { trigger: ".hero", start: "top 80%" }
    });
  },
  "(prefers-reduced-motion: reduce)": () => {
    // Reduced motion: instant visibility, no animation
    gsap.set(".hero", { autoAlpha: 1 });
  }
});
```

---

# 7) ScrollTo (Programmatic Scroll)

Use ScrollTo for smooth navigation to anchors/sections.

```js
gsap.registerPlugin(ScrollToPlugin);

// Scroll to element
gsap.to(window, { duration: 1, scrollTo: "#pricing", ease: "power2.out" });

// Scroll to position
gsap.to(window, { duration: 1, scrollTo: { y: 500, autoKill: true } });

// With offset
gsap.to(window, { scrollTo: { y: "#section", offsetY: 80 } });
```

---

# 8) ScrollSmoother (Smooth Scroll + Effects)

ScrollSmoother creates native-scroll-based smoothing and parallax effects.

```js
gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

// Required HTML structure:
// <div id="smooth-wrapper">
//   <div id="smooth-content">...content...</div>
// </div>

const smoother = ScrollSmoother.create({
  wrapper: "#smooth-wrapper",
  content: "#smooth-content",
  smooth: 1.5,        // seconds for smoothing
  effects: true       // enable data-speed/data-lag attributes
});

// HTML: <div data-speed="0.5">Slow parallax</div>
//       <div data-speed="2">Fast parallax</div>
//       <div data-lag="0.5">Trailing effect</div>
```

**Gotchas:**
- Must coordinate with ScrollTrigger and call `refresh()` after layout changes
- Always provide reduced-motion fallback
- Use `normalizeScroll: true` for mobile consistency

---

# 9) Observer (Gesture Normalization)

Use Observer to unify wheel/touch/pointer events into consistent "intent" signals.

```js
gsap.registerPlugin(Observer);

Observer.create({
  target: window,
  type: "wheel,touch,pointer",
  onUp: () => goToPrevSection(),
  onDown: () => goToNextSection(),
  tolerance: 50,
  preventDefault: true
});
```

**Use cases:**
- Scroll-jacking style step sections (careful with a11y)
- Trackpad gesture-triggered timelines
- Custom swipe navigation

---

# 10) Flip (Layout Transitions)

Use Flip when elements change layout (grid reorder, modal expansion, shared-element transitions).

```js
gsap.registerPlugin(Flip);

// 1. Capture state
const state = Flip.getState(".cards");

// 2. Change layout (DOM/CSS)
container.classList.toggle("grid");

// 3. Animate from old state
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut",
  stagger: 0.05,
  absolute: true,
  onEnter: elements => gsap.fromTo(elements, { autoAlpha: 0 }, { autoAlpha: 1 }),
  onLeave: elements => gsap.to(elements, { autoAlpha: 0 })
});
```

---

# 11) Draggable + InertiaPlugin (Momentum Dragging)

```js
gsap.registerPlugin(Draggable, InertiaPlugin);

Draggable.create(".slider", {
  type: "x",
  bounds: ".container",
  inertia: true,           // requires InertiaPlugin
  snap: value => Math.round(value / 200) * 200,  // snap to 200px intervals
  onDrag: function() { console.log(this.x); },
  onThrowComplete: () => console.log("Throw complete")
});
```

**DIY Momentum (if InertiaPlugin unavailable):**
```js
let velocity = 0;
let lastX = 0;

Draggable.create(".element", {
  type: "x",
  onDrag: function() {
    velocity = this.x - lastX;
    lastX = this.x;
  },
  onDragEnd: function() {
    // DIY momentum with exponential decay
    gsap.to(this.target, {
      x: `+=${velocity * 10}`,
      duration: Math.abs(velocity) * 0.1,
      ease: "power2.out"
    });
  }
});
```

---

# 12) Text: SplitText / ScrambleText / TextPlugin

## 12.1 SplitText

```js
gsap.registerPlugin(SplitText);

const split = new SplitText(".headline", { type: "chars,words,lines" });

gsap.from(split.chars, {
  y: 20,
  autoAlpha: 0,
  stagger: 0.02,
  duration: 0.4,
  ease: "power3.out"
});

// Cleanup (important for responsive)
// split.revert();
```

**DIY Alternative (if needed):**
```js
function splitIntoSpans(el) {
  const text = el.textContent;
  el.innerHTML = text.split('').map(char =>
    char === ' ' ? ' ' : `<span class="char">${char}</span>`
  ).join('');
  return el.querySelectorAll('.char');
}
```

## 12.2 ScrambleText

```js
gsap.registerPlugin(ScrambleTextPlugin);

gsap.to(".title", {
  duration: 1.5,
  scrambleText: {
    text: "DECODED MESSAGE",
    chars: "XO",
    revealDelay: 0.5
  }
});
```

## 12.3 TextPlugin

```js
gsap.registerPlugin(TextPlugin);

gsap.to(".counter", {
  duration: 2,
  text: { value: "100%", delimiter: "" },
  ease: "none"
});
```

---

# 13) SVG: DrawSVG / MorphSVG / MotionPath

## 13.1 DrawSVG

```js
gsap.registerPlugin(DrawSVGPlugin);

gsap.from(".line-path", {
  drawSVG: 0,          // or "0%" / "50% 50%"
  duration: 2,
  ease: "power2.inOut"
});
```

## 13.2 MorphSVG

```js
gsap.registerPlugin(MorphSVGPlugin);

gsap.to("#shape1", {
  morphSVG: "#shape2",
  duration: 1,
  ease: "power2.inOut"
});
```

## 13.3 MotionPath

```js
gsap.registerPlugin(MotionPathPlugin);

gsap.to(".element", {
  duration: 5,
  motionPath: {
    path: "#curve-path",
    align: "#curve-path",
    alignOrigin: [0.5, 0.5],
    autoRotate: true
  },
  ease: "none"
});
```

---

# 14) Physics2D / PhysicsProps

```js
gsap.registerPlugin(Physics2DPlugin, PhysicsPropsPlugin);

// 2D physics (velocity, angle, acceleration, gravity)
gsap.to(".ball", {
  duration: 3,
  physics2D: {
    velocity: 500,
    angle: -60,
    gravity: 500
  }
});

// Physics for any property
gsap.to(".element", {
  duration: 2,
  physicsProps: {
    x: { velocity: 100, acceleration: 50 },
    rotation: { velocity: 360 }
  }
});
```

---

# 15) Eases: CustomEase / CustomWiggle / CustomBounce

```js
gsap.registerPlugin(CustomEase, CustomWiggle, CustomBounce);

// Custom SVG path ease
CustomEase.create("myEase", "M0,0 C0.25,0.1 0.25,1 1,1");
gsap.to(".el", { x: 100, ease: "myEase" });

// Wiggle ease
CustomWiggle.create("myWiggle", { wiggles: 6, type: "easeOut" });
gsap.to(".el", { rotation: 20, ease: "myWiggle" });

// Custom bounce
CustomBounce.create("myBounce", { strength: 0.7, squash: 2 });
gsap.to(".el", { y: 300, ease: "myBounce" });
```

---

# 16) GSDevTools (Debug UI)

```js
gsap.registerPlugin(GSDevTools);

// Attach to a specific timeline
const tl = gsap.timeline();
tl.to(".box", { x: 500 })
  .to(".box", { rotation: 360 });

GSDevTools.create({ animation: tl });

// Or attach to global timeline
GSDevTools.create();
```

---

# 17) Next.js / React (Production Patterns)

## 17.1 Golden rule: cleanup on unmount

Use `gsap.context()` to scope selectors and revert everything.

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function SectionAnim() {
  const root = useRef(null);

  useLayoutEffect(() => {
    if (!root.current) return;

    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.8 } });
      tl.from(".title", { y: 18, autoAlpha: 0 })
        .from(".item", { y: 14, autoAlpha: 0, stagger: 0.06 }, "<0.1");

      gsap.from(".reveal", {
        y: 24, autoAlpha: 0,
        scrollTrigger: { trigger: ".reveal", start: "top 85%" }
      });
    }, root);

    return () => ctx.revert();
  }, []);

  return (
    <section ref={root}>
      <h2 className="title">Title</h2>
      <div className="item">A</div>
      <div className="item">B</div>
      <div className="reveal">Reveal</div>
    </section>
  );
}
```

## 17.2 Official useGSAP hook

```jsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function AnimatedSection() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".box", {
      y: 50,
      autoAlpha: 0,
      scrollTrigger: { trigger: ".box", start: "top 80%" }
    });
  }, { scope: container });

  return (
    <div ref={container}>
      <div className="box">Content</div>
    </div>
  );
}
```

## 17.3 SSR safety

- Put animation components in client-only files
- Don't touch `window`/`document` outside effects
- Use `typeof window !== 'undefined'` guards when needed

## 17.4 Responsive orchestration

```jsx
useLayoutEffect(() => {
  const mm = gsap.matchMedia();

  mm.add("(min-width: 768px)", () => {
    // Desktop animations
    gsap.from(".hero", { x: -100 });
    return () => { /* cleanup */ };
  });

  mm.add("(max-width: 767px)", () => {
    // Mobile animations
    gsap.from(".hero", { y: 50 });
    return () => { /* cleanup */ };
  });

  return () => mm.revert();
}, []);
```

---

# 18) Debug Checklist (Use verbatim)

## Core issues

- [ ] **Is the target real?** Double-check selector/ref (typos, scope, SSR). Confirm element exists when animation runs.
- [ ] **DOM timing**: In React/Next.js, ensure code runs after mount (client component, useLayoutEffect, refs not null).
- [ ] **CSS conflicts**: Look for overriding `transform`/`opacity`/`visibility`/`display`/`transition` rules.
- [ ] **Duplicate runs**: Use `gsap.context()` and `ctx.revert()` to avoid stacking tweens/ScrollTriggers.

## Timeline issues

- [ ] **Sequence looks wrong?** Add labels + position parameters (`<`, `>`, `+=0.2`) instead of manual delays.
- [ ] **Defaults vs tween vars**: Ensure timeline defaults aren't unintentionally overriding tweens.
- [ ] **Slow down to inspect**: `gsap.globalTimeline.timeScale(0.5)`.

## ScrollTrigger issues

- [ ] **Turn on debugging**: `markers: true` (dev only).
- [ ] **Validate start/end**: Ensure start/end match layout and element heights.
- [ ] **Refresh after layout changes**: Call `ScrollTrigger.refresh()` after images/fonts/dynamic content settle.
- [ ] **Custom scroller**: Set `scroller` consistently when not using window.
- [ ] **Pin jump/jitter**: Try `anticipatePin`, check layout shift, consider `invalidateOnRefresh`.

## Performance issues

- [ ] **Pointer/mouse jank**: Don't create a tween per event. Use `quickTo`/`quickSetter`.
- [ ] **Too many triggers**: Reduce count, use batching, consolidate timelines.
- [ ] **Avoid layout thrash**: Batch reads then writes; prefer transforms.
- [ ] **Heavy properties**: Avoid `top`/`left`/`width`/`height` where possible.

---

# 19) "If Plugin Unavailable" Policy

If user cannot use a plugin (policy/offline constraints):

1. **Offer the official plugin path first**
2. **Provide a DIY workaround** using GSAP core + CSS/JS
3. **Explicitly state limitations**: edge cases, maintainability, perf, cross-browser parity

Never suggest cracked/pirated plugins.

---

# 20) Ready-to-use Interaction Recipes

## Hover micro-interaction

```js
const el = document.querySelector(".btn");
el.addEventListener("mouseenter", () =>
  gsap.to(el, { scale: 1.03, duration: 0.2, overwrite: "auto" })
);
el.addEventListener("mouseleave", () =>
  gsap.to(el, { scale: 1.00, duration: 0.25, overwrite: "auto" })
);
```

## Cursor follower (high-perf)

```js
const xTo = gsap.quickTo(".cursor", "x", { duration: 0.2, ease: "power3" });
const yTo = gsap.quickTo(".cursor", "y", { duration: 0.2, ease: "power3" });
window.addEventListener("pointermove", (e) => { xTo(e.clientX); yTo(e.clientY); });
```

## Magnetic button

```js
const btn = document.querySelector(".magnetic");
const strength = 0.3;

btn.addEventListener("mousemove", (e) => {
  const rect = btn.getBoundingClientRect();
  const x = e.clientX - rect.left - rect.width / 2;
  const y = e.clientY - rect.top - rect.height / 2;
  gsap.to(btn, { x: x * strength, y: y * strength, duration: 0.3 });
});

btn.addEventListener("mouseleave", () => {
  gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: "elastic.out(1, 0.3)" });
});
```

## Reveal on scroll

```js
gsap.from(".reveal", {
  y: 24, autoAlpha: 0, duration: 0.8, ease: "power3.out",
  scrollTrigger: {
    trigger: ".reveal",
    start: "top 85%",
    toggleActions: "play none none reverse"
  }
});
```

## Staggered list reveal

```js
gsap.from(".list-item", {
  y: 30,
  autoAlpha: 0,
  duration: 0.6,
  stagger: 0.1,
  ease: "power3.out",
  scrollTrigger: { trigger: ".list", start: "top 80%" }
});
```

## Parallax hero

```js
gsap.to(".hero-bg", {
  yPercent: 30,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "bottom top",
    scrub: true
  }
});
```

---

# References packaged with this skill

See:

- references/GSAP_CORE.md
- references/GSAP_RECIPES.md
- references/UI_INTERACTIONS.md
- references/TEXT_ANIMATIONS.md
- references/PHYSICS_PLUGINS.md
- references/NEXTJS_REACT_PATTERNS.md
- references/GSDEVTOOLS.md
- references/DEBUG_CHECKLIST.md
