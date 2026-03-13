---
name: coinglass
version: 1.0.0
description: Comprehensive crypto derivatives data - funding rates, open interest, liquidations, long/short ratios, Hyperliquid whale tracking, volume analysis, ETF flows, futures market data
tools:
  # Basic Derivatives (7 tools)
  - funding_rate
  - long_short_ratio
  - cg_open_interest
  - cg_liquidations
  - cg_liquidation_analysis
  - cg_supported_coins
  - cg_supported_exchanges

  # Advanced Long/Short Ratios (6 tools)
  - cg_global_account_ratio
  - cg_top_account_ratio
  - cg_top_position_ratio
  - cg_taker_exchanges
  - cg_net_position
  - cg_net_position_v2

  # Advanced Liquidations (4 tools)
  - cg_coin_liquidation_history
  - cg_pair_liquidation_history
  - cg_liquidation_coin_list
  - cg_liquidation_orders

  # Hyperliquid Whale Tracking (4 tools)
  - cg_hyperliquid_whale_alerts
  - cg_hyperliquid_whale_positions
  - cg_hyperliquid_positions_by_coin
  - cg_hyperliquid_position_distribution

  # Futures Market Data (5 tools)
  - cg_coins_market_data
  - cg_pair_market_data
  - cg_ohlc_history
  - cg_taker_volume_history
  - cg_aggregated_taker_volume

  # Volume & Flow Analysis (4 tools)
  - cg_cumulative_volume_delta
  - cg_coin_netflow
  - cg_whale_transfers

  # Bitcoin ETF Data (5 tools)
  - cg_btc_etf_flows
  - cg_btc_etf_premium_discount
  - cg_btc_etf_history
  - cg_btc_etf_list
  - cg_hk_btc_etf_flows

  # Other ETF Data (8 tools)
  - cg_eth_etf_flows
  - cg_eth_etf_list
  - cg_eth_etf_premium_discount
  - cg_sol_etf_flows
  - cg_sol_etf_list
  - cg_xrp_etf_flows
  - cg_xrp_etf_list
  - cg_hk_eth_etf_flows

metadata:
  starchild:
    emoji: "📈"
    skillKey: coinglass
    plan: professional
    api_version: v4
    version: 3.0.0
    total_tools: 37
    requires:
      env:
        - COINGLASS_API_KEY

user-invocable: false
disable-model-invocation: false
---

# Coinglass

Coinglass provides the most comprehensive crypto derivatives and institutional data available. 37 tools covering futures positioning, whale tracking, volume analysis, liquidations, and ETF flows.

**API Plan**: Professional ($699/month)
**Rate Limit**: 6000 requests/minute
**API Version**: V4 (with V2 backward compatibility)
**Total Tools**: 37 across 8 categories

## When to Use Coinglass

Use Coinglass for:
- **Derivatives positioning** - What are leveraged traders doing?
- **Whale tracking** - Track large positions on Hyperliquid DEX
- **Funding rates** - Cost of holding perpetual futures
- **Open interest** - Total notional value of open positions
- **Long/Short ratios** - Sentiment among leveraged traders (global, top accounts, top positions)
- **Liquidations** - Forced position closures with heatmaps and individual orders
- **Volume analysis** - Taker volume, CVD, netflow patterns
- **ETF flows** - Institutional adoption (Bitcoin, Ethereum, Solana, XRP, Hong Kong)
- **Whale transfers** - Large on-chain movements (>$10M)
- **Futures market data** - Supported coins, exchanges, pairs, and OHLC price history

## Tool Categories

### 1. Basic Derivatives Analytics (7 tools)

Core derivatives data for market analysis:

- `funding_rate(symbol, exchange?)` - Current funding rates
- `long_short_ratio(symbol, exchange?, interval?)` - Basic L/S ratios
- `cg_open_interest(symbol)` - Current OI across exchanges
- `cg_liquidations(symbol, time?)` - Recent liquidations
- `cg_liquidation_analysis(symbol)` - Liquidation heatmap analysis
- `cg_supported_coins()` - All supported coins
- `cg_supported_exchanges()` - All exchanges with pairs

### 2. Advanced Long/Short Ratios (6 tools)

