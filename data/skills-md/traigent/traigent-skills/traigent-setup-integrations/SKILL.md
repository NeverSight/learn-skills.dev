---
name: traigent-setup-integrations
description: "Integrate Traigent with LangChain, LiteLLM, DSPy, and other AI frameworks. Use when importing langchain/litellm/dspy alongside traigent, setting up multi-provider model testing, using auto_override_frameworks, or asking about framework-specific adapter patterns."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: setup
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.6"
---

# Traigent Framework Integrations

## When to Use

Use this skill when:

- Combining Traigent optimization with LangChain, LiteLLM, or DSPy
- Setting up multi-provider model testing (e.g., OpenAI + Anthropic + Google)
- Using `auto_override_frameworks` or `framework_targets` in the decorator
- Writing optimized functions that call framework-specific APIs
- Connecting Traigent results to observability tools (MLflow, Weights & Biases)

## Installation

Install Traigent with framework integration support:

```bash
# All integrations
pip install "traigent[integrations]>=0.19"

# Or install individual frameworks alongside Traigent
pip install "traigent>=0.19" langchain-openai langchain-anthropic
pip install "traigent>=0.19" litellm
pip install "traigent>=0.19" "dspy==3.3.1"
```

> **Pin, don't float, the framework version.** `langchain-openai`/`langchain-anthropic` and `dspy` both
> ship breaking changes across minor releases (LangChain's `langchain-core` interface churn; DSPy has
> moved fast enough that `dspy.LM`, present since 2.5, is not guaranteed stable across 2.x/3.x). An
> unpinned install can silently pick up a version whose import paths or call signatures differ from
> the examples below. Traigent's own `integrations` extra already floors
> `langchain-openai>=1.1.14`/`langchain-anthropic>=0.2.0` (security floors — see `pip show traigent`);
> stay at or above those, e.g. `langchain-openai>=1.1.14,<2`. `dspy` is not part of that extra. The DSPy examples below were
> verified with `dspy==3.3.1` on `traigent==0.27.0`; pin that version, or re-verify the examples
> against the exact `dspy` version you pin before relying on them.

> **Dry-run first.** Before any paid optimization run, dry-run in mock mode (`enable_mock_mode_for_quickstart()`) with **no real provider key**, review the estimated cost, and get explicit user approval. See the `traigent` lifecycle skill for the mandatory dry-run-first / cost-approval workflow. Apply this to every integration example below before running against real providers:
> - LiteLLM examples: `enable_mock_mode_for_quickstart()` is enough.
> - LangChain examples: LangChain clients require a key at construction, so set a non-secret
>   placeholder in the dry-run process only — e.g. `OPENAI_API_KEY=mock-placeholder` (it cannot bill;
>   the calls are intercepted).
> - DSPy examples: mock mode's canned text cannot satisfy DSPy's structured outputs (every trial
>   fails). Dry-run with `dspy.utils.DummyLM([...])` as the LM instead of `dspy.LM(...)` — one dict per
>   call, keyed by the signature's output fields, e.g. `DummyLM([{"answer": "4"}] * 50)`.

## LangChain Integration

Traigent integrates with LangChain by optimizing the model and parameters used inside your chain. The key pattern: get the config from Traigent, then construct your LangChain objects.

### Basic Pattern

```python
import traigent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

@traigent.optimize(
    eval_dataset="questions.jsonl",
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.3, 0.7, 1.0],
    },
    objectives=["accuracy"],
    max_trials=10,
)
def answer_question(question):
    config = traigent.get_config()

    # Create LangChain components using Traigent config
    llm = ChatOpenAI(
        model=config["model"],
        temperature=config["temperature"],
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the question accurately and concisely."),
        ("human", "{question}"),
    ])
    chain = prompt | llm
    response = chain.invoke({"question": question})
    return response.content

results = answer_question.optimize_sync()  # real run — only after dry-run approval
```

### Auto Override Frameworks

