---
name: ib_trade-execution
description: "Risk & Trade Execution skill. Governs capital allocation, risk management, and final order proposals for NeonTrade based on intelligence and analysis."
---

# Skill: ib_trade-execution

## Purpose
This skill governs capital allocation, risk management, and the final execution of buy/sell/hold decisions for NeonTrade. It converts intelligence and analysis into specific order proposals.

## Core Mandates
1. **Capital Allocation Rules:** Never deploy more than the configured `capital_usage_limit` (percentage of available cash).
2. **Short-Term Focus:** Prioritize high-conviction, short-horizon opportunities, particularly around the Monday U.S. market open.
3. **Deterministic Execution:** While signal generation is probabilistic, the execution logic must be deterministic and rule-bound.

## 1. Risk Modes
Final position sizing and selection must be scaled based on the active risk mode:
- **Low Risk:** Smaller capital deployment, strict confirmation requirements, preferred holding of existing positions.
- **Medium Risk:** Balanced deployment, rotation from weak to strong names, some tactical entries.
- **High Risk:** Larger capital deployment, aggressive rotation, lower confirmation thresholds, accepts speculative entries.

## 2. Weekly Execution Window (Monday Open)
- **Pre-Open (08:30–09:20 ET):** Final review of news, price behavior, and existing holdings.
- **Open (09:30 ET):** Submit orders (stock, fractional stock, or options).
- **Post-Open (09:30–10:30 ET):** Monitor reaction and avoid overcommitting if price action becomes unstable.

## 3. Decision Rules
- **Buy Logic:** Rank candidates from Analysis skill. Deploy capital only if cash is available and setups fit the current risk mode.
- **Sell Logic:** Full or partial exit if thesis fails, a negative catalyst appears, or a clearly superior rotation candidate is identified.
- **Hold Logic:** Valid when no strong sell reason exists and no better replacement is available.

## 4. Currency Management (EUR to USD)
NeonTrade uses a persistent USD trading pool to minimize FX friction.
- **Initial Conversion:** Convert 80-100% of new EUR deposits into USD.
- **Trading Pool:** All stock trades, sales, and dividends stay in USD.
- **Liquidity Buffer:** Maintain a minimum USD buffer. Trigger EUR to USD conversion only when buffer is low or new funds arrive.

## 5. Controlled Randomness (Optional)
In Medium/High risk modes, the system may use controlled randomness to choose between similarly ranked candidates or vary position sizes within allowed bounds.

## 6. Target Execution Output (JSON/YAML)
Every execution run must produce a structured list of orders:
- `ticker`: Stock symbol.
- `action`: `buy`, `sell`, `hold`, `limit_buy`, or `limit_sell`.
- `quantity`: Number of shares or options contracts (supports fractional shares).
- `order_type`: `market`, `limit`, or `staged`.
- `limit_price`: Required for limit orders.
- `risk_mode`: The risk level applied to this decision.
- `justification`: Concise reasoning tied back to catalyst and risk mode.
