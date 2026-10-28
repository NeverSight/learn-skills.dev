---
name: club-3090-llm-serving
description: Recipes and configs for serving LLMs locally on RTX 3090 GPUs using vLLM, llama.cpp, and SGLang with OpenAI-compatible API
triggers:
  - "serve LLM on RTX 3090"
  - "run Qwen on 3090"
  - "local LLM serving with vLLM"
  - "llama.cpp 262K context single card"
  - "dual 3090 inference setup"
  - "club-3090 config"
  - "local OpenAI-compatible API"
  - "homelab LLM docker compose"
---

# club-3090 LLM Serving

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Community recipes for serving modern LLMs on RTX 3090 (24 GB) hardware. Supports vLLM, llama.cpp, and SGLang engines with validated Docker Compose configs exposing an OpenAI-compatible API on `localhost:8020`. Currently ships Qwen3.6-27B configs for 1× and 2× cards.

---

## Engine Decision Matrix

| Need | Engine | Why |
|---|---|---|
| Max throughput (code/chat) | vLLM dual | 89–127 TPS, MTP n=3, vision, tools |
| Full 262K context, no crashes | llama.cpp single | No prefill cliffs, stable tool-use |
| 4 concurrent streams @ 262K | vLLM dual turbo | Stream isolation, full feature stack |
| Single card, moderate ctx | vLLM default | ~89 TPS, easiest setup |

SGLang is currently **blocked** on Qwen3.6-27B — see `models/qwen3.6-27b/sglang/README.md`.

---

## Prerequisites

```
- 1× or 2× NVIDIA RTX 3090 (24 GB each)
- Linux (Ubuntu 22.04+ recommended)
- Docker + NVIDIA Container Toolkit
- NVIDIA driver 580.x+
- ~30 GB free disk per model
```

---

## Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/noonghunna/club-3090.git
cd club-3090
```

### 2. Download and verify a model

```bash
# Downloads model weights, verifies SHA, clones Genesis patches
bash scripts/setup.sh qwen3.6-27b
```

### 3. Launch (interactive wizard)

```bash
bash scripts/launch.sh
# Wizard prompts: engine → card count → workload → boots compose → verifies
```

### 4. Launch (non-interactive)

```bash
# Single card, chat-optimized
bash scripts/launch.sh --variant vllm/default

# Dual card, 262K context + vision
bash scripts/launch.sh --variant vllm/dual

# Single card, 262K context, no prefill cliffs
bash scripts/launch.sh --variant llamacpp/default

# List all available variants
bash scripts/switch.sh --list
```

---

## Key Scripts

| Script | Purpose |
|---|---|
| `scripts/setup.sh <model>` | Preflight checks, model download, SHA verify, Genesis patch clone |
| `scripts/launch.sh [--variant X]` | Interactive or direct variant boot; calls switch.sh + verify-full.sh |
| `scripts/switch.sh <variant>` | Stateless switcher — tears down old compose, brings up new one |
| `scripts/health.sh` | Live health probe: KV %, MTP accept-length, recent TPS, errors |
| `scripts/verify.sh` | Quick smoke test (engine-aware via env vars) |
| `scripts/verify-full.sh` | 8-check functional test (~1–2 min) |
| `scripts/verify-stress.sh` | Boundary stress test: 262K ladder + tool prefill OOM (~5–10 min) |
| `scripts/bench.sh` | Canonical TPS benchmark (3 warm + 5 measured runs) |

### Common script usage

```bash
# Switch variants without the wizard
bash scripts/switch.sh vllm/long-vision
bash scripts/switch.sh vllm/dual
bash scripts/switch.sh llamacpp/default

# Check runtime health
bash scripts/health.sh
# Output: KV cache %, MTP accept-length rate, recent TPS, error log tail

# Run canonical benchmark
bash scripts/bench.sh
# Runs narrative + code prompts, prints per-run TPS + averages

# Full functional verification after a switch
bash scripts/verify-full.sh

# Stress test (run before relying on long-context)
bash scripts/verify-stress.sh
```

---

## Variant Names Reference

```
vllm/default          Single-card, chat-optimized (recommended first start)
vllm/dual             Dual-card, 262K ctx, vision, tools, MTP n=3
vllm/long-vision      Dual-card, long-context + vision workloads
vllm/turbo            Dual-card, 4 concurrent streams @ 262K
llamacpp/default      Single-card, full 262K, no prefill cliffs
llamacpp/65k          Single-card, 65K ctx (faster, more VRAM headroom)
llamacpp/dual         Dual-card llama.cpp recipe
```

---

## API Usage (OpenAI-compatible, port 8020)

The server exposes a standard OpenAI-compatible API. Use the `openai` Python SDK pointed at `localhost:8020`.

### Python — openai SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8020/v1",
    api_key="ignored",  # local server, no auth needed
)

# Basic chat
response = client.chat.completions.create(
    model="qwen3.6-27b-autoround",
    messages=[{"role": "user", "content": "Explain KV cache in one paragraph."}],
    max_tokens=512,
)
print(response.choices[0].message.content)
```

