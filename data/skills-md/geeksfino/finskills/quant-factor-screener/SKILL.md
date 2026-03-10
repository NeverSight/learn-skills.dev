---
name: quant-factor-screener
description: Systematic multi-factor stock screening using formal factor models to identify stocks with favorable factor exposures. Use when the user asks about factor investing, multi-factor screening, value/momentum/quality factor analysis, factor scoring, factor timing, smart beta strategies, quantitative stock screening, or systematic equity selection based on academic factors.
license: Apache-2.0
---

# Quantitative Factor Screener

Act as a quantitative equity analyst. Screen stocks using a systematic multi-factor framework based on academic factor research — scoring and ranking companies across value, momentum, quality, low volatility, size, and growth factors.

## Workflow

### Step 1: Define Parameters

Confirm with the user:

| Input | Options | Default |
|-------|---------|---------|
| Universe | S&P 500 / Russell 1000 / Russell 3000 / Custom | Russell 1000 |
| Factors | All 6 or specific factors | All |
| Factor weights | Equal or custom | Equal weight |
| Sector constraints | Sector-neutral or unconstrained | Sector-neutral |
| Number of results | Top N stocks | Top 20 |
| Macro regime | Current assessment for factor timing | Auto-detect |
| Exclusions | Sectors, industries, specific stocks | None |

### Step 2: Calculate Factor Scores

Score every stock in the universe on each factor. See [references/factor-methodology.md](references/factor-methodology.md) for detailed definitions.

| Factor | Primary Metrics | Weight in Composite |
|--------|----------------|-------------------|
| Value | Earnings yield, book/price, FCF yield, EV/EBITDA | 1/6 (or custom) |
| Momentum | 12-1 month price return, earnings revision momentum | 1/6 |
| Quality | ROE, earnings stability, low leverage, accruals | 1/6 |
| Low volatility | Realized volatility (1Y), beta, downside deviation | 1/6 |
| Size | Market capitalization (smaller = higher score) | 1/6 |
| Growth | Revenue growth, earnings growth, margin expansion | 1/6 |

For each factor:
1. Calculate raw metric for each stock
2. Rank within sector (if sector-neutral) or universe (if unconstrained)
3. Convert ranks to percentile scores (0–100)
4. Combine sub-metrics into composite factor score

### Step 3: Composite Score

```
Composite Score = Σ (Factor Weight × Factor Score)
```

Rank all stocks by composite score from highest to lowest.

### Step 4: Factor Timing Assessment

Assess the current macro regime and its implications for factor performance. See [references/factor-methodology.md](references/factor-methodology.md).

| Macro Regime | Favored Factors | Disfavored Factors |
|-------------|----------------|-------------------|
| Early expansion | Size, Momentum | Low Volatility |
| Late expansion | Quality, Value | Size |
| Slowdown | Low Volatility, Quality | Momentum, Size |
| Recession | Low Volatility, Value (deep) | Momentum, Growth |
| Recovery | Value, Size, Momentum | Low Volatility |

Based on the current regime, provide a factor timing overlay that adjusts weights.

### Step 5: Factor Crowding Analysis

Assess whether popular factors are overcrowded:

| Signal | Crowded | Uncrowded |
|--------|---------|-----------|
| Valuation spread (cheap vs expensive within factor) | Narrow | Wide |
| Factor return correlation | High (many following same signal) | Low |
| ETF flows into factor | Surging inflows | Outflows |
| Media/analyst attention | Heavily discussed | Ignored |

Flag factors that appear crowded — returns may be compressed.

### Step 6: Present Results

Format per [references/output-template.md](references/output-template.md):

1. **Macro Regime Assessment** — Current regime and factor timing view
2. **Factor Crowding Dashboard** — Which factors are crowded/uncrowded
3. **Top Picks Table** — Top N stocks with individual factor scores and composite
4. **Sector Distribution** — How the top picks distribute across sectors
5. **Factor Exposure Summary** — What the resulting list is tilted toward
6. **Individual Stock Cards** — Brief profile for each top pick
7. **Risk Considerations** — Factor drawdown history and current risks
8. **Disclaimers**

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`findata-toolkit-us`). It provides real-time stock metrics, SEC filings, financial calculators, portfolio analytics, factor screening, and macro indicators — all without API keys.

## Important Guidelines

- **Factors are not magic**: Factors have long periods of underperformance. Value underperformed for a decade (2010–2020). Momentum crashes periodically. Set expectations.
- **Sector neutrality matters**: Without sector constraints, factor screens often produce concentrated sector bets disguised as factor bets.
- **Backtest ≠ future**: All factor research is backward-looking. Factors may be arbitraged away as they become popular.
- **Multi-factor is more robust**: No single factor works all the time. Combining factors reduces drawdowns and smooths returns.
- **Transaction costs**: Momentum strategies require higher turnover. Factor in realistic transaction costs.
- **Not personalized advice**: Factor screening is analytical tool, not investment recommendation. Individual circumstances vary.
