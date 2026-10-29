---
name: ui-intergrity
description: Prevent and fix visual integration bugs when building, modifying, or reviewing user interfaces, especially browser extensions or UI injected into third-party websites. Use for overlap, stacking, clipping, positioning, layout-shift, scrolling, animation, responsiveness, duplicate mount, click-blocking, and host-site interference issues.
---

# UI Integrity

Prevent visual integration bugs, including unintended overlap; z-index or stacking-context conflicts; clipping and overflow; broken absolute, fixed, or sticky positioning; layout shifts; scroll and animation collisions; extension UI interfering with native website UI; invisible elements blocking clicks; duplicate injected components; and responsive-layout breakage.

## Approach

When changing UI:

1. Identify the component's intended spatial owner and positioning context.
2. Inspect nearby native and custom UI for possible collisions.
3. Test default, hover, expanded, animated, scrolled, and resized states.
4. Check bounding boxes, overflow, stacking contexts, and pointer events when something looks wrong.
5. Fix the underlying layout relationship instead of masking it with arbitrary offsets or huge `z-index` values.
6. Re-test the changed component and surrounding UI.

## Browser extension rules

When injecting UI into another website:

- Treat the host DOM and CSS as untrusted and changeable.
- Scope or isolate extension styles.
- Avoid fragile selectors and assumptions about host layout.
- Do not break, cover, move, or intercept native site controls.
- Account for SPA navigation and dynamic DOM updates.
- Prevent duplicate mounts.
- Prefer positioning relative to the component the UI visually belongs to.

## Pressure-test

Before considering UI complete, actively check for overlaps, clipping, off-screen content, incorrect stacking, scroll or animation collisions, blocked click targets, long-text breakage, viewport-width breakage, and host-site interference. Do not declare the UI finished just because the default screenshot looks correct.
