---
name: lingbot-map-3d-reconstruction
description: Feed-forward 3D foundation model for streaming scene reconstruction using Geometric Context Transformer
triggers:
  - reconstruct 3D scene from images
  - streaming 3D reconstruction
  - lingbot-map inference
  - point cloud from video
  - feed-forward 3D model
  - geometric context transformer
  - reconstruct from streaming data
  - lingbot map demo

---

# LingBot-Map 3D Reconstruction Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

LingBot-Map is a feed-forward 3D foundation model that reconstructs scenes from streaming image or video data using a Geometric Context Transformer. It achieves ~20 FPS on 518×378 resolution over sequences exceeding 10,000 frames via paged KV cache attention.

## What It Does

- **Streaming 3D reconstruction** from image sequences or video
- **Feed-forward inference** (no iterative optimization needed)
- **Outputs**: point clouds with per-point confidence, camera poses, depth maps
- **Key features**: anchor context, pose-reference window, trajectory memory for drift correction

## Installation

```bash
# 1. Create environment
conda create -n lingbot-map python=3.10 -y
conda activate lingbot-map

# 2. Install PyTorch (CUDA 12.8)
pip install torch==2.9.1 torchvision==0.24.1 --index-url https://download.pytorch.org/whl/cu128

# 3. Install lingbot-map
git clone https://github.com/Robbyant/lingbot-map.git
cd lingbot-map
pip install -e .

# 4. Install FlashInfer for fast paged KV cache attention (recommended)
pip install flashinfer-python -i https://flashinfer.ai/whl/cu128/torch2.9/

# 5. Optional: visualization support
pip install -e ".[vis]"

# 6. Optional: sky masking for outdoor scenes
pip install onnxruntime       # CPU
pip install onnxruntime-gpu   # GPU
```

## Model Download

Models available on HuggingFace and ModelScope:

```python
# Download via huggingface_hub
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="robbyant/lingbot-map",
    filename="checkpoint.pt"
)
```

Or manually download from:
- HuggingFace: `https://huggingface.co/robbyant/lingbot-map`
- ModelScope: `https://www.modelscope.cn/models/Robbyant/lingbot-map`

## CLI Commands

### Demo with Interactive 3D Viewer (browser at localhost:8080)

```bash
# From image folder
python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder /path/to/images/

# From video file
python demo.py --model_path /path/to/checkpoint.pt \
    --video_path video.mp4 --fps 10

# Outdoor scene with sky masking
python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder /path/to/images/ --mask_sky

# Example scenes included in repo
python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder example/church --mask_sky

python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder example/oxford --mask_sky

python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder example/university4 --mask_sky
```

### Long Sequence Handling

```bash
# Keyframe interval: store every Nth frame in KV cache (saves memory)
# Use when sequence > 320 frames
python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder /path/to/images/ --keyframe_interval 6

# Windowed mode: for very long sequences (>3000 frames)
python demo.py --model_path /path/to/checkpoint.pt \
    --video_path video.mp4 --fps 10 \
    --mode windowed --window_size 64
```

### Without FlashInfer (SDPA fallback)

```bash
python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder /path/to/images/ --use_sdpa
```

### Sky Masking with Custom Paths

```bash
python demo.py --model_path /path/to/checkpoint.pt \
    --image_folder /path/to/images/ --mask_sky \
    --sky_mask_dir /path/to/cached_masks/ \
    --sky_mask_visualization_dir /path/to/mask_viz/
```

## CLI Arguments Reference

### Input
| Argument | Description |
|:---|:---|
| `--model_path` | Path to model checkpoint (.pt file) |
| `--image_folder` | Directory of input images |
| `--video_path` | Input video file path |
| `--fps` | Frames per second to sample from video |

### Inference Mode
| Argument | Default | Description |
|:---|:---|:---|
| `--mode` | `streaming` | `streaming` or `windowed` |
| `--window_size` | `64` | Window size for windowed mode |
| `--keyframe_interval` | `1` | Store every Nth frame in KV cache |
| `--use_sdpa` | `False` | Use PyTorch SDPA instead of FlashInfer |

### Sky Masking
| Argument | Description |
|:---|:---|
| `--mask_sky` | Enable sky segmentation and masking |
| `--sky_mask_dir` | Custom directory for cached sky masks |
| `--sky_mask_visualization_dir` | Save side-by-side mask visualizations |

### Visualization
| Argument | Default | Description |
|:---|:---|:---|
| `--port` | `8080` | Viser viewer port |
| `--conf_threshold` | `1.5` | Filter low-confidence points |
| `--point_size` | `0.00001` | Point cloud point size |
| `--downsample_factor` | `10` | Spatial downsampling for display |

## Python API Usage

### Basic Streaming Inference

```python
import torch
from lingbot_map import LingBotMap  # adjust import to actual module structure

# Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = LingBotMap.from_pretrained("/path/to/checkpoint.pt")
model = model.to(device).eval()

# Streaming inference over image list
from pathlib import Path
from PIL import Image
import torchvision.transforms as T

transform = T.Compose([
    T.Resize((378, 518)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

image_paths = sorted(Path("/path/to/images").glob("*.jpg"))

with torch.no_grad():
    for img_path in image_paths:
        img = Image.open(img_path).convert("RGB")
        frame = transform(img).unsqueeze(0).to(device)
        output = model.stream(frame)
        # output contains: pointmap, confidence, camera pose
```

