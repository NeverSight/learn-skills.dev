---
name: layer-image-editing
description: "Use when changing an image that already exists on Layer rather than generating a new one: editing or replacing part of it, inpainting with a mask, outpainting or extending the frame, reframing to another aspect ratio, relighting, restyling, re-rendering from another camera angle, splitting into layers, removing a background, vectorising, or upscaling. Keywords: img2img, edit, inpaint, outpaint, mask, expand, turnaround, upscale, background removal, PSD, layers."
license: MIT
---

# Layer Image Editing

## Overview

Editing is not generation with an image attached. Each intent maps to its own `use_case`, and picking
the wrong one is the usual reason an edit changes things it should not have touched.

| The user wants                         | `filter.use_case`    | Attach                            |
| -------------------------------------- | -------------------- | --------------------------------- |
| Change one region, keep the rest exact | `inpainting`         | `init_image` plus a `mask`        |
| Change the whole image by instruction  | `image_editing`      | `init_image`                      |
| Extend past the current frame          | `reframing`          | `init_image`                      |
| Fit another aspect ratio               | `reframing`          | `init_image`                      |
| The same subject from another angle    | `multi_angle`        | `init_image` or `reference_image` |
| Separate, editable layers              | `split_into_layers`  | `init_image`                      |
| Cut the subject out                    | `background_removal` | `init_image`                      |
| More pixels, same picture              | `upscaling`          | `init_image`                      |
| Clean line art into finished art       | `image_editing`      | `lineart` or `scribble`           |
| A crisp SVG from a raster              | `vectorization`      | `init_image`                      |

The loop and the spend gate are in the `layer` skill. If a sibling skill named here is missing from
your available skills, ask the user to install it (`npx skills add layerai/skills --skill <name>`);
unattended, proceed from tool schemas and flag the gap.

## Edit from the source, not from the last edit

Every edit pass is a fresh generation that re-renders the whole image, so each one drifts a little:
colours shift, a face loses its likeness, a logo degenerates. Three passes stacked on each other look
visibly worse than one pass that does all three things.

So when an edit is wrong, go back to the original and write a better instruction. Do not correct the
correction. Output assets carry a `file_id`, so the original is always one argument away.

The exception is genuinely independent regions: masking the left lamp and then masking the right lamp
touches disjoint pixels and stacks cleanly.

## Masks

A mask marks what may change. Supply it as an uploaded `file_id`, or use the `for_transparency` and
`for_nontransparency` flags when the image's own alpha channel already describes the region, which
saves authoring a mask by hand for an asset that is already cut out.

Mask edges matter. A hard-edged mask on a soft-edged subject leaves a halo. When the boundary is hair,
smoke, or glass, prefer an instruction edit over a mask, because the model resolves the boundary
better than your rectangle does.

## What to hold constant

State it in the instruction. Models are literal about what you mention and careless about what you
do not, so "change the banner to red, keep the pose, lighting, and armour exactly as they are" is a
materially different instruction from "make the banner red". The clause costs six words and saves a
reroll.

## Angles are not a prompt trick

"The same character from behind" appended to a text-to-image prompt produces a different character.
Re-rendering an existing asset from another view needs `multi_angle`, a model whose capabilities
report `camera_transform`, and the view supplied through the structured `camera` parameter, which
orbits to side, back, or top, or zooms. Attach the source with the guidance type that model accepts.

## Upscaling

Upscaling adds resolution without changing what the picture depicts. It must never route through a
generation model: re-rendering at a larger size is a new image that merely resembles the approved
one, and approved art has to survive the step unchanged. Use `filter.use_case: "upscaling"`.

## Layers

`split_into_layers` produces genuinely separate, independently editable elements, for rigging,
parallax, or compositing. Before reaching for it, check what the user actually wants: "give me a PSD"
usually means "give me the art with a transparent background", which is `background_removal` and far
cheaper. Ask which one they mean when the request is ambiguous.

## Worked example

"Take this approved hero portrait and make a 9:16 version for the store."

1. The intent is `reframing`, not a reroll of the portrait. Generating it again loses the approval.
2. `list_base_models` with `filter.use_case: "reframing"`, take the first result.
3. The portrait came from an earlier run, so it already has a `file_id`. No upload.
4. `estimate_forge_price` with that file as `init_image`, the target ratio, and an instruction
   naming what must not change: "extend the scene above and below, keep the character, crop, and
   lighting untouched." Above 20 CUs, present the table and wait for an explicit yes.
5. `execute_forge` with exactly those arguments, then poll `get_forge_run` at
   `poll_interval_seconds`.
6. Present the result beside the original so the user can confirm the subject survived.

## Common mistakes

- Stacking edits on edits instead of returning to the source image.
- Using `image_editing` when only one region should change, then explaining the collateral damage.
- Omitting what must stay constant.
- Appending "from behind" to a prompt instead of using `multi_angle` with `camera`.
- Re-rendering an approved asset through a generation model to make it bigger.
- Reaching for `split_into_layers` when the user just wants a transparent background.
- Uploading an asset Layer already produced, which already has a `file_id`.
