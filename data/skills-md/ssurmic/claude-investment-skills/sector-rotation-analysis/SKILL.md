---
name: sector-rotation-analysis
description: Top-down sector heat map across 11 GICS sectors + AI sub-sectors (GPU, ASIC, Memory, Power, Cloud, Network, Materials). Identifies overheated vs undervalued sectors, leader-laggard pairs, rotation signals. Recommends specific trim-from / add-to pairs with named stocks. Triggers in English ("sector rotation", "what sector to add", "which sector is cheap", "am I too tech heavy", "sector heat map") or Chinese ("板块轮动", "该买哪个板块", "板块热力图", "我是不是 tech 太重", "板块对比").
---

# Sector Rotation Analysis — Where Money Is Going

## 🔍 Pre-flight checklist — rotation creates tax + sizing events that need accounting

Rotation = realize gains in one sector, buy in another. Both halves have execution cost. Required checks:

1. **Macro regime first** — trigger `macro-warning`. Regime determines rotation type:
   - 🟢 GREEN: aggressive rotation OK (sell hot to buy cheap)
   - 🟡 YELLOW: defensive rotation only (sell high-beta to buy staples/utilities)
   - 🔴 RED: don't rotate INTO new sectors — rotate TO CASH. Then redeploy at lower prices.
2. **Tax on the trim leg** — every rotation pair has a "sell X" half. Run `tax-optimize` on it. If held < 12 months → STCG ~25-37% federal. Often a rotation that's +5% net pre-tax is breakeven or negative post-tax. **Always state the post-tax expected delta**, not just the pre-tax sector spread.
3. **Sizing per sector after rotation** — ≤ 30% in any single sector (even Tech). Document current sector weights BEFORE recommending. If user is already 40% Tech, don't recommend adding more Tech sub-sector even if signal is green.
4. **Sub-sector concentration within rotation** — "rotate from Tech to Energy" doesn't mean "buy XOM at any price." Each leg needs analyze-stock-level analysis.
5. **3-tier entry on the add leg** — Don't rotate at market. T1 = trigger, T2 = 50DMA, T3 = 200DMA on the destination sector ETF or stock.

**"Look carefully" rule**: sector ETFs hide concentration. XLK is 23% AAPL + 18% NVDA + 9% MSFT — buying XLK on a "Tech rotation" is concentrated, not diversified. Always check top-5 holdings of any sector ETF before recommending it as a rotation vehicle.

