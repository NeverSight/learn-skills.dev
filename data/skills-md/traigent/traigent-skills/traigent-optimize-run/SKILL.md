---
name: traigent-optimize-run
description: "Run Traigent optimization: async/sync execution, algorithm selection, cost limits, stop conditions, and parallel trials. Use when calling func.optimize() or optimize_sync(), choosing algorithms (auto/grid/random anywhere; named smart selectors like bayesian/optuna on authenticated connected runs, SDK 0.20.1+), setting max_trials or cost_limit, configuring parallel execution, or handling CostLimitExceeded."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: optimize
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.23"
---

# Running Traigent Optimization

## When to Use

Use this skill after you have decorated a function with `@traigent.optimize()` and need to:

- Run optimization (async or sync)
- Choose an algorithm (`auto` for connected real runs; `grid`/`random` for explicit local/offline search; named smart selectors like `bayesian`/`tpe`/`optuna` on authenticated connected runs, SDK 0.20.1+)
- Set trial limits, timeouts, or cost budgets
- Configure parallel trial execution
- Handle cost limit exceptions
- Interpret stop reasons and results

## Optimization Economics — Read This Before Sizing a Run

**Do not default to recommending zero spend.** The canonical Traigent posture on spending,
the five characterization questions with their exact options, the tailoring rules (including
the three-option paging rule), the explanation duty, and the local survey draft contract all
live in one file that ships inside this skill:
**`references/economics-characterization.v0.md`**. Read it from this skill's own directory
before you propose, size, or decline a run — it is deliberately not restated here. It is
generated from `docs/shared/economics-characterization.v0.md` in the traigent-skills repo,
which is where any edit goes; the copy shipped here is byte-identical.

**Characterize, never compute a budget locally.** Collect the characterization and relay it;
the Traigent service authors the budget, exactly as it authors the run-plan and the next-step
decision — **budget authorship belongs to the service.** Do not compute, adjust, or recommend a
budget locally: no budget arithmetic in markdown, no floor/cap table, no "roughly $X/day" of
your own. The reference describes what the service computes; it is not a local calculator, and
when the service returns no economics result, say so plainly and continue with **no budget
number at all** rather than inventing one.

**This skill's part:** enforce the service-set cap, the required receipt, and the stop rule
that were recorded before the spend.

**Mandatory whenever you relay any of it:** show the options, recommend exactly one, and
explain **why in the user's own numbers** — their agent, their volumes, their error costs. The
explanation is a product requirement, not decoration.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval before any
paid run**, an explicit spend cap, and the recorded stop rule. The service sets
*how much* to invest; it never affects *whether* approval is required — it always is.

## Objective Naming Rule

Default: at least one objective labeled `accuracy` (built-in objective or your `metric_functions` key). If accuracy doesn't apply to this problem, name the primary quality KPI after the product concept, for example `valid_schema`, and note why accuracy was skipped.

## Async Execution

The primary way to run optimization. Returns an `OptimizationResult`. Import the result type
directly — don't guess the path:

```python
from traigent.api.types import OptimizationResult  # equivalently: traigent.OptimizationResult
```

See `traigent-analyze-results` for the full field reference.

> **Dry-run first.** Before a real (paid) run, always validate in mock mode and present a cost estimate to the user. See `traigent-boost-agent` (Your Role; Step 4: Report and Estimate Costs) for the mandatory dry-run-first / cost-approval workflow.
>
> ```python
> from traigent.testing import enable_mock_mode_for_quickstart
> enable_mock_mode_for_quickstart()
> results = answer.optimize_sync(max_trials=10, algorithm="grid")  # mock, no cost
> print(f"Mock pipeline OK: {len(results.trials)} trials, {len(results.failed_trials)} failed")
> # Estimate the REAL run's calls before approving. There is no `results.estimated_cost_usd`
> # accessor. Calls ~= trials x examples x model calls per example, plus judge calls; price
> # that at your model's real rate. See references/run-cost-and-limits.md.
> max_trials, dataset_size, calls_per_example = 10, 15, 2   # your run's values
> print(f"Real run: about {max_trials * dataset_size * calls_per_example} model calls + judge calls")
> ```
> Mock mode avoids provider spend but can still contact the backend and consume quota when a
> Traigent key is set. For local-only wiring, declare `offline=True` on the decorated function
> before running it; mock mode alone is not a network boundary.
> Only proceed to the real run below after the user explicitly approves the cost.

