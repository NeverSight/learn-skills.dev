---
name: research-methods
last_reviewed: 2026-09-06
group: Research
description: >-
  Design the study itself: question framing, method choice, sampling, controls and which
  statistics actually fit. Use when designing qualitative, quantitative, or experimental research
  methods.
---

# research-methods

## Core Philosophy
Research methodology is the epistemic foundation of science: it is the disciplined architecture that allows researchers to draw valid causal inferences while systematically neutralizing cognitive bias, confounding variables, and measurement noise. A study is only as strong as its methodological rigor. Choosing the wrong sampling strategy, failing to control for confounders, or applying parametric statistics to non-normal ordinal data invalidates every chart, table, and conclusion in the final manuscript.

---

## 4-Step Research Design Architecture

### Step 1: Question Framing & Methodological Paradigms
1. **Quantitative vs Qualitative vs Mixed Methods**:
   - **Quantitative**: Tests specific causal hypotheses, measures relationships between variables, uses numerical data and inferential statistics (e.g. *RCTs, quasi-experiments, cohort studies*).
   - **Qualitative**: Explores phenomena, unpacks mental models, understands social processes (e.g. *phenomenology, grounded theory, thematic interviews*).
   - **Mixed Methods (Convergent Parallel / Sequential)**: Combines statistical breadth with qualitative depth.
2. **Variable Operationalization**:
   - Define exact, observable metrics for abstract constructs:
     - *Construct*: "Developer Cognitive Load".
     - *Operationalization*: NASA-TLX score (0-100) + Pupil dilation metrics during debugging tasks.

### Step 2: Sampling Strategy & Statistical Power ($1 - \beta$)
1. **Sampling Methodologies**:
   - **Probability Sampling**: Simple random, stratified (preserves subgroup ratios), cluster sampling. Enables statistical generalizability.
   - **Non-Probability Sampling**: Convenience, purposive, snowball. High risk of selection bias; strictly bounded generalizability.
2. **Sample Size & Statistical Power Calculations**:
   - Calculate sample size $N$ in advance based on desired effect size (Cohen's $d$), significance level ($\alpha = 0.05$), and statistical power ($1 - \beta = 0.80$):
     - Underpowered studies ($N$ too small) produce high false-negative rates and inflated effect sizes when statistical significance is achieved by chance (Winner's Curse).

### Step 3: Experimental Controls & Threats to Validity
1. **Neutralizing Threats to Internal Validity**:
   - *Selection Bias*: Mitigated by strict computer-generated **random assignment**.
   - *History / Maturation*: Mitigated by parallel **Control Groups** experiencing identical time intervals without the intervention.
   - *Observer / Hawthorne Effect*: Mitigated by **Double-Blind** protocols where neither participant nor researcher knows group allocation.
2. **Threats to External Validity**:
   - Ensure the sample demographic and testing environment reflect the real-world operational domain (ecological validity).

### Step 4: Statistical Test Alignment (Parametric vs Non-Parametric)
1. **The Decision Matrix for Statistical Tests**:
   - Continuous DV + Normal Distribution + Independent Groups (2 groups) $\to$ **Two-Sample Independent $t$-Test**.
   - Continuous DV + Normal Distribution + Repeated Measures (Same group) $\to$ **Paired $t$-Test**.
   - Continuous DV + Normal Distribution + $\ge 3$ Groups $\to$ **One-Way ANOVA** (with Tukey HSD post-hoc).
   - Ordinal DV (Likert scales) or Skewed Distribution (2 groups) $\to$ **Mann-Whitney $U$ Test** (Wilcoxon Rank-Sum).
   - Categorical IV + Categorical DV $\to$ **Chi-Square ($\chi^2$) Test of Independence**.
   - Continuous DV + Multiple Continuous/Categorical IVs $\to$ **Multiple Linear Regression**.

---

## Deliverable Format: Methodological Study Blueprint (RCT Protocol)

```markdown
# Study Protocol: Evaluating Spaced Retrieval in Software Engineering Onboarding

### 1. Research Hypothesis
Engineers onboarded using a spaced-retrieval CLI interactive tool will demonstrate significantly higher code architecture comprehension ($p < 0.01$, Cohen's $d \ge 0.5$) at Day 30 compared to engineers onboarded using traditional monolithic wiki documentation.

### 2. Experimental Design
- **Type**: Randomized Controlled Trial (Between-Subjects).
- **Independent Variable (IV)**: Onboarding Modality:
  - *Treatment Group*: Spaced retrieval CLI tool (10-min active recall challenges on Days 1, 3, 7, 14, 28).
  - *Control Group*: Standard company Confluence onboarding wiki (unconstrained self-study).
- **Dependent Variable (DV)**: Architecture Comprehension Score (0-100 on a validated 20-item diagnostic scenario exam administered on Day 30).

### 3. Sampling & Power Analysis
- Power calculation ($\alpha = 0.05, 1 - \beta = 0.80$, expected Cohen's $d = 0.60$): Requires minimum $N = 45$ participants per group ($N_{\text{total}} = 90$).
- Recruitment: 96 newly hired engineers across 4 enterprise business units, stratified by years of prior software experience, then randomly assigned 1:1.

### 4. Statistical Analysis Plan
1. Test normality of Day 30 score distribution via Shapiro-Wilk test.
2. If normal: Independent two-sample $t$-test; report mean difference and 95% Confidence Intervals.
3. If non-normal: Mann-Whitney $U$ non-parametric test.
4. Multiple regression controlling for years of experience and prior programming language familiarity.
```

---

## Worked Example: Rescuing a Flawed Product A/B Test Methodology

- **Problem**: A growth team ran an A/B test claiming a new checkout button increased conversions by 14% ($p = 0.04$). Two months later, total company revenue had declined.
- **Methodological Audit**:
  1. *Peeking Bias*: The growth team had checked the dashboard every morning and stopped the test the moment $p < 0.05$ appeared (Day 4), inflating false-positive rates to over 30%.
  2. *Novelty Effect*: Returning power users clicked the bright new button out of curiosity, not increased purchase intent.
- **Methodological Remedy**: Implemented fixed-horizon testing: mandatory 14-day run time to capture full weekly seasonal cycles, with sample sizes locked in advance via power analysis.
- **Result**: The 14% conversion lift vanished in the controlled re-test, preventing a disastrous permanent UI overhaul.

---

## Verification Checklist

- [ ] Research paradigm matches the underlying epistemic question.
- [ ] Variables clearly operationalized with validated measurement instruments.
- [ ] Sample size determined prior to data collection via formal statistical power calculations.
- [ ] Threats to internal validity (selection, maturation, confounders) controlled.
- [ ] Statistical tests aligned with variable data types (parametric vs non-parametric).

---

## Anti-Patterns

- **P-Hacking / Data Dredging**: Running 40 different statistical combinations until one randomly shows $p < 0.05$ and inventing a hypothesis after the fact (HARKing).
- **Premature Test Peeking**: Halting an A/B test or experiment early the moment the significance indicator flashes green.
- **Convenience Bias Generalization**: Running an experiment exclusively on 30 undergraduate psychology students and claiming the findings apply to all human beings.
