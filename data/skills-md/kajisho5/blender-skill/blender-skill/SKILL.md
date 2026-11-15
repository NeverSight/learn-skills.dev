---
name: blender-skill
description: 'Inspect, convert, optimize, render, bake and validate 3D assets with local, headless Blender: glb/gltf, fbx, obj, stl, usd/usdz, ply, abc, .blend. Cut triangle count, cap texture resolution, bake AO/normal/roughness/diffuse/combined maps, render a thumbnail/turntable/4-view sheet, check a file against three.js/Unity/Unreal/Godot/iOS-AR/Android-AR/WebXR/3D-print/Sketchfab budgets, assemble a multi-asset scene. Use this skill whenever the user mentions a 3D model or asset file (glb, gltf, fbx, obj, stl, usd, usdz, ply, blend), a mesh, polycount/triangle count, UV, texture baking, decimation, a turntable render, an AR/game-engine import, or asks to check/optimize/convert/render something "for Unity", "for Unreal", "for the web", "for AR" -- even when they do not say "Blender". Headless only (`blender -b`); this is not a replacement for interactive modeling or the official Blender MCP add-on, and complements rather than competes with it. Requires Blender 4.2+ on the machine; no API keys, no cloud, no pip dependencies.'
version: 0.31.0  # x-release-please-version
---

# blender-skill

Scripts live in `scripts/` next to this file; run them with `python3 <skill-dir>/scripts/<name>.py`.
Each is a thin host-side CLI (stdlib only) that launches Blender headless
(`blender -b --factory-startup --python scripts/bpy/<name>.py -- args.json result.json`) and
reads back a JSON result written to disk -- never by parsing Blender's own log output. `--help`
on the script you are about to run is the cheapest full flag list; `references/pitfalls.md` is
the long form of real gotchas hit building this (GPU-offscreen limits under `-b`, format
roundtrip quirks, an Eevee engine-name rename between Blender versions) -- read it when
something behaves unexpectedly rather than guessing.

