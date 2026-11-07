---
name: oas-layout
description: Use when producing or editing fully resolved OAS-Layout JSON — multi-level plans with levels, rooms, walls, openings, slabs, roofs, furniture, railings, and inter-level connections.
---

# OAS Layout

## When to use

Use this skill whenever the task is "give me the resolved plan" — concrete polygons, walls with coordinates, openings placed on walls, multiple levels, stairs/elevators connecting levels. If you're only authoring single-level core entities without level/connection scaffolding, `oas-core` may be enough. If the task is intent-only (no geometry), use `oas-program`.

## Key entities (top-level arrays in a Layout document)

- `levels` — abstract reference planes (`id`, `name`, `elevation_mm`, optional `is_building_story`)
- `rooms`, `walls`, `openings`, `curtain_walls`, `roofs`, `floor_slabs`, `furniture`, `railings` — Core entities, each with optional `level` reference
- `connections` — inter-room circulation graph: `{ from, to, type }` where `type` is `direct` | `through` | `single_access`
- `metadata` — optional provenance (`generated_by`, `timestamp`, `notes`)

## Critical rules

1. **Walls are straight line segments**, defined by `from`/`to` points only — not polylines. For a bent wall, emit multiple wall entities.
2. **Validate opening placement against wall length.** `position_along_wall_mm ≥ 0` and `position_along_wall_mm + width_mm ≤ Euclidean distance between wall.from and wall.to`.
3. **`Level` is abstract; `FloorSlab` is physical.** Level is the reference plane (`elevation_mm`); FloorSlab is the construction. A single Level can have multiple slabs (split-level designs).
4. **`Connection` is a room-to-room graph, not a vertical traversal.** Types are `direct` (shared doorway), `through` (passes through other rooms), `single_access` (room only reachable via one neighbor). Vertical movement between levels is modeled via openings + level refs on the room/opening, not a special connection type.
5. **Non-rectangular wall tops use `top_profile_points`.** Each entry is `{ "t": 0..1, "z_mm": int }` where `t` is the **parametric position along the wall**, not an absolute coordinate.
6. **Roof arrays must align with the boundary polygon.** `slope_angles`, `defines_slope`, and `eave_overhang_mm` must each have exactly as many entries as the polygon has points. Edges where `defines_slope` is `false` are gables.
7. **Openings reference `in_wall` *or* `in_curtain_wall`, never both.** Curtain wall panels (`IfcPlate`) are not openings — only doors/windows are.

## Full schema

See [docs/layout.md](../../../docs/layout.md) for the complete reference — the largest module in OAS, covering levels, all entity placements, and connection semantics.

## Related skills

- `oas-core` — the entity vocabulary Layout reuses and scopes to levels
- `oas-geometry` — for polygon, wall-path, and angle conventions
- `oas-program` — the upstream intent a Layout is meant to satisfy
- `oas-render` — to visualize the resolved Layout
- `oas-extensions` — for machinery, materials, Autodesk metadata attached to Layout entities
