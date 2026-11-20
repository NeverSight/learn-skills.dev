---
name: motion-design
description: Designs purposeful UI motion for microinteractions and transitions, covering purpose, duration by distance and size, easing for enter, exit and movement, choreography and stagger, spring versus bezier curves, reduced-motion fallbacks and performance, with CSS and Framer Motion (now Motion) snippets. Use when asked to add animations, transitions, hover effects or microinteractions, or when motion feels slow, janky or excessive. Not for defining loading, empty and error states; use ui-states.
---

# Motion Design

Produces motion that explains the interface: each animation has a stated purpose, uses durations and easings from a small token set, has a reduced-motion fallback, and animates only compositor-friendly properties.

## When to use
- "Add some animation", "make it feel smoother" or "make it feel more alive"
- Defining hover, press, toggle and focus feedback
- Transitions for menus, modals, drawers, toasts, accordions and route changes
- Motion that feels sluggish, janky or distracting
- Setting up motion tokens for a design system

## Workflow
1. Gather: stack (plain CSS, or React with Motion, formerly Framer Motion, already installed), brand character (calm or energetic) and the interactions in scope. Default to CSS; use Motion only if it is already a dependency or requested.
2. Give each candidate animation one purpose: feedback (confirms an action), orientation (shows where something came from or went), continuity (preserves context between states) or attention (rare). No purpose, no animation.
3. Assign duration by size and travel distance, and easing by direction.
4. Choreograph groups: what leads, what follows, stagger interval and cap.
5. Write the reduced-motion fallback for each animation.
6. Implement with transform and opacity; test with 4× CPU throttling and on a low-end phone.
7. Store durations and easings as tokens (design-tokens).

## Rules
**Duration**
- Microfeedback (hover, press, toggle, checkbox): 100–150ms. Small elements entering (tooltip, dropdown, toast): 150–200ms.
- Medium (modal, drawer, expanding card): 200–300ms. Large or full-screen: 300–400ms. Nothing in functional UI exceeds 500ms.
- Exits take about two-thirds to three-quarters of the enter duration; longer travel and larger elements sit at the top of each band.
- Stagger list items 20–50ms apart and cap total stagger near 300ms; items beyond the first 6–8 appear together.

**Easing**
- Enter: ease-out, e.g. cubic-bezier(0, 0, 0.2, 1) or the stronger cubic-bezier(0.16, 1, 0.3, 1).
- Exit: ease-in, cubic-bezier(0.4, 0, 1, 1). On-screen movement and resizing: ease-in-out, cubic-bezier(0.4, 0, 0.2, 1).
- Linear only for opacity loops, progress bars and spinners.
- Springs for gesture-driven or interruptible motion (drag release, sheets, toggles) because they carry velocity; beziers for fixed transitions that need a predictable duration. Snappy UI spring: stiffness 400, damping 30, mass 1 (damping ratio 0.75, under 3% overshoot); lower damping only for small, playful elements.

**Performance**
- Animate transform and opacity. Avoid animating width, height, top, left, margin and box-shadow; use scale or translate, or fade a pseudo-element that carries the shadow.
- Apply will-change just before an animation and remove it after; never on many elements.
- For height reveals use grid-template-rows 0fr → 1fr, or interpolate-size: allow-keywords where supported, accepting the layout cost only on small regions.
- Animations never block input; controls stay usable during transitions.

**Accessibility**
- Under prefers-reduced-motion: reduce, remove parallax, zoom, large translations and autoplay; keep short opacity fades (≤150ms) or switch instantly. Keep essential feedback.
- No more than 3 flashes per second; auto-playing motion longer than 5 seconds needs pause, stop or hide (WCAG 2.2.2). Never convey information through motion alone.

## Output
- Spec table: interaction, purpose, property, duration, easing, reduced-motion fallback.
- Motion tokens as CSS custom properties, then the CSS implementation.
- A Motion snippet (import from motion/react) when the project uses React with Motion; MotionConfig reducedMotion="user" can apply the fallback app-wide.

```css
:root { --dur-fast: 120ms; --dur-base: 200ms; --dur-slow: 300ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1); --ease-in: cubic-bezier(0.4, 0, 1, 1); }
.menu { opacity: 0; visibility: hidden; transform: translateY(-4px) scale(0.98);
  transition: opacity 150ms var(--ease-in), transform 150ms var(--ease-in), visibility 0s 150ms; }
.menu[data-open] { opacity: 1; visibility: visible; transform: none;
  transition: opacity var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out), visibility 0s; }
@media (prefers-reduced-motion: reduce) { .menu, .menu[data-open] { transform: none; } }
```

```jsx
import { motion, AnimatePresence, useReducedMotion } from "motion/react";

export function Toast({ open, children }) {
  const reduce = useReducedMotion();
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, y: reduce ? 0 : 12 }}
          animate={{ opacity: 1, y: 0, transition: { type: "spring", stiffness: 400, damping: 30 } }}
          exit={{ opacity: 0, y: reduce ? 0 : 8, transition: { duration: 0.15, ease: [0.4, 0, 1, 1] } }}
        >
          {children}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

## Avoid
- Animating every element on load, or fade-up-on-scroll on every section
- Durations over 500ms for UI responses; bounce or elastic easing on functional controls
- Animating width, height, top, left or box-shadow on large elements
- Linear easing for movement
- will-change applied globally
- Ignoring prefers-reduced-motion, or blocking input until an animation ends
- One-off durations per component (0.35s, 0.4s, 0.27s) instead of tokens

## Final check
- [ ] Every animation has a stated purpose
- [ ] Durations come from tokens; UI feedback 100–300ms; nothing over 500ms
- [ ] Enter ease-out, exit ease-in and shorter, movement ease-in-out
- [ ] Only transform and opacity animated, exceptions justified
- [ ] Reduced-motion fallback verified via the OS setting or DevTools emulation
- [ ] No flashing over 3 per second; auto motion over 5 seconds can be paused
- [ ] Smooth at 4× CPU throttling
