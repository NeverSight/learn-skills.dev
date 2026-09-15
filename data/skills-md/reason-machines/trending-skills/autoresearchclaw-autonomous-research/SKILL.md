---
name: autoresearchclaw-autonomous-research
description: Fully autonomous research pipeline that turns a topic idea into a complete academic paper with real citations, experiments, and conference-ready LaTeX.
triggers:
  - "research this topic automatically"
  - "generate a paper from an idea"
  - "run autonomous research"
  - "use AutoResearchClaw to write a paper"
  - "chat an idea get a paper"
  - "run the research pipeline"
  - "autonomous paper generation"
  - "set up AutoResearchClaw"
---

# AutoResearchClaw — Autonomous Research Pipeline

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

AutoResearchClaw is a fully autonomous 23-stage research pipeline that takes a natural language topic and produces a complete academic paper: real arXiv/Semantic Scholar citations, sandboxed experiments, statistical analysis, multi-agent peer review, and conference-ready LaTeX (NeurIPS/ICML/ICLR). No hallucinated references. No human babysitting.

---

## Installation

```bash
# Clone and install
git clone https://github.com/aiming-lab/AutoResearchClaw.git
cd AutoResearchClaw
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# Verify CLI is available
researchclaw --help
```

**Requirements:** Python 3.11+

---

## Configuration

```bash
cp config.researchclaw.example.yaml config.arc.yaml
```

### Minimum config (`config.arc.yaml`)

```yaml
project:
  name: "my-research"

research:
  topic: "Your research topic here"

llm:
  provider: "openai"
  base_url: "https://api.openai.com/v1"
  api_key_env: "OPENAI_API_KEY"
  primary_model: "gpt-4o"
  fallback_models: ["gpt-4o-mini"]

experiment:
  mode: "sandbox"
  sandbox:
    python_path: ".venv/bin/python"
```

```bash
export OPENAI_API_KEY="$YOUR_OPENAI_KEY"
```

### OpenRouter config (200+ models)

```yaml
llm:
  provider: "openrouter"
  api_key_env: "OPENROUTER_API_KEY"
  primary_model: "anthropic/claude-3.5-sonnet"
  fallback_models:
    - "google/gemini-pro-1.5"
    - "meta-llama/llama-3.1-70b-instruct"
```

```bash
export OPENROUTER_API_KEY="$YOUR_OPENROUTER_KEY"
```

### ACP (Agent Client Protocol) — no API key needed

```yaml
llm:
  provider: "acp"
  acp:
    agent: "claude"   # or: codex, gemini, opencode, kimi
    cwd: "."
```

The agent CLI (e.g. `claude`) handles its own authentication.

### OpenClaw bridge (optional advanced capabilities)

```yaml
openclaw_bridge:
  use_cron: true              # Scheduled research runs
  use_message: true           # Progress notifications
  use_memory: true            # Cross-session knowledge persistence
  use_sessions_spawn: true    # Parallel sub-sessions
  use_web_fetch: true         # Live web search in literature review
  use_browser: false          # Browser-based paper collection
```

---

## Key CLI Commands

```bash
# Basic run — fully autonomous, no prompts
researchclaw run --topic "Your research idea" --auto-approve

# Run with explicit config file
researchclaw run --config config.arc.yaml --topic "Mixture-of-experts routing efficiency" --auto-approve

# Run with topic defined in config (omit --topic flag)
researchclaw run --config config.arc.yaml --auto-approve

# Interactive mode — pauses at gate stages for approval
researchclaw run --config config.arc.yaml --topic "Your topic"

# Check pipeline status / resume a run
researchclaw status --run-id rc-20260315-120000-abc123

# List past runs
researchclaw list
```

**Gate stages** (5, 9, 20) pause for human approval in interactive mode. Pass `--auto-approve` to skip all gates.

---

## Python API

```python
from researchclaw.pipeline import Runner
from researchclaw.config import load_config

# Load config and run
config = load_config("config.arc.yaml")
config.research.topic = "Efficient attention mechanisms for long-context LLMs"
config.auto_approve = True

runner = Runner(config)
result = runner.run()

# Access outputs
print(result.artifact_dir)          # artifacts/rc-YYYYMMDD-HHMMSS-<hash>/
print(result.deliverables_dir)      # .../deliverables/
print(result.paper_draft_path)      # .../deliverables/paper_draft.md
print(result.latex_path)            # .../deliverables/paper.tex
print(result.bibtex_path)           # .../deliverables/references.bib
print(result.verification_report)  # .../deliverables/verification_report.json
```

