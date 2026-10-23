---
name: superior-responsive
description: Design, implement, or repair responsive web and app layouts across narrow, wide, zoomed, and touch-oriented viewports. Use for mobile and desktop composition variants, reflow, overflow, adaptive navigation, content-driven breakpoints, and mobile interaction layout. Do not use for purely visual styling with no responsive impact.
---

# Superior Responsive

Make the same task usable across available space and input conditions. Responsive work is re-composition, not desktop shrinkage.

## Diagnose from content

- Identify the first width where reading order, controls, data, or navigation stop working.
- Trace the element that establishes the bad width; do not hide page overflow before finding its source.
- Inspect fixed widths, minimum sizes, grid tracks, unbreakable text, positioned elements, media, tables, and viewport units.
- Test with realistic long labels and dense content, not only an empty happy path.

Choose breakpoints where the composition fails. Device names may be test targets, but they are not design evidence.

## Choose composition variants

Define what remains invariant across viewports: the user's task, content meaning, available actions, and state. Then decide what may change: grouping, placement, density, navigation model, representation, or interaction sequence.

Read [references/responsive-composition-patterns.md](references/responsive-composition-patterns.md) when creating a new responsive layout, redesigning several regions, or choosing distinct mobile and desktop compositions. Use it to compare transformation patterns for navigation, sidebars, grids, tables, forms, heroes, dashboards, and footers. For a focused overflow or breakpoint repair, work directly without loading the reference.

Do not implement separate mobile and desktop experiences that drift in capability or content ownership. Variants may look and behave differently while preserving the same task contract.

## Recompose deliberately

- Preserve task order when columns stack. Source order should remain meaningful.
- Keep one authoritative semantic and content hierarchy across breakpoints. Do not duplicate hidden desktop and mobile copies of primary content merely to achieve a different composition.
- Collapse, wrap, scroll a bounded data region, or change representation based on content needs.
- Let grids use the fewest columns that keep each item useful. Do not retain a desktop grid merely for symmetry.
- Scale type and spacing within readable limits; avoid shrinking controls and text until they technically fit.
- Prefer dynamic viewport units and content-based minimums where browser chrome or keyboards affect available space.
- Reserve fixed positioning for elements whose persistent availability justifies the space they consume.

## Navigation and touch

- Adapt navigation before labels collide or targets become too small.
- Keep the current location visible and make collapsed menus operable with keyboard and touch.
- Ensure persistent headers, bottom bars, dialogs, and virtual keyboards do not cover content or focused fields.
- Give controls sufficient target area and separation. The visible icon may be smaller than its interactive area.
- Do not rely on hover for disclosure or essential actions.

Read [references/viewport-input-and-safe-areas.md](references/viewport-input-and-safe-areas.md) when browser chrome, virtual keyboards, notches, foldable segments, orientation, pointer capability, standalone display mode, or embedded containers affect the available space or interaction.

## Overflow decisions

- Fix unintended page-level horizontal scrolling at its owner.
- Allow intentional local scrolling for wide tables, timelines, or canvases and provide a clear visual boundary.
- Do not use `overflow: hidden` to conceal text, focus rings, menus, or broken layout.
- Allow long tokens to wrap or truncate only when the complete value remains accessible.

## Verification matrix

Test the changed surface at:

- its widest supported composition;
- just above and below each affected breakpoint;
- a narrow phone-sized viewport;
- text zoom or browser zoom relevant to the platform;
- short and long content;
- keyboard focus and an open mobile keyboard for changed forms.

Verify no accidental page overflow, clipping, overlap, inaccessible actions, or order changes. Report representative dimensions and anything not exercised.

Distinguish layout-viewport, visual-viewport, container, and input constraints in the report when they produce different behavior. Do not claim mobile coverage from width-only emulation when keyboard, safe-area, orientation, or touch behavior owns the risk.
