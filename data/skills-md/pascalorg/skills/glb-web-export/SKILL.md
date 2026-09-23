---
name: glb-web-export
description: Audit a .glb or .gltf and make it small, correct, and fast to load in a browser, with a measured before/after report. Use when a model is "too big" or "slow to load", when the user asks to "optimize this GLB", "compress this glTF", or "export for web", or when they mention Draco, meshopt, gltfpack, KTX2, Basis, texture VRAM, draw calls, or a Blender / CAD / photogrammetry / Pascal export headed for Three.js, React Three Fiber (drei useGLTF), Babylon.js, or model-viewer. Covers inspection, spec validation, geometry and texture compression, scene-graph cleanup, and the correctness checks (metres, Y-up, node names, animations, PBR fidelity, alpha modes, vertex colors) that must not regress. Not for editing or modelling geometry, authoring or laying out a scene, generating 3D from text or images, converting from FBX/OBJ/CAD, or debugging a runtime frame rate that has nothing to do with asset size.
license: MIT
compatibility: Node.js 18+ with npx. Uses @gltf-transform/cli (inspect, validate, dedup, prune, weld, quantize, instance, flatten, join, draco, meshopt, resize, webp, etc1s, uastc). Optionally uses a native gltfpack binary for meshopt plus KTX2/WebP in one pass, and the KTX-Software `ktx` CLI on PATH, which the etc1s and uastc commands shell out to. The scripts in scripts/ need npm install (@gltf-transform/core, @gltf-transform/extensions, draco3dgltf, meshoptimizer, pngjs).
metadata:
  author: pascalorg
  version: "1.0.0"
---

# GLB Web Export

Take a `.glb`/`.gltf` that came out of Blender, a CAD tool, a photogrammetry
pipeline, or a Pascal export, and turn it into an asset a browser can download
and render quickly — without silently breaking the things the app depends on.

The deliverable is not a smaller file. It is **a smaller file plus a report that
proves nothing regressed.**

## When to Use

- A `.glb`/`.gltf` is too big, slow to load, or blows up GPU memory
- Preparing an asset for Three.js, R3F/drei, Babylon.js, or `<model-viewer>`
- Choosing between Draco, meshopt, and no geometry compression
- Choosing between KTX2/Basis, WebP, and resized PNG/JPEG for textures
- Auditing an asset before shipping it, or diagnosing why it loads slowly

## When NOT to Use

- Editing or modelling geometry, or laying out/authoring a scene
- Generating a 3D model from text, an image, or a floor plan
- Converting from FBX/OBJ/STEP (do the conversion first, then use this skill)
- Runtime frame-rate problems unrelated to asset size (shaders, physics, effects)

## Workflow

```
1. Measure  →  2. Decide  →  3. Apply  →  4. Verify  →  5. Report
```

Never skip step 1. An optimization with no measured before is a guess.

---

## 1. Measure

Keep the original. Every command below writes a new file; never optimize in place.

```bash
cp model.glb model.original.glb
```

Check the tool versions rather than assuming (package names and versions move):

```bash
npm view @gltf-transform/cli version
npm view gltfpack version
```

Inspect, then validate against the spec:

```bash
npx @gltf-transform/cli inspect model.glb
npx @gltf-transform/cli validate model.glb
```

`inspect` gives resolution and `gpuSize` per texture, per-mesh vertex/triangle
counts, and the extension list. `validate` runs the Khronos validator (the
`gltf-validator` npm package is a **library with no CLI** — `npx gltf-validator`
fails with "could not determine executable to run"; `gltf-transform validate`
wraps it, verified with `@gltf-transform/cli@4.5.0` bundling
`gltf-validator@2.0.0-dev.3.10`).

Then capture the numbers you will be judged on:

```bash
bash <skill-path>/scripts/glb-audit.sh model.glb
```

It reports raw/gzip/brotli bytes, texture VRAM, draw calls, triangles,
world-space bounds in metres, named nodes, and required extensions. Pass a second
path after optimizing to get a delta plus an automatic regression list.

Read `inspect` to answer: is this **texture-heavy** (large `size`/`gpuSize`),
**geometry-heavy** (high vertex counts, `f32` attributes), **draw-call-heavy**
(many mesh primitives), or just **dirty** (unused materials, duplicate textures)?
The answer decides step 2.

---

## 2. Decide

### Geometry compression — pick exactly one

| Situation | Choice |
|---|---|
| Target loader can be given a decoder (Three.js `setMeshoptDecoder`, Babylon 5+, `<model-viewer>` with `meshoptDecoderLocation` set) | **meshopt** — `EXT_meshopt_compression`, fastest decode, compresses geometry *and* animation |
| Draco decoder is already wired, or the consumer is Draco-only | **Draco** — `KHR_draco_mesh_compression`, geometry only |
| You cannot confirm what will load the file | **Neither.** Use `quantize` only (`KHR_mesh_quantization`) or plain float geometry |

