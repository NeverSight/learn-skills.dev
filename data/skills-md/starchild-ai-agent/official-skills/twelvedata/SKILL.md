---
name: twelvedata
version: 1.0.0
description: Stocks and forex price data, time series, quotes, and reference data
tools:
  - twelvedata_time_series
  - twelvedata_price
  - twelvedata_eod
  - twelvedata_quote
  - twelvedata_quote_batch
  - twelvedata_price_batch
  - twelvedata_search
  - twelvedata_stocks
  - twelvedata_forex_pairs
  - twelvedata_exchanges

metadata:
  starchild:
    emoji: "📊"
    skillKey: twelvedata
    requires:
      env:
        - TWELVEDATA_API_KEY

user-invocable: false
disable-model-invocation: false
---

# Twelve Data

Twelve Data provides stocks and forex market data including real-time quotes, historical time series, and reference data. Use for traditional markets (stocks, forex) instead of crypto.

## When to Use Twelve Data

Use Twelve Data for:
- **Stock prices** - Real-time and historical stock quotes
- **Forex prices** - Currency pair quotes and time series
- **Time series data** - OHLCV historical data
- **Reference data** - Stock lists, forex pairs, exchanges
- **Search** - Find stock symbols and company names

**Important**: Use Twelve Data for stocks and forex only. For crypto, use CoinGecko.

## Common Workflows

### Get Stock Price
```
twelvedata_quote(symbol="AAPL")  # Apple real-time quote
twelvedata_price(symbol="MSFT")  # Microsoft current price
twelvedata_quote(symbol="TSLA")  # Tesla quote with full details
```

### Get Forex Price
```
twelvedata_quote(symbol="EUR/USD")  # Euro to USD
twelvedata_quote(symbol="GBP/JPY")  # British Pound to Japanese Yen
```

### Historical Data
```
twelvedata_time_series(symbol="AAPL", interval="1day", outputsize="compact")  # Last 30 days
twelvedata_time_series(symbol="MSFT", interval="1h", outputsize="full")  # 5000 hourly candles
twelvedata_eod(symbol="GOOGL")  # End of day price
```

### Batch Queries (Efficient)
```
twelvedata_quote_batch(symbols=["AAPL", "MSFT", "GOOGL", "TSLA"])  # Up to 120 symbols
twelvedata_price_batch(symbols=["AAPL", "MSFT"])  # Just prices
```

### Search for Symbols
```
twelvedata_search(query="Apple")  # Find AAPL
twelvedata_search(query="Microsoft")  # Find MSFT
twelvedata_search(query="EUR")  # Find EUR forex pairs
```

### Reference Data
```
twelvedata_stocks(exchange="NASDAQ")  # All NASDAQ stocks
twelvedata_forex_pairs()  # All forex pairs
twelvedata_exchanges(type="stock")  # All stock exchanges
```

## Symbol Format

### Stocks
Use standard ticker symbols:
- `AAPL` - Apple
- `MSFT` - Microsoft
- `TSLA` - Tesla
- `GOOGL` - Google
- `AMZN` - Amazon

### Forex Pairs
Use slash format:
- `EUR/USD` - Euro to US Dollar
- `GBP/JPY` - British Pound to Japanese Yen
- `USD/CHF` - US Dollar to Swiss Franc

## Intervals

### Intraday
- `1min`, `5min`, `15min`, `30min`
- `1h`, `2h`, `4h`, `8h`

### Daily and Above
- `1day` - Daily candles
- `1week` - Weekly candles
- `1month` - Monthly candles

## Output Sizes

- `compact` - Last 30 data points (default, faster)
- `full` - Up to 5000 data points (for deep analysis)

## Response Fields

### Quote Response
- `symbol` - Ticker symbol
- `name` - Company/pair name
- `price` - Current price
- `open`, `high`, `low`, `close` - OHLC data
- `volume` - Trading volume
- `change` - Price change
- `percent_change` - Percentage change
- `timestamp` - Last update time

### Time Series Response
- `datetime` - Timestamp
- `open`, `high`, `low`, `close` - OHLC
- `volume` - Trading volume

## Important Notes

- **API Key**: Requires TWELVEDATA_API_KEY environment variable (Pro subscription)
- **Crypto**: DO NOT use Twelve Data for crypto. Use CoinGecko instead.
- **Fundamental data**: Fundamental data tools (income_statement, balance_sheet, etc.) require Grow/Pro+/Ultra/Enterprise tiers and are not included in this skill
- **Rate limits**: Be mindful of API rate limits. Use batch endpoints for multiple symbols.
- **Real-time**: Quotes are near real-time (typically 15-minute delay for free tier, real-time for Pro)

## Workflow Examples

### Stock Analysis
1. Search for symbol: `twelvedata_search(query="Apple")`
2. Get current quote: `twelvedata_quote(symbol="AAPL")`
3. Get historical data: `twelvedata_time_series(symbol="AAPL", interval="1day", outputsize="compact")`

### Forex Analysis
1. Get forex pair: `twelvedata_quote(symbol="EUR/USD")`
2. Get historical: `twelvedata_time_series(symbol="EUR/USD", interval="1h", outputsize="compact")`

### Portfolio Check
1. Batch quote: `twelvedata_quote_batch(symbols=["AAPL", "MSFT", "GOOGL", "TSLA"])`
2. Analyze each stock individually if needed

### Market Scan
1. List all stocks: `twelvedata_stocks(exchange="NASDAQ")`
2. Filter and analyze specific symbols
