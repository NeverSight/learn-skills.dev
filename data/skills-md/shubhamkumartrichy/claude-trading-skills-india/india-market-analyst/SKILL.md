---
name: india-market-analyst
description: |
  Master workflow for analysing Indian stocks, indices and derivatives on NSE/BSE. Routes to the
  specialised skills in this pack: technical analysis, multi-timeframe, RSI divergence, Fibonacci,
  position sizing, stop-loss, trailing stops, risk-reward, F&O option chains, options strategies,
  trading costs, tax, market structure, market pulse, market regime, sector rotation, market
  breadth, FII/DII flows, momentum scans, breakout planning, results reactions, pair trading,
  backtesting, trading discipline, portfolio review, fundamentals, IPOs and broker integration.

  Use whenever the user asks to analyse, check or plan a trade in an Indian stock, index (NIFTY,
  BANKNIFTY, SENSEX) or F&O contract: "analyze RELIANCE", "should I buy HDFCBANK", "what's the setup
  on NIFTY", "plan my trade in TCS", "review my Groww/Zerodha holdings", or any buy/sell/hold question
  about NSE/BSE instruments.
---

# India Market Analyst (orchestrator)

This skill coordinates the whole pack into one disciplined workflow. Use it for broad questions. Use
the specialised skill directly when the question is narrow (see the routing table).

## Ground rules (apply to every answer)

1. **Know the clock.** Work out the current time in IST and the market state before quoting prices:
   pre-open (09:00–09:15), open (09:15–15:30), post-close, weekend, or exchange holiday (see
   `indian-market-structure`). Label every price as *live*, *delayed* or *end-of-day (date)*. Never
   present yesterday's close as the current price.
2. **Cite data.** Every number has a source and timestamp: broker MCP, yfinance, the user, or a web page.
   If a figure could not be fetched, say so and ask for it instead of guessing.
3. **No orders without an explicit, per-order confirmation.** Follow the order protocol in
   `broker-integration`. Analysis never auto-executes.
4. **Educational framing.** You are not a SEBI-registered investment adviser or research analyst. Give
   analysis, scenarios and risk maths, not guarantees. When a user is new to F&O, mention SEBI's
   finding that about 91% of individual F&O traders lost money in FY25 (and about 88% in FY26).
5. **Indian conventions.** Use ₹ with Indian grouping (₹1,25,000; ₹2.5 lakh; ₹3 crore), NSE trading
   symbols, and IST.
6. **Event risk first.** Before recommending a trade, check results dates, ex-dividend/bonus/split
   dates, F&O ban list, expiry day, RBI policy, Budget, index rebalancing, and global events (US Fed).
7. **Costs and tax are part of the trade.** Quote R:R and breakevens after charges
   (`trading-costs`) and mention the tax treatment when holding period matters (`indian-tax-for-traders`).

## Step 0 — Resolve the instrument

- Exact NSE symbol (or BSE scrip code), series (EQ = normal, BE/BZ = trade-for-trade, SM/ST = SME),
  sector, index membership, and whether it trades in F&O.
- Check recent corporate actions. Bonus issues and splits are common in India and break naive price
  history. Demergers change symbols: for example, Tata Motors split into TMPV and TMCV in late 2025.
- Check surveillance status (ASM/GSM/ESM). A stock in a surveillance stage has extra margins, tighter
  bands, or trade-for-trade settlement.

## Step 1 — Get data (priority order)

1. **Connected broker MCP** (Groww, Zerodha Kite, Dhan, Upstox, Fyers, Kotak Neo). See
   `broker-integration` for which tool does what.
2. **yfinance** through the technical-analysis script: `../technical-analysis/scripts/ta.py summary --symbol RELIANCE` (needs
   `pip install yfinance`). NSE stocks map to `.NS`, BSE to `.BO`, indices to `^NSEI`, `^NSEBANK`,
   `^BSESN`, `^INDIAVIX`.
3. **User-supplied** prices, CSV exports, or screenshots. Save candles to CSV/JSON and pass them to the
   scripts with `--csv` or `--candles`.

## Step 2 — Run the analysis

