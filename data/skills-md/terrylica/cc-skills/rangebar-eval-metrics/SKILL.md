---
name: rangebar-eval-metrics
description: Range bar evaluation metrics for quant trading. TRIGGERS - range bar metrics, Sharpe ratio, WFO metrics, PSR DSR MinTRL.
allowed-tools: Read, Grep, Glob, Bash
---

# Range Bar Evaluation Metrics

Machine-readable reference + computation scripts for state-of-the-art metrics evaluating range bar (price-based sampling) data.

## When to Use This Skill

Use this skill when:

- Evaluating ML model performance on range bar data
- Computing Sharpe ratios with non-IID bar sequences
- Running Walk-Forward Optimization metric analysis
- Calculating PSR, DSR, or MinTRL statistical tests
- Generating evaluation reports from fold results

## Quick Start

```bash
# Compute metrics from predictions + actuals
python scripts/compute_metrics.py --predictions preds.npy --actuals actuals.npy --timestamps ts.npy

# Generate full evaluation report
python scripts/generate_report.py --results folds.jsonl --output report.md
```

## Metric Tiers

| Tier                   | Purpose            | Metrics                                                                  | Compute              |
| ---------------------- | ------------------ | ------------------------------------------------------------------------ | -------------------- |
| **Primary** (5)        | Research decisions | weekly_sharpe, hit_rate, cumulative_pnl, n_bars, positive_sharpe_rate    | Per-fold + aggregate |
| **Secondary/Risk** (5) | Additional context | max_drawdown, bar_sharpe, return_per_bar, profit_factor, cv_fold_returns | Per-fold             |
| **ML Quality** (3)     | Prediction health  | ic, prediction_autocorr, is_collapsed                                    | Per-fold             |
| **Diagnostic** (5)     | Final validation   | psr, dsr, autocorr_lag1, effective_n, binomial_pvalue                    | Aggregate only       |
| **Extended Risk** (5)  | Deep risk analysis | var_95, cvar_95, omega_ratio, sortino_ratio, ulcer_index                 | Per-fold (optional)  |

## Why Range Bars Need Special Treatment

Range bars violate standard IID assumptions:

1. **Variable duration**: Bars form based on price movement, not time
2. **Autocorrelation**: High-volatility periods cluster bars → temporal correlation
3. **Non-constant information**: More bars during volatility = more information per day

**Canonical solution**: Daily aggregation via `_group_by_day()` before Sharpe calculation.

## References

### Core Reference Files

| Topic                                | Reference File                                                    |
| ------------------------------------ | ----------------------------------------------------------------- |
| Sharpe Ratio Calculations            | [sharpe-formulas.md](./references/sharpe-formulas.md)             |
| Risk Metrics (VaR, Omega, Ulcer)     | [risk-metrics.md](./references/risk-metrics.md)                   |
| ML Prediction Quality (IC, Autocorr) | [ml-prediction-quality.md](./references/ml-prediction-quality.md) |
| Crypto Market Considerations         | [crypto-markets.md](./references/crypto-markets.md)               |
| Temporal Aggregation Rules           | [temporal-aggregation.md](./references/temporal-aggregation.md)   |
| JSON Schema for Metrics              | [metrics-schema.md](./references/metrics-schema.md)               |
| Anti-Patterns (Transaction Costs)    | [anti-patterns.md](./references/anti-patterns.md)                 |
| SOTA 2025-2026 (SHAP, BOCPD, etc.)   | [sota-2025-2026.md](./references/sota-2025-2026.md)               |
| Worked Examples (BTC, EUR/USD)       | [worked-examples.md](./references/worked-examples.md)             |
| **Structured Logging (NDJSON)**      | [structured-logging.md](./references/structured-logging.md)       |

### Related Skills

| Skill                                                | Relationship                                           |
| ---------------------------------------------------- | ------------------------------------------------------ |
| [adaptive-wfo-epoch](../adaptive-wfo-epoch/SKILL.md) | Uses `weekly_sharpe`, `psr`, `dsr` for WFE calculation |

### Dependencies

```bash
pip install -r requirements.txt
# Or: pip install numpy>=1.24 pandas>=2.0 scipy>=1.10
```

## Key Formulas

### Daily-Aggregated Sharpe (Primary Metric)

```python
def weekly_sharpe(pnl: np.ndarray, timestamps: np.ndarray) -> float:
    """Sharpe with daily aggregation for range bars."""
    daily_pnl = _group_by_day(pnl, timestamps)  # Sum PnL per calendar day
    if len(daily_pnl) < 2 or np.std(daily_pnl) == 0:
        return 0.0
    daily_sharpe = np.mean(daily_pnl) / np.std(daily_pnl)
    # For crypto (7-day week): sqrt(7). For equities: sqrt(5)
    return daily_sharpe * np.sqrt(7)  # Crypto default
```

### Information Coefficient (Prediction Quality)

```python
from scipy.stats import spearmanr

def information_coefficient(predictions: np.ndarray, actuals: np.ndarray) -> float:
    """Spearman rank IC - captures magnitude alignment."""
    ic, _ = spearmanr(predictions, actuals)
    return ic  # Range: [-1, 1]. >0.02 acceptable, >0.05 good, >0.10 excellent
```

### Probabilistic Sharpe Ratio (Statistical Validation)

```python
from scipy.stats import norm

def psr(sharpe: float, se: float, benchmark: float = 0.0) -> float:
    """P(true Sharpe > benchmark)."""
    return norm.cdf((sharpe - benchmark) / se)
```

