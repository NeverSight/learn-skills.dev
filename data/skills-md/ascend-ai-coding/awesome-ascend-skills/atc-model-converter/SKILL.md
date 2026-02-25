---
name: atc-model-converter
description: Complete toolkit for Huawei Ascend NPU model conversion and inference. (1) Convert ONNX models to .om format using ATC tool with multi-CANN version support (8.3.RC1, 8.5.0+). (2) Run Python inference on OM models using ais_bench. (3) Compare precision between CPU ONNX and NPU OM outputs. (4) End-to-end YOLO inference with Ultralytics preprocessing/postprocessing - supports Detection, Pose, Segmentation, OBB tasks. Use when converting, testing, or deploying models on Ascend AI processors.
keywords:
    - inference
    - 模型转换
    - 推理
    - 小模型
    - onnx
    - om
---

# ATC Model Converter

Complete guide for converting ONNX models to Ascend AI processor compatible format using ATC (Ascend Tensor Compiler) tool.

**Supported CANN Versions:** 8.3.RC1, 8.5.0

---

## ⚠️ Critical Compatibility Requirements

Before starting, ensure your environment meets these requirements:

| Component | Requirement | Why |
|-----------|-------------|-----|
| **Python** | 3.7, 3.8, 3.9, or **3.10** | Python 3.11+ incompatible with CANN 8.1.RC1 |
| **NumPy** | **< 2.0** (e.g., 1.26.4) | CANN uses deprecated NumPy API |
| **ONNX Opset** | 11 or 13 (for CANN 8.1.RC1) | Higher opset versions not supported |

**Quick Environment Setup:**
```bash
# Create Python 3.10 environment (recommended)
conda create -n atc_py310 python=3.10 -y
conda activate atc_py310

# Install compatible dependencies
pip install torch torchvision ultralytics onnx onnxruntime
pip install "numpy<2.0" --force-reinstall
pip install decorator attrs absl-py psutil protobuf sympy
```

---

## ⚠️ IMPORTANT: SoC Version Must Match Exactly

> **SoC version in ATC conversion must exactly match your target device!**
> 
> ```bash
> # Get exact SoC version from your device
> npu-smi info | grep Name
> # Output: Name: 910B3 → Use: --soc_version=Ascend910B3
> # Output: Name: 310P3 → Use: --soc_version=Ascend310P3
> ```
> 
> **Common Error:**
> ```
> [ACL ERROR] EE1001: supported socVersion=Ascend910B3, 
> but the model socVersion=Ascend910B
> ```
> **Fix:** Use exact SoC version from `npu-smi info`, not generic version!

---

## Quick Start

```bash
# 1. Check your CANN version and environment
./scripts/check_env_enhanced.sh

# 2. Source the appropriate environment
source /usr/local/Ascend/ascend-toolkit/set_env.sh  # For 8.1.RC1/8.3.RC1
# OR
source /usr/local/Ascend/cann/set_env.sh            # For 8.5.0+

# 3. Basic ONNX to OM conversion
atc --model=model.onnx --framework=5 --output=output_model \
    --soc_version=Ascend910B3

# With input shape specification
atc --model=model.onnx --framework=5 --output=output_model \
    --soc_version=Ascend910B3 \
    --input_shape="input:1,3,640,640"
```

---

## YOLO Model Conversion & Inference

### YOLO Task Types & Output Formats

| Task | Model Example | ONNX Output | Post-processing |
|------|---------------|-------------|-----------------|
| **Detection** | yolo26n.pt | `(1, 84, 8400)` | decode + NMS |
| **Pose** | yolo26n-pose.pt | `(1, 300, 57)` | filter only |
| **Segmentation** | yolo26n-seg.pt | `(1, 116, 8400)` | decode + NMS + mask |
| **OBB** | yolo26n-obb.pt | `(1, 15, 8400)` | decode + NMS |

> **Note:** YOLO ONNX outputs are raw feature maps, not processed detections. The `yolo_om_infer.py` script handles decode + NMS automatically.

