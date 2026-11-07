---
name: roblox-3d-model
description: "Generate game-ready Roblox meshes from text or image references using verified concepts, mesh generation, headless Blender, measured budgets, textures, and import manifests. Use for individual props or asset batches; route hard-surface assets through Kiln."
---

# Roblox 3D models, headless

> **KAGGLE IS OFF. Do not use it (2026-10-19).** Kaggle's Terms of Use allow only
> "internal, personal, non-commercial use", and its Acceptable Use Policy
> (kaggle.com/aup) bans using its resources for "server farming" or "activity
> unrelated to ML data science". Running this skill's batch stage on Kaggle got
> the author's account banned for "resource abuse". The Kaggle scripts now stop
> with this message instead of running. Do not route around that, and never make
> a second Kaggle account: the Terms ban that outright.
>
> Until a checked replacement is wired in: hard-surface props go through Kiln
> (`references/kiln-route.md`, runs locally, no GPU). Organic meshes come one at
> a time from the Hugging Face Space (`scripts/image_to_3d.py`). Read Hugging
> Face's terms for your use before relying on it: they have not been checked for
> this. With a 16GB NVIDIA GPU you could run Hi3DGen yourself, but this skill
> does not ship a script for that yet.

> **First time on this machine?** Read `LOCAL.md` in this folder. If it does not exist, run the
> `roblox-skills-setup` skill (or copy `LOCAL.template.md` to `LOCAL.md` and fill it in).
> `LOCAL.md` holds your paths and tool locations; it is yours and is never shared.

Text prompt in, a game-ready MeshPart in Studio out. Six stages, one gate.

```
prompt -> 2D concept image -> [VERIFY] -> Hi3DGen (600k faces) -> Blender (decimate, UV, bake) -> Open Cloud upload -> Studio wire
```

The pipeline is your own toolchain, not Roblox's `generate_mesh`. Cube 3D is the
Tier 1 fallback if a stage fails on the day, nothing more.

**Read the shape-class fork below before starting.** This pipeline is the wrong
tool for hard-surface props and the cost of finding that out at stage 4 is real.

## STATUS: geometry works, texturing works as of 2026-08-26

Proven end to end on 2026-08-24 against real assets (a cow and a pig), on Kaggle. Stage 4b was broken on that run and was **rebuilt and verified
on 2026-08-26** against the same two assets. Read this before trusting any stage.

| Stage | State |
|---|---|
| 1-2 concept image + gate | **works.** 16/16 generated, and the gate rejected 2 of them on sight |
| 3 Hi3DGen | **works** (measured on Kaggle, which is now OFF). ~102 GPU-seconds per asset, ~600k faces out |
| 4 Blender weld/decimate/UV/normal bake | **works.** 74:1 and 104:1 reductions, 6,000 tris, maps baked |
| 4b colour | **works. PAINT it** (`paint_texture.py`), do not project. Projection was rebuilt on 2026-08-26 and still smears; painting is exact. See below |
| 5 upload | **works**, run end to end 2026-08-26. Free: Open Cloud key costs nothing and Model/Image uploads cost no Robux. Needed only for a PERMANENT asset; stage 6 iterates with no upload at all |
| 6 Studio wiring | **works**, verified 2026-08-26 in Studio 0.735.639: 5,998 tris + a 1024 texture rebuilt in 0.05s with zero credentials. See below |

### Stage 4b was broken, and how it was fixed

The first version ran, reported healthy numbers, and produced a map that was
**visually wrong**: a cow with its face smeared across its flank, a pig dark grey
over most of its body. Its own report said `looks_projected: true`, colour
variation 2.95, alignment IoU 0.62, `alignment_trustworthy: true`.

**Those statistics measured that SOMETHING was projected, not that it landed in
the right place.** That is the lesson worth carrying; the four defects behind it
are worth carrying too, because three of them are shaped like bugs you will write
again.

| # | Defect | How it showed up |
|---|---|---|
| 1 | the subject mask covered **90.4%** of the concept and its bbox was the whole frame | a concept has a **vignette**, so a corner-sampled background colour with a global threshold reads the lighter centre as subject. Every silhouette score was then the mesh compared to **a filled square**, which is why all eight views tied within 0.02 |
| 2 | nothing ever checked the mask | the failure was silent and confident |
| 3 | the projector was framed on the **mesh** (`radius * 2.2`) and not on the concept | about 0.10 frame off in x, hanging 0.055 below the pig, so **31% of the pig's front-facing surface sampled background**. That is the grey |
| 4 | one camera cannot texture an animal | a surface edge-on to the projector gets a colour stretched along the view axis. All eight single-camera trials put a snout across the flank |

**Defect 3 is the one to remember.** The old code already knew framing was the
problem: `_normalise()` crops both silhouettes to their bounding boxes before
comparing, with a docstring explaining exactly why. **The fix had been applied to
the measurement and never to the thing being measured.**

The fixes, in `scripts/texture_bake.py`:

- **border flood fill with a local tolerance** for the mask, so it follows a
  gradient instead of fighting it. Pig: fill 0.275, correct bbox
- **`check_mask()`**, which refuses a mask over 60% or under 3%, or one whose
  bbox spans the frame. Six lines, and it converts a silent wrong answer into a
  loud failure
- **`fit_projector()`**, which moves and zooms the camera in a measured loop
  until the mesh silhouette bbox sits on the concept subject bbox. Measured in a
  loop rather than solved in one step, because the sign conventions for an ortho
  shift are easy to get backwards and a wrong sign is invisible in the output
- **a second projector**, camera A spun 180 degrees about the object's vertical
  axis, sampling the concept **mirrored in u**, blended by which way each surface
  faces. On a bilaterally symmetric animal that is the correct far side for free.
  **The mirror is load-bearing**: without it the second projector paints the face
  onto the rump. Camera B is **derived** from camera A rather than fitted
  separately, because two independent fits both scored 0.992 and still disagreed
  about which end was the head
- **a confidence fade**: where `|normal . view axis|` is near zero neither
  projector knows anything, so the shader falls back to the subject's median
  colour instead of painting a stretched sample
- **view selection scored AFTER fitting.** Unfitted silhouette IoU is dominated
  by framing: the pig spread only 0.066 across all eight candidates. Fitting
  first takes the cow's spread from 0.11 to 0.25

**Measured after the rebuild:**

| | pig | cow |
|---|---|---|
| subject mask fill (was 0.904) | 0.275 | 0.235 |
| projector bbox IoU | 0.988 | 0.810 |
| surface landing on the subject (was 69%) | 81% | 76% |

**What still cannot be done here.** A silhouette cannot tell a mirror pair apart:
the pig's top two candidates scored 0.7523 and 0.7515, and `+X` and `-X` produce
byte-identical bounding boxes. Do not try to solve that statistically. The run
sets `ambiguous_view` and prints the command to render the pair; **look at it.**
That is this stage's version of the 2D gate, applied to the one decision no
number in it can make.

```bash
"$BLENDER" --background \
  --python scripts/pair_sheet.py -- --mesh work/out/low.glb \
  --color work/out/color.png --concept work/concept.png --view=-X+Y --out pair.png
```

The report no longer carries a boolean claiming the texture is good. It carries
`pct_landing_on_subject`, which measures whether the colour landed in the right
place, and `requires_visual_check: true`, which is always true.

**Thresholds are provisional.** They rest on two assets and **no measured
failure**: pig 0.988 and cow 0.810 both look right, so the hard fail sits at 0.70
with a warning band above it. Do not tighten either number without a measured bad
case, and never tighten one to make a run go green.

**Still baked in, and not fixed:** the concept's specular highlights. The maps
carry the concept's shine, which is wrong for a `SurfaceAppearance ColorMap` and
reads as a light streak along the back. Acceptable at Roblox scale, worth fixing
if these ever get used close up.

### Measured, on real assets

| | cow | pig |
|---|---|---|
| Hi3DGen faces | 443,726 | 622,668 |
| GPU seconds | 103.4 | 101.1 |
| GLB size | 10.65 MB | 14.95 MB |
| after decimation | 6,000 tris | 6,000 tris |
| reduction | 73.8:1 | 103.6:1 |
| UV coverage | 0.39 | 0.53 |
| longest axis | 6.01 studs | 4.0 studs |

**~102 GPU-seconds per asset** is the number to budget a batch with. Sixteen
animals is about 27 minutes of a 30-hour weekly Kaggle allowance, not a fortnight.

A third asset (**sheep**) failed with **CUDA out of memory** in the same run: VRAM
is not released between assets in the loop. Unfixed.

## First decide the shape class. This pipeline is for ORGANIC

Route by what the object **is**, before touching a single stage.

| Object | Route |
|---|---|
| animals, creatures, plants, cloth, anything whose silhouette you would call *grown* | **this pipeline** |
| guns, crates, lockers, vehicles, machinery, buildings, furniture, anything with flat faces and hard edges | **Kiln** (code-authored GLB), see `references/kiln-route.md`. Not this pipeline. |

The fork is structural, not a preference:

- **The 60:1 reduction only pays for itself on organic shapes.** Hi3DGen gives
  600k faces of detail and stage 4 throws almost all of it away, which is correct
  on a cow because it comes back as a normal map. On a gun there was no organic
  detail to bake in the first place, so you pay the GPU, the decimation and the
  UV unwrap and receive a rounded-off version of a shape that code could have
  drawn crisp, cheap and already inside budget.
- **Decimation actively fights hard surface.** `--decimate-mode collapse` rounds
  off exactly the edges a gun needs to keep. `planar` mitigates it. Neither fixes
  having generated the shape the wrong way.
- **Colour is broken here and is not broken there.** Stage 4b produces unusable
  maps (see above). Parametric geometry carries colour per part in its material
  names, so it arrives correct.
