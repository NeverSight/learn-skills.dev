---
name: lending
description: Activate when the user asks about lending, borrowing, Morpho markets, vaults, positions, leverage, looping strategies, or yield farming on Katana Network.
license: MIT
metadata:
  author: katana
  version: '1.0.0'
---

# Lending — Morpho on Katana

Lending, borrowing, leveraged loops, and vault deposits on Morpho Blue on Katana Network.

## Morpho Blue Overview

Morpho Blue is a permissionless lending protocol with two modes:

1. **Direct Markets** — isolated pairs with a specific collateral token, loan token, oracle, IRM (interest rate model), and LLTV (liquidation loan-to-value). Users supply loan tokens to earn interest or deposit collateral to borrow.
2. **MetaMorpho Vaults** — ERC-4626 vaults managed by curators that auto-allocate deposits across multiple markets. Simpler: just deposit and earn.

### Key Concepts

- **Market ID**: bytes32 hex string uniquely identifying a market (derived from `keccak256(abi.encode(MarketParams))`)
- **LLTV**: Liquidation Loan-to-Value ratio. If `borrowValue / collateralValue > LLTV`, the position is liquidatable. Higher LLTV = more leverage capacity but more risk.
- **Health Factor**: `(collateralValue × LLTV) / debtValue`. Below 1.0 = liquidatable. **Keep above 1.5 for safety.**
- **Utilization**: `totalBorrow / totalSupply`. Higher utilization = higher borrow rates but less available liquidity.

### MarketParams Struct

All market-specific functions require a `MarketParams` struct:

```
struct MarketParams {
  address loanToken;
  address collateralToken;
  address oracle;
  address irm;
  uint256 lltv;
}
```

### Contract Addresses (Mainnet)

| Contract | Address |
|----------|---------|
| Morpho Core | `0xD50F2DffFd62f94Ee4AEd9ca05C61d0753268aBc` |
| Bundler3 | `0xA8C5e23C9C0DF2b6fF716486c6bBEBB6661548C8` |
| GeneralAdapter1 | `0x916Aa175C36E845db45fF6DDB886AE437d403B61` |
| MetaMorphoFactory | `0x1c8de6889acee12257899bfeaa2b7e534de32e16` |
| MetaMorphoV1_1Factory | `0xd3f39505d0c48AFED3549D625982FdC38Ea9904b` |
| AdaptiveCurveIrm | `0x4F708C0ae7deD3d74736594C2109C2E3c065B428` |
| OracleFactory | `0x7D047fB910Bc187C18C81a69E30Fa164f8c536eC` |
| PublicAllocator | `0x39EB6Da5e88194C82B13491Df2e8B3E213eD2412` |

## Contracts & Functions

### Market Discovery

Scan `CreateMarket` events on Morpho Core to discover all markets:

```
event CreateMarket(bytes32 indexed id, MarketParams marketParams)
```

Read market state:
```
market(bytes32 id) → (
  uint128 totalSupplyAssets,
  uint128 totalSupplyShares,
  uint128 totalBorrowAssets,
  uint128 totalBorrowShares,
  uint128 lastUpdate,
  uint128 fee
)
```

Read market parameters:
```
idToMarketParams(bytes32 id) → MarketParams
```

Filter out dead markets (0 supply + 0 borrow). Calculate utilization as `totalBorrowAssets / totalSupplyAssets`.

### Vault Discovery

Scan `CreateMetaMorpho` events from MetaMorphoFactory and MetaMorphoV1_1Factory to find all vaults. Vaults are standard ERC-4626, so call:
- `asset() → address` — the underlying token
- `totalAssets() → uint256` — TVL
- `name() → string` / `symbol() → string`

### Position Queries

Call on Morpho Core:
```
position(bytes32 id, address user) → (
  uint256 supplyShares,
  uint128 borrowShares,
  uint128 collateral
)
```