<!-- PROTECTED -->
> **Show the cost card once per project.** Before the first paid run on a project (no earlier
> paid result in this session or in the project's results folder), show the user the card in
> `references/run-cost-and-limits.md` — what a run costs, the guards in order, and why cost
> Traigent cannot see is still billed — once, then ask for the dollar cap and the trial count.
<!-- /PROTECTED -->

> **Verify model IDs are live first.** Catalogs change — a delisted/renamed ID causes a 404 or a
> degraded, unpriced trial that wastes the run. Preflight with
> `traigent models --provider <p> --check <id>` (or the provider's live catalog endpoint). See
> the `traigent-setup-integrations` skill for multi-provider verification.

<!-- PROTECTED -->
> **Never mock the real run.** Mock/offline mode (`enable_mock_mode_for_quickstart()`,
> `TRAIGENT_MOCK_LLM`, `TRAIGENT_OFFLINE_MODE`) is for the DRY RUN only — never the run you're
> about to bill, score, or report as real. The mock LLM returns a constant response and near-zero
> cost, and that signature silently produces garbage scores if it leaks into what was supposed to
> be a real paid run. Before treating any run as real, verify it actually was:
>
> - `results.total_cost` must be a positive number. Mock runs cost ~0.
> - Per-trial outputs must vary. A constant mock response collapses every trial to the same,
>   uniform score.
>
> If a "real" run shows this signature (cost ~0, constant outputs, uniform scores), it was **not**
> real — do not report those numbers. Check that mock mode wasn't left enabled
> (`enable_mock_mode_for_quickstart()` sets process-local state that survives inside a long-lived
> interpreter/notebook — start a fresh interpreter for the real run) and that `TRAIGENT_MOCK_LLM` /
> `TRAIGENT_OFFLINE_MODE` are unset in the environment, then rerun.
<!-- /PROTECTED -->

```python
import asyncio

import traigent
import litellm  # pip install "traigent>=0.19" — the canonical runnable LLM call

@traigent.optimize(
    eval_dataset="qa_test.jsonl",
    objectives=["accuracy"],
    configuration_space={
        # Verify these IDs are live + priced before a real run (catalogs change).
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.1, 0.5, 0.9],
    },
)
def answer(question: str) -> str:
    cfg = traigent.get_config()
    resp = litellm.completion(
        model=cfg["model"],
        temperature=cfg["temperature"],
        messages=[{"role": "user", "content": question}],
    )
    return resp.choices[0].message.content

# Run optimization (real — only after dry-run approval). `optimize()` is a coroutine:
# await it inside async code; from a plain script, drive it with asyncio.run().
async def main():
    return await answer.optimize(max_trials=10)  # default algorithm="auto"


results = asyncio.run(main())
```

### optimize() Parameters

| Parameter | Type | Description |
|---|---|---|
| `algorithm` | `str \| None` | Algorithm: `"auto"` (default cloud smart optimizer), `"grid"`/`"random"` (local search). Named smart algorithms such as `"bayesian"`/`"optuna"` are connected-only (SDK 0.20.1+) — see below. Falls back to decorator setting. |
| `max_trials` | `int \| None` | Maximum number of trials to run. |
| `timeout` | `float \| None` | Maximum wall-clock time in seconds. |
| `save_to` | `str \| None` | Path to save results to disk. |
| `custom_evaluator` | `Callable \| None` | Override evaluator for this run. |
| `callbacks` | `list[Callable] \| None` | Progress tracking callbacks. |
| `configuration_space` | `dict \| None` | Override config space for this run. |
| `objectives` | `list[str] \| ObjectiveSchema \| None` | Override objectives for this run. |
| `cost_limit` | `float \| None` | Per-run cost cap in USD. Overrides `TRAIGENT_RUN_COST_LIMIT` for this call. A pre-run estimate over the limit raises `OptimizationError`; a mid-run budget hit returns partial results with `stop_reason="cost_limit"` (see cost handling below). |
| `budget` | `ExecutionBudget \| None` | Experimental (SDK 0.26.0+): one cumulative cost / examples / deadline cap shared by every `optimize()` call it is passed to (see "Setting a Cost Limit"). |
| `**algorithm_kwargs` | `Any` | Algorithm-specific parameters (e.g., `parameter_order` for grid). |

`warm_start_from` is a **decorator** argument, not an `optimize()` one — `.optimize(warm_start_from=…)`
raises `TypeError` (SDK 0.19.1+, Traigent/Traigent#1683). To seed a connected run from a prior portal
experiment: `@traigent.optimize(..., warm_start_from="<prior experiment id>")`. Cloud sessions only:
the SDK forwards it on session creation and the backend may reuse that run's results; no local/offline
effect.

To continue from a prior run, see the post-run flow (`traigent-analyze-guidance`).

## Sync Execution

For scripts or notebooks where you do not want to manage an async event loop.

```python
# Option 1: optimize_sync() convenience method
results = answer.optimize_sync(max_trials=10, algorithm="grid")

# Option 2: asyncio.run() wrapper
import asyncio
results = asyncio.run(answer.optimize(max_trials=10, algorithm="grid"))
```

`optimize_sync()` accepts the same parameters as `optimize()`. It creates and manages the event loop internally.

**A paid run outlives your tool's foreground timeout.** Coding-agent shells commonly kill a command
after ~2 minutes, and the trials already paid for are not rolled back. Launch a real run detached and
poll its log or `save_to=` file rather than awaiting it in the foreground:

```bash
nohup python run_optimization.py > optimization-run.log 2>&1 &
```

Set `TRAIGENT_RESULTS_FOLDER` to a project-local, git-ignored directory so partial results land where
you can recover them, and `TRAIGENT_LOG_EXAMPLE_CONTENT=false` if prompts, outputs, and expected
answers must not be written to the SDK's per-example logs (they are by default).

## Algorithm Selection

### Grid Search

Exhaustive search over all configurations in the config space. Deterministic and complete.

```python
results = func.optimize_sync(max_trials=24, algorithm="grid")

# Control iteration order with parameter_order
results = func.optimize_sync(
    algorithm="grid",
    parameter_order={"model": 0, "temperature": 1},  # model varies slowest
)
```

**Best for**: Small config spaces (under 50 combinations) where you want to test everything.

### Random Search

Samples configurations randomly from the config space. Good for large spaces where exhaustive search is impractical.

```python
results = func.optimize_sync(max_trials=20, algorithm="random")
```

**Best for**: Large config spaces, quick exploration, when you have a limited trial budget.

### Smart Algorithms (Bayesian / Optuna / TPE / CMA-ES / NSGA-II) — Connected-Only

> **Named smart selectors execute on connected runs since 0.20.1** (see version-matrix: `smart-selector-exec`). On an authenticated connected run, the supported names — `algorithm="bayesian"`, `"tpe"`, `"optuna"`, `"optuna_tpe"`, `"optuna_random"` — bind to the typed backend Optuna strategy and are serialized on session creation; unsupported smart names such as `"nsga2"`/`"cmaes"` fail fast before session creation with a capability message (Traigent/Traigent#1752, #1758; on 0.20.0 no named smart selector executed end-to-end). They never run locally on any version: with `offline=True` the decorator raises `ConfigurationError` at decoration time (*"requires managed optimization and cannot be used with offline=True"*), and the SDK's local optimizer registry rejects the names with `OptimizationError` (*"Smart optimization ('bayesian') runs in the Traigent cloud and is not available in the local SDK (which supports 'grid' and 'random')"*). `algorithm="auto"` (the default) remains the connected smart path when you do not need a specific strategy.
<!-- contract: literal "requires managed optimization" in traigent.config.types -->
<!-- contract: raises ConfigurationError in traigent.core.optimized_function -->

```python
# Connected-only — requires TRAIGENT_API_KEY and offline=False; on SDK 0.20.1+
# binds the named strategy server-side (fails on 0.20.0 and always with offline=True):
# results = func.optimize_sync(max_trials=30, algorithm="bayesian")

# Default connected smart path:
results = func.optimize_sync(max_trials=30, algorithm="auto")
```

### Quick Comparison

| Algorithm | Strategy | Config Space Size | Trial Budget | Where search runs |
|---|---|---|---|---|
| `"auto"` | Cloud smart default | Any | Any | Traigent cloud |
| `"grid"` | Exhaustive | Small (< 50) | Matches space size | Local SDK search |
| `"random"` | Sampling | Any | Limited | Local SDK search |
| `"bayesian"` / `"optuna"` / `"tpe"` / `"cmaes"` / `"nsga2"` | Named backend strategy | Any | Any | **Connected only, SDK 0.20.1+** (supported names bind server-side; `nsga2`/`cmaes` fail fast — see above) |

> ⚠️ **`auto` with no live backend session is a local `random` search, not managed optimization.**
> When no `TRAIGENT_API_KEY` is found in the process, or session creation hits a connectivity
> failure, a 5xx, or the session-create HTTP 400 that both the typed and the legacy create
> request return (any other 400 raises `ConfigurationError`), `algorithm="auto"` does not fail: it falls back to local random
> sampling, prints one warning banner, and returns a result that reads like the managed one
> (verified on 0.27.0: `metadata["source"] == "local_fallback"`, `fallback_reason_code ==
> "no_api_key"`). A key the backend rejects (401/403/429) and an unresolvable backend host raise
> instead. Two rules for any run the user approved *as* managed search:
> 1. Launch it with `TRAIGENT_REQUIRE_CLOUD=1` so session-creation failure raises **before** any
>    trial is paid for, instead of degrading.
> 2. On return, treat `results.metadata.get("source") == "local_fallback"` (with
>    `metadata["fallback_reason"]` / `metadata.get("fallback_reason_code")`, the code is 0.27.0+) or `results.cloud_url is None` as a
>    failure to investigate, never a result to report. Prove tracking first at $0: a stub function
>    returning a constant, 1–2 trials, confirm a `cloud_url` comes back.

> ⚠️ **Local `default_config` consumes a `max_trials` slot.** In local SDK execution (`grid`,
> `random`, and `auto` when it resolves to local random), a supplied `default_config` runs as an
> extra baseline trial before optimizer suggestions and counts against `max_trials`. This bites
> hardest on `grid`: to cover an N-point grid, either omit `default_config` and set
> `max_trials = N`, or keep `default_config` and set `max_trials ≥ N + 1`; otherwise the last grid
> point is silently dropped. Backend-guided connected `auto` does not run `default_config` as a
> baseline trial today. (Field-observed on local SDK 0.21.0: a 2-point grid + `default_config` +
> `max_trials=2` evaluated only `[default, point-1]`.)

Results sync to the portal for every non-offline run, including `grid` and `random`; `offline=True` is the zero Traigent backend egress path and does not sync results. It does not stop provider calls, and LiteLLM fetches its public pricing map at import unless `LITELLM_LOCAL_MODEL_COST_MAP=True` is set before importing it.

<!-- PROTECTED -->
## Cost Controls

Traigent tracks the cost of the model calls it can see and stops a run at the cap. `cost_limit`
bounds only that measured spend: calls Traigent cannot see (streaming, async LangChain, raw
provider SDKs, plain HTTP — the list is in `references/run-cost-and-limits.md`) are still billed
by the provider but show as `$0` or `None`, so the cap cannot stop them.
<!-- /PROTECTED -->

### Cost Wiring Probe

Before any full paid run, do a tiny real optimization after mock validation: 1-2 dataset examples, minimal trials, and the cheapest candidate model. This is paid but should cost pennies, and it proves the billing and objective plumbing before scaling up. Check **both surfaces**:

- `results.total_cost` is `float | None`. `None` means cost tracking is unavailable. `0.0` with real calls means the model was unpriced, so the provider may bill while Traigent reports zero. Treat both as cost **not wired**.
- Each trial's `metrics` contains the declared objectives, especially an `accuracy`-labeled primary KPI by default, with real non-degenerate values. If all objective values are `0.0` or all are `1.0`, fix the evaluator/KPI wiring before the full run.

If cost or other KPIs are not picked up for custom services, self-hosted endpoints, or unknown models, fix in this order:

1. Use a model id LiteLLM can price, or map an alias with `litellm.model_alias_map`.
2. Supply custom per-token pricing with `TRAIGENT_CUSTOM_MODEL_PRICING_JSON` or `TRAIGENT_CUSTOM_MODEL_PRICING_FILE`. The JSON shape is `{"my-model": {"input_cost_per_token": 1e-6, "output_cost_per_token": 2e-6}}`; `input`/`output` aliases are accepted, provider prefixes like `openai/` are normalized, and values must be finite non-negative floats. Pricing resolves in this order: LiteLLM, custom pricing, built-in fallback table, then `UnknownModelError`.
3. Report cost from the function itself with `traigent.with_usage(text, total_cost=usd)`: return its result in place of the plain string (it also works as the first element of an `(output, metrics)` tuple). The cost reaches the trial, `results.total_cost` and the run's cost cap, and outside optimization `with_usage` returns `text` unchanged. This bypasses pricing tables and is the primary path for fully custom services. A custom `scoring_function` / `metric_functions` then receives the wrapper dict, so score `output["text"]`. Do NOT return `cost`, `total_cost`, `input_cost` or `output_cost` in the tuple's metrics dict (they are evaluator-reserved and dropped with a "Skipping user metric ... reserved" WARNING), and do not register `metric_functions={"cost": ...}` (dropped without a warning).

```python
import traigent


def call_my_endpoint(question: str, style: str) -> tuple[str, float]:
    # Stand-in for your own model call; it returns the answer and the USD it cost.
    return "4", 0.01


@traigent.optimize(
    eval_dataset="qa_test.jsonl",
    objectives=["accuracy", "cost"],
    configuration_space={"prompt_style": ["short", "detailed"]},
)
def answer(question: str):  # with_usage returns a dict during optimization, text otherwise
    text, usd = call_my_endpoint(question, traigent.get_config()["prompt_style"])
    return traigent.with_usage(text, total_cost=usd)
```

Set `TRAIGENT_STRICT_COST_ACCOUNTING=true` when an unpriced model should fail loudly instead of reporting zero (see Strict Cost Accounting below). Full pricing details: `references/cost-management.md`.

### Setting a Cost Limit

Set the `TRAIGENT_RUN_COST_LIMIT` environment variable (in USD):

```bash
export TRAIGENT_RUN_COST_LIMIT=5.00  # $5 max per optimization run
```

The default limit is $2.00 per run.

Several paid phases under one approved total (a baseline, then the search, then holdout scoring)
can share one cumulative cap on SDK 0.26.0+ — see
[`references/execution-budget.md`](references/execution-budget.md). Per-run `cost_limit` still
applies inside each call; the shared cap is the binding one, and a run it stops reports
`stop_reason="execution_budget"`. Neither cap sees calls your evaluator or a judge places directly.

### Handling a Cost Limit

**A cost limit can surface through either an exception (pre-run) or a return value (mid-run) — handle both paths:**

| Surface | When it happens | How to handle |
|---|---|---|
| `CostLimitExceeded` (**raised, pre-run**) | the *estimated* cost already exceeds the limit and the run wasn't pre-approved — raised **before any trial runs** | `except CostLimitExceeded` (an `OptimizationError` subclass) — raise the limit, shrink the run, or set `TRAIGENT_COST_APPROVED=true` |
| `results.stop_reason == "cost_limit"` (**returned**) | the run hits the budget **mid-run**, stops, and **returns** partial results (no exception) | check `stop_reason` after a normal return |
| `OptimizationError` (**fallback**) | a catch-all for optimization-time errors (include pre-run cost decline) | `except OptimizationError` will catch pre-run cost limits as a subclass, and other optimization errors |

```python
from traigent.utils.exceptions import CostLimitExceeded, OptimizationError

try:
    results = func.optimize_sync(max_trials=100, algorithm="random")
except CostLimitExceeded as e:
    if e.estimated is None:
        print(f"Cost limit exceeded before the run; estimate unavailable; limit ${e.limit:.2f}")
    else:
        print(f"Estimated cost ${e.estimated:.2f} exceeds the ${e.limit:.2f} limit")
except OptimizationError as e:
    print(f"Optimization error: {e}")
else:
    if getattr(results, "stop_reason", None) == "cost_limit":
        print("Budget reached mid-run; partial results returned.")
```

Notes:
- `CostLimitExceeded` is an `OptimizationError` subclass, so `except OptimizationError` will also catch pre-run cost declines. Catch `CostLimitExceeded` first if you want to handle cost limits differently from other optimization errors.
- A pre-run cost decline over the limit raises `CostLimitExceeded` directly at the `optimize()` boundary. A mid-run budget exhaustion does not raise — it returns partial `results` with `stop_reason="cost_limit"` instead.
- The exact exception/return contract is governed by **Traigent/Traigent#1490**. Catching both `CostLimitExceeded` **and** checking `results.stop_reason` is robust across cost-limit scenarios.

### Pre-Approving Costs

The `traigent-boost-agent` lifecycle skill mandates: **dry-run in mock mode first, present the cost estimate, then get explicit user approval before the real run.** Only pre-approve costs in automated pipelines where a human has already reviewed and approved the dry-run estimate. Never bypass this gate on a user's first run or when the config space has changed.

To skip the interactive cost approval handshake in an already-approved pipeline:

```bash
export TRAIGENT_COST_APPROVED=true
```

CI note: local/offline `optimize()` runs also require `TRAIGENT_RUN_APPROVED=1`; see
`traigent-debugging` for `OptimizationError: CI/CD Approval Required`.

### Quota & Run Sizing

Cost is not the only budget. Cloud/hybrid optimization is also **metered by plan quota**,
independent of dollars spent. Two dimensions are tracked per billing period (they reset
monthly):

- **`optimization_samples`** — examples evaluated across all sessions. This is the dimension
  that usually binds first. A run reserves roughly `max_trials × dataset_size` samples.
- **`optimization_trials`** — one optimization session counts as one trial.

A run is **admitted only when both dimensions have headroom**: it is rejected at
session-create if `current_usage + (max_trials × dataset_size)` would exceed the
`optimization_samples` limit (or if you are out of `optimization_trials`). On the free/hobby
tier the sample ceiling is small (500), so a few medium runs can exhaust it, after which new
runs are blocked (0 trials) until the monthly reset.

Before a large run:

1. **Check your current usage** on the portal billing/usage page (or your plan's usage
   summary) so you know how much of the `optimization_samples` budget remains.
2. **Size the run to fit**: pick `max_trials × dataset_size` so it lands under the remaining
   headroom. Shrink `max_trials`, use a smaller eval dataset, or split the run across periods
   if it would not fit. A blocked session-create can look like an input error — see the
   `traigent-debugging` skill ("session-create fails with quota") to recognize it.

> Quota is separate from the per-run dollar `cost_limit` above: staying under `cost_limit`
> does not guarantee you are under `optimization_samples`, and vice versa.

### Strict Cost Accounting

Fail fast if cost tracking cannot extract costs from LLM responses:

```bash
export TRAIGENT_STRICT_COST_ACCOUNTING=true
```

## Stop Conditions

Optimization can stop for several reasons. Check `results.stop_reason`:

| Stop Reason | Trigger |
|---|---|
| `"max_trials_reached"` | Hit the configured `max_trials` limit. |
| `"max_samples_reached"` | Hit the `max_total_examples` limit across all trials. |
| `"timeout"` | Exceeded the `timeout` duration. |
| `"cost_limit"` | Hit the `cost_limit` / `TRAIGENT_RUN_COST_LIMIT` cap — or, when the stop message says `per-trial cost unknown: fallback trial limit`, a trial-count stop because cost was not measured (warning `COST_UNMEASURED_TRIAL_LIMIT_REACHED`; raising `cost_limit` does not help; see `traigent-debugging`). |
| `"execution_budget"` | A shared `ExecutionBudget` (cost, examples, or deadline) was exhausted (SDK 0.26.0+); reported instead of `"cost_limit"`, detail in `results.metadata["execution_budget"]`. |
| `"metric_limit"` | A soft cumulative metric limit was hit; report the completed results. |
| `"vendor_error"` | A provider-side error (401/402/403/429, `insufficient_quota`) ended the run; the SDK does not retry by default. When every call fails before any example is scored the run instead raises `OptimizationError`, so catch that too. |
| `"optimizer"` | Algorithm exhausted the search space (e.g., grid search finished). |
| `"plateau"` | No improvement detected over recent trials. |
| `"convergence"` | Built-in convergence condition triggered. |
| `"semantic_saturation"` | Per-example quality and continuous objectives saturated; inspect `results.metadata["semantic_saturation"]`. |
| `"user_cancelled"` | User cancelled or declined cost approval. |
| `"condition"` | A generic stop condition was triggered. |
| `"error"` | Optimization failed due to an exception. |
| `"network_error"` | Connectivity failure; inspect the failure before retrying. |

```python
results = func.optimize_sync(max_trials=20, algorithm="grid")

print(f"Stop reason: {results.stop_reason}")
print(f"Trials completed: {len(results.trials)}")
print(f"Best score: {results.best_score}")
```

## Parallel Execution

Run trials and/or examples concurrently using `ParallelConfig`.

```python
from traigent.config.parallel import ParallelConfig
from traigent.api.decorators import ExecutionOptions

@traigent.optimize(
    execution=ExecutionOptions(
        parallel_config=ParallelConfig(
            mode="parallel",
            trial_concurrency=2,    # Run 2 trials at the same time
            example_concurrency=4,  # Evaluate 4 examples concurrently per trial
        ),
    ),
    eval_dataset="large_dataset.jsonl",
    objectives=["accuracy"],
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str) -> str:
    import litellm  # pip install "traigent>=0.19"
    cfg = traigent.get_config()
    resp = litellm.completion(model=cfg["model"], messages=[{"role": "user", "content": query}])
    return resp.choices[0].message.content

results = my_func.optimize_sync(max_trials=10, algorithm="random")
```

### ParallelConfig Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` | `"auto" \| "sequential" \| "parallel"` | `None` | Execution mode. `None` inherits from global config. |
| `trial_concurrency` | `int \| None` | `None` | Max concurrent trials. |
| `example_concurrency` | `int \| None` | `None` | Max concurrent examples per trial. |
| `thread_workers` | `int \| None` | `None` | Thread pool size. |

## Displaying Results

In SDK >=0.19, awaited `func.optimize()` and `func.optimize_sync()` already auto-print
the ranked trial table. Call `print_results_table()` only when you need to re-print
later, or when you need custom `objectives` / `config_space` display arguments.

```python
results = func.optimize_sync(max_trials=10, algorithm="grid")  # auto-prints the ranked table

# Optional: re-print later, or override the display metadata.
from traigent.utils.results_table import print_results_table

print_results_table(
    results,
    config_space=func.configuration_space,
    objectives=["accuracy"],   # match your objectives list
)
```

The table highlights the best trial with ★ and colors the best metric value per column.
`func.configuration_space` always reflects the decorator's current config space.

## Working with Results

`OptimizationResult` contains everything from the optimization run:

```python
results = func.optimize_sync(max_trials=10, algorithm="grid")

# Best configuration and score
print(results.best_config)     # {"model": "gpt-4o", "temperature": 0.5}
print(results.best_score)      # 0.92

# Run metadata
print(results.algorithm)       # "GridSearchOptimizer" (the resolved optimizer class name, not the "grid" string you passed in)
print(results.duration)        # 45.2 (seconds)
print(results.stop_reason)     # "max_trials_reached"
print(results.total_cost)      # 0.34 (USD, if tracked)
print(results.optimization_id) # "opt_abc123"

# Per-trial objective values live in trial.metrics under the objective's own name.
# `score` is the weighted selection basis in multi-objective runs, not an objective
# (see version-matrix: score-relocation, SDKs after 0.21.3).
for trial in results.trials:
    print(f"Config: {trial.config}, accuracy: {trial.metrics.get('accuracy')}")

# Derived properties
print(results.success_rate)       # 0.9 (fraction of successful trials)
print(len(results.successful_trials))  # 9
print(len(results.failed_trials))      # 1
```

### Applying the Best Config

After optimization, `func.apply_best_config(results)` locks in the winning configuration: subsequent calls to `func` use it automatically, `traigent.get_config()` inside the function returns it, and `func.current_config` exposes it from outside. Verify `results.best_score` against a threshold before applying — see `traigent-analyze-results` → Applying Best Config for the lifecycle table and the safety check. Applying the best config is not promotion; promotion requires candidate-vs-incumbent validation on the holdout slice (see `traigent-ci-safety-gate`).

### Confirm a Portal-Tracked Run Actually Synced

After a non-offline run, check `results.metadata.get("persistence_status")` — the SDK emits exactly
`"skipped"`, `"succeeded"`, `"degraded"`, or `"failed"` (never `"ok"`). If it's `"failed"`,
the backend finalize failed after retries and the portal session may be stuck `RUNNING` — re-check
the portal, don't assume the run synced. `"degraded"` has two cases, so check the metadata before
deciding: if `persistence_degraded_reason` is set (and `persistence_rejected` is not True), it's
benign rollup-lag — trial results *and* finalize synced (the portal link works), only summary
aggregates may lag, so keep the run and don't re-pay for a rerun. But if `persistence_rejected` is
True / `persistence_reason == "rejected"`, the backend actively **refused** the persistence (quota,
auth, or tenant) — inspect `persistence_rejection_reason` and treat it as a real problem, not benign.
Full detail: `traigent-analyze-results` → "Verify the Run Actually Persisted".

> **LiteLLM's `*_with_retries` helpers need `tenacity`.** If the decorated function calls
> `litellm.completion_with_retries()` / `acompletion_with_retries()`, know that LiteLLM imports
> `tenacity` lazily inside those helpers. On any SDK build before 0.21.3 (0.21.2 and earlier)
> `tenacity` is NOT in traigent's dependency closure, so in a clean install that retry path dies
> with `ModuleNotFoundError: tenacity`, and the failed call is scored 0, silently biasing the trial
> (field-hit on a real run; Traigent/Traigent#1824, fixed in 0.21.3 via #1825). Plain
> `litellm.completion(num_retries=)` is *not* affected — it uses LiteLLM's own internal retry loop
> and never imports `tenacity`. Traigent/Traigent#1825 (merged 2026-07-10) first declares
> `tenacity>=8.1.0` as a core dep: `tenacity` is bundled since 0.21.3 (0.21.2 and earlier lack it —
> see version-matrix: `tenacity-bundling`). On 0.21.2 and earlier, preflight
> `python -c "import tenacity"` before a paid run that relies on the `*_with_retries` helpers.

## Complete Example

End-to-end optimization from import to results:

```python
import traigent
from traigent.api.decorators import EvaluationOptions, ExecutionOptions
from traigent.config.parallel import ParallelConfig
from traigent.utils.exceptions import CostLimitExceeded, OptimizationError

def exact_match(output: str, expected: str) -> float:
    # SDK builtin accuracy is case-insensitive + whitespace-trimmed (matches SDK since #1473)
    return 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="qa_test.jsonl",
        scoring_function=exact_match,
    ),
    execution=ExecutionOptions(
        parallel_config=ParallelConfig(
            mode="parallel",
            trial_concurrency=2,
            example_concurrency=4,
        ),
    ),
    objectives=["accuracy"],
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.3, 0.7],
    },
)
def answer_question(question: str) -> str:
    import litellm  # pip install "traigent>=0.19"
    cfg = traigent.get_config()
    resp = litellm.completion(
        model=cfg["model"],
        temperature=cfg["temperature"],
        messages=[{"role": "user", "content": question}],
    )
    return resp.choices[0].message.content

async def main():
    # All three cost/failure surfaces from "Handling Cost Limit Exceptions" above.
    try:
        results = await answer_question.optimize(
            max_trials=6,
            algorithm="grid",
            # no timeout: bounded by max_trials + the cost cap, not a wall clock
        )
    except CostLimitExceeded as e:  # raised only when the pre-run estimate exceeds the cap and was not approved
        if e.estimated is None:
            print(f"Budget exceeded before the run; estimate unavailable; limit ${e.limit:.2f}")
        else:
            print(f"Estimated cost ${e.estimated:.2f} exceeds the ${e.limit:.2f} limit")
        return
    except OptimizationError as e:  # pre-run "estimate > limit" decline, and run errors
        print(f"Run declined or failed: {e}")
        return

    if results.stop_reason == "cost_limit":
        print("Budget reached mid-run; results below are partial.")

    if results.best_score is None:
        # No successful trials — do NOT apply anything; report and stop.
        print(f"No trial succeeded (stop reason: {results.stop_reason}). "
              "Inspect the failed trials before spending more.")
        return

    # SDK >=0.19 auto-prints the ranked results table for awaited optimize().
    print(f"Best config: {results.best_config}")
    print(f"Best score:  {results.best_score}")
    print(f"Stop reason: {results.stop_reason}")
    print(f"Duration:    {results.duration:.1f}s")
    if results.total_cost:
        print(f"Total cost:  ${results.total_cost:.2f}")
    else:
        print("Total cost:  NOT TRACKED — wire cost before the next run (see Cost Wiring Probe)")

    # Demo-only application. Validate a sealed holdout before production promotion;
    # never run optimization on the live serving instance (SDK 0.27+ auto-applies).
    answer_question.apply_best_config(results)
    answer = answer_question("What is the capital of France?")
    print(f"Answer: {answer}")

import asyncio
asyncio.run(main())
```

## See Also

- `references/algorithms.md` - Detailed algorithm comparison
- `references/parallel-config.md` - Full ParallelConfig reference
- `references/cost-management.md` - Cost enforcement details
- `references/run-cost-and-limits.md` - Plain-language cost card: what a run costs, guards in order, what is and isn't measured
- `traigent-boost-agent` - Lifecycle driver: dry-run-first / cost-approval mandate (read this before any real optimization run)
- `traigent-setup-quickstart` - Installation and first optimization with mock mode
- `traigent-setup-decorator` - Full `@traigent.optimize()` parameter reference
- `traigent-analyze-results` - **Next step:** read `best_config`/`best_score`, compare trials, extract the quality/cost/latency trade-off, and apply the best config after `optimize()` returns

<!-- Reserved: managed longitudinal-guidance region. Step-level edits must not write here. -->
<!-- SLOW_UPDATE -->
<!-- /SLOW_UPDATE -->

<!-- INTERACTION_POLICY v1 (synced — do not edit inline; edit docs/shared/interaction-policy.v1.md) -->
## Traigent Interaction Policy
Track an interaction profile and adapt to it. Persona (stable): control=`delegate|guided|inspect`,
expertise=`se|ds|unknown`. Mood (this session): pace=`execute|balanced|explore`. Default when
unknown: `guided,se,balanced`. Infer from explicit user statements first, then recent behavior;
an explicit correction wins immediately. Never store or send this profile anywhere by default.

### Fetch the live profile (when available)
At session or skill start, if a configured Traigent client is available, seed the profile from the
backend with the skill name:

```python
policy = None
try: policy = await client.get_interaction_policy(skill="<this skill>")
except Exception: pass
```

Treat the returned `profile` as the STARTING seed: its control/expertise/pace axes plus
`question_budget`, `options_max`, and `jargon_level` replace the static defaults below. Explicit user
corrections in-conversation ALWAYS override the seed. If the call is unavailable or
`fallback_policy="static_v1"`, simply use the static defaults below; the SDK already fails soft.

- Always be concise.
- Match terminology to expertise. For `se`: plain engineering words; define each Traigent or
  statistics term once in plain language (no Bayesian / variance-decomposition / Pareto jargon
  unless asked). For `ds`: compact optimization and statistical terms are fine.
- Presenting options: show at most 3, mark exactly one **Recommended**, and give one short
  persona-appropriate trade-off per option.
- Autonomy. For `delegate` or `execute`: pick the recommended reversible action and proceed, asking
  only at hard gates. For `guided`: offer options with a recommendation at the key decisions. For
  `inspect` or `explore`: give brief rationale or evidence before asking, and ask before branch
  choices.
- Hard gates — always confirm regardless of persona: paid or provider model calls, sending data or
  private content off the machine, destructive edits, decisions the Traigent service is meant to
  return, and any missing fact the step truly requires.
- Recommend the next skill only after a result-bearing step (a run finishes, an analysis
  completes, a configuration validates) or an explicit decision point. Omit recommendations
  during setup or mid-walkthrough. Cap at 3 recommendations per response, each on its own line
  with a one-line eligibility reason (e.g., "traigent-analyze-results — ✓ run succeeded" or
  "traigent-optimize-run — ✓ config validated").
- Never weaken Traigent safety: dry-run before any paid run; get explicit approval before real cost
  or before any data leaves the machine; treat service-returned plans and next steps as
  authoritative. Never put the persona profile or any private content into telemetry, run metadata,
  experiment names, logs, or provenance files.
<!-- /INTERACTION_POLICY v1 -->
