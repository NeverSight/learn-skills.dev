---
name: animation-recipe-library
description: "200+ copy-paste animation recipes in CSS, Framer Motion, and GSAP: entrances, micro-interactions, page transitions, scroll-driven effects, spring physics, and cursor and text effects, each with timing, easing, and a reduced-motion fallback. Use when you need working motion code rather than motion principles."
---

# Animation Recipe Library

## Mental model

Motion is a sentence about causality: this happened *because* that happened.
Animation that does not explain a relationship is decoration, and decoration is
the first thing that reads as amateur.

- **Duration follows distance and size.** A 200px slide is not a 20px nudge.
  150-200ms for small state changes, 250-350ms for entrances, 400-500ms for
  anything crossing the viewport. Over 500ms and the interface feels slow no
  matter how pretty the curve.
- **Ease out for entrances, ease in for exits.** Things arriving decelerate;
  things leaving accelerate away. Linear is for progress bars and nothing else.
- **Animate transform and opacity.** They are composited. Width, height, top,
  left and box-shadow are painted, and animating them drops frames on the
  devices least able to afford it.
- **Reduced motion is not optional.** WCAG 2.1 SC 2.3.3, and a vestibular
  trigger for real people. Every recipe here ships a fallback.

Spring physics beats a bezier when the motion should feel physical -- drags,
sheets, anything the user is directly manipulating. Bezier beats spring when
timing must be predictable.

## Constants

Every recipe in every reference file writes against these. Without them in
context the references are unusable.

```css
:root {
  /* === Core Easings === */
  --ease-out:          cubic-bezier(0.16, 1, 0.3, 1);         /* Decelerate — entrances */
  --ease-out-soft:     cubic-bezier(0.33, 1, 0.68, 1);        /* Gentle decelerate */
  --ease-out-quad:     cubic-bezier(0.25, 0.46, 0.45, 0.94);  /* Quadratic decelerate */
  --ease-out-cubic:    cubic-bezier(0.22, 0.61, 0.36, 1);     /* Cubic decelerate */
  --ease-out-quart:    cubic-bezier(0.17, 0.84, 0.44, 1);     /* Quartic decelerate */
  --ease-out-quint:    cubic-bezier(0.23, 1, 0.32, 1);        /* Quintic decelerate */
  --ease-out-expo:     cubic-bezier(0.16, 1, 0.3, 1);         /* Exponential decelerate */
  --ease-out-circ:     cubic-bezier(0.08, 0.82, 0.17, 1);     /* Circular decelerate */
  --ease-out-back:     cubic-bezier(0.34, 1.56, 0.64, 1);     /* Overshoot decelerate */

  --ease-in:           cubic-bezier(0.55, 0.055, 0.675, 0.19);/* Accelerate — exits */
  --ease-in-soft:      cubic-bezier(0.32, 0, 0.67, 0);        /* Gentle accelerate */
  --ease-in-quad:      cubic-bezier(0.55, 0.085, 0.68, 0.53); /* Quadratic accelerate */
  --ease-in-cubic:     cubic-bezier(0.55, 0.055, 0.675, 0.19);/* Cubic accelerate */
  --ease-in-quart:     cubic-bezier(0.9, 0.03, 0.69, 0.22);   /* Quartic accelerate */
  --ease-in-expo:      cubic-bezier(0.7, 0, 0.84, 0);         /* Exponential accelerate */
  --ease-in-back:      cubic-bezier(0.36, 0, 0.66, -0.56);    /* Pull-back accelerate */

  --ease-in-out:       cubic-bezier(0.87, 0, 0.13, 1);        /* Symmetric — movement */
  --ease-in-out-soft:  cubic-bezier(0.45, 0, 0.55, 1);        /* Gentle symmetric */
  --ease-in-out-quad:  cubic-bezier(0.46, 0.03, 0.52, 0.96);  /* Quadratic symmetric */
  --ease-in-out-cubic: cubic-bezier(0.65, 0, 0.35, 1);        /* Cubic symmetric */
  --ease-in-out-back:  cubic-bezier(0.68, -0.6, 0.32, 1.6);   /* Overshoot symmetric */

  /* === Spring Physics (CSS approximations) === */
  --spring-gentle:     cubic-bezier(0.34, 1.56, 0.64, 1);     /* stiffness:120 damping:14 */
  --spring-bouncy:     cubic-bezier(0.68, -0.55, 0.27, 1.55); /* stiffness:180 damping:12 */
  --spring-snappy:     cubic-bezier(0.25, 1.5, 0.5, 1);       /* stiffness:300 damping:20 */
  --spring-wobbly:     cubic-bezier(0.36, 1.7, 0.5, 0.9);     /* stiffness:150 damping:8 */
  --spring-stiff:      cubic-bezier(0.12, 1.2, 0.4, 1);       /* stiffness:400 damping:30 */
  --spring-slow:       cubic-bezier(0.34, 1.3, 0.64, 1);      /* stiffness:80 damping:20 */

  /* === Bounce === */
  --bounce:            cubic-bezier(0.34, 1.56, 0.64, 1);     /* Single overshoot bounce */
  --bounce-heavy:      cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Double overshoot */

  /* === Elastic (requires @keyframes for true elastic) === */
  --elastic-out:       cubic-bezier(0.36, 1.7, 0.5, 0.85);    /* Approximation of elastic */

  /* === Emphasis === */
  --emphasis-dramatic:  cubic-bezier(0.04, 0.62, 0.23, 0.98);
  --emphasis-energetic: cubic-bezier(0.22, 0.68, 0, 1.71);

  /* === Platform-Specific === */
  --ios-spring:        cubic-bezier(0.25, 0.8, 0.25, 1);      /* iOS default animation */
  --material-standard: cubic-bezier(0.2, 0, 0, 1);            /* M3 standard easing */
  --material-decel:    cubic-bezier(0, 0, 0, 1);              /* M3 decelerate */
  --material-accel:    cubic-bezier(0.3, 0, 1, 1);            /* M3 accelerate */
  --material-emphasized: cubic-bezier(0.2, 0, 0, 1);          /* M3 emphasized */
}
```

