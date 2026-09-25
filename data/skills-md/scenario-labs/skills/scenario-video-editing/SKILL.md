---
name: scenario-video-editing
description: "Use when editing footage that already exists on Scenario through MCP with a tool model instead of a new generation: 3D LUT grading, color correction, film grain, vignette, blur, sharpen, glow, tint, desaturate, posterize, solarize, cubism, crystallize, oilify, chromatic aberration or dodge and burn on a clip; trimming to a time range, splitting at cut points, reversing, resizing, re-encoding, frame extraction, image sequences, background removal, segmentation masks, subjects as layers."
license: MIT
---

# Scenario Video Editing

## Overview

Every image post-processing effect has a video twin, and each is a `model_run` on a tool model: one clip in, a few numbers, one clip out. Generating or restyling footage, lipsync, dubbing and upscaling are `scenario-video`; concatenating, compositing and captioning a cut are `scenario-video-assembly`; the still-image side is `scenario-image-editing`. Connection and the core loop: `scenario`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## The twin rule

A video effect's id is the image id with `-video` appended, its file field is `video` rather than `image`, and the knobs are identical: `model_scenario-postprocessing-lut-video` takes the same `lutStyle` enum and `lutIntensity` as `model_scenario-postprocessing-lut`. All eighteen have twins, from blur and color correction through oilify, posterize and vignette.

One twin differs: Dissolve (Video) blends the clip with a still `dissolveImage`, not a second clip; crossfading two clips is a concat transition.

## Quick reference

| Need                  | Model or query                                                           |
| --------------------- | ------------------------------------------------------------------------ |
| Grade or stylize      | `filters={"tags": ["Post Processing"]}`, plus the effect name as `query` |
| Trim to a range       | `model_scenario-video-cut` (`startTime`, `endTime`)                      |
| Cut into segments     | `model_scenario-video-split` (`cutPoints`; N points give N+1 clips)      |
| Rescale or re-encode  | `model_scenario-resize-video`                                            |
| Play a clip backwards | `model_reverse-video`                                                    |
| Frames out, frames in | `model_scenario-video-to-image-seq`, `model_scenario-image-seq-to-video` |
| Subjects as layers    | `model_scenario-video-layers-extractor`                                  |
| Masks, cutouts        | `recommend` with the need in the user's own words                        |
| Pull the audio track  | `model_scenario-audio-extract`                                           |

