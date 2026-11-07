---
name: alayarenderer-generative-world
description: AI coding agent skill for AlayaRenderer — a generative world rendering framework with inverse rendering (RGB→G-buffers) and game editing (G-buffers+text→stylized video) using fine-tuned video diffusion models.
triggers:
  - use AlayaRenderer to render a scene
  - run inverse renderer on video
  - game editing with G-buffers
  - stylize video with text prompt using AlayaRenderer
  - extract albedo normal depth from video
  - set up AlayaRenderer generative world renderer
  - fine-tune diffusion renderer for G-buffers
  - run Wan2.1 game editing inference
---

# AlayaRenderer — Generative World Renderer

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

AlayaRenderer is a two-stage framework for high-quality video rendering:

1. **Inverse Renderer** (RGB → G-buffers): Extracts albedo, normal, depth, roughness, and metallic maps from RGB video using a fine-tuned Cosmos-Transfer1-DiffusionRenderer 7B model.
2. **Game Editing** (G-buffers + Text → Stylized RGB): Synthesizes photorealistic, stylized RGB video from G-buffer inputs using a fine-tuned Wan2.1 1.3B model via DiffSynth-Studio.

---

## Installation

### Clone the Repository

```bash
git clone --recurse-submodules https://github.com/ShandaAI/AlayaRenderer.git
cd AlayaRenderer
```

> **Important:** Use `--recurse-submodules` — DiffSynth-Studio is a git submodule required for Game Editing.

### Two Separate Conda Environments (Recommended)

The two models have conflicting dependencies. Use separate environments:

```bash
# Environment 1: Inverse Renderer
conda create -n inverse_renderer python=3.10 -y
conda activate inverse_renderer
cd inverse_renderer
# Follow inverse_renderer/ instructions for Cosmos-Transfer1 setup

# Environment 2: Game Editing
conda create -n game_editing python=3.10 -y
conda activate game_editing
cd game_editing
# Follow DiffSynth-Studio setup instructions
```

---

## Model Weights