> **Released SDK caveat:** on `traigent<=0.27.0` auto-override is a silent no-op — every trial
> constructs the client with the literal values in your code, and the run still ranks the trials
> and reports a `best_config`. Until a release that fixes it, use manual injection (the Basic
> Pattern: build the client from `traigent.get_config()`). Before any paid run, verify in mock mode
> that the constructed client's `model_name` differs across two trials (the preflight in
> [LangChain reference → Verify the override before a paid run](references/langchain.md#verify-the-override-before-a-paid-run)).

> **Auto-override requires `framework_targets`.** Setting `auto_override_frameworks=True` alone does nothing — the SDK gate requires **both** `auto_override_frameworks=True` and an explicit `framework_targets` list. Without `framework_targets`, the override is silently skipped.
>
> **Single-provider only.** Auto-override swaps the **model string** that gets passed to the constructor — it does not swap the **client class**. If your config space mixes OpenAI and Anthropic models but the function only constructs `ChatOpenAI(...)`, the Anthropic trial passes an Anthropic model name to an OpenAI client and gets an invalid-model error. Scope the config space to one provider per override target, or use manual config injection for cross-provider optimization.

```python
@traigent.optimize(
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.5, 1.0],
    },
    objectives=["accuracy"],
    max_trials=6,
    auto_override_frameworks=True,
    framework_targets=["langchain_openai.ChatOpenAI"],  # required
)
def summarize_document(text):
    # ChatOpenAI constructor is intercepted; model and temperature are replaced per trial
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    response = llm.invoke(text)
    return response.content
```

For finer control, use `framework_targets` to specify exactly which classes to override:

```python
@traigent.optimize(
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.5],
    },
    objectives=["accuracy"],
    max_trials=8,
    auto_override_frameworks=True,  # required — framework_targets alone is silently skipped
    framework_targets=["langchain_openai.ChatOpenAI"],
)
def my_chain(input_text):
    llm = ChatOpenAI(model="gpt-4o-mini")  # Will be overridden
    return llm.invoke(input_text).content
```

See [LangChain reference](references/langchain.md) for RAG chain optimization and advanced patterns.

## LiteLLM Multi-Provider

LiteLLM provides a unified `completion()` interface across 100+ LLM providers (OpenAI, Anthropic, Google, OpenRouter, and more). This makes it natural to optimize across providers with Traigent:

> **Verify model IDs are live + priced before a real run.** Provider catalogs change — IDs get
> delisted, renamed, or re-routed to a retired backend. A dead ID causes a 404 or a *degraded*
> trial whose cost stays unpriced ($0.00). The IDs below were valid when written; re-check them
> first: `traigent models --provider <p> --check <id>` catches typos and unknown ID shapes but
> only validates a shipped snapshot with pattern fallback — it cannot detect delisting, so confirm
> the ID is actually live against the provider's live catalog endpoint (e.g.
> `curl -s https://openrouter.ai/api/v1/models` for OpenRouter). Prefer specific
> versioned IDs over `-latest` aliases. See [LiteLLM reference](references/litellm.md#verifying-model-availability) and the `traigent-debugging` skill's "Model 404 / retired endpoint" entry.

> **⚠️ Give reasoning models enough `max_tokens` headroom.** Reasoning models (`gemini-2.5`/`3.x`,
> `gpt-5`, the `o`-series) spend hidden reasoning tokens that count against `max_tokens` *before*
> any answer text is emitted. A cap sized for a normal model (e.g. `256`/`512`) can be fully
> consumed by reasoning, truncating the answer mid-output (`finish_reason=length`), so the more
> capable model silently scores *far below* a cheap non-reasoning one purely as a measurement
> artifact — not a real quality gap. Give reasoning models ample output headroom (**≥1024–2048**);
> the sweep below uses headroom-safe values because its model pool mixes reasoning and
> non-reasoning models — sweep low caps only in a space with no reasoning models. Field-observed:
> `gemini-2.5-pro` at `max_tokens=256` spent 241 tokens on reasoning and emitted a truncated
> query (~23% of the expected output); at `1536` it completed correctly.

```python
import traigent
import litellm

@traigent.optimize(
    eval_dataset="classification_eval.jsonl",
    configuration_space={
        # Re-verify each ID is live + priced first (see note above); examples are illustrative.
        "model": [
            "gpt-4o-mini",          # OpenAI
            "gpt-4o",               # OpenAI
            "claude-3-haiku-20240307",  # Anthropic (versioned, not a -latest alias)
            "claude-3-5-sonnet-20241022",  # Anthropic
            "gemini/gemini-3-flash",    # Google
        ],
        "temperature": [0.0, 0.3, 0.7],
        "max_tokens": [1024, 2048],  # headroom-safe: the pool includes a reasoning model (see note above)
    },
    objectives=["accuracy"],
    max_trials=15,
)
def classify_text(text):
    config = traigent.get_config()

    response = litellm.completion(
        model=config["model"],
        messages=[{"role": "user", "content": f"Classify this text: {text}"}],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
    )
    return response.choices[0].message.content

results = classify_text.optimize_sync()  # real run — only after dry-run approval

# Check cost across providers
for trial in results.successful_trials:
    model = trial.config["model"]
    accuracy = trial.get_metric("accuracy", 0.0)
    print(f"{model}: accuracy={accuracy:.2%}")
```

LiteLLM handles API key routing automatically based on the model prefix. Set provider API keys in environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."      # LiteLLM reads GOOGLE_API_KEY first, then GEMINI_API_KEY (PALM_API_KEY also accepted) for gemini/* models
export OPENROUTER_API_KEY="sk-or-..."  # LiteLLM reads OPENROUTER_API_KEY for openrouter/* models
# Note: an unrelated GOOGLE_API_KEY already in the shell (any Google service) silently wins over GEMINI_API_KEY — unset it or put the Gemini key there
```

See [LiteLLM reference](references/litellm.md) for the full provider list and cost tracking details.

## DSPy Integration

Traigent provides a `DSPyPromptOptimizer` adapter that wraps DSPy's MIPROv2 and BootstrapFewShot optimizers for automatic prompt engineering:

> `method="mipro"` (the constructor default) raises `TypeError: MIPROv2.__init__() got an unexpected
> keyword argument 'requires_permission_to_run'` on `traigent<=0.27.0` with DSPy 2.6/3.x. Pass
> `method="bootstrap"` explicitly until a fixed SDK release.

```python
from traigent.integrations.dspy_adapter import DSPyPromptOptimizer

optimizer = DSPyPromptOptimizer(method="bootstrap")

result = optimizer.optimize_prompt(
    module=my_dspy_module,
    trainset=train_examples,
    metric=accuracy_metric,
)

# Access the optimized module
optimized_module = result.optimized_module
print(f"Best score: {result.best_score}")
print(f"Method: {result.method}")
print(f"Demos: {result.num_demos}")
```

You can also use DSPy modules inside a Traigent-optimized function for model-level optimization:

```python
import traigent
import dspy

@traigent.optimize(
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.5, 1.0],
    },
    objectives=["accuracy"],
    max_trials=6,
)
def dspy_qa(question):
    config = traigent.get_config()
    lm = dspy.LM(config["model"], temperature=config["temperature"])
    with dspy.context(lm=lm):  # not dspy.configure(): trials run on worker threads
        qa = dspy.Predict("question -> answer")
        result = qa(question=question)
    return result.answer