See [README's Hard Rules](../README.md#%EF%B8%8F-hard-rules-never-violate) for the full anti-pattern list.

---

## Goal

Help user **rotate from overheated to undervalued sectors** while staying in the broader market. Never just "all-in" on one sector. Every quarter, identify:
1. **Which sectors are overheated?** (>30% above 200DMA, +50% YTD, insider distribution)
2. **Which sectors are undervalued?** (<5% above 200DMA, lagging YTD, insider buying)
3. **Rotation pairs**: trim X to add Y
4. **Sector ETF map** for execution

## The 11 GICS Sectors (always check all)

| Sector | ETF | Leaders 2026 |
|---|---|---|
| Technology | XLK / VGT | NVDA, MSFT, AVGO |
| Communications | XLC | GOOGL, META |
| Consumer Discretionary | XLY | AMZN, TSLA |
| Consumer Staples | XLP | COST, WMT, KO |
| Energy | XLE | XOM, CVX, EQT |
| Financials | XLF | JPM, BRK |
| Healthcare | XLV | LLY, UNH |
| Industrials | XLI | CAT, GE, RTX |
| Materials | XLB | LIN, FCX, NEM |
| Real Estate | XLRE | DLR, EQIX |
| Utilities | XLU | CEG, NEE, AEP |

## AI Sub-sectors (zoom in) + their distinct growth mechanics

Different sub-sectors have **fundamentally different supply/demand dynamics**. Critical for valuation and predictability:

| Sub-sector | Examples | Growth model | Bottleneck | Predictability | Earnings risk |
|---|---|---|---|---|---|
| **AI GPU** | NVDA, AMD | Demand-elastic, pricing power | TSMC capacity (already locked) | 🟢 High | 🟡 Medium (priced in) |
| **AI ASIC** | AVGO, MRVL | Demand-elastic + multi-customer | TSMC packaging (CoWoS) | 🟢 High | 🟡 Medium |
| **AI Memory (HBM)** | MU, SK Hynix | Independent capacity expansion | Own fab investment cycle | 🟢 High | 🟢 Lower (cycle-tied) |
| **AI Storage (HDD)** | WDC, STX | Slow capex, sold-out years out | Existing capacity | 🟢🟢 Highest | 🟢 Low risk |
| **AI Optical Modules** | LITE, COHR, FN, AAOI | **Capacity-bottlenecked by GPU schedule** | NVDA shipments | 🔴 Low | 🔴 High (component shortages) |
| **AI Networking Systems** | ANET, CIEN, JNPR | Mix of system + components | Various | 🟡 Medium | 🟡 Medium |
| **AI Test Equipment** | AMAT, LRCX, KLAC, TER | Lags fab capex by 6-12 months | Customer capex timing | 🟡 Medium | 🔴 High (cycle peaks) |
| **AI OSAT (Packaging)** | AMKR, ASE, SANM | **Capacity-bottlenecked by TSMC** | Advanced packaging | 🔴 Low | 🔴 High |
| **AI Power (Utilities)** | CEG, VST, AEP, ETR | Multi-year PPA buildout | Grid + nuclear permits | 🟢🟢 Highest | 🟢 Very low |
| **AI Power (Gas)** | EQT, ET, WMB, GEV | Long-cycle infrastructure | Pipeline capacity | 🟢 High | 🟢 Low |
| **AI Cloud (Hyperscaler)** | ORCL, MSFT, AMZN | Capex-driven, RPO-visible | Power, then GPU | 🟢 High | 🟡 Medium |
| **AI Cloud (Neocloud)** | CRWV, NBIS, IREN | Single-customer concentration | Customer payment risk | 🔴 Low | 🔴 High |
| **AI Materials** | APD, LIN, MP, FCX | Long-term contract structure | Mining/refining capacity | 🟢 High | 🟢 Low |
| **AI Connectors** | TEL, APH, GLW | Linked to GPU shipments | Various | 🟡 Medium | 🟡 Medium |
| **AI Cooling/Power Infra** | VRT, ETN, NVT, MOD | Equipment cycle | Manufacturing | 🟡 Medium | 🟡 Medium |

### Key insights from this matrix

1. **Same "AI" thesis, very different earnings risk profiles**:
   - Optical modules and OSAT are capacity-bottlenecked → "缺料" is structural, predictable disappointments
   - Memory and HDD have independent capex cycles → can deliver year-on-year visibility
   - Power utilities are slowest but most predictable → no earnings surprises

2. **Where to find "bestpredictability for the price"**:
   - 🟢 Power (CEG/EQT/AEP/ETR) — long-term contracts, low surprise risk
   - 🟢 Memory (MU/WDC) — own capacity, sold out for years
   - 🔴 Optical (LITE/COHR/FN/AAOI) — looks great but earnings keep missing on supply

3. **Earnings sensitivity by sub-sector**:
   - High earnings risk: Optical, OSAT, Test equipment (cycle-peak), Neocloud
   - Low earnings risk: Power utilities, HDD storage, Memory, Materials

4. **Capacity-bottlenecked sub-sectors** systematically disappoint when GPU cycle hits supply ceiling:
   - Even with strong demand, "shipments < demand"
   - Margin compression from input shortages
   - Pattern: beat EPS, miss on operational metrics → stock drops

## The 4-Step Workflow

### Step 1 — Pull sector performance data

For each sector ETF (XLK, XLE, XLU, etc.), pull via `mcp__yfmcp__yfinance_get_ticker_info`:
- Current price
- 50DMA, 200DMA distance
- YTD %, 1Y %
- Trailing/Forward P/E (sector aggregate)

### Step 2 — Compute sector heat map

For each sector, compute:

| Metric | Healthy | Overheated | Crisis |
|---|---|---|---|
| **% above 200DMA** | <15% | 15-30% | >30% |
| **YTD %** | <30% | 30-60% | >60% |
| **Forward P/E** | < historical avg | At historical avg | >120% of historical |
| **Sector breadth** | >65% above 50DMA | 50-65% | <50% |

**Composite score**: sum metrics, output as 🟢/🟡/🔴

### Step 3 — Identify rotation pairs

For each pair where one is overheated and one undervalued:

| Trim (overheated) | Add (undervalued) | Why |
|---|---|---|
| AI Semis (XLK) | AI Power (XLU) | Power = AI's bottleneck, cheaper, less crowded |
| Mag7 | Energy/Materials | Concentration unwinding |
| Tech | Healthcare | Late-cycle rotation |
| Crypto-adjacent | Defensive (Staples) | Risk-off |

### Step 4 — Recommend specific names within rotation

Within target sector, identify best laggards:

**Step 4a**: Within the OVER sector, pick most-overextended names to trim
**Step 4b**: Within the UNDER sector, pick best laggards (use `find-untapped-thesis` style criteria)

## Output format

```markdown
# Sector Rotation Analysis — [Date]

## TL;DR
**Overheated**: [list with status]
**Undervalued**: [list with status]
**Top 3 rotation pairs**: trim X → add Y

## Sector Heat Map (11 GICS)
| Sector | ETF | YTD | 1Y | %200DMA | %50DMA | Status |
| Tech | XLK | XX% | XX% | +XX% | +XX% | 🔴 OVERHEATED |
| Energy | XLE | XX% | XX% | +XX% | +XX% | 🟢 UNDERVALUED |
| ...

## AI Sub-sector Detail
| Sub-sector | YTD | 1Y | Status | Top idea |
| GPU/ASIC | +XX% | +XX% | 🔴 | Trim into strength |
| Power | +XX% | +XX% | 🟢 | Add EQT, AEP |
| Memory | +XX% | +XX% | 🟡 | Selective: MU only |

## Rotation Pairs (Top 3)

### Pair #1: [SECTOR_OVER] → [SECTOR_UNDER]
- **Trim from over**: [list specific stocks with quantities]
- **Add to under**: [list specific stocks with entry levels]
- **Net portfolio change**: [dollar impact, beta change]
- **Why this pair**: [thesis]

### Pair #2 ...
### Pair #3 ...

## Macro Backdrop
[1 paragraph from macro-risk-check, key signals]

## Recommended Actions Today
1. [Specific trim order]
2. [Specific add order]
3. [Hold others]

## Watch list (next 30 days)
- Sectors approaching turning point
- Sectors approaching overheat threshold
```

## Hard rules

1. **Never recommend "rotate everything"** — always paired (trim 5%, add 5%).
2. **Match risk levels.** Don't trim defensive (Staples) to add aggressive (Crypto).
3. **Use ETFs only as proxy for sector.** For specific names, use `find-untapped-thesis` or `analyze-stock`.
4. **Sector heat is NOT predictive of next quarter** — it's predictive of mean reversion over 6-12 months.
5. **Don't fight macro.** If macro is RED, "rotate" might mean "rotate to cash + bonds."

## Common patterns (2024-2026 examples)

### Pattern A: Tech overheats → Defensive rotation
- 2021/Q4: Tech XLK +30% → Healthcare XLV started outperforming
- Outcome: 2022 Tech -33%, Healthcare -2%
- Lesson: Watch when only one sector is up

### Pattern B: Energy undervalued → Catalyst-driven rally
- 2020/Q3: Energy XLE down -50% → 2021/Q4 Russia + recovery
- Outcome: XLE +60% in 2022 vs SPX -19%
- Lesson: Cycle bottoms have biggest re-rating

### Pattern C: AI mega-cap → AI infrastructure
- 2025-2026: NVDA +500% → power/utilities catch up
- Now: CEG, VST, EQT outperform NVDA in next 6mo
- Lesson: After mega-runs, the supply chain catches up

### Pattern D: K-shape divergence (winner-take-all within sectors)
- Within Tech: NVDA wins, software/SaaS lose
- Within Industrials: Defense wins, traditional loses
- Lesson: Sector ≠ Stock; pick winners within winning sector

## When to invoke

- User asks: "What sector should I rotate to"
- User asks: "Where's the next move"
- User asks: "Am I too tech-heavy"
- Quarterly review (mandatory)
- After 1 sector hits +25% in a month

## Companion skills

- Run `macro-risk-check` first for regime context
- Run `find-untapped-thesis` after picking target sector (for specific names)
- Run `portfolio-audit` to see actual current sector mix
- Run `analyze-stock` for deep dive on top picks

## Tool cheat-sheet

| Need | Tool |
|---|---|
| Sector ETF data | `mcp__yfmcp__yfinance_get_ticker_info` (XLK, XLE, etc.) |
| Sector P/E | `WebSearch`: "[sector] P/E ratio current vs historical" |
| Sub-sector ETFs | SMH (semi), XBI (biotech), KRE (banks), ITA (defense) |
| Internal breadth | `WebSearch`: "% [sector] stocks above 200DMA" |
| Historical heatmap | `WebSearch`: "S&P 500 sector returns YTD" |

## Sector "Cheat Sheet" — Quick reference

### When VIX > 25:
- Trim: XLK, XLY, XLC (high beta)
- Add: XLU, XLP, XLV (defensive)

### When 30Y > 5%:
- Trim: REITs (XLRE), Utilities (XLU sometimes)
- Add: Banks (XLF), Energy (XLE)

### When USD/JPY < 153 (yen carry unwind):
- Trim: All semis (heavy Japanese ownership)
- Add: Domestic-only (XLP, XLV)

### When OPEC + 1973 risk:
- Trim: Growth, Tech, EVs
- Add: Energy (XLE), Materials (XLB), Defense (ITA)

### When Trump-Xi summit positive:
- Trim: Defensive
- Add: China-exposed (BABA, JD), AI semis (NVDA China upside)
