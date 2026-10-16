---
name: watchlist-brief
description: Produce a concise pre-market (morning) or after-close summary of a US stock watchlist - price and % change, RSI, trend, distance to stop and targets, biggest movers, upcoming earnings, and any alerts. Use when the user asks for a "morning brief", "market recap", "how did my watchlist do today", or on a scheduled morning/close run.
---

# Watchlist Brief (morning / close)

Informational summary only - **not financial advice; no trade suggestions or order placement.**

## Steps
`scripts/` ships next to this SKILL.md after `npx skills add`. Run from this skill folder, or from a git clone.

1. Determine context with `python3 scripts/market_calendar.py`. Morning brief ~08:30-09:25 ET; close brief after 16:05 ET. On holidays/weekends, say the market is closed and give the next session. After the bell the alerter evaluates last regular close and labels it — do the same in the brief.
2. Generate the table: `python3 scripts/brief.py --kind morning` (or `--kind close`). Columns: Ticker | Price | Chg | RSI14 | Trend (SMA50 vs SMA200) | To stop | To target 1. "To stop" is remaining cushion (positive = room left); shorts use stop-minus-price. Earnings dates in the footer are upcoming only (Yahoo calendar/HTML, Nasdaq analyst page, then Finnhub/AV if keyed).
3. Run `python3 scripts/alerts.py --dry-run --format json` to list conditions currently true without consuming cooldowns; mention notable ones. After hours this uses last regular close (no `--force-session`). Use `--force-session` only on weekends/holidays if you still want to evaluate.
4. Optionally add 1 headline per ticker that moved > 3% or has earnings within 7 days (web search, or `tickertick`/news tools if available). Cite sources; never fabricate news.
5. Write the brief:
   - **Headline** (one sentence: the overall picture of the list).
   - The table.
   - **Watch today / tomorrow**: earnings, tickers within 3% of stop or target, gap moves.
   - Data source + delay note, and "Informational only - not financial advice."
   Keep it under ~250 words unless asked for more.

## Morning vs close
- **Morning**: use prior close as baseline; mention pre-market moves only if the data source returns them (label as pre-market).
- **Close**: day's change, closing levels vs stops/targets, anything that triggered today, what's on tomorrow's calendar.

## Tone
Neutral and factual: "TSLA is 2.1% above its stop" - not "you should sell TSLA".
