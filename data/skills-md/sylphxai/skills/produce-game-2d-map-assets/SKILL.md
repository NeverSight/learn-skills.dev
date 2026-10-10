---
name: produce-game-2d-map-assets
description: "Produce engine-ready 2D tilesets, prop packs, layered maps, collision metadata, and composed previews. Use when the user asks for tiles, a tilemap, terrain, Tiled/Godot/Unity 2D maps, or seam-checked atlas props. Do not use for character animation sheets or store key art."
---

# Produce Game 2D Map Assets

Run the packaged extract and preview scripts; read each script's `--help` first. Do not freehand the atlas contract. A pretty atlas with wrong collision, seams, or layer names is not engine-ready.

- [extract prop pack](scripts/extract_prop_pack.py)
- [compose layered preview](scripts/compose_layered_preview.py)

Open [map pipeline selection](references/map-pipeline-selection.md) to choose the map, visual, and collision model. Open [layered map contract](references/layered-map-contract.md) or [prop pack contract](references/prop-pack-contract.md) for the selected shape. Open [tileset and prop QC](references/tileset-and-prop-qc.md) for seam and collision checks. See [script source](references/source.md) for license.

Use `produce-game-2d-sprites` for character and VFX sheets. Use `produce-product-assets` for marketing art.
