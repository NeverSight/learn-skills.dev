---
name: dspy-core
description: Core DSPy framework guidance — signatures, modules, programs, compilation, and testing. Use when creating DSPy signatures, building modules, compiling programs, or learning DSPy fundamentals.
---

# DSPy Core

Core guidance for working with the DSPy framework: signatures, modules, programs, compilation, and testing.

## Environment Setup

This skill requires **`uv`** as the Python package manager. Always ensure a `uv` virtual environment is active before running any DSPy code.

```bash
# Create and activate a uv virtual environment
uv venv
source .venv/bin/activate

# Install dspy
uv pip install dspy
```

> **Rule**: Never use raw `pip` or `python -m pip`. Always use `uv pip` for package installation and `uv run` for script execution.

## Quick Start

### Creating a new signature
```python
import dspy

class MySignature(dspy.Signature):
    """Input and output fields with descriptions."""
    input_field = dspy.InputField(desc="Description of input")
    output_field = dspy.OutputField(desc="Description of output")
```

### Compiling a program
```python
# Use the compile-dspy script for safe compilation
uv run scripts/compile-dspy.py --module my_module --teleprompter teleprompter_name
```

## When to Use This Skill

Use this skill when:
- Creating or modifying DSPy signatures
- Building new DSPy programs or modules
- Running DSPy compilation
- Testing DSPy signatures and programs
- Learning DSPy fundamentals

## Core Concepts

### Signatures
DSPy signatures define the input/output contract for your programs. See [signatures.md](references/signatures.md) for:
- Signature design patterns
- InputField vs OutputField usage
- Type hints and validation
- Hint and description best practices

### Programs & Modules
DSPy programs are composed of modules that process inputs. See [programs.md](references/programs.md) for:
- Building DSPy programs
- Module composition
- Compilation workflows
- Chain-of-thought and other patterns

## Scripts

- **compile-dspy.py**: Compile DSPy modules with proper caching
- **test-signature.py**: Validate signature structure and types
- **clear-cache.py**: Clear DSPy cache safely

## Templates

The `assets/templates/` directory provides boilerplate:

- **signature-template.py**: Starting point for new signatures
- **program-template.py**: Starting point for new programs

## Critical Rules

1. **Always use `uv`**: Use `uv venv` for environment creation, `uv pip` for installs, and `uv run` for script execution
2. **Compilation is offline-only**: Never compile at runtime in production
3. **Clear cache after changes**: Run `clear-cache.py` after modifying DSPy modules

## Related Skills

- **[dspy-optimization](../dspy-optimization/SKILL.md)**: Optimization, metrics, evaluation, and teleprompters
- **[dspy-fleet-rlm](../dspy-fleet-rlm/SKILL.md)**: fleet-rlm-specific DSPy patterns, debugging, and integration

## Progressive Disclosure

1. **SKILL.md** (this file): Quick reference and navigation
2. **references/**: Detailed technical docs loaded as needed
3. **scripts/**: Executable tools (can be run without reading)
4. **assets/**: Templates for new work
