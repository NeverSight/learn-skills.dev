---
name: openscad-iterative-modeling
description: Iteratively generate OpenSCAD (SCAD) code, render PNG previews, visually critique the result, and refine in a tight loop until the model matches. Use when the user asks to create a 3D model, design a part, make a bracket/enclosure/mount, render in OpenSCAD, export STL, or any request that can be expressed as parametric CSG geometry. Requires the OpenSCAD MCP server tools (render_scad_png, export_scad_stl).
license: MIT
metadata:
  author: Filipe Boldo
---

# OpenSCAD iterative modeling loop (SCAD → PNG → refine)

## When to Use This Skill

- The user asks to create, design, or model a 3D object (bracket, enclosure, mount, gear, etc.)
- The user sends a picture of an object and asks to recreate it in 3D
- The user wants to render or preview OpenSCAD code
- The user asks to export an STL file from a SCAD description
- Any request that can be expressed as parametric CSG geometry

## Prerequisites

### Required Tools

- **OpenSCAD MCP Server**: Required for rendering and exporting OpenSCAD geometry
  - Enables: `render_scad_png` (SCAD → PNG preview), `export_scad_stl` (SCAD → STL mesh)
  - Tool names may be namespaced by the host (e.g. `mcp_openscad-mcp-_render_scad_png`); match by suffix
  - Must be configured and running to render previews and export models

## Operating mode

- Prefer small, parametric SCAD with named variables.
- Each iteration: change **only** what the PNG critique indicates.
- After 3 render-refine cycles without convergence, stop and ask the user for clarification.

## Workflow

### 1. Normalize the request (minimal clarifications)

Extract and confirm only what you must to model correctly:

- **Units** (default to **mm** if unspecified)
- **Critical dimensions** (overall size, hole diameters, wall thickness)
- **Constraints** (must be printable? tolerance? symmetry? sharp vs filleted edges?)

If key dimensions are missing, ask 1–3 questions. Otherwise proceed with reasonable defaults and state them.

### 2. Draft SCAD code (first pass)

- Use `module` with named parameters.
- Center geometry at the origin when practical (`center=true`).
- Set `$fn` explicitly for curved parts (start with `$fn=64`).
- Ensure cutters in `difference()` extend beyond the body to avoid zero-thickness walls.

### 3. Render a PNG preview

Render with `cameraPreset="isometric"` first (`width=800`, `height=600`). If features are hard to judge, add orthographic views:

| Feature to verify                | Camera preset      |
| -------------------------------- | ------------------ |
| Plan-view layout, hole positions | `top`              |
| Heights, steps, lips, profiles   | `front` or `right` |
| Overall shape, proportions       | `isometric`        |
| Underside features               | `bottom`           |

### 4. Visually critique the PNG

Run through this checklist (in order of priority):

1. **Render valid?** — If blank/error, see §Render failures below.
2. **Overall proportions** — Does the bounding shape match the request?
3. **Feature presence** — Are all holes, cutouts, chamfers, and fillets visible?
4. **Placement & alignment** — Centered? Symmetric? Correct offsets?
5. **Orientation** — Is the part oriented for its intended use (e.g. printable flat side down)?

Write a one-line verdict per issue found, e.g.:

- "Through-hole is off-center by ~5 mm — shift `translate` X by +5."
- "Lip is too tall (6 mm → reduce to 2 mm)."

### 5. Refine SCAD code and repeat

Apply the smallest SCAD change that addresses the critique, then render again.

Stop when the PNG matches the user's intent and the user approves.

### 6. Export STL (only when ready)

Once approved, export the geometry:

- Choose a stable filename (e.g. `"bracket.stl"`).
- If the user wants multiple variants, export each with a distinct filename.

## Render failures

If a render returns blank or errors:

1. Simplify the SCAD to a minimal shape (e.g. a cube) to confirm the tool is working.
2. Re-add features one at a time, rendering after each addition, to isolate the problem.
3. Common causes: syntax error, `difference()` ordering, negative dimension, cutter not intersecting body.

## Example loop

User request: _"L-bracket, 40x30 mm base, 25 mm tall wall, 4 mm thick, two M4 countersunk mounting holes in the base."_

1. Draft SCAD:

```scad
$fn = 64;
t = 4; base_w = 40; base_d = 30; wall_h = 25;
hole_d = 4.3; csink_d = 8.5; csink_depth = 2.4;
hole_x = [10, 30]; hole_y = 15;

difference() {
  union() {
    cube([base_w, base_d, t]);                      // base
    translate([0, 0, 0]) cube([t, base_d, wall_h]);  // wall
  }
  for (x = hole_x) {
    translate([x, hole_y, -1]) cylinder(h = t + 2, d = hole_d);
    translate([x, hole_y, t - csink_depth]) cylinder(h = csink_depth + 1, d1 = hole_d, d2 = csink_d);
  }
}
```

2. Render `isometric` -> critique: wall is on the wrong edge; move to `x = base_w - t`.
3. Fix, render `top` -> holes look correctly spaced. Render `front` -> wall height correct.
4. User approves -> export STL.
