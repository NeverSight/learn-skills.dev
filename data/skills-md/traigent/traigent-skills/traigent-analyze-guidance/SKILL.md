---
name: traigent-analyze-guidance
description: "What should this Traigent optimization run be, and what next? Three modes: (A) pre-run — fetch the service run-plan, present objectives/models/knobs/search/budget/offline options, apply preflight; (B) post-run, portal-tracked — fetch the backend decision brief via the `analytics_get_run_decision_brief` MCP tool, present its headline, confidence, recommended action, evidence, and warnings verbatim, then hand off to the matching skill; (C) offline/local fallback — diagnose flat/noisy/negative local results, which knob mattered, example evidence, form the next iteration hypothesis when offline=True or no service payload. Portal-tracked decisions come from Traigent, never local markdown."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: analyze
  traigent-maturity: stable
  author: Traigent
  version: "1.2.5"
---

# Traigent Analyze Guidance

## When to Use

Requires `traigent>=0.21.3`. The SDK's former `guidance` command group (the
Planner V2 `next` / `execute` / `receipt` / `reopen` verbs) and the older
`next-steps` command were retired from the SDK on 2026-08-03 and are absent
from 0.26.0. Post-run guidance for portal-tracked runs now comes from the
backend decision brief served by the `traigent-analytics` MCP server
(`analytics_get_run_decision_brief`); pre-run planning uses `traigent plan`.

Use this skill whenever you need to answer "what should this optimization run
be, and what should I do after it?" It has three strict modes and one doctrine:
**for portal-tracked runs the decision comes from the Traigent service, never
from local markdown reasoning.**

- **Mode A — pre-run plan:** fetch the service run-plan, confirm options, mock
  dry-run, launch on explicit go.
- **Mode B — post-run, portal-tracked:** fetch and follow the server-owned
  decision brief, then loop back to Mode A.
- **Mode C — offline/local fallback:** diagnose local results and form ONE next
  hypothesis when no service payload is available.

## Optimization Economics — Read This Before Sizing a Run

**Do not default to recommending zero spend.** The canonical Traigent posture on spending,
the five characterization questions with their exact options, the tailoring rules (including
the three-option paging rule), the explanation duty, and the local survey draft contract all
live in one file that ships inside this skill:
**`references/economics-characterization.v0.md`**. Read it from this skill's own directory
before you propose, size, or decline a run — it is deliberately not restated here. It is
generated from `docs/shared/economics-characterization.v0.md` in the traigent-skills repo,
which is where any edit goes; the copy shipped here is byte-identical.

**This skill's part — collect and relay, never compute.** Gather the characterization (infer
what you can, confirm Q1 and Q3, record it locally per the reference), pass it to the
Traigent service, and present **only the budget the service returns**, together with the
service-supplied why. This skill is a thin client for economics exactly as it is for the
run-plan and the next-step decision: **budget authorship belongs to the service.**

**Do not compute, adjust, or recommend a budget locally.** No budget arithmetic in markdown,
no scaling the returned number, no "roughly $X/day" of your own. The reference describes what
the service computes; it is not a local calculator, and a plausible-looking number you derived
here is a fabricated one.

**When the service returns no economics result:** say so plainly — "Traigent hasn't returned
a budget for this run, so I don't have one to give you" — then present the options and the
approval ask with **no budget number at all** of your own (no daily budget, floor, or payback
figure). Still state the run's own spend cap and its dry-run cost estimate in that ask, and say
that the Traigent service sizes the budget and has not returned one yet; do not present `$0` as
the recommendation unless the service returns `$0`. Without a run to approve, continue in
Mode C, still with no budget number. Diagnosis without a budget is a valid answer; an invented
budget is not. There is no local fallback calculator, and until the economics service ships
there may simply be no number available.

**Mandatory whenever you relay any of it:** show the options, recommend exactly one, and
explain **why in the user's own numbers** — their agent, their volumes, their error costs. The
explanation is a product requirement, not decoration. It applies to relaying the service's
recommendation; it is never a licence to author one.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval before any
paid run**, an explicit spend cap, and the recorded stop rule. Economics governs *how much* to
invest — and here that number comes from the service; it never affects *whether* approval is
required — it always is.

