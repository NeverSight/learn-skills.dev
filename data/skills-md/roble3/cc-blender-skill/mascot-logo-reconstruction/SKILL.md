---
name: mascot-logo-reconstruction
description: Orchestrate a fail-gated, source-locked Blender reconstruction of mascots, logos, brand avatars, and stylized flat characters from wireframes, texture packs, and orthographic views. Use when the user requires a 1:1 brand/model match rather than a plausible stylized interpretation.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info mcp__blender__get_objects_summary mcp__blender__get_object_detail_summary mcp__blender__render_viewport_to_path mcp__blender__search_api_docs mcp__blender_official__execute_blender_code mcp__blender_official__get_objects_summary mcp__blender_official__get_object_detail_summary mcp__blender_official__render_viewport_to_path mcp__blender_official__search_api_docs
---


## MCP backend

Use when: Brand mascot/logo 3D reconstruction, exact part counts, texture-driven model matching, repeated “does not match reference” feedback, or full pipeline coordination across analysis, contour mesh, registration, UV fitting, validation, animation, and export.

Before the first Blender call, read [../text-to-blender/references/mcp-backends.md](../text-to-blender/references/mcp-backends.md). Prefer official MCP for shared capabilities; preserve the selected backend for the whole task. Tool names in recipes are client/legacy examples: map them through that reference and its agent-host guide.
# Mascot / Logo Reconstruction

This is the top-level skill for 1:1 brand mascot reconstruction. It chains the specialized skills and enforces stop/go gates.

## Harmonization requirement

For mascot/logo work, use `blender-skill-harmonizer` first when multiple source types or validation failures are present. It sets canonical source policy and prevents conflicts between reconstruction, UV, fit-repair, lighting, export, and animation skills.

## Skill chain

1. `reference-analysis-validator` — source inventory, manifest, part counts, masks.
2. `orthographic-registration` — shared front/side/back/top coordinate contract.
3. `contour-to-mesh` — structural meshes from measured silhouettes.
4. `atlas-uv-fitting` — per-part texture/UV fitting.
5. `blender-materials` / `blender-lighting` — only after geometry and UVs pass.
6. `reference-analysis-validator` again — overlay gates before export.
7. `blender-export` — export only after gates pass.
8. `blender-animation` — only after static model is accepted.

## Non-negotiable order

Static reference fidelity comes before animation and beauty rendering.

```
measure → manifest → contour meshes → depth registration → UV fit → overlay validation → export → animation
```

## Hard gates

- expected structural part count equals Blender scene/export structural part count.
- front silhouette overlay passes threshold.
- face/features landmarks pass tolerance.
- side/back/top renders match their registered envelopes.
- texture atlas regions are mapped per part.
- optional aura/background is separated from base structural GLB.

## Modeling guidance

- Treat mascots/logos as designed symbols, not natural objects. Symmetry is not guaranteed.
- Do not infer hidden leaves/petals from radial math.
- Avoid primitive-first construction when a silhouette exists.
- Use semantic object names and validation prints.

## Source-manifest structural part invariant

Create exactly the structural parts declared by the source manifest. Extra background arcs, glow, aura, shadows, guide marks, and decorative rings are context/decor unless the manifest explicitly promotes them to structural geometry.


## Front-plane rotation rule

In this Blender coordinate convention, the front camera looks along the Y axis and the reference silhouette lives in the X/Z plane. Therefore 2D rotations inside the front view are rotations around the **Y axis**, not around Z. Use `rotation_euler = (0, angle, 0)` for 2D component orientation in the front projection. Z rotation spins objects into/out of screen-space incorrectly for X/Z-plane meshes.

## Output contract

Every final reconstruction folder should include:

- `reference_manifest.json`
- `registration_report.json`
- `atlas_regions.json`
- `validation/front_mask_validation.json`
- `validation/front_overlay_reference.png`
- named `.blend`
- base `.glb`
- optional aura/context `.glb`
- `BUILD_NOTES.md` with pass/fail gates
