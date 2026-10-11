---
name: leaps-screen
description: LEAPS (long-dated equity options, 1-3 years out) selection framework. Filters strikes by IV, open interest, breakeven, leverage. Computes payoff at multiple price scenarios. Compares 2027/1 vs 2028/1 expiries. Recommends 2-3 strikes with position sizing and stock-vs-LEAPS comparison. Triggers in English ("LEAPS for X", "what call should I buy on X", "stock or LEAPS for X", "long-term options on X") or Chinese ("X 买什么 LEAPS", "X 的长期 call", "X 现货还是期权", "X 2027 call 推荐").
---

# LEAPS Screen — Long-Dated Options Selection

## 🔍 Pre-flight checklist — LEAPS amplify everything, including mistakes

LEAPS give 5-10x leverage. **Every methodology layer matters 5-10x more.** Required checks before recommending a strike:

1. **Macro regime is non-negotiable** — trigger `macro-warning`. LEAPS in 🔴 RED regime is a wealth-destruction trade. RED → only suggest LEAPS on deep-value names at 200DMA, never momentum names. YELLOW → cap LEAPS allocation at 3% of book. GREEN → full plan.
2. **Insider strict on the underlying** — `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/insider_ratio.py 2>/dev/null | head -1) TICKER --window 90`. If C-suite is distributing while user is considering a 2-year LEAPS, that's a hard NO. Form 4 code "P" only — RSU grants look bullish in headlines but aren't open-market buys.
3. **3-tier entry on the UNDERLYING, mapped to LEAPS strikes** — Don't recommend "Buy Jan 2027 $1100 call at market". Map: at $current → which strike? at -20% drawdown → which deeper-ITM strike? at 200DMA → which strike? User gets 3 strikes mapped to 3 underlying levels.
4. **Sizing 3-5% MAX per LEAPS** — and that's only if confidence ≥ 8/10. LEAPS can go to $0; size accordingly.
5. **Tax-aware exit** — LEAPS held > 1 year = LTCG. If user wants to exit within 12 months, mention STCG hit and quantify it. May be worth holding 30 more days.
6. **IV check** — If IV > 80% annualized, premium is too rich. Recommend waiting or smaller size, not just "the strike."

**"Look carefully" rule**: the most expensive LEAPS mistake is buying ATM/slightly-OTM on a momentum name at 52w high in YELLOW/RED regime. Theta + IV crush + first 10% drawdown wipes 60% of premium in weeks. ALWAYS check: where's the stock vs 200DMA + what's the macro regime + has insider been selling 90d?

