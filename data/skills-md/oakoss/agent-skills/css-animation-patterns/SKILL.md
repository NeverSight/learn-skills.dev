---
name: css-animation-patterns
description: >
  CSS animations, transitions, keyframes, and modern motion APIs. Use when adding animations, transitions,
  scroll-driven effects, or view transitions. Use for css-animation, transition, keyframes, view-transitions,
  scroll-animation, transform, motion-preference, animation-timeline.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations'
user-invocable: false
---

# CSS Animation Patterns

## Overview

CSS animations and transitions provide hardware-accelerated motion for web interfaces using keyframes, transitions, transforms, and modern scroll-driven and view transition APIs. Animate only composite properties (`transform`, `opacity`, `filter`) for smooth 60fps performance, and always respect `prefers-reduced-motion`.

The browser rendering pipeline has four stages: Style, Layout, Paint, and Composite. Animating composite-only properties skips Layout and Paint entirely, running on the GPU compositor thread. This is the single most important performance principle for CSS animation.

Modern CSS adds two powerful APIs: **scroll-driven animations** link keyframe progress to scroll position or element visibility instead of time, and the **View Transitions API** creates snapshot-based animated transitions between DOM states for both SPAs and MPAs.

**When to use:** Element state changes, page transitions, scroll-linked effects, loading indicators, micro-interactions, route change animations, reveal-on-scroll patterns, parallax effects, progress indicators tied to scroll.

**When NOT to use:** Complex physics simulations (use a JS animation library), canvas/WebGL rendering, animations requiring frame-by-frame scripted control (use Web Animations API directly), highly interactive drag-and-drop (use pointer events with JS).

## Browser Support Summary

| Feature                               | Chrome | Firefox | Safari |
| ------------------------------------- | ------ | ------- | ------ |
| Transitions, keyframes, transforms    | Full   | Full    | Full   |
| Individual transform properties       | 104+   | 72+     | 14.1+  |
| `@starting-style`                     | 117+   | 129+    | 17.5+  |
| `transition-behavior: allow-discrete` | 117+   | 129+    | 17.4+  |
| Scroll-driven animations              | 115+   | Not yet | 26+    |
| Same-document view transitions        | 111+   | 144+    | 18+    |
| Cross-document view transitions       | 126+   | Not yet | 18+    |
| `view-transition-class`               | 125+   | 144+    | 18+    |

Use `@supports` for progressive enhancement with newer features. Always provide a functional non-animated fallback.

## Quick Reference

| Pattern               | API                                             | Key Points                                                  |
| --------------------- | ----------------------------------------------- | ----------------------------------------------------------- |
| State transition      | `transition: property duration easing`          | Triggers on property change, composite-only for performance |
| Discrete transition   | `transition-behavior: allow-discrete`           | Enables transitions on `display`, `visibility`              |
| Entry animation       | `@starting-style { ... }`                       | Initial state for elements appearing in DOM                 |
| Keyframe animation    | `@keyframes name` + `animation` shorthand       | Multi-step sequences, supports `forwards` fill mode         |
| Transform             | `transform: translate() scale() rotate()`       | GPU-composited, no layout recalculation                     |
| Individual transforms | `translate`, `rotate`, `scale`                  | Independently animatable with different timings             |
| Scroll progress       | `animation-timeline: scroll()`                  | Links animation to scroll position of a container           |
| View progress         | `animation-timeline: view()`                    | Links animation to element visibility in scrollport         |
| Animation range       | `animation-range: entry 0% entry 100%`          | Controls which timeline segment drives animation            |
| Named scroll timeline | `scroll-timeline-name` + `scroll-timeline-axis` | Reusable scroll timeline across elements                    |
| Named view timeline   | `view-timeline-name` + `view-timeline-axis`     | Reusable view timeline for visibility tracking              |
| View transition (SPA) | `document.startViewTransition(callback)`        | Snapshot-based animated DOM updates                         |
| View transition (MPA) | `@view-transition { navigation: auto }`         | Cross-document transitions, same-origin only                |
| Transition naming     | `view-transition-name: hero`                    | Identifies elements for independent transition groups       |
| Transition classes    | `view-transition-class: card`                   | Groups named elements for shared transition styles          |
| Transition types      | `startViewTransition({ types: [...] })`         | Conditional styling based on navigation direction           |
| GPU hint              | `will-change: transform`                        | Promotes element to compositor layer, use sparingly         |
| Motion preference     | `@media (prefers-reduced-motion: reduce)`       | Disable or simplify animations for accessibility            |
| Custom easing         | `cubic-bezier()` or `linear()`                  | Fine-tuned timing curves, `linear()` for multi-point easing |
| Step easing           | `steps(n, jump-term)`                           | Frame-by-frame discrete animation                           |
| Animation composition | `animation-composition: accumulate`             | Controls how multiple animations combine on same property   |
| Staggered delay       | `animation-delay: calc(var(--i) * 60ms)`        | Per-element delay using CSS custom properties               |
| Render containment    | `contain: layout style`                         | Isolates rendering scope for better animation perf          |
| Content visibility    | `content-visibility: auto`                      | Skips rendering of off-screen content                       |

## Common Mistakes

| Mistake                                                     | Correct Pattern                                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Animating `width`, `height`, `top`, `left`                  | Use `transform: translate()` and `scale()` for layout-free animation            |
| Adding `will-change` to every element                       | Apply only to elements that animate frequently, remove after animation          |
| Missing `prefers-reduced-motion` handling                   | Wrap motion in `@media (prefers-reduced-motion: no-preference)`                 |
| Using `translateZ(0)` hack everywhere                       | Use `will-change` instead, and only when needed                                 |
| Declaring `animation-timeline` before `animation` shorthand | Declare `animation-timeline` after `animation` (shorthand resets it to `auto`)  |
| Setting `animation-duration` for scroll-driven animations   | Duration is scroll-controlled; use `auto` or omit, set `1ms` for Firefox compat |
| Forgetting `view-transition-name` must be unique            | Each participating element needs a distinct name per page snapshot              |
| Not providing fallbacks for scroll-driven animations        | Use `@supports (animation-timeline: scroll())` for progressive enhancement      |
| Animating `background-color` expecting GPU compositing      | Only `transform`, `opacity`, and `filter` are reliably GPU-composited           |
| Using `transition: all`                                     | Specify exact properties to avoid unexpected transitions and performance hits   |
| Interleaving DOM reads and writes in JS animations          | Batch reads first, then writes, or use `requestAnimationFrame`                  |
| Not using `flushSync` with React view transitions           | React batches updates; wrap `navigate()` in `flushSync` inside the callback     |
| Calling `startViewTransition` without feature check         | Always guard with `if (!document.startViewTransition)` fallback                 |

## Delegation

- **Animation implementation**: Use `Explore` agent to discover patterns in reference files
- **Performance audit**: Use `Task` agent to review animation performance across components
- **Accessibility review**: Use `Task` agent to verify `prefers-reduced-motion` coverage
- **Code review**: Delegate to `code-reviewer` agent for animation-related PR reviews

> If the `ux-designer` skill is available, delegate visual motion design decisions to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill ux-designer`

## References

- [Transitions, keyframes, and animation properties](references/transitions-and-keyframes.md)
- [Transforms and performance optimization](references/transforms-and-performance.md)
- [Scroll-driven animations](references/scroll-driven.md)
- [View Transitions API](references/view-transitions.md)
