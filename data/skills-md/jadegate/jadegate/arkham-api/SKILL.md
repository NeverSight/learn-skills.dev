---
name: arkham-api
description: Interact with Arkham Intelligence API for blockchain analytics - wallet analysis, transfers tracking, token flows, entity intelligence, portfolio analysis, and on-chain investigations. Use when analyzing crypto addresses, tracking whale movements, investigating transactions, or getting blockchain intelligence.
user-invocable: true
allowed-tools: Bash(curl:*), Bash(jq:*), Read, Grep, Glob
---

# Arkham Intelligence API Skill

## Configuration

**API Key** must be set in Claude Code settings:

```json
// ~/.claude/settings.json
{
  "env": {
    "ARKHAM_API_KEY": "your_api_key_here"
  }
}
```

Restart Claude Code after adding the key.

## Making API Calls

**Important**: Always use this pattern for API calls:

```bash
KEY=$(printenv ARKHAM_API_KEY)
curl -s "https://api.arkm.com/ENDPOINT" -H "API-Key: $KEY" | jq .
```

## Rate Limits

- **Standard endpoints**: 20 req/sec
- **Heavy endpoints** (1 req/sec): `/transfers`, `/swaps`, `/counterparties/*`, `/token/top_flow/*`, `/token/volume/*`

## Quick Reference

### Intelligence
```bash
# Address info
curl -s "https://api.arkm.com/intelligence/address/0x...?chain=ethereum" -H "API-Key: $KEY" | jq .

# Entity info (binance, wintermute, jump-trading, etc.)
curl -s "https://api.arkm.com/intelligence/entity/wintermute" -H "API-Key: $KEY" | jq .
```

### Balances & Portfolio
```bash
# Entity balances
curl -s "https://api.arkm.com/balances/entity/wintermute" -H "API-Key: $KEY" | jq .

# Address balances
curl -s "https://api.arkm.com/balances/address/0x...?chains=ethereum,solana" -H "API-Key: $KEY" | jq .
```

### Transfers
```bash
# Recent transfers from entity
curl -s "https://api.arkm.com/transfers?base=binance&flow=out&timeLast=24h&limit=20" -H "API-Key: $KEY" | jq .

# Large transfers
curl -s "https://api.arkm.com/transfers?usdGte=1000000&timeLast=24h&limit=50" -H "API-Key: $KEY" | jq .
```

### Token Analysis
```bash
# Top holders
curl -s "https://api.arkm.com/token/holders/pepe?groupByEntity=true" -H "API-Key: $KEY" | jq .

# Trending tokens
curl -s "https://api.arkm.com/token/trending" -H "API-Key: $KEY" | jq .

# Top tokens by volume
curl -s "https://api.arkm.com/token/top?timeframe=24h&orderByAgg=volume&orderByDesc=true&orderByPercent=false&from=0&size=20" -H "API-Key: $KEY" | jq .

# Token flows (inflows/outflows)
curl -s "https://api.arkm.com/token/top_flow/ethereum?timeLast=24h" -H "API-Key: $KEY" | jq .
```

### Market Data
```bash
# Network status (prices, volume, market cap)
curl -s "https://api.arkm.com/networks/status" -H "API-Key: $KEY" | jq .

# Altcoin index (altseason indicator)
curl -s "https://api.arkm.com/marketdata/altcoin_index" -H "API-Key: $KEY" | jq .
```

## Practical Use Cases

### 1. Find Smart Money / Market Makers
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Get market maker info
curl -s "https://api.arkm.com/intelligence/entity/wintermute" -H "API-Key: $KEY" | jq .

# Check their holdings (balances organized by chain)
cat > /tmp/flatten_balances.jq << 'EOF'
[.balances | to_entries[] | .key as $chain | .value[] | {symbol, usd, chain: $chain}] | sort_by(-.usd) | .[:10]
EOF
curl -s "https://api.arkm.com/balances/entity/wintermute" -H "API-Key: $KEY" | jq -f /tmp/flatten_balances.jq