## Mode Arbitration

| Situation | Mode |
|---|---|
| About to design or launch a run (any run, always) | **A** — fetch and confirm the service run-plan |
| A portal-tracked run just completed | **B** — fetch the backend decision brief (`analytics_get_run_decision_brief`) first |
| `offline=True`, no backend access, the service payload is unavailable, or the service flagged local evidence for diagnosis | **C** — local diagnosis, one hypothesis |

Portal-tracked runs go through Mode B first. Pre-run is always Mode A. Mode C
applies only when the Mode A/B service payloads are unavailable or for local
evidence diagnosis.

---

## Mode A — Pre-Run Plan

Use this before designing or launching any Traigent optimization run.

This mode is a thin client. It gathers the minimum run context, asks the
Traigent service for an allowlisted plan, presents that payload to the user, and
executes only the returned steps after the user approves. Do not invent or
improve the plan locally.

### Boundary

The recommended plan comes from the Traigent service via `traigent plan` or the
MCP tool `get_optimization_plan`. The returned payload is advisory and currently
static guidance: expect `phase` such as `P1_STATIC`, plus `evidence_level`,
`caveat`, and `advisory`.

This requires an SDK build that ships the optimization-plan tool (the `traigent
plan` CLI / `get_optimization_plan` MCP tool). If your installed SDK does not
expose it yet, tell the user the plan service is not available in this build and
fall back to `traigent generate-config` for knob recommendations (see
`traigent-optimize-config-space`) — never fabricate a plan locally. (`traigent
recommend` used to serve this and was retired from the SDK in `7eea70c9`,
"retire recommendation catalogs", along with `traigent recommend-eval`.)

Do not embed local planning intelligence in this skill:

- Do not choose or rank models, knobs, algorithms, budgets, or option order in markdown.
- Do not compute plan-quality bands, search-space rules, or recommended trial counts locally.
- Do not add a replacement plan if the service omits one. Ask the service again with clearer context or stop for user input.
- Do not treat the advisory plan as proof that a real run will improve. The mock and heldout results remain the evidence.

### Protocol

1. Gather a short summary from the user or project files:
   - task description and agent entrypoint,
   - dataset size and holdout split — confirm a holdout slice is reserved and disjoint from the tuning slice; if none exists, the plan must say so and create one before optimization begins,
   - objectives the user cares about,
   - budget or maximum spend for the run.
2. Fetch the plan from the Traigent service:
   - Prefer `traigent plan` when the CLI is available.
   - Use `get_optimization_plan` when working through the Traigent MCP surface.
   - Pass only the short summary and any existing run id or portal context the user approved.
3. Validate the response shape before presenting it. The allowlisted top-level
   keys are `schema_version`, `phase`, `plan`, `steps`, `evidence_level`,
   `caveat`, and `advisory`. The `plan` object may include `objectives`,
   `models`, `knobs`, `algorithm`, `max_trials`, `cost_limit_usd`, and `offline`.
4. Present the returned plan option by option. For each option, show:
   - the exact value or choices returned by the service,
   - any matching `evidence_level`, `caveat`, or `advisory` text,
   - a short confirmation prompt: keep it, adjust it, or ask Traigent for a refreshed plan.
5. Record the user's confirmations and adjustments as a run-plan record. Use
   `references/run-plan.template.md` only as a capture format for the service
   payload and user decisions, not as a source of recommended settings. See
   `references/run-plan.txt2sql-example.md` for a filled text2SQL example of this
   capture format (the recommended values shown there came from the service, not
   from this skill).
6. Before launching, walk the preflight checklist in `references/preflight.md`.
   For program-level principles, see `references/optimization-principles.md`.
7. Mock dry-run first. The mock must be free/no-spend and should verify that the
   agent, dataset loader, scorer, and returned steps are wired.
8. Stop after the mock with a short readout: what executed, what did not execute,
   estimated cost if available, and the exact real-run command or SDK step that
   will run next. **If the mock fails** (agent, loader, or scorer unwired), do
   NOT present the real-run go prompt — fix the wiring first and re-mock.
