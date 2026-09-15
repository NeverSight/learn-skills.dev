---
name: llmfit-hardware-model-matcher
description: Terminal tool that detects your hardware and recommends which LLM models will actually run well on your system
triggers:
  - "find LLM models that fit my hardware"
  - "which AI models can I run locally"
  - "recommend models for my GPU RAM"
  - "check if a model will run on my machine"
  - "llmfit model recommendations"
  - "local LLM hardware compatibility"
  - "what LLM fits my system specs"
  - "score models for my computer"
---

# llmfit Hardware Model Matcher

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

llmfit detects your system's RAM, CPU, and GPU then scores hundreds of LLM models across quality, speed, fit, and context dimensions — telling you exactly which models will run well on your hardware. It ships with an interactive TUI and a CLI, supports multi-GPU, MoE architectures, dynamic quantization, and local runtime providers (Ollama, llama.cpp, MLX, Docker Model Runner).

---

## Installation

### macOS / Linux (Homebrew)
```sh
brew install llmfit
```

### Quick install script
```sh
curl -fsSL https://llmfit.axjns.dev/install.sh | sh

# Without sudo, installs to ~/.local/bin
curl -fsSL https://llmfit.axjns.dev/install.sh | sh -s -- --local
```

### Windows (Scoop)
```sh
scoop install llmfit
```

### Docker / Podman
```sh
docker run ghcr.io/alexsjones/llmfit

# With jq for scripting
podman run ghcr.io/alexsjones/llmfit recommend --use-case coding | jq '.models[].name'
```

### From source (Rust)
```sh
git clone https://github.com/AlexsJones/llmfit.git
cd llmfit
cargo build --release
# binary at target/release/llmfit
```

---

## Core Concepts

