---
name: desk-operations
description: Running the autonomous desk as a service rather than an experiment - where the API key comes from (environment, secrets-manager command, or a locked-down file, with recipes for 1Password, AWS, GCP, Azure, Vault and Doppler), maker-first execution with taker fallback and what it does and does not save, real fees from userFees and the execution-stats controller that tunes the maker offset and wait per market, the paper-record gate that stands between paper and live, the weekly walk-forward re-review with automatic demotion, the correlation report to read before raising a share, the drawdown risk ladder and the thin-book deferral, the read-only dashboard, alerts and metrics, and the operator checklist. Use when deploying, rotating a key, reading the dashboard, explaining why a strategy was demoted, why size fell after a drawdown or why an entry was deferred, or answering "is this production-ready".
license: MIT
metadata:
  version: "1.0.0"
  author: SWC Studio
  category: desk
---

# Operations

Everything the desk needs to be left alone safely for weeks: a key it never sees in plain text, execution that does not pay the taker fee when it does not have to, a paper record before real money, a re-review that demotes a strategy the moment its own criteria stop holding, a page a human can glance at, an alert that arrives when something needs one, and, since v2.4.0, the account's real fees, a measured fill rate, a risk ladder that shrinks size in a drawdown, and a depth check before every entry.

## 1. The key

`engine/secrets.py` resolves the API wallet key in this order and reports which source it used, never the value: `HYPERLIQUID_PRIVATE_KEY` in the environment; then `HYPERGROK_KEY_COMMAND`, a command run without a shell whose stdout is the key; then `HYPERGROK_KEY_FILE` or `~/.hyperliquid/api-wallet.key`, which must be mode 600 and owned by the running user or it is refused. The key must be a 32-byte hex string; anything else is refused before it reaches the SDK.

