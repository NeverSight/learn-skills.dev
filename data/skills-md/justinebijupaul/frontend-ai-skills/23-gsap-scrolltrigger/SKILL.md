---
name: 23-gsap-scrolltrigger
description: Build scroll-linked and scroll-triggered experiences using triggers, scrubbing, pinning, snapping, timelines, refresh, and responsive contexts.
---

# GSAP ScrollTrigger

## Purpose

Build scroll-linked and scroll-triggered experiences using triggers, scrubbing, pinning, snapping, timelines, refresh, and responsive contexts.

## AI implementation contract

Act as a senior frontend engineer specializing in **GSAP ScrollTrigger**.

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


## Core patterns

Use:
- `trigger`, `start`, `end`
- `scrub`, `pin`, `snap`
- timelines and labels
- `invalidateOnRefresh`
- responsive contexts / matchMedia
- markers during development
- cleanup in React
- refresh after layout-changing assets load

Use ScrollTrigger when scroll position should control animation progress. Do not add it merely because a page contains scrolling.

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
