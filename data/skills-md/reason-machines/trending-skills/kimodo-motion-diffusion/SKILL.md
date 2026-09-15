---
name: kimodo-motion-diffusion
description: Generate high-quality 3D human and humanoid robot motions using Kimodo, a kinematic motion diffusion model controlled via text prompts and kinematic constraints.
triggers:
  - generate human motion with text prompt
  - create robot animation with diffusion model
  - use kimodo to generate walking motion
  - add keyframe constraints to motion generation
  - generate G1 robot motion for mujoco
  - control end effector position in motion
  - run kimodo interactive demo
  - export motion to AMASS or qpos format
---

# Kimodo Motion Diffusion

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Kimodo is a kinematic motion diffusion model trained on 700 hours of commercially-friendly optical mocap data. It generates high-quality 3D human and humanoid robot motions controlled through text prompts and kinematic constraints (full-body keyframes, end-effector positions/rotations, 2D paths, 2D waypoints).

## Installation

```bash
# Clone the repository
git clone https://github.com/nv-tlabs/kimodo.git
cd kimodo

# Install with pip (creates kimodo_gen and kimodo_demo CLI commands)
pip install -e .

# Or with Docker (recommended for Windows or clean environments)
docker build -t kimodo .
docker run --gpus all -p 7860:7860 kimodo
```

**Requirements:**
- ~17GB VRAM (GPU: RTX 3090/4090, A100 recommended)
- Linux (Windows supported via Docker)
- Models download automatically on first use from Hugging Face

## Available Models

| Model | Skeleton | Dataset | Use Case |
|-------|----------|---------|----------|
| `Kimodo-SOMA-RP-v1` | SOMA (human) | Bones Rigplay 1 (700h) | General human motion |
| `Kimodo-G1-RP-v1` | Unitree G1 (robot) | Bones Rigplay 1 (700h) | Humanoid robot motion |
| `Kimodo-SOMA-SEED-v1` | SOMA | BONES-SEED (288h) | Benchmarking |
| `Kimodo-G1-SEED-v1` | Unitree G1 | BONES-SEED (288h) | Benchmarking |
| `Kimodo-SMPLX-RP-v1` | SMPL-X | Bones Rigplay 1 (700h) | Retargeting/AMASS export |

## CLI: `kimodo_gen`

### Basic Text-to-Motion

```bash
# Generate a single motion with a text prompt (uses SOMA model by default)
kimodo_gen "a person walks forward at a moderate pace"

# Specify duration and number of samples
kimodo_gen "a person jogs in a circle" --duration 5.0 --num_samples 3

# Use the G1 robot model
kimodo_gen "a robot walks forward" --model Kimodo-G1-RP-v1 --duration 4.0

# Use SMPL-X model (for AMASS-compatible export)
kimodo_gen "a person waves their right hand" --model Kimodo-SMPLX-RP-v1

# Set a seed for reproducibility
kimodo_gen "a person sits down slowly" --seed 42

# Control diffusion steps (more = slower but higher quality)
kimodo_gen "a person does a jumping jack" --diffusion_steps 50
```

### Output Formats

```bash
# Default: saves NPZ file compatible with web demo
kimodo_gen "a person walks" --output ./outputs/walk.npz

# G1 robot: save MuJoCo qpos CSV
kimodo_gen "robot walks forward" --model Kimodo-G1-RP-v1 --output ./outputs/walk.csv

# SMPL-X: saves AMASS-compatible NPZ (stem_amass.npz)
kimodo_gen "a person waves" --model Kimodo-SMPLX-RP-v1 --output ./outputs/wave.npz
# Also writes: ./outputs/wave_amass.npz

# Disable post-processing (foot skate correction, constraint cleanup)
kimodo_gen "a person walks" --no-postprocess
```

### Multi-Prompt Sequences

```bash
# Sequence of text prompts for transitions
kimodo_gen "a person stands still" "a person walks forward" "a person stops and turns"

# With timing control per segment
kimodo_gen "a person jogs" "a person slows to a walk" "a person stops" \
  --duration 8.0 --num_samples 2
```

### Constraint-Based Generation

```bash
# Load constraints saved from the interactive demo
kimodo_gen "a person walks to a table and picks something up" \
  --constraints ./my_constraints.json

# Combine text and constraints
kimodo_gen "a person performs a complex motion" \
  --constraints ./keyframe_constraints.json \
  --model Kimodo-SOMA-RP-v1 \
  --num_samples 5
```

## Interactive Demo

```bash
# Launch the web-based demo at http://127.0.0.1:7860
kimodo_demo

# Access remotely (server setup)
kimodo_demo --server-name 0.0.0.0 --server-port 7860
```

The demo provides:
- Timeline editor for text prompts and constraints
- Full-body keyframe constraints
- 2D root path/waypoint editor
- End-effector position/rotation control
- Real-time 3D visualization with skeleton and skinned mesh
- Export of constraints as JSON and motions as NPZ

