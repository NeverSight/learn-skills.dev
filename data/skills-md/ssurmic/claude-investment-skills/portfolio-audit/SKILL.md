---
name: portfolio-audit
description: Comprehensive portfolio risk audit. Computes single-name concentration, factor cluster exposure, leverage ETF decay risk, options Greeks aggregation, stress test scenarios (-10% SPX, yen carry, single-name miss), hedge effectiveness. Outputs explicit trim list with $ amounts and reasons + cash target. Triggers in English ("review my portfolio", "audit my book", "am I too concentrated", "what should I trim", "portfolio risk check") or Chinese ("审一下我的组合", "我组合风险大吗", "该减什么仓", "组合审计", "我哪里太集中").
---

# Portfolio Audit — Full Risk Review

## Goal

A **fund-manager-level audit** of the user's entire book. Answer 6 questions definitively:

1. **Where is concentration risk?** (single-name + factor cluster)
2. **What blows up in -10% SPX day?** (correlation unwind paths)
3. **What's the true equity beta?** (incl. leverage ETFs and options delta)
4. **Where am I over-earning?** (positions that have run too far)
5. **What hedges should I add?** (gap protection)
6. **What trims should I execute today?** (with $ amounts + tax considerations)

## The 7-Step Workflow

### Step 1 — Inventory the book

Get from user (or screenshot via `review-investment-screenshot`):

**Stocks**: ticker, qty, avg cost, current price, market value
**Options**: ticker, strike, expiry, qty, cost, market value
**Cash + short-term**: $ amount

Compute:
- Total equity value
- Cash %
- Stock %
- Options notional %
- Total leveraged exposure

### Step 2 — Single-name concentration check

For each position, compute % of portfolio:

| % of book | Status | Action |
|---|---|---|
| < 3% | OK | None |
| 3-7% | Watching | Review thesis |
| 7-10% | Limit | Don't add |
| 10-15% | High | Trim to ≤10% |
| > 15% | EXTREME | Force trim to 10% (unless explicit conviction & long-term) |

**Exception**: User-defined "core hold" with locked thesis (e.g., NOK 19% with 1Y target $20+) — note but don't force trim.

### Step 3 — Factor cluster analysis

Group positions into factor clusters:

**Standard clusters for 2026:**
- **AI Semis** (NVDA, AMD, AVGO, MU, AMUU, MSFU等杠杆 ETF)
- **AI Compute / Cloud** (ORCL, CRWV, NBIS, IREN, APLD)
- **AI Network** (TEL, ANET, CIEN, FN, HPE, NOK)
- **AI Power** (CEG, VST, EQT, AEP, ETR, LEU)
- **AI Materials** (HBM, FCX, APD, MP)
- **Crypto-adjacent** (COIN, HOOD, MSTR)
- **Speculative growth** (AFRM, SOFI, U)
- **Mega-tech** (GOOGL, MSFT, META, AAPL, AMZN)
- **China** (BABA, JD, PDD, BIDU)
- **Defense/Aerospace** (LMT, CSTM)

**Aggregation rule**:
- Same factor cluster > 25% = **one bet** regardless of how many tickers
- Recommend trim or cross-cluster diversification

### Step 4 — Leverage / volatility decay check

Flag any:
- **Daily-reset 2x/3x ETFs** (MSFU, AMUU, GDXU, SOXL, TQQQ, NVDL等)
- **Held >2 weeks** (vol decay accumulates)
- **Up >20%** (rotate to LEAPS for cleaner exposure)

**Action**: Most leverage ETFs should be **closed and rotated to LEAPS** on the underlying.

### Step 5 — Options aggregation (Greeks-aware)

For each option position:
- **Delta** (estimate): ATM = 0.5, OTM 10% = 0.35, OTM 20% = 0.25, deep ITM = 0.85
- **Notional exposure**: contracts × 100 × strike (full notional)
- **Delta-weighted exposure**: notional × delta (true equity equivalence)
- **Theta risk**: short-dated (< 30 days) = high decay
- **IV exposure**: post-earnings IV crush risk

