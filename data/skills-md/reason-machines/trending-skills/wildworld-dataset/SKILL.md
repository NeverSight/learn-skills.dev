---
name: wildworld-dataset
description: WildWorld large-scale action-conditioned world modeling dataset with 108M+ frames from a photorealistic ARPG game, featuring per-frame annotations, 450+ actions, and explicit state information for generative world modeling research.
triggers:
  - use WildWorld dataset
  - load WildWorld ARPG data
  - work with WildWorld annotations
  - WildWorld world modeling
  - action conditioned video dataset
  - WildBench benchmark evaluation
  - WildWorld frame annotations
  - generative ARPG dataset
---

# WildWorld Dataset Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

## What WildWorld Is

**WildWorld** is a large-scale action-conditioned world modeling dataset automatically collected from a photorealistic AAA action role-playing game (ARPG). It is designed for training and evaluating **dynamic world models** — generative models that predict future game states given past observations and player actions.

### Key Statistics

| Property | Value |
|---|---|
| Total frames | 108M+ |
| Actions | 450+ semantically meaningful |
| Monster species | 29 |
| Player characters | 4 |
| Weapon types | 4 |
| Distinct stages | 5 |
| Max clip length | 30+ minutes continuous |

### Per-Frame Annotations

Every frame includes:
- **Character skeletons** — joint positions for player and monsters
- **Actions & states** — HP, animation state, stamina, etc.
- **Camera poses** — position, rotation, field of view
- **Depth maps** — monocular depth for each frame
- **Hierarchical captions** — action-level and sample-level natural language descriptions

---

## Project Status

> ⚠️ As of March 2026, the dataset and WildBench benchmark have **not yet been released**. Monitor the repository for updates.

```bash
# Watch the repository for dataset release
# https://github.com/ShandaAI/WildWorld
```

---

## Repository Setup

```bash
# Clone the repository
git clone https://github.com/ShandaAI/WildWorld.git
cd WildWorld

# Install dependencies (when benchmark code is released)
pip install -r requirements.txt
```

---

## Expected Dataset Structure

Based on the paper and framework description, the dataset is expected to follow this structure:

```
WildWorld/
├── data/
│   ├── sequences/
│   │   ├── stage_01/
│   │   │   ├── clip_000001/
│   │   │   │   ├── frames/          # RGB frames (e.g., PNG)
│   │   │   │   ├── depth/           # Depth maps
│   │   │   │   ├── skeleton/        # Per-frame skeleton JSON
│   │   │   │   ├── states/          # HP, animation, stamina JSON
│   │   │   │   ├── camera/          # Camera pose JSON
│   │   │   │   └── actions/         # Action label files
│   │   │   └── clip_000002/
│   │   └── stage_02/
│   └── captions/
│       ├── action_level/            # Per-action descriptions
│       └── sample_level/            # Clip-level descriptions
├── benchmark/
│   └── wildbench/                   # WildBench evaluation code
├── assets/
│   └── framework-arxiv.png
├── LICENSE
└── README.md
```

---

## Working with the Dataset (Anticipated API)

### Loading Frame Annotations