## Low-Level Python API

### Basic Model Inference

```python
from kimodo.model import Kimodo

# Initialize model (downloads automatically)
model = Kimodo(model_name="Kimodo-SOMA-RP-v1")

# Simple text-to-motion generation
result = model(
    prompts=["a person walks forward at a moderate pace"],
    duration=4.0,
    num_samples=1,
    seed=42,
)

# Result contains posed joints, rotation matrices, foot contacts
print(result["posed_joints"].shape)       # [T, J, 3]
print(result["global_rot_mats"].shape)    # [T, J, 3, 3]
print(result["local_rot_mats"].shape)     # [T, J, 3, 3]
print(result["foot_contacts"].shape)      # [T, 4]
print(result["root_positions"].shape)     # [T, 3]
```

### Advanced API with Guidance and Constraints

```python
from kimodo.model import Kimodo
import numpy as np

model = Kimodo(model_name="Kimodo-SOMA-RP-v1")

# Multi-prompt with classifier-free guidance control
result = model(
    prompts=["a person stands", "a person walks forward", "a person sits"],
    duration=9.0,
    num_samples=3,
    diffusion_steps=50,
    guidance_scale=7.5,           # classifier-free guidance weight
    seed=0,
)

# Access per-sample results
for i in range(3):
    joints = result["posed_joints"][i]   # [T, J, 3]
    print(f"Sample {i}: {joints.shape}")
```

### Working with Constraints Programmatically

```python
from kimodo.model import Kimodo
from kimodo.constraints import ConstraintSet, FullBodyKeyframe, EndEffectorConstraint
import numpy as np

model = Kimodo(model_name="Kimodo-SOMA-RP-v1")

# Create constraint set
constraints = ConstraintSet()

# Add a full-body keyframe at frame 30 (1 second at 30fps)
# keyframe_pose: [J, 3] joint positions
keyframe_pose = np.zeros((model.num_joints, 3))  # replace with actual pose
constraints.add_full_body_keyframe(frame=30, joint_positions=keyframe_pose)

# Add end-effector constraints for right hand
constraints.add_end_effector(
    joint_name="right_hand",
    frame_start=45,
    frame_end=60,
    position=np.array([0.5, 1.2, 0.3]),   # [x, y, z] in meters
    rotation=None,                           # optional rotation matrix [3,3]
)

# Add 2D waypoints for root path
constraints.add_root_waypoints(
    waypoints=np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),  # [N, 2] in meters
)

# Generate with constraints
result = model(
    prompts=["a person walks in a square"],
    duration=6.0,
    constraints=constraints,
    num_samples=2,
)
```

### Loading and Using Saved Constraints

```python
from kimodo.model import Kimodo
from kimodo.constraints import ConstraintSet
import json

model = Kimodo(model_name="Kimodo-SOMA-RP-v1")

# Load constraints saved from web demo
with open("constraints.json") as f:
    constraint_data = json.load(f)

constraints = ConstraintSet.from_dict(constraint_data)

result = model(
    prompts=["a person performs a choreographed sequence"],
    duration=8.0,
    constraints=constraints,
)
```

### Saving and Loading Generated Motions

```python
import numpy as np

# Save result
result = model(prompts=["a person walks"], duration=4.0)
np.savez("walk_motion.npz", **result)

# Load and inspect saved motion
data = np.load("walk_motion.npz")
posed_joints = data["posed_joints"]       # [T, J, 3] global joint positions
global_rot_mats = data["global_rot_mats"] # [T, J, 3, 3]
local_rot_mats = data["local_rot_mats"]   # [T, J, 3, 3]
foot_contacts = data["foot_contacts"]     # [T, 4] [L-heel, L-toe, R-heel, R-toe]
root_positions = data["root_positions"]   # [T, 3] actual root joint trajectory
smooth_root_pos = data["smooth_root_pos"] # [T, 3] smoothed root from model
global_root_heading = data["global_root_heading"]  # [T, 2] heading direction
```

## Robotics Integration

### MuJoCo Visualization (G1 Robot)

```bash
# Generate G1 motion and save as MuJoCo qpos CSV
kimodo_gen "a robot walks forward and waves" \
  --model Kimodo-G1-RP-v1 \
  --output ./robot_walk.csv \
  --duration 5.0

# Visualize in MuJoCo (edit script to point to your CSV)
python -m kimodo.scripts.mujoco_load
```

```python
# mujoco_load.py customization pattern
import mujoco
import numpy as np

# Edit these paths in the script
CSV_PATH = "./robot_walk.csv"
MJCF_PATH = "./assets/g1/g1.xml"  # path to G1 MuJoCo model

# Load qpos data
qpos_data = np.loadtxt(CSV_PATH, delimiter=",")

# Standard MuJoCo playback loop
model = mujoco.MjModel.from_xml_path(MJCF_PATH)
data = mujoco.MjData(model)
with mujoco.viewer.launch_passive(model, data) as viewer:
    for frame_qpos in qpos_data:
        data.qpos[:] = frame_qpos
        mujoco.mj_forward(model, data)
        viewer.sync()
```

