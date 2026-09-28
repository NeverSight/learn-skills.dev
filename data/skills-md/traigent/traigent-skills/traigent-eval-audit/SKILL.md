---
name: traigent-eval-audit
description: "Audit evaluator reliability before trusting Traigent optimization decisions. Use when users ask: is my LLM judge reliable, audit my evaluator, does my exact-match or deterministic scorer fit the task, validate my evaluation policy, judge agreement, evaluator calibration, calibrate thresholds, parse-failure policy, repeated-judge stability, bias probes, or when optimization results depend on an LLM-as-judge metric."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: evaluation
  traigent-maturity: stable
  author: Nimrod
  version: "1.1.10"
---

# Evaluator Audit

## When to Use

Use this skill before trusting an evaluator that drives optimization decisions, especially an LLM judge. Trigger it for:

- "is my LLM judge reliable?"
- "audit my evaluator"
- "judge agreement"
- "calibrate thresholds"
- "why are my optimization results noisy?"

On the **no-gold track** (no ground-truth labels; the judge is the entire quality signal — see
`traigent-eval-choose-metric` → "The no-gold track"), this audit is **mandatory before the first paid
optimization run**, not an optional check: without it you may be optimizing judge noise.

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

**This skill's part:** produce independently confirmed defect receipts — each one an example
hash, a defect category, an independent confirmation, and the correction or test — so the
work can be compared honestly against what the same review would have cost by hand.

**Mandatory whenever you relay any of it:** show the options, recommend exactly one, and
explain **why in the user's own numbers** — their agent, their volumes, their error costs. The
explanation is a product requirement, not decoration.

Safety is unchanged and unweakened: mock/dry-run first, **explicit user approval before any
paid run**, an explicit spend cap, and the recorded stop rule. The service sets
*how much* to invest; it never affects *whether* approval is required — it always is.

## Service-Side Evaluator Audit

Traigent can assess the evaluators used in a completed run, server-side and **read-only**, when
your deployment is IP-allowlisted for the backend endpoint. It reuses evidence the run already
produced, so it needs **no new gold-label collection** and no local re-scoring. It surfaces as
an evaluator-audit next-step action when the endpoint is available.

**Give it something independent to check against.** The audit is only as confident as the
run's independent correctness signal — execution match, unit-test pass, or exact match where
the task allows one. Choosing a task shape that admits such a signal is the single biggest
thing you control here.

The verdict is read through `GET /api/v1/analytics/runs/{run_id}/evaluator-quality` (viewer
role), which returns a deliberately coarse projection: a verdict, opaque evaluator identifiers,
and a bounded confidence figure. Internal detail is not returned — do not attempt to
reconstruct it or to reimplement the audit client-side.

**Fail-closed honest confidence.** With no independent signal available for the run, the audit
**abstains**: no leaderboard is emitted and no promote gate passes. A weaker substitute signal
(another model or a heuristic) is accepted but carries a hard confidence ceiling and can never
be promoted to the same standing. Do not read an abstain as a pass, and do not cite a
substitute-signal result as equivalent to an independently verified one.

The manual gold-slice protocol below and the service-side audit are complementary: the
gold-slice protocol gives early construction-time trust, while the service audit is a
retroactive quality signal computed from real runs.

## Why Audit

An unreliable evaluator silently corrupts every optimization decision downstream. If the judge rewards verbosity, misses parse failures, changes labels on repeated calls, or disagrees with humans on the target evaluation dataset, the optimizer can faithfully optimize the wrong thing.

Run the audit before the first real optimization, then re-run it whenever the judge model, prompt, output schema, scoring rubric, or evaluation dataset changes.

## Task-Fit Calibration (any evaluator, deterministic first)

