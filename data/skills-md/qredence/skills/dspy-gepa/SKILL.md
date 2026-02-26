---
name: dspy-gepa
description: >-
  Evaluates and optimizes agent skills using a DSPy-powered GEPA
  (Generate/Evaluate/Propose/Apply) loop. Loads scenario YAML files as
  DSPy datasets, scores outputs with pattern-matching metrics, and
  optimizes prompts via BootstrapFewShot or MIPROv2 teleprompters.
  Also generates new scenario YAML files from skill descriptions.
---

# DSPy GEPA — Generate, Evaluate, Propose, Apply

GEPA is a DSPy-powered tool for evaluating, optimizing, and **generating** skill scenarios.

## Quick Start

Requires Python 3.10+ with `dspy`, `pyyaml`, and `jsonschema`:

```bash
pip install dspy-ai pyyaml jsonschema
```

### Generate New Scenarios

Point GEPA at an existing skill to generate new test scenarios:

```bash
python scripts/gepa.py generate \
  --skill-description "Creates FastAPI routers with CRUD endpoints" \
  --skill-name fastapi-router-py \
  --num-scenarios 5 \
  --output tests/scenarios/fastapi-router-py/generated.yaml
```

Or expand an existing scenario file with more variations:

```bash
python scripts/gepa.py generate \
  --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \
  --num-scenarios 3 \
  --output new-scenarios.yaml
```

### Evaluate Scenarios

Score a DSPy program against scenario patterns:

```bash
python scripts/gepa_evaluate.py \
  --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml
```

### Full GEPA Loop

Evaluate baseline → optimize → evaluate optimized → save:

```bash
python scripts/gepa.py optimize \
  --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \
  --output optimized_program.json
```

### Convert Scenarios to Dataset

```bash
python scripts/scenario_to_dataset.py \
  --scenarios tests/scenarios/fastapi-router-py/scenarios.yaml \
  --output dataset.json
```

## Architecture

See `references/gepa-architecture.md` for the full GEPA loop design and DSPy mapping.

## Metrics

See `references/metrics.md` for pattern-matching scoring details.

## Example Output

See `examples/sample-run.md` for a complete CLI session with output.