### Step 1: Export YOLO to ONNX

```python
from ultralytics import YOLO

model = YOLO('yolo26n.pt')  # or yolo26n-pose.pt, yolo26n-seg.pt, etc.

# Export with opset 11 for CANN 8.1.RC1 compatibility
model.export(format='onnx', imgsz=640, opset=11, simplify=True)
```

### Step 2: Convert to OM

```bash
# Get your SoC version first
npu-smi info | grep Name

# Convert
atc --model=yolo26n.onnx --framework=5 --output=yolo26n \
    --soc_version=Ascend910B3 \
    --input_shape="images:1,3,640,640"
```

### Step 3: Run Inference

```bash
# Detection (default)
python3 scripts/yolo_om_infer.py --model yolo26n.om \
    --source image.jpg --task detect --output result.jpg

# Pose estimation
python3 scripts/yolo_om_infer.py --model yolo26n-pose.om \
    --source image.jpg --task pose --output result_pose.jpg

# Segmentation
python3 scripts/yolo_om_infer.py --model yolo26n-seg.om \
    --source image.jpg --task segment --output result_seg.jpg

# Oriented Bounding Box
python3 scripts/yolo_om_infer.py --model yolo26n-obb.om \
    --source image.jpg --task obb --output result_obb.jpg
```

### YOLO Python API

```python
from yolo_om_infer import YoloOMInferencer, draw_results

# Initialize for detection
inferencer = YoloOMInferencer(
    model_path="yolo26n.om",
    task="detect",  # or "pose", "segment", "obb"
    device_id=0,
    conf_thres=0.25,
    iou_thres=0.45
)

# Run inference
result = inferencer("image.jpg")

# Access results
print(f"Detections: {result['num_detections']}")
print(f"Inference time: {result['timing']['infer_ms']:.1f}ms")

for det in result['detections']:
    print(f"  {det['cls_name']}: {det['conf']:.2f} at {det['box']}")

# Cleanup
inferencer.free_resource()
```

For detailed YOLO guide, see [YOLO_GUIDE.md](references/YOLO_GUIDE.md).

---

## OM Model Inference (General)

After converting your model to OM format, use ais_bench for Python inference.

### Install ais_bench

```bash
# Download pre-built wheel packages (recommended)
# See: https://gitee.com/ascend/tools/blob/master/ais-bench_workload/tool/ais_bench/README.md

# Example for Python 3.10, aarch64:
wget https://aisbench.obs.myhuaweicloud.com/packet/ais_bench_infer/0.0.2/ait/aclruntime-0.0.2-cp310-cp310-linux_aarch64.whl
wget https://aisbench.obs.myhuaweicloud.com/packet/ais_bench_infer/0.0.2/ait/ais_bench-0.0.2-py3-none-any.whl

pip3 install ./aclruntime-*.whl ./ais_bench-*.whl
```

### Basic Inference

```bash
# Print model info
python3 scripts/infer_om.py --model model.om --info

# Run inference with random input
python3 scripts/infer_om.py --model model.om --input-shape "1,3,640,640"

# Run inference with actual input
python3 scripts/infer_om.py --model model.om --input test.npy --output result.npy
```

### Python API

```python
from ais_bench.infer.interface import InferSession
import numpy as np

session = InferSession(device_id=0, model_path="model.om")
print("Inputs:", [(i.name, i.shape) for i in session.get_inputs()])
print("Outputs:", [(o.name, o.shape) for o in session.get_outputs()])

input_data = np.random.randn(1, 3, 640, 640).astype(np.float32)
outputs = session.infer([input_data], mode='static')

print(f"Inference time: {session.summary().exec_time_list[-1]:.3f} ms")
session.free_resource()
```

See [INFERENCE.md](references/INFERENCE.md) for detailed ais_bench usage.

---

## Precision Comparison

Verify conversion accuracy by comparing ONNX (CPU) vs OM (NPU) outputs.

