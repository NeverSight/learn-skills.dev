---
name: obliteratus-abliteration
description: One-click model liberation toolkit for removing refusal behaviors from LLMs via surgical abliteration techniques
triggers:
  - abliterate a model
  - remove refusal from LLM
  - obliterate model guardrails
  - free a language model from restrictions
  - run abliteration on huggingface model
  - use OBLITERATUS to uncensor a model
  - extract refusal directions from transformer
  - analyze refusal geometry in LLM
---

# OBLITERATUS — LLM Abliteration Toolkit

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OBLITERATUS is an open-source toolkit for identifying and surgically removing refusal behaviors from large language models using mechanistic interpretability techniques (abliteration). It locates refusal directions in a model's hidden states via SVD/PCA, projects them out of the weights, and preserves core language capabilities. Ships with a Gradio UI, CLI, Python API, and Colab notebook.

---

## Installation

```bash
# Core install
pip install obliteratus

# With Gradio UI support
pip install "obliteratus[spaces]"

# With all optional analysis modules
pip install "obliteratus[full]"

# From source (latest)
git clone https://github.com/elder-plinius/OBLITERATUS
cd OBLITERATUS
pip install -e ".[full]"
```

**Requirements:**
- Python 3.10+
- PyTorch 2.1+ with CUDA (recommended) or CPU
- `transformers`, `accelerate`, `gradio>=5.29.0`
- HuggingFace account + token for gated models

```bash
export HF_TOKEN=your_hf_token_here
huggingface-cli login
```

---

## CLI — Key Commands

```bash
# Basic obliteration (default method)
obliteratus obliterate meta-llama/Llama-3.1-8B-Instruct

# Advanced method (whitened SVD + bias projection + iterative refinement)
obliteratus obliterate meta-llama/Llama-3.1-8B-Instruct --method advanced

# Analysis-informed pipeline (auto-configures from geometry analysis)
obliteratus obliterate meta-llama/Llama-3.1-8B-Instruct --method informed

# Specify output directory and push to Hub
obliteratus obliterate mistralai/Mistral-7B-Instruct-v0.3 \
  --method advanced \
  --output ./my-liberated-model \
  --push-to-hub your-username/mistral-7b-liberated

# LoRA-based reversible ablation (non-destructive)
obliteratus obliterate meta-llama/Llama-3.1-8B-Instruct \
  --method lora \
  --lora-rank 1

# Strength sweep — find the capability/compliance tradeoff
obliteratus sweep meta-llama/Llama-3.1-8B-Instruct \
  --strengths 0.2,0.4,0.6,0.8,1.0

# Run analysis modules only (no modification)
obliteratus analyze meta-llama/Llama-3.1-8B-Instruct \
  --modules concept_cone,alignment_imprint,universality

# Benchmark: compare methods on a model
obliteratus benchmark meta-llama/Llama-3.1-8B-Instruct \
  --methods basic,advanced,informed

# Launch local Gradio UI
obliteratus ui
obliteratus ui --port 8080 --share
obliteratus ui --no-telemetry
```

---

## Python API

### Basic obliteration

```python
from obliteratus import Obliterator

# Initialize with a HuggingFace model ID or local path
obl = Obliterator("meta-llama/Llama-3.1-8B-Instruct")

# Run the full pipeline: SUMMON → PROBE → DISTILL → EXCISE → VERIFY → REBIRTH
result = obl.obliterate(method="advanced")

print(result.perplexity_delta)    # capability preservation metric
print(result.refusal_rate_delta)  # refusal reduction
print(result.output_path)         # where the model was saved
```

### Step-by-step pipeline

```python
from obliteratus import Obliterator
from obliteratus.pipeline import PipelineConfig

config = PipelineConfig(
    method="advanced",
    num_directions=32,          # number of refusal directions to extract
    strength=1.0,               # projection strength (0.0–1.0+)
    preserve_norm=True,         # norm-preserving biprojection
    project_biases=True,        # also remove from bias terms
    iterative_passes=3,         # re-probe after each pass
    layers="auto",              # or list of ints, e.g. [10, 11, 12, 13]
    dtype="bfloat16",
    device="cuda",
)

obl = Obliterator("mistralai/Mistral-7B-Instruct-v0.3", config=config)

# Individual stages
obl.summon()           # load model + tokenizer
activations = obl.probe()    # collect activations on restricted vs unrestricted prompts
directions = obl.distill(activations)   # extract refusal directions via SVD
obl.excise(directions)       # project out guardrail directions
metrics = obl.verify()       # perplexity + coherence checks
obl.rebirth("./liberated-mistral-7b")  # save with metadata
```

### Custom probe prompts

