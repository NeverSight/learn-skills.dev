---
name: vllm-deploy-docker
description: Deploy vLLM using Docker (pre-built images or build-from-source) with NVIDIA GPU support and run the OpenAI-compatible server.
---

# vLLM Docker Deployment

A Claude skill describing how to deploy vLLM with Docker using the official pre-built images or building the image from source supporting NVIDIA GPUs with CUDA. Instructions include NVIDIA CUDA support, example `docker run` and a minimal `docker-compose` snippet, recommended flags, and troubleshooting notes. For AMD, Intel, or other accelerators, please refer to the [vLLM documentation](https://docs.vllm.ai/) for alternative deployment methods.

## What this skill does

- Deploy vLLM with docker using pre-built images (recommended for most users) or build from source for custom configurations
- Provide example commands for running the OpenAI-compatible server with GPU access and mounted Hugging Face cache
- Point to build-from-source instructions when a custom image or optional dependencies are needed
- Explain common flags: `--ipc=host`, shared cache mounts, and `HF_TOKEN` handling

## Prerequisites

- Docker Engine installed (Docker 20.10+ recommended)
- NVIDIA GPU(s) with appropriate drivers and CUDA toolkit installed
- Optional: `curl` for API tests
- A Hugging Face token if pulling private models or to avoid rate-limits: `HF_TOKEN`

## Quickstart using Pre-built Image (recommended)

Run a vLLM OpenAI-compatible server with GPU access, mounting the HF cache and forwarding port 8000:

```bash
docker run --rm --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen2.5-1.5B-Instruct
```

- `--gpus all` exposes all GPUs to the container. Adjust if you need specific GPUs.
- `--ipc=host` or an appropriately large `--shm-size` is recommended so PyTorch and vLLM can share host shared memory.
- Mounting `~/.cache/huggingface` avoids re-downloading models inside the container.

> **Note:** vLLM and this skill recommend using the latest Docker image (`vllm/vllm-openai:latest`). For legacy version images, you may refer to the [Docker Hub image tags](https://hub.docker.com/r/vllm/vllm-openai/tags).

## Build Docker image from source

You can build and run vLLM from source by using the provided [docker/Dockerfile](https://github.com/vllm-project/vllm/blob/main/docker/Dockerfile). 
First, check the hardware of the host machine and ensure you have the necessary dependencies installed (e.g., NVIDIA drivers, CUDA toolkit, Docker with BuildKit support). For ARM64/aarch64 builds, refer to the "Building for ARM64/aarch64" section.

### Basic build command

```bash
DOCKER_BUILDKIT=1 docker build . \
  --target vllm-openai \
  --tag vllm/vllm-openai \
  --file docker/Dockerfile
```

The `--target vllm-openai` specifies that you are building the OpenAI-compatible server image. The `DOCKER_BUILDKIT=1` environment variable enables BuildKit, which provides better caching and faster builds.

### Build arguments and options

- **`--build-arg max_jobs=<N>`** — sets the number of parallel compilation jobs for building CUDA kernels. Useful for speeding up builds on multi-core systems.
- **`--build-arg nvcc_threads=<N>`** — controls CUDA compiler threads. Recommended to use a smaller value than `max_jobs` to avoid excessive memory usage.
- **`--build-arg torch_cuda_arch_list=""`** — if set to empty string, vLLM will detect and build only for the current GPU's compute capability. By default, vLLM builds for all GPU types for wider distribution.

### Using precompiled wheels to speed up builds

If you have not changed any C++ or CUDA kernel code, you can use precompiled wheels to significantly reduce Docker build time:

- **Enable precompiled wheels:** Add `--build-arg VLLM_USE_PRECOMPILED="1"` to your build command.
- **How it works:** By default, vLLM automatically finds the correct precompiled wheels from the [Nightly Builds](https://docs.vllm.ai/en/latest/contributing/ci/nightly_builds/) by using the merge-base commit with the upstream `main` branch.
- **Specify a commit:** To use wheels from a specific commit, add `--build-arg VLLM_PRECOMPILED_WHEEL_COMMIT=<commit_hash>`.

**Example with precompiled wheels and options for fast compilation:**
```bash
DOCKER_BUILDKIT=1 docker build . \
  --target vllm-openai \
  --tag vllm/vllm-openai \
  --file docker/Dockerfile \
  --build-arg max_jobs=8 \
  --build-arg nvcc_threads=2 \
  --build-arg VLLM_USE_PRECOMPILED="1"
```

### Building with optional dependencies (optional)

vLLM does not include optional dependencies (e.g., audio processing) in the pre-built image to avoid licensing issues. If you need optional dependencies, create a custom Dockerfile that extends the base image:

**Example: adding audio optional dependencies**
```dockerfile
# NOTE: MAKE SURE the version of vLLM matches the base image!
FROM vllm/vllm-openai:0.11.0

# Install audio optional dependencies
RUN uv pip install --system vllm[audio]==0.11.0
```

**Example: using development version of transformers:**
```dockerfile
FROM vllm/vllm-openai:latest

# Install development version of Transformers from source
RUN uv pip install --system git+https://github.com/huggingface/transformers.git
```

Build this custom Dockerfile with:
```bash
docker build -t my-vllm-custom:latest -f Dockerfile .
```

Then use it like any other vLLM image:
```bash
docker run --rm --gpus all \
  -p 8000:8000 \
  --ipc=host \
  my-vllm-custom:latest \
  --model Qwen/Qwen2.5-1.5B-Instruct
```

### Building for ARM64/aarch64

A Docker container can be built for ARM64 systems (e.g., NVIDIA Grace-Hopper and Grace-Blackwell). Use the flag `--platform "linux/arm64"`:

```bash
DOCKER_BUILDKIT=1 docker build . \
  --target vllm-openai \
  --tag vllm/vllm-openai \
  --file docker/Dockerfile \
  --platform "linux/arm64"
```

**Note:** Multiple modules must be compiled, so this process can take longer. Use build arguments like `--build-arg max_jobs=8 --build-arg nvcc_threads=2` to speed up the process (ensure `max_jobs` is substantially larger than `nvcc_threads`). Monitor memory usage, as parallel jobs can require significant RAM.

**For cross-compilation** (building ARM64 on an x86_64 host), register QEMU user-static handlers first:
```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

Then use the `--platform "linux/arm64"` flag in your build command.

### Running your custom-built image

After building, run your image just like the pre-built image:

```bash
docker run --rm --runtime nvidia --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 8000:8000 \
  --ipc=host \
  vllm/vllm-openai \
  --model Qwen/Qwen2.5-1.5B-Instruct
```

Replace `vllm/vllm-openai` with the tag you specified during the build (e.g., `my-vllm-custom:latest`).
> **Note:** `--runtime nvidia` is deprecated for most environments. Prefer `--gpus ...` with NVIDIA Container Toolkit. Use `--runtime nvidia` only for legacy Docker configurations.

## Common server flags

- `--model <MODEL_ID>` — model to load (HF ID or local path)
- `--port <PORT>` — server port (default 8000 for OpenAI-compatible server)
- `--log-level` — adjust verbosity
- You may pass additional `engine_args` after the image tag; see vLLM docs for tuning options.

## Testing the API

After the container starts, make a quick test request against the OpenAI-compatible endpoint:

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen2.5-1.5B-Instruct","messages":[{"role":"user","content":"Who are you?"}],"max_tokens":128}'
```

## Security and operational notes

- Keep `HF_TOKEN` secret; prefer passing it via environment variables or a secret manager.
- For production, run behind a reverse proxy (Nginx) with TLS and authentication.
- Mount only necessary host paths into the container.

## Troubleshooting

- Container can't access GPUs: ensure `nvidia-container-toolkit` is installed and restart Docker.
- Model download failures: check `HF_TOKEN` and network; mount cache directory to persist downloads.
- Memory / OOM errors: try a smaller model or add more GPU memory; check `--shm-size`.
- If the container fails with NCCL library path issues (rare): set `VLLM_NCCL_SO_PATH` per upstream guidance.
- Permission issues of current user with Docker: ensure your user is in the `docker` group or suggest user to add current user to `docker` group manually following:
```bash
# 1. Create docker group if it doesn't exist (may already exist on some systems)
sudo groupadd docker

# 2. Add current user to the docker group (replace $USER with your username if needed)
sudo usermod -aG docker $USER

# 3. Apply the new group membership (you may need to log out and log back in for this to take effect)
newgrp docker

# 4. Verify that the user is in the docker group (output should include docker)
groups $USER
```
- Docker pull failed due to a network timeout connecting to Docker Hub: check the network connection and try again. If the issue persists, suggest and show the user how to use a mirror for Docker Hub.
- Error during downloading models from Hugging Face: check if the `HF_TOKEN` is passed to the container and is valid. Check if `HTTP_PROXY` and `HTTPS_PROXY` are passed to the container if the host is behind a proxy. Also, verify that the model ID is correct and that the model is public or accessible with the provided token.

## References

- vLLM repository (docker/Dockerfile): https://github.com/vllm-project/vllm/tree/main/docker
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
- Up-to-date deployment instructions and troubleshooting: https://docs.vllm.ai/en/latest/deployment/docker/