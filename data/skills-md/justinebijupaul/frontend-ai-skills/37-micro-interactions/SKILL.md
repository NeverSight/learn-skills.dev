---
name: 37-micro-interactions
description: Create polished hover, press, focus, toggle, card, button, and feedback animations that improve usability.
---

# Micro Interactions

## Purpose

Create polished hover, press, focus, toggle, card, button, and feedback animations that improve usability.

## AI implementation contract

Act as a senior frontend engineer specializing in **Micro Interactions**.

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
