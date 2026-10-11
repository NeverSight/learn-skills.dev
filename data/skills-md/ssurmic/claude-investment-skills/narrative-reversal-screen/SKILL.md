---
name: narrative-reversal-screen
description: Screens for "narrative reversal" candidates — stocks down 30%+ from 52W high with concrete catalyst still intact, worst-case priced in, early reversal signal (first higher low, 50DMA cross, insider buying after capitulation). Returns top 3 with entry plan. Triggers in English ("beaten-down stocks with thesis", "find reversal plays", "stocks at bottom that can recover", "fallen angel screen", "comeback candidates") or Chinese ("找暴跌反转股", "找回归类股票", "ORCL 那种反转", "已经跌透的好股", "底部反弹候选").
---

# Narrative Reversal Screen — Buy The Beaten Down

## 🔍 Pre-flight checklist — reversals fail spectacularly in the wrong regime

A "down 50% with intact catalyst" looks like value until the broader market sells off another 20% and your "value" becomes -70%. Required checks:

1. **Macro regime gate** — trigger `macro-warning`. Reversals work in 🟢 GREEN (recovering market lifts beaten-down names) and **mid-late 🟡 YELLOW** (capitulation phase). 🔴 RED → reversals are still falling knives. Don't recommend reversal buys in RED; flag as "watch list only" instead.
2. **Insider must be slowing sells or starting to buy** — `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/insider_ratio.py 2>/dev/null | head -1) TICKER --window 180` (180d for reversals — see the trend over 2 quarters, not just 90d). The ORCL signal was: pre-crash 8 sells / 2 buys → post-crash 2 sells / 5 buys. Form 4 code "P" only.
3. **First higher low CONFIRMED, not predicted** — Don't pre-empt. Wait for: (a) 50DMA crossover OR (b) confirmed higher low on weekly. Pre-empting "looks bottomed" is how -30% becomes -50%.
4. **3-tier entry** — T1 = first confirmed higher low; T2 = retest of capitulation low; T3 = full revisit (if it happens). Never "buy at market on a chart that looks bottomed."
5. **Sizing 2-3% per pick** — reversals are higher-risk than momentum names; don't size like core holdings.
6. **Tax framing** — reversal entries are positions, not swings; assume 12+ month hold. Frame return targets after-tax: +50% gross = +40-43% after LTCG.

**"Look carefully" rule**: most "beaten-down with intact catalyst" stocks are beaten down for a REASON the bull case denies. Always answer: "what would have to be true for the bear thesis to be correct?" If you can't articulate it, you don't understand the trade. Verified false reversals from 2026: WBA -60% (mgmt still selling), DLTR -45% (insiders also exited), KSS -50% (PE walked away).

