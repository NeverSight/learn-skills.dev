---
name: desk-strategy-engine
description: The systematic strategy engine that trades the liquid Hyperliquid perp universe without an LLM in the loop per trade - the hg-systematic factor model (momentum, carry, reversion, breakout, open-interest change, BTC regime), the dynamic top-20 universe, the one-minute risk clock and four-hour decision clock, the drawdown risk ladder and the thin-book deferral, real fees from userFees, how tickets reach the gate and sender, the backtester on 1h, 4h and daily bars and its honest record, engine state files, and how the agent roles supervise it. Use when running, promoting, debugging, backtesting or explaining the engine, or when anyone asks what "high frequency" means on this desk.
license: MIT
metadata:
  version: "1.1.0"
  author: SWC Studio
  category: desk
---

# Strategy engine

The desk's agents are good at evidence, judgement and review and bad at doing the same arithmetic every minute for months. The engine does the arithmetic. It is deterministic Python (`engine/` and `scripts/strategy_engine.py`, standard library only), it runs as a service on the desk computer, and it produces tickets in exactly the shape the Risk Manager would: the gate checks them, the sender sends them, the agents supervise. It has no other path to the exchange.

## 1. What "high frequency" means here

Not what the phrase means on an exchange with co-location. The engine runs a one-minute clock for risk (protection, exits at the exchange stop, reconciliation, halts) and a four-hour clock for decisions (entries and signal exits). The backtest in `template/strategies/hg-systematic/BACKTEST.md` shows why: an hourly decision clock on this fee schedule turned 10,000 USD into 5,400 in seven months, almost entirely fees and stop churn. The desk trades as fast as the evidence says it can afford to, and says so.

## 2. The strategy: hg-systematic

Rules in `template/strategies/hg-systematic/RULES.md` (copied to `<desk-root>/strategies/hg-systematic/`), parameters in `params.json`, evidence in `BACKTEST.md`. In one paragraph: rank the top 20 perps by open interest that pass liquidity floors; on hourly closed bars compute cross-sectional z-scores of vol-normalised momentum (48h and 168h), funding carry (72h), and short-horizon reversion (24h EMA in ATR units); combine 0.5/0.3/0.2; halve risk when BTC vol is in its top 15% and halve the slots against BTC's 96-hour trend; every four hours exit what crossed zero (after a 24-hour minimum hold) or aged past 168 hours and enter what scores past plus or minus 1.0, IOC at the mid moved by the slippage bound with a 3 ATR stop grouped with the entry; size on the stressed stop to the policy's risk per trade, capped by a 1% daily-vol target, the notional cap and margin.

`status:` in `RULES.md` is the switch: `draft` observes only, `paper` trades while the policy is on testnet, `live` trades on whatever network the policy names. The engine refuses `paper` on mainnet, and it refuses `live` unless `strategies/<name>/paper-record.json`, written and signed by `scripts/paper_record.py` for the current review, says `ready`.

`params.json` also carries the execution parameters: `execution_style` (`maker-first`, the shipped default, or `taker`), `maker_offset_bps` and `maker_wait_s`, which the engine copies into each entry ticket's `execution` block for the sender, and `maker_fee` and `maker_fill_rate` for the backtester, where the fill rate is a stated assumption, not a measurement (`desk-execution-protocol`, `desk-operations`). When `autonomy/execution-stats.json` (written by `scripts/execution_stats.py`) carries a `recommended` block for the coin, the engine applies that offset and wait to the new entry ticket instead, as `execution_override`; `params.json` itself is never changed by it.

The factor model has five factors since v2.4.0. Beside momentum, carry and reversion, `breakout` scores the close's position relative to the prior `breakout_hours` high-low channel in ATR units (zero inside the range), and `oi_change` scores the change in open interest over `oi_change_hours` (default 24), read from `data/oi-<network>.jsonl`, which the engine appends on every universe refresh. Both are at weight 0 in `hg-systematic`, so its record is unchanged; `hg-breakout` uses the first. Until enough OI history exists for a coin, the `oi_change` weight is renormalised away rather than scored as zero, so a new desk is not quietly trading a factor it cannot compute.

Two things sit between a score and a ticket, both from `autonomy.json` and both able only to shrink. The **risk ladder** (`limits.risk_ladder`, `engine/risk.py`): the desk records the equity peak per network in `autonomy/equity-peak-<network>.json`, and when drawdown from that peak crosses a rung (default 0.5 at 3%, 0.25 at 6%) the engine multiplies its gross exposure by the rung's scale, the gate multiplies the per-trade budget by the same scale, and the heartbeat carries `ladder_scale` and `drawdown_pct`. The **liquidity check** (`limits.min_depth_multiple`, default 20): before an entry ticket is written the engine reads resting depth within 10 bps on the entry side (`engine.data.l2_depth`) and, when it is below the multiple times the intended notional, defers the entry with a log line naming both numbers; the decision stays open and is retried each tick for `limits.entry_retry_minutes` (default 30), then marked done until the next clock. A ticket that is written records `engine.depth_usd_10bps`. Fees in the ticket come from `autonomy/fees.json`, the account's real taker rate as `desk_send.py` last read it from `userFees`, or the 0.045% default until the first send writes the file.