- **Hard surface is where variants live.** Skins, attachments, compact vs long
  barrel. Parametric geometry regenerates a variant in one turn; this pipeline
  reruns the full ~102-GPU-second chain per variant.

**Where this pipeline wins and nothing else does:** organic shapes, turning an
existing reference image into a mesh, and volume. Sixteen assets headless is
about 27 minutes of GPU. Nobody hand-downloads sixteen GLBs.

## The one idea this skill is built on

**Verification is cheap at 2D and expensive at 3D.** A vision model can reliably
answer "is this a revolver, is it one object, is it facing the right way" from a
PNG. It cannot reliably answer that from a screenshot of a raw mesh. So the gate
goes at stage 2, where a bad result costs seconds and nothing else.

Everything downstream of the gate is deterministic. If the image is right and the
mesh comes back wrong, that is a seed problem, not a judgement problem: rerun.

**Never skip the gate to save time.** Skipping it moves the failure to the
expensive end, which is the difference between a thirty-second regenerate and a
dead hour.

## Read this first: five things that will bite

**0. A GLB imports as a triangle soup, and it poisons everything downstream.**
Measured while building this skill: glTF stores normals per corner, so Blender
splits every vertex on import. The test shape came in at **245,680 vertices and
welded back down to 40,962**. Nothing looks wrong, and then:

- `Decimate/Collapse` cannot collapse across disconnected faces, so it
  under-reduces while reporting success
- `Smart UV Project` gives every triangle its own island, the islands land
  sub-pixel, and the bake rasterises **nothing** - producing a valid, perfectly
  **flat** normal map

Every step exits 0. `mesh_pipeline.py` welds immediately after import (clear
custom split normals, then merge by distance) and the verifier asserts the weld
happened. If you ever write a second importer, do this first. Full account, and
the three wrong diagnoses that came before it, in `references/traps.md`.

**1. Hi3DGen returns geometry ONLY. No colour, no UVs, no texture.** Confirmed by
reading the Space's `app.py`: TRELLIS is called with `formats=["mesh"]` and is fed
the *normal* image, not the colour image. So:

- there is nothing to bake a base colour from, and a base-colour bake produces a
  flat grey PNG that looks like a bug and is not one
- `Smart UV Project` is mandatory, not optional cleanup
- **the colour has to come from somewhere else**: the concept image projected on,
  the `roblox-texture-gen` skill, or Studio's `generate_material`

Advice to "bake base colour too if there is anything to capture" does not apply
here: there is definitively nothing. Plan the colour stage separately.

**2. The ratio is 60:1, and decimation alone cannot do it.** Hi3DGen gives about
600,000 faces. Roblox's hard cap is **20,000 triangles per MeshPart**, enforced at
upload, and the number that actually governs is **under 10,000**, because 20k is a
moderation ceiling and not a performance budget, and most of Roblox is mobile.
Collapsing 600k to 10k destroys exactly the detail that made the model good.
**Bake, do not discard**: decimate to 8-10k, then bake the 600k mesh's detail into
a tangent-space normal map and let lighting carry the geometry.

**3. The upload is `assetType: Model`, never `Mesh`.** The Assets API `Mesh` type
takes Roblox-native content only; `Model` accepts .fbx/.gltf/.glb. Getting it
backwards **presents as a permissions error**, so it burns time looking like an API
key problem. `scripts/upload_asset.py` refuses `Mesh` with that explanation.

**4. 1024 is the texture cap.** `SurfaceAppearance` maps are capped at 1024x1024
and larger source art is downscaled on upload. Bake at 1024. Baking at 2048 and
hoping costs bake time and buys nothing.

## Before the first run

| Variable | Needed by | Notes |
|---|---|---|
| `HF_TOKEN` | stages 1 and 3 | Raises the ZeroGPU quota above the signed-out floor and buys queue priority. Effectively required. |
| `CF_ACCOUNT_ID`, `CF_API_TOKEN` | stage 1 only | Cloudflare Workers AI. Preferred for images because it costs **no** ZeroGPU quota, leaving all of it for the mesh. |
| `ROBLOX_API_KEY` | stage 5 | Open Cloud key with Assets write. |
| `ROBLOX_USER_ID` or `ROBLOX_GROUP_ID` | stage 5 | Who the asset is created under. |

`gradio_client` must be installed (`pip install gradio_client`). The Blender
commands below use `"$BLENDER"`: set the `BLENDER` environment variable to your
Blender 4.x executable (or put `blender` on PATH and use that). `batch.py` finds
Blender itself from `BLENDER`, then PATH, then the standard install folders.
Your value goes in `LOCAL.md`.

## Stage by stage

### 1-2. Concept image, then verify

```bash
python scripts/concept_image.py --prompt "a weathered brass steampunk revolver" --out work/concept.png
python scripts/concept_image.py --preset creature --prompt "a Holstein dairy cow" --out cow.png
```

Default backend is **FLUX.1-schnell on the official HuggingFace Space**, which
needs no credentials and is Apache-2.0, so its output is clean for a commercial
game. Two measured things decide this stage:

- **Pollinations' anonymous tier now serves only `sana`.** `/models` returns
  exactly `["sana"]`, and asking for `flux` silently gets the small model with no
  error. That is why an early batch of sixteen came back malformed. It is the
  fallback of last resort now, not the default.
- **Anonymous FLUX is queue-limited.** First request 12s, the very next one
  refused with "No GPU was available after 60s". The backend retries with
  backoff; `HF_TOKEN` (free account) buys priority, and the old
  Kaggle image route is OFF (see the notice at the top).

The `--preset creature` framing is not cosmetic, and **a prettier picture can
make a worse mesh**. Hi3DGen reads an estimated *normal map*, not colour, so flat
vector-style art carries almost no shading to infer geometry from. The creature
preset asks for a shaded 3D toy render precisely to give the estimator gradients,
and pins the two failures that wasted a whole batch: all legs planted (the duck
and goose each generated standing on one leg) and no ground plane or scenery (the
pig generated on grass under a pink sky).

**Then read the PNG yourself and answer four questions:**

1. Is it the object that was asked for?
2. Is it **one** object, with nothing else in frame?
3. Is the **whole** object visible, uncropped?
4. Is the background plain and separable from the subject?

Any "no" means regenerate with a corrected prompt or a new seed. This costs
seconds. Do not proceed on a "close enough".

### 3. Image to 3D on Hi3DGen

Hosted, not local: Hi3DGen needs a 16GB NVIDIA GPU, and without one (for example a card with
less VRAM, or no CUDA) local generation is impossible rather than merely slow. Kaggle is
OFF (see the notice at the top), so that leaves the Space:

**Kaggle: OFF. Do not use it.** See the notice at the top. `kaggle_run.py` now
stops with that message instead of running.

**A HuggingFace Space (one-offs only).** `python scripts/image_to_3d.py --image
work/concept.png --out work/high.glb`. Free ZeroGPU is **300 GPU-seconds per
day** against a generation of minutes, which is one or two meshes. Fine for a
single test, useless for a set of sixteen.

Expect a GLB of roughly 600k faces and tens of MB. Both paths also save the
normal-bridge image the model produced internally, which is the best diagnostic
when a mesh comes back wrong: if the bridge is wrong, the concept was the
problem and no reseed will fix it.

### 4. Blender: decimate, unwrap, bake

One command, runs headless, no live connection:

```bash
"$BLENDER" --background \
  --python scripts/mesh_pipeline.py -- \
  --input work/high.glb --outdir work/out --target-tris 9000 --texture-size 1024 \
  --decimate-mode collapse --target-studs 4.0
```

It writes `low.glb`, `normal.png` and `report.json` with the real triangle counts.

- **`--decimate-mode` matters.** `collapse` for organic shapes, `planar` for hard
  surface. On a gun or a crate, `collapse` rounds off exactly the edges that should
  stay crisp.
- **The UV unwrap is the weak link**, not the decimation, and the dial is
  `--uv-margin`. It is charged **per island** and a generated mesh has many, so a
  margin that looks small eats the texture. Measured on the test shape at 1024px:
  margin 0.02 used **29%** of the UV square, 0.003 used **49%**, 0.001 used 51%.
  Default is 0.003. Raise it only if islands visibly bleed into each other; lower
  it and you gain almost nothing. `report.json` carries `uv_coverage`, and under
  0.25 means the padding is the problem, not the decimation.
- **The cage matters.** Too small and the bake misses geometry (black patches), too
  large and it picks up the wrong surface (smeared detail). `--cage-extrusion`
  auto-scales from the model size; only override it if the bake is visibly wrong.

### 4b. Colour. Paint it, do not project it

Hi3DGen returns no colour, so colour has to come from somewhere. There are two
routes here and **the painter is the default**.

#### The painter (default)

```bash
# once per mesh: which way does it face in object space
"$BLENDER" --background \
  --python scripts/axes_probe.py -- --mesh work/out/low.glb --out axes.png

# read landmarks and the concept's real palette
"$BLENDER" --background \
  --python scripts/paint_texture.py -- --mesh work/out/low.glb \
  --concept work/concept.png --describe

# paint
"$BLENDER" --background \
  --python scripts/paint_texture.py -- --mesh work/out/low.glb \
  --spec work/pig.paint.json --outdir work/out
```

Every texel of the mesh's own UV layout is rasterised back to the 3D point it
belongs to, normalised into the bounding box, and coloured by a short stack of
stamps. **There is no camera anywhere in it**, so there is nothing to align,
nothing to smear, and no mirror-pair view to choose. Working example in
`references/example-pig.paint.json`.

- **`--describe` first, always.** It prints the bounding box, a ten-slice Y
  profile with the z and x extent of each slice, the nose-most vertex, the
  footprint of the lowest 5% of Z, and a six-colour k-means palette of the
  concept. That is enough to place a snout, eyes, ears and hooves without
  guessing, and it takes seconds.
