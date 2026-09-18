---
name: layer-video-timeline
description: "Use when assembling assets a user already has into one finished video with Layer: sequencing clips, adding transitions, overlaying text, captions, a logo or a CTA, layering music or voice-over, or cutting a trailer, ad, or promo from generated shots. Also when a multi-shot piece needs to become a single deliverable file. Keywords: video editor, timeline, assemble, stitch, sequence, concatenate, transitions, overlay, captions, CTA, trailer, montage, render."
license: MIT
---

# Layer Video Timeline

## Overview

`render_video_timeline` edits assets the user already has into one finished video: clips in
sequence, transitions between them, text and logo overlays, and layered audio.
`estimate_video_timeline_price` prices a render without rendering, and `get_generation_run` polls it.

These three are named directly rather than discovered because they are first-party Layer tools
rather than models, with no competing alternative in the catalogue.

This is an assembly step, not a generation step. It composites assets that already exist. Generating
the clips is `layer-video`, and the shots should be approved before any of them reach a timeline.

If a sibling skill named here is missing from your available skills, ask the user to install it
(`npx skills add layerai/skills --skill <name>`); unattended, proceed from tool schemas and flag the
gap.

## Check for a single-generation answer first

Before assembling, ask whether one video model could render the whole piece. A model that produces a
multi-shot sequence in one generation holds its own continuity across the cuts, which assembly cannot
do. Assembly is right when the shots must be individually approved, when they come from different
sources, or when the piece is longer than any model will render.

## Get the inputs right before rendering

Every clip, image, and audio file must already be in the workspace and referenced by `file_id`.
Generated assets carry one, so they feed the timeline directly. Local files upload first.

Two things to settle before the first render, because both are expensive to fix afterwards:

- **One aspect ratio and one resolution for the whole piece.** Clips generated at mixed ratios either
  letterbox or crop, and the crop is where a character's head goes missing. Decide the delivery
  format first, then generate the shots to it.
- **Audio duration against picture duration.** A track shorter than the cut ends in silence; a track
  longer plays over the end card. Trim intent belongs in the timeline, not in a reroll of the music.

## Cutting

Shot length carries pace. A montage that holds every shot for the same three seconds reads as a
slideshow, so vary it: short shots for energy, longer holds where the viewer must read something.

Transitions are a decision, not decoration. A straight cut is right most of the time. Use a
dissolve for a time or location change, and keep any one piece to a single transition vocabulary,
because mixing wipes, dissolves, and fades reads as unfinished rather than varied.

For a piece with a CTA, hold the end card long enough to read twice at the viewer's pace, not the
editor's.

## Overlays

Text overlays must survive the platform. Keep titles and CTAs inside the safe area, well clear of the
edges, since social players crop and overlay their own UI at top and bottom. Set type against a
plate, a scrim, or a deliberately quiet part of the frame rather than over busy motion.

Generated video is the worst possible background for small text. Where the deliverable has more than
a few words, favour a held frame or a plain plate behind them.

## Worked example

"Cut these five approved shots into a 20-second vertical ad with our logo and a CTA."

1. All five shots came from earlier runs, so they carry `file_id` values. Confirm they were all
   generated at 9:16, since mixing ratios here is the common defect.
2. Upload the logo if it is not already in the workspace, and pick up the music track's `file_id`.
3. Compose the timeline: five clips in order with straight cuts, the logo overlaid small in a
   consistent corner throughout, a CTA card held at the end, and the music layered under the whole
   piece.
4. `estimate_video_timeline_price` first. Present the table, and above 20 CUs wait for an explicit
   yes.
5. `render_video_timeline`, then `get_generation_run` at `poll_interval_seconds`.
6. Watch the result end to end before delivering. Check the cut points, that the music resolves
   rather than stopping dead, and that the CTA sits inside the safe area.

## Common mistakes

- Assembling when one model could have rendered the sequence with real continuity.
- Mixing aspect ratios across clips, then discovering the crop on delivery.
- Uploading assets that Layer already produced and that already carry a `file_id`.
- Holding every shot for the same duration.
- Mixing transition styles inside one piece.
- Putting small text over busy generated motion, or outside the safe area.
- Delivering a render without watching it end to end.