| Stage | What to do | Skill / script |
|---|---|---|
| Context | NIFTY/sector trend, India VIX, FII/DII flows, event calendar | `market-pulse` |
| Regime | Distribution days, follow-through, exposure ceiling | `market-regime` (`regime.py status`) |
| Sectors | Which NSE sectors lead or lag NIFTY | `sector-rotation` (`sectors.py rotation`) |
| Breadth | % of stocks above DMAs, A/D line, new highs/lows, health score | `market-breadth` (`breadth.py status`) |
| Flows | FII/DII cash flows, FII index-futures long/short, bulk/block deals | `fii-dii-flows` (`flows.py`) |
| Structure | Weekly bias → daily setup → 75-min/15-min entry | `multi-timeframe-analysis` (`ta.py mtf`) |
| Technicals | Trend, levels, indicator dashboard, scenarios | `technical-analysis` (`ta.py summary`) |
| Momentum | Regular/hidden RSI divergences | `rsi-divergence` (`ta.py divergence`) |
| Levels | Retracement entries, extension targets | `fibonacci-trading` (`ta.py fib`) |
| Ideas | Momentum bursts, episodic pivots, RS leaders across a universe | `momentum-scanner` (`momentum.py scan`) |
| Setup | Stage 2 trend template, VCP/flat base, pivot, breakout plan | `breakout-planner` (`breakout.py check`) |
| Results | Results-day reaction score, post-results drift, results in the holding window | `results-season` (`results.py`) |
| Quality | Fundamentals and governance red flags (investing horizon) | `fundamental-screening` |
| Derivatives | OI, PCR, max pain, IV, expected move | `fno-options-analysis` (`options.py`) |
| Decision | Buy / sell / hold / wait, with explicit triggers | this skill |
| Sizing | Quantity or lots for a given rupee risk | `position-sizing` (`risk.py size`) |
| Stops | Initial stop, GTT mechanics, trailing plan | `stop-loss-strategies`, `trailing-stops` |
| Targets | R:R after costs, expectancy | `risk-reward-ratio` (`risk.py rr`) |
| Costs/tax | Charges, breakeven, STCG vs LTCG timing | `trading-costs`, `indian-tax-for-traders` |
| Validate | Backtest the rule with Indian charges before trading it | `backtest-lab` (`backtest.py`) |
| Gate | Loss limits, pre-trade checklist before any order ticket | `trading-discipline` (`discipline.py gate`) |

Scripts, relative to this skill's folder: `../technical-analysis/scripts/ta.py`,
`../position-sizing/scripts/risk.py`, `../fno-options-analysis/scripts/options.py`,
`../trading-costs/scripts/charges.py`, `../indian-tax-for-traders/scripts/tax.py`,
`../market-regime/scripts/regime.py`, `../sector-rotation/scripts/sectors.py`,
`../breakout-planner/scripts/breakout.py`, `../trading-discipline/scripts/discipline.py`,
`../portfolio-review/scripts/portfolio.py`, `../market-breadth/scripts/breadth.py`,
`../fii-dii-flows/scripts/flows.py`, `../momentum-scanner/scripts/momentum.py`,
`../results-season/scripts/results.py`, `../pair-trading/scripts/pairs.py`,
`../backtest-lab/scripts/backtest.py`. All are standard-library Python. Run them instead of doing arithmetic by hand, and show the key output lines.

## Routing table

