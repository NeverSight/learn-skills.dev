---
name: responsive-implementation
description: "Implements a responsive layout plan in CSS: fluid layout, breakpoints tied to content, container-based adaptation, resilience to zoom, text-size, and input mode, and verification at defined viewports. Use when a layout specification must be built, or when an existing layout breaks at some sizes, zoom levels, or text settings."
---

# Responsive Implementation

## Purpose
Build layouts that adapt to viewport, container, input mode, and user settings as specified, and verify the behavior at stated conditions.

## When to use
- Use when: a responsive layout specification must be implemented.
- Use when: a layout overflows, clips, or loses content at some widths, zoom levels, or text settings.
- Do not use when: how the layout adapts is undecided. This work implements decisions. It does not make them.
- Pairs with: `responsive-layout-planning` decides how the layout adapts; use it first when that is undecided.

## Inputs
- Required: how each region or component adapts (reflow order, what collapses, minimum and maximum widths, content that can grow), and the supported viewport range and browsers.
- Optional: tokens for spacing and breakpoints, existing layout primitives, target devices and orientations, a touch target size requirement.
- Assumptions: unspecified adaptation behavior is reported as a gap. If the specification names no breakpoints, derive them from where the content needs a change and record each as proposed.

## Process
1. Extract the adaptation rule for each region and component. Mark gaps, such as no behavior below some width or no touch target size.
2. Write the base styles for the narrowest case: a single column in source order that works without media queries. Add layout as space allows.
3. Prefer intrinsic and fluid techniques first: flexible and grid layout with minimum and maximum sizes, wrapping, relative units, and logical properties. Add a breakpoint only where the layout truly changes.
4. Set each breakpoint from the specification, or from where the content breaks if none is given. Take its name and value from the token source when one exists. Record the reason for each.
5. Adapt a component that appears in containers of different widths to its container's size where browser support allows. Record the support decision and any fallback.
6. Make layout survive user settings. Size text and spacing in relative units, avoid fixed-height containers for text, bound line length, and let text spacing overrides apply without clipping.
7. Handle input modes. Use capability-based media features and not device detection. Give targets the specified size and spacing, and never make essential information depend on hover. Honor reduced-motion and other preference features where specified.
8. Reserve space for media and embeds to prevent layout shift. Scale them to their container and keep their aspect ratio.
9. Handle overflow deliberately. Let long words and URLs wrap, and let wide data such as tables and code scroll inside its own container. Avoid page-level horizontal scrolling except for content that requires it.
10. Verify at the conditions listed below.

## Rules and heuristics
- Required: do not disable user zoom or text scaling.
- Required: all content and functionality remain available at every supported size. Hiding follows the specification, and hidden content is not focusable.
- Required: when CSS reorders content, reading order and focus order stay meaningful. Record any divergence from source order and its impact.
- Recommended: name breakpoints by role and not by device, and keep their number small.
- Recommended: use fixed pixel values only where a fixed size is the intent, such as hairlines.

## Checks
- Render at the narrowest supported width, at and just below each breakpoint, between breakpoints, and at the widest supported width. Record what was observed, or mark the condition unverified.
- At narrow widths, check zoom and text enlargement against the applicable accessibility standard's resize and reflow criteria, including text spacing overrides. Confirm no content or function is lost.
- Check each specified orientation.
- Confirm focus is visible and not covered by fixed or sticky elements at each size.
- Measure touch target sizes against the specified value.
- State which conditions used browser emulation and which used real devices. Overflow detection and screenshots show what they observe and do not show real-device usability.

## Output
Return the CSS and markup changes, an adaptation table (region or component, behavior per range, mechanism), the breakpoints with reasons, support and fallback decisions, a verification matrix with evidence, and gaps and assumptions.

## Completion criteria
- The layout matches the specification at every verified condition.
- No content or function is lost at the checked zoom and text settings, or each loss is listed.
- Gaps are reported and verification limits are stated.
