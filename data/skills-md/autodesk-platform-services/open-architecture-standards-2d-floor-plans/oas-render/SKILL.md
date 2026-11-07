---
name: oas-render
description: Use when mapping OAS plans to a visual output — SVG, Canvas, or WebGL — including scale, axis orientation, and z-order layering.
---

# OAS Render

## When to use

Use this skill when the task is about *visualizing* an OAS plan rather than authoring its data: picking a mm→px scale, choosing axis orientation, deciding layer order, producing SVG/Canvas/WebGL output. There are no new JSON object types here — this is a rendering contract over existing OAS entities.

## Critical rules

1. **Pick one mm→px scale per render context.** A single scale factor applies to every coordinate in the drawing; do not mix scales across entities or layers. Aspect ratio must be preserved.
2. **OAS Y-axis points up.** Most screen renderers (SVG, Canvas) have Y pointing down. Invert Y at the render boundary; do not mutate the source data.
3. **Use the documented SVG group ids.** Group output into `<g id="oas-rooms">`, `<g id="oas-walls">`, `<g id="oas-openings">`, `<g id="oas-circulation">`, `<g id="oas-labels">` — the spec depends on this naming for selection and theming.
4. **Walls render in one of two ways.** Either as a `<line>` with `stroke-width = thickness_mm * scale`, or as a polygon for full accuracy. Pick one strategy per renderer; don't mix.
5. **Follow the documented draw order.** Room fills → room boundaries → walls → openings → circulation → labels → annotations. The spec lists the exact order — don't reinvent it.
6. **Renderers should not invent geometry.** Doors, windows, labels, dimensions all come from existing OAS entities. Don't synthesize them from inferred adjacency.

## Full schema

See [docs/render.md](../../../docs/render.md) for the full rendering rules, including layer ordering, recommended line weights, and target-specific guidance for SVG / Canvas / WebGL.

## Related skills

- `oas-layout` — the source data being rendered
- `oas-geometry` — for the coordinate conventions that the render transforms
