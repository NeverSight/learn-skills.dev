---
name: install-geoai
description: >
  Verify that the geoai Python package is installed and functional. If not,
  provide installation instructions. Optionally check extra dependencies
  for deep learning models.
argument-hint: "[--check] [--extras]"
allowed-tools: Bash
---

Arguments: `$@`

## Step 1 -- Check if geoai is importable

```bash
python3 -c "import geoai; print(f'geoai v{geoai.__version__}')"
```

- **Success** -> report the version and continue to Step 2 if `--check` or `--extras` was passed, otherwise stop.
- **ImportError** -> go to Step 3.

## Step 2 -- Check optional dependencies

If `--check` is present in `$@`, run a comprehensive dependency check:

```bash
python3 -c "
deps = [
    'geoai', 'geopandas', 'rasterio', 'rioxarray', 'shapely',
    'leafmap', 'numpy', 'pandas', 'matplotlib',
]
for dep in deps:
    try:
        mod = __import__(dep)
        ver = getattr(mod, '__version__', 'unknown')
        print(f'{dep}: {ver}')
    except ImportError:
        print(f'{dep}: NOT INSTALLED')
"
```

If `--extras` is present in `$@`, also check deep learning dependencies:

```bash
python3 -c "
import sys
dl_deps = ['torch', 'torchvision', 'transformers', 'timm', 'segmentation_models_pytorch']
for dep in dl_deps:
    try:
        mod = __import__(dep)
        ver = getattr(mod, '__version__', 'unknown')
        print(f'{dep}: {ver}')
    except ImportError:
        print(f'{dep}: NOT INSTALLED')

try:
    import torch
    if torch.cuda.is_available():
        print(f'CUDA: {torch.version.cuda} (device: {torch.cuda.get_device_name(0)})')
    else:
        print('CUDA: not available (CPU only)')
except ImportError:
    print('CUDA: torch not installed')
"
```

Report the results and note any missing packages.

## Step 3 -- Installation instructions

If geoai is not installed, tell the user:

> **geoai is not installed.** Install it with:
>
> ```
> pip install geoai-py
> ```
>
> For GPU-accelerated AI models (object detection, segmentation), also install PyTorch:
>
> ```
> pip install torch torchvision
> ```
>
> For the full set of optional dependencies:
>
> ```
> pip install "geoai-py[extra]"
> ```

Stop after showing the instructions. Do not attempt to install automatically unless the user explicitly asks.
