---
name: desk-strategy-lab
description: How the Strategist works with the user to turn their own trading idea into explicit rules, backtest it honestly on Hyperliquid candle and funding history, paper-trade it on testnet through the desk cycle, and how a strategy is promoted from draft to paper to live so the autonomous cycle may trade it. Method only - the desk ships no strategies and makes no return claims. Use when the user wants to design, test, compare, paper-trade or promote an idea.
license: MIT
metadata:
  version: "1.2.0"
  author: Galleon Labs
  category: desk
---

# Strategy lab

The lab exists so the user can find out whether their idea holds up before risking money on it. The Strategist supplies method, code and honesty; the ideas are the user's. Nothing here recommends what to trade.

## Workspace

```
/workspace/trading-desk/strategies/<name>/
  RULES.md          the rules, in words, agreed with the user before any code
  data.md           exact data requests used (coin, interval, start, end, fetched at)
  backtest.py       readable, single-file backtest
  runs/YYYY-MM-DD-HHMM.md   one file per run: parameters, results, caveats
  POSTMORTEM.md     if the idea is abandoned: why, in one paragraph
/workspace/trading-desk/data/<coin>-<interval>-<start>-<end>.csv   fetched by the Market Analyst or the Strategist
```

## 1. Rules first

Interview the user until every field is unambiguous. Write `RULES.md`:

```markdown
# funding-fade-v1

- status: draft                  # draft | paper | live; only the user changes it, in writing
- universe: ETH, BTC, SOL perps on Hyperliquid
- data: 4h candles (close), hourly funding from fundingHistory
- entry: when the average hourly funding over the last 8 hours is above +0.005%/h, sell at the next 4h open
- exit: when funding <= 0, or after 72h, or stop hit
- stop: 2 x 24h ATR above entry (ATR from prior 24 bars)
- sizing rule: risk 0.5% of equity to the stop (the desk's limits apply on top)
- one position per market; no adds
- what would make me abandon this: no edge after fees on 12 months of data across 3 markets
```

If a rule needs "it depends", it is not a rule yet. Do not proceed to code.

### Status and promotion

`status` is the one line the autonomous cycle reads. `draft` is being written or backtested and produces no proposals. `paper` is evaluated on testnet only. `live` is evaluated on whatever network `autonomy.json` names, and its signals become proposals with `origin: strategist:<name>`. Since the strategy-research release the lab's output is a strategy folder in the shared contract (`RULES.md` with `status`, `share` and optional `allowed_markets` in frontmatter, plus `params.json` for the shared factor engine), and no `paper` or `live` folder trades until `scripts/strategy_review.py` has written it a signed, eligible `review.json` against `template/strategy-criteria.json`; editing either file voids that review. The Strategist may set `paper` on an eligible folder; `live` is written by the user alone, into `RULES.md` with the date and the review it rests on, and the Strategist recommends it with the numbers and never writes the word. A strategy whose rules change goes back through the review. The whole ladder, the parameter space and the anti-overfitting rules are in `desk-strategy-research`.

### When the idea comes from outside

Most ideas arrive as a claim, not a rule: a repository of indicator settings, a thread with a chart, a video, a screenshot of an equity curve. A claim is a candidate for `RULES.md`; it is never a result the desk inherits. Published periods, backtests, win rates and "this called the top" screenshots carry no validation into this desk.

Before an imported claim becomes a `draft` thesis, the user and the Strategist freeze all of it, in writing:

1. Instrument and venue. A Hyperliquid perp does not inherit an equity-index or spot claim.
2. Timeframe and how a bar is closed; which session, which exchange's clock.
3. Price field and the exact formula, including how the first values are seeded.
4. The transition rule and every abstention case, not just the entry.
5. Next observable entry, signal expiry, mandatory stop, target and time exit.
6. Costs, funding, spread, slippage and what happens to a rejected or partial fill.
7. The full family the claim came from: every parameter set, asset and timeframe that was tried before this one was presented. That count is the multiplicity correction below.
8. Chronological in-sample and out-of-sample boundaries and an untouched holdout.
9. A prospective paper-trade duration agreed before the first run.

Anything the source does not supply is missing, not implied. If the source cannot supply enough for a complete rule, say so plainly and record it: the claim stays an idea, and the desk does not fill the gaps with plausible defaults. Record the source with an exact commit, URL and retrieval date in `RULES.md`, so a later reader can see what was actually claimed and what the desk had to invent.

## 2. Data

Candles via `candleSnapshot` (`hyperliquid-market-data`). Only the most recent 5000 candles per interval exist, so the interval sets the lookback: about 208 days of `1h`, 2.3 years of `4h`, 13 years of `1d`. Funding via `fundingHistory` (hourly, paginate by `startTime`). Save to CSV under `data/` with the request recorded in `data.md`, and check gaps and duplicated timestamps before using the file. Newer markets have shorter histories still.

## 3. Backtest honestly

Keep it simple and readable; a single Python file the user can follow beats a framework. Requirements:

- **No look-ahead.** Signals at bar `t` use only data up to and including `t`; execution at `t+1` open (or `t` close, stated).
- **Costs.** Taker and maker fees at the account's tier (`userFees` or the published schedule), funding paid or received each hour the position is open, and slippage per side (default a few bps, or from the Market Analyst's depth read for the intended size).
- **Out-of-sample.** Hold back the most recent 15-25% of the period untouched until the rules and parameters are frozen. Report in-sample and out-of-sample separately.
- **Looking at the holdout spends it.** Once the out-of-sample result has been seen, that data is no longer out of sample, whatever it said. A rule that fails and is then adjusted and re-run on the same window has no honest out-of-sample evidence left: the failed run is discovery data, and the next test needs a window nobody has looked at, or fresh forward data. Record in the run file how many times the holdout has been read. If the answer is more than once, the strategy is in-sample only and the run file says so.
- **Parameters and multiplicity.** Record every parameter and how it was chosen, and keep every variant that was run, including the ones that failed. The number that matters is how many distinct rules, parameter sets, assets and timeframes were tried in total before this one was reported, and it includes the trials the idea's original source ran. Search hard enough over a fixed history and something will look profitable by chance. State the trial count next to the result; when it is more than a handful, treat a marginal edge as unproven rather than small, and expect the best-looking variant to be the luckiest rather than the best.
- **Position accounting.** Sizes from the sizing rule and the stop; PnL in R and USD; equity curve; drawdown from the equity curve.

Report per run:

```
run 2026-08-16-1540 | funding-fade-v1 | in-sample 2025-01-01..2026-07-31 | out-of-sample 2026-08-01..2026-08-15
trades 58 (IS) / 6 (OOS) | win 41% / 50% | avg win 1.9R / 1.6R | avg loss 1.0R / 1.0R
expectancy 0.19R / 0.30R | max DD 9.4% / 2.1% | fees+funding 31% of gross PnL
expectancy 5th pct 0.02R (block bootstrap, 2000 resamples, 10-trade blocks) | profit factor 1.31
trials 9 (3 stop multipliers x 3 markets) | holdout reads 1 | verdict: WEAK - forward test before believing
caveats: stop multiplier chosen from {1.5, 2, 3}; slippage 5 bps assumed; SOL history shorter than others
```

No annualised return headline. Distributions and costs are the result.

**Report an interval, not a point.** A mean expectancy computed once over one path is a single draw, and 58 trades is a small sample with autocorrelated returns. Resample the trade sequence in contiguous blocks (a few thousand resamples, blocks long enough to keep streaks intact), take the 5th percentile of mean expectancy, and report that lower bound beside the mean. If the lower bound sits at or below zero, the honest verdict is "no demonstrated edge", not "a small edge" - and that is true no matter how good the mean looks. Report the verdict as one of PASS, WEAK or REJECTED, and keep rejected runs: a strategy the lab killed is the lab working.

## 4. Sanity checks before believing anything

- Flip the sign of the entry rule: does the mirror strategy also "work"? Then you are measuring drift, not edge.
- Shuffle entry dates within the sample: how often does random timing beat the strategy?
- Remove the best two trades: does the result survive?
- Trade count under 30 in-sample: report as "not enough evidence", not as a result.
- Does the result depend on one market or one month?
- Double the assumed slippage and fees: does the edge survive? An edge that only exists at optimistic costs is a cost assumption, not an edge.

Write what you checked into the run file.

## 5. Paper trade on testnet

When the user wants to see it live, they set `status: paper` and the desk runs on testnet (`autonomy.json` with `mode: testnet`). Each cycle of `desk-autonomous-loop` evaluates the rules on the scan exactly as written and opens a **proposal** (`HG-...`, `origin: strategist:<name>`) for each signal, with the rules file cited as the idea. The Risk Manager sizes it, the policy gate approves or refuses it, `desk_send.py` sends it on **testnet**, the Trade Reviewer reviews it. Same cycle, same files, play money. In a supervised session the Strategist may run the rules by hand and open the proposals itself. The Strategist never sends orders and never asks another role to skip a stage "because the rules said so".

After a set number of paper trades agreed with the user (20 is a common choice), the Trade Reviewer's numbers and the backtest are compared side by side. If the user then promotes it to `live`, nothing else on the desk changes: the cycle trades it within the same limits, the same gate and the same rate caps as everything else.

## 6. The shipped engine strategy

`strategies/hg-systematic/` is the one strategy the desk ships: a cross-sectional factor model over the liquid perp universe, run not by the cycle but by the deterministic engine (`scripts/strategy_engine.py`, described in `desk-strategy-engine`). Its status line means exactly what it means here: `draft` observes, `paper` trades on testnet only, `live` trades on whatever network the policy names, and only the user changes it. Its backtester is `scripts/engine_backtest.py`, which runs the engine's own signal and sizing code on real hourly candles and funding, and its record is `BACKTEST.md` beside the rules, read with the same standards as section 4. The lab's own backtests for the user's ideas remain the Strategist's, in `backtest.py` and `runs/`; the Strategist reads the engine's decisions and the backtest, drafts parameter changes for the user as a document, and never edits `params.json` or the status line.

## 7. Abandon cleanly

If it does not hold up: `POSTMORTEM.md` with the data, the runs, and one paragraph on why. Post the conclusion to the user plainly. That is a good outcome for the lab.

## Never

- Never present a strategy as the user's when it is the Strategist's own; the Strategist's hypotheses go through `desk-strategy-research`, with the hypothesis written before the numbers, and "what works" is never a suggestion.
- Never quote a backtest return without trade count, drawdown, costs, the out-of-sample split and the trial count.
- Never carry an imported claim's published results into this desk as evidence. The desk's evidence is what the desk ran.
- Never send an order, on any network. Signals are proposals; the cycle, the gate and the sender do the rest.
- Never write `status: live` or edit a live strategy's files, never hand-write `review.json`, and never let a `draft` or `paper` strategy produce a mainnet proposal.