Secrets-manager recipes for `HYPERGROK_KEY_COMMAND` (names are examples; keep them in the service's environment file, never in the repository):

| Manager | Command |
| --- | --- |
| 1Password | `op read op://Trading/hyperliquid-api-wallet/private-key` |
| AWS Secrets Manager | `aws secretsmanager get-secret-value --secret-id hypergrok/api-wallet --query SecretString --output text` |
| GCP Secret Manager | `gcloud secrets versions access latest --secret hypergrok-api-wallet` |
| Azure Key Vault | `az keyvault secret show --vault-name hypergrok --name api-wallet --query value -o tsv` |
| HashiCorp Vault | `vault kv get -field=private_key secret/hypergrok/api-wallet` |
| Doppler | `doppler secrets get HYPERLIQUID_PRIVATE_KEY --plain` |

The command runs with the service's own identity, so the manager's access policy is the real boundary: give that identity read on that one secret and nothing else. `desk_send.py` calls the resolver only at the moment it signs; the engine, the gate, the dashboard and the agents never do. Rotation is `hyperliquid-setup` section 6 plus one edit in the manager.

## 2. Maker-first execution

An entry ticket with `execution.style: maker-first` (the engine sets it from `params.json`; the shipped strategy ships with it on) is sent as a post-only `Alo` limit at the mid moved inside by `maker_offset_bps`, with its stop grouped as before. The sender then polls the order by cloid for `maker_wait_s`. Filled: done, at maker fee. Not filled: cancel by cloid, protect any partial fill with a standalone stop for exactly the filled size, and send the remainder as the bounded IOC the ticket would have been, with its own stop, unless the mid has moved past the ticket's slippage bound, in which case the remainder is dropped and the record says so. Every step is in `proposals/<id>.execution.json` under `steps`. All of it is one approval: the same ticket, the same cloid family, the same expiry discipline.

What it saves: the taker fee and the crossing on the fraction that fills passively. On the shipped strategy's 208-day backtest, assuming half of entries fill as maker, fees drop from 137 to 114 USD on 10,000 and the return moves from +15.5% to +16.4%; at 80% fills, +16.7%. That is real and it is one point, because the strategy already trades slowly. It matters far more for anything faster, which is exactly the kind of strategy the review tends to reject. The backtester's `maker_fill_rate` is an assumption, stated in `params.json`, not a measurement; the paper record measures the real fill rate from `steps`.

**Real fees.** Each run of `desk_send.py` asks `userFees` for the account's taker and maker rates and writes `autonomy/fees.json` (`taker`, `maker`, `at`, `source: userFees`); a failed read leaves the previous file in place. The engine sizes every ticket on that taker rate rather than the 0.045% base-tier default, so the stressed stop and `risk_usd` reflect the tier the account is actually on. A negative maker rate is a rebate, and the controller below treats it as a reason to wait longer for a maker fill.

**Measuring execution.** `scripts/execution_stats.py --desk-root <root>` reads the `steps` of every maker-first execution record and, per market, counts posts, full and partial fills, taker fallbacks and dropped remainders, the median seconds to a fill and the offset and wait used, and writes `autonomy/execution-stats.json`. For any market with at least 5 posts it adds a `recommended` block: the fill rate (a partial counts as half) is steered toward a band of 45 to 75% by moving `maker_offset_bps` one step of 0.25 bps toward the mid when fills are scarce or away from it when they are plentiful, within 0.25 to 4.0 bps; `maker_wait_s` grows by 15 s when the median fill arrives later than 70% of the wait, and by another 15 s when `fees.json` shows a maker rebate, within 15 to 180 s. The engine applies the recommendation to the next entry ticket for that market as `execution_override`; `params.json` is untouched, so the review stays valid. The rule is deliberately slow, one step per run and clamped, so a handful of trades cannot swing it; run it weekly, or after a market has five or more fills, and read the table before trusting the recommendation. `--json` prints the file.

## 3. The paper-record gate

`status: live` is refused by the engine unless `strategies/<name>/paper-record.json` exists, is signed for the strategy's current review, and says `ready`. `scripts/paper_record.py --desk-root <root> --strategy <name>` writes it from the engine's realised events on testnet since the review: at least `paper.min_trades` closed trades over `paper.min_days`, win rate within `win_rate_tolerance_pct` points of the backtest, average hold within `hold_hours_tolerance_pct`, stop rate within `stop_rate_tolerance_pct` points, and paper drawdown no worse than `max_drawdown_multiple_of_backtest` times the backtest's. The block lives in `template/strategy-criteria.json`. A paper record that does not resemble the backtest is the most useful thing the desk can tell you before mainnet: either the market changed or the backtest was wrong, and neither is a reason to go live.

## 4. Walk-forward re-review and demotion

`scripts/strategy_review.py` now also checks a recent window (`recent_window_days`, `recent_min_return_pct`), so a strategy whose last month looks nothing like its history fails even when the whole-period numbers still pass. `scripts/strategy_rereview.py` reruns the review for every paper and live strategy on fresh history and, on a rejection, demotes one rung: live to paper, paper to draft. It is the one path that ever moves a status downward on its own; nothing moves one upward. Each demotion is an event, an alert, and a line in the journal the Trade Reviewer picks up. Run it weekly from cron (`deploy/supervisor-cron.example`); the engine's own 14-day review expiry is the backstop if the cron dies.

**Correlation before share.** `scripts/strategy_correlation.py --desk-root <root>` reads the daily curve stored in every `review.json`, prints the pairwise daily-return correlation between reviewed strategies and the combined equal-weight curve's return and drawdown against each alone. A pair above 0.7 is one bet with two names. Run it before raising any strategy's `share` and before acting on a promotion proposal; it reads only and changes nothing.

## 5. The risk ladder and the liquidity check

Two limits keys in `autonomy.json`, both the user's, both able only to reduce. `limits.risk_ladder` is a list of `{drawdown_pct, scale}` rungs (template: 0.5 at 3%, 0.25 at 6%). The gate and the engine keep the highest equity seen per network in `autonomy/equity-peak-<network>.json`; when drawdown from that peak crosses a rung, the engine multiplies its gross exposure and the gate multiplies the per-trade budget by the rung's scale, and the `risk-per-trade` gate line prints it (`max 0.5% x ladder 0.5 at 3.2% drawdown from peak`). The gate validates the ladder at policy load (drawdowns ascending, scales in (0, 1]) and a malformed one invalidates the policy as a whole. The backtester applies the same rungs, so a review already reflects the ladder. Nothing lowers the peak; size returns as equity climbs back inside a rung.

`limits.min_depth_multiple` (template 20) is the liquidity check: before an entry ticket is written the engine reads the resting depth within 10 bps on the entry side from `l2Book` and, when it is below the multiple times the intended notional, defers the entry with a log line (`deferred, thin book: <available> USD within 10 bps vs <needed> needed`), leaves the decision open and retries each tick for `limits.entry_retry_minutes` (default 30) before marking it done. An unreadable book defers the same way. On any day the log shows repeated deferrals in one market, the question is whether the notional cap is too large for that market, not whether the multiple is too strict.

## 6. Dashboard

`scripts/desk_dashboard.py --desk-root <root>` writes `autonomy/dashboard.html`: policy mode, halt, engine heartbeat age, equity, positions and protection, the universe, the last cycle, an equity line from the start-of-day records, every strategy with its status, review state, backtest, paper record and slots, the last decisions, sends, realised results, alerts and today's journal. It is one file with no external requests, refreshes itself every minute from the file, and cannot act. `--serve 8787` serves the autonomy folder read-only on localhost for a private network or an SSH tunnel; do not expose it, and remember that `sends.jsonl` and the execution records are in that folder. Cron it every ten minutes or run it from the supervising cycle.

## 7. Alerts and metrics

`HYPERGROK_ALERT_WEBHOOK` receives halts, unknown send results, repeated unavailable reads and demotions as plain text; `autonomy/alerts.jsonl` keeps them regardless. `autonomy/metrics.prom` is rewritten each tick with `hypergrok_up`, status, equity, positions, unprotected count, per-strategy slots and the heartbeat time; point a node exporter's textfile collector at it or scrape it from the dashboard server. Alert on `hypergrok_heartbeat_unix` older than three intervals, on `hypergrok_halted`, and on `hypergrok_unprotected_positions` above zero.

## 8. Operator checklist

Before mainnet: the key comes from a manager or a 600 file and `desk_send.py --dry-run` reports the source; `check.sh` and `desk_doctor.py` pass; the policy ceilings are the tight ones; every live strategy has an eligible review younger than 14 days and a ready paper record; the re-review cron, the dashboard cron and the engine service are installed and the heartbeat is fresh; the webhook has received a test alert (`kill_switch.py halt` then the user's `resume`); the user has read a week of journals. Weekly: read the re-review output and the dashboard's strategy table, compare each live strategy's realised exit mix with its backtest, run `execution_stats.py` (or sooner, once a market has five or more fills) and read its table before the engine applies the recommendation, and check that `fees.json` is dated since the last send. Before raising any strategy's `share`, or acting on a promotion proposal: run `strategy_correlation.py` and treat a pair above 0.7 as one bet. On any halt: read `alerts.jsonl` and the last execution record before anything else. After a drawdown: read `equity-peak-<network>.json` and the ladder scale in the heartbeat before asking why size fell.

## Never

- Never put the key in a prompt, a routine, a cron line, a compose file in git, a log, or an exception message.
- Never run the dashboard server on a public interface.
- Never promote a strategy because the re-review passed; passing keeps it where it is.
- Never treat the maker fill-rate assumption in a backtest as measured; the paper record measures it.
- Never disable the re-review to keep a strategy live.
- Never edit `params.json` to match an execution-stats recommendation; the engine applies it per ticket, and the edit would void the review.
- Never raise a `share` without the correlation report, and never add a rung to the ladder that scales above 1.