### Framer Motion Spring Presets

```tsx
// Gentle — modals, overlays, panels
const springGentle = { type: "spring", stiffness: 120, damping: 14, mass: 1 };

// Bouncy — playful UI, notifications, FABs
const springBouncy = { type: "spring", stiffness: 180, damping: 12, mass: 1 };

// Snappy — toggles, switches, small elements
const springSnappy = { type: "spring", stiffness: 300, damping: 20, mass: 0.8 };

// Wobbly — emphasis, celebrations, attention-grab
const springWobbly = { type: "spring", stiffness: 150, damping: 8, mass: 1 };

// Stiff — precise, utility, no-nonsense
const springStiff = { type: "spring", stiffness: 400, damping: 30, mass: 1 };

// Slow — large-area reveals, page transitions
const springSlow = { type: "spring", stiffness: 80, damping: 20, mass: 1.2 };

// iOS-like — platform-matching for hybrid apps
const springIOS = { type: "spring", stiffness: 200, damping: 22, mass: 1 };

// Material-like — for M3 matching
const springMaterial = { type: "spring", stiffness: 250, damping: 25, mass: 1 };
```

### When to Use Each Easing

| Easing | Use For | Avoid For |
|--------|---------|-----------|
| ease-out | Entrances, appearing elements | Exits, disappearing elements |
| ease-in | Exits, disappearing elements | Entrances (feels sluggish) |
| ease-in-out | Position changes, slides between states | Quick micro-interactions |
| ease-out-back | Playful entrances, bouncing buttons | Serious/enterprise UI |
| spring (gentle) | Modals, sheets, overlays | Rapid repeated actions |
| spring (snappy) | Toggles, switches, small controls | Large page transitions |
| spring (bouncy) | Notifications, celebrations | Data-heavy interfaces |
| linear | Progress bars, continuous rotation only | Everything else |

---

The reduced-motion floor, which every recipe assumes is already in the sheet:

```css
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
```

## Index

