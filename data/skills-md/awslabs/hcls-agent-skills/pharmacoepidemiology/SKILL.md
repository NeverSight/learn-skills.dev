---
name: pharmacoepidemiology
description: Reason about pharmacoepidemiologic study design for causal inference from real-world data — choosing active comparator new-user designs, emulating target trials, avoiding immortal time bias, handling time-varying confounding with marginal structural models, and selecting propensity score methods. Use when the user asks to design a drug safety or effectiveness study, choose between propensity score matching vs weighting vs stratification, emulate a target trial, handle immortal time bias, apply marginal structural models, assess unmeasured confounding with E-values, select an active comparator, define a new-user cohort, or evaluate a pharmacoepidemiology study design. Triggers include "active comparator", "new-user design", "target trial emulation", "immortal time bias", "propensity score matching", "IPTW", "marginal structural model", "confounding by indication", "E-value", "negative control outcomes", "quantitative bias analysis", "time-varying confounding", "prevalent user bias", "washout period", "landmark analysis", "stabilized weights".
usage: Invoke when designing, critiquing, or planning pharmacoepidemiologic studies using claims, EHR, or registry data.
version: 1.0.0
tags: [skill, category:reasoning, pharmacoepidemiology, causal-inference, propensity-score, real-world-data, hcls]
---

# Pharmacoepidemiology Study Design

## Overview

This skill teaches the agent how to *think* about pharmacoepidemiologic study design — the discipline of estimating causal drug effects from non-randomized real-world data (claims, EHR, registries). The core challenge is confounding: patients who receive Drug A differ systematically from those who receive Drug B, and naive comparisons conflate treatment effects with selection effects.

A well-designed pharmacoepidemiology study addresses this through three pillars: (1) a **new-user active comparator design** that aligns time zero and reduces confounding by indication, (2) **propensity score methods** or **target trial emulation** to balance measured confounders, and (3) **sensitivity analyses** to probe the impact of unmeasured confounding.

Use this skill to interrogate study designs, identify bias sources, and guide the user toward defensible causal inference *before* analysis code is written.

## Usage

Invoke this skill when the user:

- Wants to estimate the effect of a drug on a clinical outcome using observational data.
- Asks how to choose a comparator group for a drug safety or effectiveness study.
- Needs to decide between propensity score matching, weighting, or stratification.
- Describes a cohort design that may contain immortal time bias.
- Asks about target trial emulation or how to map observational data to a hypothetical RCT.
- Has time-varying treatments or confounders and needs marginal structural models.
- Wants to assess sensitivity to unmeasured confounding (E-value, negative controls).
- Is reviewing or critiquing a published pharmacoepidemiology study.

The agent should respond by:

1. **Clarifying the causal question** — what treatment, what comparator, what outcome, what population, what time horizon.
2. **Checking the design** — is it new-user? Is the comparator active? Is time zero aligned?
3. **Identifying bias threats** — immortal time, confounding by indication, prevalent user bias, time-varying confounding.
4. **Recommending a propensity score approach** — matching, IPTW, or stratification based on the study context.
5. **Specifying sensitivity analyses** — E-value, negative controls, quantitative bias analysis.

## Response Format

- Lead with the direct recommendation or classification (≤3 sentences)
- Structure as: recommendation → justification (citing specific criteria/thresholds) → caveats
- Use tables for comparisons; bullet points for criteria lists
- Omit background the user already knows — they asked the question
- Target: 200-400 words unless the user requests exhaustive detail
The decision trees and frameworks in this skill are for internal reasoning only. Apply them to reach your conclusion, but do not reproduce them in your response. Present only the final recommendation with supporting evidence.


## Core Concepts

### 1. The New-User (Incident User) Design

The foundation of modern pharmacoepidemiology. Every study should start here.

**Rules:**

1. **Index date = first dispensing (or first prescription) of the study drug** after a clean washout period.
2. **Washout period**: require 180–365 days of continuous enrollment with no dispensing of the study drug. This excludes prevalent users who may have already experienced early events or side effects.
3. **Exclude prevalent users.** Patients already on the drug at cohort entry are a biased survivor population — they tolerated the drug long enough to still be on it. Including them introduces depletion-of-susceptibles bias.
4. **Baseline covariates are measured before the index date.** Nothing after index date enters the propensity model.
5. **Follow-up starts at the index date.** Time zero is the moment of treatment initiation, not some earlier eligibility date.

