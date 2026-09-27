---
name: blockbench-vanilla-textures
description: Pull original ("vanilla") Minecraft textures from Mojang's bedrock-samples repository through the jsDelivr CDN and apply them to Blockbench models, resolving block IDs to per-face files, tinting grayscale grass/leaves/water, tiling large faces, handling flipbooks, and importing the vanilla PBR texture_set (MERS/normal). Use when the user asks for vanilla, default, original, real or Minecraft-accurate textures, names a Minecraft block or material for a model (brick wall, oak log, stone bricks, grass block, wool, glass), wants a model to match the base game, or needs a Bedrock texture name mapped to Java Edition. Works for Bedrock, Java and generic models.
---

# Blockbench Vanilla Textures

Use Mojang's own texture files instead of painting or generating an imitation. Source: [Mojang/bedrock-samples](https://github.com/Mojang/bedrock-samples) (`resource_pack/textures/...`), served by jsDelivr:

```
https://cdn.jsdelivr.net/gh/Mojang/bedrock-samples@<ref>/resource_pack/textures/blocks/brick.png
```

`<ref>` is `main` or a release tag such as `v1.26.50.4`. Pin a tag when results must be reproducible. The names are **Bedrock** names, but the pixel art matches Java Edition for almost every block, so the files also work for Java and generic models after renaming where needed.

Load [blockbench-use](../blockbench-use/SKILL.md) before changing the project, and [blockbench-texturing](../blockbench-texturing/SKILL.md) for UV details.