- **`axes_probe.py` before that**, once per mesh. Three markers at known
  normalised positions, four views. It answers "which end is the head" from a
  picture rather than from a guess. On the pig: head at **y=0**, tail at y=1,
  z up, x across.
- **`mirror: "x"`** gives two eyes, two ears and two of anything from one entry.
- **`facing`** restricts a stamp to surfaces pointing a given way, which is how
  eyes stay on the sides of the head instead of wrapping around it.
- **The palette must come from `--describe`, not from looking at the concept.**
  A chroma test is not enough to drop the background: the pig concept's grey
  backdrop carries a pink cast off the subject, so a saturation threshold kept
  85% of it and the palette came back as three greys. The flood-fill mask fixes
  it (subject 29.4% of frame).
- **Colours are pure albedo.** They carry no baked light, so they read flatter
  and darker in a dim preview than the projected maps did, which had the
  concept's highlights baked in. Verified: `#F2A8C4` in, `#F1A6C2` back out of
  the atlas. Do not brighten the palette to compensate for preview lighting;
  brighten the preview.
- `uv_coverage` in the report should match `report.json` from stage 4. On the
  pig both read 0.525, which is the cheap proof that the rasteriser and Blender
  agree about the layout.

**It took three passes on the pig**, each about two minutes: colours too dark
under a dim preview, then the snout too small and the pupils sitting outboard of
the whites, then the brow landing on the ear. That loop is the method, not a
failure of it: paint, render six views, look, adjust three numbers.

#### Projection (`texture_bake.py`, kept, not the default)

Camera-projects the concept onto the mesh. Rebuilt once and it works far better
than it did, but **it still smears** and the failure is structural, not a bug:

- a photograph has to be wrapped around geometry it was never taken of, so
  surfaces edge-on to the projector get colour stretched along the view axis
- only 81% of the pig and 76% of the cow land on the subject at all
- a silhouette cannot tell a view from its mirror, so the last call is always
  yours

Use it when the asset needs the concept's actual markings and a flat palette
would lose them - a specific cow's patches, a decal, a logo. For anything
stylised, paint.

### 5b. The permanent route, verified end to end

Run once when an asset is worth keeping. **Everything here is free**: the Open
Cloud key costs nothing, and Model and Image uploads cost no Robux.

```bash
python scripts/upload_asset.py --file work/out/low.glb   --name Pig_Mesh --asset-type Model
python scripts/upload_asset.py --file work/out/color.png --name Pig_Tex  --asset-type Image
```

Both returned `moderationState: Approved` immediately on a first run.

**THE TRAP THAT COSTS THE MOST TIME HERE: upload the texture as `Image`, NOT
`Decal`.** Both succeed. Both come back Approved. Only one works. A Decal asset
**wraps** an image and has a **different id** from the image inside it, so
assigning a Decal id to `MeshPart.TextureID` **silently does nothing** and the
model renders grey. There is no error anywhere. Measured: the Decal id
left the pig grey; the Image id, from the same PNG,
textured it correctly.

**A .glb uploads as a `Model`, which means there is no bare mesh id to assign.**
The Model wraps a MeshPart. To get a permanent `MeshId` you insert the Model
once and take the MeshPart out of it:

```lua
local m = game:GetObjects("rbxassetid://MODEL_ID")[1]
local p = m:IsA("MeshPart") and m or m:FindFirstChildWhichIsA("MeshPart", true)
p.Parent = workspace
p.TextureID = "rbxassetid://IMAGE_ID"
if m ~= p then m:Destroy() end
```

After this the part carries a real `MeshId` and a real `TextureID`, and survives
saving and publishing.

**IF THE MCP BRIDGE IS WEDGED, USE STUDIO'S COMMAND BAR.** It needs no plugin
and no bridge, and it takes the same Luau. Two things about it:

- **Ctrl+Enter runs it. Plain Enter inserts a newline.**
- Anything touching `CurrentCamera` raises a **"Dangerous Command Detected"**
  dialog that must be cleared before the command runs. Avoid camera calls in an
  automated path, or expect to clear the prompt.

### 5 and 6. Into Studio, with no upload

**This is the finding that unblocked both stages.** The Open Cloud upload needs
`ROBLOX_API_KEY` and the Studio MCP's `upload_decal` needs that or a
`ROBLOSECURITY` cookie. With **neither set**, there is still a complete path:
`AssetService` builds an `EditableMesh` and an `EditableImage` from raw data in
process and hands back a real `MeshPart`.

```bash
# 1. pack the mesh and texture as binary blobs
"$BLENDER" --background \
  --python scripts/export_for_studio.py -- \
  --mesh work/out/low.glb --color work/out/color.png \
  --outdir work/serve --name pig

# 2. serve them to localhost only
python scripts/serve_assets.py --dir work/serve
```

Then run `references/studio_import.lua` through the MCP's `execute_luau`, in
**edit mode**. Measured on the pig: **0.05s** for 5,378 verts, 5,378 UVs, 5,998
triangles and a 1024x1024 texture.

**Three things that were unknown and are now measured:**

