---
name: layer-textures
description: "Use when generating a texture with Layer that must repeat without a visible seam: ground, terrain, walls, fabric, foliage, stone, wood, pattern fills, or a tiling material for a game engine. Also when a generated texture shows seams at its edges, an obvious repeating motif across a surface, or baked-in lighting that fights the engine. Keywords: tileable, seamless, tiling, texture, material, pattern, trim sheet, terrain, repeat."
license: MIT
---

# Layer Textures

## Overview

A texture is not an image of a surface. It is an image whose left edge continues into its right edge
and whose top continues into its bottom, so that a plane tiled with it shows no seam. A model will
not do this unless the run asks for it.

The mandatory step is the capability filter: `list_base_models` with
`filter.capabilities: {tileability: true}`. Note the shape: `capabilities` is an object of booleans,
not a list of names. A model without it produces a picture of stone that seams visibly the moment it
repeats, and no editing pass fixes that afterwards. Everything else on this
page is secondary to getting that filter right.

Generation mechanics are in the `layer` skill. If a sibling skill named here is missing from your
available skills, ask the user to install it (`npx skills add layerai/skills --skill <name>`);
unattended, proceed from tool schemas and flag the gap.

## State the scale

Scale is what separates a usable texture from an unusable one, and it is the most commonly omitted
field. Say how much real-world surface the tile covers: "a 2-metre square of cobblestone, roughly
twenty stones across" is a texture. "Cobblestone" could be one boulder or a city square, and the
model will pick.

Anchor it to the feature rather than the tile: "individual planks about 15cm wide", "grass blades
roughly 5cm", "brick courses at standard size". The engine will scale the material, but only if the
density inside the tile is right to begin with.

## Flat light, no hero features

Two prompt clauses do most of the remaining work:

- **Even, diffuse, flat lighting, no directional shadows.** Baked-in shadow is the second-biggest
  defect after seams. A texture lit from the upper left looks wrong everywhere the engine's light is
  not upper left, and it cannot be removed later.
- **Uniform distribution, no focal point, no single distinguishing feature.** Generative models like
  to compose, so they will place one dramatic cracked stone in the middle. Tiled across a floor, that
  crack becomes a grid of identical cracks and is the thing every player notices.

Ask for consistent variation instead: "evenly distributed wear and colour variation across the whole
tile, no single dominant feature."

## Judging the result

Do not judge a texture by looking at the tile. Judge it tiled. Check the four edges continue into
each other, then check a 3x3 repeat for a motif that has become a pattern. A tile that looks
excellent alone and shows an obvious rhythm at 3x3 is a failed tile.

If the seam is right but a feature repeats too visibly, the fix is usually a rerun with stronger
uniformity language rather than an edit, since removing the feature locally reintroduces a seam.

## Material maps

A texture for a lit engine scene usually needs more than colour. Where a model declares PBR or
material outputs, take them in the same run rather than deriving normals from the colour map
afterwards, which produces flat-looking surfaces. `get_base_model` is the authority on what a given
model returns.

Pixel-art tiles carry these rules plus their own: see `layer-pixel-art`.

## Worked example

"A seamless mossy stone floor for our dungeon."

1. `list_base_models` with `filter.use_case: "text_to_image"` and
   `filter.capabilities: {tileability: true, square: true}`. Take the first result. Without
   `tileability` this run is wasted.
2. `get_base_model`, to see whether it exposes a tiling parameter that must also be set, and what
   material outputs it offers.
3. Prompt: "Seamless tileable texture of worn dungeon flagstones with moss in the joints, covering
   roughly 2 metres square with about eight stones across. Even diffuse flat lighting, no directional
   shadows, no cast shadows. Uniform distribution of wear and moss across the whole tile, no focal
   point, no single dominant crack or feature. Top-down orthographic view."
4. Estimate, then execute with `batch_size: 4` so there are options.
5. Judge each candidate at a 3x3 repeat before choosing.

## Common mistakes

- Skipping the `tileability` filter, which no later step can compensate for.
- Omitting scale, so the tile is one enormous stone or a thousand tiny ones.
- Accepting directional lighting baked into the tile.
- A dramatic hero feature that becomes a visible grid when repeated.
- Judging the tile on its own rather than tiled at 3x3.
- Deriving normal maps from the colour map when the model could return them directly.
- Requesting a perspective view of a surface instead of a top-down orthographic one.