**Aggregate by underlying**: if user has 6 NVDA LEAPS + 350 stock + AMD LEAPS, what's the combined NVDA+AMD delta?

### Step 6 — Stress test scenarios

For each scenario, compute estimated portfolio impact:

| Scenario | What happens | Impact estimate |
|---|---|---|
| **SPX -5%** | Mild correction | Use beta × -5% |
| **SPX -10%** | Standard pullback | Beta × -10% + leverage ETF decay |
| **NDX -15%** (tech rotation) | Mag7/AI sells off | Heavy if cluster >30% AI |
| **Yen carry unwind (USD/JPY <153)** | -8 to -22% on AI semis | Compute by sector exposure |
| **Single name -30% (e.g., NVDA earnings miss)** | If concentrated | Show $ loss |
| **VIX > 30 (volatility regime change)** | Options IV crush + delta loss | Compute by options exposure |
| **OPEC + 1973 重演** | Energy spike + risk-off | Show defensive vs growth |

**Output**: "In a -10% SPX day, your book loses ~$X (X% of total)."

### Step 7 — Generate trim list + hedge recommendations

**Trim list** (specific orders):
| Ticker | Qty | $ proceeds | Rule fired | Tax impact |
|---|---|---|---|---|

**Hedge recommendations**:
| Hedge | Cost | Coverage | Why |
|---|---|---|---|
| SPY 6/18 $XXX Put × N | $X,XXX | Index gap | Macro red signal |
| Underlying-specific puts | | | If single name 10%+ |

**Cash target**:
- Risk-on regime → 5-15% cash
- Late-cycle / yellow → 20-30%
- Yellow + binary events → 30-40%
- Red regime / crisis → 40-60%

## Output format

```markdown
# Portfolio Audit — [Date]

## TL;DR
- Total: $X.XX M (stocks + options + cash)
- Cash %: X% (target Y% based on macro)
- Top 3 risks: [concrete sentences]
- **Action today**: [trim X / hedge Y / hold Z]

## Position Table (top 25 by % of book)
| Ticker | Qty | Mkt Val | % of book | P&L $ | P&L % | Status | Action |

## Cluster Concentration
| Cluster | % of book | Status | Top names |
| AI Semis | XX% | 🔴 Over (>25%) | NVDA, AMD, AVGO |
| AI Power | XX% | 🟢 OK | EQT, CEG, AEP |

## Concentration Flags
- 🔴 Single-name > 15%: [list]
- 🔴 Cluster > 25%: [list]
- 🔴 Leverage ETF > 5%: [list]

## Greeks Aggregation
| Underlying | Stock notional | Options delta-weighted | Total | $ Risk |

## Stress Tests
| Scenario | Impact $ | Impact % |
| -10% SPX | -$XX,XXX | -X.X% |
| Yen carry unwind | -$XX,XXX | -X.X% |

## Trim List (orders to place today)
| Ticker | Qty | ~$ proceeds | Rule | Tax |

## Hedge Recommendations
| Hedge | Cost | Why |

## What's NOT to trim (core holds)
- [List positions to leave alone]

## Tax Considerations
- Proceeds from suggested trims: $X
- Estimated tax (LTCG/STCG mix): $X
- Net to bank: $X
- Better: hedge with puts on [list] to defer tax

## Recommended Cash Target
- Current: X%
- Target (based on macro): Y%
- Action: raise/lower by trimming/buying [list]
```

## Hard rules (the trim ladder)

Run **every position** through this in order. Call the FIRST rule that fires:

| # | Condition | Action |
|---|---|---|
| 1 | Daily-reset leveraged ETF held >2 weeks AND up >20% | **Trim 50%+**, rotate to LEAPS |
| 2 | Position up >100% unrealized | **Sell at least 1/3** to recover cost basis |
| 3 | Position up >50% AND single-name >10% of book | **Trim to ≤10%** |
| 4 | Single factor cluster >25% of book | **Reduce to ≤20%** by trimming most-extended in cluster |
| 5 | At 1-year high AND earnings within 7 days | **Trim 25-50%** before print |
| 6 | Up >30% AND >40% above 200DMA (parabolic) | **Trim 25%** OR set hard stop at MA20 |
| 7 | Portfolio total unrealized >20% AND macro = late-cycle euphoria | **Reduce gross 10-15%** via index hedge |
| 8 | Up >20% but thesis broken (below MA50 in downtrend OR narrative shift) | **Exit 50%+** immediately |
| 9 | Underwater >15% AND bear case confirmed by price | **Cut.** Don't average |
| 10 | None of above | **Hold.** State trailing stop level |

## Macro contextual overlays

Adjust trim aggressiveness based on macro signals (run `macro-risk-check` first):
- **Yen carry risk active (USD/JPY < 153)**: Reduce semi-cluster to <20%
- **Pre-major central bank meeting**: Cash target 30%+
- **Pre-major geopolitical summit**: Hold core thesis names for upside optionality
- **Energy/oil supply shock active**: Defensive + reduce growth allocation

## Common pitfalls

| Pitfall | Example | Lesson |
|---|---|---|
| Counting tickers as diversification | 6 AI semis = "diversified" | One bet |
| Ignoring options notional | $50K LEAPS = $200K delta | Use Greeks |
| Trim winners, hold losers | Sell NVDA +20%, hold INTC -50% | Reverse — trim losers, ride winners (with stops) |
| Over-trim during stress | Sell 50% on -3% day | Wait for trigger or hedge instead |
| No tax plan | Sell 1000 NOK STCG vs LTCG | Lose 12-15% to tax |
| Hedge after the move | Buy puts after -10% drop | Should be pre-event, not reactive |

## Tool cheat-sheet

| Need | Tool |
|---|---|
| Live prices for all positions | `mcp__yfmcp__yfinance_get_ticker_info` (batch) OR `quote_pull.py` |
| Sector classification | `mcp__yfmcp__yfinance_get_ticker_info` → `sector` field |
| Options Greeks | Estimate from strike/spot/days. Use `mcp__yfmcp__yfinance_get_option_chain` for IV |
| Insider check on top positions | `insider_ratio.py "TICKER1,TICKER2,..." --window 90` (openinsider primary; only Form 4 code "P" counts as buy) |
| Macro overlay | Run `macro-risk-check` skill first |
| Tax math | Run `tax-optimize` skill on each trim candidate |
| Trim execution rules | This SKILL.md, the 10-rule ladder |

## When to invoke

- User asks: "Review my portfolio"
- User asks: "Am I too concentrated"
- User asks: "What should I trim"
- User asks: "Should I hedge"
- After macro-risk-check shows YELLOW or worse
- Monthly (recommended)
- Pre-major event (Fed, BOJ, Trump-Xi, earnings cluster)
- After any position becomes >15% of book (auto-trigger)

## Companion skills

This skill orchestrates these others:
- `macro-risk-check` → regime context (run first)
- `analyze-stock` → deep dive on questionable positions
- `tax-optimize` → calculate trim taxes
- `earnings-prep` → for any position with earnings <30 days
- `option-wall-analysis` → set strike levels for hedges
- `leaps-screen` → for ETF→LEAPS rotation (Rule #1)
- `review-investment-screenshot` → if user provides screenshot input

## Integration with existing review-investment-screenshot skill

`portfolio-audit` is the **deeper sibling** of `review-investment-screenshot`. Differences:

| | review-investment-screenshot | portfolio-audit |
|---|---|---|
| Input | Screenshot | Manual list or screenshot |
| Depth | 7-point check | 7 steps + Greeks + clusters + tax |
| Output | Sell list | Sell list + hedges + cash target + stress tests |
| When | Quick review | Monthly deep dive |
| Audience | Single review | Full periodic audit |
