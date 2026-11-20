---
name: restyle
description: Restyle or re-motion an existing clip with open-weights LTX (IC-LoRA depth/union control restyle, or LTX-2.5 motion guide from a reference video). Use when the user wants a clip redone in a new look while keeping its motion.
---

# restyle

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model. LTX weights are under the Lightricks LTX license, which is **not** an OSI-approved open-source license (it is open weights with use conditions), so read it before commercial use.

| Need | Workflow | Set |
|---|---|---|
| Keep the motion and change the look (depth-controlled IC-LoRA, with a Qwen-edited first frame) | `ltx_ic_lora_depth_restyle.api.json` | `src.video`, `pos.text` (look), `e_pos.prompt` (first-frame redraw), `lat.length` |
| Drive a photo with a reference clip's motion | `ltx25_motion_guide.api.json` | `199.file` motion clip, `200.image` photo, `950.file` mask, `1002.image` end key |

## Notes
- Use 24 GB+ of VRAM. On Google Colab use an A100.
- Video inputs go through `upload` too (the same endpoint takes any file).
- The restyle graph needs ComfyUI-VideoHelperSuite and comfyui_controlnet_aux (see requirements). `AudioAmplify` in the motion-guide graph comes from a pack that is unverified: run preflight.
