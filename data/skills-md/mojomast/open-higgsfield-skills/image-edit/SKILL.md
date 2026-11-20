---
name: image-edit
description: Edit a still with open-weights Qwen-Image-Edit in ComfyUI - instruction edits, new camera angles, push-in, coverage close-ups, relighting, and outpainting to a new aspect. Use for chat edits on keyframes and to build coverage from one master shot.
---

# image-edit

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model.

## Pick a graph
| Request | Workflow | Set |
|---|---|---|
| Any instruction edit ("make her coat red") | `qwen_edit_2511_instruct.api.json` | `41.image`, `100.prompt`, `106.seed` |
| New camera angle (2511 multi-angle LoRA) | `qwen_edit_2511_angles.api.json` | `41.image`, angle words go into the `120`-`122` string chain (`<sks>` trigger) |
| Rotate the camera, fast (8-step Lightning) | `qwen_edit_2509_angle_lightning.api.json` | `img1.image`, `pos.prompt` |
| Push in / close-up coverage | `qwen_edit_2509_pushin_lightning.api.json`, `qwen_edit_2509_coverage_lightning.api.json` | `img1.image`, `pos.prompt` |
| Relight (time of day, key light) | `qwen_edit_2509_relight.api.json` | `1.image`, `11.prompt` |
| Virtual try-on (person + garment image) | `qwen_edit_2511_try_on.api.json` | `41.image` person, `83.image` garment, `149.prompt`, `169.seed` |
| Four-angle set in one run | `qwen_edit_2511_angles_set.api.json` | `41.image`; angle words in `1120`/`2120`/`3120`/`4120` `.string_a` |
| Edit one layer (Qwen layered) | `qwen_edit_2511_layers_edit.api.json` | `1.image`, `13.prompt`, `18.seed` |
| Outpaint to a new aspect | `qwen_image_outpaint_format.api.json` | `1.image`, `7`/`8` aspect W:H, `9` long side, `37.text` |

## Rules
- Make one change per edit, and describe what must stay the same ("keep face, outfit and background unchanged").
- After an edit, re-run `still-qa` with the original image as `--ref`.