9. Launch the real run only when the user explicitly says to go and the returned
   plan's cost cap is set. Execute the returned `steps[]`; do not substitute a
   locally generated run sequence.
10. After the run, hand control to Mode B (post-run next steps) with the run id
   and portal link.

### Confirmation Rules

- Defaults are confirmed, not silent. A user can approve the service plan as-is,
  but you still show every returned option group.
- If the user changes an option, ask Traigent for an updated plan when that
  change could affect later steps or cost. Treat manual edits as user overrides
  and label them that way in the run-plan record.
- If the service returns no plan, an incomplete plan, or a plan for the wrong
  task, do not patch it locally. Re-query with corrected context or stop.
- If prior runs exist, run Mode B first and pass its server recommendation
  into the plan request as context. The next-step decision still comes from the
  service. Fetch the decision brief **at most once per planning cycle** — if you
  arrived at Mode A *from* Mode B, do not fetch it again; proceed to step 1
  with its payload as context.
- Keep content local unless the user approves egress. Summaries sent to the
  service should be minimal and should not include raw private examples by
  default.

### First Run Onboarding

If the user has not run Traigent before, ask whether they want to start with the
bundled text2SQL example or use their own agent. The example is useful because it
exercises the same thin-client loop: gather summary, fetch the service plan,
confirm options, mock dry-run, then real run on explicit approval.

Do not hard-code example models, knobs, or trial counts here. Fetch the example
plan from Traigent using the same protocol.

---

## Mode B — Post-Run Next Steps (Portal-Tracked)

Use this after every portal-tracked Traigent optimization run before planning the next one.

This is the canonical "what next" path for portal-tracked runs: fetch and follow the
server-owned decision brief first. For offline/local runs with no service payload, fall
through to Mode C; for reading result fields or producing reports without making a decision, hand
off to `traigent-analyze-results`.

Fetch the decision brief from the Traigent service; do not substitute markdown reasoning.

This mode is a thin client. Fetch the post-run brief through the
`traigent-analytics` MCP server, present the backend's headline and recommended
action verbatim, then send that direction into Mode A as context for a fresh
service plan.

The server needs a one-time setup: `pip install "traigent[mcp]>=0.19"` (already included
in `traigent[recommended]`), then register the stdio command `traigent-analytics-mcp`
with your coding assistant under the name `traigent-analytics`. The full steps are in
`traigent-analyze-results` → "Prerequisites (one time)". If the `analytics_*` tools
are not listed, the brief cannot be fetched.

This mode is inert without the backend payload. If the tool cannot fetch a
service response, report that directly and stop unless the user asks you to
retry. Retry **at most once**; if the second attempt also fails, fall through to
Mode C for local diagnosis instead of retrying again.

### Surface Status — the guidance CLI is retired

The SDK's former `guidance` command group (the Planner V2 `next` / `execute` /
`receipt` / `reopen` verbs) and the older `next-steps` command were retired
from the SDK on 2026-08-03 and are absent from 0.26.0 — an instruction to run
either is dead on a current install. The supported post-run surface is the
backend **decision brief**, fetched with the `analytics_get_run_decision_brief`
tool on the `traigent-analytics` MCP server, plus the portal.

The Planner V2 guidance CLI was retired without a lifecycle replacement:
execution/receipt flows are not currently available from the SDK — the portal
and the decision brief are the supported surface. Present the brief's
recommended action, hand off to the matching skill (see Handoff Reference), and
let the user perform it; never invent a lifecycle command, and never resurrect
a retired one.

### Boundary

For portal-tracked runs handled by this mode, the decision comes from the
Traigent service. Do not maintain local next-action rules, derive
recommendations from local files, or infer what should happen next from
markdown.

The MCP server resolves the caller's tenant from the authenticated session and
returns backend-produced payloads. Treat every returned field as authoritative:
never invent fields, numbers, or rankings, and never re-rank the backend's
recommendation. Never execute a server-supplied shell fragment: the brief's
`recommended_action.kind` is a label to relay and hand off, not a command to
run. If the user asks for a different action, label that as a manual override
and fetch a fresh brief.

### Protocol

