---
name: arviz-diagnostics
description: >-
  Diagnose existing Bayesian inference output and evaluate fitted predictions
  with modern ArviZ DataTree summaries, divergences, rank R-hat, ESS and Monte
  Carlo precision. Use for posterior predictive checks, calibration, LOO/ELPD,
  Pareto k, stacking, grouped or temporal validation, survival diagnostics and
  Bayes-factor interpretation.
---

# ArviZ diagnostics

Assess computational health, predictive adequacy and scientific validity
separately, matching each check to the claim it can support.

## Workflow

1. **Identify the target and output.** Establish the model, observations,
   algorithm, independent chains, warmup and retained draws. A `posterior` group
   does not prove that draws came from MCMC; an observation-free model samples a
   prior target. Preserve chains and draw order, and save inference before costly
   postprocessing. Establish whether this is exploratory output or intended to
   support reportable inference: a rough fit may guide debugging without being
   accepted as an accurate posterior.
2. **Check exploration and precision.** Access `idata["posterior"]` and
   `idata["sample_stats"]`. Count HMC divergences by chain; inspect rank-normalized
   split R-hat, bulk/tail ESS and MCSE for the actual estimands, including relevant
   latent coordinates. R-hat below 1.01 and ESS above 400 are screening heuristics,
   not guarantees; choose precision requirements in scientific units.
3. **Inspect the plots.** Look for drifting/stuck chains, rank imbalance and
   divergence clusters. Use energy/BFMI, autocorrelation and ESS evolution where
   appropriate. Missing or nonfinite diagnostics are unresolved, not zero;
   HMC statistics may be inapplicable for other algorithms.
4. **Address causes before adding draws.** Investigate scaling, gradients,
   constraints, identifiability and parameterization. Non-centering often helps
   weakly informed hierarchies; centering can suit strong data. Higher
   `target_accept`, thinning or dropping bad chains cannot certify a repair.
5. **Criticize predictions separately.** Generate replicated observations and
   inspect task-relevant discrepancies, conditional calibration and uncertainty.
   Distinguish latent means from noisy new observations. In-sample PPCs are not
   held-out predictive validation.
6. **Evaluate the declared prediction target.** Compute pointwise log likelihood
   explicitly, check PSIS reliability before LOO/ELPD comparisons, and keep the
   same observations in the same order. Use grouped holdouts for new groups and
   past-only training for forecasts. Diagnose high Pareto k rather than hiding it.
7. **Interpret uncertainty honestly.** Report paired ELPD uncertainty and practical
   relevance, not only ranks. Stacking weights are neither model probabilities
   nor equivalence tests. Never exponentiate an ELPD difference as a Bayes factor.
   Adaptive model revisions and repeated CV comparisons can overfit selection.
   Explain consequential revisions and compare substantive inferences across
   viable alternatives, not only a winning score. For an action recommendation,
   propagate uncertainty through stated loss/utility and constraints, or hand off
   the inference to the decision maker without inventing their preferences.

## References

- [Diagnostics and predictive checks](references/diagnostics.md) — a complete
  diagnostic example, DataTree APIs, interval/MCSE semantics, plots, regression,
  counts, survival and nested chains.
- [Predictive evaluation and model comparison](references/model_evaluation.md) —
  LOO, high-k remedies, predictive metrics, stacking and validation design.

Examples use the modern ArviZ package family; version-specific cautions are
identified in the references. This skill does not require another skill.
