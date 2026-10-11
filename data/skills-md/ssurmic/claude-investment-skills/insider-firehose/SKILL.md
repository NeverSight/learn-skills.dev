---
name: insider-firehose
description: Real-time SEC Form 4 insider-trading aggregator with Telegram push alerts when officers/directors buy more than $200k of their own stock on the open market. v2.1 adds automatic enrichment — every alert is augmented with company one-liner, P/E + market cap + net cash, 52W price context, and a 0-10 Smart Money Score. Triggers in English ("show today's insider buys", "form 4 today", "who's buying right now", "insider firehose") or Chinese ("今天 insider 怎么样", "今天谁在加仓", "form 4 实时", "内部交易实时").
---

# Insider Firehose — Real-Time Form 4 Aggregator (v2.1)

Pulls the SEC EDGAR Form 4 "current filings" atom feed and pushes a Telegram alert for every open-market purchase ≥ $200k by officers or directors.

**v2.1 (May 2026):** every alert now auto-enriches with a business one-liner, P/E + valuation block, 52W price context, and a 0-10 Smart Money Score. Toggle on/off any time via `/enrich on` or `/enrich off` in Telegram (or `firehose_cli.py`).

## Why this exists

Tools like openinsider.com aggregate Form 4 filings but scrape on a 12-24 hour delay. **This skill pulls directly from SEC EDGAR with a 2-5 minute delay** — same authoritative source, 100-300x faster.

It also enforces the methodology rules from `review-investment-screenshot/SKILL.md`:
- **Form 4 code "P" only** (open-market purchase) — never A/M/F/G/D/C (RSU vest, option exercise, tax withholding, gift, distribution, conversion). Aggregators that conflate these produce false-positive cluster-buy headlines like the 2026-04-01 UNH "10 directors buying" story (all DSU grants).
- **10% holder-only buys skipped** by default. These are often activist funds (Saba Capital) or institutional positions, not officer/director conviction signals.
- **$200k threshold** filters out small qualifying purchases (board minimums, ESPP-style buys).

## Architecture

```
SEC EDGAR atom feed (every 30 min cron, weekdays 9 AM - 7:30 PM ET)
   │
   ▼
form4_firehose.py
   │  pulls feed, dedupes via form4_state.json
   │  for each NEW filing: fetch raw XML, parse <nonDerivativeTransaction>
   │  filter: code == "P", value ≥ $200k, role != pure 10% holder
   │
   ├──► enrichment/ (v2.1, on by default)
   │      pull yfinance: valuation + 52W price + business one-liner
   │      compute 0-10 Smart Money Score from role + value + valuation + price
   │      (non-fatal — if yfinance fails, falls back to basic v2.0 alert)
   ▼
Telegram bot ($TELEGRAM_BOT_TOKEN)
   │
   ▼
🚨🟢 INSIDER BUY — $X.XM
$TICKER (Company) — Owner (Officer/Director/Title)
N,NNN shares @ $X.XX  · [SEC EDGAR ›]
🏢 _One-line business description_ · Sector
📈 Valuation: Cap · P/E · Net cash · Div yield
📊 Price: Now · 1Y · 52W range · vs MAs
⭐ Smart Money Score: N/10 + triggered factors
```

