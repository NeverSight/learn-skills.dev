---
name: ml-researcher
description: Reason about ML experiment design for healthcare and life sciences data. Use when the user asks to design an ML study, choose a model for clinical/biomedical data, set up cross-validation, pick evaluation metrics, audit fairness, plan a regulatory submission, or critique an ML pipeline on EHR, medical imaging, genomics, molecules, or clinical text. Triggers include "design an ML experiment", "which model for this clinical data", "how should I split", "nested CV", "class imbalance", "AUROC vs AUPRC", "calibration", "decision curve", "net benefit", "TRIPOD+AI", "PROBAST", "CLAIM", "FDA SaMD", "PCCP", "GMLP", "site generalization", "temporal leakage", "scaffold split", "foundation model evaluation", "subgroup fairness", "is this model ready for deployment".
usage: Invoke when designing ML experiments, choosing evaluation strategies, or assessing model readiness for HCLS data.
version: 1.0.0
tags: [skill, category:reasoning, machine-learning, experiment-design, biomedical, hcls]
---

# ML Researcher — Reasoning Skill for HCLS

## Overview

This skill teaches the agent how to *think* about machine learning experiments on healthcare and life sciences data. HCLS ML differs from general ML: samples are scarce, labels are noisy, distributions shift across sites and time, subgroup harms are real, and deployment is governed by reporting standards and regulators. The dominant failure mode is not model choice — it is leakage, miscalibration, and evaluation that does not mirror deployment.

Use this skill to structure a study *before* any code is written, to critique an existing pipeline, or to decide whether a model is ready to advance.

## Usage

Invoke this skill when the user:
- Frames a clinical or biomedical prediction problem and asks how to approach it.
- Shares a dataset description (EHR, WSI, omics, molecules, notes) and asks which model to use.
- Asks about splitting, CV, metrics, calibration, fairness, or reporting.
- Wants a review of an ML plan or manuscript for rigor or regulatory fit.

Outputs should be *prescriptive*: name the design, splits, metrics, and reporting checklist. Challenge assumptions; ask for the index time, the cohort definition, the decision point, and the site structure before recommending models.

## Response Format

- Lead with the direct recommendation or classification (≤3 sentences)
- Structure as: recommendation → justification (citing specific criteria/thresholds) → caveats
- Use tables for comparisons; bullet points for criteria lists
- Omit background the user already knows — they asked the question
- Target: 200-400 words unless the user requests exhaustive detail
The decision trees and frameworks in this skill are for internal reasoning only. Apply them to reach your conclusion, but do not reproduce them in your response. Present only the final recommendation with supporting evidence.


## Core Concepts

### The Mental Model (use every time)

Walk the chain in order. A gap at any link invalidates downstream choices:

1. **Clinical question** — what decision will change?
2. **Target population** — inclusion/exclusion, cohort entry criteria.
3. **Decision point** — the moment the model is queried in the clinical workflow.
4. **Outcome definition** — label, adjudication, censoring, time window.
5. **Data-generating process** — how features arrive, missingness mechanism, site/device variation.
6. **Evaluation mirroring deployment** — same population, same decision point, same features available at prediction time, same temporal/site boundary.

If evaluation does not mirror deployment, the model is not evaluated.

### Key Terms

- **Index time**: the timestamp at which prediction is made. Everything after is forbidden as a feature.
- **Observation window**: lookback period for features, ending at index time.
- **Prediction gap**: buffer between index time and outcome window (prevents target leakage).
- **Horizon**: outcome window length.
- **Patient-level grouping**: no patient appears in more than one split.
- **Site-level holdout**: at least one site/hospital never seen in training.
- **Scaffold split**: molecules grouped by Bemis–Murcko scaffold so test scaffolds are unseen.

---

## Experiment Design for Biomedical Data

### Small Samples, High Dimensions (n < p)

Common in omics, rare-disease imaging, biomarker discovery.

- Use **nested cross-validation**: outer loop estimates performance, inner loop tunes hyperparameters. A single CV loop overfits hyperparameters to the test folds.
- Prefer **regularized models**: elastic net, ridge, sparse GBM with early stopping.
- Use **stability selection** (subsample + refit + count feature selection frequency) rather than a single feature ranking.
- **Never** perform feature selection, normalization, or imputation on the full dataset before CV. All preprocessing must be refit inside each training fold.
- Report confidence intervals from the outer folds, not point estimates.

### Class Imbalance