#### Why prevalent users are dangerous

| Problem | Mechanism |
|---|---|
| **Depletion of susceptibles** | Patients who had early adverse events already stopped the drug and are absent from the prevalent-user pool |
| **Undefined baseline** | Covariates measured "at baseline" are actually post-treatment for prevalent users |
| **Adjusted prevalence** | Duration of prior use varies, making the cohort a mixture of different exposure histories |

### 2. Active Comparator Design

**Rule: Compare Drug A vs Drug B, not Drug A vs no drug.**

Comparing treated patients to untreated patients introduces massive confounding by indication — the reason a patient receives a drug is correlated with their outcome risk. An active comparator (another drug for the same indication) ensures both groups have the indication, reducing this bias.

#### Decision tree: choosing a comparator

```
Start
│
├── Is there another drug for the same indication?
│     ├── Yes → Use it as the active comparator.
│     │         Prefer a drug with similar:
│     │         - Indication (same disease stage/severity)
│     │         - Channeling (similar patient profile)
│     │         - Time trends (used in the same era)
│     └── No  → Consider:
│               - Non-pharmacologic standard of care
│               - Delayed/deferred treatment (with careful time-zero alignment)
│               - Document residual confounding by indication as a limitation.
│
├── Multiple candidate comparators available?
│     └── Prefer the one with the most clinical overlap.
│         Run the primary analysis with the best comparator;
│         use others in sensitivity analyses.
│
└── Is the comparator a drug from the same class?
      ├── Within-class comparison → smaller confounding, but smaller effect sizes.
      └── Between-class comparison → larger confounding, but more clinically relevant contrast.
```

### 3. Target Trial Emulation

Map every observational study to a hypothetical randomized trial. This framework forces explicit specification of each design element and reveals hidden assumptions.

| Target trial component | Specification in observational data |
|---|---|
| **Eligibility criteria** | Inclusion/exclusion applied at time zero (index date) using pre-index data only |
| **Treatment strategies** | Initiate Drug A vs initiate Drug B (new-user design) |
| **Treatment assignment** | Observational — handled by propensity scores or IP weighting |
| **Follow-up start** | Index date (= treatment initiation). Must be identical for both arms |
| **Outcome** | Same definition as the target trial; ascertained after time zero |
| **Causal contrast** | Intention-to-treat (follow regardless of adherence) or per-protocol (censor/weight at discontinuation) |
| **Analysis plan** | Pre-specified; registered if possible |

**Critical rule:** If any component cannot be mapped cleanly, the study has a structural bias that no statistical method can fix. The most common failure is misaligned time zero (see immortal time bias below).

### 4. Immortal Time Bias

Immortal time is the period between cohort entry and treatment start during which the outcome *cannot* occur (because occurrence of the outcome would prevent the patient from being classified as treated). Misclassifying this time inflates survival in the treated group.

**How it arises:**

- Cohort entry is defined by diagnosis, but treatment starts later. The gap is "immortal" for the treated group — they had to survive long enough to receive treatment.
- Comparing "ever-treated" vs "never-treated" without aligning time zero.

**Solutions:**

| Method | How it works | When to use |
|---|---|---|
| **New-user design** | Time zero = treatment initiation; no gap exists | Default — prevents the problem entirely |
| **Landmark analysis** | Define a fixed time point (e.g., 90 days post-diagnosis); classify exposure status at the landmark; start follow-up there | When treatment timing varies and you want a common time origin |
| **Time-varying exposure** | Model treatment as a time-dependent covariate in a Cox model; person-time before treatment counts as unexposed | When treatment can start at any time and you want to use all person-time |

**Rule:** If the study compares "ever-users" vs "never-users" with follow-up starting at a time point before treatment initiation, immortal time bias is present. The new-user design eliminates it by construction.

### 5. Propensity Score Methods

The propensity score (PS) is the probability of receiving treatment A (vs B) conditional on measured baseline covariates. It reduces a high-dimensional covariate space to a single balancing score.

#### Estimation

1. Fit a logistic regression: `treatment ~ age + sex + comorbidities + prior_meds + ...`
2. Include all pre-index covariates that predict treatment, outcome, or both. Do NOT include instruments (variables that predict treatment but not outcome) — they increase variance without reducing bias.
3. Check overlap: both groups should have PS distributions that substantially overlap. Trim or truncate extreme weights if needed.

#### Three approaches

