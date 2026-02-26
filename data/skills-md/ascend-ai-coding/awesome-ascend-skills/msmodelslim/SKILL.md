---
name: msmodelslim
description: Huawei Ascend NPU model compression tool (msModelSlim). Use for LLM quantization (W4A8, W8A8, W8A8S, W8A16), MoE model compression, multimodal model compression (Qwen-VL, InternVL, HunyuanVideo, FLUX, SD3), calibration data preparation, precision auto-tuning, sensitive layer analysis, custom model integration, and deployment in MindIE/vLLM-Ascend. Supports Qwen, LLaMA, DeepSeek, GLM, Kimi, InternLM and more.
keywords:
    - model compression
    - quantization
    - 量化
    - 模型压缩
---

# msModelSlim - Ascend Model Compression Tool

MindStudio ModelSlim (msModelSlim) is a model compression tool optimized for Huawei Ascend AI processors. It supports quantization and compression for LLMs, MoE models, and multimodal models.

---

## Quick Start

### One-Click Quantization (V1 - Recommended)

V1 automatic quantization uses configuration files from `lab_practice/` directory.

```bash
# Basic W8A8 quantization for Qwen2.5-7B-Instruct
# Config files located at: lab_practice/<model_series>/<model>-<quant_type>-v1.yaml
msmodelslim quant \
    --model_path /path/to/Qwen2.5-7B-Instruct \
    --save_path /path/to/output \
    --device npu \
    --model_type Qwen2.5-7B-Instruct \
    --config_path /path/to/msmodelslim/lab_practice/qwen2.5/qwen2.5-7b-w8a8-v1.yaml \
    --trust_remote_code True

# MoE model quantization (Qwen3-30B-A3B W4A8)
msmodelslim quant \
    --model_path /path/to/Qwen3-30B-A3B \
    --save_path /path/to/output \
    --device npu \
    --model_type Qwen3-30B \
    --config_path /path/to/msmodelslim/lab_practice/qwen3_moe/qwen3-30b-w4a8-v1.yaml \
    --trust_remote_code True

# Multi-device distributed quantization
msmodelslim quant \
    --model_path /path/to/model \
    --save_path /path/to/output \
    --device npu:0,1,2,3 \
    --model_type Qwen2.5-72B-Instruct \
    --config_path /path/to/msmodelslim/lab_practice/qwen2.5/qwen2.5-72b-w8a8c8-v1.yaml \
    --trust_remote_code True
```

> **Note**: Find config files in `lab_practice/` directory of msmodelslim repository:
> - Structure: `lab_practice/<model_series>/<model>-<quant_type>-v1.yaml`
> - Example: `lab_practice/qwen2.5/qwen2.5-7b-w8a8-v1.yaml`

### Traditional Quantization (V0)

```bash
cd msmodelslim
python3 example/Qwen/quant_qwen.py \
    --model_path /path/to/Qwen2.5-7B-Instruct \
    --save_directory /path/to/output \
    --calib_file example/common/boolq.jsonl \
    --w_bit 8 --a_bit 8 \
    --device_type npu \
    --trust_remote_code True
```

---

## Installation

### Prerequisites

- **Python**: 3.8+ (3.9+ recommended for some environments)
- **CANN**: 8.2.RC1+ (8.3.RC1 or 8.5.0 recommended)
- **PyTorch Ascend**: Ascend Extension for PyTorch

### Install Steps

```bash
# 1. Clone repository
git clone https://gitcode.com/Ascend/msmodelslim.git
cd msmodelslim

# 2. Run installation script
bash install.sh

# 3. For Atlas 300I Duo (sparse quantization support)
cd ${PYTHON_SITE_PACKAGES}/msmodelslim/pytorch/weight_compression/compress_graph/
sudo bash build.sh ${CANN_INSTALL_PATH}/ascend-toolkit/latest
chmod -R 550 build
```

> **Note**: Do not run `msmodelslim` commands from within the source directory to avoid module path conflicts.

See [references/installation.md](references/installation.md) for detailed environment setup.

---

## Quantization Types

| Type | Weight | Activation | Description | Use Case |
|------|--------|------------|-------------|----------|
| **W8A8** | INT8 | INT8 | Standard 8-bit quantization | General use, balanced precision/performance |
| **W8A16** | INT8 | FP16 | Weight-only quantization | Higher precision needs (MindIE only) |
| **W4A8** | INT4 | INT8 | Low-bit weight quantization | Higher compression ratio |
| **W8A8C8** | INT8 | INT8 + KV Cache | With KV Cache quantization | Long sequence inference |
| **W8A8S** | INT8 Sparse | INT8 | Sparse quantization | Atlas 300I Duo optimization |
| **W16A16S** | FP16 Sparse | FP16 | Float sparse quantization | High compression needs |

### Quantization Type Selection

| Priority | Recommended Type |
|----------|-----------------|
| **Precision first** | W8A16 > W8A8 > W4A8 |
| **Memory first** | W4A8 > W8A8 > W8A16 |
| **Long sequence** | W8A8C8 (with KV Cache quant) |
| **Atlas 300I Duo** | W8A8S or W16A16S |

