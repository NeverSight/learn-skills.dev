---
name: reference-analysis-validator
description: Measure and validate supplied reference images, wireframes, texture atlases, and Blender renders before declaring a reconstruction 1:1. Use when an asset must match a template, when visual feedback says the output is off, when part counts must be exact, or before exporting a brand mascot/logo reconstruction. Pairs with reference-to-3d, contour-to-mesh, orthographic-registration, atlas-uv-fitting, and Blender MCP.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info mcp__blender__get_objects_summary mcp__blender__get_object_detail_summary mcp__blender__render_viewport_to_path mcp__blender__search_api_docs mcp__blender_official__execute_blender_code mcp__blender_official__get_objects_summary mcp__blender_official__get_object_detail_summary mcp__blender_official__render_viewport_to_path mcp__blender_official__search_api_docs
---


## MCP backend

Use when: Any 1:1 reference/model validation task involving masks, overlays, part counts, centroids, bounding boxes, SSIM/IoU, source manifests, or fail-before-export gates.

Before the first Blender call, read [../text-to-blender/references/mcp-backends.md](../text-to-blender/references/mcp-backends.md). Prefer official MCP for shared capabilities; preserve the selected backend for the whole task. Tool names in recipes are client/legacy examples: map them through that reference and its agent-host guide.
# Reference Analysis Validator

This skill converts “looks close” into measurable gates. For brand/logo/mascot work, **do not model or export until a source manifest and validation thresholds exist**.

## Required outputs

Create these in the asset output folder:

- `reference_manifest.json` — classified source files, expected parts, thresholds.
- `source_analysis/*.json` — image metadata, masks/components/landmarks.
- `validation/front_overlay_reference.png` — reference and render overlay.
- `validation/front_mask_validation.json` — IoU/SSIM/bbox/centroid report.

## Workflow

1. Classify sources: front, side, back, top, texture atlas, decals, maps, lightmap, aura/context.
2. Build/refresh `reference_manifest.json` with hard expected counts and view roles.
3. Extract masks/components from each source using `scripts/reference_manifest_compiler.py` or existing analyzers.
4. Render model from matching orthographic camera with reference planes hidden.
5. Compare reference mask vs render mask using `scripts/render_overlay_validator.py`.
6. Refuse final export if hard gates fail.

## Modality rule

Compare like with like. A wireframe edge mask compared against a shaded beauty render gives misleadingly low IoU. For hard gates, render a flat silhouette/matte pass from Blender or compare reference edges to render edges. Use `render_overlay_validator.py --reference-mode ... --render-mode ...` when the source and render need different mask extraction modes.

## Default validation gates

- primary structural part count: exact.
- front silhouette IoU: target >= 0.90 for rigid/logotype shapes; >= 0.82 acceptable for first mascot reconstruction pass.
- bbox center drift: <= 12 px at 1024 px validation size.
- bbox size drift: <= 3% of image dimension.
- face/eye/smile landmark drift: <= 2% of image dimension when landmarks are defined.

## Failure policy

If a repeated mismatch occurs, record the measured failure, then route to the missing specialty skill:

- wrong silhouette → `contour-to-mesh`
- wrong depth/side/back → `orthographic-registration`
- wrong textures → `atlas-uv-fitting`
- wrong whole workflow → `mascot-logo-reconstruction`

## Read when needed

- `references/metrics-and-thresholds.md` for metric definitions and recommended gates.

## Sources distilled

Official/library docs to prefer while extending this skill:

- OpenCV contour features: moments, area, perimeter, bounding rectangles.
- OpenCV shape matching / Hu moments.
- OpenCV homography and geometric transforms.
- scikit-image SSIM for perceptual comparison.
