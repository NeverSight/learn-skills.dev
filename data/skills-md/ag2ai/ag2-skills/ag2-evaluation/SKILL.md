---
name: ag2-evaluation
description: Evaluate, test, and track an AG2 Agent offline. Build a Suite of tasks, run the agent with run_agent, and grade answers with prebuilt scorers (final_answer_matches, tool_called, no_tool_errors, token_budget) or a custom @scorer — including the agent_judge LLM judge. Read the RunResult scorecard (pass_rate, score_stats, value_counts), gate it in CI with deterministic TestConfig cassettes, persist to store_dir and diff runs to catch regressions, and grade existing traces with evaluate_traces. Use when the user wants to evaluate, test, grade, or benchmark an agent, build a CI or regression gate, or score correctness, tool use, cost, or quality. To compare builds head-to-head or on a leaderboard, see ag2-eval-comparison.
license: Apache-2.0
---

# Evaluation — run, grade, and track an agent

## When to use

- Evaluate / test / benchmark an AG2 `Agent`, or build a regression / CI gate
- Grade answers for correctness, tool use, cost, or subjective quality
- Track a metric across versions (did this change help or regress?)

To compare two-plus builds head-to-head or on a leaderboard, use `ag2-eval-comparison`.

## Install

```bash
pip install "ag2[openai,tracing]"
```

`run_agent` reconstructs each task's trace from OpenTelemetry spans, so the `tracing` extra is required. Run this install before delivering the code. If you cannot run commands, state the exact `pip install` command.

## The loop — dataset, agent, scorers, run_agent

```python
import asyncio
from ag2 import Agent
from ag2.config import OpenAIConfig
from ag2.eval import Suite, run_agent
from ag2.eval.scorers import final_answer_matches

suite = Suite.from_list([
    {"task_id": "france", "inputs": {"input": "Capital of France?"}, "reference_outputs": {"answer": "Paris"}},
    {"task_id": "japan",  "inputs": {"input": "Capital of Japan?"},  "reference_outputs": {"answer": "Tokyo"}},
])
agent = Agent("geographer", prompt="Answer with the capital city.", config=OpenAIConfig(model="gpt-4o-mini"))

async def main():
    result = await run_agent(
        suite, agent=agent,
        scorers=[final_answer_matches(field="answer", matcher="contains")],
        store_dir="./runs",
    )
    print(result.summary())                            # the scorecard
    print(result.pass_rate("final_answer_matches"))    # 1.0

asyncio.run(main())
```

`inputs["input"]` is the prompt; `reference_outputs` is the gold answer (a dict — omit it for trace-only checks). Each scorer is a column, looked up by its **key**.

## Scorers

A scorer asks ONE question. Its RETURN TYPE picks the aggregation:

| return | aggregation | accessor |
|---|---|---|
| `bool` | pass rate | `result.pass_rate(key)` |
| `int` / `float` | mean / p50 / p95 | `result.score_stats(key)` |
| `str` | value counts | `result.value_counts(key)` |

Prebuilt (`ag2.eval.scorers`): `final_answer_matches(field=, matcher="contains"|"casefold"|"exact")`, `tool_called(name)`, `no_tool_errors()`, `token_budget(n)`, `failure_attribution(...)`, `agent_judge(...)`.

Custom — decorate a function that declares what it needs by name (`outputs`, `trace`, `reference_outputs`, `inputs`, `task`):

```python
from ag2.eval import scorer

@scorer
def answered_briefly(outputs) -> bool:
    return len(outputs["body"]) < 100      # outputs["body"] = final answer text
```

`agent_judge` grades quality you can't check with `==` (use a different model than the agent under test):

```python
from ag2.eval.scorers import agent_judge
judge = agent_judge(OpenAIConfig(model="gpt-4o"), criterion="Helpful and accurate.", key="quality")
```

## CI — deterministic, no API key

Swap the model for a `TestConfig` cassette (a canned reply per task) so CI is free and repeatable. `model_config` is a `dict[task_id, ModelConfig]` — one cassette per task — and overrides the agent's own config for that task:

```python
from ag2.testing import TestConfig

agent = Agent("geographer", prompt="Answer with the capital city.")   # an Agent instance, not a factory

canned = {"france": TestConfig("Paris"), "japan": TestConfig("Tokyo")}
result = await run_agent(suite, agent=agent, scorers=scorers, model_config=canned, store_dir="./runs")
assert result.pass_rate("final_answer_matches") == 1.0      # the gate
```

## Persist, track, grade existing traces

`store_dir=` writes one JSON per run. Reload a past run and diff for regressions; or grade traces you already have (e.g. production telemetry) without re-running the agent:

```python
from ag2.eval import load_run, evaluate_traces, DirectoryTraceSource

assert not result.diff(load_run("./runs/<run_id>.json")).regressions   # scorers that flipped pass -> fail
graded = await evaluate_traces(DirectoryTraceSource("./traces"), scorers=scorers, store_dir="./runs")
```

## Common pitfalls

- **Missing `tracing` extra** — `run_agent` can't reconstruct traces. Install `ag2[<provider>,tracing]`.
- **Return type vs aggregation** — `bool` for pass/fail, a number for stats, a `str` for categories; look results up by the scorer's `key`.
- **Same model answers and judges** — biases `agent_judge`; use a different judge model.

## Going deeper

- `website/docs/user-guide/evaluation/` — `getting-started`, `scorers` (catalog + custom + return-type rules), `runs`, `persistence`
- `ag2-eval-comparison` — leaderboard (`run_variants`) + head-to-head (`run_pairwise`)