# Get total portfolio value (totalBalance is object by chain)
curl -s "https://api.arkm.com/balances/entity/wintermute" -H "API-Key: $KEY" | jq '[.totalBalance | to_entries[] | .value] | add'
```

### 2. Analyze Whale Holdings for Meme/Speculative Tokens
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Get portfolio and filter by USD value (must flatten across chains first)
cat > /tmp/whale_holdings.jq << 'EOF'
[.balances | to_entries[] | .value[] | select(.usd > 100000) | {symbol, usd}] | sort_by(-.usd)
EOF
curl -s "https://api.arkm.com/balances/entity/wintermute" -H "API-Key: $KEY" | jq -f /tmp/whale_holdings.jq
```

### 3. Track Large Movements
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Whale transfers last 24h (note: use historicalUSD, not unitValueUsd)
curl -s "https://api.arkm.com/transfers?usdGte=5000000&timeLast=24h&limit=50" -H "API-Key: $KEY" \
  | jq '.transfers[] | {from: .fromAddress.arkhamEntity.name, to: .toAddress.arkhamEntity.name, usd: .historicalUSD, token: .tokenSymbol}'
```

### 4. Token Holder Analysis
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Who holds this token? (entityTopHolders organized by chain)
cat > /tmp/token_holders.jq << 'EOF'
[.entityTopHolders | to_entries[] | .key as $chain | .value[:10][] | {
  entity: .entity.name,
  type: .entity.type,
  usd,
  chain: $chain
}] | sort_by(-.usd) | .[:15]
EOF
curl -s "https://api.arkm.com/token/holders/pepe?groupByEntity=true" -H "API-Key: $KEY" | jq -f /tmp/token_holders.jq
```

### 5. ETH Accumulation Analysis (Who's Buying/Selling)
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Create filter for complex jq query (avoids bash escaping issues)
cat > /tmp/accumulators.jq << 'EOF'
[.[] | select(.address.arkhamEntity.name != null) | {
  entity: .address.arkhamEntity.name,
  type: .address.arkhamEntity.type,
  net_flow_usd: (.inUSD - .outUSD),
  inETH: .inValue,
  outETH: .outValue
}] | sort_by(-.net_flow_usd) | .[:20]
EOF

# Find who's accumulating ETH (positive net flow = buying)
curl -s "https://api.arkm.com/token/top_flow/ethereum?timeLast=7d" \
  -H "API-Key: $KEY" | jq -f /tmp/accumulators.jq

# Find who's distributing ETH (sort ascending for sellers)
cat > /tmp/sellers.jq << 'EOF'
[.[] | select(.address.arkhamEntity.name != null) | {
  entity: .address.arkhamEntity.name,
  type: .address.arkhamEntity.type,
  net_flow_usd: (.inUSD - .outUSD)
}] | sort_by(.net_flow_usd) | .[:15]
EOF

curl -s "https://api.arkm.com/token/top_flow/ethereum?timeLast=7d" \
  -H "API-Key: $KEY" | jq -f /tmp/sellers.jq
```

### 6. Track Hacker/Exploit Funds
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Check known hacker entity
curl -s "https://api.arkm.com/intelligence/entity/lazarus-group" -H "API-Key: $KEY" | jq '{name, type}'

# Check their current holdings
cat > /tmp/hacker_holdings.jq << 'EOF'
{
  total_usd: ([.totalBalance | to_entries[] | .value] | add),
  top_holdings: [.balances | to_entries[] | .value[] | {symbol, usd}] | sort_by(-.usd) | .[:10]
}
EOF
curl -s "https://api.arkm.com/balances/entity/lazarus-group" -H "API-Key: $KEY" | jq -f /tmp/hacker_holdings.jq

# Track their recent transfers
curl -s "https://api.arkm.com/transfers?base=lazarus-group&timeLast=30d&limit=20" -H "API-Key: $KEY" \
  | jq '.transfers[] | {to: .toAddress.arkhamEntity.name, usd: .historicalUSD, token: .tokenSymbol}'
```

