---
name: mc-asset
description: Author, render, inspect, batch-build, check, and package Minecraft Java Edition resource-pack textures, models, and complete packs with the mc-asset CLI or its MCP server — text-grid sprites (.grid), editable multi-layer sources (.mcpx), procedural block textures, material recolors and variants, tiling checks, animation strips, nine-slice GUI scaling, declarative recipe batch builds, style auditing, contact sheets, and whole-pack validation. Use when you need to produce or edit textures as text, build a complete resource pack, or batch-edit pixels without a paint program. For how the art should look, also load the minecraft-pixel-art skill.
---

# mc-asset

mc-asset turns texture and resource pack work into text and commands. You can
draw single sprites as character grids, or author an entire resource pack
declaratively from recipes with lockfile tracking, automated 2D/3D model
generation, style auditing, contact sheets, and byte-reproducible zip packaging.
The same inputs always produce the same bytes. Every command exists both as a
CLI subcommand and as an MCP tool (`mc-asset mcp`); this skill shows the CLI
form, and `references/commands.md` maps each one to its MCP tool.

**Art direction lives in the `minecraft-pixel-art` skill.** Load it before you
draw anything that should look like Minecraft; this skill only covers the tool.

## Authoring complete resource packs

To create and ship an entire resource pack project from scratch:
1. **Initialize**: `mc-asset pack init <dir> --namespace <ns> --minecraft-version <v>`
2. **Style & Presets**: `mc-asset style list` (`vanilla`, `soft`, `fairy-flat`, `dark-frame`)
3. **Reference & Catalog**: `mc-asset pack catalog --vanilla <path>`
4. **Recipes**: `recipes/*.recipe.json` with block and item definitions, entity templates, equipment, fonts, particles, matrix variables, and animations. Choose the recipe `formatVersion` for the steps used.
5. **Batch Build**: `mc-asset pack build --project <file>` (three-stage safe build with lockfile)
6. **Check & Audit**: `mc-asset pack check` (ordered fix list) and `mc-asset style audit`
7. **Contact Sheet**: `mc-asset preview contact-sheet --inputs <paths...> --output <file.png>`
8. **Package**: `mc-asset pack package --output <file.zip>` (deterministic zip delivery)

See `references/pack-workflow.md` for the complete 8-step guide, full recipe
examples, and failure recovery.

## Getting the tool

```sh
npx -y mc-asset --version        # run without installing
npm install -g mc-asset          # or install the CLI
```

Node.js 22 or newer. In a checkout of the mc-asset repository, run directly
with `bun src/cli/index.ts`, or use `node bin/mc-asset.js` after `bun run build`.

## The drawing loop

1. **Write the grid.** One character per pixel; the palette maps symbols to
   colors and, optionally, roles. `references/grid-format.md` has the rules.

   ```text
   [palette]
   . = transparent
   O = #3A2418FF role=outline
   D = #6B452CFF role=shadow
   B = #8F5C2AFF role=base
   L = #C08A4EFF role=highlight

   [grid]
   ....
   .OO.
   OLBO
   ODDO
   ```

2. **Render** to a PNG and keep the editable source:

   ```sh
   mc-asset render item.grid --output item.png --source item.mcpx
   ```

3. **Look at it.** Upscale with nearest neighbour and view the image (a 16px
   sprite is unreadable at 1×):

   ```sh
   mc-asset preview item.png --scale 12 --output item-x12.png
   ```

   Over MCP, `inspect_asset` with `mode: "view"` and `scale` returns the image
   directly, and `apply_asset_operations` with `feedback` returns a picture of
   each edit.

4. **Measure it.**

   ```sh
   mc-asset analyze item.png                         # size, color count, alpha, dominant colors
   mc-asset --json palette inspect item.png          # full color distribution
   mc-asset --json cleanup item.png --output tmp.png # detected: isolated / noise / aa counts
   mc-asset preview item.png --ascii                 # the PNG back as a .grid
   ```

5. **Review** against the minecraft-pixel-art checklist, edit the grid, and
   render again. Keep going until the checklist passes at 1× and at ×8.

6. **Validate** for its destination:

   ```sh
   mc-asset validate item.png --profile minecraft:item
   ```

## Common tasks