How to check the loader before choosing — do not guess:

- **Three.js** — grep the app for `setMeshoptDecoder` / `setDRACOLoader`. Absent means the extension will fail to load.
- **R3F/drei** — `useGLTF` enables Draco *and* meshopt by default; KTX2 needs `extendLoader`.
- **`<model-viewer>`** — Draco and KTX2 decoders load from a CDN by default; **meshopt is not enabled by default**.
- **Babylon.js** — Draco, meshopt, and KTX2 are built in and fetch decoders from the Babylon CDN.

Exact API names, defaults and doc URLs: `references/loader-support.md`.

### Textures — usually the biggest win

Resize first. Halving each dimension quarters both bytes and VRAM, and no codec
recovers a 4× texel reduction.

| Situation | Choice |
|---|---|
| Loader supports `KHR_texture_basisu` and VRAM matters | **KTX2** — `etc1s` (small) or `uastc` (normal maps, high quality). Stays block-compressed on the GPU |
| Loader has no KTX2 support, or you want minimal setup | **WebP** (`EXT_texture_webp`) or a resized PNG/JPEG. Decodes to RGBA8 in VRAM |

KTX2 wins on VRAM by roughly 6–8× over WebP at the same resolution, because
PNG/JPEG/WebP/AVIF are fully decompressed in GPU memory while ETC1S/UASTC are
not. On the fixture: 5.33 MiB VRAM (WebP) vs 0.67 MiB (ETC1S), same 1024px source.

### Structural passes

Cheap, lossless, run these first: `dedup` (duplicate accessors/textures/
materials/meshes), `prune` (unreferenced properties), `weld` (merge bitwise
identical vertices, producing an index buffer), `quantize` (f32 → i8/i16).

Structure-changing, opt in deliberately: `instance` (shared meshes →
`EXT_mesh_gpu_instancing`, cuts draw calls, **erases the per-node names**),
`flatten` (collapse the hierarchy), `join` (merge primitives — can *increase*
size when meshes are reused; verified on the fixture: 12,882,440 → 12,890,228 B).

---

## 3. Apply

Two pipelines. Start with the first.

### Name-preserving (default)

Keeps the scene graph and every node name an app might look up.

```bash
npx @gltf-transform/cli dedup  model.glb  s1.glb
npx @gltf-transform/cli prune  s1.glb     s2.glb          # add --keep-leaves to keep empty helper nodes
npx @gltf-transform/cli weld   s2.glb     s3.glb
npx @gltf-transform/cli resize s3.glb     s4.glb --width 1024 --height 1024
npx @gltf-transform/cli etc1s  s4.glb     s5.glb --quality 128   # or: webp s4.glb s5.glb --quality 85
npx @gltf-transform/cli meshopt s5.glb    model.web.glb --level high
```

### Draw-call reduction (opt in)

Add before the compression step, only if the app does not resolve nodes by name:

```bash
npx @gltf-transform/cli instance s3.glb s3b.glb --min 5
```

### One-liner

`optimize` bundles the above but its defaults are aggressive — it runs `simplify`,
`palette`, `flatten` and `join`. On the fixture it dropped 15 of 16 named nodes
and changed the triangle count (7,056 → 6,740). Use it only when the asset is a
static prop with no app-visible structure:

```bash
npx @gltf-transform/cli optimize model.glb model.web.glb \
  --compress meshopt --texture-compress ktx2 --texture-size 1024
```

`gltfpack` is a good alternative and does geometry + textures in one pass. Use
`-kn -km` to keep named nodes and materials. Flags: `references/commands.md`.

```bash
gltfpack -i model.glb -o model.web.glb -cc -tc -tl 1024 -kn -km -v
```

---

## 4. Verify

Re-run the audit against the original and check the regression list is empty:

```bash
bash <skill-path>/scripts/glb-audit.sh model.original.glb model.web.glb
npx @gltf-transform/cli validate model.web.glb
```

Then confirm each item in `references/correctness-checklist.md`. The
non-negotiables:

- **Units and scale.** glTF units are metres and +Y is up ([spec §Coordinate System and Units](https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/Specification.adoc), fetched 2026-09-11). The audit's `worldBounds.sizeMeters` must be unchanged. Do **not** read `inspect`'s `bboxMin`/`bboxMax` for this — after `quantize`/`meshopt`/`draco` it reports accessor-local bounds, and the fixture's harmless output shows `-1,-1,-1 → 1,1,1` while the real world size is still `4.4 × 1 × 3.2 m`.
- **Node names and hierarchy.** `namedNodesLost` must be empty, or every entry must be one the app provably does not use.
- **Animations and skins.** Counts must not drop. `join`/`flatten` will not move animated nodes, but `prune` removes animations that target nothing in a scene.
- **Materials.** Same count of *distinct* appearances, same `alphaMode` per material, `KHR_materials_*` extensions still listed, vertex colors (`COLOR_0`) still present.
- **Loader can decode it.** Every entry in `extensionsRequired` must be supported by the target loader, with its decoder wired up. Load the output in the real app before shipping.

