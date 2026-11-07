---
name: mac-code-local-ai-agent
description: Run a free 35B AI coding agent on Apple Silicon Macs using local LLMs via llama.cpp or MLX with web search, shell, and file tools.
triggers:
  - "set up mac code local AI agent"
  - "run Claude Code alternative on Mac for free"
  - "local LLM agent on Apple Silicon"
  - "35B model on 16GB Mac"
  - "llama.cpp agent with tools on Mac"
  - "MLX local coding agent"
  - "out of RAM model inference Mac"
  - "mac-code setup and usage"
---

# mac-code — Free Local AI Agent on Apple Silicon

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Run a 35B reasoning model locally on your Mac for $0/month. mac-code is a CLI AI coding agent (Claude Code alternative) that routes tasks — web search, shell commands, file edits, chat — through a local LLM. Supports llama.cpp (30 tok/s) and MLX (64K context, persistent KV cache) backends on Apple Silicon.

---

## What It Does

- **LLM-as-router**: The model classifies every prompt as `search`, `shell`, or `chat` and routes accordingly
- **35B MoE at 30 tok/s** via llama.cpp + IQ2_M quantization (fits in 16 GB RAM)
- **35B full Q4 on 16 GB** via custom MoE Expert Sniper (1.54 tok/s, only 1.42 GB RAM used)
- **9B at 64K context** via quantized KV cache (`q4_0` keys/values)
- **MLX backend** adds persistent KV cache save/load, context compression, R2 sync
- **Tools**: DuckDuckGo search, shell execution, file read/write

---

## Installation

### Prerequisites

```bash
brew install llama.cpp
pip3 install rich ddgs huggingface-hub mlx-lm --break-system-packages
```

### Clone the repo

```bash
git clone https://github.com/walter-grace/mac-code
cd mac-code
```

### Download models

**35B MoE — fast daily driver (10.6 GB, fits in 16 GB RAM):**

```bash
mkdir -p ~/models
python3 -c "
from huggingface_hub import hf_hub_download
hf_hub_download(
    'unsloth/Qwen3.5-35B-A3B-GGUF',
    'Qwen3.5-35B-A3B-UD-IQ2_M.gguf',
    local_dir='$HOME/models/'
)
"
```

**9B — 64K context, long documents (5.3 GB):**

```bash
python3 -c "
from huggingface_hub import hf_hub_download
hf_hub_download(
    'unsloth/Qwen3.5-9B-GGUF',
    'Qwen3.5-9B-Q4_K_M.gguf',
    local_dir='$HOME/models/'
)
"
```

---

## Starting the Backend

### Option A: llama.cpp + 35B MoE (recommended, 30 tok/s)

```bash
llama-server \
    --model ~/models/Qwen3.5-35B-A3B-UD-IQ2_M.gguf \
    --port 8000 --host 127.0.0.1 \
    --flash-attn on --ctx-size 12288 \
    --cache-type-k q4_0 --cache-type-v q4_0 \
    --n-gpu-layers 99 --reasoning off -np 1 -t 4
```

### Option B: llama.cpp + 9B (64K context)

```bash
llama-server \
    --model ~/models/Qwen3.5-9B-Q4_K_M.gguf \
    --port 8000 --host 127.0.0.1 \
    --flash-attn on --ctx-size 65536 \
    --cache-type-k q4_0 --cache-type-v q4_0 \
    --n-gpu-layers 99 --reasoning off -t 4
```

### Option C: MLX backend (persistent context, 9B)

```bash
# Starts server on port 8000, downloads model on first run
python3 mlx/mlx_engine.py
```

### Start the agent (all options)

```bash
python3 agent.py
```

---

## Agent CLI Commands

Inside the agent REPL, type `/` for all commands:

| Command | Action |
|---|---|
| `/agent` | Agent mode with tools (default) |
| `/raw` | Direct streaming, no tools |
| `/model 9b` | Switch to 9B model (64K context) |
| `/model 35b` | Switch to 35B MoE |
| `/search <query>` | Quick DuckDuckGo search |
| `/bench` | Run speed benchmark |
| `/stats` | Session statistics |
| `/cost` | Show cost savings vs cloud |
| `/good` / `/bad` | Grade the last response |
| `/improve` | View response grading stats |
| `/clear` | Reset conversation |
| `/quit` | Exit |

