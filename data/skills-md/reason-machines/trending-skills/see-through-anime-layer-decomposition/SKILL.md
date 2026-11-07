---
name: see-through-anime-layer-decomposition
description: Expertise in See-through, a framework for single-image layer decomposition of anime characters into manipulatable 2.5D PSD files using diffusion models.
triggers:
  - decompose anime character into layers
  - split anime illustration into PSD layers
  - see-through layer decomposition
  - anime character layer separation
  - extract anime character body parts
  - generate layered PSD from anime image
  - anime 2.5D model from single image
  - segment anime character into semantic layers
---

# See-through: Anime Character Layer Decomposition

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

See-through is a research framework (SIGGRAPH 2026, conditionally accepted) that decomposes a single anime illustration into up to **23 fully inpainted, semantically distinct layers** with inferred drawing orders — exporting a layered PSD file suitable for 2.5D animation workflows.

## What It Does

- Decomposes a single anime image into semantic layers (hair, face, eyes, clothing, accessories, etc.)
- Inpaints occluded regions so each layer is complete
- Infers pseudo-depth ordering using a fine-tuned Marigold model
- Exports layered `.psd` files with depth maps and segmentation masks
- Supports depth-based and left-right stratification for further refinement

## Installation

```bash
# 1. Create and activate environment
conda create -n see_through python=3.12 -y
conda activate see_through

# 2. Install PyTorch with CUDA 12.8
pip install torch==2.8.0+cu128 torchvision==0.23.0+cu128 torchaudio==2.8.0+cu128 \
  --index-url https://download.pytorch.org/whl/cu128

# 3. Install core dependencies
pip install -r requirements.txt

# 4. Create assets symlink
ln -sf common/assets assets
```

### Optional Annotator Tiers

Install only what you need:

```bash
# Body parsing (detectron2 — for body attribute tagging)
pip install --no-build-isolation -r requirements-inference-annotators.txt

# SAM2 (language-guided segmentation)
pip install --no-build-isolation -r requirements-inference-sam2.txt

# Instance segmentation (mmcv/mmdet — recommended for UI)
pip install -r requirements-inference-mmdet.txt
```

> Always run all scripts from the **repository root** as the working directory.

## Models

Models are hosted on HuggingFace and downloaded automatically on first use:

| Model | HuggingFace ID | Purpose |
|-------|---------------|---------|
| LayerDiff 3D | `layerdifforg/seethroughv0.0.2_layerdiff3d` | SDXL-based transparent layer generation |
| Marigold Depth | `24yearsold/seethroughv0.0.1_marigold` | Anime pseudo-depth estimation |
| SAM Body Parsing | `24yearsold/l2d_sam_iter2` | 19-part semantic body segmentation |

## Key CLI Commands

### Main Pipeline: Layer Decomposition to PSD

```bash
# Single image → layered PSD
python inference/scripts/inference_psd.py \
  --srcp assets/test_image.png \
  --save_to_psd

# Entire directory of images
python inference/scripts/inference_psd.py \
  --srcp path/to/image_folder/ \
  --save_to_psd
```

Output is saved to `workspace/layerdiff_output/` by default. Each run produces:
- A layered `.psd` file with semantically separated layers
- Intermediate depth maps
- Segmentation masks

### Heuristic Post-Processing

After the main pipeline, further split layers using `heuristic_partseg.py`:

```bash
# Depth-based stratification (e.g., separate near/far handwear)
python inference/scripts/heuristic_partseg.py seg_wdepth \
  --srcp workspace/test_samples_output/PV_0047_A0020.psd \
  --target_tags handwear

# Left-right stratification
python inference/scripts/heuristic_partseg.py seg_wlr \
  --srcp workspace/test_samples_output/PV_0047_A0020_wdepth.psd \
  --target_tags handwear-1
```

### Synthetic Training Data Generation

```bash
python inference/scripts/syn_data.py
```