### BFLOAT16 Model Notes

For models with `torch_dtype=bfloat16` weights (e.g., Qwen3-30B-A3B):

If you encounter `AclNN_Parameter_Error(EZ1001): Tensor self not implemented for DT_BFLOAT16`, this is likely a **Docker image issue**, not a msmodelslim limitation.

**Quick Diagnosis**:
```bash
# Test if torch_npu works correctly
python3 -c "import torch; import torch_npu; a = torch.tensor(1).npu(); print('NPU OK')"
```

If this fails, your Docker image has compatibility issues. Try:
1. Use a different/updated Docker image
2. Reinstall torch_npu matching your CANN version
3. Ensure CANN 8.3.RC1+ for BF16 support

> **Container Setup**: See [ascend-docker](../ascend-docker/SKILL.md) for proper Docker container creation with NPU device mappings. Refer to [references/docker-setup.md](references/docker-setup.md) for msmodelslim-specific container configuration.

---

## Algorithm Selection

### Outlier Suppression Algorithms

| Algorithm | Description | When to Use |
|-----------|-------------|-------------|
| **SmoothQuant** | Co-scale activation and weight | Standard outlier suppression |
| **QuaRot** | Orthogonal rotation matrix | High precision requirements |
| **Iterative Smooth** | Iterative smoothing | Complex distributions |
| **Flex Smooth** | Grid search for optimal alpha/beta | Different architectures |
| **KV Smooth** | KV Cache smoothing | KV Cache quantization |

### Quantization Algorithms

| Algorithm | Description | When to Use |
|-----------|-------------|-------------|
| **AutoRound** | SignSGD optimization for rounding | 4-bit ultra-low quantization |
| **GPTQ** | Column-wise optimization | High precision weight quantization |
| **SSZ** | Iterative scale/offset search | Uneven weight distributions |
| **PDMIX** | Dynamic (prefill) + static (decode) | Large model inference |
| **FA3** | Per-head INT8 attention | Long sequence, MLA models |
| **MinMax** | Min-max range statistics | Basic quantization |
| **Histogram** | Histogram distribution analysis | Filter outliers |

### Quick Selection Guide

- **Beginners**: Use one-click quantization with `--config_path` pointing to `lab_practice/` config files
- **Precision priority**: QuaRot + AutoRound
- **Long sequence**: FA3 + KVCache Quant
- **Custom model**: See [references/model-integration.md](references/model-integration.md)

See [references/quantization-algorithms.md](references/quantization-algorithms.md) for algorithm details.

---

## Supported Models

### Large Language Models

| Model Series | One-Click | V0 Script | Notes |
|-------------|-----------|-----------|-------|
| **Qwen3** | ✓ | `example/Qwen/` | Qwen3-8B/14B/32B |
| **Qwen2.5** | ✓ | `example/Qwen/` | 7B/32B/72B/Coder |
| **Qwen2** | - | `example/Qwen/` | 7B/72B |
| **DeepSeek-V3** | ✓ | `example/DeepSeek/` | V3/V3.1/V3.2, R1 |
| **LLaMA** | - | `example/Llama/` | LLaMA2, LLaMA3.1 |
| **GLM** | - | `example/GLM/` | GLM-4, GLM-5 |
| **InternLM2** | - | `example/InternLM2/` | InternLM2-20B |
| **Kimi** | - | `example/Kimi/` | Kimi K2 |
| **HunYuan** | - | `example/HunYuan/` | HunYuan-A52B |

### MoE Models

| Model | One-Click | Notes |
|-------|-----------|-------|
| **Qwen3-MoE** | ✓ | Qwen3-30B-A3B, Qwen3-235B-A22B |
| **DeepSeek MoE** | ✓ | DeepSeek-V2, V3 series |

### Multimodal Models

| Type | Models | Example Script |
|------|--------|----------------|
| **Vision-Language** | Qwen-VL, Qwen2-VL, Qwen3-VL, InternVL2, LLaVA, GLM-4.1V | `example/multimodal_vlm/` |
| **Generation** | FLUX, SD3, HunyuanVideo, OpenSoraPlan, Wan2.1 | `example/multimodal_sd/` |

See [references/model-support.md](references/model-support.md) for complete support matrix.

---

## Custom Model Integration

### Quick Overview

1. **Create adapter file**: `msmodelslim/model/my_model/model_adapter.py`
2. **Define adapter class**: Inherit `TransformersModel` + interface classes
3. **Implement interfaces**: `handle_dataset`, `init_model`, `generate_model_visit`, etc.
4. **Register model**: Add to `config/config.ini`

### Example

