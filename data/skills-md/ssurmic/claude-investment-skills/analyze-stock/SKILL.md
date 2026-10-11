---
name: analyze-stock
description: Top-down deep dive analysis on a US-listed stock with macro context, valuation audit, insider check, catalysts, and 3-tier entry plan with LEAPS option. Pulls live data via yfmcp. Triggers in English ("analyze X", "is X a buy", "deep dive on X", "should I buy X", "what about X stock", "research X") or Chinese ("分析 X", "X 怎么样", "X 能买吗", "深度看一下 X", "调研 X", "X 这只股票").
---

# Analyze Stock — 10-Step Top-Down Master Framework

The job: deliver a fund-manager-grade analysis that connects **macro context → year theme → sector position → individual thesis → entry plan**. Every claim has concrete evidence. Every recommendation has size + reason.

## Prime Directive

Never analyze a stock in isolation. **A great stock in a bad macro window is still a sell.** Always start with macro, end with sizing.

## The 10 Steps (run in order)

### Step 1 — Macro backdrop & event calendar (NEW: MANDATORY)
Before touching the stock, ask:
- **What's the regime today?** (risk-on melt-up / chop / late-cycle / risk-off / bear)
- **What macro events in the next 30 days could move this stock?**
  - Fed meetings, FOMC minutes, CPI, NFP
  - **Trade summits** (Trump-Xi 5/14-15, G20)
  - **BOJ meetings** (carry trade trigger)
  - **OPEC** (oil/inflation)
  - **Major regulatory** (FTC, SEC, China MOFCOM)
  - **Geopolitical hotspots** (Taiwan, Iran/Hormuz, Russia)

**Tools:**
- `WebSearch`: "[stock] macro impact [next event]" e.g., "NVDA Trump-Xi summit impact"
- `WebSearch`: "Fed meeting [next month]", "BOJ meeting [next month]"

**Output**: 1 paragraph naming the regime + 3 bullet macro events that affect THIS stock.

### Step 2 — Year theme alignment
Identify which **annual narrative** this stock fits. Common 2026 themes:
- **K-shape divergence** (winners up, losers crushed within sectors)
- **AI = factory/capex mode** (hyperscalers buy compute like factories buy machines)
- **Power as AI bottleneck** (nuclear/gas/utilities revaluation)
- **Late-cycle demand destruction risk** (oil/inflation pressure)
- **Yen carry trade unwind risk** (BOJ rate hikes triggering JPY borrowing reversal)

**Question**: Does this stock benefit from this year's theme, or fight it?

### Step 3 — Sector position + Industry chain mechanics

**Step 3a: Sector classification**
- Which sector? (Use yfmcp `get_ticker_info` → `sector`)
- Sector status: **过热 / 合理 / 未爆发 / 熊市**
- Within sector, is this **龙头 / 二线 / 笨马**?
- Sector ETF distance from 50DMA / 200DMA (overheated check)

**Step 3b: Industry chain position (CRITICAL — different sub-sectors have different growth mechanics)**

Identify which growth model this stock fits:

| Growth Model | Mechanics | Examples | Predictability |
|---|---|---|---|
| **Capacity-bottlenecked downstream** | Cannot grow faster than upstream allows | Optical modules tied to NVDA GPU schedule, OSAT tied to TSMC | 🔴 Low — "缺料"是常态 |
| **Independent capacity expansion** | Owns fabs, can scale on own timeline | Memory (MU/WDC), SiC fabs (WOLF), some semis | 🟢 High — capex visibility |
| **Demand-elastic with structural growth** | Demand >> supply, can raise price | NVIDIA GPUs, AI ASICs (AVGO/MRVL), ARM IP | 🟢 High — pricing power |
| **Cyclical commodity** | Boom-bust by macro | Memory DRAM/NAND cycle, copper, oil | 🟡 Medium — cycle visibility |
| **Long-cycle infrastructure** | Multi-year buildout, slow but visible | Power utilities, gas pipelines, data center REIT | 🟢 High — backlog-driven |
| **Service/SaaS recurring** | ARR-based, low capex sensitivity | Oracle DB, Cisco software, EDA (CDNS/SNPS) | 🟢 Highest — recurring rev |

**Identify bottleneck specifically**:
- What limits this stock's growth? (component shortage / fab capacity / customer demand / regulation)
- Is the bottleneck upstream or downstream of this stock?
- Does this stock have pricing power against the bottleneck?

**Critical insight**: A "great thesis" stock with the wrong growth model is still wrong. Example:
- Optical modules ride AI capex BUT are capacity-bottlenecked by GPU schedules
- Memory rides AI capex AND can expand independently
- Same upside narrative, very different earnings trajectory