## Python API Usage

### Running the Full Pipeline Programmatically

```python
import subprocess
import os

def decompose_anime_image(image_path: str, output_dir: str = "workspace/layerdiff_output") -> str:
    """
    Run See-through layer decomposition on a single anime image.
    Returns path to the output PSD file.
    """
    result = subprocess.run(
        [
            "python", "inference/scripts/inference_psd.py",
            "--srcp", image_path,
            "--save_to_psd",
        ],
        capture_output=True,
        text=True,
        cwd=os.getcwd()  # Must run from repo root
    )
    if result.returncode != 0:
        raise RuntimeError(f"Decomposition failed:\n{result.stderr}")
    
    # Derive expected output filename
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    psd_path = os.path.join(output_dir, f"{base_name}.psd")
    return psd_path


# Example usage
psd_output = decompose_anime_image("assets/test_image.png")
print(f"PSD saved to: {psd_output}")
```

### Batch Processing a Directory

```python
import subprocess
from pathlib import Path

def batch_decompose(input_dir: str, output_dir: str = "workspace/layerdiff_output"):
    """Process all images in a directory."""
    result = subprocess.run(
        [
            "python", "inference/scripts/inference_psd.py",
            "--srcp", input_dir,
            "--save_to_psd",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Batch processing failed:\n{result.stderr}")
    
    output_psds = list(Path(output_dir).glob("*.psd"))
    print(f"Generated {len(output_psds)} PSD files in {output_dir}")
    return output_psds

# Example
psds = batch_decompose("path/to/my_anime_images/")
```

### Post-Processing: Depth and LR Splits

```python
import subprocess

def split_by_depth(psd_path: str, target_tags: list[str]) -> str:
    """Apply depth-based layer stratification to a PSD."""
    tags_str = " ".join(target_tags)
    result = subprocess.run(
        [
            "python", "inference/scripts/heuristic_partseg.py",
            "seg_wdepth",
            "--srcp", psd_path,
            "--target_tags", *target_tags,
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    # Output naming convention: original name + _wdepth suffix
    base = psd_path.replace(".psd", "_wdepth.psd")
    return base


def split_by_lr(psd_path: str, target_tags: list[str]) -> str:
    """Apply left-right layer stratification to a PSD."""
    result = subprocess.run(
        [
            "python", "inference/scripts/heuristic_partseg.py",
            "seg_wlr",
            "--srcp", psd_path,
            "--target_tags", *target_tags,
        ],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return psd_path.replace(".psd", "_wlr.psd")


# Full post-processing pipeline example
psd = "workspace/test_samples_output/PV_0047_A0020.psd"
depth_psd = split_by_depth(psd, ["handwear"])
lr_psd = split_by_lr(depth_psd, ["handwear-1"])
print(f"Final PSD with depth+LR splits: {lr_psd}")
```

### Loading and Inspecting PSD Output

```python
from psd_tools import PSDImage  # pip install psd-tools

def inspect_psd_layers(psd_path: str):
    """List all layers in a See-through output PSD."""
    psd = PSDImage.open(psd_path)
    print(f"Canvas size: {psd.width}x{psd.height}")
    print(f"Total layers: {len(list(psd.descendants()))}")
    print("\nLayer structure:")
    for layer in psd:
        print(f"  [{layer.kind}] '{layer.name}' — "
              f"bbox: {layer.bbox}, visible: {layer.is_visible()}")
    return psd

psd = inspect_psd_layers("workspace/layerdiff_output/my_character.psd")
```

### Interactive Body Part Segmentation (Notebook)

Open and run the provided demo notebook:

```bash
jupyter notebook inference/demo/bodypartseg_sam.ipynb
```

This demonstrates interactive 19-part body segmentation with visualization using the SAM body parsing model.

## Dataset Preparation for Training

See-through uses Live2D model files as training data. Setup requires a separate repo:

```bash
# 1. Clone the CubismPartExtr utility
git clone https://github.com/shitagaki-lab/CubismPartExtr
# Follow its README to download sample model files and prepare workspace/

# 2. Run data parsing scripts per README_datapipeline.md
# (scripts are in inference/scripts/ — check docstrings for details)
```

## Launching the UI

```bash
# Requires workspace/datasets/ at repo root (contains sample data)
# Recommended: install mmdet tier first
pip install -r requirements-inference-mmdet.txt

# Then follow ui/README.md for launch instructions
cd ui
# See ui/README.md for the specific launch command
```

## Directory Structure

```
see-through/
├── inference/
│   ├── scripts/
│   │   ├── inference_psd.py        # Main pipeline
│   │   ├── heuristic_partseg.py    # Depth/LR post-processing
│   │   └── syn_data.py             # Synthetic data generation
│   └── demo/
│       └── bodypartseg_sam.ipynb   # Interactive segmentation demo
├── common/
│   ├── assets/                     # Test images, etc.
│   └── live2d/
│       └── scrap_model.py          # Full body tag definitions
├── ui/                             # User interface
├── workspace/                      # Runtime outputs (auto-created)
│   ├── layerdiff_output/           # Default PSD output location
│   ├── datasets/                   # Required for UI
│   └── test_samples_output/        # Sample outputs
├── requirements.txt
├── requirements-inference-annotators.txt
├── requirements-inference-sam2.txt
├── requirements-inference-mmdet.txt
└── README_datapipeline.md
```

## Common Patterns

### Pattern: End-to-End Single Image Workflow

```bash
# Step 1: Decompose
python inference/scripts/inference_psd.py \
  --srcp assets/test_image.png \
  --save_to_psd

# Step 2: Depth-split a specific part tag
python inference/scripts/heuristic_partseg.py seg_wdepth \
  --srcp workspace/layerdiff_output/test_image.psd \
  --target_tags arm sleeve

# Step 3: Left-right split
python inference/scripts/heuristic_partseg.py seg_wlr \
  --srcp workspace/layerdiff_output/test_image_wdepth.psd \
  --target_tags arm-1 sleeve-1
```

### Pattern: Check Available Body Tags

```python
# Body tag definitions are in common/live2d/scrap_model.py
import importlib.util, sys
spec = importlib.util.spec_from_file_location(
    "scrap_model", "common/live2d/scrap_model.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
# Inspect the module for tag constants/enums
print(dir(mod))
```

## ComfyUI Integration

A community-maintained ComfyUI node is available:

```
https://github.com/jtydhr88/ComfyUI-See-through
```

Install via ComfyUI Manager or clone into `ComfyUI/custom_nodes/`.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` for detectron2/mmcv | Install the appropriate optional tier: `pip install --no-build-isolation -r requirements-inference-annotators.txt` |
| Scripts fail with path errors | Always run from the **repository root**, not from within subdirectories |
| UI fails to launch | Install mmdet tier: `pip install -r requirements-inference-mmdet.txt`; ensure `workspace/datasets/` exists |
| CUDA out of memory | Use a GPU with ≥16GB VRAM; SDXL-based LayerDiff 3D is memory-intensive |
| Assets not found | Re-run `ln -sf common/assets assets` from repo root |
| SAM2 install fails | Use `--no-build-isolation` flag as shown in the install commands |
| Output PSD empty or malformed | Check `workspace/layerdiff_output/` for intermediate depth/mask files to diagnose which stage failed |

## Citation

```bibtex
@article{lin2026seethrough,
  title={See-through: Single-image Layer Decomposition for Anime Characters},
  author={Lin, Jian and Li, Chengze and Qin, Haoyun and Chan, Kwun Wang and
          Jin, Yanghua and Liu, Hanyuan and Choy, Stephen Chun Wang and Liu, Xueting},
  journal={arXiv preprint arXiv:2602.03749},
  year={2026}
}
```