### 7. Compare Market Maker Portfolios
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Download both portfolios
curl -s "https://api.arkm.com/balances/entity/wintermute" -H "API-Key: $KEY" > /tmp/wm.json
curl -s "https://api.arkm.com/balances/entity/jump-trading" -H "API-Key: $KEY" > /tmp/jt.json

# Compare totals and top holdings
cat > /tmp/portfolio_summary.jq << 'EOF'
{
  total_usd: ([.totalBalance | to_entries[] | .value] | add),
  top_5: [.balances | to_entries[] | .value[] | {symbol, usd}] | sort_by(-.usd) | .[:5]
}
EOF

echo "=== WINTERMUTE ===" && jq -f /tmp/portfolio_summary.jq /tmp/wm.json
echo "=== JUMP TRADING ===" && jq -f /tmp/portfolio_summary.jq /tmp/jt.json
```

### 8. Market-Wide CEX Flow Analysis (Sentiment Indicator)
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Analyze all CEX ETH flows to gauge market sentiment
cat > /tmp/cex_flows.jq << 'EOF'
[.[] | select(.address.arkhamEntity.type == "cex") | {
  exchange: .address.arkhamEntity.name,
  net_flow_usd: (.inUSD - .outUSD),
  inUSD,
  outUSD
}] | group_by(.exchange) | map({
  exchange: .[0].exchange,
  total_net_flow: (map(.net_flow_usd) | add),
  total_inflow: (map(.inUSD) | add),
  total_outflow: (map(.outUSD) | add)
}) | sort_by(-.total_net_flow)
EOF

curl -s "https://api.arkm.com/token/top_flow/ethereum?timeLast=7d" -H "API-Key: $KEY" | jq -f /tmp/cex_flows.jq
# Positive = accumulation (bullish), Negative = distribution (bearish)
```

### 9. Network Analysis - Find Entity Trading Partners
```bash
KEY=$(printenv ARKHAM_API_KEY)

# Get top counterparties aggregated across all chains
cat > /tmp/network.jq << 'EOF'
[to_entries[] | .key as $chain | .value[] | {
  counterparty: (.address.arkhamEntity.name // .address.arkhamLabel.name // "Unknown"),
  type: .address.arkhamEntity.type,
  usd,
  txCount: .transactionCount,
  chain: $chain
}] | group_by(.counterparty) | map({
  counterparty: .[0].counterparty,
  type: .[0].type,
  total_usd: (map(.usd) | add),
  total_tx: (map(.txCount) | add),
  chains: (map(.chain) | unique)
}) | sort_by(-.total_usd) | .[:15]
EOF

curl -s "https://api.arkm.com/counterparties/entity/wintermute?timeLast=30d&limit=100" \
  -H "API-Key: $KEY" | jq -f /tmp/network.jq
```

## Entity Types

- `exchange` - CEX (binance, coinbase)
- `market_maker` - MM (wintermute, jump-trading, cumberland-drw)
- `fund` - Investment funds (a16z, paradigm)
- `individual` - Whales (vitalik-buterin)
- `protocol` - DeFi (uniswap, aave)

## Common Parameters

| Param | Description | Example |
|-------|-------------|---------|
| `chain` | Single chain | `ethereum` |
| `chains` | Multiple chains | `ethereum,solana,base` |
| `timeLast` | Time window | `1h`, `24h`, `7d`, `30d` |
| `usdGte` | Min USD value | `1000000` |
| `limit` | Results limit | `50` |
| `flow` | Direction | `in`, `out`, `all` |

## Supported Chains

`ethereum`, `bitcoin`, `solana`, `polygon`, `arbitrum_one`, `base`, `optimism`, `avalanche`, `bsc`, `tron`, `ton`, `flare`, `mantle`, `dogecoin`, `sonic`, `zcash`