1. Collect the completed run id, its project id, and the portal `View` link.
   In SDK >= 0.18.1.dev2, `result.experiment_run_id` (and `result.experiment_id`) are
   populated directly on the optimize result object — use `result.experiment_run_id` as
   the `run_id`. Do not ask the user to search logs; the value is on the result.
   ```python
   results = await my_func.optimize(max_trials=10)
   run_id = results.experiment_run_id   # available directly; pass this to the decision brief
   ```
2. Fetch exactly one decision brief through the `traigent-analytics` MCP
   server:

   ```text
   analytics_get_run_decision_brief(
       project_id = "<the project the run belongs to>",
       run_id     = "<the completed run id>",
       intent     = "iterate",
   )
   ```

   Use `intent="iterate"` for choosing the next optimization round, `"deploy"`
   for a promotion decision, and `"debug"` for a run that looks broken;
   `"report"` reading belongs to `traigent-analyze-results`.
3. Validate the response before presenting it: require the `ok` flag and a
   `decision_brief` object (decision_payload v0: `headline`, `confidence`,
   `recommended_action`, `evidence`, `drilldowns`, `warnings`). On a false
   `ok` or an absent brief, report that and stop, or fall through to Mode C;
   do not synthesize a decision from partial fields.
4. Present the brief without re-ranking it, in this order:
   - **Headline** — the backend's one-sentence verdict, verbatim.
   - **Confidence** — never upgrade a `low`/`medium` confidence into a
     stronger claim.
   - **Recommended action** — `recommended_action.kind`, optional `config_id`,
     and `why`, exactly as returned. This is the single authoritative next
     step; do not add alternatives of your own.
   - **Evidence** — the `summary` strings from the brief's `evidence` list.
   - **Warnings** — relay every warning; do not filter or soften them.
5. Follow at most one `drilldowns[]` entry per turn, and only when the user
   asks or the brief clearly calls for it. The registered drilldown tools
   (`analytics_get_run_report`, `analytics_get_example_insights`, and the rest
   of the registered analytics tool set) are cataloged in
   `traigent-analyze-results`; use the portal deep-link for any view without a
   registered tool.
6. Map the recommended action to the matching skill through the Handoff
   Reference below, confirm with the user, and hand off. Execution is manual
   (see Surface Status): the user or the handoff skill performs the action, and
   the portal remains the durable record of what was decided.
7. Loop back to Mode A with the run id, portal link, and the brief's
   recommended action as context. The next paid run still requires a fresh
   service plan, mock dry-run, cost approval, and explicit go.

### Presentation Rules

- Use Traigent's words for the recommendation. You may summarize for readability,
  but do not change the ordering or imply stronger support than the payload gives.
- Present the single backend recommendation and its `why` rationale. Do not
  reconstruct hidden evidence from local files, and do not expand the brief's
  evidence references into guessed internals.
- Always include the portal link when available; as a fallback, build the
  navigation-only link `https://portal.traigent.ai/p/<project_id>/runs/<run_id>`.
  The portal is the durable record for best performers, tradeoffs, parameter
  importance, and decision context.
- If the run is absent from the portal, treat that as a registration or
  connectivity issue. Do not invent a next-step decision from partial local data.
- Keep raw examples, traces, and private content local unless the user explicitly
  approves egress.
- Traigent recommendations (including "compare with baseline before promotion") are
  advisory, not promotion authorizations. Promotion requires candidate-vs-incumbent
  evaluation on the holdout slice. If the repo already has a holdout mechanism, present
  it as that repo's implementation of this general rule, not as something Traigent
  mandated in that exact form.
- The brief knows the numbers, not where the data came from. A run whose dataset,
  evaluator, or agent was a generated substitute (check the project's own run record; the
  guided first run leaves one under `traigent-runs/`) is walkthrough evidence: say
  so before the headline, relay a `promote_winner` action as advisory on generated
  material — promotion still needs real components and the holdout check above — and
  keep that disclosure attached to every number quoted from the brief.

### Handoff Reference

The brief's `recommended_action` may route to the current skill names below;
reject a stale or unavailable skill instead of guessing what it meant. These
are handoff labels, not a local decision menu:

- evaluation-set scoring -> `traigent-dataset-curate`
- dataset curation -> `traigent-dataset-curate`
- hard-example reflection -> `traigent-dataset-curate`
- evaluator review -> `traigent-eval-audit`
- evaluator repair -> `traigent-eval-build`
- optimization run -> `traigent-optimize-run`
- holdout validation -> `traigent-ci-safety-gate`
- safety gate setup -> `traigent-ci-safety-gate`

---

## Mode C — Offline / Local Diagnosis

Use this mode after an offline/local Traigent optimization run (`offline=True` or no backend
access), or when a portal run's service guidance decision is unavailable and you need to form a
local hypothesis from evidence. It also applies when the service has already flagged local evidence
for inspection and the user asks:

- "results are flat/noisy/negative"
- "which knob mattered locally?"
- "should I expand or narrow the space?"
- "what do I do with weak examples?"

The goal is to choose the next single local hypothesis, not to change every part of the system at
once.

### Read the Evidence First

Start with the local run object and existing analysis skills. `traigent-analyze-results` covers
result fields in depth, and `traigent-analyze-variable-importance` covers richer importance reporting.
Use this mode to form the local next hypothesis after those facts are known.

For a portal-tracked run, first fetch the service-owned decision brief through
Mode B. If that payload is unavailable, or if it flags local evidence that needs
diagnosis, keep the service limitation visible and use the local facts below as a fallback or
supporting diagnosis:

- `confidence` - keep low/medium confidence visible; do not upgrade it based on intuition.
- `evidence[].summary` - use backend summaries only when they are actually present in the service
  payload; otherwise use local result fields.
- local result fields - identify whether the issue is flat scores, noisy examples, high cost, thin
  samples, a dominated winner, or a narrow knob.

```python
from traigent.utils.insights import get_optimization_insights
from traigent.utils.importance import ParameterImportanceAnalyzer

print(f"stop_reason={results.stop_reason}")
print(f"best_config={results.best_config}")
print(f"trial_count={len(results.trials)}")
print(f"total_cost={results.total_cost}")

insights = get_optimization_insights(results)
print(insights.get("performance_summary", {}))
print(insights.get("parameter_insights", {}))

analyzer = ParameterImportanceAnalyzer(objective="accuracy")
importance = analyzer.analyze_variance_based(results.trials)
print(analyzer.get_top_parameters(importance, top_k=5))
```

If importance is empty, do not infer that no knob matters. Common reasons are too few successful trials, flat objective variance, missing objective metrics, or a configuration space that did not vary enough.

Below about 20 completed trials — a first-run search is 12 — read `importance_score`,
`optimization_priority`, and the insights `recommendations` as directional, the label the
`traigent-analyze-variable-importance` script gives the same data. The analyzer's sample floors
are explicit: `analyze_variance_based` and the correlation method return `{}` under 10 successful
trials, and `analyze_permutation_based` does so under 20. Below the applicable floor, an empty
result means insufficient samples, never "no knob matters". At or above the floor, inspect flat
objective variance, missing objective metrics, and parameters that did not vary before diagnosing
the empty result. Rankings above the floors still carry no underpowered marker, so "focus on these
parameters" is a hypothesis to test, not a finding.

### Example-Side Evidence

<!-- PROTECTED -->
Use example-side evidence when the aggregate score hides where the candidate wins or fails. `ExampleInsightsClient` requires a Traigent account/backend and returns scoring metadata only: example ids, sample counts, algorithm version, and scored flags. It does not expose proprietary difficulty, informativeness, ambiguity, or latent feature-vector values. The ranked and flagged "examples to review" surface (`analytics_get_example_insights` / `GET /api/v1/analytics/runs/{run_id}/example-insights`) is likewise non-signal: it ranks by review urgency and provides enum flags and a suggested action — never raw scores or hidden feature values.
<!-- /PROTECTED -->