Shared flags, on every script: `--json` (structured result instead of a one-line summary --
prefer it for anything you'll act on programmatically); `--blender PATH` (override Blender
discovery: `--blender` > `$BLENDER` > `PATH` > the OS's usual install location); `--timeout
SECONDS` (default 1800). Writing tools also take `--dry-run` (prints the Blender command and
bpy script that would run, without running it) and `--fast` (lower-quality/fewer-samples
preview).

## Workflow (always follow this order)

0. **Never assume Blender is installed.** A script fails with `kind: missing_tool` and an
   install hint per OS if it can't find one -- report that, don't guess a path.
1. **Probe before you operate.** Run `info.py` on every input you plan to change: object/mesh/
   material/texture/animation counts, unit scale, bounding box, non-manifold-edge and UV
   presence. It welds a scratch copy of each mesh before checking manifoldness, so a perfectly
   normal hard-edged/UV-seamed asset isn't misreported as broken (`references/pitfalls.md`).
   Plan from these real numbers, never assumptions about what a file "probably" contains.
2. **Operate with the narrowest tool for the job.** A pure format swap is `convert.py`, not
   `optimize.py` with no flags. Chain tools when the user's request genuinely needs more than
   one (e.g. decimate, then bake, then check).
3. **Verify, don't assume, that a conversion is faithful.** `convert.py --verify` re-imports the
   output and diffs object/triangle/vertex/material/animation counts against the input. A diff
   is not automatically a bug -- STL has no shared-vertex index buffer at all (a cube: 24 -> 36
   vertices is inherent to the format, not a defect) -- but report what changed rather than
   silently trusting the conversion.
4. **Check the deliverable against where it's going.** `check.py FILE --target NAME` (three.js,
   unity, unreal, godot, ios-ar, android-ar, webxr, 3d-print, sketchfab) PASS/WARN/FAILs against
   this tool's own conservative budgets (not each platform's official published numbers, which
   are unpublished or change over time -- treat a WARN as "worth checking against that target's
   current docs"), and every row that can be fixed mechanically names the exact fix command.
5. **Look at the picture whenever the geometry or texture changed.** `look.py --wireframe` (a
   real render with every mesh shown as wireframe), `--textures` (a grid of every texture in the
   file), `--compare BEFORE AFTER` (two renders side by side, plus a PSNR/SSIM score when they
   share pixel dimensions -- render the same file/camera before and after an `optimize.py` pass
   to quantify how much a decimation or texture-resize actually changed the picture, not just the
   triangle/byte counts), `--uv` (UV layout as SVG -- headless Blender's PNG UV export needs a GPU
   offscreen context that `-b` doesn't have; SVG is the only mode this uses, deliberately, not a
   limitation to work around). A probe cannot see whether a decimated mesh still reads correctly,
   or a baked texture landed where expected.
6. **Report exact numbers**, not vibes: triangle/vertex counts before and after, texture
   dimensions, PASS/WARN/FAIL rows, `bake.py`'s pixel min/max/mean (a bake is mostly outside-UV
   black background with real data concentrated in a comparatively small island -- verify with
   those numbers, not by eyeballing a thumbnail at small size).
7. **Never overwrite the user's original file.** Every script writes a new output
   (`<input>_<operation>.<ext>` by convention, or wherever `-o`/`--out` points); nothing here
   mutates an input in place.

## Request → script

| Script | Does |
|---|---|
| `info.py FILE [--skip-uv-overlap-check]` | Object/mesh/material/texture/animation/armature counts, unit scale, bounding box, non-manifold-edge and duplicate-vertex detection, approximate self-intersection detection, flipped-normal detection (skipped, not guessed, when non-manifold edges make it unreliable), unapplied-scale detection, origin offset from bbox center/bottom-center (data, not a defect), UV out-of-bounds/zero-area/overlap detection (out-of-bounds and overlap are data, not defects; zero-area is a real "never unwrapped" defect; `--skip-uv-overlap-check` skips only the overlap scan's own uncapped O(n^2) candidate-pair loop -- confirmed it didn't finish within 20s on a real 105,600-triangle UV-mapped mesh; `check.py`/`fit.py` already pass this internally, since neither reads the overlap count), vertex color layers and other genuinely custom mesh attributes, per-clip bone count and root-motion detection (root bone's `location` channel actually moving, not just any bone animated), bone hierarchy and unweighted-vertex detection on skinned meshes (a vertex with no bone weight, skipped rather than flagged on meshes with no armature modifier at all), default LOD1/2/3 ratio suggestions from the current total triangle count, a draw-call estimate (one per distinct material actually used, not materials x objects), misconfigured-transparency detection (a binary alpha mask using real blending instead of dithered mode), misconfigured-texture-colorspace detection (Base Color/Emission not tagged `sRGB`, or Metallic/Roughness/Alpha/a normal map's own texture not tagged `Non-Color`), glb/gltf `extensionsUsed`/`extensionsRequired` read from the file's own JSON (Blender's importer doesn't expose this), duplicate-mesh/instancing detection (already-shared datablocks reported as data, identical geometry on separate datablocks flagged as a memory-saving opportunity), `.obj`'s referenced `.mtl` Phong parameters plus Blender's own confirmed Ns->roughness heuristic (metallic never guessed -- OBJ/MTL has no metallic channel), ray-cast wall-thickness analysis (per-object minimum, in the mesh's own local units), point-cloud detection (`is_point_cloud`, skips the meaningless no-UV-map warning). The foundation every other script leans on. |
| `convert.py FILE -o OUT [--verify] [--up-axis {X,Y,Z,-X,-Y,-Z}] [--forward-axis {X,Y,Z,-X,-Y,-Z}]` | Cross-format conversion: glb/gltf, fbx, obj, stl, usd, usdz, ply, abc, .blend; explicit coordinate-system conversion for the output (glTF: up-axis Y/Z only, no forward-axis; ABC/.blend: unsupported). |
| `split.py FILE --out-dir DIR [--format FMT]` | Split one multi-object file into one output file per independent object hierarchy (a root object plus every descendant it has -- a skinned mesh and its armature stay together; an unrelated standalone object becomes its own file). |
| `anim.py FILE --extract [--action NAME] -o OUT` / `anim.py FILE --combine ANIM_FILE... -o OUT` | Extract animation-only data (armature + actions, no mesh) from a rigged file, or combine several files' actions (matched by bone name) onto one base character in a single output with every action as its own clip -- a Mixamo-style workflow. `--combine` supports glTF/glb and FBX output only. |
| `lod.py FILE --out-dir DIR [--target-triangles N \| --ratios R1,R2,R3] [--format FMT]` | Batch-generate LOD0 (unmodified original) through LOD3, one output file per level, at the default 50%/25%/10% ratios (matching `info.py`'s own LOD suggestions) or an absolute `--target-triangles` for LOD1 with LOD2/LOD3 auto-scaled. |
| `optimize.py FILE -o OUT [--decimate-ratio R] [--weld-doubles] [--clean-mesh] [--vertex-cache-report] [--fill-holes] [--fix-scale] [--origin center\|bottom\|keep] [--recalc-normals] [--triangulate] [--texture-max PX\|--texture-auto-resolution [--viewport-width PX]] [--purge-unused] [--point-thin-voxel SIZE] [--webp] [--webp-quality N] [--fix-colorspace\|--texture-colorspace NAME] [--remove-unused-bones] [--max-bones N] [--keyframe-decimate TOLERANCE] [--remove-unused-shape-keys] [--instance-duplicate-meshes] [--merge-materials] [--target-web\|--target-mobile\|--target-ar\|--target-sketchfab\|--target-vrchat\|--target-roblox\|--target-gltf-viewer\|--target-quicklook] [--draco\|--meshopt] [--ktx2] [--generate-mipmaps DIR] [--flip-normal-map-green]` | Shrink triangle count, texture size, and orphan data; `--clean-mesh` removes orphan/loose vertices (touching no face at all) and degenerate (zero-area) faces from every mesh object, no-op on a point cloud, runs first so a decimate ratio/triangle budget is derived from a count that excludes dead geometry; `--vertex-cache-report` reports each mesh's ACMR (Average Cache Miss Ratio, a FIFO 32-entry vertex-cache simulation over the current triangle order; 3.0 is the real worst case, 0.5 a common target for a large closed mesh but not a universal floor; a zero-triangle mesh reports `null` in `--json`, `n/a` in text output) before and after this run's own topology changes -- reports only, does not reorder; use `--meshopt` (gltf-transform's `reorder`) for the actual cache-aware reordering; fill boundary-edge holes; bake unapplied scale into the mesh; recenter an object's origin without moving its geometry; thin a point cloud by voxel-grid downsampling (no-op on a mesh with faces); convert textures to WebP (glb/gltf only, reports real measured before/after bytes -- not always smaller, see pitfalls.md); `--texture-auto-resolution` computes each texture's own cap from how much of the file's combined bounding box its largest user object spans, instead of one flat `--texture-max`; `--fix-colorspace` corrects a texture's colorspace tag per the material socket it feeds (info.py flags the mismatch), `--texture-colorspace NAME` forces every texture to one named colorspace instead (e.g. `ACEScg` for an ACES-aware pipeline); `--remove-unused-bones` prunes zero-weight, unanimated bones from the leaves inward; `--max-bones N` caps an armature's bone count (a real mobile bone budget), removing the lowest-influence unanimated leaves first and reassigning their skin weight to the parent, never touching an animated bone; `--keyframe-decimate TOLERANCE` reduces every action's keyframe count via Ramer-Douglas-Peucker curve simplification, exact for LINEAR/CONSTANT-interpolated segments only (a keyframe is dropped only if its real post-removal value would deviate by at most TOLERANCE, in that fcurve's own units; a BEZIER-governed keyframe is never touched -- see pitfalls.md; a glTF import is exclusively LINEAR; the first/last keyframe of every fcurve always survives); `--remove-unused-shape-keys` removes every non-Basis shape key whose max per-vertex displacement from what it's actually defined relative to (usually Basis, but can chain to another shape key) is below a tiny fixed epsilon -- geometrically a no-op regardless of value/mute/drivers, resolving multi-level dead chains via Blender's own automatic relative_key re-pointing; `--instance-duplicate-meshes` merges every group of mesh objects on separate datablocks that are fully identical within a tight floating-point tolerance (vertex positions, face topology/material_index/use_smooth, sharp-face/sharp-edge marks, UV layer names+active-render+coordinates, color attribute names+render fallback+values, and the exact same Material datablocks -- stricter than info.py's own loose duplicate_mesh_candidates suggestion; never a mesh with custom split normals) onto one shared datablock, never touching a mesh with shape keys or an Armature modifier, or any datablock shared with such a mesh (shared mesh data means shared shape-key/vertex-weight state in Blender's own data model); `--merge-materials` merges every group of separate Material datablocks that are fully identical (every non-identity RNA property, plus -- when use_nodes is on -- true node-tree structural equality: same node types/settings/socket values matched by node name, and the exact same links; an ID reference inside the graph such as an Image Texture's `.image` compares by datablock identity, not pixel content) onto one canonical datablock, redirecting every real reference to a duplicate via Blender's own `ID.user_remap` (every data-block's material slot and every per-object slot override, not a hand-enumerated walk that could miss a user type such as a Curve's own `.materials`) before freeing it; `--target-sketchfab`/`--target-vrchat`/`--target-roblox`/`--target-gltf-viewer`/`--target-quicklook` extend the `--target-web`/`--target-mobile`/`--target-ar` presets, each citing its source in `PRESETS`' own comment (VRChat's official PC "Good" Performance Rank 70,000-triangle threshold, Roblox's official 20,000-triangle-per-mesh/1024px texture caps, Apple's own AR Quick Look guidance); a preset with a real *absolute* platform triangle cap converts it into an actual decimate ratio from the file's own pre-decimate triangle count at run time (never a fixed fraction that can't guarantee compliance for an arbitrary input size), a no-op when already within budget; `--draco`/`--meshopt`/`--ktx2` delegate to gltf-transform (and, for `--ktx2`, the KTX-Software `ktx` CLI) if installed, otherwise say so and skip just that step; `--generate-mipmaps DIR` pre-generates the full mip chain (level 0 = this run's own final texture size after any `--texture-max`/`--texture-auto-resolution` resize, each level independently halved per dimension down to 1x1) as separate PNG files under `DIR` for every texture a mesh object's material actually references, using Blender's own `Image.scale()` (a real box/bilinear filter, confirmed against a checkerboard pattern -- not nearest-neighbor), on a throwaway copy that never touches the texture still referenced by this run's own export; for a pipeline that needs mips as loose files rather than runtime-generated or KTX2-embedded (`--ktx2` already embeds its own generated mip chain); `--flip-normal-map-green` inverts the green (Y) channel of every texture genuinely wired as a tangent-space normal map (Image Texture -> Normal Map node -> a material's Normal input) -- the complete, sole pixel operation to convert between OpenGL (+Y) and DirectX (-Y) convention (R/X and B/Z untouched). Does not auto-detect which convention a normal map is currently in -- no reliable general-case, pixel-only method exists (confirmed: even Substance 3D Painter can't do it without an explicit tag; Unity holds a patent for a statistical heuristic with no published reliability figures); glTF's own spec mandates OpenGL, Unity/Godot expect OpenGL, Unreal expects DirectX -- each engine's own importer exposes only a manual flip toggle, never auto-detection, which this mirrors. `--recalc-normals` warns rather than trusting itself on a still-non-manifold mesh -- fix holes first. |
| `render.py FILE -o OUT [--turntable] [--sheet] [--cycles] [--light studio\|outdoor] [--transparent] [--resolution-preset thumbnail\|square\|720p\|1080p\|4k\|vertical] [--resolution W H]` | Thumbnail (default), 360° turntable (PNG sequence or FFmpeg-encoded video), or a 4-view sheet. `--resolution-preset` sets the frame size (each tile's, for `--sheet`): `1080p` 1920x1080, `4k` 3840x2160 (UHD), `vertical` 1080x1920 (9:16), `square` 1080x1080, `720p` 1280x720, `thumbnail` 512x512 (the default); an explicit `--resolution W H` wins over a preset; an unknown name is an `input` error listing the valid ones; the result's `resolution` block says which size was used and why (`source`: explicit/preset/default). `--transparent` renders with alpha for compositing: RGBA PNG (still, or a `NAME_####.png` sequence) or ProRes 4444 `.mov` (QuickTime Animation/QTRLE with a warning on a Blender without a ProRes encoder, e.g. 4.2 LTS); `.mp4`/`.jpg` are refused (no alpha). The result's `alpha` block is read back from the written output (`verified`); a PNG sequence's `sequence` block (`dir`/`pattern`/`start_number`/`fps`) is ffmpeg-skill `sequence.py`'s interface. |
| `look.py FILE --uv\|--wireframe\|--textures -o OUT` / `look.py --compare A B -o OUT` | The agent's eyes: UV layout (SVG), a wireframe render, a texture grid, or a before/after comparison -- `--compare` also reports a pure-numpy PSNR/SSIM similarity score (`score_skipped` with a reason instead, when A and B don't share pixel dimensions); an identical pair reports PSNR as the finite sentinel 100.0, not `+inf` (invalid in strict JSON). |
| `check.py FILE --target NAME` | PASS/WARN/FAIL against a delivery target's budget, with a fix command per row; for `.usdz`, also validates the package's own zip structure against Apple's real requirements (uncompressed, 64-byte-aligned entries); for `3d-print`, also flags any sampled face under a 0.8mm wall-thickness budget (assuming the file's units are mm, the standard STL convention). |
| `fit.py FILE -o OUT --target NAME [--max-stages N]` | Automatically re-optimizes in escalating stages (default up to 5) until the file fits `check.py`'s own real budget for `NAME`, or reports honestly (non-zero exit) that it still doesn't. Only loops on the three budget rows this skill can actually fix (triangle count, texture size, transmission size); triangle/texture budgets get an exact one-shot fix at stage 0 (decimate ratio is precise, confirmed directly), transmission size is the one genuinely unpredictable dimension (only measurable after compression, never computable in advance) so it's the one that really escalates -- halving the texture cap each further stage. Reads results from `optimize.py`'s own report and the output file's real bytes, never by re-importing a `--meshopt`/`--ktx2`-compressed stage through Blender (which can't read that format back -- see pitfalls.md). |
| `bake.py FILE --pass ao\|normal\|roughness\|diffuse\|combined -o OUT [--atlas]` | Bake a material to a texture; `--atlas` repacks UVs across several objects into one shared image first. |
| `scene.py --init FILE` / `scene.py FILE.json [-o OUT] [--export OUT]` | Assemble a declarative scene (asset placement, lights, camera, background) into a render and/or an exported 3D file. |
| `batch.py DIR --recipe RECIPE.json --out-dir OUT [--cache] [--watch]` | Chain this skill's own scripts as a recipe over every file in a folder, with a content-hash cache. |
| `verify.py FILE... [--target NAME]` | The whole toolchain (info -> convert --verify -> check) over one or more files, PASS/FAIL per file. |

