---
name: blockbench-substance
description: Optional, advanced pipeline between Blockbench and Adobe Substance 3D (Designer, Painter and the Substance Automation Toolkit command lines). Use only when the user has Substance installed and asks for it — render .sbsar procedural materials to Blockbench-sized PBR maps with sbsrender, cook .sbs graphs with sbscooker, bake AO/curvature/normal/position/ID maps from a Blockbench export with substance3d_baker, drive Substance 3D Painter over its remote-scripting HTTP API to paint a Blockbench model and export Bedrock MER or glTF maps, and pack results into texture_set.json. Triggers on Substance, Substance 3D, Substance Designer, Substance Painter, SAT, Substance Automation Toolkit, sbsar, .sbs, sbsrender, sbscooker, sbsmutator, sbsupdater, sbsbaker, substance3d_baker, pysbs, bake AO for Blockbench, Painter export to Blockbench. Not needed for ordinary painting, generated textures or derived normal maps.
---

# Blockbench + Adobe Substance 3D

**Optional and advanced.** Most Blockbench work never needs this: paint with [blockbench-texturing](../blockbench-texturing/SKILL.md), generate with [blockbench-gpt-image-textures](../blockbench-gpt-image-textures/SKILL.md), derive normal/MER with [blockbench-albedo-to-pbr](../blockbench-albedo-to-pbr/SKILL.md). Use this skill only when the user asks for Substance or already has `.sbsar`/`.sbs`/Painter assets. It needs a licensed Adobe Substance 3D install. Load [blockbench-use](../blockbench-use/SKILL.md) first and [blockbench-pbr-materials](../blockbench-pbr-materials/SKILL.md) to assign results.

Substance produces **image files**. Blockbench stays the source of geometry and UVs. Every path ends with files imported through `create_texture` (`data`, `pbr_channel`) or `import_texture_set`.

## 0. Locate the tools

```bash
python scripts/sat_locate.py
```

Designer bundles `sbsrender`, `sbscooker`, `sbsupdater` and `substance3d_baker`, off PATH, in `C:\Program Files\Adobe\Adobe Substance 3D Designer\`. `sbsmutator` and the `pysbs` Python API come only with the standalone Substance Automation Toolkit. Painter is a GUI app driven over HTTP. If nothing is found, stop and tell the user; do not install Adobe software.

## Pick the path

| Goal | Tool | Reference |
|---|---|---|
| Procedural material (bricks, rust, leaves) as Blockbench textures | `sat_render.py` → `sbsrender` | [sat-cli.md](references/sat-cli.md) |
| Have a `.sbs` graph, need an `.sbsar` | `sbscooker` (`sbsupdater` first if old) | [sat-cli.md](references/sat-cli.md) |
| Edit/specialise a `.sbs` headlessly | `sbsmutator` (SAT only) | [sat-cli.md](references/sat-cli.md#sbsmutator) |
| AO / curvature / ID / position masks from the model | `substance3d_baker` | [baker.md](references/baker.md) |
| Hand-paint the model with smart materials | Painter + `painter_remote.py` | [painter.md](references/painter.md) |
| Pack Bedrock MER, convert bit depth, flip normal green, shrink | `prep_maps.py` | below |

## Workflow A: procedural material → Blockbench

```bash
python scripts/sat_render.py material.sbsar --out out --size 16 --seed 7 \
  --set Season=0.8 --normal-format directx
