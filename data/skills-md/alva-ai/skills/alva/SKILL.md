---
name: alva
description: >-
  Build and deploy agentic finance applications on the Alva platform. Access
  250+ financial data sources (crypto, equities, macro, on-chain, social), run
  cloud-side analytics, backtest trading strategies, and release interactive
  playbooks -- all from your AI agents.
metadata:
  author: alva
---

# Alva

## What is Alva

Alva is an agentic finance platform. It provides unified access to 250+
financial data sources spanning crypto, equities, ETFs, macroeconomic
indicators, on-chain analytics, and social sentiment -- including spot and
futures OHLCV, funding rates, company fundamentals, price targets, insider and
senator trades, earnings estimates, CPI, GDP, Treasury rates, exchange flows,
DeFi metrics, news feeds, social media and more!

## What Alva Skills Enables

The Alva skill connects any AI agent or IDE to the full Alva platform. With
it you can:

- **Access financial data** -- query any of Alva's 250+ data SDKs
  programmatically, or bring your own data via HTTP API or direct upload.
- **Run cloud-side analytics** -- write JavaScript that executes on Alva Cloud
  in a secure runtime. No local compute, no dependencies, no infrastructure to
  manage.
- **Build agentic playbooks** -- create data pipelines, trading strategies, and
  scheduled automations that run continuously on Alva Cloud.
- **Deploy trading strategies** -- backtest with the Altra trading engine and
  run continuous live paper trading.
- **Release and share** -- turn your work into a hosted playbook web app at
  `https://yourusername.playbook.alva.ai/playbook-name/version/index.html`, and share it with the world.

In short: turn your ideas into a forever-running finance agent that gets things
done for you.

## Capabilities & Common Workflows

### 1. ALFS (Alva FileSystem)

The foundation of the platform. ALFS is a globally shared filesystem with
built-in authorization. Every user has a home directory; permissions control who
can read and write each path. Scripts, data feeds, playbook assets, and shared
libraries all live on ALFS.

Key operations: read, write, mkdir, stat, readdir, remove, rename, copy,
symlink, chmod, grant, revoke.

### 2. JS Runtime

Run JavaScript on Alva Cloud in a secure V8 isolate. The runtime has access to
ALFS, all 250+ SDKs, HTTP networking, LLM access, and the Feed SDK. Everything
executes server-side -- nothing runs on your local machine.

### 3. SDKHub

250+ built-in financial data SDKs. To find the right SDK for a task, use the
two-step retrieval flow:

1. **Pick a partition** from the index below.
2. **Call `GET /api/v1/sdk/partitions/:partition/modules`** to see module
   summaries, then load the full doc for the chosen module.

#### SDK Partition Index

| Partition | Description |
| --------- | ----------- |
| `spot_market_price_and_volume` | Spot OHLCV for crypto and equities. Price bars, volume, historical candles. |
| `crypto_futures_data` | Perpetual futures: OHLCV, funding rates, open interest, long/short ratio. |
| `crypto_technical_metrics` | Crypto technical & on-chain indicators: MA, EMA, RSI, MACD, Bollinger, MVRV, SOPR, NUPL, whale ratio, market cap, FDV, etc. (20 modules) |
| `crypto_exchange_flow` | Exchange inflow/outflow data for crypto assets. |
| `crypto_fundamentals` | Crypto market fundamentals: circulating supply, max supply, market dominance. |
| `crypto_screener` | Screen crypto assets by technical metrics over custom time ranges. |
| `company_crypto_holdings` | Public companies' crypto token holdings (e.g. MicroStrategy BTC). |
| `equity_fundamentals` | Stock fundamentals: income statements, balance sheets, cash flow, margins, PE, PB, ROE, ROA, EPS, market cap, dividend yield, enterprise value, etc. (31 modules) |
| `equity_estimates_and_targets` | Analyst price targets, consensus estimates, earnings guidance. |
| `equity_events_calendar` | Dividend calendar, stock split calendar. |
| `equity_ownership_and_flow` | Institutional holdings, insider trades, senator trading activity. |
| `stock_screener` | Screen stocks by sector, industry, country, exchange, IPO date, earnings date, financial & technical metrics. (9 modules) |
| `stock_technical_metrics` | Stock technical indicators: beta, volatility, Bollinger, EMA, MA, MACD, RSI-14, VWAP, avg daily dollar volume. |
| `etf_fundamentals` | ETF holdings breakdown. |
| `macro_and_economics_data` | CPI, GDP, unemployment, federal funds rate, Treasury rates, PPI, consumer sentiment, VIX, TIPS, nonfarm payroll, retail sales, recession probability, etc. (20 modules) |
| `technical_indicator_calculation_helpers` | 50+ pure calculation helpers: RSI, MACD, Bollinger Bands, ATR, VWAP, Ichimoku, Parabolic SAR, KDJ, OBV, etc. Input your own price arrays. |
| `feed_widgets` | Social & news data feeds: news, Twitter/X, YouTube, Reddit, podcasts, web search (Brave, Grok). |
| `ask` | General news and market articles. |

