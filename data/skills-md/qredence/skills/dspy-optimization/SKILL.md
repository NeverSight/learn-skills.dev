---
name: dspy-optimization
description: DSPy optimization workflows — teleprompters, metrics, evaluation, and compilation strategies. Use when optimizing DSPy programs with BootstrapFewShot, MIPROv2, or custom metrics.
---

# DSPy Optimization

Guidance for optimizing DSPy programs: teleprompter selection, metric definition, evaluation workflows, and save/load patterns.

## Environment Setup

This skill requires **`uv`** as the Python package manager.

```bash
uv venv
source .venv/bin/activate
uv pip install dspy
```

> **Rule**: Never use raw `pip`. Always use `uv pip` for installs and `uv run` for script execution.

## Quick Start

### Optimizing with metrics
```python
# Use the optimize-dspy script
uv run scripts/optimize-dspy.py --module my_module --metric my_metric --examples examples.jsonl
```

### BootstrapFewShot
```python
from dspy.teleprompt import BootstrapFewShot

optimizer = BootstrapFewShot(metric=my_metric, max_bootstrapped_demos=4)
compiled = optimizer.compile(program, trainset=trainset)
compiled.save("./compiled/program.json")
```

## When to Use This Skill

Use this skill when:
- Running DSPy optimization or compilation with teleprompters
- Defining custom metrics for DSPy evaluation
- Evaluating DSPy programs with dev sets
- Choosing between BootstrapFewShot, MIPROv2, or other optimizers
- Saving and loading compiled programs

## Core Concepts

### Optimization Reference
See [optimization.md](references/optimization.md) for:
- Teleprompter selection guide (BootstrapFewShot, MIPROv2, etc.)
- Metric definition patterns
- Optimization strategies and hyperparameters
- Evaluation and testing workflows
- Save/load best practices (`.save()` / `.load()`, never raw pickle)

## Scripts

- **optimize-dspy.py**: Run optimization with custom metrics and teleprompters

## Critical Rules

1. **Always use `uv`**: `uv pip` for installs, `uv run` for scripts
2. **Use `.save()` / `.load()`**: Never use raw `pickle` for DSPy programs
3. **Use `dspy.LM`**: Never use deprecated `dspy.OpenAI` or `dspy.settings.configure`
4. **Mark inputs on examples**: Always call `.with_inputs()` on `dspy.Example`

## Related Skills

- **[dspy-core](../dspy-core/SKILL.md)**: Signatures, modules, programs, and compilation fundamentals
- **[dspy-fleet-rlm](../dspy-fleet-rlm/SKILL.md)**: fleet-rlm-specific DSPy patterns and integration

## Progressive Disclosure

1. **SKILL.md** (this file): Quick reference and navigation
2. **references/**: Detailed optimization docs loaded as needed
3. **scripts/**: Executable optimization tools
