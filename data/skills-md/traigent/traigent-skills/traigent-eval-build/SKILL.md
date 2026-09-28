---
name: traigent-eval-build
description: "Build Traigent evaluators and scoring code. Use when wiring eval_dataset, scoring_function, metric_functions, custom_evaluator, ExampleResult, BaseEvaluator subclasses, deterministic checks, LLM judges, statistical repeated evaluations, hybrid evaluators, or fixing tuple-return/custom-scorer pitfalls."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: evaluation
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.11"
---

# Traigent Build Evaluator

## When to Use

Use this skill after the metric is chosen and the user needs concrete evaluator code.

- For metric selection first, use `traigent-eval-choose-metric`.
- Mock/offline check before paid runs with `TRAIGENT_OFFLINE_MODE`, `enable_mock_mode_for_quickstart()`, and a tiny local dataset.
- Ask for explicit approval and set `TRAIGENT_RUN_COST_LIMIT` before any evaluator calls paid LLMs or backend services. For custom evaluators that make several calls per row, see the cost-metering caveat in `references/evaluator-templates.md`: on traigent <= 0.29.0 only the first LLM call per row is metered, fixed in 0.30.0.
- A judge call placed inside `metric_functions` is **not** in the SDK's cost ledger: on 0.27.0 the local evaluator settles an example's cost from the agent's captured responses before it calls your metric functions, and `TRAIGENT_RUN_COST_LIMIT` admits trials on that recorded cost (Traigent/Traigent#2297). Budget judge calls as their own line (calls per scored row × price × rows × trials), cap them in your own code, and never rely on the SDK limit to stop judge spend.
- Disjointness invariant: any slice used to tune a threshold, rubric, or metric must be disjoint from the holdout used to claim the result (see `traigent-eval-audit`). The example dataset paths below stand for your *tuning* slice.
- For full templates by method, read `references/evaluator-templates.md`.

## Wire-first decision ladder

Prefer the smallest evaluator surface that measures the chosen objective.

| Tier | Wire | Exact signature | Enough when |
|---|---|---|---|
| 1 | `eval_dataset` only | path/list/`Dataset` | Built-in metrics such as `accuracy`, `success_rate`, `error_rate`, `avg_output_length`, `cost`, or `latency` match the task. |
| 2 | `scoring_function` | `scoring_function(output, expected) -> float` | One numeric score per example is enough. |
| 3 | `metric_functions` | `{name: (output, expected, input_data) -> float}` | Multiple named metrics or input-aware checks are needed. |
| 4 | `custom_evaluator` | `custom_evaluator(func, config, example) -> ExampleResult` | The evaluator must call the function itself, collect timing/cost, run a judge, repeat samples, or fail closed. |
| 5 | `BaseEvaluator` subclass | not wireable through `@traigent.optimize` on traigent <= 0.27.0 | The `custom_evaluator=` evaluation option accepts only a `(func, config, example)` callable and the decorator's `evaluator=` accepts only an external-service evaluator. Tier 4 is the highest tier you can wire today. |

The built-in `latency` metric uses the bare key `latency`, reported in milliseconds on SDKs after 0.22.0 (see version-matrix: `latency-unit`).

A `custom_evaluator` does not produce `latency`. If `latency` is an objective, put `metrics["latency"]` (milliseconds) on every `ExampleResult`, or the objective reads 0.0 on every trial and silently ranks nothing. `ExampleResult.execution_time` is in seconds, so convert before copying it across.

**No `expected_output` at all?** Tiers 1-3 assume a gold label to compare against. For
subjective/generative tasks with no labels, skip straight to Tier 4 with the **"LLM judge with
rubric, strict parse, and cost guardrails"** template in `references/evaluator-templates.md` —
and treat `traigent-eval-audit` as mandatory, because the judge owns the whole quality
signal (see `traigent-eval-choose-metric` → "The no-gold track").

### Tier 2: scoring function

