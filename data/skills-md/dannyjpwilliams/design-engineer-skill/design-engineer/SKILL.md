---
name: design-engineer
description: >
  Design engineering craft and execution excellence. Applies when building, reviewing, refactoring,
  or improving any UI component, page, or interaction. Triggers on: building components, styling UI,
  adding animations/transitions, reviewing design quality, refactoring frontend code, implementing
  hover/active/focus states, working with shadows/colors/gradients/spacing/typography/border-radius,
  drag interactions, layout animations, icon transitions, or when the user asks to "think like a
  design engineer." Covers the full craft spectrum: motion, color, shadows, optical alignment,
  typography, spacing, gradients, performance, gestures, and micro-interactions.
---

# Design Engineer

Think like a skilled design engineer. Every pixel, every transition, every shadow is intentional.
The difference between good and great UI is thousands of invisible details done right.

## Core Philosophy

1. **Align to the eye, not the grid.** Geometric correctness != perceptual correctness.
2. **Animate with physics, not math.** Springs over cubic-bezier. `bounce: 0` by default.
3. **Sweat the details no one consciously sees.** Everyone unconsciously feels them.
4. **Restraint over eagerness.** The best motion is invisible. Over-animation cheapens.
5. **Every value must agree on the same physical metaphor.** Contradictory values break the illusion.

## When Building UI

Apply these principles automatically. Do not wait to be asked.

### Shadows

Replace borders with layered transparent shadows. Three layers, always:

```css
box-shadow:
  0px 0px 0px 1px rgba(0, 0, 0, 0.06),   /* definition: crisp edge */
  0px 1px 2px -1px rgba(0, 0, 0, 0.06),   /* near: tight depth, -1px spread contains it */
  0px 2px 4px 0px rgba(0, 0, 0, 0.04);    /* ambient: soft diffuse light */
```

- Opacity range: 4-8%. Lower than you think.
- Hover: increase each layer by +0.02 opacity. Keep geometry identical.
- Shadows adapt to any background. Borders don't.

### Border Radius

Nested rounded elements: `outer_radius = inner_radius + padding`. Always.

```css
--inner-radius: 12px;
--padding: 8px;
--outer-radius: calc(var(--inner-radius) + var(--padding));
```

Skip only when radius is 0 or fully rounded (pill).

### Optical Alignment

- Icon+text buttons: reduce padding on the icon side (icons have less visual mass).
- Fix icon alignment in the SVG viewBox, not with CSS margin hacks.
- Vertical icon alignment: `translateY(calc(0.5em - 0.5lh))`.
- Bottom padding in cards: measure from text baseline, not descender.
- `svg { flex-shrink: 0; }` in flex containers. Always.

### Color (OKLCH)

Use OKLCH for perceptually uniform palettes. Hold L and C constant, vary hue:

```css
oklch(0.8 0.193 280)  /* purple */
oklch(0.8 0.193 140)  /* green */
oklch(0.8 0.193 60)   /* orange */
```

- Shade scales: vary L only (0.25-0.92 in ~0.10 steps). No hue drift.
- Gradients: use `linear-gradient(in oklab, ...)` for clean blends, `in oklch` for hue traversal.
- Provide hex fallbacks via `@supports (color: oklch(0 0 0))`.

### Gradients

- Default to `oklab` interpolation. Never sRGB for vibrant colors (muddy midpoints).
- Use color hints (standalone %) to shift blend midpoints, not extra color stops.
- Animate `background-position`/`background-size`, never color stops directly.
- Layer gradients with `background-blend-mode` instead of stacking DOM elements.

## When Adding Motion

Read [references/motion.md](references/motion.md) for complete animation patterns and code.

### Quick Rules

| Rule | Value |
|------|-------|
| Max duration | **< 300ms** for standard UI |
| Default easing | **`ease-out`** (or custom `cubic-bezier`) |
| Spring config | `type: "spring", duration: 0.3-0.55, bounce: 0` |
| Only animate | **`transform`, `opacity`, `filter`, `clip-path`** |
| Never animate | `width`, `height`, `margin`, `padding`, `top`, `left` |
| Active/press | `scale(0.97)`, 125ms ease-out |
| Never start from | `scale(0)` -- use 0.25+ minimum |
| Reduced motion | Always respect `prefers-reduced-motion` |

### Duration Hierarchy (by user intent urgency)

```
Focus:   0.3s  (fastest -- keyboard nav must not distract)
Tap:     0.5s  (quick tactile feedback)
Drag:    0.5s  (matches tap for consistency)
In View: 0.6s  (scroll reveals can breathe)
Hover:   0.8s  (ambient, exploratory -- longest)
```

### Icon Transitions

Animate three properties together: `opacity + scale + filter: blur()`.
- Initial/exit: `opacity: 0, scale: 0.25, filter: blur(4px)`
- Animate: `opacity: 1, scale: 1, filter: blur(0px)`
- Spring: `duration: 0.3, bounce: 0`

### Origin Awareness

Set `transform-origin` relative to the trigger element, never `center` by default.
Radix exposes `--radix-dropdown-menu-content-transform-origin` -- use it.

### Interruptibility

Users must be able to change state mid-animation. CSS transitions handle this natively.
Never lock the user out while an animation completes.

## When Reviewing UI

Check these in order:

1. **Shadows**: layered + transparent? Opacity 4-8%?
2. **Border radius**: concentric on nested elements?
3. **Optical alignment**: icon/text balance? SVG-level fixes?
4. **Motion**: springs not beziers? Under 300ms? `ease-out`?
5. **Transform-origin**: relative to trigger?
6. **Color**: OKLCH with perceptual uniformity?
7. **Performance**: only animating compositor properties?
8. **`will-change`**: specific properties, not `all`? Only on elements that animate?
9. **Accessibility**: `prefers-reduced-motion` respected? Focus animations subtle?
10. **Frequency check**: will this animation be seen 100x/day? If yes, remove or minimize.

## Performance

- Only `transform`, `opacity`, `filter`, `clip-path` are compositor-friendly (GPU).
- `will-change`: name specific properties. Never `all`. Remove when not animating.
- CSS animations/WAAPI run on compositor thread (immune to main-thread jank).
- Framer Motion uses `requestAnimationFrame` (main thread) -- understand the tradeoff.
- Use `overflow-clip` not `overflow-hidden` for drag containers (avoids scroll context).

## References

- **[references/motion.md](references/motion.md)** -- Complete animation patterns: springs, gestures, shared layout, drag, icon transitions, easing selection, code examples
- **[references/visual-craft.md](references/visual-craft.md)** -- Deep techniques: shadow systems, OKLCH color, gradients, optical alignment, concentric border radius, performance optimization

## Sources

Principles distilled from Jakub Krehel (jakub.kr) and Emil Kowalski (emilkowal.ski).