You can also bring your own data by uploading files to ALFS or fetching from
external HTTP APIs within the runtime.

### 4. Altra (Alva Trading Engine)

A feed-based event-driven backtesting engine for quantitative trading
strategies. A trading strategy IS a feed: all output data (targets, portfolio,
orders, equity, metrics) lives under a single feed's ALFS path. Altra supports
historical backtesting and continuous live paper trading, with custom
indicators, portfolio simulation, and performance analytics.

### 5. Deploy on Alva Cloud

Once your data analytics scripts and feeds are ready, deploy them as scheduled
cronjobs on Alva Cloud. They run continuously on your chosen schedule (e.g.
every hour, every day). Grant public access so anyone -- or any playbook page --
can read the data.

### 6. Build the Playbook Web App

After your data pipelines are deployed and producing data, build the playbook's
web interface. Create HTML5 pages that read from Alva's data gateway and
visualize the results. Follow the Alva Design System for styling, layout, and
component guidelines.

### 7. Release

Three phases:

1. **Write HTML to ALFS**: `POST /api/v1/fs/write` the playbook HTML to
   `~/playbooks/{name}/index.html`.
2. **Call release API**: `POST /api/v1/release/playbook` — creates DB records
   and uploads HTML to CDN. Returns `playbook_id` (numeric).
3. **Write ALFS files**: Using the returned numeric `playbook_id`, write
   release files, draft files, and `playbook.json` to ALFS. See
   [api-reference.md](references/api-reference.md) for details.

The `playbook.json` **must** include a `type` field (`"dashboard"` or
`"strategy"`) and a `draft` object. Omitting `type` causes wrong frontend
routing; omitting `draft` causes the dashboard iframe to never load.

Once released, the playbook is accessible at
`https://yourusername.playbook.alva.ai/playbook-name/version/index.html`.
-- ready to share with the world.

---

**Detailed sub-documents** (read these for in-depth reference):

| Document                                                                              | Contents                                                                          |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [api-reference.md](references/api-reference.md)                                       | Full REST API reference (filesystem, run, deploy, user info, time series paths)   |
| [jagent-runtime.md](references/jagent-runtime.md)                                     | Writing jagent scripts: module system, built-in modules, async model, constraints |
| [feed-sdk.md](references/feed-sdk.md)                                                 | Feed SDK guide: creating data feeds, time series, upstreams, state management     |
| [altra-trading.md](references/altra-trading.md)                                       | Altra backtesting engine: strategies, features, signals, testing, debugging       |
| [deployment.md](references/deployment.md)                                             | Deploying scripts as cronjobs for scheduled execution                             |
| [design-system.md](references/design-system.md)                                       | Alva Design System: design tokens, colors, typography, font rules                 |
| [design-widgets.md](references/design-widgets.md)                                     | Widget design: chart cards, KPI cards, table cards, feed cards, layout grid       |
| [design-components.md](references/design-components.md)                               | Base component templates: dropdown, button, switch, modal, select, markdown       |
| [design-playbook-trading-strategy.md](references/design-playbook-trading-strategy.md) | Trading strategy playbook guideline                                               |
| [adk.md](references/adk.md)                                                           | Agent Development Kit: `adk.agent()` API, tool calling, ReAct loop, examples      |

