---
name: find-alpha
description: Find alpha across 3 time horizons (1-3 week swing, 1-3 month position, 6-12+ month LEAPS). Each scan returns top 3 candidates with strict filters (insider real buying not RSU, theme fit, catalyst, valuation). Designed to be invoked manually OR via schedule (weekly Monday pre-market). Companion to review-investment-screenshot skill.
---

# Find Alpha — 3-Horizon Screener

**Goal:** Find 3 tickers per time horizon (swing / position / LEAPS) where market hasn't fully priced the upside. Not "good companies" — **mispriced setups**.

**Companion to** `review-investment-screenshot`. Output of this skill feeds INTO that skill for full review.

---

## 🔍 Pre-flight checklist — run BEFORE returning any candidate

Discovery is the easy half. Execution discipline is where alpha leaks. Every candidate output MUST pass:

1. **Macro regime gate** — trigger `macro-warning` skill first. Regime determines which horizons to run:
   - 🟢 GREEN: all 3 horizons (swing + position + LEAPS)
   - 🟡 YELLOW: position + LEAPS only (skip swing — chop kills swings)
   - 🔴 RED: LEAPS only at deep value, no swing/position adds. Output should default to "no swings/positions this week" in RED.
2. **Insider strict per candidate** — already in Hard Rules #1 below. Don't bend it for a "great story."
3. **3-tier entry MANDATORY per candidate** — output "Entry: $X" alone is insufficient. Must be T1 (trigger) / T2 (50DMA or 20% drawdown) / T3 (200DMA or 38% drawdown). User should never have to ask "but at what price specifically?"
4. **Position size capped per horizon** (already defined in horizons below — enforce strictly):
   - Swing: 1-2% per pick · Position: 2-4% · LEAPS: 3-5%
   - High-beta total book ≤ 50%.
5. **Tax flag for Swing horizon** — Swing = 1-3 weeks = STCG when exited. If user is in high bracket, surface that explicitly in output ("STCG ~30% federal — net win must clear that").
6. **No "speculative" hidden in confidence** — If thesis is unverified, label "🟡 SPECULATIVE" in confidence column. Don't bundle speculation into 8/10 ratings.

**"Look carefully" rule**: blacklisted names (APH, EME, ETN, PWR, POWL, GEV) and similar distribution-at-top patterns return via news cycles. Always re-verify with `insider_ratio.py`, don't trust the cached blacklist as the only filter. New distribution patterns appear; refresh the blacklist quarterly.

