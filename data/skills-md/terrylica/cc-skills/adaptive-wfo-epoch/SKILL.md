---
name: adaptive-wfo-epoch
description: Adaptive epoch selection for Walk-Forward Optimization. TRIGGERS - WFO epoch, epoch selection, WFE optimization, overfitting epochs.
allowed-tools: Read, Grep, Glob, Bash
---

# Adaptive Walk-Forward Epoch Selection (AWFES)

Machine-readable reference for adaptive epoch selection within Walk-Forward Optimization (WFO). Optimizes training epochs per-fold using Walk-Forward Efficiency (WFE) as the objective.

## When to Use This Skill

Use this skill when:

- Selecting optimal training epochs for ML models in WFO
- Avoiding overfitting via Walk-Forward Efficiency metrics
- Implementing per-fold adaptive epoch selection
- Computing efficient frontiers for epoch-performance trade-offs
- Carrying epoch priors across WFO folds

## Quick Start

```python
from adaptive_wfo_epoch import AWFESConfig, compute_efficient_frontier

# Generate epoch candidates from search bounds and granularity
config = AWFESConfig.from_search_space(
    min_epoch=100,
    max_epoch=2000,
    granularity=5,  # Number of frontier points
)
# config.epoch_configs → [100, 211, 447, 945, 2000] (log-spaced)

# Per-fold epoch sweep
for fold in wfo_folds:
    epoch_metrics = []
    for epoch in config.epoch_configs:
        is_sharpe, oos_sharpe = train_and_evaluate(fold, epochs=epoch)
        wfe = config.compute_wfe(is_sharpe, oos_sharpe, n_samples=len(fold.train))
        epoch_metrics.append({"epoch": epoch, "wfe": wfe, "is_sharpe": is_sharpe})

    # Select from efficient frontier
    selected_epoch = compute_efficient_frontier(epoch_metrics)

    # Carry forward to next fold as prior
    prior_epoch = selected_epoch
```

## Methodology Overview

### What This Is

Per-fold adaptive epoch selection where:

1. Train models across a range of epochs (e.g., 400, 800, 1000, 2000)
2. Compute WFE = OOS_Sharpe / IS_Sharpe for each epoch count
3. Find the "efficient frontier" - epochs maximizing WFE vs training cost
4. Select optimal epoch from frontier for OOS evaluation
5. Carry forward as prior for next fold

### What This Is NOT

- **NOT early stopping**: Early stopping monitors validation loss continuously; this evaluates discrete candidates post-hoc
- **NOT Bayesian optimization**: No surrogate model; direct evaluation of all candidates
- **NOT nested cross-validation**: Uses temporal WFO, not shuffled splits

## Academic Foundations

| Concept                     | Citation                       | Key Insight                                       |
| --------------------------- | ------------------------------ | ------------------------------------------------- |
| Walk-Forward Efficiency     | Pardo (1992, 2008)             | WFE = OOS_Return / IS_Return as robustness metric |
| Deflated Sharpe Ratio       | Bailey & López de Prado (2014) | Adjusts for multiple testing                      |
| Pareto-Optimal HP Selection | Bischl et al. (2023)           | Multi-objective hyperparameter optimization       |
| Warm-Starting               | Nomura & Ono (2021)            | Transfer knowledge between optimization runs      |

See [references/academic-foundations.md](./references/academic-foundations.md) for full literature review.

## Core Formula: Walk-Forward Efficiency

```python
def compute_wfe(
    is_sharpe: float,
    oos_sharpe: float,
    n_samples: int | None = None,
) -> float | None:
    """Walk-Forward Efficiency - measures performance transfer.

    WFE = OOS_Sharpe / IS_Sharpe

    Interpretation (guidelines, not hard thresholds):
    - WFE ≥ 0.70: Excellent transfer (low overfitting)
    - WFE 0.50-0.70: Good transfer
    - WFE 0.30-0.50: Moderate transfer (investigate)
    - WFE < 0.30: Severe overfitting (likely reject)

    The IS_Sharpe minimum is derived from signal-to-noise ratio,
    not a fixed magic number. See compute_is_sharpe_threshold().

    Reference: Pardo (2008) "The Evaluation and Optimization of Trading Strategies"
    """
    # Data-driven threshold: IS_Sharpe must exceed 2σ noise floor
    min_is_sharpe = compute_is_sharpe_threshold(n_samples) if n_samples else 0.1

    if abs(is_sharpe) < min_is_sharpe:
        return None
    return oos_sharpe / is_sharpe
```

## Principled Configuration Framework

All parameters are derived from first principles or data characteristics. `AWFESConfig` provides unified configuration with log-spaced epoch generation, Bayesian variance derivation from search space, and market-specific annualization factors.

See [references/configuration-framework.md](./references/configuration-framework.md) for the full `AWFESConfig` class and `compute_is_sharpe_threshold()` implementation.

## Guardrails (Principled Guidelines)