```python
import traigent
from traigent.api.decorators import EvaluationOptions

def exact_match_score(output, expected) -> float:
    # SDK builtin accuracy is case-insensitive + whitespace-trimmed (since SDK #1473)
    return 1.0 if str(output).strip().lower() == str(expected).strip().lower() else 0.0

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="eval/qa.jsonl",
        scoring_function=exact_match_score,
    ),
    objectives=["accuracy"],
    configuration_space={"temperature": [0.0, 0.3]},
)
def answer(question: str) -> str:
    cfg = traigent.get_config()
    import litellm  # pip install "traigent[integrations]>=0.19"
    resp = litellm.completion(model=cfg.get("model", "gpt-4o-mini"), temperature=cfg["temperature"],
                              messages=[{"role": "user", "content": question}])
    return resp.choices[0].message.content
```

### Tier 3: metric functions

```python
import json

import traigent
from traigent.api.decorators import EvaluationOptions
from traigent.core.objectives import ObjectiveDefinition, ObjectiveSchema

def valid_json_metric(output, expected, input_data) -> float:
    try:
        json.loads(output)
    except json.JSONDecodeError:
        return 0.0
    return 1.0

def expected_field_metric(output, expected, input_data) -> float:
    # Model output that is not a JSON object is a wrong answer: score 0.0.
    # A gold that is not a dict is a dataset defect: let it raise. On 0.27.0 an
    # objective metric that raises fails the trial closed with a distinct
    # EvaluationError instead of a fake 0.0 the search would rank as "wrong answer".
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return 0.0
    if not isinstance(data, dict):
        return 0.0
    return 1.0 if data.get("label") == expected["label"] else 0.0

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="eval/extraction.jsonl",
        metric_functions={
            "valid_json": valid_json_metric,
            "label_accuracy": expected_field_metric,
        },
    ),
    # Custom metric names need a declared orientation; only built-ins such as
    # accuracy, cost and latency have one.
    objectives=ObjectiveSchema.from_objectives([
        ObjectiveDefinition(name="label_accuracy", orientation="maximize", weight=1.0),
        ObjectiveDefinition(name="valid_json", orientation="maximize", weight=1.0),
    ]),
    configuration_space={"temperature": [0.0, 0.2]},
)
def extract(text: str) -> str:
    cfg = traigent.get_config()
    import litellm  # pip install "traigent[integrations]>=0.19"
    resp = litellm.completion(model=cfg.get("model", "gpt-4o-mini"), temperature=cfg["temperature"],
                              messages=[{"role": "user", "content": text}])
    return resp.choices[0].message.content
```

#### Binding a per-example side field (e.g. `db_path`) — name a `metadata` parameter