Extracted frames carry no index and share one `createdAt`, so their order exists only in the job row's `assetIds`, and that list has come back out of time order (a confirmed defect at authoring time). The extractor takes a scalar `video`; every frame is `extractAllFrames: true`, and `frameInterval` (default 24 at authoring time, about one frame a second on a 24 fps clip) applies only when that flag is off. Check that the row holds exactly the clip's `nbFrames` ids (`asset_get` reports it beside `frameRate`; a short row is a dropped frame, which no reordering fixes), then, before reassembling with `model_scenario-image-seq-to-video` or handing frames on, lay the returned ids into `model_scenario-grid-maker` in that order (a fixed first-party id: Scenario's single grid tool; its `images` field takes an array of 1 to 100 ids and ignores a bare id while the run still succeeds, so past 100 frames sheet in batches or raise `frameInterval`; set `columns`, default 3 and up to 20, so a batch reads as a near-square sheet) and read the sheet against the clip's free `firstFrame` and `lastFrame` and its motion; a frame that breaks continuity is out of place, and the corrected order travels as your own id list from then on. Never rebuild order from listings or timestamps, and a preview that runs backwards on a clean sheet is the assembler's `pingpong` flag, not the order.

A cutout with transparency never ships as mp4: at authoring time the removal models carried alpha only as WebM or ProRes 4444 MOV, so read the output-format enum off `model_schema_get` and agree the container with the user before pricing the run.

Effect lookups go through `search`, `target="models"`, `public=true`. The `model_scenario-` ids are constants: each is Scenario's single deterministic tool for its operation, so discovery would only re-derive it. `model_reverse-video` sits outside that set and is an authoring-time hit: re-discover it by name (`search` `query="video reverse"`).

## Cost follows the clip, so trim first

On the video twins the `video` input carries `cost_impact: true`, which the image versions do not: price tracks the footage rather than the settings. Trim to the frames that ship, then grade; `dry_run=true` prices a payload before it runs. Video tools also outlast `model_run`'s wait window, so launch with `wait=false` and follow with `jobs_wait`, re-calling it with the returned `pending_job_ids`. A client-side timeout on `jobs_wait` is as harmless as the server's own: re-call it with the same ids rather than treating the job as lost.

Checking costs nothing: `asset_get` returns `firstFrame` and `lastFrame` as their own asset ids, so `asset_display` one to confirm a grade before chaining another billable run onto it.

## Field names drift between neighbors

- Video Cut and the effect twins take a scalar `video`. Resize Video takes `video` as an `array: true` field capped at one item, where a bare id is dropped silently; its size is `width` and `height` in pixels, both optional, and one alone keeps the aspect ratio.
- The output format field is `outputFormat` on cut and split, `videoOutputFormat` on resize.
- `preserveAudio` defaults to true on cut, split and resize; the effects expose no audio field and pass the track through.
- Enum values are copied, not retyped: one `lutStyle` string contains a space.
- `asset_download` takes no `format` for a video: it converts image formats only. A GIF from the sequence tool is an image asset and takes `format: "gif"`; the `png` default flattens it to one frame.

## Resizing is not reframing

No tool model repaints a video's canvas. Resize Video takes `fit`: `contain` (default) fits the clip inside the target, `stretch` forces the size and distorts, `cover` fills the target and center-crops the rest. `cover` is the cheap way to an exact ratio when losing the edges is acceptable, but none of them gives a 16:9 clip a vertical frame with the whole picture kept, so that brief needs a decision before any spend, between two routes an order of magnitude apart in price.

- **Generative reframe** (`query="reframe"`, Luma Ray 3.2 Reframe and Wan 2.2 Reframe, `scenario-video` territory) outpaints past the frame and keeps the whole picture, at by far the highest price in such a job. Resolution ceilings bite: a schema can allow a vertical ratio and its top resolution tier separately yet reject the pair at run time.
- **Compositor** (Video Studio, cropping or pillarboxing onto a vertical canvas) is cheap but throws away width or adds bars, and its layer geometry is `scenario-video-assembly`'s contract rather than a one-line setting.

`dry_run` prices a payload without validating it, so either route can bill for a run that fails outright or returns a mis-composed frame at exactly the right dimensions.

## Worked example: a graded cutdown

Launch every `model_run` below with `wait=false` and retire it with `jobs_wait` before the next step reads its asset.

1. `asset_get` the master and read `properties.duration` before choosing times.
2. Trim: `model_scenario-video-cut` with `startTime` and `endTime` in seconds. Going first is what makes every later step cheaper.
3. Reshape: `model_scenario-resize-video`, `video` as a one-item array, `width` and `height` at the delivery size, `videoOutputFormat: "mp4"`. `fit` settles the shape at this step rather than later: `cover` lands an exact ratio once the edges are spendable, and a shape that has to keep the whole picture is the reframe decision above.
4. Grade: `model_schema_get`, then the LUT twin with `lutIntensity` near 0.6.
5. Texture: `model_schema_get`, then the Grain twin with `grainProfile` (a 22-value enum, default `kodak_portra_400` at authoring time) on that output, last, so its grain is sized for the delivered frame rather than resampled by a later resize.
6. `asset_display` the result's `firstFrame` to confirm the look, then `asset_download` with no `format`.

## Common mistakes

- Grading each source clip and then concatenating: grade the finished master once, or the shots drift apart.
- Reaching for local ffmpeg, or for an MCP tool named `video_edit`: the surface is `model_run` on tool models.
- Polling `job_get` in a loop instead of `jobs_wait`, whose timeout is not an error.
- Trusting a Grain profile to add grain: the 22 profiles are looks, not intensities, and some soften the picture instead. Compare a frame against the input.