### Loading and Running the Demo Programmatically

```python
# The demo.py script is the primary entry point
# Run it as a subprocess or study it for API patterns
import subprocess

result = subprocess.run([
    "python", "demo.py",
    "--model_path", "/path/to/checkpoint.pt",
    "--image_folder", "example/church",
    "--mask_sky",
    "--port", "8080"
], check=True)
```

### Video Input Pattern

```python
import cv2
import torch

# Extract frames from video for batch processing
def extract_frames(video_path: str, fps: int = 10):
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    interval = max(1, int(video_fps / fps))
    
    frames = []
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % interval == 0:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
        frame_idx += 1
    
    cap.release()
    return frames

frames = extract_frames("video.mp4", fps=10)
```

## Common Patterns

### Pattern 1: Outdoor Scene Reconstruction

```bash
# Always use --mask_sky for outdoor scenes to remove noisy sky points
python demo.py \
    --model_path ./checkpoint.pt \
    --image_folder ./outdoor_images \
    --mask_sky \
    --conf_threshold 2.0 \
    --downsample_factor 5
```

### Pattern 2: Long Indoor Sequence

```bash
# Use keyframe_interval to manage KV cache for sequences 320-3000 frames
python demo.py \
    --model_path ./checkpoint.pt \
    --image_folder ./long_sequence \
    --keyframe_interval 6 \
    --conf_threshold 1.5
```

### Pattern 3: Very Long Video (>3000 frames)

```bash
# Use windowed mode for extremely long sequences
python demo.py \
    --model_path ./checkpoint.pt \
    --video_path long_video.mp4 \
    --fps 5 \
    --mode windowed \
    --window_size 64
```

### Pattern 4: High Quality Dense Reconstruction

```bash
# Lower conf_threshold keeps more points, smaller downsample shows more detail
python demo.py \
    --model_path ./checkpoint.pt \
    --image_folder ./images \
    --conf_threshold 1.0 \
    --downsample_factor 1 \
    --point_size 0.00005
```

### Pattern 5: CPU / No FlashInfer Fallback

```bash
# When FlashInfer is unavailable, use SDPA
python demo.py \
    --model_path ./checkpoint.pt \
    --image_folder ./images \
    --use_sdpa
```

## Architecture Concepts

| Component | Role |
|:---|:---|
| **Anchor Context** | Coordinate grounding to prevent drift |
| **Pose-Reference Window** | Dense geometric cues from recent frames |
| **Trajectory Memory** | Long-range drift correction across the sequence |
| **Paged KV Cache** | Efficient attention over long streaming sequences |

## Troubleshooting

### FlashInfer Not Available
```bash
# Error: FlashInfer not found
# Solution: Install or use SDPA fallback
pip install flashinfer-python -i https://flashinfer.ai/whl/cu128/torch2.9/
# Or add --use_sdpa to any command
python demo.py --model_path ./checkpoint.pt --image_folder ./imgs --use_sdpa
```

### CUDA Out of Memory on Long Sequences
```bash
# Reduce memory with keyframe interval
python demo.py --model_path ./checkpoint.pt \
    --image_folder ./images --keyframe_interval 6

# Or switch to windowed mode
python demo.py --model_path ./checkpoint.pt \
    --image_folder ./images --mode windowed --window_size 32
```

### Sky Mask Model Download Fails
```bash
# Manual download of skyseg.onnx
wget https://huggingface.co/JianyuanWang/skyseg/resolve/main/skyseg.onnx
# Place in expected path or specify via --sky_mask_dir
```

### Low Quality / Noisy Point Cloud
```bash
# Increase confidence threshold to filter noisy points
python demo.py --model_path ./checkpoint.pt \
    --image_folder ./images --conf_threshold 2.5

# For outdoor, always add sky masking
python demo.py --model_path ./checkpoint.pt \
    --image_folder ./images --mask_sky --conf_threshold 2.0
```

### Port Already in Use
```bash
# Change the viewer port
python demo.py --model_path ./checkpoint.pt \
    --image_folder ./images --port 8090
```

### Images Not Loading
```bash
# Ensure images are sorted and in supported formats (jpg, png)
ls /path/to/images | head -5
# Supported: .jpg, .jpeg, .png, .bmp, .webp
```

## Performance Guidelines

| Sequence Length | Recommended Mode | Notes |
|:---|:---|:---|
| < 320 frames | Default streaming | Full KV cache |
| 320–3000 frames | `--keyframe_interval 6` | Reduces cache by 6x |
| > 3000 frames | `--mode windowed --window_size 64` | Sliding window |

- **Target resolution**: 518×378 for ~20 FPS throughput
- **GPU**: CUDA-capable GPU required for practical speeds
- **Model size**: ~4.63 GB checkpoint

## Citation

```bibtex
@article{chen2026geometric,
  title={Geometric Context Transformer for Streaming 3D Reconstruction},
  author={Chen, Lin-Zhuo and Gao, Jian and Chen, Yihang and Cheng, Ka Leong and Sun, Yipengjing and Hu, Liangxiao and Xue, Nan and Zhu, Xing and Shen, Yujun and Yao, Yao and Xu, Yinghao},
  journal={arXiv preprint arXiv:2604.14141},
  year={2026}
}
```