- **`HttpService:GetAsync` works from plugin context with
  `HttpService.HttpEnabled = false`.** That setting governs game scripts, not
  plugins. This is what makes the whole route possible.
- **`GetAsync` is byte-exact on a binary body.** A 251,532-byte blob arrived
  intact, so `buffer.fromstring(body)` reads it directly: no base64, no JSON,
  and no giant literal pasted into a script.
- **`CreateMeshPartAsync` is permitted from plugin context in edit mode.** That
  had been an open question here for weeks. It is not.

**THE LIMIT, and it is real.** `MeshContent` and `TextureContent` both come back
as `Enum.ContentSourceType.Object` with a **nil `Uri`**. They are session-local
objects, not asset URIs, so **they will not survive saving or publishing the
place.** This route is for building, iterating and looking at the thing in
engine. Making an asset permanent still needs an upload, or Studio's own
right-click **Save to Roblox** on the resulting MeshPart.

**Two traps, both of which produce a confidently wrong model:**

- **Do not flip the winding when converting axes.** Blender Z-up to Roblox Y-up
  is `(x, y, z) -> (x, z, -y)`, whose determinant is **+1**, so it is a rotation
  and preserves winding. Flipping it "because an axis was negated" renders every
  face backwards: the model looks **hollow and see-through with dark patches**,
  which reads as a texture alpha bug and is not one.
- **Do not flip the texture rows.** Blender's row 0 is the bottom of the image
  and Roblox's buffer row 0 is the top, **but Roblox's UV v also runs from the
  top while Blender's runs from the bottom**. The two conventions cancel, so the
  array is written as-is. Flipping it sends UV islands into the atlas gutter and
  the model comes back **covered in black blotches**. That one cost two wrong
  diagnoses first: texture resolution, then the UV dedupe. Both were fine.

**Diagnosing this class of bug:** the same mesh and the same texture render
correctly in Blender, so when Studio disagrees, the export is wrong, not the
asset. `paint_texture.py`'s `uv_coverage` matching stage 4's `report.json` is the
cheap proof that the UVs themselves are sound.

## Run a whole set

One manifest, eight stages, all resumable: an asset whose output exists is
skipped unless `--force`.

```bash
python scripts/batch.py concepts --outdir work/farm   # 1-2  text -> concept png
python scripts/batch.py sheet    --outdir work/farm   #      LOOK at the gate sheet
# 3  Kaggle is OFF: image_to_3d.py per asset (the Space), or Kiln for hard surface
python scripts/batch.py meshes   --outdir work/farm   # 4    -> low.glb + normal
python scripts/batch.py orient   --outdir work/farm   #      LOOK once, whole set
python scripts/batch.py paint    --outdir work/farm   # 4b   spec + colour map
python scripts/batch.py publish  --outdir work/farm   # 5    Open Cloud upload
python scripts/batch.py studio   --outdir work/farm   # 6    emits _studio_wire.lua
```

Then run `_studio_wire.lua` through the Studio MCP's `execute_luau` in edit mode.

**Proven end to end on 2026-08-26** with a cow and a pig, and again on
2026-08-31 with a coin and a trophy: painted, uploaded, inserted, textured,
standing in a place, permanent.

### THERE ARE TWO IDS PER ASSET AND THEY ARE NOT INTERCHANGEABLE

Open Cloud cannot upload a raw **Mesh**, so stage 5 uploads a **Model**, and that
model *wraps* a MeshPart whose `MeshId` points at an inner Mesh asset Roblox
mints on ingest. `_assets.json` records the **model** id. Measured 2026-08-31:

```
AssetService:CreateMeshPartAsync(model_id) -> "Failed to load mesh asset"
AssetService:CreateMeshPartAsync(mesh_id)  -> OK, exact size
```

Two consequences, and the first one costs an hour if you meet it cold:

**A MeshPart cannot be expressed in a Rojo `.model.json`.** `MeshId` is not
settable by property assignment. Rojo will build the part, apply `TextureID`,
`Size` and `CFrame`, and leave the geometry blank - and the only symptom is the
plugin saying *"Synced, but 1 change failed to apply"* next to a part that looks
like an untextured cube. Do not try to ship meshes through Rojo.

**So there are two real routes, and they suit different jobs:**

| Route | Needs | Use it for |
|---|---|---|
| `game:GetObjects(model_id)` | Studio (plugin/`execute_luau`) | **shipping.** Bakes the mesh into the place, so the running game needs no network and no moderation round trip. This is what `_studio_wire.lua` does. |
| `AssetService:CreateMeshPartAsync(mesh_id)` | the INNER mesh id | runtime creation in a live server. Yields. |

The inner `mesh_id` is only discoverable by inserting the model once and reading
`.MeshId` off the result, so **record it** alongside the model id rather than
rediscovering it. In a game project that belongs in a `MeshBank.luau` next to the
`SoundBank`, with a `work/meshes/install.lua` doing the insert - the same shape
as the sfx stage, for the same reason: the ids live on disk, the instances live
in the place.