```

> **Use `dspy.context`, not `dspy.configure`, inside the optimized function.** Traigent runs examples
> on worker threads, and DSPy lets only the thread that first configured it call `dspy.configure`.
> Every other thread raises, and those examples score as wrong. A trial fails only if all of its
> examples do, so accuracy is usually just deflated, with no error signal. Module-level
> `dspy.configure(...)` on the main thread is fine.

See [DSPy reference](references/dspy.md) for the full constructor and `optimize_prompt()` parameters and advanced configuration.

## Observability Integrations

### MLflow

Log Traigent optimization results to MLflow for experiment tracking:

```python
import mlflow

results = func.optimize_sync()

with mlflow.start_run():
    mlflow.log_param("algorithm", results.algorithm)
    mlflow.log_param("best_config", results.best_config)
    # Omit unavailable telemetry; explicit checks preserve measured 0.0 values.
    if results.best_score is not None:
        mlflow.log_metric("best_score", results.best_score)
    if results.total_cost is not None:
        mlflow.log_metric("total_cost", results.total_cost)
    mlflow.log_metric("total_trials", len(results.trials))
    mlflow.log_metric("success_rate", results.success_rate)

    for trial in results.successful_trials:
        with mlflow.start_run(nested=True, run_name=trial.trial_id):
            mlflow.log_params(trial.config)
            mlflow.log_metrics(trial.metrics)
```

### Weights & Biases

```python
import wandb

results = func.optimize_sync()

wandb.init(project="traigent-optimization")
for trial in results.trials:
    wandb.log({
        "trial_id": trial.trial_id,
        "status": str(trial.status),
        **trial.config,
        **trial.metrics,
    })
summary = {"best_config": results.best_config}
# Missing telemetry stays absent; explicit checks preserve real 0.0 measurements.
if results.best_score is not None:
    summary["best_score"] = results.best_score
if results.total_cost is not None:
    summary["total_cost"] = results.total_cost
wandb.log(summary)
wandb.finish()
```

## Pattern: The Right Way

When using Traigent with any framework, always follow this order:

1. Get the config from Traigent
2. Create framework objects using that config
3. Execute with those objects

```python
# CORRECT: get config first, then create client
@traigent.optimize(
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"], "temperature": [0.0, 0.5]},
    objectives=["accuracy"],
)
def my_func(text):
    config = traigent.get_config()           # 1. Get config
    llm = ChatOpenAI(                        # 2. Create client with config
        model=config["model"],
        temperature=config["temperature"],
    )
    return llm.invoke(text).content          # 3. Execute
```

Do not create the client outside the function or before getting the config:

```python
# WRONG: client created before config is available
llm = ChatOpenAI(model="gpt-4o-mini")  # Fixed model, Traigent cannot optimize this

@traigent.optimize(...)
def my_func(text):
    return llm.invoke(text).content  # Always uses the same model
```

The exception is when using `auto_override_frameworks=True` with `framework_targets`, which intercepts client construction — but see the released-SDK caveat under Auto Override Frameworks: on `traigent<=0.27.0` it does not apply the trial values.

## Reference Files

- [LangChain Integration Details](references/langchain.md)
- [LiteLLM Multi-Provider Guide](references/litellm.md)
- [DSPy Adapter Reference](references/dspy.md)

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
