---
name: 51-animation-performance
description: Keep animation smooth by minimizing layout work, controlling render frequency, managing assets, and profiling expensive effects.
---

# Animation Performance

## Purpose

Keep animation smooth by minimizing layout work, controlling render frequency, managing assets, and profiling expensive effects.

## AI implementation contract

Act as a senior frontend engineer specializing in **Animation Performance**.

Before implementation:
- Inspect the existing repository, framework, dependencies, and conventions.
- Understand the user's actual requirement and constraints.
- Reuse existing infrastructure when it is appropriate.
- Choose the simplest technique that satisfies the requirement.
- Do not introduce a library merely because it is popular.
- Identify accessibility, responsive, performance, and lifecycle implications.

During implementation:
- Produce production-quality, maintainable code.
- Prefer composition and clear boundaries.
- Avoid unnecessary abstractions and global state.
- Handle relevant loading, error, empty, and fallback states.
- Clean up event listeners, observers, timers, animation contexts, media resources, and GPU resources.
- Keep high-frequency animation outside React state when appropriate.
- Treat mobile and reduced-motion behavior as first-class requirements.

After implementation:
- Verify the requested behavior.
- Check desktop, tablet, and mobile behavior when relevant.
- Check keyboard/accessibility behavior.
- Check console/runtime errors.
- Check performance and memory implications.
- Remove temporary debugging and dead code.
- Do not claim something is verified if it was not actually checked.

## Quality checklist

- [ ] Requirement is complete.
- [ ] Existing project conventions are respected.
- [ ] No unnecessary dependencies were introduced.
- [ ] Responsive behavior is intentional.
- [ ] Accessibility is considered.
- [ ] Performance is acceptable.
- [ ] Lifecycle cleanup is correct.
- [ ] Relevant fallbacks are implemented.
- [ ] Code is maintainable.


## Non-negotiable performance rules

Prefer `transform` and `opacity`. Be cautious with layout-affecting properties such as `width`, `height`, `top`, and `left`.

Watch for:
- forced synchronous layout
- excessive blur/filter
- huge Canvas/WebGL buffers
- high device-pixel-ratio rendering
- many simultaneous animated DOM nodes
- per-frame React renders
- unbounded asset caches

Profile expensive experiences and provide mobile fallbacks.

## Anti-patterns

Avoid:
- monolithic components
- unnecessary global state
- per-frame React state for high-frequency animation
- layout thrashing
- inaccessible custom controls
- motion without reduced-motion consideration
- replacing working infrastructure without justification
- dependency sprawl