- **G1: WFE Thresholds** - 0.30 (reject), 0.50 (warning), 0.70 (target) based on practitioner consensus
- **G2: IS_Sharpe Minimum** - Data-driven threshold: `2/sqrt(n)` adapts to sample size
- **G3: Stability Penalty** - Adaptive threshold derived from WFE variance prevents epoch churn
- **G4: DSR Adjustment** - Deflated Sharpe corrects for epoch selection multiplicity via Gumbel distribution

See [references/guardrails.md](./references/guardrails.md) for full implementations of all guardrails.

## WFE Aggregation Methods

Under the null hypothesis, WFE follows a **Cauchy distribution** (no defined mean). Always prefer median or pooled methods:

- **Pooled WFE**: Precision-weighted by sample size (best for variable fold sizes)
- **Median WFE**: Robust to outliers (best for suspected regime changes)
- **Weighted Mean**: Inverse-variance weighting (best for homogeneous folds)

See [references/wfe-aggregation.md](./references/wfe-aggregation.md) for implementations and selection guide.

## Efficient Frontier Algorithm

Pareto-optimal epoch selection: an epoch is on the frontier if no other epoch dominates it (better WFE AND lower training time). The `AdaptiveEpochSelector` class maintains state across folds with adaptive stability penalties.

See [references/efficient-frontier.md](./references/efficient-frontier.md) for the full algorithm and carry-forward mechanism.

## Anti-Patterns

| Anti-Pattern                      | Symptom                             | Fix                               | Severity |
| --------------------------------- | ----------------------------------- | --------------------------------- | -------- |
| **Expanding window (range bars)** | Train size grows per fold           | Use fixed sliding window          | CRITICAL |
| **Peak picking**                  | Best epoch always at sweep boundary | Expand range, check for plateau   | HIGH     |
| **Insufficient folds**            | effective_n < 30                    | Increase folds or data span       | HIGH     |
| **Ignoring temporal autocorr**    | Folds correlated                    | Use purged CV, gap between folds  | HIGH     |
| **Overfitting to IS**             | IS >> OOS Sharpe                    | Reduce epochs, add regularization | HIGH     |
| **sqrt(252) for crypto**          | Inflated Sharpe                     | Use sqrt(365) or sqrt(7) weekly   | MEDIUM   |
| **Single epoch selection**        | No uncertainty quantification       | Report confidence interval        | MEDIUM   |
| **Meta-overfitting**              | Epoch selection itself overfits     | Limit to 3-4 candidates max       | HIGH     |

**CRITICAL**: Never use expanding window for range bar ML training. See [references/anti-patterns.md](./references/anti-patterns.md) for the full analysis (Section 7).

## Decision Tree

See [references/epoch-selection-decision-tree.md](./references/epoch-selection-decision-tree.md) for the full practitioner decision tree.

```
Start
  │
  ├─ IS_Sharpe > compute_is_sharpe_threshold(n)? ──NO──> Mark WFE invalid, use fallback
  │         │                                            (threshold = 2/√n, adapts to sample size)
  │        YES
  │         │
  ├─ Compute WFE for each epoch
  │         │
  ├─ Any WFE > 0.30? ──NO──> REJECT all epochs (severe overfit)
  │         │                (guideline, not hard threshold)
  │        YES
  │         │
  ├─ Compute efficient frontier
  │         │
  ├─ Apply AdaptiveStabilityPenalty
  │         │ (threshold derived from WFE variance)
  └─> Return selected epoch
```

## Integration with rangebar-eval-metrics

This skill extends [rangebar-eval-metrics](../rangebar-eval-metrics/SKILL.md):

| Metric Source         | Used For                                 | Reference                                                                                |
| --------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| `sharpe_tw`           | WFE numerator (OOS) and denominator (IS) | [range-bar-metrics.md](./references/range-bar-metrics.md)                                |
| `n_bars`              | Sample size for aggregation weights      | [metrics-schema.md](../rangebar-eval-metrics/references/metrics-schema.md)               |
| `psr`, `dsr`          | Final acceptance criteria                | [sharpe-formulas.md](../rangebar-eval-metrics/references/sharpe-formulas.md)             |
| `prediction_autocorr` | Validate model isn't collapsed           | [ml-prediction-quality.md](../rangebar-eval-metrics/references/ml-prediction-quality.md) |
| `is_collapsed`        | Model health check                       | [ml-prediction-quality.md](../rangebar-eval-metrics/references/ml-prediction-quality.md) |
| Extended risk metrics | Deep risk analysis (optional)            | [risk-metrics.md](../rangebar-eval-metrics/references/risk-metrics.md)                   |

### Recommended Workflow

1. **Compute base metrics** using `rangebar-eval-metrics:compute_metrics.py`
2. **Feed to AWFES** for epoch selection with `sharpe_tw` as primary signal
3. **Validate** with `psr > 0.85` and `dsr > 0.50` before deployment
4. **Monitor** `is_collapsed` and `prediction_autocorr` for model health

---

## OOS Application Phase

AWFES uses **Nested WFO** with three data splits per fold (Train 60% / Val 20% / Test 20%) with 6% embargo gaps at each boundary. The per-fold workflow: epoch sweep on train, WFE computation on validation, Bayesian update, final model training on train+val, evaluation on test.

