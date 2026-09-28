---
name: traigent-ci-safety-gate
description: "Add Traigent safety and promotion gates to CI. Use when users ask to add safety constraints, gate the optimized config, prevent regressions in CI, enforce cost or latency budgets, compare candidate versus incumbent, validate TVL specs, or write GitHub Actions for agent optimization safety."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: gate-debug
  traigent-maturity: stable
  author: Nimrod
  version: "1.0.6"
---

# CI Safety Gate

## When to Use

Use this skill when the user asks:

- "add safety constraints"
- "gate the optimized config"
- "prevent regressions in CI"
- "cost/latency budget"
- "GitHub Actions for my agent"

<!-- PROTECTED -->
The gate should fail closed: missing metrics, NaN metrics, parse failures, rejected promotion decisions, and budget breaches should stop promotion.
<!-- /PROTECTED -->

The reference gate rejects non-finite or negative cost and latency limits, malformed or
non-finite measurements, negative latency, and accuracy outside `[0, 1]`. Boolean values are
not measurements. The holdout adapter validates each call's cost before accumulating it.

## In-Run Safety Constraints (Not Yet Available)

`safety_constraints=[...]` on `@traigent.optimize` is planned to filter unsafe trial results during optimization, but the installed SDK does not implement it yet. Passing any non-empty value raises `NotImplementedError: safety_constraints are not yet implemented` **at decoration time** (verified against SDK 0.18.x); statistical chance-constraints are on the roadmap. The `SafetyConstraint`, `CompoundSafetyConstraint`, `MetricKeyMetric`, `CallableMetric`, and `SafetyThreshold` classes exist and import cleanly, but do not pass any of them via `safety_constraints=` today.

Do not teach a `safety_constraints=[...]` code sample as runnable. For gating today, use the two mechanisms this skill already covers that ARE implemented:

- **`PromotionGate`** (below) to statistically compare a candidate config against the incumbent before promoting it.
- **TVL spec validation** (`python -m traigent.tvl ... --strict`) to enforce configuration-space and objective constraints ahead of a run.

Keep safety semantics simple, explicit, and reviewable regardless of mechanism: schema validity, refusal policy, citation checks, cost caps, and latency caps.

## Promotion Gate

Use `PromotionGate` to compare a candidate config against the incumbent on the same holdout. `evaluate` returns a decision with `decision` equal to `promote`, `reject`, or `no_decision`.

The holdout is rows the optimization's `eval_dataset` never scored: the candidate was selected on
those tuning rows, so its tuning score is optimistic, and gating on them re-measures the selection,
not the promotion. It is also not a ten-row split an assistant built and can read (what a guided first run
leaves under `traigent-runs/`) — that is held-back and non-blind, and on ten rows a statistical gate can
only separate a very large lift — a modest one reads `no_decision`; build a sealed slice sized for the effect you require. The gate judges
**one** committed candidate: re-running it over several candidates until one promotes turns the
holdout into a selection set and forfeits the guarantee. Traigent does not manage this split for you.

```python
from traigent.tvl.models import PromotionPolicy
from traigent.tvl.promotion_gate import ObjectiveSpec, PromotionGate

policy = PromotionPolicy(
    dominance="epsilon_pareto",
    alpha=0.05,
    min_effect={"accuracy": 0.01, "latency_ms": 25.0},
    adjust="BH",
)
objectives = [
    ObjectiveSpec(name="accuracy", direction="maximize"),
    ObjectiveSpec(name="latency_ms", direction="minimize"),
]

gate = PromotionGate(policy=policy, objectives=objectives)
decision = gate.evaluate(
    incumbent_metrics={"accuracy": [0.81, 0.82, 0.80], "latency_ms": [880, 900, 870]},
    candidate_metrics={"accuracy": [0.84, 0.85, 0.83], "latency_ms": [910, 905, 920]},
)
print(decision.decision, decision.reason)
```

A statistical gate can tell you whether the candidate has enough evidence to promote, reject, or remain undecided on the measured evaluation dataset. It cannot prove universal safety, discover unmeasured regressions, or rescue a biased evaluator.

Validate TVL specs in CI before running the gate:

```bash
python -m traigent.tvl path/to/promotion-gate.tvl.yml --strict
```

Name specs `*.tvl.yml` (or `*.tvl.yaml`): the validator discovers only those in a directory, and it
exits 0 when it finds no spec at all, even after printing `ERROR: File not found` for a missing
path. So a CI step must assert that at least one spec exists, as the workflows below do.

## Applying the Winning Config

