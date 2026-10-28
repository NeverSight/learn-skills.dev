---
name: oransim-causal-marketing-twin
description: Causal digital twin for marketing simulation — predict campaign ROI, run counterfactual KOL swaps, and audit causal graphs before spending a dollar.
triggers:
  - simulate marketing campaign ROI
  - run counterfactual campaign analysis
  - predict KOL performance before launch
  - swap KOL mid-campaign simulation
  - causal marketing twin
  - oransim predict campaign
  - what if I change my marketing budget
  - pre-launch ROI ranking for creatives
---

# Oransim — Causal Digital Twin for Marketing

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Oransim is an open-source causal simulation engine for marketing teams. It lets you predict campaign ROI, run counterfactual "what if" scenarios (swap KOLs, reallocate budget, change platforms), and audit every prediction through a transparent 64-node causal graph — before spending a dollar.

**Core capabilities:**
- **Pre-launch ROI ranking** across creative × KOL × budget combinations
- **Mid-campaign `do()`-operator rollouts** (e.g. swap KOL on day 3, see 14-day path diff)
- **Post-mortem counterfactuals** (what if we'd spent on 小红书 instead of 抖音?)
- LLM-backed "soul personas" for 1M+ virtual consumer agents
- Causal Neural Hawkes Process for temporal cascade simulation
- Per-arm counterfactual heads (TARNet / Dragonnet architecture)

---

## Installation

```bash
git clone https://github.com/OranAi-Ltd/oransim.git
cd oransim
pip install -e '.[dev]'
```

### Backend (mock mode — no API key needed)

```bash
LLM_MODE=mock python -m uvicorn oransim.api:app --port 8001
```

### Backend (real LLM pipeline)

```bash
LLM_MODE=api \
LLM_API_KEY=$YOUR_LLM_API_KEY \
LLM_MODEL=gpt-4o \
python -m uvicorn oransim.api:app --port 8001
```

### Frontend

```bash
python -m http.server 8090 --directory frontend
# Open http://localhost:8090
```

---

## Configuration

All config via environment variables (see `.env.example`):

```bash
# LLM mode: "mock" (deterministic stubs) or "api" (real LLM)
LLM_MODE=api

# Provider: openai (default), anthropic, gemini, qwen
LLM_PROVIDER=openai

# API key (also accepts provider-specific: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
LLM_API_KEY=sk-...

# Model
LLM_MODEL=gpt-4o

# Custom base URL (DeepSeek, vLLM, etc.)
LLM_BASE_URL=https://api.deepseek.com/v1
```

### Provider quick-reference

| Provider | `LLM_PROVIDER` | `LLM_BASE_URL` | Example model |
|---|---|---|---|
| OpenAI | `openai` | `https://api.openai.com/v1` | `gpt-4o` |
| DeepSeek | `openai` | `https://api.deepseek.com/v1` | `deepseek-chat` |
| vLLM (local) | `openai` | `http://localhost:8000/v1` | any |
| Anthropic | `anthropic` | *(default)* | `claude-sonnet-4-6` |
| Gemini | `gemini` | *(default)* | `gemini-2.5-flash` |
| Qwen | `qwen` | *(default)* | `qwen-plus` |

---

## Key API Endpoints

All endpoints served at `http://localhost:8001`.

### POST `/api/predict` — Run a campaign simulation

```python
import httpx

payload = {
    "campaign": {
        "name": "Summer Beauty Launch",
        "platform": "xhs",           # xhs | douyin | tiktok
        "budget": 500000,            # CNY
        "duration_days": 14,
        "creatives": [
            {"id": "vid_A", "type": "video", "duration_sec": 30},
            {"id": "vid_B", "type": "video", "duration_sec": 60},
        ],
        "kols": [
            {"id": "kol_001", "tier": "mid", "vertical": "beauty", "fans": 250000},
            {"id": "kol_002", "tier": "koc", "vertical": "skincare", "fans": 45000},
        ],
        "budget_split": {"xhs": 0.6, "douyin": 0.4},
    },
    "mode": "fast",   # "fast" (quantile baseline) | "full" (LLM agent simulation)
    "n_simulations": 100,
}

response = httpx.post("http://localhost:8001/api/predict", json=payload, timeout=120)
result = response.json()

print(result["roi"]["p50"])    # median ROI
print(result["roi"]["p35"])    # lower confidence band
print(result["roi"]["p65"])    # upper confidence band
print(result["causal_path"])   # which nodes drove the prediction
```

### GET `/api/graph/inspect` — Audit the causal graph

```python
import httpx, json

graph = httpx.get("http://localhost:8001/api/graph/inspect").json()
print(f"Nodes: {len(graph['nodes'])}")   # 64 nodes
print(f"Edges: {len(graph['edges'])}")   # 117 edges

# Find all paths from budget allocation to purchase intent
for edge in graph["edges"]:
    if edge["source"] == "budget_allocation":
        print(edge)
```

### POST `/api/sandbox/counterfactual` — Mid-campaign KOL swap

```python
import httpx

# Scenario: campaign running, day 3, swap KOL
counterfactual = httpx.post(
    "http://localhost:8001/api/sandbox/counterfactual",
    json={
        "base_campaign_id": "campaign_abc123",
        "intervention": {
            "do": {
                "kol": {"remove": ["kol_001"], "add": ["kol_003"]},
                "day": 3,
                "budget_realloc": {"kol_001_budget": "kol_003"},
            }
        },
        "rollout_days": 14,
    },
    timeout=120,
).json()

print(counterfactual["roi_diff"])          # ROI change from intervention
print(counterfactual["trajectory_diff"])   # day-by-day path difference
print(counterfactual["attribution"])       # which causal nodes shifted
```

### POST `/api/sandbox/postmortem` — Platform counterfactual

```python
import httpx

postmortem = httpx.post(
    "http://localhost:8001/api/sandbox/postmortem",
    json={
        "actuals": {
            "campaign_id": "q2_campaign",
            "spend": {"xhs": 200000, "douyin": 300000},
            "observed_roi": 1.4,
        },
        "counterfactual_alloc": {"xhs": 1.0, "douyin": 0.0},  # what if all on XHS?
    },
    timeout=120,
).json()

print(postmortem["counterfactual_roi"])   # what ROI would have been
print(postmortem["delta"])                # difference from actuals
```

### GET `/api/adapters` — List available platform adapters

```python
import httpx
adapters = httpx.get("http://localhost:8001/api/adapters").json()
# Returns: ["xhs_v1", "tiktok_agent", "douyin", ...]
```

---

## Python SDK Usage (Direct Engine)

For programmatic use without the HTTP layer:

```python
from oransim.world_model import AgentSociety
from oransim.causal import CausalGraph, do_operator
from oransim.diffusion import HawkesRollout

# 1. Build the causal graph
graph = CausalGraph.from_config("configs/default_graph.yaml")

# 2. Initialize virtual consumer society
society = AgentSociety(
    n_agents=10_000,        # scale down from 1M for local dev
    vertical="beauty",
    platform="xhs",
    llm_mode="mock",        # "mock" | "api"
)

# 3. Define campaign
campaign = {
    "budget": 200_000,
    "kols": [{"id": "kol_001", "tier": "mid", "fans": 150_000}],
    "creative_ids": ["vid_A"],
    "duration_days": 14,
}

# 4. Run baseline simulation
baseline = HawkesRollout(graph=graph, society=society)
result = baseline.run(campaign, n_simulations=50)
print(f"P50 ROI: {result.roi.p50:.2f}")

# 5. Apply do()-operator intervention
with do_operator(graph) as intervened_graph:
    intervened_graph.set("kol_assignment", "kol_002")
    intervened_graph.set("intervention_day", 3)

    counterfactual = HawkesRollout(graph=intervened_graph, society=society)
    cf_result = counterfactual.run(campaign, n_simulations=50)

print(f"Counterfactual P50 ROI: {cf_result.roi.p50:.2f}")
print(f"Delta: {cf_result.roi.p50 - result.roi.p50:.2f}")
```

---

## Pre-launch ROI Ranking (All Combinations)

```python
from itertools import product
from oransim.world_model import AgentSociety
from oransim.causal import CausalGraph
from oransim.diffusion import HawkesRollout
import pandas as pd

graph = CausalGraph.from_config("configs/default_graph.yaml")
society = AgentSociety(n_agents=5_000, vertical="beauty", platform="xhs", llm_mode="mock")

creatives = ["vid_A", "vid_B", "vid_C", "vid_D"]
kol_lists = [["kol_001"], ["kol_002"], ["kol_003"]]
budgets = [200_000, 500_000]

results = []
for creative, kols, budget in product(creatives, kol_lists, budgets):
    campaign = {"budget": budget, "kols": kols, "creative_ids": [creative], "duration_days": 14}
    rollout = HawkesRollout(graph=graph, society=society)
    r = rollout.run(campaign, n_simulations=30)
    results.append({
        "creative": creative,
        "kol": kols[0],
        "budget": budget,
        "roi_p35": r.roi.p35,
        "roi_p50": r.roi.p50,
        "roi_p65": r.roi.p65,
    })

df = pd.DataFrame(results).sort_values("roi_p50", ascending=False)
print(df.head(5).to_string())   # top 5 combinations
```

---

## Common Patterns

### Pattern 1: Mock mode for CI / testing

```python
import os
os.environ["LLM_MODE"] = "mock"

from oransim.world_model import AgentSociety
society = AgentSociety(n_agents=100, vertical="beauty", platform="xhs", llm_mode="mock")
# All LLM calls return deterministic stubs — fast, free, reproducible
```

### Pattern 2: Check if backend is in mock mode

```python
import httpx
health = httpx.get("http://localhost:8001/health").json()
if health.get("llm_mode") == "mock":
    print("WARNING: Running in mock mode — LLM features are stubs")
```

### Pattern 3: Inspect a prediction's causal path

```python
result = httpx.post("http://localhost:8001/api/predict", json=payload).json()

# Every prediction includes which causal nodes fired
for node in result["causal_path"]:
    print(f"{node['id']:30s}  weight={node['weight']:.3f}  layer={node['layer']}")
```

### Pattern 4: Load the LightGBM quantile baseline (fast mode)

```python
import pickle, numpy as np

with open("models/lgbm_quantile_baseline.pkl", "rb") as f:
    model = pickle.load(f)

# Feature vector: [budget, n_kols, avg_fans, duration_days, platform_enc]
X = np.array([[500_000, 2, 150_000, 14, 0]])   # 0=xhs, 1=douyin
p35, p50, p65 = model.predict(X)
print(f"ROI P35={p35[0]:.2f}  P50={p50[0]:.2f}  P65={p65[0]:.2f}")
```

---

## Project Structure

```
oransim/
├── oransim/
│   ├── api.py                  # FastAPI app + god-file (being refactored to api_routers/)
│   ├── api_routers/            # Split routers: predict, sandbox, graph, adapters
│   ├── causal/                 # SCM, do()-operator, 64-node graph, Pearl 3-step
│   ├── world_model/            # AgentSociety, IPF population synthesis, soul personas
│   ├── diffusion/              # Causal Neural Hawkes Process rollout (14-day)
│   └── adapters/               # Platform adapters: xhs_v1, tiktok_agent, douyin, ...
├── frontend/
│   ├── index.html
│   └── js/                     # Modular JS: hero, tabs, cascade animation
├── configs/
│   └── default_graph.yaml      # 64 nodes / 117 edges causal graph definition
├── models/
│   └── lgbm_quantile_baseline.pkl
├── data/                       # 21k-note OSS demo corpus
├── docs/
│   └── en/quickstart.md
└── .env.example
```

---

## Troubleshooting

### Backend returns mock data even with API key set

Check the yellow banner in the frontend. Verify env vars are exported:
```bash
echo $LLM_MODE    # should be "api"
echo $LLM_API_KEY # should be non-empty
# Restart the server after setting env vars — uvicorn reads them at startup
```

### `ModuleNotFoundError: oransim`

Install in editable mode from the repo root:
```bash
pip install -e '.[dev]'
```

### Simulation times out (> 120s)

Reduce agent count or use fast mode:
```python
# In payload:
{"mode": "fast", "n_simulations": 30}
# Or reduce society size in direct SDK usage:
AgentSociety(n_agents=1_000, ...)
```

### CORS errors when calling API from browser

The FastAPI app includes CORS middleware for `localhost:8090`. If using a different port:
```python
# In oransim/api.py, update the origins list or set:
CORS_ORIGINS=http://localhost:YOUR_PORT uvicorn oransim.api:app --port 8001
```

### Counterfactual returns identical result to baseline

In mock mode this is expected — stubs are deterministic. Switch to `LLM_MODE=api` for real divergence between baseline and intervention arms.

### Enterprise data access (4.3M+ 小红书 notes, 2.1M+ creators)

The OSS corpus is 21k notes. For production-scale data:
- Browse: [datacenter.oran.cn](https://datacenter.oran.cn/)
- Contact: `cto@orannai.com`

---

## Key Concepts

| Term | Meaning |
|---|---|
| `do()` operator | Pearl's intervention operator — sets a variable to a value, cuts its incoming causal edges |
| Soul persona | LLM-backed agent personality that reads actual creatives and decides engagement |
| Hawkes rollout | Self-exciting point process simulating cascade of social shares over 14 days |
| P35/P50/P65 | Confidence bands on ROI — not point estimates, always a distribution |
| KOL tier | Top (>1M fans), Mid (50k–1M), KOC (1k–50k), long-tail (<1k) |
| Fast mode | LightGBM quantile baseline — seconds, no LLM calls |
| Full mode | Complete agent simulation with LLM soul personas — minutes, requires `LLM_MODE=api` |
