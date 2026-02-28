---
name: comfyui-video-pipeline
description: Generate videos using ComfyUI with Wan 2.2, FramePack, or AnimateDiff. Handles image-to-video, text-to-video, talking heads, and motion-controlled animation. Use when creating any video content from character images or text descriptions.
user-invocable: true
metadata: {"openclaw":{"emoji":"🎬","os":["darwin","linux","win32"],"requires":{"anyBins":["curl","wget"]},"primaryEnv":"COMFYUI_URL"}}
---

# ComfyUI Video Pipeline

Orchestrates video generation across three engines, selecting the best one based on requirements and available resources.

## Engine Selection

```
VIDEO REQUEST
    |
    |-- Need film-level quality?
    |   |-- Yes + 24GB+ VRAM → Wan 2.2 MoE 14B
    |   |-- Yes + 8GB VRAM → Wan 2.2 1.3B
    |
    |-- Need long video (>10 seconds)?
    |   |-- Yes → FramePack (60 seconds on 6GB)
    |
    |-- Need fast iteration?
    |   |-- Yes → AnimateDiff Lightning (4-8 steps)
    |
    |-- Need camera/motion control?
    |   |-- Yes → AnimateDiff V3 + Motion LoRAs
    |
    |-- Need first+last frame control?
    |   |-- Yes → Wan 2.2 MoE (exclusive feature)
    |
    |-- Default → Wan 2.2 (best general quality)
```

## Pipeline 1: Wan 2.2 MoE (Highest Quality)

### Image-to-Video

**Prerequisites:**
- `wan2.1_i2v_720p_14b_bf16.safetensors` in `models/diffusion_models/`
- `umt5_xxl_fp8_e4m3fn_scaled.safetensors` in `models/clip/`
- `open_clip_vit_h_14.safetensors` in `models/clip_vision/`
- `wan_2.1_vae.safetensors` in `models/vae/`

**Settings:**
| Parameter | Value | Notes |
|-----------|-------|-------|
| Resolution | 1280x720 (landscape) or 720x1280 (portrait) | Native training resolution |
| Frames | 81 (~5 seconds at 16fps) | Multiples of 4 + 1 |
| Steps | 30-50 | Higher = better quality |
| CFG | 5-7 | |
| Sampler | uni_pc | Recommended for Wan |
| Scheduler | normal | |

**Frame count guide:**
| Duration | Frames (16fps) |
|----------|----------------|
| 1 second | 17 |
| 3 seconds | 49 |
| 5 seconds | 81 |
| 10 seconds | 161 |

**VRAM optimization:**
- FP8 quantization: halves VRAM with minimal quality loss
- SageAttention: faster attention computation
- Reduce frames if OOM

### Text-to-Video

Same as I2V but uses `wan2.1_t2v_14b_bf16.safetensors` and `EmptySD3LatentImage` instead of image conditioning.

### First+Last Frame Control (Wan 2.2 Exclusive)

Wan 2.2 MoE allows specifying both the first and last frame, enabling precise video planning:
1. Generate two hero images with consistent character
2. Use first as start frame, second as end frame
3. Wan interpolates the motion between them

## Pipeline 2: FramePack (Long Videos, Low VRAM)

### Key Innovation

VRAM usage is **invariant to video length** - generates 60-second videos at 30fps on just 6GB VRAM.

**How it works:**
- Dynamic context compression: 1536 markers for key frames, 192 for transitions
- Bidirectional memory with reverse generation prevents drift
- Frame-by-frame generation with context window

### Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Resolution | 640x384 to 1280x720 | Depends on VRAM |
| Duration | Up to 60 seconds | VRAM-invariant |
| Quality | High (comparable to Wan) | Uses same base models |

### When to Use

- Videos longer than 10 seconds
- Limited VRAM systems (but RTX 5090 doesn't need this)
- When VRAM is needed for parallel operations
- Batch video generation

## Pipeline 3: AnimateDiff V3 (Fast, Controllable)

### Strengths

- Motion LoRAs for camera control (pan, zoom, tilt, roll)
- Effect LoRAs (shatter, smoke, explosion, liquid)
- Sliding context window for infinite length
- Very fast with Lightning model (4-8 steps)

### Settings

| Parameter | Value (Standard) | Value (Lightning) |
|-----------|-----------------|-------------------|
| Motion Module | `v3_sd15_mm.ckpt` | `animatediff_lightning_4step.safetensors` |
| Steps | 20-25 | 4-8 |
| CFG | 7-8 | 1.5-2.0 |
| Sampler | euler_ancestral | lcm |
| Resolution | 512x512 | 512x512 |
| Context Length | 16 | 16 |
| Context Overlap | 4 | 4 |

### Camera Motion LoRAs

| LoRA | Motion |
|------|--------|
| v2_lora_ZoomIn | Camera zooms in |
| v2_lora_ZoomOut | Camera zooms out |
| v2_lora_PanLeft | Camera pans left |
| v2_lora_PanRight | Camera pans right |
| v2_lora_TiltUp | Camera tilts up |
| v2_lora_TiltDown | Camera tilts down |
| v2_lora_RollingClockwise | Camera rolls clockwise |

## Post-Processing Pipeline

After any video generation:

### 1. Frame Interpolation (RIFE)

Doubles or quadruples frame count for smoother motion:
```
Input (16fps) → RIFE 2x → Output (32fps)
Input (16fps) → RIFE 4x → Output (64fps)
```

Use `rife47` or `rife49` model.

### 2. Face Enhancement (if character video)

Apply FaceDetailer to each frame:
- denoise: 0.3-0.4 (lower than image - preserves temporal consistency)
- guide_size: 384 (speed optimization for video)
- detection_model: face_yolov8m.pt

### 3. Deflicker (if needed)

Reduces temporal inconsistencies between frames.

### 4. Color Correction

Maintain consistent color grading across frames.

### 5. Video Combine

Final output via VHS Video Combine:
```
frame_rate: 16 (native) or 24/30 (after interpolation)
format: "video/h264-mp4"
crf: 19 (high quality) to 23 (smaller file)
```

## Talking Head Pipeline

Complete pipeline for character dialogue:

```
1. Generate audio → comfyui-voice-pipeline
2. Generate base video → This skill (Wan I2V or AnimateDiff)
   - Prompt: "{character}, talking naturally, slight head movement"
   - Duration: match audio length
3. Apply lip-sync → Wav2Lip or LatentSync
4. Enhance faces → FaceDetailer + CodeFormer
5. Final output → video-assembly
```

## Quality Checklist

Before marking video as complete:
- [ ] Character identity consistent across frames
- [ ] No flickering or temporal artifacts
- [ ] Motion looks natural (not jerky or frozen)
- [ ] Face enhancement applied if character video
- [ ] Frame rate is smooth (24+ fps for delivery)
- [ ] Audio synced (if talking head)
- [ ] Resolution matches delivery target

## Reference

- `references/workflows.md` - Workflow templates for Wan and AnimateDiff
- `references/models.md` - Video model download links
- `references/research-2025.md` - Latest video generation advances
- `state/inventory.json` - Available video models
