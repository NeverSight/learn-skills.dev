---
name: blockbench-gpt-image-textures
description: Generate Blockbench texture atlases, skins and tiles with OpenAI GPT Image 2.5 (Flare or Sunburst) on fal.ai, writing the model's expected UV layout into the prompt so painted regions land on the right faces. Use when asked to AI-generate, concept, or repaint a texture for a Blockbench model, or to call openai/gpt-image-2.5/flare/text-to-image or openai/gpt-image-2.5/sunburst/text-to-image. Triggers on gpt image 2.5, gpt-image-2.5, flare, sunburst, fal.ai texture, generate texture with AI, UV-aware prompt, texture atlas prompt, AI skin, AI texture sheet.
---

# GPT Image 2.5 Textures for Blockbench

Generate a texture image with GPT Image 2.5 on fal.ai and land it on an existing Blockbench UV layout. The prompt must carry the UV layout: which pixel rectangle of the image belongs to which face. Without it the model paints a picture, not an atlas.

Load [blockbench-use](../blockbench-use/SKILL.md) first for discovery and verification rules, and [blockbench-texturing](../blockbench-texturing/SKILL.md) for UV inspection and cleanup painting.

## Pick a model

| Model | fal endpoint | Use for |
|---|---|---|
| Flare (default) | `openai/gpt-image-2.5/flare/text-to-image` | Fast drafts, most atlases, transparent backgrounds |
| Sunburst | `openai/gpt-image-2.5/sunburst/text-to-image` | Final high-resolution atlases with intricate detail; slower |

Both accept the same parameters and share `/edit` variants that take reference images. Details, pricing and recipes: [references/fal-api.md](references/fal-api.md).

## Workflow

### 1. Establish the UV layout first

The atlas layout must exist in Blockbench before prompting. Run `get_capabilities: include_tools=true`, then `list_textures`. If no texture or UVs exist, generate a native texture template as described in the texturing skill, then continue. Do not invent a layout in the prompt that the model does not have.

Collect the layout:

```
list_textures                              # frame_size and uv_size of the target atlas
get_cube_uv: id="<cube uuid>"              # one call per textured cube
get_mesh_info: mesh_id="<uuid>", include_uv=true   # meshes, if any
```

Save the raw results into one JSON file:

```json
{ "textures": [ ...list_textures... ], "cubes": [ ...get_cube_uv results... ],
  "meshes": [ { "name": "cloth", "faces": [ { "key": "f1", "uv": [[40,40],[56,40],[56,52],[40,52]] } ] } ] }
```

### 2. Compute the canvas and regions

fal rejects images under 655,360 pixels, so a 64x64 atlas cannot be generated at native size. Generate an integer upscale and downsample afterwards. The script picks the scale and converts every face rectangle into generated-image pixels:

```bash
node scripts/uv_layout_prompt.mjs inspection.json --texture <atlas name|uuid> > layout.json
node scripts/uv_layout_prompt.mjs inspection.json --format text   # human-readable check
```

Output includes `image_size` (pass to fal unchanged), `canvas.texel_scale`, one region per face with `px` and `texels` rectangles, and `shared_regions` for faces that reuse the same pixels. An exit code of 2 means the atlas aspect exceeds 3:1; generate a padded canvas and crop with `--crop` in step 5, or split the atlas.

### 3. Write the prompt with the layout inside it

Structure the prompt as JSON. The `layout` block is mandatory and comes straight from step 2. Read [references/uv-layout-prompting.md](references/uv-layout-prompting.md) for the full template, region-description rules and worked examples. Minimum shape:

```json
{
  "type": "UV texture atlas for a low-poly 3D game model, flat orthographic texture sheet, not a 3D render",
  "subject": "brown alpaca, cartoon Minecraft style",
  "style": "crisp pixel art, each texel a solid 16x16 px block, no anti-aliasing, 12-color palette, flat unlit colors",
  "canvas": { "width": 1024, "height": 1024, "texel_scale": 16, "represents": "64x64 texel atlas" },
  "background": "fully transparent outside the listed regions",
  "regions": [
    { "name": "head/north (face)", "px": [128, 128, 256, 256], "paint": "front of the head: two dark eyes, muzzle, no outline" },
    { "name": "head/up",   "px": [128, 0, 256, 128], "paint": "top of head fur, seam-continuous with head/north" }
  ],
  "rules": [
    "paint every region edge to edge; leave everything else transparent",
    "no labels, grid lines, borders, drop shadows or text anywhere",
    "adjacent faces of one cube must continue seamlessly across their shared edge",
    "regions listed as shared receive identical content"
  ]
}
```

Describe what each face shows, not the 3D scene. Name regions by cube and direction, keep the pixel rectangles exactly as computed, and mention rotation or mirroring the script reported.

### 4. Generate

```bash
FAL_KEY=... node scripts/fal_gpt_image.mjs --prompt-file prompt.json --model flare \
  --width 1024 --height 1024 --background transparent --quality medium --num 2 --out ./output --label alpaca
```

Use `--width/--height` from `layout.json` `image_size`. `--background transparent` yields real alpha on Flare; verify alpha on Sunburst output before relying on it. Start with `medium` quality and `--num 2` to pick a candidate; `high` or `xhigh` only for finals. `--dry-run` prints the request body for review. Download happens inside the script; fal URLs expire.

### 5. Downscale to the atlas

Skip this step when `texel_scale` is 1. Otherwise sample the centre of each texel block with nearest-neighbour and snap alpha for pixel art:

```bash
python scripts/resize_to_atlas.py output/alpaca_<ts>.png output/alpaca_64.png --width 64 --height 64 --alpha-threshold 128
```

Use `--sample average` for painterly high-resolution atlases, and `--crop X Y W H` to cut a padded canvas back to the atlas aspect first.

### 6. Import, apply and verify in Blockbench

```
create_texture: name="alpaca", data="<absolute path to alpaca_64.png>"
apply_texture: id="<group or element>", texture="alpaca", applyTo="all"
get_texture: texture="alpaca"
capture_screenshot
```

In formats with `per_texture_uv_size`, pass `uv_width`/`uv_height` to `create_texture` matching the original atlas `uv_size`. Check every face on the rendered model: regions drift, colours bleed across seams, and box-UV mirrored faces are often flipped. Fix small errors with the texturing skill's paint tools instead of regenerating. For larger errors, iterate through the `/edit` endpoint with the previous output URL and a prompt naming only the regions to change.

## What to expect

- The model treats pixel rectangles as guidance, not a contract. Expect 1 to 3 texel drift at region borders and occasional content spilling into transparent gutters; the downscale and cleanup pass absorb most of it.
- Fewer, larger regions work better than many tiny ones. For atlases with more than about 20 regions, group by body part in the prompt and describe shared regions once.
- Pixel-art phrasing ("each texel a solid 16x16 px block") keeps blocks aligned to the texel grid. Without it the model anti-aliases and the downscale muddies edges.
- A rendered UV template or checker fed through `/edit` as `image_urls` anchors the layout far more reliably than text alone. Use `capture_screenshot` or the native template texture, upload it, and prompt "paint this texture sheet" with the same `layout` block.
- Long text, logos and readable labels belong in a separate pass; they compete with the layout rules.
- Every output is a full RGB(A) image; nothing prevents the model from painting outside regions. Verify against `get_cube_uv` rectangles, not against the prompt.

## Resources

- [references/fal-api.md](references/fal-api.md): endpoints, parameters, sizes, pricing, transparency, curl/Node/Python recipes, edit endpoint.
- [references/uv-layout-prompting.md](references/uv-layout-prompting.md): prompt template, how to describe box-UV nets, per-face rectangles and mesh islands, worked examples for Bedrock entity, Java block and Generic Model targets.
- `scripts/uv_layout_prompt.mjs`: inspection JSON to canvas size and pixel regions.
- `scripts/fal_gpt_image.mjs`: call Flare or Sunburst (text-to-image or edit), save results.
- `scripts/resize_to_atlas.py`: nearest-neighbour or box downscale to atlas size, optional crop and alpha snap (needs Pillow).
