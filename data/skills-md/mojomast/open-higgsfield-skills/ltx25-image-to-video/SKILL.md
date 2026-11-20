---
name: ltx25-image-to-video
description: Animate a still into a shot with open-weights LTX-2.5 in ComfyUI (image-to-video with optional last frame, or text-to-video), including LTX's native audio latent. Use after a keyframe passes still-qa.
---

# ltx25-image-to-video

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license (it is open weights with use conditions), so read it before commercial use.

## Pick a graph
| Need | Workflow | Set |
|---|---|---|
| I2V, two-pass with latent upsampling (sharpest) | `ltx25_i2v_two_pass.api.json` | `395.image`, `364.text`, `356.width/height/length`, `338.noise_seed` |
| I2V from a start frame, with an optional last frame | `ltx25_start_frame_i2v.api.json` | `401.image` start, `402.image` last, prompt in `900.string_a`, `356.*` size and length |
| Text to video | `ltx25_t2v.api.json` | prompt in `900.string_a`, `356.*` |

## Rules
- `length` must be 8n+1 frames (97, 121 ...). Width and height must be multiples of 32. At 24 fps, 121 frames is about 5 s.
- Write the prompt for motion, not appearance: what moves, the camera move, and the pacing. The keyframe already carries the look.
- **Keyframe chaining:** use the last frame of shot N (extract it with ffmpeg `-sseof -0.05`) as the start frame of shot N+1 when two shots must cut together without a visible jump.
- Never change the sampler or sigma nodes. Leave the guider and `ManualSigmas` as they are.
- **Google Colab:** on a 24 GB L4, run the two-pass graph at 640x352 or the start-frame graph at 672x384.
