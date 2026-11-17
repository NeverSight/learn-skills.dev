---
name: langgraph-testing-evaluation
description: "Use this skill when you need to test or evaluate LangGraph/LangChain agents: writing unit or integration tests, generating test scaffolds, mocking LLM/tool behavior, running trajectory evaluation (match or LLM-as-judge), running LangSmith dataset evaluations, and comparing two agent versions with A/B-style offline analysis. Use it for Python and JavaScript/TypeScript workflows, evaluator design, experiment setup, regression gates, and debugging flaky/incorrect evaluation results."
---

# LangGraph Testing & Evaluation

Practical workflows for validating agent quality with:
- Unit/integration tests
- Trajectory evaluation
- LangSmith dataset evaluations
- A/B-style comparisons between versions

Use this file for high-level flow. Load `references/*` for detailed implementation.

## Start Here

Choose the smallest approach that answers your question:

| Goal | Primary method | Load first |
| --- | --- | --- |
| Validate node logic quickly | Unit tests with mocks | `references/unit-testing-patterns.md` |
| Validate multi-step agent behavior | Trajectory evaluation | `references/trajectory-evaluation.md` |
| Track quality over datasets over time | LangSmith evaluation | `references/langsmith-evaluation.md` |
| Compare old vs new agent versions | A/B comparison | `references/ab-testing.md` |

Recommended order:
1. Unit tests
2. Integration/trajectory checks
3. Dataset evaluation in LangSmith
4. A/B comparison before deployment

## Quick Commands

Run from repo root.

### Generate test scaffolding

```bash
# Python (preferred)
uv run skills/langgraph-testing-evaluation/scripts/generate_test_cases.py my_agent:graph --output tests/ --framework pytest

# JavaScript/TypeScript
node skills/langgraph-testing-evaluation/scripts/generate_test_cases.js ./my-agent.ts:graph --output tests/ --framework vitest
```

### Run trajectory evaluation

```bash
# Python: LLM-as-judge
uv run skills/langgraph-testing-evaluation/scripts/run_trajectory_eval.py my_agent:run_agent my_dataset --method llm-judge --model openai:o3-mini

# Python: trajectory match
uv run skills/langgraph-testing-evaluation/scripts/run_trajectory_eval.py my_agent:run_agent dataset.json --method match --trajectory-match-mode strict --reference-trajectory reference.json

# JavaScript/TypeScript
node skills/langgraph-testing-evaluation/scripts/run_trajectory_eval.js ./agent.ts:runAgent my_dataset --method llm-judge --model openai:o3-mini --max-concurrency 4
```

### Run LangSmith dataset evaluation

```bash
# Python
uv run skills/langgraph-testing-evaluation/scripts/evaluate_with_langsmith.py my_agent:run_agent my_dataset --evaluators accuracy,latency --max-concurrency 4

# Python (do not upload experiment results)
uv run skills/langgraph-testing-evaluation/scripts/evaluate_with_langsmith.py my_agent:run_agent my_dataset --evaluators accuracy --no-upload

# JavaScript/TypeScript
node skills/langgraph-testing-evaluation/scripts/evaluate_with_langsmith.js ./agent.ts:runAgent my_dataset --evaluators accuracy,latency --max-concurrency 4
```

### Compare two agent versions

```bash
# Python
uv run skills/langgraph-testing-evaluation/scripts/compare_agents.py my_agent:v1 my_agent:v2 dataset.json --output comparison_report.json

# JavaScript/TypeScript
node skills/langgraph-testing-evaluation/scripts/compare_agents.js ./v1.ts:run ./v2.ts:run dataset.json --output comparison_report.json

# JavaScript/TypeScript (force local dataset file only)
node skills/langgraph-testing-evaluation/scripts/compare_agents.js ./v1.ts:run ./v2.ts:run dataset.json --no-langsmith
```

### Create mock response configs

```bash
# Python
uv run skills/langgraph-testing-evaluation/scripts/mock_llm_responses.py create --type sequence --output mock_config.json

# JavaScript/TypeScript
node skills/langgraph-testing-evaluation/scripts/mock_llm_responses.js create --type sequence --output mock_config.json
```

## Core Workflow

1. Define test scope.
- Unit: deterministic logic in one node/function.
- Integration: node interactions and routing.
- End-to-end: complete response quality on realistic inputs.

2. Start from deterministic checks.
- Mock LLM/tool IO for speed and repeatability.
- Keep real-model tests as a smaller, explicit suite.

3. Build/curate dataset examples.
- Use stable inputs and expected outputs.
- Keep schema simple: `inputs` and `outputs` objects (optional `metadata`).
- Compatibility note: scripts also accept singular keys (`input`, `output`) for legacy datasets.