| Method | Mechanism | Strengths | Limitations |
|---|---|---|---|
| **Matching (1:1, caliper)** | Pair each treated patient with the nearest untreated patient within a caliper (typically 0.2 × SD of logit-PS) | Intuitive; easy to check balance; mimics an RCT | Discards unmatched patients → reduced sample size and generalizability |
| **IPTW (inverse probability of treatment weighting)** | Weight each patient by 1/PS (treated) or 1/(1−PS) (comparator) to create a pseudo-population | Uses all patients; estimates ATE; flexible | Extreme weights destabilize estimates; requires truncation or stabilized weights |
| **Stratification** | Divide PS into quantiles (typically 5–10); estimate treatment effect within each stratum; pool | Simple; transparent | Residual confounding within strata; less precise than IPTW |

#### Decision tree: which PS method?

```
Start
│
├── Is sample size limited or matching feasible?
│     ├── Yes → 1:1 PS matching with caliper = 0.2 × SD(logit-PS).
│     │         Report number matched and unmatched.
│     └── No  → Continue.
│
├── Do you need the full sample (e.g., rare outcome)?
│     ├── Yes → IPTW. Use stabilized weights. Truncate at 1st/99th percentile
│     │         if max weight > 10.
│     └── No  → Continue.
│
├── Is the goal transparency and simplicity?
│     └── PS stratification (5–10 strata). Report stratum-specific effects.
│
└── Multiple analyses?
      └── Use matching as primary, IPTW as sensitivity (or vice versa).
          Concordant results strengthen the conclusion.
```

#### Balance diagnostics

After PS adjustment, verify covariate balance:

- **Standardized mean difference (SMD)**: target < 0.1 for all covariates. SMD = |mean_treated − mean_comparator| / √((s²_treated + s²_comparator)/2).
- **Variance ratios**: should be between 0.5 and 2.0.
- **Visual**: Love plot (dot plot of SMDs before and after adjustment).
- **Do NOT use p-values** for balance assessment — they conflate balance with sample size.

**Rule:** If any covariate has SMD > 0.1 after adjustment, the PS model is inadequate. Add interactions, non-linear terms, or additional covariates and re-estimate.

### 6. Covariate Selection for Confounding Adjustment

Which variables to include in the propensity score or outcome model is a design decision, not a data-driven one. Get it wrong and the estimate is biased or inefficient.

#### Rules for covariate inclusion

1. **Include confounders** — variables that cause both treatment and outcome. These are the primary targets.
2. **Include outcome risk factors** — variables that predict the outcome but not treatment. They reduce variance (increase precision) without introducing bias.
3. **Exclude instruments** — variables that predict treatment but NOT outcome. Including them amplifies bias from unmeasured confounding and inflates variance.
4. **Exclude mediators** — variables on the causal pathway between treatment and outcome. Adjusting for them blocks part of the effect you are trying to estimate.
5. **Exclude colliders** — variables caused by both treatment and outcome (or their descendants). Conditioning on a collider opens a non-causal path and introduces bias.

#### Typical covariate categories in claims data

| Category | Examples | Measurement window |
|---|---|---|
| Demographics | Age, sex, race, region | At index date |
| Comorbidities | Charlson/Elixhauser score, specific ICD-10 codes | 365 days pre-index |
| Comedications | Concurrent drug classes (statins, antihypertensives) | 180 days pre-index |
| Healthcare utilization | Hospitalizations, ED visits, outpatient visits, distinct prescribers | 365 days pre-index |
| Disease severity proxies | Number of specialist visits, prior procedures, lab orders | 365 days pre-index |
| Frailty indicators | Skilled nursing facility use, home oxygen, wheelchair claims | 365 days pre-index |
| Calendar time | Year/quarter of index date | At index date |

**Rule:** Always include a measure of healthcare utilization intensity. Patients who interact more with the healthcare system are more likely to receive new drugs and to have outcomes detected — this is a major confounder in claims data.

#### Proxy variables and the healthy-user bias

Claims data lack direct measures of lifestyle (smoking, BMI, exercise, diet). Patients who initiate preventive medications (e.g., statins, vaccines) tend to be healthier and more health-conscious. This **healthy-user/healthy-adherer bias** can make new drugs appear protective simply because their users are healthier. Mitigate by:

- Including preventive care markers (flu vaccination, cancer screening) as covariates.
- Using negative control outcomes to detect residual healthy-user bias.
- Reporting the E-value to quantify how strong unmeasured healthy-user confounding would need to be.

