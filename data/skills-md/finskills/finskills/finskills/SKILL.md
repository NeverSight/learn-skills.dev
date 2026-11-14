---
name: finskills
display_name: Finskills — Stock Quantitative Investment
description: Real-time financial data API for systematic stock analysis and quantitative investment research. Access stock quotes, historical OHLCV, batch screening, company fundamentals (income statement, balance sheet, cash flow), earnings estimates, analyst recommendations, options chains, institutional holders, macroeconomic indicators (GDP, CPI, Fed Funds rate, Treasury yields, FRED series), commodity price signals, SEC filings, and financial news. Use this skill for momentum screening, value/quality factor analysis, earnings event research, portfolio risk assessment, sector rotation, and macro factor overlays.
homepage: https://finskills.net
---

# Finskills — Stock Quantitative Investment

Use the Finskills REST API at `https://finskills.net` to perform systematic stock analysis and quantitative investment research in real time.

## Authentication

All requests require the `X-API-Key` header. Ask the user for their key if not provided.
Get a key at: https://finskills.net/register

```
X-API-Key: YOUR_API_KEY_HERE
```

Base URL: `https://finskills.net`

## Quick Start

1. Ask the user for their Finskills API key if not provided.
2. Make HTTP requests to `https://finskills.net/v1/...` with the `X-API-Key` header.
3. Use `/v1/free/...` endpoints when available — they work with any valid API key.
4. For universe-level analysis, always start with the **batch quote** endpoint to minimize API calls.

---

## Stock Data

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/stocks/quote/{symbol}` | Real-time price, change%, volume, market cap, P/E, 52-week range | symbol e.g. `AAPL` |
| `GET /v1/stocks/quotes?symbols=` | Batch quotes for a stock universe | `symbols=AAPL,MSFT,GOOGL` (CSV) |
| `GET /v1/stocks/history/{symbol}` | Historical OHLCV candlestick data | `interval`: 1d/1wk/1mo · `from`/`to`: YYYY-MM-DD |
| `GET /v1/stocks/search?q=` | Find stocks by company name or ticker | `q=apple` |
| `GET /v1/stocks/profile/{symbol}` | Company description, sector, industry, country | — |
| `GET /v1/stocks/financials/{symbol}` | Income statement, balance sheet, cash flow | `freq`: yearly / quarterly |
| `GET /v1/stocks/earnings/{symbol}` | EPS history, actuals vs. estimates, surprise% | — |
| `GET /v1/stocks/dividends/{symbol}` | Dividend payment history and yield | — |
| `GET /v1/stocks/recommendations/{symbol}` | Analyst buy/hold/sell counts with trend history | — |
| `GET /v1/stocks/holders/{symbol}` | Top institutional holders, insider ownership % | — |
| `GET /v1/stocks/options/{symbol}` | Options chain: IV, open interest, Greeks | `date`: YYYY-MM-DD |

## Market Overview

| Endpoint | Description |
|----------|-------------|
| `GET /v1/market/summary` | Major indices (S&P 500, Dow, Nasdaq), trending tickers, top movers |
| `GET /v1/market/sectors` | S&P 500 sector performance — all 11 GICS sectors |

## Macroeconomics & Risk

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/macro/inflation` | US CPI monthly inflation series | — |
| `GET /v1/macro/interest-rates` | US Federal Funds rate history | — |
| `GET /v1/macro/indicator/{series}` | Any FRED series by ID | `series`: CPIAUCSL, FEDFUNDS, UNRATE, T10Y2Y, VIXCLS |
| `GET /v1/free/macro/treasury-rates` | Full US Treasury yield curve (1-month to 30-year) | — |
| `GET /v1/free/macro/gdp` | World Bank GDP by country | `countryCode`: US/CN/JP/DE |
| `GET /v1/free/macro/indicator/{indicator}` | World Bank macro indicator | `indicator`: CPI/GDP/UNEMPLOYMENT · `country`: US |
| `GET /v1/free/forex/rates` | Live exchange rates (150+ currencies) | `base`: USD/EUR/CNY |
| `GET /v1/free/forex/history` | Historical forex rates | `base`, `target`, `startDate`, `endDate` |

