---
name: meta-harness-optimization
description: Framework for automated search over task-specific model harnesses — the code around a fixed base model that decides what to store, retrieve, and show while the model works.
triggers:
  - set up meta-harness for my project
  - optimize model harness automatically
  - apply meta-harness to a new domain
  - run meta-harness text classification experiment
  - harness evolution for LLM agents
  - terminal bench harness optimization
  - how do I use meta-harness framework
  - scaffold evolution for AI agents
---

# Meta-Harness Optimization

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Meta-Harness is a framework for automated end-to-end search over **model harnesses** — the scaffolding code around a fixed base model that controls what the model stores, retrieves, and sees while working on a task. Rather than hand-crafting prompts and memory systems, Meta-Harness proposes, evaluates, and evolves harness implementations automatically.

**Paper**: [Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052)  
**Homepage**: https://yoonholee.com/meta-harness/

## Core Concepts

| Term | Meaning |
|------|---------|
| **Harness** | All code around the base model: memory, retrieval, prompt construction, tool use |
| **Proposer Agent** | LLM (e.g. Claude Code) that proposes new harness variants |
| **Evaluator** | Runs proposed harnesses on a benchmark, returns a score |
| **Meta-Loop** | Iterative propose → evaluate → feedback cycle |

## Installation

Meta-Harness uses `uv` for dependency management. Each reference experiment is self-contained:

```bash
# Text classification experiment
cd reference_examples/text_classification
uv sync

# Terminal-Bench 2 experiment
cd reference_examples/terminal_bench_2
uv sync
```

No global pip install is needed. All dependencies are managed per-experiment via `pyproject.toml`.

## Quick Start

### Text Classification (Memory System Search)

```bash
cd reference_examples/text_classification

# Run 1 iteration of meta-harness optimization
uv run python meta_harness.py --iterations 1

# Run more iterations for better optimization
uv run python meta_harness.py --iterations 10
```

### Terminal-Bench 2 (Scaffold Evolution)

```bash
cd reference_examples/terminal_bench_2

# Smoke test with a single task
uv run bash scripts/run_eval.sh agents.baseline_kira:AgentHarness full 1 1 -i extract-elf

# General eval format:
# run_eval.sh <agent_module:AgentClass> <split> <num_tasks> <num_workers> [flags]
```

## Applying Meta-Harness to a New Domain

The recommended workflow uses the onboarding document with your AI coding assistant:

```bash
# 1. Open ONBOARDING.md in your coding assistant (Claude Code, Cursor, etc.)
# and have a conversation about your domain. This produces domain_spec.md.

# 2. domain_spec.md will contain:
#   - What the harness controls in your domain
#   - How to evaluate harness quality (benchmark / metric)
#   - What the proposer agent should modify
#   - Constraints and budget considerations
```

### Minimum Required Components for a New Domain

```
my_domain/
├── pyproject.toml          # uv-managed dependencies
├── domain_spec.md          # generated via ONBOARDING.md conversation
├── meta_harness.py         # main optimization loop
├── harness.py              # base harness implementation
├── evaluator.py            # benchmark runner → numeric score
└── claude_wrapper.py       # proposer agent wrapper
```

## Implementing a Harness

A harness wraps a base model and manages context/memory/tools:

```python
# harness.py — minimal harness structure
from dataclasses import dataclass, field
from typing import Any

@dataclass
class HarnessConfig:
    model: str = "claude-3-5-sonnet-20241022"
    memory_strategy: str = "last_k"
    k: int = 5
    retrieval_enabled: bool = False
    system_prompt: str = "You are a helpful assistant."

class AgentHarness:
    def __init__(self, config: HarnessConfig):
        self.config = config
        self.memory: list[dict] = []

    def reset(self):
        self.memory = []

    def _build_context(self, new_input: str) -> list[dict]:
        """Core harness logic: what does the model see?"""
        if self.config.memory_strategy == "last_k":
            recent = self.memory[-self.config.k:]
        elif self.config.memory_strategy == "all":
            recent = self.memory[:]
        else:
            recent = []
        
        return recent + [{"role": "user", "content": new_input}]

    def step(self, user_input: str) -> str:
        messages = self._build_context(user_input)
        # Call base model with constructed context
        response = call_model(
            model=self.config.model,
            system=self.config.system_prompt,
            messages=messages
        )
        # Update memory
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": response})
        return response
```

## Implementing the Evaluator

```python
# evaluator.py — runs harness on benchmark, returns score
from harness import AgentHarness, HarnessConfig

def evaluate_harness(config: HarnessConfig, dataset: list[dict]) -> float:
    """
    Evaluate a harness configuration on a dataset.
    Returns a scalar score (higher is better).
    """
    harness = AgentHarness(config)
    correct = 0
    
    for example in dataset:
        harness.reset()
        prediction = harness.step(example["input"])
        if grade(prediction, example["label"]):
            correct += 1
    
    return correct / len(dataset)

def grade(prediction: str, label: str) -> bool:
    """Task-specific grading logic."""
    return label.lower().strip() in prediction.lower()
```

## The Meta-Harness Loop

