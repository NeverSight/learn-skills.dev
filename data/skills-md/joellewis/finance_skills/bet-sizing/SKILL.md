---
name: bet-sizing
description: "Determine how much capital to allocate to individual positions within a portfolio. Use when the user asks about position sizing, the Kelly criterion, fractional Kelly, risk budgeting, or conviction weighting. Also trigger when users mention 'how much to put in one stock', 'maximum position size', 'how concentrated should my portfolio be', 'number of holdings', 'VaR budget per position', 'how big a bet', or ask about scaling position sizes with volatility."
---

# Bet Sizing

## Purpose
Provides frameworks for determining how much capital to allocate to individual positions within a portfolio. Covers the Kelly criterion, fractional Kelly, risk budgeting, liquidity-based sizing, and conviction weighting. Proper bet sizing is critical — even a portfolio of good ideas can fail with poor sizing.

## Layer
4 — Portfolio Construction

## Direction
prospective

## When to Use
- Determining the appropriate size for a new position
- Applying the Kelly criterion to a bet or investment with estimable odds
- Allocating a risk budget across active positions
- Setting maximum position sizes based on liquidity or risk limits
- Sizing positions proportional to conviction and edge
- Deciding the optimal number of positions in a concentrated portfolio
- Scaling position sizes with volatility changes

## Core Concepts

### Kelly Criterion (Discrete)
For a binary bet with payoff odds b, win probability p, and loss probability q = 1-p:

f* = (b*p - q) / b

where f* is the optimal fraction of wealth to wager. The Kelly criterion maximizes the expected logarithm of wealth (geometric growth rate) over repeated bets.

Properties:
- f* = 0 when edge = 0 (no bet when there is no advantage)
- f* < 0 when negative edge (the formula tells you to bet the other side)
- f* > 0 only when b*p > q (positive expected value)

### Kelly Criterion (Continuous / Investment)
For a normally distributed investment return with expected excess return mu-r_f and variance sigma^2:

f* = (mu - r_f) / sigma^2

This gives the fraction of total wealth to allocate. For example, an asset with 8% expected excess return and 20% volatility: f* = 0.08 / 0.04 = 2.0 (200% of wealth — implying leverage).

### Fractional Kelly
Full Kelly sizing is theoretically optimal but practically too aggressive because:
- It assumes perfect knowledge of probabilities and payoffs
- It produces large drawdowns (the expected drawdown of full Kelly is significant)
- Estimation error in parameters can turn optimal into catastrophic

Practical approach: use a fraction of Kelly, commonly:
- **Half Kelly (f*/2):** Achieves 75% of the growth rate with substantially lower variance and drawdown risk
- **Third Kelly (f*/3):** Even more conservative; appropriate when parameter uncertainty is high
- **Quarter Kelly (f*/4):** Suitable for highly uncertain estimates

The key insight: the growth rate curve is flat near the peak. Reducing from full Kelly to half Kelly only sacrifices 25% of growth but reduces risk dramatically.

### Risk Budgeting
Allocate risk (not capital) across positions. The total risk budget is the maximum acceptable portfolio risk (e.g., 10% VaR or 5% tracking error).

**VaR-based budgeting:**
- Total VaR budget: e.g., $1M at 95% confidence
- Allocate across positions: Position VaR_i <= allocated VaR_i
- Position VaR = w_i * sigma_i * z_alpha * Portfolio Value

**Tracking error budgeting (for active managers):**
- Total active risk budget: e.g., 4% tracking error
- Allocate across bets: each active bet consumes a portion of tracking error
- Size active positions so that sum of risk contributions equals total risk budget

### Maximum Position Sizes
Hard limits on individual positions to prevent concentration risk:

**Liquidity-based limits:**
- Position < X% of average daily volume (ADV) — common limits: 10-25% of ADV
- Ensures ability to exit within a reasonable time frame (e.g., 5-10 trading days)

**Risk-based limits:**
- Position risk contribution < X% of portfolio volatility (e.g., max 10% of portfolio risk)
- Single position < X% of portfolio value (common: 5% for diversified, 10% for concentrated)

**Regulatory/mandate limits:**
- Mutual fund: no more than 5% in a single name (diversified fund) or 25% (non-diversified)
- Index tracking: weight cannot deviate from benchmark by more than specified amount

### Conviction Weighting
Size positions proportional to the strength of the investment thesis:

- **High conviction (largest positions):** Strong edge, deep research, multiple confirming factors
- **Medium conviction:** Solid thesis but some uncertainty or limited information
- **Low conviction (smallest positions):** Early-stage idea, limited edge, or purely diversification-motivated

Framework: Score each position on edge strength (1-5) and certainty (1-5). Size proportional to the product: edge * certainty.

### Optimal Number of Positions
Trade-off between diversification and conviction:

- **Concentrated (10-20 positions):** High conviction, deep research. Each position is 5-10% of the portfolio. Appropriate when the manager has genuine skill and edge.
- **Diversified (50-100 positions):** Lower conviction per position but broader risk reduction. Each position is 1-3%. Appropriate for systematic or factor-based strategies.
- **Very diversified (100+):** Index-like. Risk comes from factor tilts, not individual positions.

### Volatility Scaling
Adjust position sizes inversely with volatility to maintain consistent risk per position:

Adjusted size = Target risk / Current volatility

When volatility doubles, position size halves, keeping the dollar risk constant. This is a core principle in managed futures and risk-targeting strategies.

### Anti-Martingale (Kelly-like) Sizing
Increase position sizes after gains (wealth grows, so Kelly fraction applied to larger base) and decrease after losses. This contrasts with martingale strategies (doubling down after losses) which can lead to ruin.

Kelly naturally implements anti-martingale sizing: bet a constant fraction of current wealth, so absolute bet size grows with wealth and shrinks with losses.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Kelly (Discrete) | f* = (b*p - q) / b | Binary bet sizing |
| Kelly (Continuous) | f* = (mu - r_f) / sigma^2 | Investment position sizing |
| Half Kelly | f = f* / 2 | Practical conservative sizing |
| Growth Rate at Kelly | g* = (mu - r_f)^2 / (2*sigma^2) | Maximum geometric growth |
| Growth Rate at f | g(f) = f*(mu - r_f) - f^2*sigma^2/2 | Growth rate for any fraction |
| Volatility-Scaled Size | w = target_risk / sigma_i | Constant risk per position |
| Position VaR | VaR_i = w_i * sigma_i * z_alpha * V | Position-level risk |

## Worked Examples

### Example 1: Kelly Criterion for a Discrete Bet
**Given:**
- Win probability: p = 55%
- Loss probability: q = 45%
- Even-money payoff: b = 1 (win $1 for every $1 wagered)

**Calculate:** Optimal bet size

**Solution:**

f* = (b*p - q) / b = (1 * 0.55 - 0.45) / 1 = 0.10 / 1 = **10%**

Interpretation: Wager 10% of current wealth on each bet. This maximizes long-run geometric growth.

Practical adjustment (half Kelly): f = 10% / 2 = **5%** — achieves 75% of the maximum growth rate with much lower drawdown risk.

Full Kelly expected drawdown: the probability of losing 50% of wealth at some point is substantial. Half Kelly dramatically reduces this tail risk.

### Example 2: Continuous Kelly for an Investment
**Given:**
- Expected excess return (mu - r_f): 8%
- Volatility (sigma): 20%

**Calculate:** Kelly-optimal allocation

**Solution:**

f* = (mu - r_f) / sigma^2 = 0.08 / (0.20)^2 = 0.08 / 0.04 = **2.00 (200%)**

This implies 200% allocation (2x leverage), which is extremely aggressive.

Practical adjustments:
- Half Kelly: 100% (no leverage, fully invested)
- Third Kelly: 67% allocation
- Quarter Kelly: 50% allocation

Given that the 8% expected return and 20% volatility are estimates with significant uncertainty, half Kelly (100%) or less is prudent. The growth rate curve is:
- Full Kelly: g* = 0.08^2 / (2 * 0.04) = 8% per year
- Half Kelly: g(1.0) = 1.0 * 0.08 - 1.0^2 * 0.04/2 = 6% per year (75% of maximum)
- Quarter Kelly: g(0.5) = 0.5 * 0.08 - 0.5^2 * 0.04/2 = 3.5% per year (44% of maximum)

## Common Pitfalls
- Full Kelly is too aggressive for practical use — estimation errors in probabilities and payoffs can lead to over-betting and ruin; always use fractional Kelly
- Kelly assumes known probabilities and payoffs — in reality these are estimated with significant error, making full Kelly dangerous
- Kelly maximizes log wealth (geometric growth rate), which may not match an investor's actual utility function or risk tolerance
- Ignoring liquidity constraints: Kelly-optimal size may exceed what the market can absorb without impact
- Correlation between positions: the single-asset Kelly formula does not account for portfolio effects; positions with correlated risk collectively require smaller sizing
- Survivorship bias in parameter estimation: historical win rates may overstate future edge
- Not adjusting for regime changes: edge and volatility are time-varying

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): realized volatility as a key input to Kelly sizing
- **forward-risk** (wealth-management plugin, Layer 1b): expected return forecasts as inputs to Kelly criterion
- **diversification** (wealth-management plugin, Layer 4): tension between concentration (large bets) and diversification (many small bets)
- **asset-allocation** (wealth-management plugin, Layer 4): bet sizing operates within the asset allocation framework
- **rebalancing** (wealth-management plugin, Layer 4): positions drift from target sizes and require rebalancing
- **quantitative-valuation** (wealth-management plugin, Layer 3): valuation-based edge estimates feed into conviction weighting

## Reference Implementation
See `scripts/bet_sizing.py` for computational helpers.
