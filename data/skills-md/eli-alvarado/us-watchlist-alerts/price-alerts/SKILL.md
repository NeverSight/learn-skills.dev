---
name: price-alerts
description: Check a US stock watchlist for price alerts - price above/below, % daily move, gaps, 52-week highs/lows, moving-average crosses, RSI, ATM IV, volume spikes, intraday range, stop/target hits, and upcoming earnings - with dedupe, cooldowns, NYSE market hours, optional ntfy/Slack/webhook delivery, pre/after-market, holidays and US/Eastern time. Use when the user asks "any alerts?", "check my watchlist", "alert me if AAPL drops below 200", "send alerts to ntfy", or when running a scheduled/heartbeat check.
---

# Price Alerts (US markets)

Evaluates alert rules from the watchlist (see `watchlist-manager`) against fresh quotes and reports **only new** alerts.
**Not financial advice. Never place, modify or cancel orders** - even if an alert fires, even if a broker tool is connected, unless the user explicitly confirms that specific order in this conversation.

`scripts/` ships **next to this SKILL.md** (copied by `npx skills add`). Run from this skill folder, or from a git clone of the repo (root `scripts/` is the same files).

## Run it
```bash
python3 scripts/watchlist.py init                                                         # copy examples/watchlist.json if missing
python3 scripts/quickstart.py                                                             # offline fixture demo (labeled, not live)
python3 scripts/alerts.py --watchlist watchlist.json --state .alert_state.json           # text output
python3 scripts/alerts.py --format json                                                    # machine-readable
python3 scripts/alerts.py --force-session                                                  # evaluate on weekends / holidays too
python3 scripts/alerts.py --dry-run                                                        # don't update cooldown state
python3 scripts/alerts.py --notify                                                         # also deliver via WATCHLIST_NOTIFY sinks
python3 scripts/market_calendar.py                                                         # current ET session
```
Output: `ALERT <message>` lines, or `no new alerts`, or `market closed, showing last regular close` after the bell (last regular print; no `--force-session` needed). Weekends and full-day holidays stay silent (`market closed (weekend|holiday). Next session YYYY-MM-DD`) unless `--force-session`. Data errors go to stderr as `WARN` (including `earnings_error` / `iv_error`). `NOTIFY <sink>` confirms delivery; sink failures are `WARN notify …` and must not abort the check. Never treat a notify sink as a broker.

## Alert types
| type | value | fires when | kind |
|---|---|---|---|
| `price_above` / `price_below` | price | last >= / <= value | level |
| `stop_hit` | price (default: ticker `stop`) | long: last <= stop; short: last >= stop | level (implicit if `stop` set) |
| `target_hit` | - | last crosses any `targets` entry | level (implicit if `targets` set) |
| `pct_change_up` / `pct_change_down` / `pct_move` | % | **last** vs prior close (after hours: last regular close). A recovered session low does **not** fire | daily |
| `gap_up` / `gap_down` | % (default 2) | open vs prior close | daily |
| `new_52w_high` / `new_52w_low` | - | last beyond prior 252-session range | daily |
| `near_52w_high` / `near_52w_low` | % (default settings.near_52w_pct) | within value% of 52w extreme | daily-ish (level latch) |
| `golden_cross` / `death_cross` | `fast`, `slow` (50/200) | SMA fast crosses slow on latest bar | daily |
| `cross_above_ma` / `cross_below_ma` | MA length (default 50) | last close crosses its SMA | daily |
| `rsi_above` / `rsi_below` | RSI level; optional `period` (14) | Wilder RSI on daily closes | level |
| `iv_above` / `iv_below` | IV percent | unofficial Yahoo ATM IV (nearest expiry); skip if missing/0 | level |
| `volume_spike` | multiple (default 2.0) | today's volume >= value x 20-day avg | daily |
| `earnings_within` | days (default 3) | next earnings date within N days | daily |
| `intraday_range_pct` | % | `(day_high-day_low)/prev_close`; skip if high/low missing | daily |
| `intraday_low_pct` / `intraday_high_pct` | % | **opt-in** session low/high vs prior close. Catches a −3% low that recovered into the close | daily |
| `intraday_extreme_pct` | % | alias: expands to both `intraday_low_pct` and `intraday_high_pct` | daily |

Any rule may set `cooldown_minutes` to override `settings.cooldown_minutes`.

**Default % checks use last print vs prior close** (`pct_change_*` / `pct_move`). They do not look at the session high/low. If the user says “alert me if it drops 3% today” and they mean the print that traded through 3% even if it bounced, add `intraday_low_pct` (or `intraday_extreme_pct`). Do not add those unless they ask — they are opt-in.

## Anti-spam rules (implemented in `scripts/alerts.py`, state in `.alert_state.json`)
- **Level alerts latch**: once fired they stay silent until price moves back through the level by `rearm_pct` (default 0.5%). A stock hovering at $240 never pings repeatedly. `iv_*` rearms when ATM IV no longer breaches the threshold.
- **Daily-event alerts** fire at most once per trading day per ticker/type.
- **Cooldown** (`cooldown_minutes`, default 240) applies to every re-fire.
- **Cap** of `max_alerts_per_run` (default 20). Alerts past the cap are **not** written to state, so they can fire on the next run. If many fire, summarize ("7 alerts, 4 on TSLA") rather than dumping walls of text.
- If the state file is missing or corrupt, start fresh but warn the user that duplicates are possible on this run.
- Each `targets[]` level is its own latched `target_hit` (T1 firing does not hide T2).