> **Import note (verified against SDK 0.18.x):** `ExampleInsightsClient` ships in the core SDK at `traigent.analytics` — no separate install required. The module's own `DeprecationWarning` points at the separate `traigent-analytics` plugin, but that plugin does not export `ExampleInsightsClient` (`from traigent_analytics import ExampleInsightsClient` raises `ImportError`); use the core import below and ignore the warning for this class. **Caveat if you HAVE installed the plugin:** the core shim then defers to the plugin and stops exposing this class, so the import below itself raises `ImportError` — uninstall the plugin or use the deep import `from traigent.analytics.example_insights import ExampleInsightsClient` (works with or without the plugin, verified).

`ExampleInsightsClient` takes the **`/api/v1` base** (`https://portal.traigent.ai/api/v1`), while `BackendAnalyticsClient` and `traigent plan --backend-url` take the **origin** (`https://portal.traigent.ai`) — mixing the two gives a 405 or a doubled path (full table in `traigent-setup-audit`).

```python
from traigent.analytics import ExampleInsightsClient

async def fetch_example_metadata(run_id: str):
    async with ExampleInsightsClient(
        backend_url="https://portal.traigent.ai/api/v1",
        timeout=60.0,
    ) as client:
        job = await client.compute_scores(experiment_run_id=run_id)
        status = await client.get_job_status(job_id=job["job_id"])
        scores = await client.get_example_scores(experiment_run_id=run_id)
        quality = await client.get_dataset_quality(experiment_run_id=run_id)
        return {"status": status, "scores": scores, "quality": quality}
```

When aggregate scores hide where the candidate wins or fails, pull the ranked "examples to review" rows: use the `analytics_get_example_insights` MCP tool (or the `GET /api/v1/analytics/runs/{run_id}/example-insights` endpoint). Work through rows in `review_priority` order (critical first) and use each row's `suspicious_flags` and `recommended_action` to choose the next iteration — these are coarse enum signals, not hidden numeric scores. See `traigent-dataset-curate` for the flag-to-action guide.

Backend-only report surfaces, each requiring a Traigent account/backend:

- `GET /api/v1/experiment-runs/runs/{run_id}/report-payload`: winner, trade-off, and stability insights.
- `/api/v1/optimization-comparisons`: cross-run comparison across candidate runs.
<!-- contract: path /api/v1/optimization-comparisons in traigent.cloud.analytics_client -->
- Example-scoring compute, scores, and dataset-quality endpoints: scoring status and scoring metadata.
- `GET /api/v1/analytics/runs/{run_id}/example-insights`: ranked and flagged examples to review (IP-safe: review_priority, suspicious_flags, recommended_action).

### Next-Step Decision Table

| Symptom | Likely read | Ranked next action |
|---|---|---|
| Flat scores everywhere | Evaluation dataset is too easy, objective is saturated, or the space lacks meaningful variation | First rule out rerun noise (`traigent-analyze-results` → "Is the Delta Real?" — see the note below); then synthesize harder examples with `traigent-dataset-curate`; add discriminating cases; then re-run a small grid |
| High variance across repetitions | Evaluator or model behavior is noisy | Rule out rerun noise first (`traigent-analyze-results` → "Is the Delta Real?" — see the note below): measure your own rerun spread and treat any single-cell delta inside it as unreportable. Then raise repetitions, use statistical aggregation, and audit the evaluator with `traigent-eval-audit`. A server-side evaluator-audit action is coming as a next-step option — prefer it when available. |
| One knob dominates | The useful region is narrower than the current space | Narrow that knob's range; add structural knobs with `traigent-optimize-config-space` or `traigent-optimize-composite-knobs` |
| Winner ties baseline | Objective weights or threshold may not reflect the product decision | Revisit objective weights with `traigent-eval-choose-metric`; inspect holdout slices before changing the space |
| `stop_reason` is budget-bound | Search stopped before enough evidence accumulated | Adjust budget, cheaper models, max trials, or algorithm with `traigent-optimize-run` |
| Weak examples identified | The same examples fail across good configs | Feed those examples into guided optimization and add a heldout check |

> **Before treating a flat or noisy result as signal, rule out rerun noise.** See
> `traigent-analyze-results` → *"Is the Delta Real?"*: the same config on the same data moves
> ±5–10 pp across days at n=40 (same-config SD ≈ `50/√k` pp at p≈0.5), so a single-cell delta
> under ~10 pp is unreportable, pooling ≥4 cells only halves the noise, and numbers measured in
> different sessions/days must never be cross-compared. Claim a win only when a bootstrap CI on
> the difference excludes zero — a "flat" or "high-variance" result is often just this floor.