Deep positioning analysis with multiple metrics:

- `cg_global_account_ratio(symbol, interval?)` - Global account-based L/S ratio
- `cg_top_account_ratio(symbol, exchange, interval?)` - Top trader accounts ratio
- `cg_top_position_ratio(symbol, exchange, interval?)` - Top positions by size
- `cg_taker_exchanges(symbol)` - Taker buy/sell by exchange
- `cg_net_position(symbol, exchange)` - Net long/short positions
- `cg_net_position_v2(symbol)` - Enhanced net position data

**Use cases**:
- Smart money tracking (top accounts vs retail)
- Exchange-specific sentiment
- Position size distribution analysis

### 3. Advanced Liquidations (4 tools)

Granular liquidation tracking for cascade prediction:

- `cg_coin_liquidation_history(symbol, interval?, limit?, start_time?, end_time?)` - Aggregated across all exchanges
- `cg_pair_liquidation_history(symbol, exchange, interval?, limit?, start_time?, end_time?)` - Exchange-specific pair
- `cg_liquidation_coin_list(exchange)` - All coins on an exchange
- `cg_liquidation_orders(symbol, exchange, min_liquidation_amount, start_time?, end_time?)` - Individual orders (past 7 days, max 200)

**Use cases**:
- Identifying liquidation clusters
- Tracking liquidation patterns over time
- Finding large liquidation events

### 4. Hyperliquid Whale Tracking (4 tools)

Track large traders on Hyperliquid DEX (~200 recent alerts):

- `cg_hyperliquid_whale_alerts()` - Recent large position opens/closes (>$1M)
- `cg_hyperliquid_whale_positions()` - Current whale positions with PnL
- `cg_hyperliquid_positions_by_coin()` - All positions grouped by coin
- `cg_hyperliquid_position_distribution()` - Distribution by size with sentiment

**Use cases**:
- Following smart money on Hyperliquid
- Detecting large position changes
- Tracking whale PnL and sentiment

### 5. Futures Market Data (5 tools)

Market overview and price data:

- `cg_coins_market_data()` - ALL coins data in one call (100+ coins)
- `cg_pair_market_data(symbol, exchange)` - Specific pair metrics
- `cg_ohlc_history(symbol, exchange, interval, limit?)` - OHLC candlesticks
- `cg_taker_volume_history(symbol, exchange, interval, limit?, start_time?, end_time?)` - Pair-specific taker volume
- `cg_aggregated_taker_volume(symbol, interval, limit?, start_time?, end_time?)` - Aggregated across exchanges

**Use cases**:
- Market screening (scan all coins at once)
- Price action analysis
- Volume pattern recognition

### 6. Volume & Flow Analysis (4 tools)

Order flow and capital movement tracking:

- `cg_cumulative_volume_delta(symbol, exchange, interval, limit?, start_time?, end_time?)` - CVD = Running total of (buy - sell)
- `cg_coin_netflow()` - Capital flowing into/out of coins
- `cg_whale_transfers()` - Large on-chain transfers (>$10M, past 6 months)

**Use cases**:
- Order flow divergence detection
- Smart money tracking
- Institutional movement monitoring

### 7. Bitcoin ETF Data (5 tools)

Track institutional Bitcoin adoption:

- `cg_btc_etf_flows()` - Daily net inflows/outflows
- `cg_btc_etf_premium_discount()` - ETF price vs NAV
- `cg_btc_etf_history()` - Comprehensive history (price, NAV, premium%, shares, assets)
- `cg_btc_etf_list()` - List of Bitcoin ETFs
- `cg_hk_btc_etf_flows()` - Hong Kong Bitcoin ETF flows

**Use cases**:
- Institutional demand tracking
- Premium/discount arbitrage
- Regional flow comparison (US vs Hong Kong)

### 8. Other ETF Data (8 tools)

Ethereum, Solana, XRP, and Hong Kong ETFs:

- `cg_eth_etf_flows()` - Ethereum ETF flows
- `cg_eth_etf_list()` - Ethereum ETF list
- `cg_eth_etf_premium_discount()` - ETH ETF premium/discount
- `cg_sol_etf_flows()` - Solana ETF flows
- `cg_sol_etf_list()` - Solana ETF list
- `cg_xrp_etf_flows()` - XRP ETF flows
- `cg_xrp_etf_list()` - XRP ETF list
- `cg_hk_eth_etf_flows()` - Hong Kong Ethereum ETF flows

**Use cases**:
- Multi-asset institutional tracking
- Comparative flow analysis
- Regional preference analysis

## Common Workflows

### Quick Market Scan
```
# Get everything in 3 calls
all_coins = cg_coins_market_data()  # 100+ coins with full metrics
btc_liquidations = cg_liquidations("BTC")
whale_alerts = cg_hyperliquid_whale_alerts()
```

### Deep Position Analysis
```
# BTC positioning across metrics
cg_global_account_ratio("BTC")  # Retail sentiment
cg_top_account_ratio("BTC", "Binance")  # Smart money
cg_net_position_v2("BTC")  # Net positioning
cg_liquidation_heatmap("BTC", "Binance")  # Cascade levels
```

### ETF Flow Monitoring
```
# Institutional demand
btc_flows = cg_btc_etf_flows()
eth_flows = cg_eth_etf_flows()
sol_flows = cg_sol_etf_flows()
```

### Whale Tracking
```
# Follow the whales
hyperliquid_whales = cg_hyperliquid_whale_alerts()
whale_positions = cg_hyperliquid_whale_positions()
onchain_whales = cg_whale_transfers()  # >$10M on-chain
```

### Volume Analysis
```
# Order flow
cvd = cg_cumulative_volume_delta("BTC", "Binance", "1h", 100)
netflow = cg_coin_netflow()  # All coins
taker_vol = cg_aggregated_taker_volume("BTC", "1h", 100)
```

## Interpretation Guides

### Funding Rates

| Rate (8h) | Read |
|------------|------|
| > +0.05% | Extreme greed — crowded long, squeeze risk |
| +0.01% to +0.05% | Bullish bias, normal |
| -0.005% to +0.01% | Neutral |
| -0.05% to -0.005% | Bearish bias, normal |
| < -0.05% | Extreme fear — crowded short, bounce risk |

Extreme funding often precedes reversals. The crowd is usually wrong at extremes.

### Open Interest + Price Matrix

| OI | Price | Read |
|----|-------|------|
| Up | Up | New longs entering — bullish conviction |
| Up | Down | New shorts entering — bearish conviction |
| Down | Up | Short covering — weaker rally, less conviction |
| Down | Down | Long liquidation — weaker selloff, capitulation |

### Long/Short Ratio

| Ratio | Read |
|-------|------|
| > 1.5 | Crowded long — contrarian bearish |
| 1.1–1.5 | Moderately bullish |
| 0.9–1.1 | Balanced |
| 0.7–0.9 | Moderately bearish |
| < 0.7 | Crowded short — contrarian bullish |

### CVD (Cumulative Volume Delta)

| Pattern | Read |
|---------|------|
| CVD rising, price rising | Strong buy pressure, healthy uptrend |
| CVD falling, price rising | Weak rally, distribution |
| CVD rising, price falling | Accumulation, potential bottom |
| CVD falling, price falling | Strong sell pressure, healthy downtrend |

### ETF Flows

| Flow | Read |
|------|------|
| Large inflows | Institutional buying, bullish |
| Consistent inflows | Sustained demand |
| Large outflows | Institutional selling, bearish |
| Premium to NAV | High demand, bullish sentiment |
| Discount to NAV | Weak demand, bearish sentiment |

## Analysis Patterns

**Multi-metric confirmation**: Combine tools across categories for high-confidence signals:
- Funding + L/S ratio + liquidations = positioning extremes
- CVD + taker volume + whale alerts = smart money direction
- ETF flows + whale transfers + open interest = institutional conviction

**Smart money vs retail**: Compare metrics to identify divergence:
- `cg_top_account_ratio` (smart money) vs `cg_global_account_ratio` (retail)
- Hyperliquid whale positions vs overall long/short ratios

