---
name: hy-world-2-0-3d-world-model
description: Expert skill for using HY-World 2.0, Tencent's multi-modal world model for reconstructing, generating, and simulating 3D worlds from text, images, and video.
triggers:
  - reconstruct a 3D scene from images
  - generate a 3D world from text or image
  - use WorldMirror for 3D reconstruction
  - convert video to 3D gaussian splatting
  - predict depth and camera parameters from multi-view images
  - run HY-World 2.0 pipeline
  - set up world model for scene generation
  - export 3DGS or mesh from photos
---

# HY-World 2.0 — 3D World Model Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

HY-World 2.0 is a multi-modal world model by Tencent Hunyuan that reconstructs, generates, and simulates 3D worlds. It accepts text, single-view images, multi-view images, and videos as input and produces 3D representations (meshes, 3D Gaussian Splattings, point clouds). Two core capabilities:

- **World Reconstruction** (multi-view images / video → 3D): Powered by WorldMirror 2.0, a ~1.2B feed-forward model predicting depth, surface normals, camera parameters, 3D point clouds, and 3DGS attributes in a single forward pass.
- **World Generation** (text / single image → 3D world): Four-stage pipeline — Panorama Generation (HY-Pano 2.0) → Trajectory Planning (WorldNav) → World Expansion (WorldStereo 2.0) → World Composition (WorldMirror 2.0 + 3DGS).

---

## Installation

### Requirements
- Python 3.10
- CUDA 12.4 (recommended)
- PyTorch 2.4.0

```bash
# 1. Clone repository
git clone https://github.com/Tencent-Hunyuan/HY-World-2.0
cd HY-World-2.0

# 2. Create conda environment
conda create -n hyworld2 python=3.10
conda activate hyworld2

# 3. Install PyTorch with CUDA 12.4
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124

# 4. Install project dependencies
pip install -r requirements.txt

# 5a. Install FlashAttention-3 (recommended for performance)
git clone https://github.com/Dao-AILab/flash-attention.git
cd flash-attention/hopper
python setup.py install
cd ../../
rm -rf flash-attention

# 5b. OR install FlashAttention-2 (simpler)
pip install flash-attn --no-build-isolation
```

### Model Weights
Model weights are **automatically downloaded from Hugging Face** on first run. Alternatively, download manually:

| Model | HuggingFace |
|---|---|
| WorldMirror 2.0 | `tencent/HY-World-2.0` → `HY-WorldMirror-2.0` |
| WorldMirror 1.0 (legacy) | `tencent/HunyuanWorld-Mirror` |

To pre-download:
```bash
# Set HuggingFace cache directory if needed
export HF_HOME=/path/to/cache

pip install huggingface_hub
python -c "from huggingface_hub import snapshot_download; snapshot_download('tencent/HY-World-2.0')"
```

---

## Core API — WorldMirror 2.0 (World Reconstruction)

### Basic Usage

```python
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

# Load pipeline — weights auto-downloaded on first run
pipeline = WorldMirrorPipeline.from_pretrained('tencent/HY-World-2.0')

# Run reconstruction from a folder of images
result = pipeline('path/to/images')
```

### With Prior Injection (Camera & Depth)

Provide known camera parameters or depth priors to improve accuracy:

```python
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

pipeline = WorldMirrorPipeline.from_pretrained('tencent/HY-World-2.0')

result = pipeline(
    'path/to/images',
    prior_cam_path='path/to/prior_camera.json',
    prior_depth_path='path/to/prior_depth.npy',  # optional
)
```

### Camera JSON Format

The `prior_camera.json` format expected by the pipeline:

```json
[
  {
    "image": "frame_001.jpg",
    "fx": 800.0,
    "fy": 800.0,
    "cx": 640.0,
    "cy": 360.0,
    "width": 1280,
    "height": 720,
    "c2w": [
      [1.0, 0.0, 0.0, 0.0],
      [0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0]
    ]
  }
]
```

### Result Object

The pipeline returns a result object with the following attributes:

```python
result = pipeline('path/to/images')

# Access outputs
point_cloud  = result.point_cloud      # 3D point cloud (numpy or torch)
depth_maps   = result.depth_maps       # Per-image depth maps
normals      = result.normals          # Surface normal maps
cameras      = result.cameras          # Predicted camera parameters
gaussians    = result.gaussians        # 3DGS attributes

# Save outputs
result.save('output_dir/')             # Saves all outputs to directory
```

---

## Gradio App — WorldMirror 2.0

Launch an interactive web UI for 3D reconstruction:

```bash
# From project root
python -m hyworld2.worldrecon.app

# Or if a dedicated script exists
python app.py --model tencent/HY-World-2.0
```

Access at `http://localhost:7860` by default.

---

## Common Patterns

### Pattern 1: Reconstruct from a Video

Extract frames from a video, then run reconstruction:

```python
import cv2
import os
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

def extract_frames(video_path, output_dir, fps=2):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / fps)
    frame_idx = 0
    saved = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            cv2.imwrite(f"{output_dir}/frame_{saved:04d}.jpg", frame)
            saved += 1
        frame_idx += 1
    cap.release()
    return output_dir

# Extract frames at 2 fps
frames_dir = extract_frames("scene.mp4", "frames/", fps=2)

# Run reconstruction
pipeline = WorldMirrorPipeline.from_pretrained('tencent/HY-World-2.0')
result = pipeline(frames_dir)
result.save("output_3d/")
```

### Pattern 2: Flexible Resolution Inference

WorldMirror 2.0 supports 50K–500K pixel resolution. Control via resize parameters:

```python
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

pipeline = WorldMirrorPipeline.from_pretrained('tencent/HY-World-2.0')

# Low resolution (fast, lower memory)
result_fast = pipeline(
    'path/to/images',
    resolution=512,        # resize shorter edge to 512
)

# High resolution (slower, more detail)
result_hq = pipeline(
    'path/to/images',
    resolution=1024,
)
```

### Pattern 3: Batch Processing Multiple Scenes

```python
import os
from pathlib import Path
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

pipeline = WorldMirrorPipeline.from_pretrained('tencent/HY-World-2.0')

scenes_root = Path("scenes/")
output_root = Path("outputs/")

for scene_dir in sorted(scenes_root.iterdir()):
    if not scene_dir.is_dir():
        continue
    out_dir = output_root / scene_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing: {scene_dir.name}")
    try:
        result = pipeline(str(scene_dir))
        result.save(str(out_dir))
        print(f"  Saved to {out_dir}")
    except Exception as e:
        print(f"  Failed: {e}")
```

### Pattern 4: Export to Common 3D Formats

After reconstruction, export to formats compatible with Blender / Unity / Unreal:

```python
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

pipeline = WorldMirrorPipeline.from_pretrained('tencent/HY-World-2.0')
result = pipeline('path/to/images')

# Save 3DGS (.ply format for tools like 3D Gaussian Splatting viewer)
result.save_gaussians("scene.ply")

# Save mesh (if mesh export is supported)
result.save_mesh("scene.obj")   # or scene.glb

# Save point cloud
result.save_pointcloud("scene_pointcloud.ply")
```

### Pattern 5: GPU Memory Management

For large scenes or limited VRAM:

```python
import torch
from hyworld2.worldrecon.pipeline import WorldMirrorPipeline

# Load in fp16 to reduce memory
pipeline = WorldMirrorPipeline.from_pretrained(
    'tencent/HY-World-2.0',
    torch_dtype=torch.float16,
)
pipeline = pipeline.to('cuda')

# Run with lower resolution to fit in memory
result = pipeline('path/to/images', resolution=768)

# Free memory after use
del result
torch.cuda.empty_cache()
```

---

## Project Structure

```
HY-World-2.0/
├── hyworld2/
│   ├── worldrecon/          # WorldMirror 2.0 reconstruction
│   │   ├── pipeline.py      # Main WorldMirrorPipeline class
│   │   ├── app.py           # Gradio web app
│   │   └── ...
│   ├── worldgen/            # World generation (coming soon)
│   │   ├── panorama/        # HY-Pano 2.0
│   │   ├── nav/             # WorldNav trajectory planning
│   │   └── stereo/          # WorldStereo 2.0
│   └── utils/
├── assets/                  # Demo assets
├── requirements.txt
└── README.md
```

---

## Environment Variables

```bash
# HuggingFace model cache location
export HF_HOME=/path/to/hf/cache

# HuggingFace token (if accessing private/gated models)
export HUGGING_FACE_HUB_TOKEN=your_token_here

# CUDA device selection
export CUDA_VISIBLE_DEVICES=0

# For multi-GPU setups
export CUDA_VISIBLE_DEVICES=0,1
```

---

## Troubleshooting

### FlashAttention installation fails
```bash
# Use FlashAttention-2 as fallback
pip install flash-attn --no-build-isolation

# If that fails, disable flash attention (slower but works)
# Set environment variable before running
export USE_FLASH_ATTENTION=0
```

### CUDA out of memory
```python
# 1. Reduce resolution
result = pipeline('path/to/images', resolution=512)

# 2. Use fp16
pipeline = WorldMirrorPipeline.from_pretrained(
    'tencent/HY-World-2.0',
    torch_dtype=torch.float16
)

# 3. Process fewer images at once — use a subset
import os
images = sorted(os.listdir('path/to/images'))[:10]  # limit to 10 frames
```

### Model download issues
```bash
# Use HF mirror if huggingface.co is blocked
export HF_ENDPOINT=https://hf-mirror.com

# Or manually download and point to local path
pipeline = WorldMirrorPipeline.from_pretrained('/local/path/to/model')
```

### Wrong PyTorch/CUDA version
```bash
# Verify versions match
python -c "import torch; print(torch.__version__, torch.version.cuda)"
# Should output: 2.4.0 12.4

# Reinstall if mismatch
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124
```

### Images not loading
```python
# Ensure images are valid and in supported formats (.jpg, .png)
from PIL import Image
import os

img_dir = 'path/to/images'
for f in os.listdir(img_dir):
    try:
        img = Image.open(os.path.join(img_dir, f))
        img.verify()
    except Exception as e:
        print(f"Bad image {f}: {e}")
```

---

## Related Projects

| Project | Use Case | Link |
|---|---|---|
| WorldStereo | Panorama → 3DGS (open-source preview of WorldStereo-2) | [GitHub](https://github.com/FuchengSu/WorldStereo) |
| HunyuanWorld 1.0 | Panorama generation (interim for HY-Pano 2.0) | [GitHub](https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0) |
| WorldMirror 1.0 | Legacy reconstruction model | [HuggingFace](https://huggingface.co/tencent/HunyuanWorld-Mirror) |

---

## Key Limitations (Current Release)

- **World Generation pipeline** (WorldNav, WorldStereo-2, HY-Pano-2) is **not yet open-sourced** — only WorldMirror 2.0 reconstruction is available.
- **Panorama generation**: Use [HunyuanWorld 1.0](https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0) as interim.
- **World Expansion**: Use [WorldStereo](https://github.com/FuchengSu/WorldStereo) as interim.
- Requires CUDA GPU — CPU inference not officially supported.
- Minimum ~8GB VRAM recommended; 16GB+ for full-resolution inference.