---

## Setup

All configuration is done via environment variables.

| Variable        | Required | Description                                                     |
| --------------- | -------- | --------------------------------------------------------------- |
| `ALVA_API_KEY`  | **yes**  | Your API key (create and manage at [alva.ai](https://alva.ai))  |
| `ALVA_ENDPOINT` | no       | Alva API base URL. Defaults to `https://api-llm.prd.alva.ai` if not set |

### Making API Requests

All API examples in this skill use HTTP notation (`METHOD /path`). Every request
requires the `X-Alva-Api-Key` header unless marked **(public, no auth)**.

Curl templates for reference:

```bash
# Authenticated
curl -s -H "X-Alva-Api-Key: $ALVA_API_KEY" "$ALVA_ENDPOINT{path}"

# Authenticated + JSON body
curl -s -H "X-Alva-Api-Key: $ALVA_API_KEY" -H "Content-Type: application/json" \
  "$ALVA_ENDPOINT{path}" -d '{body}'

# Public read (no API key, absolute path)
curl -s "$ALVA_ENDPOINT{path}"
```

### Discovering User Info

Retrieve your `user_id` and `username`:

```
GET /api/v1/me
→ {"id":1,"username":"alice"}
```

---

## Quick API Reference

See [api-reference.md](references/api-reference.md) for full details.

### Filesystem (`/api/v1/fs/`)

| Method | Endpoint                          | Description                                       |
| ------ | --------------------------------- | ------------------------------------------------- |
| GET    | `/api/v1/fs/read?path={path}`     | Read file content (raw bytes) or time series data |
| POST   | `/api/v1/fs/write`                | Write file (raw body or JSON with `data` field)   |
| GET    | `/api/v1/fs/stat?path={path}`     | Get file/directory metadata                       |
| GET    | `/api/v1/fs/readdir?path={path}`  | List directory entries                            |
| POST   | `/api/v1/fs/mkdir`                | Create directory (recursive)                      |
| DELETE | `/api/v1/fs/remove?path={path}`   | Remove file or directory                          |
| POST   | `/api/v1/fs/rename`               | Rename / move                                     |
| POST   | `/api/v1/fs/copy`                 | Copy file                                         |
| POST   | `/api/v1/fs/symlink`              | Create symlink                                    |
| GET    | `/api/v1/fs/readlink?path={path}` | Read symlink target                               |
| POST   | `/api/v1/fs/chmod`                | Change permissions                                |
| POST   | `/api/v1/fs/grant`                | Grant read/write access to a path                 |
| POST   | `/api/v1/fs/revoke`               | Revoke access                                     |

Paths: `~/data/file.json` (home-relative) or `/alva/home/<username>/...` (absolute).
Public reads use absolute paths without API key.

### Run (`/api/v1/run`)

| Method | Endpoint      | Description                                                                  |
| ------ | ------------- | ---------------------------------------------------------------------------- |
| POST   | `/api/v1/run` | Execute JavaScript (inline `code` or `entry_path` to a script on filesystem) |

### Deploy (`/api/v1/deploy/`)

| Method | Endpoint                            | Description                       |
| ------ | ----------------------------------- | --------------------------------- |
| POST   | `/api/v1/deploy/cronjob`            | Create a cronjob                  |
| GET    | `/api/v1/deploy/cronjobs`           | List cronjobs (paginated)         |
| GET    | `/api/v1/deploy/cronjob/:id`        | Get cronjob details               |
| PATCH  | `/api/v1/deploy/cronjob/:id`        | Update cronjob (name, cron, args) |
| DELETE | `/api/v1/deploy/cronjob/:id`        | Delete cronjob                    |
| POST   | `/api/v1/deploy/cronjob/:id/pause`  | Pause cronjob                     |
| POST   | `/api/v1/deploy/cronjob/:id/resume` | Resume cronjob                    |

### Release (`/api/v1/release/`)

| Method | Endpoint                    | Description                                     |
| ------ | --------------------------- | ----------------------------------------------- |
| POST   | `/api/v1/release/feed`      | Register feed (DB + link to cronjob task). Call after deploying cronjob. |
| POST   | `/api/v1/release/playbook`  | Release playbook for public hosting. Call after writing playbook HTML. |

**Name uniqueness**: Both `name` in releaseFeed and releasePlaybook must be
unique within your user space. Use `GET /api/v1/fs/readdir?path=~/feeds` or
`GET /api/v1/fs/readdir?path=~/playbooks` to check existing names before
releasing.

### SDK Documentation (`/api/v1/sdk/`)

| Method | Endpoint                                      | Description                                      |
| ------ | --------------------------------------------- | ------------------------------------------------ |
| GET    | `/api/v1/sdk/doc?name={module_name}`            | Get full doc for a specific SDK module             |
| GET    | `/api/v1/sdk/partitions`                        | List all SDK partitions                            |
| GET    | `/api/v1/sdk/partitions/:partition/summary`     | Get one-line summaries of all modules in a partition |

**SDK retrieval flow**: pick a partition from the index above → call
`/partitions/:partition/summary` to see module summaries → call
`/sdk/doc?name=...` to load the full doc for the chosen module.

### Trading Pair Search (`/api/v1/trading-pairs/`)

| Method | Endpoint                             | Description                                      |
| ------ | ------------------------------------ | ------------------------------------------------ |
| GET    | `/api/v1/trading-pairs/search?q={q}` | Search trading pairs by base asset (fuzzy match) |

Search before writing code to check which symbols/exchanges Alva supports.
Supports exact match + prefix fuzzy search by base asset or alias.
Comma-separated queries for multiple searches.

```
GET /api/v1/trading-pairs/search?q=BTC,ETH
→ {"trading_pairs":[{"base":"BTC","quote":"USDT","symbol":"BINANCE_PERP_BTC_USDT","exchange":"binance","type":"crypto-perp","fee_rate":0.001,...},...]}
```

### User Info

| Method | Endpoint     | Description                              |
| ------ | ------------ | ---------------------------------------- |
| GET    | `/api/v1/me` | Get authenticated user's id and username |

---

## Runtime Modules Quick Reference

Scripts executed via `/api/v1/run` run in a V8 isolate. See
[jagent-runtime.md](references/jagent-runtime.md) for full details.

| Module          | require()                    | Description                                                        |
| --------------- | ---------------------------- | ------------------------------------------------------------------ |
| alfs            | `require("alfs")`            | Filesystem (uses absolute paths `/alva/home/<username>/...`)            |
| env             | `require("env")`             | `userId`, `username`, `args` from request                                      |
| net/http        | `require("net/http")`        | `fetch(url, init)` for async HTTP requests                         |
| @alva/algorithm | `require("@alva/algorithm")` | Statistics                                |
| @alva/feed      | `require("@alva/feed")`      | Feed SDK for persistent data pipelines + FeedAltra trading engine  |
| @alva/adk       | `require("@alva/adk")`       | Agent SDK for LLM requests — `agent()` for LLM agents with tool calling |
| @test/suite     | `require("@test/suite")`     | Jest-style test framework (`describe`, `it`, `expect`, `runTests`) |

**SDKHub**: 250+ data modules available via
`require("@arrays/crypto/ohlcv:v1.0.0")` etc. Version suffix is optional
(defaults to `v1.0.0`). To discover function signatures and response shapes,
use the SDK doc API (`GET /api/v1/sdk/doc?name=...`).

**Key constraints**: No top-level `await` (wrap script in
`(async () => { ... })();`). No Node.js builtins (`fs`, `path`, `http`). Module
exports are frozen.

---

## Feed SDK Quick Reference

See [feed-sdk.md](references/feed-sdk.md) for full details.

Feeds are persistent data pipelines that store time series data, readable via
filesystem paths.

```javascript
const { Feed, feedPath, makeDoc, num } = require("@alva/feed");
const { getCryptoKline } = require("@arrays/crypto/ohlcv:v1.0.0");
const { indicators } = require("@alva/algorithm");

const feed = new Feed({ path: feedPath("btc-ema") });

feed.def("metrics", {
  prices: makeDoc("BTC Prices", "Close + EMA10", [num("close"), num("ema10")]),
});

(async () => {
  await feed.run(async (ctx) => {
    const raw = await ctx.kv.load("lastDate");
    const lastDateMs = raw ? Number(raw) : 0;

    const now = Math.floor(Date.now() / 1000);
    const start =
      lastDateMs > 0 ? Math.floor(lastDateMs / 1000) : now - 30 * 86400;

    const bars = getCryptoKline({
      symbol: "BTCUSDT",
      start_time: start,
      end_time: now,
      interval: "1h",
    })
      .response.data.slice()
      .reverse();
    const closes = bars.map((b) => b.close);
    const ema10 = indicators.ema(closes, { period: 10 });

    const records = bars
      .map((b, i) => ({
        date: b.date,
        close: b.close,
        ema10: ema10[i] || null,
      }))
      .filter((r) => r.date > lastDateMs);

    if (records.length > 0) {
      await ctx.self.ts("metrics", "prices").append(records);
      await ctx.kv.put("lastDate", String(records[records.length - 1].date));
    }
  });
})();
```

Feed output is readable at: `~/feeds/btc-ema/v1/data/metrics/prices/@last/100`

---

## Data Modeling Patterns

All data produced by a feed should use `feed.def()` + `ctx.self.ts().append()`.
Do not use `alfs.writeFile()` for feed output data.

**Pattern A -- Snapshot (latest-wins)**: For data that represents current state
(company detail, ratings, price target consensus). Use start-of-day as the date
so re-runs overwrite.

```javascript
const today = new Date();
today.setHours(0, 0, 0, 0);
await ctx.self
  .ts("info", "company")
  .append([
    { date: today.getTime(), name: company.name, sector: company.sector },
  ]);
```

Read `@last/1` for current snapshot, `@last/30` for 30-day history.

**Pattern B -- Event log**: For timestamped events (insider trades, news,
senator trades). Each event uses its natural date. Same-date records are
auto-grouped.

```javascript
const records = trades.map((t) => ({
  date: new Date(t.transactionDate).getTime(),
  name: t.name,
  type: t.type,
  shares: t.shares,
}));
await ctx.self.ts("activity", "insiderTrades").append(records);
```

**Pattern C -- Tabular (versioned batch)**: For data where the whole set
refreshes each run (top holders, EPS estimates). Stamp all records with the same
run timestamp; same-date grouping stores them as a batch.

```javascript
const now = Date.now();
const records = holdings.map((h, i) => ({
  date: now,
  rank: i + 1,
  name: h.name,
  marketValue: h.value,
}));
await ctx.self.ts("research", "institutions").append(records);
```

| Data Type               | Pattern                | Date Strategy   | Read Query  |
| ----------------------- | ---------------------- | --------------- | ----------- |
| OHLCV, indicators       | Time series (standard) | Bar timestamp   | `@last/252` |
| Company detail, ratings | Snapshot (A)           | Start of day    | `@last/1`   |
| Insider trades, news    | Event log (B)          | Event timestamp | `@last/50`  |
| Holdings, estimates     | Tabular (C)            | Run timestamp   | `@last/N`   |

See [feed-sdk.md](references/feed-sdk.md) for detailed data modeling examples
and deduplication behavior.

---

## Deploying Feeds

Every feed follows a 6-step lifecycle:

1. **Write** -- define schema + incremental logic with `ctx.kv`
2. **Upload** -- write script to `~/feeds/<name>/v1/src/index.js`
3. **Test** -- `POST /api/v1/run` with `entry_path` to verify output
4. **Grant** -- make feed public via `POST /api/v1/fs/grant`
5. **Deploy** -- `POST /api/v1/deploy/cronjob` for scheduled execution
6. **Release** -- `POST /api/v1/release/feed` to register the feed in the
   database (requires the `task_id` from the deploy step)

| Data Type                     | Recommended Schedule     | Rationale                           |
| ----------------------------- | ------------------------ | ----------------------------------- |
| Stock OHLCV + technicals      | `0 */4 * * *` (every 4h) | Markets update during trading hours |
| Company detail, price targets | `0 8 * * *` (daily 8am)  | Changes infrequently                |
| Insider/senator trades        | `0 8 * * *` (daily 8am)  | SEC filings are daily               |
| Earnings estimates            | `0 8 * * *` (daily 8am)  | Updated periodically                |

See [deployment.md](references/deployment.md) for the full deployment guide and
API reference.

---

## Debugging Feeds

### Resetting Feed Data (development only)

During development, use the REST API to clear stale or incorrect data. **Do not
use this in production.**

```
# Clear a specific time series output
DELETE /api/v1/fs/remove?path=~/feeds/my-feed/v1/data/market/ohlcv&recursive=true

# Clear an entire group (all outputs under "market")
DELETE /api/v1/fs/remove?path=~/feeds/my-feed/v1/data/market&recursive=true

# Full reset: clear ALL data + KV state (removes the data mount, re-created on next run)
DELETE /api/v1/fs/remove?path=~/feeds/my-feed/v1/data&recursive=true
```

### Inline Debug Snippets

Test SDK shapes before building a full feed:

```
POST /api/v1/run
{"code":"const { getCryptoKline } = require(\"@arrays/crypto/ohlcv:v1.0.0\"); JSON.stringify(Object.keys(getCryptoKline({ symbol: \"BTCUSDT\", start_time: 0, end_time: 0, interval: \"1h\" })));"}
```

---

## Altra Trading Engine Quick Reference

See [altra-trading.md](references/altra-trading.md) for full details.

Altra is a feed-based event-driven backtesting engine. A trading strategy IS a
feed: all output data lives under a single ALFS path. Decisions execute at bar
CLOSE.

```javascript
const { createOHLCVProvider } = require("@arrays/data/ohlcv-provider:v1.0.0");
const { FeedAltraModule } = require("@alva/feed");
const { FeedAltra, e, Amount } = FeedAltraModule;

const altra = new FeedAltra(
  {
    path: "~/feeds/my-strategy/v1",
    startDate: Date.parse("2025-01-01T00:00:00Z"),
    portfolioOptions: { initialCash: 1_000_000 },
    simOptions: { simTick: "1min", feeRate: 0.001 },
    perfOptions: { timezone: "UTC", marketType: "crypto" },
  },
  createOHLCVProvider(),
);

const dg = altra.getDataGraph();
dg.registerOhlcv("BINANCE_SPOT_BTC_USDT", "1d");
dg.registerFeature({ name: "rsi" /* ... */ });

altra.setStrategy(strategyFn, {
  trigger: { type: "events", expr: e.ohlcv("BINANCE_SPOT_BTC_USDT", "1d") },
  inputConfig: {
    ohlcvs: [{ id: { pair: "BINANCE_SPOT_BTC_USDT", interval: "1d" } }],
    features: [{ id: "rsi" }],
  },
  initialState: {},
});

(async () => {
  await altra.run(Date.now());
})();
```

---

## Deployment Quick Reference

See [deployment.md](references/deployment.md) for full details.

Deploy feed scripts or tasks as cronjobs for scheduled execution:

```
POST /api/v1/deploy/cronjob
{"path":"~/feeds/btc-ema/v1/src/index.js","cron_expression":"0 */4 * * *","name":"BTC EMA Update"}
```

Cronjobs execute the script via the same jagent runtime as `/api/v1/run`. Max 20
cronjobs per user. Min interval: 1 minute.

After deploying a cronjob, register the feed and release the playbook for public
hosting. The playbook HTML must already be written to ALFS at
`~/playbooks/{name}/index.html` via `fs/write` before releasing.

**Important**: Feed names and playbook names must be unique within your user
space. Before creating a new feed or playbook, use
`GET /api/v1/fs/readdir?path=~/feeds` or `GET /api/v1/fs/readdir?path=~/playbooks`
to check for existing names and avoid conflicts.

```
# 1. Release feed (register in DB, link to cronjob)
POST /api/v1/release/feed
{"name":"btc-ema","version":"1.0.0","task_id":42}
→ {"feed_id":100,"name":"btc-ema","feed_major":1}

# 2. Release playbook (uploads HTML to CDN, returns numeric playbook_id)
POST /api/v1/release/playbook
{"name":"btc-dashboard","version":"v1.0.0","description":"BTC market dashboard with price and technicals","feeds":[{"feed_id":100}]}
→ {"playbook_id":99,"version":"v1.0.0"}

# 3. Write release layout.html (CDN URL, using numeric playbook_id from step 2)
POST /api/v1/fs/write?path=~/playbooks/99/releases/v1.0.0/layout.html&mkdir_parents=true
Content-Type: application/octet-stream
Body: https://alice.playbook.alva.ai/btc-dashboard/v1.0.0/index.html

# 4. Write draft layout.html (required for frontend dashboard iframe rendering)
POST /api/v1/fs/write?path=~/playbooks/99/draft/layout.html&mkdir_parents=true
Content-Type: application/octet-stream
Body: https://alice.playbook.alva.ai/btc-dashboard/v1.0.0/index.html

# 5. Write playbook.json (must include "type" and "draft" fields)
POST /api/v1/fs/write
Content-Type: application/json
{"path":"~/playbooks/99/playbook.json","data":"{\"playbook_id\":99,\"owner_uid\":\"1\",\"type\":\"dashboard\",\"name\":\"btc-dashboard\",\"created_at\":\"2026-03-12T00:00:00Z\",\"updated_at\":\"2026-03-12T00:00:00Z\",\"draft\":{\"playbook_version_id\":0,\"updated_at\":\"2026-03-12T00:00:00Z\",\"layout_path\":\"./draft/layout.html\",\"feeds_dir\":\"./draft/feeds/\",\"feeds\":[{\"feed_id\":100,\"feed_major\":1}]},\"releases\":[{\"version\":\"v1.0.0\",\"playbook_version_id\":0,\"created_at\":\"2026-03-12T00:00:00Z\",\"layout_path\":\"./releases/v1.0.0/layout.html\",\"feeds_dir\":\"./releases/v1.0.0/feeds/\",\"feeds\":[{\"feed_id\":100,\"feed_major\":1}]}],\"latest_release\":{\"version\":\"v1.0.0\",\"playbook_version_id\":0,\"created_at\":\"2026-03-12T00:00:00Z\",\"layout_path\":\"./releases/v1.0.0/layout.html\",\"feeds_dir\":\"./releases/v1.0.0/feeds/\",\"feeds\":[{\"feed_id\":100,\"feed_major\":1}]}}","mkdir_parents":true}
```

The playbook will be accessible at `https://alice.playbook.alva.ai/btc-dashboard/v1.0.0/index.html`.

---

## Alva Design System

All Alva playbook pages, dashboards, and widgets must follow the Alva Design
System. The system defines design tokens (colors, spacing, shadows), typography
rules, and component/widget templates.

Key rules:

- **Font**: Delight (Regular 400, Medium 500). No Semibold/Bold. Font files: [Delight-Regular.ttf](https://alva-ai-static.b-cdn.net/fonts/Delight-Regular.ttf),
  [Delight-Medium.ttf](https://alva-ai-static.b-cdn.net/fonts/Delight-Medium.ttf)
- **Page background**: `--b0-page` (`#ffffff`)
- **Semantic colors**: `--main-m3` (bullish/green), `--main-m4` (bearish/red),
  `--main-m1` (Alva theme/teal)
- **Charts**: Use ECharts. Select colors from the chart palette in
  [design-system.md](references/design-system.md). Grey only when >= 3 series.
- **Widgets**: No borders on widget cards. Chart cards use dotted background;
  table card has no background; other cards use `--grey-g01`.
- **Grid**: 8-column grid (web), 4-column grid (mobile). Column spans must sum
  to 8 per row.

**Reference documents** (read for detailed specs when building playbook web
apps):

| When                                                                    | Read                                                                          |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Design tokens, typography, font rules, general guidelines               | [design-system.md](references/design-system.md)                               |
| Widget types, chart/KPI/table/feed cards, grid layout                   | [design-widgets.md](references/design-widgets.md)                             |
| Component templates (button, dropdown, modal, select, switch, markdown) | [design-components.md](references/design-components.md)                       |
| Trading strategy playbook layout, sections, and content guidelines      | [design-playbook-trading-strategy.md](references/design-playbook-trading-strategy.md) |

---

## Filesystem Layout Convention

| Path                      | Purpose                                     |
| ------------------------- | ------------------------------------------- |
| `~/tasks/<name>/src/`     | Task source code                            |
| `~/feeds/<name>/v1/src/`  | Feed script source code                     |
| `~/feeds/<name>/v1/data/` | Feed synth mount (auto-created by Feed SDK) |
| `~/playbooks/<name>/`     | Playbook web app assets                     |
| `~/data/`                 | General data storage                        |
| `~/library/`              | Shared code modules                         |

**Prefer using the Feed SDK for all data organization**, including point-in-time
snapshots. Store snapshots as single-record time series rather than raw JSON
files via `alfs.writeFile()`. This keeps all data queryable through a single
consistent read pattern (`@last`, `@range`, etc.).

---

## Common Pitfalls

- **`@last` returns chronological (oldest-first) order**, consistent with
  `@first` and `@range`. No manual sorting needed.
- **Time series reads return flat JSON records.** Paths with `@last`, `@range`,
  etc. return JSON arrays of flat records like
  `[{"date":...,"close":...,"ema10":...}]`. Regular paths return file content
  with `Content-Type: application/octet-stream`.
- **`last(N)` limits unique timestamps, not records.** When multiple records
  share a timestamp (grouped via `append()`), auto-flatten may return more than
  N individual records.
- **The `data/` in feed paths is the synth mount.** `feedPath("my-feed")` gives
  `~/feeds/my-feed/v1`, and the Feed SDK mounts storage at `<feedPath>/data/`.
  Don't name your group `"data"` or you'll get `data/data/...`.
- **Public reads require absolute paths.** Unauthenticated reads must use
  `/alva/home/<username>/...` (not `~/...`). Discover your username via `GET /api/v1/me`.
- **Top-level `await` is not supported.** Wrap async code in
  `(async () => { ... })();`.
- **`require("alfs")` uses absolute paths.** Inside the V8 runtime,
  `alfs.readFile()` needs full paths like `/alva/home/alice/...`. Get your username from
  `require("env").username`.
- **No Node.js builtins.** `require("fs")`, `require("path")`, `require("http")`
  do not exist. Use `require("alfs")` for files, `require("net/http")` for HTTP.
- **Altra `run()` is async.** `FeedAltra.run()` returns a `Promise<RunResult>`.
  Always `await` it: `const result = await altra.run(endDate);`
- **Altra decisions happen at bar CLOSE.** Feature timestamps must use
  `bar.endTime`, not `bar.date`. Using `bar.date` introduces look-ahead bias.
- **Altra lookback: feature vs strategy.** Feature lookback controls how many
  bars the feature computation sees. Strategy lookback controls how many feature
  outputs the strategy function sees. They are independent.
- **Cronjob path must point to an existing script.** The deploy API validates
  the entry_path exists via filesystem stat before creating the cronjob.
- **`playbook.json` must include `type` and `draft`; draft ALFS files are
  required.** Omitting `type` defaults to "strategy" (wrong routing for
  dashboards). Omitting `draft` or the `draft/layout.html` file causes the
  dashboard iframe to never load.

---

## Resource Limits

| Resource              | Limit                 |
| --------------------- | --------------------- |
| Write payload         | 10 MB max per request |
| HTTP response body    | 128 MB max            |
| Max cronjobs per user | 20                    |
| Min cron interval     | 1 minute              |

---

## Error Responses

All errors return: `{"error":{"code":"...","message":"..."}}`

| HTTP Status | Code              | Meaning                            |
| ----------- | ----------------- | ---------------------------------- |
| 400         | INVALID_ARGUMENT  | Bad request or invalid path        |
| 401         | UNAUTHENTICATED   | Missing or invalid API key         |
| 403         | PERMISSION_DENIED | Access denied                      |
| 404         | NOT_FOUND         | File/directory not found           |
| 429         | RATE_LIMITED      | Rate limit / runner pool exhausted |
| 500         | INTERNAL          | Server error                       |
