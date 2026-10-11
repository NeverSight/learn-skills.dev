---
name: tax-optimize
description: Calculate optimal trim strategy with tax math. Compares Sell-Now (STCG/LTCG depending on holding period) vs Wait-for-LTCG vs Hedge-with-Puts (no taxable event). Computes lot identification (FIFO/HIFO/Specific Lot), tax loss harvesting opportunities. Asks for shares + buy date + income bracket + state. Triggers in English ("should I sell X for tax", "tax on selling X", "LTCG vs STCG on X", "trim X tax efficient") or Chinese ("X 减仓税务", "X 卖出税多少", "现在卖还是等长期", "X 减仓最省税").
---

# Tax Optimize — LTCG vs STCG Decision Framework

## Goal

When user wants to trim a winner, **don't just sell** — calculate:
1. **LTCG vs STCG difference** ($ saved by waiting)
2. **Specific lot identification** (which shares to sell first)
3. **Hedge-with-put alternative** (no taxable event, similar risk reduction)
4. **Tax-loss harvesting** (offset gains with losses elsewhere)

## US Tax Rates Quick Reference (2026)

### Short-Term Capital Gains (held < 1 year)
**Taxed as ordinary income.** Federal rates depend on AGI:

| AGI (single) | AGI (MFJ) | Rate |
|---|---|---|
| < $11,925 | < $23,850 | 10% |
| $11,925-48,475 | $23,850-96,950 | 12% |
| $48,475-103,350 | $96,950-206,700 | 22% |
| $103,350-197,300 | $206,700-394,600 | 24% |
| $197,300-250,525 | $394,600-501,050 | 32% |
| $250,525-626,350 | $501,050-751,600 | 35% |
| > $626,350 | > $751,600 | 37% |

**Plus state tax**: 0-13.3% (CA highest, TX/FL/WA = 0%)
**Plus NIIT** (Net Investment Income Tax): 3.8% if MAGI > $200K (single) / $250K (MFJ)

### Long-Term Capital Gains (held ≥ 1 year)
**Federal:**
| AGI (single) | AGI (MFJ) | Rate |
|---|---|---|
| < $48,350 | < $96,700 | 0% |
| $48,350-533,400 | $96,700-600,050 | 15% |
| > $533,400 | > $600,050 | 20% |

**Plus state**: same as ordinary (CA does NOT distinguish LTCG)
**Plus NIIT**: 3.8% if applicable

### Quick rule of thumb (high earner, $400K+ income)
- **STCG**: 32-37% federal + 3.8% NIIT + state = **38-50%+ effective**
- **LTCG**: 20% federal + 3.8% NIIT + state = **24-37% effective**
- **Difference**: ~12-15% of gain

## The 5-Step Workflow

### Step 1 — Get user's input

Ask if not provided:
- **Ticker** + how many shares to sell
- **Approximate income bracket** (or just "high earner $400K+" / "mid $200K" / etc.)
- **Buy date(s) for the lots being sold** — CRITICAL for STCG vs LTCG
- **State of residence** (CA/NY/TX/FL/WA)
- **Any浮亏 positions?** (for tax loss harvesting)

### Step 2 — Calculate STCG vs LTCG difference

```python
# Example: 1000 shares of XYZ, avg cost $10, current $13
gain_per_share = 13 - 10  # $3
total_gain = 1000 * 3  # $3,000

# STCG (high earner, NIIT applies, CA resident as example)
stcg_rate = 0.32 + 0.038 + 0.093  # federal + NIIT + CA = ~45%
stcg_tax = total_gain * stcg_rate  # ~$1,350
stcg_net = (1000 * 13) - stcg_tax  # ~$11,650

# LTCG (same income bracket)
ltcg_rate = 0.15 + 0.038 + 0.093  # CA does not distinguish, still ~28%
ltcg_tax = total_gain * ltcg_rate  # ~$840
ltcg_net = (1000 * 13) - ltcg_tax  # ~$12,160

# Savings by waiting for LTCG
savings = stcg_tax - ltcg_tax  # ~$510 per 1000 shares
```