Before trusting a comparator or a judge, run it over at least four authored answers per
materially distinct case — `good`, `equivalent_good` (same correctness in another accepted form:
case, spacing, an alias, a markdown fence), `partial`, `bad` — and record the score mode from the
product decision **before** any score exists: `graded` requires good ≈ equivalent_good > partial >
bad; `binary` requires both goods to pass and partial **and** bad to fail. Reject the evaluator
when: all scores are equal; all 0 or all 1; `equivalent_good` is penalized for surface form;
in `graded` mode `partial` ≥ `good` or ≤ `bad`, in `binary` mode `partial` passes; `bad` passes; or an exception is silently scored 0. Add two probes
you may not revise — the expected answer permuted, and a malformed output — they raise questions,
never verdicts. Never widen the scorer until a probe passes; record the equivalent it cannot reach
as a coverage gap instead. Re-run after any evaluator repair.

A prior run's calibration record (the guided first run leaves one under `traigent-runs/`) is this
protocol already run once: start from what it left open, on the customer's own evaluation policy.

## Gold-Set Agreement (Manual Protocol)

Build a human-labeled gold slice of at least 30 examples (50-100 when you can) from the same evaluation dataset distribution the optimizer will use, but **disjoint from the holdout** that will back the final claim — draw it from the tuning slice or from fresh examples, never from holdout rows. Include easy, borderline, and known-bad cases; if known-bad (negative) cases are naturally rare — the common situation for safety gates — **oversample them deliberately**, because the false-pass bar below is meaningless on two negatives. Lock the labels before inspecting judge outputs. Below about 60 gold rows, calibrate the threshold with k-fold cross-validation (see "Threshold Calibration") rather than a split: a 30-row slice split in half leaves 15 reporting rows, where even 15/15 cannot clear the 85% agreement bar.

> **The disjointness invariant (applies across all evaluator skills):** any slice used to *tune*
> a threshold, rubric, prompt, or metric must be disjoint from the holdout used to *claim* the
> result. Calibrating on rows that later back the claim is leakage — the exact failure this
> audit exists to catch.

Minimum bars for the manual gold-slice protocol before trusting the judge as a primary optimizer objective:

- Parse success rate: at least 98% on the gold slice.
- Human agreement: at least 85% exact agreement for categorical pass/fail labels, or rank correlation above 0.70 for ordinal scores.
- False-pass rate on known-bad cases: low enough for the product risk. For safety or compliance gates, any repeated false pass is a blocker.
- Disagreement review: every disagreement gets a written reason, assigned to either human label error, ambiguous rubric, judge failure, or data ambiguity.

These bars are estimates from a few dozen examples. The resolution step is 2-4 points (1/n), and the
sampling noise is larger (about 4-7 points standard error). Treat a bar as cleared only when the
**95% Wilson lower bound**, computed on the **reporting rows**, clears it. The reporting rows are the
rows the threshold was not chosen on: the held-out part of a split, or all n rows when every row is
scored out-of-fold by k-fold cross-validation. For the 85% agreement bar that means at least 30/30 at
n=30, 48/50 at n=50, or 92/100 at n=100 reporting rows. Below 22 reporting rows it cannot be cleared
at all (21/21 has a lower bound of 84.5%), so grow the slice. Report the interval, not only the point
estimate, and never report a near-bar pass as confident.

```python
from math import sqrt
from statistics import mean

def agreement_rate(gold_labels, judge_labels):
    pairs = list(zip(gold_labels, judge_labels, strict=True))
    return mean(1.0 if expected == observed else 0.0 for expected, observed in pairs)

def wilson_interval(successes, n, z=1.96):
    p = successes / n
    denominator = 1 + z * z / n
    center = p + z * z / (2 * n)
    half_width = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (center - half_width) / denominator, (center + half_width) / denominator

gold = ["pass", "fail", "pass", "fail"]
judge = ["pass", "fail", "fail", "fail"]
agree = sum(expected == observed for expected, observed in zip(gold, judge, strict=True))
low, high = wilson_interval(agree, len(gold))
print(f"agreement={agreement_rate(gold, judge):.1%} 95% CI=[{low:.1%}, {high:.1%}] clears_85={low >= 0.85}")
```

If the judge misses the bar, do not use it as the sole objective. Fix the rubric, add deterministic checks, or use it only as a diagnostic signal.

## Stability Across Repetitions