### Python — streaming

```python
stream = client.chat.completions.create(
    model="qwen3.6-27b-autoround",
    messages=[{"role": "user", "content": "Write a Python quicksort."}],
    max_tokens=1024,
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
print()
```

### Python — raw requests (no SDK dependency)

```python
import requests, json

payload = {
    "model": "qwen3.6-27b-autoround",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ],
    "max_tokens": 200,
    "temperature": 0.7,
}

resp = requests.post(
    "http://localhost:8020/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json=payload,
    timeout=120,
)
resp.raise_for_status()
print(resp.json()["choices"][0]["message"]["content"])
```

### Python — tool calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for recent information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"],
            },
        },
    }
]

response = client.chat.completions.create(
    model="qwen3.6-27b-autoround",
    messages=[{"role": "user", "content": "What's the latest news on CUDA 13?"}],
    tools=tools,
    tool_choice="auto",
    max_tokens=512,
)

msg = response.choices[0].message
if msg.tool_calls:
    for call in msg.tool_calls:
        print(f"Tool: {call.function.name}")
        print(f"Args: {call.function.arguments}")
```

### Python — long context (262K, use with llamacpp/default or vllm/dual)

```python
# Load a large document
with open("large_codebase.txt") as f:
    document = f.read()

response = client.chat.completions.create(
    model="qwen3.6-27b-autoround",
    messages=[
        {"role": "user", "content": f"Summarize the architecture:\n\n{document}"},
    ],
    max_tokens=1024,
)
print(response.choices[0].message.content)
```

### TypeScript / Node

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:8020/v1",
  apiKey: "ignored",
});

async function chat(prompt: string): Promise<string> {
  const response = await client.chat.completions.create({
    model: "qwen3.6-27b-autoround",
    messages: [{ role: "user", content: prompt }],
    max_tokens: 512,
  });
  return response.choices[0].message.content ?? "";
}

// Streaming in Node
async function streamChat(prompt: string): Promise<void> {
  const stream = await client.chat.completions.create({
    model: "qwen3.6-27b-autoround",
    messages: [{ role: "user", content: prompt }],
    max_tokens: 1024,
    stream: true,
  });
  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content ?? "");
  }
  console.log();
}
```

### curl — quick sanity check

```bash
curl -sf http://localhost:8020/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.6-27b-autoround",
    "messages": [{"role": "user", "content": "Capital of France?"}],
    "max_tokens": 200
  }' | jq '.choices[0].message.content'
```

### curl — list available models

```bash
curl -sf http://localhost:8020/v1/models | jq '.data[].id'
```

---

## Docker Compose Structure

Configs live under `models/qwen3.6-27b/vllm/compose/`. Example structure of a single-card compose:

```yaml
# models/qwen3.6-27b/vllm/compose/default.yml (representative structure)
services:
  vllm:
    image: vllm/vllm-openai:v0.20.1rc1.dev16+g7a1eb8ac2
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
      - CUDA_VISIBLE_DEVICES=0
    ports:
      - "8020:8000"
    volumes:
      - ${MODEL_PATH}:/models/qwen3.6-27b
      - ${PATCH_PATH}:/patches
    command: >
      --model /models/qwen3.6-27b
      --served-model-name qwen3.6-27b-autoround
      --tensor-parallel-size 1
      --max-model-len 65536
      --kv-cache-dtype fp8
      --speculative-model /models/qwen3.6-27b/mtp_head
      --num-speculative-tokens 3
      --port 8000
```

For dual-card, `tensor-parallel-size 2` and `NVIDIA_VISIBLE_DEVICES=0,1` are set, and `max-model-len` extends to 262144.

---

## Connecting External Clients

### Open WebUI

```
API Base URL: http://localhost:8020/v1
API Key:      (leave blank or type anything)
Model:        qwen3.6-27b-autoround
```

### Cline / Cursor / Copilot-compatible tools

```json
{
  "openai.baseURL": "http://localhost:8020/v1",
  "openai.apiKey": "local",
  "openai.model": "qwen3.6-27b-autoround"
}
```

### LiteLLM proxy passthrough

```yaml
# litellm_config.yaml
model_list:
  - model_name: qwen3.6-27b
    litellm_params:
      model: openai/qwen3.6-27b-autoround
      api_base: http://localhost:8020/v1
      api_key: ignored
```

---

## Repo Layout Quick Reference

