---
name: corridorkey-green-screen
description: AI-powered green screen keyer that unmixes foreground colors and generates clean linear alpha channels using neural networks
triggers:
  - green screen keying with AI
  - remove green screen background
  - extract foreground from green screen
  - CorridorKey setup and usage
  - generate alpha matte from green screen
  - VFX green screen compositing Python
  - chroma key neural network unmixing
  - corridorkey inference pipeline
---

# CorridorKey Green Screen Keying

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CorridorKey is a neural network that solves the color *unmixing* problem in green screen footage. For every pixel — including semi-transparent ones from motion blur, hair, or out-of-focus edges — it predicts the true straight (un-premultiplied) foreground color and a clean linear alpha channel. It reads/writes 16-bit and 32-bit EXR files for VFX pipeline integration.

## How It Works

Two inputs required per frame:
1. **RGB green screen image** — sRGB or linear gamma, sRGB/REC709 gamut
2. **Alpha Hint** — rough coarse B&W mask (doesn't need to be precise)

The model fills in fine detail from the hint; it's trained on blurry/eroded masks.

## Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) package manager (handles Python automatically)
- NVIDIA GPU with CUDA 12.8+ drivers (for GPU), or Apple M1+ (for MLX), or CPU fallback

### Windows
```bat
# Double-click or run from terminal:
Install_CorridorKey_Windows.bat

# Optional heavy modules:
Install_GVM_Windows.bat
Install_VideoMaMa_Windows.bat
```

### Linux / macOS
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies — pick one:
uv sync                  # CPU / Apple MPS (universal)
uv sync --extra cuda     # NVIDIA GPU (Linux/Windows)
uv sync --extra mlx      # Apple Silicon MLX

# Download required model (~300MB)
mkdir -p CorridorKeyModule/checkpoints
# Place downloaded CorridorKey_v1.0.pth as:
# CorridorKeyModule/checkpoints/CorridorKey.pth
```

Model download: https://huggingface.co/nikopueringer/CorridorKey_v1.0/resolve/main/CorridorKey_v1.0.pth

### Optional Alpha Hint Generators
```bash
# GVM (automatic, ~80GB VRAM, good for people)
uv run hf download geyongtao/gvm --local-dir gvm_core/weights

# VideoMaMa (requires mask hint, <24GB VRAM with community tweaks)
uv run hf download SammyLim/VideoMaMa \
  --local-dir VideoMaMaInferenceModule/checkpoints/VideoMaMa

uv run hf download stabilityai/stable-video-diffusion-img2vid-xt \
  --local-dir VideoMaMaInferenceModule/checkpoints/stable-video-diffusion-img2vid-xt \
  --include "feature_extractor/*" "image_encoder/*" "vae/*" "model_index.json"
```

## Key CLI Commands

```bash
# Run inference on prepared clips
uv run python main.py run_inference --device cuda
uv run python main.py run_inference --device cpu
uv run python main.py run_inference --device mps   # Apple Silicon

# List available clips/shots
uv run python main.py list

# Interactive setup wizard
uv run python main.py wizard
uv run python main.py wizard --win_path /path/to/ClipsForInference
```

## Docker (Linux + NVIDIA GPU)

```bash
# Build
docker build -t corridorkey:latest .

# Run inference
docker run --rm -it --gpus all \
  -e OPENCV_IO_ENABLE_OPENEXR=1 \
  -v "$(pwd)/ClipsForInference:/app/ClipsForInference" \
  -v "$(pwd)/Output:/app/Output" \
  -v "$(pwd)/CorridorKeyModule/checkpoints:/app/CorridorKeyModule/checkpoints" \
  corridorkey:latest run_inference --device cuda

# Docker Compose
docker compose build
docker compose --profile gpu run --rm corridorkey run_inference --device cuda
docker compose --profile gpu run --rm corridorkey list

# Pin to specific GPU on multi-GPU systems
NVIDIA_VISIBLE_DEVICES=0 docker compose --profile gpu run --rm corridorkey run_inference --device cuda
```

## Directory Structure

```
CorridorKey/
├── ClipsForInference/          # Input shots go here
│   └── my_shot/
│       ├── frames/             # Green screen RGB frames (PNG/EXR)
│       ├── alpha_hints/        # Coarse alpha masks (grayscale)
│       └── VideoMamaMaskHint/  # Optional: hand-drawn hints for VideoMaMa
├── Output/                     # Processed results
│   └── my_shot/
│       ├── foreground/         # Straight RGBA EXR frames
│       └── alpha/              # Linear alpha channel frames
├── CorridorKeyModule/
│   └── checkpoints/
│       └── CorridorKey.pth     # Required model weights
├── gvm_core/weights/           # Optional GVM weights
└── VideoMaMaInferenceModule/
    └── checkpoints/            # Optional VideoMaMa weights
```

## Python Usage Examples

### Basic Inference Pipeline
```python
import torch
from pathlib import Path
from CorridorKeyModule.model import CorridorKeyModel  # adjust to actual module path
from CorridorKeyModule.inference import run_inference

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CorridorKeyModel()
model.load_state_dict(torch.load("CorridorKeyModule/checkpoints/CorridorKey.pth"))
model.to(device)
model.eval()

# Run inference on a shot folder
run_inference(
    shot_dir=Path("ClipsForInference/my_shot"),
    output_dir=Path("Output/my_shot"),
    device=device,
)
```

### Reading/Writing EXR Files
```python
import cv2
import numpy as np
import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

# Read a 32-bit linear EXR frame
frame = cv2.imread("frame_0001.exr", cv2.IMREAD_UNCHANGED | cv2.IMREAD_ANYCOLOR)
# frame is float32, linear light, BGR channel order

# Convert BGR -> RGB for processing
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Write output EXR (straight RGBA)
# Assume `foreground` is float32 HxWx4 (RGBA, linear, straight alpha)
foreground_bgra = cv2.cvtColor(foreground, cv2.COLOR_RGBA2BGRA)
cv2.imwrite("output_0001.exr", foreground_bgra.astype(np.float32))
```

### Generating a Coarse Alpha Hint with OpenCV
```python
import cv2
import numpy as np

def generate_chroma_key_hint(image_bgr: np.ndarray, erode_px: int = 5) -> np.ndarray:
    """
    Quick-and-dirty green screen hint for CorridorKey input.
    Returns grayscale mask (0=background, 255=foreground).
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Tune these ranges for your specific green screen
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    foreground_mask = cv2.bitwise_not(green_mask)

    # Erode to pull mask away from edges (CorridorKey handles edge detail)
    kernel = np.ones((erode_px, erode_px), np.uint8)
    eroded = cv2.erode(foreground_mask, kernel, iterations=2)

    # Optional: slight blur to soften hint
    blurred = cv2.GaussianBlur(eroded, (15, 15), 5)
    return blurred


# Usage
frame = cv2.imread("greenscreen_frame.png")
hint = generate_chroma_key_hint(frame, erode_px=8)
cv2.imwrite("alpha_hint.png", hint)
```

### Batch Processing Frames
```python
from pathlib import Path
import cv2
import numpy as np
import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

def prepare_shot_folder(
    raw_frames_dir: Path,
    output_shot_dir: Path,
    hint_generator_fn=None
):
    """
    Prepares a CorridorKey shot folder from raw green screen frames.
    """
    frames_out = output_shot_dir / "frames"
    hints_out = output_shot_dir / "alpha_hints"
    frames_out.mkdir(parents=True, exist_ok=True)
    hints_out.mkdir(parents=True, exist_ok=True)

    frame_paths = sorted(raw_frames_dir.glob("*.png")) + \
                  sorted(raw_frames_dir.glob("*.exr"))

    for frame_path in frame_paths:
        frame = cv2.imread(str(frame_path), cv2.IMREAD_UNCHANGED | cv2.IMREAD_ANYCOLOR)

        # Copy frame
        cv2.imwrite(str(frames_out / frame_path.name), frame)

        # Generate hint
        if hint_generator_fn:
            hint = hint_generator_fn(frame)
        else:
            hint = generate_chroma_key_hint(frame)

        hint_name = frame_path.stem + ".png"
        cv2.imwrite(str(hints_out / hint_name), hint)

    print(f"Prepared {len(frame_paths)} frames in {output_shot_dir}")


prepare_shot_folder(
    raw_frames_dir=Path("raw_footage/shot_01"),
    output_shot_dir=Path("ClipsForInference/shot_01"),
)
```

### Using clip_manager.py Alpha Hint Generators
```python
# GVM (automatic — no extra input needed)
from clip_manager import generate_alpha_hints_gvm

generate_alpha_hints_gvm(
    shot_dir="ClipsForInference/my_shot",
    device="cuda"
)

# VideoMaMa (place rough mask in VideoMamaMaskHint/ first)
from clip_manager import generate_alpha_hints_videomama

generate_alpha_hints_videomama(
    shot_dir="ClipsForInference/my_shot",
    device="cuda"
)

# BiRefNet (lightweight option, no large VRAM needed)
from clip_manager import generate_alpha_hints_birefnet

generate_alpha_hints_birefnet(
    shot_dir="ClipsForInference/my_shot",
    device="cuda"
)
```

## Alpha Hint Best Practices

```python
# GOOD: Eroded, slightly blurry hint — pulls away from edges
# The model fills edge detail from the hint
kernel = np.ones((10, 10), np.uint8)
good_hint = cv2.erode(raw_mask, kernel, iterations=3)
good_hint = cv2.GaussianBlur(good_hint, (21, 21), 7)

# BAD: Expanded / dilated hint — model is worse at subtracting
# Don't push the mask OUTWARD past the true subject boundary
bad_hint = cv2.dilate(raw_mask, kernel, iterations=3)  # avoid this

# ACCEPTABLE: Binary rough chroma key as-is
# Even a hard binary mask works — just not expanded
acceptable_hint = raw_chroma_key_mask  # no dilation
```

## Output Integration (Nuke / Fusion / Resolve)

CorridorKey outputs **straight (un-premultiplied) RGBA EXRs** in linear light:

```python
# In Nuke: read as EXR, set colorspace to "linear"
# The alpha is already clean — no need for Unpremult node
# Connect straight to a Merge (over) node with your background plate

# Verify output is straight alpha (not premultiplied):
import cv2, numpy as np, os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

result = cv2.imread("Output/shot_01/foreground/frame_0001.exr",
                    cv2.IMREAD_UNCHANGED | cv2.IMREAD_ANYCOLOR)
# result[..., 3] = alpha channel (linear 0.0–1.0)
# result[..., :3] = straight color (not multiplied by alpha)

# Check a semi-transparent pixel
h, w = result.shape[:2]
sample_alpha = result[h//2, w//2, 3]
sample_color = result[h//2, w//2, :3]
print(f"Alpha: {sample_alpha:.3f}, Color: {sample_color}")
# Color values should be full-strength even where alpha < 1.0 (straight alpha)
```

## Troubleshooting

### CUDA not detected / falling back to CPU
```bash
# Check CUDA version requirement: driver must support CUDA 12.8+
nvidia-smi  # shows max supported CUDA version

# Reinstall with explicit CUDA extra
uv sync --extra cuda

# Verify PyTorch sees GPU
uv run python -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"
```

### OpenEXR read/write fails
```bash
# Must set environment variable before importing cv2
export OPENCV_IO_ENABLE_OPENEXR=1
uv run python your_script.py

# Or in Python (must be BEFORE import cv2)
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2
```

### Out of VRAM
```bash
# Use CPU fallback
uv run python main.py run_inference --device cpu

# Or reduce batch size / use tiled inference if supported
# The engine dynamically scales to 2048x2048 tiles — for 4K,
# ensure at least 6-8GB VRAM

# Apple Silicon: use MPS
uv run python main.py run_inference --device mps
```

### Model file not found
```bash
# Verify exact filename and location:
ls CorridorKeyModule/checkpoints/
# Must be named exactly: CorridorKey.pth
# Not: CorridorKey_v1.0.pth

mv CorridorKeyModule/checkpoints/CorridorKey_v1.0.pth \
   CorridorKeyModule/checkpoints/CorridorKey.pth
```

### Docker GPU passthrough fails
```bash
# Test NVIDIA container toolkit
docker run --rm --gpus all nvidia/cuda:12.6.3-runtime-ubuntu22.04 nvidia-smi

# If it fails, install/reconfigure nvidia-container-toolkit:
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# Then restart Docker daemon
sudo systemctl restart docker
```

### Poor keying results
- **Hint too expanded**: Erode your alpha hint more — CorridorKey is better at adding edge detail than removing unwanted mask area
- **Wrong color space**: Ensure input is sRGB/REC709 gamut; don't pass log-encoded footage directly
- **Green spill**: The model handles color unmixing, but extreme green spill in source may degrade results; consider a despill pass before inference
- **Static subjects**: GVM works best on people; try VideoMaMa with a hand-drawn hint for props/objects

## Community & Resources

- **Discord**: https://discord.gg/zvwUrdWXJm (Corridor Creates — share results, forks, ideas)
- **Easy UI**: [EZ-CorridorKey](https://github.com/edenaion/EZ-CorridorKey) — artist-friendly interface
- **Model weights**: https://huggingface.co/nikopueringer/CorridorKey_v1.0
- **GVM project**: https://github.com/aim-uofa/GVM
- **VideoMaMa project**: https://github.com/cvlab-kaist/VideoMaMa