State (which filings we've already alerted on) lives in `scripts/form4_state.json` and is auto-committed by the workflow back to the repo. Cap of 5000 entries (≈ 1 week of Form 4 volume).

User preference (enrichment on/off) lives in `enrichment_config.json` at the firehose root. Telegram `/enrich` commands edit this file via the same GitHub API path as `alerts.json`.

## Files

- `scripts/form4_firehose.py` — core script: fetch + parse + filter + (enrich) + send
- `scripts/firehose_cli.py` — CLI for toggling enrichment on/off + status
- `scripts/enrichment/` — Tier-2 augmentation package (v2.1)
  - `pipeline.py` — entry point `enrich(ticker, filing, total)` + on/off resolver
  - `valuation.py` — P/E, market cap, net cash, dividend yield (via yfinance)
  - `price_action.py` — 50DMA / 200DMA / 52W context
  - `company_info.py` — one-line business description
  - `score.py` — 0-10 Smart Money Score (role + value + valuation + price)
  - `format.py` — assembles enriched Telegram Markdown message
- `scripts/form4_state.json` — accession-number ledger (auto-managed)
- `enrichment_config.json` — user-managed on/off flag (default `enabled: true`)
- `.github/workflows/insider-firehose.yml` — cron + state commit + yfinance install

## Tuning knobs (workflow_dispatch inputs)

| Input | Default | Use |
|---|---|---|
| `min_value` | `200000` | Bump to `500000` or `1000000` if too noisy |
| `include_sells` | `false` | `true` to also alert on sells ≥ 5x threshold |
| `test_mode` | `false` | `true` prints to log instead of Telegram |
| `enrich` (v2.1) | `default` | `on` / `off` override the config file for this single run |

Or run manually:

```bash
TEST_MODE=1 FORM4_MIN_VALUE=500000 python scripts/form4_firehose.py
ENRICH=0 python scripts/form4_firehose.py   # force-disable enrichment
ENRICH=1 python scripts/form4_firehose.py   # force-enable enrichment
```

## v2.1 enrichment — how to toggle

Enrichment is **on by default**. Every alert includes a business one-liner, valuation block, 52W price context, and a 0-10 Smart Money Score.

### Option A: Telegram (recommended — works from your phone)

Send any of these to your alert bot:

```
/enrich           → shows current state
/enrich on        → enable
/enrich off       → disable
/enrich status    → shows current state
```

Chinese aliases also work: `/enrich 开`, `/enrich 关`, `/enrich 状态`.

The webhook commits the new state to `enrichment_config.json` via the GitHub API, and the next cron run picks it up.

### Option B: CLI (from your laptop)

```bash
python scripts/firehose_cli.py --status      # show current state
python scripts/firehose_cli.py --enrich-on   # enable
python scripts/firehose_cli.py --enrich-off  # disable
# then: git add enrichment_config.json && git commit && git push
```

### Option C: One-off via GitHub Actions

Actions → Insider Firehose → Run workflow → `enrich = off` (just for this run, doesn't change the saved default).

## Sample enriched alert

This is what an alert looks like in v2.1 (MKTW · Frank Porter Stansberry's $974,582 director buy on 2026-05-11):

```
🚨🟢 INSIDER BUY — $974,582

Ticker: MKTW  (MARKETWISE, INC.)
🪑 Stansberry Frank Porter
Dir, 10%

51,375 shares @ $18.97
(4 transactions same filing)

[SEC EDGAR ›]

🏢 MarketWise, Inc. operates a content and technology multi-brand platform
   for self-directed investors. · Financial Services / Financial Data

📈 Valuation
  Cap: $48M
  P/E: 10.8 (fwd 90.3)
  Net cash: $47M (99% of cap)
  Div yield: 4.81%
  Rev growth: -7.8% YoY

📊 Price
  Now: $18.06
  1Y: +18.3%
  52W: +34% from low / -17% from high
  vs MA: 50d +8.5% · 200d +9.9%

⭐ Smart Money Score: 4/10
  ✅ Cheap P/E (10.8)
  ✅ Net cash 99% of mcap
  ✅ Dividend 4.8%
```

Compare to the v2.0 basic alert (above the 🏢 line). v2.1 keeps the basic block on top so existing eye-scanning habits still work — enrichment is additive.

## Smart Money Score rubric

A 0-10 score combining role + check size + valuation + price action. Designed to be **interpretive, not prescriptive** — high score ≠ automatic buy.

Score range:
- **🔥🔥🔥 9-10** — Founder/CEO whale check + cheap + near 52W low (rare, ~1-2/month)
- **⭐⭐⭐ 7-8** — Senior officer big check with valuation OR price discount tailwind
- **⭐⭐ 5-6** — Decent conviction signal but balance-sheet or price extension caveats
- **⭐ 3-4** — Noteworthy but mixed (e.g. director-only buy, or expensive multiple)
- **▫️ 0-2** — Low-conviction filing (small size, 10% holder only, ATH chase)

Full rubric in `scripts/enrichment/score.py`. Tune freely to your conviction.

## Tradeoffs vs. openinsider.com

| | Firehose (this) | openinsider.com |
|---|---|---|
| Latency | 2-5 min from filing | 12-24 hours |
| Form 4 code filter | P only (true buy) | All codes shown |
| 10% holder vs officer | Officers prioritized | Mixed together |
| Threshold filter | Configurable USD | Manual UI sort |
| Notification | Telegram push | None (pull-only website) |
| Bilingual output | EN + CN role labels | EN only |
| Cost | $0 (free EDGAR + GH Actions) | Free (website) |

## What this skill does NOT do (yet)

- **Cluster detection** — currently alerts on each filing independently. If 9 insiders of one company all file on the same day (as AVA did on 2026-05-11), you get 9 separate alerts. v2.2 will roll these up into a single "🚨 CLUSTER" alert.
- **Watchlist filter** — alerts fire for ALL tickers ≥ $200k. v2.2 will let you highlight tickers you already own.
- **Daily digest** — currently push-only. v2.2 adds an end-of-day Telegram summary aggregating the day's buys.
- **Historical insider context in score** — current v2.1 score is filing + valuation + price only. v2.2 will pull openinsider 180d history into the score (e.g. +1 if 3rd buy in 90 days).
- **Sells by default** — sells are 10x more common and mostly noise (10b5-1 plans). Set `include_sells=true` for unusual-sell alerts (≥ $1M).

## When this triggers (examples from real Form 4 filings)

Real signals this script catches:
- **PLSE Duggan Robert W (Director + 10%)**: bought $12,999,988 — Pulse Biosciences founder doubling down
- **PLSE Laviolette Paul A (CEO)**: bought $295,350 on same day → cluster signal
- **LW Gray James D**: bought $409,225 — Lamb Weston (foods)
- **ATEC Valentine Keith**: bought $996,192 — Alphatec spine

Real signals from the user's 2026-05-11 SEC EDGAR pull this skill would have alerted on:
- **ET Kelcy Warren (Founder)**: $22M — Energy Transfer (highest-conviction founder buy of the day)
- **AVA 9-insider cluster**: $1.3M total ($145k each, just below $200k individually → cluster would catch it)
- **KGS 6-insider cluster**: $900k total
- **EFX 3-director cluster**: $660k total
- **SOFI CEO Anthony Noto**: $248k (4th buy in 90 days)

## Setup

Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in GitHub Secrets (same ones used by `price-alert/`). See `SETUP.md` for first-run checklist.

## Companion skills

- `review-investment-screenshot/scripts/insider_ratio.py` — per-ticker deep dive (when an alert fires, run this for full 90d context)
- `analyze-stock` — when alert + you don't recognize the ticker, this skill pulls fundamentals + macro context
- `macro-warning` — gate any conviction buy by current regime