Convert shares to assets using market state:
- `supplyAssets = supplyShares × totalSupplyAssets / totalSupplyShares`
- `borrowAssets = borrowShares × totalBorrowAssets / totalBorrowShares`

**If health factor < 1.0, the position is liquidatable.**

### Supply (Lend)

Call on Morpho Core:
```
supply(
  MarketParams memory marketParams,
  uint256 assets,
  uint256 shares,     // pass 0 to supply by asset amount
  address onBehalf,
  bytes memory data   // pass empty bytes
) → (uint256 assetsSupplied, uint256 sharesSupplied)
```

**Requires approval:** User must call `approve()` on the loan token for Morpho Core (`0xD50F...8aBc`).

### Withdraw

```
withdraw(
  MarketParams memory marketParams,
  uint256 assets,
  uint256 shares,     // pass 0 to withdraw by asset amount
  address onBehalf,
  address receiver
) → (uint256 assetsWithdrawn, uint256 sharesWithdrawn)
```

May fail if insufficient liquidity in the market (totalSupply - totalBorrow < withdrawal amount).

### Borrow

```
borrow(
  MarketParams memory marketParams,
  uint256 assets,
  uint256 shares,     // pass 0 to borrow by asset amount
  address onBehalf,
  address receiver
) → (uint256 assetsBorrowed, uint256 sharesBorrowed)
```

Requires sufficient collateral already deposited. The LLTV constrains maximum borrow. **Check health factor after borrowing.**

### Supply Collateral

```
supplyCollateral(
  MarketParams memory marketParams,
  uint256 assets,
  address onBehalf,
  bytes memory data   // pass empty bytes
)
```

**Requires approval** for the collateral token to Morpho Core.

### Vault Detail & Risk Inspection

MetaMorpho vaults allocate across multiple Morpho Blue markets. To understand a vault's composition and withdrawal risk, read these on-chain:

```
withdrawQueueLength() → uint256
withdrawQueue(uint256 index) → bytes32 marketId
supplyQueueLength() → uint256
supplyQueue(uint256 index) → bytes32 marketId
config(bytes32 id) → (uint184 cap, bool enabled, uint64 removableAt)
totalAssets() → uint256
fee() → uint256
curator() → address
timelock() → uint256
guardian() → address
```

For each market in the withdraw queue, read its `position()` on Morpho Core (with the vault address as user) and `market()` state to calculate:
- **Vault supply per market**: convert the vault's supply shares to assets
- **Market utilization**: `totalBorrow / totalSupply`
- **Vault withdrawable per market**: `min(vaultSupplyAssets, marketLiquidity)` where `marketLiquidity = totalSupply - totalBorrow`
- **Aggregate withdrawal liquidity**: sum of per-market withdrawable amounts vs vault TVL

#### Morpho Blue GraphQL API (alternative data source)

The Morpho Blue GraphQL API provides pre-aggregated vault data including APY, allocation breakdowns, and utilization — useful when you need rich analytics without multiple RPC calls:

```
Endpoint: https://blue-api.morpho.org/graphql
```

Example query:
```graphql
query VaultDetail($address: String!, $chainId: Int!) {
  vaultByAddress(address: $address, chainId: $chainId) {
    name, symbol
    asset { address, symbol, decimals }
    state {
      totalAssets, fee, apy, netApy, curator
      allocation {
        market {
          marketId, lltv
          loanAsset { symbol }
          collateralAsset { symbol }
          state { supplyAssets, borrowAssets, liquidityAssets, utilization }
        }
        supplyAssets, supplyCap
      }
    }
  }
}
```

Use `chainId: 747474` for Katana mainnet. Falls back gracefully — if the API is unavailable, use the on-chain reads above.

### Vault Deposits (ERC-4626)

Standard ERC-4626 interface on vault addresses:
```
deposit(uint256 assets, address receiver) → uint256 shares
redeem(uint256 shares, address receiver, address owner) → uint256 assets
convertToShares(uint256 assets) → uint256
convertToAssets(uint256 shares) → uint256
```

