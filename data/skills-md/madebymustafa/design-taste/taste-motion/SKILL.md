---
name: taste-motion
description: |
  Motion craft for agent-built interfaces: duration and easing tokens, entrance choreography, hover/active micro-interactions, scroll-driven reveals, layout transitions, and prefers-reduced-motion compliance. Prevents the two AI-motion crimes: nothing moves at all, or everything moves forever. Stack on the design-taste core skill.
triggers:
  - "animation"
  - "motion design"
  - "transitions"
  - "micro interactions"
  - "scroll animation"
  - "easing"
---

# taste-motion

> Motion's job is to explain the interface, not decorate it. Every animation must answer: what happened, where is it, what do I do next.

## 1. THE DURATION SCALE (Fixed Tokens)

| Token | Duration | Use for |
|---|---|---|
| `--dur-fast` | 100–150ms | hovers, pressed states, focus rings |
| `--dur-base` | 200–300ms | small entrances, state changes (toggle, open/close) |
| `--dur-slow` | 400–600ms | section reveals, page-level transitions, dialog open |
| `--dur-hero` | 600–900ms | the ONE hero entrance sequence |

Under 100ms reads as a blink (unless it's a snap, which brutalist packs do deliberately). Over 900ms reads as a slow website.

## 2. THE EASING TOKENS (Fixed)

- **Standard (UI states):** `cubic-bezier(0.4, 0, 0.2, 1)` — fast in, calm out. Default for hovers and toggles.
- **Emphasized (entrances/reveals):** `cubic-bezier(0.22, 1, 0.36, 1)` — long calm tail. Premium feel.
- **Exit:** `cubic-bezier(0.4, 0, 1, 1)` or faster — exits are snappier than entrances.
- **Spring/overshoot (playful packs only):** `cubic-bezier(0.34, 1.56, 0.64, 1)` — max once per element, never on loops.
- Never use `ease-in-out` as a catch-all. Never use `linear` except for marquees/progress.

## 3. WHAT TO ANIMATE (And What Not To)

**Animate:** `transform` and `opacity`. That's it. 60fps guaranteed.

**Never animate:** `width`/`height` (layout jank — use transform: scale), `margin`, `top/left` (use transform), `box-shadow` at large sizes (use a pre-blurred pseudo-element), `filter: blur` on large surfaces.

## 4. CHOREOGRAPHY (Entrances)

- **One scene per section:** on scroll reveal, the section's elements enter in 2–3 stages (heading → body → CTA), 60–120ms apart, same duration and easing. Stagger is hierarchy.
- **Distance ≤ 20px** for reveals (translateY 8–16px) + opacity. Bigger distances look like PowerPoint.
- **Scale entrances ≤ 0.96→1** and only on dialogs/popovers, never on full sections.
- **Hero:** one sequence, 600–900ms total, elements entering once. No looping float, no repeating wave.
- **Loop allowance:** exactly one class of loops allowed per page — ambient status indicators (live dots, loaders, spinners). Everything else loops = error.

## 5. MICRO-INTERACTIONS (Hover, Press, Focus)

- Hover: 100–150ms, standard easing, one property change (bg tone, border, translateY −1 to −3px). Never both color AND position AND shadow at once.
- Pressed: inverse of hover (translate down, shadow off), 80–120ms.
- Focus-visible: 2px ring, 3:1 contrast, `outline-offset: 2px`, animated in with 100ms fade — never `outline: none` without replacement.
- Disabled: no hover states at all — the element must look inert (opacity 0.4–0.5, no pointer change).
- Transitions on load/state-change only where the state is visible; a transition nobody can perceive is dead code.

## 6. SCROLL & LAYOUT

- **Scroll-triggered:** IntersectionObserver (or CSS `animation-timeline` where supported), one reveal per element, then done. No elements that re-animate on every scroll pass.
- **Sticky:** allowed for nav and section labels; sticky + animation = performance risk, keep the animation out.
- **View transitions / page transitions:** 300–500ms, shared-element moves where they earn it (list → detail). Disabled entirely under `prefers-reduced-motion`.
- **Layout transitions:** `FLIP` pattern (transform-based), never re-layout animations.

## 7. REDUCED MOTION (Non-Negotiable)

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

- Above the CSS gate, zero motion by default when the media query matches: no parallax, no auto-scroll carousels, no marquees.
- Animate presence only: content appears without motion (opacity 0→1 over 1 frame).

## 8. CHECKLIST (Fail the Page If…)

- [ ] Any element animates for more than ~1.5s (outside loops/loaders).
- [ ] More than one looping element per viewport.
- [ ] Any `width`, `height`, `margin`, or `top` animation.
- [ ] Reveal distances beyond 20px.
- [ ] `ease-in-out` used as the global easing.
- [ ] Every element on the page animates on load (bounce-entrance festival).
- [ ] No `prefers-reduced-motion` handling exists at all.

*If you can't explain an animation in one sentence, delete it.*