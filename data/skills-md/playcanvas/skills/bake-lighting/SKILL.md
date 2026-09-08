---
name: bake-lighting
description: Use when a PlayCanvas scene's static lighting, shadows, or ambient occlusion costs too much per frame, or lighting must ship precomputed for startup or payload budgets.
---

# Precompute static lighting

Static geometry lit by static lights can bake into lightmap textures once, removing per-frame
shadow-map rendering and per-pixel dynamic lighting for that light entirely.

## Engine `Lightmapper` flags

- Engine-only bootstraps must register it: `AppOptions.lightmapper = Lightmapper`. `Application`
  wires this by default; only a manual `AppOptions` assembly needs the explicit line.
- Per light: `light.bake = true`, then `light.affectDynamic = false` once every mesh it lights is
  lightmapped, so it stops contributing to the real-time pass.
- Per mesh: `render.lightmapped = true` — required for the mesh to receive any light once
  `affectDynamic` is false, a correctness requirement, not just an optimization —
  `render.lightmapSizeMultiplier` to size its lightmap, `render.castShadowsLightmap` so lightmapped
  meshes still shadow each other in the bake.
- Bake mode: `BAKE_COLOR` for flat diffuse materials; `BAKE_COLORDIR` adds a dominant-light-direction
  pass for normal- or specular-mapped materials that need one.
- Baked ambient occlusion, independent of any light: `scene.ambientBake` plus
  `ambientBakeNumSamples`, `ambientBakeOcclusionBrightness`/`OcclusionContrast`.
- Run `app.lightmapper.bake(null, mode)` once the scene exists; `null` bakes every lightmapped node.

## Verify UVs before trusting this on real assets

The installed `Lightmapper` bakes a node only when every mesh instance on it has a second UV set
(`mesh.vertexBuffer.format.hasUv1`). A node missing one is skipped silently — no warning, no
lightmap — and its mesh simply stays dynamically lit, which a glance at a screenshot will not catch.
Procedural primitives generate that set; imported GLB models often do not. Check `hasUv1` on every
mesh you expect to bake, and unwrap or re-export the ones without it before the bake. Do not carry a
primitive-only test result into production assets unchecked.

## Choose the rung by budget, not by default

On-device bake cost scales with baked-node count and lightmap resolution; measure it once on the
target device (`performance.now()` around `bake()`) and compare it with the startup budget before
choosing a rung. Stay on-device unless:

- the measured bake time does not fit the startup or first-paint budget on the target device, or
- the result needs stylized material detail beyond lighting that the runtime `Lightmapper` cannot
  produce.

Only then move to an offline bake shipped as assets, and size the pipeline to the scene count. For
one deterministic scene the whole pipeline is a build script that computes or renders the maps and
writes them next to the other static assets, plus a loader; that is sufficient. Registry-keyed
per-asset configs, worker-thread parallelism and a coverage audit that fails the bake on a missing
output belong to multi-asset pipelines — add them when the second scene arrives, not before.

Offline maps are payload. State the compressed size delta in the change description and compare it
with the download or package budget; a modest lightmap set can double the archive of a small web
app.

## Keep dynamic objects consistent

Whichever rung you use, dynamic objects moving through baked lighting must not read as ignoring it:
sample or approximate the baked occlusion/shadow field for them and their attachments so they dim to
the same levels as the static geometry around them, and ground them with a contact shadow. A
dynamic object whose custom shading must meet baked maps is `override-shader-chunks` territory.

## Prove it

Capture `verify-pixels`-style frames both in and out of the baked shadow, before and after the
change, and compare them. A screenshot glanced at once is not proof the bake reproduced the lighting
it removed.
