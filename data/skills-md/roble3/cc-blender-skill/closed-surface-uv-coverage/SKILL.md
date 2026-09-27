---
name: closed-surface-uv-coverage
description: Ensure textures and decals cover all visible surfaces of a closed or extruded Blender asset, especially front/back caps and sidewalls, instead of relying on partial projected planes, curves, or linework overlays. Use when back textures do not fill the model, side textures are missing, spin/turntable views expose plain sidewalls, or a model needs separate UV treatment for caps and side surfaces.
when_to_use: Full surface texture coverage, sidewall UVs, back cap UVs, closed mesh UV coverage audits, texture fill validation, side/back turntable QA, replacing projected overlays with real surface materials.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_object_info mcp__blender__get_scene_info
---

# Closed Surface UV Coverage

This skill prevents a common false pass: a model looks textured from the front because it has a projected front image or curve overlays, but the closed surface has untextured back caps or plain sidewalls when viewed in a spin/turntable.

## Failure modes to catch

- Back detail is only a floating plane or curve overlay, not a material/UV on the back surface.
- Sidewalls have procedural color only; no side UV island, generated/object coordinate material, or baked strip.
- A back projection covers only a center shape and leaves the actual silhouette/back mesh plain.
- Side/back QA uses front-biased frames and misses edge-on/back-on samples.
- Decorative HUD/aura is mistaken for surface texture coverage.

## Required surface taxonomy

For extruded/logo-like assets, classify visible surfaces before look-dev:

1. `front_cap` — canonical front texture/decal.
2. `back_cap` — back texture, back linework, or baked/procedural fill mapped to the real back cap.
3. `sidewall` — depth surface connecting front/back, with its own UV parameterization or procedural material.
4. `overlay_context` — HUD/aura/circles; never counted as model surface coverage.

## Workflow

1. **Audit current coverage**: list mesh material slots, UV layers, image texture nodes, and face counts for front/back/side material indices.
2. **Reject overlay-only fixes**: curves/planes may add rim accents, but they do not satisfy back/side fill unless the mesh surface beneath is also textured/materialized.
3. **Create per-surface UVs**:
   - front/back caps: project local X/Z to UV 0–1 or map into a back/front atlas rectangle;
   - sidewall: map perimeter arc length to U and depth/front-back coordinate to V;
   - if a clean side texture is unavailable, use a generated procedural side material plus baked glow/edge strip and document it.
4. **Assign true surface materials**: back cap and sidewall mesh faces must have material nodes, active UVs, and/or generated coordinates. Optional curves are accents only.
5. **Validate turntable frames**: sample front, 45°, side/edge-on, back-on, opposite 45°, and rest. Back and side frames must show surface fill, not just outlines.

## Acceptance gates

- Back cap mesh faces have either an image/procedural material with a declared UV/generated coordinate policy, not only separate curves.
- Sidewall mesh faces have a sidewall material with UV/generated coordinates and visible depth treatment.
- Overlay/context collections are excluded from coverage counts.
- QA contact sheet includes back and edge-on frames.
- A `surface_coverage_report.json` states which surfaces are image-textured, procedural, baked, or intentionally plain.

## Handoff

Use after geometry is locked and before final material/look/animation acceptance. It complements `blender-uv-texturing` and `atlas-uv-fitting`: those skills explain UV/material setup; this skill enforces complete visible-surface coverage.

## Script

- `scripts/surface_texture_coverage_audit.py` audits selected mesh objects for UV layers, material image nodes, face material counts, and overlay-only warning patterns.
