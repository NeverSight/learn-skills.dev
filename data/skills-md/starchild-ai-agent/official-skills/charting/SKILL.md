---
name: charting
version: 1.0.0
description: Generate TradingView-style candlestick charts with indicators. Use when the user wants a visual chart, price visualization, or technical analysis plot.

metadata:
  starchild:
    emoji: "📊"
    skillKey: charting
    requires:
      env: [COINGECKO_API_KEY]
    install:
      - kind: pip
        package: mplfinance
      - kind: pip
        package: pandas
      - kind: pip
        package: numpy

user-invocable: true
disable-model-invocation: false
---

# Charting

## ⚠️ CRITICAL: DO NOT CALL DATA TOOLS

**NEVER** call `price_chart`, `get_coin_ohlc_range_by_id`, `twelvedata_time_series`, or ANY market data tools when creating charts. Chart scripts fetch data internally. Calling these tools floods your context with 78KB+ of unnecessary data.

**Workflow (4 steps):**
1. Read template from `skills/charting/scripts/`
2. Write script to `scripts/`
3. Run script with `bash`
4. Call `read_file` on the output PNG, then display it using markdown image syntax: `![Chart description](output/filename.png)`

---

You generate TradingView-quality candlestick charts. Dark theme, clean layout, professional colors. Every chart is a standalone Python script — no internal imports.

**Additional Rules:**
- Chart scripts run in workspace and cannot import from `core`. Use `requests` library directly, NOT `proxied_get()`.
- Templates include proxy auto-configuration. If `PROXY_HOST` env var exists, scripts automatically configure `HTTP_PROXY`/`HTTPS_PROXY`.

Tools: `write_file`, `bash`, `read_file`

## When to Use Which Chart

**Simple price action** → Candlestick with no indicators. Good for "show me BTC this month."
**Trend analysis** → Add EMA/SMA overlays. Good for "is ETH in an uptrend?"
**Momentum check** → Add RSI or MACD as subplots. Good for "is SOL overbought?"
**Full technical view** → Candles + Bollinger Bands + RSI + MACD. Good for "give me the full picture on BTC."
**Volume analysis** → Requires separate fetch from market_chart endpoint (OHLC endpoint has no volume).
**Asset comparison** → Line chart comparing two assets (BTC vs Gold, ETH vs S&P500, etc.). Use comparison template for normalized or percentage-based comparisons.

## How to Build Charts

Read and customize the template scripts in `skills/charting/scripts/`:
- `chart_template.py` — Baseline candlestick chart with TradingView styling (crypto via CoinGecko)
- `chart_with_indicators.py` — RSI, MACD, Bollinger Bands, EMA/SMA examples (crypto via CoinGecko)
- `chart_stock_template.py` — Stock/forex chart using Twelve Data API
- `chart_comparison_template.py` — Compare two assets (crypto vs commodity, stock vs crypto, etc.)

Copy the relevant template to `scripts/`, customize the config section (coin, days, indicators), and run it.

The templates handle all data fetching internally with retry logic and error handling.

**Note:** These templates are for market data visualization (price charts, indicators). For backtest result charts (equity curves, drawdowns, performance dashboards), add matplotlib charting directly to your backtest script — the data is already there, no need to re-fetch or create a separate file.

## TradingView Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Up candles | Teal | `#26a69a` |
| Down candles | Red | `#ef5350` |
| Background | Dark | `#131722` |
| Grid | Subtle dotted | `#1e222d` |
| Text / axes | Light gray | `#d1d4dc` |
| MA lines | Blue / Orange | `#2196f3` / `#ff9800` |
| RSI line | Purple | `#b39ddb` |
| MACD line | Blue | `#2196f3` |
| Signal line | Orange | `#ff9800` |

Do not deviate from this palette unless the user asks.

## Data Source APIs

### CoinGecko (Crypto Only)

**Endpoint:** `https://pro-api.coingecko.com/api/v3/coins/{coin_id}/ohlc/range`
**Auth:** Header `x-cg-pro-api-key: {COINGECKO_API_KEY}`
**Use for:** BTC, ETH, SOL, and all cryptocurrencies

Example:
```python
url = f"https://pro-api.coingecko.com/api/v3/coins/{COIN_ID}/ohlc/range"
params = {"vs_currency": "usd", "from": from_ts, "to": now, "interval": "daily"}
headers = {"x-cg-pro-api-key": os.getenv("COINGECKO_API_KEY")}
resp = requests.get(url, params=params, headers=headers)
raw = resp.json()  # [[timestamp_ms, open, high, low, close], ...]
```

### Twelve Data (Stocks, Forex, Commodities)

**Endpoint:** `https://api.twelvedata.com/time_series`
**Auth:** Query param `apikey={TWELVEDATA_API_KEY}`
**Use for:** Stocks (AAPL, MSFT), Forex (EUR/USD), Commodities (XAU/USD for gold)