**Tools:**
- `mcp__yfmcp__yfinance_get_ticker_info` for sector
- `WebSearch`: "[sector] supply chain bottleneck", "[ticker] capacity expansion", "[ticker] supply constraints"

### Step 4 — Price snapshot + technicals
Pull live data via `mcp__yfmcp__yfinance_get_ticker_info`:
- Current price, day range, 52W range, ATH/ATL
- 50DMA, 200DMA — **calculate % distance from each**
- 6mo, 1Y change
- Beta, average volume

**Red flags:**
- 现价 +30%+ above 50DMA = 抛物线
- 现价 +50%+ above 200DMA = 极端透支
- 1Y >+200% = 概率回调

### Step 5 — Full valuation audit + sub-sector value ranking

Compute via yfmcp:
- **Forward P/E** (most important)
- **PEG** (Forward P/E / EPS growth %)
- **P/S, P/B**
- **EV/EBITDA, EV/Revenue**
- **OPM, Net margin, ROE, ROA**
- **FCF (TTM), Operating CF, Total Debt, Cash**
- **D/E ratio**

**Compare to 2-3 peers** (same sub-sector, similar size). Use WebSearch if unclear who peers are.

**Output table** with cost-benefit ranking:
| Metric | This Stock | Peer 1 | Peer 2 | Peer 3 | Verdict |
| Forward P/E | X | Y | Z | W | Cheapest / Mid / Most expensive |
| PEG | X | Y | Z | W | |
| 1Y % | X | Y | Z | W | Most laggard / leader |
| Distance from ATH | X | Y | Z | W | |
| Capacity model | (from Step 3b) | | | | |

**Rank within sub-sector**:
- 🟢 **Best value**: Cheapest PE/PEG + clean capacity model + lagging price
- 🟡 **Fair value**: Middle of pack
- 🔴 **Stretched**: Most expensive in sub-sector at ATH

**Sub-sector cost-benefit examples** (showing why peer ranking matters):
- *Memory*: MU PE 5.3 vs WDC PE 24.8 — both AI memory but very different value
- *Optical*: COHR PE 43 vs LITE PE 59 — same sub-sector, COHR cheaper
- *AI Power*: EQT PE 12.6 vs AEP PE 19.9 vs ETR PE 23.3 — tier by valuation
- *Hyperscaler*: ORCL PE 21 vs MSFT PE 33 — similar AI thesis, different valuations

### Step 6 — Concrete catalysts (last 30 days + next 30 days)
**Past 30 days**:
- Last earnings results (beat/miss, guidance)
- New contracts/customer wins
- Analyst upgrades/downgrades with specific targets
- M&A activity

**Next 30 days**:
- Earnings date + implied move from straddle
- Conferences (e.g., Computex, GTC, Investor Day)
- Product launches
- Macro events from Step 1

**Tools:**
- `WebSearch`: "[ticker] earnings [last quarter]"
- `WebSearch`: "[ticker] news [current month]"
- `WebSearch`: "[ticker] analyst price target [current month]"

### Step 7 — Insider trading (MANDATORY — use insider_ratio.py v3, openinsider primary)
**Never trust yfinance "Net Shares Purchased" headline — it counts RSU as buys.** Form 4 code "P" is the only real-buy signal; A/M/F/G are compensation flows. Verify any "cluster buy" claim at openinsider.com/[TICKER] — news routinely mislabels DSU/RSU grants as cluster buys.

Run (uses openinsider as primary source, 90-day default window, code-aware):
```bash
uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/insider_ratio.py 2>/dev/null | head -1) "TICKER" --window 90
```
For high-stakes calls add `--source both` to cross-verify against yfinance.

**Verdict ladder:**
| Buy/Sell ratio | Verdict |
|---|---|
| Buy ≥ 2× Sell | 🟢 STRONG BUY |
| Buy ≥ Sell | 🟡 Mild buy |
| Buy 0.1×-1× Sell | 🟡 Mixed |
| Buy < 10% Sell | 🔴 DISTRIBUTION |
| Buy = 0, Sell > 0 | 🔴 INSIDERS ONLY SELLING |

**Always report seniority**: CEO > CFO > Director > Officer. CEO buying $1M >> 5 directors selling $5M.

### Step 8 — Risk dissection (bear/base/bull)
For each, give **specific price target** + **assumption**:

| Scenario | Probability | 12mo target | Trigger |
|---|---|---|---|
| 🟢 Bull | X% | $Y | What needs to happen |
| 🟡 Base | X% | $Y | What needs to happen |
| 🔴 Bear | X% | $Y | What needs to happen |
| 💀 Black swan | X% | $Y | E.g., yen carry, war |

