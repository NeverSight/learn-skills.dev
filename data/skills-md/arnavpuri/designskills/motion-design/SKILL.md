---
name: motion-design
description: >
  UI animation and micro-interactions in CSS/JS: duration and easing tokens,
  hover/press feedback, page and view transitions, scroll-driven reveals, loaders,
  staggering, reduced-motion handling, and performance. Use for motion in web/app
  interfaces (not video or animated image generation). Trigger phrases: "animation", "micro-interaction",
  "motion design", "page transition", "scroll animation", "loading animation",
  "css animation", "hover effect", "skeleton loader", "stagger animation"
license: MIT
---

# Motion Design

Add purposeful animation and micro-interactions that enhance UX without compromising performance.

## Prerequisites

- Read `.agents/design-context.md` (see `design-context`): the style archetype sets motion character (Minimal/Corporate = short, no overshoot; Playful = springs allowed; Luxurious = slower, smooth ease-out).
- If a design system exists, use its transition tokens. The token names below (`--duration-*`, `--ease-*`) are the same ones the design-system skill defines.
- Always respect `prefers-reduced-motion`.

---

## Step 1: Animation Principles for UI

### The Three Rules
1. **Every animation must have a purpose**: Guide attention, provide feedback, show relationships, or convey state change.
2. **Faster is almost always better**: UI animations should be 100-500ms.
3. **Animate what changes**: Only animate properties that are actually changing.

### Duration Guidelines

| Action                    | Duration    |
|---------------------------|-------------|
| Button hover/press        | 100-150ms   |
| Toggle/switch             | 200ms       |
| Dropdown/menu open        | 200-250ms   |
| Modal/dialog appear       | 250-300ms   |
| Page transition           | 300-400ms   |
| Expand/collapse           | 250-350ms   |
| Loading spinner cycle     | 700-1200ms  |

Exits should be ~20-30% shorter than the matching entrance (e.g. modal in 250ms, out 200ms). Large or long-distance movement takes longer than small; mobile durations are typically shorter than desktop/tablet.

### Easing Functions

```css
:root {
  --duration-fast: 100ms; --duration-normal: 200ms; --duration-slow: 300ms; --duration-slower: 500ms;

  --ease-out: cubic-bezier(0, 0, 0.2, 1);        /* Decelerate: ENTER */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);          /* Accelerate: EXIT */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);    /* Standard: MOVE */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);    /* Bouncy overshoot */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Strong bounce */
}
```

Use ease-out for entrances, ease-in for exits, ease-in-out for moves, spring for playful feedback.

---

## Step 2: Micro-Interaction Patterns

### Button Press

```css
.btn {
  transition: transform 0.1s var(--ease-out), background-color 0.15s var(--ease-out), box-shadow 0.15s var(--ease-out);
}
.btn:hover { box-shadow: 0 4px 12px oklch(from var(--interactive-primary) l c h / 0.3); }
.btn:active { transform: scale(0.97); }
```

### Toggle Switch

```css
.toggle-track { width: 44px; height: 24px; background: var(--gray-300); border-radius: 12px; padding: 2px; cursor: pointer; transition: background-color 0.2s var(--ease-out); }
.toggle-thumb { width: 20px; height: 20px; background: white; border-radius: 50%; transition: transform 0.2s var(--ease-spring); }
.toggle-input:checked + .toggle-track { background: var(--brand-500); }
.toggle-input:checked + .toggle-track .toggle-thumb { transform: translateX(20px); }
.toggle-input:focus-visible + .toggle-track { outline: 2px solid var(--interactive-primary); outline-offset: 2px; }
```

`.toggle-input` must be a real `<input type="checkbox" role="switch">` inside a `<label>`, visually hidden (not `display: none`) so it stays keyboard- and screen-reader-operable.

### Like/Heart Animation

