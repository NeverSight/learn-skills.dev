---
name: scenario-video-assembly
description: "Use when generated clips must become a finished video on Scenario via MCP: cutting a shot list together, laying a timeline, concatenating with transitions, overlaying a logo or title card, adding a music bed or voiceover, burning in or exporting captions and subtitles, trimming and splitting, or producing vertical and square variants of one master. Keywords: edit, assemble, stitch, concat, compositor, timeline, layers, overlay, captions, SRT, ad, UGC, social cut."
license: MIT
---

# Scenario Video Assembly

## Overview

Scenario has no editing tools on the MCP surface. Every compositor, concatenator, trimmer and captioner is a deterministic model run through `model_run`. The compositor, concatenator and trimmer ids are fixed and named below; Scenario ships two captioners, so that one is discovered with `recommend`. Connection and the core loop: see the `scenario` skill; the clips themselves: see `scenario-video`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference: pick the backend first

| Need                                       | Model                          |
| ------------------------------------------ | ------------------------------ |
| Clips end to end, optional transitions     | `model_scenario-video-concat`  |
| Anything overlapping: overlay, bed, titles | `model_scenario-compose-video` |
| Still layout (thumbnails, sheets, key art) | `model_scenario-compose-image` |

These ids are constants: each is Scenario's single deterministic tool for its operation, so discovery would only re-derive it.

Concat is sequential: `videos` takes 2 to 50 files (never 1), `preserveAudio` (default true) carries each clip's own track into the cut, and the optional `transitions` array's "length must be number of videos - 1". Each entry is an object `{type, duration}`, never a bare string: `type` is one of 18 names read off the schema (`fade`, the default, is the plain crossfade; `dissolve` is a different effect; `none` a hard cut) and `duration` runs 0.1 to 5 seconds, default 0.5. Omit the array for hard cuts throughout, the right call whenever the brief does not ask one shot to flow into the next.

`preserveAudio` is not a guarantee of sync: a concatenated cut has come back with its audio drifting against the picture, with and without transitions (a confirmed defect at authoring time). A concat of clips carrying dialogue or effects is verified, never trusted: `asset_get` the output and compare `properties.duration` with the inputs' sum (each transition shortens the cut by up to its `duration`), then download it and check that the audio and video streams run the same length (a local probe of the download is inspection, not editing) and that a visible cue (a cut, a mouth opening, an impact) lands on its sound. When speech must stay locked to the picture, assemble in Video Studio instead: each clip layer carries its own track at its `startTime`, so a drift introduced by joining has nowhere to arise, at the price of hard cuts or per-layer fades in place of the transition set. Concat stays the tool for silent clips and for cuts whose bed is laid afterwards.

Video Studio is an absolute timeline: `layers` holds 1 to 50 image, video or audio sources placed by `startTime` and stacked by `zIndex` (higher in front), with per-layer `fadeIn`/`fadeOut` rather than a between-clip array, so a cross-fade between two clips belongs in concat. At least one layer must be a video, so a music bed over a still is rejected.

## The Video Studio contract

Per layer, three timing ideas have confusable names:

- `startTime` and `endTime` place the layer on the timeline.
- `trimStart` and `trimEnd` are amounts shaved off the head and tail of the source, not in and out points: to play the first 20 seconds of a 90-second track, set `trimEnd: 70`.
- `duration` overrides the layer's length. The top-level `duration` is a different field, setting the whole composition, and applies only when `durationMode` is `"custom"`.

Everything is in seconds at `step: 0.1`, so do not promise frame-accurate cuts. `x` and `y` are strings taking pixels, percentages or words, and `anchor` says which point of the layer they address: `top-left`, `top-center`, `top-right`, `center-left`, `center`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right` (the middle one is bare `center`), defaulting to `"top-left"`. A bottom-right logo is `x: "right"`, `y: "bottom"`, `anchor: "bottom-right"`, flush to the edge unless you inset it with a percentage.

`canvasMode` and `durationMode` both default to `"auto"`, computed from the layers: a custom frame is `canvasMode: "custom"` plus numeric `canvasWidth` and `canvasHeight` (there are no top-level `width`/`height`, and unlike the layers' string `width`/`height` these are numbers), and a custom length is `durationMode: "custom"` plus the top-level `duration`. `fit` only acts on a layer that also sets the layer's own `width` and `height`, strings like `x` and `y`: to reframe a clip, set both to the canvas size as bare pixel numbers in strings (`width: "1920"`, `height: "1080"`, the form of the schema's own `"0"` default; a percent string also works) and pass `"cover"` (crops) or `"contain"` (letterboxes), since the default `"fill"` stretches. Give an overlay layer an explicit `width` and `height` even at its native size: leaving them empty is documented as preserving the original but does not reliably, and a 560x80 strip came back at 1792x256 on a 1920x1080 canvas. The output field is `videoOutputFormat` here, `imageOutputFormat` in Image Studio, and `outputFormat` in concat and the trim utilities.

A layer's `type` (image, video, audio, or mask) is optional and otherwise inferred from `source`. There is no text layer, so titles, lower thirds and end cards arrive as rendered PNGs composited as image layers; `scenario-text-overlay` renders them letter-perfect.

## Worked example: three clips, a music bed, and captions

1. For every source, `asset_get` and read `properties`: the real `duration` (audio carries it too), `frameRate` on video, and `width`/`height` on video and images alike. A model asked for eight seconds does not always return exactly eight.
2. Add them up to get each clip's `startTime`, then `model_schema_get` on `model_scenario-compose-video`.
3. `model_run` it with `layers` holding the three clips at their computed `startTime`s (`zIndex: 0`), a logo PNG pinned by `x`/`y`/`anchor` at `zIndex: 1`, and the music as an audio layer trimmed to the clips' total with `trimEnd`, since auto `durationMode` computes from every layer, the bed included. `volume` (0 to 2) and `mute` are per-layer and apply to video layers too, so balance the bed from either side. Set `canvasMode: "custom"` with `canvasWidth` and `canvasHeight`; `fps` defaults to 30 and takes whole numbers from 1 to 120, so set it to the clips' measured `frameRate` when they agree (rounded), which is what step 1 read it for.
4. `jobs_wait`, then caption the finished cut rather than each clip: `model_scenario-caption-studio` (an authoring-time pick, since Scenario ships two captioners: re-discover with `recommend`) takes it as `video` and transcribes whatever audio the master actually carries, so lower the bed's `volume` rather than muting the dialogue. It burns captions in by default, takes an existing `.srt` as `subtitles`, a file input needing `upload_asset` first, returns a sidecar when `outputSrt` is true, and positions them with `textPosition` (`top`, `middle` or `bottom`, default `bottom`, so move it off a bottom-edge overlay).
5. `asset_display` to review, then `asset_download` with `format` left unset (it is an image conversion target) for the file.

Trim, split and resize have their own tool models. Note `model_scenario-video-cut`'s `startTime`/`endTime` are source in and out points, not timeline placement.

## Common mistakes

- Reaching for an MCP tool like `video_compose`, or for local ffmpeg to do the edit itself. The editing surface is `model_run` on tool models; probing a download is fine.
- Handing concat one clip, or one transition per clip: the minimum is 2 videos, and transitions run one fewer.
- Trusting `dry_run` here as validation: it returns a cost estimate only, and assembly payloads are the most structurally complex in the catalog.
- Captioning a concatenated master before checking its sync: the captioner times its lines to the audio it hears, so drifted audio ships drifted captions on top of it.
