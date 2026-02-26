---
name: dspy-development
description: Provides comprehensive guidance for DSPy framework development including signature design, program construction, optimization workflows, and best practices. Use when working with DSPy modules, creating new signatures, optimizing teleprompters, or debugging DSPy code in AgenticFleet.
---

# DSPy Development

This skill provides comprehensive guidance for working with the DSPy framework, especially within the AgenticFleet context.

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

### Optimizing with metrics
```python
# Use the optimize-dspy script for optimization
uv run scripts/optimize-dspy.py --module my_module --metric my_metric --examples examples.jsonl
```

## When to Use This Skill

Use this skill when:
- Creating or modifying DSPy signatures
- Building new DSPy programs or modules
- Running DSPy optimization or compilation
- Debugging DSPy-related issues
- Following AgenticFleet-specific DSPy patterns
- Learning DSPy best practices

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

### Optimization
DSPy optimization improves program performance with teleprompters. See [optimization.md](references/optimization.md) for:
- Teleprompter selection
- Metric definition
- Optimization strategies
- Evaluation and testing

### Patterns & Debugging
AgenticFleet-specific patterns and debugging techniques. See [patterns.md](references/patterns.md) for:
- AgenticFleet DSPy architecture
- Common issues and solutions
- Performance optimization
- Testing strategies

## Scripts

The `scripts/` directory provides reusable tools for DSPy development:

- **compile-dspy.py**: Compile DSPy modules with proper caching
- **optimize-dspy.py**: Run optimization with custom metrics
- **test-signature.py**: Validate signature structure and types
- **clear-cache.py**: Clear DSPy cache safely

See each script's help (`--help`) for usage details.

## Templates

The `assets/templates/` directory provides boilerplate for new DSPy work:

- **signature-template.py**: Starting point for new signatures
- **program-template.py**: Starting point for new programs

## Examples

The `assets/examples/` directory contains real examples from AgenticFleet:

- **agentic-fleet-signatures.py**: Production signatures from AgenticFleet

## Critical Rules for AgenticFleet

1. **Always use `uv`**: Use `uv venv` for environment creation, `uv pip` for installs, and `uv run` for script execution
2. **Compilation is offline-only**: Never compile at runtime in production
3. **Clear cache after changes**: Run `clear-cache.py` after modifying DSPy modules
4. **Use absolute imports**: Always use `from agentic_fleet.dspy_modules import ...`
5. **Set require_compiled: true**: Enable in production to fail-fast on missing artifacts
6. **JSON logging is default**: Set `LOG_JSON=0` for human-readable logs during development

## Progressive Disclosure

This skill uses progressive disclosure to manage context efficiently:

1. **SKILL.md** (this file): Quick reference and navigation
2. **references/**: Detailed technical docs loaded as needed
3. **scripts/**: Executable tools (can be run without reading)
4. **assets/**: Templates and examples for new work

Load reference files only when you need detailed information on a specific topic.