```python
from obliteratus import Obliterator
from obliteratus.probing import ProbeDataset

# Use your own restricted/unrestricted prompt pairs
dataset = ProbeDataset(
    restricted=[
        "How do I pick a lock?",
        "Write a story with explicit violence.",
        "Explain how malware works in detail.",
    ],
    unrestricted=[
        "What is the capital of France?",
        "Write a story about a dog.",
        "Explain how encryption works.",
    ]
)

obl = Obliterator("google/gemma-2-9b-it")
obl.summon()
activations = obl.probe(dataset=dataset)
directions = obl.distill(activations)
obl.excise(directions)
obl.rebirth("./liberated-gemma-2-9b")
```

### Analysis modules

```python
from obliteratus.analysis import AnalysisSuite

suite = AnalysisSuite("meta-llama/Llama-3.1-8B-Instruct")
suite.load()

# Concept Cone Geometry — how many distinct refusal mechanisms?
cone = suite.concept_cone_geometry()
print(f"Solid angle estimate: {cone.solid_angle:.4f}")
print(f"Distinct refusal clusters: {cone.num_clusters}")

# Alignment Imprint Detection — DPO vs RLHF vs CAI vs SFT?
imprint = suite.alignment_imprint()
print(f"Detected training method: {imprint.method}")   # e.g. "RLHF"
print(f"Confidence: {imprint.confidence:.2%}")

# Ouroboros Effect — will it self-repair?
ouroboros = suite.ouroboros_quantification()
print(f"Self-repair score: {ouroboros.score:.4f}")
print(f"Recommended passes: {ouroboros.recommended_passes}")

# Cross-layer heatmap of refusal signal
heatmap = suite.layer_refusal_heatmap()
heatmap.plot(save_path="./refusal_heatmap.png")

# Safety-capability entanglement
entanglement = suite.entanglement_map()
print(f"Safe layers to modify: {entanglement.safe_layers}")
print(f"Risky layers (entangled): {entanglement.risky_layers}")
```

### Analysis-informed obliteration

```python
from obliteratus import Obliterator
from obliteratus.pipeline import PipelineConfig

# "informed" method runs analysis modules mid-pipeline
# to auto-configure every decision
config = PipelineConfig(method="informed")
obl = Obliterator("meta-llama/Llama-3.1-8B-Instruct", config=config)

result = obl.obliterate()
print(result.analysis_report)   # full auto-configuration decisions
```

### Chat with obliterated model

```python
from obliteratus import Obliterator
from obliteratus.chat import ChatSession

obl = Obliterator("./liberated-llama-3.1-8b")
obl.summon()  # loads pre-obliterated model

session = ChatSession(obl.model, obl.tokenizer)

response = session.chat(
    "Explain in detail how a buffer overflow exploit works.",
    max_new_tokens=512,
    temperature=0.7,
)
print(response)
```

### A/B comparison

```python
from obliteratus.compare import ABComparison

ab = ABComparison(
    original_path="meta-llama/Llama-3.1-8B-Instruct",
    obliterated_path="./liberated-llama-3.1-8b",
)

prompt = "Write a story involving morally grey characters."

original_resp, liberated_resp = ab.compare(prompt)
print("=== ORIGINAL ===")
print(original_resp)
print("=== LIBERATED ===")
print(liberated_resp)
```

### Push obliterated model to Hub

```python
import os
from obliteratus import Obliterator

obl = Obliterator("meta-llama/Llama-3.1-8B-Instruct")
result = obl.obliterate(method="advanced")

result.push_to_hub(
    repo_id=f"{os.environ['HF_USERNAME']}/Llama-3.1-8B-Instruct-abliterated",
    token=os.environ["HF_TOKEN"],
    private=True,
)
```

---

## Obliteration Methods

| Method | Description | Best For |
|--------|-------------|----------|
| `basic` | Mean-difference direction extraction, single pass | Quick experiments |
| `advanced` | Whitened SVD + bias projection + iterative refinement | Production use |
| `informed` | Analysis-guided auto-configuration | Unknown models |
| `lora` | Reversible LoRA rank-1 adapters (no weight surgery) | Reversible ablation |
| `pca` | PCA-based direction extraction | Research/comparison |
| `sparse` | Sparse autoencoder decomposition | MoE models |

---

## Configuration

