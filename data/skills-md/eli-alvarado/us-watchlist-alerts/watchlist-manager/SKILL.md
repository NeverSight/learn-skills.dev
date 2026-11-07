---
name: watchlist-manager
description: Manage a US stock/ETF watchlist file - add, remove, update, list and validate tickers with thesis, entry, price targets, stop, tags, and per-ticker alert rules. Use when the user says things like "add NVDA to my watchlist", "set a stop on AAPL at 210", "what's on my watchlist", "remove TSLA", or "tag these as semis".
---

# Watchlist Manager (US markets)

Maintains a single source-of-truth watchlist file that the `price-alerts` and `watchlist-brief` skills read.
Informational tool only. **Never place, modify, or cancel a trade.** Editing the watchlist is not trading.

## File location
Shared with `price-alerts` and `watchlist-brief`. Survives `npx skills add` reinstall. Do **not** `cd` into this skill folder to run scripts (that folder is replaced on update). Run from the **project root** by path, e.g. `python3 .claude/skills/watchlist-manager/scripts/watchlist.py init`.

1. `$WATCHLIST_FILE` if set.
2. Else `./watchlist.json` in the **project** directory. If cwd is inside `.claude/skills/<name>` or `.agents/skills/<name>` (this folder, or `scripts/`), walk up to the project root and use **that** `watchlist.json` so the skill folder and project root cannot diverge. YAML `watchlist.yaml` works if PyYAML is installed and you pass `--file`.
3. Else `~/.config/us-watchlist-alerts/watchlist.json` (Windows: `%APPDATA%\us-watchlist-alerts\watchlist.json`; or `$XDG_CONFIG_HOME/us-watchlist-alerts/`).
4. A leftover `watchlist.json` inside a skill folder is copied to that destination on first run so reinstall cannot delete it.
5. If none exists, `init` writes an empty valid list at that default path (`init` / `add` / `list` print `using <path>`). Ask before overwriting an existing file.

## Schema (version 1)
```json
{
  "version": 1,
  "settings": { "cooldown_minutes": 240, "rearm_pct": 0.5, "sessions": ["regular"],
                "volume_spike_multiple": 2.0, "near_52w_pct": 2.0, "earnings_days": 3,
                "max_alerts_per_run": 20, "extra_closures": [], "stale_after_seconds": 900 },
  "tickers": [{
    "symbol": "NVDA",            // required, uppercase; class shares as BRK.B or BRK-B
    "side": "long",              // long | short | watch
    "added": "2026-10-15",
    "thesis": "AI datacenter capex",
    "entry": 160.0, "targets": [190.0, 220.0], "stop": 140.0,
    "tags": ["ai", "semis"],
    "alerts": [ {"type": "price_below", "value": 150, "cooldown_minutes": 60} ],
    "notes": ""
  }]
}
```
Alert `type` values and their `value` meaning are documented in `../price-alerts/SKILL.md` (sibling skill after install).
A `stop` implies a `stop_hit` alert and `targets` imply `target_hit` automatically.

## Operations (prefer the script; it validates and writes atomically)
`scripts/` ships next to this SKILL.md after `npx skills add`. Run from the project root by path (or from a git clone; root `scripts/` is the same files):
```bash
python3 scripts/watchlist.py init
python3 scripts/watchlist.py init --example
python3 scripts/watchlist.py init --list-presets
python3 scripts/watchlist.py init --preset mega-cap-tech
python3 scripts/watchlist.py add NVDA --thesis "AI capex" --entry 160 --target 190 --target 220 --stop 140 --tag ai --tag semis --alert price_below:150
python3 scripts/watchlist.py add NVDA --file swing.json --alert price_below:150
python3 scripts/watchlist.py add NVDA --no-verify
python3 scripts/watchlist.py update NVDA --stop 145
python3 scripts/watchlist.py update NVDA --tag megacap --alert rsi_above:75 --append
python3 scripts/watchlist.py remove NVDA
python3 scripts/watchlist.py list [--tag semis]
python3 scripts/watchlist.py show NVDA
python3 scripts/watchlist.py validate
```
`add` looks the symbol up on the Yahoo chart (same default quote path as `quotes.py`). Unknown tickers are rejected (`NVDA is not a known US ticker…`). `--no-verify` / `WATCHLIST_NO_VERIFY=1` skips the lookup when you are offline. If the chart request fails because the network is down, the CLI prints a WARN and **adds the ticker anyway**. `--fixture` / `WATCHLIST_FIXTURE` checks the bundled sample quotes instead — presets work in that mode (the fixture `_default` alias covers built-in preset symbols that are not in the 3-name demo).
If Python is unavailable, edit the JSON by hand following the schema and the validation rules below.

## Workflow
1. **Resolve the ticker.** Uppercase it. If the user gives a company name, confirm the symbol (e.g. "Alphabet" -> GOOGL or GOOG?). Reject non-US listings or say they are unsupported by default data.
2. **Sanity-check with a live quote**: `add` already checks the symbol on the Yahoo chart (skip with `--no-verify`). Run `python3 scripts/quotes.py NVDA` when you want the price printed. If the user's stop is above price for a long (or target below), point it out and ask.
3. **Capture the why.** If no thesis is given, ask once for a one-line reason; store `""` if they decline. Don't invent a thesis.
4. **Suggest, don't impose, alerts.** Reasonable defaults to offer: stop/target levels, `earnings_within: 3`, `pct_move: 5` (last vs prior close). If they want a drop that trades through a % and then recovers, offer opt-in `intraday_low_pct` / `intraday_extreme_pct` and say those use session low/high, not last. Mention `iv_above`/`intraday_range_pct` only if they ask about vol or today's range — ATM IV is unofficial Yahoo, not IV rank. Only add what they agree to.
5. **Write, validate, confirm.** Show the resulting entry (symbol, entry, stop, targets, alerts) in one compact line.

## Validation rules
- Symbol matches `^[A-Z]{1,5}([.-][A-Z]{1,2})?$`; no duplicates.
- `add` also checks the symbol on the Yahoo chart unless `--no-verify` is set. Reject unknown symbols. On network outage, warn and add anyway.
- Built-in presets (`mega-cap-tech`, `index-etfs`, `sector-etfs`, `dividend-staples`) are valid symbol lists; `init --list-presets` prints them.
- `entry`, `stop`, `targets[]` are numbers. For `side: long`, stop < entry; for `side: short`, stop > entry.
- `settings.sessions` if present is a non-empty list of `regular` / `pre` / `after`.
- `settings.extra_closures` if present is ISO dates (`YYYY-MM-DD`) for unscheduled full-day closures.
- Every alert `type` is a known type.

## Listing format
Compact table: Ticker | Side | Entry | Stop | Targets | Tags | Thesis. Add a live price column only if the user asks or you're already fetching quotes.

## Don'ts
- Don't delete tickers without explicit instruction; for "clean up my list" propose removals first.
- Don't give buy/sell recommendations. You may describe levels and risk (e.g. "stop is 12% below entry").