### Step 3 — Decision matrix

| Scenario | Action |
|---|---|
| Lots all > 1 year old | Sell freely (already LTCG) |
| Lots all < 1 year, market risk high | **Hedge with puts**, don't sell |
| Lots all < 1 year, will hit 1Y in <30d | **Wait** for LTCG, then sell |
| Lots all < 1 year, will hit 1Y in 60+ days | **Hedge with put**, hold to LTCG |
| Mixed lots (some > 1Y, some < 1Y) | **Specific lot ID**: sell long-term lots first |
| Position is huge (>15% portfolio) | Consider gradual sell over multiple tax years |

### Step 4 — Recommend specific lot identification

If broker supports (most do — IBKR, Fidelity, Schwab, Robinhood):
- Use **Specific Lot ID** (not FIFO default)
- Sell highest cost basis first (HIFO) → reduces gain
- OR sell long-term lots first → favorable rate

**Example**:
| Lot # | Date | Shares | Cost | Days held | Gain/share | Tax type |
|---|---|---|---|---|---|---|
| 1 | 2024-09-15 | 5,000 | $5.50 | 600 | $7.64 | LTCG |
| 2 | 2025-03-20 | 8,000 | $8.20 | 410 | $4.94 | LTCG |
| 3 | 2025-09-10 | 5,000 | $11.00 | 240 | $2.14 | STCG |
| 4 | 2026-02-15 | 3,100 | $12.50 | 80 | $0.64 | STCG |

To sell 3,000 shares: **Sell from Lot 1** (LTCG + lowest tax, highest gain $/share but lowest %).

### Step 5 — Alternative: Hedge with Puts (NO TAXABLE EVENT)

If sell triggers high STCG, consider:

**Buy ATM/OTM Put instead of selling:**
- Pros: No taxable event, keep upside
- Cons: Premium cost (typically 2-5% of position value for 3-6mo cover)

**Example for 1,000 shares at $13**:
- Buy ATM Put × 10 contracts (covers 1,000 shares) ~3 months out
- Cost: ~$0.30 × 100 × 10 = $300 (~2.3% of position)
- Protects $13 floor — if stock drops to $11, puts gain $2/share = $2,000
- Net: $300 cost for $2,000 protection
- **No tax event** — keep stock until LTCG window opens

**Cost comparison**:
| Strategy | Tax cost | Hedge cost | Net cost |
|---|---|---|---|
| Sell now (STCG) | ~$1,350 | $0 | -$1,350 |
| Sell after LTCG (wait) | ~$840 | $0 | -$840 |
| **Buy put + hold** | **$0** | $300 | **-$300** |

**Hedge typically wins by $500-1,000+ per 1,000 shares**, KEEPS upside, position intact.

### Step 6 — Tax loss harvesting (bonus alpha)

If user has 浮亏 positions:
- Sell loser to crystallize loss
- Loss offsets capital gains (dollar for dollar, no limit)
- Buy back after **31 days** (avoid wash sale)

**Example**:
- User wants to sell 1,000 NOK with $2,800 gain
- User has 100 GDXU at $154 (cost $166 = $1,200 loss)
- Sell GDXU first: realize -$1,200 loss
- Sell NOK: realize +$2,800 gain
- Net taxable: +$1,600 (vs $2,800)
- Tax savings: $1,200 × 35% = **$420 saved**
- Wait 31 days, can rebuy GDXU if still bullish

## Output format

