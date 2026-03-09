---
name: vllm-ascend
description: vLLM Ascend plugin for LLM inference serving on Huawei Ascend NPU. Use for offline batch inference, API server deployment, quantization inference (with msmodelslim quantized models), tensor/pipeline parallelism for distributed serving, and OpenAI-compatible API endpoints. Supports Qwen, DeepSeek, GLM, LLaMA models with Ascend-optimized kernels.
keywords:
    - vllm
    - vllm-ascend
    - inference
    - llm serving
    - 推理服务
    - 大模型部署
    - tensor parallelism
    - 张量并行
    - distributed inference
    - 分布式推理
    - ascend npu
    - quantization
    - 量化推理
    - openai api
    - deployment
    - api服务
---

# vLLM-Ascend - LLM Inference Serving

vLLM-Ascend is a plugin for vLLM that enables efficient LLM inference on Huawei Ascend AI processors. It provides Ascend-optimized kernels, quantization support, and distributed inference capabilities.

---

## Quick Start

### Offline Batch Inference

```python
import os

# Required for vLLM-Ascend: set multiprocessing method before importing vLLM
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

from vllm import LLM, SamplingParams

# Load model with Ascend NPU (device auto-detected when vllm-ascend is installed)
llm = LLM(
    model="Qwen/Qwen2.5-7B-Instruct",
    max_model_len=4096
)

# Prepare prompts and sampling params
prompts = [
    "Hello, how are you?",
    "Explain quantum computing in simple terms.",
]
sampling_params = SamplingParams(temperature=0.7, top_p=0.9, max_tokens=512)

# Generate outputs
outputs = llm.generate(prompts, sampling_params)

# Print results
for output in outputs:
    print(f"Prompt: {output.prompt}")
    print(f"Output: {output.outputs[0].text}\n")
```

### OpenAI-Compatible API Server

```bash
# Start the API server
vllm serve Qwen/Qwen2.5-7B-Instruct \
    --max-model-len 4096 \
    --max-num-seqs 256 \
    --served-model-name "qwen2.5-7b"

# Or using Python
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --max-model-len 4096
```

### API Client Example

```python
import requests

# Completions API
response = requests.post(
    "http://localhost:8000/v1/completions",
    json={
        "model": "qwen2.5-7b",
        "prompt": "Once upon a time",
        "max_tokens": 100,
        "temperature": 0.7
    }
)
print(response.json())

# Chat Completions API
response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "qwen2.5-7b",
        "messages": [
            {"role": "user", "content": "Hello!"}
        ],
        "max_tokens": 100
    }
)
print(response.json())
```

---

## Installation

### Prerequisites

- **CANN**: 8.0.RC1 or higher
- **Python**: 3.9 or higher
- **PyTorch Ascend**: Compatible with your CANN version

### Method 1: Docker (Recommended)

```bash
# Pull pre-built image
docker pull ascendai/vllm-ascend:latest

# Run with NPU access
docker run -it --rm \
    --device /dev/davinci0 \
    --device /dev/davinci_manager \
    --device /dev/devmm_svm \
    --device /dev/hisi_hdc \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
    -v /usr/local/Ascend/add-ons:/usr/local/Ascend/add-ons \
    -e ASCEND_RT_VISIBLE_DEVICES=0 \
    ascendai/vllm-ascend:latest
```

### Method 2: pip Installation

```bash
# Install vLLM with Ascend plugin
pip install vllm-ascend

# Or install from source
git clone https://github.com/vllm-project/vllm-ascend.git
cd vllm-ascend
pip install -e .
```

### Verify Installation

```bash
# Check vLLM Ascend installation
python -c "import vllm_ascend; print(vllm_ascend.__version__)"

# Check NPU availability
python -c "import torch; import torch_npu; print(torch_npu.npu.device_count())"
```

---

## Deployment

### Server Mode

```bash
# Basic server deployment
vllm serve <model_path> \
    \
    --served-model-name <name> \
    --host 0.0.0.0 \
    --port 8000

# Production deployment with optimizations
vllm serve /path/to/model \
    \
    --served-model-name "qwen2.5-72b" \
    --max-model-len 8192 \
    --max-num-seqs 256 \
    --tensor-parallel-size 4 \
    --gpu-memory-utilization 0.9 \
    --dtype bfloat16 \
    --api-key <your-api-key>
```

### Python API

```python
import os

# Required: Set spawn method before importing vLLM
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

from vllm import LLM, SamplingParams

# Single NPU
llm = LLM(
    model="Qwen/Qwen2.5-7B-Instruct",
    max_model_len=4096,
    dtype="bfloat16"
)

# Distributed inference (multi-NPU)
llm = LLM(
    model="Qwen/Qwen2.5-72B-Instruct",
    tensor_parallel_size=4,
    max_model_len=8192
)

# Generate
params = SamplingParams(temperature=0.7, max_tokens=512)
outputs = llm.generate(["Hello world"], params)
```

### LLM Engine (Advanced)

```python
from vllm import LLMEngine, EngineArgs, SamplingParams

engine_args = EngineArgs(
    model="Qwen/Qwen2.5-7B-Instruct",
    max_model_len=4096
)
engine = LLMEngine.from_engine_args(engine_args)

# Add requests and step through generation
request_id = "req-001"
prompt = "Hello, world!"
params = SamplingParams(max_tokens=50)
engine.add_request(request_id, prompt, params)

while engine.has_unfinished_requests():
    outputs = engine.step()
    for output in outputs:
        if output.finished:
            print(f"{output.request_id}: {output.outputs[0].text}")
```

---

## Quantization

vLLM-Ascend supports models quantized with msModelSlim. For quantization details, see [msmodelslim](../msmodelslim/SKILL.md).

### Using Quantized Models

