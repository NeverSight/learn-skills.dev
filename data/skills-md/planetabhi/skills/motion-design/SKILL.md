---
name: motion-design
description: >
  Load this skill when adding or reviewing web UI motion such as animations, transitions, entrances and exits, hovers, modals, dropdowns, toasts, page transitions, and micro-interactions. Triggers on "animate", "add a transition", "make it move", "motion", "fade", "slide", "stagger", "open and close". Builds dependency-free, Baseline-first, framework-agnostic CSS, with the Web Animations API and View Transitions API where they help.
---

# Motion design

Apply these rules to every animation and transition. Examples are dependency-free CSS, plus the Web Animations API and the View Transitions API. They translate directly to any framework or utility system. The detailed rules and patterns are bundled under `./reference/`. Read the relevant file before applying or citing a rule.

## Core mandate

Animate only with a clear purpose, keep every animation accessible, and add no runtime dependencies. Motion should clarify a change, not decorate it. Prefer the cheapest technique that works, reuse the project's existing motion tokens, and ship the reduced-motion alternative with the animation rather than as a follow-up.

## Confirmation

When you are only reviewing, report findings without pausing. Before applying edits to existing files, confirm the intended change set first, and ask for any context you need to judge correctly instead of guessing.

## Decision sequence

Work every animation through these steps in order, and stop at any step that fails.

1. Decide whether to animate. Apply the frequency and purpose gate in the next section, and be willing to ship no animation. Refer to [reference/principles.md](./reference/principles.md).
2. Choose what moves. Animate `transform` and `opacity` only, and keep off layout properties. Refer to [reference/performance.md](./reference/performance.md).
3. Choose the technique. Use a CSS transition for a state change, a CSS animation for a loop, the Web Animations API for scripted or interruptible motion, or the View Transitions API for a DOM change with a fallback. Refer to [reference/techniques.md](./reference/techniques.md).
4. Shape the entrance and exit. Decelerate in, make the exit faster, set `transform-origin` at the trigger for popovers, and stagger short lists. Refer to [reference/entrances-and-exits.md](./reference/entrances-and-exits.md).
5. Define the reduced-motion alternative. Provide a real substitute such as a cross-fade, not just an off switch. Refer to [reference/accessibility.md](./reference/accessibility.md).
6. Make it interruptible. Let the user reverse or redirect the motion mid-flight where that is expected. Refer to [reference/interactivity.md](./reference/interactivity.md).
7. Verify performance and quality. Hold 60fps on a mid-range device, then run the checklist. Code inspection cannot confirm frame rate or smoothness, so mark anything that needs a running page as pending verification rather than passed. Refer to [reference/performance.md](./reference/performance.md) and [reference/checklist.md](./reference/checklist.md).

## Decision gate

Two questions gate every animation, in order. If either fails, do not animate.

1. Frequency. Consider how often a user sees this. Something seen hundreds of times a day should not animate. Occasional and first-time surfaces carry the budget.
2. Purpose. Name one: feedback, spatial consistency, state indication, preventing a jarring change, or delight. Delight is allowed only on rare or first-time surfaces.

| Frequency | Decision |
| --- | --- |
| Hundreds of times a day (keyboard shortcuts, command palette) | No animation |
| Tens of times a day (hovers, list navigation) | Near-imperceptible only, or nothing |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare or first-time (onboarding, success) | The delight budget lives here |

Content the user is reading or acting on must not move for style. Full detail is in [reference/principles.md](./reference/principles.md).

## Motion tokens

Reuse the project's existing tokens if it has them. Otherwise use this built-in scale, which is self-contained and needs no other skill installed. Full scale and a copyable `_tokens.css` are in [reference/motion-tokens.md](./reference/motion-tokens.md).

| Duration | Value | Usage |
| --- | --- | --- |
| `--motion-duration-1` | `100ms` | micro feedback, hover, icon |
| `--motion-duration-2` | `150ms` | exits, tooltip out |
| `--motion-duration-3` | `200ms` | dropdowns, popovers, small enter |
| `--motion-duration-4` | `300ms` | modals, drawers, page transitions |
| `--motion-duration-5` | `500ms` | large or first-time emphasis |

| Easing | Value | Usage |
| --- | --- | --- |
| `--motion-ease-out` | `cubic-bezier(0.22, 1, 0.36, 1)` | entrances, the default |
| `--motion-ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | movement within the screen |
| `--motion-ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | exits that leave the screen |

## Reference map

Read the relevant file before applying or citing a rule.

- Foundations:
   - [reference/principles.md](./reference/principles.md) — When to animate, purpose, and restraint
   - [reference/motion-tokens.md](./reference/motion-tokens.md) — Duration, easing, distance, and scale
- Techniques:
   - [reference/techniques.md](./reference/techniques.md) — Transition, animation, Web Animations API, and View Transitions
   - [reference/entrances-and-exits.md](./reference/entrances-and-exits.md) — Enter, exit, open and close asymmetry, transform-origin, stagger
   - [reference/interactivity.md](./reference/interactivity.md) — Interruptible motion and gesture feel
   - [reference/performance.md](./reference/performance.md) — Compositor-friendly properties and 60fps
- Patterns:
   - [reference/patterns.md](./reference/patterns.md) — Curated dependency-free, accessible recipes
- Quality:
   - [reference/accessibility.md](./reference/accessibility.md) — Reduced-motion alternatives and vestibular safety
   - [reference/checklist.md](./reference/checklist.md) — Testing checklist
- Credits:
   - [reference/credits.md](./reference/credits.md) — Lineage and sources

## Anti-patterns

- Animating layout properties like `width`, `height`, `top`, or `left`.
- Treating reduced motion as an off switch instead of a real substitute.
- Animating high-frequency surfaces such as a command palette.
- Moving content the user is actively reading or acting on.

---

Authored by @planetabhi
