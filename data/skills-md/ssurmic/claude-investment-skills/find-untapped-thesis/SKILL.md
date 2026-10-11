---
name: find-untapped-thesis
description: Screens for "未爆发 / undiscovered" stocks within a theme — low Forward P/E, lagging 1Y returns vs leaders, real catalyst (concrete contracts not just narrative), low institutional ownership room for re-rating. Returns top 3 candidates with entry plan. Triggers in English ("find undervalued in X", "find next big winner in Y", "what's underrated in Z", "screen for theme X", "show me cheap names in Y") or Chinese ("找未爆发的 X 股", "X 板块还有什么便宜的", "未涨过的 Y", "下一个 NOK", "X 主题筛选").
---

# Find Untapped Thesis — NOK-Style 未爆发 Hunting

## Goal

Find stocks that meet ALL of these criteria:
1. **未涨过头**: 1Y return < 50% (vs sector that's +100%+)
2. **估值便宜**: Forward P/E < 25 OR PEG < 1.2
3. **真 catalyst**: Concrete contracts, financials confirm thesis (not just narrative)
4. **机构未挤进**: Institutional ownership <30% (room for re-rating)
5. **Insider 不在大量卖**: Use insider_ratio.py to filter out distribution

The classic pattern that captures multi-bagger reversal: low PE + low attention + new narrative tailwind + low institutional ownership + insider conviction.

## Why this matters

**Crowded names = limited upside** (NVDA, AVGO, AMD already +100%+ YTD).
**Untapped names = asymmetric R/R** because:
- Estimates can still be revised up
- Multiple expansion possible (PE 12 → 25 = +108%)
- Institutional buying creates flow tailwind
- Less covered by analysts = slower price discovery

## The 6-Step Workflow

### Step 1 — Define theme (user asks or you suggest)

Common themes for 2026:
- **AI Data Center power** (electricity, gas, nuclear) — EQT, AEP, ETR
- **AI infrastructure 2nd derivative** (cooling, busbar) — NVT, MOD, ENS
- **Memory recovery** (HBM, HDD) — MU, WDC
- **Industrial gases for fabs** — APD, LIN
- **Copper for AI buildout** — HBM, FCX, TECK
- **Optical networking 2.0** — TEL, FN, CIEN
- **EU defense / aerospace aluminum** — CSTM
- **Quantum computing** (longer-term) — IONQ, RGTI, QBTS
- **Robotics / industrial automation** — ROK, EMR

### Step 2 — Build candidate list

For each theme, generate 10-15 candidates via:
- Sector ETFs (XLE, XLU, XLB, SMH, XLK)
- WebSearch: "[theme] stocks 2026", "small cap [theme]"
- News: "[theme] suppliers", "[theme] picks-and-shovels"

### Step 3 — Apply hard filters (parallel pull data)

For each candidate, pull via `mcp__yfmcp__yfinance_get_ticker_info`:

**Hard cuts (must pass ALL):**
| Filter | Threshold |
|---|---|
| Market cap | > $500M (avoid micro-cap) |
| Forward P/E | < 25 (or PEG < 1.2 for higher growth) |
| 1Y return | < 50% (laggard) |
| 200DMA gap | < +30% (not parabolic) |
| Volume | Avg > 100K daily (liquidity) |

**Bonus filter — favor predictable growth models** (see `sector-rotation-analysis` for sub-sector mechanics):
- 🟢 Prefer: Memory, Storage, Power utilities, Materials, SaaS (independent capacity / long-cycle)
- 🔴 Discount: Optical modules, OSAT, Neocloud (capacity-bottlenecked / single-customer risk)
- A 1Y-laggard in a high-predictability sub-sector beats a 1Y-laggard in a structurally constrained one

**Soft preferences:**
- Institutional ownership < 30%
- Analyst coverage < 15 (less crowded)
- Recent earnings beat
- Dividend yield > 1% (signal of cash gen)

### Step 4 — Insider check (mandatory)

For each surviving candidate, run with **--window 90** (recent activity only):
```bash
uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/insider_ratio.py 2>/dev/null | head -1) "TICKER1,TICKER2,..." --window 90
```

The script uses openinsider.com as primary source (Form 4 codes; only `P` = real purchase counts). For high-stakes calls, use `--source both` to cross-verify against yfinance.

**Reject if (RECENT 0-90d):**
- Buy/sell ratio < 0.1 (heavy distribution, NOT 10b5-1)
- 0 buys, 5+ ad-hoc sells from execs (verify codes are S, not F/A/M)
- CEO/CFO ad-hoc selling within 30 days

**Boost if (RECENT 0-90d):**
- 3+ unique insider open-market buys = "RECENT CLUSTER BUY ✅✅✅" (the MRVL/CEVA/NKE pattern)
- CEO/Founder/Chairman recent buy ($100K+, code "P")
- 0 ad-hoc sells AND any insider buy at all
- Buys clustered within 7 days

**Don't punish:**
- Old sells from "trusts" (THE EEC TRUST etc.) → 10b5-1 scheduled, not new info
- Tax withholding "F" code → mechanical
- RSU/DSU "A" code → compensation, not signal

### Step 5 — Concrete catalyst verification

For each remaining candidate, WebSearch for:
- Last earnings: did revenue/EPS beat?
- Specific contracts: company name, $ amount, duration
- Partner announcements (NVIDIA, Microsoft, Meta, AWS, etc.)
- Capacity expansion / new fabs / facility openings
- Recent guidance raise

**Reject if no concrete evidence**, just narrative.

### Step 6 — Rank by composite score

For each surviving candidate:

| Factor | Weight | Score |
|---|---|---|
| Forward P/E lower (vs theme median) | 20% | 0-10 |
| 1Y laggard vs theme leaders | 15% | 0-10 |
| Insider signal | 15% | 0-10 |
| Concrete catalyst strength | 20% | 0-10 |
| Institutional room | 10% | 0-10 |
| **Predictability of growth model** | **20%** | 0-10 (see sub-sector matrix) |

**Predictability scoring**:
- 10: Long-cycle infra (utilities, materials with multi-year backlog)
- 8: Independent capacity (memory, storage)
- 6: Demand-elastic with pricing power (GPU/ASIC)
- 4: Cyclical commodity
- 2: Capacity-bottlenecked downstream (optical modules, OSAT)
- 0: Single-customer concentration (some neoclouds)

**Top 5 = recommend with entry plan + risk assessment.**

## Output format

```markdown
# Untapped Thesis Screen: [Theme] — [Date]

## TL;DR
Found [N] candidates passing all filters. Top 3 recommendations:
1. [TICKER1] — [reason in 10 words]
2. [TICKER2] — [reason]
3. [TICKER3] — [reason]

## Theme Context
[Why this theme matters in 2026, what's the upside catalyst]

## Theme leaders (already up, for reference NOT to buy)
| Ticker | Price | YTD% | 1Y% | Forward P/E |

## Theme laggards (CANDIDATES)
| Ticker | Price | YTD% | 1Y% | Forward P/E | PEG | Inst% | Insider | Catalyst | Score |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | X/10 |

## Top 3 Deep Dive

### #1 [TICKER] — [tagline]
- **Why undervalued**: [concrete evidence — PE, peers, what's missed]
- **Catalyst (with date if known)**: [contracts, earnings, M&A]
- **Insider**: [ratio + key buyers]
- **Entry plan (3-tier)**:
  - Now: $X (try 30%)
  - 50DMA: $Y (add 30%)
  - 200DMA: $Z (add 40%)
- **12-month target**: $A (+B%)
- **Risk**: [main risks]
- **LEAPS suggestion**: [if applicable]

### #2 ...
### #3 ...

## Rejected (and why)
| Ticker | Why rejected |
| TICKER1 | Insider 1:50 distribution |
| TICKER2 | 1Y +180%, no longer laggard |
| TICKER3 | No concrete catalyst, just narrative |
```

## Hard rules

1. **Filter before deep-diving.** Don't waste 15min analyzing a stock that's already up 200%.
2. **Insider check is mandatory.** No insider data = skip.
3. **Concrete catalyst > narrative.** "AI" is not a catalyst. "Microsoft signed $19.4B deal on 9/22/2025" is.
4. **Show the rejected list.** Transparency. Show 5-10 rejected so user knows you screened broadly.
5. **Don't recommend market cap < $500M unless explicitly asked.** Liquidity issues.
6. **Cap "未爆发" claim:** if 1Y > 100%, it's not 未爆发 anymore. EQT (1Y +10%) qualifies; CSTM (1Y +189%) does not.

## Theme template (illustrative — verify with live data each time)

When screening a theme, organize results like this. Live data will populate specifics:

### Theme Template
| Ticker | Status | Why |
|---|---|---|
| **[Top pick]** | ⭐ Top | Lowest PE + concrete contract + insider clean |
| [Solid pick] | Solid | OK metrics, growing thesis |
| [Wait] | Wait | Good thesis but needs pullback or insider issue |
| [Hidden gem] | Hidden | Off-radar but unique angle (insider buy, special structure) |

**Always run live screening** — themes evolve quarterly. Past laggards become leaders, leaders become laggards. Use `mcp__yfmcp__yfinance_get_ticker_info` for current data.

## When to invoke

- User asks: "Find me the next NOK"
- User asks: "What undervalued [theme] stocks are there?"
- User asks: "What's 未爆发?"
- User asks: "Show me 落后 stocks in [theme]"
- Auto: weekly Monday scan (via schedule skill)

## Companion skill

After this skill identifies top 3, run `analyze-stock` on each for the deep dive (10-step framework). This skill is the **funnel**, analyze-stock is the **deep dive**.