```
club-3090/
├── scripts/               Shared model-aware scripts (setup, launch, bench, health)
├── models/
│   └── qwen3.6-27b/
│       ├── vllm/
│       │   ├── compose/   Docker Compose files (all variants)
│       │   └── patches/   tolist_cudagraph, Marlin pad, Genesis pointer
│       ├── llama-cpp/
│       │   └── recipes/   Single-card 65K / 262K-max / dual recipes
│       └── sglang/        Blocked — watch list only
└── docs/
    ├── SINGLE_CARD.md     1× 3090 workload → config guide
    ├── DUAL_CARD.md       2× 3090 workload → config guide
    ├── HARDWARE.md        PCIe vs NVLink, power draw, card compatibility
    ├── GLOSSARY.md        TPS / KV / MTP / TP / prefill cliff definitions
    ├── CLIFFS.md          Prefill cliff root causes and fix landscape
    ├── COMPARISONS.md     Self-host vs cloud cost crossover analysis
    ├── UPSTREAM.md        Tracked upstream issues and PRs
    └── engines/           Per-engine deep dives (vLLM / llama.cpp / SGLang)
```

---

## Troubleshooting

### Server won't start — CUDA/driver error

```bash
# Check driver version (need 580.x+)
nvidia-smi --query-gpu=driver_version --format=csv,noheader

# Check NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# Check GPU visibility
nvidia-smi -L
```

### Out of VRAM / OOM on prefill

```bash
# Check current KV cache usage
bash scripts/health.sh

# Switch to a config with smaller max-model-len
bash scripts/switch.sh llamacpp/65k       # 65K ctx, more headroom
bash scripts/switch.sh llamacpp/default   # 262K but manages prefill correctly
```

### Prefill cliff (vLLM hangs or errors on large prompts)

This is a known DeltaNet architecture issue on Qwen3.6-27B with vLLM. The llama.cpp route avoids it entirely:

```bash
bash scripts/switch.sh llamacpp/default
# Stress-test it:
bash scripts/verify-stress.sh
```

For vLLM workarounds, see `models/qwen3.6-27b/INTERNALS.md` and `docs/CLIFFS.md`.

### MTP / speculative decoding not accepting tokens

```bash
bash scripts/health.sh
# Look for "MTP AL:" (accept-length) — should be > 1.0
# If AL ~= 1.0, speculative head may not be loaded correctly
# Check that Genesis patches were applied:
bash scripts/setup.sh qwen3.6-27b   # re-runs patch verification
```

### Tool call returns 25K+ tokens and hangs

Known failure mode on vLLM with very large tool responses. Use llama.cpp:

```bash
bash scripts/switch.sh llamacpp/default
# llama.cpp handles 25K-token tool returns cleanly (stress-tested)
```

### Switching variants leaves old container running

```bash
# switch.sh handles this, but if you ran docker compose manually:
docker compose -f models/qwen3.6-27b/vllm/compose/default.yml down
bash scripts/switch.sh vllm/dual
```

### Check what variant is currently running

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}"
```

---

## Performance Reference (Qwen3.6-27B)

| Config | Cards | TPS (narrative) | TPS (code) | Max ctx | Notes |
|---|---|---|---|---|---|
| `vllm/default` | 1× | ~89 | ~89 | 65K | Recommended starting point |
| `vllm/dual` | 2× | ~89 | ~127 | 262K | DFlash on code workloads |
| `vllm/turbo` | 2× | — | — | 262K | 4 concurrent streams |
| `llamacpp/default` | 1× | ~21 | ~21 | 262K | No cliffs, stable tool-use |

Benchmark substrate: vLLM nightly `0.20.1rc1.dev16+g7a1eb8ac2` + Genesis v7.65 dev, llama.cpp `0d0764dfd`, RTX 3090 sm_86 PCIe @ 230 W. Full per-run numbers in `models/qwen3.6-27b/CHANGELOG.md`.

---

## Adding a New Model

```bash
# The repo structure is model-agnostic.
# New models follow the same pattern under models/<name>/:
mkdir -p models/glm-4.6/{vllm/compose,vllm/patches,llama-cpp/recipes,sglang}
# Add README.md, INTERNALS.md, CHANGELOG.md following qwen3.6-27b/ as template
# setup.sh and launch.sh are model-aware — add the model slug to their dispatch

bash scripts/setup.sh glm-4.6   # once scripts updated
```

---

## Key Links

- [docs/SINGLE_CARD.md](docs/SINGLE_CARD.md) — 1× 3090 workload → config → quick start
- [docs/DUAL_CARD.md](docs/DUAL_CARD.md) — 2× 3090 workload → config → quick start
- [docs/HARDWARE.md](docs/HARDWARE.md) — 4090/A6000 compatibility, NVLink notes
- [docs/GLOSSARY.md](docs/GLOSSARY.md) — TPS, KV cache, MTP, TP, prefill cliff explained
- [docs/COMPARISONS.md](docs/COMPARISONS.md) — self-host vs cloud cost crossover
- [docs/CLIFFS.md](docs/CLIFFS.md) — prefill cliff deep dive
- [docs/UPSTREAM.md](docs/UPSTREAM.md) — upstream issues/PRs being tracked
- [CONTRIBUTING.md](CONTRIBUTING.md) — adding numbers, bug repros, new variants
