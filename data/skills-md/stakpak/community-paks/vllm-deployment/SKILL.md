---
name: vllm-deployment
description: |
  Deploy vLLM for high-performance LLM inference. Covers Docker CPU/GPU deployments and cloud VM provisioning with OpenAI-compatible API endpoints.
license: MIT
tags:
  - vllm
  - llm
  - inference
  - gpu
  - ai
  - machine-learning
  - docker
  - openai-api
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.3"
---

# vLLM Model Serving and Inference

## Quick Start

### Docker (CPU)

```bash
docker run --rm -p 8000:8000 \
  --shm-size=4g \
  --cap-add SYS_NICE \
  --security-opt seccomp=unconfined \
  -e VLLM_CPU_KVCACHE_SPACE=4 \
  <vllm-cpu-image> \
  --model <model-name> \
  --dtype float32
# Access: http://localhost:8000
```

### Docker (GPU)

```bash
docker run --rm -p 8000:8000 \
  --gpus all \
  --shm-size=4g \
  <vllm-gpu-image> \
  --model <model-name>
# Access: http://localhost:8000
```

## Docker Deployment

### 1. Assess Hardware Requirements

| Hardware | Minimum RAM | Recommended |
|----------|-------------|-------------|
| CPU | 2x model size | 4x model size |
| GPU | Model size + 2GB | Model size + 4GB VRAM |

- Check model documentation for specific requirements
- Consider quantized variants to reduce memory footprint
- Allocate 50-100GB storage for model downloads

### 2. Pull the Container Image

```bash
# CPU image (check vLLM docs for latest tag)
docker pull <vllm-cpu-image>

# GPU image (check vLLM docs for latest tag)
docker pull <vllm-gpu-image>
```

**Notes:**
- Use CPU-specific images for CPU inference
- Use CUDA-enabled images matching your GPU architecture
- Verify CPU instruction set compatibility (AVX512, AVX2)

### 3. Configure and Run

**CPU Deployment:**

```bash
docker run --rm \
  --shm-size=4g \
  --cap-add SYS_NICE \
  --security-opt seccomp=unconfined \
  -p 8000:8000 \
  -e VLLM_CPU_KVCACHE_SPACE=4 \
  -e VLLM_CPU_OMP_THREADS_BIND=0-7 \
  <vllm-cpu-image> \
  --model <model-name> \
  --dtype float32 \
  --max-model-len 2048
```

**GPU Deployment:**

```bash
docker run --rm \
  --gpus all \
  --shm-size=4g \
  -p 8000:8000 \
  <vllm-gpu-image> \
  --model <model-name> \
  --dtype auto \
  --max-model-len 4096
```

### 4. Verify Deployment

```bash
# Check health
curl http://localhost:8000/health

# List models
curl http://localhost:8000/v1/models

# Test inference
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "<model-name>", "prompt": "Hello", "max_tokens": 10}'
```

### 5. Update

```bash
docker pull <vllm-image>
docker stop <container-id>
# Re-run with same parameters
```

## Cloud VM Deployment

### 1. Provision Infrastructure

```bash
# Create security group with rules:
# - TCP 22 (SSH)
# - TCP 8000 (API)

# Launch instance with:
# - Sufficient RAM/VRAM for model
# - Docker pre-installed (or install manually)
# - 50-100GB root volume
# - Public IP for external access
```

### 2. Connect and Deploy

```bash
ssh -i <key-file> <user>@<instance-ip>

# Install Docker if not present
# Pull and run vLLM container (see Docker Deployment section)
```

### 3. Verify External Access

```bash
# From local machine
curl http://<instance-ip>:8000/health
curl http://<instance-ip>:8000/v1/models
```

### 4. Cleanup

```bash
# Stop container
docker stop <container-id>

# Terminate instance to stop costs
# Delete associated resources (volumes, security groups) if temporary
```

## Configuration Reference

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `VLLM_CPU_KVCACHE_SPACE` | KV cache size in GB (CPU) | `4` |
| `VLLM_CPU_OMP_THREADS_BIND` | CPU core binding (CPU) | `0-7` |
| `CUDA_VISIBLE_DEVICES` | GPU device selection | `0,1` |
| `HF_TOKEN` | HuggingFace authentication | `hf_xxx` |

### Docker Flags

| Flag | Purpose |
|------|---------|
| `--shm-size=4g` | Shared memory for IPC |
| `--cap-add SYS_NICE` | NUMA optimization (CPU) |
| `--security-opt seccomp=unconfined` | Memory policy syscalls (CPU) |
| `--gpus all` | GPU access |
| `-p 8000:8000` | Port mapping |

### vLLM Arguments

| Argument | Purpose | Example |
|----------|---------|---------|
| `--model` | Model name/path | `<model-name>` |
| `--dtype` | Data type | `float32`, `auto`, `bfloat16` |
| `--max-model-len` | Max context length | `2048` |
| `--tensor-parallel-size` | Multi-GPU parallelism | `2` |

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/v1/models` | GET | List available models |
| `/v1/completions` | POST | Text completion |
| `/v1/chat/completions` | POST | Chat completion |
| `/metrics` | GET | Prometheus metrics |

## Production Checklist

- [ ] Verify model fits in available memory
- [ ] Configure appropriate data type for hardware
- [ ] Set up firewall/security group rules
- [ ] Test API endpoints before production use
- [ ] Configure monitoring (Prometheus metrics)
- [ ] Set up health check alerts
- [ ] Document model and configuration used
- [ ] Plan for model updates and rollbacks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container exits immediately | Increase RAM or use smaller model |
| Slow inference (CPU) | Verify OMP thread binding configuration |
| Connection refused externally | Check firewall/security group rules |
| Model download fails | Set HF_TOKEN for gated models |
| Out of memory during inference | Reduce max_model_len or batch size |
| Port already in use | Change host port mapping |
| Warmup takes too long | Normal for large models (1-5 min) |

## References

- [vLLM Documentation](https://docs.vllm.ai/)
- [vLLM CPU Installation](https://docs.vllm.ai/en/stable/getting_started/installation/cpu/)
- [vLLM GPU Installation](https://docs.vllm.ai/en/stable/getting_started/installation/gpu/)
- [vLLM Supported Models](https://docs.vllm.ai/en/stable/models/supported_models.html)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [HuggingFace Model Hub](https://huggingface.co/models)
