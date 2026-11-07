---
name: oas-geometry
description: Use when writing or debugging OAS geometry — points, polygons, line segments, arcs, circles, spirals, fillets, units, or coordinate conventions. Load before any geometry-heavy edit.
---

# OAS Geometry

## When to use

Use this skill whenever the task touches coordinates, curves, polygon validity, units, or angular conventions. This is the largest section of the spec, so load it early when you suspect a geometry bug (integer-mm violations, polygon not closing, arc winding wrong). If the work is about which entity owns the geometry (room vs. wall etc.), prefer `oas-core` or `oas-layout`.

## Key types

- `Point` — `{ x, y }` in integer mm (optionally `z` for railings on stairs)
- `Polygon` — ordered `points` array plus explicit `"closed": true`; `closed: false` is allowed for open paths (e.g. railings)
- `LineSegment` — straight edge from `start` to `end`
- `Arc` — circular arc with `center`, `radius_mm`, `start_angle_deg`, `end_angle_deg`
- `Circle` — full circle (`center`, `radius_mm`)
- `Spiral` / `Fillet` — specialty curves used for stairs and corners

## Critical rules

1. **No decimals in coordinates.** Every `x`, `y`, `z`, radius, length is integer millimeters. The single exception is `area_m2`, which is a derived decimal value in square meters.
2. **Polygons must declare `"closed": true` explicitly.** A polygon without this flag is not closed by convention — don't rely on the last point matching the first.
3. **Consistent winding.** Point order must be uniformly clockwise or counterclockwise; do not mix. Positive rotation is counterclockwise.
4. **Arc sweep is CCW from `start_angle_deg` to `end_angle_deg`.** If you want a clockwise visual arc, swap start/end — do not negate angles.
5. **Units are global.** `units.length` is `"mm"` and `units.angle` is `"deg"` for the whole document; do not introduce per-entity unit overrides.

## Full schema

See [docs/geometry.md](../../../docs/geometry.md) for the complete reference, including arc parameterization, spiral construction, and fillet rules.

## Related skills

- `oas-core` and `oas-layout` — consumers of these geometric primitives
- `oas-render` — for how these primitives map onto screen coordinates (Y typically inverts)
