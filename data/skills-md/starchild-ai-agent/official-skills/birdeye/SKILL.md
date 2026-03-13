---
name: birdeye
version: 1.0.0
description: Token intelligence and wallet analytics for Solana and EVM chains. Use for token security checks, comprehensive token data, and wallet portfolio analysis.
tools:
  - birdeye_token_security
  - birdeye_token_overview
  - birdeye_wallet_networth

metadata:
  starchild:
    emoji: "👁️"
    skillKey: birdeye
    requires:
      env: [BIRDEYE_API_KEY]

user-invocable: false
disable-model-invocation: false
---

# Birdeye

Multi-chain data provider for token intelligence and wallet analytics. Covers Solana + EVM chains (Ethereum, Arbitrum, Base, etc.). Focus on Birdeye's unique capabilities for security analysis and portfolio tracking.

## Available Tools (3)

### Token Intelligence (2 tools)
- **birdeye_token_security**: Security score and rug pull risk analysis
- **birdeye_token_overview**: Comprehensive token data (price, volume, market cap, liquidity)

### Wallet Analytics (1 tool)
- **birdeye_wallet_networth**: Current wallet net worth and portfolio breakdown

## When to Use Each Tool

**"Is this token safe?"** → `birdeye_token_security`
Security score, rug pull risk analysis, and contract vulnerability detection.

**"Give me the full rundown on this token"** → `birdeye_token_overview`
Price, volume, market cap, liquidity, and price changes all in one call.

**"What's this wallet worth?"** → `birdeye_wallet_networth`
Current portfolio value and detailed token breakdown with balances and values.

## Multi-Chain Support

All tools accept a `chain` parameter:
- **Solana**: `solana` (default for most queries)
- **EVM**: `ethereum`, `arbitrum`, `base`, `optimism`, `polygon`, `bsc`, `avalanche`, `zksync`, `sui`

**Chain selection guidelines:**
- Solana: Most active trading, best for memecoins
- Ethereum: Blue-chip tokens, DeFi protocols
- Arbitrum/Base: L2 trading, low-fee DeFi
- Use the chain where the token/wallet is native

## Interpretation Guides

### Security Scores

| Score | Risk Level | Action |
|-------|-----------|--------|
| 90-100 | Very Low | Safe to trade, verified contract |
| 70-89 | Low | Generally safe, standard risks |
| 50-69 | Medium | Proceed with caution, check issues list |
| 30-49 | High | High risk — investigate issues carefully |
| 0-29 | Very High | Likely rug pull or scam — avoid |

**Common red flags:**
- Mint authority not renounced (owner can print tokens)
- Freeze authority enabled (owner can freeze trading)
- Low liquidity (< $10k = high rug risk)
- Concentrated holdings (top 10 holders > 80% supply)
- No social links or website

### Token Overview Metrics

**Price & Market Cap**: Current valuation and trading price
**Volume**: Trading activity indicates liquidity and interest
**Liquidity**: Available liquidity for trades (higher = safer exits)
**Price Change %**: 1h/24h/7d price movements

**Interpreting liquidity:**
- < $10k: Very high risk, easy to manipulate
- $10k-$100k: Moderate risk, watch for large exits
- $100k-$1M: Good liquidity for small/medium trades
- > $1M: Strong liquidity, safer for larger positions

### Wallet Net Worth

**Total USD Value**: Sum of all token holdings at current prices
**Token Breakdown**: Individual holdings with balances and values
**Portfolio Concentration**: How diversified is the wallet?

**Portfolio health indicators:**
- High concentration (>80% in one token) = high risk
- Balanced holdings = better risk management
- Large unrealized gains = potential for profit-taking

## Common Workflows

### Token Due Diligence

1. **birdeye_token_security** — Security score and risk check
2. **birdeye_token_overview** — Price, volume, market cap, liquidity

**Red flags**: Low security score (<50) + low liquidity (<$10k) = rug pull risk

**Example:**
```
User: "Is this token safe? [Solana address]"
1. Check birdeye_token_security → Score 85 (Low risk)
2. Check birdeye_token_overview → $500k liquidity, $2M volume
3. Result: Generally safe, good liquidity for trading
```

### Wallet Analysis

1. **birdeye_wallet_networth** — Current portfolio value and breakdown

**Use cases:**
- Track your own portfolio value
- Analyze whale wallets
- Monitor competitor holdings

**Example:**
```
User: "What's in this wallet? [address]"
1. Check birdeye_wallet_networth → $45k total value
2. Breakdown: 60% SOL, 25% USDC, 15% memecoins
3. Result: Balanced Solana portfolio with stablecoin hedging
```

### Quick Token Check

For quick validation of a token before trading:

**birdeye_token_overview** → Get price, liquidity, volume in one call

If liquidity < $10k or volume < $1k → High risk, proceed with caution

## Tool Details

### birdeye_token_security

**Parameters:**
- `address` (required): Token contract address
- `chain` (optional): Blockchain (default: `solana`)

**Returns:**
- Security score (0-100)
- Risk level
- List of detected issues
- Contract analysis results

**Example:**
```
birdeye_token_security(
  address="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  chain="solana"
)
```

### birdeye_token_overview

**Parameters:**
- `address` (required): Token contract address
- `chain` (optional): Blockchain (default: `solana`)

**Returns:**
- Symbol, name
- Current price
- 24h volume
- Market cap
- Liquidity
- Price changes (1h, 24h, 7d)

**Example:**
```
birdeye_token_overview(
  address="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  chain="solana"
)
```

### birdeye_wallet_networth

**Parameters:**
- `wallet` (required): Wallet address
- `chain` (optional): Blockchain (default: `solana`)

**Returns:**
- Total USD value
- Token holdings breakdown:
  - Token symbol, name
  - Balance
  - Current price
  - USD value
  - Portfolio percentage

**Example:**
```
birdeye_wallet_networth(
  wallet="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
  chain="solana"
)
```

**Note**: Wallet APIs have rate limits (5 req/s, 75 req/min). Space out requests.

## Chain-Specific Notes

**Solana**:
- Best supported chain for Birdeye
- Token addresses are base58 encoded
- Most liquid trading on Raydium, Orca
- Use for memecoin analysis and portfolio tracking

**Ethereum**:
- Blue-chip tokens and DeFi protocols
- Token addresses are 0x... format
- Higher gas fees = less micro-trading

**Arbitrum/Base**:
- L2 scaling solutions with lower fees
- Growing DeFi ecosystem
- Good for L2-native projects

## Integration with Other Skills

**Complementary to CoinGecko:**
- Use **Birdeye** for: Security checks, Solana tokens, wallet analytics
- Use **CoinGecko** for: Broad market data, historical prices, market cap rankings

**Don't duplicate**: Each service has unique strengths. Use Birdeye for its specialized data (security, Solana focus, wallet tracking).

## Notes

- **API key required**: Set `BIRDEYE_API_KEY` environment variable
- **Rate limits**: Wallet endpoints limited to 5 req/s, 75 req/min
- **Multi-chain**: Always specify `chain` parameter for non-Solana queries
- **Security scores**: Automated analysis — validate manually for high-value trades
- **Real-time data**: Prices and data update frequently, good for active trading decisions

## Limitations

- **No trending tokens**: Use CoinGecko for trending/top tokens lists
- **No holder distribution**: Cannot check who holds a token
- **No trade history**: Cannot see recent trades
- **No smart money signals**: Use other sources for whale tracking
- **Limited wallet tools**: Only net worth available (no PnL, holdings detail, or transfers)

Focus on the 3 available tools for security checks, token overviews, and wallet valuations.