```css
.like-btn.is-liked .heart-icon { animation: like-pop 0.4s var(--ease-spring); color: #ef4444; fill: currentColor; }
@keyframes like-pop { 0% { transform: scale(1); } 30% { transform: scale(1.3); } 60% { transform: scale(0.9); } 100% { transform: scale(1); } }
```

---

## Step 3: Page Transition Animations

### Slide Up and Fade

```css
.page-enter { animation: slideUpFade 0.4s var(--ease-out) both; }
@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### View Transitions API (Modern)

```css
/* Cross-document (MPA, same origin): opt in on BOTH pages */
@view-transition { navigation: auto; }
::view-transition-old(root) { animation: vt-fade-out 0.2s var(--ease-in) both; }
::view-transition-new(root) { animation: vt-fade-in 0.3s var(--ease-out) both; }
@keyframes vt-fade-out { to { opacity: 0; } }
@keyframes vt-fade-in { from { opacity: 0; } }
.hero-image { view-transition-name: hero; } /* must be unique on the page */
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*), ::view-transition-old(*), ::view-transition-new(*) { animation: none !important; } }
```

For SPAs, wrap the DOM update: `document.startViewTransition ? document.startViewTransition(update) : update();`. Browsers without support simply skip the animation.

---

## Step 4: Scroll-Triggered Animations

### CSS-Only with `animation-timeline`

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .scroll-reveal { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% entry 100%; }
  }
}
@keyframes reveal { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
```

`animation-timeline` must come after the `animation` shorthand (the shorthand resets it). Content stays fully visible where scroll-driven animations are unsupported.

### Intersection Observer Approach

```css
/* Hide only when JS is running, so content is never lost without JS */
.js .reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out); }
.js .reveal.is-visible { opacity: 1; transform: translateY(0); }
```

```js
document.documentElement.classList.add('js');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

---

## Step 5: Loading Animations

### Skeleton Loader

```css
.skeleton { background: var(--gray-200); border-radius: var(--radius-md); position: relative; overflow: hidden; }
.skeleton::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent, oklch(1 0 0 / 0.4), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
.skeleton-text { height: 1em; margin-bottom: 0.75em; }
.skeleton-text:last-child { width: 60%; }
.skeleton-avatar { width: 48px; height: 48px; border-radius: 50%; }
```

### Spinner

```css
.spinner { width: 24px; height: 24px; border: 3px solid var(--gray-200); border-top-color: var(--brand-500); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
```

### Three-Dot Bounce

```css
.dots-loader { display: flex; gap: 4px; }
.dots-loader span { width: 8px; height: 8px; background: var(--brand-500); border-radius: 50%; animation: dot-bounce 1.2s ease-in-out infinite; }
.dots-loader span:nth-child(2) { animation-delay: 0.15s; }
.dots-loader span:nth-child(3) { animation-delay: 0.3s; }
@keyframes dot-bounce { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; } 40% { transform: scale(1); opacity: 1; } }
```

---

## Step 6: CSS Animation Techniques

### Transition vs Animation
- **`transition`**: For state changes (hover, focus, class toggle). A-to-B.
- **`animation`**: For multi-step sequences, continuous effects, or entrance animations.

### Animation Fill Modes

| Value     | Behavior                                              |
|-----------|-------------------------------------------------------|
| none      | Reverts to original state after animation             |
| forwards  | Stays at the last keyframe                            |
| backwards | Applies first keyframe during delay period            |
| both      | Combines forwards + backwards. Usually what you want  |

---

## Step 7: Spring Physics with CSS

```css
:root {
  --spring-gentle: cubic-bezier(0.34, 1.2, 0.64, 1);   /* Slight overshoot */
  --spring-medium: cubic-bezier(0.34, 1.56, 0.64, 1);   /* Noticeable bounce */
  --spring-strong: cubic-bezier(0.22, 1.8, 0.36, 1);    /* Dramatic bounce */
  --spring-snappy: cubic-bezier(0.075, 0.82, 0.165, 1); /* Not a spring: fast ease-out (easeOutCirc), no overshoot */
}
```

For multi-bounce, use keyframes:

```css
@keyframes spring-bounce {
  0% { transform: scale(0.8); } 40% { transform: scale(1.08); }
  60% { transform: scale(0.97); } 80% { transform: scale(1.02); } 100% { transform: scale(1); }
}
```

---

## Step 8: Reduced Motion

### Global Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```