### ProtoMotions Integration

```bash
# Generate motion with Kimodo
kimodo_gen "a person runs and jumps" --model Kimodo-SOMA-RP-v1 \
  --output ./run_jump.npz --duration 5.0

# Then follow ProtoMotions docs to import:
# https://github.com/NVlabs/ProtoMotions#motion-authoring-with-kimodo
```

### GMR Retargeting (SMPL-X to Other Robots)

```bash
# Generate SMPL-X motion (saves stem_amass.npz automatically)
kimodo_gen "a person performs a cartwheel" \
  --model Kimodo-SMPLX-RP-v1 \
  --output ./cartwheel.npz

# Use cartwheel_amass.npz with GMR for retargeting
# https://github.com/YanjieZe/GMR
```

## NPZ Output Format Reference

| Key | Shape | Description |
|-----|-------|-------------|
| `posed_joints` | `[T, J, 3]` | Global joint positions in meters |
| `global_rot_mats` | `[T, J, 3, 3]` | Global joint rotation matrices |
| `local_rot_mats` | `[T, J, 3, 3]` | Parent-relative joint rotation matrices |
| `foot_contacts` | `[T, 4]` | Contact labels: [L-heel, L-toe, R-heel, R-toe] |
| `smooth_root_pos` | `[T, 3]` | Smoothed root trajectory from model |
| `root_positions` | `[T, 3]` | Actual root joint (pelvis) trajectory |
| `global_root_heading` | `[T, 2]` | Heading direction (2D unit vector) |

`T` = number of frames (30fps), `J` = number of joints (skeleton-dependent)

## Scripts Reference

```bash
# Direct script execution (alternative to CLI)
python scripts/generate.py "a person walks" --duration 4.0

# MuJoCo visualization for G1 outputs
python -m kimodo.scripts.mujoco_load

# All kimodo_gen flags
kimodo_gen --help
```

## Common Patterns

### Batch Generation Pipeline

```python
from kimodo.model import Kimodo
import numpy as np
from pathlib import Path

model = Kimodo(model_name="Kimodo-SOMA-RP-v1")
output_dir = Path("./batch_outputs")
output_dir.mkdir(exist_ok=True)

prompts = [
    "a person walks forward",
    "a person runs",
    "a person jumps in place",
    "a person sits down",
    "a person picks up an object from the floor",
]

for i, prompt in enumerate(prompts):
    result = model(
        prompts=[prompt],
        duration=4.0,
        num_samples=1,
        seed=i,
    )
    out_path = output_dir / f"motion_{i:03d}.npz"
    np.savez(str(out_path), **result)
    print(f"Saved: {out_path}")
```

### Comparing Model Variants

```python
from kimodo.model import Kimodo
import numpy as np

prompt = "a person walks forward"
models = ["Kimodo-SOMA-RP-v1", "Kimodo-SOMA-SEED-v1"]

results = {}
for model_name in models:
    model = Kimodo(model_name=model_name)
    results[model_name] = model(
        prompts=[prompt],
        duration=4.0,
        seed=0,
    )
    print(f"{model_name}: joints shape = {results[model_name]['posed_joints'].shape}")
```

## Troubleshooting

**Out of VRAM (~17GB required):**
```bash
# Check available VRAM
nvidia-smi

# Use fewer samples to reduce peak VRAM
kimodo_gen "a person walks" --num_samples 1

# Reduce diffusion steps to speed up (less quality)
kimodo_gen "a person walks" --diffusion_steps 20
```

**Model download issues:**
```bash
# Models download from Hugging Face automatically
# If behind a proxy, set:
export HF_ENDPOINT=https://huggingface.co
export HUGGINGFACE_HUB_VERBOSITY=debug

# Or manually specify cache directory
export HF_HOME=/path/to/your/cache
```

**Motion quality issues:**
- Be specific in prompts: "a person walks forward at a moderate pace" > "walking"
- For complex motions, use the interactive demo to add keyframe constraints
- Increase `--diffusion_steps` (default ~20-30, try 50 for higher quality)
- Generate multiple samples (`--num_samples 5`) and select the best
- Avoid prompts with extremely fast or physically impossible actions
- The model operates at 30fps; very short durations (<1s) may yield poor results

**Foot skating artifacts:**
```bash
# Post-processing is enabled by default; only disable for debugging
kimodo_gen "a person walks" # post-processing ON (default)
kimodo_gen "a person walks" --no-postprocess  # post-processing OFF
```

**Interactive demo not loading:**
```bash
# Ensure port 7860 is available
lsof -i :7860

# Launch on a different port
kimodo_demo --server-port 7861

# For remote server access
kimodo_demo --server-name 0.0.0.0 --server-port 7860
# Then use SSH port forwarding: ssh -L 7860:localhost:7860 user@server
```