```python
from msmodelslim.model.interface_hub import ModelSlimPipelineInterfaceV1
from msmodelslim.model.common.transformers import TransformersModel

class MyModelAdapter(TransformersModel, ModelSlimPipelineInterfaceV1):
    def handle_dataset(self, dataset, device):
        return self._get_tokenized_data(dataset, device)
    
    def init_model(self, device):
        return self._load_model(device)
    
    def generate_model_visit(self, model):
        from msmodelslim.model.common.layer_wise_forward import generated_decoder_layer_visit_func
        yield from generated_decoder_layer_visit_func(model)
    
    def generate_model_forward(self, model, inputs):
        from msmodelslim.model.common.layer_wise_forward import transformers_generated_forward_func
        yield from transformers_generated_forward_func(model, inputs)
```

See [references/model-integration.md](references/model-integration.md) and [scripts/model_adapter_template.py](scripts/model_adapter_template.py) for complete guide.

---

## Precision Auto-Tuning

### Sensitive Layer Analysis

```bash
# Analyze model sensitivity
msmodelslim analyze --model_path /path/to/model --model_type Qwen2.5-7B-Instruct
```

**Analysis Algorithms**:
- **std**: Standard deviation based (recommended for general use)
- **quantile**: Quantile/IQR based (for long-tail distributions)
- **kurtosis**: Kurtosis based (for extreme value detection)

### Auto-Tuning Strategy

**Standing High**: Binary search to minimize fallback layers while maintaining precision.

```bash
# Use auto-tuning config
msmodelslim quant \
    --model_path /path/to/model \
    --save_path /path/to/output \
    --model_type Qwen2.5-7B-Instruct \
    --config_path /path/to/auto_tuning_config.yaml
```

See [references/precision-tuning.md](references/precision-tuning.md) for tuning strategies.

---

## Deployment

### vLLM-Ascend

```bash
# Online service
vllm serve /path/to/quantized-model \
    --served-model-name "Qwen2.5-7B-w8a8" \
    --max-model-len 4096 \
    --quantization ascend

# Offline inference (Python)
from vllm import LLM, SamplingParams

llm = LLM(
    model="/path/to/quantized-model",
    max_model_len=4096,
    quantization="ascend"
)
outputs = llm.generate(["Hello"], SamplingParams(temperature=0.6))
```

### MindIE

```bash
# Deploy with MindIE
# See MindIE documentation for details
```

### Weight Conversion

```bash
# Convert to AutoAWQ/AutoGPTQ format
python3 example/common/ms_to_vllm.py --input /path/to/quantized --output /path/to/converted
```

See [references/deployment.md](references/deployment.md) for deployment details.

---

## Output Files

After quantization, the output directory contains:

```
output/
├── config.json                      # Original model config
├── generation_config.json           # Generation config
├── quant_model_description.json     # Quantization description
├── quant_model_weight_w8a8.safetensors  # Quantized weights
├── tokenizer_config.json            # Tokenizer config
├── tokenizer.json                   # Tokenizer vocabulary
└── vocab.json                       # Vocabulary (if applicable)
```

---

## Troubleshooting

### Common Issues

**Q: Out of memory during quantization?**
```bash
# Use layer-by-layer quantization (default in V1)
# Or use CPU quantization
msmodelslim quant --device cpu ...
```

**Q: Precision degradation after quantization?**
- Use higher precision type (W8A8 instead of W4A8)
- Check `lab_practice/` for best practice configs
- Enable outlier suppression algorithms
- See [references/precision-tuning.md](references/precision-tuning.md)

**Q: Model type not supported?**
- Check [references/model-support.md](references/model-support.md)
- Implement custom adapter: [references/model-integration.md](references/model-integration.md)

**Q: How to enable debug logging?**
```bash
export MSMODELSLIM_LOG_LEVEL=DEBUG
msmodelslim quant ...
```

---

## Scripts & Assets

### Scripts
- [scripts/check_env.sh](scripts/check_env.sh) - Environment check
- [scripts/quantize_model.sh](scripts/quantize_model.sh) - Quantization template
- [scripts/model_adapter_template.py](scripts/model_adapter_template.py) - Model adapter template

### Config Templates (assets/)
- [assets/quant_config_w8a8.yaml](assets/quant_config_w8a8.yaml) - W8A8 config
- [assets/quant_config_w4a8.yaml](assets/quant_config_w4a8.yaml) - W4A8 config
- [assets/quant_config_sparse.yaml](assets/quant_config_sparse.yaml) - Sparse quantization
- [assets/quant_config_pdmix.yaml](assets/quant_config_pdmix.yaml) - PDMIX config

---

## Official References

- **Documentation**: https://msmodelslim.readthedocs.io/zh-cn/latest/
- **GitCode Repository**: https://gitcode.com/Ascend/msmodelslim
- **vLLM-Ascend**: https://docs.vllm.ai/projects/ascend/en/latest/
- **Huawei Ascend**: https://www.hiascend.com/document

---

## Related Skills

- [atc-model-converter](../atc-model-converter/SKILL.md) - Model conversion for Ascend
- [npu-smi](../npu-smi/SKILL.md) - NPU device management
- [hccl-test](../hccl-test/SKILL.md) - HCCL performance testing