Preferred approach: replace motion with non-motion transitions (e.g., opacity changes instead of transforms). The global rule above is a safety net: it also stops spinners after one turn, so give loaders a non-rotating fallback (pulsing opacity or "Loading…" text).

For JS-driven animation (Web Animations API, GSAP, Framer Motion), check the preference and listen for changes:

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const duration = () => (reduce.matches ? 0 : 300);
reduce.addEventListener('change', () => { /* re-read duration(), stop autoplaying loops */ });
```

Also: no flashing more than 3 times per second (WCAG 2.3.1), and any auto-playing motion lasting over 5 seconds needs a pause control (WCAG 2.2.2).

---

## Step 9: Performance Optimization

### The Golden Rule
Only animate `transform` and `opacity`. These are GPU-composited and do not trigger layout or paint.

### Property Cost

| Property        | Layout | Paint | Composite | Performance |
|-----------------|--------|-------|-----------|-------------|
| transform       | No     | No    | Yes       | Excellent   |
| opacity         | No     | No    | Yes       | Excellent   |
| filter          | No     | Often | Varies    | Good (blur is costly on large areas) |
| box-shadow      | No     | Yes   | No        | Moderate    |
| width/height    | Yes    | Yes   | No        | Poor        |
| top/left        | Yes    | Yes   | No        | Poor        |

Use `will-change` sparingly -- only on elements about to animate, remove when done. Do NOT set on many elements permanently.

---

## Step 10: Stagger Animations for Lists

### Dynamic Stagger with Custom Properties

```css
.stagger-list > * {
  animation: stagger-in 0.4s var(--ease-out) both;
  animation-delay: calc(var(--index, 0) * 60ms);
}
@keyframes stagger-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
```

```html
<ul class="stagger-list">
  <li style="--index: 0">Item 1</li>
  <li style="--index: 1">Item 2</li>
  <li style="--index: 2">Item 3</li>
</ul>
```

### Stagger Rules
- Total stagger time should not exceed 600ms
- Per-item delay: 40-80ms between items
- Cap the delay after 8-10 items (they can all appear together): `animation-delay: calc(min(var(--index, 0), 8) * 60ms);`

---

## Quick Reference

1. Every animation needs a purpose: feedback, guidance, or state change.
2. Keep durations short: 100-400ms for most UI interactions.
3. Use ease-out for entrances, ease-in for exits, ease-in-out for moves.
4. Only animate `transform` and `opacity` for best performance.
5. Always implement `prefers-reduced-motion`.
6. Use skeleton loaders for content loading, spinners for actions.
7. Stagger list animations at 40-80ms intervals, total under 600ms.
8. Use `animation: ... both` to maintain end state.
9. Spring easings (`cubic-bezier` with values >1) add personality.
10. Test on low-end devices -- animation that jitters is worse than no animation.

## Verify the Motion

Motion can't be judged from code. Check it before handing off:

1. **Frames**: with Playwright, capture the element mid-animation and at rest (e.g. `page.screenshot()` right after triggering, then after `await page.waitForTimeout(duration + 50)`), and view both with Read. Confirm the start and end states are correct and nothing jumps or overflows.
2. **Reduced motion**: re-run with `await page.emulateMedia({ reducedMotion: 'reduce' })` (or `browser.newContext({ reducedMotion: 'reduce' })`) and confirm content is visible and static immediately.
3. **Performance**: in DevTools Performance (or `chrome://tracing`), look for long frames and "Layout" during the animation; if present, switch to `transform`/`opacity`.