```python
# Run specific stages only
from researchclaw.pipeline import Runner, StageRange

runner = Runner(config)
result = runner.run(stages=StageRange(start="LITERATURE_COLLECT", end="KNOWLEDGE_EXTRACT"))
```

```python
# Access knowledge base after a run
from researchclaw.knowledge import KnowledgeBase

kb = KnowledgeBase.load(result.artifact_dir)
findings = kb.get("findings")
literature = kb.get("literature")
decisions = kb.get("decisions")
```

---

## Output Structure

After a run, all outputs land in `artifacts/rc-YYYYMMDD-HHMMSS-<hash>/`:

```
artifacts/rc-20260315-120000-abc123/
├── deliverables/
│   ├── paper_draft.md          # Full academic paper (Markdown)
│   ├── paper.tex               # Conference-ready LaTeX
│   ├── references.bib          # Real BibTeX — auto-pruned to inline citations
│   ├── verification_report.json # 4-layer citation integrity report
│   └── reviews.md              # Multi-agent peer review
├── experiment_runs/
│   ├── run_001/
│   │   ├── code/               # Generated experiment code
│   │   ├── results.json        # Structured metrics
│   │   └── sandbox_output.txt  # Execution logs
├── charts/
│   └── *.png                   # Auto-generated comparison charts
├── evolution/
│   └── lessons.json            # Self-learning lessons for future runs
└── knowledge_base/
    ├── decisions.json
    ├── experiments.json
    ├── findings.json
    ├── literature.json
    ├── questions.json
    └── reviews.json
```

---

## Pipeline Stages Reference

| Phase | Stage # | Name | Notes |
|-------|---------|------|-------|
| A | 1 | TOPIC_INIT | Parse and scope research topic |
| A | 2 | PROBLEM_DECOMPOSE | Break into sub-problems |
| B | 3 | SEARCH_STRATEGY | Build search queries |
| B | 4 | LITERATURE_COLLECT | Real API calls to arXiv + Semantic Scholar |
| B | 5 | LITERATURE_SCREEN | **Gate** — approve/reject literature |
| B | 6 | KNOWLEDGE_EXTRACT | Extract structured knowledge |
| C | 7 | SYNTHESIS | Synthesize findings |
| C | 8 | HYPOTHESIS_GEN | Multi-agent debate to form hypotheses |
| D | 9 | EXPERIMENT_DESIGN | **Gate** — approve/reject design |
| D | 10 | CODE_GENERATION | Generate experiment code |
| D | 11 | RESOURCE_PLANNING | GPU/MPS/CPU auto-detection |
| E | 12 | EXPERIMENT_RUN | Sandboxed execution |
| E | 13 | ITERATIVE_REFINE | Self-healing on failure |
| F | 14 | RESULT_ANALYSIS | Multi-agent analysis |
| F | 15 | RESEARCH_DECISION | PROCEED / REFINE / PIVOT |
| G | 16 | PAPER_OUTLINE | Structure paper |
| G | 17 | PAPER_DRAFT | Write full paper |
| G | 18 | PEER_REVIEW | Evidence-consistency check |
| G | 19 | PAPER_REVISION | Incorporate review feedback |
| H | 20 | QUALITY_GATE | **Gate** — final approval |
| H | 21 | KNOWLEDGE_ARCHIVE | Save lessons to KB |
| H | 22 | EXPORT_PUBLISH | Emit LaTeX + BibTeX |
| H | 23 | CITATION_VERIFY | 4-layer anti-hallucination check |

---

## Common Patterns

### Pattern: Quick paper on a topic

```bash
export OPENAI_API_KEY="$OPENAI_API_KEY"
researchclaw run \
  --topic "Self-supervised learning for protein structure prediction" \
  --auto-approve
```

### Pattern: Reproducible run with full config

```yaml
# config.arc.yaml
project:
  name: "protein-ssl-research"

research:
  topic: "Self-supervised learning for protein structure prediction"

llm:
  provider: "openai"
  api_key_env: "OPENAI_API_KEY"
  primary_model: "gpt-4o"
  fallback_models: ["gpt-4o-mini"]

experiment:
  mode: "sandbox"
  sandbox:
    python_path: ".venv/bin/python"
  max_iterations: 3
  timeout_seconds: 300
```