See [README's Hard Rules](../README.md#%EF%B8%8F-hard-rules-never-violate) for the full anti-pattern list.

---

## When to invoke

- User asks: "find alpha", "find me 3 tickers", "what's the next MRVL setup", "screen swing trades", "weekly alpha scan"
- Scheduled run (Monday pre-market, weekly)
- After major macro event (Fed decision, big earnings) — universe regime may have shifted

## Hard rules (carry over from review-investment-screenshot)

1. **Insider data must come from `insider_ratio.py --window 90` (openinsider primary)** — never trust yfinance net% headline.
2. **Form 4 code "P" only counts as buy.** A/M/F/G are RSU/exercise/tax — NOT buys, regardless of how news headlines describe them. Verified false positives: UNH "10 directors 4/1/2026" (all DSU grants), PLTR "Karp 1.47M shares" (RSU vesting).
3. **Filter out 52w-high distribution traps** (positions where insider net is "+net buy" but absolute SELL $ >> BUY $). Verified blacklist: APH, EME, ETN, PWR, POWL, GEV.
4. **Each candidate must have action + size + reason** (entry, stop, target, why).
5. **Confidence < 7/10 → don't include**. Quality > quantity. If only 2 candidates pass at swing horizon, output 2 not 3.
6. **No backtest fabrication**. If thesis is unverified, label "speculative."
7. **Theme fit explicit** — name the cluster (CPU inference, AI DC photonics, nuclear, etc.) not "AI play."
8. **Use `cluster_buy_scan.py` to discover new candidates** — it hits openinsider.com/latest-cluster-buys directly. Don't rely on news article "cluster buy" claims; verify Form 4 code = "P" for every name.

---

## The 3 horizons + their alpha sources

### Horizon 1: Swing (1-3 weeks)
**Primary signals (any 2 must hit):**
- Earnings within 21 days + ESP > +3% + last 4Q beat ≥ 3
- Short squeeze: short % of float > 15% + days-to-cover > 5
- Gamma squeeze: ATM/OTM call OI > put OI 3:1 within 30 DTE
- Insider cluster buy within last 14 days (≥2 insiders, ratio ≥ 3:1)
- Mean reversion: 10-15% drop from 30d high + RSI < 30 + bounce confirmed

**Sizing:** 1-2% of book per pick (small, fast, high-uncertainty).
**Stop:** -8% from entry or break of MA20.
**Script:** `swing_scan.py`

### Horizon 2: Position (1-3 months)
**Primary signals (any 2 must hit):**
- Insider cluster buy within 60 days (ratio buy:sell ≥ 2:1, $ value > $500k)
- Analyst PT raises (3+ in last 30 days)
- Quarter earnings revision: NTM EPS revision > +5% in last 30 days
- Mean reversion: near MA200 + RSI 30-50 + recent insider activity
- Catalyst within 30-90 days (product launch, FDA, contract, M&A rumor)

**Sizing:** 2-4% of book per pick.
**Stop:** -12% from entry or thesis break.
**Script:** `position_scan.py`

### Horizon 3: LEAPS Thesis (6-12+ months)
**Primary signals (any 2 must hit):**
- Founder/family/10%+ holder open-market buy ≥ $5M (AMKR Kim family pattern)
- Forward P/E < 25x AND revenue growth > 20% (GARP)
- Below MA200 (early cycle) + cash > 15% of mcap + low debt
- Multi-year secular thesis: CPU inference, AI DC photonics, edge AI, nuclear power, US re-shoring
- New CEO with skin-in-the-game (LSCC pattern: $1M+ open-market buy in first 3 months)

**Sizing:** 3-5% of book per pick. Use deep-ITM LEAPS (delta 0.85+) as stock replacement.
**Stop:** -25% from entry or fundamental thesis break.
**Script:** `leaps_scan.py`

---

## Workflow when invoked

1. **Start with cluster-buy discovery** — fast pass to surface market-wide candidates:
   ```bash
   uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/cluster_buy_scan.py 2>/dev/null | head -1) --days 30 --min-value 500000 --min-insiders 2 --detail --enrich
   ```
2. **Run the 3 scripts in parallel:**
   ```bash
   uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/find-alpha/scripts/swing_scan.py 2>/dev/null | head -1) &
   uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/find-alpha/scripts/position_scan.py 2>/dev/null | head -1) &
   uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/find-alpha/scripts/leaps_scan.py 2>/dev/null | head -1) &
   wait
   ```
3. For each finalist (top 5 from each script), **call `insider_ratio.py --window 90` to verify** (uses openinsider primary).
4. Cross-check any "cluster" claims at openinsider.com/[TICKER] for Form 4 code "P".
5. For each verified candidate, do a **2-paragraph deep dive**: thesis, why mispriced, what could break it.
6. Output formatted table (see below).

## Output format

```
# Alpha Scan — [DATE]

## 📊 Macro regime (gate — drives which horizons output)
🟢/🟡/🔴 — [1-line: composite score, sectors hot/cold, regime call]
[If 🔴 → "Only LEAPS horizon below. Swing/Position disabled this scan."]

## 🎯 Top 3 SWING (1-3 weeks) — [SKIP if regime != 🟢]
| Rank | Ticker | Thesis (1 line) | T1 | T2 | T3 | Stop | Target | Size | Confidence |
| 1 | XXX | ... | $X | $X | $X | $X | $X | 1.5% | 8/10 |

Where T1=trigger, T2=50DMA or -20%, T3=200DMA or -38%. ⚠️ STCG warning: 1-3 week swing = short-term cap gains when exited.

[For each: 2-paragraph deep dive. Must explicitly call out macro regime + insider verification.]

## 🎯 Top 3 POSITION (1-3 months) — [SKIP if regime == 🔴]
[Same structure with T1/T2/T3, size 2-4%]

## 🎯 Top 3 LEAPS (6-12+ months)
[Same structure with T1/T2/T3 for underlying, size 3-5%, mention dec 2027 vs jan 2028 expiry choice]

## ⚠️ Disqualified candidates
[Names that came up in scan but failed insider_ratio strict check. Include WHY (e.g. "INTC: 4 sells, 0 buys 90d", "PLTR: Karp Rule 10b5-1 vesting only — looks like buy but isn't").]

## 🧮 Sizing summary
- Current high-beta book exposure: X% (cap 50%)
- This scan's adds if all accepted: +Y%
- Post-add high-beta: Z% [warn if > 50%]
```

---

## Tool cheat-sheet

| Task | Script |
|------|--------|
| **Market-wide cluster-buy discovery** | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/cluster_buy_scan.py 2>/dev/null | head -1) --days 30 --min-value 500000 --min-insiders 2 --detail --enrich` (always run first) |
| 1-3 week swing alpha scan | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/find-alpha/scripts/swing_scan.py 2>/dev/null | head -1)` |
| 1-3 month position alpha scan | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/find-alpha/scripts/position_scan.py 2>/dev/null | head -1)` |
| LEAPS alpha scan | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/find-alpha/scripts/leaps_scan.py 2>/dev/null | head -1)` |
| **Verify candidate insider strict** (openinsider primary) | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/insider_ratio.py 2>/dev/null | head -1) "TICKER" --window 90` (mandatory cross-check). Add `--source both` for high-stakes calls. |
| Live quote/MAs | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/quote_pull.py 2>/dev/null | head -1)` |
| Option walls | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/option_walls.py 2>/dev/null | head -1)` |
| Max pain | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/max_pain.py 2>/dev/null | head -1)` |

---

## Schedule integration

This skill is configured to auto-run via cron:
- **Mondays 8:00 AM ET (pre-market)**: full 3-horizon scan
- **Daily 9:15 AM ET (15 min before open)**: swing-only scan (catches overnight catalysts)
- **First of each month**: LEAPS-only deep scan

Schedule managed via `schedule` skill. Trigger names:
- `weekly-alpha-scan` (Monday)
- `daily-swing-scan` (weekdays)
- `monthly-leaps-scan` (1st of month)

To pause: `/schedule pause [trigger-name]`. To run on-demand: just ask "run alpha scan now."

---

## Hard exclusions (verified distribution-at-top, do not surface)

These appeared with positive net% but failed strict buy-vs-sell check on 2026-04-24:
- **APH, EME, ETN, PWR, POWL, GEV** — all CEO/Officer dumping at 52w high

These will be auto-filtered by scripts via blacklist.

## Anti-patterns (will reject candidates if these appear)

- "Insider net buy %" used as primary signal without dollar ratio
- Tax-withholding events counted as sales (filtered automatically)
- RSU grants counted as buys (filtered automatically)
- Single-Director small buy ($<$200k) without C-suite confirmation
- Stock at 52w high + recent C-suite open market sell > $5M (auto-blacklist)