**License:** the files are © Mojang AB and covered by the [Minecraft EULA](https://www.minecraft.net/en-us/eula). They are fine for Minecraft content, add-ons, resource packs and personal work. If the user plans to sell the model outside Minecraft or bundle the textures into a non-Minecraft asset pack, say so once and let them decide. Do not strip the attribution the manifest records.

## 1. Map the Request to Vanilla Blocks

Translate the subject into block IDs: a brick wall becomes `brick_block`, a log cabin `oak_log` plus `oak_planks`, a castle `stone_bricks` plus `cobblestone`. Ask only when a name is genuinely ambiguous ("stone" or "wood") and the choice changes the look. Otherwise pick the obvious block and state it. Block IDs resolve per-face textures, including log tops, grass tops and crafting-table fronts. Java IDs mostly work; the exceptions (`bricks` → `brick_block`, `grass_block` → `grass`, …) are in [names, tints and animation](references/names-tints-and-animation.md).

## 2. Fetch

Run the bundled resolver (Node 18+ or Bun, no dependencies). Script paths are relative to this skill folder.

```bash
node scripts/vanilla_texture.mjs search brick                                   # find IDs/keys
node scripts/vanilla_texture.mjs fetch brick_block oak_log grass --out <workspace>/textures/vanilla
node scripts/vanilla_texture.mjs fetch grass oak_leaves --carried --out <dir>   # pre-tinted inventory art
node scripts/vanilla_texture.mjs fetch brick_block --pbr --out <dir>            # + texture_set.json, MERS, normal
node scripts/vanilla_texture.mjs fetch entity/pig/pig --out <dir>               # any path under textures/
node scripts/vanilla_texture.mjs search zombie --tree --out <dir>               # entities/UI: one GitHub API call, cached
```

It prints and saves `<out>/vanilla_manifest.json`. Use these fields:
- `requests[].faces`: Blockbench face → atlas key.
- `requests[].atlas_keys[key].path`: the file for each key.
- `textures[]`: the local `file` (absolute path), `width`/`height`, `format` (`png` or `tga`), `frames`, `ticks_per_frame`, `tint`, `variants`, and `texture_set` layers.

Read the manifest instead of guessing file names.

A single known file needs no script:

```bash
curl -fsSLo brick.png https://cdn.jsdelivr.net/gh/Mojang/bedrock-samples@main/resource_pack/textures/blocks/brick.png
```
```powershell
iwr https://cdn.jsdelivr.net/gh/Mojang/bedrock-samples@main/resource_pack/textures/blocks/brick.png -OutFile brick.png
```

Some colour textures exist only as `.tga`, including leaves, `grass_side`, cactus and ferns. A 404 on `.png` means you should try `.tga`, which the script does automatically. The jsDelivr package-listing API rejects this repository as too large, so discovery goes through `blocks.json`, `terrain_texture.json`, `item_texture.json`, or the GitHub tree (`--tree`).

**Where to save:** put files the model will keep in the user's asset workspace, for example `textures/vanilla/`, not in a temp folder. Blockbench remembers an imported file's path and can write the texture back to it when the project is saved. Never modify a downloaded file in place after importing it; write edits such as tints and tiles to new file names.

## 3. Prepare: Tint, Tile, Animate

Check each manifest entry before importing:

- **`tint` is set:** the art is grayscale and Minecraft colors it by biome (grass top, leaves, vines, water). Either fetch with `--carried` for pre-tinted versions, or run `python scripts/tint_texture.py <in> <out> --color "#91BD59"`. Use `--colormap <colormap/grass.png> --temperature T --downfall D` to match a biome. Pillow is required.
- **`grass_side.tga`'s alpha is a tint mask, not transparency.** Its dirt pixels have alpha 0. Import `blocks/grass_side_carried` instead, or run `tint_texture.py ... --overlay`.
- **Large faces:** vanilla scale is 16 px per block, which is 1 px per Blockbench unit. Do not stretch one 16×16 tile across a 48-unit face; it produces giant bricks. Either use one 16-unit element per block, or pre-tile the texture: `tint_texture.py brick.png brick_3x2.png --tile 3x2` gives 48×32 px for a 48×32-unit face. Pre-tiling suits generic, Bedrock entity and glTF targets. Java block and item models need square 16×16 textures (a taller image is treated as a flipbook), so use one element per block there and keep the original file.
- **`frames` > 1** means a vertical flipbook, such as water, lava or sea lantern. Map UVs to one frame and follow [flipbook textures](../blockbench-flipbook-textures/SKILL.md) for playback and export metadata.

Tint colors, biome parameters and the full flipbook list are in [names, tints and animation](references/names-tints-and-animation.md).

## 4. Import and Assign

1. **Import each file** with `create_texture: name="brick", data="<absolute file path>"`. File paths require Blockbench desktop and load PNG and TGA. On Blockbench web, or when the file cannot be reached, pass a `data:image/png;base64,...` URL instead. Data URLs must be browser-decodable, so convert TGA to PNG first, for example with Pillow. Importing a path that is already loaded is refused; reuse that texture instead. For formats with `per_texture_uv_size`, pass `uv_width`/`uv_height` equal to the pixel size so UV coordinates are pixels.
2. **One texture for a whole element:** use `apply_texture: id=<element>, texture=<name>, applyTo="all"`.
3. **Different textures per face** (logs, grass, furnace, crafting table): use `set_cube_uv` with `faces: { up: { uv: [0,0,16,16], texture: "log_oak_top" }, north: { …, texture: "log_oak" }, … }`, following `requests[].faces`. Use `set_mesh_uv` for meshes. `blocks.json` names the south face as the front for furnaces, pumpkins and similar blocks; rotate the element or swap faces so the front faces the viewer.
4. **Box-UV formats** (Bedrock entity, Java entity) put one texture per cube in a box layout, so separate 16×16 block tiles do not fit them directly. Switch the element to per-face UV where the format allows it, or pack the tiles into an atlas and map the faces to their rectangles.
5. **Transparent textures** (glass, leaves, doors) need the target's cutout or blend settings. See the texturing skill.

**Fetching inside Blockbench.** jsDelivr sends `Access-Control-Allow-Origin: *`, so Blockbench can download a PNG itself when the agent has no shell, or its shell cannot reach Blockbench's file system. `risky_eval` awaits an expression, so wrap the code in an async IIFE that returns a data URL, then pass that URL to `create_texture`. Follow the repository's authorization rules for `risky_eval`.

```js
(async () => {
  const response = await fetch("https://cdn.jsdelivr.net/gh/Mojang/bedrock-samples@main/resource_pack/textures/blocks/brick.png");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const blob = await response.blob();
  return await new Promise(resolve => { const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.readAsDataURL(blob); });
})()
```

Vanilla block textures are a few hundred bytes, so the returned data URL is small. Prefer the file-path route for large entity sheets and for TGA files.

## 5. PBR (Optional)

Every vanilla block ships `<name>.texture_set.json` with `<name>_mers.tga` (metalness, emissive, roughness, subsurface), and some also ship `_normal.tga` or `_heightmap.tga`. Fetch with `--pbr`, keep the files together in the same folder, then call `import_texture_set: path="<out>/blocks/brick.texture_set.json"` on desktop. Follow [PBR materials](../blockbench-pbr-materials/SKILL.md) for assignment and export. Tinted color maps still need tinting; tint the color file and repoint the material's color channel to it.

## 6. Deliver for the Target Edition

| Target | What to do |
|---|---|
| Bedrock | Keep Bedrock names and paths, for example `textures/blocks/brick`. For custom blocks, the vanilla texture can be referenced by its terrain key instead of shipping a copy; see [material instances](../blockbench-use/references/bedrock-material-instances.md) |
| Java | Rename to the Java file name (`brick.png` → `bricks.png`, `planks_oak` → `oak_planks`) under `assets/minecraft/textures/block/`, or reference `minecraft:block/bricks` in the model JSON so the game's own texture is used. Add `.png.mcmeta` for flipbooks |
| Generic / glTF | Keep the pixel size and use nearest-neighbour filtering. Bake tints and tiling into the image, because no runtime will apply them |

## 7. Verify

- Run `list_textures` and confirm each texture's size and UV size.
- Run `get_cube_uv` or `get_mesh_info` and confirm every face shows `texture_status: "resolved"` with the intended texture.
- Capture a screenshot. Check brick or plank scale against a 16-unit reference, confirm tinted textures are not gray, check that transparency shows only where intended, and check that log tops sit on the ends.

## Worked Example: Brick Wall

"Model a brick wall" (Generic Model; a 3×2-block wall, 4 units thick):

1. Run `node scripts/vanilla_texture.mjs fetch brick_block --out ./textures/vanilla`. The manifest shows `blocks/brick.png`, 16×16, no tint.
2. Run `python scripts/tint_texture.py ./textures/vanilla/blocks/brick.png ./textures/vanilla/brick_wall_3x2.png --tile 3x2` to produce a 48×32 image.
3. Import it: `create_texture name="brick_wall_3x2" data="<abs>/textures/vanilla/brick_wall_3x2.png"`. Add `uv_width=48, uv_height=32` when the format uses per-texture UV size.
4. Place the cube: `from [0,0,0]`, `to [48,32,4]`.
5. Map every face 1 px per unit with `set_cube_uv`, all using `brick_wall_3x2`:
   - `north` and `south`: `[0,0,48,32]`.
   - `up` and `down`: `[0,0,48,4]`.
   - `east` and `west`: `[0,0,4,32]`.
6. Run `get_cube_uv` and confirm every face resolves. Capture a screenshot and check that one brick course matches a vanilla 16-unit block.

For a Java block model, build the same wall from six 16×16×4 elements. Map each one with the untouched `brick` texture: `[0,0,16,16]` on the large faces and `[0,0,16,4]` / `[0,0,4,16]` on the edges.
