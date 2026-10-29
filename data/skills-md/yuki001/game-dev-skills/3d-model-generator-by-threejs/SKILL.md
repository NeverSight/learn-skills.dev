---
name: 3d-model-generator-by-threejs
description: Generate procedural 3D models from natural-language requests by writing a constrained buildModel(ctx) module that uses Three.js, bundled builders and helpers, deterministic validation and export scripts, PNG previews, and optional browser visual review. Use when needs to create, revise, export, or visually audit programmatic 3D assets in GLB, glTF, OBJ, or STL without Blender or another DCC tool.
---

# 3D Model Generator by Three.js

Generate model-specific JavaScript while keeping model construction helpers, validation, export, and review deterministic and reusable.

## Workflow

1. Choose a task output directory outside this skill.
2. Run `node scripts/init-model-task.mjs --out <task-dir>` to copy the build-module template without overwriting existing work.
3. Read `references/build-contract.md`. Read `references/builder-api.md` before using bundled builders or helpers. Read `references/export-formats.md` before choosing formats.
4. Edit only `<task-dir>/model-build.mjs`. Export one `buildModel(ctx)` function and keep it deterministic.
5. Install the pinned runtime once with `npm ci --prefix scripts`.
6. Build, validate, and export:

   ```text
   node scripts/build-and-export.mjs --build <task-dir>/model-build.mjs --out <task-dir> --formats glb,obj,stl
   ```

7. Inspect `<task-dir>/validation.json`. Fix every error and evaluate warnings that affect the requested formats.
8. Render a deterministic PNG preview of the exported artifact:

   ```text
   node scripts/render-preview.mjs --model <task-dir>/model.glb --out <task-dir>/preview.png --views iso,front,top
   ```

   Read `references/preview-rendering.md` for supported formats, views, and rendering limitations.
9. When interactive visual review is useful, run:

   ```text
   node scripts/serve-viewer.mjs --artifact-dir <task-dir> --model model.glb
   ```

   Open the printed local URL with an available browser tool. Review the exported artifact, not only the source scene. Use `--source model-build.mjs` when source-scene comparison is needed.
10. Iterate by modifying only `model-build.mjs`, rebuilding, and reviewing again.

## Build Rules

- Return a `THREE.Object3D` or `{ root, animations, metadata }`.
- Use `ctx.builders` and `ctx.helpers` for common construction. Use `ctx.THREE` directly for custom geometry.
- Do not import modules from generated build code. Do not access files, processes, environment variables, network APIs, dynamic imports, `eval`, or `Function`.
- Use `ctx.rng` instead of `Math.random()` so revisions are reproducible.
- Treat Y as up and meters as the default unit unless the request requires otherwise.
- Prefer `MeshStandardMaterial`, `MeshPhysicalMaterial`, or bundled material presets for GLB.
- Keep textures out of the default Node export path. Texture encoding requires a browser or a separate image-capable runtime.
- Set meaningful node names and organize multipart assets under groups.
- Keep triangle counts proportional to the requested use case. Use lower segment counts for distant or mobile assets.

## Validation and Review

Run numeric validation before visual review. The validator checks finite transforms and vertices, empty geometry, normals, bounds, counts, unsupported shader materials, textures, and configured limits.

For visual review, inspect:

- silhouette and recognizable shape;
- relative scale and proportions;
- symmetry, alignment, grounding, and unintended intersections;
- front, rear, side, top, and perspective views;
- material separation and final-format fidelity;
- wireframe density when topology matters.

Prefer round-trip review of GLB, OBJ, or STL. Source mode can look correct even when export loses hierarchy, materials, transforms, or animations.

## Completion Criteria

Complete a model task only when:

- the build module runs without forbidden capabilities;
- validation contains no errors;
- every requested file exists and is non-empty;
- exported-file review is satisfactory when browser review is available;
- the build is reproducible with the recorded seed;
- generated source and artifacts remain outside this skill directory.

## Resources

- `scripts/runtime/`: Stable build context, builders, helpers, seeded RNG, source checks, and scene validation.
- `scripts/exporters/`: Format-specific GLB/glTF, OBJ, and STL exporters.
- `scripts/build-and-export.mjs`: Main deterministic pipeline.
- `scripts/render-preview.mjs`: Standalone exported-model PNG renderer.
- `scripts/serve-viewer.mjs`: Local source and round-trip viewer server.
- `assets/model-build.template.mjs`: Generated-task starting point.
- `assets/viewer/`: Browser review application.
- `references/build-contract.md`: Generated module contract and safety rules.
- `references/builder-api.md`: Builder and helper API.
- `references/export-formats.md`: Format capabilities and limitations.
- `references/preview-rendering.md`: Standalone preview command and limitations.
