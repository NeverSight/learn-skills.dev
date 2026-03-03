---
name: self-improving-agent-builder
version: 1.1.0
description: |
  Encodes a continuous improvement loop for goal-seeking agents: EVAL, ANALYZE,
  RESEARCH (hypothesis + evidence + counter-arguments), IMPROVE, RE-EVAL, DECIDE.
  Auto-commits improvements (+2% net, no regression >5%) and reverts failures.
  Works with all 4 SDK implementations.
  Auto-activates on "improve agent", "self-improving loop", "agent eval loop",
  "benchmark agents", "run improvement cycle".
source_urls:
  - https://github.com/rysweet/amplihack
---

# Self-Improving Agent Builder

## Purpose

Run a closed-loop improvement cycle on any goal-seeking agent implementation:

```
EVAL -> ANALYZE -> RESEARCH -> IMPROVE -> RE-EVAL -> DECIDE -> (repeat)
```

Each iteration measures L1-L12 progressive test scores, identifies failures
with `error_analyzer.py`, runs a research step with hypothesis/evidence/
counter-arguments, applies targeted fixes, and gates promotion through
regression checks.

## When I Activate

- "improve agent" or "self-improving loop"
- "agent eval loop" or "run improvement cycle"
- "benchmark agents" or "compare SDK implementations"
- "iterate on agent scores" or "fix agent regressions"

## Quick Start

```
User: "Run the self-improving loop on the mini-framework agent for 3 iterations"

Skill: Executes 3 iterations of EVAL->ANALYZE->RESEARCH->IMPROVE->RE-EVAL->DECIDE
       Reports per-iteration scores, net improvement, and commits/reverts.
```

## Runner Script

The self-improvement loop is implemented as a Python CLI:

```bash
# Basic usage
python -m amplihack.eval.self_improve.runner --sdk mini --iterations 3

# Full options
python -m amplihack.eval.self_improve.runner \
  --sdk mini \
  --iterations 5 \
  --improvement-threshold 2.0 \
  --regression-tolerance 5.0 \
  --levels L1 L2 L3 L4 L5 L6 \
  --output-dir ./eval_results/self_improve \
  --dry-run  # evaluate only, don't apply changes
```

**Source:** `src/amplihack/eval/self_improve/runner.py`

## The Loop (6 Phases per Iteration)

### Phase 1: EVAL

Run the L1-L12 progressive test suite on the current agent implementation.

**Execution:**

```bash
python -m amplihack.eval.progressive_test_suite \
  --agent-name <agent_name> \
  --output-dir <output_dir>/iteration_N/eval \
  --levels L1 L2 L3 L4 L5 L6
```

**Output:** Per-level scores and overall baseline.

### Phase 2: ANALYZE

Classify failures using `error_analyzer.py`. Maps each failed question to a
failure taxonomy (retrieval_insufficient, temporal_ordering_wrong, etc.) and
the specific code component responsible.

```python
from amplihack.eval.self_improve import analyze_eval_results

analyses = analyze_eval_results(level_results, score_threshold=0.6)
# Each ErrorAnalysis maps to:
#   failure_mode -> affected_component -> prompt_template
```

### Phase 3: RESEARCH (New)

The critical thinking step that prevents blind changes. For each proposed
improvement:

1. **State hypothesis**: What specific change will fix the failure?
2. **Gather evidence**: From eval results, failure patterns, baseline scores
3. **Consider counter-arguments**: What could go wrong? Risk of regression?
4. **Make decision**: Apply, skip, or defer with full reasoning

Decisions are logged in `research_decisions.json` for auditability.

**Decision criteria:**

- **Apply**: Clear failure pattern + prompt template available + low score
- **Skip**: Score above 50% (likely stochastic variation)
- **Defer**: Ambiguous evidence, needs more data

### Phase 4: IMPROVE

Apply the improvements approved by the research step. Priority order:

1. Prompt template improvements (safest, highest impact)
2. Retrieval strategy adjustments
3. Code logic fixes (most risky, needs careful review)

### Phase 5: RE-EVAL

Re-run the same eval suite after applying fixes to measure impact.

### Phase 6: DECIDE

**Promotion gate:**

- Net improvement >= +2% overall score: COMMIT the changes
- Any single level regression > 5%: REVERT all changes
- Otherwise: COMMIT with marginal improvement note

## Configuration

| Parameter               | Default                       | Description                              |
| ----------------------- | ----------------------------- | ---------------------------------------- |
| `sdk_type`              | `mini`                        | Which SDK: mini/claude/copilot/microsoft |
| `max_iterations`        | `5`                           | Maximum improvement iterations           |
| `improvement_threshold` | `2.0`                         | Minimum % improvement to commit          |
| `regression_tolerance`  | `5.0`                         | Maximum % regression on any level        |
| `levels`                | `L1-L6`                       | Which levels to evaluate                 |
| `output_dir`            | `./eval_results/self_improve` | Results directory                        |
| `dry_run`               | `false`                       | Evaluate only, don't apply changes       |

## Programmatic Usage

```python
from amplihack.eval.self_improve import run_self_improvement, RunnerConfig

config = RunnerConfig(
    sdk_type="mini",
    max_iterations=3,
    improvement_threshold=2.0,
    regression_tolerance=5.0,
    levels=["L1", "L2", "L3", "L4", "L5", "L6"],
    output_dir="./eval_results/self_improve",
    dry_run=False,
)

result = run_self_improvement(config)
print(f"Total improvement: {result.total_improvement:+.1f}%")
print(f"Final scores: {result.final_scores}")
```

## 4-Way Benchmark Mode

Compare all SDK implementations side by side:

```
User: "Run a 4-way benchmark comparing all SDK implementations"

Skill: Runs eval suite on mini, claude, copilot, microsoft
       Generates comparison table with scores, LOC, and coverage.
```

## Integration Points

- `src/amplihack/eval/self_improve/runner.py`: Self-improvement loop runner
- `src/amplihack/eval/self_improve/error_analyzer.py`: Failure classification
- `src/amplihack/eval/progressive_test_suite.py`: L1-L12 eval runner
- `src/amplihack/agents/goal_seeking/sdk_adapters/`: All 4 SDK implementations
- `src/amplihack/eval/metacognition_grader.py`: Advanced eval dimensions
- `src/amplihack/eval/teaching_session.py`: L7 teaching quality eval
