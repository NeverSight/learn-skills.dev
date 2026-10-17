---
name: sgdk-pixellab
description: Generate and refine Mega Drive game art through PixelLab MCP with native pixel dimensions, cohesive palettes, prompt iteration and SGDK asset validation. Use for new sprites, UI, tilesets, maps and title art, rather than importing existing art alone.
---

# SGDK PixelLab

Turn the game's art brief into a measurable asset contract before spending
credits. Preserve the artist's style; the included study demonstrates several
styles and does not define how another game should look.

## Before generating

Look for existing palettes, assets, camera conventions and art references in
the project. If palette/style preferences remain unclear, ask the artist.
When they have none, propose a few suitable [Lospec palettes](https://lospec.com/palette-list)
with previews. Read [palette planning](references/palettes-and-validation.md)
before converting one: a sixteen-color palette is not automatically a suitable
Mega Drive palette or a complete scene palette plan.

Establish the native canvas and occupied area, facing/projection, frame anchor,
transparency, palette role and intended background. A single object, terrain
sheet and full title illustration need different prompts. Read
[prompting and tool selection](references/prompting.md) for templates and the
live-tool limitations found in our trials.

Use the available PixelLab MCP tools and their current schemas. Check the
[official MCP docs](https://api.pixellab.ai/mcp/docs), tool receipts and account
balance when costs matter. Respect the user's generation allowance, including
candidate batches, animations and cleanup calls; stop before exceeding it.
Submit a small representative batch, inspect it, then change the specific
failure. More prompt prose is not a substitute for hard palette controls.
Do not repeatedly regenerate an almost-correct icon when a few exact edits
would finish it. Poll existing jobs instead of submitting duplicates.

## Review and finish

Inspect the original at actual size and an integer nearest-neighbor zoom.
Verify dimensions, silhouette, perspective, facing, alpha, palette and frame
alignment. Test sprites over their intended scenery. Preserve raw outputs,
exact requests, selected candidates and edits so the artist can see how the
final asset was obtained. Treat tile-edge similarity and isolated-pixel counts
as review hints; neither establishes that art is seamless or wrong.

For large gradients, compare clean color bands, authored dithering and gentle
ordered palette reduction when useful. Choose what looks right for the game.
Dithering is optional: it can obscure silhouettes, create scrolling shimmer,
look noisy and increase unique tiles. Avoid making it a default for sprites,
UI, flat areas or backgrounds where the undithered version reads better.

Do not smooth-resize larger art into the working dimensions. Regenerate or
rework on the native grid. Cropping empty canvas or adding transparent padding
is different from rescaling: verify that no subject pixels are lost and update
anchors deliberately. Quantize all related frames against the same explicit
palette, preserve opaque colors independently of transparent index zero, and
review the converted image again.

The self-contained [asset helper](scripts/art_pipeline.py) inspects, prepares
and validates indexed exports without resizing. Read its
[contract and validation guide](references/palettes-and-validation.md) before
using it; it supports a deliberately limited PNG subset. The basic exporter
uses one line; the optional background exporter assigns a planned line per
8×8 tile. It does not certify visual quality or an entire game's graphics
budget. Use the real ResComp and linked-resource checks after preparation.

Near-color cleanup or swaps are acceptable when they preserve the art brief.
Treat specifically requested colors as constraints; explain hardware rounding
and any proposed change rather than silently replacing them. Never use an
unrelated generic palette simply to make the asset pass validation.

## Optional hardware lighting

When palette reduction loses useful light/dark shades, consider shadow/highlight
with the artist. It spans generation, export and rendering: plan the effect and
sprite/VRAM budget before prompting; retain a base indexed image, lighting mask,
palette ownership and modeled preview; then integrate the matching SGDK priority
and sprite rules. A PNG alone cannot activate hardware lighting. Do not silently
make it the default or prescribe it as an art style.

The [tested background experiment](assets/color-study/SHADOW-HIGHLIGHT.md)
includes an optional converter and a toggled ROM. Its full-background sprite
mask is costly and deliberately narrow, not a general production importer.
Use it as an executable reference or adapt selective masks within the game’s
budget. Report both the visual result and its rendering cost. Consult
`sgdk-graphics` for broader rendering integration when available; the experiment
is self-contained and does not require another installed skill.

## Evidence and integration

[The prompt study](assets/prompt-study/README.md) includes exact requests,
raw outputs, all Pro candidate overviews, assessments, explicit corrections,
final assets and a local comparison gallery. Its findings are a small sample,
not a benchmark or a promise of repeatability.

The [expanded color study](assets/color-study/README.md) corrects the initial
gallery’s confusing design comparisons and tests four themed scene palettes.
It includes same-asset exports, source-derived palette proposals, per-tile
background lines and a buildable four-page showcase ROM.

The [Asterfall catalog](assets/asterfall/README.md) brings generated artwork
into a navigable JRPG mockup: intro/title, naming, mock saves, travel, four
locations, NPC dialogue and character menus. Its style and mock game rules are
illustrative. Reuse the preparation and palette-ownership patterns, not an
assumption that another game should share its look, music or framework.

Use `ewrogers/sgdk:latest`, pulled before validation, and verify resource syntax
in the selected image's `bin/rescomp.txt`. Budget actual frame tiles, palettes,
VRAM, transfers and hardware sprite pieces separately. Read
[integration checks](references/integration.md) for the tested boundaries.
`sgdk-assets`, `sgdk-graphics` and `sgdk-levels` can help with wider integration
when available; no other installed skill is required by these helpers.