This skill covers the gate in the export -> gate -> apply flow. For the full
end-to-end flow, see `traigent-boost-agent` → Fast Path, Step 5 ("Do not promote
the winner straight into production …"). Keep promotion staged: export the winning config as a candidate, run the
holdout/promotion gate, then apply only after the gate passes and the user
approves.

```python
# Export the winning config as a CANDIDATE artifact for review/gating
my_function.export_config("candidate_config.json")

# After the holdout/promotion gate passes and the user approves:
my_function.apply_best_config(results)
answer = my_function("What is Python?")
```

## The Two CI Checks

SAFETY: run a holdout regression check against a pinned baseline config.

- Pull request job: run offline/mock under `TRAIGENT_OFFLINE_MODE=true` to verify wiring, script shape, and fail-closed behavior without spending.
- Scheduled job: run the real holdout evaluation under `TRAIGENT_RUN_COST_LIMIT` with account credentials and compare candidate vs incumbent. That limit bounds only calls placed through the SDK; the holdout script's own provider calls are bounded by the script (rows × configs × a per-call cap), and it must write the **measured** `total_cost` — a `0.0` placeholder or a missing field would make `--max-cost` pass vacuously, so the holdout script refuses a `0.0` total after real calls (cost is not wired) and the gate script refuses a missing, NaN or negative field.

Any CI workflow that executes `optimize()` or `optimize_sync()` in local/offline mode, including
mock/offline wiring checks, must set `TRAIGENT_RUN_APPROVED=1`. This is the SDK's explicit
approval signal for approved CI runs, not a bypass; cloud-mode runs are unaffected.

EFFICIENCY: assert `results.total_cost` and latency metrics remain within budget. Fail the job on cost breach, latency breach, rejected promotion, missing metrics, parse failures, or safety regression.

### Key Hygiene in CI

CI logs are shareable artifacts — visible to every collaborator with repo access and often
retained for months. The same leaks apply here, at a larger blast radius, and have been observed
across multiple coding-agent CLI families (Codex, Claude, Gemini) authoring the workflow — this is
a universal agent failure mode, not one CLI's quirk:

- **Never print, echo, or log a key value** in a workflow step. `echo $TRAIGENT_API_KEY`, an
  `env`/`printenv` dump, and `set -x` wrapped around a key-touching step all write the raw secret
  into the CI run log.
- **Reference keys only by env-var name**, wired `${{ secrets.* }}` → job/step `env:` — never
  inline a literal key value in the workflow YAML or a script.
- **GitHub Actions masks only registered secrets.** It redacts values it was told about via
  `secrets:`; a value reconstructed, echoed through an intermediate variable, or printed by
  `set -x` before the secret is registered can bypass masking — so the rules above still apply.

Minimal GitHub Actions shape:

```yaml
name: Traigent safety gate

on:
  pull_request:

permissions:
  contents: read

jobs:
  # PR job: offline wiring check only — static env, zero spend. The paid
  # nightly job is a separate job with its own static env; see
  # references/gate-workflow.md for the full two-job workflow.
  safety-gate:
    runs-on: ubuntu-latest
    env:
      TRAIGENT_RUN_COST_LIMIT: "0.00"
      TRAIGENT_OFFLINE_MODE: "true"
      TRAIGENT_RUN_APPROVED: "1"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - name: Validate TVL specs (fail if none found)
        run: |
          set -euo pipefail
          mapfile -t specs < <(find tvl -name '*.tvl.yml' -o -name '*.tvl.yaml' 2>/dev/null)
          [ "${#specs[@]}" -gt 0 ] || { echo "no *.tvl.yml specs under tvl/" >&2; exit 1; }
          python -m traigent.tvl "${specs[@]}" --strict --verbose
      - run: python scripts/run_holdout_eval.py --mode mock --config configs/baseline.json --output .gate/incumbent.json
      - run: python scripts/run_holdout_eval.py --mode mock --config configs/candidate.json --output .gate/candidate.json
      - run: python scripts/traigent_gate.py --incumbent .gate/incumbent.json --candidate .gate/candidate.json --max-cost 0.01 --max-latency-ms 1200
```

For a full copy-paste workflow and gate script, read `references/gate-workflow.md`.

Planned: a `traigent ci` command group will package these checks; the manual recipe stays valid.

## Claim Scope

Gate decisions are statistical decisions on the measured evaluation dataset and configured objectives, not broad safety claims. Re-run the gate when the evaluation dataset, evaluator, baseline config, candidate config, objective weights, provider, or budget changes.

## See Also

- `traigent-optimize-run` - cost limits, algorithms, and stop reasons.
- `traigent-analyze-results` - result fields, best config, cost, and stop-reason interpretation.
- `traigent-analyze-guidance` - decide what to change after a failed or inconclusive gate.

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
