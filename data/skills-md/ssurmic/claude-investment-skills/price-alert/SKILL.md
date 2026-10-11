---
name: price-alert
description: Set, list, and cancel parameterized price alerts on any US-listed stock or ETF. Supports absolute price thresholds (above/below) and percentage moves (drop/rise from anchor). Alerts run via GitHub Actions cron (every 15 min during US trading hours) and fire Telegram notifications. Use when user wants to be notified when a stock hits a specific price or moves a specific percentage. Triggers in English ("alert me when X hits Y", "notify me if X drops Z%", "set price alert", "watch X at Y", "list my alerts", "cancel alert") or Chinese ("X 跌到 Y 通知我", "X 涨到 Y 提醒", "设个 alert", "盯一下 X", "列出我的 alert", "取消 alert").
---

# Price Alert Skill

Parameterized price-alert management. The user can set, list, and cancel alerts on any ticker; they fire a Telegram push when the threshold hits.

## Architecture

```
price-alert/
├── SKILL.md              # this file
├── alerts.json           # active alert definitions (committed to git)
├── alerts_fired.log      # append-only history of triggered alerts
├── scripts/
│   ├── add_alert.py      # add new alert
│   ├── list_alerts.py    # list all / active / fired
│   ├── cancel_alert.py   # cancel by id, ticker, or --all
│   ├── check_alerts.py   # run by GitHub Actions cron, sends Telegram
│   └── chat_handler.py   # Option A chat path: poll Telegram + tool-use via Claude API
└── webhook/              # OPTIONAL Option B chat path (Cloudflare Worker)
    ├── worker.ts         # TypeScript webhook handler (mirrors chat_handler.py)
    └── wrangler.toml     # CF Worker deploy config
```

Price scanning runs in **GitHub Actions** (`.github/workflows/price-alerts.yml`), which executes `check_alerts.py` every 2 minutes 24/7 and pushes Telegram notifications for any triggered alerts.

The bidirectional NL **chat path has two interchangeable implementations** — pick one per the latency you want:
- **Option A (default)**: `telegram-chat.yml` GH Actions cron polls Telegram every 2-5 min, runs `chat_handler.py`. Latency 2-15 min. $0. Setup: [SETUP.md](./SETUP.md).
- **Option B (optional upgrade)**: Cloudflare Worker (`webhook/worker.ts`) receives Telegram webhook POSTs and processes instantly. Latency 1-3 sec. Still $0 (CF free tier 100k req/day). Setup: [SETUP-WEBHOOK.md](./SETUP-WEBHOOK.md) on top of basic SETUP.

Both paths use the same Anthropic API and end up modifying the same `alerts.json` via GitHub. They are not used together — Option B replaces Option A entirely once you enable it.

## Decision tree

| User says | → Action |
|---|---|
| "Alert me when GLW hits $140" | `add_alert.py GLW below 140` |
| "Notify me if NVDA drops 10%" | `add_alert.py NVDA drop 10` |
| "Watch SMH at $480" | `add_alert.py SMH below 480` |
| "Alert if AAPL goes above $250" | `add_alert.py AAPL above 250` |
| "GLW 跌到 140 通知我" | `add_alert.py GLW below 140` |
| "NVDA 跌 10% 提醒我" | `add_alert.py NVDA drop 10` |
| "List my alerts" / "我的 alerts" | `list_alerts.py --active` |
| "Cancel GLW alert" / "取消 GLW" | `cancel_alert.py GLW` |
| "Re-arm the GLW alert" | `cancel_alert.py <id> --rearm` |

After running any add/cancel, **commit and push** `alerts.json` so GitHub Actions sees the change on its next run.

## Adding alerts — parameter mapping

```bash
# Absolute price thresholds
python add_alert.py TICKER below PRICE [--note "..."]
python add_alert.py TICKER above PRICE [--note "..."]

# Percentage moves (auto-anchors to current price unless --anchor specified)
python add_alert.py TICKER drop PCT  [--note "..."] [--anchor PRICE]
python add_alert.py TICKER rise PCT  [--note "..."] [--anchor PRICE]
```