hg-systematic is the shipped example, not the only strategy the engine runs. Since the strategy-research release the engine loads every `strategies/<name>/` folder (`engine/strategies.py`): a strategy is `RULES.md` (frontmatter `status`, `share`, optional `allowed_markets`) plus `params.json` for the same factor code, and it runs only when its status is `paper` or `live` **and** its `review.json`, written by `scripts/strategy_review.py` against `template/strategy-criteria.json`, verifies: same bytes as the two files, signed with this desk's gate key, verdict `eligible`, younger than 14 days. Editing `RULES.md` or `params.json` voids the review. Each runnable strategy gets its slots from `share` of the policy's `max_positions`, trades only its own universe subset, keeps its own decision clock, and owns the positions it opened; the ticket's `origin` is `strategist:<name>`. Anything else is treated as draft and the reason is listed once under `skipped` in the heartbeat. The Strategist may set `paper`; `live` is the user's word alone (`desk-strategy-research`).

## 3. Running the engine

```bash
python3 /workspace/hypergrok/scripts/strategy_engine.py --desk-root /workspace/trading-desk --once --dry-run   # compute, print, write nothing to the gate
python3 /workspace/hypergrok/scripts/strategy_engine.py --desk-root /workspace/trading-desk --once --observe   # gate every ticket, send none
python3 /workspace/hypergrok/scripts/strategy_engine.py --desk-root /workspace/trading-desk --loop --interval 60
```

As a service: `deploy/hypergrok-engine.service` (systemd), `deploy/Dockerfile` and `deploy/docker-compose.yml`, with `HYPERLIQUID_NETWORK`, `HYPERLIQUID_ACCOUNT_ADDRESS` and the key in the environment from `deploy/engine.env.example`. The engine needs only the standard library; `desk_send.py`, which it calls as a subprocess, needs the Hyperliquid SDK.

