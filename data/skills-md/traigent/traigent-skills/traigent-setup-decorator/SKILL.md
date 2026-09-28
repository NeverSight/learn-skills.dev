---
name: traigent-setup-decorator
description: "Configure the @traigent.optimize() decorator with evaluation, injection, and execution options. Use when setting up eval_dataset, choosing injection_mode, choosing the optimization algorithm or offline execution, defining objectives, naming an optimization with experiment_name (an agent identity key, not a per-run label; there is no tags/metadata argument), using EvaluationOptions/InjectionOptions/ExecutionOptions, or integrating custom evaluators. Provide the agent function + its path, an eval dataset, and the objective(s)."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: setup
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.17"
---

# Traigent Decorator Setup

## When to Use

Use this skill when you need to go beyond the basic `@traigent.optimize()` decorator and configure:

- Evaluation datasets, custom evaluators, scoring functions, or metric functions
- Injection modes (how optimized configs reach your function)
- Execution behavior (`algorithm` and `offline` — where and how optimization runs)
- Multi-objective optimization with weighted objectives
- Naming an optimization with `experiment_name` — an **agent identity key**, not a per-run
  label (there is no `tags`/`metadata` argument)
- Portal-synced or local execution with zero Traigent backend egress

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

**This skill's part:** wire the decorator so the service-set cap, the required receipt, and
the stop rule are enforceable on the run that follows.

**Mandatory whenever you relay any of it:** show the options, recommend exactly one, and
explain **why in the user's own numbers** — their agent, their volumes, their error costs. The
explanation is a product requirement, not decoration.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval before any
paid run**, an explicit spend cap, and the recorded stop rule. The service sets
*how much* to invest; it never affects *whether* approval is required — it always is.

## Inputs to Provide (Quick Cycle)

To wire and run an optimization, three inputs are needed — supply them up front (e.g. when invoking the skill: agent name, agent path, dataset path) so setup proceeds without back-and-forth:

1. **Agent function** — the function to optimize, plus the **file/module path** where it lives, so `@traigent.optimize()` can be applied to it.
2. **Evaluation dataset** — a path to a JSONL eval set (one `input`/`output` per line) used to score each trial.
3. **Objective(s)** — what to optimize: a string list (e.g. `["accuracy"]`) or a weighted `ObjectiveSchema` (see [Objectives](#objectives) below).

A typical **quick cycle is two steps**: configure the decorator with this skill, then launch with the **`traigent-optimize-run`** skill. The decorator config below is identical whether you pass these inputs at invocation or provide them interactively — if any is missing, ask for it before wiring the decorator.

**Multiple candidate agents?** If the skill is invoked without an agent and the project has more than one function that could be optimized (e.g. several that call an LLM), do **not** guess — list the candidates and ask the user which one to wire. Optimize one decorated function per run.

## Imports

```python
import litellm
import traigent
from traigent.api.decorators import (
    EvaluationOptions,
    InjectionOptions,
    ExecutionOptions,
)

def prompt_model(prompt: str, *, model: str = "gpt-4o-mini", temperature: float = 0.0, max_tokens: int = 512) -> str:
    response = litellm.completion(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""
```

## Objectives

Objectives tell Traigent what to optimize for. Pass them as a string list or as an `ObjectiveSchema` for weighted multi-objective optimization.

**Objective naming rule:** Default: at least one objective labeled `accuracy` (built-in objective or your `metric_functions` key). If accuracy doesn't apply to this problem, name the primary quality KPI after the product concept, for example `valid_schema`, and note why accuracy was skipped.

### String List (Simple)

```python
@traigent.optimize(
    objectives=["accuracy", "cost"],
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(query, model=cfg["model"])
```

### ObjectiveSchema (Weighted)

```python
from traigent.core.objectives import ObjectiveSchema, ObjectiveDefinition

schema = ObjectiveSchema(
    objectives=[
        ObjectiveDefinition(name="accuracy", weight=0.7, orientation="maximize"),
        ObjectiveDefinition(name="cost", weight=0.3, orientation="minimize"),
    ],
    weights_sum=1.0,
    weights_normalized={"accuracy": 0.7, "cost": 0.3},
)
```

**`weights_sum`/`weights_normalized` are not free-form fields — they are validated against the
per-objective `weight=` values at construction time.** `ObjectiveSchema.__post_init__` recomputes the
sum and each normalized share from `objectives` and raises `ValueError` immediately if your hand-computed
`weights_sum`/`weights_normalized` disagree (there is no silent "which one wins": construction fails
fast). Prefer the classmethod below, which derives both fields for you so they can never disagree:

```python
schema = ObjectiveSchema.from_objectives(
    objectives=[
        ObjectiveDefinition(name="accuracy", weight=0.7, orientation="maximize"),
        ObjectiveDefinition(name="cost", weight=0.3, orientation="minimize"),
    ],
)

@traigent.optimize(
    objectives=schema,
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(query, model=cfg["model"])
```

## Naming: `experiment_name` identifies the agent, not the run

**`experiment_name` is an identity key, not a per-run label.** The backend derives the
agent from it, and your optimization history is grouped by (agent, evaluation dataset).
Keep it **stable across every run of the same agent**.

> **Do not encode a variant, date, hypothesis, or dataset version into
> `experiment_name`.** Each distinct value creates a *separate agent* in the portal, so
> a per-run name splits one agent's optimization history into a pile of one-run
> fragments — losing exactly the cross-run comparison the portal exists to give you.

```python
@traigent.optimize(
    experiment_name="txt2sql_agent",   # stable identity — same string every run
    objectives=["accuracy"],
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(query, model=cfg["model"])
```

| Intent | Do |
|---|---|
| Name the agent being optimized | `experiment_name="txt2sql_agent"` — stable forever |
| Distinguish two genuinely different agents | Two different `experiment_name` values |
| Record what one run was testing | Not a decorator argument — see below |
| Attach tags/metadata to a run | Not supported; there is no `tags`/`metadata` argument |

**Anti-pattern** — every one of these silently forks the agent:

```python
experiment_name="txt2sql v3 (claude, ACL>=0.8)"   # variant + config in the name
experiment_name=f"txt2sql-{datetime.now():%Y%m%d}"  # date in the name
experiment_name="check best router model"          # hypothesis in the name
```

To tell runs of one agent apart, use the portal: runs are already distinguished by
timestamp, configuration space, objectives, and results. Do not reach for the name.

- `experiment_name` accepts spaces and punctuation (it is not a Python identifier), but
  prefer a short stable slug.
- Precedence, highest to lowest: explicit `experiment_name` decorator argument;
  `TRAIGENT_EXPERIMENT_NAME` environment variable checked at access time, not decoration
  time; self-describing default built at decoration time as
  `"<func_name>[<obj1>,<obj2>,...][<knob1>,...]"` with at most 4 knobs shown, a
  120-character cap, and deterministic ordering; bare `func.__name__` only when no
  objectives or knobs were registered.
- Because the default is derived from the function name, objectives, and knobs, **adding
  or removing a knob or objective changes the default identity**. If you intend a series
  of runs to share one history while you vary the search space, set `experiment_name`
  explicitly.
- The name is set on the **decorator**, not on the run call — there is no
  `experiment_name` (or `tags`) parameter on `.optimize()` / `.optimize_sync()`.

## Evaluation Setup

Configure how Traigent evaluates each trial using `EvaluationOptions`.

> **The decorated agent function must not accept `expected` as a parameter.**
> Traigent calls your function with the example's *input* fields only (plus any
> config-injected params such as a `config` dict in parameter-injection mode).
> `expected` is the ground-truth label used *exclusively* by the scoring function
> to score the function's output. Including `expected` in the function signature
> causes every trial to fail with `TypeError: missing required argument: 'expected'`.
>
> ```python
> # WRONG — will fail every trial
> def my_agent(query: str, expected: str) -> str: ...
>
> # CORRECT — function takes input fields only; scorer receives (output, expected)
> def my_agent(query: str) -> str: ...
> def score(output: str, expected: str) -> float: ...
> ```

### Fields

| Field | Type | Description |
|---|---|---|
| `eval_dataset` | `str \| list[str] \| Dataset \| None` | Path to JSONL dataset or list of paths |
| `custom_evaluator` | `Callable \| None` | Full-control evaluator: `(func, config, example) -> ExampleResult` |
| `scoring_function` | `Callable \| None` | Lightweight scorer: `(output, expected) -> float` |
| `surrogate_evaluator` | `Callable \| None` | Optional secondary scorer for existing outputs only; it never re-executes the decorated function. |
| `surrogate_evaluator_name` | `str \| None` | Display/evaluator id override for `surrogate_evaluator`; runtime `optimize(surrogate_evaluator_name=...)` can override it. |
| `metric_functions` | `dict[str, Callable] \| None` | Named metrics: `{"accuracy": fn, "relevance": fn}` |

**The evaluator-quality anchor is not a client-side field.** An evaluator-quality audit
(`traigent-eval-audit`) scores your evaluator against an **anchor** — verifiable ground truth
computed independently of that evaluator. The anchor is designated server-side, from the
independent correctness signal registered for the run; you never name one yourself.
`EvaluationOptions` forbids unknown fields, so a task-category kwarg such as
`EvaluationOptions(task_type="exact_match")` raises `ValidationError: Extra inputs are not
permitted` at construction on traigent 0.27.0 — do not pass it. Such a field is expected in a
later SDK release, but it is in no released version. Until then a run with no independent
correctness signal registered resolves to "no anchor" and the audit abstains — a correct
refusal, not a failure.

`surrogate_evaluator` uses the same calling convention as `scoring_function`:
`(output, expected_output=None, example=None) -> float` in `[0, 1]`, or a dict
containing `surrogate_score` or `score`. Its result is stored alongside primary
metrics as `surrogate_score` and feeds the backend's per-evaluator score tensor.
The evaluator id comes from the callable `__name__` or class name, falling back to
`"surrogate"`, unless `surrogate_evaluator_name` or runtime
`optimize(surrogate_evaluator_name=...)` overrides it.

Public API, mechanically supported. A cheap surrogate has **no validated
evaluation-cost benefit**: in Traigent's 3-domain evaluation, a cheap surrogate
judge did not reliably track the authoritative judge; on hard tasks its agreement
collapsed to the anchor base rate. Do not use it as a substitute for the
authoritative evaluator. Quality and promotion decisions remain anchored
server-side.

### When to Use Each

| Approach | Best For | Signature |
|---|---|---|
| `eval_dataset` only | Built-in evaluation with default metrics | N/A (path string) |
| `scoring_function` | Simple pass/fail or numeric scoring | `(output, expected) -> float` |
| `metric_functions` | Multiple named metrics per example | `{"name": (output, expected, input_data) -> float}` |
| `custom_evaluator` | Full control over execution and measurement | `(func, config, example) -> ExampleResult` |

### Example: Scoring Function

```python
def exact_match(output: str, expected: str) -> float:
    return 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="qa_pairs.jsonl",
        scoring_function=exact_match,
    ),
    objectives=["accuracy"],
    configuration_space={"temperature": [0.0, 0.3, 0.7]},
)
def answer(question: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(question, temperature=cfg["temperature"])
```

### Example: Metric Functions

```python
def accuracy_metric(output, expected, input_data) -> float:
    return 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

def length_metric(output, expected, input_data) -> float:
    return min(len(output) / 500, 1.0)

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="test_data.jsonl",
        metric_functions={
            "accuracy": accuracy_metric,
            "brevity": length_metric,
        },
    ),
    objectives=["accuracy"],
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def summarize(text: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(f"Summarize: {text}", model=cfg["model"])
```

## Injection Modes

Injection mode controls how the optimized configuration reaches your function code.

### Context Mode (Default)

The recommended mode. Uses Python `contextvars` for thread-safe config access.

```python
@traigent.optimize(
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str) -> str:
    cfg = traigent.get_config()  # Thread-safe context access
    return prompt_model(query, model=cfg["model"])
```

### Parameter Mode

Passes config as an explicit function parameter. Set `config_param` to the parameter name.

```python
@traigent.optimize(
    injection=InjectionOptions(
        injection_mode="parameter",
        config_param="config",
    ),
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str, config: dict = None) -> str:
    return prompt_model(query, model=config["model"])
```

### Seamless Mode

No `get_config()` call. Traigent rewrites the function's AST per trial — but only **local assignments or parameters whose name equals a configuration key**.

```python
@traigent.optimize(
    injection=InjectionOptions(injection_mode="seamless"),
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.1, 0.5, 0.9],
    },
)
def my_func(query: str) -> str:
    model = "gpt-4o-mini"      # seamless rewrites THIS local assignment per trial
    temperature = 0.5          # a matching local name (or parameter) is required
    return litellm.completion(
        model=model,
        temperature=temperature,
        messages=[{"role": "user", "content": query}],
    )
```

> **A literal in the call is not rewritten.** `model="gpt-4o-mini"` written directly as a keyword argument, a value from `os.environ.get(...)`, or a dict-built kwarg has no matching local name, so the SDK logs `Seamless provider found no injectable targets for <fn>; no local assignment or parameter matched configuration keys [...], so the function ran with original values` and every trial runs the original configuration — and the dry-run still passes (fail-closed behaviour is tracked in Traigent/Traigent#2298). Before any paid run, prove the value reaching the provider call changes across two configurations (mock mode, diff the request); if it does not, use context mode.

> **Mock intercepts this example only because it calls `litellm.completion`.** Mock mode covers LiteLLM/LangChain calls only — a raw `openai` / `anthropic` client in the body makes **real, billable calls even during a "keyless" mock dry-run**. For a genuinely free dry-run of a seamless-mode function, keep `litellm.completion` in the body or run fully offline (`offline=True`, no keys).

## Execution Options

Where and how runs execute is controlled by two public knobs: `algorithm` and `offline`.
See `references/execution-modes.md` for the full reference.

### Tiny Real Cost and KPI Probe

After mock/dry-run validation passes and before any full run, run one tiny **real** optimization: 1-2 dataset examples, minimal trials, and the cheapest candidate model. Check both surfaces: `results.total_cost` must be neither `None` nor `0.0` with real calls (both mean cost is not wired — the provider may still bill), and each trial's `metrics` must contain the declared objectives with non-degenerate values (not all `0.0`/all `1.0`). If either surface fails, wire it before scaling up — see `traigent-optimize-run` → Cost Wiring Probe for the fix ladder (custom model pricing env vars, per-trial cost metrics, `TRAIGENT_STRICT_COST_ACCOUNTING`).

> **Real LLM runs require the user's approval — the SDK's cost handshake is conditional.** It
> prompts only when the pre-run estimate exceeds `TRAIGENT_RUN_COST_LIMIT` (default $2.00) or
> a model is unpriced; a priced run under the cap starts real calls with no prompt. The user's
> explicit yes to a stated ceiling is the gate. Set `TRAIGENT_COST_APPROVED=true` (or
> `cost_approved=True` in the decorator) only in the process of that approved run, never in
> `.env` or a shell profile — it also turns the unpriced-model refusal into a warning. The
> estimate may be high (fallback pricing is conservative); read `results.stop_reason` after
> the run.

```python
@traigent.optimize(
    execution=ExecutionOptions(
        algorithm="auto",        # default: Traigent cloud smart optimizer
        offline=False,           # set True for a local run with no Traigent backend egress
        local_storage_path="./results",
    ),
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
)
def my_func(query: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(query, model=cfg["model"])
```

### `algorithm` and `offline`

| Choice | Behavior |
|---|---|
| `algorithm="auto"` (default) | Traigent cloud smart optimizer proposes trials; your agent/LLM calls run in your environment. Results sync to the portal. |
| `algorithm="grid"` / `"random"` | Local search in the SDK. Results still sync to the portal unless `offline=True`. |
| `algorithm="bayesian"`/`"tpe"`/`"optuna*"`/`"cmaes"`/`"nsga2"` | Named smart selectors execute on connected runs since 0.20.1 (see version-matrix: `smart-selector-exec`): supported names (`bayesian`/`tpe`/`optuna`/`optuna_tpe`/`optuna_random`) bind to the typed backend Optuna strategy on authenticated connected runs; unsupported names (`nsga2`/`cmaes`) fail fast with a capability message (Traigent/Traigent#1752, #1758). Never local: `ConfigurationError` with `offline=True`, `OptimizationError` from the local registry. Use `"auto"` for the default connected smart path; use `"grid"`/`"random"` only for explicit local/offline search. |
| `offline=True` | Fully local, **zero backend egress**. Results are not synced to the portal. |

The synced path sends configuration IDs and numeric metrics for portal result history, not
example inputs/outputs/prompts. Use `offline=True` only when zero backend traffic is required; a
fully no-network run also needs `LITELLM_LOCAL_MODEL_COST_MAP=True` set before `litellm` is imported
(see `references/execution-modes.md`).
To optimize an external HTTP/MCP service, put the service call in your decorated function or
custom evaluator; keep optimization strategy on the same `algorithm`/`offline` knobs.

### Winner-stability rerun — `winner_stability_reps`

`winner_stability_reps` is an opt-in, measured-only rerun of the winning configuration after
selection completes — for reading run-to-run dispersion, never for gating or re-ranking.
**Requires `traigent>=0.27.0`**, which shipped to PyPI on 2026-09-02 (on `0.26.0` and
earlier the option does not exist at all — passing it raises `TypeError` /
`pydantic.ValidationError`). Check the installed `traigent.__version__` before offering it.
Full reference, call forms, defaults, and rejected forms: `references/winner-stability-reps.md`.

## Config Access Lifecycle

Inside the decorated function, read the active config with `traigent.get_config()` — it returns the current trial config during optimization (thread-safe via contextvars) and, after `apply_best_config(results)`, the applied best config. Use `traigent.get_trial_config()` when you want a strict variant that raises `OptimizationStateError` outside an active trial.

For the full lifecycle — the access table (`get_config` / `get_trial_config` / `results.best_config` / `func.current_config`), applying the winner, and the safety check before applying — see `traigent-analyze-results` → Applying Best Config.

## Complete Example

Putting together evaluation, injection, and execution options:

```python
import traigent
from traigent.api.decorators import EvaluationOptions, ExecutionOptions

def exact_match(output: str, expected: str) -> float:
    return 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

@traigent.optimize(
    evaluation=EvaluationOptions(
        eval_dataset="qa_test.jsonl",
        scoring_function=exact_match,
    ),
    execution=ExecutionOptions(
        local_storage_path="./optimization_results",
    ),
    objectives=["accuracy", "cost"],
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.3, 0.7, 1.0],
        "max_tokens": [256, 512, 1024],
    },
)
def answer_question(question: str) -> str:
    cfg = traigent.get_config()
    return prompt_model(
        question,
        model=cfg["model"],
        temperature=cfg["temperature"],
        max_tokens=cfg["max_tokens"],
    )

# Run optimization
results = answer_question.optimize_sync(max_trials=10, algorithm="random")

# Apply best configuration for production
answer_question.apply_best_config(results)

# Use in production
answer = answer_question("What is the capital of France?")
```

## See Also

- `references/evaluation-options.md` - Full EvaluationOptions field reference
- `references/injection-modes.md` - Detailed injection mode comparison
- `references/execution-modes.md` - Full ExecutionOptions field reference
- `references/winner-stability-reps.md` - `winner_stability_reps` opt-in post-selection winner rerun (requires `traigent>=0.27.0`)
- `traigent-eval-build` - Deep evaluator implementation, ExampleResult, custom evaluators, and evaluator templates
- `traigent-eval-choose-metric` - Metric interview and objective selection before decorator wiring
- `traigent-setup-quickstart` - Installation, API-key setup, and first cloud-smart optimization

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