| Model | Base Model | Size | HuggingFace Link |
|---|---|---|---|
| Inverse Renderer | Cosmos-Transfer1-DiffusionRenderer 7B | ~7B params | [Brian9999/world_inverse_renderer](https://huggingface.co/Brian9999/world_inverse_renderer/tree/main) |
| Game Editing | Wan2.1 1.3B | ~1.3B params | [Brian9999/stylerenderer](https://huggingface.co/Brian9999/stylerenderer/tree/main) |

### Download and Place Weights

```bash
# Inverse Renderer — replace the base checkpoint
huggingface-cli download Brian9999/world_inverse_renderer \
  --local-dir inverse_renderer/checkpoints/Diffusion_Renderer_Inverse_Cosmos_7B

# Game Editing — place in game_editing models directory
mkdir -p game_editing/models/train/Wan2.1-T2V-1.3B_gbuffer
huggingface-cli download Brian9999/stylerenderer \
  --local-dir game_editing/models/train/Wan2.1-T2V-1.3B_gbuffer
```

---

## Inverse Renderer Usage

The inverse renderer decomposes an RGB video into 5 G-buffer channels: **albedo, normal, depth, roughness, metallic**.

### Setup

```bash
cd inverse_renderer
# Follow Cosmos-Transfer1-DiffusionRenderer environment setup
# Ensure checkpoint is at:
# inverse_renderer/checkpoints/Diffusion_Renderer_Inverse_Cosmos_7B/
```

### Inference

Refer to the `inverse_renderer/` subdirectory for the full inference script. The general pattern follows Cosmos-Transfer1-DiffusionRenderer conventions:

```python
# inverse_renderer/run_inverse.py (typical pattern)
import torch
from pathlib import Path

# Input: path to RGB video
input_video = "path/to/rgb_video.mp4"
output_dir = "outputs/gbuffers/"

# The model outputs 5 synchronized channels:
# - albedo (diffuse color)
# - normal (surface orientation)
# - depth (scene geometry)
# - roughness (surface roughness)
# - metallic (metallic property)
```

---

## Game Editing Usage

### Quick Start — CLI Inference

```bash
cd game_editing

CUDA_VISIBLE_DEVICES=0 python \
    examples/wanvideo/model_inference/inference_gbuffer_caption.py \
    --checkpoint models/train/Wan2.1-T2V-1.3B_gbuffer/model.safetensors \
    --gpu 0 \
    --style snowy_winter \
    --prompt "the scene is set in a frozen, snow-covered environment under cold, pale winter light with falling snowflakes, creating a silent and ethereal winter wonderland atmosphere." \
    --gbuffer_dir test_dataset \
    --save_dir outputs/ \
    --num_frames 81 \
    --height 480 \
    --width 832
```

### CLI Parameters

| Parameter | Description | Example |
|---|---|---|
| `--checkpoint` | Path to fine-tuned `.safetensors` weights | `models/train/Wan2.1-T2V-1.3B_gbuffer/model.safetensors` |
| `--gpu` | GPU device index | `0` |
| `--style` | Named style preset | `snowy_winter`, `rainy`, `night`, `sunset` |
| `--prompt` | Text description of target lighting/atmosphere | See examples below |
| `--gbuffer_dir` | Directory containing G-buffer input frames/video | `test_dataset` |
| `--save_dir` | Output directory for rendered video | `outputs/` |
| `--num_frames` | Number of frames to generate (must be `8n+1`) | `81` |
| `--height` | Output height in pixels | `480` |
| `--width` | Output width in pixels | `832` |

### G-buffer Directory Structure

```
test_dataset/
├── albedo/
│   ├── frame_0000.png
│   ├── frame_0001.png
│   └── ...
├── normal/
│   ├── frame_0000.png
│   └── ...
├── depth/
│   ├── frame_0000.png
│   └── ...
├── roughness/
│   ├── frame_0000.png
│   └── ...
└── metallic/
    ├── frame_0000.png
    └── ...
```

### Style Prompt Examples

```bash
# Cyberpunk night scene
--style night \
--prompt "neon-lit urban environment at night with rain-slicked streets reflecting colorful neon signs, creating a cyberpunk noir atmosphere"

# Golden hour / sunset
--style sunset \
--prompt "warm golden hour lighting with long shadows and a glowing amber sky, soft cinematic atmosphere"

# Rainy urban
--style rainy \
--prompt "overcast rainy day with wet surfaces, soft diffuse lighting, and atmospheric fog creating a moody cinematic look"

# Fantasy / stylized
--style fantasy \
--prompt "magical forest environment with bioluminescent plants, ethereal blue-green lighting, and mystical particle effects"

# Foggy morning
--style foggy \
--prompt "early morning dense fog with soft diffused light creating a mysterious and quiet atmosphere"
```

### Multi-GPU Inference

```bash
# Run on specific GPU
CUDA_VISIBLE_DEVICES=1 python \
    examples/wanvideo/model_inference/inference_gbuffer_caption.py \
    --checkpoint models/train/Wan2.1-T2V-1.3B_gbuffer/model.safetensors \
    --gpu 1 \
    --style rainy \
    --prompt "heavy rainfall with dark storm clouds and dramatic lightning in the distance" \
    --gbuffer_dir my_gbuffers \
    --save_dir outputs/rainy_scene \
    --num_frames 81 --height 480 --width 832
```

---

## Full Pipeline: RGB Video → Stylized Output

```bash
# Step 1: Extract G-buffers from RGB video (Inverse Renderer env)
conda activate inverse_renderer
cd inverse_renderer
python run_inverse.py \
    --input path/to/gameplay_video.mp4 \
    --output_dir ../game_editing/test_dataset/

# Step 2: Apply game editing style (Game Editing env)
conda activate game_editing
cd ../game_editing
CUDA_VISIBLE_DEVICES=0 python \
    examples/wanvideo/model_inference/inference_gbuffer_caption.py \
    --checkpoint models/train/Wan2.1-T2V-1.3B_gbuffer/model.safetensors \
    --gpu 0 \
    --style snowy_winter \
    --prompt "frozen tundra with blizzard conditions, pale blue-white lighting and drifting snow" \
    --gbuffer_dir test_dataset \
    --save_dir outputs/final_render \
    --num_frames 81 --height 480 --width 832
```

---

## Online Demos

| Demo | URL |
|---|---|
| Game Editing Demo | https://huggingface.co/spaces/Brian9999/game-editing |
| Project Page | https://alaya-studio.github.io/renderer/ |

---

## Dataset Overview

The AlayaRenderer dataset (release pending) features:

- **4M+ frames** at 720p / 30 FPS
- **6 synchronized channels**: RGB + albedo, normal, depth, metallic, roughness
- **40 hours** from **Cyberpunk 2077** and **Black Myth: Wukong**
- Average clip length: **8 minutes**, up to **53 minutes continuous**
- Weather variants: sunny, rainy, foggy, night, sunset
- Motion blur variant via sub-frame interpolation

---

## Architecture Summary

```
RGB Video Input
      │
      ▼
┌─────────────────────────────────────┐
│  Inverse Renderer                   │
│  (Cosmos-Transfer1 7B fine-tuned)   │
│  RGB → [albedo, normal, depth,      │
│          roughness, metallic]       │
└─────────────────┬───────────────────┘
                  │  G-buffers
                  ▼
┌─────────────────────────────────────┐
│  Game Editing                       │
│  (Wan2.1 1.3B fine-tuned)           │
│  G-buffers + Text Prompt            │
│  → Stylized RGB Video               │
└─────────────────────────────────────┘
```

---

## Troubleshooting

### Submodule not found / DiffSynth-Studio missing
```bash
# If cloned without --recurse-submodules:
git submodule update --init --recursive
```

### CUDA Out of Memory
- Reduce `--num_frames` (try `41` instead of `81`)
- Reduce resolution: `--height 320 --width 576`
- Ensure no other processes are using the GPU: `CUDA_VISIBLE_DEVICES=0`

### `num_frames` must follow `8n+1` pattern
Valid values: `9, 17, 25, 33, 41, 49, 57, 65, 73, 81`

```bash
# Valid
--num_frames 81   # 8*10 + 1 ✓
--num_frames 41   # 8*5 + 1  ✓

# Invalid
--num_frames 80   # ✗
--num_frames 60   # ✗
```

### Checkpoint not found
```bash
# Verify checkpoint placement
ls game_editing/models/train/Wan2.1-T2V-1.3B_gbuffer/model.safetensors
ls inverse_renderer/checkpoints/Diffusion_Renderer_Inverse_Cosmos_7B/
```

### Version conflicts between models
Always use the two separate conda environments (`inverse_renderer` and `game_editing`). Do not install both models' dependencies in one environment.

---

## Citation

```bibtex
@article{huang2026generativeworldrenderer,
    title={Generative World Renderer},
    author={Zheng-Hui Huang and Zhixiang Wang and Jiaming Tan and Ruihan Yu and Yidan Zhang and Bo Zheng and Yu-Lun Liu and Yung-Yu Chuang and Kaipeng Zhang},
    journal={arXiv preprint arXiv:2604.02329},
    year={2026}
}
```