Use weak examples as evidence, not as a replacement for a holdout.

```python
# (input, expected, actual) for each case the current prompt handles poorly.
weak_examples = [
    ("question text", "expected answer", "candidate answer"),
]

def my_rewrite_llm(prompt: str) -> str:
    """Your own model call, on your own provider key. Example content stays on your machine."""
    ...

results = answer.optimize_with_guidance(
    provider=provider,            # a GuidancePlanProvider
    rewrite_llm=my_rewrite_llm,   # required: Traigent never builds one from environment credentials
    plan_kind="prompt_rewrite",   # weak_examples are read only by a prompt-rewrite plan
    prompt_param="system_prompt", # the tuned knob whose string values are prompt variants
    weak_examples=weak_examples,
    max_trials=8,
)
```

`optimize_with_guidance` is a synchronous method on the decorated optimized function — do not `await` it (it returns the `OptimizationResult` directly). `rewrite_llm` is required (a callable `fn(prompt) -> str` or a constructed client); `provider` supplies the guidance plan. `weak_examples` are `(input, expected, actual)` tuples, and only a `plan_kind="prompt_rewrite"` plan reads them: it rewrites the prompt variants of the knob named by `prompt_param` (a tuned knob whose values are prompt strings). Under the default `benchmark_guide` plan they are ignored. Keep the provider and rewrite model project-specific, and confirm the new candidate still improves on a heldout slice.

This is a **paid real run** — the same gate as any other applies: dry-run/mock first, present the cost estimate, and get explicit user approval before executing (see the `traigent` lifecycle skill).

Before iterating, note that flat/negative scores can also mean: (a) the base model
isn't capable enough — structural knobs fix *form*, not reasoning the model lacks;
if a stronger/SOTA model is available, add it to the search (model capability is
itself a lever on hard tasks); and (b) a genuine difficulty/annotation ceiling —
after the metric is validated and knobs are complete, if even a strong model fails
the residual items, the ceiling is the data (report it / clean degenerate
references), not more tuning. Distinguish both from "dataset too easy".

### One Iteration = One Hypothesis

Change one thing per round. Good iteration statements look like:

- "Scores are flat because the evaluation dataset lacks hard negatives; add 30 hard negatives."
- "Variance is high because the LLM judge flips on borderline cases; raise repetitions and demote to statistical aggregation."
- "Temperature dominates; narrow temperature and add a retrieval-depth structural knob."

For each round:

1. Write the hypothesis.
2. Make one change.
3. Re-run on the same holdout.
4. Compare to the pinned baseline and previous candidate.
5. Keep a tiny iteration log.

Use `references/iteration-log-template.md` as the 10-line per-iteration log.

**Stop condition (mandatory):** stop iterating and report to the user when any
of these hold — two consecutive rounds with no heldout improvement, the cost
budget or sample quota is exhausted, or the user's goal is met. Never start
another paid round after a stop condition fires without the user's explicit
go-ahead. Iteration is a loop with an exit, not a background process.

### Claim Scope

Iteration decisions are local to the current evaluation dataset, holdout, objective, evaluator, configuration space, and budget. A better next action on one slice does not imply the same action is best after the dataset, evaluator, model provider, or objective weights change.

---

## See Also

- `traigent-optimize-run` - execute approved optimization runs; adjust algorithms, trial budgets, and cost controls.
- `traigent-dataset-curate` - build or improve local evaluation data, follow a returned curation command, and join server-flagged example ids to local content.
- `traigent-eval-audit` - diagnose noisy or biased judge metrics; follow a returned evaluator command.
- `traigent-ci-safety-gate` - follow a returned gate command.
- `traigent-analyze-results` - field-level result reading and stop-reason interpretation.
- `traigent-analyze-variable-importance` - deeper tuned-variable importance and video-card output.
- `traigent-optimize-config-space` - narrow or expand tuned variables.
- `traigent-optimize-composite-knobs` - add structural knobs when scalar knobs are not enough.

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