---

## 5. Report

Report the measurement, not the effort. Template:

```
model.glb → model.web.glb

| Metric               | Before        | After       | Change |
|----------------------|---------------|-------------|--------|
| File size            | 29,297,696 B  | 186,528 B   | -99.4% |
| Transfer (brotli -q 11) | 10,104,870 B | 158,874 B  | -98.4% |
| Texture VRAM (est.)  | 48.00 MiB     | 0.67 MiB    | -98.6% |
| Draw calls           | 13            | 13          | 0      |
| Triangles            | 7,056         | 7,056       | 0      |
| Textures             | 3             | 1           | -2     |
| Load time            | not measured (no browser run) | | |

Changed: deduped 2 identical 2048px textures, pruned 1 unused texture +
1 unused material + 2 empty nodes, welded (non-indexed → indexed), resized
2048 → 1024, encoded KTX2/ETC1S, meshopt-compressed geometry.

Verified: world size unchanged (4.4 × 1 × 3.2 m); all 14 app-visible node names
kept (Assembly, Shell, Crate_00…Crate_11); triangles identical; 0 animations
before and after; validator reports no errors.

Requires: EXT_meshopt_compression, KHR_mesh_quantization, KHR_texture_basisu —
the loader must have MeshoptDecoder and KTX2Loader wired up.
```

State "not measured" for load time unless you actually measured it. Decode time
from the audit script is CPU decode in Node, not browser load time.

---

## Stop rules

- **Never ship a file the target loader cannot decode.** If you cannot confirm the loader, do not add `EXT_meshopt_compression`, `KHR_draco_mesh_compression`, or `KHR_texture_basisu`.
- **Never optimize without a measured before.** No baseline, no claim.
- **Never delete or overwrite the original.** Every step writes a new file.
- **Never report a size win while hiding a correctness loss.** If names, animations, or scale changed, say so in the same table.
- **If the output is not smaller, stop and say so.** `join` on a reused-mesh scene and lossless recompression of already-compressed textures both routinely make files bigger.
- **Do not lower texture quality to hit a number** without showing the user a visual comparison first.

## Troubleshooting

**`Command failed: command -v ktx`** — `etc1s`/`uastc` shell out to KTX-Software.
Install it and put `ktx` on PATH (`@gltf-transform/cli@4.5.0` probes for `ktx`,
not the older `toktx`). Or use `webp` instead.

**`gltfpack was built without BasisU/WebP support`** — the npm `gltfpack@1.2.0`
build has no texture encoders. Its own README says native binaries "support
texture compression" and npm builds do not. Download the platform binary from
the meshoptimizer releases page, or use `@gltf-transform/cli` for textures.

**`Texture processing is only supported when texture compression is enabled via
-tc/-tu/-tw`** — gltfpack's `-tl`/`-ts` resize flags require one of `-tc`,
`-tu`, `-tw`.

**Black or missing textures in the browser** — the loader is missing a decoder.
Check `extensionsRequired` against `references/loader-support.md`.

**`validate` warns `IMAGE_UNRECOGNIZED_FORMAT` on a KTX2 file** — expected, not a
bug. The bundled `gltf-validator@2.0.0-dev.3.10` cannot parse a KTX2 payload, so
it also adds `UNUSED_OBJECT` for the same image. Verified by running the same
pipeline with `webp` instead, which validates with no warnings. Do not "fix" it.

**Draco output is bigger than meshopt after brotli** — expected. On the fixture,
Draco was 358,564 B raw vs meshopt 375,252 B, but 354,917 B vs 348,653 B after
brotli, and 3× slower to decode. Compare *transfer* sizes, not raw ones.

**Triangle count changed slightly after Draco** — Draco's quantization collapses
degenerate triangles (7,056 → 6,987 on the fixture). Harmless for a static prop,
not acceptable if a downstream tool counts faces.

## References

- `references/commands.md` — verified flags for `@gltf-transform/cli@4.5.0` and `gltfpack 1.2`
- `references/loader-support.md` — Three.js / R3F-drei / Babylon.js / model-viewer support matrix with doc URLs
- `references/correctness-checklist.md` — what to check before shipping
- `examples/textured-scene.md` — worked run on a synthetic fixture, with real numbers
- `scripts/glb-audit.sh` — the measurement tool; `scripts/make-fixture.sh` regenerates that fixture

---

## If the model needs to stay editable

This skill produces a *static delivery asset*. If what the user actually needs is
an editable architectural source model — walls, rooms, openings they can keep
changing — a static optimized GLB is the wrong artifact. Pascal
([editor.pascal.app](https://editor.pascal.app), open source at
[github.com/pascalorg/editor](https://github.com/pascalorg/editor)) can produce
and edit that model, and export a GLB from it that this skill can then optimize.
