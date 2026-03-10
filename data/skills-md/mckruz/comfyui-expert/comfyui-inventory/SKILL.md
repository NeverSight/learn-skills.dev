---
name: comfyui-inventory
description: Discover and cache all installed ComfyUI models, custom nodes, and system capabilities. Works online (API queries) and offline (directory scanning). Use before generating workflows to verify available resources.
user-invocable: true
metadata: {"openclaw":{"emoji":"📦","os":["darwin","linux","win32"],"requires":{"bins":["pwsh"]},"primaryEnv":"COMFYUI_PATH"}}
---

# ComfyUI Inventory Skill

Discovers what's installed in the user's ComfyUI instance and caches results for workflow validation.

## Purpose

Every workflow generation MUST be preceded by an inventory check. This prevents:
- Referencing models that aren't downloaded
- Using nodes that aren't installed
- Exceeding VRAM limits

## Two Discovery Modes

### Online Mode (ComfyUI API Running)

Query the live server for authoritative information.

**1. System info:**
```bash
curl http://127.0.0.1:8188/system_stats
```
Extracts: GPU name, total VRAM, free VRAM, ComfyUI version.

**2. Installed nodes:**
```bash
curl http://127.0.0.1:8188/object_info
```
Returns all registered node classes with their input/output specifications.

**3. Installed models (per type):**
```bash
curl http://127.0.0.1:8188/models/checkpoints
curl http://127.0.0.1:8188/models/loras
curl http://127.0.0.1:8188/models/vae
curl http://127.0.0.1:8188/models/controlnet
curl http://127.0.0.1:8188/models/clip
curl http://127.0.0.1:8188/models/clip_vision
curl http://127.0.0.1:8188/models/upscale_models
curl http://127.0.0.1:8188/models/diffusion_models
```

### Offline Mode (Directory Scan)

When ComfyUI isn't running, scan the filesystem directly.

**Requires**: ComfyUI installation path (e.g., `C:\ComfyUI`)

**Scan directories:**
```
{ComfyUI}/models/checkpoints/    → .safetensors, .ckpt
{ComfyUI}/models/loras/          → .safetensors
{ComfyUI}/models/vae/            → .safetensors, .pt
{ComfyUI}/models/controlnet/     → .safetensors, .pth
{ComfyUI}/models/clip/           → .safetensors
{ComfyUI}/models/clip_vision/    → .safetensors
{ComfyUI}/models/upscale_models/ → .pth, .safetensors
{ComfyUI}/models/diffusion_models/ → .safetensors
{ComfyUI}/models/ipadapter/      → .safetensors, .bin
{ComfyUI}/models/instantid/      → .bin
{ComfyUI}/models/insightface/    → .onnx + folders
{ComfyUI}/models/facerestore_models/ → .pth
{ComfyUI}/models/ultralytics/bbox/ → .pt
{ComfyUI}/custom_nodes/          → folder names = node packages
```

**Custom node detection**: List directories under `custom_nodes/`. Each directory name corresponds to a node package (e.g., `ComfyUI_IPAdapter_plus`, `ComfyUI-Impact-Pack`).

## Cache Format

Save results to `state/inventory.json`:

```json
{
  "last_updated": "2026-02-06T12:00:00Z",
  "mode": "online",
  "comfyui_version": "0.3.10",
  "system": {
    "gpu": "NVIDIA RTX 5090",
    "vram_total_gb": 32,
    "vram_free_gb": 28
  },
  "models": {
    "checkpoints": ["flux1-dev.safetensors", "RealVisXL_V5.0.safetensors"],
    "loras": ["sage_character.safetensors"],
    "vae": ["ae.safetensors", "wan_2.1_vae.safetensors"],
    "controlnet": ["instantid_controlnet.safetensors"],
    "clip": ["t5xxl_fp16.safetensors", "clip_l.safetensors"],
    "clip_vision": ["CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"],
    "upscale_models": ["4x-UltraSharp.pth"],
    "diffusion_models": ["wan2.1_i2v_720p_14b_bf16.safetensors"],
    "ipadapter": ["ip-adapter-faceid-plusv2_sd15.bin"],
    "instantid": ["ip-adapter.bin"],
    "insightface": ["inswapper_128.onnx"],
    "facerestore": ["codeformer.pth"],
    "detection": ["face_yolov8m.pt"]
  },
  "custom_nodes": [
    "ComfyUI-Manager",
    "ComfyUI_IPAdapter_plus",
    "ComfyUI_InstantID",
    "ComfyUI-Impact-Pack",
    "ComfyUI-AnimateDiff-Evolved",
    "ComfyUI-VideoHelperSuite"
  ]
}
```

## Workflow Validation

Given a workflow JSON, validate against inventory:

```
For each node:
  1. Check class_type against known node classes
  2. If missing: identify which custom_node package provides it
  3. Suggest install: "Install via ComfyUI-Manager: {package_name}"

For each model reference:
  1. Check filename against inventory models of that type
  2. If missing: look up in references/models.md for download link
  3. Report: "Missing: {filename} - Download from {url} -> {path}"
```

## Common Node-to-Package Mapping

| Node Class | Package |
|-----------|---------|
| ApplyInstantID | ComfyUI_InstantID |
| IPAdapterUnifiedLoader | ComfyUI_IPAdapter_plus |
| FaceDetailer | ComfyUI-Impact-Pack |
| ReactorFaceSwap | ComfyUI-ReActor |
| AnimateDiffLoaderWithContext | ComfyUI-AnimateDiff-Evolved |
| VideoHelper* | ComfyUI-VideoHelperSuite |
| ControlNetApply* | comfyui_controlnet_aux |
| UltimateSDUpscale | ComfyUI_UltimateSDUpscale |
| VHS_* | ComfyUI-VideoHelperSuite |
| RIFE* | ComfyUI-Frame-Interpolation |

## Cache Freshness

- Cache is valid for **1 hour** during active sessions
- Invalidate cache when user installs new models/nodes
- Force refresh: `scan-inventory.ps1` or API re-query

## Integration

- Called by `comfyui-workflow-builder` before generating workflows
- Called by `comfyui-character-gen` (via agent wrapper) for model selection
- Called by `comfyui-troubleshooter` when diagnosing missing model errors
- Results stored in `state/inventory.json` for all skills to reference
