---
name: traigent-analyze-variable-importance
description: "Show tuned-variable associations and rank which variables differed within a Traigent optimization. Use for: show significant tuned variables, which variables mattered, tuned variable importance, feature importance for optimization, within-run score associations, parameter importance with honest confidence labels, or one-glance video card summaries of observed score differences."
license: Apache-2.0
metadata:
  traigent-audience: sdk-user
  traigent-topic: agent-optimization
  traigent-stage: analyze
  traigent-maturity: stable
  author: Nimrod
  version: "1.2.0"
---

# Show Significant Tuned Variables

## Purpose

Use this skill to show which tuned variables were associated with score differences within an
optimization run. It ranks configuration knobs by effect size, adds honest confidence labels, and
emits a one-glance SVG video card suitable for demos or review.

The bundled script is designed for Traigent text2sql demo artifacts but works with any JSONL trial file that has a numeric objective and a `config` object.

## When to Use

Use this skill when the user asks:

- "show significant tuned variables"
- "which variables mattered?"
- "tuned variable importance"
- "feature importance for optimization"
- "which variables were associated with score differences?"
- "make a video card for the important knobs"

The script ranks knobs within **one run's** trials. For multi-run evidence, fetch the cohort table,
export each run's rows to a separate per-run trials JSONL, run the script per run, and compare the
rankings across runs. Do not concatenate runs into one file; mixed search spaces or objectives
corrupt the ranking.

## Inputs

The script accepts:

- `--trials`: required JSONL, one trial per line. Each row must contain `config` and a numeric objective such as `accuracy`.
- `--config-space`: optional JSON object `{knob: [values...]}`. If absent, the script infers knobs and values observed in trials.
- `--heldout`: optional heldout report JSON with `baseline`, `optimized`, and `delta`. When present, the video card uses the heldout optimized-vs-baseline accuracy and cost deltas for context.
- `--objective`: objective field to maximize. This must exactly match the metric key present in each
  trial row of `--trials` (typically `accuracy`, but a text2SQL run may score under `exec_accuracy` or
  another custom `metric_functions` key) — it is not a fixed literal. An empty or all-`directional`
  `importance.json` means insufficient variation in the trials for this objective, not "no knob
  matters" — check that `--config-space` values were actually sampled and that there are enough
  trials per value before concluding a knob is unimportant.
- `--sampling-design`: `randomized`, `adaptive`, or `unknown` (default). Choose `randomized` only
  when knob assignments were independent of outcomes and time/order effects, so trial labels are
  exchangeable under the no-effect null, **and** each knob was assigned independently of every
  other knob (no constraints or conditional knobs); otherwise use `unknown`. The test is per knob,
  so a no-effect knob that a constrained space ties to a real one inherits that knob's effect.
  Adaptive optimizer output and results whose assignment process is not known remain directional
  even when their adjusted p-values are small.
- `--alpha`: family-wise significance level for the Holm-adjusted permutation test (default
  `0.05`, at most `0.10`). It is written into every `importance.json` row and `video_card.json`.
- `--confidence`: bootstrap CI confidence for the whiskers (default `0.9`). Display only; it does
  not change any label.
- `--bootstrap-draws`: bootstrap and permutation draws per knob (default `2000`). A `significant`
  label needs `draws + 1 >= 10 x eligible knobs / alpha`; the default covers up to 10 knobs at
  alpha 0.05. When `insufficient_permutation_resolution` appears, `insights.md` names the draws to
  rerun with.

Present objectives must be finite numeric values; booleans, NaN and infinity are rejected with
the input file and row number. Supplied costs must also be finite and nonnegative. Missing costs
remain unavailable, while a measured zero stays zero. Permutation comparisons count numerical
roundoff ties conservatively using a tolerance scaled by both the spread and the group means,
so tiny-scale objectives and large-offset ones (token counts, latency in ms) both keep their
true ties. Numbers in a `--heldout` report follow the same finite-number rule, and costs there
must be nonnegative.

An SDK result saved with `save_to=` (for example `traigent-runs/optimized-results.json` after the
guided first run) is one JSON object whose `trials[]` already carry `config` and `metrics` (the
script reads the objective from either the top level or `metrics`); write it out one trial per
line first, then pass that file as `--trials`:

```bash
python3 -c 'import json,sys; [print(json.dumps(t)) for t in json.load(open(sys.argv[1]))["trials"]]' \
  traigent-runs/optimized-results.json > trials.jsonl
```

Failed or pruned trials are skipped automatically (their `status` is not `completed`; a failed
trial still carries a `0.0` score that is not a measurement); the script prints how many and
records the count as `skipped_non_completed` in `video_card.json`. Rows without a `status` field
are read as measured.

Expected trial shape:

```json
{"accuracy": 0.58, "config": {"schema_context": "linked_top10", "fewshot_k": 5}, "mock_cost": 0.02052, "correct": 7, "total": 12, "trial_index": 8}
```

## Outputs

The script writes these files into `--output-dir`:

- `importance.json`: ranked tuned variables with effect fields plus raw `p_value`, Holm
  `p_adjusted`, `family_size`, the `alpha` used, sampling design, sample counts, permutation
  resolution, and an explicit `inference_status`.