**Cascade prediction**: Use liquidation tools to predict volatility:
- `cg_coin_liquidation_history` shows liquidation patterns over time
- `cg_liquidation_orders` reveals recent forced closures
- Large liquidation events = cascade risk zones

**Flow divergence**: Track capital movements:
- `cg_coin_netflow` shows where money is flowing
- `cg_whale_transfers` reveals large movements
- ETF flows show institutional demand

## Performance Optimization

### Batch vs Individual Calls

**✅ OPTIMAL**: Use batch endpoints
```
# One call gets 100+ coins
all_coins = cg_coins_market_data()

# One call gets all whale alerts
whales = cg_hyperliquid_whale_alerts()

# One call gets all ETF flows
btc_etf = cg_btc_etf_flows()
```

**❌ INEFFICIENT**: Multiple individual calls
```
# Don't do this - wastes API quota
btc = cg_pair_market_data("BTC", "Binance")
eth = cg_pair_market_data("ETH", "Binance")
sol = cg_pair_market_data("SOL", "Binance")
```

### Query Parameters

Most history endpoints support:
- `interval`: Time granularity (1h, 4h, 12h, 24h, etc.)
- `limit`: Number of records (default varies, max 1000)
- `start_time`: Unix timestamp (milliseconds)
- `end_time`: Unix timestamp (milliseconds)

Example:
```
cg_coin_liquidation_history(
    symbol="BTC",
    interval="1h",
    limit=100,
    start_time=1704067200000,  # 2024-01-01
    end_time=1704153600000     # 2024-01-02
)
```

## Supported Exchanges

Major exchanges with futures data:
- **Tier 1**: Binance, OKX, Bybit, Gate, KuCoin, MEXC
- **Traditional**: CME (Bitcoin and Ethereum futures), Coinbase
- **DEX**: Hyperliquid, dYdX, ApeX
- **Others**: Bitfinex, Kraken, HTX, BingX, Crypto.com, CoinEx, Bitget

Use `cg_supported_exchanges()` for complete list with pair details.

## Important Notes

- **API Key**: Requires COINGLASS_API_KEY environment variable
- **Symbols**: Use standard symbols (BTC, ETH, SOL, etc.) - check with `cg_supported_coins()`
- **Exchanges**: Check `cg_supported_exchanges()` for full list with pairs
- **Update Frequency**:
  - Market data: ≤ 1 minute
  - Funding rates: Every 8 hours (or 1 hour for some exchanges)
  - OHLC: Real-time to 1 minute depending on interval
  - ETF data: Daily (after market close)
  - Whale transfers: Real-time (within minutes)
- **API Versions**:
  - V4 endpoints use `CG-API-KEY` header (most tools)
  - V2 endpoints use `coinglassSecret` header (some legacy tools)
  - Both work with the same COINGLASS_API_KEY environment variable
- **Rate Limits**: Professional plan allows 6000 requests/minute
- **Historical Data Limits**:
  - Liquidation orders: Past 7 days, max 200 records
  - Whale transfers: Past 6 months, minimum $10M
  - Hyperliquid alerts: ~200 most recent large positions
  - Other endpoints: Typically months to years of history

## Data Quality Notes

- **Hyperliquid**: Data is exchange-specific, doesn't include other DEXs
- **Whale Transfers**: Covers Bitcoin, Ethereum, Tron, Ripple, Dogecoin, Litecoin, Polygon, Algorand, Bitcoin Cash, Solana
- **ETF Data**: US ETFs updated after market close (4 PM ET), Hong Kong ETFs updated after Hong Kong market close
- **Liquidation Orders**: Limited to 200 most recent, use heatmap for broader view
- **CVD**: Cumulative metric - resets are not automatic, track changes not absolute values

## Version History

- **v3.0.0** (2025-03): Added 36 new tools
  - Advanced liquidations (5 tools)
  - Hyperliquid whale tracking (5 tools)
  - Volume & flow analysis (5 tools)
  - Whale transfers (1 tool)
  - Bitcoin ETF (6 tools)
  - Other ETFs (8 tools)
  - Advanced L/S ratios (6 tools)
- **v2.2.0** (2024): V4 API migration with futures market data
- **v1.0.0** (2024): Initial release with basic derivatives data