### Example prompts

```
> find all Python files modified in the last 7 days
→ routes to "shell", generates: find . -name "*.py" -mtime -7

> who won the NBA finals
→ routes to "search", queries DuckDuckGo, summarizes

> explain how attention works
→ routes to "chat", streams directly
```

---

## MLX Backend — Persistent KV Cache API

The MLX engine exposes a REST API on `localhost:8000`.

### Save context after processing a large codebase

```bash
curl -X POST localhost:8000/v1/context/save \
    -H "Content-Type: application/json" \
    -d '{"name": "my-project", "prompt": "$(cat README.md)"}'
```

### Load saved context instantly (0.0003s)

```bash
curl -X POST localhost:8000/v1/context/load \
    -H "Content-Type: application/json" \
    -d '{"name": "my-project"}'
```

### Download context from Cloudflare R2 (cross-Mac sync)

```bash
# Requires R2 credentials in environment
export R2_ACCOUNT_ID=your_account_id
export R2_ACCESS_KEY_ID=your_key_id
export R2_SECRET_ACCESS_KEY=your_secret
export R2_BUCKET=your_bucket_name

curl -X POST localhost:8000/v1/context/download \
    -H "Content-Type: application/json" \
    -d '{"name": "my-project"}'
```

### Standard OpenAI-compatible chat

```python
import requests

response = requests.post("http://localhost:8000/v1/chat/completions", json={
    "model": "local",
    "messages": [{"role": "user", "content": "Write a Python quicksort"}],
    "stream": False
})
print(response.json()["choices"][0]["message"]["content"])
```

### Streaming chat

```python
import requests, json

with requests.post("http://localhost:8000/v1/chat/completions", json={
    "model": "local",
    "messages": [{"role": "user", "content": "Explain transformers"}],
    "stream": True
}, stream=True) as r:
    for line in r.iter_lines():
        if line.startswith(b"data: "):
            chunk = json.loads(line[6:])
            delta = chunk["choices"][0]["delta"].get("content", "")
            print(delta, end="", flush=True)
```

---

## KV Cache Compression (MLX)

Compress context 4x with 99.3% similarity:

```python
from mlx.turboquant import compress_kv_cache
from mlx.kv_cache import save_kv_cache, load_kv_cache

# After building a KV cache from a long document
compressed = compress_kv_cache(kv_cache, bits=4)  # 26.6 MB → 6.7 MB
save_kv_cache(compressed, "my-project-compressed")

# Load later
kv = load_kv_cache("my-project-compressed")
```

---

## Flash Streaming — Out-of-Core Inference

For models larger than your RAM (research mode):

```bash
cd research/flash-streaming

# Run 35B MoE Expert Sniper (22 GB model, 1.42 GB RAM)
python3 moe_expert_sniper.py

# Run 32B dense flash stream (18.4 GB model, 4.5 GB RAM)
python3 flash_stream_v2.py
```

### How F_NOCACHE direct I/O works

```python
import os, fcntl

# Open model file bypassing macOS Unified Buffer Cache
fd = os.open("model.bin", os.O_RDONLY)
fcntl.fcntl(fd, fcntl.F_NOCACHE, 1)  # bypass page cache

# Aligned read (16KB boundary for DART IOMMU)
ALIGN = 16384
offset = (layer_offset // ALIGN) * ALIGN
data = os.pread(fd, layer_size + ALIGN, offset)
weights = data[layer_offset - offset : layer_offset - offset + layer_size]
```

### MoE Expert Sniper pattern

```python
# Router predicts which 8 of 256 experts activate per token
active_experts = router_forward(hidden_state)  # returns [8] indices

# Load only those experts from SSD (8 threads, parallel pread)
from concurrent.futures import ThreadPoolExecutor

def load_expert(expert_idx):
    offset = expert_offsets[expert_idx]
    return os.pread(fd, expert_size, offset)

with ThreadPoolExecutor(max_workers=8) as pool:
    expert_weights = list(pool.map(load_expert, active_experts))

# ~14 MB loaded per layer instead of 221 MB (dense)
```

---

## Common Patterns

### Use as a Python library (direct API calls)

