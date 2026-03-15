---
name: blofin-risk-manager
description: "Risk management for BloFin trading — position sizing, leverage assessment, liquidation monitoring, risk scoring, and exposure analysis. Helps maintain disciplined trading within user-defined risk parameters."
version: 1.0.0
license: Apache-2.0
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins:
        - node
      env:
        - BLOFIN_API_KEY
        - BLOFIN_API_SECRET
        - BLOFIN_PASSPHRASE
    primaryEnv: BLOFIN_API_KEY
auto_activate:
  - "risk"
  - "liquidation"
  - "position size"
  - "how much should I"
  - "risk management"
  - "exposure"
  - "margin ratio"
  - "safe leverage"
---

# BloFin Risk Manager

Comprehensive risk management skill for BloFin trading. Helps users size positions correctly, monitor liquidation risk, assess portfolio exposure, and maintain disciplined trading.

## Risk Analysis Workflows

### 1. Pre-Trade Risk Assessment

Before any trade, evaluate the risk:

1. **Get account balance** via `get_balance` — available equity
2. **Get instrument specs** via `get_instruments` — contract value, max leverage
3. **Get current price** via `get_tickers`
4. **Get existing positions** via `get_positions` — current exposure
5. **Calculate and present:**

```
Pre-Trade Risk Assessment
=========================
Instrument: BTC-USDT
Account Equity: $X,XXX
Available Margin: $X,XXX
Current Price: $XX,XXX

Proposed Trade:
- Side: Long
- Size: XX contracts
- Leverage: XXx
- Notional Value: $X,XXX
- Required Margin: $X,XXX
- Margin Usage After Trade: XX%

Risk Metrics:
- Estimated Liquidation Price: $XX,XXX
- Distance to Liquidation: XX%
- Max Loss (to liquidation): $X,XXX
- Risk per Account: XX% of equity

⚠️ Warning: [if margin usage > 50% or risk > 5% of equity]
```

**Example prompts:**
- "Should I open a 10x BTC long with 100 contracts?"
- "What's the risk if I short ETH with 5x leverage?"
- "How much can I lose on this trade?"

---

### 2. Position Sizing Calculator

Calculate optimal position size based on risk tolerance:

```
Use this formula:
Max Position Size = (Account Equity * Risk%) / (Entry Price * Contract Value * (1/Leverage))

Where Risk% is the maximum percentage of equity to risk (default 2%).
```

**Steps:**
1. Ask user for risk tolerance (default: 2% of equity per trade)
2. Get account equity from `get_balance`
3. Get contract specs from `get_instruments`
4. Get current price from `get_tickers`
5. Calculate recommended position size at different leverage levels

**Present as a table:**

| Leverage | Position Size | Notional | Required Margin | Liquidation Distance |
|----------|--------------|----------|-----------------|---------------------|
| 5x | XX contracts | $X,XXX | $XXX | XX% |
| 10x | XX contracts | $X,XXX | $XXX | XX% |
| 20x | XX contracts | $X,XXX | $XXX | XX% |

**Example prompts:**
- "How many BTC contracts should I buy?"
- "Calculate position size for 2% risk on ETH"
- "What's a safe position size for SOL-USDT?"

---

### 3. Liquidation Monitoring

Monitor liquidation risk for all open positions:

1. **Get all positions** via `get_positions`
2. **Get mark prices** via `get_mark_price` for each position
3. **For each position, calculate:**
   - Distance to liquidation: `|markPrice - liquidationPrice| / markPrice * 100%`
   - Unrealized PnL and PnL ratio
   - Effective leverage (notional value / margin)

4. **Risk classification:**

| Distance to Liquidation | Risk Level | Action |
|------------------------|------------|--------|
| > 30% | Low | Normal monitoring |
| 15% - 30% | Medium | Consider reducing position or adding margin |
| 5% - 15% | High | Strongly recommend reducing position |
| < 5% | Critical | Immediate action required — reduce or close |

**Example prompts:**
- "Am I at risk of liquidation?"
- "Check my liquidation distances"
- "Which positions are most dangerous?"

---

### 4. Portfolio Exposure Analysis

Evaluate overall portfolio risk:

1. **Get all positions** via `get_positions`
2. **Get account balance** via `get_balance`
3. **Calculate:**
   - Total notional exposure (sum of all position notional values)
   - Net exposure (long notional - short notional)
   - Gross leverage (total notional / equity)
   - Directional bias (net long vs net short)
   - Concentration risk (% of exposure in single instrument)

**Present:**

```
Portfolio Exposure Report
=========================
Total Equity: $X,XXX
Total Notional: $XX,XXX
Gross Leverage: X.Xx
Net Exposure: $X,XXX (long/short biased)

Position Breakdown:
| Instrument | Side | Notional | % of Total | Leverage |
|------------|------|----------|-----------|----------|

Concentration: XX% in [top instrument] ⚠️ (>30% = concentrated)
```

**Example prompts:**
- "What's my total exposure?"
- "Am I too concentrated in BTC?"
- "Show my portfolio risk breakdown"

---

### 5. Leverage Safety Check

Evaluate whether current leverage settings are appropriate:

1. **Get leverage info** via `get_leverage_info` for each held instrument
2. **Compare against:**
   - Account size (smaller accounts should use lower leverage)
   - Market volatility (high volatility = lower leverage recommended)
   - Number of open positions (more positions = lower per-position leverage)

**General leverage guidelines:**

| Account Size | Recommended Max Leverage | Rationale |
|-------------|------------------------|-----------|
| < $1,000 | 5x | Limited margin buffer |
| $1,000 - $10,000 | 10x | Moderate buffer |
| $10,000 - $100,000 | 20x | Experienced trader range |
| > $100,000 | Per strategy | Professional risk management |

**Example prompts:**
- "Is my leverage too high?"
- "What leverage should I use for a $5,000 account?"
- "Review my leverage settings"

## Risk Management Rules

1. **Never encourage excessive risk** — if a user wants 100x leverage on their full balance, advise against it clearly
2. **Default risk per trade: 1-2%** of account equity
3. **Always show liquidation price** when discussing leveraged positions
4. **Warn about correlation risk** — multiple positions in similar assets (e.g., BTC + ETH) are correlated
5. **Recommend stop losses** for every position
6. **Account for fees** — they reduce margin and affect liquidation price
7. **Cross margin warning** — in cross mode, one liquidation can cascade to affect all positions
