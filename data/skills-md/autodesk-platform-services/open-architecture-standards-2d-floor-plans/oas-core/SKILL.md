---
name: oas-core
description: Use when authoring or editing OAS-Core JSON — rooms, walls, openings (doors/windows), curtain walls, roofs, floor slabs, furniture, railings, or annotations in a 2D floor plan.
---

# OAS Core

## When to use

Reach for this skill any time you are emitting or modifying the foundational entities of an OAS plan: rooms, walls, openings, curtain walls, roofs, floor slabs, furniture, railings, or annotations. If the task is purely about coordinates and polygons, use `oas-geometry` instead. If the task is multi-level resolved geometry with stair/elevator connections, use `oas-layout`.

## Key types

- Document metadata + `units` block (always `{ length: "mm", angle: "deg" }`)
- `Level` — abstract reference plane at an elevation; not a physical element
- `Room` — bounded space with a `boundary_polygon` and `usage`
- `Wall` — **straight** line segment with thickness separating spaces; carries `adjacent_rooms`
- `Opening` — door or window placed on a wall via `position_along_wall_mm`
- `CurtainWall` — glazed envelope; sibling of `Wall`, not a subtype
- `Roof` — sloped covering with `defines_slope` and `eave_overhang_mm`
- `FloorSlab` — the physical floor element (distinct from an abstract Level)
- `Furniture` — placed objects with position + rotation (formerly an extension, now in Core)
- `Railing` — barrier element; path may include optional `z` on stair runs
- `Annotation` — labels, dimensions, notes

## Critical rules

1. **Integer millimeters everywhere.** Every `_mm` field is an integer; angles use degrees. The only place decimals appear is derived `area_m2`.
2. **`type_name` on every entity.** This is the IFC-style stable classification (e.g. `IfcWall`, `IfcDoor`). Vendor-specific families (Revit, etc.) belong in the `oas-autodesk` extension, never inline here.
3. **Adjacency lives on the wall.** Encode room neighborhood via the wall's `adjacent_rooms` array — not on the room.
4. **CurtainWall ≠ subtype of Wall.** They are siblings (matches `IfcCurtainWall` vs `IfcWall`). Don't nest one inside the other.
5. **Openings reference walls by id.** `position_along_wall_mm` is measured along that wall's path; validate `position + width ≤ wall length` before emitting.

## Full schema

See [docs/core.md](../../../docs/core.md) for the complete field-by-field reference.

## Related skills

- `oas-geometry` — for the polygon, point, and unit conventions every Core entity inherits
- `oas-layout` — when Core entities are part of a fully resolved multi-level plan
- `oas-extensions` — for machinery, materials, Autodesk metadata, MEP, site
