---
name: ag2-eval-comparison
description: Compare AG2 agents, models, or prompts to decide which is better. run_variants scores several named agents on one suite and ranks them on a leaderboard (Variants holds a mapping of named Agent instances plus an axis label). run_pairwise with pairwise_judge does head-to-head LLM comparison using a dual-order position swap (a win counts only if it survives the swap, else a tie), reporting win-rate with a Wilson 95% CI, wins, losses, ties, flips, and agreement (Cohen's kappa). human_pairwise collects a person's blinded vote inline, or via an exported manifest with export_pairwise_cases and human_labels. Use when the user wants to A/B test prompts or models, run a leaderboard, pick a winner, judge head-to-head, measure win-rate, or collect human preference labels. For running and grading a single agent, see ag2-evaluation.
license: Apache-2.0
---

# Evaluation — comparing builds (variants & pairwise)

## When to use

- Rank N models / prompts / configs on a **leaderboard** → `run_variants`
- Decide **which of two is better**, head-to-head → `run_pairwise` with `pairwise_judge` (LLM) or `human_pairwise` (people)

For running and grading a single agent (scorers, CI, persistence), use `ag2-evaluation`.

## Install

```bash
pip install "ag2[openai,tracing]"
```

> Required. Run this install before delivering the code. If you cannot run commands, state the exact `pip install` command.

## Leaderboard — run_variants

`Variants` is a frozen dataclass holding a mapping of named **`Agent` instances** plus an `axis` label naming what you varied. Build each agent with the one thing that differs (config, prompt, tools, middleware, …), hold the rest fixed, score each, rank:

```python
from ag2 import Agent
from ag2.config import OpenAIConfig, GeminiConfig
from ag2.eval import Variants, run_variants
from ag2.eval.scorers import agent_judge

board = await run_variants(
    suite,
    variants=Variants(
        {
            "gpt-4o": Agent("a", prompt="Answer helpfully.", config=OpenAIConfig("gpt-4o")),
            "flash":  Agent("a", prompt="Answer helpfully.", config=GeminiConfig("gemini-3-flash-preview")),
        },
        axis="config",                  # label for what was varied (used in summary)
    ),
    scorers=[agent_judge(OpenAIConfig("gpt-4o"), criterion="Helpful and accurate.", key="quality")],
    store_dir="runs",
    repeats=5,                          # optional: N runs per variant for stability
)
print(board.summary("quality"))         # ranked leaderboard
board.best("quality")                   # winning variant name (None if tied)
board.leaderboard("quality")            # list[LeaderboardRow] — variant, score, n, rank
board.results["gpt-4o"]                 # each variant's full RunResult
```

Vary whatever you like across the agents — set `axis` to label it (e.g. `"config"`, `"prompt"`, `"tools"`). Tied scores share a rank; a 3-way tie usually means the eval isn't discriminating — make it harder, or score quality with a judge.

## Head-to-head (LLM) — run_pairwise + pairwise_judge

A comparator picks a winner PER task. `pairwise_judge` shows the pair in BOTH orders and counts a win only if it's consistent — else a tie (cancels position bias):

```python
from ag2.eval import run_pairwise
from ag2.eval.scorers import pairwise_judge

result = await run_pairwise(
    suite, variant_a=agent_v1, variant_b=agent_v2,
    comparators=[pairwise_judge(OpenAIConfig("gpt-4o"), criterion="more helpful answer", key="quality")],
    store_dir="runs",
)
wr = result.win_rate("quality")         # B's win-rate
print(wr.rate, wr.ci, wr.wins, wr.losses, wr.ties)   # ties count 0.5; ci is a Wilson 95% interval
print(result.flips("quality"))          # int — count of cases where the two orders disagreed
```

`variant_a` / `variant_b` are **`Agent` instances**; `comparators=` is a plural iterable. `result.agreement("quality", "human")` returns an `Agreement` (`.rate`, `.cohen_kappa`, …) between two comparator keys. Use a judge model different from the variants.

## Head-to-head (human) — human_pairwise

Same unit, decided by a person. The pair is blinded and order-randomized; the default prints it and reads `1` / `2` / `tie`. Pass your own async `ask(task, response_1, response_2)` to collect a vote from a UI (returns `"1"`, `"2"`, or `"tie"`):

```python
from ag2.eval.scorers import human_pairwise

async def ask(task, response_1, response_2) -> str:
    return await my_ui.compare(task.inputs["input"], response_1, response_2)   # "1" / "2" / "tie"

result = await run_pairwise(suite, variant_a=agent_v1, variant_b=agent_v2,
                            comparators=[human_pairwise(key="quality", ask=ask)], store_dir="runs")
```

At scale, export a blinded manifest, label it in any tool, import it. `evaluate_pairwise` is the grade-only twin of `run_pairwise` (pairs two existing trace sources by `task_id`):

```python
from ag2.eval import evaluate_pairwise, DirectoryTraceSource
from ag2.eval.scorers import export_pairwise_cases, human_labels

a, b = DirectoryTraceSource("runs/champion"), DirectoryTraceSource("runs/challenger")
await export_pairwise_cases(a, b, criteria=["more helpful"], out="labels.jsonl", suite=suite)   # blinded JSONL
# a person adds  "preferred": "1" | "2" | "tie"  per line, then:
result = await evaluate_pairwise(a, b, suite=suite, store_dir="runs",
                                 comparators=[human_labels("labels.jsonl", criterion="more helpful", key="helpful")])
```

The manifest hides which model is which; its `first_variant` field de-blinds it for `human_labels`.

## Common pitfalls

- **Judge == a variant's model** — self-preference bias; use a different judge model.
- **Bare win-rate on few pairs** — report `wr.ci` (Wilson); a small n straddles 50%.
- **Passing factories, not agents** — `run_variants` (`variants=Variants({name: Agent(...)})`) and `run_pairwise` (`variant_a=`/`variant_b=`) take **`Agent` instances**, not build callables. Vary the model per task with `model_config=` (a `dict[task_id, ModelConfig]`) rather than rebuilding the agent. Keep `pairwise_judge`'s default swap (don't set `swap=False`) for unbiased verdicts.

## Going deeper

- `website/docs/user-guide/evaluation/` — `variants` (the `Variants` mapping + `axis`), `pairwise` (comparators, win-rate, blinded labeling)
- `ag2-evaluation` — single-agent run/grade, scorers, CI, persistence