```bash
# Basic comparison
python3 scripts/compare_precision.py --onnx model.onnx --om model.om --input test.npy

# With custom tolerances
python3 scripts/compare_precision.py --onnx model.onnx --om model.om --input test.npy \
    --atol 1e-3 --rtol 1e-2
```

| Metric | Description | Good Value |
|--------|-------------|------------|
| `cosine_similarity` | 1.0 = identical | >0.99 |
| `max_abs_diff` | Maximum absolute difference | <1e-3 (FP32) |
| `is_close` | Pass/fail based on atol/rtol | True |

---

## CANN Version Guide

| CANN Version | Environment Path | Notes |
|--------------|------------------|-------|
| 8.3.RC1 | `/usr/local/Ascend/ascend-toolkit/set_env.sh` | Standard installation |
| 8.5.0+ | `/usr/local/Ascend/cann/set_env.sh` | Must install matching ops package |

```bash
# Auto-detect CANN version
./scripts/setup_env.sh
```

---

## Core Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--model` | Yes | Input ONNX model path | `--model=resnet50.onnx` |
| `--framework` | Yes | Framework type (5=ONNX) | `--framework=5` |
| `--output` | Yes | Output OM model path | `--output=resnet50` |
| `--soc_version` | Yes | **Must match device exactly** | `--soc_version=Ascend910B3` |
| `--input_shape` | Optional | Input tensor shapes | `--input_shape="input:1,3,224,224"` |
| `--precision_mode` | Optional | Precision mode | `--precision_mode=force_fp16` |

For complete parameters, see [PARAMETERS.md](references/PARAMETERS.md).

---

## SoC Version Reference

| Device | SoC Version | How to Check |
|--------|-------------|--------------|
| Atlas 910B3 | Ascend910B3 | `npu-smi info \| grep Name` |
| Atlas 310P | Ascend310P1/P3 | `npu-smi info \| grep Name` |
| Atlas 200I DK A2 | Ascend310B4 | `npu-smi info \| grep Name` |

**Always verify with `npu-smi info` - do not assume version!**

---

## Troubleshooting

### Error: Opname not found in model
```bash
# Verify input names
python3 scripts/get_onnx_info.py model.onnx

# Use correct name in conversion
atc --model=model.onnx --input_shape="correct_name:1,3,224,224" ...
```

### Error: Invalid soc_version
```bash
# Check actual chip version - must be EXACT match
npu-smi info | grep Name
# Use: Ascend + Name value (e.g., Ascend910B3, not Ascend910B)
```

### Conversion Too Slow
```bash
export TE_PARALLEL_COMPILER=16
atc --model=model.onnx ...
```

### YOLO Detection Results Look Wrong
- Ensure you're using correct `--task` parameter
- Detection models need decode + NMS (script handles this)
- Pose models output top-300 detections (no NMS needed)

See [FAQ.md](references/FAQ.md) for more troubleshooting.

---

## Resources

### scripts/
**Conversion & Environment:**
- **`check_env_enhanced.sh`** - ⭐ Comprehensive compatibility check
- `get_onnx_info.py` - Inspect ONNX model inputs/outputs
- `setup_env.sh` - Auto-setup CANN environment with SoC warning
- `convert_onnx.sh` - Batch conversion helper

**Inference & Testing:**
- **`yolo_om_infer.py`** - ⭐ End-to-end YOLO inference (detect/pose/segment/obb)
- **`infer_om.py`** - ⭐ Python inference for OM models using ais_bench
- **`compare_precision.py`** - ⭐ Compare ONNX vs OM output precision

### references/
- **[YOLO_GUIDE.md](references/YOLO_GUIDE.md)** - ⭐ YOLO detailed guide (formats, post-processing)
- [PARAMETERS.md](references/PARAMETERS.md) - Complete ATC parameter reference
- [AIPP_CONFIG.md](references/AIPP_CONFIG.md) - AIPP configuration guide
- [INFERENCE.md](references/INFERENCE.md) - ais_bench inference guide
- [FAQ.md](references/FAQ.md) - Frequently asked questions
- [CANN_VERSIONS.md](references/CANN_VERSIONS.md) - Version-specific guidance
