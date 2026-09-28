---
name: traigent-optimize-config-space
description: "Define tuned variables, structural knobs, and configuration spaces for Traigent optimization. Use when setting up parameter search spaces, choosing models/temperatures/prompts, designing task-level text2SQL/RAG/multi-hop knobs, using Range/IntRange/Choices/LogRange types, adding constraints, or using factory presets like Range.temperature()."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: optimize
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.9"
---

# Traigent Configuration Space

## When to Use

Use this skill when:

- Defining which parameters to optimize (model, temperature, max_tokens, prompts, etc.)
- Choosing between dict-based and typed parameter definitions
- Designing task-level structural knobs for text2SQL, RAG, multi-hop QA, schema
  context, retrieval strategy, generation paths, few-shot policies,
  self-consistency, or repair policies (see `references/structural-spine.md`)
- Using `Range`, `IntRange`, `Choices`, or `LogRange` for search spaces
- Adding constraints between parameters (e.g., "if model is gpt-4, temperature must be low")
- Using factory presets like `Range.temperature()` or `Choices.model()`
- Bundling parameters and constraints into a `ConfigSpace` object

## Quick Start

The simplest way to define a configuration space is with a dictionary passed to `configuration_space`:

```python
import traigent

@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy"],
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.1, 0.5, 0.9],
        "max_tokens": [256, 512, 1024],
    },
)
def my_function(query: str) -> str:
    config = traigent.get_config()
    # config["model"], config["temperature"], config["max_tokens"]
    ...
```

Lists create categorical choices. Tuples of two numbers create continuous ranges:

```python
configuration_space={
    "model": ["gpt-4o-mini", "gpt-4o"],       # Categorical: pick one
    "temperature": (0.0, 1.0),                  # Continuous float range
    "max_tokens": (100, 4096),                  # Continuous int range (both ints)
    "use_cache": [True, False],                 # Boolean knob: native Python bools
}
```

> **Boolean knobs: use native `[True, False]`, never `["true", "false"]`.** A native bool list
> works directly in the dict shorthand (above) and as `Choices([True, False])`; your function reads
> it back as a real `bool` (`if config["use_cache"]: ...`). **Do not** string-encode a bool as
> `["true", "false"]`: in Python the string `"false"` is **truthy** (`bool("false") is True`), so a
> consumer that does `if config["x"]:` is **silently always True** and the `False` arm of your
> search is never exercised — the optimizer reports both points as identical behaviour and you never
> learn one was a no-op. If a string encoding is unavoidable (legacy specs), the consumer **must**
> decode explicitly: `enabled = config["x"] == "true"`.

## SE-Friendly Typed Parameters

For stronger typing, validation, and constraint support, use the parameter range classes:

```python
from traigent import Range, IntRange, Choices, LogRange
```

Pass them as keyword arguments directly to the decorator:

```python
import traigent
from traigent import Range, IntRange, Choices

@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy", "cost"],
    model=Choices(["gpt-4o-mini", "gpt-4o"]),
    temperature=Range(0.0, 1.0),
    max_tokens=IntRange(100, 4096),
)
def my_function(query: str) -> str:
    config = traigent.get_config()
    ...
```

### Parameter Types

| Class      | Use Case                    | Example                                      |
| ---------- | --------------------------- | -------------------------------------------- |
| `Range`    | Continuous float values     | `Range(0.0, 1.0)`                            |
| `IntRange` | Integer values              | `IntRange(100, 4096)`                         |
| `Choices`  | Categorical selection       | `Choices(["gpt-4o-mini", "gpt-4o"])`         |
| `LogRange` | Log-scale float values      | `LogRange(1e-5, 1e-1)`                        |

### Range Options

```python
# Basic float range
temperature = Range(0.0, 1.0)

# With step size (discretized)
temperature = Range(0.0, 1.0, step=0.1)

# With log-scale sampling
learning_rate = Range(1e-5, 1e-1, log=True)

# With a default value
temperature = Range(0.0, 1.0, default=0.7)
```