Default stance: **do nothing to the data.**

Decision tree:

```
Is the positive class rare (e.g., <10%)?
├── No → standard training, report AUPRC alongside AUROC.
└── Yes → Is the model's ranking adequate (AUPRC vs. prevalence baseline)?
         ├── Yes → shift the decision threshold to match clinical costs.
         │        Use decision curve analysis to pick the operating point.
         └── No → try class weights or focal loss BEFORE resampling.
                  If you must resample:
                    - Resample only the training fold.
                    - Recalibrate probabilities afterward (Platt/isotonic on held-out fold).
                    - Never resample the validation or test fold.
```

Resampling distorts the prior and breaks calibration. Most "imbalance problems" are really threshold problems.

### Temporal Leakage

Patients are longitudinal. Random splits leak the future into the past.

For every feature, ask: *Was this value known at index time?* If not, it cannot be used.

Required construction:
- Define **index time** per patient.
- Define **observation window** (e.g., 365 days lookback).
- Define **prediction gap** (e.g., 24 hours) between index time and outcome window start.
- Define **horizon** (e.g., 30-day mortality).
- Use **forward-chaining CV**: train on [t0, t1], validate on [t1, t2], advance. No future peeking.
- Hold out the most recent time period as a final temporal test set.

---

## Model Selection by Data Modality

Default choices. Deviate only with justification.

| Modality | First choice | Strong alternative | Notes |
|---|---|---|---|
| Tabular clinical (structured EHR, labs, vitals) | Logistic regression + elastic net | XGBoost / LightGBM | Start linear for interpretability and calibration. Tree GBMs usually win accuracy with modest gain. |
| Medical imaging (2D, 3D, WSI) | Transfer learning from ImageNet/RadImageNet/foundation models | nnU-Net for segmentation | Fine-tune with aggressive augmentation; freeze early layers on small data. |
| Temporal EHR (sequences of events) | GRU or Transformer with time embeddings | Tabularize (aggregate over windows) + GBM | Tabularized GBM is a hard baseline; beat it before claiming a sequence model helps. |
| Genomics (expression, methylation) | Elastic net on pathway-aggregated features | GNN on protein–protein-interaction graph | Pathway aggregation reduces dimension and increases biological interpretability. |
| Graphs / small molecules | GNN (GIN, D-MPNN) with **scaffold splits** | Fingerprint + GBM | Random splits on molecules overstate performance 2–5×. |
| Clinical text | Domain-adapted encoders (ClinicalBERT, BioClinicalBERT, Gatortron) | Instruction-tuned clinical LLM with retrieval | General-domain BERT underperforms; adapt to clinical vocabulary. |

### Decision Tree: Model Selection

```
What is the input?
├── Structured rows (one row per patient) → Tabular branch
│     ├── n small or interpretability required → logistic + elastic net
│     └── n moderate/large, accuracy priority → GBM (XGBoost/LightGBM)
├── Images → Imaging branch
│     ├── Classification → transfer learning (foundation model preferred if in-domain)
│     └── Segmentation → nnU-Net
├── Longitudinal events → Temporal branch
│     ├── Fixed feature set works → tabularize + GBM (baseline, often wins)
│     └── Irregular, long sequences, rich history → Transformer with time encoding
├── Sequences with biology (DNA/RNA/protein) → specialized encoder or pathway features
├── Molecules → GNN with scaffold split (or fingerprint + GBM baseline)
└── Free text → domain-adapted encoder; RAG if generative
```

Always run a trivial baseline (majority class, logistic regression, or existing clinical score). If the deep model cannot beat it by a clinically meaningful margin, stop.

---

## Cross-Validation Pitfalls

The split defines the claim. Match the split to the deployment claim.

- **Patient-level grouping is mandatory.** No patient in both train and test. Violating this is the single most common error in HCLS ML papers.
- **Site-level holdout** when the claim is "generalizes across hospitals." Hold out entire sites, not random patients across sites.
- **Temporal holdout** when the claim is "works prospectively." Train on older data, test on newer.
- **Scaffold splits** for molecules; time-based splits for drug discovery when assay dates exist.
- **Preprocessing inside the fold.** Normalization, imputation, feature selection, and oversampling are part of the model and must be refit inside each training fold. Leakage here is invisible and common.
- **Leakage audit checklist:**
  - Any feature derived from the label?
  - Any feature computed with information after index time?
  - Any patient, visit, image, or molecule scaffold in both splits?
  - Any normalization statistic computed on the full dataset?
  - Any hyperparameter chosen using the test set?