- **Fit tiers**: `perfect` (runs great), `good` (runs well), `marginal` (runs but tight), `too_tight` (won't run)
- **Scoring dimensions**: quality, speed (tok/s estimate), fit (memory headroom), context capacity
- **Run modes**: GPU, CPU+GPU offload, CPU-only, MoE
- **Quantization**: automatically selects best quant (e.g. Q4_K_M, Q5_K_S, mlx-4bit) for your hardware
- **Providers**: Ollama, llama.cpp, MLX, Docker Model Runner

---

## Key Commands

### Launch Interactive TUI
```sh
llmfit
```

### CLI Table Output
```sh
llmfit --cli
```

### Show System Hardware Detection
```sh
llmfit system
llmfit --json system   # JSON output
```

### List All Models
```sh
llmfit list
```

### Search Models
```sh
llmfit search "llama 8b"
llmfit search "mistral"
llmfit search "qwen coding"
```

### Fit Analysis
```sh
# All runnable models ranked by fit
llmfit fit

# Only perfect fits, top 5
llmfit fit --perfect -n 5

# JSON output
llmfit --json fit -n 10
```

### Model Detail
```sh
llmfit info "Mistral-7B"
llmfit info "Llama-3.1-70B"
```

### Recommendations
```sh
# Top 5 recommendations (JSON default)
llmfit recommend --json --limit 5

# Filter by use case: general, coding, reasoning, chat, multimodal, embedding
llmfit recommend --json --use-case coding --limit 3
llmfit recommend --json --use-case reasoning --limit 5
```

### Hardware Planning (invert: what hardware do I need?)
```sh
llmfit plan "Qwen/Qwen3-4B-MLX-4bit" --context 8192
llmfit plan "Qwen/Qwen3-4B-MLX-4bit" --context 8192 --quant mlx-4bit
llmfit plan "Qwen/Qwen3-4B-MLX-4bit" --context 8192 --target-tps 25 --json
llmfit plan "Qwen/Qwen2.5-Coder-0.5B-Instruct" --context 8192 --json
```

### REST API Server (for cluster scheduling)
```sh
llmfit serve
llmfit serve --host 0.0.0.0 --port 8787
```

---

## Hardware Overrides

When autodetection fails (VMs, broken nvidia-smi, passthrough setups):

```sh
# Override GPU VRAM
llmfit --memory=32G
llmfit --memory=24G --cli
llmfit --memory=24G fit --perfect -n 5
llmfit --memory=24G recommend --json

# Megabytes
llmfit --memory=32000M

# Works with any subcommand
llmfit --memory=16G info "Llama-3.1-70B"
```

Accepted suffixes: `G`/`GB`/`GiB`, `M`/`MB`/`MiB`, `T`/`TB`/`TiB` (case-insensitive).

### Context Length Cap
```sh
# Estimate memory fit at 4K context
llmfit --max-context 4096 --cli

# With subcommands
llmfit --max-context 8192 fit --perfect -n 5
llmfit --max-context 16384 recommend --json --limit 5

# Environment variable alternative
export OLLAMA_CONTEXT_LENGTH=8192
llmfit recommend --json
```

---

## REST API Reference

Start the server:
```sh
llmfit serve --host 0.0.0.0 --port 8787
```

### Endpoints

```sh
# Health check
curl http://localhost:8787/health

# Node hardware info
curl http://localhost:8787/api/v1/system

# Full model list with filters
curl "http://localhost:8787/api/v1/models?min_fit=marginal&runtime=llamacpp&sort=score&limit=20"

# Top runnable models for this node (key scheduling endpoint)
curl "http://localhost:8787/api/v1/models/top?limit=5&min_fit=good&use_case=coding"

# Search by model name/provider
curl "http://localhost:8787/api/v1/models/Mistral?runtime=any"
```

### Query Parameters for `/models` and `/models/top`

| Param | Values | Description |
|---|---|---|
| `limit` / `n` | integer | Max rows returned |
| `min_fit` | `perfect\|good\|marginal\|too_tight` | Minimum fit tier |
| `perfect` | `true\|false` | Force perfect-only |
| `runtime` | `any\|mlx\|llamacpp` | Filter by runtime |
| `use_case` | `general\|coding\|reasoning\|chat\|multimodal\|embedding` | Use case filter |
| `provider` | string | Substring match on provider |
| `search` | string | Free-text across name/provider/size/use-case |
| `sort` | `score\|tps\|params\|mem\|ctx\|date\|use_case` | Sort column |
| `include_too_tight` | `true\|false` | Include non-runnable models |
| `max_context` | integer | Per-request context cap |

---

## Scripting & Automation Examples

### Bash: Get top coding models as JSON
```bash
#!/bin/bash
# Get top 3 coding models that fit perfectly
llmfit recommend --json --use-case coding --limit 3 | \
  jq -r '.models[] | "\(.name) (\(.score)) - \(.quantization)"'
```

### Bash: Check if a specific model fits
```bash
#!/bin/bash
MODEL="Mistral-7B"
RESULT=$(llmfit info "$MODEL" --json 2>/dev/null)
FIT=$(echo "$RESULT" | jq -r '.fit')
if [[ "$FIT" == "perfect" || "$FIT" == "good" ]]; then
  echo "$MODEL will run well (fit: $FIT)"
else
  echo "$MODEL may not run well (fit: $FIT)"
fi
```

### Bash: Auto-pull top Ollama model
```bash
#!/bin/bash
# Get the top fitting model name and pull it with Ollama
TOP_MODEL=$(llmfit recommend --json --limit 1 | jq -r '.models[0].name')
echo "Pulling: $TOP_MODEL"
ollama pull "$TOP_MODEL"
```

### Python: Query the REST API
```python
import requests

BASE_URL = "http://localhost:8787"

def get_system_info():
    resp = requests.get(f"{BASE_URL}/api/v1/system")
    return resp.json()

def get_top_models(use_case="coding", limit=5, min_fit="good"):
    params = {
        "use_case": use_case,
        "limit": limit,
        "min_fit": min_fit,
        "sort": "score"
    }
    resp = requests.get(f"{BASE_URL}/api/v1/models/top", params=params)
    return resp.json()

def search_models(query, runtime="any"):
    resp = requests.get(
        f"{BASE_URL}/api/v1/models/{query}",
        params={"runtime": runtime}
    )
    return resp.json()

# Example usage
system = get_system_info()
print(f"GPU: {system.get('gpu_name')} | VRAM: {system.get('vram_gb')}GB")

models = get_top_models(use_case="reasoning", limit=3)
for m in models.get("models", []):
    print(f"{m['name']}: score={m['score']}, fit={m['fit']}, quant={m['quantization']}")
```

### Python: Hardware-aware model selector for agents
```python
import subprocess
import json

def get_best_model_for_task(use_case: str, min_fit: str = "good") -> dict:
    """Use llmfit to select the best model for a given task."""
    result = subprocess.run(
        ["llmfit", "recommend", "--json", "--use-case", use_case, "--limit", "1"],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    models = data.get("models", [])
    return models[0] if models else None

def plan_hardware_requirements(model_name: str, context: int = 4096) -> dict:
    """Get hardware requirements for running a specific model."""
    result = subprocess.run(
        ["llmfit", "plan", model_name, "--context", str(context), "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# Select best coding model
best = get_best_model_for_task("coding")
if best:
    print(f"Best coding model: {best['name']}")
    print(f"  Quantization: {best['quantization']}")
    print(f"  Estimated tok/s: {best['tps']}")
    print(f"  Memory usage: {best['mem_pct']}%")

# Plan hardware for a specific model
plan = plan_hardware_requirements("Qwen/Qwen3-4B-MLX-4bit", context=8192)
print(f"Min VRAM needed: {plan['hardware']['min_vram_gb']}GB")
print(f"Recommended VRAM: {plan['hardware']['recommended_vram_gb']}GB")
```

### Docker Compose: Node scheduler pattern
```yaml
version: "3.8"
services:
  llmfit-api:
    image: ghcr.io/alexsjones/llmfit
    command: serve --host 0.0.0.0 --port 8787
    ports:
      - "8787:8787"
    environment:
      - OLLAMA_CONTEXT_LENGTH=8192
    devices:
      - /dev/nvidia0:/dev/nvidia0  # pass GPU through
```

---

## TUI Key Reference

| Key | Action |
|---|---|
| `↑`/`↓` or `j`/`k` | Navigate models |
| `/` | Search (name, provider, params, use case) |
| `Esc`/`Enter` | Exit search |
| `Ctrl-U` | Clear search |
| `f` | Cycle fit filter: All → Runnable → Perfect → Good → Marginal |
| `a` | Cycle availability: All → GGUF Avail → Installed |
| `s` | Cycle sort: Score → Params → Mem% → Ctx → Date → Use Case |
| `t` | Cycle color theme (auto-saved) |
| `v` | Visual mode (multi-select for comparison) |
| `V` | Select mode (column-based filtering) |
| `p` | Plan mode (what hardware needed for this model?) |
| `P` | Provider filter popup |
| `U` | Use-case filter popup |
| `C` | Capability filter popup |
| `m` | Mark model for comparison |
| `c` | Compare view (marked vs selected) |
| `d` | Download model (via detected runtime) |
| `r` | Refresh installed models from runtimes |
| `Enter` | Toggle detail view |
| `g`/`G` | Jump to top/bottom |
| `q` | Quit |

### Themes
`t` cycles: Default → Dracula → Solarized → Nord → Monokai → Gruvbox  
Theme saved to `~/.config/llmfit/theme`

---

## GPU Detection Details

| GPU Vendor | Detection Method |
|---|---|
| NVIDIA | `nvidia-smi` (multi-GPU, aggregates VRAM) |
| AMD | `rocm-smi` |
| Intel Arc | sysfs (discrete) / `lspci` (integrated) |
| Apple Silicon | `system_profiler` (unified memory = VRAM) |
| Ascend | `npu-smi` |

---

## Common Patterns

### "What can I run on my 16GB M2 Mac?"
```sh
llmfit fit --perfect -n 10
# or interactively
llmfit
# press 'f' to filter to Perfect fit
```

### "I have a 3090 (24GB VRAM), what coding models fit?"
```sh
llmfit recommend --json --use-case coding | jq '.models[]'
# or with manual override if detection fails
llmfit --memory=24G recommend --json --use-case coding
```

### "Can Llama 70B run on my machine?"
```sh
llmfit info "Llama-3.1-70B"
# Plan what hardware you'd need
llmfit plan "Llama-3.1-70B" --context 4096 --json
```

### "Show me only models already installed in Ollama"
```sh
llmfit
# press 'a' to cycle to Installed filter
# or
llmfit fit -n 20  # run, press 'i' in TUI for installed-first
```

### "Script: find best model and start Ollama"
```bash
MODEL=$(llmfit recommend --json --limit 1 | jq -r '.models[0].name')
ollama serve &
ollama run "$MODEL"
```

### "API: poll node capabilities for cluster scheduler"
```bash
# Check node, get top 3 good+ models for reasoning
curl -s "http://node1:8787/api/v1/models/top?limit=3&min_fit=good&use_case=reasoning" | \
  jq '.models[].name'
```

---

## Troubleshooting

**GPU not detected / wrong VRAM reported**
```sh
# Verify detection
llmfit system

# Manual override
llmfit --memory=24G --cli
```

**`nvidia-smi` not found but you have an NVIDIA GPU**
```sh
# Install CUDA toolkit or nvidia-utils, then retry
# Or override manually:
llmfit --memory=8G fit --perfect
```

**Models show as too_tight but you have enough RAM**
```sh
# llmfit may be using context-inflated estimates; cap context
llmfit --max-context 2048 fit --perfect -n 10
```

**REST API: test endpoints**
```sh
# Spawn server and run validation suite
python3 scripts/test_api.py --spawn

# Test already-running server
python3 scripts/test_api.py --base-url http://127.0.0.1:8787
```

**Apple Silicon: VRAM shows as system RAM (expected)**
```sh
# This is correct — Apple Silicon uses unified memory
# llmfit accounts for this automatically
llmfit system  # should show backend: Metal
```

**Context length environment variable**
```sh
export OLLAMA_CONTEXT_LENGTH=4096
llmfit recommend --json  # uses 4096 as context cap
```
