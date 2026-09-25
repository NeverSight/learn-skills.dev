---
name: scenario-product-shots
description: "Use when producing product photography with Scenario from a real product photo: e-commerce packshots on white, transparent, or brand backgrounds, lifestyle scenes placing the product in an environment, hero shots for a landing page or marketplace listing, angle and colorway sets, relighting or shadow fixes, or any shot where the label, logo, and shape must stay exact. Keywords: product photo, packshot, e-commerce, lifestyle shot, compositing, relight, label fidelity, catalog."
license: MIT
---

# Scenario Product Shots

## Overview

The product is never generated. A text-prompted bottle ships a wrong label to a landing page; every credible shot starts from an uploaded photo of the real product, and fidelity is a gated check, not a hope. Two lanes cover most work: deterministic packshot tools (cutout, background, shadow, relight) and generative scene placement with an instruction-editing model. Connection and the core loop: see the `scenario` skill. Edit-model contracts: `scenario-image`. Deterministic tools: `scenario-image-editing`. Reading assets back: `scenario-asset-analysis`. Animating an approved still into an ad: `scenario-video-ads`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Need               | Route                                                                                                                                                                                                                             |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The source         | `upload_asset` the best photo available: sharp, evenly lit, whole product in frame (`search` `"uncrop"` finds tools that rebuild a clipped edge)                                                                                  |
| Fidelity checklist | `asset_analyze` the upload once, instructing an inventory of label text, geometry, materials, and colors; every later check reuses it                                                                                             |
| Packshot           | `recommend` with the packshot need in the user's own words (a cutout-and-stage tool with solid, transparent, or custom backgrounds, margins, and shadows was the authoring-time hit), or background removal plus your own compose |
| Lifestyle scene    | `recommend` with `capability="img2img"`, product photo as reference, preserve-first prompt, one scene per run                                                                                                                     |
| Relight            | `search` `"relighting"` (the authoring-time hit adjusts light, exposure, and mood, with a brand-color lock)                                                                                                                       |
| Upscale keepers    | `recommend` with the user's own words; product-tuned upscalers existed at authoring time                                                                                                                                          |
| Gate               | `asset_analyze` the outputs against the checklist: up to 10 ids in `images`, the saved checklist in `text_inputs`, the letter-by-letter brief in `instruction`                                                                    |

## The preserve-first prompt

Scene prompts subordinate the world to the product: "The exact can from the reference image, proportions and colors unchanged, the label reads 'SUMMIT COLD BREW', no other text, standing on a wet slate counter, morning side light, shallow depth of field." Name the placement, the surface, the light. What goes unstated drifts: "label unchanged" alone leaves the type to whatever the model resolves from the reference, so the preserve clause quotes the checklist's label copy (existing on-pack text only) and the gate reads it back letter by letter rather than trusting the render.

Shadows and reflections carry the realism: a cutout pasted without them floats. Prefer a stage tool that rebuilds shadows, or name one in the edit prompt ("soft contact shadow falling right").

## Worked example: one can, a packshot plus three scenes

1. `upload_asset` the studio photo, then `upload_asset_complete`: `asset_can`.
2. Build the checklist once with `asset_analyze` (write lane, contract in `scenario-asset-analysis`); the inventory lands as a text asset, so `asset_download` it and keep the text.
3. Packshot: `recommend` with the packshot need in the user's own words, `model_schema_get` the pick, then run it with `asset_can` in its image field, the background set to the brand hex, and margins per the marketplace's current spec (confirm specs with the user; unattended, take them from the task instructions, else keep the tool's defaults).
4. Scenes: `recommend` with `capability="img2img"`; on `next_step.type="ask_user"`, present the options (unattended, the task instructions name the pick, else `proceed`: `specialty.model_id` first, skipping a specialty whose `caveats` or `when_general_better` name the task at hand, then the top `ranked` entry, never one flagged `requires_plan_upgrade`). `model_schema_get` the pick, then three runs, each the preserve-first prompt with one scene clause and `asset_can` wired as the schema says (an array only under `array: true`).
5. `jobs_wait`, then gate all four outputs in one `asset_analyze` call, the saved checklist passed via `text_inputs` and an instruction to read the label back letter by letter. A drifted label fails the shot: re-run from `asset_can` with the preserve clause tightened (the quoted copy spelled letter by letter, "no other text" kept), never from the drifted output. Text the gate cannot resolve at output resolution is unverified, not passed: upscale and re-gate, or flag it in the delivery note.
6. Upscale the keepers, `asset_download` with `format="png"`, file the set in a collection.

## Common mistakes

- Generating the product from a text description because the photo seems easy to describe: the one unfixable error, since no edit restores a label that never existed.
- Compositing from a screenshot of a crop: fidelity caps at the source; ask for the original file, and when nobody can supply one, proceed with the best source at hand and flag the ceiling in the delivery note.
- Skipping the gate because it "looks fine": label drift hides at thumbnail size; the checklist compare reads letter by letter.
- Prompting prices, claims, or promo copy into the image: overlay them with `scenario-text-overlay`; regulations and locales change faster than plates.
- Removing the background and losing the real shadow with it: restage with a shadow-building tool or prompt a new one.
- One run with a batch count for "the same scene, four angles": per-angle clauses need one run each (`scenario-image`).