## Commodities

| Endpoint | Description | Key Params |
|----------|-------------|------------|
| `GET /v1/free/commodity/prices` | Real-time prices for all or one category | `category`: energy/metals_precious/agriculture |
| `GET /v1/free/commodity/price/{symbol}` | Single commodity real-time quote | `CL=F` (WTI), `GC=F` (Gold), `HG=F` (Copper) |
| `GET /v1/free/commodity/history/{symbol}` | Commodity OHLCV history | `range`: 1y · `interval`: 1d/1wk/1mo |
| `GET /v1/free/commodity/fred/{seriesId}` | FRED daily commodity series | `DCOILWTICO`, `GOLDAMGBD228NLBM` |
| `GET /v1/free/commodity/imf/batch` | IMF monthly data for multiple commodities | `indicators`: POILAPSP,PGOLD,PCOPP |

## News & SEC Filings

| Endpoint | Description |
|----------|-------------|
| `GET /v1/news/by-symbol/{symbol}` | News articles for a specific stock |
| `GET /v1/free/news/finance` | Latest financial news headlines |
| `GET /v1/free/sec/filings/{cik}` | SEC filings: 10-K, 10-Q, 8-K |
| `GET /v1/free/sec/company-facts/{cik}` | XBRL-structured financial facts from SEC EDGAR |

Common CIK numbers: Apple `0000320193` · Microsoft `0000789019` · Tesla `0001318605` · Nvidia `0001045810`

---

## Usage Guidelines

- **Batch first**: For >3 stocks, use `/v1/stocks/quotes?symbols=` rather than individual calls.
- Use `/v1/free/...` endpoints whenever available — no additional external API keys required.
- For crypto, use CoinGecko IDs (bitcoin, ethereum) not ticker symbols (BTC, ETH).
- Always include units (USD, %, bps, ×) and cite data freshness ("as of [date]").
- Format large numbers as `$1.23B`, `$456.7M` — never raw 9-digit values.
- **No investment advice**: Present data factually. Say "the data shows…" not "you should buy/sell".

---

## Example Interactions

**Batch screening:**
> "Screen the Magnificent 7 stocks for momentum and valuation"
→ `GET /v1/stocks/quotes?symbols=AAPL,MSFT,GOOGL,META,NVDA,AMZN,TSLA`, then history per stock

**Fundamental analysis:**
> "Analyze Apple's profitability and financial health"
→ `GET /v1/stocks/financials/AAPL?freq=yearly` — compute ROE, margins, FCF yield

**Earnings trend:**
> "Has Microsoft been consistently beating earnings estimates?"
→ `GET /v1/stocks/earnings/MSFT`

**Analyst sentiment:**
> "What is the analyst consensus on Nvidia?"
→ `GET /v1/stocks/recommendations/NVDA`

**Yield curve:**
> "Is the yield curve inverted right now?"
→ `GET /v1/free/macro/treasury-rates`, then `GET /v1/macro/indicator/T10Y2Y`

**Sector rotation:**
> "Which sectors are outperforming? What does the macro backdrop say?"
→ `GET /v1/market/sectors` + `GET /v1/macro/interest-rates` + `GET /v1/macro/inflation`

**Options volatility:**
> "What is the implied volatility on NVIDIA options before earnings?"
→ `GET /v1/stocks/options/NVDA`

**Commodity macro signal:**
> "Is copper trending up or down? What does it signal for the economy?"
→ `GET /v1/free/commodity/history/HG=F?range=1y&interval=1wk`

**SEC filing:**
> "Find Tesla's latest 10-K annual report"
→ `GET /v1/free/sec/filings/0001318605` (filter `form: 10-K`)

**Risk environment:**
> "Show me the macro risk dashboard: VIX, credit spreads, yield curve"
→ `GET /v1/macro/indicator/VIXCLS` + `GET /v1/macro/indicator/T10Y2Y` + `GET /v1/free/macro/treasury-rates`