`mcp/server.py` exposes every script above as an MCP tool over stdio; each tool takes the exact
CLI `argv` as its one argument rather than a separate structured schema that could drift from
what the CLI actually does.

## What this skill does and does not decide

This skill measures, converts, and mechanically transforms 3D files -- it does not make
creative or content-understanding judgements:

- **Whether a decimated/optimized result still looks right** -- `check.py` measures against a
  budget, `look.py` renders it for you to judge; this skill doesn't decide "good enough" itself.
- **What a scene should contain, or how it should be composed** -- `scene.py` assembles exactly
  what a `scene.json` declares; deciding the layout, lighting mood, or camera angle is the
  calling agent's or the user's call.
- **Picking a subject, crop, or region not given explicitly** -- every script's parameters are
  mechanical once known (a decimate ratio, a texture cap, a bake pass); choosing *what value* to
  use for an ambiguous request belongs to the calling agent, from `info.py`'s real numbers.
- **UV unwrapping** -- `check.py`/`info.py` detect a missing UV map and say so; this skill does
  not (yet -- see ROADMAP.md) unwrap one automatically. Say what's wrong and point at Blender's
  own UV tools rather than guessing a fix.
- **Non-manifold/topology repair beyond a simple hole** -- `optimize.py --fill-holes` closes a
  boundary-edge hole/gap; it does not touch non-manifold edges shared by 3+ faces or fix
  self-intersecting geometry (`info.py` flags both, with no safe automatic repair for either).
  Say what's wrong and point at Blender's own mesh-cleanup tools rather than guessing a fix.

If a request needs a Blender feature none of these scripts expose, say so and name the closest
built-in option -- never hand-write a raw `bpy` script outside `scripts/bpy/*.py` as a fallback.
A raw script bypasses every guarantee this skill makes (no shell, typed arguments, verification
afterwards, cross-Blender-version compatibility via `_compat.py`).