- `importance.csv`: flat CSV with the same fields.
- `significant_variables.svg`: hand-written 1280x720 dark-theme SVG with horizontal bars, bootstrap CI whiskers, best-value annotations, and a directional/significance caption.
- `insights.md`: short human-readable summary using honest claim language.
- `video_card.json`: compact payload: `top_variables` (each with the knob's own effect,
  raw/adjusted p-values, family size, and inference status), `n_trials`, `skipped_non_completed`,
  `alpha`, `objective`, run-level `heldout_accuracy_pp`/`heldout_cost_delta_pct`, and `caption`.
- `sdk_cross_check.json`: the SDK variance-based cross-check (`computed`, `note`, `results`);
  `results` is empty when the SDK analyzer was unavailable or returned nothing.

<!-- PROTECTED -->
## Honesty Rule

Never overclaim significance:

- A variable is called `significant` only for an explicitly randomized design, with at least 20
  observations for that knob and 5 observations per value, enough permutation draws for the full
  family, and a Holm-adjusted p-value below `--alpha` (default 0.05). Every other result is
  `directional`, with `inference_status` explaining why.
- Under `randomized`, a knob whose observed values depend on another eligible knob's (pairwise
  chi-square test of independence, p < 0.001) gets `knobs_not_independent` and stays
  `directional`. The screen catches strongly coupled spaces but can miss a mild constraint in a
  small run, so it backs up the `--sampling-design` choice rather than replacing it.
- Holm correction covers every knob with at least two observed values before ranking and `top-k`
  display truncation. `p_value` is the raw permutation result; `p_adjusted` is the family-wise
  value used by the label. The displayed interval is for scale only and must never be used to
  infer significance.
- The minimum attainable permutation p-value is `1 / (draws + 1)`. The script requires ten times
  the family-size/alpha threshold for a statistically significant label; otherwise it reports
  `insufficient_permutation_resolution` instead of a quiet negative.
- The video card's per-knob `accuracy_pp`/`cost_delta_pct` are that knob's own measured effect; the whole-run heldout optimized-vs-baseline delta is reported once as a card-level field, never copied onto each knob.
- The ranking is observational: "on this fixed Spider slice, in this run." It is not proof of causal attribution.
<!-- /PROTECTED -->

**Fewer than 20 trials — a first small run, such as the guided first run's 12-trial search.**
Every row will read `directional`. Present the card as *which knobs to test next*, never
as a ranking that holds: say "n=<trials> — directional; a knob showing no spread was mostly not
sampled enough to show one". Do not rerun the search to reach 20; the run size that can support the
ranking comes from the service plan (`traigent-analyze-guidance`, Mode A), not from this skill.
Pass `--heldout` only when baseline **and** optimized were scored on the same held-out rows; a
held-out score of one selected configuration — what the guided first run reports — is not a
baseline-vs-optimized delta, so leave `--heldout` off and say the held-out check covers the
selected configuration only.

The primary importance is the spread between the best and worst per-value mean objective. The script also reports variance-decomposition share: between-group variance divided by total variance.

## Worked Example

Run with the Python interpreter where you installed the Traigent SDK (`python3`, or your project's
`.venv/bin/python`). Resolve `<skill-dir>` to the directory
containing this `SKILL.md`; plugin and flat-install locations differ.

```bash
python3 <skill-dir>/scripts/significant_tuned_variables.py \
  --trials /path/to/02_trials.jsonl \
  --heldout /path/to/07_heldout_report.json \
  --objective accuracy \
  --top-k 4 \
  --confidence 0.9 \
  --output-dir /tmp/significant-tuned-variables
```

Then inspect:

```bash
cat /tmp/significant-tuned-variables/importance.json
cat /tmp/significant-tuned-variables/video_card.json
```

The generic command leaves `--sampling-design` at its conservative `unknown` default. Add
`--sampling-design randomized` only when a run plan or sampler log verifies all four conditions:
knob assignments were randomized, assignment probabilities did not depend on earlier outcomes,
no time/order trend affected scores, and each knob was assigned independently of the others (no
constraints or conditional knobs). A sampler name or a balanced result table alone is not enough
evidence.

## Method Notes

For each knob, the script groups trials by the knob's value, computes mean objective per value,
ranks by the max-min spread, and reports variance share as a companion statistic. It computes
label-shuffled permutation p-values for all eligible knobs, applies Holm correction across that
fixed family, then sorts for display. Bootstrap confidence intervals use trial resampling with
replacement and fixed seed `55`.

The permutation test assumes exchangeable trial labels: under the null, reassigning observed
objectives among knob values must reproduce the assignment process. Random or independently
randomized search can meet that assumption. Adaptive optimization generally does not because knob
choices depend on earlier outcomes; time trends and sampler choices can then look like effects.
Use `adaptive` or the default `unknown` in those cases. Their effect sizes and p-values remain
exploratory and never receive a statistically significant label.

The script also attempts to adapt trials to `traigent.utils.importance.ParameterImportanceAnalyzer` for a variance-based SDK cross-check. When it returns output, the numbers are written to `sdk_cross_check.json` and to an "SDK cross-check" table in `insights.md`; they never change the ranking or labels. If that adaptation is unavailable or returns no output, it skips gracefully and states that the skill's own variance/bootstrap method was used, inspired by the SDK analyzer. Do not fabricate SDK analyzer output.

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