See [README's Hard Rules](../README.md#%EF%B8%8F-hard-rules-never-violate) for the full anti-pattern list.

---

## What is a LEAPS?

**LEAPS** = Long-term Equity AnticiPation Securities. Options with **>1 year to expiry**. Used for:
- Leveraged long bets (5-10x leverage on capital)
- Lower capital requirement vs stock
- Defined max loss (premium paid)
- Tax efficiency (LTCG if held >1 year)

## When LEAPS > Stock

| Situation | Why LEAPS wins |
|---|---|
| High conviction + want leverage | 5-10x exposure with same capital |
| Limited capital, big idea | $5K LEAPS = $50K stock equivalent |
| Hedge alternative (sell stock + buy call) | Locks profit, keeps upside |
| Want defined max loss | Stock can go to $0; LEAPS just costs premium |
| Tax: short-term holder, long-term thesis | Hold LEAPS >1 year for LTCG |

## When Stock > LEAPS

| Situation | Why stock wins |
|---|---|
| Dividend payer (NOK, ORCL, BABA) | LEAPS don't get dividends |
| Uncertain timeline | LEAPS expire; stock doesn't |
| IV very high (>80%) | Premium too expensive, theta heavy |
| Buying for income | Need stock for covered calls/puts |
| Already maxed delta exposure | Adding LEAPS = double-down on same bet |

## The 5-Step LEAPS Selection Process

### Step 1 — Get available expiries
```
mcp__yfmcp__yfinance_get_option_dates(symbol="NVDA")
```
**Filter to LEAPS** (>1 year out). Typically:
- 2027/1/15
- 2027/3/19
- 2027/6/17
- 2027/9/17
- 2027/12/17
- **2028/1/21** (most popular)
- 2028/6/16
- 2028/12/15

### Step 2 — Pull option chains for top 2-3 expiries
```
mcp__yfmcp__yfinance_get_option_chain(symbol="NVDA", expiration_date="2027-01-15", option_type="calls")
```

### Step 3 — Filter strikes
**Hard filters:**
- **OI > 1000** (liquidity, must be able to exit)
- **IV < 80%** (not too pricey, but >40% for leverage)
- **Strike from ATM to +30% OTM**

**Goldilocks zone:**
- ATM strike: 0.50 delta, 50% leverage, breakeven需 +X% (depends on time to expiry)
- +10% OTM: 0.40 delta, more leverage, harder to win
- +20% OTM: 0.30 delta, 4-5x leverage, needs big move

### Step 4 — Calculate R/R for each candidate

For each strike, compute:

| Metric | Formula | Notes |
|---|---|---|
| Premium | (bid + ask) / 2 | Mid price |
| Cost per contract | premium × 100 | $ paid for 100 shares exposure |
| Breakeven | strike + premium | Stock must hit this to profit |
| Breakeven % gain | (breakeven - current) / current × 100 | How much stock needs to move |
| 2x scenario | strike + 2 × premium | Where stock = doubled premium |
| 3x scenario | strike + 3 × premium | Where stock = tripled |
| Max loss | premium × 100 | Total paid (if expires worthless) |
| Max loss % | 100% | Premium goes to 0 if OTM at expiry |

### Step 5 — Recommend 2-3 strikes with sizing

**Allocation rule of thumb:**
- LEAPS = **0.5-2%** of total portfolio per single position
- More than that = excessive concentration / risk
- Multiple LEAPS on same underlying: combine within 2-3% cap

**Tiered sizing (NVDA example):**
| Strike | Type | Cost | Allocation | Why |
|---|---|---|---|---|
| ATM ($200) | Conservative | $35 | 1% | Highest delta, lowest leverage |
| +10% OTM ($220) | Balanced | $25 | 0.7% | Best R/R at typical 1Y move |
| +20% OTM ($240) | Aggressive | $18 | 0.3% | Bull case lottery |

## Output format

```markdown
# [TICKER] LEAPS Screen — [Date]
**Current price**: $XXX | **Thesis**: [user's thesis or "general bullish"]

## Available LEAPS Expiries
- 2027/1/15 ([X] months out)
- 2028/1/21 ([Y] months out)

## Recommended: [Strike] [Expiry]

### Why this one
[2-3 bullet points: liquidity, R/R, IV reasonable]

### Specifics
| Metric | Value |
|---|---|
| Strike | $X |
| Expiry | YYYY-MM-DD |
| Mid premium | $X.XX |
| OI | X,XXX |
| IV | X.X% |
| Delta (est) | 0.X |
| Cost per contract | $X,XXX |
| Breakeven | $XXX (+X.X%) |
| 2x premium scenario | Stock @ $YYY (+Y.Y%) |
| 3x premium scenario | Stock @ $ZZZ (+Z.Z%) |

### Position sizing
- Suggested: X contracts = $Y,YYY total cost
- Portfolio %: Z.Z%
- Stop loss: 50% of premium ($X) or stock breaks 200DMA

### P&L Scenarios at expiry
| Stock @ Expiry | Intrinsic | P&L | % Return |
|---|---|---|---|
| Current ($XXX) | $0 | -$X (premium) | -100% |
| +10% | $X | -$Y | -X% |
| +20% | $X | +$Y | +X% |
| +50% | $X | +$Y | +X% |
| Bull target | $X | +$Y | +X% |

## Alternatives Considered (NOT recommended)
| Strike | Why NOT |
| $X | OI too low / IV too high / breakeven too far |

## Compared to Stock
- Stock $XXX: 1x leverage, no time decay, gets dividends
- LEAPS $X strike: ~Yx leverage, 12mo expiry, no dividend
- **Recommendation**: [LEAPS / mix / stock] because [reason]

## Risks
- IV crush after [event] could lose 20-30% even if stock unchanged
- If stock chops sideways, LEAPS lose to theta
- 12/18/2026 LEAPS in 2026 危险窗口 (yen carry / 1973)

## Tax considerations
- If held >1 year: LTCG (15-20%)
- If held <1 year: STCG (32-37%)
- Specific lot ID matters at exit
```

## Hard rules

1. **OI < 1000 = skip.** Liquidity > leverage.
2. **IV > 80% = warn user.** "贵了，等回调或换 expiry"
3. **Position size cap.** Per LEAPS = max 2% portfolio. Total LEAPS = max 10% portfolio.
4. **Always show breakeven %.** If breakeven needs +25%, that's not a "small" move.
5. **ATM vs OTM decision.** ATM = safer. OTM = more leverage but lower probability.
6. **Don't recommend 12/18 LEAPS in 2026.** User's portfolio审计显示 12/18 LEAPS 在 5-6 月 yen carry 窗口内 = 双重风险。Recommend 2027/1+ instead.
7. **Show alternatives that were considered but rejected.** Transparency.

## Common pitfalls

| Pitfall | Example | Lesson |
|---|---|---|
| Buying high-IV LEAPS pre-earnings | NVDA $250 call before NVDA ER, IV 90% | Pay 30% extra premium, IV crush after |
| Going too far OTM | NVDA $300 LEAPS when stock $200 | Need +60% just to break even |
| Buying 6-9 month "LEAPS" | NVDA 12/18 calls bought in 5/2026 | Theta heavy, not real LEAPS |
| Single huge LEAPS | $50K in one 2027 ATM call | Concentration = pain |
| Ignoring underlying tax | Buying 1/15/27 in 11/2025 = 14 months hold for LTCG | Plan exit dates |

## Special case: when user already owns stock

If user has 100+ shares, ask:
- "Want to add leverage with LEAPS?" → +OTM call, small size
- "Want to lock profit but stay in?" → Sell stock + buy LEAPS (synthetic long)
- "Want to hedge?" → That's `earnings-prep` skill, not this one

## Tool cheat-sheet

| Need | Tool |
|---|---|
| List expiries | `mcp__yfmcp__yfinance_get_option_dates` |
| Option chain | `mcp__yfmcp__yfinance_get_option_chain` |
| Live price | `mcp__yfmcp__yfinance_get_ticker_info` |
| Historical price for context | `mcp__yfmcp__yfinance_get_price_history` |

## Recommendation matrix (quick reference)

| Conviction | IV | Time horizon | Capital | Recommendation |
|---|---|---|---|---|
| High | <50% | 1-2 years | Limited | **LEAPS ATM, full size** |
| High | 50-70% | 1-2 years | Limited | LEAPS ATM, half size |
| High | >70% | Any | Any | Wait for IV drop, OR call spread |
| Med | <50% | 1+ years | Any | LEAPS +10% OTM, small size |
| Med | 50-70% | Any | Any | Stock or wait |
| Low | Any | Any | Any | Don't buy options, don't be in this |
| High | <50% | <1 year | Limited | Short-term call (not LEAPS) |
| High | <50% | >2 years | Any | 2028 LEAPS, deep ATM |

## When to invoke

- User asks: "What LEAPS should I buy on X?"
- User asks: "Should I buy stock or LEAPS?"
- User asks: "What's the best 2027 call for NVDA?"
- User describes a thesis with 1-2 year horizon
- After `analyze-stock` recommends LEAPS as the vehicle
