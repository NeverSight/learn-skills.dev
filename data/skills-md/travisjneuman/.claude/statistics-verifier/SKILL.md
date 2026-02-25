---
name: statistics-verifier
description: Verify statistics from raw data with methodology checking, significance testing, claim validation, and bias detection. Use when fact-checking statistical claims, validating research findings, or auditing data analysis.
---

# Statistics Verifier

Structured frameworks for verifying statistical claims, validating research methodology, and detecting analytical errors and biases.

## Statistical Claim Verification Checklist

### Rapid Claim Assessment

```
CLAIM VERIFICATION PROTOCOL:

1. SOURCE CHECK
   - Who made the claim?
   - What is their expertise and incentive?
   - Where was it published (peer-reviewed, preprint, press release)?
   - Is the original data or study accessible?

2. METHODOLOGY CHECK
   - What type of study (RCT, observational, survey, meta-analysis)?
   - What was the sample size and population?
   - What was the measurement method?
   - Is the statistical test appropriate for the data type?

3. NUMBER SENSE CHECK
   - Does the claim pass a basic plausibility test?
   - Are units and denominators clearly stated?
   - Absolute vs relative numbers — which is being used?
   - Is the base rate provided for context?

4. REPLICATION CHECK
   - Have other studies found similar results?
   - Are the findings consistent across populations?
   - Has anyone attempted and failed to replicate?

5. CONCLUSION CHECK
   - Does the conclusion follow from the data?
   - Are alternative explanations addressed?
   - Is the scope of the claim proportional to the evidence?
```

### Claim Red Flags

| Red Flag | What It Means | Action |
| --- | --- | --- |
| No sample size given | Cannot assess reliability | Request or estimate N |
| Only relative risk reported | May hide small absolute effect | Calculate absolute difference |
| "Up to X%" framing | Cherry-picked best case | Ask for median or mean |
| No confidence interval | Precision unknown | Treat with skepticism |
| Correlation stated as causation | Confounders likely ignored | Check study design |
| Self-selected sample | Selection bias likely | Note limitation |
| Composite endpoint | May mask weak individual results | Decompose the endpoint |
| Subgroup analysis highlighted | Likely post-hoc fishing | Require pre-registration |

## Common Statistical Errors

### Error Detection Framework

```
CATEGORY 1: DESIGN ERRORS
- Sampling bias (convenience, voluntary response, survivorship)
- Confounding variables not controlled
- Insufficient sample size (underpowered study)
- No control group or inappropriate comparator
- Measurement instrument not validated

CATEGORY 2: ANALYSIS ERRORS
- Multiple comparisons without correction (p-hacking)
- Treating ordinal data as interval
- Assuming normality without checking
- Ignoring missing data patterns (MCAR vs MNAR)
- Using parametric tests on non-parametric data

CATEGORY 3: INTERPRETATION ERRORS
- Confusing statistical significance with practical significance
- Interpreting non-significant result as "no effect"
- Ecological fallacy (group-level applied to individuals)
- Simpson's paradox not checked
- Ignoring effect size and confidence intervals

CATEGORY 4: REPORTING ERRORS
- Selective reporting of favorable results
- Omitting negative or null findings
- Misleading axis scales in visualizations
- Presenting percentages without base numbers
- Switching between absolute and relative metrics
```

### Error Severity Assessment

| Error Type | Severity | Impact on Conclusion |
| --- | --- | --- |
| P-hacking / HARKing | Critical | Invalidates findings |
| Selection bias | Critical | Fundamentally flawed sample |
| Confounding not addressed | High | Alternative explanations remain |
| Wrong statistical test | High | Results may be artifactual |
| Multiple comparisons uncorrected | High | Inflated false positive rate |
| Small sample without power analysis | Medium | May miss real effects |
| Missing confidence intervals | Medium | Cannot judge precision |
| Misleading visualization | Medium | Misrepresents magnitude |
| Minor rounding errors | Low | Minimal impact |

## Significance Testing Framework

### Test Selection Guide

