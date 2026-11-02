---
name: apply-transitions
description: "Finds modals, dropdowns, hover states and other UI changes that happen instantly with no animation, sorts each by the kind of interaction, and applies the matching duration and easing from DESIGN.md. Use after the design-system pipeline, or when an app feels abrupt when things open, close or change."
---

# Apply Transitions

Find parts of the UI that appear, disappear or change instantly, and give them transitions using the motion tokens in `DESIGN.md`.

## Before you start

```bash
grep -A6 '^## Motion' DESIGN.md || echo "MISSING"
```

Stop if `DESIGN.md` has no Motion section. Adding durations without shared tokens creates the exact inconsistency this pass is meant to fix.

## Step 1: Find changes with no transition

You're looking for something that's missing, so search for the places where UI changes, then check each one for a transition.

Things that show and hide:

```bash
# Svelte
grep -rn '{#if' src --include="*.svelte" | head -40
# React and JSX
grep -rn -E '\{\s*\w+\s*&&\s*<|\{\s*\w+\s*\?\s*<' src --include="*.tsx" --include="*.jsx" | head -40
# Vue
grep -rn 'v-if=' src --include="*.vue" | head -40
```

For each result, check whether the element has `transition:`, `<AnimatePresence>` or `<Transition>`. Note the ones that don't. The usual suspects are modals, dropdowns, toasts, tooltips, accordions, tab panels, error messages and loading states.

Hover, focus and open states:

```bash
grep -rn -E 'hover:|focus:|active:|aria-expanded|data-state' src --include="*.svelte" --include="*.tsx" | grep -v 'transition' | head -40
```

For example, a `hover:bg-*` without `transition-colors` changes color instantly.

Inline styles that change:

```bash
grep -rn -E 'style=.*(height|width|opacity|transform).*\$?\{' src --include="*.svelte" --include="*.tsx" | head -20
```

## Step 2: Pick a speed by the kind of interaction

Choose the duration by what kind of interaction it is, not element by element.

| Kind | Duration | Examples |
|---|---|---|
| Small | 150ms | hover, focus, press, checkbox, toggle |
| Standard | 250ms | dropdown, tooltip, popover, accordion, tab |
| Large | 400ms | modal, drawer, page change, anything full-screen |

Use the duration tokens from the Motion section of `DESIGN.md`, not raw numbers. Take the easing from there too: the ease-out curve for things entering, ease-in for things leaving.

## Step 3: Rules for every transition

**Only animate `transform` and `opacity`.** Animating `width`, `height`, `top` or `margin` makes the browser redo the page layout on every frame, which stutters. To animate height, animate `grid-template-rows` or use a scale transform instead.

**Respect the reduced-motion setting.** Add this whenever you add transitions:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

With reduced motion on, keep fades and remove movement. Sliding and zooming can make people with motion sensitivity feel sick. Fades don't.

**Don't animate things that are already there when the page loads.** Animate elements when they appear or change, not on first render.

## Step 4: Report

For each file: what you found, which kind of interaction it is, and the token you used. Then the total for each kind.

List anything you deliberately left without a transition, and why. Some changes should be instant.