`metric_functions` binds its arguments **by parameter name**, not by position (SDK
`evaluators/local.py` `_build_metric_keyword_arguments`). The names available are:
`output`/`expected` (the row's prediction + gold), `input_data` (the **nested `input` dict only**),
`metadata` (the row's top-level extras), `config`, `example`, and `example_index`.

For optional `surrogate_evaluator` mechanics and caveats, see `traigent-setup-decorator` -> "Evaluation Setup".

The documented `(output, expected, input_data)` signature **cannot** see a top-level side field like
`db_path` — `input_data` is only the `input` dict. To reach it, **name a `metadata` parameter** and
read the key the dataset contract routed there (see `traigent-dataset-curate` for the row mapping):

```python
from text2sql.execaccuracy import execution_accuracy  # opens metadata["db_path"], runs pred vs gold
from traigent.core.objectives import ObjectiveDefinition, ObjectiveSchema

def exec_acc(output, expected, metadata) -> float:   # NAME the param `metadata`
    return execution_accuracy(output, expected["sql"], metadata["db_path"])

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="eval/salesco_30.jsonl",        # rows: {"input": {...}, "output": {"sql": "<gold>"}, "db_path": "..."}
        metric_functions={"exec_acc": exec_acc},     # Tier 3 — no climb to Tier 4 needed
    ),
    objectives=ObjectiveSchema.from_objectives([
        ObjectiveDefinition(name="exec_acc", orientation="maximize", weight=1.0),  # custom name: declare it
    ]),
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def to_sql(question: str, schema: str = "", db_id: str = "") -> str:
    ...
```

A param named `input_data` would receive the nested `input` dict, **not** `db_path` — that is the
silent trap. (Tier-4 alternative: read `example.metadata["db_path"]` directly inside a
`custom_evaluator`.)

### Tier 4: custom evaluator

```python
import time

import traigent
from traigent.api.decorators import EvaluationOptions
from traigent.api.types import ExampleResult

def evaluate_answer(func, config, example) -> ExampleResult:
    started = time.perf_counter()
    try:
        prediction = func(**example.input_data)
        # SDK builtin accuracy is case-insensitive + whitespace-trimmed (since SDK #1473)
        score = 1.0 if str(prediction).strip().lower() == str(example.expected_output).strip().lower() else 0.0
        error_message = None
        success = True
    except Exception as exc:
        prediction = None
        score = 0.0
        error_message = str(exc)
        success = False

    elapsed_s = time.perf_counter() - started
    return ExampleResult(
        example_id=str(example.metadata.get("id", "unknown")),
        input_data=example.input_data,
        expected_output=example.expected_output,
        actual_output=prediction,
        metrics={"accuracy": score, "latency": elapsed_s * 1000.0},  # latency objective is milliseconds
        execution_time=elapsed_s,  # ExampleResult field is seconds
        success=success,
        error_message=error_message,
        metadata={"method": "deterministic_exact_match"},
    )

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="eval/qa.jsonl",
        custom_evaluator=evaluate_answer,
    ),
    objectives=["accuracy"],
    configuration_space={"temperature": [0.0, 0.3]},
)
def answer(question: str) -> str:
    cfg = traigent.get_config()
    import litellm  # pip install "traigent[integrations]>=0.19"
    resp = litellm.completion(model=cfg.get("model", "gpt-4o-mini"), temperature=cfg["temperature"],
                              messages=[{"role": "user", "content": question}])
    return resp.choices[0].message.content
```

### Tier 5: BaseEvaluator subclass (not wireable today)

Do not write a `BaseEvaluator` subclass to plug into `@traigent.optimize`: no public option accepts one on traigent <= 0.27.0. Passing an instance as the `custom_evaluator=` evaluation option fails validation with `Input should be callable`, and passing the class fails with `custom_evaluator must accept (func, config, example)`. The top-level `custom_evaluator=` argument of `@traigent.optimize` and of `optimize_sync()` accepts an instance at first, then fails when the run starts with `custom_evaluator must be callable`. The decorator's `evaluator=` takes only an external-service evaluator. Use a Tier 4 `custom_evaluator` for per-row control (calling the function, timing, judges, repeats, fail-closed handling).

## The EvaluationExample input contract

The `example` argument passed to `custom_evaluator(func, config, example)` is an `EvaluationExample` object — not a dict.

| Attribute | Source in JSONL | Type | Notes |
|---|---|---|---|
| `example.input_data` | `"input"` key | `dict` | Expand as `func(**example.input_data)` to call the decorated function. |
| `example.expected_output` | `"output"` key | `Any` | Gold label; string, dict, or list depending on dataset. |
| `example.metadata` | All other keys | `dict` | Extra JSONL fields land here — `db_id`, `id`, `difficulty`, etc. |

**Common pitfalls:**
- `example["input"]` → `TypeError: 'EvaluationExample' object is not subscriptable`. Use `.input_data`, not dict access.
- `example.input` does not exist — the attribute is `.input_data` (name differs from the JSONL key).
- `example.output` does not exist — use `.expected_output`.
- Extra JSONL keys (e.g. `db_id`) are in `example.metadata["db_id"]`, not top-level attributes.
- A row that carries its own `metadata` object is nested one level down on 0.27.0 (Traigent/Traigent#1768): `db_id` is at `example.metadata["metadata"]["db_id"]`; `example.metadata.get("db_id")` reads `None` and `example.metadata["db_id"]` raises `KeyError`. Read both shapes.

## The ExampleResult contract

On `traigent` 0.12.0+ (including the current SDK), construct `ExampleResult` with these fields (0.14+ adds one optional field, `user_metrics`):

| Field | Required | Meaning |
|---|---|---|
| `example_id` | yes | Stable example id for reporting. |
| `input_data` | yes | Input dictionary used for this example. |
| `expected_output` | yes | Gold label or expected value. |
| `actual_output` | yes | Function output, judge result, or `None` on failure. |
| `metrics` | yes | Numeric metrics such as `{"accuracy": 1.0}`. |
| `execution_time` | yes | Seconds spent evaluating this example. |
| `success` | yes | Whether the evaluator completed this example without an evaluator/runtime failure. |
| `error_message` | no | Failure text, or `None`. |
| `metadata` | no | Method, model, rubric version, parse policy, or other non-secret context. |

The decorator validates `custom_evaluator` signature at decoration time. The required contract is `(func, config, example) -> ExampleResult`. A two-argument evaluator fails with:

```text
ValidationError custom_evaluator must accept (func, config, example), got 2 required parameters: ['func', 'config']
```

## The interview when nothing exists

If no evaluator exists, ask:

1. Which metric did `traigent-eval-choose-metric` select?
2. Can it be checked deterministically from `output`, `expected`, and `input_data`?
3. Does the evaluator need to call the function itself, repeat calls, inspect tool traces, or count judge cost?
4. Is judge output parseable into a strict schema?
5. What should happen on parse failure, tool failure, timeout, or missing labels?

Map the answer to `deterministic`, `llm_based`, `statistical`, or `hybrid`, then pick the lowest tier in the ladder.

## Templates by evaluation method

Use compact patterns inline and the full versions in `references/evaluator-templates.md`.

| Method | Inline pattern |
|---|---|
| `deterministic` | Exact/normalized/schema checks with `scoring_function` or `metric_functions`; fail invalid schema to `0.0`. |
| `llm_based` | Custom evaluator calls a judge with a rubric, parses strict JSON, counts judge cost, and returns `0.0` on parse failure. |
| `statistical` | Custom evaluator repeats the same example, scores agreement or pass rate across reps, and reports variance metadata. |
| `hybrid` | Deterministic gate first; call the judge only if the output passes the gate. |

## Known pitfall: tuple returns and custom scorers

If the optimized function returns `(output, metrics)`, make sure the custom scorer receives the model output, not the whole tuple, unless your scorer intentionally handles tuples. Prefer one of these patterns:

- Keep the production function returning the plain output, and collect extra metrics inside `custom_evaluator`.
- If returning `(output, metrics)`, unwrap before string comparison, JSON parsing, or label matching.
- Do not reuse a metric name for both tuple-returned metrics and evaluator-computed metrics.

## Known pitfall: arbitrary gold ordering caps accuracy

When a deterministic scorer compares structured outputs against a gold whose internal ordering is arbitrary (SQL projection columns, JSON object keys, set-valued answers), decide the order policy explicitly and write it in the evaluator docstring. If the gold's ordering is arbitrary and the comparator is positional, correct answers score 0 and impose a hard accuracy ceiling that no configuration can cross — the optimizer then ranks knobs by their accidental effect on ordering. Policy for SQL execution match (the Spider test-suite convention): row order significant only when gold has `ORDER BY`; column order never significant (compare under column permutations); column count must match. Audit signal: an example that fails in 100% of trials across all configs is a metric-artifact suspect — re-check its gold and your order policy before blaming the model.

## Known pitfall: score what the evaluator is handed, not what the model meant

A chat model wraps code, SQL, and JSON in a markdown fence by default — and sometimes when told not to. An exact or normalized comparator scores that reply 0 for every configuration, so every candidate ties and the search ranks noise. Put the agent's own extraction step (fence strip, first statement, JSON parse) between model and scorer, then pass a known-right answer through that step and confirm it still scores right. A first paid run whose primary metric is exactly 0.0 or 1.0 on every trial is a scorer-or-extraction suspect: dump one raw reply and the value the scorer received before spending again.

## Claim scope

- Deterministic scores measure only the rules encoded in the evaluator.
- A metric's 0.0 must mean the answer was wrong; a harness or data-shape failure must raise or be flagged, never scored as an ordinary wrong answer without being counted separately (the judge template's parse-failure 0.0 is such a counted class).
- Judge scores are model opinions under the stated rubric. Label them as judge scores.
- Statistical scores depend on repeat count, sampling settings, and dataset slice.
- Hybrid scores inherit both the deterministic gate assumptions and judge limitations.

## See Also

- `traigent-eval-choose-metric` - choose objectives before building evaluator code
- `traigent-boost-agent` Step 3.5 - lightweight evaluator sanity gate (run this before the first paid optimization)
- `traigent-eval-audit` - evaluator reliability: manual gold-slice protocol + service-side evaluator-audit action (no new gold collection required)
- `traigent-setup-decorator` - decorator wiring for evaluation options
- `traigent-analyze-results` - inspect the metrics emitted by evaluator runs
- `traigent-dataset-curate` - create and improve the evaluation dataset

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