One tick, in order: load and validate the policy (mode `off` ends the tick); read the halt file; read the strategy status and params; refresh the universe every 15 minutes (`autonomy/universe.json`, ranked on mainnet liquidity, intersected with the policy's `allowed_markets` unless it is `["*"]`); read `clearinghouseState`, `frontendOpenOrders` and `allMids` (three consecutive failures halt a trading desk); adopt any position the engine did not open; log vanished positions as `realised_gain` or `realised_loss` events; write a `protect` ticket for every position without a resting stop and send nothing else while one exists; refresh candles (every five minutes) and funding (hourly); on the decision clock score the universe, plan exits and entries, write each as `proposals/<id>.ticket.json` plus a proposal markdown, run `policy_gate.check`, and on PASS call `desk_send.py` once. Exit code 3 from the sender (unknown result) halts the desk and ends the tick.

## 4. Files the engine owns

| File | What it is |
| --- | --- |
| `autonomy/engine-state.json` | held positions with open time, ticket id and stop; last refresh times; today's ticket sequence; cached funding |
| `autonomy/engine-heartbeat.json` | status (`off`, `observing`, `trading`, `halted`, `unavailable`, `policy-invalid`), counts for the tick, the plan and top scores |
| `autonomy/engine.log` | one line per event, UTC |
| `autonomy/universe.json` | the coins the engine may trade; the gate reads it when the policy says `["*"]` and treats it as stale after six hours |
| `data/<network>-<coin>-1h.json` | candle cache, extended incrementally, never invented (`-4h` and `-1d` caches appear when the backtester runs on those bars). Every read goes through `engine/data.py` `post_info`, which retries HTTP 429, 502, 503 and 504 with backoff (2, 5, 12 and 30 seconds) before raising `DataError`; other errors are not retried |
| `data/oi-<network>.jsonl` | open interest per coin, one line per universe refresh; the `oi_change` factor reads it |
| `autonomy/equity-peak-<network>.json` | the highest equity seen on that network; the gate and the engine raise it, nothing lowers it; the risk ladder measures drawdown from it |
| `autonomy/fees.json` | the account's taker and maker rates as `desk_send.py` last read them from `userFees`, with the time; the engine sizes on the taker rate |
| `autonomy/execution-stats.json` | per-market post and fill counts, fill rate and the `recommended` maker offset and wait, written by `scripts/execution_stats.py`; the engine applies `recommended` to new entry tickets |
| `proposals/HG-*.ticket.json`, `.md` | tickets and their proposal files, `origin: strategist:<strategy name>` |
| `strategies/<name>/review.json` | the signed verdict of `scripts/strategy_review.py`; read by the engine, written only by the script |
| `strategies/<name>/paper-record.json` | the signed comparison of testnet trades with the backtest, written only by `scripts/paper_record.py`; the engine requires `ready` before it runs a `live` strategy |
| `autonomy/dashboard.html` | the read-only page `scripts/desk_dashboard.py` renders from these files; it refreshes itself every minute and cannot act |
| `autonomy/events.jsonl` | engine events (`realised_gain`, `realised_loss`, demotions and the rest), each carrying `strategy`, `hold_hours`, `exit` and `network`; the paper record and the Trade Reviewer read them |
| `autonomy/alerts.jsonl` | one line per alert (halt, unknown send, repeated unavailable, demotion); the same text is posted to `HYPERGROK_ALERT_WEBHOOK` when it is set |
| `autonomy/metrics.prom` | Prometheus text metrics rewritten each tick: up, status, positions, open risk, tick counts |

The engine never writes `autonomy.json`, `risk-limits.md`, `gate.key`, `sends.jsonl` or `HALT` except through `kill_switch.py halt`.

## 5. The backtester

```bash
python3 /workspace/hypergrok/scripts/engine_backtest.py --desk-root /workspace/trading-desk --hours 5000 --top 20 --ablate
python3 /workspace/hypergrok/scripts/engine_backtest.py --desk-root /workspace/trading-desk --hours 5000 --bar-hours 4 --top 20   # about 833 days
```

Same signal and sizing code as the live engine, fills at the next bar's open with slippage and taker fees both ways, stops checked against each bar's range and filled worse than their trigger, funding accrued hourly from `fundingHistory`, the risk ladder applied from the same `engine/risk.py` the gate uses (the summary reports how many bars it was active), an in-sample / out-of-sample split, per-factor ablation over the active factors (`--ablate`: each non-zero factor removed, then each alone), and a saved JSON of every trade. `--bar-hours` is 1 (about 207 days on Hyperliquid), 4 (back to 2024-05) or 24 (to 2020); the hour-denominated parameters are converted to bars. It reports a distribution and refuses to be a headline: read `BACKTEST.md` for the sweep that produced the defaults, for the row two lines away that loses 32% on the same data with different weights, and for the 4-hour, 833-day run (+13.47%, Sharpe 0.83, maxDD -7.06%) that is a longer sample of the same one strategy, not a forecast. Rerun it before changing any parameter of a live strategy, and change that `params.json` by editing the file yourself; the engine and the agents never do. `strategy_review.py` wraps the same backtest in the written criteria and signs the result; its criteria include a recent-window check (the last `recent_window_days` must return no worse than `recent_min_return_pct`), a `history-complete` check that fails the review when any coin in the ranked universe could not be read, a `long-history` check on 4-hour bars and a `wide-universe` check on the top 40, all on a universe pinned by the criteria's `universe_floors` rather than the live policy's, and `strategy_rereview.py` reruns it weekly and demotes a strategy one rung when it fails (`desk-strategy-research`). `scripts/strategy_correlation.py` reads the daily curve each review stores and prints the correlation between strategies; read it before changing any `share`.

## 6. How the roles supervise it

The agent cycle (`desk-autonomous-loop`) does not decide trades while the engine is running; it runs the same pre-flight, book, reconciliation and journal passes and adds these engine checks:

- Desk Lead: `engine-heartbeat.json` newer than two engine intervals; status matches the policy and the strategy status; halt if the engine is silent while positions are open.
- Risk Manager: every engine ticket in the last cycle was gated (the `## approval` section carries a gate block), the book's open risk agrees with the sum of engine stops, no position is unprotected, the ladder scale in the heartbeat matches the `risk-per-trade` detail in the gate blocks, and the taker rate in `fees.json` matches its own `userFees` read.
- Execution Trader: every `sends.jsonl` entry has a reconciled `.execution.json`; unknown results follow playbook A; deferred entries (`thin book` lines in `engine.log`) are listed, not chased.
- Strategist: reads the decision lines in `engine.log`, compares regime and top scores with the market scan, and writes one paragraph of interpretation to the journal, naming any entry deferred for depth and whether the ladder was in force; proposes parameter changes to a live strategy as a draft for the user, never applies them. Once a day it also runs the research loop in `desk-strategy-research`: a new hypothesis becomes a new folder, `strategy_review.py` decides whether it is eligible, and an eligible one may be set to `paper` on testnet.
- Trade Reviewer: journals the cycle, grades closed engine trades on process (was the gate block clean, was the stop resting, was the exit the rule's) separately from outcome, and reconciles the engine's `realised_*` events against `userFills`.

A supervising agent may halt the engine's desk. It may not resume it, edit a live strategy's parameters, write `status: live`, or write a ticket of its own while the engine is trading; a discretionary idea goes to the user as a proposal draft with `status: gate` left empty.

## Never

- Never call the engine "high frequency" without the sentence that explains the clock and why.
- Never quote the backtest as expected return; quote the drawdown, the trade count and the sensitivity in the same breath.
- Never write `status: live`, edit a live strategy's `params.json`, or widen the universe floors from an agent session.
- Never hand-write `review.json`; only `strategy_review.py` writes it, and a forged one fails the signature.
- Never run two engines against one desk root; the state file assumes one writer.
- Never let the engine keep trading through an `unavailable` read, an unknown send, or a naked position: it halts, and the log says why.