```markdown
# [TICKER] Tax-Optimized Trim — [Date]

## Inputs
- Ticker: [X], Shares to sell: N
- Avg cost: $X, Current: $Y
- Income bracket: [High/Mid/Low]
- State: [CA/NY/TX/etc]

## Tax Cost Analysis

### Scenario A: Sell Now (assumes STCG)
- Gross proceeds: $XX,XXX
- Total gain: $X,XXX
- STCG tax (X% effective): $X,XXX
- **Net to bank**: $XX,XXX

### Scenario B: Wait for LTCG (sell in [date])
- Gross proceeds: $XX,XXX (assumes price stable)
- LTCG tax (Y% effective): $X,XXX
- **Net to bank**: $XX,XXX
- **Savings vs Now**: $X,XXX

### Scenario C: Hedge with Put (no sale)
- Recommended put: [TICKER] [Date] $X Put × N contracts
- Hedge cost: $XXX
- Tax cost: $0
- **Net cash impact**: -$XXX (vs -$X,XXX in Scenario A)
- **Best if**: Long-term thesis intact, just want short-term protection

## Specific Lot ID Recommendation
| Lot | Buy Date | Days held | Suggested action |
| Lot 1 | YYYY-MM-DD | XXX | Sell first (LTCG, lowest tax) |
| Lot 2 | YYYY-MM-DD | XXX | Sell next |

**Broker instruction**: "Use Specific Lot ID, sell from Lot 1 (settled date YYYY-MM-DD)"

## Tax Loss Harvesting Opportunities
- [If user has loss positions]: Sell [TICKER] to realize -$X loss, offsets gain.

## My Recommendation
[Specific action: which scenario + why + step-by-step orders]
```

## Hard rules

1. **Always ask for buy dates if not provided.** Without dates, can't determine STCG/LTCG.
2. **Never recommend without state context.** CA has no LTCG benefit; FL has no state tax.
3. **Show all 3 scenarios** (sell now / wait / hedge). Let user choose.
4. **NIIT**: Apply if income > $200K single / $250K MFJ.
5. **Wash sale rule**: Cannot rebuy same security 30 days before/after loss sale. Use similar-but-different (NOK → ERIC for example).
6. **Don't recommend "sell" just for tax reasons.** If thesis intact and stock undervalued, hedging is often better.
7. **Specific Lot ID requires broker setup BEFORE the sale.** Tell user to call broker first if unsure.

## Common scenarios

### Scenario 1: All shares held > 1 year (LTCG)
- All long-term capital gain treatment
- Sell freely if you want to trim
- Recommendation: Standard trim, no special tax planning needed beyond LTCG

### Scenario 2: All shares held < 1 year (STCG)
- Example: 1,000 shares at $230 avg cost, now $250 (6 weeks held)
- Sell now: ~35% on $20K gain = $7,000 tax
- Wait 11 months: 18.8% = $3,760 tax
- **Hedge with put** until LTCG: cost ~$2K, save $5,000 net

### Scenario 3: Tax loss harvesting
- Have a winner with $10K LTCG
- Have a loser with $5K loss in unrelated position
- Sell loser to crystallize loss + sell winner for gain
- Net taxable: $5K (vs $10K alone)
- Save $1,000-2,000 in tax (depending on bracket)
- Wait 31 days before rebuying loser (avoid wash sale)

## Tool cheat-sheet

| Need | Tool |
|---|---|
| Current price | `mcp__yfmcp__yfinance_get_ticker_info` |
| Put options for hedge | `mcp__yfmcp__yfinance_get_option_chain` (puts) |
| User's specific positions | Ask user, OR review `review-investment-screenshot` |

## Pro tips

1. **December is for harvesting** — review portfolio for losses to crystallize.
2. **January 1 resets** — short-term holdings cross to long-term throughout year.
3. **Married couples have $94,250 LTCG 0% bracket** (2026) — useful for low-income years.
4. **Roth IRA holds** — no tax on gains. Use for high-turnover ideas.
5. **HSA holds** — same as Roth, plus tax-deductible contribution.
6. **Avoid "constructive sale"** — covered call deep ITM = IRS may treat as sale.

## When to invoke

- User asks: "Should I sell X now or wait for LTCG?"
- User asks: "How much tax will I pay if I sell N shares?"
- User asks: "How can I trim without paying high taxes?"
- After `analyze-stock` recommends trim, BEFORE executing
- Year-end (Dec) tax planning