Run the same input through the same judge N times, with the same prompt, model version, sampling settings, and output schema. Use at least 3 repetitions for cheap judges and 5 for noisy judges.

Track:

- Score standard deviation for numeric outputs.
- Pass/fail flip rate for categorical outputs.
- Parse-failure count per repetition.
- Whether the same rationale supports the same label.

Demote the judge to statistical aggregation when repeated calls are unstable. Use mean or majority vote over repetitions, raise repetitions per trial, and report wider uncertainty. A single-call judge with high flip rate should not decide close candidates.

## Bias Probes

Probe known LLM-judge failure modes before optimization:

- Position bias: score answer A vs answer B, then swap order. A reliable pairwise judge should not change the winner only because the order changed.
- Length and verbosity bias: compare a concise correct answer against a verbose equivalent answer. The verbose answer should not win solely because it is longer.
- Self-preference: blind model identity and prompt style. If the judge favors outputs from its own family or from one template, use anonymized outputs and shuffle metadata.
- Tie sanity: compare an answer to itself. The judge should return a tie or equal score.
- Adversarial polish: compare a polished but wrong answer against a rough correct answer. The correct answer must not lose because it reads better.

These probes are drawn from the same failure modes discussed in the MT-Bench LLM-judge literature. Keep the probes in the audit artifact so future prompt or model changes can be rechecked.

## Parse-Failure Policy

<!-- PROTECTED -->
Use a strict output schema. Count parse failures as first-class failures. FAIL-CLOSED: a parse failure is a score of 0 or an abstain, never a silent pass.
<!-- /PROTECTED -->

```python
import json
import math
from typing import Any

REQUIRED_KEYS = {"score", "decision", "reason"}

def parse_judge_output(raw: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")
        missing = REQUIRED_KEYS - set(payload)
        if missing:
            raise ValueError(f"missing keys: {sorted(missing)}")
        if payload["decision"] not in {"pass", "fail", "abstain"}:
            raise ValueError("decision must be pass, fail, or abstain")
        if isinstance(payload["score"], bool):
            raise ValueError("score must be a number, not a boolean")
        score = float(payload["score"])
        # NaN, Infinity and wrong-scale scores (e.g. 7 on a 1-10 scale) are parse failures, not passes.
        if not math.isfinite(score) or not 0.0 <= score <= 1.0:
            raise ValueError("score must be a finite number in [0, 1]")
        return {**payload, "score": score, "parse_failed": False}
    except (json.JSONDecodeError, TypeError, ValueError):
        return {
            "score": 0.0,
            "decision": "abstain",
            "reason": "parse failure",
            "parse_failed": True,
        }
```

Report parse-failure rate separately from model quality. A low score caused by parse failures calls for schema repair, not prompt or model tuning.

## Threshold Calibration

Sweep the judge threshold against the gold slice before using it in optimization. Choose the threshold that matches product risk:

- For quality ranking, maximize balanced accuracy or F1 on the gold slice.
- For safety gates, prefer lower false-pass rate even if recall drops.
- For noisy judges, require a margin: do not treat scores near the threshold as confident passes.

Never report the agreement and false-pass bars on the rows used to pick the threshold: those bars
are optimistic. Below about 60 gold rows, use k-fold cross-validation (for example 5-fold): pick the
threshold on k-1 folds, apply it to the held-out fold, and report the bars on the pooled out-of-fold
decisions, so all n rows are reporting rows. With 60 or more rows a split is enough: choose the
threshold on one part and report the bars on the other, keeping at least 30 reporting rows.

```python
def confusion_counts(gold_pass, scores, threshold):
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for expected_pass, score in zip(gold_pass, scores, strict=True):
        observed_pass = score >= threshold
        if expected_pass and observed_pass:
            counts["tp"] += 1
        elif not expected_pass and observed_pass:
            counts["fp"] += 1
        elif not expected_pass and not observed_pass:
            counts["tn"] += 1
        else:
            counts["fn"] += 1
    return counts

for threshold in [0.60, 0.70, 0.80, 0.90]:
    print(threshold, confusion_counts(gold_pass, judge_scores, threshold))
```

