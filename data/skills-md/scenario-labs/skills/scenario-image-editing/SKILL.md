---
name: scenario-image-editing
description: "Use when editing an existing image on Scenario through MCP with a tool model, not a new generation: upscale or enhance to 2x, 4K, 8K, super resolution, 3D LUT color grade, color correction, posterize, solarize, vignette, film grain, blur, sharpen, glow, chromatic aberration, oilify, cubism, crystallize, dodge and burn, tint, desaturate, expand or uncrop, reframe an aspect ratio, resize to exact pixels, slice tiles, contact sheet, split into layers, remove a background or watermark, vectorize."
license: MIT
---

# Scenario Image Editing

## Overview

Editing an existing image is a `model_run` on a tool model: one file in, a few numeric knobs, one or more assets out, nothing to prompt on most of them. Generating a new image, prompt-driven edits and masked inpainting are `scenario-image`; the same effects on footage are `scenario-video-editing`; stacking layers is `scenario-video-assembly` (Image Studio). Connection and the core loop: `scenario`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Two discovery lanes. A family is browsed with `search` (`target="models"`, `public=true`) by tag. A single utility is a capability, so it goes to `recommend` with `capability="img2img"` and the need in the user's own words, which names the purpose-built tool and prices it against the general editors; when it answers a utility job with general editors only, find the tool by name with `search` and `filters={"tags": ["tool"]}`, as the watermark row does:

| Need                             | Route                                                                                                                                                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The effects family               | `search`, `filters={"tags": ["Post Processing"]}` (40 hits, image and video)                                                                                                                                  |
| Upscale or enhance               | `search`, `filters={"tags": ["image-upscale"]}`                                                                                                                                                               |
| Cutouts, relight, layers, vector | `recommend`: at authoring time each lane returned its purpose-built tool ranked by measured cost and latency against the general editors, where `search` returned the same tools with nothing to rank them by |
| Watermarks, burned-in text       | `search`, `query="text remover"`, a name lookup: at authoring time `recommend` sent watermark removal to general instruction editors and missed the purpose-built Photoroom Text Remover                      |
| Tiles, sheets                    | none: `model_scenario-image-slicer`, `model_scenario-grid-maker` (fixed first-party ids, each Scenario's single deterministic tool for its job)                                                               |

Reframe ids below are authoring-time hits: re-discover them.

## The effects family

Eighteen effects share one shape, a required `image` file plus one to three knobs: blur, chromatic aberration, color correction, crystallize, cubism, desaturate, dissolve, dodge and burn, glow and bloom, grain, 3D color LUT, oilify, parabolize, posterize, sharpen, solarize, tint, vignette.

Ranges are per tool and unguessable. `posterizeThreshold` runs 0 to 1 (default 0.5) while Color Correction's `temperature`, `contrast` and `saturation` run -100 to 100 with `gamma` on 0.2 to 2.2, all from `model_schema_get`. Not every knob is a number: Grain takes a 22-value profile enum, a color temperature and a boolean, no strength control at all. Those profiles are looks, not intensities, and some soften instead of texturing: compare against the input rather than assuming grain landed. Grain's `grainColorTemp` (2000 to 10000) hides a sharper trap: the 6500 default is not neutral, and it warms the frame and lifts blacks harder than a restrained LUT pass does, so the texture step quietly re-grades what the grade step just set. Set it deliberately and judge the result against the graded input, not the original; which direction neutralizes it is unverified, so compare one frame each side of 6500 before a batch. Defaults disagree too: Color Correction's are no-ops (nothing set returns the input unchanged and still charges) where LUT and Posterize ship a visible default.

`lutStyle` holds 140+ exact strings, one of which contains a space (`cgc_look_teal and orange`), so copy them from the schema rather than retyping. Prefixes group them: `cgc_film_emulation_*` and `rec709_*` emulate film stocks, `cgc_log_to_rec709_*` expects log footage and will over-contrast an ordinary render, and the bulk of the list (`cgc_look_*`, `pond5_*`, `distant_land_*`, `shutterstock_*`) are look packs. Five bare presets sit outside every prefix, and one of them, `teal_orange`, is the model's default: leave `lutStyle` unset and the grade that lands is teal and orange, not neutral.

These finish inside `model_run`, returning `status: "success"` with the assets attached, so no `jobs_wait`. They are flat-priced: at authoring time every effect dry-ran at 1 CU whatever the input size (Resize Image at 2), so one `dry_run` stands for the family, where an upscale's price moves with output pixels. Chain them by passing one run's `asset_id` to the next. The pipeline order across this skill: reshape and upscale first (see the next section), then grade, then texture. Grain and sharpening are high-frequency effects that any later resize interpolates away, so they go last, at delivery resolution; a LUT is resolution-tolerant and sits on either side.

## Upscaling is a model family, not a knob

Upscalers are `img2img` models, many taking no prompt at all: discover with `filters={"tags": ["image-upscale"]}` (13 hits at authoring time). Fidelity upscalers (Topaz, Recraft Crisp) sharpen and enlarge what exists, the pick when output must stay on-model; creative ones (Magnific Creative, the Clarity pair) carry a creativity dial that invents detail and can redraw fine features, so compare against the source. Sizing comes only from `model_schema_get` and varies per model: a factor, a target resolution or megapixels, or just `image` with no dial (2x to 16x and 4K to 8K ceilings were typical, not bounds). Cost follows output pixels: `dry_run=true`, top-level on `model_run` and never inside `parameters`, prices the exact size before a batch. An upscale can also outrun `model_run`'s wait budget where the effects above never do: a modest one still returns `status: "success"` inline, a larger one returns `status: "in_progress"` and a job id for `jobs_wait`, re-called with any returned `pending_job_ids` as `job_ids`. Purpose-built variants protect seams on tileable textures and continuity on 360 panoramas: see `scenario-textures` and `scenario-skyboxes`.

## Expanding a canvas is four different tools

- **Reframe** (`model_scenario-gemini-reframe`): an `aspectRatio` enum plus a `resolution` tier (1K, 2K, 4K), so exact pixels are out of reach; optional `prompt`. The enum is approximate: `4:5` came back 1856x2304 (29:36), so a true ratio needs a Resize Image pass after it (`fit: "cover"`, so it crops the sliver instead of squashing).
- **Smart Reframe** (`model_scenario-smart-reframe`): `width` and `height` are required and exact, and it protects on-image text, brand marks and palette. `textDensity: "DENSE"` costs substantially more.
- **Photoroom Expand**: exact `outputWidth` and `outputHeight` up to 4096, plus a `seed`.
- **Photoroom Uncrop**: rebuilds a subject the frame edge cut off.

Resize Image (`model_scenario-resize-image`, a fixed first-party id: Scenario's single exact-dimension resize tool, so discovery would only re-derive it) is none of these: it scales pixels to `width` and `height` (one alone keeps the ratio) and never invents canvas; `fit` decides what an off-ratio box does (`contain`, the default, may land smaller than the box, `stretch` distorts, `cover` center-crops to exact dimensions).

Both reframes recompose generatively rather than filling canvas, and at tens of times an effect's price they are the chain's expensive step: `dry_run` them. They re-render, so reframe first and grade after: a grade or grain pass beforehand comes back partly reinterpreted.

## Cardinality

Effects take a scalar `image`. Resize Image (`images`, max 10) and Grid Maker (`images`, max 100) are `array: true`, where a bare id is silently dropped and the run succeeds having ignored it.

## Worked example: grade a key art, then export at size

1. `upload_asset` the file, then `upload_asset_complete` unless it went inline under ~100KB.
2. Reshape first: Resize Image to the delivery size, with `images` as an array even for the one file.
3. `model_schema_get` on `model_scenario-postprocessing-lut` (a fixed first-party id: Scenario's single deterministic LUT tool, so discovery would only re-derive it), pick a `lutStyle` from its enum, price it with `model_run` and `dry_run=true`, then run it with `lutIntensity` near 0.6 for a restrained grade.
4. Grain last, on that output, so its texture is sized for the shipping frame.
5. `asset_display` to review, `asset_download` to save.

## Common mistakes

- Reaching for an `image_edit` MCP tool, or for local ImageMagick or Pillow: the surface is `model_run` on tool models.
- Prompting an effect ("more posterized"): they read numbers only. Reframe and the layer extractors take text.
- Slicing or extracting layers before grading: both return one asset per piece, so every piece then needs its own run.
- Saving a traced SVG with `asset_download`: it comes back rasterized, so take the stored file from `asset_get`'s `url` with `curl -L`.