**Requires approval** for the underlying asset to the vault address.

### Vault Withdrawals (ERC-4626)

Two modes for exiting a vault position:

```
withdraw(uint256 assets, address receiver, address owner) → uint256 shares
```
Specify the exact asset amount to receive. The vault burns the proportional shares.

```
redeem(uint256 shares, address receiver, address owner) → uint256 assets
```
Specify shares to burn. Receive the proportional asset amount.

Use preview and max functions before building the transaction:
```
previewWithdraw(uint256 assets) → uint256 shares   // how many shares will be burned
previewRedeem(uint256 shares) → uint256 assets      // how many assets will be received
maxWithdraw(address owner) → uint256                 // max assets withdrawable by owner
maxRedeem(address owner) → uint256                   // max shares redeemable by owner
```

**Withdrawals may partially fail** if underlying markets have high utilization locking liquidity. Always check `maxWithdraw()` or `maxRedeem()` first, and inspect per-market liquidity via the vault detail reads above.

### Authorization for Bundler3

One-time authorization for leverage loops. Call on Morpho Core:
```
setAuthorization(address authorized, bool newIsAuthorized)
```

Authorize GeneralAdapter1 (`0x916Aa175C36E845db45fF6DDB886AE437d403B61`) to act on behalf of the user.

Check current status:
```
isAuthorized(address authorizer, address authorized) → bool
```

### Leverage Loops

Leverage loops use Bundler3 (`0xA8C5...48C8`) to execute an atomic multicall:

```
multicall(bytes[] memory data)
```

The multicall encodes a sequence of actions via GeneralAdapter1:
1. **Pull collateral** from user into Bundler3
2. **Flash loan** additional loan tokens from Morpho
3. **Swap** loan tokens → collateral on SushiSwap V3 (see dex skill for swap mechanics)
4. **Supply collateral** to Morpho market
5. **Borrow** loan tokens to repay the flash loan

**Two prerequisites:**
1. Morpho authorization for GeneralAdapter1 (via `setAuthorization`)
2. ERC20 approval for **Bundler3** (`0xA8C5...48C8`) to pull initial collateral — **not Morpho Core**

**Always simulate before executing.** Use the SushiSwap QuoterV2 (see dex skill) to estimate swap slippage across each loop iteration, then calculate the resulting health factor and unwind cost.

## Workflows

### Explore and Supply (3 Steps)
1. Scan `CreateMarket` events on Morpho Core — discover available markets with yields and utilization
2. Call `approve()` for the loan token → Morpho Core (`0xD50F...8aBc`)
3. Call `supply()` on Morpho Core

### Passive Vault Deposit
1. Scan factory events to find vaults — check `totalAssets()` and `name()` for best options
2. Inspect vault allocations — read `withdrawQueue` + per-market positions to understand risk exposure and withdrawal liquidity (or query the Morpho Blue GraphQL API)
3. Call `approve()` for the underlying asset → vault address
4. Call `deposit()` on the vault (returns preview of shares received)

### Vault Withdrawal
1. Check withdrawal liquidity — read per-market positions and utilization. If `maxWithdraw()` is less than desired amount, some markets have high utilization locking funds.
2. Call `withdraw(assets, receiver, owner)` to withdraw a specific asset amount, or `redeem(shares, receiver, owner)` to burn a specific share amount.

### Vault Risk Analysis
1. Read vault allocations — inspect per-market supply, caps, and utilization to understand concentration risk
2. Check DEX exit liquidity — for each collateral token in the vault's markets, check if there's a SushiSwap pool with sufficient depth (see dex skill). If a collateral token has no pool or thin liquidity, liquidations may be difficult, increasing vault risk.
3. Estimate liquidation slippage — use QuoterV2 (see dex skill) to simulate liquidation-sized trades for each collateral token. High slippage = higher risk for the vault's markets.