## Known Limitations & Gotchas

### Critical Issues (from benchmark testing)

| Issue | Severity | Workaround |
|-------|----------|------------|
| **Most endpoints organized by chain** | 🔴 Critical | Use `to_entries` to flatten |
| **`/transfers/entity/{entity}` doesn't exist** | 🔴 High | Use `/transfers?base={entity}` instead |
| **`/flow` ignores `timeLast`** | 🔴 High | Returns ALL history from 2017 (~500KB+) |
| **`/history` returns massive arrays** | 🔴 High | 3000+ items/chain, use `jq '.[0:10]'` to limit |
| **Balance inconsistency** | 🟡 Medium | `/balances` vs `/entity/summary` can differ by ~10% |
| **`/transfers/histogram` errors** | 🟡 Medium | Use `/histogram/simple` instead |
| **`/portfolio/timeSeries` needs `pricingId`** | 🟡 Medium | Add `?pricingId=usd` (may still return empty) |
| **`/token/top` requires `orderByPercent`** | 🟡 Medium | Add `&orderByPercent=false` (required param) |
| **`/health` returns plain text** | 🟢 Low | Returns "ok" not JSON |

### Endpoint-Specific Notes

- **`/transfers`**: Use `/transfers?base={entity}` (NOT `/transfers/entity/{entity}`), USD in `historicalUSD` field
- **`/swaps`**: Works - returns swap data with entity filtering
- **`/counterparties`**: HEAVY endpoint, organized by chain like balances
- **`/networks/status`**: Chain-organized object (`.ethereum.price`), not array
- **`/token/top`**: Requires `orderByPercent` param, returns `{tokens: [], total}`
- **`/token/holders`**: Uses `.entity.name` not `.arkhamEntity.name`
- **Heavy endpoints** (1 req/sec): `/transfers`, `/swaps`, `/counterparties/*`, `/token/top_flow/*`, `/token/volume/*`

### jq Escaping in Bash

Bash escapes special characters in jq filters. Use `.jq` files for complex queries:

```bash
# ❌ FAILS - bash escapes these operators:
#    !=  becomes \!=
#    //  becomes problematic (null coalescing)

# ✅ WORKS - write filter to file
cat > /tmp/filter.jq << 'EOF'
[.[] | select(.address.arkhamEntity.name != null) | {
  entity: (.address.arkhamEntity.name // "unknown"),
  type: .address.arkhamEntity.type,
  net_flow: (.inUSD - .outUSD)
}] | sort_by(-.net_flow)
EOF

curl -s "https://api.arkm.com/token/top_flow/ethereum?timeLast=7d" \
  -H "API-Key: $KEY" | jq -f /tmp/filter.jq

# ✅ For simple cases, use alternative syntax:
curl ... | jq 'select(.name | . != null)'  # wrap in subexpression
```

### Response Structure Variations

**⚠️ CRITICAL**: Most endpoints return data organized by chain, NOT flat arrays!

| Endpoint | Structure | How to Access |
|----------|-----------|---------------|
| `/balances/entity` | `{balances: {chain: [...]}, totalBalance: {chain: num}}` | `.balances.ethereum[]` or flatten with `to_entries` |
| `/token/holders` | `{entityTopHolders: {chain: [...]}}` | `.entityTopHolders.solana[]` |
| `/token/top_flow` | `[{address: {arkhamEntity}, inUSD, outUSD}]` | Direct array, entity in `.address.arkhamEntity` |
| `/counterparties` | `{chain: [...]}` | `.ethereum[]` (no wrapper key) |
| `/transfers` | `{transfers: [...]}` | `.transfers[]`, USD in `.historicalUSD` |
| `/token/trending` | `[{name, symbol, identifier}]` | Direct array, flat structure |
| `/token/top` | `{tokens: [...], total}` | `.tokens[]`, requires `orderByPercent` param |
| `/networks/status` | `{chain: {price, volume, ...}}` | `.ethereum.price`, chain-organized |
| `/loans/entity` | `{balances, entities, totalPositions}` | DeFi positions by protocol |

