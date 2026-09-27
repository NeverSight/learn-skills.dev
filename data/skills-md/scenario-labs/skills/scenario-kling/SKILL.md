---
name: scenario-kling
description: "Use when generating or editing video with Kling models on Scenario via MCP: text-to-video, image-to-video with first and last frames, multi-shot sequences with per-shot prompts, consistent characters via elements and reference images, prompt-based video editing, motion transfer from a driving video (motion control, mocap), lipsync to audio or text, talking avatars, native audio and dialogue, or picking 720p, 1080p, or 4K tiers. Keywords: Kling V3, O1, 2.6, Omni, Kuaishou, T2V, I2V, V2V."
license: MIT
---

# Scenario Kling Video

## Overview

Kling, Kuaishou's video family on Scenario, ships as specialists, eighteen at authoring time: V3 (Omni plus dedicated T2V and I2V tiers), O1, 2.6, motion control, lipsync, and a talking avatar. Pick the member whose conditioning matches the job, then treat `model_schema_get` as the contract: the same parameter changes shape, default, and legality between members. Kling Video to Audio is audio output, the `scenario-audio` skill's domain.

Connection and the core loop: see the `scenario` skill in this repo; model-agnostic video work: the `scenario-video` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Pick by job; discover ids with `search` (`target="models"`, `query="kling"`, `public=true`):

| Job                                        | Members                                                                 |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Every mode in one model, tier via `mode`   | V3 Omni (`standard` 720p, `pro` 1080p, `4k`)                            |
| Text to video at a fixed tier              | V3 T2V Standard / Pro / 4K, 2.6 T2V Pro                                 |
| Animate a still, optional last frame       | V3 I2V Standard / Pro / 4K, O1 I2V, 2.6 I2V Pro                         |
| Consistent characters from photos          | O1 Reference Images, V3 I2V `elements`                                  |
| Edit or restyle footage by prompt          | O1 Video Editing / Reference Video, Omni (`videoReferenceType: "base"`) |
| Motion from a video onto a character image | Motion Control (V3 Pro / Std, V2.6)                                     |
| Talking head                               | AI Avatar (image plus audio), Lipsync (video plus audio or text)        |

Schema traps (names from live schemas, caps at authoring time):

- V3 dedicated lines take `prompt` or `multiPrompt`, never both; `multiPrompt` is an array of `{prompt, duration}` shots, and `shotType` (`customize` or `intelligent`) exists only on the V3 T2V members and I2V 4K. Omni keeps `prompt` required; its `multiPrompt` is a JSON string of up to 6 shots whose durations sum to `duration`.
- `duration` is a string enum on most members (`"5"`, not `5`); Omni alone takes a number, 3 to 15. The V3 dedicated lines reach 15 seconds; O1 and 2.6 stop at 10.
- On O1 and V3 I2V an element is a `frontalImage` plus up to 4 angle `referenceImages`: both required on O1, each optional on V3 I2V, where a `video` can define the element instead.
- Budgets shrink beside a video: O1 Reference Images takes 7 total (elements plus images), the O1 video members 4, and Omni's `referenceImages` drops from 7 to 4 next to `referenceVideo`. Tags bind by order (`@Element1`, `@Image1`); Omni prompts use `<<<image_1>>>` and `<<<video_1>>>`.
- A reference clip runs 3 to 10 seconds on Omni and the O1 video members, 2 to 10 on Lipsync (trim first, per `scenario-video`). Omni's `referenceVideo` defaults to `videoReferenceType: "feature"`, lending style and camera to a new clip; `"base"` edits the clip and ignores `duration`; `4k` mode refuses a reference video either way.
- `cfgScale` (0 to 1, default 0.5): raise toward 0.8 for storyboard fidelity, drop toward 0.3 to let the model invent.
- Prompt in director order: scene, subject, action, one camera move, then audio and style; natural sentences beat tag lists, and complex scenes hold together near 5 seconds, not 15.

## Audio is a per-member switch

`generateAudio` defaults true on the V3 dedicated lines and 2.6 T2V, false on Omni and 2.6 I2V, and does not exist on O1 (editing members carry source audio via `keepAudio`). It is refused beside Omni's reference video and beside `lastFrameImage` on 2.6 I2V; the 4K members bill per second either way. Voice output is Chinese and English, other languages auto-translate to English: put dialogue in quotes in the prompt, lowercase for English speech, uppercase for acronyms. For new speech on existing footage use Lipsync: an audio file, or `text` with a `voiceId`, never both.

## Motion control reads two inputs

Motion members require a character `image` and a driving `video`; `characterOrientation` names which input holds the character and, on V2.6, caps the driving clip at authoring time: 10 seconds for `image`, 30 for `video`. Defaults differ (V3 Std says `video`, the others `image`), so set it explicitly. `keepOriginalSound` decides whether the source audio survives.

## Worked example: two-shot character clip from a still

1. `search` with `target="models"`, `query="kling image to video"`, `public=true`. Prefer the newest non-deprecated hit, e.g. `model_kling-v3-i2v-pro` (a live hit at authoring time: re-discover each session).
2. `model_schema_get` with that id: multiPrompt shape, duration values, element caps.
3. `upload_asset` the start frame and the character's frontal photo (see the `scenario` skill).
4. `model_run` with that `model_id`, `dry_run=true`, and `parameters={"startImage": "asset_s", "multiPrompt": [{"prompt": "Wide shot, @Element1 crosses the plaza, slow dolly-in", "duration": "5"}, {"prompt": "Close-up, @Element1 smiles and says: 'we made it'", "duration": "4"}], "generateAudio": true, "elements": [{"frontalImage": "asset_f"}]}` for the cost estimate; re-estimate after changing durations, tier, or audio.
5. Repeat `model_run` with `wait=false`, then `jobs_wait` with the returned job id, re-called with `pending_job_ids` on timeout, never a second `model_run`.
6. `asset_display` the output and review both shots with sound.

## Common mistakes

- Passing both `prompt` and `multiPrompt` to a V3 dedicated line: exclusive there (Omni alone keeps `prompt` required).
- Numeric durations: outside Omni, `duration` is the string `"5"`, not `5`.
- Expecting audio beside a last frame (2.6 I2V) or a reference video (Omni): exclusive pairs.
- Carrying one member's caps to another: 15 seconds, `elements`, and 4K each exist on one member, not the next.
- Compound camera moves ("dolly in while orbiting"): one dominant move per shot; split the rest across `multiPrompt` shots.
- Overloaded negative prompts: a short artifact list steers; a long one stiffens motion.
- Prompting Omni `base` to extend a clip: it edits in place, and no Kling member extends at authoring time. Continue from the clip's `lastFrame` id (`asset_get`) as the start frame of a new I2V run, then concatenate, per `scenario-video`.
- Skipping `dry_run` on 4K or avatar runs: at authoring time 4K ran several times Standard and avatar cost spanned a 100x range. Iterate on a Standard tier; no V3, O1, or 2.6 schema carries a seed, so a 4K re-run of the keeper is a new take, while upscaling it (`scenario-video`) keeps the take.
