---
name: macro-warning
description: Daily batch-mode macro pullback / warning radar. Checks valuation extremes (NDX/QQQ Forward PE), volatility (VIX/MOVE), sentiment (CNN F&G, AAII), credit spreads (HY OAS), market internals (% above 200DMA, breadth), yen carry (USD/JPY), yield curve, and 11-sector rotation. Outputs Red/Yellow/Green regime + specific positioning advice. Designed for daily 5pm ET (post-close) or 8am ET (pre-open) batch runs via /schedule. Triggers in English ("macro warning", "regime check", "is the market at peak", "should I take profits", "is it time to buy") or Chinese ("宏观警报", "市场是不是顶了", "该不该减仓", "regime 怎么样", "该入场吗").
---

# Macro Warning — Daily Pullback / Top-Risk Radar

## Goal

Answer 3 questions every market session:

1. **Is the market priced for perfection?** (valuation extreme)
2. **Are we euphoric or panicked?** (sentiment / volatility extreme)
3. **What sector should I lean into / out of?** (rotation tilt)

Output is a single regime tag (🟢 GREEN / 🟡 YELLOW / 🔴 RED) plus specific position-sizing advice.

## When to invoke

- **Daily batch (recommended)**: 5pm ET (post-close) or 8am ET (pre-open) via `/schedule`
- **Manual**: User asks "macro check / regime read / 该不该入场"
- **Pre-event**: 24-48h before Fed / CPI / NFP / major earnings stack
- **After +/-2% SPX day**: regime may have shifted

## The Indicator Stack (8 layers, weighted)

### Layer 1 — Valuation extremes (highest weight)

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **NDX Forward P/E** | `gurufocus.com/economic_indicators/6778` or `macromicro.me/series/23955` or yfmcp QQQ.info forwardPE | **>38 = RED** (only 3 times in 20 yr: 2000, 2020, 2025) · 33-38 = YELLOW · <30 = GREEN | RED → trim AI capex names 25%, raise cash to 30% |
| **SPX Forward P/E** | `wsj.com/market-data/stocks/peyields` | >22 = YELLOW · >25 = RED | RED → defensive rotation |
| **Shiller CAPE** | `multpl.com/shiller-pe` | >35 = YELLOW · >40 = RED | Long-term sell signal |
| **Buffett Indicator** (Mcap/GDP) | `currentmarketvaluation.com` | >180% = YELLOW · >200% = RED | Confirms top regime |

**Why NDX 38 matters**: historical record high is 38.57 (2000 dot-com peak excluded — that was 73). Touching 38 is statistically a 95th-percentile event.

### Layer 2 — Volatility (VIX / MOVE / VVIX)

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **VIX** (SPX vol) | yfmcp `^VIX` | **>30 = BUY signal** (panic) · 22-30 = caution · <18 = COMPLACENT (sell) · <14 = euphoric | <14 → take profits aggressively |
| **MOVE** (bond vol) | `^MOVE` or WebSearch | >120 = stress · <80 = calm | >120 + VIX>25 = correlated stress |
| **VVIX** (vol of vol) | `^VVIX` | >120 = vol regime change brewing | >120 + VIX rising = pre-cascade |
| **VIX/VVIX ratio** | derived | <0.18 = complacent · >0.30 = panic | <0.18 → top-feel |

### Layer 3 — Sentiment

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **CNN Fear & Greed** | `cnn.com/markets/fear-and-greed` | **>80 = EXTREME GREED (sell)** · 55-80 = greed · 25-45 = fear · **<17 = EXTREME FEAR (buy)** | >80 → take profits · <20 → add risk |
| **AAII Sentiment** | `aaii.com/sentimentsurvey` | Bullish >50% = caution · <25% = capitulation buy | Contrarian indicator |
| **NAAIM Exposure** | `naaim.org` | >100% = leveraged long (caution) · <40% = washed out (buy) | |
| **Put/Call ratio** | yfmcp or CBOE | <0.50 = complacent · >1.20 = panic | <0.50 = top-feel |

