---
name: override-shader-chunks
description: Use when a PlayCanvas StandardMaterial needs custom shading its properties cannot express — procedural or stylized looks, custom vertex displacement, per-material screen effects — before writing a standalone shader from scratch.
---

# Override shading through chunks

A `StandardMaterial`'s shader is assembled from named chunks (lighting, combine, transform, and
more). Overriding one keeps the rest of the pipeline — fog, tonemapping, shadows, skinning,
instancing — intact. Reach for a fully custom `ShaderMaterial` only when the look needs a stage the
chunk system does not expose at all (its own vertex/fragment pair and attribute layout); a chunk
override is the default for everything else, since it is cheaper and stays integrated.

## Pin the version, read the source

Set `material.shaderChunksVersion` to the installed engine's major.minor (for example `'2.22'`)
before shipping any override. Chunk names and their contracts — what a chunk defines, what globals
it reads or writes — are version-keyed and change between releases. Read the installed `playcanvas`
source for the exact chunk being touched; do not recall its contract from memory or an older
version's documentation.

## Clone before overriding a shared material

Clone a material that other mesh instances share — including default and asset-imported materials —
before changing its chunks, properties, or material-level parameters for only some meshes, and assign
the clone. For per-mesh uniforms, use `meshInstance.setParameter()` without cloning the material.

## Set chunks through the documented accessor

Use `material.getShaderChunks(SHADERLANGUAGE_GLSL).set(name, source)`, and the WGSL equivalent —
the public, documented method — not the underlying `shaderChunks` maps, which are internal. Call
`material.update()` after any change so cached shader variants are cleared.

## Emissive-only overrides

An `emissivePS` override implements `void getEmission()`, writing the result into `dEmission`. When
the override is meant to fully drive the visible color, zero the material's `diffuse`/`specular` and
disable `useSkybox` so no other lighting term still contributes underneath it.

## Uniforms are raw

`setParameter` uploads exactly what it is given, with no color-space conversion. Convert any
authored sRGB color with `Color#linear()` before calling `setParameter`; an sRGB color passed
straight through renders visibly darker and less saturated than it was authored.

## Keep vertex chunks instancing-aware

A custom `transformCoreVS` (or any vertex chunk reading the model matrix) must keep the engine's
`INSTANCING` define path — pulling the per-instance matrix under that define — with a
non-instanced fallback that uses `matrix_model` directly, matching the stock chunk's structure.
Dropping this path silently breaks instancing for any mesh instance using the material.

## Provide GLSL and WGSL, or pin to WebGL

Override both `SHADERLANGUAGE_GLSL` and `SHADERLANGUAGE_WGSL` chunks for anything touched. On a
WebGPU device, a chunk supplied only in GLSL forces the material's entire shader — not just that
chunk — onto a GLSL-compiled-then-transpiled path; without the optional transpiler modules loaded
(the common case), that shader fails to compile. Supply both languages, or explicitly pin the
graphics device to WebGL if WGSL support is not required.

## Expand bounds for vertex displacement

If the override displaces vertices, expand the mesh's bounds by the maximum displacement (see
`apply-conventions`) — CPU-computed bounds never observe shader-side deformation, so culling breaks
silently otherwise.