```

- `--size` is pixels; the script converts to log2 `$outputsize` (raw `sbsrender` needs `'$outputsize@4,4'` for 16 px). It creates `--out`; raw `sbsrender` exits 47 if the folder is missing.
- Read `inputs` from the JSON report, then set parameters by identifier. Unknown identifiers come back as `warnings`, because `sbsrender` ignores them silently.
- Match outputs to channels by `usages`: `baseColor`/`diffuse` → color; `normal`; `height`; `metallic` + `roughness` (or `glossiness`, inverted) + `emissive` → MER.
- Output is 8-bit by default. Tiling block textures render straight at 16/32 px. For atlases, render at the atlas size or larger and shrink.

## Workflow B: bake masks from the Blockbench model

1. **Fix UVs**: every face needs its own UV rectangle. Default per-face Auto UV on block formats stacks faces on top of each other and ruins the bake. See [baker.md § Prepare](references/baker.md#prepare-the-blockbench-mesh).
2. `export_model` → `codec_id: "gltf"`, `options: {"encoding": "binary"}`, `path: <abs>.glb` (or `obj`).
3. Bake at 8–16× density with **underscore** flags (the online docs show hyphens, which fail):
   ```bash
   substance3d_baker AmbientOcclusion.Raytraced model.glb --use_lowdef_as_highdef true --output_size 512,512 --output_path bake
   ```
4. `python scripts/prep_maps.py convert bake/*.png --out bake/64 --size 64` (16-bit → 8-bit, box downsample).
5. Use the maps as masks: multiply AO into the colour texture, or feed them to `sbsrender --set-entry` / Painter.

## Workflow C: paint in Painter, bring maps back

1. Fix UVs, then `export_model` with `codec_id: "obj"`. Painter cannot import glTF.
2. Start Painter with `--enable-remote-scripting` (never `--help`: it opens the app), then:
   ```bash
   python scripts/painter_remote.py --ping --wait 240
   python scripts/painter_remote.py --python-file scripts/painter_new_project.py --result \
     --set MESH=C:/work/model.obj --set NORMAL=DirectX --set RESOLUTION=1024 --set BAKE=1
   ```
3. The user paints in Painter (or you script layers after reading the local API docs).
4. Export and shrink:
   ```bash
   python scripts/painter_remote.py --python-file scripts/painter_bedrock_export.py --result \
     --set OUT=C:/work/painter_out --set NAME=model --set PRESET=bedrock --set SIZE_LOG2=9
   python scripts/prep_maps.py convert C:/work/painter_out/model*.png --out final --size 64
   ```
   `bedrock` gives `NAME.png`, `NAME_mer.png`, `NAME_normal.png` (DirectX). `gltf` gives ORM + OpenGL normal. Painter never exports below 128 px, and skips maps whose channel is absent. Trust the `files` list in the result.

## Pack and import

```bash
python scripts/prep_maps.py pack-mer --metallic out/m_metallic.png --emissive 0 --roughness out/m_roughness.png --out final/model_mer.png
python scripts/prep_maps.py texture-set --color model --mer model_mer --normal model_normal --out final/model.texture_set.json
```

Constants are 0–255; `--glossiness` replaces `--roughness` and is inverted. Then `import_texture_set` with the JSON path, or `create_texture` per file (`pbr_channel`: `color`/`normal`/`height`/`mer`) + `create_pbr_material`. Normal **or** height, never both.

## Conventions and verification

- **Normals**: Bedrock → DirectX (green-down), glTF/Java labPBR → OpenGL. Baker default is `directx`. A graph's `$normalformat` is graph-defined (one tested graph flipped red, not green), so compare renders or use `prep_maps.py convert --flip-green`. After import, raised features must read as raised in the Blockbench preview.
- **16-bit trap**: AO/curvature/height PNGs are often 16-bit; `PIL.Image.convert("L")` clips them to white. Use `prep_maps.py convert` or `--output-bit-depth 8`.
- **Paths**: pass `C:/...` paths to the executables; `/c/...` from Git Bash breaks `--alias`. Quote `'$outputsize@...'`.
- **Blockbench project safety**: note the project UUID before export and import, and confirm it before writing textures back.
- Check each imported map with `list_textures`/`get_texture` and a `capture_screenshot`. A blank-white or uniformly gray map means the bit depth, UV overlap or parameter was wrong. It is not a stylistic result.
