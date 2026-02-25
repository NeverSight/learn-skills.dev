---
name: comfyui-workflow-builder
description: Generate ComfyUI workflow JSON from natural language descriptions. Validates against installed models/nodes before output. Use when building custom ComfyUI workflows from scratch or modifying existing ones.
user-invocable: true
metadata: {"openclaw":{"emoji":"🔧","os":["darwin","linux","win32"],"requires":{"anyBins":["curl","wget"]},"primaryEnv":"COMFYUI_URL"}}
---

# ComfyUI Workflow Builder

Translates natural language requests into executable ComfyUI workflow JSON. Always validates against inventory before generating.

## Workflow Generation Process

### Step 1: Understand the Request

Parse the user's intent into:
- **Output type**: Image, video, or audio
- **Source material**: Text-only, reference image(s), existing video
- **Identity method**: None, zero-shot (InstantID/PuLID), LoRA, Kontext
- **Quality level**: Draft (fast iteration) vs production (maximum quality)
- **Special requirements**: ControlNet, inpainting, upscaling, lip-sync

### Step 2: Check Inventory

Read `state/inventory.json` to determine:
- Available checkpoints → select best match for task
- Available identity models → determine which methods are possible
- Available ControlNet models → enable pose/depth control if available
- Custom nodes installed → verify all required nodes exist
- VRAM available → optimize settings accordingly

### Step 3: Select Pipeline Pattern

Based on request + inventory, choose from:

| Pattern | When | Key Nodes |
|---------|------|-----------|
| Text-to-Image | Simple generation | Checkpoint → CLIP → KSampler → VAE |
| Identity-Preserved Image | Character consistency | + InstantID/PuLID/IP-Adapter |
| LoRA Character | Trained character | + LoRA Loader |
| Image-to-Video (Wan) | High-quality video | Diffusion Model → Wan I2V → Video Combine |
| Image-to-Video (AnimateDiff) | Fast video, motion control | + AnimateDiff Loader + Motion LoRAs |
| Talking Head | Character speaks | Image → Video → Voice → Lip-Sync |
| Upscale | Enhance resolution | Image → UltimateSDUpscale → Save |
| Inpainting | Edit regions | Image + Mask → Inpaint Model → KSampler |

### Step 4: Generate Workflow JSON

**ComfyUI workflow format:**

```json
{
  "{node_id}": {
    "class_type": "{NodeClassName}",
    "inputs": {
      "{param_name}": "{value}",
      "{connected_param}": ["{source_node_id}", {output_index}]
    }
  }
}
```

**Rules:**
- Node IDs are strings (typically "1", "2", "3"...)
- Connected inputs use array format: `["source_node_id", output_index]`
- Output index is 0-based integer
- Filenames must match exactly what's in inventory
- Seed values: use random large integer or fixed for reproducibility

### Step 5: Validate

Before presenting to user:

1. Every `class_type` exists in inventory's node list
2. Every model filename exists in inventory's model list
3. All required connections are present (no dangling inputs)
4. VRAM estimate doesn't exceed available VRAM
5. Resolution is compatible with chosen model (512 for SD1.5, 1024 for SDXL/FLUX)

### Step 6: Output

**If online mode**: Queue via `comfyui-api` skill
**If offline mode**: Save JSON to `projects/{project}/workflows/` with descriptive name

## Workflow Templates

### Basic Text-to-Image (FLUX)

```json
{
  "1": {
    "class_type": "LoadCheckpoint",
    "inputs": {"ckpt_name": "flux1-dev.safetensors"}
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {"text": "{positive_prompt}", "clip": ["1", 1]}
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {"text": "{negative_prompt}", "clip": ["1", 1]}
  },
  "4": {
    "class_type": "EmptyLatentImage",
    "inputs": {"width": 1024, "height": 1024, "batch_size": 1}
  },
  "5": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 25,
      "cfg": 3.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["1", 0],
      "positive": ["2", 0],
      "negative": ["3", 0],
      "latent_image": ["4", 0]
    }
  },
  "6": {
    "class_type": "VAEDecode",
    "inputs": {"samples": ["5", 0], "vae": ["1", 2]}
  },
  "7": {
    "class_type": "SaveImage",
    "inputs": {"filename_prefix": "output", "images": ["6", 0]}
  }
}
```

### With Identity Preservation (InstantID + IP-Adapter)

Extends basic template by adding:
- Load reference image node
- InstantID Model Loader + Apply InstantID
- IPAdapter Unified Loader + Apply IPAdapter
- FaceDetailer post-processing

See `references/workflows.md` for complete node settings.

### Video Generation (Wan I2V)

Uses different loader chain:
- Load Diffusion Model (not LoadCheckpoint)
- Wan I2V Conditioning
- EmptySD3LatentImage (with frame count)
- Video Combine (VHS)

See `references/workflows.md` Workflow 4 for complete settings.

## VRAM Estimation

| Component | Approximate VRAM |
|-----------|-----------------|
| FLUX FP16 | 16GB |
| FLUX FP8 | 8GB |
| SDXL | 6GB |
| SD1.5 | 4GB |
| InstantID | +4GB |
| IP-Adapter | +2GB |
| ControlNet (each) | +1.5GB |
| Wan 14B | 20GB |
| Wan 1.3B | 5GB |
| AnimateDiff | +3GB |
| FaceDetailer | +2GB |

## Common Mistakes to Avoid

1. **Wrong output index**: CheckpointLoader outputs `[model, clip, vae]` at indices `[0, 1, 2]`
2. **CFG too high for InstantID**: Use 4-5, not default 7-8
3. **Wrong resolution for model**: FLUX/SDXL=1024, SD1.5=512
4. **Missing VAE**: FLUX needs explicit VAE (`ae.safetensors`)
5. **Wrong model in wrong loader**: Diffusion models need `LoadDiffusionModel`, not `LoadCheckpoint`

## Reference Files

- `references/workflows.md` - Detailed node-by-node templates
- `references/models.md` - Model files and paths
- `references/prompt-templates.md` - Model-specific prompts
- `state/inventory.json` - Current inventory cache