| Want | Category | Reference |
|---|---|---|
| Fade, scale, slide, blur, drop in | Entrance (25) | `css-animation-recipes.md` |
| Fade, scale, slide, collapse out | Exit (18) | `css-animation-recipes.md` |
| Spinner, skeleton shimmer, progress, dots | Loading (16) | `css-animation-recipes.md` |
| Button press, toggle, hover lift, focus ring | Micro-interaction (35) | `micro-interaction-recipes.md` |
| Route change, shared element, container morph | Page transition (18) | `page-transition-recipes.md` |
| List reorder, grid reflow, accordion | Layout (12) | `page-transition-recipes.md` |
| Reveal on scroll, parallax, sticky progress | Scroll-driven (16) | `scroll-gesture-recipes.md` |
| Swipe, drag, pull-to-refresh, long press | Gesture (12) | `scroll-gesture-recipes.md` |
| Stagger, sequence, orchestrated groups | Orchestration | `framer-motion-recipes.md` |
| Framer Motion variants and layout prop | — | `framer-motion-recipes.md` |
| Pin, scrub, horizontal scroll, SplitText | GSAP / ScrollTrigger | `gsap-scrolltrigger-recipes.md` |
| Custom cursor, magnetic button, text effects, 3D | — | `cursor-text-3d-effects.md` |
| More than two visual states | State machines | `animation-state-machines.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `references/gsap-scrolltrigger-recipes.md` | GSAP, ScrollTrigger, Lenis | 1897 |
| `references/cursor-text-3d-effects.md` | cursor, text, R3F, particles | 1394 |
| `references/css-animation-recipes.md` | entrance, exit, loading in CSS | 1325 |
| `references/scroll-gesture-recipes.md` | scroll-driven and gesture | 1292 |
| `references/framer-motion-recipes.md` | Framer Motion + orchestration | 965 |
| `references/micro-interaction-recipes.md` | 35 micro-interactions | 400 |
| `references/page-transition-recipes.md` | page and layout transitions | 323 |
| `references/animation-state-machines.md` | multi-state animation | 73 |

## What every reference file contains

1. The recipe name and what it is for in one line
2. Complete, runnable CSS or JSX -- no placeholders
3. Exact duration and easing, using the tokens above
4. The reduced-motion fallback for that specific recipe
5. What it costs: composited, painted, or layout-triggering
6. When to reach for a different recipe instead

## Performance

Composited properties are `transform`, `opacity`, and `filter`. Everything else
repaints. `will-change` is a promise you pay for whether or not you keep it --
set it immediately before the animation and remove it after, never in a
stylesheet at rest. Sixty frames per second is 16.7ms per frame including
everything else on the page.

## Routing

For **CSS entrances, exits and loading states**: read
`references/css-animation-recipes.md`.

For **the small responses that make an interface feel alive** -- presses,
toggles, hovers, focus, drag affordances: read
`references/micro-interaction-recipes.md`.

For **moving between screens** -- route changes, shared-element morphs, list
reordering: read `references/page-transition-recipes.md`.

For **scroll and touch** -- reveal, parallax, sticky progress, swipe, drag,
pull-to-refresh: read `references/scroll-gesture-recipes.md`.

For **Framer Motion** -- variants, the layout prop, stagger and orchestration:
read `references/framer-motion-recipes.md`.

For **GSAP** -- pin and scrub, horizontal scroll, SplitText, Lenis smooth
scroll: read `references/gsap-scrolltrigger-recipes.md`.

For **the showy stuff** -- custom cursors, magnetic buttons, text effects,
React Three Fiber, particles: read `references/cursor-text-3d-effects.md`.

For **anything with more than two visual states**: read
`references/animation-state-machines.md`.

For **why a motion should exist at all** -- Disney's twelve principles
translated into interface terms: read `references/motion-principles.md`.

## Cross-References

- `interaction-motion-design` -- the principles behind these recipes; read that
  when deciding *whether* to animate, this when deciding *how*
- `performance-states-patterns` -- loading and skeleton states as UX, not motion
- `accessibility-inclusive-design` -- the full reduced-motion and vestibular story
- `shadow-elevation-density` -- animating elevation specifically
