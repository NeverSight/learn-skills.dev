---
name: actuarial-risk-modeling
description: >-
  Use when analyzing, selecting, validating, or communicating models for insurance,
  actuarial, financial-risk, or other consequential uncertain outcomes. Covers
  regression, generalized linear models, frequency-severity, panel and longitudinal
  data, survival, time series, credibility, reserving, tail risk, calibration,
  and model governance. Do not use for generic software forecasting, ordinary
  SaaS financial models, or credentialed actuarial, investment, legal, or regulatory
  advice without the relevant specialist review.
license: MIT
---

# Actuarial and Financial Risk Modeling

## Overview

Apply statistical modeling to uncertain outcomes where distributional assumptions,
exposure, dependence, tail behavior, calibration, and decision consequences matter.
The skill is methodology-first: it teaches model selection and evidence, not a
particular library or rating formula.

## When to Use

Load this skill when the task involves:

- insurance pricing, claims, reserving, solvency, risk classification, or experience rating;
- claim frequency, severity, pure premium, medical expenditure, loss, or event-time outcomes;
- linear, generalized linear, two-part, count, survival, panel, longitudinal, or tail models;
- financial returns, volatility, portfolio loss, risk measures, or scenario output;
- calibration, forecast evaluation, backtesting, model comparison, or assumption diagnosis;
- explaining model results, uncertainty, limitations, or use controls to decision-makers.

## When Not to Use

- Use the Decision Entry Points table above for adjacent work. In brief: `data-scientist` owns general statistical, causal, experimental, and machine-learning methodology; `financial-modeling` owns deterministic operating, SaaS, fundraising, and cash-flow models.
- Use a named tool skill for operating a forecasting, database, or modeling platform.
- Do not present output as licensed actuarial, investment, legal, accounting, or regulatory advice. Escalate consequential decisions to qualified practitioners and applicable standards.

## Decision Entry Points

| Starting situation | First move | Load next |
|---|---|---|
| Policy, claim, or loss data | Define grain, exposure, target, and horizon | `references/problem-framing.md` |
| Claims development triangle or reserve estimate | Identify accident/development/calendar structure and valuation boundary | `references/applications-and-governance.md` + `references/validation-and-calibration.md` |
| Financial returns, volatility, or ordered observations | Define information cutoff and forecast horizon | `references/model-families.md` + `references/validation-and-calibration.md` |
| Deterministic SaaS, cash-flow, or fundraising model | Route out of this skill | `financial-modeling` |
| Generic causal, experimental, or ML methodology | Route out of this skill | `data-scientist` |

## Core Workflow

1. **Frame the decision.** State the decision, audience, horizon, unit of observation, estimand or forecast target, action threshold, and cost of false positives and negatives. Separate descriptive, predictive, and causal questions.
2. **Write the data contract.** Define grain, exposure or offset, outcome support, observation and development windows, censoring/truncation, policy or account boundaries, leakage risks, missingness states, and provenance.
3. **Profile before modeling.** Inspect distributions, zeros, negatives, skew, tail concentration, dependence, repeated entities, time ordering, category sparsity, exposure balance, and data-quality exceptions. Use `scripts/risk_preflight.py` for a read-only first pass.
4. **Choose the simplest defensible model family.** Match the outcome and data-generating structure before comparing algorithms. Load `references/model-families.md` for the decision table.

   **Model-selection quick pick:** counts with exposure → count GLM with an offset; zero plus positive loss → two-part/frequency-severity; event time with censoring → survival; ordered observations → dynamic/time-series model; tail decision → tail-aware or quantile model plus stress sensitivity. Load `references/model-families.md` before choosing a specific distribution or link.
5. **Fit without contaminating evaluation.** Treat transformations, imputation, feature selection, calibration, resampling, and hyperparameter choices as part of the fitted procedure. Fit them only on the permitted training partition.
6. **Diagnose and challenge.** Check residual structure, link and variance assumptions, overdispersion, zero inflation, leverage, collinearity, separation, calibration, dependence, censoring, tail fit, and sensitivity to plausible alternatives. A convergence flag is not validation.
7. **Validate for use.** Use grouped, blocked, or rolling splits when the deployment boundary demands them. Report point accuracy, probabilistic scores, calibration, ranking, tail or aggregate-loss behavior, stability across segments, and uncertainty. Use `scripts/temporal_split_audit.py` to audit time-ordered partitions.

   **Validation-design quick pick:** exchangeable observations → random holdout; repeated entities or clusters → grouped split; ordered deployment → blocked or rolling-origin split; overlapping development or labels → gap/embargo; extensive tuning or candidate comparison → nested validation. Load `references/validation-and-calibration.md` before fixing the final design.
8. **Compare and govern.** Prefer a transparent model unless a more complex one earns its complexity on the decision-relevant metric and remains stable, interpretable enough, and monitorable. Record assumptions, overrides, limitations, approvals, and rollback or review triggers.
9. **Communicate the decision.** Use `templates/model-report.md` and state what was observed, inferred, assumed, estimated, not identified, and not tested. Include units, intervals, scenario definitions, diagnostics, and a plain-language recommendation.

## Required Distinctions

