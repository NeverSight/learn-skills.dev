---
name: dspy-fleet-rlm
description: fleet-rlm-specific DSPy patterns, debugging, and integration with the qredence/fleet-rlm-dspy codebase. Use when working on fleet-rlm DSPy modules, debugging fleet-rlm DSPy issues, or following fleet-rlm architecture conventions.
---

# DSPy fleet-rlm Integration

Patterns, debugging techniques, and integration guidance for using DSPy within the `qredence/fleet-rlm-dspy` codebase.

## Environment Setup

This skill requires **`uv`** as the Python package manager.

```bash
uv venv
source .venv/bin/activate
uv pip install dspy
```

> **Rule**: Never use raw `pip`. Always use `uv pip` for installs and `uv run` for script execution.

## When to Use This Skill

Use this skill when:
- Working on DSPy modules inside the `fleet-rlm` codebase
- Debugging fleet-rlm DSPy issues
- Following fleet-rlm architecture conventions for DSPy
- Integrating new DSPy signatures or programs into fleet-rlm
- Understanding the fleet-rlm DSPy module layout

## fleet-rlm Module Layout

The `qredence/fleet-rlm-dspy` codebase organizes DSPy code as:

```
src/fleet_rlm/
├── signatures.py          # Re-export shim (imports from _prod and _demo)
├── signatures_prod.py     # Production signatures (runtime)
├── signatures_demo.py     # Demo/example signatures
├── core/
│   ├── interpreter.py     # Core reasoning / DSPy program execution
│   ├── llm_tools.py       # LLM tool integration
│   └── config.py          # DSPy configuration
└── ...
```

### Import Conventions

```python
# Production signatures
from fleet_rlm.signatures import AnalyzeLongDocument, CodeChangePlan

# Core interpreter
from fleet_rlm.core.interpreter import ...

# Configuration
from fleet_rlm.core.config import ...
```

## Core Concepts

### Patterns & Debugging
See [patterns.md](references/patterns.md) for:
- fleet-rlm DSPy architecture overview
- Common issues and solutions
- Performance optimization
- Testing strategies

## Examples

The `assets/examples/` directory contains real examples from fleet-rlm:

- **fleet-rlm-signatures.py**: Production signatures from fleet-rlm

## Critical Rules

1. **Always use `uv`**: `uv pip` for installs, `uv run` for scripts
2. **Use absolute imports**: Always use `from fleet_rlm.signatures import ...`
3. **Set require_compiled: true**: Enable in production to fail-fast on missing artifacts
4. **JSON logging is default**: Set `LOG_JSON=0` for human-readable logs during development
5. **Compilation is offline-only**: Never compile at runtime in production
6. **Clear cache after changes**: Run `clear-cache.py` after modifying DSPy modules

## Related Skills

- **[dspy-core](../dspy-core/SKILL.md)**: Signatures, modules, programs, and compilation fundamentals
- **[dspy-optimization](../dspy-optimization/SKILL.md)**: Optimization, metrics, evaluation, and teleprompters

## Progressive Disclosure

1. **SKILL.md** (this file): Quick reference and navigation
2. **references/**: Detailed fleet-rlm patterns and debugging docs
3. **assets/**: Real examples from the fleet-rlm codebase
