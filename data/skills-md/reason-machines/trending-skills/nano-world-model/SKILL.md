---
name: nano-world-model
description: Minimalist batteries-included repository for training, evaluating, and deploying diffusion-forcing video world models for robot manipulation, gaming, and MPC planning.
triggers:
  - train a world model
  - video world model with diffusion
  - diffusion forcing transformer
  - model predictive control with world model
  - autoregressive video generation robot
  - long horizon rollout world model
  - nano world model training
  - world model MPC planning
---

# Nano World Model

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Nano World Model is a minimalist, batteries-included repository for training video world models using diffusion-forcing transformers. It supports diverse domains (robot manipulation, gaming, simulation), long-horizon autoregressive rollouts, video-to-3D reconstruction, and MPC-style planning via CEM.

---

## Installation

```bash
git clone https://github.com/simchowitzlabpublic/nano-world-model.git
cd nano-world-model
conda env create -f environment.yml && conda activate nanowm
```

Download the I3D model used for FID/FVD evaluation:

```bash
mkdir -p pretrained_models/i3d && curl -L \
    "https://www.dropbox.com/scl/fi/c5nfs6c422nlpj880jbmh/i3d_torchscript.pt?rlkey=x5xcjsrz0818i4qxyoglp5bb8&dl=1" \
    -o pretrained_models/i3d/i3d_torchscript.pt
```

---

## Environment Variables / Path Configuration

Set these before running any command, or define them in `src/configs/local/paths.yaml`:

```bash
export DATASET_DIR=/path/to/dino_wm_data       # DINO-WM envs (point_maze, pusht, ...)
export CSGO_DATA_DIR=/path/to/csgo             # CSGO HDF5 files
export RT1_DATA_ROOT=/path/to/rt1_fractal      # RT-1 LeRobot mirror (optional)
export RESULTS_DIR=/path/to/results            # checkpoints + logs
```

Or create `src/configs/local/paths.yaml`:

```yaml
# src/configs/local/paths.yaml
dataset_dir: /path/to/dino_wm_data
csgo_data_dir: /path/to/csgo
rt1_data_root: /path/to/rt1_fractal
results_dir: /path/to/results
```

---

## Key CLI Commands

