---
name: trade-api
description: "Use this skill for any work with Finam / Финам broker and Trade API: questions about the API, developing algorithmic trading strategies and scripts, and interacting with the broker programmatically. Trigger on: Finam/Финам mentions, api.finam.ru URLs, ticker@mic symbol format, finam-sdk. Also trigger for Russian-market trading workflows even without explicit Finam mention — portfolio analysis, scanning Moscow Exchange stocks (MISX/RTSX), volatility/momentum/arbitrage strategies, order placement and cancellation, real-time quotes via gRPC or WebSocket, OHLCV candles, backtesting on Russian equities, risk management for algo trading."
metadata: '{"openclaw": {"emoji": "📈", "homepage": "https://api.finam.ru/", "requires": {"bins": ["curl", "jq", "python3"]}, "primaryEnv": "TRADE_API_SECRET"}}'
---

# Finam Trade API Skill

## Setup

To execute Trade API requests, the skill needs one credential:

- `TRADE_API_SECRET` — API token. Get it at [api.finam.ru/docs/tokens](https://api.finam.ru/docs/tokens)

You can use this skill without it — to design strategies, explore docs, or write scripts.

The secret comes from the environment if the user exported it, otherwise from a `.env` file in the project root (your working directory). Most users only paste the token into `.env` — they don't need to know any shell.

### Auth prefix

Every shell call starts a fresh shell, and the JWT expires after 15 minutes, so start **every** shell call that talks to the API with this auth prefix and append your command after the last `&& \`:

```shell
export TRADE_API_SECRET="${TRADE_API_SECRET:-$(sed -n 's/^TRADE_API_SECRET=//p' .env 2>/dev/null | tr -d "\r\"' ")}" ACCOUNT_ID="${ACCOUNT_ID:-$(sed -n 's/^ACCOUNT_ID=//p' .env 2>/dev/null | tr -d "\r\"' ")}" && \
{ [ -n "$TRADE_API_SECRET" ] || { echo "❌ TRADE_API_SECRET is not set"; false; }; } && \
TOKEN=$(curl -sL "https://api.finam.ru/v1/sessions" \
  --header "Content-Type: application/json" \
  --data '{"secret": "'"$TRADE_API_SECRET"'"}' | jq -r '.token') && \