### IntRange Options

```python
# Basic integer range
max_tokens = IntRange(100, 4096)

# With step size
batch_size = IntRange(16, 256, step=16)

# With a default
max_tokens = IntRange(100, 4096, default=512)
```

### LogRange

Convenience class for `Range(low, high, log=True)`. Use for parameters that vary over orders of magnitude:

```python
learning_rate = LogRange(1e-5, 1e-1)
regularization = LogRange(0.001, 10.0)
```

### Choices Options

```python
# String choices
model = Choices(["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet-20241022"])

# Boolean choices
use_cot = Choices([True, False], default=True)

# Numeric choices (discrete set)
temperature = Choices([0.0, 0.3, 0.7, 1.0])

# With a default
model = Choices(["gpt-4o-mini", "gpt-4o"], default="gpt-4o-mini")
```

See `references/parameter-types.md` for complete API details.

## Factory Presets

Each parameter type offers factory methods with sensible defaults for common LLM parameters.

### Range Presets

```python
from traigent import Range

# Temperature
temp = Range.temperature()                       # [0.0, 1.0], default 0.7
temp = Range.temperature(conservative=True)      # [0.0, 0.5], default 0.2
temp = Range.temperature(creative=True)          # [0.7, 1.5], default 1.0

# Other LLM parameters
top_p = Range.top_p()                            # [0.1, 1.0], default 0.9
freq_pen = Range.frequency_penalty()             # [0.0, 2.0], default 0.0
pres_pen = Range.presence_penalty()              # [0.0, 2.0], default 0.0

# RAG parameters
threshold = Range.similarity_threshold()         # [0.0, 1.0], default 0.5
mmr = Range.mmr_lambda()                         # [0.0, 1.0], default 0.5
overlap = Range.chunk_overlap_ratio()            # [0.0, 0.5], default 0.1
```

### IntRange Presets

```python
from traigent import IntRange

# Token limits
tokens = IntRange.max_tokens()                   # [256, 1024], step 64, default 512
tokens = IntRange.max_tokens(task="short")       # [50, 256], step 64, default 128
tokens = IntRange.max_tokens(task="long")        # [1024, 4096], step 64, default 2048

# RAG parameters
k = IntRange.k_retrieval()                       # [1, 10], default 3
k = IntRange.k_retrieval(max_k=20)               # [1, 20], default 3
chunk = IntRange.chunk_size()                     # [100, 1000], step 100, default 500
overlap = IntRange.chunk_overlap()                # [0, 200], step 25, default 50
few_shot = IntRange.few_shot_count()              # [0, 10], default 3
batch = IntRange.batch_size()                     # [1, 64], default 16
```

### Choices Presets

```python
from traigent import Choices

# Model selection
model = Choices.model()                                   # Balanced: gpt-4o-mini, gpt-4o, claude-sonnet-4-6
model = Choices.model(provider="openai", tier="fast")     # Fast OpenAI: gpt-4o-mini
model = Choices.model(provider="anthropic", tier="quality")  # Quality Anthropic: claude-opus-4-8

# Prompting and RAG
strategy = Choices.prompting_strategy()           # direct, chain_of_thought, react, self_consistency
ctx_fmt = Choices.context_format()                # bullet, numbered, xml, markdown, json
retriever = Choices.retriever_type()              # similarity, mmr, bm25, hybrid
embedding = Choices.embedding_model()             # text-embedding-3-small, text-embedding-3-large
reranker = Choices.reranker_model()               # none, cohere-rerank-v3, cross-encoder, llm-rerank
```

## Constraints

Constraints define valid parameter combinations. They prevent the optimizer from exploring invalid configurations.

### Lambda Constraints

The simplest form -- pass lambda functions that return `True` for valid configs:

```python
@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy"],
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.1, 0.5, 0.9],
        "max_tokens": [256, 512, 1024],
    },
    constraints=[
        # If model is gpt-4o, temperature must be below 0.8
        lambda config: config["temperature"] < 0.8 if config["model"] == "gpt-4o" else True,
        # Max tokens must be at least 512
        lambda config: config["max_tokens"] >= 512,
    ],
)
def my_function(query: str) -> str:
    ...
```

A lambda that takes a second `metrics` argument is a **post-trial** check. It runs after that
trial has been evaluated (and paid for), receives the trial's own aggregate metrics, and
marks the trial failed if it returns False. Use it to disqualify results, not to limit spend
(use `cost_limit` / `ExecutionBudget` for that). Keys include `accuracy`, `cost` (trial USD),
`response_time_ms` (mean per example), `total_tokens`; `latency` exists only when it is a
declared objective. Default a missing key to fail, not pass:

```python
constraints=[
    lambda config, metrics: metrics.get("cost", float("inf")) <= 0.10,
    lambda config, metrics: metrics.get("response_time_ms", float("inf")) <= 5000,
]
```

### Builder-Style Constraints

For typed parameters, use the builder methods on `Range`, `IntRange`, and `Choices` objects combined with the `implies()` function:

```python
from traigent import Range, IntRange, Choices, implies

model = Choices(["gpt-4o-mini", "gpt-4o"])
temperature = Range(0.0, 1.0)
max_tokens = IntRange(100, 4096)

@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy"],
    model=model,
    temperature=temperature,
    max_tokens=max_tokens,
    constraints=[
        # If model is gpt-4o, temperature must be <= 0.7
        implies(model.equals("gpt-4o"), temperature.lte(0.7)),
        # If model is gpt-4o-mini, max_tokens must be >= 256
        implies(model.equals("gpt-4o-mini"), max_tokens.gte(256)),
    ],
)
def my_function(query: str) -> str:
    ...
```

### Three Syntax Styles for Constraints

All three produce equivalent `Constraint` objects:

```python
from traigent import Range, Choices, implies, when

model = Choices(["gpt-4o-mini", "gpt-4o"])
temp = Range(0.0, 1.0)

# 1. Functional (canonical)
implies(model.equals("gpt-4o"), temp.lte(0.7))

# 2. Operator-based (concise)
model.equals("gpt-4o") >> temp.lte(0.7)

# 3. Fluent (readable)
when(model.equals("gpt-4o")).then(temp.lte(0.7))
```

### Combining Conditions

Use `&` (and), `|` (or), `~` (not) operators to combine conditions:

```python
from traigent import Range, Choices, implies

model = Choices(["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet-20241022"])
temp = Range(0.0, 1.5)
max_tokens = IntRange(100, 4096)

constraints = [
    # If model is gpt-4o AND temperature is high, require many tokens
    implies(
        model.equals("gpt-4o") & temp.gte(0.8),
        max_tokens.gte(1024),
    ),
    # If model is NOT gpt-4o-mini, temperature must be <= 1.0
    implies(
        ~model.equals("gpt-4o-mini"),
        temp.lte(1.0),
    ),
    # If model is gpt-4o OR claude, limit temperature
    implies(
        model.equals("gpt-4o") | model.equals("claude-3-5-sonnet-20241022"),
        temp.lte(0.9),
    ),
]
```

**Operator precedence warning:** Python precedence is `~` > `>>` > `&` > `|`. Always use parentheses when combining `&`/`|` with `>>`:

```python
# Correct
(model.equals("gpt-4o") & temp.lte(0.7)) >> max_tokens.gte(1000)

# Wrong -- evaluates as model.equals("gpt-4o") & (temp.lte(0.7) >> max_tokens.gte(1000))
model.equals("gpt-4o") & temp.lte(0.7) >> max_tokens.gte(1000)
```

See `references/constraints.md` for the full constraint system reference.

## ConfigSpace Object

For complex setups, bundle parameters and constraints into a `ConfigSpace`:

```python
from traigent import Range, IntRange, Choices, implies
from traigent.api.config_space import ConfigSpace

# Define parameters
temperature = Range(0.0, 1.0, name="temperature", unit="ratio")
max_tokens = IntRange(100, 4096, name="max_tokens", unit="tokens")
model = Choices(["gpt-4o-mini", "gpt-4o"], name="model")

# Define constraints
constraints = [
    implies(model.equals("gpt-4o"), temperature.lte(0.7)),
]

# Bundle into ConfigSpace
space = ConfigSpace(
    tvars={"temperature": temperature, "max_tokens": max_tokens, "model": model},
    constraints=constraints,
    description="QA optimization space",
)

# Validate a configuration
result = space.validate({"temperature": 0.5, "max_tokens": 2000, "model": "gpt-4o"})
print(result.is_valid)  # True

# Check satisfiability (are there any valid configs?)
sat = space.check_satisfiability()
print(sat)
# `check_satisfiability()` returns a `SatResult` (frozen dataclass, no truthiness override —
# `bool(sat)` is always True, so never `if sat:`). Check the field instead. The built-in
# validator only enumerates FINITE spaces of up to 10,000 combinations. Choices and IntRange are
# finite (an IntRange step defaults to 1); a Range without `step=` (like `temperature` above) is
# not, and neither is any space above the cap. Either returns SatStatus.UNKNOWN = "not checked".
from traigent_validation import SatStatus

if sat.status is SatStatus.UNSAT:
    # Every finite combination is ruled out, so no trial can ever run. `sat.unsat_core` lists
    # ALL constraint indices (not a minimal core); bisect the constraints to find the conflict.
    # Loosen or drop a constraint (widen a `Range`, remove an `implies`/mutual-exclusion rule)
    # and re-check before wiring the decorator; do not proceed to `@traigent.optimize` with an
    # unsatisfiable space.
    ...
elif sat.status is SatStatus.UNKNOWN:
    # Not proven either way. To actually check, make the space finite AND under the cap. Here that
    # means `Range(0.0, 1.0, step=0.1, ...)` for temperature plus a coarse
    # `IntRange(100, 4096, step=512, ...)` for max_tokens (3,997 values alone keeps it over the
    # cap), which checks 176 combinations and returns SAT. Or spot-check with
    # space.validate({...}) on representative configs.
    ...

# Use with decorator
@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy"],
    configuration_space=space,
)
def my_function(query: str) -> str:
    config = traigent.get_config()
    ...
```

## Common Patterns

### Model Selection with Cost Awareness

```python
from traigent import Range, Choices, implies

model = Choices(["gpt-4o-mini", "gpt-4o"])
temperature = Range(0.0, 1.0)

@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy", "cost"],
    model=model,
    temperature=temperature,
    constraints=[
        implies(model.equals("gpt-4o"), temperature.lte(0.7)),
    ],
)
def answer(question: str) -> str:
    config = traigent.get_config()
    ...
```

### Reasoning-Effort Knobs (native effort parameters)

For models exposing a native effort control (`reasoning_effort` / thinking budgets), treat it as a
categorical knob — with three field-measured rules (same fold, three token budgets incl.
uncapped, plus a same-day paired rerun; measured on real benchmark runs, 2026-07):

1. **Don't assume more effort = more accuracy.** On a task the model already saturates, `high`
   matched `medium` on accuracy (+1.2 pp, statistical noise) while billing ~2× the reasoning
   tokens — and its extra spend concentrated on *defective* eval items (a self-contradictory
   question consumed up to ~3.7K reasoning tokens per call and still failed under every effort).
   Sweep effort as a knob and let the data decide; expect `medium` to win cost-adjusted.
