---
name: scenario-reel-recast
description: "Use when recreating a trending reel, TikTok or Short with a different performer: the same dance, moves, timing and camera, performed by the user's own character from a reference sheet, optionally in another outfit or a redecorated room, keeping the original song in sync. Keywords: reel recast, trend remake, TikTok dance, replace the dancer, character swap, choreography transfer, video to video, keep the music, Seedance edit mode."
license: MIT
---

# Scenario Reel Recast

## Overview

A recast performs an existing reel again with a new performer. Seedance's edit mode takes the reel
as `@video1` and keeps its choreography, timing, camera and framing, while the prompt changes who
dances, what they wear and how the room is dressed. The performer is rendered at the reel's scale,
so anything that brings its own camera breaks the result: a background plate shot from another angle
produces a performer with wrong proportions. The song never goes through generation: lift it off the
reel first, lay it back on the finals.

Recast only characters the user owns or has rights to, never a real person's likeness without their
consent; clearing the song for where it ships is the user's call.

Edit mode, references and moderation: `scenario-seedance`. Variations, review, ranking and the 1080p
finish: `scenario-seedance-drafts`. Plate edits: `scenario-image`. Timeline and sync:
`scenario-video-assembly`. Connection and the core loop: `scenario`. If a sibling skill named here
is missing from your available skills, ask the user to install it
(`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and
flag the gap.

## Quick reference

| Step               | Call                                                     | Detail                                                                                                                     |
| ------------------ | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Upload             | `upload_asset`, `upload_asset_complete`                  | Then `asset_get`: `duration`, `frameRate`, and the `firstFrame` asset id the plate starts from                             |
| Keep the song      | `model_scenario-audio-extract`, `outputFormat: "wav"`    | Returns inline                                                                                                             |
| Mute the reference | `model_scenario-video-cut`, `preserveAudio: false`       | `startTime: 0` and no `endTime` keep the whole clip; returns inline; probe the download to confirm no audio stream remains |
| Room plate         | Image edit of the reel's `firstFrame` (`scenario-image`) | Optional; see Changing the room, and check it before any video spend                                                       |
| Recast drafts      | Seedance edit mode, `"draft": true`                      | `referenceVideos: [muted reel]`, `referenceImages` in tag order, `duration: -1`, `generateAudio: false`; see Prompt recipe |
| Pick and finish    | `scenario-seedance-drafts`                               | Review every take, complete only the picks                                                                                 |
| Song back          | `model_scenario-compose-video`                           | A video layer and an audio layer, both at `startTime: 0`                                                                   |

The three tool ids are fixed: each is Scenario's single deterministic tool for its job, so discovery
would only re-derive them. Discover the Seedance member each session per `scenario-seedance`.

Plan from the output, not the source: at authoring time 30 fps reels came back at 24 fps (480x854
drafts, 1080x1920 completions) and a few frames off their length either way (14.87 s gave 14.71 s,
6.00 s gave 6.04 s), and edit-mode drafts priced 366 CU for 15 s, 148 CU for 6 s.

## Prompt recipe

This structure held identity, outfit and timing across three outfits and nine takes:

1. **The swap**: "Edit @video1: replace the dancing woman with the woman from @image1", plus
   "wearing the dress from @image2" and "redecorate the room as shown in @image3" when those apply.
   Tags follow `referenceImages` order: with no outfit image, the plate is `@image2`.
2. **The keep list**: "Keep from @video1 exactly: the room itself (walls, floor, window; with a
   plate, only its decoration changes), the camera position, height, lens and framing, her size,
   proportions and position in the frame, the light, and the choreography with every movement,
   gesture and head turn at the same timing."
3. **The sheet binding**: "@image1 is a character reference sheet of her: use it for her face, hair
   and outfit. Take nothing else from @image1: no panels, labels or text." The whole sheet works as
   one reference: no cropping into panels. When another image supplies the outfit, bind the sheet to
   face and hair only, and the outfit image to "only the dress: nothing of the mannequin, the
   background, the logos or any text".
4. **Keeping the reel's outfit**: "replace only the dancing woman's face and hair", with the outfit
   listed under the keep list.
5. **Named fragile details**: hair ("tied high at the crown, hangs down her back, keeps the same
   length, sections and color from the first frame to the last, never falls forward over her
   shoulder or blends into the curtains"), accessories ("the gloves stay black with natural
   fingers"), and props. Unnamed, they drifted: lace gloves vanished from one take, and a long
   ponytail draped forward.

## Changing the room

Outcomes at authoring time, best first:

- **Redecorate the reel's own room: works.** Edit the `firstFrame` with that frame as the only
  reference: remove the dancer, keep walls, floor, window, camera and light, add the decoration in
  words, keep the center floor clear, and set the output to the frame's own pixel size so the two
  overlay. Then overlay the plate on the frame locally
  (`ffmpeg -filter_complex "[0][1]blend=all_mode=average"`): walls, floor line and window must
  coincide within a few pixels, with no sideways shift, and the original dancer must fit the empty
  floor at her own size. Pass the plate as the last `referenceImages` entry: "this same room seen
  from this same camera, with only the decoration changed; the decorations are fixed props that stay
  in place behind her and never move, morph, multiply or overlap her."
- **A new location rebuilt from the frame**, the same single-reference edit with the place described
  in words: the camera held in the overlay, but the user rejected the result. Prefer redecorating.
- **A location plate from text-to-image**, or a plate edit given a second scene image as a
  reference: fails. The plate keeps its own camera (the second reference made the editor copy that
  scene's angle), Seedance renders the performer at the reel's scale on top of it, and the
  proportions break.

## Worked example: one reel, three outfits, a Halloween room

1. `upload_asset` the reel, `upload_asset_complete`, then `asset_get` it.
2. `model_run` the audio extractor and the muted cut. Download the cut and confirm it has a video
   stream only.
3. `recommend` with `capability="img2img"` and the decor in the user's words; edit the `firstFrame`
   as above, run the overlay check, and show the user the plate before any video spend (unattended:
   a passed overlay check is the gate, and a failed one stops the run before any draft).
4. Discover Seedance and `model_schema_get` it. `dry_run` one draft payload and quote N takes per
   outfit times that price.
5. Three payloads (the sheet outfit, an outfit image, the reel's own outfit), each sent N times with
   `"draft": true` and `wait=false`; `jobs_wait` all of them, re-called with the returned
   `pending_job_ids` until every row is done (7 to 8 minutes), never a second launch.
6. Give each draft a music review copy (step 8 recipe at the draft's length), then review per
   `scenario-seedance-drafts`, adding a timing check: the reel and the draft side by side at four
   matched timestamps.
7. Complete the picks with the draft job's own asset ids, never the music copies.
8. Compose each completion: the video and the extracted song as layers at `startTime: 0`,
   `durationMode: "custom"` at the completion's `duration` rounded down to the field's 0.1 s step,
   `canvasMode: "custom"` with numeric `canvasWidth` and `canvasHeight` at its size, `fps` at its
   frame rate. Then `asset_download` it and measure sync on that file (see Common mistakes).

## Common mistakes

- Muting, extracting or muxing the song with local ffmpeg: each step has a tool model above. Local
  ffmpeg is for inspecting downloads.
- Writing the new performer into the plate: it then sits in the background as a second figure. The
  plate is the empty room.
- Spending on video before the plate passes the overlay check.
- Expecting the source's frame rate and exact length, or composing to the source's duration: take
  both from `asset_get` on the output.
- Assuming the song lands in sync at 0: the offset varies per run (one recast's dance ran 83 ms
  early against a track 110 ms early, another's 57 ms late against an exact track). Measure it on
  the final: cross-correlate its audio envelope against the reel's, and its frame-difference motion
  envelope against the reel's. Line the song up with the dance, not the reel's audio: the compositor
  moves layers in 0.1 s steps, so keep whichever of song `startTime: 0.1` (dance late), song
  `trimStart: 0.1` (dance early) or neither leaves the smaller residual.
- Promising to keep an approved performer while changing only the room: every edit re-renders the
  performer, so a room change means new takes. Say so before spending (unattended: run the new takes
  from the approved prompt and report it).