```
CHOOSING THE RIGHT TEST:

DATA TYPE → COMPARISON → TEST

Continuous + 2 groups + independent → Independent t-test (or Mann-Whitney)
Continuous + 2 groups + paired     → Paired t-test (or Wilcoxon signed-rank)
Continuous + 3+ groups + independent → One-way ANOVA (or Kruskal-Wallis)
Continuous + 2+ factors            → Two-way ANOVA (or Friedman)
Continuous + continuous             → Pearson correlation (or Spearman)

Categorical + 2 groups             → Chi-square test (or Fisher's exact)
Categorical + ordered              → Cochran-Armitage trend test
Binary outcome + predictors        → Logistic regression

Time-to-event + groups             → Log-rank test / Cox regression
Count data                          → Poisson regression
Proportion + large sample           → Z-test for proportions
```

### P-Value Interpretation Guide

```
P-VALUE CONTEXT:

p-value = P(data this extreme | null hypothesis is true)

COMMON MISINTERPRETATIONS:
  p = 0.03 does NOT mean:
  - "There is a 3% chance the result is due to chance"
  - "There is a 97% probability the hypothesis is true"
  - "The effect is large or important"
  - "The study will replicate"

  p = 0.03 DOES mean:
  - If the null hypothesis were true, data this extreme
    would occur about 3% of the time by chance alone.

THRESHOLDS (conventional, not absolute):
  p < 0.001  — strong evidence against null
  p < 0.01   — moderate evidence against null
  p < 0.05   — conventional threshold (context-dependent)
  p > 0.05   — insufficient evidence to reject null
                (NOT evidence of no effect)

ALWAYS COMPLEMENT WITH:
  - Effect size (Cohen's d, odds ratio, etc.)
  - Confidence interval (range of plausible values)
  - Practical significance (is the effect meaningful?)
  - Study power (could it have detected a real effect?)
```

### Multiple Comparisons Correction

| Method | When to Use | Conservativeness |
| --- | --- | --- |
| **Bonferroni** | Few comparisons, need strong control | Very conservative |
| **Holm-Bonferroni** | Moderate comparisons, step-down | Less conservative |
| **Benjamini-Hochberg** | Many comparisons (FDR control) | Liberal |
| **Tukey's HSD** | All pairwise comparisons after ANOVA | Moderate |
| **Dunnett's** | Multiple treatments vs one control | Moderate |

## Sample Size Validation

### Quick Reference Table

```
MINIMUM SAMPLE SIZE GUIDELINES:

Survey (population estimate):
  ±3% margin, 95% CI → n ≈ 1,067
  ±5% margin, 95% CI → n ≈ 385
  ±10% margin, 95% CI → n ≈ 97

A/B Test (detecting 5% relative lift):
  Baseline 10% conversion → n ≈ 3,200 per group
  Baseline 5% conversion  → n ≈ 6,400 per group
  Baseline 2% conversion  → n ≈ 16,000 per group

Clinical trial (medium effect d=0.5):
  Two-group comparison, 80% power → n ≈ 64 per group
  Two-group comparison, 90% power → n ≈ 86 per group

Correlation (detecting r=0.3):
  80% power, alpha=0.05 → n ≈ 85
  90% power, alpha=0.05 → n ≈ 113
```

### Power Analysis Checklist

| Parameter | Must Specify | Source |
| --- | --- | --- |
| Alpha (Type I error rate) | Yes | Convention (usually 0.05) |
| Power (1 - Type II error) | Yes | Usually 0.80 or 0.90 |
| Effect size | Yes | Prior research or MCID |
| Variance / SD | Yes | Pilot data or literature |
| Sample size | Calculated | Output of power analysis |
| Attrition rate | Recommended | Inflate N by expected dropout |

## Correlation vs Causation Checklist

### Bradford Hill Criteria for Causation

