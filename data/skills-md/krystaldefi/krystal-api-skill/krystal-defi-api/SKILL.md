---
name: krystal-defi-api
description: Provides DeFi liquidity pool data, vault management, user positions, and LP transaction-building via the Krystal API. Use for pool analytics (TVL/volume/APR), listing positions (including single-position lookup by positionId), and LP actions like zap-in, zap-out (including fee-claim via liquidityPercent=0), swap-and-increase, adjust-range (rebalance), and compound across chains like Ethereum, BSC, Polygon, Arbitrum, Base, and Solana.
---

# Krystal API

DeFi liquidity pool explorer and transaction API supporting 13+ blockchains.

## Quick Start

**Base URL**: `https://api.krystal.app`

```bash
# Get top pools across all chains
curl "https://api.krystal.app/all/v2/lp_explorer/top_pools?skipCheckAutomation=true"

# Get pool details
curl "https://api.krystal.app/all/v1/lp_explorer/pool_detail?chainId=8453&poolAddress=0x..."
```

## Instructions

### Finding Pools

1. Use [Top Pools](reference/top-pools.md) to discover high-performing pools
2. Use [Pool Detail](reference/pool-detail.md) for specific pool information
3. Use [Pool Chart](reference/pool-chart.md) for liquidity distribution visualization

### Creating LP Positions

1. Get pool details including `tickSpacing` from Pool Detail
2. Calculate tick range aligned with pool's tick spacing
3. Use [Zap In](reference/lp-actions/zap-in.md) to build the transaction
4. Sign and send `txData` using a web3 provider

### Increasing Liquidity (Swap and Increase)

1. Get position `tokenId` from [User Positions](reference/user-positions.md) (for Solana, also pass `nftMintAddress`)
2. Use [Swap and Increase](reference/lp-actions/swap-and-increase.md) with `tokenInAddress`, `amountIn`, `swapSlippage`, and `liquiditySlippage`
3. Set `fundFromOwner=true` and `isVault=true` when adding to a Krystal [auto-farm vault](reference/vaults.md) position
4. Sign and send `txData` using a web3 provider (same as Zap In)

### Withdrawing LP Positions (Zap Out)

1. Get position `tokenId` from [User Positions](reference/user-positions.md) (for Solana, also pass `nftMintAddress`)
2. Use [Zap Out](reference/lp-actions/zap-out.md) with `targetToken`, `liquidityPercent`, `swapSlippage`, and `withdrawSlippage`
   - Set `liquidityPercent = 0` to **claim only fees** (principal stays in the pool; claimed tokens are swapped to `targetToken`)
   - Use `0 < liquidityPercent ≤ 1` to withdraw principal liquidity (plus any fees) to `targetToken`
3. Sign and send `txData` using a web3 provider (same as Zap In)

### Compounding Fees into a Position

1. Get position `tokenId` from [User Positions](reference/user-positions.md) (for Solana, also pass `nftMintAddress`)
2. Use [Compound](reference/lp-actions/compound.md) with `swapSlippage` and `liquiditySlippage` to reinvest unclaimed fees back into the same position
3. Set `isVault=true` when compounding a Krystal [auto-farm vault](reference/vaults.md) position
4. Sign and send `txData` using a web3 provider

### Rebalancing Positions (Adjust Range)

1. Get position `tokenId` from [User Positions](reference/user-positions.md) (for Solana, also pass `nftMintAddress`)
2. Get pool `tickSpacing` from [Pool Detail](reference/pool-detail.md) and choose new `newTickLower` and `newTickUpper` aligned with it
3. Use [Adjust Range](reference/lp-actions/adjust-range.md) with `swapSlippage`, `liquiditySlippage`, and `withdrawSlippage`
4. On EVM chains, sign and send `txData` directly. On Solana, call with `buildTx=true` first to get `txData`, then sign and send it.

### Exploring Vaults

1. Use [Vaults](reference/vaults.md) to list available vaults
2. Filter by `category` (`ALL_VAULT`, `NEW_VAULT`, `BOOST_VAULT`) and `isAutoFarmVault` to narrow results
3. Evaluate vaults by `tvl`, `apr`, `riskScore`, and `vaultSecurities`
4. Use [Vault Profile Stats](reference/vaults.md#vault-profile-stats) to get a wallet's aggregate vault statistics (owned, joined, yields, PnL)

### Viewing Positions

1. Use [User Positions](reference/user-positions.md) to list a wallet's liquidity positions
2. Check `statsByChain["all"]` for aggregate portfolio metrics (total PnL, APR, unclaimed fees)
3. Filter by `chainIds` or `positionStatus` (`open`/`closed`) to narrow results
4. Evaluate individual positions by `pnl`, `apr`, `impermanentLoss`, `compareWithHodl`, and `status` (`IN_RANGE`/`OUT_RANGE`)
5. Use `refreshAll=true` for fresh on-chain data (slower) or omit for cached data (faster)

### Wallet Operations

1. Use [Token Search](reference/token-search.md) to get user's token balances
2. Select input token for swap/zap operations

## Key Conventions

- **Always use** `skipCheckAutomation=true` for faster responses
- **Monetary values**: Returned as strings to preserve precision
- **APR values**: Returned as numbers (percentages)
- **Native tokens**: Use [NativeTokenAddress](types.md#nativetokenaddress) placeholders
- **Amounts**: Always in wei (smallest unit)

## Endpoints Reference

| Endpoint | Purpose |
|----------|---------|
| [Top Pools](reference/top-pools.md) | Discover pools by TVL, volume, APR |
| [Pool Detail](reference/pool-detail.md) | Get pool info, tick spacing, incentives |
| [Pool Chart](reference/pool-chart.md) | Liquidity distribution and price history |
| [Zap In](reference/lp-actions/zap-in.md) | Build swap + mint transaction |
| [Swap and Increase](reference/lp-actions/swap-and-increase.md) | Add liquidity to existing position (swap + increase) |
| [Zap Out](reference/lp-actions/zap-out.md) | Build withdraw + swap transaction |
| [Compound](reference/lp-actions/compound.md) | Reinvest unclaimed fees into existing position |
| [Adjust Range](reference/lp-actions/adjust-range.md) | Rebalance position to new tick range |
| [User Positions](reference/user-positions.md) | List wallet LP positions & stats |
| [Vaults](reference/vaults.md) | List shared & auto-farm vaults |
| [Token Search](reference/token-search.md) | Query wallet token balances |

## Types Reference

See [types.md](types.md) for complete type definitions:

**Core Types**: [Token](types.md#token), [Pool](types.md#pool), [PoolDetail](types.md#pooldetail), [ChainId](types.md#chainid), [LPProtocolAlias](types.md#lpprotocolalias)

**Chart Types**: [PoolChartData](types.md#poolchartdata), [Tick](types.md#tick), [PricePoint](types.md#pricepoint)

**Transaction Types**: [TxData](types.md#txdata), [ZapTxInfo](types.md#zaptxinfo), [SwapAmount](types.md#swapamount)

**Position Types**: [UserPosition](types.md#userposition), [PositionChainStats](types.md#positionchainstats), [PositionTokenAmount](types.md#positiontokenamount), [PositionPool](types.md#positionpool)

**Vault Types**: [Vault](types.md#vault), [VaultOwner](types.md#vaultowner), [VaultSecurity](types.md#vaultsecurity), [VaultStats](types.md#vaultstats)

**Wallet Types**: [WalletToken](types.md#wallettoken), [TokenBalance](types.md#tokenbalance)
