---
name: digital-assets
description: "Analyze digital assets including cryptocurrency fundamentals, blockchain mechanics, DeFi protocols, and on-chain metrics. Use when the user asks about crypto investing, Bitcoin, Ethereum, staking yields, DeFi lending, impermanent loss, or on-chain valuation metrics. Also trigger when users mention 'blockchain', 'proof of stake', 'proof of work', 'smart contracts', 'NFTs', 'stablecoins', 'NVT ratio', 'TVL', 'crypto portfolio allocation', 'halving', or ask about risks and returns of cryptocurrency."
---

# Digital Assets

## Purpose
Analyze digital assets including cryptocurrency fundamentals, blockchain mechanics, DeFi protocols, staking yields, and on-chain metrics. This skill covers the unique valuation challenges, risk characteristics, and technical mechanics of the digital asset ecosystem.

## Layer
2 — Asset Classes

## Direction
both

## When to Use
- User asks about cryptocurrency analysis or crypto portfolio allocation
- User asks about blockchain mechanics, consensus mechanisms (PoW, PoS)
- User asks about DeFi protocols, lending, or decentralized exchanges
- User asks about staking yields or validator economics
- User asks about on-chain metrics (NVT, active addresses, hash rate)
- User asks about stablecoin types or mechanisms
- User asks about impermanent loss in liquidity pools
- User asks about digital asset custody or regulatory considerations

## Core Concepts

### Blockchain Fundamentals
A distributed ledger maintained by a network of nodes. Transactions are grouped into blocks, cryptographically linked in sequence. Immutability comes from the chain structure — altering any block requires recomputing all subsequent blocks. Consensus mechanisms determine how the network agrees on the valid state of the ledger.

### Consensus Mechanisms
**Proof of Work (PoW):** Miners compete to solve computational puzzles. The winner adds the next block and earns a reward. High energy consumption but battle-tested security (Bitcoin). Security scales with hash rate.

**Proof of Stake (PoS):** Validators lock up tokens as collateral ("stake"). Block proposers are selected based on stake weight. Slashing penalizes malicious behavior. Far more energy-efficient than PoW. Ethereum transitioned to PoS in September 2022.

### Bitcoin
Fixed supply of 21 million coins, enforced by protocol rules. Block reward halves approximately every 4 years (halving cycle), reducing new supply issuance. Current block reward is 3.125 BTC (after April 2024 halving). Mining reward = block reward + transaction fees. Scarcity narrative drives the "digital gold" thesis.

### Ethereum
The leading smart contract platform. The Ethereum Virtual Machine (EVM) executes arbitrary programs (smart contracts). Gas fees compensate validators for computation. EIP-1559 introduced a base fee that is burned (destroyed), making ETH potentially deflationary when network usage is high. The merge to PoS (Sept 2022) reduced energy usage by ~99.95%.

### Staking Yield
For Proof of Stake networks:

Staking Yield = (Rewards + MEV Tips - Validator Costs) / Staked Amount

Rewards come from new token issuance and transaction fees. MEV (Maximal Extractable Value) provides additional income from transaction ordering. Validator costs include hardware, bandwidth, and the risk of slashing. Real yield (after accounting for inflation of token supply) can be significantly lower than nominal yield.

### DeFi (Decentralized Finance)
- **Lending protocols (Aave, Compound):** Users deposit assets to earn interest; borrowers post collateral to borrow. Interest rates are algorithmically determined by supply/demand (utilization rate).
- **DEXs (Uniswap, Curve):** Decentralized exchanges using automated market makers instead of order books. Liquidity providers deposit token pairs and earn trading fees.
- **Yield farming:** Deploying capital across DeFi protocols to maximize yield, often involving multiple protocol interactions and leverage.

### Automated Market Maker (AMM)
The constant product formula: x * y = k

where x and y are the reserves of two tokens in a liquidity pool. Price is determined by the ratio of reserves. Large trades cause slippage (price impact proportional to trade size relative to pool depth).

### Impermanent Loss
The loss that liquidity providers experience relative to simply holding the tokens when prices change:

IL = 2 * sqrt(p_ratio) / (1 + p_ratio) - 1

where p_ratio = new_price / old_price for one token relative to the other. At a 2x price change, IL is approximately 5.7%. At a 5x change, IL is approximately 25.5%. "Impermanent" because the loss reverses if prices return to original levels — but it becomes permanent if the LP withdraws at diverged prices.

### On-Chain Metrics
- **NVT Ratio (Network Value to Transactions):** Market cap / daily transaction volume (on-chain). Analogous to P/E for equities. Higher NVT suggests overvaluation relative to network usage.
- **Active addresses:** Number of unique addresses transacting daily. Proxy for network adoption.
- **Hash rate (PoW):** Total computational power securing the network. Higher hash rate = more security.
- **TVL (Total Value Locked):** Total value of assets deposited in DeFi protocols. Measure of DeFi ecosystem size.

