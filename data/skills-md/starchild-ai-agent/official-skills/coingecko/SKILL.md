---
name: coingecko
version: 1.0.0
description: CoinGecko crypto price data, charts, market discovery, and global stats
tools:
  - coin_price
  - coin_ohlc
  - coin_chart
  - cg_trending
  - cg_top_gainers_losers
  - cg_new_coins
  - cg_global
  - cg_global_defi
  - cg_categories
  - cg_derivatives
  - cg_derivatives_exchanges
  - cg_coins_list
  - cg_coins_markets
  - cg_coin_data
  - cg_coin_tickers
  - cg_exchanges
  - cg_exchange
  - cg_exchange_tickers
  - cg_exchange_volume_chart
  - cg_nfts_list
  - cg_nft
  - cg_nft_by_contract
  - cg_asset_platforms
  - cg_exchange_rates
  - cg_vs_currencies
  - cg_categories_list
  - cg_search
  - cg_token_price
  - cg_coin_by_contract

metadata:
  starchild:
    emoji: "🦎"
    skillKey: coingecko
    requires:
      env:
        - COINGECKO_API_KEY

user-invocable: false
disable-model-invocation: false
---

# CoinGecko

CoinGecko provides comprehensive crypto market data including spot prices, OHLC candles, market cap, trending coins, sector performance, and global stats.

## When to Use CoinGecko

Use CoinGecko for:
- **Price queries** - Current prices, historical prices, OHLC data
- **Market overview** - Market cap, volume, trending coins, top gainers/losers
- **Coin information** - Detailed coin data, tickers, trading pairs
- **Exchange data** - Exchange listings, volumes, trading pairs
- **NFT data** - NFT collections, floor prices, market stats
- **Global metrics** - Total market cap, dominance, DeFi stats
- **Categories** - Sector performance (DeFi, Gaming, Layer 1, etc.)

## Common Workflows

### Get Coin Price
```
coin_price(coin_id="bitcoin")  # Supports symbols like BTC, ETH, SOL
coin_price(coin_id="ethereum", vs_currencies="usd,eur")
```

### Historical Data
```
coin_ohlc(coin_id="bitcoin", vs_currency="usd", days=7)  # OHLC candles
coin_chart(coin_id="ethereum", vs_currency="usd", days=30)  # Price chart data
```

### Market Discovery
```
cg_trending()  # Trending coins in the last 24h
cg_top_gainers_losers()  # Top movers
cg_new_coins()  # Recently listed coins
cg_coins_markets(vs_currency="usd", order="market_cap_desc", per_page=100)
```

### Coin Information
```
cg_coin_data(id="bitcoin")  # Detailed coin data
cg_coin_tickers(id="ethereum")  # All trading pairs
cg_search(query="solana")  # Search for coins
```

### Exchange Data
```
cg_exchanges()  # All exchanges
cg_exchange(id="binance")  # Specific exchange
cg_exchange_tickers(id="binance")  # Exchange trading pairs
cg_exchange_volume_chart(id="binance", days=7)
```

### Global Metrics
```
cg_global()  # Total market stats
cg_global_defi()  # DeFi specific stats
cg_categories()  # Sector performance
```

### Contract Address Queries
```
cg_token_price(contract_addresses=["0x..."], vs_currencies="usd")
cg_coin_by_contract(contract_address="0x...", platform="ethereum")
```

## Important Notes

- **Coin IDs**: CoinGecko uses slug IDs (e.g., "bitcoin", "ethereum", "solana"). The tools auto-resolve common symbols like BTC, ETH, SOL.
- **API Key**: Requires COINGECKO_API_KEY environment variable (Pro API)
- **Rate Limits**: Be mindful of API rate limits. Use batch endpoints when querying multiple coins.
- **vs_currencies**: Most endpoints support multiple currencies (usd, eur, btc, eth, etc.). Use `cg_vs_currencies()` to see all supported currencies.

## Symbol Resolution

Common symbols are automatically resolved:
- BTC → bitcoin
- ETH → ethereum
- SOL → solana
- USDT → tether
- USDC → usd-coin
- BNB → binancecoin

**Important:** If unsure about a coin ID, always use `cg_search(query="coin name")` first to find the exact CoinGecko ID before calling price tools.