4. Run evaluation with explicit gates.
- Use evaluator keys that map to deployment decisions.
- Set thresholds in CI for regression prevention.

5. Compare versions before rollout.
- Run same dataset on both versions.
- Check both quality and latency.

6. Diagnose failures from traces/experiments.
- Inspect low-scoring examples.
- Split failures by pattern (routing, tool usage, hallucination, latency spikes).

## Current References (Load On Demand)

### `references/unit-testing-patterns.md`
Load when:
- You need node-level and routing test patterns.
- You need pytest/vitest/Jest integration patterns.
- You need robust mocking and flaky-test reduction.

### `references/trajectory-evaluation.md`
Load when:
- You need trajectory match evaluation (`strict`, `unordered`, `subset`, `superset`).
- You need LLM-as-judge trajectory scoring.
- You need LangSmith experiment comparison for trajectory results.

### `references/langsmith-evaluation.md`
Load when:
- You need dataset creation/management in LangSmith.
- You need evaluator signatures and experiment runs in Python/TS.
- You need CI-friendly workflows with quality thresholds.

### `references/ab-testing.md`
Load when:
- You need offline A/B comparison methodology.
- You need significance testing and interpretation.
- You need production traffic split strategy and guardrails.

## Assets

### `assets/templates/test_template.py`
- Runnable Python pytest template aligned with current LangGraph testing patterns.
- Includes:
  - Compiled-graph invocation with `thread_id`
  - Single-node testing via `compiled_graph.nodes[...]`
  - Integration-test placeholder

### `assets/datasets/sample_dataset.json`
- Deterministic seed dataset for LangSmith ingestion.
- Uses `examples: [{ inputs, outputs, metadata }]` format.

### `assets/examples/README.md`
- Documentation-only index for current asset usage.
- Notes where runnable assets live today.

## Script Interface Summary

### `scripts/generate_test_cases.py` / `.js`
Use for fast test scaffolding.

Inputs:
- Graph module path
  - Python: `my_module:graph` or `my_module.graph`
  - JS/TS: `./file.ts:graph`

Outputs:
- Framework-specific starter tests in target directory.

### `scripts/run_trajectory_eval.py` / `.js`
Use for trajectory scoring with either:
- `--method match`
- `--method llm-judge`

Supports:
- Local dataset files (`.json`)
- LangSmith dataset names
- Optional reference trajectory file with `--reference-trajectory`
- Match modes: `strict`, `unordered`, `subset`, `superset`

Local-only mode:
- `--no-langsmith` in both Python and JavaScript scripts (requires local JSON dataset file)

### `scripts/evaluate_with_langsmith.py` / `.js`
Use for dataset-based evaluation runs and experiment tracking.

Supports:
- Existing dataset by name
- Dataset creation from JSON examples file
- Multiple evaluators (`--evaluators accuracy,latency,...`)
- Concurrency control (`--max-concurrency`)

Python-only:
- `--no-upload` to run without uploading experiment results

### `scripts/compare_agents.py` / `.js`
Use for offline version comparisons:
- Shared dataset input
- Success/latency summaries
- JSON report output for CI artifacts
- Local JSON datasets or LangSmith datasets (JS supports `--no-langsmith` to disable remote loading)

### `scripts/mock_llm_responses.py` / `.js`
Use for deterministic test doubles:
- single
- sequence
- conditional

## Decision Rules

If behavior is deterministic and local:
- Use unit tests first.

If behavior depends on tool sequence/routing:
- Add trajectory evaluation.

If behavior depends on realistic distribution quality:
- Run LangSmith dataset evaluation.

If approving a replacement model/prompt/graph:
- Run A/B comparison and check both quality and latency.

## Common Failure Patterns

### Flaky tests
- Cause: real-model nondeterminism in unit scope.
- Fix: mock LLM/tool calls for unit tests; reserve real-model tests for separate integration marks.

### High trajectory variance
- Cause: overly strict matching for workflows with equivalent paths.
- Fix: switch match mode (`unordered`, `subset`, or `superset`) where appropriate.

### Regressions hidden by averages
- Cause: only aggregate score monitored.
- Fix: inspect per-example failures and segment by category metadata.

### Latency regressions with same quality
- Cause: no explicit latency gate.
- Fix: include latency evaluator and CI threshold.

## Minimal Best Practices

1. Keep fast deterministic tests as the largest share.
2. Version datasets and keep them stable.
3. Track both correctness and latency.
4. Add explicit go/no-go thresholds in CI.
5. Compare candidate vs baseline before production rollout.
6. Investigate failures with trace-level evidence, not only aggregate scores.
