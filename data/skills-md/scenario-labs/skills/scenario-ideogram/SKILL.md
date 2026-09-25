---
name: scenario-ideogram
description: "Use when generating or editing images with Ideogram models on Scenario via MCP: posters, logos, menus, packaging, or signage with exact in-image text, native transparent PNG generation with an alpha channel, background removal that keeps hair and glass edges, splitting a flat graphic into editable text layers for localization, or keeping one character consistent from a single reference photo, with inpainting. Keywords: Ideogram V4 and V3, typography, layerize, character reference, face swap."
license: MIT
---

# Scenario Ideogram Image

## Overview

Ideogram's image family on Scenario is five single-purpose members, not one model with modes: V4 for generation where in-image text must read, V3 Generate Transparent for native alpha output, V3 Layerize Text for turning a flat graphic into editable text layers, Character for one identity held across scenes, and Remove Background for cutouts. Mechanically they agree on almost nothing: the same concept changes name, casing, and allowed values between members, so discover each with `search` and treat its `model_schema_get` as the contract.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic image work (sizing families, reference cardinality, masks): the `scenario-image` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Pick the member by the job (names from the live schemas, caps at authoring time):

| Member                  | Job                        | Inputs that matter                                                                                                                                                                  |
| ----------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| V4                      | Text-heavy generation      | `prompt`, `imageSize` (six presets), `renderingSpeed` (TURBO, BALANCED, QUALITY), `enablePromptExpansion`, `acceleration`, `numOutputs` (up to 4), `seed`                           |
| V3 Generate Transparent | Native alpha output        | `prompt`, `negativePrompt`, `aspectRatio` (15 ratios), `renderingSpeed` (adds FLASH), `expandPrompt`, `numOutputs` (up to 8), `seed`                                                |
| V3 Layerize Text        | Flat graphic to layers     | `image`, optional `prompt`, `fontName*` or `fontFile*` per tier (H1, H2, Body, Small), `seed`                                                                                       |
| Character               | Same character, new scenes | `prompt`, `characterReferenceImage`, `styleType` (Auto, Fiction, Realistic), `aspectRatio` or `resolution`, `image` plus `mask`, `renderingSpeed` (Default, Turbo, Quality), `seed` |
| Remove Background       | Cutout to transparent PNG  | `image` (10MB cap)                                                                                                                                                                  |

Nothing transfers between members. Sizing is `imageSize` presets on V4 (`square_hd` is the largest), `aspectRatio` ratios on V3 Transparent and Character, and on Character alone an exact `resolution` that overrides the ratio. `renderingSpeed` values are uppercase on the two generators and Title case on Character, whose middle tier is Default, not BALANCED. Only V3 Transparent takes a `negativePrompt`. V4's `acceleration` buys speed on top of the tier at some quality cost; its default `none` is right for finals. Per-asset cost differs several-fold across members and moves with every `cost_impact: true` field, so `dry_run` the same job on the candidates before a batch.

## Exact text wants expansion off

Both generators rewrite the prompt before generating by default, which helps a short exploratory prompt and hurts the family's specialty: the rewrite can paraphrase the exact copy that must render. When the image carries wording, disable expansion (`enablePromptExpansion: false` on V4, `expandPrompt: false` on V3 Transparent), quote each piece of copy, and give it a place and a style ('the headline reads "GRAND OPENING" in bold condensed capitals across the top'). V4 renders multilingual text the same way: quote it.

## Two routes to transparency

Native: V3 Generate Transparent writes the alpha channel directly, so icons, stickers, and UI elements arrive compositing-ready. Cutout: generate on V4, then run Remove Background on the result; it reconstructs edge pixels with partial transparency rather than segmenting, so hair, fur, and glass survive. Go native when the asset is designed as an isolated element; go cutout when typography or overall quality leads, since at authoring time V4 scored well above the V3 line on public text-to-image arena ratings. Prompting "transparent background" on V4 does nothing: its outputs are opaque.

## Worked example: a localizable poster

1. `search` with `target="models"`, `query="ideogram"`, `public=true`. Members return as separate hits; match by name, e.g. `model_ideogram-v4` for typography (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: field names, allowed values, and defaults before anything else.
3. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"prompt": "Retro travel poster, warm dusk palette. The headline reads \"KYOTO IN BLOOM\" in bold serif across the top; caption \"April 2027\" bottom right.", "imageSize": "portrait_16_9", "renderingSpeed": "QUALITY", "enablePromptExpansion": false, "numOutputs": 2}` for the cost estimate.
4. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
5. `asset_display` the outputs and pick one.
6. To make the copy editable, discover the Layerize member the same way (`model_ideogram-v3-layerize-text` at authoring time), read its schema, and `model_run` with `parameters={"image": "<poster asset id>"}`: a generated asset's id feeds a file input directly, no re-upload. The output is a text-erased base plus text blocks with role, position, and content.
7. `jobs_wait`, then `asset_display` and `asset_download`.

## Common mistakes

- Carrying one member's block to the next: `imageSize` and `enablePromptExpansion` are V4's; V3 Transparent wants `aspectRatio` and `expandPrompt`.
- Leaving expansion on with exact copy in the prompt: the rewrite can change the words before the model sees them.
- Prompting a transparent background on V4: generate on V3 Transparent or chain Remove Background instead.
- Inpainting on Character with `image` but no `mask`: they go together (black repaints, white stays, mask resized to the image), `characterReferenceImage` stays required, and sizing fields are ignored while inpainting.
- Setting `fontNameH1` and `fontFileH1` together on Layerize: a tier's font comes from a font name or a font file, never both. `upload_asset` has no font kind, so with only a local font file use the font name route and flag the gap.