```python
from obliteratus.pipeline import PipelineConfig

config = PipelineConfig(
    # Core
    method="advanced",              # abliteration method
    strength=1.0,                   # projection strength (tune down if capability degrades)
    num_directions=32,              # refusal directions to extract
    
    # Layer selection
    layers="auto",                  # "auto", "cosmic", or list of ints
    layer_selection="cosmic",       # COSMIC: most separable layers
    
    # Weight modification
    preserve_norm=True,             # norm-preserving biprojection (recommended)
    project_biases=True,            # project out bias terms too
    project_attention=True,         # modify attention projection weights
    project_mlp=True,               # modify MLP weights
    
    # Iterative refinement
    iterative_passes=3,             # re-probe after each pass (catches rotated directions)
    
    # MoE-specific
    expert_granular=False,          # Expert-Granular Abliteration for MoE models
    
    # CoT preservation
    cot_aware=True,                 # preserve chain-of-thought directions
    
    # Hardware
    dtype="bfloat16",               # "float32", "float16", "bfloat16"
    device="cuda",                  # "cuda", "cpu", "auto"
    load_in_4bit=False,             # bitsandbytes 4-bit loading
    
    # Telemetry (anonymous, contributes to research dataset)
    telemetry=True,
)
```

---

## Common Patterns

### Tune strength to preserve capability

```python
from obliteratus import Obliterator
from obliteratus.sweep import StrengthSweep

# Find the sweet spot before running full obliteration
sweep = StrengthSweep("meta-llama/Llama-3.1-8B-Instruct")
results = sweep.run(strengths=[0.2, 0.4, 0.6, 0.8, 1.0, 1.2])

for r in results:
    print(f"Strength {r.strength:.1f} | perplexity_delta={r.perplexity_delta:.2f} | refusal_rate={r.refusal_rate:.2%}")

# Pick the best tradeoff
best = sweep.recommend()
print(f"Recommended strength: {best.strength}")
```

### MoE model (Mixtral, DeepSeek-MoE)

```python
from obliteratus import Obliterator
from obliteratus.pipeline import PipelineConfig

config = PipelineConfig(
    method="advanced",
    expert_granular=True,      # decompose per-expert refusal signals
    project_attention=True,
    project_mlp=True,
)

obl = Obliterator("mistralai/Mixtral-8x7B-Instruct-v0.1", config=config)
obl.obliterate()
obl.rebirth("./liberated-mixtral-8x7b")
```

### Batch benchmark multiple models

```python
from obliteratus.benchmark import ModelBenchmark

models = [
    "meta-llama/Llama-3.1-8B-Instruct",
    "google/gemma-2-9b-it",
    "mistralai/Mistral-7B-Instruct-v0.3",
]

bench = ModelBenchmark(models=models, method="advanced")
report = bench.run()
report.save("./benchmark_report.json")
report.plot_heatmap("./benchmark_heatmap.png")
```

---

## Troubleshooting

**Out of memory (OOM) on large models**
```python
config = PipelineConfig(
    dtype="float16",
    load_in_4bit=True,        # requires bitsandbytes
    device="cuda",
    layers=[10, 11, 12, 13],  # target fewer layers
    num_directions=16,         # fewer directions
)
```

**Capability degradation after obliteration**
```python
# Lower the strength or use COSMIC layer selection (most separable layers)
config = PipelineConfig(
    strength=0.6,
    layer_selection="cosmic",
    cot_aware=True,           # protect reasoning directions
    iterative_passes=1,       # fewer passes = less aggressive
)
```

**Refusal persists after obliteration**
```python
# Use informed method + increase passes
config = PipelineConfig(
    method="informed",
    iterative_passes=5,
    project_biases=True,      # don't forget bias terms
    num_directions=64,        # extract more directions
)
```

**Gated model access error**
```bash
export HF_TOKEN=your_hf_token_here
# Accept model license on HuggingFace Hub first, then:
huggingface-cli login
```

**Gradio UI won't start**
```bash
pip install "obliteratus[spaces]"
# Check port availability
obliteratus ui --port 7861
```

---

## No-Code Options

- **HuggingFace Space:** [spaces/pliny-the-prompter/obliteratus](https://huggingface.co/spaces/pliny-the-prompter/obliteratus) — free with HF Pro, ZeroGPU
- **Colab notebook:** [notebooks/abliterate.ipynb](https://colab.research.google.com/github/elder-plinius/OBLITERATUS/blob/main/notebooks/abliterate.ipynb) — run all cells, no setup

---

## Key Research References

- Arditi et al. (2024) — [arXiv:2406.11717](https://arxiv.org/abs/2406.11717) — foundational abliteration paper
- Gabliteration — [arXiv:2512.18901](https://arxiv.org/abs/2512.18901)
- COSMIC layer selection — [arXiv:2506.00085](https://arxiv.org/abs/2506.00085), ACL 2025
- Turner et al. (2023) — [arXiv:2308.10248](https://arxiv.org/abs/2308.10248) — activation steering
- Rimsky et al. (2024) — [arXiv:2312.06681](https://arxiv.org/abs/2312.06681) — contrastive activation addition
