---
name: fairness-medical-imaging
description: Use this skill when the user is investigating bias, fairness, shortcut learning, or protected-attribute effects in a medical imaging model. Triggers include "my model is biased towards X", "check for shortcut learning", "fairness analysis for my segmentation model", "does my classifier depend on site/scanner", "evaluate performance across demographic subgroups", "concept erasure for medical images", or "detect spurious correlations in medical AI". Handles bias diagnosis, protected attribute analysis, fairness metric selection, mitigation strategy, and evaluation protocol. Do not use for general model evaluation without a fairness hypothesis — use pre-submission-review or paper-analyst instead.
license: MIT
metadata:
  category: "Domain: Medical Imaging"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Fairness in Medical Imaging

A skill for diagnosing and mitigating bias, shortcut learning, and protected-attribute dependence in medical imaging AI systems. VIOS has deep expertise here — including SWiFT (soft-mask weight fine-tuning for bias mitigation), CRCE (concept erasure in diffusion models), and systematic shortcut detection in clinical datasets.

## When to invoke this skill

- A classification or segmentation model shows performance disparities across patient subgroups (age, sex, race, scanner, institution)
- You suspect a model is using a spurious feature (e.g., hospital-specific tag, image border, demographic proxy) rather than the clinical signal
- You want to design a fairness evaluation before submitting to a clinical AI venue (Nature Medicine, MICCAI, MELBA)
- You are building a synthetic data pipeline and need to evaluate whether it inherits or amplifies biases
- You want to apply concept erasure or latent space disentanglement to remove a protected attribute's influence

## Workflow

### 1. Define the fairness hypothesis

Before any experiment, state the hypothesis explicitly:

```
Hypothesis: Model M uses [spurious feature S] as a proxy for [target label Y], 
causing performance to drop for subgroup [G] when [S] is absent / differs from training.
```

Identify:
- **Protected attributes**: sex, age group, race, scanner model, acquisition site, annotation source
- **Spurious features**: image borders, DICOM header artefacts, pathology prevalence by site, protocol-specific image quality
- **Fairness notion**: equalised odds, demographic parity, calibration by group, worst-group accuracy

Different fairness notions are appropriate for different clinical contexts — equalised odds matters for screening; calibration matters for risk scoring.

### 2. Stratified evaluation

Run inference and stratify results by each protected attribute:

| Metric | Per subgroup | Gap threshold |
|--------|-------------|---------------|
| AUC | Report mean ± std per group | Flag if max − min > 0.05 |
| Dice / F1 | Report per group | Flag if max − min > 0.03 |
| Calibration (ECE) | Report per group | Flag if any group ECE > 0.10 |
| Sensitivity / Specificity | Report per group | Flag clinical implication |

For segmentation: always split at **patient level**, not slice level. Slice-level aggregation inflates N and hides per-patient variance.

### 3. Shortcut diagnosis

If a performance gap is found, diagnose the cause:

**Test 1 — Shuffle the protected attribute**:
Train on data where the protected attribute label is randomly permuted. If performance drops to chance, the model was using it. If performance holds, the attribute was not a primary feature.

**Test 2 — Occlusion / GradCAM by subgroup**:
Compare saliency maps between high-performing and low-performing subgroups. If saliency peaks on clinically irrelevant regions (image border, corner artefact) for the low-performing group, a shortcut is confirmed.

**Test 3 — Domain shift probing**:
If scanner/site is the protected attribute: train on sites A,B; test on site C. A large gap between in-distribution and out-of-distribution performance indicates the model learned site-specific features.

**Test 4 — Concept activation vectors (CAVs)**:
For protected attributes like sex or age: train a linear probe on the model's penultimate layer to predict the protected attribute. If the probe accuracy >> chance, the representation encodes the protected attribute even if the label was not used in training.

### 4. Mitigation strategy selection

Choose based on the diagnosis:

| Diagnosis | Recommended mitigation | VIOS reference |
|-----------|----------------------|----------------|
| Model encodes protected attribute in representation | **SWiFT** — soft-mask weight fine-tuning to suppress attribute-predictive weights | Yan et al., MELBA 2025 |
| Spurious concept baked into diffusion model | **CRCE** — coreference-retention concept erasure | Xue et al., BMVC 2025 |
| Distribution shift by acquisition site | Domain generalisation via causal shift model | Machlanski et al., arXiv 2025 |
| Training data imbalance by subgroup | Re-weighting or resampling; check that validation set is balanced before declaring success | — |
| Annotation bias (label noise correlates with demographic) | Separate label noise study; do not conflate annotation bias with model bias | — |

### 5. Post-mitigation evaluation

After applying mitigation:
1. Re-run stratified evaluation (Step 2). Report **both** overall performance and per-group performance.
2. Check that overall performance has not degraded beyond an acceptable threshold (typically ≤ 1% Dice drop, ≤ 0.02 AUC drop for the primary metric).
3. Verify that the protected attribute probe (Step 3, Test 4) accuracy is reduced.
4. Report the fairness–utility trade-off explicitly: "Mitigation reduced the sex-gap in AUC from 0.08 to 0.02, with a 0.5% drop in overall AUC."

### 6. Reporting checklist for venue submission

For MICCAI, Nature Medicine, MELBA, IEEE TMI:
- [ ] Protected attributes and their distributions in the dataset are reported in a demographics table
- [ ] Fairness notion used is defined and justified for the clinical context
- [ ] Stratified results are in a dedicated table (not buried in supplementary)
- [ ] Mitigation method described with sufficient detail to reproduce
- [ ] Fairness–utility trade-off curve or table provided
- [ ] Limitations: which subgroups had insufficient sample size for reliable stratification

## Anti-patterns

- **Do not** report only aggregate AUC and claim fairness — subgroup gaps can be large even when aggregate metrics look good.
- **Do not** conflate "the model doesn't explicitly use sex as a feature" with "the model is fair" — proxy learning via correlated features is the most common failure mode.
- **Do not** apply mitigation and evaluate only on the overall metric — this hides whether the gap was actually closed.
- **Do not** split data at the slice/patch level when protected attribute is at the patient level — this leaks patient identity across train/test and inflates performance estimates.
- **Do not** claim a method is fair on one dataset and generalise — fairness properties are dataset- and deployment-context-specific.

## See also

- `causal-dag-builder` for encoding the causal structure of protected attributes, mediators, and outcomes before choosing a fairness notion.
- `medical-image-synthesis` if synthetic data augmentation is the proposed mitigation.
- `venue-reviewer` for venue-specific fairness reporting requirements (MICCAI vs. Nature Medicine differ significantly).
