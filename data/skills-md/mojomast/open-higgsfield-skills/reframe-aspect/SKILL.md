---
name: reframe-aspect
description: Reframe a finished clip to another aspect ratio (16:9 to 9:16, 1:1, 4:5) by outpainting video with an open-weights LTX-2.3 IC-LoRA in ComfyUI, instead of cropping. Use for multi-platform deliveries.
---

# reframe-aspect

Run with `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`, and upload inputs first with `comfy_client.py upload <file>`. Before the first run, check the server with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses are listed in `references/requirements.md`. Use open-weights models only. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license.

Use `ltx23_video_reframe.api.json`: set `1.file` to the clip, `12.value`/`13.value` to the target width and height (multiples of 32; the defaults are 480×864 for 9:16), `5138.text` to describe the extended area, and `5117.noise_seed`.

## When to use it instead of a crop
- Use it when the subject would be cut off by a center crop. Otherwise `film-assembly --aspect` (a crop) is cheaper.
- For a still, use `image-edit`'s outpaint graph. This skill is for video.
- Describe the *surroundings* in the prompt, not the subject, and keep the style words the same as the story bible's.
