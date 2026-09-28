---
name: traigent-analyze-results
description: "Analyze and report Traigent optimization results from the terminal — without opening the portal's tabs. Use when a user asks to analyze a run, 'how did my run do?', 'analyze my latest run in project X', what the winner is, or to read result fields, reports, leaderboards, Pareto trade-offs, correlations, or parameter/example insights. Decision questions route to `traigent-analyze-guidance` (Mode B for portal-tracked runs, Mode C for offline/local). Also covers the local OptimizationResult object: reading results.best_config, comparing trials, checking stop_reason, automatic best-config application, candidate export, accessing total_cost or total_tokens, or understanding why optimization stopped."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: analyze
  traigent-maturity: stable
  author: Nimrod
  version: "1.1.25"
---

# Analyzing Traigent Optimization Results

This skill makes optimization-result analysis **terminal-first**. Instead of navigating the
portal's many tabs, ask in plain language ("how did my latest run in project X do?") and the
skill calls the `traigent-analytics` MCP server, then narrates the answer: a headline, a
confidence label, a few evidence bullets, and a portal deep-link as a fallback. It surfaces a
deeper view (Pareto, leaderboard, correlation,
parameter/example insights) only when the brief's evidence/action calls for it or you ask.

There are two surfaces, and this skill covers both:

- **Cloud / portal run (terminal-first, the default below).** A run that lives in the
  Traigent cloud — analyzed through the `traigent-analytics` MCP tools.
- **In-process `OptimizationResult` object.** The value `optimize_sync()` /
  `await optimize()` returns in your own Python process — analyzed field-by-field (the
  "Working with the local OptimizationResult" section).

## When to Use

Requires `traigent>=0.24.0` (the `traigent local sync` flow used below shipped in 0.20.0).

Use this skill when you want to understand a finished run. This covers:

- "Analyze my latest run in project X" / "how did my run do?"
- Getting the one-line verdict, confidence, and evidence summary for a run
- Pulling a focused drilldown (Pareto, leaderboard, correlations, parameter- or
  example-insights) directly via its registered tool, with the portal deep-link for
  interactive exploration
- Reading the best configuration and score
- Comparing individual trial results
- Understanding why optimization stopped (stop reasons)
- Checking cost and token usage
- Applying the best configuration for production use
- Reviewing optimization history across multiple runs

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

**This skill's part:** turn a finished run into exactly one machine-verifiable receipt — a
winner, a no-gain, or an insufficient-evidence result. A narrative is not a receipt, and the
agent that proposed a run cannot validate its own.

**Mandatory whenever you relay any of it:** show the options, recommend exactly one, and
explain **why in the user's own numbers** — their agent, their volumes, their error costs. The
explanation is a product requirement, not decoration.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval before any
paid run**, an explicit spend cap, and the recorded stop rule. The service sets
*how much* to invest; it never affects *whether* approval is required — it always is.

## Terminal-First Analysis (MCP)

When the run lives in the Traigent cloud/portal, drive the analysis through the
`traigent-analytics` MCP server. **This skill orchestrates and narrates; it does not compute
analytics and does not do any auth or tenant logic** — the MCP server resolves the caller's
tenant from the authenticated session and returns backend-produced analytics payloads. Treat
every tool response as authoritative and never invent fields, numbers, rankings, or charts.

### Prerequisites (one time)

The server ships with the SDK as the `traigent-analytics-mcp` command, but it needs the `mcp`
extra: on an install without it, the command exits with an install hint. The `recommended` and
`all` extras already include it, and pandas for the dataframe recipes below.

```bash
pip install "traigent[mcp,analytics]>=0.19"   # or "traigent[recommended]>=0.19", which includes both
traigent auth login                           # or export TRAIGENT_API_KEY; the server reuses these credentials
```

Register the stdio server with your coding assistant under the name `traigent-analytics`, command
`traigent-analytics-mcp` (an `mcpServers` entry in your assistant's MCP config, or its `mcp add`
command). If the SDK is installed in a virtualenv, use that environment's absolute path to
`traigent-analytics-mcp`:

```json
{"mcpServers": {"traigent-analytics": {"command": "traigent-analytics-mcp"}}}
```

Confirm the `analytics_*` tools are listed before calling the brief (the server's `health_check`
and `auth_status` tools report readiness and masked credentials without a network call). If they
are not listed, treat the server as unreachable (step 2): use the portal deep-link.

### 1. Collect explicit project + run context

Before calling anything, pin down **which project and which run**. Never assume a global
"latest" — "latest" is only meaningful inside one project.

