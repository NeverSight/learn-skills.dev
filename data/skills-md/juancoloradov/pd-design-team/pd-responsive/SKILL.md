---
name: pd-responsive
description: >-
  Use when a design must work across screen sizes, devices, or platforms: responsive breakpoints, fluid
  layouts, adaptive component behavior, touch targets, density, and platform conventions (web, mobile
  web, iOS, Android, native apps). Consumes the design; binds to the live system. Part of the pd-* design team.
metadata:
  team: product-design
  role: responsive
  version: "2.0.0"
---

# pd-responsive — hold up across devices

## Overview

Make the design work across the real range of devices and platforms it will run on by **adapting**
layout and behavior, not just scaling pixels. A field app, a consumer app, and a dense admin console
can be very different contexts even within one product, so start from who uses which surface, where,
and with what input.

## Before you start

- Load `pd-foundations`: `design-system.md`, `accessibility.md` (targets, zoom/reflow), `principles.md`.
- Read `docs/design/PROJECT.md` (`platforms`, `users`, `design_system`). If it is missing, proceed with
  defaults recorded as assumptions, or ask `pd-design-lead`.
- Read the upstream `*-design-*.md` (required) and `*-flows-*.md` (optional).

## When to use

- A design must support multiple breakpoints, devices, or platforms.
- Touch or mobile behavior, or platform conventions, need defining.

## Breakpoints and strategy

- **Mobile-first, content-driven**: set breakpoints where the content breaks, not at device sizes.
  Check `design-system.md` and the live system for existing breakpoint tokens and reuse them; if none
  exist, propose rough ranges (small mobile ~360-480px, tablet ~768px, desktop ~1024-1280px, large
  ~1440px+) and flag the gap to `pd-design-system-ops`.
- **Fluid plus adaptive**: fluid scaling within a range (`clamp()` for type and spacing, CSS Grid
  `minmax()`/`auto-fit` for columns), with layout changes at breakpoints. Prefer container queries over
  viewport media queries for components that adapt to their parent's size.
- **Reflow**: usable at 400% zoom / 320 CSS px wide without loss of content or function (WCAG 1.4.10).

## Adaptive behavior

- Layout: stack vs. multi-column; what reflows, reveals, or hides at each size.
- Navigation: the pattern per size (tabs, drawer, sidebar) and how it transforms.
- Orientation: define portrait and landscape where both are expected (tablets, foldables).
- Density: state the concrete levers (row height, type-scale step, touch-target padding) so the
  trade-off between a dense admin and a focused mobile task is specified, not just named.

## Touch and platform

- **Touch targets** come from three sources with different units and purposes. WCAG 2.2 SC 2.5.8
  (AA) sets a 24x24 CSS px minimum, with spacing and inline exceptions; treat it as the compliance
  floor. Apple HIG recommends 44x44 pt; Material recommends 48x48 dp. State the unit per platform,
  keep units separate, and keep spacing between adjacent targets so hit areas do not overlap. Platform
  guidance changes, so verify the current HIG or Material guidance when a number matters.
- Input differences: touch, mouse, and keyboard; hover cannot be required.
- Platform conventions: use the platform's native patterns rather than a generic guess (iOS: bottom
  tab bar, swipe-back, action sheets, native pickers; Android: bottom nav or rail, system back,
  bottom sheets and snackbars; web: responsive nav collapsing to a drawer, no hover-only
  affordances). Note safe areas and notches, and the back-navigation model per screen.

## Process

1. **Target matrix**: devices and platforms to support, with priority.
2. **Breakpoints and strategy**, mobile-first.
3. **Per-breakpoint specs**: layout and component behavior at each size (what adapts and how).
4. **Touch and platform adaptations**: targets, input, conventions, safe areas.
5. **Accessibility check**: reflow at 400%, zoom, target sizes.

## Output

`<artifacts_dir>/<date>-responsive-<topic>.md`: handoff header (`discipline: responsive`), then target/platform
matrix, breakpoints and strategy, per-breakpoint layout and behavior, touch/platform notes, reflow and
zoom results, flagged gaps. `upstream:` design (and flows, if used). `downstream:` `mocks` (optional reader),
`handoff`, `qa`.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for responsive and apply it on top of
this skill.

## Common mistakes

- Scaling instead of adapting; designing desktop-first, then cramming into mobile.
- Touch targets under the platform minimum, or quoting one number without its unit.
- Requiring hover, or ignoring platform conventions and safe areas.
- Breaking reflow or zoom (content clipped or horizontal scroll at 320 CSS px).
- Inventing breakpoint values when the system already defines them.
