---
name: scenario-asset-analysis
description: "Use when finished Scenario assets have to give something back: a caption for a dataset or alt text, a reusable style description, a verdict against a brief, a canny, depth, pose, or segmentation control map for the next model, or the asset itself found again by text, tags, or visual similarity and filed into a collection. Keywords: caption, describe, analyze, QA, control map, find similar, reverse image search, semantic search, tag, collection."
license: MIT
---

# Scenario Asset Analysis

## Overview

Four tools read assets back instead of making new ones: three fixed-purpose, one open-ended. With `search` (default toolset) they answer the questions that come after a batch lands, which is where most of the work actually is: is this on brief, what look is this, what does this show, what can the next model condition on, where did last week's approved version go.

None of them are in the default toolset. Get schemas with `scenario_tools_search`, then run each through the executor matching its `permission`: `asset_caption` and `asset_describe` are read-class, `asset_analyze` and `asset_detect` are write-class. Or reconnect with `?toolsets=full`. Connection and scope: see the `scenario` skill in this repo. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Need                                 | Tool                    | Shape                                                             |
| ------------------------------------ | ----------------------- | ----------------------------------------------------------------- |
| A caption for one image              | `asset_caption` (read)  | `details_level`: `action` or `action+style`                       |
| A reusable look off one image        | `asset_describe` (read) | Returns a full description plus a promptable synthesis            |
| Anything else, in your own words     | `asset_analyze` (write) | `instruction` plus up to 10 `images` and 10 `text_inputs`         |
| A conditioning map for another model | `asset_detect` (write)  | `modality`, one of ten including canny, depth, pose, segmentation |

All four bill credits and all four take `dry_run: true` for an estimate first. Read-class does not mean free.

## The four facts that change the plan

- **`asset_analyze` batches.** One call carries up to 10 images against one `instruction`, so reviewing 200 assets is 20 calls, not 200. `num_outputs` (1 to 5) is unrelated: it returns several distinct answers to the same instruction, not one answer per image. Ask for a fixed per-image output shape in the `instruction` so the answers stay parseable.
- **`asset_detect` strips the background by default.** `remove_background` defaults to true, so a depth or pose map comes back with the frame's context already gone. Set it false whenever the map has to cover the whole image.
- **It reads a render, not the file.** On a vector or layered source it cannot confirm what the file is or report its exact values: one call called a 16-path SVG raster, shifted a `#101614` fill to `#131A18`, and missed an off-palette path. Parse the file for exact color and structure; the tool judges what the render shows.
- **Fixed beats flexible when it fits.** `asset_caption` and `asset_describe` are purpose-built and faster than instructing an LLM to do the same job. Reach for `asset_analyze` for classification, extraction, comparison, translation, or a verdict against a brief. One carve-out: for a structured pass/warn/fail verdict against a configured brand brief, teams with the Quality Gate add-on have a dedicated tool that stores its verdict and re-reads it free (see `scenario-quality-gate`); `asset_analyze` stays the route when the add-on is missing or the brief exists only as prose.

`asset_analyze` and `asset_detect` wait up to 180s and then hand back a `job_id`; carry on with `jobs_wait` as anywhere else.

## Finding an asset again

Retrieval is `search` with `target="assets"`, and at least one of `query`, `filters`, `filter`, `image`, or `images` must be set: an empty call is a 400, not an everything-list.

- **By text.** `query` is keyword matching by default; `query_semantic_ratio` moves it toward meaning (0.5 to 0.8 suits mood queries like "dark medieval atmosphere", 1 is pure semantic). `sort_by` (say `["createdAt:desc"]`) is ignored while that ratio is above 0, so a newest-first list needs keyword mode.
- **By similarity.** `image` takes one asset id or image URL and returns lookalikes; `images` takes `{"like": [...], "unlike": [...]}` to steer with positive and negative examples (the two fields are mutually exclusive). `image_semantic_ratio` decides what similar means: 1, the default, matches subject and mood; 0 matches image features, the setting for hunting near-duplicates and crops. Add a `query` beside it for "like these, but more stylized".
- **By structure.** `filters` narrows on `kind`, `tags`, `model_id`, `collection_ids`, and `created_after`/`created_before`, ANDed with everything above.

## Worked example: reviewing a batch against a brief

1. Collect the asset ids from the run (`jobs_wait` returns them).
2. `asset_analyze` with `dry_run: true` on the first chunk to price the pass.
3. `asset_analyze` with `images` set to 10 ids and an `instruction` that states the brief and fixes the output: "For each image in order, reply `<index>: pass|fail, <reason in under 12 words>`, a reason on every line, passes included. Fail anything not centered, not on a plain field, or carrying text." Repeat per chunk. Answers land as text assets (one, or one per image): `asset_download` them to read the verdicts.
4. `asset_describe` on the strongest pass. Its promptable synthesis goes straight into the next batch's prompt, which holds the look without a training run (see `scenario-consistency`); when the synthesis is only a short title, prompt with the description instead.
5. File the result: `collection_create`, then `collection_add_assets` in chunks of at most 49 ids. `asset_add_tags` is additive, so tag the failures rather than rebuilding a tag set. The set comes back later with `search` `filters={"collection_ids": [...]}`, and its lookalikes with `images={"like": [...]}`.

## Common mistakes

- One `asset_analyze` call per asset when 10 fit in a call.
- Treating `num_outputs` as a batch size over `images`.
- Leaving `remove_background` at its default on an `asset_detect` map that must match the source frame.
- Running `asset_analyze` or `asset_detect` through `scenario_tool_execute_read`: both are write-class and the call is rejected by lane, not by argument.
- Sending more than 49 ids to `collection_add_assets`, or re-adding an asset already in the collection: both are hard errors, not no-ops.
- Asking `asset_analyze` to produce an image. It returns text; control maps come from `asset_detect` and final renders from `model_run`.
