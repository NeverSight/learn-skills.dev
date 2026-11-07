---
name: position-sizing
description: |
  Calculate optimal position sizes for NSE/BSE equity trades using fixed fractional,
  ATR-based, and Kelly criterion methods. Includes portfolio constraints and leverage adjustments.

  Use when the user asks: "how many shares to buy", "position size for [stock]", "how much to
  invest in [stock]", "calculate lot size", "risk per trade", or any question about how much
  capital to allocate to a trade. Also triggers on portfolio allocation and leverage sizing questions.
---

# Position Sizing

Position sizing is how you survive. The goal: risk a small, consistent percentage of capital per trade so that no single loss can cripple your account.

## Prerequisites

No dependencies required. Works with manually provided prices. Enhanced with Groww MCP (live price, ATR, portfolio) or yfinance (`pip install yfinance`).

## Data Needed

1. **Account size**: Total trading capital (ask user if not known)
2. **Current price**: `get_quotes_and_depth` from Groww, or user-provided
3. **ATR(14)**: `get_historical_technical_indicators` from Groww, or calculate from candle data
4. **Existing positions**: `get_equity_portfolio_holdings` to check concentration (optional)

## Method 1: Fixed Fractional (Default)

This is the go-to method. Simple, robust, works for everyone.

```
Risk per trade = Account size × Risk%
Shares = Risk per trade ÷ (Entry price - Stop-loss price)
Capital required = Shares × Entry price
```

**Risk% guidelines:**
| Situation | Risk% |
|-----------|-------|
| Normal (no leverage) | 1-2% |
| With 2x leverage | 0.5-1% |
| With 3-4x leverage | 0.25-0.5% |
| High conviction trade | Up to 3% (rare) |
| New/uncertain setup | 0.5% |

### Example
```
Account: Rs.10,00,000
Risk: 2% = Rs.20,000
Entry: Rs.1,800
Stop: Rs.1,700 (Rs.100 risk per share)
Shares: 20,000 ÷ 100 = 200 shares
Capital: 200 × 1,800 = Rs.3,60,000 (36% of account)
```

## Method 2: ATR-Based Sizing

Uses volatility to set the stop distance, then sizes accordingly.

```
Stop distance = ATR(14) × multiplier
Shares = Risk amount ÷ Stop distance
```

| Market Condition | ATR Multiplier |
|-----------------|----------------|
| Low volatility (ADX < 20) | 1.5× ATR |
| Normal volatility | 2.0× ATR |
| High volatility (ADX > 30) | 2.5× ATR |

This naturally sizes you smaller in volatile stocks and larger in calm ones.

## Method 3: Kelly Criterion (Advanced)

For traders with a track record of at least 30 trades:

```
Kelly% = W - (1 - W) / R
W = historical win rate
R = average win / average loss

Use Half-Kelly (Kelly% ÷ 2) for real trading — full Kelly is too aggressive.
```

| Win Rate | Avg W/L Ratio | Kelly% | Half-Kelly |
|----------|---------------|--------|------------|
| 40% | 2.0 | 10% | 5% |
| 50% | 1.5 | 17% | 8% |
| 60% | 1.2 | 27% | 13% |

## Portfolio Constraints

These are hard limits — never exceed them regardless of sizing method:

| Constraint | Limit |
|-----------|-------|
| Single stock | Max 20% of portfolio |
| Single sector | Max 35% of portfolio |
| Total open risk | Max 6% of portfolio (sum of all position risks) |
| Correlated positions | Max 3 stocks in same sector simultaneously |

If a position would breach a constraint, reduce size until it fits.

## Leverage Adjustment

When using margin/leverage, the math changes because losses are amplified:

```
Effective risk% = Risk% × Leverage
So: reduce your base risk% by dividing by leverage

At 3.74x leverage:
  Normal risk: 2%
  Adjusted risk: 2% ÷ 3.74 ≈ 0.5%
  This keeps your effective risk at ~2%
```

## Output

Present position sizing as:
```
Position Size: XXX shares
Capital Required: Rs.X,XX,XXX
Risk Amount: Rs.X,XXX (X.X% of account)
Stop-Loss: Rs.XXX (X.X% below entry)
Portfolio Allocation: XX% of total capital
```
