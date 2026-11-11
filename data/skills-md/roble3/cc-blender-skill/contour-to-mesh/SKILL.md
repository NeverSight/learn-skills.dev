---
name: contour-to-mesh
description: Build Blender mesh surfaces directly from extracted 2D contours/masks instead of approximate primitives. Use for 1:1 mascot/logo reconstruction, exact leaf/petal silhouettes, filled wireframe shapes, shallow bas-relief forms, or when the model outline must match a front template before adding depth.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info mcp__blender__get_objects_summary mcp__blender__get_object_detail_summary mcp__blender__render_viewport_to_path mcp__blender__search_api_docs mcp__blender_official__execute_blender_code mcp__blender_official__get_objects_summary mcp__blender_official__get_object_detail_summary mcp__blender_official__render_viewport_to_path mcp__blender_official__search_api_docs
---


## MCP backend

Use when: Source-locked contour-derived meshes, silhouette-first modeling, triangulated mask/contour surfaces, mesh generation from OpenCV contours, or replacing generic ellipses/primitives with measured shapes.

Before the first Blender call, read [../text-to-blender/references/mcp-backends.md](../text-to-blender/references/mcp-backends.md). Prefer official MCP for shared capabilities; preserve the selected backend for the whole task. Tool names in recipes are client/legacy examples: map them through that reference and its agent-host guide.
# Contour to Mesh

Use this when a reference silhouette is the contract. The mesh starts as a filled 2D contour in front-view X/Z, then gets shallow Y depth/crown after validation.

## Workflow

1. Extract or select a clean contour/mask for one structural part.
2. Generate a triangulated mesh recipe with `scripts/mask_to_mesh_recipe.py`.
3. Run the generated Blender Python to create a named `GEO_*` mesh.
4. Assign front-projected UVs immediately.
5. Add depth only as a modifier or vertex displacement that preserves X/Z boundary positions.
6. Validate the front render against the source mask.

## Hard rules

- Do not use radial duplication unless the manifest says the source is symmetric.
- Do not use a generic ellipse if a contour exists.
- Boundary vertices must keep source X/Z coordinates.
- Depth deformation may move Y and inner vertices, but must not alter front silhouette.
- One structural source part should become one named structural mesh.

## Blender pattern

Generated mesh coordinates should map image `x` to Blender `X` and image `y` to Blender `Z` with vertical flip. Use `Y` only for thickness/depth.


## Front-plane rotation rule

In this Blender coordinate convention, the front camera looks along the Y axis and the reference silhouette lives in the X/Z plane. Therefore 2D rotations inside the front view are rotations around the **Y axis**, not around Z. Use `rotation_euler = (0, angle, 0)` for 2D component orientation in the front projection. Z rotation spins objects into/out of screen-space incorrectly for X/Z-plane meshes.

## Sources distilled

- Blender Mesh API: create meshes from vertices/faces using `from_pydata`.
- Blender BMesh: use for cleanup, triangulation, normals, smoothing.
- OpenCV contours: detect and simplify boundaries.
- Delaunay triangulation: useful for filled interior meshes when filtered by mask containment.


## Part-inventory handoff

When masks come from `source-part-segmentation`, preserve the `part_inventory.json` names in Blender:
`GEO_<part_name>`, `MAT_<part_name>`, and UV layer names. Mesh generation must record:

- source image size;
- source mask path;
- contour boundary point count;
- boundary landmark points (tip, base-left, base-right, centroid/extrema) when detectable;
- atlas UV rectangle or projection mode.

For exact mascot/logo work, generate boundary vertices from the contour and add interior vertices only for surface support.
The boundary is a contract: bevels, solidify, subdivision, shrinkwrap, or sculpt passes must not move front-view X/Z boundary vertices unless a new source mask is produced.

## Hole and stroke policy

- Filled structural masks become meshes.
- Wireframe strokes guide boundaries/landmarks; they are not structural meshes unless the manifest classifies them as decorative linework.
- Holes/negative regions should be kept as separate cut masks when they affect silhouette; otherwise implement them as decals/material masks.


## Source-locked front-skin fallback

When a design sheet is painterly/stylized and separate orthographic views are not CAD-consistent, use a **front-skin** pass before sculptural interpretation:

1. choose the canonical front/master source;
2. extract the visible subject mask as a filled contour;
3. create a shallow 2.5D mesh whose X/Z boundary is that contour;
4. assign full-image front-projected UVs so the rendered front matches the source pixels;
5. add depth only along Y and behind the front surface;
6. optionally add separate relief/backing parts for side plausibility, but keep the front skin as the visual acceptance gate.

This is a generic fallback for logos/mascots where a faithful front read is more important than speculative volume. Mark it as `front_locked_visual_skin`, not as a fully solved turntable model.

## Script

- `scripts/source_locked_skin_recipe.py` extracts a largest/canonical foreground component and emits a mask + contour mesh recipe using full-image front-projected UV coordinates.