Always include `--note` when context is meaningful — it shows up in the Telegram message and helps you remember why you set it weeks later.

## Examples

```bash
# AI glass substrate retracement watchlist
python add_alert.py GLW below 140 --note "AI glass tier 1 entry"
python add_alert.py ONTO below 210 --note "Inspection tools post-reset"
python add_alert.py LRCX below 240 --note "50DMA support"
python add_alert.py KLAC below 1500 --note "Conservative semicap entry"

# Macro flip warnings
python add_alert.py SPY drop 5 --note "Material pullback from current ATH"
python add_alert.py SMH drop 10 --note "Semi correction trigger"

# Take-profit alerts on long positions
python add_alert.py NVDA above 1300 --note "Target reached - consider trim"
```

## Telegram message format

When an alert fires, the user receives:

```
🔻 PRICE ALERT: GLW

Current: $138.45
Trigger: $138.45 ≤ $140.00
52W high: $198.25 (-30.2% off)
52W low: $46.34

Note: AI glass tier 1 entry

Alert id: glw-below-a3b2c1
Set: 2026-05-10
```

## GitHub Actions setup (one-time)

Required GitHub repo secrets:
- `TELEGRAM_BOT_TOKEN` — from @BotFather
- `TELEGRAM_CHAT_ID`   — from `https://api.telegram.org/bot<TOKEN>/getUpdates`

Workflow lives at `.github/workflows/price-alerts.yml`. Cron is `*/15 13-21 * * 1-5` (every 15 min during US trading hours, weekdays).

To trigger manually for testing: GitHub repo → Actions tab → "Price Alert Checker" → "Run workflow".

## Important behaviors

- **Idempotent**: once fired, an alert is marked `fired=true` and won't re-trigger. To get the same alert again, run `cancel_alert.py <id> --rearm`.
- **Anchors are static**: `drop 10%` from anchor $100 fires at $90 forever — even if the stock first drops to $85 and then rebounds to $95 before falling to $90 again. The first $90 cross fires it.
- **GitHub Actions auto-commits** the updated `alerts.json` when alerts fire, keeping the source of truth in git.
- **No re-fire**: after firing once, the alert stays in alerts.json (so you can audit history) but is filtered out of `list_alerts.py --active`.

## When NOT to use this skill

- **Intraday scalping**: 2-min granularity is too coarse. Use a real broker alert.
- **Composite conditions** (e.g., "GLW < 140 AND VIX > 25"): not supported by current schema. Set two alerts and use your judgment.
- **Crypto / non-US tickers**: not tested. yfinance support varies.

## ⚠️ Alert fired — what to do BEFORE adding

A fired alert is a **trigger to research**, not a buy signal. When the user receives an alert and asks "should I add now":

1. **Run `analyze-stock TICKER`** — has the bull thesis changed since the alert was set? Fresh insider check, valuation, catalysts.
2. **Trigger `macro-warning`** — if regime flipped to 🔴 RED between alert-set and alert-fire, the entry price you wanted is no longer the entry price you want.
3. **Verify the 3-tier plan** — the alert price was T1. If T1 hit because of macro selloff (not stock-specific), T2 and T3 likely follow. Pre-commit to tier sizes now.
4. **Position-size check** — if adding pushes the position above 10% of book, scale the add down.
5. **Insider strict 30d** — `insider_ratio.py TICKER --window 30` — catch any pre-alert C-suite distribution that explains the drop.

**"Look carefully" rule**: alerts fire because of price moves; price moves often have a REASON. Don't add without finding the reason. If you can't articulate why the stock dropped to your alert price, you don't yet understand whether the bull thesis is intact.

## Verification

To verify GitHub Actions is working without waiting for a real trigger:
1. Set a guaranteed-fire alert: `add_alert.py SPY below 99999`
2. Manually trigger workflow in GitHub UI
3. Check Telegram for message
4. Cancel: `cancel_alert.py <id>`