```
DOES CORRELATION IMPLY CAUSATION? CHECK:

1. STRENGTH           Is the association large?
                      Larger effects harder to explain away.

2. CONSISTENCY        Replicated across settings, populations?
                      Multiple studies, same finding.

3. SPECIFICITY        Is X linked specifically to Y (not everything)?
                      Less useful for multifactorial diseases.

4. TEMPORALITY        Does X precede Y in time?
                      REQUIRED — cause must come before effect.

5. BIOLOGICAL GRADIENT  Does more X produce more Y (dose-response)?
                        Strong support for causation.

6. PLAUSIBILITY       Is there a credible mechanism?
                      Based on current knowledge.

7. COHERENCE          Consistent with known biology/theory?
                      No conflict with established facts.

8. EXPERIMENT         Does removing X reduce Y?
                      Strongest evidence (RCT).

9. ANALOGY            Similar exposures cause similar effects?
                      Weakest criterion, supporting only.

VERDICT:
  Criteria 1-3 met + Temporality → Suggestive of causation
  Criteria 1-6 met + Experiment  → Strong evidence of causation
  Only correlation observed      → Association only, cannot infer cause
```

### Common Third-Variable Confounders

| Observed Association | Likely Confounder |
| --- | --- |
| Ice cream sales and drowning | Warm weather (season) |
| Shoe size and reading ability | Age |
| Hospital visits and death rate | Illness severity |
| Organic food and health | Socioeconomic status |
| Screen time and depression | Social isolation, sleep |

## Survey Methodology Review

### Survey Quality Assessment

```
SURVEY METHODOLOGY CHECKLIST:

SAMPLING:
- [ ] Probability sampling method described?
- [ ] Sampling frame defined and appropriate?
- [ ] Response rate reported (acceptable: >60% mail, >80% in-person)?
- [ ] Non-response bias assessed?

QUESTIONNAIRE:
- [ ] Questions validated or adapted from validated instruments?
- [ ] Leading or double-barreled questions absent?
- [ ] Response options balanced and exhaustive?
- [ ] Pilot tested with target population?

ADMINISTRATION:
- [ ] Mode (online, phone, in-person) appropriate?
- [ ] Anonymity/confidentiality assured?
- [ ] Informed consent obtained?
- [ ] Social desirability bias mitigated?

ANALYSIS:
- [ ] Weighting applied for non-response or oversampling?
- [ ] Margin of error and confidence level reported?
- [ ] Subgroup analyses pre-specified (not exploratory)?
```

## Data Visualization Integrity Checks

### Chart Audit Checklist

| Check | What to Look For | Fail Condition |
| --- | --- | --- |
| Y-axis starts at zero (bar charts) | Truncated axis exaggerates differences | Axis starts above zero without clear label |
| Consistent scale | Both axes have proportional increments | Non-linear scale without explanation |
| Area proportional to data | Bubble/icon size matches values | Area misrepresents magnitude |
| Time axis evenly spaced | Equal intervals between data points | Uneven spacing compresses/expands trends |
| Appropriate chart type | Data type matches visualization | Pie chart with 20+ categories |
| Context provided | Benchmarks, comparisons, baselines | Single data point with no reference |
| Source cited | Data origin traceable | No source attribution |
| Dual axes used responsibly | Two Y-axes can create false correlations | Arbitrary scaling implies relationship |

### Misleading Visualization Patterns

```
WATCH FOR THESE TRICKS:

1. TRUNCATED AXIS
   Small differences look dramatic when baseline removed.
   FIX: Always check if y-axis starts at zero for bar charts.

2. CHERRY-PICKED TIME WINDOW
   Start/end dates chosen to show desired trend.
   FIX: Ask for longer time series with consistent intervals.

3. 3D EFFECTS
   Perspective distortion makes sizes unequal.
   FIX: Use flat 2D charts for accurate comparison.

4. DUAL AXIS MANIPULATION
   Two y-axes scaled to create apparent correlation.
   FIX: Normalize data or use separate panels.

5. CUMULATIVE VS DAILY
   Cumulative charts always go up — hides declining rates.
   FIX: Show rate of change alongside cumulative.
```