| Task | Command |
| --- | --- |
| Reference image → pixel art | `pixelize ref.png --size 16 --preset item --output out.png` |
| Procedural block texture | `generate noise --size 16 --palette stone --seed 42 --output stone.png` |
| Tiling check / wall preview | `tile stone.png`, then `tile stone.png --preview 4x4 --output wall.png` |
| One material recolor | `recolor sword.mcpx --material gold --output sword_gold.png` |
| All material variants | `variant sword.mcpx --materials iron,gold,copper --output-dir out --mkdir` |
| Reduce colors | `quantize in.png --colors 8 --output out.png` |
| Fix stray pixels | `cleanup in.png --fix isolated,noise --allow-render-pass-change --output out.png` |
| Pixel edits in a batch | `build src.mcpx --operations ops.json --output out.png` |
| Flip / rotate / crop / pad | `transform in.png --flip h --output out.png` |
| Animation strip | `animate pack --frames-dir frames --layout vertical --output anim.png` |
| Contact sheet of sprites | `animate pack --frames-dir sprites --layout horizontal --output sheet.png` |
| Nine-slice GUI scaling | `gui-scale panel.png --mcmeta panel.png.mcmeta --size 48x32 --output big.png` |
| Whole resource pack | `validate-pack ./MyPack --minecraft-version 26.3` |
| Shrink a PNG losslessly | `optimize in.png --output-dir out --mkdir` (add `--dry-run` to preview) |
| Validate a Java model | `model validate model.json --pack ./MyPack --minecraft-version 26.3` |
| Initialize pack project | `pack init ./MyPack --namespace mypack --minecraft-version 1.21.9` |
| Batch build from recipes | `pack build --project ./MyPack/mc-asset.pack.json` |
| Style audit & check | `pack check --project ./MyPack/mc-asset.pack.json` |
| Family silhouette audit | `style audit textures/item/*_sword.png` |
| Contact sheet overview | `preview contact-sheet --inputs textures/item/*.png --output overview-{page}.png` |
| Package pack zip | `pack package --project ./MyPack/mc-asset.pack.json --output MyPack.zip` |

`references/commands.md` explains each one, its MCP twin, and the gotchas.

## Rules the tool enforces

- **Explicit outputs.** Every write needs `--output`, `--source`, or `--stdout`;
  existing files need `--force`; missing folders need `--mkdir`. MCP tools
  never overwrite and never create folders.
- **Deterministic.** Procedural commands take a `--seed`; the same seed gives
  the same bytes.
- **Machine-readable.** `--json` puts a `{ success, result, error }` envelope
  on stdout. Exit codes: 0 ok, 2 bad invocation, 3 validation failed,
  4 filesystem refusal, 5 unsupported or over a limit.

## Recolor and variants: understand the two paths

`recolor` and `variant` have two separate execution paths with different role
rules:

### 1. Palette Family Path (`--family` / `--families`, used in pack recipes)
- **Six direct roles**: `outline`, `shadow`, `dark`, `base`, `light`, and
  `highlight` map directly to the target family's six ramp steps.
- **Geometric boundary override**: Body pixels touching transparency or the
  canvas edge are geometrically detected and forced to the family `outline` color.
- **`accent` and `custom` are NOT preserved by default**: they map across the
  six integer luminance bands (<43 outline, 43–85 shadow, 86–127 dark,
  128–170 base, 171–213 light, ≥214 highlight).
- **Protecting non-metal parts**: To prevent handles or inlays from being
  recolored, you **must** explicitly specify `preserveRoles: ["custom"]`,
  `preserveRegions: ["handle"]`, or pass a `--selection`.

### 2. Builtin Material Path (`--material` / `--materials`)
- Maps three tones: `shadow`/`dark` → material shadow; `base` → base;
  `light`/`highlight` → highlight.
- `outline`, `accent`, and `custom` stay exactly as drawn.

## Gotchas

- `preview --scale` and `transform --resize-mode nearest` are the only upscales
  to use for pixel art; other resize modes blend colors.
- `animate pack` reads only the `.mcpx` files in a folder, in file-name order,
  and warns about anything else. Prefix names (`1-sword.mcpx`) to fix the
  order. All frames must share one size.
- `tile --preview` accepts `2x2`, `4x4`, or `8x8`.
- `.grid` symbols are single characters from `[.0-9A-Za-z]`; `.` is always
  transparent. Past 63 colors, switch to `[grid tokens]`.
- A shell variable holding a command with spaces (`M="node bin/mc-asset.js"`)
  does not word-split in zsh; use a shell function instead.
- `gui-scale` never reads a sibling `.mcmeta` by itself; pass `--mcmeta`.