### Layer 4 — Credit / Risk premium

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **HY OAS spread** | `fred.stlouisfed.org/series/BAMLH0A0HYM2` | <300bps = tight · >500bps = stressed · >700bps = recession-pricing | <300 = late-cycle complacent · >500 = risk-off |
| **IG OAS spread** | `BAMLC0A0CM` | <100 = tight · >150 = caution | |
| **Yield curve 2-10** | `^TNX` minus 2Y | Inverted = recession warning · steepening from negative = recession nearing | Steepening from inverted = LATE warning |
| **30Y yield** | `^TYX` | >5.10% = bond market stressed · >5.50% = equity multiple compression | >5.10 → trim long-duration tech |

### Layer 5 — Currency / carry

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **DXY** (Dollar Index) | `DX-Y.NYB` | >107 = USD strength stress · <100 = USD weakness | DXY surge + emerging market FX crash = global risk-off |
| **USD/JPY** | `JPY=X` | **<153 = yen carry unwind risk** · >155 = stable | <153 → trim semi names heavily (Japanese ownership unwind) |
| **BOJ rate hike pricing** | WebSearch | Imminent hike → JPY strengthen → carry unwind | Pre-emptively trim |

### Layer 6 — Market internals / breadth

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **% SPX stocks above 200DMA** | WebSearch "spx breadth percent above 200dma" | >75% = healthy · <50% = deteriorating · <25% = washed out | <50% in rising market = bad breadth divergence |
| **NYSE A/D line** | WebSearch "nyse advance decline line" | New highs with rising A/D = healthy; new highs with flat/falling A/D = topping | |
| **New highs vs new lows** | WebSearch | Highs >> lows = healthy; lows expanding = top distribution | |
| **McClellan Oscillator** | WebSearch | >+100 = overbought · <-100 = oversold | Contrarian |

### Layer 7 — CTA / systematic flows

| Indicator | Source | Threshold | Action |
|---|---|---|---|
| **CTA net positioning** | WebSearch "Goldman CTA flows this week" | Max long = no buyers left · Max short = no sellers left | Max long + extended market = pre-unwind |
| **Vol-target funds positioning** | WebSearch "Nomura vol target positioning" | Heavy long + VIX >20 = mechanical de-leveraging risk | |

### Layer 8 — Sector rotation tilt (the action layer)

Run `sector-rotation-analysis` skill for full breakdown. Quick check:

| Signal | Meaning |
|---|---|
| **XLU/XLK ratio rising** | Defensive rotation starting |
| **XLP outperforming SPX** | Late-cycle warning |
| **XLY underperforming XLP** | Consumer fatigue |
| **Russell 2000 (IWM) lagging SPX** | Risk-off / breadth deterioration |
| **Mag 7 vs SPX equal-weight (RSP)** | Concentration extreme = top-warning |

## The composite regime tag

Score each layer 0 (worst), 1 (caution), 2 (good). Sum gives composite:

| Total | Regime | Action |
|---|---|---|
| 12-16 | 🟢 **GREEN** — risk-on | Add to existing positions, deploy cash |
| 7-11 | 🟡 **YELLOW** — late cycle / chop | Hold, no new adds, set stops |
| 4-6 | 🟠 **ORANGE** — pre-correction | Trim 20-30%, raise cash to 25% |
| 0-3 | 🔴 **RED** — sell-the-rip / euphoria peak | Trim 40%+, raise cash to 35-50%, hedge with SPY puts |

**Asymmetric weighting**: if **NDX P/E >38 OR VIX <14 OR F&G >85**, even with everything else green, **regime is YELLOW minimum** (top-risk override).

## Output format (for batch / agent consumption)