## Bias Detection Framework

### Cognitive Biases in Data Analysis

```
BIAS DETECTION CHECKLIST:

CONFIRMATION BIAS
- Are they only presenting data that supports their hypothesis?
- Were negative results reported?
- Was the analysis plan pre-registered?

ANCHORING BIAS
- Is the first number presented influencing interpretation of later data?
- Are comparisons made to appropriate benchmarks?

SURVIVORSHIP BIAS
- Are only successful cases included (ignoring failures)?
- Is the denominator complete (not just survivors)?

AVAILABILITY BIAS
- Are dramatic or recent events overweighted?
- Is systematic data used rather than anecdotal evidence?

PUBLICATION BIAS
- Is there a funnel plot asymmetry (meta-analyses)?
- Are null results published or only significant ones?

TEXAS SHARPSHOOTER FALLACY
- Were clusters or patterns found after looking at data?
- Was the hypothesis formed before or after seeing results?
```

### Bias Severity Matrix

| Bias | Detection Method | Mitigation |
| --- | --- | --- |
| Selection bias | Compare sample to population demographics | Probability sampling, weighting |
| Measurement bias | Check instrument validity and calibration | Validated instruments, blinding |
| Reporting bias | Look for asymmetric funnel plots | Pre-registration, open data |
| Recall bias | Compare to objective records | Prospective data collection |
| Observer bias | Check if assessors were blinded | Double-blind design |
| Attrition bias | Compare completers vs dropouts | Intention-to-treat analysis |

## Reproducibility Checklist

### Study Reproducibility Assessment

```
REPRODUCIBILITY REQUIREMENTS:

DATA AVAILABILITY:
- [ ] Raw data accessible (repository, supplement, on request)?
- [ ] Data dictionary / codebook provided?
- [ ] Data collection protocol documented?

CODE / ANALYSIS:
- [ ] Analysis code shared (GitHub, OSF, supplement)?
- [ ] Software versions and packages specified?
- [ ] Random seeds set for reproducible computation?
- [ ] Pipeline documented end-to-end?

METHODOLOGY:
- [ ] Study pre-registered (OSF, ClinicalTrials.gov)?
- [ ] Deviations from protocol documented?
- [ ] All outcome measures reported (not just significant ones)?
- [ ] Sensitivity analyses included?

REPORTING:
- [ ] Follows reporting guidelines (CONSORT, STROBE, PRISMA)?
- [ ] Effect sizes and confidence intervals reported?
- [ ] Power analysis or sample size justification provided?
- [ ] Limitations section thorough and honest?
```

### Reporting Standards by Study Type

| Study Type | Guideline | Key Elements |
| --- | --- | --- |
| Randomized trial | CONSORT | Flow diagram, ITT analysis, blinding |
| Observational study | STROBE | Selection criteria, confounders, missing data |
| Systematic review | PRISMA | Search strategy, inclusion criteria, risk of bias |
| Diagnostic accuracy | STARD | Index test, reference standard, flow diagram |
| Qualitative research | COREQ | Research team, study design, data analysis |
| Prediction model | TRIPOD | Model development, validation, performance |

## Quick Verification Workflow

```
FAST VERIFICATION (5 minutes):

1. Read the claim carefully — what exactly is being stated?
2. Check: source, sample size, study type
3. Ask: absolute or relative? What is the base rate?
4. Check: confidence interval or margin of error given?
5. Search: has this been replicated independently?

VERDICT CATEGORIES:
  VERIFIED    — multiple strong sources, robust methodology
  PLAUSIBLE   — reasonable evidence, some limitations
  UNCERTAIN   — mixed evidence, methodology concerns
  MISLEADING  — technically true but presented deceptively
  FALSE       — contradicted by strong evidence
  UNVERIFIABLE — cannot assess with available information
```

## See Also

- [Data Science](../data-science/SKILL.md)
- [Research Presenter](../research-presenter/SKILL.md)
- [Product Analytics](../product-analytics/SKILL.md)