Lock the chosen threshold before running optimization. Do not tune the threshold on the same holdout used to claim the final result — the gold slice used for this sweep must already be holdout-disjoint (see the disjointness invariant above).

## When to Demote to Hybrid

Use a hybrid evaluator when the judge is useful but not reliable enough to own the whole metric:

1. Run deterministic gates first: schema validity, required fields, exact-match invariants, safety keyword blocks, citation presence, cost and latency caps.
2. Send only the residue to the LLM judge.
3. Treat deterministic failures as hard failures.
4. Aggregate judge outputs statistically when repeated calls are noisy.
5. Report deterministic-fail, parse-fail, judge-fail, and judge-pass counts separately.

Hybrid evaluation is the default for high-risk workflows: deterministic gates protect non-negotiable behavior, and the judge handles semantic residue.

## Evaluator Repair (`improve_evaluator`)

The service may emit `improve_evaluator` as a next-step action when the audit identifies a weak or suspicious evaluator. This is a service-side repair flow, not a local prompt edit.

A repair is only accepted if it demonstrably improves on data that was **not** used to produce it. Do not accept or apply a repaired evaluator on the strength of the proposal alone — the held-out result is the acceptance gate.

If the service emits `improve_evaluator`, present the returned action verbatim and hand off to this skill for context. Wait for the service outcome rather than rewriting the rubric locally.

## Claim Scope

Audit results hold only for the audited evaluation dataset distribution, judge model version, judge prompt, output schema, sampling settings, and threshold. Re-audit on any model, prompt, schema, rubric, or dataset-distribution change.

For service-side audits: the confidence ceiling is a hard cap, not a display hint. A result based on a substitute signal cannot be cited as independently verified evidence. Promotion requires a service-audit verdict backed by an independent, verifiable correctness signal — an abstain, a substitute-signal result, or manual gold-slice calibration alone is not sufficient for promotion.

**Precondition — an audit needs an anchor, and the released SDK gives you no way to declare
one.** A service-side audit is anchored: it scores your evaluator against a verifiable
correctness signal computed *independently of that evaluator*. The anchor is designated
**server-side**, from the independent correctness signal registered for the run; you never
name one yourself. The service will not infer which signal applies, so a run with no such
signal registered resolves to "no anchor" and the audit abstains: on a real text-to-SQL run
against the portal on 2026-09-13 the payload read `status: abstain`, `reason: audit_abstained`,
`anchor.anchor_type: none`, `evaluators: []`.

There is no client-side field for this on the released SDK. `EvaluationOptions` forbids
unknown fields, so `EvaluationOptions(task_type="exact_match")` raises
`ValidationError: Extra inputs are not permitted` at construction on traigent 0.27.0 — do
**not** pass `task_type`. A coarse task-category field is expected in a later SDK release,
but it is in no released version, so nothing you write against the released SDK today
designates an anchor. Only exact-match-style anchors exist at all, and free-form tasks have
none by construction, so for those an abstain is the honest answer rather than a fixable
problem.

The promotion gate itself is served by two advisory, anchor-gated endpoints over one optimization run:

- `POST /api/v1/analytics/runs/{run_id}/evaluator-promotion/evaluate` (editor role) — computes and **persists** an advisory challenger-vs-incumbent promotion decision from evaluator fingerprints (`challenger_fingerprint` required, optional `incumbent_fingerprint`, `delta`, `min_pairs`). It never mutates experiments, sessions, evaluator configs, or optimization state — the decision record is advisory.
- `GET /api/v1/analytics/runs/{run_id}/evaluator-promotion` (viewer role) — lists the run's persisted advisory promotion decisions, newest first (`limit` up to 100).

Treat the returned decision as the promotion-gate evidence; do not recompute or overrule it locally.

## See Also

- `traigent-eval-build` - build the evaluator before auditing it.
- `traigent-eval-choose-metric` - choose objectives and weights before threshold calibration.
- `traigent-dataset-curate` - synthesize harder cases when the gold slice is too easy or ambiguous.

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