See [references/oos-workflow.md](./references/oos-workflow.md) for the complete workflow with diagrams, `BayesianEpochSelector` class, and `apply_awfes_to_test()` implementation. Also see [references/oos-application.md](./references/oos-application.md) for the extended reference.

## Epoch Smoothing Methods

Bayesian updating (recommended) provides principled, uncertainty-aware smoothing. Alternatives include EMA and SMA. Initialization via `AWFESConfig.from_search_space()` derives variances from the epoch range automatically.

See [references/epoch-smoothing-methods.md](./references/epoch-smoothing-methods.md) for all methods, formulas, and initialization strategies. See [references/epoch-smoothing.md](./references/epoch-smoothing.md) for extended mathematical analysis.

## OOS Metrics Specification

Three-tier metric hierarchy for test evaluation:

- **Tier 1 (Primary)**: `sharpe_tw`, `hit_rate`, `cumulative_pnl`, `positive_sharpe_folds`, `wfe_test`
- **Tier 2 (Risk)**: `max_drawdown`, `calmar_ratio`, `profit_factor`, `cvar_10pct`
- **Tier 3 (Statistical)**: `psr`, `dsr`, `binomial_pvalue`, `hac_ttest_pvalue`

See [references/oos-metrics-implementation.md](./references/oos-metrics-implementation.md) for full metric tables, `compute_oos_metrics()`, and fold aggregation code. See [references/oos-metrics.md](./references/oos-metrics.md) for threshold justifications.

## Look-Ahead Bias Prevention

**CRITICAL (v3 fix)**: TEST must use `prior_bayesian_epoch` (from prior folds only), NOT `val_optimal_epoch`. The Bayesian update happens AFTER test evaluation, ensuring information flows only from past to present.

See [references/look-ahead-bias-v3.md](./references/look-ahead-bias-v3.md) for the v3 fix details, embargo requirements, validation checklist, and anti-patterns. See [references/look-ahead-bias.md](./references/look-ahead-bias.md) for detailed examples.

---

## References

| Topic                    | Reference File                                                                    |
| ------------------------ | --------------------------------------------------------------------------------- |
| Academic Literature      | [academic-foundations.md](./references/academic-foundations.md)                   |
| Mathematical Formulation | [mathematical-formulation.md](./references/mathematical-formulation.md)           |
| Configuration Framework  | [configuration-framework.md](./references/configuration-framework.md)             |
| Guardrails               | [guardrails.md](./references/guardrails.md)                                       |
| WFE Aggregation          | [wfe-aggregation.md](./references/wfe-aggregation.md)                             |
| Efficient Frontier       | [efficient-frontier.md](./references/efficient-frontier.md)                       |
| Decision Tree            | [epoch-selection-decision-tree.md](./references/epoch-selection-decision-tree.md) |
| Anti-Patterns            | [anti-patterns.md](./references/anti-patterns.md)                                 |
| OOS Workflow             | [oos-workflow.md](./references/oos-workflow.md)                                   |
| OOS Application          | [oos-application.md](./references/oos-application.md)                             |
| Epoch Smoothing Methods  | [epoch-smoothing-methods.md](./references/epoch-smoothing-methods.md)             |
| Epoch Smoothing Analysis | [epoch-smoothing.md](./references/epoch-smoothing.md)                             |
| OOS Metrics Impl         | [oos-metrics-implementation.md](./references/oos-metrics-implementation.md)       |
| OOS Metrics Thresholds   | [oos-metrics.md](./references/oos-metrics.md)                                     |
| Look-Ahead Bias (v3)     | [look-ahead-bias-v3.md](./references/look-ahead-bias-v3.md)                       |
| Look-Ahead Bias Examples | [look-ahead-bias.md](./references/look-ahead-bias.md)                             |
| **Feature Sets**         | [feature-sets.md](./references/feature-sets.md)                                   |
| **xLSTM Implementation** | [xlstm-implementation.md](./references/xlstm-implementation.md)                   |
| **Range Bar Metrics**    | [range-bar-metrics.md](./references/range-bar-metrics.md)                         |
| Troubleshooting          | [troubleshooting.md](./references/troubleshooting.md)                             |

## Full Citations

- Bailey, D. H., & López de Prado, M. (2014). The deflated Sharpe ratio: Correcting for selection bias, backtest overfitting and non-normality. _The Journal of Portfolio Management_, 40(5), 94-107.
- Bischl, B., et al. (2023). Multi-Objective Hyperparameter Optimization in Machine Learning. _ACM Transactions on Evolutionary Learning and Optimization_.
- López de Prado, M. (2018). _Advances in Financial Machine Learning_. Wiley. Chapter 7.
- Nomura, M., & Ono, I. (2021). Warm Starting CMA-ES for Hyperparameter Optimization. _AAAI Conference on Artificial Intelligence_.
- Pardo, R. E. (2008). _The Evaluation and Optimization of Trading Strategies, 2nd Edition_. John Wiley & Sons.
