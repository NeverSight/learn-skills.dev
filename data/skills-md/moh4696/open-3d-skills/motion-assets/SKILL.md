---
name: motion-assets
description: Plans and generates the images and video clips an animated website needs with AI image and video models, without wasting money. Covers proposing the concept and asset list with exact prompts and costs before spending, keeping one style across every asset, start and end frames for clips that chain or loop, choosing a model by what it can do, calibrating cost, staying under rate limits, recovering failed jobs, fixing loops and outpaints, and logging every prompt so the project can be rebuilt. Use whenever a site needs generated heroes, characters, product shots, textures, background loops or camera-move clips, or when someone says "use Higgsfield", "use Runway", "use Kling", "use Veo", "generate the assets" or "animate this image".
---

# Motion assets

Generated assets make or break an animated site, and they cost real money per attempt. This skill is the production discipline around the models: decide everything that can be decided before spending, make every asset in one look, generate in the order that lets later assets anchor on earlier ones, check each one with numbers, and write it all down.

## Tools

| Script | What it does |
| --- | --- |
| `scripts/loop_check.py` | Scores how well a clip loops, finds the best loop point, trims and cross-fades it |
| `scripts/paste_back.py` | Puts the original pixels back into an outpainted image (outpainting re-renders the middle too) |

Related: `alpha-cutout` (clips that need transparency), `scroll-film` (`prep.py seams` scores joins between chained clips), `cursor-rig` (head-turn clips).

Needs Python 3.9+, `pip install numpy opencv-python-headless`, ffmpeg.

## Before spending anything

Write a short plan and show it to the person paying:

1. **The concept in two sentences**, and what moves on the page.
2. **The asset list**: every image and clip, its size and aspect, its role on the page, and its exact prompt.
3. **The model for each**, chosen by capability (table below), and **the cost** of each and in total. Calibrate first: run one still and one short clip, read what was charged, then estimate the rest from that. Plans and prices change; never quote a price from memory.
4. **What the visitor sees with reduced motion** and on a phone.

Get a yes, then generate.

## Choose models by capability

| You need | The model must support | Notes |
| --- | --- | --- |
| A clip that ends on a planned frame | Start frame **and** end frame | Essential for chained scroll films, head turns and loops |
| A seamless loop | Start = end frame | Then check with `loop_check.py`; models rarely land exactly |
| A pose or expression change on the same character | Image editing that holds framing | Compare to the source at full size: only the edited part may change |
| A transparent subject | Nothing special: shoot on a key plate | See `alpha-cutout`. A few image models return real alpha; video models do not |
| Wider artwork | Outpainting | It re-renders the original area: paste it back (`paste_back.py`) |
| Sharpness | Native resolution | Never upscale a clip and call it 1080p; encode what the model returned |

Observed while building with these models in 2026 (check current docs; behaviour changes):

- Video models drift a flat background colour within a single clip (pure magenta came back pale pink); key per frame.
- Models change small details mid-clip (a black cap turned green late in a serve). Watch the whole clip, not the first and last frames.
- Some higher resolutions and quality modes are gated by subscription plan. A rejected submission usually costs nothing: test the cheapest request that proves access.
- Rate limits are tight on many plans: two or three video jobs in flight. Submit in small batches and resubmit only the job that returned 429 once others finish.
- A "server not responding" error does not always mean no job was created. List recent jobs before resubmitting, or you pay twice.
- A request can come back as a suggested preset instead of a job; decline the preset and resubmit.

## One look across every asset

- Write a **style preamble** (medium, palette, light, lens, texture) once and prepend it byte-for-byte to every image prompt.
- Make one **hero still** first, approve it, then pass it as the style reference to every later image.
- Use **one video model for a whole chain** of clips. Each model has its own motion, colour and grain; switching mid-film shows as a style jump at the seam.

## Generation order

1. Stills: hero, then keyframes (every start and end frame of every clip), then supporting images. Review them side by side before any video.
2. Clips, each anchored on approved stills. For chains, anchor each clip's start on the **exact extracted last frame** of the previous clip, not on the still, so colour drift does not accumulate as a jump.
3. Check every clip: `loop_check.py` for loops, `scroll-film/scripts/prep.py seams` for chains, the whole clip by eye for detail drift.

Clip prompts that behave:

- Name the camera: "locked-off camera" or the exact move ("slow push in, no rotation").
- Name what must not move: "the body, background and lighting stay perfectly still".
- For loops: "constant, even motion; no slowing down at the end". Models ease to a stop by default, which hitches every loop. `loop_check.py` reports it.
- Repeat the plate colour for anything that will be keyed.

## Fixing instead of regenerating

| Problem | Fix |
| --- | --- |
| Loop jumps slightly | `loop_check.py clip.mp4 --fix loop.mp4` cuts at the best loop point; add `--blend 6` to cross-fade small drift |
| Loop jumps a lot (over ~8) | Regenerate with start = end frame and the constant-motion wording |
| Outpaint softened the subject | `paste_back.py original.png extended.png out.png` |
| Seam between chained clips | Regenerate the later clip from the extracted last frame of the earlier one |
| One detail changes colour mid-clip | Recolour that hue in post if it is isolated; otherwise regenerate |

## Log everything

Every generation goes in `prompts/asset-prompts.md` (and machine-readable in a JSONL log): the asset name, model, exact prompt, input images, settings, job id, cost, and which output was kept. It is the only way to regenerate one asset months later in the same style, and the honest record of what was AI-generated.
