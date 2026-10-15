---
name: 29-video-scroll-scrubbing
description: Synchronize scroll progress with HTML5 video currentTime for cinematic, frame-like scroll scrubbing with robust loading and mobile fallbacks.
---

# Video Scroll Scrubbing

## Purpose

Synchronize scroll progress with HTML5 video currentTime for cinematic, frame-like scroll scrubbing with robust loading and mobile fallbacks.

## AI implementation contract

Act as a senior frontend engineer specializing in **Video Scroll Scrubbing**.

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


## Canonical video pipeline

`scroll progress → target time → video.currentTime`

- Wait for metadata before using `duration`.
- Use `muted`/`playsInline` where needed for mobile playback behavior.
- Use a poster while loading.
- Coalesce frequent seeks with `requestAnimationFrame` when needed.
- Handle seek stalls and mobile limitations.
- Do not assume every browser provides perfectly frame-accurate random seeking.
- Consider an image sequence when exact visual control is required.
- Provide reduced-motion and static fallbacks.

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