### Decision Tree: Which Split?

```
What claim is being made?
├── "Works on new patients at this hospital" → patient-level random split
├── "Works at other hospitals" → site-level holdout (leave-site-out CV)
├── "Works in the future" → temporal holdout + forward-chaining CV
├── "Works on new chemical series" → scaffold split
└── "Works on a new population/demographic" → demographic holdout + subgroup eval
```

---

## Three-Layer Evaluation

Report all three. Always.

1. **Discrimination** — can the model rank positives above negatives?
   - AUROC (overall ranking).
   - AUPRC (especially if prevalence < 10%; report prevalence as the baseline).
2. **Calibration** — do predicted probabilities match observed rates?
   - Calibration slope and intercept.
   - Brier score.
   - Reliability diagram with confidence bands.
   - Miscalibrated probabilities are clinically dangerous even when AUROC is high.
3. **Clinical utility** — does using the model improve decisions?
   - Decision curve analysis (DCA) / net benefit across the clinically plausible threshold range.
   - Compare against: treat-all, treat-none, and current standard of care.
   - A model can have higher AUROC and lower net benefit than standard care.

### Decision Tree: Evaluation Strategy

```
Is the task classification with a clinical decision attached?
├── Yes → discrimination + calibration + DCA (all three).
│         Report subgroup performance for prespecified groups.
└── No (ranking only, research use) → discrimination + calibration; DCA optional.

Is prevalence < ~10%?
├── Yes → lead with AUPRC, include AUROC; show PR curve.
└── No → AUROC primary, AUPRC secondary.

Are probabilities used downstream (risk communication, triage threshold)?
├── Yes → calibration is mandatory. Recalibrate on a held-out fold if off.
└── No → calibration still reported for transparency.
```

---

## Fairness and Subgroup Analysis

Bias in HCLS data is rarely random. Labels themselves encode historical care disparities.

- **Prespecify subgroups** (sex, race/ethnicity as socially constructed, age band, insurance, site). Do not go fishing after seeing results.
- Report **discrimination, calibration, and net benefit per subgroup**. A model can discriminate equally well and still harm a subgroup through miscalibration.
- Prefer **equalized subgroup net benefit** over strict demographic parity. Parity metrics (equal FPR, equal selection rate) can reduce overall utility *and* harm the worst-off group. Net benefit directly captures clinical consequence.
- **Audit label bias.** If the label is "received treatment X," disparities in access become disparities in labels. Triangulate with outcome-based labels where possible.
- When subgroup n is small, report wide intervals rather than hiding the group.

---

## Reporting Standards

Match the standard to the artifact:

- **TRIPOD+AI** — development/validation of prediction models. Default for most HCLS ML papers.
- **PROBAST+AI** — risk-of-bias assessment. Use to self-audit before submission.
- **CLAIM 2024** — medical imaging AI reporting.
- **MI-CLAIM-GEN** — generative AI in medicine.
- **STARD-AI** — diagnostic accuracy studies with AI.
- **SPIRIT-AI / CONSORT-AI** — protocols and reports of AI trials.

Require the checklist before writing. Missing items are almost always missing experiments, not missing sentences.

---

## FDA Regulatory Considerations (US)

For models intended as Software as a Medical Device (SaMD):

- **AI-DSF** (AI/ML-Enabled Device Software Functions) guidance scopes what counts and what documentation is expected.
- **Predetermined Change Control Plan (PCCP)** lets sponsors specify the kinds of updates (retraining cadence, new data sources, performance bounds) that may be made post-clearance without a new submission. Define it early.
- **GMLP** (Good Machine Learning Practice) ten principles — multidisciplinary teams, representative data, independent train/test, model design fit for clinical workflow, human-in-the-loop performance, deployed-model monitoring.
- Most HCLS ML devices are **Class II**, cleared via **510(k)** (predicate device exists) or **De Novo** (novel, low-to-moderate risk, no predicate). Class III (PMA) is rare for ML.
- Even for non-regulated research models, applying GMLP and PCCP thinking catches real problems early.

---

## When NOT to Use This Skill

- Deploying a model to production without engineering review
- When the task requires real-time inference optimization (systems engineering)
- Building data pipelines or MLOps infrastructure (use platform-specific tools)

## When to Escalate to a Human Expert

- Before submitting SaMD (Software as Medical Device) to FDA
- When model fairness audit reveals disparities across protected groups
- When clinical validation requires prospective trial design

