---
name: scenario-side-view-game-kit
description: "Use when making the art for a side-scroller or 2D platformer: side-view pixel-art sprite sheets for a hero and ground enemies (run, walk, idle, attack, hurt cycles, air spin, jump and fall poses) and per-level layers (parallax background and midground, seamless wall texture, platform strip, props). Also use when a magenta key eats part of a sprite, a walk loop will not close, a slash trail keys into a solid block, generated textures do not tile, or poses on one sheet will not split."
license: MIT
---

# Scenario Side-View Game Kit

## Overview

A side-scroller needs two families of image assets no single generation gives: pixel sprites that animate cleanly on one feet line, and painted level layers that stack into parallax and repeat without seams. This route comes from a browser side-scroller made in one agent session (one hero, two ground enemies, five levels):

1. **Characters.** A text-to-image still with two poses on flat magenta (hero: rest and jump; enemy: rest and attack wind-up), reframed with headroom, then one 3 second image-to-video clip per cycle, the character running or walking "like a treadmill" in a pure side profile facing right. A local script keys the magenta, cuts a loop or one-shot window, and pixelates every cycle of a character onto one shared canvas and palette. Fall, wall cling, plunge and dash come from one pose sheet. Make one facing; the game mirrors it.
2. **Levels.** Per level, five renders in "richly detailed high-resolution pixel art" (background, midground, wall texture, platform strip, props), made into WebP layers locally.

The finish is local on purpose: keying, the loop search, the shared palette and the seamless cross-fade need pixels on disk, and the deliverables are game files. If the user wants the finished strips on the platform too, `upload_asset` them into a collection.

Connection, scope and the core loop: the `scenario` skill. Frame tools, GIF previews and engine slicing: `scenario-sprite-animation`. Pixel cleanup and other statics: `scenario-game-assets`. Clip model families: `scenario-video`. Music and sound effects are outside this image skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

The agent runs the scripts locally (Python 3, Pillow, NumPy; `side_sprites.py` also needs ffmpeg): [reframe_stills.py](scripts/reframe_stills.py) makes the clip first frames, [side_sprites.py](scripts/side_sprites.py) builds the strips and imports [sprite_cycles.py](scripts/sprite_cycles.py) (never run directly), and [process_env.py](scripts/process_env.py) finishes the level layers. Prompts with slots: [references/prompt-templates.md](references/prompt-templates.md). Read [references/processing-settings.md](references/processing-settings.md) before changing a script flag or when `--report` flags a loop.

## Quick reference

| Step               | How                                                                                                                                                                                 | Keep when                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Models             | `recommend` with `capability: "txt2img"` (stills, pose sheet, layers) or `"img2video"` plus `features: ["endImage"]` (clips), the user's words as `prompt`; then `model_schema_get` | You know each schema's field names, enums and caps           |
| Reframe and upload | `reframe_stills.py`: figure 58% of a 960 square, feet at 82%; `upload_asset` + `upload_asset_complete` the rest frame, and the action frame for the hero's air spin                 | Headroom for a raised weapon or a somersault                 |
| Pose sheet         | Text to image, chosen still as reference, 4 poses in a row on magenta                                                                                                               | Same design and palette as the strips                        |
| Price and wait     | `dry_run: true` per distinct payload, then `wait: false` for the batch and `jobs_wait`, re-called with `pending_job_ids` until done                                                 | The user heard the total before spending                     |
| Strips             | `side_sprites.py --report`, then without `--report`                                                                                                                                 | Loop seams (idle aside) under 0.6x baseline; no solid blocks |
| Level layers       | Five renders per level, level 1 first                                                                                                                                               | Dark lower middle, empty midground center, props apart       |
| Level finish       | `process_env.py --env env --out assets --levels N`                                                                                                                                  | Texture tiles, ledge trims flat, prop count matches          |
| Deliver            | Strips and pose images as lossless WebP plus `<name>_meta.json` (cell, feet anchor, fps); layers as lossy WebP                                                                      | One anchor per character; nothing magenta at the edges       |