See [README's Hard Rules](../README.md#%EF%B8%8F-hard-rules-never-violate) for the full anti-pattern list.

---

## Goal

Find stocks where:
1. **Worst-case is already priced in** (down 30%+ from ATH)
2. **Concrete catalyst still intact** (real contracts, not just hope)
3. **Reversal early signal** (50DMA up-cross or first higher low)
4. **Insider not capitulating** (sells slowing or buying starting)
5. **Forward valuation cheap** (P/E < pre-crash 50%)

The ORCL pattern that delivered $172 → $185 reversal: down 50% from $345 + OpenAI $300B intact + insider selling slowing + 50DMA crossover.

## Why this matters

**Most "value" looks dead.** But true narrative reversals (where the bear story is wrong) outperform:
- ORCL 2025/9 → 2026/5: -50% then +35% rebound
- META 2022 → 2023: -76% then +200%
- NFLX 2022 → 2023: -75% then +180%
- CRM 2022 → 2023: -55% then +90%

These all share: panic priced in **maximum darkness** then truth comes out.

## The 5-Step Workflow

### Step 1 — Define hunting ground

Common buckets where reversals happen:
- **AI Cloud** (ORCL after OpenAI doubts)
- **Big Tech** (META 2022 metaverse fear)
- **Beaten retailers** (NFLX 2022 streaming saturation fear)
- **Software** (CRM, ZM, DOCU after 2022 reset)
- **Healthcare/Biotech** after FDA rejection
- **China** after regulatory crackdown
- **Auto** after EV demand reset
- **Banks** after credit fear

### Step 2 — Apply hard filters

Pull via `mcp__yfmcp__yfinance_get_ticker_info` for candidate list:

**Hard cuts (must pass ALL):**
| Filter | Threshold | Why |
|---|---|---|
| **Distance from ATH** | -30% to -65% | Need real darkness, but not complete failure |
| **Forward P/E** | <30 (cheap for sector) | Avoid "down but still expensive" |
| **Market cap** | >$10B | Liquidity for institutional re-entry |
| **Revenue growth (latest)** | >0% (positive) | Don't catch a falling knife |
| **Cash flow** | Positive OR within 1 quarter | Survives long enough for reversal |

**Optional but strong:**
- Recent earnings beat (sentiment shift)
- New CEO or strategy reset
- Activist investor involvement
- Big contract / partnership announcement

### Step 3 — Look for reversal signals

For each survivor, check:

| Signal | What to look for |
|---|---|
| **50DMA cross** | Stock has crossed above 50DMA (or testing) |
| **First higher low** | Recent low > previous low (bottoming) |
| **Volume divergence** | Down moves on lower volume vs up moves |
| **RSI bullish divergence** | Lower price, higher RSI |
| **Insider buying** | First insider buys in 6+ months (BIG signal) |
| **Short interest declining** | Shorts covering |

### Step 4 — Verify catalyst is intact (CRITICAL)

The hardest part. Use WebSearch and earnings transcripts to verify:

**Questions to ask:**
1. **Is the original thesis still true?** (e.g., ORCL OpenAI $300B contract still active)
2. **What's been added since the crash?** (new contracts, customers)
3. **Is management same/changed?** (new CEO often = catalyst)
4. **Have analysts started raising targets?** (early signs of recognition)
5. **Are insider buying?** (ultimate signal)

**Reject if catalyst is broken:**
- Major customer lost
- Management change without coherent strategy
- Regulatory headwinds increased
- Competitive moat eroded

### Step 5 — Check insider for capitulation/buying

Run `insider_ratio.py "TICKER" --window 90` (or wider window covering capitulation date). Uses openinsider primary; only Form 4 code "P" counts as buy.
- 🟢🟢🟢 **RECENT CLUSTER BUY** (3+ insiders, $500K+ each): Bottom signal — most reversal candidates have this. Real 2026 example: NKE (CEO Hill + Tim Cook + 2 Directors, $3.7M, 7 days, after -46% drop).
- 🟢 **STRONG BUY**: 1-2 senior insiders buying after period of selling
- 🟡 **OK**: Selling slowed / stopped + sells are 10b5-1 trusts (verify at secform4.com)
- 🔴 **AVOID**: CEO/CFO ad-hoc selling (not 10b5-1) = haven't capitulated

**Reminder**: News articles' "cluster buy" claims are often false positives (RSU/DSU grants). Always verify Form 4 code = "P" at openinsider.com/[TICKER].

Especially good: **CEO/CFO/Director cluster buy after stock down 50%** (CEVA 2026 / NKE 2026 / AMKR Kim family / LSCC new CEO patterns).

## Output format

```markdown
# Narrative Reversal Screen — [Date]

## TL;DR
Found [N] candidates with intact catalyst + reversal signal. Top 3:
1. [TICKER] — [tagline]
2. [TICKER] — [tagline]
3. [TICKER] — [tagline]

## Screen Results

### Top 3 Deep Dive

#### #1 [TICKER]
**The Crash**: ATH $X (Date) → Low $Y (Date) = -Z%
**Why it crashed**: [1 sentence]
**The Recovery**: Current $A, +B% from low

**Catalyst Status**:
- Original thesis: [check if still true]
- Concrete evidence: [contracts, customers]
- New positives since crash: [list]

**Reversal signals**:
- 50DMA: [above/below + how recently crossed]
- First higher low: [yes/no, when]
- Insider: [buy ratio + key buyers]
- Analyst: [recent upgrades/raises]

**Valuation**:
- Pre-crash P/E: 35x
- Current P/E: 21x
- 50% multiple compression already
- Peer P/E: 28x → upside in re-rating

**Entry Plan**:
- Now: $A (try 30%)
- Pullback to 50DMA $B: add 30%
- Pullback to 200DMA $C: add 40%

**12-month target**: $D (+E%)

**Risk**: [main risk that would invalidate]

## Watch list (not yet entry signal but close)
| Ticker | Reason waiting |

## Rejected
| Ticker | Why rejected |
| TICKER | Catalyst actually broken |
| TICKER | Insider still capitulating |
| TICKER | Down 30% but PE still 60x |
```

## Hard rules

1. **Verify catalyst is INTACT.** Don't catch falling knives. ORCL had OpenAI $300B verifiable; some falling stocks don't have anything.
2. **Don't buy at exactly the bottom.** Wait for first higher low + 50DMA cross.
3. **Insider matters MORE here.** In growth stocks insider is noise; in reversals it's THE signal (CEVA pattern).
4. **Re-rating > earnings growth.** ORCL went from PE 35 → 21 = -40%. Going back to 28-30 = +35% just on multiple, before earnings.
5. **Cap position size** at 5-7% (still risky, R/R asymmetric).
6. **Set stop at recent low.** If thesis breaks, exit fast.

## Common pitfalls

| Pitfall | Example | Lesson |
|---|---|---|
| Catching falling knife | Buying ORCL at $200 (still falling) | Wait for higher low |
| Anchoring to ATH | "ORCL was $345, must go back" | ATH is meaningless; intrinsic value matters |
| Ignoring why it crashed | "Stock down 50%, must be good" | Some crashes are correct (BBBY, WW) |
| Buying first reversal signal | Bought 50DMA cross, then -10% retest | Wait for confirmation (volume + 2nd higher low) |
| Selling too early on bounce | Bought $172, sold $185 (+8%) | Multi-month moves can return 30-50% |

## Templates: Common reversal patterns

### Pattern A: The "Worst-Case Priced In"
- ORCL 2026/5 (China=0 priced in for NVDA, OpenAI doubt for ORCL)
- META 2022 (metaverse + ad recession fears)
- Sign: forward P/E at multi-year low, but earnings stable

### Pattern B: The "Activist or New CEO"
- INTC under Lip-Bu Tan (2026 turnaround attempt)
- DIS under Iger return (2022)
- Sign: new strategy = new buying

### Pattern C: The "Sector Rotation Reversal"
- Energy 2020 → 2022 (oil $30 → $130)
- Bank 2023 (post-SVB collapse, then recovery)
- Sign: macro tailwind reasserts

### Pattern D: The "Earnings Inflection"
- AMD 2023 (data center inflection)
- NVDA 2023 Q1 ER (AI catalyst surprise)
- Sign: first surprise beat after string of misses

## Watch list management

**Status categories:**
- 🟢 **BUY now** — all 5 criteria pass
- 🟡 **WATCH** — 4 of 5 pass, waiting for trigger
- 🟠 **STILL FALLING** — early, wait for higher low
- 🔴 **REJECTED** — catalyst broken or value trap

**Update cadence**: Weekly review of WATCH list, daily for current entries.

## When to invoke

- User asks: "Find beaten-down stocks with real story"
- User asks: "ORCL-style plays"
- User asks: "Reversal candidates"
- After SPX -10%+ correction (lots of opportunities open up)
- Quarterly: routine reversal hunting

## Tool cheat-sheet

| Need | Tool |
|---|---|
| Distance from ATH | `mcp__yfmcp__yfinance_get_ticker_info` → `52WeekHigh`, current price |
| Pre-crash valuation | `WebSearch`: "[ticker] historical P/E 2024 2025" |
| Catalyst verification | `WebSearch`: "[ticker] [catalyst keyword] update [current month]" |
| Insider | `insider_ratio.py "TICKER" --since [crash date]` |
| 50DMA cross | `mcp__yfmcp__yfinance_get_price_history` (3-6mo) |

## Companion skills

After this screens 3 candidates:
- Run `analyze-stock` for deep dive
- Run `option-wall-analysis` for short-term levels
- Run `leaps-screen` for LEAPS (LEAPS work GREAT for reversals — high IV after crash)
- Run `tax-optimize` if user wants to use as alternative to current holdings