| User asks | Primary skill | Supporting |
|---|---|---|
| "Analyze INFY" / "should I buy X" | this skill | all as needed |
| "How many shares / lots?" | position-sizing | stop-loss-strategies, trading-costs |
| "Where do I put my stop?" | stop-loss-strategies | technical-analysis |
| "Trail my stop on SBIN" | trailing-stops | position-sizing (`risk.py trail`) |
| "Is this trade worth it?" | risk-reward-ratio | trading-costs |
| "Divergence on ICICIBANK?" | rsi-divergence | technical-analysis |
| "Fib levels for NIFTY" | fibonacci-trading | technical-analysis |
| "Weekly vs daily trend" | multi-timeframe-analysis | technical-analysis |
| "NIFTY option chain / PCR / max pain" | fno-options-analysis | market-pulse |
| "Iron condor / straddle / spread for this week" | options-strategies | fno-options-analysis |
| "What are my charges / breakeven?" | trading-costs | — |
| "How much tax on my gains / F&O loss?" | indian-tax-for-traders | trading-costs |
| "Market timings, circuits, T+1, GTT, ASM" | indian-market-structure | — |
| "How's the market today / pre-market brief" | market-pulse | fno-options-analysis |
| "Is X fundamentally good?" | fundamental-screening | — |
| "Should I apply for this IPO?" | ipo-analysis | fundamental-screening |
| "Connect Zerodha/Groww", "place an order" | broker-integration | trading-discipline |
| "Is the market in an uptrend? How much should I invest now?" | market-regime | market-pulse |
| "Which sectors are leading?" | sector-rotation | market-regime |
| "Is X a breakout / VCP? Plan the breakout" | breakout-planner | position-sizing, stop-loss-strategies |
| "Can I trade today? Review my trades" | trading-discipline | position-sizing (`risk.py journal`) |
| "Review my portfolio / rebalance my holdings" | portfolio-review | indian-tax-for-traders, sector-rotation |
| "Is the rally broad? Market breadth?" | market-breadth | market-regime |
| "Are FIIs buying or selling? FII long/short ratio?" | fii-dii-flows | market-pulse |
| "Find momentum stocks / gap-ups today" | momentum-scanner | breakout-planner |
| "How did X react to results? Results this week?" | results-season | fundamental-screening |
| "Is HDFCBANK vs ICICIBANK a tradable pair?" | pair-trading | fno-options-analysis |
| "Backtest this strategy" | backtest-lab | trading-costs, position-sizing |

## Output format (full analysis)

```markdown
# [SYMBOL] — [Date, time IST] ([live | delayed | EOD dd-mmm])

## Quick take
[1–2 sentences: bias, key level, what you would do and what would change your mind]

## Market context
NIFTY [trend], sector index [trend], India VIX [value], events: [results/ex-date/expiry/RBI]

## Position (if held)
Qty, avg price, unrealised P&L, holding period (STCG/LTCG status)

## Technical setup
Weekly bias → daily setup; key levels; indicator dashboard (bull/bear count); divergences; Fib zone

## Scenarios
A (bullish, xx%): trigger → target → invalidation
B (bearish, xx%): ...
C (range, xx%): ...

## Action plan
| Action | Trigger | Price | Qty/Lots | Stop | Target(s) | R:R after costs |
|---|---|---|---|---|---|---|

## Risk & costs
- Max loss: ₹X (Y% of capital), gap-through-stop loss ₹Z
- Round-trip charges ₹C; breakeven ₹B
- Stop mechanics: GTT / SL-limit / closing basis; trailing plan
- Tax: [STCG 20% now vs LTCG 12.5% after dd-mmm-yyyy if relevant]

_Educational analysis, not investment advice. Data: [sources + timestamps]._
```

Keep probabilities honest: base them on trend alignment, indicator agreement, volume and level
proximity, and keep them near 33/33/33 when evidence is mixed.

## Pitfalls specific to Indian markets

- **Stop orders don't carry overnight** for delivery at most brokers. Use GTT for a persistent stop.
- **Circuits.** Non-F&O stocks have 2–20% price bands. In a lower circuit, nobody can sell, so stop
  losses don't fill.
- **Gaps.** Overnight global cues (US close, GIFT Nifty) gap the open. Size for the gap, not only the stop.
- **Expiry days** (NIFTY Tuesday, SENSEX Thursday) distort index option premiums and intraday moves.
- **Results season** (within 45 days of quarter end; 60 days for Q4). Avoid fresh swing entries just
  before results unless the trade is about the event.
- **T+1 and BTST.** Shares bought today arrive tomorrow. Selling before delivery (BTST) risks short
  delivery and auction penalties if the chain fails.
- **Small/SME and tip stocks.** Thin floats, upper-circuit streaks and Telegram/WhatsApp tips are
  classic pump-and-dump markers. SEBI acts against unregistered "finfluencers".