```python
import json
import os
from pathlib import Path
from PIL import Image
import numpy as np

class WildWorldClip:
    """Helper class to load a WildWorld clip and its annotations."""

    def __init__(self, clip_dir: str):
        self.clip_dir = Path(clip_dir)
        self.frames_dir = self.clip_dir / "frames"
        self.depth_dir = self.clip_dir / "depth"
        self.skeleton_dir = self.clip_dir / "skeleton"
        self.states_dir = self.clip_dir / "states"
        self.camera_dir = self.clip_dir / "camera"
        self.actions_dir = self.clip_dir / "actions"

    def get_frame(self, frame_id: int) -> Image.Image:
        frame_path = self.frames_dir / f"{frame_id:06d}.png"
        return Image.open(frame_path)

    def get_depth(self, frame_id: int) -> np.ndarray:
        depth_path = self.depth_dir / f"{frame_id:06d}.npy"
        return np.load(depth_path)

    def get_skeleton(self, frame_id: int) -> dict:
        skeleton_path = self.skeleton_dir / f"{frame_id:06d}.json"
        with open(skeleton_path) as f:
            return json.load(f)

    def get_state(self, frame_id: int) -> dict:
        """Returns HP, animation state, stamina, etc."""
        state_path = self.states_dir / f"{frame_id:06d}.json"
        with open(state_path) as f:
            return json.load(f)

    def get_camera(self, frame_id: int) -> dict:
        """Returns camera position, rotation, and FOV."""
        camera_path = self.camera_dir / f"{frame_id:06d}.json"
        with open(camera_path) as f:
            return json.load(f)

    def get_action(self, frame_id: int) -> dict:
        action_path = self.actions_dir / f"{frame_id:06d}.json"
        with open(action_path) as f:
            return json.load(f)

    def iter_frames(self, start: int = 0, end: int = None):
        """Iterate over all frames in the clip."""
        frame_files = sorted(self.frames_dir.glob("*.png"))
        for frame_path in frame_files[start:end]:
            frame_id = int(frame_path.stem)
            yield {
                "frame_id": frame_id,
                "frame": self.get_frame(frame_id),
                "depth": self.get_depth(frame_id),
                "skeleton": self.get_skeleton(frame_id),
                "state": self.get_state(frame_id),
                "camera": self.get_camera(frame_id),
                "action": self.get_action(frame_id),
            }


# Usage
clip = WildWorldClip("data/sequences/stage_01/clip_000001")
for sample in clip.iter_frames(start=0, end=100):
    frame_id = sample["frame_id"]
    state = sample["state"]
    action = sample["action"]
    print(f"Frame {frame_id}: HP={state.get('hp')}, Action={action.get('name')}")
```

### PyTorch Dataset

```python
import torch
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import json
import numpy as np
from PIL import Image
import torchvision.transforms as T

class WildWorldDataset(Dataset):
    """
    PyTorch Dataset for WildWorld action-conditioned world modeling.
    
    Returns sequences of (frames, actions, states) for next-frame prediction.
    """

    def __init__(
        self,
        root_dir: str,
        sequence_length: int = 16,
        image_size: tuple = (256, 256),
        stage: str = None,
        split: str = "train",
    ):
        self.root_dir = Path(root_dir)
        self.sequence_length = sequence_length
        self.image_size = image_size

        self.transform = T.Compose([
            T.Resize(image_size),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225]),
        ])

        # Discover all clips
        self.clips = self._discover_clips(stage, split)
        self.samples = self._build_sample_index()

    def _discover_clips(self, stage, split):
        clips = []
        stage_dirs = (
            [self.root_dir / "data" / "sequences" / stage]
            if stage
            else sorted((self.root_dir / "data" / "sequences").iterdir())
        )
        for stage_dir in stage_dirs:
            if stage_dir.is_dir():
                for clip_dir in sorted(stage_dir.iterdir()):
                    if clip_dir.is_dir():
                        clips.append(clip_dir)
        # Simple train/val split
        split_idx = int(len(clips) * 0.9)
        return clips[:split_idx] if split == "train" else clips[split_idx:]

    def _build_sample_index(self):
        """Build index of (clip_dir, start_frame) pairs."""
        samples = []
        for clip_dir in self.clips:
            frames = sorted((clip_dir / "frames").glob("*.png"))
            n_frames = len(frames)
            for start in range(0, n_frames - self.sequence_length, self.sequence_length // 2):
                samples.append((clip_dir, start))
        return samples

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        clip_dir, start = self.samples[idx]
        frames_dir = clip_dir / "frames"
        frame_files = sorted(frames_dir.glob("*.png"))[start:start + self.sequence_length]

        frames, actions, states = [], [], []
        for frame_path in frame_files:
            frame_id = int(frame_path.stem)

            # Load RGB frame
            img = Image.open(frame_path).convert("RGB")
            frames.append(self.transform(img))

            # Load action
            action_path = clip_dir / "actions" / f"{frame_id:06d}.json"
            with open(action_path) as f:
                action_data = json.load(f)
            actions.append(action_data.get("action_id", 0))

            # Load state
            state_path = clip_dir / "states" / f"{frame_id:06d}.json"
            with open(state_path) as f:
                state_data = json.load(f)
            states.append([
                state_data.get("hp", 1.0),
                state_data.get("stamina", 1.0),
                state_data.get("animation_id", 0),
            ])

        return {
            "frames": torch.stack(frames),            # (T, C, H, W)
            "actions": torch.tensor(actions, dtype=torch.long),   # (T,)
            "states": torch.tensor(states, dtype=torch.float32),  # (T, S)
        }


# Usage
dataset = WildWorldDataset(
    root_dir="/path/to/WildWorld",
    sequence_length=16,
    image_size=(256, 256),
    split="train",
)

loader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4)

for batch in loader:
    frames = batch["frames"]   # (B, T, C, H, W)
    actions = batch["actions"] # (B, T)
    states = batch["states"]   # (B, T, S)
    print(f"Frames: {frames.shape}, Actions: {actions.shape}")
    break
```

