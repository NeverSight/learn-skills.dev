---
name: akshare-skill
description: AKShare CLI wrapper and API reference documentation. Use this skill to access Chinese financial market data via command line (stocks, futures, funds, bonds, forex, macro indicators) or browse comprehensive API documentation with parameter tables, output schemas, and code examples for all supported data categories.
---

# AKShare Data API Reference

AKShare is a Python package providing access to Chinese financial market data. This skill contains complete API documentation organized by asset class and data category.

## Quick Start

AKShare can be used via CLI wrapper or Python library.

### CLI (Recommended)

```bash
# Get stock data (JSON output is default)
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101

# Get as JSON explicitly
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101 --format json

# Export to CSV when needed for complex analysis
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20200101 --end_date 20210101 --format csv > stock_data.csv
```

### Python Library (Legacy)

```python
import akshare as ak

stock_df = ak.stock_zh_a_hist(symbol="000001", start_date="20200101", end_date="20210101")
print(stock_df)
```

## Data Categories

All APIs below are available via CLI wrapper. See individual API docs for both CLI and Python usage:

### **Equities & Indices**
- **[Stock Data](references/stock.md)** - A/B shares, history, daily snapshots, sector data, board listings
- **[Index Data](references/index.md)** - Stock indices, index components, performance data

### **Fixed Income & Rates**
- **[Bonds](references/bond.md)** - Government bonds, corporate bonds, municipal bonds
- **[Interest Rates](references/interest_rate.md)** - LPR rates, deposit/loan rates, yield curves

### **Derivatives & Futures**
- **[Futures](references/futures.md)** - Futures contracts, open interest, delivery data
- **[Options](references/option.md)** - Options contracts, Greeks, implied volatility

### **Alternative Assets**
- **[Funds](references/fund/)** - Public funds (mutual funds), private funds (hedge funds), fund ratings
- **[QDII](references/qdii.md)** - Qualified Domestic Institutional Investor products
- **[Commodities & Spot Trading](references/spot.md)** - Commodity futures, spot market data

### **Forex & International**
- **[Foreign Exchange (FX)](references/fx.md)** - Currency pairs, exchange rates
- **[Hong Kong/Singapore Data (QHKC)](references/qhkc/)** - Hong Kong stocks, Singapore data, commodity analysis

### **Macro & Economics**
- **[Macroeconomic Data](references/macro.md)** - GDP, CPI, industrial production, consumer spending
- **[Currency & FX Markets](references/currency.md)** - Currency data, forex indicators
- **[Energy Data](references/energy.md)** - Oil, coal, natural gas prices and data
- **[Interest Rates](references/interest_rate.md)** - Central bank rates, yield curves

### **Specialized Data**
- **[Bank Data](references/bank.md)** - Bank regulatory data, administrative penalties
- **[Data Center (DC)](references/dc.md)** - Data center services and infrastructure
- **[Digital Currency](references/dc.md)** - Cryptocurrency and digital asset data
- **[Events & News](references/event.md)** - Market events, corporate actions, news events
- **[Natural Language Processing](references/nlp.md)** - Text analysis, sentiment analysis
- **[Technical Indicators & Tools](references/tool.md)** - Technical analysis tools, indicators
- **[Financial Articles](references/article.md)** - Financial research articles and reports
- **[Others](references/others.md)** - Additional specialized data sources

## API Documentation Structure

Each reference file contains:

- **API name** - The function name (e.g., `stock_zh_a_hist`)
- **Target URL** - Data source web address
- **Description** - What the API provides
- **Rate limits** - Data return limits per request
- **Input parameters** - Function parameters with types and descriptions
- **Output parameters** - DataFrame columns returned by the API
- **Code example** - Working Python example
- **Data sample** - Sample output rows

## Parameter Conventions

Common parameter patterns across AKShare APIs:

- **`symbol`** - Stock symbol (e.g., "000001" for SZZF)
- **`start_date` / `end_date`** - Date strings in format "YYYYMMDD" (e.g., "20200101")
- **`period`** - Time period ("daily", "weekly", "monthly")
- **`page`** / **`limit`** - Pagination parameters for large datasets
- **Date output** - Most APIs return datetime columns in format "YYYY-MM-DD HH:MM:SS"

## Multi-Part Categories

Some data categories have multiple sub-APIs:

- **[Funds (references/fund/)](references/fund/)** - Public funds vs. private funds documentation
- **[QHKC (references/qhkc/)](references/qhkc/)** - Hong Kong stocks, fundamentals, brokers, commodities, analysis tools

## Finding What You Need

**By asset class:** Start with the category above that matches your market focus

**By function:** If you know the AKShare function name, search within the corresponding reference file using grep patterns:
- Stock functions: `stock_`
- Fund functions: `fund_`
- Futures functions: `futures_` or `future_`
- Forex functions: `fx_` or `exchange_`

**By data type:** All APIs include parameter tables and examples. Look for "Input parameters" and "Output parameters" sections.

## Example Usage Patterns

### Get historical stock data:
See [references/stock.md](references/stock.md) - use `stock_zh_a_hist()` function

### Access futures data:
See [references/futures.md](references/futures.md) - functions like `futures_open_interest()`, `futures_delivery()`

### Query fund performance:
See [references/fund/fund_public.md](references/fund/fund_public.md) for mutual funds or [references/fund/fund_private.md](references/fund/fund_private.md) for private funds

### Macroeconomic indicators:
See [references/macro.md](references/macro.md) - GDP, inflation, industrial production

### Hong Kong/Singapore market data:
See [references/qhkc/](references/qhkc/) subdirectory for index data, fundamentals, and analysis tools

## CLI Usage Guide

All AKShare functions are available via the CLI wrapper in `scripts/akshare_cli.py`.

### Output Formats

- `--format json`: JSON format for API integration (default)
- `--format pretty`: Human-readable tables
- `--format csv`: CSV format for import into Excel/databases (use when complex analysis is needed)

### Examples by Category

```bash
# Stock data
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110

# Index data
python3 scripts/akshare_cli.py index_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110

# Macro data
python3 scripts/akshare_cli.py macro_china_gdp --format json

# Bank data
python3 scripts/akshare_cli.py bank_fjcf_table_detail --page 1 --item "分局本级"

# Export to file
python3 scripts/akshare_cli.py stock_zh_a_hist --symbol 000001 --start_date 20240101 --end_date 20240110 --format csv > output.csv
```

See [CLI_DESIGN.md](CLI_DESIGN.md) for complete CLI documentation.