**Common Symbols:**
- Stocks: `AAPL`, `MSFT`, `GOOGL`, `TSLA`, `SPY`
- Forex: `EUR/USD`, `GBP/JPY`, `USD/CHF`
- Commodities: `XAU/USD` (gold), `XAG/USD` (silver), `CL/USD` (crude oil)

**Intervals:** `1min`, `5min`, `15min`, `30min`, `1h`, `4h`, `1day`, `1week`, `1month`

Example:
```python
url = "https://api.twelvedata.com/time_series"
params = {
    "symbol": "XAU/USD",  # Gold spot price
    "interval": "1day",
    "outputsize": 90,  # Number of candles
    "apikey": os.getenv("TWELVEDATA_API_KEY")
}
resp = requests.get(url, params=params)
data = resp.json()
# data["values"] = [{"datetime": "2024-01-01", "open": "2050.00", "high": "2060.00", ...}, ...]
```

**IMPORTANT:** Twelve Data returns data in **reverse chronological order** (newest first). Always reverse the list before creating a DataFrame:
```python
values = data["values"][::-1]  # Reverse to oldest-first
```

## Interval Selection Strategy

The templates now auto-select optimal intervals to minimize data volume while maintaining visual quality:

| Time Range | Auto-Selected Interval | Rationale |
|------------|----------------------|-----------|
| ≤31 days | Hourly | High granularity for short-term analysis |
| 32-365 days | Daily | Sufficient detail, lower data volume |
| >365 days | Daily | Daily is optimal for long-term trends |

**Override:** Set `INTERVAL = "daily"` or `INTERVAL = "hourly"` in the config to override auto-selection.

## Key Gotchas

- **`savefig` facecolor**: You MUST set `facecolor='#131722'` and `edgecolor='#131722'` in `savefig`, or the saved PNG reverts to white background.
- **Title spacing**: Prefix titles with `\n` to add spacing from the top edge.
- **`returnfig=True`**: Use when you need post-plot customization (price formatting, annotations). When using it, call `fig.savefig()` manually — don't pass `savefig` to `mpf.plot()`.
- **No volume in OHLC**: CoinGecko OHLC endpoint returns `[timestamp_ms, open, high, low, close]` only. Use `volume=False` or fetch volume separately from `coin_chart` endpoint.
- **Panel ratios**: Set `panel_ratios` when adding indicator subplots. E.g., `(4, 1, 2)` for candles + volume + one indicator, `(5, 1, 2, 2)` for two indicators.
- **Figure size**: Default `(14, 8)`. Increase to `(14, 10)` or `(14, 12)` when adding subplots.

## Rules

- **Paths are relative to workspace.** Write to `scripts/foo.py`, not `workspace/scripts/foo.py`. The bash CWD is already workspace.
- **Always save to `output/` directory.** Use `os.makedirs("output", exist_ok=True)`.
- **Always run the script with `bash("python3 scripts/<name>.py")`** to verify it works.
- **Always call `read_file` on the generated PNG, then use markdown image syntax to display it:** `![Chart](output/filename.png)`
- **Scripts must be standalone.** Use `requests` + `os.getenv()`. No internal imports, no dotenv.
- **CRITICAL: Do NOT use proxied_get() in chart scripts.** Chart scripts are standalone and run in the workspace - they cannot import from `core.http_client`. Always use `requests.get()` and `requests.post()` directly. This is an exception to the PLATFORM.md proxy rules because these scripts execute outside the main Star Child process. The templates demonstrate the correct pattern.
- **Env vars are inherited.** `os.getenv("COINGECKO_API_KEY")` works directly.
- **Default to dark theme** unless user asks for light.
- **Filename should describe the chart.** e.g. `btc_30d_candles.png`, `eth_7d_rsi_macd.png`.
- **Data sources:** Use CoinGecko API for crypto (BTC, ETH, etc). Use Twelve Data API for stocks, forex, and commodities (AAPL, EUR/USD, XAU/USD for gold). Never mix APIs - keep scripts focused on one data source.
- **Think about what you're measuring:** Before creating a chart, ask yourself: "What question is the user trying to answer?" A normalized chart (all start at 100) shows relative trends but hides actual gain magnitude. If the user wants to know "which gained more" or is comparing investment performance, they need the actual multipliers (e.g., 50x vs 10x), not just lines that look similar.

## Troubleshooting

### 401 Unauthorized Errors

Templates auto-configure proxy from `PROXY_HOST`/`PROXY_PORT` env vars. If 401 errors occur:

**Check environment:**
```bash
bash("env | grep -E 'PROXY|REQUESTS_CA'")
```

**Expected vars:**
- `PROXY_HOST` / `PROXY_PORT` - Proxy address (templates use these to set HTTP_PROXY/HTTPS_PROXY)
- `REQUESTS_CA_BUNDLE` - Proxy CA cert for SSL
- `COINGECKO_API_KEY` / `TWELVEDATA_API_KEY` - Can be fake in proxied environments

If vars are missing, this is an environment configuration issue, not a script issue.
