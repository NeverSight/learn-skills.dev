---
name: traigent-debugging
description: "Debug and troubleshoot Traigent optimization issues. Use when encountering CostLimitExceeded, ConfigurationError, OptimizationStateError, ModuleNotFoundError, or when optimization produces unexpected results. Covers mock mode, logging configuration, and common error resolution."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: gate-debug
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.10"
---

# Debugging and Troubleshooting Traigent

## When to Use

Use this skill when:

- An optimization run fails or produces unexpected results
- You encounter a Traigent exception (CostLimitExceeded, ConfigurationError, etc.)
- You need to test without real API keys (mock mode)
- You want to increase logging verbosity for diagnosis
- Your function works standalone but fails during optimization
- Import errors occur due to missing optional dependencies

## Quick Diagnostic

Enable detailed logging to see what Traigent is doing at each step:

```python
import traigent

traigent.configure(logging_level="DEBUG")  # SDK debug output for traigent.* loggers
# ...then define and run the optimization as usual
```

```bash
# Full tracebacks for ConfigurationError (shows raw exception, not user-friendly message)
export TRAIGENT_DEBUG=1
```

`TRAIGENT_LOG_LEVEL` on its own is applied only by `traigent.configure(logging_level=...)`, `traigent.initialize()` and the `traigent` CLI (when set, it overrides the level they are given). In a script that only uses `@traigent.optimize`, exporting it changes LiteLLM's verbosity, not Traigent's. `configure()` reconfigures the root logger; if your application manages its own logging, attach a handler to the `traigent` logger instead (see [Logging Configuration](references/logging-config.md), "Programmatic Logging Configuration"). `TRAIGENT_DEBUG=1` is separate: it only shows raw ConfigurationError tracebacks.

Then run your optimization. Debug output includes:
- Configuration sampling decisions
- Trial execution start/stop/status
- Metric extraction and scoring
- Cost tracking per trial
- Backend communication for cloud smart optimization and portal result sync

## Common Errors

### Invalid API key format (cloud auth)

**When raised**: a cloud run (`algorithm="auto"`/smart optimizers, or any backend sync) fails with `auth: Invalid API key format` / `Cloud brain session creation failed without an allowed connectivity fallback`. The key *is* being read — it just doesn't match the expected **shape** (prefix + length + character set), so this fires *before* any "is this key valid?" backend check. Two common causes:

1. **A paste artifact** on an otherwise-correct Traigent key — a stray leading/trailing space, a newline, or surrounding quotes.
2. **The wrong credential entirely** — most often a **provider key pasted into `TRAIGENT_API_KEY`** (e.g. an OpenAI `sk-proj-…` / `sk-…` key: the `sk-` prefix uses a hyphen, not the `sk_` the validator expects, and the length won't match either), or any non-Traigent token. A provider key belongs in `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / etc., **not** `TRAIGENT_API_KEY`.

(A *correctly-shaped* Traigent key that is revoked or for the wrong tenant fails later with an auth/authorization error, not this format error.)

**Check the key's shape** without revealing it:

```python
import os
k = os.environ["TRAIGENT_API_KEY"]
print(len(k), repr(k[:4]), "HAS-SPACE" if " " in k else "no-space")
```

Valid `TRAIGENT_API_KEY` formats — prefix → exact total length, then only `A–Z a–z 0–9 _ -`:

| Prefix | Length | Kind |
|---|---|---|
| `tg_` | 64 | standard API key |
| `uk_` / `sk_` / `ak_` / `tk_` | 46 | user / service / admin / temporary key |

Any space, wrong length, surrounding quotes, or other character → rejected. Confirm the value is a **Traigent** key (one of the prefixes above), not a provider key; then re-copy it cleanly (nothing before/after it), or trim at the first whitespace.

### Connected run ended local-only (`cloud_url` is None, nothing on the portal)

Read `results.metadata.get("source")` first. `"local_fallback"` means `algorithm="auto"` could not
create a backend session — no key was found in the process, or session creation hit a
connectivity failure, a 5xx, or an HTTP 400 — and the SDK ran a **local** search after one warning
(an unresolvable backend host raises `CloudUrlUnreachableError` instead); `results.metadata["fallback_reason"]` (and, on SDK 0.27.0+,
`["fallback_reason_code"]`) say which. That result is not the managed run: do not present it as
one and do not pay for it again. Set `TRAIGENT_REQUIRE_CLOUD=1` so the next run raises
(`ConfigurationError: Cloud execution is required, but backend session creation failed …`) before
any trial is paid for.

A key the backend **rejects** never falls back — the run stops with a category in the message:

- `invalid API key (HTTP 401 from POST <backend>/keys/validate)` — the `<backend>` URL names the
  server that judged the key. A key issued by another deployment needs `TRAIGENT_BACKEND_URL`
  pointed there (the default is `https://portal.traigent.ai`). A key exported in the shell shadows
  the one in `.env` — `load_dotenv` keeps the process value — so a 401 can be the shell's key, not
  the one you pasted: run once with `env -u TRAIGENT_API_KEY <command>` to tell them apart.
- `insufficient scope (HTTP 403 …)` — a manually created portal key defaults to read-only. Create a
  full-access key in the same project; never register a new account for it.
- `expired API key` / `rate limited` / `edge blocked` — the text is the diagnosis; retrying blindly
  changes nothing.

A run that raised **after** paid trials carries `exc.sync_session_id` (SDK 0.27.0+; below that, take the session id from the run log): `traigent sync <session_id>`
uploads what was logged locally. For a run that returned but did not persist, read
`results.metadata["persistence_status"]` — `traigent-analyze-results` → "Verify the Run Actually
Persisted" owns that table (degraded is kept, failed is synced, neither is re-paid).

### ConfigurationError

**When raised**: Invalid or malformed configuration values, unsupported features, missing required configuration.

Note the two cases below raise **different** exception types, neither of which is
`ConfigurationError` — catch `ValidationError`/`TraigentError`, or a bare `ValueError`
for the empty-space case:

```
# Non-list parameter value:
traigent.utils.exceptions.ValidationError: Validation failed:
configuration_space.model: Parameter must be a list of values or a (min, max) tuple
```

```python
# WRONG: configuration_space values must be lists -> raises ValidationError
@traigent.optimize(
    configuration_space={"model": "gpt-4o-mini"},  # String, not list
)

# CORRECT
@traigent.optimize(
    configuration_space={"model": ["gpt-4o-mini"]},  # List
)
```

```python
# WRONG: empty configuration space -> raises a builtin ValueError
#        ("Configuration space cannot be empty..."), NOT a TraigentError
@traigent.optimize(
    configuration_space={},
)

# CORRECT: at least one parameter to optimize
@traigent.optimize(
    configuration_space={"temperature": [0.0, 0.5, 1.0]},
)
```

Set `TRAIGENT_DEBUG=1` to see the full traceback instead of the clean error message.

### CostLimitExceeded

**When raised**: only **before the first trial**, when the pre-run cost estimate exceeds
`cost_limit` / `TRAIGENT_RUN_COST_LIMIT` and approval was declined (a non-interactive shell without
`TRAIGENT_COST_APPROVED=true`). Nothing was spent. A budget hit **mid-run never raises**:
`optimize_sync()` returns normally with the paid trials kept and `results.stop_reason ==
"cost_limit"` — report that partial result as a result, never as a failure. `CostLimitExceeded`
is an `OptimizationError` subclass (`except OptimizationError` also catches it). Attributes:
`estimated`, `limit`, `accumulated` (reads `0.0` on the pre-run decline).

```
traigent.utils.exceptions.CostLimitExceeded: Cost limit exceeded: estimated $0.52 >= $0.50 USD; spent $0.00
```

**Fixes**:

```python
# Option 1: Increase the cost limit (only after the user approves the higher ceiling;
# it does not help when cost was not measured -- see the next entry)
@traigent.optimize(
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
    cost_limit=2.0,  # $2.00 USD
)

# Option 2: Use cheaper models
@traigent.optimize(
    configuration_space={"model": ["gpt-4o-mini"]},  # Cheaper than gpt-4o
)

# Option 3: Reduce trials
@traigent.optimize(
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"]},
    max_trials=5,  # Fewer trials = lower cost
)
```

**Handling programmatically**:

```python
from traigent.utils.exceptions import CostLimitExceeded

try:
    results = func.optimize_sync()
except CostLimitExceeded as e:
    # Pre-run decline: nothing ran, nothing was spent — take the estimate back to the user.
    print(f"Refused before spending: estimated ${e.estimated or 0:.2f} > limit ${e.limit:.2f}")
    raise
if results.stop_reason == "cost_limit":
    # Mid-run budget hit: the paid trials are in `results`; this is a partial result, not an error.
    print(f"Budget reached after {len(results.successful_trials)} trials — partial result kept")
```

### Run stopped because cost was not measured

**Symptom**: `results.stop_reason == "cost_limit"`, but `results.total_cost` is far below the
cap (often `$0` or `None`), and the stop message says `per-trial cost unknown: fallback trial
limit N reached`.

**Cause**: Traigent could not measure the cost of the model calls, so it stopped on a trial
count instead of dollars. This is not a dollar cap. **Raising `cost_limit` does not help** — a cap
cannot bound cost it cannot see, and your provider still bills those calls. The result carries
warning `COST_UNMEASURED_TRIAL_LIMIT_REACHED` (SDK 0.30.0+).

**Fix**: make the calls measurable, or set `max_trials` explicitly. Route the calls through a
measured client (LangChain sync `.invoke`, non-streaming `litellm.completion` /
`litellm.acompletion`, or Traigent's Bedrock client), or price a gateway/custom model with
`TRAIGENT_CUSTOM_MODEL_PRICING_JSON`. Then rerun a tiny paid probe and confirm
`results.total_cost` is above 0. Or set `max_trials` explicitly (on the decorator, `.optimize()`,
or `.optimize_sync()`) — that is taken as your consent to run unmeasured, up to the size you set
(warning `COST_UNMEASURED_TRIALS_RAN`, SDK 0.30.0+; the default fallback trial limit, raised with
`TRAIGENT_FALLBACK_TRIAL_LIMIT`, otherwise still applies). The full list of measured and
unmeasured calls is in the `traigent-optimize-run` skill's run-cost-and-limits card.

### OptimizationStateError

**When raised**: Accessing configuration in an invalid lifecycle state.

```
traigent.utils.exceptions.OptimizationStateError: Cannot access config outside of optimization trial
```

**Common causes** — note the two distinct failure modes:

```python
# Case A: a bare get_config() with no active trial and nothing applied
traigent.get_config()  # raises OptimizationStateError

# Case B: directly calling a decorated function before optimize()/apply_best_config()
@traigent.optimize(...)
def my_func(text):
    config = traigent.get_config()
    return config["model"]

# The wrapper supplies a (default/empty) config dict, so get_config() itself does NOT
# raise here — but the missing key does:
my_func("hello")  # KeyError: 'model'  (NOT OptimizationStateError)

# CORRECT: run optimization first, then apply
results = my_func.optimize_sync()
my_func.apply_best_config(results)
my_func("hello")  # Works - get_config() returns the applied config
```

`OptimizationStateError` has `current_state` and `expected_states` attributes for diagnostics.

### ProviderValidationError

**When raised**: API key validation fails before optimization starts. Extends ConfigurationError.

```
traigent.utils.exceptions.ProviderValidationError: Provider validation failed:
  - openai: InvalidAPIKey
  - anthropic: MissingAPIKey
```

**Fixes**:

```bash
# Set the correct API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

```bash
# Skip provider validation (if you know keys are valid but validation is failing)
export TRAIGENT_SKIP_PROVIDER_VALIDATION=true
```

Provider validation is controlled by the `TRAIGENT_SKIP_PROVIDER_VALIDATION`
environment variable, not a decorator argument (there is no `validate_providers`
keyword on `@traigent.optimize`).

The `failed_providers` attribute contains a list of `(provider, error_type)` tuples.

### OptimizationError: CI/CD Approval Required

**When raised**: `optimize()` or `optimize_sync()` is running in local/offline mode inside CI
(for example, with `CI=true`) without explicit approval. This applies to mock/offline runs too:
`TRAIGENT_MOCK_LLM` no longer bypasses the CI approval gate by design.

**Fix**: set the purpose-built approval signal in the CI environment for legitimately approved
runs:

```bash
export TRAIGENT_RUN_APPROVED=1
```

This is the required explicit approval, not a bypass. Cloud-mode runs are unaffected because the
gate only applies to local/offline mode.

### Model 404 / Retired Provider Endpoint

**Symptom**: A trial fails with a `404` / "model not found" / "no such model" error from the
provider, or a run *degrades* — one or more trials silently fail or report `$0.00` cost (the ID
isn't in the pricing table) while others succeed. The function and config are fine; the **model
ID is stale**. Provider catalogs change: IDs get delisted, renamed, or quietly re-routed to a
retired backend. Two IDs we have seen go dead: `openrouter/google/gemini-flash-1.5-8b`
(delisted → 404) and `openrouter/anthropic/claude-3.5-haiku` (routes to a retired Bedrock
endpoint → degraded run).

**Fix**: verify the ID against the provider's *live* catalog, then swap any dead ID for a
verified live one:

```bash
# SDK-native shape preflight (no spend): checks ID shape vs a shipped snapshot w/ pattern fallback;
# catches typos/unknown shapes but a retired-but-well-formed ID still passes -- can't detect delisting
traigent models --provider openai
traigent models --provider anthropic --check claude-3-haiku-20240307
```

```bash
# Then confirm liveness against the provider's live catalog -- the authoritative check the
# preflight above can't do (required for providers not covered by `traigent models`, e.g. OpenRouter)
curl -s https://openrouter.ai/api/v1/models | grep -o '"id":"[^"]*"' | sort
```

Prefer a specific versioned ID (e.g. `claude-3-haiku-20240307`) over a moving `-latest` alias —
versioned IDs price reliably; an alias can resolve to a model whose pricing isn't recognized yet,
leaving cost untracked. The `traigent-setup-integrations` skill's
[Verifying model availability](../traigent-setup-integrations/references/litellm.md#verifying-model-availability)
section has the full per-provider check list.

### InvocationError

**When raised**: The decorated function raised an exception during a trial.

```
traigent.utils.exceptions.InvocationError: Function 'classify' failed with config {'model': 'gpt-4o'}
```

Has `config`, `input_data`, and `original_error` attributes. Check the original error:

```python
from traigent.utils.exceptions import InvocationError

try:
    results = func.optimize_sync()
except InvocationError as e:
    print(f"Config that caused failure: {e.config}")
    print(f"Original error: {e.original_error}")
```

### EvaluationError

**When raised**: The evaluator function failed when scoring a trial's output.

```
traigent.utils.exceptions.EvaluationError: Evaluator raised exception for config {'model': 'gpt-4o'}
```

Check your evaluator function handles edge cases (empty output, None, unexpected formats).

### Session-create fails with `400 VALIDATION_ERROR` / `429 quota_exceeded`

**When raised**: A cloud/hybrid run is rejected at session-create because a **plan quota** —
most often `optimization_samples` — has no headroom. Optimization is metered per billing
period along two dimensions: `optimization_samples` (examples evaluated; the usual binding
one) and `optimization_trials` (one session = one trial). A run is admitted only if
`current_usage + (max_trials × dataset_size)` stays under the `optimization_samples` limit;
on the free/hobby tier that limit is small (500), so a few runs can exhaust it and then
**every new run is blocked (0 trials)** until the monthly reset.

The backend's canonical signal is HTTP **429** with `error_code: "quota_exceeded"`, carrying
`resource_type`, `current_usage`, `limit`, and `reset_at`.

**Fixes**:

- Check your remaining quota and the reset date on the portal billing/usage page (or your
  plan's usage summary) before retrying.
- Size the next run to fit: lower `max_trials`, use a smaller eval dataset, or wait for the
  monthly reset. See the `traigent-optimize-run` skill ("Quota & Run Sizing").
- Upgrade the plan if you consistently need more `optimization_samples` headroom.

**Current SDK behavior (re-verified on 0.24.0 and 0.27.0 — may change):**

- A quota block can **surface as a generic `400 VALIDATION_ERROR`** on session-create rather
  than a clean 429, so a run that "looks like bad input" may actually be a quota block. If
  session-create fails right at the start of a cloud run, check quota before assuming the
  config or dataset is malformed.
- A **connected** mock run (`offline=False` with a key) creates a session and consumes
  `optimization_samples` like any other run. An `offline=True` run makes no backend call and
  touches no quota.

### FeatureNotAvailableError

**When raised**: A feature requires an uninstalled plugin or optional dependency.

```
traigent.utils.exceptions.FeatureNotAvailableError: Feature 'LangChain integration' is not available.
  Requires the 'traigent-langchain' plugin. Install with: pip install "traigent[integrations]>=0.19"
```

**Fix**: Install the indicated package.

### ModuleNotFoundError (Python)

**When raised**: Missing optional dependencies.

```
ModuleNotFoundError: No module named 'langchain_openai'
```

**Fix**:

```bash
# Install with specific extras
pip install "traigent[integrations]>=0.19"    # LangChain, LiteLLM support
pip install "traigent[all]>=0.19"             # Everything
pip install "traigent[dev]>=0.19"             # Development tools
```

## Mock Mode

<!-- PROTECTED -->
Test your optimization setup without making real API calls or connecting to the backend. The recommended activation is in-code (production-blocked, visible in code review); the env-var path below remains as a legacy fallback that works in non-production.
<!-- /PROTECTED -->

> **Mock is free of LLM spend. It is free of quota only when `offline=True`** (no backend call is made); a connected mock run (`offline=False` with a key) creates a session and consumes `optimization_samples` (see the quota-exhaustion entry above). And exact/execution-match scorers read a uniform 0.0 under mock — see "Scores are all 0.0" below before concluding the pipeline is broken.

**Recommended (in-code):**

```python
import traigent
from traigent.testing import enable_mock_mode_for_quickstart

enable_mock_mode_for_quickstart()  # raises in production
```

**Legacy fallback (env-var, dev/test only, deprecated):**

`TRAIGENT_MOCK_LLM=true` is deprecated on traigent 0.27.0 (a DeprecationWarning, hidden by default, says it "will be removed in a future release"). Use `traigent.testing.enable_mock_mode_for_quickstart()` in code, e.g. from a pytest fixture/conftest, for new setups.

```bash
# Deprecated: mock LLM responses (no API keys needed) — hard-blocked in production
export TRAIGENT_MOCK_LLM=true
```

A complete keyless dry-run with the in-code API:

```python
import traigent
from traigent.testing import enable_mock_mode_for_quickstart

enable_mock_mode_for_quickstart()

@traigent.optimize(
    eval_dataset="test_data.jsonl",
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"], "temperature": [0.0, 0.5]},
    objectives=["accuracy"],
    max_trials=5,
    offline=True,
)
def my_func(text):
    config = traigent.get_config()
    # LLM calls return mock responses
    return "mock response"

# Runs without API keys, provider calls, or backend egress
results = my_func.optimize_sync()
```

Mock mode is essential for:
- CI/CD pipelines
- Unit testing
- Validating configuration space setup
- Testing evaluator logic

> **Uniform 0.0 scores under mock are expected, not a bug.** The mock LLM returns a single fixed
> string (`"This is a mock response for testing."`), so a deterministic / execution-style scorer
> (exact-match, JSON-schema, SQL execution-accuracy) scores **0.0 on every example × every config**.
> That all-zero board means **mock plumbing is working and your real output is being replaced** —
> it is *not* a broken evaluator, dataset, or config space, and you should **not** debug it as
> "wrong results / low scores" below. Confirm only that the pipeline runs (trials > 0, no failed
> trials), then switch to a real run to see real scores. To get a *non-degenerate* mock board
> without paying for a run, either point the dry-run at an exact-match/identity eval, or have your
> function consult a small mock answer table (the pattern the SDK's own text-to-sql example uses)
> so the dry-run returns plausible-but-fake outputs.

See [Mock Mode reference](references/mock-mode.md) for details.

## Troubleshooting Decision Tree

### No trials ran

1. Check dataset: does the file exist and contain valid JSONL?
2. Check configuration space: is it non-empty with valid lists?
3. Check for ConfigurationError in output
4. Call `traigent.configure(logging_level="DEBUG")` before the run (the env var alone does not reach a decorated run) and check for early failures
5. On a cloud/hybrid run, rule out a plan-quota block before looking further — see "Session-create
   fails with `400 VALIDATION_ERROR` / `429 quota_exceeded`" above; a quota block can present as zero
   trials with no other symptom.

### All trials failed

1. Check API keys: are they set and valid?
2. Check `results.failed_trials` for error messages:
   ```python
   for trial in results.failed_trials:
       print(f"{trial.trial_id}: {trial.error_message}")
   ```
3. Test your function standalone (outside optimization) with a sample config
4. Check provider status pages for outages
5. Check for a stale/dead model ID (404 or `$0.00` unpriced trials) — verify with `traigent models --provider <p> --check <id>` and swap any delisted/renamed ID (see "Model 404 / Retired Provider Endpoint" above)

### Wrong results (low scores)

0. **Are you in mock mode?** If scores are **uniformly 0.0 / identical** and `TRAIGENT_MOCK_LLM`
   or `enable_mock_mode_for_quickstart()` is active, stop — that is the constant mock string, not
   a real result (see the Mock Mode note above). Re-run without mock before debugging the items below.
0b. **Uniform 0.0 / 1.0 on a REAL run?** Stop paying. Print the raw model output and the value the
   scorer actually received for two rows, and run every gold answer through the scorer once: a parse
   bug (a markdown fence the comparator never strips) or a degenerate gold (empty, unparseable)
   scores every configuration the same, and more trials cannot separate what the scorer cannot.
1. Check your evaluator: does it correctly score good vs bad outputs?
2. Check your dataset: are expected outputs correct?
3. Check configuration space: does it include good model/parameter combinations?
4. Check `results.best_metrics` and compare with manual testing
5. Look at individual trial scores:
   ```python
   for trial in results.successful_trials:
       print(f"{trial.config} -> {trial.metrics}")
   ```

### Cost too high

1. Reduce `max_trials` to limit total API calls
2. Set a `cost_limit` on the decorator
3. Use cheaper models in the configuration space (e.g., `gpt-4o-mini` instead of `gpt-4o`)
4. Reduce dataset size for initial exploration
5. Check `results.experiment_stats.cost_per_configuration` to identify expensive configs

### Optimization is slow

1. Check trial durations: `results.experiment_stats.average_trial_duration`
2. Reduce dataset size for faster feedback
3. Set a `timeout` on the run call (`func.optimize_sync(timeout=30)` / `await func.optimize(timeout=30)`) — it is not a decorator argument
4. Use smaller models for initial exploration
5. Reduce `max_trials` or configuration space size

## Environment Verification

Verify your Traigent installation and environment:

```bash
# Check Traigent version and configuration
traigent info

# Validate a dataset file
traigent validate dataset.jsonl
```

From Python:

```python
import traigent
print(traigent.__version__)

# Check common diagnostic environment settings
import os
from traigent.testing import is_mock_mode_enabled
print(f"Mock mode (in code): {is_mock_mode_enabled()}")
print(f"TRAIGENT_MOCK_LLM (deprecated env var): {os.getenv('TRAIGENT_MOCK_LLM', 'unset')}")
import logging
print("traigent log level:", logging.getLevelName(logging.getLogger("traigent").getEffectiveLevel()))
```

## Graceful Fallback Pattern

When optimization might fail, use a try/except pattern with a known-good default:

```python
import traigent
from traigent.utils.exceptions import TraigentError, CostLimitExceeded

DEFAULT_CONFIG = {"model": "gpt-4o-mini", "temperature": 0.0}

@traigent.optimize(
    eval_dataset="eval_data.jsonl",
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o"],
        "temperature": [0.0, 0.3, 0.7],
    },
    objectives=["accuracy"],
    max_trials=10,
)
def classify(text):
    config = traigent.get_config()
    # ... LLM call ...
    return result

# Attempt optimization with fallback
try:
    results = classify.optimize_sync()

    if results.best_score is not None and results.best_score >= 0.7:
        classify.apply_best_config(results)
        print(f"Applied optimized config: {results.best_config}")
    else:
        print(f"Score {results.best_score} too low, using default config")

except CostLimitExceeded as e:
    # Pre-run decline only: nothing ran. A mid-run budget hit does not land here — it returns
    # normally with results.stop_reason == "cost_limit" and the paid trials kept.
    print(f"Refused before spending (estimate ${e.estimated or 0:.2f} > ${e.limit:.2f}), using default config")

except TraigentError as e:
    print(f"Optimization failed: {e.message}, using default config")

# The function still works with either applied or default config
```

This pattern ensures your application remains functional even when optimization encounters problems.

## Reference Files

- [Complete Error Reference](references/error-reference.md)
- [Mock Mode Details](references/mock-mode.md)
- [Logging Configuration](references/logging-config.md)

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
