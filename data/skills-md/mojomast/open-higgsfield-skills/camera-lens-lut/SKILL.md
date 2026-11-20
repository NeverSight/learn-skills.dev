---
name: camera-lens-lut
description: Apply film-style camera moves (handheld, push, drift), lens effects, a 3D .cube grade LUT and letterboxing to a clip in ComfyUI with the bundled Backlot node pack. Use as a finishing pass on generated shots.
---

# camera-lens-lut

Run every graph with the bundled client: `python scripts/comfy_client.py --url $COMFY_URL run workflows/<file> --set NODE.INPUT=VALUE --out out/`. Upload input files first with `python scripts/comfy_client.py upload <file>`. Before the first run on a server, check it with `python scripts/preflight.py --url $COMFY_URL workflows/<file>`. Node packs, model files, VRAM and weight licenses for this skill are in `references/requirements.md`. Use open-weights models only, and never swap in a hosted or closed model.

## Install the node pack (once)
Copy `assets/comfyui-backlot/` into `ComfyUI/custom_nodes/comfyui-backlot/` and restart. It is Apache-2.0, from Trenchplanet/mogfield; read its README for each node's inputs. Its seven looks are in `luts/` (anime_pastel, bleach_bypass, nature_doc, noir, scifi_cyan, tungsten_night, western). You can add your own `.cube` files there.

## Graph
`backlot_direct.api.json`: `1.file` input clip, `4` BacklotCameraRig, `5` BacklotLensKit, `6.lut` (a LUT filename), then the letterbox node, then `9` SaveVideo.

## Rules
- Use one LUT for every shot in a sequence. Pick it in the story bible.
- Keep camera moves subtle when the shot already has generated motion.
- This is post-processing only: it loads no generative weights.