Payload names below (`startImage`, `endImage`, `referenceImages`, `background`, `quality`, `numOutputs`, `cfgScale`) are the build's schemas' examples: use the fields your pick's `model_schema_get` lists. The image pick needs strong layout adherence, a reference-image input, a transparent-background option and the template's 1536x1024; if its schema lacks one (a pixel-art specialty pick can cap far below that size), take the next ranked pick, even when `recommend` asks you to choose between such capped picks.

## Worked example

A user asks: "Make the art for my side-scroller: a fox knight hero with a rapier, a mole miner enemy with a pickaxe, and two levels, a mushroom forest and a crystal mine." Pass `team_id` and `project_id` on every call (the `scenario` skill covers picking them).

1. **Hero still.** `recommend { "capability": "txt2img", "prompt": "<the user's request>; needs reference image input, transparent output" }`, `model_schema_get` the pick, price the [two-pose template](references/prompt-templates.md#1-two-pose-still-text-to-image) (left: standing ready facing right; right: mid-jump facing right) with `model_run { "model_id": "<pick>", "dry_run": true, "parameters": { "prompt": "...", "width": 1536, "height": 1024, "quality": "high", "background": "opaque", "numOutputs": 2 } }`. Tell the user the price, run (`jobs_wait` with its `job_id` if it returns in progress), `asset_display` both takes; keep one with both poses on model, in a pure side profile (every clip inherits a three-quarter body), and nothing pink or purple, `asset_download` it and `curl -L` it to `fox_two_pose.png`.

2. **First frames.** `python3 scripts/reframe_stills.py fox_two_pose.png --name fox --out frames` writes `frames/fox_rest.png` (left pose, the first frame of every ground clip) and `frames/fox_action.png` (the jump). Check both, then `upload_asset { "file_name": "fox_rest.png", "content_type": "image/png", "kind": "image", "file_size": <bytes> }`, PUT the parts, `upload_asset_complete { "upload_id": "<id>" }`; same for the action frame, which only the air spin uses.

3. **Hero clips.** `recommend { "capability": "img2video", "features": ["endImage"], "prompt": "<the user's request>; square clip, no audio" }`, then `model_schema_get`. One payload per cycle from the [motion templates](references/prompt-templates.md#2-motion-prompts-image-to-video). With the build's schema:

   ```
   run:  { "prompt": "<run sentence> <facing and tail>", "negativePrompt": "<negative>, slowing down, stopping, standing still",
           "startImage": "<fox_rest id>", "duration": "3", "aspectRatio": "1:1", "generateAudio": false }
   atk1: { "prompt": "<attack: a fast rapier thrust ... returns to the starting ready pose> <facing and tail>", "negativePrompt": "<negative>",
           "startImage": "<fox_rest id>", "endImage": "<fox_rest id>", "duration": "3", "aspectRatio": "1:1", "generateAudio": false }
   ```

   Idle and hurt pin like the attack; the air spin uses the action id as both frames. Price each distinct payload with `dry_run: true` (first frame only, pinned, changed guidance), give the user the total, launch every clip with `"wait": false`, and collect them with one `jobs_wait { "job_ids": [...] }`, re-called with the returned `pending_job_ids` as `job_ids` while any is in progress (never poll `job_get`). `asset_download` each (omit `format` on video) and save as `clips/fox_<cycle>.mp4`, `<cycle>` being exactly the step 5 `--cycles` name (`run`, `idle`, `atk1`, `spin`, `hurt`). Review each as a local contact sheet (`ffmpeg -i clips/fox_run.mp4 -vf "fps=6,scale=240:-1,tile=6x3" fox_run_sheet.png`), since `asset_display` shows no frames of a video; re-run only one that turns toward or away from the camera or travels.

4. **Pose sheet.** Text to image with `referenceImages: ["<chosen still id>"]` and the [pose-sheet template](references/prompt-templates.md#3-static-pose-sheet) (fall, wall cling, plunge, dash). Price, tell the user, run, download as `fox_poses.png`.

5. **Strips.**

   ```
   python3 scripts/side_sprites.py --clips clips --name fox --cycles run:loop:8,idle:loop:8,atk1:attack:7,spin:attack:8,hurt:attack:5 --report
   python3 scripts/side_sprites.py --clips clips --name fox --height 56 --palette 28 \
       --cycles run:loop:8,idle:loop:8,atk1:attack:7,spin:attack:8,hurt:attack:5 \
       --poses fox_poses.png --jump frames/fox_action.png --webp --out sprites
   ```

   View the strips at 4x, nearest-neighbor. If the slash trail keyed into a white block, re-run with `--drop atk1=<index>` (0-based) and `--force`.

6. **Enemy.** Same route: two-pose still (rest, and an attack wind-up that keeps the design consistent), reframe, upload only `mole_rest.png`; walk with the first frame only, the [armed-enemy walk wording](references/prompt-templates.md#armed-enemy-walk) and a lower guidance such as `cfgScale: 0.7` if the schema has one; attack and hurt pinned. `side_sprites.py --clips clips --name mole --height 72 --cycles walk:loop:8,attack:attack:8,hurt:attack:5 --report`; a walk flagged as a weak loop gets `--range walk=12:48` before any re-run.

7. **Level layers.** Fill the five [environment templates](references/prompt-templates.md#4-environment-layer-set) for the mushroom forest (opaque background and texture, the rest transparent). `dry_run` each distinct setting, tell the user the total, run, download as `env/bg1.png`, `env/mid1.png`, `env/tex1.png`, `env/ledge1.png`, `env/props1.png`, then `python3 scripts/process_env.py --env env --out assets --levels 1`. Put level 1 in the game with the fox on it before generating the crystal mine; process that one alone with `--levels 2,` (a bare `2` is a count and redoes level 1), `--force` after a re-render.

8. **Check.** Play each strip at its fps from `<name>_meta.json`, tile the texture across a wall, and draw a long and a short platform.

## Common mistakes

- **An end frame on run or walk.** Pinning the still at both ends of short locomotion spends the clip speeding up and slowing down. First frame only for run and walk; pin first = last for idle and every one-shot so they return to rest.
- **An armed enemy's walk using its weapon.** The build's first armed walk swung its weapon mid-stride and closed at 1.44x baseline. "His arms stay still ... never lifts, swings or twirls it", the weapon terms in the negative and a guidance of 0.7 closed it at 0.42x.
- **Keeping a frame where an effect keyed into a block.** A white slash trail and an impact dust cloud came out of the key as solid blobs; `--drop` removes the sampled frame without changing the shared canvas or palette.
- **Paying to regenerate every weak loop.** A heavy walk closed at 1.03x, a wider range found the same window, and it shipped after review. Widen the range, look at the loop, and pay only when it visibly hitches.
- **Splitting a pose sheet by columns.** Poses overlap horizontally; split by connected components (`--poses` does) and ask for wide gaps.
- **Trusting "seamless tileable" in a texture prompt.** The renders do not tile reliably; `process_env.py` cross-fades opposite edges instead of a re-render.
- **Stretching a platform strip.** Draw left cap + repeated middle + right cap so every length keeps the carved ends.
- **Retro-scale level art.** Small retro paintings failed the first playtest; 1920x1152 detailed layers drawn at 2x replaced them while sprites kept nearest-neighbor scaling. Validate level 1 in the game before the rest.
- **Pink or purple on a character.** Everything strongly magenta is keyed away; say "no pink, no purple, no magenta anywhere on the character" and reject takes that show any. A fast weapon swing can pick up a purple motion-blur tint and key away mid-strike, which `--drop` cannot fix since it would remove the strike itself: reject that take, or re-run with "no motion blur, the weapon keeps its colors" in the prompt and "purple or magenta tint on the weapon" in the negative (in one validation run this cleared the tint, and one impact frame still needed `--drop`).
- **Rewording a blocked combat clip.** A thrust or pickaxe swing can come back `moderation_blocked`, and the filter is the provider's: read the error, then run the unchanged payload on a pick from another provider (same `recommend`, `endImage` feature kept) per `scenario-moderation` before softening the beat.
- **Lossy sprite strips.** Lossy WebP shifts the shared palette; only the HD layers ship lossy.