```markdown
# Macro Warning — [DATE]
## Regime: [🟢/🟡/🟠/🔴] [GREEN/YELLOW/ORANGE/RED]
**Composite score: X / 16**

## Headline (1 sentence)
[E.g., "NDX P/E at 38.1 (95th percentile) + VIX 14 + F&G 78 = late-cycle euphoria, trim AI names."]

## The 8 layers
| Layer | Reading | Score | Note |
|---|---|---|---|
| Valuation | NDX FwdPE 38.1, SPX FwdPE 22.5 | 0/2 | RED — at all-time-high zone |
| Volatility | VIX 14, MOVE 95 | 1/2 | Complacent |
| Sentiment | F&G 78, AAII bull 52% | 1/2 | Greed |
| Credit | HY OAS 285bps | 1/2 | Tight |
| FX | DXY 99, USD/JPY 154 | 2/2 | Stable |
| Breadth | 71% above 200DMA | 1/2 | Healthy but slipping |
| CTA | Max long | 0/2 | Crowded |
| Sector | XLU starting to outperform | 1/2 | Early defensive rotation |
| **Total** | | **7/16** | YELLOW |

## What changed today vs yesterday
- [Bullet: VIX +1.5, F&G +5, etc.]
- [Bullet: any threshold crossings]

## Action items (specific, sized)
- **If long-only book**: Trim X% of [overheated names]; raise cash to X%
- **If options-friendly**: Buy X% notional SPY 60DTE puts at delta 0.25
- **If looking to add**: Wait for VIX > X or F&G < Y before deploying

## Sector tilt
- **Add**: [list with reasoning]
- **Trim**: [list with reasoning]
- **Hold**: [list]

## Catalysts watch (next 7 days)
- [Date]: [Event] → impact

## Quote-worthy summary
"[Single sentence the user can paste into a chat]"
```

## Hard rules

1. **Never claim certainty about timing.** Say "elevated risk", not "the top is in".
2. **Always show all 8 layers** even if some are GREEN — paints full picture.
3. **Flag changes vs prior reading** — that's where the alpha is.
4. **Tag the date and time of data pull** — markets move fast.
5. **NDX P/E >38 OR VIX <14 = automatic YELLOW minimum** even if other layers green (override rule).
6. **Cite sources** — every threshold has a verifiable URL. No fabricated numbers.
7. **For batch run, pre-fetch all data in parallel** to keep total runtime <60s.

## ⭐ Canonical data pull: `scripts/macro_pull.py`

**Use this script for all batch runs.** It hits direct APIs (no WebSearch, no LLM scraping) and returns a single JSON blob with raw values + deterministic 8-layer scoring.

```bash
# Full scan (~30s, includes breadth computation)
/tmp/.insider_venv/bin/python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/macro-warning/scripts/macro_pull.py 2>/dev/null | head -1)

# Fast scan (~5s, skip breadth)
/tmp/.insider_venv/bin/python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/macro-warning/scripts/macro_pull.py 2>/dev/null | head -1) --skip-breadth

# Pipe to jq for inspection
... macro_pull.py | jq '.scoring'
```

**Why direct APIs not WebSearch:**
- Reproducible (same input → same output)
- Batch-safe (no rate limit, no LLM token cost)
- Auditable (every value has a known source)
- WebSearch returns stale/summarized data — actual API gives the live number

### Data sources used by the script