**And re-check orientation when a mesh replaces a primitive.** A Roblox
`Cylinder`'s flat faces are on its LOCAL X and need a 90 degree roll to read as a
coin; a generated coin mesh is already upright on Z, so the same roll lays it
flat on the floor. Carry the corrective CFrame with the part, not in the caller.

**Uploading was never the fragile part.** The pig, the cow, the coin and the
trophy all uploaded first time. Everything above is about getting an uploaded
asset *into the tree*.

### The two stages that need eyes, and why that is not a human clicking

`sheet` and `orient` both produce ONE image for the WHOLE set. The agent reads
them. Nobody has to click anything, and neither is skippable:

- **`sheet`** is the 2D concept gate. It has already caught a bee that generated
  as three bees and a chicken that generated as a grid of seven.
- **`orient`** answers which end of each body axis is the head. **Geometry
  cannot decide this.** The cross-section heuristic is right on a pig (11.3x)
  and **wrong on a cow** (2.3x), because a cow's rump out-bulks its head. Width
  contradicts too, in the opposite direction: the pig's head region is wider
  than its rump, the cow's is narrower. Two animals, two contradictions.
  `make_paint_spec.py` therefore **refuses** to guess below 5x and `batch.py
  paint` **skips** any asset still marked `UNKNOWN` in `_orientation.json`.

Read the orient sheet like this: a **green sphere marks the MAX end** of the
body axis. Head opposite it means `min`; head on the same side means `max`.

### Speed: what is worth optimising, measured

Timed on a desktop CPU with the pig, 2026-08-26. Optimise what is
actually slow, not what feels slow.

| Step | Cost | Verdict |
|---|---|---|
| `mesh_pipeline` (600k -> 6k + normal bake) | **14.7 s** | the local floor. Cost is welding and decimating 600k faces |
| the same with a **512** bake instead of 1024 | 13.4 s | **not worth it.** Saves 1.3 s and costs texture quality |
| `make_paint_spec` + `paint_texture` | **3.7 s** | painting is nearly free |
| `render_check`, 6 views, **Cycles** | **16.8 s** | was costing 4x the actual work |
| `render_check`, 6 views, **EEVEE** | **6.5 s** | **now the default.** Reads identically for judging placement |
| `render_check`, 6 views, **Workbench** | 3.9 s | fastest, flatter. `--engine WORKBENCH` when you only need placement |

**Two changes came out of this, both real:**

- **EEVEE is the default render engine.** The sheet exists to answer "did the
  colour land in the right place", and EEVEE answers it identically 2.6x faster.
  Cycles is still there with `--engine CYCLES` for a presentable render.
- **`batch.py --jobs N` runs per-asset work in parallel** for `meshes` and
  `paint`. The jobs are genuinely independent. Default is `cores // 3`, because
  Blender is itself multi-threaded and more than that thrashes. Measured on two
  assets: 15.4 s serial, 9.4 s at `--jobs 4`; the gain scales with set size.

**What NOT to touch:**

- **Hi3DGen sampler steps.** That is the quality knob, not a speed knob.
- **Bake resolution.** Measured above: 1.3 s.
- On a real sixteen-asset run the **Kaggle round trip dominates everything
  local** - ~102 GPU-seconds per asset plus kernel boot and dependency install.
  Local Blender work is minutes; the GPU stage is tens of minutes. Push all
  sixteen in ONE kernel run and do the local stages while it is queued.

### The spec generator

`make_paint_spec.py` writes a first-pass paint spec from measured landmarks plus
the concept's palette, so a set of sixteen is not sixteen hand-authored specs.
It reproduced the hand-tuned pig closely enough to be indistinguishable at
gameplay distance.

- **Patterned animals get a patch scatter.** If the palette holds a second
  common colour far from the base in luminance, a deterministic set of patch
  blobs is added. Without it the cow came out **entirely white** - a clean model
  of the wrong animal.
- The scatter is fixed, not random, so a set regenerates identically.
- The generated spec is plain JSON. Move a stamp, change a colour, delete the
  patches - then rerun `paint` with `--force`.

**Always render after painting.** `scripts/render_check.py` gives six views on a
plain ground. The spec generator is a first pass, not an oracle.

## Verify before believing

```bash
"$BLENDER" --background --python scripts/verify.py
"$BLENDER" --background --python scripts/verify_texture.py
```

`verify.py` builds an 82k-triangle high-poly, runs the whole geometry stage on it,
and asserts on the outputs: the split import was detected and welded, triangle
count under budget, UVs exist, lie in range and cover enough of the texture, the
normal map is neither empty nor flat, the exported GLB re-imports at the reported
count. **19 checks.**

`verify_texture.py` uses **Suzanne**, because the test has to be able to fail: a
sphere looks the same from every side, so a view picker would score 100% while
being wrong. It renders her from a known direction as a fake concept and asks the
stage to recover that direction from silhouettes alone, then checks the colour
bake landed. **9 checks.**