## Market hours (America/New_York, handled by `scripts/market_calendar.py`)
- Pre-market 04:00-09:30, regular 09:30-16:00, after-hours 16:00-20:00 ET; early-close days (day after Thanksgiving, Christmas Eve, July 3 when a weekday) close 13:00 with after-hours to 17:00.
- NYSE holidays: New Year's (not observed when Saturday), MLK, Presidents', Good Friday, Memorial, Juneteenth, Independence, Labor, Thanksgiving, Christmas (Sat -> Fri, Sun -> Mon). Unscheduled closures: bundled `data/holidays_overrides.json`, `NYSE_EXTRA_CLOSURES` / `settings.extra_closures`, and (with Alpaca keys) weekdays missing from the official calendar. Mention it if quotes look stale on a weekday the calendar thinks is open.
- `settings.sessions` controls when **extended-hours quotes** are treated as live. Default `["regular"]`. After the bell (or pre-open / overnight) on a trading day, the script still evaluates the last regular close and labels `last_close` — you do not need `--force-session`. Add `"pre"`/`"after"` only if you want to treat extended-hours prints as the live session. Those quotes are thinner and free sources may lag.
- Always state times in ET (add the user's local time if known, e.g. "10:05 ET / 9:05 CT").

## Data sources (`scripts/quotes.py`, auto-fallback in this order)
1. `--fixture` path, if given (tests/demos only).
2. Alpaca snapshot + daily bars, if `ALPACA_API_KEY_ID` **and** `ALPACA_API_SECRET_KEY` are set (official US feed).
3. `yfinance` if installed (`pip install yfinance`).
4. Yahoo public chart API (stdlib, unofficial, best-effort): `query1.finance.yahoo.com`, then `query2`. `prev_close` is `previousClose` or the prior aligned daily bar — after ~20:00 ET a today-row with `close: None` is dropped, not treated as yesterday.
5. Finnhub quote + candles, if `FINNHUB_API_KEY` is set.
6. Alpha Vantage daily, if `ALPHAVANTAGE_API_KEY` is set.

Force one with `--provider` or `WATCHLIST_PROVIDER`. HTTP 429/5xx are retried; failures are tagged `QuoteError`s (provider, HTTP status, hint). Free data can be delayed ~15 min; say so when precision matters.

**Earnings dates** are filled after the quote, first hit: existing field (yfinance/fixture) → Yahoo `calendarEvents` (cookie + crumb) → Yahoo quote HTML → Nasdaq analyst `earnings-date` (free, no key) → Finnhub / Alpha Vantage if keyed. `earnings_source` says which layer won; if none do, `earnings_error` prints a WARN.

**Stale quotes:** `--stale-after` / `WATCHLIST_STALE_AFTER` / `settings.stale_after_seconds` (default 900). During the regular session, warn if `as_of` is older than that. `0` disables.

**ATM IV:** only fetched for tickers with `iv_above`/`iv_below`. Unofficial Yahoo options chain (same crumb), then yfinance if installed. Nearest expiration, ATM call/put average as percent. Not IV rank. Failures set `iv_error` and print a WARN. `python3 scripts/quotes.py AAPL --iv` to inspect.

**Notify (optional):** `WATCHLIST_NOTIFY=ntfy,slack,webhook,desktop,file` and/or `--notify`. See README for env vars. Do not notify on empty/skipped/dry-run. Delivery errors stay warnings.

**Known limits:** unscheduled closures live in `data/holidays_overrides.json` (incomplete) plus env/settings plus an optional Alpaca official calendar overlay (day-cached). Yahoo endpoints are unofficial. See `docs/LIMITATIONS.md`.

**MCP option:** if an `alpaca` MCP server (alpacahq/alpaca-mcp-server) or `tradingview` MCP (atilaahmettaner/tradingview-mcp) is connected, you may use it for quotes/indicators instead of the scripts, then apply the exact same rules and anti-spam logic (read/write `.alert_state.json` in the same format). Use broker MCPs for **read-only** calls only.

## Reporting format
```
🔔 3 new alerts (10:05 ET, regular session, data: yahoo, ~15m delayed)
- AAPL $241.50 is above $240.00  (thesis: services margin; stop $210, T1 $250)
- TSLA down -6.0% today, gapped down -5.0%, volume 3.0x avg
- TSLA reports earnings in 1 day (2026-10-16)
```
Group by ticker, include the stored thesis/stop/target for context, no recommendations. If no alerts: one short line, or stay silent when running on a heartbeat (see `HEARTBEAT.md`).

## Creating alerts from chat
"Alert me if AAPL drops below 200" -> `python scripts/watchlist.py update AAPL --alert price_below:200 --append` (add the ticker first if missing). Confirm the rule back in plain English.
