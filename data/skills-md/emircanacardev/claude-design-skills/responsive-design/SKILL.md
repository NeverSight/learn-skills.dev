---
name: responsive-design
description: Makes web layouts work from 320px phones to 1440px and wider desktops using mobile-first CSS, content-driven breakpoints, container queries, fluid type and spacing, responsive images with srcset, sizes and aspect-ratio, and input-aware styles via hover and pointer media queries. Use when a page breaks on mobile or scrolls sideways, or when asked to make something responsive. Not for native app screens; use mobile-app-ui.
---

# Responsive Design

Produces layouts that adapt to their content rather than to device names: mobile-first CSS, a small set of justified breakpoints, components that respond to their container, fluid sizing, and images that never ship more pixels than the slot needs.

## When to use
- "It breaks on mobile" or "there is horizontal scroll"
- Converting a desktop-only design or codebase to responsive
- A component must work both in a narrow sidebar and a wide main column
- Large images slow down mobile loading or cause layout shift
- Hover-dependent menus or actions fail on touch devices

## Workflow
1. Gather: current breakpoints, framework, and viewport analytics if available. Assume evergreen browsers.
2. Write base styles for a 320px viewport with no media queries.
3. Widen the viewport until content breaks (lines too long, cards stretched, nav crowded) and add a breakpoint exactly there; record the reason in a comment.
4. Move component-level changes into container queries so components respond to their slot.
5. Replace stepped font sizes and section padding with clamp() where it removes breakpoints.
6. Fix media: srcset and sizes or picture, explicit dimensions, lazy loading below the fold.
7. Adapt to input with hover and pointer media queries.
8. Test at 320, 375, 414, 768, 1024, 1280, 1440 and 1920px, at 200% and 400% zoom, and on a landscape phone.

## Rules
**Layout**
- Mobile-first: base styles target small screens; enhancements use min-width queries in em (e.g. @media (min-width: 48em)) so they follow user font settings.
- Content-driven breakpoints usually land near 40em, 48em, 64em and 80em (640, 768, 1024, 1280px). Use only the 2–4 the content needs.
- No horizontal scrolling at 320 CSS px, which equals a 1280px window at 400% zoom (WCAG 1.4.10 Reflow). Data tables, maps and diagrams are exempt but scroll inside their own container.
- Prefer intrinsic layouts that need no breakpoint: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)) and flex-wrap.
- Give flex and grid children min-width: 0 when they hold long content; use overflow-wrap: anywhere for URLs and IDs.
- Use svh or dvh for full-height mobile sections; 100vh hides content behind browser toolbars.
- Never disable zoom: no maximum-scale=1 or user-scalable=no in the viewport meta.

**Container queries**
- Set container-type: inline-size on the slot and query with @container (min-width: 30rem). Use cqi units for sizes relative to the container.

**Fluid sizing**
- clamp(min, rem + vw, max) for type and section spacing; keep text max ≤2.5× min (see typography-system).
- Line length stays at or under 75 characters at every width; cap it with max-width in ch.

**Images**
- Always set width and height attributes or aspect-ratio to prevent layout shift.
- Use srcset with width descriptors (480w, 800w, 1200w, 1600w) and an accurate sizes attribute, e.g. sizes="(min-width: 64em) 50vw, 100vw"; without sizes the browser assumes 100vw.
- Use picture for art direction or for AVIF/WebP with a fallback.
- loading="lazy" below the fold only; the LCP image gets fetchpriority="high" and is never lazy.

**Input**
- Wrap hover-only effects in @media (hover: hover) and (pointer: fine). Anything revealed on hover must also be reachable by tap and keyboard.
- Under @media (pointer: coarse), targets are at least 44×44px with ≥8px between adjacent targets; never below the 24×24px WCAG minimum anywhere.

## Output
- Mobile-first CSS with a comment explaining each breakpoint, or Tailwind responsive classes if the project uses Tailwind (min-width defaults: sm 640, md 768, lg 1024, xl 1280, 2xl 1536px).
- Image markup with srcset, sizes and dimensions.
- Test matrix: width or zoom level × pass/fail, with the issue and fix for each failure.

## Avoid
- Device-named breakpoints (iPhone, iPad) and desktop-first max-width cascades full of overrides
- Hiding content users need on mobile with display: none
- Fixed pixel widths on containers (width: 1200px)
- 100vh heroes on mobile
- Hover-only menus, tooltips or row actions
- Breakpoints every 100px to patch single elements
- Shipping desktop-sized images to phones

## Final check
- [ ] No horizontal scroll at 320px or at 400% zoom on a 1280px window
- [ ] Each breakpoint justified by content; 4 or fewer
- [ ] Components placed in multiple slots use container queries
- [ ] Images have dimensions or aspect-ratio; LCP image not lazy-loaded
- [ ] Hover interactions have tap and keyboard equivalents
- [ ] Coarse-pointer targets ≥44×44px
- [ ] Measure ≤75ch at wide widths