**Both suites pass as of 2026-08-24.** They fail loudly rather than exiting 0 on a
broken artifact, which they have already done twice: the flat-normal-map bug in
trap 0 was found by `verify.py` on its first run, and the left/right silhouette
ambiguity by `verify_texture.py` on its first run.

**And then look at the PNG.** The verifier checks that a normal map has variation;
it cannot tell you the seams are ugly. Code exiting 0 is not the artifact being
correct.

## References

- `references/traps.md` - every failure mode found so far, symptom first
- `references/licences.md` - the licence audit, what was read and when
- `scripts/export_for_studio.py` + `scripts/serve_assets.py` + `references/studio_import.lua` - the no-upload route into Studio
- `scripts/make_paint_spec.py` - measured landmarks + palette -> a first-pass spec
- `scripts/orient_sheet.py` - the head-end gate for a whole set in one image
- `scripts/render_check.py` - six views of a textured mesh, for judging by eye
- `scripts/paint_texture.py` - the painter, and `axes_probe.py` for object-space orientation
- `references/example-pig.paint.json` - a hand-tuned spec (solid colour)
- `references/example-manifest.json` - a batch manifest to copy (`--manifest`); names, studs, prompts, optional per-asset `tris`
- `references/example-cow.paint.json` - a GENERATED spec (patterned, patch scatter)
- `scripts/pair_sheet.py` - concept next to the mesh from both sides, the 4b eye check
- `references/kiln-route.md` - HOW: the hard-surface route with Kiln, run end to end to a Roblox-ready GLB
- `scripts/kiln_to_roblox.mjs` - Kiln GLB -> Roblox: -Z front, studs, one mesh per hex-named colour, 20k tri gate
- `references/example-rifle.kiln.js` - a worked hard-surface program
- `references/hard-surface-route.md` - WHY hard surface forks off this pipeline (its Claude Design route is superseded by Kiln)
- `references/studio-wire.lua` - insert, SurfaceAppearance, CollisionFidelity

## Fallback ladder

| Tier | Route | When |
|---|---|---|
| T3 | Kiln program -> `kiln_to_roblox.mjs` -> Studio Import 3D | **Hard-surface objects.** First choice for them, not a fallback |
| T2 | This pipeline | Default for organic, and for any batch |
| T1 | Studio MCP `generate_mesh` (Cube 3D) | Space down, quota gone, or the clock beat you |
| T0 | Primitive parts assembled in code | Always works, never impressive |

Decide which tier you will drop to before you start a long batch. Deciding mid-run wastes the run.

## Quadrupeds: rig, animate, and export as a SKINNED mesh

Promoted from a real build 2026-09-09. Four-legged creatures are not covered by
the R15 rig, so this chain exists to fit one:

| Script | Does |
|---|---|
| `probe_rig.py` | Report what is actually inside a rigged blend before building on it |
| `quadruped_rig.py` | Fit a 19-bone armature by MEASURING the mesh, then skin it explicitly - Blender's `ARMATURE_AUTO` binds ZERO vertex groups on these meshes, silently, with no error |
| `quadruped_anim.py` | Gaits from footfall phases: walk LATERAL, run DIAGONAL, lunge BOUND |
| `export_skinned.py` | Export a Roblox-ready skinned GLB, and emit each bone's swing axis expressed in its OWN rest basis |

**Export as a skinned mesh, not as one rigid box per bone.** A previous build did
the latter and argued for it - a skinned MeshPart must be uploaded before Roblox
accepts bones, and the run could not verify that round trip. The upload works,
and the performance law it was really defending (no Humanoid, no Animator, one
bulk write per frame) is BETTER served by the mesh: `Bone.Transform` is a plain
property set, and a skinned creature puts ONE part into a `BulkMoveTo` where
nineteen boxes put nineteen.

`export_skinned.py` refuses to ship a mesh Roblox will render wrong: more than 4
influences on any vertex (Roblox silently drops the rest, which reads as a limb
tearing on one animation frame), or any vertex bound to no bone at all. It emits
the swing axis per bone because `Bone.Transform` is expressed in the bone's own
rest frame - a hardcoded X rotation is right for some bones and quietly wrong for
others, which reads as "the walk looks a bit odd" rather than as a bug.

## Mesh verification scripts

| Script | Answers |
|---|---|
| `check_colours.py` | Does the colour map's ACTUAL pixels match the spec hexes? This is the gate for the linear/sRGB trap - a paint pass once shipped every map at half brightness, asking `#969BA0` and writing `#4E545A`, with no metric noticing. Sample the file, never trust the lighting |
| `check_prop.py` | What fraction of a built prop's VISIBLE surface is the thing you meant it to be |
| `landmarks.py` | Dump a mesh's landmarks with the head end STATED, not inferred |
| `zprofile.py` | Per-height slice - how wide is the mesh at each point along its length. Print the whole profile BEFORE writing a rule about its shape; three verifier rewrites came from picking an extreme instead of a landmark |
| `finish_creature.py` | Centre a creature on its own mass, export, and MEASURE the result |