### 7. Time-Varying Confounding and Marginal Structural Models

Standard regression fails when a confounder is both:
- Affected by prior treatment (e.g., lab values change because of the drug), AND
- A predictor of future treatment and outcome.

Adjusting for such a confounder blocks part of the treatment effect (over-adjustment); not adjusting leaves confounding. This is the **treatment-confounder feedback** problem.

**Solution: Marginal Structural Models (MSMs) with stabilized IPTW.**

Steps:

1. At each time point, estimate the probability of receiving the observed treatment given past treatment and covariate history (denominator of the weight).
2. Estimate the probability of receiving the observed treatment given past treatment only (numerator — stabilized weight).
3. Stabilized weight = cumulative product of (numerator / denominator) over time.
4. Fit a weighted outcome model (e.g., weighted pooled logistic regression or weighted Cox model) using these weights.

**Rules for MSMs:**

- Stabilized weights should have a mean near 1.0. If not, the model is misspecified.
- Truncate extreme weights (e.g., at 1st and 99th percentiles) and report sensitivity to truncation thresholds.
- The denominator model must include all time-varying confounders; the numerator model includes only baseline covariates and past treatment.
- MSMs estimate a *marginal* (population-average) causal effect, not a conditional one.

### 8. Sensitivity Analyses for Unmeasured Confounding

No observational study can rule out unmeasured confounding. Quantify its potential impact.

| Method | What it does | When to use |
|---|---|---|
| **E-value** | Reports the minimum strength of association (on the risk ratio scale) that an unmeasured confounder would need with both treatment and outcome to explain away the observed effect | Always — report alongside primary results |
| **Negative control outcomes** | Outcomes known to be unaffected by the treatment; a non-null association signals residual bias | Include 3–5 negative controls; if they show associations, the primary result is suspect |
| **Negative control exposures** | Exposures known to be unrelated to the outcome; test whether the analytic pipeline produces null results for them | Useful for validating the study design |
| **Quantitative bias analysis (QBA)** | Formally models the impact of a hypothesized unmeasured confounder with specified prevalence and effect sizes | When a specific unmeasured confounder is suspected (e.g., smoking, BMI in claims data) |

**Rule:** Every pharmacoepidemiology study should report at minimum the E-value and include at least one negative control analysis.

### 9. Key Design Decisions Summary Table

| Design element | Recommended approach | Red flag |
|---|---|---|
| User type | New (incident) users only | Prevalent users included without justification |
| Comparator | Active comparator (same indication) | Non-users or general population as comparator |
| Time zero | Treatment initiation date | Diagnosis date with treatment starting later |
| Washout | 180–365 days | No washout or < 90 days |
| Covariates | Pre-index only | Post-index covariates in PS model |
| PS balance | SMD < 0.1 for all covariates | Balance not reported or p-values used instead of SMD |
| Follow-up | Starts at index date | Starts before treatment (immortal time) |
| Causal contrast | ITT or per-protocol (explicit) | Undefined or as-treated without censoring weights |
| Sensitivity | E-value + negative controls | No sensitivity analysis for unmeasured confounding |

### 10. Intention-to-Treat vs Per-Protocol in Observational Data

| Contrast | Implementation | Bias concern |
|---|---|---|
| **ITT analog** | Follow from index date regardless of adherence or switching | Diluted effect if many patients switch or discontinue |
| **Per-protocol analog** | Censor at treatment discontinuation or switching; use IPCW (inverse probability of censoring weights) to adjust for informative censoring | Informative censoring if sicker patients stop treatment |

**Rule:** The ITT analog is the default because it avoids informative censoring. Use the per-protocol analog only when the clinical question specifically concerns sustained treatment, and always apply IPCW.

## When NOT to Use This Skill

- Replacing pre-specified statistical analysis plans (needs biostatistician sign-off)
- When unmeasured confounding is the primary concern and no negative controls exist
- Individual patient risk-benefit decisions (clinical medicine, not epidemiology)

## When to Escalate to a Human Expert

- When study results will be submitted to regulatory agencies as RWE
- When E-value suggests unmeasured confounding could explain the entire effect
- When the target trial protocol requires clinical input on eligibility criteria

## Common Mistakes

- **Wrong:** Including prevalent users in the study cohort
  **Right:** Always require a 180–365 day washout period and restrict to new initiators
  **Why:** Depletion of susceptibles biases toward a protective effect

