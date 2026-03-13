---
name: vllm-deploy-simple
description: Quick install and deploy vLLM, start serving with a simple LLM, and test OpenAI API.
---

# vLLM Simple Deployment

A simple skill to quickly install vLLM, start a server, and validate the OpenAI-compatible API.

## What this skill does

This skill provides a streamlined workflow to:
- Detect hardware backend (NVIDIA CUDA, AMD ROCm, Google TPU, or CPU)
- Install vLLM with appropriate backend support
- Start the vLLM server with configurable model and port
- Test the OpenAI-compatible API endpoint
- Validate the deployment is working correctly
- Support virtual environment isolation

## Prerequisites

- Python 3.10+
- GPU (NVIDIA CUDA, AMD ROCm) (recommended) or TPU or CPU
- pip or uv package manager
- curl (for API testing)
- Virtual environment (optional but recommended)

## Usage

### Create a venv

If user did not specify the venv path or asked to deploy in the current environment, create a venv using uv with python 3.12 in the current folder. If uv not found, make a folder in this path and use python to create a virtual environment.

### Run the complete workflow (suggested)

If user did not specify the venv path, model, or port, use default options:

```bash
# Default deployment options (--venv "." --model "Qwen/Qwen2.5-1.5B-Instruct" --port 8000 --gpu_memory_utilization 0.8)
scripts/quickstart.sh
```

Or with custom options:

```bash
# Use custom virtual environment
scripts/quickstart.sh --venv /path/to/venv

# Use custom model and port
scripts/quickstart.sh --model "Qwen/Qwen2.5-1.5B-Instruct" --port 8000

# Use custom GPU memory utilization
scripts/quickstart.sh --gpu_memory_utilization 0.6

# Combine all options
scripts/quickstart.sh --venv /path/to/venv --model "Qwen/Qwen2.5-1.5B-Instruct" --port 8000 --gpu_memory_utilization 0.8
```

This will:
1. Activate the virtual environment (if specified)
2. Detect hardware backend (CUDA/ROCm/TPU/CPU)
3. Install vLLM with appropriate backend support
4. Start the vLLM server in the background
5. Wait for the server to be ready
6. Test the API with a sample request
7. Display the server status

### Run individual commands (for step-by-step usage or troubleshooting)

**Install vLLM:**
```bash
scripts/quickstart.sh install
# Or with virtual environment
scripts/quickstart.sh install --venv /path/to/venv
```

**Start the server:**
```bash
scripts/quickstart.sh start
# Or with custom options
scripts/quickstart.sh start --venv /path/to/venv --model "Qwen/Qwen2.5-1.5B-Instruct" --port 8000 --gpu_memory_utilization 0.8
```

**Test the API:**
```bash
scripts/quickstart.sh test
# Or with custom port
scripts/quickstart.sh test --port 8000
```

**Stop the server:**
```bash
scripts/quickstart.sh stop
# Or with virtual environment
scripts/quickstart.sh stop --venv /path/to/venv
```

**Check server status:**
```bash
scripts/quickstart.sh status
```

**Restart the server:**
```bash
scripts/quickstart.sh restart
# Or with custom options
scripts/quickstart.sh restart --venv /path/to/venv --port 8000 --gpu_memory_utilization 0.8
```

## Configuration

The script supports the following command-line options:

```bash
scripts/quickstart.sh [command] [OPTIONS]

Commands:
  install  - Install vLLM and dependencies
  start    - Start the vLLM server
  stop     - Stop the vLLM server
  test     - Test the OpenAI-compatible API
  status   - Show server status
  restart  - Restart the server
  all      - Run complete workflow (default)

Options:
  --model MODEL                 Model to use (default: Qwen/Qwen2.5-1.5B-Instruct)
  --port PORT                   Port to run server on (default: 8000)
  --venv VENV_PATH              Virtual environment path (default: .)
  --gpu_memory_utilization VRAM GPU memory utilization (default: 0.8)
```

### Hardware Backend Detection

The script automatically detects your hardware and installs the appropriate vLLM version:

- **NVIDIA CUDA**: Detected via `nvidia-smi` command
- **AMD ROCm**: Detected via `/dev/kfd` and `/dev/dri` devices
- **Google TPU**: Detected via `TPU_NAME` environment variable or `gcloud` command
- **CPU**: Fallback if no GPU/TPU detected

For Google TPU, the script installs `vllm-tpu` instead of the standard `vllm` package.

## API Testing

The test script sends a simple chat completion request:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-1.5B-Instruct",
    "messages": [{"role": "user", "content": "Say hello!"}],
    "max_tokens": 50
  }'
```

## Troubleshooting

**Virtual environment not found:**
- Ensure the path provided with `--venv` exists and is a valid virtual environment
- Check that the activation script exists (`bin/activate` on Linux/macOS or `Scripts/activate` on Windows)
- Check and install uv, and create a new virtual environment with uv: `uv venv /path/to/venv` (suggested); or with pip: `python3 -m venv /path/to/venv` 

**Server won't start:**
- Check if the port is already in use: `lsof -i :8000`
- Verify GPU availability: `nvidia-smi` (for NVIDIA) or `rocm-smi` (for AMD)
- Check vLLM installation: `python -c "import vllm; print(vllm.__version__)"`
- Review server logs at `$VENV_PATH/tmp/vllm-server.log`

**API returns errors:**
- Wait a few seconds for the model to load
- Check server logs: `cat $VENV_PATH/tmp/vllm-server.log`
- Verify the server is running: `scripts/quickstart.sh status`

**Out of memory:**
- Use a smaller model (e.g., Qwen2.5-0.5B-Instruct)
- Reduce `--gpu-memory-utilization` parameter
- Close other GPU-intensive applications

**Wrong backend detected:**
- For NVIDIA: Ensure `nvidia-smi` is in your PATH
- For AMD: Check that ROCm drivers are properly installed
- For TPU: Set `TPU_NAME` environment variable or install `gcloud`

## Notes

- The server runs in the background and logs to `$VENV_PATH/tmp/vllm-server.log`
- The PID is stored in `$VENV_PATH/tmp/vllm-server.pid` for easy management
- First run will download the model (~3GB for Qwen2.5-1.5B-Instruct)
- Subsequent runs will use the cached model
- The script automatically detects and uses `uv` if available, otherwise falls back to `pip`
- Virtual environment support allows isolation from system Python packages
- Arguments can be specified in any order (e.g., `scripts/quickstart.sh --port 8080 start --venv /path/to/venv`)