- If the user named a project but not a run, ask for the run (or confirm "the most recent
  run in project X" explicitly with them) before proceeding.
- If neither is given, ask which project first.

Keep these as opaque ids the user provides; the skill does not guess or enumerate them.

If the portal shows several optimization runs together as a cohort/group, treat that as
browsing help only. The group is formed from source ids for runs that share the same agent and
canonical dataset; it does not merge configurations, dedupe by tuned variables/objectives/config
hashes, or create one analytics run. Analytics stay scoped to one explicit `run_id`, or to an
explicit `run_ids` list when the user asks to compare runs (see the Multi-Run View section for
the source-preserving cohort table).

### 2. Call the analytics brief first (progressive disclosure)

The keystone tool returns an already-computed backend brief. Call it first and lead with
its headline, confidence, evidence, and any backend-reported action fields — do **not** open a
drilldown yet.

```text
analytics_get_run_decision_brief(
    project_id = "<the project the user named>",
    run_id     = "<the run the user named>",
    intent     = "iterate" | "deploy" | "debug" | "report",
)
```

Use `deploy` for reading deployment-relevant result fields, `debug` for "why is it stuck?",
`report` for a summary/report request, and `iterate` only when you are inspecting the backend's
analysis payload without deciding the next run.

**If the call itself fails or the `traigent-analytics` MCP server is unreachable** (as opposed to
the tool returning `ok=False` or an empty payload for a real portal run), do not retry it silently
or fabricate a brief. For a local/offline run this is expected — go straight to the "Working with
the local OptimizationResult" section below. For a portal-tracked run, say the analytics service is
unreachable and fall back to the portal deep-link.

Decision questions are out of scope for this read-only analysis skill. Route open-ended
next-step decisions to `traigent-analyze-guidance`: Mode B for portal-tracked runs (it fetches the
same backend decision brief, `analytics_get_run_decision_brief`, with the decision-making protocol
around it), Mode C for offline/local runs or unavailable service payloads.

The tool returns an `ok` flag and a `decision_brief` object. Narrate the brief in this order:

1. **Headline** — the one-sentence verdict, in plain language.
2. **Confidence** — the brief's `confidence`. Never upgrade a `low`/`medium` confidence
   into a stronger claim.
3. **Evidence** — the `summary` strings from the brief's `evidence` list.
4. **Backend-reported action fields** — `recommended_action.kind`, optional `config_id`, and
   `why`, if present. Report these fields as analysis output; do not turn them into this skill's
   decision.
5. **Fallback** — build a navigation-only portal link:
   `https://portal.traigent.ai/p/<project_id>/runs/<run_id>`.

The brief knows the numbers, not where the data came from: a run whose dataset, evaluator, or agent
was a generated substitute (check the project's own run record) is
walkthrough evidence — say so before the headline and keep that disclosure attached to every number
quoted from it.

### 3. Pull one drilldown only when the brief or user asks

The brief may include `drilldowns`. The single-run drilldown fetchers are registered
(SDK >= 0.18.0.dev0), so a `drilldowns[].tool` that names one of the registered tools below can
be called directly. Pull at most **one** extra tool per turn, and only when the user asks or the
brief clearly calls for it. Use the portal deep-link for interactive exploration or for any view
that has no registered tool.

The analytics tools this skill may call are:

- `analytics_get_run_decision_brief(project_id, run_id, intent="iterate")`
- `analytics_get_run_report(project_id, run_id)`
- `analytics_get_project_overview(project_id)`
- `analytics_compare_runs(project_id, run_ids)`
- `analytics_list_experiment_groups(project_id, agent_id=None, dataset_id=None)` — requires an SDK build that exposes the experiment-group analytics tools; if absent, fall back to `analytics_compare_runs` for explicit `run_ids` or the portal.
- `analytics_get_experiment_group(project_id, group_id)` — same experiment-group tool gate.
- `analytics_list_experiment_group_configuration_runs(project_id, group_id)` — same experiment-group tool gate.
- `analytics_get_single_run_pareto(project_id, run_id, x_measure="cost", y_measure="quality", request_count=1)`
- `analytics_get_correlation_matrix(project_id, run_id, method="pearson", min_sample=3)`
- `analytics_get_run_leaderboard(project_id, run_id, objective="weighted", weights=None, constraints=None, request_count=1, limit=50)`
- `analytics_get_parameter_insights(project_id, run_id, target_measure="quality", min_trials=10, top_k=10)`
- `analytics_get_example_insights(project_id, run_id)`
- `analytics_render_chart(payload, kind, output_path=None)` with `kind` in
  `{run_pareto, run_correlations}`

Do not call any other analytics tool name. The render tool does not fetch or compute a
drilldown; it renders an already-fetched backend payload. Call it only when you already have a
backend-produced `run_pareto` or `run_correlations` object from a registered tool response.
If the payload is absent, use the portal deep-link instead.

| Symptom / requested view | First surface (only if triggered / asked) | Reported signal / handoff |
|---|---|---|
| Clean winner | (none — headline is enough) | Report the winner and route promotion decisions to `traigent-analyze-guidance` or `traigent-ci-safety-gate` |
| Expensive winner / Pareto trade-off | `analytics_get_single_run_pareto`, then `analytics_render_chart` with `kind="run_pareto"` to draw it | Report the trade-off; route operating-point decisions to `traigent-analyze-guidance` for portal runs |
| Dominated winner / leaderboard | `analytics_get_run_leaderboard` | Report the dominating config; route the next-step decision to `traigent-analyze-guidance` |
| Low trials | (none — state low confidence) | Report low confidence; route more-trials decisions to `traigent-analyze-guidance` (Mode B portal, Mode C offline/local) |
| One knob dominates | `analytics_get_parameter_insights` | Report the dominant knob; route space changes to `traigent-analyze-guidance` (Mode B portal, Mode C offline/local) |
| Flat scores | `analytics_get_parameter_insights` | Report flatness; route dataset/space decisions to `traigent-analyze-guidance` (Mode B portal, Mode C offline/local) |
| Noisy examples | `analytics_get_example_insights` (safe projection) | Report the safe projection; route evaluator/data changes to `traigent-analyze-guidance` (Mode B portal, Mode C offline/local) |
| Cost blowup | `analytics_get_single_run_pareto` (+ render `kind="run_pareto"`) | Report cost evidence; route budget/guardrail decisions to `traigent-analyze-guidance` or `traigent-ci-safety-gate` |

For the full tool contract (every tool's arguments and response shape and the geometry-vs-words
rule), see
[references/mcp-analytics-tools.md](references/mcp-analytics-tools.md). For choosing the
*next experiment* once analysis names the problem, hand off to `traigent-analyze-guidance`
(Mode B for portal-tracked runs, Mode C for offline/local).

### 4. Multi-Run View (Cohort Table)

When the user asks for multi-run, history, "across my runs", or cohort results for one
agent+dataset, use the experiment-group view. Requires an SDK build that exposes the
experiment-group analytics tools; if they are absent, fall back to `analytics_compare_runs` for
explicit `run_ids` or the portal.

Call the cohort tools in this order:

```text
analytics_list_experiment_groups(project_id, agent_id=None, dataset_id=None)
analytics_get_experiment_group(project_id, group_id)
analytics_list_experiment_group_configuration_runs(project_id, group_id)
```

Each cohort tool is a thin reader over a read-only backend endpoint (viewer role, paginated
where it lists):

- `analytics_list_experiment_groups` / `GET /api/v1/experiment-groups` — list cohorts,
  optionally filtered by `agent_id` and `dataset_id` query params.
- `analytics_get_experiment_group` / `GET /api/v1/experiment-groups/{group_id}` — one cohort's
  summary (404 when the group is not visible in your scope).
- `analytics_list_experiment_group_configuration_runs` /
  `GET /api/v1/experiment-groups/{group_id}/configuration-runs` — the cohort's
  configuration-run rows, source ids preserved.

Present **one** aggregated table labelled:

`grouped by agent+dataset — rows remain individual source runs`

Rows are configuration-runs across the cohort's runs. Include these columns when present:
`experiment_run_id`, `configuration_run_id`, `trial_number`, key configuration parameters, key
measures such as accuracy/score, cost, and latency (bare `latency` is milliseconds on SDKs
after 0.22.0 — see version-matrix: `latency-unit`), `status`, and `timestamp`. Keep source ids
visible in every row; join on ids and never deduplicate by configuration hash.

This is a presentation aggregation over source rows, not a merged analytics identity. The portal
GROUP is browsing help and never a merged analytics run. Per-run analytics still go through the
single-run tools above.

<!-- PROTECTED -->
### Privacy: narrate findings, not raw example values

The example-insights drilldown (`analytics_get_example_insights`) is registered, but it is
**privacy-bounded**: the backend returns scoring metadata only — coarse counts, cohort labels,
redacted example refs, dataset-quality buckets, and templated recommendations.
It must never expose proprietary difficulty, informativeness, ambiguity, or latent feature-vector
values. Do not request, infer, or print such values, and do not paste raw per-example payloads
into the conversation.
<!-- /PROTECTED -->

### Tool availability

Registered (SDK >= 0.18.0.dev0): `analytics_get_run_decision_brief`,
`analytics_get_run_report`, `analytics_get_project_overview`, `analytics_compare_runs`,
`analytics_get_single_run_pareto`, `analytics_get_correlation_matrix`,
`analytics_get_run_leaderboard`, `analytics_get_parameter_insights`,
`analytics_get_example_insights`, and `analytics_render_chart`.

Experiment-group tools: `analytics_list_experiment_groups`,
`analytics_get_experiment_group`, and `analytics_list_experiment_group_configuration_runs`.
Requires an SDK build that exposes the experiment-group analytics tools; if absent, fall back to
`analytics_compare_runs` for explicit `run_ids` or the portal.

The portal deep-link is a fallback for interactive exploration (hover / zoom / filter) or any
view without a registered tool. Treat every tool response as authoritative; never fabricate
output, charts, rankings, or field behavior, and do not call an unlisted analytics tool name.

## Working with the local OptimizationResult

The rest of this skill covers the in-process `OptimizationResult` object returned by
`optimize_sync()` (or `await optimize()`) when you analyze a run inside your own Python
program rather than from the cloud. The same outcomes — best config, trials, stop reason,
cost — read directly off the returned object.

## Quick Results

After running optimization, the `OptimizationResult` object provides immediate access to the key outcomes:

```python
import traigent

@traigent.optimize(
    eval_dataset="eval_data.jsonl",
    configuration_space={"model": ["gpt-4o-mini", "gpt-4o"], "temperature": [0.0, 0.5, 1.0]},
    objectives=["accuracy"],
    max_trials=10,
)
def classify(text):
    config = traigent.get_config()
    # ... LLM call using config ...
    return result

results = classify.optimize_sync()

# Top-level results
print(results.best_config)      # {"model": "gpt-4o", "temperature": 0.0}
print(results.best_score)       # 0.92 (float or None if no eligible trial)
print(results.stop_reason)      # "max_trials_reached"
print(results.duration)         # 45.3 (seconds, wall-clock)
print(results.status)           # OptimizationStatus.COMPLETED
print(results.algorithm)        # Name of optimization algorithm used
print(results.optimization_id)  # Unique ID for this run
print(results.objectives)       # ["accuracy"]
print(results.timestamp)        # datetime when optimization completed
```

> **Identifying a run in the portal.** `experiment_name` (set on the decorator, or the
> access-time `TRAIGENT_EXPERIMENT_NAME` env var, then the deterministic self-describing
> default `"<func_name>[<obj1>,<obj2>,...][<knob1>,...]"`, then bare `func.__name__`) names
> the **agent**, not the individual run — the portal groups optimization history by
> (agent, evaluation dataset). Keep it **stable across runs**; giving each run its own name
> splits that history into one-run fragments. Find a specific run by
> `results.experiment_run_id`; `results.experiment_id` identifies only its experiment group.
> Treat `results.cloud_url` as exact only when its query contains the matching
> `run_id=<experiment_run_id>`; otherwise open the group and select that run ID. Use the timestamp
> for chronology, not identity, and do not name each run separately.
> The current SDK has no `tags`/`metadata` argument.
> See `traigent-setup-decorator` -> "Naming: `experiment_name` identifies the agent, not the run".

`best_score` is `None` when no trial produced a valid score (e.g., all trials failed). Always check before comparing:

```python
if results.best_score is not None:
    print(f"Best accuracy: {results.best_score:.2%}")
else:
    print("No successful trials produced a score")
```

## Reading Trials

Each trial in `results.trials` is a `TrialResult` with full details about what happened:

```python
for trial in results.trials:
    print(f"Trial {trial.trial_id}")
    print(f"  Config: {trial.config}")
    print(f"  Status: {trial.status}")        # TrialStatus enum
    print(f"  Duration: {trial.duration:.1f}s")
    print(f"  Metrics: {trial.metrics}")       # {"accuracy": 0.85, "latency": 1200.0}  # latency in ms on SDKs after 0.22.0 (see version-matrix: latency-unit)
    print(f"  Successful: {trial.is_successful}")
    print(f"  Timestamp: {trial.timestamp}")

    # Safe metric access with default
    accuracy = trial.get_metric("accuracy", default=0.0)
    latency = trial.get_metric("latency", default=None)  # ms on SDKs after 0.22.0 (see version-matrix: latency-unit)

    # Check for errors
    if trial.error_message:
        print(f"  Error: {trial.error_message}")

    # Trial metadata (additional context)
    if trial.metadata:
        print(f"  Metadata: {trial.metadata}")
```

### Filtering Trials

Use the built-in properties to filter trials by outcome:

```python
# Only successful trials
for trial in results.successful_trials:
    print(f"{trial.config} -> accuracy={trial.get_metric('accuracy')}")

# Only failed trials
for trial in results.failed_trials:
    print(f"FAILED: {trial.config} -> {trial.error_message}")

# Success rate
print(f"Success rate: {results.success_rate:.0%}")
# e.g., "Success rate: 80%"
```

### Comparing Trial Configurations

Find which configuration parameters matter most:

```python
# Sort trials by a specific metric
sorted_trials = sorted(
    results.successful_trials,
    key=lambda t: t.get_metric("accuracy", 0.0),
    reverse=True,
)

# Show top 3
for i, trial in enumerate(sorted_trials[:3], 1):
    print(f"#{i}: accuracy={trial.get_metric('accuracy'):.3f} config={trial.config}")

# Compare best vs worst
if len(sorted_trials) >= 2:
    best = sorted_trials[0]
    worst = sorted_trials[-1]
    for key in best.config:
        if best.config[key] != worst.config[key]:
            print(f"  {key}: best={best.config[key]}, worst={worst.config[key]}")
```

### Is the Delta Real? Rerun Noise, Paired Comparisons, and Non-Portable Winners

Before reporting any config-A-vs-config-B difference, know the noise floor — field-measured on
real benchmark runs (2026-07): **the same config on the same data, nothing changed,
moved ±5–10 pp across days at n=40 examples per cell** (one cell measured 82.5 → 87.5 → 95.0
across three passes). Three rules follow:

1. **Resolution rule:** rerun noise follows a √k law — the same-config SD is ≈ `50/√k` pp at
   p≈0.5 (≈8 pp at k=40, consistent with the ±5–10 pp above), so a k-example evaluation resolves
   only gaps several times that. Marginal means pooled over ≥4 cells (n ≥ 160) roughly halve the
   noise (4× the samples → √4 = 2× tighter); single-cell deltas under ~10 pp are unreportable.
2. **Pair, don't cross-compare:** never compare numbers measured in different sessions/days.
   Case study: an apparent 12-pp effort-knob gap dissolved to +1.2 pp (2 answers in 160 — noise)
   once both sides were rerun same-day on the same fold. Cross-day deltas were the artifact.
3. **Ship deltas with a bootstrap CI** over held-out examples (≥1,000 resamples); a win is
   claimable only if the CI excludes zero. The same skepticism applies to public leaderboard
   gaps of a few points.

**Read the SDK's own winner verdict before any local delta test (SDK >= 0.26.0).**
`results.best_config_margin` qualifies `best_config` without changing it: a paired test of the
winner against the best *distinct* runner-up on their shared per-example scores (McNemar exact for
0/1 scorers, paired t otherwise), Bonferroni-corrected for having picked the best of `n_configs` —
the selection effect that inflates `best_score`. Read `verdict`: `"clear"` = the winner beats the
runner-up at `effective_alpha`; `"statistical_tie"` = report a tie, whatever `best_score` says;
`"na"` = no paired data (needs >= 5 shared examples; `reason` says why). The payload also carries
`delta`, `ci95`, `p_value`, `n_shared_examples`, `runner_up`, `n_configs`. `None` means there was no
runner-up. This is the paired delta and interval the winner receipt asks for; never upgrade a tie
into a win.

**Winning configs do not port across model families.** Identical knob grids on two families kept
the knob *ranking* but flipped the *optimum* (one model peaked with full schema context; the
other did better on the compact variant — full slightly hurt it). Re-optimize per model; never
copy a winner onto a new model and report the old score.

### Per-Example Diagnostics: Your Eval Set Is Also Under Test

Across N trials every eval row gets scored N times — which makes the run itself an audit of the
dataset, at zero additional API cost. Two independent signals (both field-validated 2026-07):

- **Variance flags.** The portal's Deterministic Insights flag rows whose pass/fail flips in
  ways overall trial quality doesn't explain ("high variance unexplained by trial quality").
  Read them as: *this row's verdict can't be trusted for this model*. On inspection a subset is
  intrinsically defective (one flagged row's gold answered a different question than asked, and
  replicated as unstable on a second model family); the rest are model-specific instability.
  Treat the two causes differently: fix or drop **only** rows confirmed as defective gold (wrong
  or ambiguous, replicated across model families). **Keep** the model-instability rows in the set
  and report them as an instability signal — those are exactly where the model is weak, so
  deleting them before a promotion decision cherry-picks the easy items and inflates the promoted
  score.
- **Token-runaway.** A row that hits the token cap (`finish_reason == "length"`) or burns
  outlier reasoning tokens under *every* config is usually a broken item (ambiguous or
  self-contradictory) — one such row was later confirmed removed by GSM8K-Platinum's expert
  audit. Report it as a dataset fix, not a model problem.

Mapping trap: the SDK keys rows as `example_{<0-based row index in the eval_dataset file>}`
(`traigent/evaluators/base.py`). The portal's separate `example_num` field has undefined
semantics — map flags back to your dataset via `example_id`, never `example_num`. Built-in
evaluators emit those `example_{index}` keys automatically; a custom evaluator should set
`example_id` to a real per-row id (e.g. `example.metadata.get("id", index)`) so the two keyings
line up.

**Run the SDK's free local audit before reading portal flags (SDK >= 0.24.0).** `results.eval_audit`
is computed only when read, makes no calls, and is `None` when the run captured no per-example
detail or spanned fewer than two configurations:

```python
audit = results.eval_audit
if audit is not None:
    for flag in audit.flagged:   # never-correct, token-leak, cross-family-consensus-on-wrong
        print(flag.example_id, flag.detectors, flag.suggested_answer)
```

A never-correct row is a suspect *expectation* before it is a model failure; `suggested_answer` is
set only where unrelated model families agreed on the same non-gold output. `results.example_matrix`
is the per-example × per-trial grid behind it (two trials of one config are two columns). Do not call `results.analyze()`: it needs the
separate tuned-variables plugin, which the SDK does not install, and raises `ImportError`
without it.

### Configuration Insights

Use `get_optimization_insights(results)` for a first structured pass over top configurations,
performance summary, parameter insights, and recommendations. Treat it as analysis input; deciding
the next experiment belongs in `traigent-analyze-guidance` (Mode B for portal-tracked runs, Mode C
for offline/local runs).

```python
from traigent.utils.insights import get_optimization_insights

insights = get_optimization_insights(results)
print(insights.get("top_configurations", []))
print(insights.get("performance_summary", {}))
print(insights.get("parameter_insights", {}))
print(insights.get("recommendations", []))
```

## Cost and Performance

Track what the optimization run cost in API spend and tokens:

```python
# Total cost across all trials (None if not tracked)
if results.total_cost is not None:
    print(f"Total cost: ${results.total_cost:.4f}")

# Total tokens consumed (None if not tracked)
if results.total_tokens is not None:
    print(f"Total tokens: {results.total_tokens:,}")

# Aggregated experiment statistics
stats = results.experiment_stats
print(f"Total duration: {stats.total_duration:.1f}s")
print(f"Total cost: ${stats.total_cost:.4f}")
print(f"Unique configurations tested: {stats.unique_configurations}")
print(f"Average trial duration: {stats.average_trial_duration:.1f}s")
print(f"Cost per configuration: ${stats.cost_per_configuration:.4f}")
print(f"Trial counts: {stats.trial_counts}")
# Trial counts: {"total": 10, "completed": 8, "failed": 2, ...}

# Best metrics from the winning trial
print(f"Best metrics: {results.best_metrics}")
# {"accuracy": 0.92, "latency": 800.0}  # latency in ms on SDKs after 0.22.0 (see version-matrix: latency-unit)
```

> **`None` means *not tracked*, not *local*.** `results.total_cost` / `total_tokens` are
> aggregated locally from per-trial metrics and read `None` only when no positive cost was captured
> (mock/offline runs, unpriced custom models — see `traigent-optimize-run` → Cost Wiring Probe).
> A real paid run — local or portal-tracked — should show a positive `total_cost`; treat
> `None`/`0.0` with real calls as cost not wired, never as "expected for a local run".
> Per-trial: `trial.get_metric("total_cost")` is the trial total. `"cost"` is the per-trial total
> on SDKs after 0.22.0 (see version-matrix: `cost-unit`) — it reconciles with `total_cost`, and the
> per-example mean moved to `"cost_per_example_mean"`. On 0.22.0 and earlier, local runs reported
> `"cost"` as the per-example mean — ~N× smaller than hybrid runs of the same config.
> **A per-trial total is not comparable across runs with a different eval-dataset example count** —
> more examples means a bigger total for the same per-example cost. Use `"cost_per_example_mean"`
> (or divide the total by the example count) whenever you compare cost across runs, not the raw total.

## The Quality / Cost / Latency Trade-off (multi-objective)

After a multi-objective run (`objectives=["accuracy", "cost"]`), the single `best_score` no longer
tells the whole story — you want the **trade-off set** (the Pareto frontier): the configurations
where you cannot improve one objective without sacrificing another.

Get one aggregated row per configuration with `to_aggregated_dataframe()` (groups repeated samples
of the same config and averages each metric), then filter to the non-dominated set.
`to_aggregated_dataframe()` / `to_dataframe()` need pandas: `pip install "traigent[analytics]>=0.19"`
(also included in `traigent[recommended]`).

```python
df = results.to_aggregated_dataframe(primary_objective="accuracy")
# One row per unique config. Columns: config params + samples_count + each metric as its mean
# under its BARE name (e.g. "accuracy", "cost", "latency" in ms) + "duration" (mean total
# wall-clock seconds) + "avg_response_time_ms" / "avg_response_time" (mean PER-CALL latency, in
# ms / seconds) when the run recorded per-call timings. "duration" (total wall-clock) is a
# DIFFERENT metric from the per-call "latency"/"avg_response_time_ms" — don't read one for the other.
print(df.columns.tolist())  # confirm the exact metric column names for your run

# Guard the frontier against rerun noise — see "Is the Delta Real?" above. Without this, a
# few-point sampling blip makes a config momentarily non-dominated and a noise artifact lands
# on the frontier. Two guards: drop under-sampled configs, and require a config to BEAT
# another by more than the noise floor on the quality axis before it counts as dominating.
# Set BOTH from YOUR run — there is deliberately no default, because both are properties of
# your run, not of the tool.
#   MIN_SAMPLES: the per-config repetition count you predeclared before running.
#   TIE_BAND:    your measured rerun spread from "Is the Delta Real?" above, in your metric's
#                units. A gap smaller than your own noise is not a gap.
import math

MIN_SAMPLES = None
TIE_BAND = None
# Validate values, not just types: a negative tie band inverts the domination test and a NaN
# one makes every comparison False, either of which corrupts the frontier silently.
# `isinstance(True, int)` is True in Python, so booleans are excluded explicitly.
if not (isinstance(MIN_SAMPLES, int) and not isinstance(MIN_SAMPLES, bool) and MIN_SAMPLES > 0):
    raise SystemExit("MIN_SAMPLES must be a positive int: your predeclared repetition count.")
if not (
    isinstance(TIE_BAND, (int, float))
    and not isinstance(TIE_BAND, bool)
    and math.isfinite(TIE_BAND)
    and TIE_BAND >= 0
):
    raise SystemExit("TIE_BAND must be a finite number >= 0: your measured rerun spread.")
df = df[df["samples_count"] >= MIN_SAMPLES]
# A config missing either metric (NaN) cannot be placed on the frontier: drop it and say so,
# rather than letting NaN comparisons silently keep or discard it.
n_configs = len(df)
df = df.dropna(subset=["accuracy", "cost"])  # use your run's actual metric names
if len(df) < n_configs:
    print(f"Excluded {n_configs - len(df)} config(s) with no accuracy or cost value")

# Non-dominated (Pareto) frontier with a tie band: maximize accuracy, minimize cost. Walk from
# cheapest to most expensive and keep a config only if it beats every cheaper KEPT config by more
# than TIE_BAND. Every dropped config is within TIE_BAND of a kept config that costs no more, so a
# chain of small steps can never erase a config that is clearly better than every survivor.
# With TIE_BAND = 0 it keeps exactly the strict Pareto frontier's (accuracy, cost) points;
# configs that tie exactly on both are shown once, so look for exact duplicates in `df` if
# another axis (latency, provider) should decide between them.
def pareto_front(df, maximize="accuracy", minimize="cost", tol=TIE_BAND):
    keep, best_kept = [], float("-inf")
    for i, row in df.sort_values([minimize, maximize], ascending=[True, False]).iterrows():
        if row[maximize] > best_kept + tol:
            keep.append(i)
            best_kept = row[maximize]
    return df.loc[keep]

frontier = pareto_front(df)
# For a latency objective, read the PER-CALL latency column (ms) — NOT "duration" (total wall-clock):
print(frontier[["accuracy", "cost", "avg_response_time_ms"]])  # use your run's actual metric names
```

Each frontier row is a *candidate* operating point, not yet a proven one: pick the cheapest config
that clears your accuracy bar, or the strongest quality/cost trade-off within your cost budget —
note the tie band folds a config into a cheaper kept config when it is within the band of it, so
every dropped config is within your noise of a kept config that costs no more, and the literal
highest-accuracy config may not appear. Confirm your choice with a bootstrap CI on the difference
(see "Is the Delta Real?" above) before promoting.
(`results.to_dataframe()` gives the raw per-trial rows if you want to plot the full cloud behind
the frontier.)

## Find Your Run on the Portal

A run that actually reaches the backend syncs to the Traigent portal, where the same trade-off is
rendered visually. That requires **both** `offline=False` (the default) **and** valid credentials
(`TRAIGENT_API_KEY`): a run with no key can fall back to local-only execution and then is **not**
portal-tracked. The portal Pareto/frontier view also requires >=2 objectives; a single-objective
run shows an "add a second measure" hint there, not a blank frontier. To locate a synced run:

> **Portal list order reflects arrival, not execution.** The Experiments list's default sort
> is driven by when the backend received and finalized the run, not by when you executed it
> locally — there is no client-supplied execution timestamp in that ordering. A normal run's
> receive order usually matches your execution order, but a deferred or retried sync
> (`traigent local sync`, or a finalize retry after a persistence hiccup — see "Verify the Run
> Actually Persisted" below) can land it out of that order. Do not infer execution order from
> list position: use `results.timestamp` (the local completion time) to know when a run
> actually finished. `results.experiment_id` identifies the experiment group; pair it with
> `results.experiment_run_id`, which identifies this exact run. Treat `results.cloud_url` as an
> exact-run link only when its query contains `run_id=<experiment_run_id>`; otherwise it opens
> the group and you must select that run ID.

```python
# The portal/backend identifiers (None when offline or local-fallback):
print(f"Experiment group: {results.experiment_id}")      # groups related runs
print(f"Exact run:        {results.experiment_run_id}")  # this backend run
print(f"Portal link:      {results.cloud_url}")
# (results.optimization_id is the SDK's local run id, not the portal identifier.)
# Open results.cloud_url only if it contains run_id=<results.experiment_run_id>.
# Otherwise open the experiment group and select results.experiment_run_id.
```

An `offline=True` run, or a non-offline run that fell back to local (no key), is **not** on the
portal — use the dataframe read above instead.

### Verify the Run Actually Persisted (`persistence_status`)

A portal-tracked run (non-offline, `experiment_id` set) can finish all its trials locally but still
fail to *finalize* on the backend — e.g. a network blip or backend 5xx during the final
session-close call. The SDK retries that finalize call (3 attempts, exponential backoff) before
giving up; if every attempt fails, it does not pretend the run is fine:

```python
if results.metadata.get("persistence_status") == "failed":
    print("Backend finalize failed after retries — the portal session may be stuck RUNNING.")
    print(results.metadata.get("persistence_error"))  # the underlying exception, if any
```

When this is `"failed"`, **do not assume the run synced** — the local `OptimizationResult` can look
complete while the backend session is left `RUNNING` on the portal. Re-check the run on the portal
(or run `traigent local sync`) before reporting a portal-tracked result as final. (Newer SDK builds
— the fix merged as Traigent#1731 — also expose this as `results.persistence_failed`, a bool
shorthand for the same check; check the metadata key directly if your installed SDK predates it.)

The status is not binary — read it precisely (field-verified on SDK 0.21.0 real runs, 2026-07-09):

| `persistence_status` | Meaning | Action |
|---|---|---|
| `"succeeded"` (or `"skipped"`/absent when backend tracking is off) | fully synced | none |
| `"degraded"` (benign) | **partial, not broken** — trial results *and* finalize synced (the portal link works; trial views and per-example diagnostics are live), only the session aggregation rollup was dropped, so summary aggregates may lag | keep the run; do **not** re-run (and re-pay) |
| `"degraded"` (backend-rejected) | the backend actively **refused** the persistence — `persistence_rejected` is True and `persistence_rejection_reason` explains why (quota/auth/tenant) | inspect `persistence_rejection_reason`; treat as a real problem, do **not** assume it's safe |
| `"failed"` | finalize lost after retries | recover via `traigent local sync`; re-run only if sync can't recover |

The two `"degraded"` cases are distinguished by metadata: benign rollup-lag sets
`persistence_degraded_reason` (trial results and session finalize both persisted — keep the run);
a backend rejection sets `persistence_rejected=True`, `persistence_reason="rejected"`, and
`persistence_rejection_reason=<why>` (the backend refused the data — do not treat it as benign).
The SDK never emits `"ok"`.

The portal may group runs that share the same agent and canonical dataset. Use that group only to
find related source runs. Before applying or recommending a configuration, record the exact source
`experiment_id`, `experiment_run_id`, and `configuration_run_id` shown by the portal/API. A grouped
view does not make grouped configurations a single analytics run, and it does not imply equivalent
configs have been merged across runs.

## Stop Reasons

The `stop_reason` field tells you why optimization ended. This is critical for deciding whether to run more trials:

| Stop Reason | Meaning | Action |
|---|---|---|
| `"max_trials_reached"` | Hit the `max_trials` limit | Report the best completed configuration as a result, never as a failure; whether to buy more trials is the decision brief's call (`traigent-analyze-guidance`, Mode B), not this skill's |
| `"max_samples_reached"` | Hit the max samples/examples limit | Increase sample budget or reduce dataset size |
| `"timeout"` | Exceeded the timeout duration | Increase timeout or reduce config space |
| `"cost_limit"` | Hit the per-run cost budget — or, if the stop message says `per-trial cost unknown: fallback trial limit`, a trial-count stop because cost was not measured (warning `COST_UNMEASURED_TRIAL_LIMIT_REACHED`; see `traigent-debugging`) | Report the best completed configuration as a result, never as a failure — the paid trials are kept; a larger run needs a new approval, and the decision is `traigent-analyze-guidance`'s |
| `"execution_budget"` | Shared cumulative `ExecutionBudget` exhausted — cost, examples, or deadline (SDK >= 0.26.0); reported instead of `"cost_limit"` | Report the best completed configuration as the result; `results.metadata["execution_budget"]` says which limit hit |
| `"metric_limit"` | A soft cumulative metric limit was hit | Results are valid; report them |
| `"optimizer"` | Optimizer decided to stop (search space exhausted) | Config space fully explored; results are final |
| `"plateau"` | No improvement detected | Results have converged; more trials unlikely to help |
| `"convergence"` | Built-in convergence condition triggered | Converged for this space; results are final |
| `"semantic_saturation"` | Per-example quality and continuous objectives saturated | Report; detail in `results.metadata["semantic_saturation"]` |
| `"user_cancelled"` | User cancelled or declined cost approval | Review cost estimates, re-run if needed |
| `"condition"` | A generic stop condition triggered | Check convergence_info for details |
| `"error"` | Optimization failed due to an exception | Check failed trials for error messages |
| `"vendor_error"` | Provider error (rate limit, quota, service issue) | Check API keys, quotas, and provider status |
| `"network_error"` | Connectivity failure | Check network connection and retry |
| `None` | Stop reason not set | Typically means the run completed normally |

```python
if results.stop_reason == "max_trials_reached":
    print("Trial cap reached - report the winner; more trials is a decision-brief question")
elif results.stop_reason == "plateau":
    print("Optimization converged - these are likely the best results")
elif results.stop_reason == "cost_limit":
    if results.total_cost is None:
        print("Cost limit reached; tracked total cost unavailable - partial result, paid trials kept")
    else:
        print(f"Cost limit reached at ${results.total_cost:.2f} - partial result, paid trials kept")
elif results.stop_reason == "execution_budget":
    budget = results.metadata.get("execution_budget")
    exhausted_dimension = (
        budget.get("exhausted_dimension") if isinstance(budget, dict) else None
    )
    dimension = exhausted_dimension or "unknown dimension"
    cost = (
        "tracked total cost unavailable"
        if results.total_cost is None
        else f"tracked total cost ${results.total_cost:.2f}"
    )
    print(f"Shared execution budget reached ({dimension}); {cost} - partial result kept")
elif results.stop_reason == "error":
    for trial in results.failed_trials:
        print(f"Error in trial {trial.trial_id}: {trial.error_message}")
```

## Exporting a Candidate and Promoting It Safely

On SDK 0.27.0, `optimize()` / `optimize_sync()` automatically applies a nonempty
`results.best_config` to the same `OptimizedFunction` instance before returning. Calling
`apply_best_config(results)` afterwards only reapplies it. Therefore, if the incumbent must keep
serving while you inspect a candidate, never optimize the serving-process instance. Run the search
in a separate candidate process with its own decorated function instance:

```python
# candidate_optimize.py — a separate OS process, never the serving process
results = classify.optimize_sync()

# A nonempty winner is already active on this process-local `classify` instance.
if results.best_config:
    classify.export_config("candidate_config.json")
```

Exit that candidate process after export. The serving process and its incumbent instance remain
unchanged because they do not share process memory. `classify.load_optimization_results(path)` also
applies the loaded `best_config` as a sticky override on that instance, so use a disposable process
for replay too. To inspect a saved result without mutation, read its JSON (`trials[]`, `best_config`,
`best_config_margin`, `stop_reason`) directly.

The exported candidate is not promoted yet. Compare it with the exact incumbent on a frozen holdout
slice through `traigent-ci-safety-gate`, then load or deploy it to the serving process only after the
gate passes. `best_config_margin` compares the search winner with its runner-up on the search slice;
it cannot replace the candidate-vs-incumbent holdout comparison.

### Config Access Lifecycle

| When | API | Notes |
|---|---|---|
| During optimization trials | `traigent.get_config()` | Returns current trial config. Thread-safe via contextvars. |
| During optimization trials (strict) | `traigent.get_trial_config()` | Raises `OptimizationStateError` if not in active trial. |
| After a successful `optimize()` with nonempty `best_config` | `traigent.get_config()` | Returns the automatically applied winner on that same instance. |
| After `apply_best_config()` | `traigent.get_config()` | Returns the explicitly reapplied best config. |
| From optimization results | `results.best_config` | Dict with the best configuration found. |
| From the function object | `func.current_config` | Current config on the `OptimizedFunction` instance. |

<!-- PROTECTED -->
### Safety Check Before Applying

Verify results before applying:
<!-- /PROTECTED -->

```python
# Run this only in the disposable candidate process described above.
results = classify.optimize_sync()

# best_config_margin exists from SDK 0.26.0; getattr keeps this runnable on the 0.24.0 floor (verdict None there)
verdict = (getattr(results, "best_config_margin", None) or {}).get("verdict")
if results.best_score is None or results.best_score < 0.85:
    print(f"Score {results.best_score} below threshold; candidate not exported")
elif verdict == "statistical_tie":
    print(f"Score {results.best_score:.2%} but the winner is tied with the runner-up; candidate not exported")
else:
    classify.export_config("candidate_config.json")
    print(f"Exported candidate with search score {results.best_score:.2%}")
```

This threshold and runner-up check runs on the optimization/search slice — it gates whether to
export a candidate. Promotion is a separate decision that requires candidate-vs-incumbent
evaluation on the holdout slice (see `traigent-ci-safety-gate`). The process is disposable because
the SDK already applied the winner to its local instance before these checks ran.

## Optimization History

Review results from previous optimization runs on the same function:

```python
history = classify.get_optimization_history()

for past_result in history:
    print(f"Run {past_result.optimization_id}")
    print(f"  Algorithm: {past_result.algorithm}")
    print(f"  Best score: {past_result.best_score}")
    print(f"  Best config: {past_result.best_config}")
    print(f"  Trials: {len(past_result.trials)}")
    print(f"  Duration: {past_result.duration:.1f}s")
    print(f"  Stop reason: {past_result.stop_reason}")
    print(f"  Timestamp: {past_result.timestamp}")
```

Compare across runs only when `objectives`, dataset, evaluator, and space are identical (compare
the sampled space from `trials[].config` and `objectives`; the declared search space is not stored
on the result, and no result field records the dataset or evaluator, so confirm those from your
run-plan record) — otherwise the two numbers were measured on different things, and even then the
difference is directional, not a paired result (see "Pair, don't cross-compare" above). Two
random or adaptive runs that sampled different parts of the same space also read as different;
that blocks the comparison rather than allowing a wrong one:

```python
import json

def observed_space(result):
    """Knob -> set of values the run actually sampled (the declared space is not on the result)."""
    space = {}
    for t in result.trials:
        for k, v in t.config.items():
            space.setdefault(k, set()).add(json.dumps(v, sort_keys=True))
    return space

history = classify.get_optimization_history()
if len(history) >= 2:
    latest, previous = history[-1], history[-2]
    same_setup = latest.objectives == previous.objectives and observed_space(latest) == observed_space(previous)
    if same_setup and latest.best_score is not None and previous.best_score is not None:
        print(f"Directional change: {latest.best_score - previous.best_score:+.3f}")
```

## Complete Example

Candidate-process workflow: optimize, analyze, decide whether to export. Save this as a batch script
and run it in a separate OS process from the serving agent. A later holdout gate owns promotion.

```python
import traigent

@traigent.optimize(
    eval_dataset="summarization_eval.jsonl",
    configuration_space={
        "model": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
        "temperature": [0.0, 0.3, 0.7],
        "max_tokens": [256, 512, 1024],
    },
    objectives=["accuracy"],
    max_trials=15,
)
def summarize(text):
    config = traigent.get_config()
    # ... your LLM summarization logic ...
    return summary

# 1. Run optimization
results = summarize.optimize_sync()

# 2. Quick summary
print(f"Best config: {results.best_config}")
print(f"Best score: {results.best_score}")
print(f"Stop reason: {results.stop_reason}")
print(f"Duration: {results.duration:.1f}s")
print(f"Success rate: {results.success_rate:.0%}")

# 3. Cost analysis
if results.total_cost is not None:
    print(f"Total cost: ${results.total_cost:.4f}")
if results.total_tokens is not None:
    print(f"Total tokens: {results.total_tokens:,}")

# 4. Trial breakdown
print(f"\nTop 5 trials by accuracy:")
top_trials = sorted(
    results.successful_trials,
    key=lambda t: t.get_metric("accuracy", 0.0),
    reverse=True,
)[:5]
for trial in top_trials:
    print(f"  {trial.config} -> accuracy={trial.get_metric('accuracy'):.3f}")

# 5. Stop reason — a result, never a verdict on buying more trials (see the table above)
print(f"\nStop reason: {results.stop_reason}")

# 6. Export if good enough and not a statistical tie (SDK 0.26.0+ verdict; None below).
# optimize_sync() already applied a nonempty winner to this disposable process-local instance.
THRESHOLD = 0.80
verdict = (getattr(results, "best_config_margin", None) or {}).get("verdict")
if (
    results.best_score is not None
    and results.best_score >= THRESHOLD
    and verdict != "statistical_tie"
):
    summarize.export_config("candidate_config.json")
    print(f"\nExported candidate (search score={results.best_score:.2%})")
    print("Compare candidate_config.json with the incumbent on the frozen holdout before promotion")
elif verdict == "statistical_tie":
    print(f"\nScore {results.best_score:.2%} but the winner is tied with the runner-up; not exporting")
else:
    print(f"\nScore {results.best_score} below threshold {THRESHOLD}; not exporting")
```

## Reference Files

- [Terminal-First Analytics — MCP Tool Contract](references/mcp-analytics-tools.md)
- [OptimizationResult and TrialResult API Reference](references/optimization-result-api.md)
- [Convergence Analysis Patterns](references/convergence-patterns.md)

## See Also

| Skill | Use |
|---|---|
| `traigent-analyze-guidance` | Mode B: the canonical next-step decision for a portal-tracked run. Mode C: a local next-iteration hypothesis for offline/local runs, unavailable service payloads, or service-flagged local evidence. |
| `traigent-analyze-variable-importance` | A deeper, local tuned-variable importance card when `one_knob_dominates` and you want the bootstrap-CI breakdown. |
| `traigent-ci-safety-gate` | Gate a `clean_winner` (or a cost guardrail for `cost_blowup`) before promoting it to production. |

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