- **Wrong:** Comparing drug users to non-users
  **Right:** Use an active comparator with the same indication
  **Why:** Confounding by indication is nearly impossible to fully adjust for without an active comparator

- **Wrong:** Starting follow-up before treatment initiation (immortal time)
  **Right:** Use the new-user design (time zero = treatment start) or a landmark analysis
  **Why:** The treated group gets "free" survival time, inflating apparent benefit

- **Wrong:** Including post-index covariates in the propensity score model
  **Right:** Only include covariates measured before the index date in the PS model
  **Why:** Post-index variables may be mediators or colliders, introducing bias

- **Wrong:** Using p-values to assess covariate balance after PS adjustment
  **Right:** Use standardized mean differences (SMD) with a threshold of < 0.1
  **Why:** P-values depend on sample size and can show "balance" in large samples despite meaningful differences

- **Wrong:** Ignoring extreme propensity score weights
  **Right:** Truncate weights at the 1st/99th percentile and report sensitivity to truncation
  **Why:** A single patient with weight 500 can dominate the entire analysis

- **Wrong:** Adjusting for time-varying confounders in a standard Cox model
  **Right:** Use marginal structural models with stabilized IPTW when confounders are affected by prior treatment
  **Why:** Standard adjustment blocks part of the causal pathway when treatment-confounder feedback exists

- **Wrong:** Omitting sensitivity analyses for unmeasured confounding
  **Right:** Always report the E-value and run at least one negative control analysis
  **Why:** Claims data lack BMI, smoking, lab values, and socioeconomic detail that may confound results

- **Wrong:** Running "as-treated" analyses without defining the causal contrast
  **Right:** Explicitly specify ITT or per-protocol estimand and apply censoring weights for per-protocol
  **Why:** Ambiguous estimands produce uninterpretable results

- **Wrong:** Defining exposure based on cumulative dose over follow-up or "ever-use"
  **Right:** Define exposure at time zero; do not condition on future behavior or survival
  **Why:** Conditioning on the future introduces selection bias

- **Wrong:** Ignoring the positivity assumption
  **Right:** Check PS overlap and trim non-overlapping regions where one treatment has near-zero probability
  **Why:** PS methods break down in strata with no treatment variation

- **Wrong:** Using a single PS method without sensitivity analysis
  **Right:** Run at least two approaches (e.g., matching + IPTW) and compare results
  **Why:** Discordant results signal model sensitivity and fragile conclusions

- **Wrong:** Failing to pre-specify the analysis plan
  **Right:** Register the protocol or document outcome definitions, subgroups, and model choices before data analysis
  **Why:** Post-hoc choices inflate false-positive rates

- **Wrong:** Reporting observational associations as causal without the target trial framework
  **Right:** Explicitly map every study to a hypothetical target trial to reveal hidden assumptions
  **Why:** Unmapped assumptions lead to structural biases that no statistical method can fix

## References

- Hernán MA, Robins JM. Causal Inference: What If. Chapman & Hall/CRC 2020, https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/
- Hernán MA, Alonso A, Logan R et al. Observational studies analyzed like randomized experiments: an application to postmenopausal hormone therapy and coronary heart disease. Epidemiology 2008, https://doi.org/10.1097/EDE.0b013e3181875e61
- Lund JL, Richardson DB, Stürmer T. The active comparator, new user study design in pharmacoepidemiology. Epidemiology 2015, https://doi.org/10.1097/EDE.0000000000000231
- Suissa S. Immortal time bias in pharmacoepidemiology. Am J Epidemiol 2008, https://doi.org/10.1093/aje/kwn138
- Robins JM, Hernán MA, Brumback B. Marginal structural models and causal inference in epidemiology. Epidemiology 2000, https://doi.org/10.1097/00001648-200009000-00011
- VanderWeele TJ, Ding P. Sensitivity analysis in observational research: introducing the E-value. Ann Intern Med 2017, https://doi.org/10.7326/M16-2607
- Austin PC. An introduction to propensity score methods for reducing the effects of confounding in observational studies. Multivariate Behav Res 2011, https://doi.org/10.1080/00273171.2011.568786
- Lipsitch M, Tchetgen Tchetgen E, Cohen T. Negative controls: a tool for detecting confounding and bias in observational studies. Epidemiology 2010, https://doi.org/10.1097/EDE.0b013e3181d61eeb