```python
# meta_harness.py — the optimization loop
import json
from pathlib import Path
from evaluator import evaluate_harness
from claude_wrapper import run_proposer

def meta_harness_loop(
    iterations: int = 10,
    train_dataset: list = None,
    val_dataset: list = None,
):
    history: list[dict] = []
    best_score = 0.0
    best_config = None

    for i in range(iterations):
        print(f"\n=== Iteration {i+1}/{iterations} ===")

        # 1. Propose: ask the proposer agent for a new harness variant
        proposal = run_proposer(
            history=history,
            task_description="Optimize the memory system for text classification.",
            code_context=Path("harness.py").read_text(),
        )

        # 2. Evaluate: run the proposed harness
        try:
            new_config = parse_proposal(proposal)
            score = evaluate_harness(new_config, train_dataset)
        except Exception as e:
            score = 0.0
            print(f"Evaluation failed: {e}")

        # 3. Record: log result for proposer feedback
        record = {
            "iteration": i + 1,
            "proposal": proposal,
            "score": score,
        }
        history.append(record)
        print(f"Score: {score:.4f}")

        if score > best_score:
            best_score = score
            best_config = new_config
            print(f"New best: {best_score:.4f}")

    # Final validation on held-out set
    if best_config and val_dataset:
        val_score = evaluate_harness(best_config, val_dataset)
        print(f"\nFinal val score: {val_score:.4f}")

    return best_config, history
```

## Proposer Agent Wrapper (Claude Code)

The shipped examples use Claude Code as the proposer. Adapt `claude_wrapper.py`:

```python
# claude_wrapper.py — wraps proposer agent calls
import subprocess
import json
from pathlib import Path

def run_proposer(
    history: list[dict],
    task_description: str,
    code_context: str,
) -> str:
    """
    Call Claude Code (or another proposer) to suggest harness modifications.
    Logs all interactions for reproducibility.
    """
    prompt = build_proposer_prompt(history, task_description, code_context)
    
    # Example: call Claude via API
    import anthropic
    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    
    result = response.content[0].text
    
    # Log for reproducibility
    log_entry = {"prompt": prompt, "response": result}
    with open("proposer_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return result

def build_proposer_prompt(
    history: list[dict],
    task_description: str,
    code_context: str,
) -> str:
    history_str = "\n".join(
        f"Iteration {h['iteration']}: score={h['score']:.4f}\nProposal:\n{h['proposal']}"
        for h in history[-5:]  # last 5 for context window
    )
    return f"""You are optimizing a model harness for: {task_description}

Current harness code:
```python
{code_context}
```

Optimization history (recent):
{history_str if history_str else "No history yet — this is the first iteration."}

Propose a modified HarnessConfig or changes to the harness code that may improve performance.
Output your proposal as a JSON config dict, followed by any code changes.
"""
```

## Environment Variables

```bash
# Required for Claude-based proposer
export ANTHROPIC_API_KEY=your_key_here

# Optional: control model used
export PROPOSER_MODEL=claude-opus-4-5
export EVALUATOR_MODEL=claude-3-5-sonnet-20241022
```

## Reference Experiment Structure

### Text Classification (`reference_examples/text_classification/`)

Searches over memory system configurations for a classification task:
- Proposer modifies memory strategy, retrieval settings, prompt templates
- Evaluator scores on held-out classification benchmark
- Optimized config is saved for reuse

```bash
uv run python meta_harness.py --iterations 20 --dataset ag_news
```

### Terminal-Bench 2 (`reference_examples/terminal_bench_2/`)

Evolves agent scaffolding for computer-use / terminal tasks:

```bash
# Run baseline agent on a specific task
uv run bash scripts/run_eval.sh agents.baseline_kira:AgentHarness full 1 1 -i extract-elf

# Arguments: <module:Class> <split> <num_tasks> <num_workers> [task_filter]
# Optimized artifact: stanford-iris-lab/meta-harness-tbench2-artifact
```

## Common Patterns

### Saving and Loading Optimized Configs

```python
import json
from dataclasses import asdict

# Save
with open("best_config.json", "w") as f:
    json.dump(asdict(best_config), f, indent=2)

# Load
with open("best_config.json") as f:
    data = json.load(f)
config = HarnessConfig(**data)
```

### Adding Early Stopping

```python
PATIENCE = 3
no_improve = 0

for i in range(iterations):
    score = evaluate_harness(config, dataset)
    if score > best_score + 1e-4:
        best_score = score
        no_improve = 0
    else:
        no_improve += 1
    if no_improve >= PATIENCE:
        print(f"Early stop at iteration {i+1}")
        break
```

### Parallel Evaluation

```python
from concurrent.futures import ProcessPoolExecutor

def batch_evaluate(configs, dataset, num_workers=4):
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(evaluate_harness, c, dataset) for c in configs]
        return [f.result() for f in futures]
```

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `uv sync` fails | Missing Python version | Install Python 3.11+ via `pyenv` |
| Proposer returns unparseable JSON | Prompt too vague | Add explicit JSON schema to proposer prompt |
| Scores don't improve | Too few iterations or search space too large | Increase `--iterations`, narrow config space |
| API rate limits | Too many evaluator calls | Add `time.sleep()` or batch requests |
| Claude Code not found | CLI not installed | `npm install -g @anthropic-ai/claude-code` |

## Citation

```bibtex
@misc{lee2026metaharnessendtoendoptimizationmodel,
      title={Meta-Harness: End-to-End Optimization of Model Harnesses},
      author={Yoonho Lee and Roshen Nair and Qizheng Zhang and Kangwook Lee and Omar Khattab and Chelsea Finn},
      year={2026},
      eprint={2603.28052},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2603.28052},
}
```