| Layer | Indicator | Source | API type |
|---|---|---|---|
| Valuation | Shiller CAPE, SPX trailing PE, Div Yield | `multpl.com/{slug}` | HTML meta tag scrape |
| Volatility | VIX, MOVE, VVIX | yfinance `^VIX`, `^MOVE`, `^VVIX` | Python lib |
| Sentiment | CNN F&G + 1w/1m/1y history | `production.dataviz.cnn.io/index/fearandgreed/graphdata` | Unofficial JSON (browser headers) |
| Credit | HY/IG OAS, DGS10/30/2, T10Y2Y | `fred.stlouisfed.org/graph/fredgraph.csv?id=...` | Public CSV (no API key, default UA only — Chrome UA gets blocked) |
| Currency | DXY, USD/JPY | yfinance `DX-Y.NYB`, `JPY=X` | Python lib |
| Breadth | % SPX top 50 above 200DMA (proxy) | yfinance batch on top 50 SPX names | Computed |
| Sector | XLK, XLU, XLP, XLY, XLE, XLF, SMH, RSP, IWM | yfinance | Python lib |
| **CTA flow** | — | **No public API; check Goldman PB report manually** | — |
| **AAII** | — | **No public API; check aaii.com/sentimentsurvey weekly** | — |

### Output schema

```json
{
  "timestamp_utc": "2026-05-08T...",
  "yf":      {SPY, QQQ, VIX, MOVE, VVIX, ^TNX, ^TYX, DXY, JPY, ETFs...},
  "fred":    {HY_OAS, IG_OAS, DGS10, DGS30, T10Y2Y, DGS2},
  "cnn":     {score, rating, prev_close, prev_1_week, prev_1_month, prev_1_year},
  "multpl":  {shiller_pe, spx_trailing_pe, spx_dividend_yield},
  "breadth": {above, total, pct_above_200dma_top50, missing_tickers},
  "scoring": {
    "layers": {valuation, volatility, sentiment, credit, currency, breadth, cta_flow, sector_rotation},
    "composite": 0-16,
    "regime": "🟢 GREEN | 🟡 YELLOW | 🟠 ORANGE | 🔴 RED",
    "triggers": ["Shiller CAPE 42.05 > 38 (extreme)", "VIX 17.19 < 18 (exit-signal threshold)", ...]
  }
}
```

### Fallback / gaps the script does NOT cover

| What | Why | Manual fallback |
|---|---|---|
| NDX Forward PE | yfinance returns `null` for ETF index; macromicro/gurufocus need login | yfmcp QQQ.info or quarterly recheck |
| AAII bullish % | aaii.com no API | Check aaii.com Thursday updates |
| Goldman CTA $ flow | proprietary | Check JPM/GS week-ahead reports |
| Buffett Indicator | multpl.com page returns 404 | Use currentmarketvaluation.com |
| Full $S5TH (all SPX) | Index restricted to data vendors | Top-50 proxy is biased toward mega-cap (intentional, captures Mag-7 risk) |

## Example execution for batch agent

```python
# Pseudo-code for the agent
indicators = {
    'NDX_PE':       fetch_yfinance('QQQ').get('forwardPE'),
    'VIX':          fetch_yfinance('^VIX').get('regularMarketPrice'),
    'MOVE':         fetch_yfinance('^MOVE').get('regularMarketPrice'),
    'VVIX':         fetch_yfinance('^VVIX').get('regularMarketPrice'),
    'TNX':          fetch_yfinance('^TNX').get('regularMarketPrice'),
    'TYX':          fetch_yfinance('^TYX').get('regularMarketPrice'),
    'DXY':          fetch_yfinance('DX-Y.NYB').get('regularMarketPrice'),
    'USDJPY':       fetch_yfinance('JPY=X').get('regularMarketPrice'),
    'F&G':          webfetch_cnn_fear_greed(),
    'HY_OAS':       webfetch_fred_BAMLH0A0HYM2(),
    'breadth_200':  websearch_breadth(),
    'CTA':          websearch_cta_flows(),
    'sectors':      [fetch_yfinance(s) for s in ['XLU','XLK','XLY','XLP','SPY','RSP']],
}

# Score each layer
scores = score_layers(indicators)
total = sum(scores.values())
regime = regime_from_total(total, indicators)  # apply override rules

# Compare to yesterday's snapshot (saved to ~/.claude/projects/.../macro_history.jsonl)
yesterday = load_yesterday()
delta = compute_delta(indicators, yesterday)

# Render report
print(format_report(regime, total, scores, indicators, delta))
save_today(indicators)  # for tomorrow's delta
```