## Annualization Factors

| Market            | Daily → Weekly | Daily → Annual   | Rationale           |
| ----------------- | -------------- | ---------------- | ------------------- |
| **Crypto (24/7)** | sqrt(7) = 2.65 | sqrt(365) = 19.1 | 7 trading days/week |
| **Equity**        | sqrt(5) = 2.24 | sqrt(252) = 15.9 | 5 trading days/week |

**NEVER use sqrt(252) for crypto markets.**

## CRITICAL: Session Filter Changes Annualization

| View                             | Filter               | days_per_week | Rationale             |
| -------------------------------- | -------------------- | ------------- | --------------------- |
| **Session-filtered** (London-NY) | Weekdays 08:00-16:00 | **sqrt(5)**   | Trading like equities |
| **All-bars** (unfiltered)        | None                 | **sqrt(7)**   | Full 24/7 crypto      |

**Using sqrt(7) for session-filtered data overstates Sharpe by ~18%!**

See [crypto-markets.md](./references/crypto-markets.md#critical-session-specific-annualization) for detailed rationale.

## Dual-View Metrics

For comprehensive analysis, compute metrics with BOTH views:

1. **Session-filtered** (London 08:00 to NY 16:00): Primary strategy evaluation
2. **All-bars**: Regime detection, data quality diagnostics

## Academic References

| Concept                      | Citation                       |
| ---------------------------- | ------------------------------ |
| Deflated Sharpe Ratio        | Bailey & López de Prado (2014) |
| Sharpe SE with Non-Normality | Mertens (2002)                 |
| Statistics of Sharpe Ratios  | Lo (2002)                      |
| Omega Ratio                  | Keating & Shadwick (2002)      |
| Ulcer Index                  | Peter Martin (1987)            |

## Decision Framework

### Go Criteria (Research)

```yaml
go_criteria:
  - positive_sharpe_rate > 0.55
  - mean_weekly_sharpe > 0
  - cv_fold_returns < 1.5
  - mean_hit_rate > 0.50
```

### Publication Criteria

```yaml
publication_criteria:
  - binomial_pvalue < 0.05
  - psr > 0.85
  - dsr > 0.50 # If n_trials > 1
```

## Scripts

| Script                       | Purpose                                      |
| ---------------------------- | -------------------------------------------- |
| `scripts/compute_metrics.py` | Compute all metrics from predictions/actuals |
| `scripts/generate_report.py` | Generate Markdown report from fold results   |
| `scripts/validate_schema.py` | Validate metrics JSON against schema         |

## Remediations (2026-01-19 Multi-Agent Audit)

The following fixes were applied based on a 12-subagent adversarial audit:

| Issue                          | Root Cause                | Fix                                            | Source             |
| ------------------------------ | ------------------------- | ---------------------------------------------- | ------------------ |
| `weekly_sharpe=0`              | Constant predictions      | Model collapse detection + architecture fix    | model-expert       |
| `IC=None`                      | Zero variance predictions | Return 1.0 for constant (semantically correct) | model-expert       |
| `prediction_autocorr=NaN`      | Division by zero          | Guard for std < 1e-10, return 1.0              | model-expert       |
| Ulcer Index divide-by-zero     | Peak equity = 0           | Guard with np.where(peak > 1e-10, ...)         | risk-analyst       |
| Omega/Profit Factor unreliable | Too few samples           | min_days parameter (default: 5)                | robustness-analyst |
| BiLSTM mean collapse           | Architecture too small    | hidden_size: 16→48, dropout: 0.5→0.3           | model-expert       |
| `profit_factor=1.0` (n_bars=0) | Early return wrong value  | Return NaN when no data to compute ratio       | risk-analyst       |

### Model Collapse Detection

```python
# ALWAYS check for model collapse after prediction
pred_std = np.std(predictions)
if pred_std < 1e-6:
    logger.warning(
        f"Constant predictions detected (std={pred_std:.2e}). "
        "Model collapsed to mean - check architecture."
    )
```

### Recommended BiLSTM Architecture

```python
# BEFORE (causes collapse on range bars)
HIDDEN_SIZE = 16
DROPOUT = 0.5

# AFTER (prevents collapse)
HIDDEN_SIZE = 48  # Triple capacity
DROPOUT = 0.3     # Less aggressive regularization
```

See reference docs for complete implementation details.

---

## Troubleshooting

| Issue                      | Cause                        | Solution                                           |
| -------------------------- | ---------------------------- | -------------------------------------------------- |
| weekly_sharpe is 0         | Constant predictions         | Check for model collapse, increase hidden_size     |
| IC returns None            | Zero variance in predictions | Model collapsed - check architecture               |
| prediction_autocorr is NaN | Division by zero             | Guard for std < 1e-10 in autocorr calculation      |
| Ulcer Index divide error   | Peak equity is zero          | Add guard: np.where(peak > 1e-10, ...)             |
| profit_factor = 1.0        | No bars processed            | Return NaN when n_bars is 0                        |
| Sharpe inflated 18%        | Wrong annualization for data | Use sqrt(5) for session-filtered, sqrt(7) for 24/7 |
| PSR/DSR not computed       | Missing scipy                | Install: `pip install scipy`                       |
| Timestamps not parsed      | Wrong format                 | Ensure Unix timestamps, not datetime strings       |
