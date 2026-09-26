---
name: scenario-wan
description: "Use when generating or editing video with Wan models on Scenario via MCP: text-to-video, image-to-video from a still, first and last frame brackets, extending a clip, instruction-based video editing, character motion transfer or person replacement (Animate), aspect ratio reframing, video outpainting, uploaded-audio sync or auto-generated audio, or multi-shot prompts with timing brackets. Keywords: Wan 2.7, 2.6, 2.5, 2.2, Alibaba, VACE, T2V, I2V, V2V, lip-sync, multiShots."
license: MIT
---

# Scenario Wan Video

## Overview

Wan, Alibaba's video family on Scenario, ships each job as its own member, and members a generation apart disagree on parameter names, not just numbers: pick the member with `search`, then treat `model_schema_get` as the contract before every run. Wan 2.7 Image is an image model, covered by the `scenario-image` skill.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Members by job (at authoring time):

| Job                                 | Member                | Required inputs                       |
| ----------------------------------- | --------------------- | ------------------------------------- |
| Text to video                       | 2.7, 2.6, 2.5 T2V     | `prompt`                              |
| Animate a still                     | 2.7, 2.6, 2.5 I2V     | `image` + motion `prompt`             |
| Extend a clip                       | 2.7 I2V               | `video` + `prompt` (excludes `image`) |
| Restyle footage                     | 2.7 Video Edit        | `video` + edit `prompt`               |
| Character performs a video's motion | 2.2 Animate (Move)    | `imageUrl` + `videoUrl`               |
| Swap the person in footage          | 2.2 Animate (Replace) | `videoUrl` + `imageUrl`               |
| Change aspect ratio                 | 2.2 Reframe           | `videoUrl`                            |
| Expand the canvas                   | 2.2 Outpainting       | `videoUrl` + `prompt`                 |

Parameters do not port across generations. At authoring time: the 2.7 generators take `resolution` (720p or 1080p) and whole-second `duration` from 2 to 15, with `aspectRatio` (16:9 through 3:4) on T2V only. 2.6 and 2.5 T2V instead take one `size` string such as `"1920*1080"`, with `duration` from a fixed grid (5, 10, or 15 on 2.6; 5 or 10 on 2.5), while their I2V members take `resolution`. Video Edit takes a 2 to 10 second source; its `duration` is optional and truncates. Reframe and Outpainting have no `duration`: length is `numFrames` (81 to 241) at `framesPerSecond` (5 to 30), and output matches the source only when `matchInputNumFrames` and `matchInputFramesPerSecond` are true (both default false). Outpainting guides new content with up to 10 `refImageUrls`.

On 2.7 I2V, `image` and `video` are mutually exclusive, and `endImage` (last frame) is only valid alongside `image`. Resolution and duration carry cost (1080p ran about triple 720p on 2.7 T2V at authoring time), so `dry_run` before batches.

## Prompt the member's job

T2V wants a full scene in natural language: subject action, one camera move, lighting, style tags. I2V wants motion only: the still already fixes look and composition, so re-describing it wastes the prompt. Video Edit wants instructions, one clear change per sentence with a precise target, plus preservation language ("keep subject identity and camera path"); `referenceImage` carries a target look. In-frame readable text is unreliable on every member; push artifacts into `negativePrompt` (Video Edit and Animate lack it).

2.6 alone does multi-shot: with `multiShots` true (the default, but active only while `enablePromptExpansion` is true), open with a global style line, then `Shot 1 [0-3s] ...`, `Shot 2 [3-7s] ...`, keeping characters and location continuous. `enablePromptExpansion` defaults true on the generators (helps thin prompts, adds latency) and false on Reframe and Outpainting.

## Where the audio comes from

The 2.7 generators always deliver audio: upload an `audio` file to drive it, or omit it and a synced track is generated from whatever sound the prompt describes, so prompt the ambience you want. On 2.6 and 2.5, audio comes only from an uploaded file (3 to 30 seconds, 15 MB or less at authoring time), which 2.6 lip-syncs. Video Edit's `audioSetting` decides the track: `origin` keeps the source audio, `auto` lets the model regenerate it. Animate carries the source track while `mergeAudio` stays true (the default).

## Worked example: bracket a shot between two stills

1. `search` with `target="models"`, `query="wan image to video"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_wan-2-7-i2v` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: exclusivity notes, caps, defaults.
3. `upload_asset` the opening and closing stills (see the `scenario` skill) for asset ids.
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"prompt": "She turns from the window and walks toward the door, coat swaying; slow push-in. Room tone and distant traffic, no music.", "image": "asset_open", "endImage": "asset_close", "duration": 5, "resolution": "1080p"}` for the cost estimate; re-estimate after changing duration or resolution.
5. Re-run with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and review motion and audio together.

## Common mistakes

- Combining `image` with `video` on 2.7 I2V, or passing `endImage` without `image`: the schema forbids both.
- Porting a 2.7 payload to 2.6 or 2.5 T2V: they take `size` (`"1280*720"` style), not `resolution` plus `aspectRatio`, and off-grid durations fail.
- Expecting Reframe or Outpainting to preserve length: defaults render 81 frames at 16 fps; set the two match flags.
- Outpainting's expand flags default to all four sides: set the unwanted directions (`expandTop`, `expandBottom`, `expandLeft`, `expandRight`) to false.
- Writing shot brackets with `enablePromptExpansion` false: `multiShots` is inert without it; no other member reads brackets.
- Re-describing the still or requesting content changes in an I2V prompt: I2V animates; Video Edit changes content.
