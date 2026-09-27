---
name: scenario-formats
description: "Use when one approved visual, image or video, must ship at many sizes or placements through Scenario: adapting a master to 1:1, 4:5, 9:16, or 16:9, social formats for feeds and stories, YouTube thumbnails, storefront capsules and app store graphics, marketplace product images, link previews, display banners, a website hero, or choosing between crop, resize, expand, and generative reframe. Keywords: aspect ratio, resize, reframe, outpaint, expand, derivative, safe zone, thumbnail, banner."
license: MIT
---

# Scenario Formats

## Overview

Format adaptation is derivation, not regeneration: re-prompting the concept per placement makes five cousins, not five formats of one approved master. The failure modes are picking the wrong operation (a resize where canvas needed inventing, a crop that beheads the subject) and deriving in the wrong order. The canvas tools' exact contracts live in `scenario-image-editing`; this skill is the decision ladder and the order of operations around them, with per-placement ratios, pixel targets, and safe zones in [references/placement-specs.md](references/placement-specs.md). A video master climbs the same ladder: video resize versus generative reframe lives in `scenario-video-editing`, and far ratios recompose per `scenario-video`. Connection and the core loop: see the `scenario` skill. Lettering per format: `scenario-text-overlay`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## The decision ladder

Per target format, take the first rung that fits. Each rung is a `model_run` on a model found with `search` (`target="models"`, `public=true`), never a dedicated MCP tool of its own:

| The target needs                             | Operation                                                                                                                           |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Same ratio, other pixels                     | Resize: exact, scales pixels, invents nothing                                                                                       |
| A tighter ratio, edges expendable            | Resize with `fit: "cover"`: exact, center-crops the overflow; only when the subject clears the cut                                  |
| More canvas, composition intact              | Expand or uncrop: exact pixels, fills outward                                                                                       |
| Another ratio, recomposed around the subject | Generative reframe; the text-protecting variant when lettering or marks are on the plate                                            |
| A far ratio or a new visual hierarchy        | Recompose natively: a fresh run per `scenario-image` with the master as reference (`scenario-consistency`), composed for that ratio |

The last rung applies more often than it looks: 16:9 key art seldom survives to 9:16 by any amount of outpainting, which is why the director siblings (`scenario-video-ads`) design each delivery ratio as its own composition.

## Order of operations

1. Approve one master first, at the largest clean size available, on a text-free plate (unattended, the task's named master or the brief's own description stands in for the approval).
2. Derive every format from that master, never from another derivative: derivative-of-derivative compounds re-rendering artifacts.
3. Reframe and expand before grading and grain: generative canvas work re-renders the image, so finishing passes applied first come back partly reinterpreted (`scenario-image-editing` holds the pipeline order). A video reframe also precedes any upscale: it renders at its own resolution tier whatever the input carries (1080p at most at authoring time), so an upscale ahead of it is discarded; upscale the reframed clip to delivery size.
4. Verify by measurement before finishing: reframe ratio enums are approximate (a 4:5 request came back 29:36 at authoring time), so check output dimensions, land exact with a resize, and batch-check that subjects survived with `asset_analyze` (`scenario-asset-analysis`).
5. Letter last: re-overlay lettering per format with `scenario-text-overlay`, sized to each final canvas, since type scaled by a resize turns soft and each placement has its own safe area. Keep critical content and text away from the edges platform UI covers: each placement's target and safe zone is in [references/placement-specs.md](references/placement-specs.md) as an authoring-time value, so confirm contractual specs with the user (unattended, task instructions win over the reference, and the delivery report states which was used).

## Worked example: key art to story, feed, and thumbnail

1. Master: 16:9 text-free key art, approved.
2. 1:1 feed: generative reframe with a prompt naming what must stay ("the knight centered, both banners visible"), then a resize pass to the exact deliverable pixels.
3. 9:16 story: a far ratio, so recompose natively: one run per `scenario-image` with the master as reference and a 9:16 composition clause; the master holds palette and subject on-look.
4. Thumbnail: readability rules the crop, so reframe tight on the face or product, land exact with a resize, then `asset_display` the result and judge it small: thumbnails are seen at a tenth of their size.
5. Verify dimensions against the deliverable list and batch-check that subjects survived with one `asset_analyze` pass, then overlay the title card per format onto each final canvas and file the set in a collection.

## Common mistakes

- Re-prompting per format: five generations of one prompt are five different images; derive from the master.
- Stretching into a new ratio with a resize (`fit: "stretch"`): it distorts. A ratio change is `fit: "cover"` when the edges are expendable, else reframe, expand, or recomposition.
- Grading and grain before reframing: the order is reshape, then grade, then texture.
- Deriving from the lettered master: generative operations re-render type; keep a text-free plate and re-overlay per format.
- Trusting a ratio enum: measure the output and resize to exact.
- Center-cropping toward 9:16 because it is cheap: it is also how subjects lose their heads; the ladder exists to be climbed.
- Skipping `dry_run` on reframes: generative canvas work is the expensive step in the chain, tens of times an effect's price (`scenario-image-editing`).