```bash
# W8A8 quantized model
vllm serve /path/to/quantized-model-w8a8 \
    \
    --quantization ascend \
    --max-model-len 4096

# W4A8 quantized model
vllm serve /path/to/quantized-model-w4a8 \
    \
    --quantization ascend \
    --max-model-len 4096
```

### Python API with Quantization

```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="/path/to/quantized-model",
    quantization="ascend",
    max_model_len=4096
)

params = SamplingParams(temperature=0.7, max_tokens=512)
outputs = llm.generate(["Hello"], params)
```

---

## Distributed Inference

### Tensor Parallelism

Distributes model layers across multiple NPUs for large models.

```bash
# 4-way tensor parallelism
vllm serve Qwen/Qwen2.5-72B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 8192
```

```python
import os
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"

from vllm import LLM

llm = LLM(
    model="Qwen/Qwen2.5-72B-Instruct",
    tensor_parallel_size=4,
    max_model_len=8192
)
```

### Pipeline Parallelism

```python
from vllm import LLM

llm = LLM(
    model="DeepSeek-V3",
    pipeline_parallel_size=2,
    tensor_parallel_size=4
)
```

### Multi-Node Deployment

```bash
# Node 0 (Rank 0)
vllm serve <model> \
    \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --distributed-init-method "tcp://192.168.1.10:29500" \
    --distributed-rank 0

# Node 1 (Rank 1)
vllm serve <model> \
    \
    --tensor-parallel-size 8 \
    --pipeline-parallel-size 2 \
    --distributed-init-method "tcp://192.168.1.10:29500" \
    --distributed-rank 1
```

---

## Performance Optimization

### Key Parameters

| Parameter | Default | Description | Tuning Advice |
|-----------|---------|-------------|---------------|
| `--max-model-len` | Model max | Maximum sequence length | Reduce if OOM |
| `--max-num-seqs` | 256 | Max concurrent sequences | Increase for throughput |
| `--gpu-memory-utilization` | 0.9 | GPU memory fraction | Lower if OOM during warmup |
| `--dtype` | auto | Data type | bfloat16 for speed, float16 for compatibility |
| `--tensor-parallel-size` | 1 | Tensor parallelism degree | Use for large models |
| `--pipeline-parallel-size` | 1 | Pipeline parallelism degree | Use for very large models |

### Example Configurations

```bash
# Small model (7B), single NPU
vllm serve <model> --max-model-len 4096 --max-num-seqs 256

# Medium model (32B), single NPU
vllm serve <model> --max-model-len 8192 --max-num-seqs 128

# Large model (72B), multi-NPU
vllm serve <model> --tensor-parallel-size 4 --max-model-len 8192

# Maximum throughput
vllm serve <model> --max-num-seqs 512 --gpu-memory-utilization 0.95
```

---

## Troubleshooting

### Common Issues

**Q: AclNN_Parameter_Error or dtype errors?**
```bash
# Check CANN version compatibility
npu-smi info
# Ensure CANN >= 8.0.RC1

# Try different dtype
vllm serve <model> --dtype float16
```

**Q: Out of Memory (OOM)?**
```bash
# Reduce max model length
vllm serve <model> --max-model-len 2048

# Lower memory utilization
vllm serve <model> --gpu-memory-utilization 0.8

# Reduce concurrent sequences
vllm serve <model> --max-num-seqs 128
```

**Q: Model loading fails?**
```bash
# Check model path
ls /path/to/model

# Verify tokenizer
python -c "from transformers import AutoTokenizer; tok = AutoTokenizer.from_pretrained('/path/to/model'); print('OK')"

# Use trust_remote_code for custom models
vllm serve <model> --trust-remote-code
```

**Q: Slow inference?**
```bash
# Enable bfloat16 for faster compute
vllm serve <model> --dtype bfloat16

# Adjust block size
vllm serve <model> --block-size 256

# Enable prefix caching
vllm serve <model> --enable-prefix-caching
```

**Q: API server connection refused?**
```bash
# Check server is running
curl http://localhost:8000/health

# Verify port is not in use
lsof -i :8000

# Use explicit host/port
vllm serve <model> --host 0.0.0.0 --port 8000
```

### Environment Variables

```bash
# Required: Set multiprocessing method for vLLM-Ascend
export VLLM_WORKER_MULTIPROC_METHOD=spawn

# Set Ascend device IDs
export ASCEND_RT_VISIBLE_DEVICES=0,1,2,3

# Debug logging
export VLLM_LOGGING_LEVEL=DEBUG

# Disable lazy initialization (for debugging)
export VLLM_ASCEND_LAZY_INIT=0
```

---

## Scripts

- `scripts/benchmark_throughput.py` - Throughput benchmark
- `scripts/benchmark_latency.py` - Latency benchmark
- `scripts/start_server.sh` - Server startup template

---

## References

- [references/deployment.md](references/deployment.md) - Deployment patterns and best practices
- [references/supported-models.md](references/supported-models.md) - Complete model support matrix
- [references/api-reference.md](references/api-reference.md) - API endpoint documentation

---

## Related Skills

- [msmodelslim](../msmodelslim/SKILL.md) - Model quantization for vLLM-Ascend
- [ascend-docker](../ascend-docker/SKILL.md) - Docker container setup for Ascend
- [npu-smi](../npu-smi/SKILL.md) - NPU device management
- [hccl-test](../hccl-test/SKILL.md) - HCCL performance testing for multi-NPU

---

## Official References

- **vLLM-Ascend Documentation**: https://docs.vllm.ai/projects/ascend/en/latest/
- **vLLM Documentation**: https://docs.vllm.ai/
- **Huawei Ascend**: https://www.hiascend.com/document
- **GitHub Repository**: https://github.com/vllm-project/vllm-ascend