- **Frequency is not severity.** A count model and a positive-loss model have different supports, exposures, diagnostics, and aggregation rules.
- **Prediction is not causation.** A useful rating variable is not automatically a fair causal explanation or a permitted classification factor.
- **Calibration is not discrimination.** A model can rank well while producing systematically wrong probabilities.
- **Backtesting is not proof.** Historical success can reflect regime, selection, leakage, or unavailable information.
- **Uncertainty is layered.** Separate sampling error, parameter uncertainty, process variance, model-form uncertainty, scenario uncertainty, and data-quality uncertainty.
- **A reserve or risk estimate is a decision input.** It is not an objective fact independent of horizon, assumptions, and intended use.

## Minimum Analysis Contract

Before presenting a recommendation, state: the decision and estimand; row grain, horizon, exposure, and information cutoff; candidate model family and why its support/dependence assumptions fit; validation boundary and metrics; uncertainty and sensitivity; limitations and permitted use. If one of these is unknown, label it as an unresolved input rather than silently choosing a convention.

## Failure-Mode Quick Map

| Symptom | First checks | Route |
|---|---|---|
| Many zeros or variance above the mean | Exposure, structural zeros, overdispersion, dependence | `references/model-families.md` |
| Strong ranking but wrong probabilities | Segment calibration, population shift, recalibration boundary | `references/validation-and-calibration.md` |
| Random CV beats next-period performance | Feature availability, entity/time leakage, revisions, drift | `references/validation-and-calibration.md` |
| Estimate moves with a few large losses | Provenance, tail fit, threshold, stress and scenario sensitivity | `references/applications-and-governance.md` |
| “No event” before full development | Censoring, observation horizon, reporting lag | `references/problem-framing.md` |

## Reference Routing

| Reference | Load when |
|---|---|
| [Problem framing](references/problem-framing.md) | The target, grain, exposure, estimand, or decision is ambiguous |
| [Model families](references/model-families.md) | Selecting regression, GLM, count, severity, survival, panel, time-series, or tail models |
| [Validation and calibration](references/validation-and-calibration.md) | Designing splits, backtests, metrics, calibration, uncertainty, or stress tests |
| [Applications and governance](references/applications-and-governance.md) | Working on pricing, reserving, solvency, credibility, risk classification, or model use controls |
| [Diagnostics and communication](references/diagnostics-and-communication.md) | Reviewing assumptions, interpreting output, or writing a decision-safe report |
| [Source index](references/source-index.md) | Checking authoritative references, scope, or currency |

## Templates and Scripts

Use the templates by stage: `model-brief.md` before data work; `validation-plan.md` before fitting or release; `model-report.md` for findings and decisions; `model-governance-record.md` for controlled deployment, review, monitoring, or retirement.

First-pass scripts are read-only: run `python3 scripts/risk_preflight.py input.csv --output preflight.json` before fitting, and `python3 scripts/temporal_split_audit.py observations.csv --time-column observed_at --output splits.json` when ordered data or forecast leakage is possible.

- `templates/model-brief.md` — decision, data contract, estimand, and acceptance criteria.
- `templates/validation-plan.md` — split design, metrics, calibration, stress tests, and release gates.
- `templates/model-report.md` — evidence-led analysis and communication structure.
- `templates/model-governance-record.md` — ownership, assumptions, limitations, approvals, monitoring, and retirement triggers.
- `scripts/risk_preflight.py` — dependency-free, read-only CSV/JSONL profiling with machine-readable output.
- `scripts/temporal_split_audit.py` — dependency-free audit of chronological train/test windows and leakage boundaries.

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/risk_preflight.py` | Read-only profiling pass over a CSV or JSONL input: distributions, zeros, negatives, skew, repeated entities, exposure balance, and data-quality exceptions, written as machine-readable JSON. Run it at workflow step 3, before any modeling, to profile the data before framing the model family. | `python3 scripts/risk_preflight.py input.csv --output preflight.json` |
| `scripts/temporal_split_audit.py` | Audits chronological train/test windows and leakage boundaries in an ordered observation file (`--time-column` required; optional `--test-size`, `--step`, `--gap`, `--output`). Run it at workflow step 7 whenever observations are time-ordered or forecast leakage is possible, before trusting any validation result. | `python3 scripts/temporal_split_audit.py observations.csv --time-column observed_at --output splits.json` |
| `scripts/test_risk_scripts.py` | Offline pytest suite covering both scripts above. Run it if you modify either script or when auditing a change to their output. | `python3 -m pytest scripts/test_risk_scripts.py` |

Both analysis scripts are dependency-free and never modify their inputs.

## Completion Gate

Do not call a model analysis complete until the decision and data contract are explicit,
the evaluation design matches intended use, diagnostics and sensitivity are recorded,
uncertainty and limitations are stated, and an independent reader could reproduce the
reported result from the cited data, code, assumptions, and environment.

## Prerequisites

- Python 3 with standard library only; both analysis scripts are dependency-free and require no third-party packages.
- A CSV or JSONL input with a documented data contract: grain, exposure or offset, outcome support, observation window, and time column (for the split audit) — the scripts profile what you point them at, not what the data means.
- `pytest` only when running the bundled script tests.

## Limitations

- The scripts perform first-pass profiling and split auditing only: no model fitting, selection, calibration, or validation metrics happen here, and a clean preflight does not validate a model.
- Neither script modifies its inputs; both write reports to stdout or an `--output` path for you to interpret under the Required Distinctions above.
- Output is evidence about the data and partition design, not licensed actuarial, investment, legal, accounting, or regulatory advice (see When Not to Use).