2. **Pair the effort knob with output headroom.** A truncated call
   (`finish_reason == "length"`) scores 0 and corrupts the sweep, so size `max_tokens` above the
   reasoning budget: `≥ 2048` for `low`/`medium`, and — because truncation was still observed at
   `4096` under `high` — `≥ 8192` when `high` is in the space. (Canonical, model/effort-dependent
   floor: `references/parameter-types.md` → "Reasoning models need more than the default
   `max_tokens` range".)
3. **One knob per mechanism.** Don't put a prompt-CoT knob and a native effort knob in the same
   space expecting them to add: prompt-CoT measured as a no-op (+0.4 pp) on a native-reasoning
   model. Redundant knobs waste grid budget and muddy variable-importance readouts.

```python
config_space = {
    "model": ["openrouter/openai/gpt-oss-120b"],
    "reasoning_effort": ["low", "medium", "high"],
    "max_tokens": [8192],          # headroom rule: ≥8192 because "high" is in the space (4096 still truncated)
}
```

### RAG Pipeline Tuning

```python
from traigent import Range, IntRange, Choices

@traigent.optimize(
    eval_dataset="rag_evals.jsonl",
    objectives=["accuracy"],
    model=Choices.model(provider="openai"),
    temperature=Range.temperature(conservative=True),
    k=IntRange.k_retrieval(),
    chunk_size=IntRange.chunk_size(),
    chunk_overlap=IntRange.chunk_overlap(),
    retriever=Choices.retriever_type(),
)
def rag_query(question: str) -> str:
    config = traigent.get_config()
    ...
```

### Multi-Agent Parameters

Assign parameters to specific agents using the `agent` keyword:

```python
from traigent import Range, Choices

@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy"],
    planner_model=Choices(["gpt-4o-mini", "gpt-4o"], agent="planner"),
    planner_temperature=Range(0.0, 0.5, agent="planner"),
    executor_model=Choices(["gpt-4o-mini", "gpt-4o"], agent="executor"),
    executor_temperature=Range(0.5, 1.0, agent="executor"),
)
def multi_agent_workflow(task: str) -> str:
    config = traigent.get_config()
    ...
```

### Temperature Tuning Only

The minimal configuration -- just optimize temperature:

```python
import traigent
from traigent import Range

@traigent.optimize(
    eval_dataset="evals.jsonl",
    objectives=["accuracy"],
    temperature=Range.temperature(),
)
def my_function(query: str) -> str:
    config = traigent.get_config()
    ...
```

## Widening a space after a first small run

Start from what the first run recorded — the space it actually searched and the knobs the function
provably read (the guided first run leaves both under `traigent-runs/`) — and the controls it named
as left out. A control, a knob, and a tuned variable (TVAR) are the same thing here. Widen, then
check three things no scorer can count:

1. **Values too close together are one value** (`temperature: [0.1, 0.115]`); values must be far
   enough apart to change behaviour, not just the field's number.
2. **Two knobs naming one dimension are one knob** — one lever, one name.
3. **A knob the function never reads is not a lever**: prove every key from `traigent.get_config()`
   changes the outgoing request (two configs in mock mode, diff the request dicts) before paying.

Keep the space materially larger than `max_trials` — the guided first run's generated space is 24
configurations under a 12-trial cap; a space the cap nearly exhausts is a grid, not a search. Carry the first run's "control X
seemed to matter" as a hypothesis to test, never a finding to build on.

## Next Steps

You have defined the search space. Now run it:

- **`traigent-optimize-run`** — launch the optimization: algorithm choice (`auto`/`grid`/`random`/cloud-only smart), `max_trials`, cost limits, and the mandatory dry-run-first gate. This is the next lifecycle step (configuration-space → **run-optimization** → analyze-results).
- **`traigent-setup-decorator`** — if you still need to wire evaluation/objectives/injection onto `@traigent.optimize()` before running.

## See Also

- `traigent-boost-agent` — lifecycle driver (dry-run-first / cost-approval mandate)
- `traigent-optimize-run` — run the space you just defined
- `traigent-analyze-results` — read `best_config`/`best_score` and the trade-off after the run

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