curl -sL "https://api.finam.ru/v1/..." --header "Authorization: $TOKEN" | jq
```

What it does:
- **Loads the secret** — keeps an already exported value, otherwise extracts just `TRADE_API_SECRET` and `ACCOUNT_ID` from `./.env`. The file is parsed, not executed (unlike `source`), and nothing is printed, so the value never shows up in the conversation. `export` lets Python scripts and SDK snippets started in the same call see it.
- **Checks it** — if the secret is missing, prints ❌ and stops the chain; go to [If the secret is missing](#if-the-secret-is-missing).
- **Exchanges it for a JWT** in `$TOKEN`.

Shell examples in this skill are POSIX (bash/zsh). On Windows, run them via Git Bash or WSL; if your shell is PowerShell, call `bash -c '...'` or translate the command — a PowerShell error here doesn't mean the secret is missing.

The examples below show only the part that goes after the prefix.

Scripts and SDK code — bundled `scripts/*.py`, code you write, official strategies — read `TRADE_API_SECRET` only from the environment. Run them after the first two lines of the prefix (load and check); the SDK gets the JWT on its own. The `scripts/...` paths in the examples are relative to the skill directory (where this `SKILL.md` lives) — run them from the project root by full path, e.g. `python3 "<skill dir>/scripts/scanner.py" ru 10`, so the prefix finds the project's `./.env`. Don't `cd` into the skill directory.

When you hand the user a command to run a script themselves, include loading `.env` in it: `uv run --env-file .env python main.py ...` for uv projects (all official strategies), otherwise `set -a && source .env && set +a && python3 script.py`. Don't ask them to `export` the token by hand.

### If the secret is missing

Set up `.env` for the user rather than asking them to type shell commands:

1. If `./.env` doesn't exist, copy the template that ships with this skill (`.env.example` next to this `SKILL.md`): `cp "<skill dir>/.env.example" .env`. If you can't locate the skill directory, create `.env` with the same content yourself — a comment with the tokens page link, an empty `TRADE_API_SECRET=` line and a commented-out `# ACCOUNT_ID=`. Never write a real token into it.
2. If the project is a git repo, make sure `.env` is ignored so the token never gets committed:
   ```shell
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 && { grep -qxF '.env' .gitignore 2>/dev/null || echo '.env' >> .gitignore; }
   ```
3. Tell the user the full path to `.env`, ask them to open it in any text editor, paste the token right after `TRADE_API_SECRET=` (no quotes or spaces), save, and let you know. Mention where to get a token ([tokens page](https://api.finam.ru/docs/tokens)) and that a 2-week demo account is available there.
4. When they confirm, retry the request with the auth prefix.

If `.env` already exists but the prefix still reports ❌, skip to step 3 — the key is probably empty or misspelled.

Users who prefer not to keep a file can export the variable in their own terminal before launching the agent (`export TRADE_API_SECRET=...`), or in Claude Code put it into `.claude/settings.local.json` as `{ "env": { "TRADE_API_SECRET": "..." } }`. An exported value takes priority over `.env`.

**Handling the secret** — the token gives full trading access to the user's account, and anything that appears in the conversation is stored in the session history:
- Don't ask the user to paste the token into the chat, and don't run `export TRADE_API_SECRET=...` with the value on their behalf.
- Don't display the value or the contents of files that hold it: no `echo $TRADE_API_SECRET`, `env`, `printenv`, no `cat`/Read of `.env` or `.claude/settings.local.json`. Get the value only through the auth prefix.
- If the user pastes the token into the chat anyway, warn them that it is now exposed and recommend revoking it and issuing a new one on the [tokens page](https://api.finam.ru/docs/tokens).

### Resolving the account ID

Account-scoped requests (portfolio, orders, account-specific asset fields) need an `ACCOUNT_ID`. Resolve it once per session — the token itself knows which accounts it can access. After the auth prefix:

```shell
DETAILS=$(curl -sL "https://api.finam.ru/v1/sessions/details" \
  --header "Content-Type: application/json" \
  --data '{"token": "'"$TOKEN"'"}') && \
ACCOUNT_ID="${ACCOUNT_ID:-$(echo "$DETAILS" | jq -r 'if (.account_ids | length) == 1 then .account_ids[0] else empty end')}" && \
echo "ACCOUNT_ID=${ACCOUNT_ID:-❌ could not resolve automatically}"
```

- If `ACCOUNT_ID` is already set in the environment or in `.env` (picked up by the auth prefix), it wins — treat it as an explicit override (useful when the token exposes several accounts and the user always wants the same one). Most users never need to set it.
- Otherwise, if the token exposes exactly one account, `ACCOUNT_ID` resolves automatically from `/v1/sessions/details` — no setup step required.
- If the token exposes **multiple** accounts and none is pre-set, the command above resolves to empty. In that case, run `printf '%s\n' "$DETAILS" | jq -r '.account_ids'` and ask the user which account to use for this session before making any account-scoped request — don't guess which one.
- Use `$ACCOUNT_ID` in every request below. Like `$TOKEN`, it lives only within one shell call — once resolved, put the value into later calls yourself (`ACCOUNT_ID=... && ...` after the prefix).

**Demo account:** Can be opened at the [tokens page](https://api.finam.ru/docs/tokens). Valid for 2 weeks; works identically to a real account.

**Rate limits:** 200 requests/min per method by default (some methods are lower) — see [Rate Limits](#rate-limits).

**Maintenance window:** 05:00–06:15 MSK daily — API may be unavailable.

## Rate Limits

Quotas are counted **per method**, per user, in a 1-minute window. Defaults:

| Method | Limit |
| --- | --- |
| Every method (including gRPC streams and `/v1/usage` itself) | 200 requests/min |
| `ReportsService.createAccountReport` | 3 requests/min |

Defaults can change and may be raised for a specific user — the live numbers come from `GET /v1/usage`, so check it rather than relying on this table when it matters.

### Check current quotas

```shell
curl -sL "https://api.finam.ru/v1/usage" --header "Authorization: $TOKEN" \
  | jq -r '.quotas | sort_by(.name)[] | [.name, .limit, .remaining, (.reset_time // "-")] | @tsv' | column -t
```

Each entry in `quotas`:
- `name` — `Service.method`, e.g. `MarketDataService.bars`, `OrdersService.placeOrder`
- `limit` — quota size for the window (int64, serialized as a string in REST JSON)
- `remaining` — requests left in the current window
- `reset_time` — when the current window resets (RFC 3339, UTC). Present only for methods already called in the current window; absent means the full `limit` is available.

Python SDK: `client.metrics.GetUsageMetrics(GetUsageMetricsRequest())` (`from finam_trade_api.metrics import GetUsageMetricsRequest`).

### Staying within limits

- Exceeding a quota returns HTTP `429` / gRPC `RESOURCE_EXHAUSTED` (`RateLimitError` in the SDK). Don't retry in a tight loop — wait until `reset_time` for that method. The SDK does not auto-retry 429 unless the server sends a retry pushback.
- Scripts that loop over many symbols (scanners, bulk bar downloads) hit `MarketDataService.bars` hardest: throttle to under 200 calls/min (e.g. `time.sleep(0.3)` between calls) or check `remaining` before a large batch.
- For live data, prefer a gRPC subscription (`subscribeQuote`, `subscribeOrderBook`, …) over polling `lastQuote` / `orderBook` — opening a stream is one call that keeps delivering updates, while every poll spends quota.

### Raising limits

Limits can't be changed through the API. If the user needs more (e.g. a bot regularly hits 429), point them to the request form: open [api.finam.ru/docs/rest/#introduction](https://api.finam.ru/docs/rest/#introduction), click **«Увеличить лимиты API»** and fill in the form. The user submits it themselves — don't fill it in on their behalf.

Raised limits are bound to an application ID, not to the secret alone. The ID (`source_app_id`) is issued to the user once the request is approved — the user can't make one up, so if they don't have it yet, the request is still pending. Every token request must carry `source_app_id`, otherwise the session gets the default quotas. Keep the ID in an env var (e.g. `SOURCE_APP_ID`) and pass it when exchanging the secret for a JWT — use this instead of the `TOKEN=` step of the auth prefix:

```shell
TOKEN=$(curl -sL "https://api.finam.ru/v1/sessions" \
  --header "Content-Type: application/json" \
  --data "$(jq -n --arg s "$TRADE_API_SECRET" --arg a "$SOURCE_APP_ID" '{secret: $s, source_app_id: $a}')" \
  | jq -r '.token')
```

The same field exists on gRPC `AuthRequest` and `SubscribeJwtRenewalRequest`. `FinamClient` / `AsyncFinamClient` currently send only `secret`, so a script that needs the raised limits must obtain the token via REST (as above) or call `AuthService.Auth` itself with `source_app_id` set.

After approval, fetch a token with `source_app_id` and verify the new numbers with `GET /v1/usage`.

## Market assets

### List Available Exchanges

**Symbol Format:** All symbols must be in `ticker@mic` format (e.g., `SBER@MISX`)

**Base MIC Codes:**
- `MISX` - Moscow Exchange (all markets)
- `RTSX` - Moscow Exchange, Derivatives Market (futures & options)
- `XNYS` - New York Stock Exchange
- `ARCX` - NYSE Arca (ETFs)
- `XNGS` - NASDAQ/NGS (Global Select Market)
- `XNMS` - NASDAQ/NNS (Global Market)
- `XNCM` - NASDAQ Capital Market

View all supported exchanges with their MIC codes:

```shell
curl -sL "https://api.finam.ru/v1/exchanges" --header "Authorization: $TOKEN" | \
  jq -r '.exchanges[] | "\(.mic) - \(.name)"'
```

### Get Asset Specification

Fetch detailed specification for a specific instrument (lot size, price step, decimals, trading schedule, etc.):

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/assets/$SYMBOL?account_id=$ACCOUNT_ID" \
  --header "Authorization: $TOKEN" | jq
```

`account_id` is optional but recommended — returns account-specific fields (margin, available quantity, etc.).

### Search Assets

Search instruments by ticker glob pattern and/or name substring:

```shell
# By ticker glob
python3 scripts/asset_search.py 'SBER*'

# By name (case-insensitive substring)
python3 scripts/asset_search.py --name 'apple'

# By ticker glob + type + exchange filter
python3 scripts/asset_search.py 'NG*' --type FUTURES --mic RTSX

# Search expired/archived instruments (e.g. expired futures contracts)
python3 scripts/asset_search.py 'NGF6' --type FUTURES --mic RTSX --archived

# By name + exchange + archived
python3 scripts/asset_search.py --name 'NG-' --type FUTURES --mic RTSX --archived
```

Available types: `EQUITIES`, `FUTURES`, `BONDS`, `FUNDS`, `SPREADS`, `OTHER`, `CURRENCIES`, `OPTIONS`, `SWAPS`, `INDICES`

`--mic MIC` filters by exchange (e.g. `RTSX`, `MISX`). `--archived` fetches expired/delisted instruments via `GET /v1/assets/all?only_disabled=true`. `--max=N` sets the pagination cap (default: 200 000).

### Get Top Stocks

Fetch current index components — IMOEX for RU market, NDX for US market:

```shell
# Table output (default)
python3 scripts/top_stocks.py ru
python3 scripts/top_stocks.py us

# First N entries
python3 scripts/top_stocks.py ru --n 10

# JSON output (for piping to other tools)
python3 scripts/top_stocks.py ru --json
```

## Account Management

### Get Account Portfolio

Retrieve portfolio information including positions, balances, and P&L:

```shell
curl -sL "https://api.finam.ru/v1/accounts/$ACCOUNT_ID" \
  --header "Authorization: $TOKEN" | jq
```

## Market Data

### Get Latest Quote

Retrieve current bid/ask prices and last trade:

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/quotes/latest" \
  --header "Authorization: $TOKEN" | jq
```

### Get Order Book (Depth)

View current market depth with bid/ask levels:

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/orderbook" \
  --header "Authorization: $TOKEN" | jq
```

### Get Recent Trades

List the most recent executed trades:

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/trades/latest" \
  --header "Authorization: $TOKEN" | jq
```

### Get Historical Candles (OHLCV)

Retrieve historical price data with specified timeframe:

```shell
SYMBOL="SBER@MISX"
TIMEFRAME="TIME_FRAME_D"
START_TIME="2024-01-01T00:00:00Z"
END_TIME="2024-04-01T00:00:00Z"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/bars?timeframe=$TIMEFRAME&interval.start_time=$START_TIME&interval.end_time=$END_TIME" \
  --header "Authorization: $TOKEN" | jq
```

**Available Timeframes:**

| Timeframe | Description | Max data depth (end_time - start_time) |
|---|---|---|
| `TIME_FRAME_UNSPECIFIED` | Not specified | — |
| `TIME_FRAME_M1` | 1 minute | 7 days |
| `TIME_FRAME_M5` | 5 minutes | 30 days |
| `TIME_FRAME_M15` | 15 minutes | 30 days |
| `TIME_FRAME_M30` | 30 minutes | 30 days |
| `TIME_FRAME_H1` | 1 hour | 30 days |
| `TIME_FRAME_H2` | 2 hours | 30 days |
| `TIME_FRAME_H4` | 4 hours | 30 days |
| `TIME_FRAME_H8` | 8 hours | 30 days |
| `TIME_FRAME_D` | Day | 365 days |
| `TIME_FRAME_W` | Week | ~5 years |
| `TIME_FRAME_MN` | Month | ~5 years |
| `TIME_FRAME_QR` | Quarter | ~5 years |

> **Note:** The max data depth is the maximum allowed range for `end_time - start_time`. If the range exceeds the limit, the API returns empty data.

**Date Format (RFC 3339):**

- Format: `YYYY-MM-DDTHH:MM:SSZ` or `YYYY-MM-DDTHH:MM:SS+HH:MM`
- `start_time` - Inclusive (interval start, included in results)
- `end_time` - Exclusive (interval end, NOT included in results)
- Examples:
    - `2024-01-15T10:30:00Z` (UTC)
    - `2024-01-15T10:30:00+03:00` (Moscow time, UTC+3)

## News

### Get Latest Market News

Fetch and display the latest news headlines via Finam. No JWT token required.

Russian market news

```shell
curl -sL "https://www.finam.ru/analysis/conews/rsspoint/" | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
for item in reversed(root.findall('.//item')):
    t=item.findtext('title',''); d=item.findtext('description','').split('...')[0]
    print(f'* {t}. {d}')
"
```

US market news

```shell
curl -sL "https://www.finam.ru/international/advanced/rsspoint/" | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
for item in reversed(root.findall('.//item')):
    t=item.findtext('title',''); d=item.findtext('description','').split('...')[0]
    print(f'* {t}. {d}')
"
```

## Order Management

> **IMPORTANT:** Before placing or cancelling any order, you MUST explicitly confirm the details with the user and
> receive their approval. State the full order parameters (symbol, side, quantity, type, price) and wait for confirmation
> before executing.

### Place Order

**Order Types:**

- `ORDER_TYPE_MARKET` - Market order (executes immediately, no `limit_price` required)
- `ORDER_TYPE_LIMIT` - Limit order (requires `limit_price`)

```shell
curl -sL "https://api.finam.ru/v1/accounts/$ACCOUNT_ID/orders" \
  --header "Authorization: $TOKEN" \
  --header "Content-Type: application/json" \
  --data "$(jq -n \
    --arg symbol   "SBER@MISX" \
    --arg quantity "10" \
    --arg side     "SIDE_BUY" \
    --arg type     "ORDER_TYPE_LIMIT" \
    --arg price    "310.50" \
    '{symbol: $symbol, quantity: {value: $quantity}, side: $side, type: $type, limit_price: {value: $price}}')" \
  | jq
```

**Parameters:**

- `symbol` - Instrument (e.g., `SBER@MISX`)
- `quantity.value` - Number of shares/contracts
- `side` - `SIDE_BUY` or `SIDE_SELL`
- `type` - `ORDER_TYPE_MARKET` or `ORDER_TYPE_LIMIT`
- `limit_price` - Only for `ORDER_TYPE_LIMIT` (omit for market orders)

### Get Order Status

Check the status of a specific order:

```shell
ORDER_ID="12345678"
curl -sL "https://api.finam.ru/v1/accounts/$ACCOUNT_ID/orders/$ORDER_ID" \
  --header "Authorization: $TOKEN" | jq
```

### Cancel Order

Cancel a pending order:

```shell
ORDER_ID="12345678"
curl -sL --request DELETE "https://api.finam.ru/v1/accounts/$ACCOUNT_ID/orders/$ORDER_ID" \
  --header "Authorization: $TOKEN" | jq
```

## Building Strategies

### Pattern: scan → signal → execute

Every algo strategy follows the same loop:
1. **Scan** — fetch market data for a universe of instruments (candles, quotes, scanner)
2. **Signal** — compute metrics (growth, volatility, momentum) and decide action per symbol
3. **Execute** — place or cancel orders based on signals; confirm with user before executing

For one-off runs use `FinamClient` (sync). For continuous bots, use `AsyncFinamClient` with a reconnection loop (see Python SDK section).

### Momentum strategy

Buy if the stock grew over the last N days, sell otherwise:

```python
import os
from datetime import datetime, timedelta, timezone
from google.type.decimal_pb2 import Decimal
from finam_trade_api import FinamClient
from finam_trade_api.auth_messages import TokenDetailsRequest
from finam_trade_api.market_data import BarsRequest, TimeFrame
from finam_trade_api.orders import Order, OrderType, Side, TimeInForce

SYMBOLS = ["SBER@MISX", "GAZP@MISX", "LKOH@MISX"]
LOOKBACK_DAYS = 30
QUANTITY = "1"

def get_growth(client, symbol, days):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    req = BarsRequest(symbol=symbol, timeframe=TimeFrame.TIME_FRAME_D)
    req.interval.start_time.FromDatetime(start)
    req.interval.end_time.FromDatetime(end)
    bars = list(client.market_data.Bars(req).bars)
    if len(bars) < 2:
        return None
    first, last = float(bars[0].close.value), float(bars[-1].close.value)
    return (last - first) / first * 100

def resolve_account_id(client) -> str:
    if account_id := os.environ.get("ACCOUNT_ID"):
        return account_id
    details = client.auth.TokenDetails(TokenDetailsRequest(token=client.get_token()))
    if len(details.account_ids) == 1:
        return details.account_ids[0]
    raise RuntimeError(
        f"Token exposes {len(details.account_ids)} accounts {list(details.account_ids)}; "
        "ask the user which one to use, or set ACCOUNT_ID to pin one"
    )

with FinamClient(secret=os.environ["TRADE_API_SECRET"]) as client:
    account_id = resolve_account_id(client)

    for symbol in SYMBOLS:
        growth = get_growth(client, symbol, LOOKBACK_DAYS)
        if growth is None:
            print(f"{symbol}: not enough data, skipping")
            continue

        side = Side.SIDE_BUY if growth > 0 else Side.SIDE_SELL
        print(f"{symbol}: growth={growth:+.1f}% → {'BUY' if side == Side.SIDE_BUY else 'SELL'}")

        # IMPORTANT: confirm with user before uncommenting
        # state = client.orders.PlaceOrder(Order(
        #     account_id=account_id,
        #     symbol=symbol,
        #     quantity=Decimal(value=QUANTITY),
        #     side=side,
        #     type=OrderType.ORDER_TYPE_MARKET,
        #     time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
        # ))
        # print(f"  Order placed: {state.order_id}")
```

### Backtesting

To backtest a strategy on historical data, shift the `start`/`end` window in `BarsRequest` to a past period and replay your signal logic bar by bar. No external framework needed:

```python
# Continues the momentum example above (same imports and `client`)
# Simulate momentum over 2024
backtest_end = datetime(2025, 1, 1, tzinfo=timezone.utc)
backtest_start = datetime(2024, 1, 1, tzinfo=timezone.utc)

req = BarsRequest(symbol="SBER@MISX", timeframe=TimeFrame.TIME_FRAME_D)
req.interval.start_time.FromDatetime(backtest_start)
req.interval.end_time.FromDatetime(backtest_end)
bars = list(client.market_data.Bars(req).bars)

# Walk forward: at each bar, compute signal on the preceding window
window = 30
for i in range(window, len(bars)):
    segment = bars[i - window:i]
    first = float(segment[0].close.value)
    last = float(segment[-1].close.value)
    signal = "BUY" if last > first else "SELL"
    print(f"{bars[i].time.ToDatetime():%Y-%m-%d}  {signal}  close={last}")
```

> Max historical depth per request depends on timeframe (e.g. `TIME_FRAME_D` → 365 days). For longer periods, paginate by shifting the window.

## Market Scanner

Scans top-100 stocks for volatility, growth, and volume. Supports filtering and sorting by any metric.

**Usage:**

```shell
python3 scripts/scanner.py [ru|us] [N] [--sort volatility|growth|volume] [--days N] [--min-growth PCT] [--min-volume VAL]
```

**Examples:**

```shell
# Top 10 most volatile Russian stocks (last 60 days)
python3 scripts/scanner.py ru 10

# Stocks up >5% this week with avg daily volume >500M rubles
python3 scripts/scanner.py ru --days 5 --sort growth --min-growth 5 --min-volume 500000000

# Top 5 most volatile US stocks
python3 scripts/scanner.py us 5
```

All scripts support `--help` for usage details (e.g. `python3 scripts/scanner.py --help`).

## API Protocols

### REST

Endpoint: `https://api.finam.ru/v1` (HTTP/2 required — HTTP/1 causes method errors)

Use for one-off requests: historical OHLCV data, account info, positions, balances, trade history, instrument search, placing or cancelling orders where 100–200 ms latency is acceptable.

### gRPC

Endpoint: `api.finam.ru:443`

Use for low-latency and streaming scenarios: real-time quotes, order book, trade feed, live bar data for signal generation, monitoring own orders/trades via subscription, long-running trading bots with persistent auto-reconnecting connections.

**Note:** Streams disconnect once per day (~86400s from subscription start) — implement reconnection logic in long-running bots.

### WebSocket / AsyncAPI

Endpoints: `api.finam.ru/ws` or `api.finam.ru/tradinginfo`

Use when you need a browser-compatible or firewall-friendly alternative to gRPC for real-time data: streaming quotes, order book updates, and trade events over a standard WebSocket connection.

## Fetching API Documentation

**Always fetch live docs** — never rely on local cached copies. Use the `WebFetch` tool to load documentation on demand.

### Algorithm

1. **Fetch the index** for the relevant protocol to discover available docs:

   | Protocol | Index URL |
   | --- | --- |
   | REST | `https://api.finam.ru/docs/rest/llms.txt` |
   | gRPC | `https://api.finam.ru/docs/grpc/llms.txt` |
   | WebSocket / AsyncAPI | `https://api.finam.ru/docs/async-api/llms.txt` |

2. **Fetch the specific endpoint doc** linked from the index. URL patterns:
   - REST: `https://api.finam.ru/docs/rest/<servicename_methodname>.md` (e.g. `ordersservice_placeorder.md`)
   - gRPC: `https://api.finam.ru/docs/grpc/<methodname>.md` (e.g. `placeorder.md`)
   - AsyncAPI: `https://api.finam.ru/docs/async-api/<topicname>.md`

Fetch only the docs you actually need for the current task.

## Python SDK

Use the Finam SDK (`pip install finam-sdk`) for any Python scripts that interact with the API — both for one-off queries and streaming/trading bots. It handles JWT issuance and refresh automatically, provides typed exceptions, and exposes the full gRPC surface via a single `FinamClient` / `AsyncFinamClient` entry point.

Before running any script that imports `finam_trade_api`, make sure the package is installed — run `python3 -c "import finam_trade_api"` and, if it fails, install with `pip install finam-sdk` before executing the script.

Full reference: fetch live from `https://raw.githubusercontent.com/FinamWeb/finam-trade-api/main/sdk/python/README.md` (source: https://github.com/FinamWeb/finam-trade-api/tree/main/sdk/python)

### Resolve the account ID

Most account-scoped calls need an `account_id`. The JWT token itself knows which accounts it can access — fetch that via `TokenDetails` instead of hardcoding an account. Reuse this helper in every example below:

```python
import os
from finam_trade_api.auth_messages import TokenDetailsRequest

def resolve_account_id(client) -> str:
    if account_id := os.environ.get("ACCOUNT_ID"):
        return account_id  # explicit override — pins a specific account
    details = client.auth.TokenDetails(TokenDetailsRequest(token=client.get_token()))
    if len(details.account_ids) == 1:
        return details.account_ids[0]
    raise RuntimeError(
        f"Token exposes {len(details.account_ids)} accounts {list(details.account_ids)}; "
        "ask the user which one to use, or set ACCOUNT_ID to pin one"
    )
```

If `resolve_account_id` raises because of multiple accounts, don't guess — ask the user which account to use, or have them set `ACCOUNT_ID` (or pass it directly).

### Authenticate and fetch account info

```python
import os
from finam_trade_api import FinamClient
from finam_trade_api.accounts import GetAccountRequest

with FinamClient(secret=os.environ["TRADE_API_SECRET"]) as client:
    account = client.accounts.GetAccount(
        GetAccountRequest(account_id=resolve_account_id(client))
    )
    print(account)
```

### Place a limit order and cancel it

```python
import os
from google.type.decimal_pb2 import Decimal
from finam_trade_api import FinamClient
from finam_trade_api.orders import (
    CancelOrderRequest, Order, OrderType, Side, TimeInForce,
)

with FinamClient(secret=os.environ["TRADE_API_SECRET"]) as client:
    account_id = resolve_account_id(client)

    state = client.orders.PlaceOrder(Order(
        account_id=account_id,
        symbol="SBER@MISX",
        quantity=Decimal(value="1"),
        side=Side.SIDE_BUY,
        type=OrderType.ORDER_TYPE_LIMIT,
        time_in_force=TimeInForce.TIME_IN_FORCE_DAY,
        limit_price=Decimal(value="100.00"),  # far below market — won't fill
        client_order_id="example-001",
    ))
    print(f"Placed: {state.order_id} status={state.status}")

    cancelled = client.orders.CancelOrder(
        CancelOrderRequest(account_id=account_id, order_id=state.order_id)
    )
    print(f"Cancelled: {cancelled.order_id} status={cancelled.status}")
```

### Stream live quotes (async)

```python
import asyncio, os, sys
from finam_trade_api import AsyncFinamClient
from finam_trade_api.market_data import SubscribeQuoteRequest

async def main(symbols: list[str]) -> None:
    async with AsyncFinamClient(secret=os.environ["TRADE_API_SECRET"]) as client:
        async for tick in client.market_data.SubscribeQuote(
            SubscribeQuoteRequest(symbols=symbols)
        ):
            print(tick, flush=True)

asyncio.run(main(sys.argv[1:] or ["SBER@MISX"]))
```

### Reconnection loop for long-running bots

Streams can disconnect for two reasons: the server closes them after ~86400 s, or the JWT token expires mid-stream (`UNAUTHENTICATED`). In both cases the client must be recreated — reusing the same `AsyncFinamClient` instance after `UNAUTHENTICATED` will fail again immediately. Create the client **inside** the loop:

```python
import asyncio, os, grpc
from finam_trade_api import AsyncFinamClient
from finam_trade_api.market_data import SubscribeQuoteRequest

async def stream_with_reconnect(symbols: list[str]) -> None:
    while True:
        try:
            async with AsyncFinamClient(secret=os.environ["TRADE_API_SECRET"]) as client:
                async for tick in client.market_data.SubscribeQuote(
                    SubscribeQuoteRequest(symbols=symbols)
                ):
                    process(tick)
        except grpc.RpcError:
            await asyncio.sleep(5)  # brief pause before reconnect
```

## Strategy Examples

Ready-to-run strategy implementations built with the Finam SDK.

**Index:** `https://raw.githubusercontent.com/FinamWeb/finam-trade-api/main/examples/strategies/README.md`

When the user asks about strategies or wants to copy one:

1. Fetch the index above to discover available strategies and their language implementations.
2. Follow the links in the index to fetch the specific strategy README (`examples/strategies/<name>/README.md`) — it describes the rule, candle handling, safety guards, and configuration.
3. To **copy** a strategy locally:
   - Ask which language (if multiple are available) and which target directory (default: `./<strategy_name>`).
   - Use the GitHub Contents API to list files — it returns filenames and download URLs. Fetch the top-level strategy directory first, then the language subdirectory:
     ```
     https://api.github.com/repos/FinamWeb/finam-trade-api/contents/examples/strategies/<name>
     https://api.github.com/repos/FinamWeb/finam-trade-api/contents/examples/strategies/<name>/<lang>
     ```
   - Download all files in a single Bash call using the `download_url` values from the API response:
     ```bash
     mkdir -p "<target_dir>/<lang>"
     curl -sL "url1" -o "<target_dir>/file1" \
          "url2" -o "<target_dir>/file2" ...
     ```
     Do not copy subdirectories — only top-level files in each directory.
4. After writing all files, show the user how to install dependencies and run the dry-run check (see the language README for exact commands).