The main entry point is `src/main.py` with [Hydra](https://hydra.cc/) config composition.

### Training

```bash
# DINO-WM PushT, NanoWM-B/2 (default best config: pred-v, additive injection, cosine+ZTSNR)
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2

# DINO-WM Point Maze
python src/main.py experiment=dino_wm_point_maze dataset=dino_wm/point_maze model=nanowm_b2

# CSGO with L/2 model
python src/main.py experiment=csgo dataset=game/csgo model=nanowm_l2_csgo

# RT-1 (fractal)
python src/main.py experiment=rt1 dataset=rt1/rt1 model=nanowm_b2

# Override training steps and batch size inline
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    train.max_steps=50000 train.batch_size=16
```

### Evaluation

```bash
# Evaluate a checkpoint (256 samples, seed=42, 250 DDIM steps)
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    mode=eval checkpoint_path=/path/to/checkpoint.ckpt

# Evaluate with custom sample count
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    mode=eval checkpoint_path=/path/to/checkpoint.ckpt eval.num_samples=512
```

### Long-Horizon Rollout

```bash
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    mode=rollout checkpoint_path=/path/to/checkpoint.ckpt \
    rollout.horizon=50
```

### MPC Planning (CEM)

```bash
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    mode=plan checkpoint_path=/path/to/checkpoint.ckpt \
    planning.method=cem planning.horizon=10 planning.num_samples=128
```

### Video → 3D Point Cloud

```bash
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    mode=video_to_3d checkpoint_path=/path/to/checkpoint.ckpt
```

---

## Pretrained Checkpoints

Load from HuggingFace directly:

```python
from huggingface_hub import hf_hub_download

# Download checkpoint
ckpt_path = hf_hub_download(
    repo_id="knightnemo/nanowm-b2-dino-wm-pusht-100k",
    filename="checkpoint.ckpt"
)
```

Available checkpoints:

| Domain | HF Repo | Steps |
|--------|---------|-------|
| Point Maze | `knightnemo/nanowm-b2-dino-wm-point-maze-30k` | 30k |
| Wall | `knightnemo/nanowm-b2-dino-wm-wall-15k` | 15k |
| Rope | `knightnemo/nanowm-b2-dino-wm-rope-15k` | 15k |
| Granular | `knightnemo/nanowm-b2-dino-wm-granular-15k` | 15k |
| PushT | `knightnemo/nanowm-b2-dino-wm-pusht-100k` | 100k |
| RT-1 | `knightnemo/nanowm-b2-rt1-300k` | 300k |
| CSGO | `knightnemo/nanowm-l2-csgo-100k` | 100k |

Use with CLI:

```bash
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    mode=eval checkpoint_path=$ckpt_path
```

---

## Configuration System (Hydra)

Config is composed from `src/configs/`. Key axes:

```
src/configs/
├── experiment/          # e.g. dino_wm_pusht, csgo, rt1
├── dataset/             # e.g. dino_wm/pusht, game/csgo, rt1/rt1
├── model/               # e.g. nanowm_b2, nanowm_l2_csgo
├── local/
│   └── paths.yaml       # your local paths (gitignored)
```

Override any config key on the command line:

```bash
# Change prediction target (pred-v vs pred-x0 vs pred-eps)
python src/main.py experiment=rt1 dataset=rt1/rt1 model=nanowm_b2 \
    model.pred_target=pred_x0

# Change action injection strategy
python src/main.py experiment=rt1 dataset=rt1/rt1 model=nanowm_b2 \
    model.action_injection=concat

# Change noise schedule
python src/main.py experiment=rt1 dataset=rt1/rt1 model=nanowm_b2 \
    model.noise_schedule=linear model.zero_terminal_snr=false
```

---

## Code Examples

### Loading a Trained Model Programmatically

```python
import torch
from omegaconf import OmegaConf
from src.models import NanoWM  # adjust import to actual module path

# Load config and checkpoint
cfg = OmegaConf.load("src/configs/model/nanowm_b2.yaml")
model = NanoWM(cfg)

checkpoint = torch.load("/path/to/checkpoint.ckpt", map_location="cpu")
model.load_state_dict(checkpoint["state_dict"])
model.eval()
```

### Custom Dataset with DataSource API

```python
# src/wm_datasets/my_dataset.py
from src.wm_datasets.base import DataSource
import torch

class MyRobotDataSource(DataSource):
    """Custom data source following the DataSource API."""

    def __init__(self, data_root: str, split: str = "train"):
        self.data_root = data_root
        self.split = split
        self._load_index()

    def _load_index(self):
        # Build list of (video_path, action_path) tuples
        ...

    def __len__(self) -> int:
        return len(self.index)

    def __getitem__(self, idx: int) -> dict:
        # Must return dict with keys: "video" (T, C, H, W) and "actions" (T, A)
        video = torch.zeros(16, 3, 64, 64)   # float32, [0, 1]
        actions = torch.zeros(16, 7)          # float32
        return {"video": video, "actions": actions}
```

Register in dataset config:

```yaml
# src/configs/dataset/my_robot.yaml
_target_: src.wm_datasets.my_dataset.MyRobotDataSource
data_root: ${oc.env:DATASET_DIR}/my_robot
split: train
```

### Running Autoregressive Rollout in Python

```python
import torch
from src.models import NanoWM
from src.utils.rollout import autoregressive_rollout

model = NanoWM.load_from_checkpoint("/path/to/checkpoint.ckpt")
model.eval().cuda()

# context_frames: (B, T_ctx, C, H, W), actions: (B, T_rollout, A)
context_frames = torch.randn(1, 4, 3, 64, 64).cuda()
actions = torch.randn(1, 50, 7).cuda()

with torch.no_grad():
    rollout_frames = autoregressive_rollout(
        model=model,
        context_frames=context_frames,
        actions=actions,
        num_ddim_steps=250,
        horizon=50,
    )
# rollout_frames: (B, 50, C, H, W)
```

### MPC / CEM Planning Loop

```python
from src.planning.cem import CEMPlanner

planner = CEMPlanner(
    world_model=model,
    horizon=10,
    num_samples=128,
    num_elites=10,
    num_iterations=5,
    action_dim=7,
)

obs = torch.randn(1, 4, 3, 64, 64).cuda()  # current context
best_actions = planner.plan(obs)             # (horizon, action_dim)
```

---

## Design Choices & Ablation Axes

The repo provides clean ablation across three axes (see `docs/training.md`):

| Axis | Options |
|------|---------|
| **Prediction target** | `pred_v` ✓ (best), `pred_x0`, `pred_eps` |
| **Action injection** | `additive` ✓ (best), `concat`, `cross_attn` |
| **Noise schedule** | `cosine + ZTSNR` ✓ (best), `linear`, `cosine` |

Best config (used in all main checkpoints):

```bash
model.pred_target=pred_v \
model.action_injection=additive \
model.noise_schedule=cosine \
model.zero_terminal_snr=true
```

---

## Model Variants

| Model | Params | Patch Size | Use Case |
|-------|--------|------------|----------|
| `nanowm_b2` | Base | 2 | Most domains (default) |
| `nanowm_l2_csgo` | Large | 2 | CSGO (high-res, complex) |

---

## Evaluation Metrics

Evaluated on 256 samples, seed=42, 250 DDIM steps, sequential autoregressive denoising:

| Dataset | PSNR ↑ | SSIM ↑ | LPIPS ↓ | FID ↓ |
|---------|--------|--------|---------|-------|
| Point Maze | 36.74 | 0.984 | 0.019 | 9.66 |
| Wall | 34.05 | 0.994 | 0.010 | 2.64 |
| PushT | 33.19 | 0.982 | 0.016 | 13.63 |
| Rope | 31.63 | 0.953 | 0.056 | 35.20 |
| Granular | 26.08 | 0.917 | 0.073 | 40.05 |
| RT-1 | 24.36 | 0.787 | 0.180 | 35.08 |

---

## Troubleshooting

**Missing I3D model error during eval:**
```bash
mkdir -p pretrained_models/i3d && curl -L \
    "https://www.dropbox.com/scl/fi/c5nfs6c422nlpj880jbmh/i3d_torchscript.pt?rlkey=x5xcjsrz0818i4qxyoglp5bb8&dl=1" \
    -o pretrained_models/i3d/i3d_torchscript.pt
```

**Hydra config not found:**
- Ensure you run from repo root: `cd nano-world-model`
- Check `src/configs/local/paths.yaml` exists or env vars are set

**CUDA OOM during training:**
```bash
# Reduce batch size or use gradient accumulation
python src/main.py experiment=dino_wm_pusht dataset=dino_wm/pusht model=nanowm_b2 \
    train.batch_size=4 train.grad_accumulation=4
```

**Dataset not found:**
```bash
# Verify env var is set and path exists
echo $DATASET_DIR
ls $DATASET_DIR
# See docs/datasets/README.md for download instructions
```

**Slow rollout generation:**
```bash
# Reduce DDIM steps (quality/speed tradeoff)
python src/main.py ... mode=eval eval.ddim_steps=50
```

---

## Project Structure

```
nano-world-model/
├── src/
│   ├── main.py                  # Entry point
│   ├── configs/                 # Hydra configs
│   │   ├── experiment/
│   │   ├── dataset/
│   │   ├── model/
│   │   └── local/paths.yaml     # Your paths (gitignored)
│   ├── models/                  # NanoWM model definitions
│   ├── wm_datasets/             # DataSource API + loaders
│   ├── planning/                # CEM planner
│   └── utils/                   # Rollout, metrics, visualization
├── docs/
│   ├── training.md
│   ├── evaluation.md
│   ├── config_system.md
│   ├── datasets/README.md
│   └── applications/
│       ├── planning.md
│       ├── long_rollout.md
│       └── video_to_3d.md
├── pretrained_models/
│   └── i3d/                     # FID/FVD scoring model
├── assets/                      # Demo GIFs
└── environment.yml
```

---

## References

- Built on: [Latte](https://github.com/Vchitect/Latte), [DFoT](https://github.com/kwsong0113/diffusion-forcing-transformer), [DINO-WM](https://github.com/gaoyuezhou/dino_wm), [Vid2World](https://github.com/thuml/Vid2World)
- Design inspired by: [NanoGPT](https://github.com/karpathy/nanoGPT)
- HuggingFace collection: [knightnemo/nano-world-model](https://huggingface.co/collections/knightnemo/nano-world-model)
- Project page: [simchowitzlabpublic.github.io/nano-world-model](https://simchowitzlabpublic.github.io/nano-world-model/)