**Key Fields:**
- Transfers: `historicalUSD` (not `unitValueUsd`)
- Token holders: `.entity.name` (not `.arkhamEntity.name`)
- Balances: organized by chain, `totalBalance` is object not number

**Tip**: Always run `jq 'keys'` or `jq 'type'` first to explore unknown structures.

---

## All Endpoints Reference

For detailed parameters, see `ARKHAM_API_DOCUMENTATION.md`

| Category | Endpoint | Note |
|----------|----------|------|
| **Health** | `GET /health` | |
| | `GET /chains` | |
| **Transfers** | `GET /transfers` | HEAVY |
| | `GET /transfers/histogram` | HEAVY |
| | `GET /transfers/histogram/simple` | HEAVY |
| | `GET /swaps` | HEAVY, works |
| **Transaction** | `GET /tx/{hash}` | |
| **Intelligence** | `GET /intelligence/address/{address}` | |
| | `GET /intelligence/address/{address}/all` | Multi-chain |
| | `GET /intelligence/address_enriched/{address}` | With tags/predictions |
| | `GET /intelligence/address_enriched/{address}/all` | |
| | `GET /intelligence/entity/{entity}` | |
| | `GET /intelligence/entity/{entity}/summary` | |
| | `GET /intelligence/entity_predictions/{entity}` | ML predictions |
| | `GET /intelligence/contract/{chain}/{address}` | |
| | `GET /intelligence/token/{id}` | By CoinGecko ID |
| | `GET /intelligence/token/{chain}/{address}` | By contract |
| **Clusters & Tags** | `GET /cluster/{id}/summary` | |
| | `GET /tag/{id}/params` | |
| | `GET /tag/{id}/summary` | |
| **History** | `GET /history/entity/{entity}` | |
| | `GET /history/address/{address}` | |
| **Portfolio** | `GET /portfolio/entity/{entity}?time={ms}` | Snapshot |
| | `GET /portfolio/address/{address}?time={ms}` | |
| | `GET /portfolio/timeSeries/entity/{entity}` | Daily series |
| | `GET /portfolio/timeSeries/address/{address}` | |
| **Token** | `GET /token/top` | By exchange movements |
| | `GET /token/holders/{pricing_id}` | |
| | `GET /token/holders/{chain}/{address}` | |
| | `GET /token/trending` | |
| | `GET /token/trending/{id}` | |
| | `GET /token/top_flow/{id}` | HEAVY |
| | `GET /token/top_flow/{chain}/{address}` | HEAVY |
| | `GET /token/volume/{id}` | HEAVY |
| | `GET /token/volume/{chain}/{address}` | HEAVY |
| | `GET /token/balance/{id}` | |
| | `GET /token/balance/{chain}/{address}` | |
| **Balances** | `GET /balances/address/{address}` | |
| | `GET /balances/entity/{entity}` | |
| **Loans** | `GET /loans/address/{address}` | DeFi positions |
| | `GET /loans/entity/{entity}` | |
| **Counterparties** | `GET /counterparties/address/{address}` | HEAVY |
| | `GET /counterparties/entity/{entity}` | HEAVY |
| **Flow** | `GET /flow/address/{address}` | USD flows |
| | `GET /flow/entity/{entity}` | |
| **Networks** | `GET /networks/status` | |
| | `GET /networks/history/{chain}` | |
| **Market** | `GET /marketdata/altcoin_index` | |
| **User** | `GET /user/entities` | |
| | `GET /user/entities/{id}` | |
| | `GET /user/labels` | |
| | `POST /user/labels` | |
| **WebSocket** | `wss://api.arkm.com/ws/transfers` | Real-time |
