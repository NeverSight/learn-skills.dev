---
name: blockbench-albedo-to-pbr
description: Derive height, tangent-space normal and packed MER (metalness, emissive, roughness) maps from an albedo/base-color texture for Blockbench PBR materials, using PyPBR (Python) or vgpu + Dawn WebGPU (Node.js), with optional Depth Anything V2 height estimation and MER inferred from the albedo plus the normal's curvature. Use after a color texture exists (painted, imported, or generated with blockbench-gpt-image-textures) when a material needs normal, heightmap or MER channels, a Bedrock RTX texture_set, or when asked to make a normal map, bump map, height map, roughness, metalness or emissive map from a texture. Triggers on albedo to normal, normal map from texture, height map from albedo, MER map, roughness from texture, metalness map, emissive map, Depth Anything, PyPBR, vgpu, Sobel normal, DirectX vs OpenGL normal, texture_set normal, heightmap or metalness_emissive_roughness layer.
---

# Albedo to Normal and MER for Blockbench

PBR channels are derived, not painted: albedo → height field → tangent-space normal, then metalness, emissive and roughness inferred from the albedo, the height and the normal's curvature and packed into one MER image. Two scripts share one CLI and the same maths; pick by runtime. Load [blockbench-use](../blockbench-use/SKILL.md) first for discovery and verification, and [blockbench-pbr-materials](../blockbench-pbr-materials/SKILL.md) to assign the results. This skill produces the image files only.

| Runtime | Script | Install | Height estimation |
|---|---|---|---|
| Python | `scripts/albedo_to_normal.py` | `pip install pypbr` (+ `transformers` for depth) | Depth Anything V2 through transformers, CUDA when available |
| Node.js | `scripts/albedo_to_normal.mjs` | `npm install vgpu pngjs` (+ `@huggingface/transformers` for depth) | Depth Anything V2 ONNX through transformers.js, CPU or WebGPU |

Both write `<name>_height.png` (grayscale, light = high), `<name>_normal.png` (RGB, opaque) and `<name>_mer.png` (R metalness, G emissive, B roughness) and print a JSON report. Runtime setup, API notes and troubleshooting: [references/python-pypbr.md](references/python-pypbr.md), [references/node-vgpu.md](references/node-vgpu.md). Node needs the script's `scripts/` folder reachable from a project that has the dependencies installed; Python only needs the packages.

## Workflow

### 1. Get the color texture as a file

Run `list_textures` and note the target texture's UUID, `bitmap_size` and `uv_size`; it does not report a file path. If the texture was imported from a file you wrote (for example the downscaled atlas from the GPT image workflow), use that file. Otherwise fetch the image with `get_texture` and save the returned PNG to disk, or have Blockbench save the texture. Work on the atlas at its native texel size, not on an upscaled generation canvas, so the maps share the texel grid with the color map.

Check the atlas before deriving anything: relief scale must be consistent across faces, so apply [UV scale and distortion guidance](../blockbench-texturing/references/uv-scale-and-distortion.md) to the color map first. A normal map inherits every stretch in the UV layout.

### 2. Choose the height source

| Source | Flag | Use for |
|---|---|---|
| Luminance (default) | `--height-source luminance` | Pixel art and flat-shaded painted textures. Light reads as high; add `--invert-height` when dark paint is the raised part (dark grout should stay low). |
| Depth Anything V2 | `--height-source depth` | Photographic or painterly textures with real structure: bricks, planks, cobble, foliage, machinery. Useless on a two-tone checker. Depth is downloaded on first use. |
| Height file | `--height-source file --height-file h.png` | A height painted in Blockbench, from another tool, or a previous `_height.png` to reshape. |

Depth estimation sees a photo, not a tile: it returns a foreground-to-background ramp that breaks tiling. The script keeps `--flatten 1` and normalize on for depth; add `--high-pass <texels>` (about a quarter of the tile width) for non-linear bias and `--seam offset` for seamless tiles. Small textures are nearest-neighbour upscaled to at least 1024 px before the model and block-averaged back, so 16× art keeps its edges. Details: [references/height-processing.md](references/height-processing.md).

### 3. Run

