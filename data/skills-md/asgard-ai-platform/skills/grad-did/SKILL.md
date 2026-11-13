---
name: "grad-did"
description: "Apply Difference-in-Differences (DID) to estimate causal treatment effects by comparing changes in outcomes between treatment and control groups. Use this skill when the user evaluates policy interventions, natural experiments, or regulatory changes, needs to test parallel trends, or when they ask 'did this policy work', 'how do I identify causal effects without randomization', or 'what is the treatment effect'."
metadata:
  category: "WP-31 量化方法"
  tags: ["DID", "difference-in-differences", "causal-inference", "parallel-trends", "policy-evaluation", "treatment-effect"]
---

# 雙重差分法 (Difference-in-Differences)

## Overview

Difference-in-Differences (DID) estimates causal effects by comparing the change in outcomes over time between a treatment group (affected by an intervention) and a control group (unaffected). By differencing out both time-invariant group differences and common time trends, DID isolates the treatment effect under the parallel trends assumption.

## When to Use

- Evaluating the impact of a policy, regulation, or intervention
- A natural experiment assigns treatment at a group level (state, industry, firm)
- Panel or repeated cross-section data with pre- and post-treatment periods
- Randomized experiment is infeasible but a plausible control group exists

## When NOT to Use

- Parallel trends assumption is violated and cannot be remedied
- Treatment and control groups differ in ways that change over time
- Treatment is self-selected based on anticipated outcomes (anticipation effects)
- Only post-treatment data are available (no pre-treatment baseline)

## Assumptions

```
IRON LAW: DID is valid ONLY if the parallel trends assumption holds —
without it, the estimated treatment effect is biased by differential
pre-existing trends.
```

Key assumptions:
1. Parallel trends: absent treatment, treated and control groups would have followed the same trajectory
2. No spillover effects from treated to control units (SUTVA)
3. Treatment timing is sharp and exogenous
4. Composition of groups is stable over time (no differential attrition)

## Methodology

### Step 1 — Establish Treatment and Control Groups

Define who is treated and when. Verify groups are comparable on pre-treatment observables. Document the treatment event and its timing.

### Step 2 — Test Parallel Trends

Plot outcome trends for treatment vs control groups in pre-treatment periods. Run an event-study specification with leads and lags. Pre-treatment coefficients should be statistically insignificant.

### Step 3 — Estimate the DID Model

Y = β₀ + β₁×Treat + β₂×Post + β₃×(Treat×Post) + Controls + ε. The coefficient β₃ is the DID estimator. Cluster standard errors at the treatment assignment level. See `references/` for staggered adoption extensions.

### Step 4 — Robustness Checks

Run placebo tests (fake treatment dates, fake treatment groups). Test sensitivity to control group choice. For staggered DID, use Callaway-Sant'Anna or Sun-Abraham estimators.

## Output Format

```markdown
## DID Analysis: [Policy / Intervention]

### Research Design
| Element | Description |
|---------|-------------|
| Treatment group | [who] |
| Control group | [who] |
| Treatment date | [when] |
| Pre-treatment periods | [range] |

### Parallel Trends Test
| Pre-period lead | Coefficient | S.E. | p-value |
|-----------------|-------------|------|---------|
| t-3 | x.xx | x.xx | x.xx |
| t-2 | x.xx | x.xx | x.xx |
| t-1 | x.xx | x.xx | x.xx |

### DID Estimate
| Specification | β (Treat×Post) | S.E. | p-value | N |
|---------------|----------------|------|---------|---|
| Baseline | x.xx | x.xx | x.xx | xxx |
| With controls | x.xx | x.xx | x.xx | xxx |

### Robustness
- Placebo test result: [pass/fail]
- Alternative control group: [result]

### Limitations
- [Note any assumption violations]
```

## Gotchas

- Visual parallel trends are necessary but not sufficient — the assumption is about counterfactual trends
- Too few clusters for clustering standard errors inflates Type I error (use wild bootstrap if clusters < 50)
- Staggered adoption makes the standard two-way FE DID estimator biased (use recent robust estimators)
- Anticipation effects violate the sharp treatment timing assumption
- Differential pre-trends are often "fixed" by adding group-specific trends, but this is fragile
- DID estimates a local average treatment effect on the treated (ATT), not ATE

## References

- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
- Callaway, B., & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200-230.
- Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. *Journal of Econometrics*, 225(2), 254-277.