### Stablecoin Types
- **Fiat-backed (USDC, USDT):** Each token backed by reserves of fiat currency or equivalents. Centralized issuance and custody.
- **Crypto-backed (DAI):** Overcollateralized with cryptocurrency. Decentralized but capital-inefficient.
- **Algorithmic:** Maintain peg through minting/burning mechanisms without full collateral backing. Higher risk of de-peg (e.g., UST/Luna collapse in 2022).

### Token Valuation
No universally accepted model. Approaches include:
- NVT ratio (compare to peers and historical range)
- Fees/revenue analysis (protocol revenue as proxy for earnings)
- TVL multiples (market cap / TVL)
- Fully diluted valuation (FDV) vs circulating supply market cap
- Discounted cash flow on protocol fee revenue (experimental)

### Custody
**Self-custody:** Hardware wallets (Ledger, Trezor) or software wallets. User controls private keys. "Not your keys, not your coins." Risk of loss if keys are lost.

**Custodial:** Exchanges (Coinbase, Kraken) or qualified custodians hold assets on behalf of users. Convenience but counterparty risk (e.g., FTX collapse).

### Regulatory Considerations
Regulatory treatment is evolving. In the US, crypto is generally treated as property for tax purposes — each sale, exchange, or use is a taxable event. Securities classification (Howey test) remains contentious for many tokens. Regulatory clarity is improving but varies significantly by jurisdiction.

## Key Formulas

| Formula | Expression | Use Case |
|---------|-----------|----------|
| Staking Yield | (Rewards + MEV - Costs) / Staked Amount | Validator return |
| Impermanent Loss | 2*sqrt(p_ratio)/(1+p_ratio) - 1 | LP loss from price divergence |
| AMM Price | Price_x = y/x (for token x in terms of y) | DEX pricing |
| NVT Ratio | Market Cap / Daily On-Chain Tx Volume | Network valuation metric |
| Real Staking Yield | Nominal Yield - Token Inflation Rate | Inflation-adjusted return |

## Worked Examples

### Example 1: Staking Yield on Ethereum
**Given:** 32 ETH staked (one validator), 4.5% APR nominal yield, ETH price = $3,000
**Calculate:** Annual rewards in ETH and USD
**Solution:**
Annual ETH rewards = 32 ETH × 4.5% = 1.44 ETH
Annual USD value = 1.44 ETH × $3,000 = $4,320
Total staked value = 32 × $3,000 = $96,000

If ETH supply inflation is approximately 0.5% per year (net of EIP-1559 burns), the real staking yield is roughly 4.5% - 0.5% = 4.0%. Note that the USD return depends entirely on ETH price changes — a 10% decline in ETH price would far exceed the 4.5% staking yield.

### Example 2: Impermanent Loss Calculation
**Given:** A liquidity provider deposits equal value of ETH and USDC into a Uniswap pool. ETH price doubles from $2,000 to $4,000.
**Calculate:** Impermanent loss
**Solution:**
p_ratio = $4,000 / $2,000 = 2.0
IL = 2 × sqrt(2.0) / (1 + 2.0) - 1
IL = 2 × 1.4142 / 3.0 - 1
IL = 2.8284 / 3.0 - 1
IL = 0.9428 - 1 = -0.0572 = -5.72%

The LP's position is worth 5.72% less than if they had simply held the tokens. If the pool earned 8% in trading fees over the period, the net return is 8% - 5.72% = 2.28% — still positive but substantially reduced. If ETH had tripled (p_ratio = 3), IL would be approximately 13.4%, potentially exceeding fee income.

## Common Pitfalls
- Confusing APR with APY — compounding matters significantly at high yield rates (100% APR ≈ 171.8% APY)
- Impermanent loss can exceed trading fee income — LPs can have negative returns even in active pools if price divergence is large
- Smart contract risk in DeFi protocols — bugs, exploits, and rug pulls can result in total loss of deposited funds
- Comparing crypto "yields" to traditional fixed income — very different risk profiles; crypto yields compensate for smart contract risk, impermanent loss, token price volatility, and regulatory uncertainty

## Cross-References
- **historical-risk** (wealth-management plugin, Layer 1a): volatility and risk measurement (crypto exhibits extreme volatility)
- **currencies-and-fx** (wealth-management plugin, Layer 2): stablecoin and crypto-fiat exchange dynamics
- **alternatives** (wealth-management plugin, Layer 2): crypto as an alternative asset class
- **tax-efficiency** (wealth-management plugin, Layer 5): cryptocurrency tax reporting and optimization

## Reference Implementation
N/A — this skill is qualitative and does not require a computational script.