```bash
researchclaw run --config config.arc.yaml --auto-approve
```

### Pattern: Use Claude via OpenRouter for best reasoning

```bash
export OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

cat > config.arc.yaml << 'EOF'
project:
  name: "my-research"
llm:
  provider: "openrouter"
  api_key_env: "OPENROUTER_API_KEY"
  primary_model: "anthropic/claude-3.5-sonnet"
  fallback_models: ["google/gemini-pro-1.5"]
experiment:
  mode: "sandbox"
  sandbox:
    python_path: ".venv/bin/python"
EOF

researchclaw run --config config.arc.yaml \
  --topic "Efficient KV cache compression for transformer inference" \
  --auto-approve
```

### Pattern: Resume after a failed run

```bash
# List runs to find the run ID
researchclaw list

# Resume from last completed stage
researchclaw run --resume rc-20260315-120000-abc123
```

### Pattern: Programmatic batch research

```python
import asyncio
from researchclaw.pipeline import Runner
from researchclaw.config import load_config

topics = [
    "LoRA fine-tuning on limited hardware",
    "Speculative decoding for LLM inference",
    "Flash attention variants comparison",
]

config = load_config("config.arc.yaml")
config.auto_approve = True

for topic in topics:
    config.research.topic = topic
    runner = Runner(config)
    result = runner.run()
    print(f"[{topic}] → {result.deliverables_dir}")
```

### Pattern: OpenClaw one-liner (if using OpenClaw agent)

```
Share the repo URL with OpenClaw, then say:
"Research mixture-of-experts routing efficiency"
```

OpenClaw auto-reads `RESEARCHCLAW_AGENTS.md`, clones, installs, configures, and runs the full pipeline.

---

## Compile the LaTeX Output

```bash
# Navigate to deliverables
cd artifacts/rc-*/deliverables/

# Compile (requires a LaTeX distribution)
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Or upload paper.tex + references.bib directly to Overleaf
```

---

## Troubleshooting

### `researchclaw: command not found`
```bash
# Make sure the venv is active and package is installed
source .venv/bin/activate
pip install -e .
which researchclaw
```

### API key errors
```bash
# Verify env var is set
echo $OPENAI_API_KEY
# Should print your key (not empty)

# Set it explicitly for the session
export OPENAI_API_KEY="sk-..."
```

### Experiment sandbox failures
The pipeline self-heals at Stage 13 (ITERATIVE_REFINE). If it keeps failing:
```yaml
# Increase timeout and iterations in config
experiment:
  max_iterations: 5
  timeout_seconds: 600
  sandbox:
    python_path: ".venv/bin/python"
```

### Citation hallucination warnings
Stage 23 (CITATION_VERIFY) runs a 4-layer check. If references are pruned:
- This is **expected behaviour** — fake citations are removed automatically
- Check `verification_report.json` for details on which citations were rejected and why

### PIVOT loop running indefinitely
Stage 15 (RESEARCH_DECISION) may pivot multiple times. To cap iterations:
```yaml
research:
  max_pivots: 2
  max_refines: 3
```

### LaTeX compilation errors
```bash
# Check for missing packages
pdflatex paper.tex 2>&1 | grep "File.*not found"

# Install missing packages (TeX Live)
tlmgr install <package-name>
```

### Out of memory during experiments
```yaml
# Force CPU mode in config
experiment:
  sandbox:
    device: "cpu"
    max_memory_gb: 4
```

---

## Key Concepts

- **PIVOT/REFINE Loop**: Stage 15 autonomously decides PROCEED, REFINE (tweak params), or PIVOT (new hypothesis direction). All artifacts are versioned.
- **Multi-Agent Debate**: Stages 8, 14, 18 use structured multi-perspective debate — not a single LLM pass.
- **Self-Learning**: Each run extracts lessons with 30-day time decay. Future runs on similar topics benefit from past mistakes.
- **Sentinel Watchdog**: Background monitor detects NaN/Inf in results, checks paper-evidence consistency, scores citation relevance, and guards against fabrication throughout the run.
- **4-Layer Citation Verification**: arXiv lookup → CrossRef lookup → DataCite lookup → LLM relevance scoring. A citation must pass all layers to survive.