### Filtering by Action Type

```python
# Action categories in WildWorld
ACTION_CATEGORIES = {
    "movement": ["walk", "run", "sprint", "dodge", "jump"],
    "attack": ["light_attack", "heavy_attack", "combo_finisher"],
    "skill": ["skill_cast_1", "skill_cast_2", "skill_cast_3", "skill_cast_4"],
    "defense": ["block", "parry", "guard"],
    "idle": ["idle", "idle_combat"],
}

def filter_clips_by_action(dataset_root: str, action_category: str) -> list:
    """Find all frame indices that contain a specific action category."""
    root = Path(dataset_root)
    results = []
    target_actions = ACTION_CATEGORIES.get(action_category, [])

    for clip_dir in root.glob("data/sequences/**"):
        if not clip_dir.is_dir():
            continue
        for action_file in sorted((clip_dir / "actions").glob("*.json")):
            with open(action_file) as f:
                data = json.load(f)
            if data.get("action_name") in target_actions:
                results.append({
                    "clip": str(clip_dir),
                    "frame_id": int(action_file.stem),
                    "action": data.get("action_name"),
                })
    return results

# Find all skill cast frames
skill_frames = filter_clips_by_action("/path/to/WildWorld", "skill")
print(f"Found {len(skill_frames)} skill cast frames")
```

---

## WildBench Evaluation

```python
# WildBench evaluates world models on next-frame prediction quality.
# Expected metrics: FVD, PSNR, SSIM, action accuracy

class WildBenchEvaluator:
    """Evaluator for world model predictions on WildBench."""

    def __init__(self, benchmark_dir: str):
        self.benchmark_dir = Path(benchmark_dir)
        self.metrics = {}

    def evaluate(self, model, dataloader):
        from torchmetrics.image import StructuralSimilarityIndexMeasure, PeakSignalNoiseRatio

        ssim = StructuralSimilarityIndexMeasure()
        psnr = PeakSignalNoiseRatio()

        all_psnr, all_ssim = [], []

        for batch in dataloader:
            frames = batch["frames"]       # (B, T, C, H, W)
            actions = batch["actions"]     # (B, T)
            states = batch["states"]       # (B, T, S)

            # Use first T-1 frames to predict the T-th frame
            context_frames = frames[:, :-1]
            context_actions = actions[:, :-1]
            target_frame = frames[:, -1]

            with torch.no_grad():
                predicted_frame = model(context_frames, context_actions, states[:, :-1])

            all_psnr.append(psnr(predicted_frame, target_frame).item())
            all_ssim.append(ssim(predicted_frame, target_frame).item())

        return {
            "PSNR": np.mean(all_psnr),
            "SSIM": np.mean(all_ssim),
        }
```

---

## Citation

```bibtex
@misc{li2026wildworldlargescaledatasetdynamic,
      title={WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG}, 
      author={Zhen Li and Zian Meng and Shuwei Shi and Wenshuo Peng and Yuwei Wu and Bo Zheng and Chuanhao Li and Kaipeng Zhang},
      year={2026},
      eprint={2603.23497},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2603.23497}, 
}
```

---

## Resources

- **Project Page**: https://shandaai.github.io/wildworld-project/
- **arXiv Paper**: https://arxiv.org/abs/2603.23497
- **YouTube Demo**: https://www.youtube.com/watch?v=9vcSg553r2g
- **GitHub**: https://github.com/ShandaAI/WildWorld

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Dataset not yet available | Monitor the repo; dataset release is pending as of March 2026 |
| Frame loading OOM | Reduce `sequence_length` or `image_size` in the Dataset |
| Missing annotation files | Check that all subdirs (frames, depth, skeleton, states, camera, actions) are fully downloaded |
| Slow DataLoader | Increase `num_workers`, use SSD storage, or preprocess to HDF5 |
| Benchmark code not found | The `benchmark/wildbench` directory will be released separately — watch the repo |
