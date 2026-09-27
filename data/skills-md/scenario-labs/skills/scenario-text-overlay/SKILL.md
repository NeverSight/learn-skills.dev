---
name: scenario-text-overlay
description: "Use when text must appear letter-perfect on generated media: taglines, CTAs, prices, legal supers, lower thirds, end cards, nameplates, or styled rich cards composited over Scenario images and video. Keywords: text overlay, text card, caption card, CTA, legal super, tagline, end card, lower third, price card, HUD text, transparent PNG."
license: MIT
---

# Scenario Text Overlay

## Overview

Generation models drift on type, so text that must be exact is rendered deterministically here and composited over the media. One JSON payload describes one overlay, in one of two kinds: a text layer (plain styled text in a box) or a rich layer (HTML/CSS typography: gradients, strokes, shadows, card layouts). Both substitute Mustache `{{variables}}` strictly (a missing variable fails the render) on a transparent canvas.

[scripts/overlay.py](scripts/overlay.py) renders the payload to a PNG with an installed Chromium-family browser (both kinds, discovered automatically) or a Pillow fallback (text layers only), embeds the payload JSON into the PNG, and prints the path. Its modules: [scripts/templating.py](scripts/templating.py) (strict Mustache), [scripts/html_render.py](scripts/html_render.py) (browser engine), [scripts/pillow_render.py](scripts/pillow_render.py) (fallback). The field-by-field contract and example payloads live in [references/payloads.md](references/payloads.md). The script needs `pip install chevron pillow`.

Connection and the core MCP loop: see the `scenario` skill. The overlay meets its content on the platform, never locally: `model_run` on the compose tool models, `model_scenario-compose-image` for stills and `model_scenario-compose-video` for video (fixed ids: each is Scenario's single deterministic compositor for its medium, so discovery would only re-derive them), whose layer contract lives in `scenario-video-assembly`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Step                    | Detail                                                                                               |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| 1. Write the payload    | Kind by field (`text_template` or `html_template`); every changeable string in `variables`           |
| 2. Render               | `python3 overlay.py --payload card.json --out card.png`                                              |
| 3. Verify               | Open the PNG: glyphs verbatim, box placement right, background transparent                           |
| 4. Upload               | `upload_asset` (kind `image`, multipart path)                                                        |
| 5. Persist the template | `asset_update` sets `metadata.description` to the payload JSON; `asset_add_tags` adds `text-overlay` |
| 6. Composite            | `model_run` on `model_scenario-compose-image` or `model_scenario-compose-video`, overlay on top      |

## Choose the face for its meaning

The face is part of the message: heavy condensed sans shouts (hooks, prices, CTAs), light geometric or grotesque sans reads neutral and premium (legal supers, lower thirds, nameplates), serif signals editorial or heritage weight, rounded forms read friendly and casual. Match the media's art direction rather than fighting it, keep one family per card, and build hierarchy with `font_weight` (100 to 900) and size instead of mixing faces. `font_family` reaches any Google Fonts family, so every class above is available by name; a contractual brand face rides `font_url` instead. Meaning survives only above legibility, so judge the flattened preview at destination size, where a subtle face turns generic.

## Worked example: a localized legal super

1. Payload, with the changeable line as a variable:

```json
{
  "text_template": "{{disclaimer}}",
  "variables": [
    {
      "key": "disclaimer",
      "value": "EPA-estimated 310 mi. Actual range varies."
    }
  ],
  "font_family": "Inter",
  "font_weight": 500,
  "size": 34,
  "color": "#FFFFFF",
  "align": "center",
  "bbox": [{ "x": 86, "y": 1560, "w": 908, "h": 120 }],
  "canvas_width": 1080,
  "canvas_height": 1920,
  "overflow": "shrink"
}
```

2. `python3 overlay.py --payload super.json --out super.png`, then open `super.png`: the line must read exactly as written, shrunk to fit the box.
3. Upload with `upload_asset`, then `asset_update` with the payload JSON as `metadata.description` and `asset_add_tags` with `["text-overlay"]` (`asset_update`'s own `metadata.tags` replaces the whole set): the template now lives on the platform beside its render, and the PNG itself carries it in a `tEXt` chunk.
4. Composite over the spot: `model_schema_get` on `model_scenario-compose-video`, then `model_run` with the base video at `zIndex` 0 and the super as an image layer above it (layer fields: `scenario-video-assembly`); `jobs_wait`, then `asset_display`.
5. The French variant is the same payload with one `value` edited, never a new template.

## Common mistakes

- Baking changeable strings into the template: variants and localizations should be edits to `variables`; the uploaded payload is the reproducibility contract.
- Using `{{var}}` for values holding `&`, `<`, or `>`: it HTML-escapes, so they render as literal entity text; `{{{var}}}` is the raw opt-out (full Mustache rules: the payload reference).
- Leaving images or fonts as remote URLs: inline them as `data:` URIs (Google Fonts links excepted) or the render depends on the network and drifts.
- Skipping the visual check before upload: font resolution differs per machine, and light text on the transparent canvas previews as blank; flatten over a contrasting backdrop first.
- Letting a generation model paint the text instead: generated type drifts frame to frame; overlays exist to avoid exactly that.
- Generating the plate with no room for the card: brief the base image or video with the overlay's zone kept plain and text-free (a dark right third, an empty top band) for every frame the card is up, so the composite lands on quiet pixels rather than generated lettering or detail.
- Merging the overlay locally with Pillow or ffmpeg: compositing is a `model_run` on the compose models, so the finished creative lands on the platform beside its layers.
- Sizing the canvas to something other than the destination: match the target resolution so the overlay composites 1:1 with no post-scale blur. Content layers may scale inside the compose run when a generation model cannot hit the exact size; the overlay must not.
- Expecting the fallback to match the browser: Pillow draws plain text only; rich layers need a Chromium-family browser installed.
- Trusting `wrap` with a hard box: it lets text spill below; use `shrink` (fits or fails loudly) or `clip` when the box is binding.