```bash
# tiling 16x block, pronounced pixel relief
python scripts/albedo_to_normal.py block.png --out ./pbr --wrap --strength 1
node   scripts/albedo_to_normal.mjs block.png --out ./pbr --wrap --strength 1

# entity/prop atlas with transparent gutters (islands isolated automatically)
python scripts/albedo_to_normal.py goal_atlas.png --out ./pbr --strength 0.5

# HD tile from a painterly texture, depth-estimated, softened for smooth relief
node scripts/albedo_to_normal.mjs planks.png --out ./pbr --height-source depth --high-pass 32 --seam offset --wrap --soften 1
```

| Flag | Default | Effect |
|---|---|---|
| `--wrap` | off | Sample across borders. On for seamless tiles, off for atlases and non-tiling art. |
| `--strength F` | 0.5 | Gradient multiplier. 0.25 subtle, 0.5 default, 1–2 strong pixel relief; halve per doubling of texture density. |
| `--operator` | sobel | `sobel`, `prewitt` (softer), `scharr` (smooth HD height). |
| `--convention` | directx | `directx` green-down (Bedrock RTX assumption) or `opengl` green-up (Blender, glTF, labPBR). |
| `--alpha-threshold` | 8 | Albedo alpha below this is off-island: no relief bleeds across gutters; gutters get the flat normal. |
| `--soften M` | 0 | Density-scaled Gaussian on the height (≈ shortSide/64 · M texels). Use 1 for ≥64× textures; keep 0 for 16×. |
| `--levels B,W,G` | 0,1,1 | Input black/white/gamma on the height before the kernel. |
| `--flatten`, `--high-pass`, `--normalize`/`--no-normalize`, `--invert-height` | depth: 1, 0, on | Depth shaping, also available for `file` and `luminance` sources. |
| `--seam offset --seam-amount A` | off, 0.15 | Wrap-and-heal seam blend on the height for tiles. |
| `--no-height`, `--no-mer` | off | Skip writing `_height.png` / `_mer.png`. |
| `--metal`, `--emissive`, `--roughness` | auto | `auto` infers the channel; a 0..1 value makes it uniform (`--metal 0` for anything that is not metal). |
| `--palette "#RRGGBB=m,e,r;..."` | none | Exact-colour MER overrides; `-` keeps the inferred channel. The precise tool for pixel-art palettes. |
| `--rough-curvature W`, `--rough-height I`, `--rough-weights V,E,S`, `--rough-scale`, `--rough-bias` | 0.25, 0, 0.4/0.3/0.3, 1, 0 | Roughness terms: normal curvature (crevices rougher, ridges smoother), height influence, variance/edge/saturation weights, output remap. |
| `--metal-brightness`, `--metal-saturation`, `--gold-hue`, `--copper-hue`, `--no-metal-clean` | 0.6, 0.15, 0.11–0.17, 0.03–0.10, clean on | Metal heuristic thresholds; the clean-up is a 3×3 majority vote against speckle. |
| `--emissive-brightness`, `--emissive-saturation`, `--emissive-overbright`, `--emissive-softness` | 0.8, 0.5, 1 (off), 0 | Emissive thresholds, over-bright fallback, glow-edge anti-aliasing. |
| Python `--depth-device`, `--material-folder`; Node `--depth-device`, `--depth-dtype`, `--gpu` | | Runtime specifics; see the references. |

MER inference is heuristic. Read [references/mer-inference.md](references/mer-inference.md) before tuning it: bright desaturated colours read as metal and bright saturated colours read as glow, which is wrong for wool, bone, snow, pale skin, yellow beaks and painted signs. Decide the material first, then choose `auto`, a uniform value or palette overrides per channel.

### 4. Read the report

The JSON on stdout ends with `report` and `merReport`. For the normal, require `verdict: "ok"` and `classification: "standard"`; `meanXYBias` near 0 and `negativeZCount` 0. A `heightfield` classification means the albedo argument was a grayscale image; `warn` with a large bias on a tile means an unflattened ramp in the height. `flatPct` is informational (high on flat art and on atlases with big gutters).

For the MER, compare `metalPct` and `emissivePct` with what the material actually is, and `roughnessMean` with how matte it should look. A wooden crate with `metalPct` 0.4 means the pale planks were misread as steel: rerun with `--metal 0` or a palette. `paletteTexels` 0 with a palette means the colour did not match exactly. The report says the encodings are sound, not that the relief direction, scale or material assignments are right; that is step 6.