**Calculate weighted average price** = Σ(probability × target).

### Step 9 — Entry plan (3 tiers)
| 价位 | 性质 | 仓位 % |
|---|---|---|
| 现价 | 试仓 | 30% |
| 50DMA | 健康回调 | 30% |
| 200DMA | 库重 | 40% |

**Position size cap**: any single stock max **8-10% of portfolio**, max **5%** for high beta/parabolic names.

### Step 10 — LEAPS recommendation (if applicable)
For each stock, also check:
- `mcp__yfmcp__yfinance_get_option_dates`
- For 2027/1 and 2028/1 expiries: pull option chain
- Filter: **OI > 1000, IV < 80%, ATM to +20% OTM**

Recommend 1-2 strikes with:
- Mid price
- Breakeven
- 2x scenario
- Max loss (premium)

**LEAPS over stock when**: high conviction + want leverage + IV reasonable.
**Stock over LEAPS when**: dividend yield matters + tax efficiency + uncertain timeline.

## Output format

```markdown
# [TICKER] Deep Dive — [Date]

## TL;DR (Verdict)
[One paragraph: action + size + reason]

## Step 1 — Macro Context
- Regime: [tag]
- Macro events 30d: [list with dates]

## Step 2 — Year Theme Fit
[Which 2026 narrative? Yes/No fit?]

## Step 3 — Sector Position
[Sector / leader-laggard / overheated?]

## Step 4 — Price + Technicals
| Metric | Value | Signal |

## Step 5 — Valuation
[Table vs peers]

## Step 6 — Catalysts
- Past 30d: [list]
- Next 30d: [list with dates]

## Step 7 — Insider
[Run insider_ratio.py output + verdict]

## Step 8 — Scenarios
[Bear/base/bull table]

## Step 9 — Entry Plan
[3-tier table with $ and %]

## Step 10 — LEAPS
[Recommended strikes + R/R]

## What I'd do today
[Specific action: buy X shares at $Y / wait for Z / hedge with W]
```

## Hard rules

1. **Always start with macro.** A perfectly priced stock in a bad regime is still wrong.
2. **Never skip insider check.** Use insider_ratio.py — yfinance summary is RSU-polluted.
3. **Concrete evidence over narrative.** "AI is good" ≠ thesis. "Microsoft signed $19.4B 5-year contract on 9/22/2025" = thesis.
4. **Position size has a CAP.** No single stock >10%, no high-beta name >5%.
5. **3-tier entry mandatory.** No "buy at market" recommendations.
6. **If insider distribution + parabolic price → 🔴 even if business is great.** ADI/TER pattern.
7. **Report what's NOT priced in.** ORCL pattern: China=0 in NVDA case = pure upside.
8. **Always check 30-day macro events.** Trump-Xi, BOJ, FOMC, OPEC.

## Common patterns to recognize

| Pattern | Example | Signal |
|---|---|---|
| 已涨爆 + 内部人卖 + 距 ATH < 5% | ADI, TER, AVGO 4/2026 | 🔴 顶部分发 |
| 估值便宜 + 大跌 -50% + 反转早期 | ORCL 5/2026, NOK 2024 | 🟢 narrative reversal |
| 1Y 落后 + PE 低 + 真 thesis | EQT, AEP, HBM 2026 | 🟢 未爆发 |
| 业绩好 + 但指引平 | TER 4/2026, AMD 2/2026 | 🔴 priced in，跌 |
| Insider 集中买 (3+ 高管 1 周内) | CEVA 2026, COHR 2024 | 🟢 STRONG BUY signal |
| 高 beta + 客户集中 | APLD (CRWV 60%) | 🔴 单点失败风险 |

## When user asks "is X a buy?"

Run all 10 steps. Don't shortcut. The user is asking for a full analysis, not an opinion.

## Tool cheat-sheet

| Need | Tool |
|---|---|
| Live price + valuation | `mcp__yfmcp__yfinance_get_ticker_info` |
| Historical prices | `mcp__yfmcp__yfinance_get_price_history` |
| Option chain | `mcp__yfmcp__yfinance_get_option_chain` |
| News | `mcp__yfmcp__yfinance_get_ticker_news` + `WebSearch` |
| Insider | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/insider_ratio.py 2>/dev/null | head -1)` |
| Max pain | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/max_pain.py 2>/dev/null | head -1)` |
| Option walls | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/option_walls.py 2>/dev/null | head -1)` |
| Macro events | `WebSearch` |