### Leverage Loop (5 Steps)
1. Discover markets — find a suitable market (good LLTV, sufficient liquidity)
2. **Always simulate first** — use QuoterV2 to estimate swap slippage per iteration, calculate effective leverage, health factor, and unwind cost
3. Call `setAuthorization(GeneralAdapter1, true)` on Morpho Core (one-time)
4. Call `approve()` for collateral token → **Bundler3** (`0xA8C5...48C8`)
5. Call `multicall()` on Bundler3 with the encoded loop actions

### Monitor and Manage Position
1. Call `position()` on Morpho Core — check supply, borrow, collateral, compute health factor
2. If health factor is dropping: supply more collateral or repay debt
3. Call `withdraw()` on Morpho Core when ready to exit

## Safety Notes

- **Health factor:** Always check after borrowing or looping. Keep above **1.5** for safety margin (1.0 = liquidation threshold). Enforce a 5% safety margin on max leverage: `maxSafeLeverage = 1/(1-LLTV) × 0.95`.
- **LLTV is NOT a safe borrow ratio.** Borrowing at exactly LLTV means instant liquidation risk. Stay well below.
- **Simulate before looping.** Calculate real swap slippage and unwind costs. If unwinding the loop costs extra due to slippage, warn the user.
- **Market liquidity.** Available borrow = totalSupply - totalBorrow. Warn the user if utilization is very high (>90%) — they may have trouble withdrawing later.
- **Leverage loops are complex.** Make sure the user understands: they are taking a leveraged position that amplifies both gains and losses. Liquidation risk increases with leverage.

- **Approval targets differ by operation:**
  - Supply/borrow → approve **Morpho Core** (`0xD50F...8aBc`)
  - Leverage loops → approve **Bundler3** (`0xA8C5...48C8`)
- **Authorization is separate from approval.** `setAuthorization` grants GeneralAdapter1 permission to act in Morpho on the user's behalf. `approve()` grants ERC20 token spending. Both are needed for loops.
- **First market discovery scan may be slow** — it scans events from genesis. Cache results when possible.

## Data Sources

The lending skill uses two complementary data sources:

1. **Morpho Blue GraphQL API** (`https://blue-api.morpho.org/graphql`) — Pre-aggregated vault data including APY, allocations, and utilization breakdowns. Best for vault analytics and dashboards.
2. **Katana RPC** (`https://rpc.katana.network/`) — Direct on-chain reads via `eth_call`. Authoritative for market data, positions, and transaction building. Use as fallback when the GraphQL API is unavailable.

The SushiSwap DEX contracts (see dex skill) provide additional on-chain data for swap quotes, pool discovery, and liquidity analysis — essential for assessing collateral exit liquidity and liquidation risk.

## Common Mistakes

- **Confusing market IDs with token symbols.** Market-specific functions require a `marketId` (bytes32 hex, exactly 66 characters: `0x` + 64 hex). To find the right market ID, scan `CreateMarket` events and match by loan/collateral token pair and LLTV.
- **Truncated or malformed market IDs.** Market IDs must be exactly 66 characters. A shorter string will fail with a bytes size mismatch error.
- **Wrong approval target.** Supply/withdraw/borrow → approve Morpho Core. Leverage loops → approve Bundler3. Mixing these up will revert.

## Cross-References

- **wallet-manager**: `approve()` patterns for Morpho Core or Bundler3 approvals, balance checks
- **dex**: SushiSwap V3 provides the swap leg inside leverage loops. Use QuoterV2 to preview swap rates. Use pool reads to check DEX exit liquidity for vault collateral tokens — essential for assessing liquidation risk.
- **merkl**: check reward incentives on Morpho markets/vaults before entering positions
- **analytics**: on-chain price derivation for USD position values, gas cost estimates for complex transactions