### 5. Import and assign in Blockbench

```
create_texture: name="<name>_normal", data="<absolute path to <name>_normal.png>"
create_texture: name="<name>_mer",    data="<absolute path to <name>_mer.png>"
create_pbr_material: name="<material>", color_texture="<albedo>", normal_texture="<name>_normal", mer_texture="<name>_mer"
# or on an existing material:
assign_texture_channel: material="<material>", texture="<name>_normal", channel="normal"
assign_texture_channel: material="<material>", texture="<name>_mer", channel="mer"
get_material_info: material="<material>"
```

Bedrock texture sets take `normal` **or** `heightmap`, never both. Assign the `_height.png` as `height_texture` instead when the target is 16× vanilla-style pixel art and the pack convention prefers heightmaps; otherwise use the normal. A MER texture requires the color texture on the same material; when the whole surface shares one metal/emissive/roughness value, `mer_value` on the material is simpler than a map (generate with `--no-mer`). Match `uv_width`/`uv_height` on `create_texture` to the color texture in formats with per-texture UV sizes. Channel rules, uniform MER values and `save_material_config` are in [blockbench-pbr-materials](../blockbench-pbr-materials/SKILL.md).

### 6. Verify direction and scale

Look at the lit model with `capture_screenshot` from at least two angles and at the intended viewing distance:

- Raised features must read as raised. Inverted top-to-bottom shading means the wrong green convention: regenerate with the other `--convention`. Everything reading inverted (pits as bumps) means the height sense is wrong: regenerate with `--invert-height`.
- Relief must look the same size on every face. Adjust `--strength` globally; fix uneven results in the UV layout or the color atlas, not by hand-editing the normal.
- Tiling blocks: place several copies and check the seams; `--wrap` and `--seam offset` on the height are the fixes, not painting over the seam.
- No rim around atlas islands. If one appears, the albedo alpha was not clean; raise `--alpha-threshold` or clean the gutters and regenerate.
- Metal regions must be the parts that are metal (they turn dark and reflective under RTX), glow must sit only on light sources, and roughness must not make cloth or paint shiny. Fix with uniform values, palette overrides or the roughness terms, and regenerate the MER rather than painting it.
- The rendered preview only proves Blockbench's shading; confirm in the target game or renderer before delivery.

## What to expect

- Luminance height is an artistic proxy: painted highlights become bumps and painted shadows become pits. It is the right choice for stylised and pixel art, and wrong for photo-sourced textures.
- Depth estimation on textures is relief-plausible, not measured. Expect per-run variation between the PyTorch and ONNX model conversions and treat `--flatten` / `--high-pass` / `--seam` as required cleanup for tiles.
- Both runtimes produce byte-identical heights from the same luminance input, normals within two levels of each other from the same height, and MER within three levels on roughness with identical metal masks.
- MER inference is colour and shape heuristics, not material recognition. Expect false metal on pale desaturated areas and false glow on bright saturated ones; the report makes both visible and the overrides fix them without painting.
- PyPBR's own `compute_normal_from_height` (0.1.0b5) zero-pads borders and flips X, so the Python script derives the normal itself and uses PyPBR for the material object, folder I/O and follow-up operations.
- Node resolves `vgpu`, `pngjs` and the shaders from the script's location; without a GPU, run `npx vgpu install-software-renderer` once and pass `--gpu software`.

## Resources

- [references/height-processing.md](references/height-processing.md): the height and normal pipeline stage by stage, depth shaping, kernel maths, conventions, report fields, runtime parity.
- [references/mer-inference.md](references/mer-inference.md): how metalness, emissive and roughness are inferred, every MER flag, overrides, the MER report and the checks to run.
- [references/python-pypbr.md](references/python-pypbr.md): install, PyPBR material API and quirks, Depth Anything through transformers.
- [references/node-vgpu.md](references/node-vgpu.md): install, vgpu compute/texture API used by the script, WGSL notes, transformers.js depth in Node.
- `scripts/albedo_to_normal.py`: Python pipeline (torch + PyPBR, optional transformers).
- `scripts/albedo_to_normal.mjs`: Node pipeline (vgpu + Dawn, pngjs, optional transformers.js).
- `scripts/shaders/height-map.wgsl`, `normal-map.wgsl`, `mer-map.wgsl`: the GPU passes; also readable as the reference maths.