```python
import requests

BASE = "http://localhost:8000/v1"

def ask(prompt: str, system: str = "You are a helpful coding assistant.") -> str:
    r = requests.post(f"{BASE}/chat/completions", json={
        "model": "local",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    })
    return r.json()["choices"][0]["message"]["content"]

# Examples
print(ask("Write a Python function to parse JSON safely"))
print(ask("Explain this error: AttributeError: NoneType has no attribute split"))
```

### Process a large file with paged inference

```python
from mlx.paged_inference import PagedInference

engine = PagedInference(model="mlx-community/Qwen3.5-9B-4bit")

with open("large_codebase.txt") as f:
    content = f.read()  # beyond single context window

# Automatically pages through content
result = engine.summarize(content, question="What does this codebase do?")
print(result)
```

### Monitor server performance

```bash
python3 dashboard.py
```

---

## Model Selection Guide

| Your Mac RAM | Best Option | Command |
|---|---|---|
| 8 GB | 9B Q4_K_M | `--model ~/models/Qwen3.5-9B-Q4_K_M.gguf --ctx-size 4096` |
| 16 GB | 35B IQ2_M (30 tok/s) | Default Option A above |
| 16 GB (quality) | 35B Q4 Expert Sniper | `python3 research/flash-streaming/moe_expert_sniper.py` |
| 48 GB | 35B Q4_K_M native | Download full Q4, `--n-gpu-layers 99` |
| 192 GB | 397B frontier | Any large GGUF, full offload |

---

## Troubleshooting

### Server not responding on port 8000

```bash
# Check if server is running
curl http://localhost:8000/health

# Check what's on port 8000
lsof -i :8000

# Restart llama-server with verbose logging
llama-server --model ~/models/Qwen3.5-35B-A3B-UD-IQ2_M.gguf \
    --port 8000 --verbose
```

### Model download fails / incomplete

```bash
# Resume interrupted download
python3 -c "
from huggingface_hub import hf_hub_download
hf_hub_download(
    'unsloth/Qwen3.5-35B-A3B-GGUF',
    'Qwen3.5-35B-A3B-UD-IQ2_M.gguf',
    local_dir='$HOME/models/',
    resume_download=True
)
"
```

### Slow inference / RAM pressure on 16 GB Mac

```bash
# Reduce context size to free RAM
llama-server --model ~/models/Qwen3.5-35B-A3B-UD-IQ2_M.gguf \
    --port 8000 --ctx-size 4096 \   # reduced from 12288
    --cache-type-k q4_0 --cache-type-v q4_0 \
    --n-gpu-layers 99 -t 4

# Or switch to 9B for lower RAM usage
python3 agent.py
# Then: /model 9b
```

### MLX engine crashes with memory error

```bash
# MLX uses unified memory — check pressure
vm_stat | grep "Pages free"

# Reduce batch size in mlx_engine.py
# Edit: max_batch_size = 512  →  max_batch_size = 128
```

### F_NOCACHE not bypassing page cache (macOS Sonoma+)

```python
# Verify F_NOCACHE is active
import fcntl, os
fd = os.open(model_path, os.O_RDONLY)
result = fcntl.fcntl(fd, fcntl.F_NOCACHE, 1)
assert result == 0, "F_NOCACHE failed — check macOS version and SIP status"
```

### `ddgs` search fails

```bash
pip3 install --upgrade ddgs --break-system-packages
# ddgs uses DuckDuckGo — no API key required, but may rate-limit
# Retry after 60 seconds if you get a 202 response
```

### Wrong reshape on GGUF dequantization

```python
# GGUF tensors are column-major — correct reshape:
weights = dequantized_flat.reshape(ne[1], ne[0])   # CORRECT
# NOT: dequantized_flat.reshape(ne[0], ne[1]).T     # WRONG
```

---

## Architecture Summary

```
agent.py
  ├── Intent classification → "search" | "shell" | "chat"
  ├── search → ddgs.DDGS().text() → summarize
  ├── shell  → generate command → subprocess.run()
  └── chat   → stream directly

Backends (both expose OpenAI-compatible API on :8000)
  ├── llama.cpp  → fast, standard, no persistence
  └── mlx/       → KV cache save/load/compress/sync

Flash Streaming (research/)
  ├── moe_expert_sniper.py  → 35B Q4, 1.42 GB RAM
  └── flash_stream_v2.py    → 32B dense, 4.5 GB RAM
      └── F_NOCACHE + pread + 16KB alignment
```