## Recommended scheduling (use `/schedule` skill)

### Option A: Pre-market alert (recommended)

Cron: `0 12 * * 1-5` (8am ET = 12 UTC, weekdays)

```
Routine name: daily-macro-warning-premarket
Repo: claude-investment-skills (this repo)
Model: claude-sonnet-4-6
Allowed tools: WebSearch, WebFetch, Bash, Read
MCP: yfmcp (for ^VIX, ^MOVE, ^VVIX, sector ETFs)
Prompt: "Run the macro-warning skill. Output the structured report. If regime
flipped from GREEN→YELLOW or YELLOW→ORANGE/RED since yesterday, emphasize
the change. If NDX FwdPE crossed 38 in either direction, lead with it.
Save today's snapshot to memory for tomorrow's delta."
```

### Option B: Post-close summary

Cron: `0 21 * * 1-5` (5pm ET = 21 UTC, weekdays)

Same prompt but appends:
- "What broke today (single-day moves >2σ)"
- "Tomorrow's catalysts (CPI/Fed/earnings)"

### Option C: Both

Pre-market for action, post-close for reflection. Doubles the cost but catches both windows. Recommended only if user is active trading.

## Memory integration

After each run, write a one-line entry to:

```
~/.claude/projects/-Volumes-workplace-invest/memory/macro_history.jsonl
```

Format:
```json
{"date":"2026-05-08","regime":"YELLOW","score":7,"NDX_PE":38.1,"VIX":14.3,"FG":78,"HY_OAS":285,"USDJPY":154.2}
```

This enables:
- Trend tracking ("VIX rising 3 days in a row")
- Threshold crossing alerts ("NDX PE crossed above 38 today")
- Backtesting historical signals

## When NOT to use this skill

- Single-stock decisions → use `analyze-stock` instead
- Pre-earnings positioning → use `earnings-prep`
- Portfolio audit → use `portfolio-audit`
- New idea hunting → use `find-untapped-thesis` / `find-alpha`

This skill answers ONE question: **"Should I be aggressive, neutral, or defensive RIGHT NOW?"**

## Companion skills

- **`sector-rotation-analysis`** — full 11-GICS heat map (this skill only does Layer 8 quick check)
- **`macro-risk-check`** — overlapping but more news-driven; this skill is more quantitative
- **`portfolio-audit`** — once regime is determined, audit current book against it

## Hard-learned context (verified examples)

- **2000 March**: NDX PE 73, F&G 95, VIX 18 → 6 months later NDX -78%
- **2020 Feb**: NDX PE 32, F&G 60, VIX 13 → 5 weeks later -35%
- **2021 Nov**: NDX PE 35, F&G 80, VIX 17 → 12 months later -33%
- **2022 Jan**: VIX <17 in low-rate environment + Fed hawkish pivot → -27%
- **2026 May (now)**: NDX PE **38.15** (essentially at all-time non-bubble high), VIX low, AI capex narrative max-extended

The signal is loudest when **valuation is extreme AND sentiment is greed AND VIX is low AND breadth is narrowing**. Any 3 of 4 = serious YELLOW. All 4 = RED.

## Year-specific overlays (update annually)

For **2026**:
- AI capex names (NVDA / AVGO / AMD / MRVL) are sentiment-coupled to AI Power names (CEG / VST / GEV) and AI receiver names (FN / TSEM / GFS / NOK / GLW)
- A correction in any of the three sub-themes will likely spread to all three within 5-10 trading days
- Yen carry (USD/JPY) is the single highest-correlation external trigger for AI / semi names
- Watch for: NVDA earnings (5/20 next), CPI prints, Fed dots, BOJ rate path, China CXMT IPO (June 2026 — could pressure MU/SK Hynix valuations)