## Common Mistakes

Each of these invalidates a study. Treat finding any of them as a stop-the-line event.

- **Wrong:** Including features derived from post-outcome data (e.g., post-event labs, discharge codes) in the training set
  **Right:** Audit every feature against the index time — only data available at the decision point may be used
  **Why:** Outcome-containing features yield near-perfect AUROC in development and zero real-world performance

- **Wrong:** Randomly splitting longitudinal patient data or molecular datasets without respecting grouping
  **Right:** Use patient-level grouping for clinical data and scaffold splits for molecules — no entity in both train and test
  **Why:** Random splits leak future information or structural similarity, producing inflated performance estimates (2–5× overstatement for molecules)

- **Wrong:** Reporting only AUROC on imbalanced data (prevalence < 10%)
  **Right:** Always report AUPRC with prevalence baseline and decision curve analysis alongside AUROC
  **Why:** AUROC can be 0.95 while the model is clinically useless — AUPRC and DCA reveal whether the model helps at realistic operating points

- **Wrong:** Using resampling (SMOTE, oversampling) as the primary fix for class imbalance
  **Right:** Adjust the decision threshold first; if resampling is truly needed, apply only within training folds and recalibrate afterward
  **Why:** Resampling distorts the prior and breaks probability calibration — most "imbalance problems" are actually threshold problems

- **Wrong:** Claiming generalizability from a single-site study
  **Right:** Require site-level holdout or external validation from a different hospital/scanner/EHR vendor
  **Why:** One site's data reflects its specific population, workflows, and coding practices — this does not generalize

- **Wrong:** Evaluating a foundation model on data that overlaps with its pretraining corpus
  **Right:** Demand a clean, post-cutoff, or curated held-out benchmark with no pretraining overlap
  **Why:** Any overlap between pretraining data and evaluation set inflates performance and masks true generalization ability

- **Wrong:** Computing normalization statistics, imputation parameters, or feature selection on the full dataset before splitting
  **Right:** Refit all preprocessing steps inside each training fold — treat them as part of the model
  **Why:** Full-dataset preprocessing leaks test-set information into training, producing optimistic and unreproducible results

- **Wrong:** Tuning hyperparameters using the test set (single-loop CV)
  **Right:** Use nested CV — outer loop for performance estimation, inner loop for hyperparameter tuning
  **Why:** Test-set tuning reports a tuned score, not a generalization estimate — the test set is no longer independent

- **Wrong:** Skipping subgroup analysis because subgroup sample sizes are small
  **Right:** Report subgroup performance with wide confidence intervals rather than hiding the group
  **Why:** Small subgroups are often the most vulnerable to model harm — silence about them is not safety

- **Wrong:** Deploying a model with high AUROC without checking calibration
  **Right:** Always assess calibration (slope, intercept, reliability diagram) — recalibrate if probabilities do not match observed rates
  **Why:** Probabilities drive thresholds, triage, and patient communication — an uncalibrated model with high AUROC is clinically dangerous

---

## Readiness Checklist (use before claiming a model is ready)

- [ ] Clinical question, decision point, and deployment workflow written down.
- [ ] Index time, observation window, prediction gap, and horizon defined per patient.
- [ ] Splits match the deployment claim (patient, site, temporal, scaffold).
- [ ] All preprocessing refit inside each training fold.
- [ ] Nested CV if n is small; forward-chaining CV for temporal claims.
- [ ] Trivial and clinical-score baselines reported.
- [ ] Discrimination + calibration + decision curve analysis reported.
- [ ] Prespecified subgroup analyses with intervals.
- [ ] Reporting checklist (TRIPOD+AI or modality-specific) completed.
- [ ] External validation plan and, if SaMD, GMLP + PCCP outline.
- [ ] Leakage audit completed and documented.

If any box is unchecked, the answer to "is it ready?" is no.

## References

- TRIPOD+AI: Collins et al. BMJ 2024, https://doi.org/10.1136/bmj-2023-078378
- PROBAST+AI: Wolff et al. BMJ 2024, https://doi.org/10.1136/bmj-2023-078434
- CLAIM 2024: Mongan et al. Radiology:AI 2024, https://doi.org/10.1148/ryai.230513
- FDA AI/ML SaMD guidance: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-software-medical-device
- Decision curve analysis: Vickers et al. Med Decis Making 2006, https://doi.org/10.1177/0272989X06295361
