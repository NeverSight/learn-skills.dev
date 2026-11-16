---
name: wallet-manager
description: Activate when the user asks about wallet balances, token transfers, ETH wrapping/unwrapping, or ERC20 token approvals on Katana Network.
license: MIT
metadata:
  author: katana
  version: '1.0.0'
---

# Wallet Manager — Katana Network

Core wallet operations: check balances, transfer tokens, wrap/unwrap ETH, and manage ERC20 approvals.

## Katana Basics

- Mainnet chain ID: **747474** / Testnet (Bokuto): **737373**
- Gas token: ETH
- WETH on Katana is **vbETH** (Vault Bridge ETH) — a yield-generating token that implements the WETH9 interface. Wrapping ETH earns bridge yield automatically.
- RPC: `https://rpc.katana.network/` (mainnet) / `https://rpc-bokuto.katanarpc.com` (testnet)

## Transaction Model

All write operations produce unsigned transaction payloads (`{to, data, value, chainId}`). The agent **never signs or sends** transactions — the user's wallet handles signing and submission.

## Known Tokens (Mainnet)

| Symbol | Address | Decimals | Notes |
|--------|---------|----------|-------|
| KAT | `0x7F1f4b4b29f5058fA32CC7a97141b8D7e5ABDC2d` | 18 | Katana governance token |
| WETH | `0xEE7D8BCFb72bC1880D0Cf19822eB0A2e6577aB62` | 18 | Yield-generating vbETH |
| WBTC | `0x0913DA6Da4b42f538B445599b46Bb4622342Cf52` | 8 | Wrapped Bitcoin |
| USDC | `0x203A662b0BD271A6ed5a60EdFbd04bFce608FD36` | 6 | USD stablecoin |
| USDT | `0x2DCa96907fde857dd3D816880A0df407eeB2D2F2` | 6 | USD stablecoin |
| USDS | `0x62D6A123E8D19d06d68cf0d2294F9A3A0362c6b3` | 18 | USD stablecoin |
| AUSD | `0x00000000eFE302BEAA2b3e6e1b18d08D69a9012a` | 6 | Agora USD |
| LBTC | `0xecAc9C5F704e954931349Da37F60E39f515c11c1` | 8 | Lombard BTC |
| weETH | `0x9893989433e7a383Cb313953e4c2365107dc19a7` | 18 | Wrapped eETH |
| wstETH | `0x7Fb4D0f51544F24F385a421Db6e7D4fC71Ad8e5C` | 18 | Wrapped stETH |
| MORPHO | `0x1e5eFCA3D0dB2c6d5C67a4491845c43253eB9e4e` | 18 | Morpho governance token |
| SUSHI | `0x17BFF452dae47e07CeA877Ff0E1aba17eB62b0aB` | 18 | SushiSwap token |
| vKAT | `0x106F7D67Ea25Cb9eFf5064CF604ebf6259Ff296d` | — | ERC-721 NFT (non-transferable staked KAT) |
| avKAT | `0x7231dbaCdFc968E07656D12389AB20De82FbfCeB` | 18 | ERC-4626 vault shares (liquid staked KAT) |
| jitoSOL | `0x6C16E26013f2431e8B2e1Ba7067ECCcad0Db6C52` | 18 | Jito Staked SOL |
| BTCK | `0xB0F70C0bD6FD87dbEb7C10dC692a2a6106817072` | 8 | BTC Katana |
| POL | `0xb24e3035d1FCBC0E43CF3143C3Fd92E53df2009b` | 18 | POL |
| YFI | `0x476eaCd417cD65421bD34fca054377658BB5E02b` | 18 | yearn.finance |
| uSOL | `0x9B8Df6E244526ab5F6e6400d331DB28C8fdDdb55` | 18 | Universal SOL |
| uSUI | `0xb0505e5a99abd03d94a1169e638B78EDfEd26ea4` | 18 | Universal SUI |
| uADA | `0xa3A34A0D9A08CCDDB6Ed422Ac0A28a06731335aA` | 18 | Universal ADA |
| uXRP | `0x2615a94df961278DcbC41Fb0a54fEc5f10a693aE` | 18 | Universal XRP |

## Contracts & Functions

### Checking Balances

**Native ETH balance:**
- JSON-RPC: `eth_getBalance(address, "latest")`
- Returns balance in wei (18 decimals)

**ERC-20 token balances:**
- Call `balanceOf(address)` on each token contract
- Function signature: `balanceOf(address) → uint256`
- Selector: `0x70a08231`
- Returns the raw token amount — divide by `10^decimals` for human-readable value

To check a full portfolio, call `balanceOf` on each token in the Known Tokens table. Use Multicall3 (`0xcA11bde05977b3631167028862bE2a173976CA11`) to batch all calls in a single RPC request.

### Wrapping / Unwrapping ETH

WETH contract: `0xEE7D8BCFb72bC1880D0Cf19822eB0A2e6577aB62` (implements WETH9 interface)

**Wrap ETH → WETH (vbETH):**
- Call `deposit()` with ETH as `msg.value`
- Selector: `0xd0e30db0`
- Transaction: `{to: WETH, value: amountInWei, data: "0xd0e30db0"}`

**Unwrap WETH → ETH:**
- Call `withdraw(uint256 wad)` with the amount in wei
- Selector: `0x2e1a7d4d`

Mention to users that WETH on Katana earns yield — wrapping is beneficial for DeFi participation.

### Transferring Tokens

**Native ETH transfer:**
- Transaction: `{to: recipient, value: amountInWei, data: "0x"}`

**ERC-20 transfer:**
- Call `transfer(address to, uint256 amount)` on the token contract
- Selector: `0xa9059cbb`
- The `amount` must be in the token's smallest unit (e.g., 100 USDC = `100000000` with 6 decimals)

**Always confirm the recipient address with the user before building.** Transfers are irreversible.

### Approving Spenders

Call `approve(address spender, uint256 amount)` on the token contract.
- Selector: `0x095ea7b3`
- Pass `amount` in the token's smallest unit, or `type(uint256).max` for unlimited approval

**Common spender addresses (mainnet):**

| Protocol | Contract | Address |
|----------|----------|---------|
| Sushi V3 | SwapRouter | `0x4e1d81A3E627b9294532e990109e4c21d217376C` |
| Sushi V3 | PositionManager | `0x2659C6085D26144117D904C46B48B6d180393d27` |
| Sushi V2 | Router | `0x69cC349932ae18ED406eeB917d79b9b3033fB68E` |
| Morpho | Core | `0xD50F2DffFd62f94Ee4AEd9ca05C61d0753268aBc` |
| Morpho | Bundler3 | `0xA8C5e23C9C0DF2b6fF716486c6bBEBB6661548C8` |
| KAT | VotingEscrow | `0x4d6fC15Ca6258b168225D283262743C623c13Ead` |
| KAT | avKAT Vault | `0x7231dbaCdFc968E07656D12389AB20De82FbfCeB` |

Note that unlimited approval grants unlimited spending rights. Users may prefer exact amounts instead.

## Workflows

### Check Portfolio
1. Call `eth_getBalance` for native ETH
2. Call `balanceOf` on each token contract (batch via Multicall3)
3. See **analytics** skill for converting balances to USD values using on-chain price feeds

### Send Tokens
1. Confirm recipient address and amount with the user
2. Construct the transfer transaction (native ETH or ERC-20 `transfer()`)
3. Return unsigned tx for the user to sign

### Prepare for DeFi (Approval)
1. Determine which contract needs approval (swap router, Morpho, etc.) from the spender table above
2. Construct `approve()` call with the correct spender address
3. Hand off to the relevant skill (dex, lending)

### Wrap ETH for DeFi
1. Call `deposit()` on WETH with ETH value — explain that WETH on Katana earns bridge yield
2. Proceed to swap, liquidity, or lending operations

## Safety Notes

- Token symbols are case-insensitive when resolving. Always use the canonical contract address from the Known Tokens table when constructing calls.
- Always verify the user has sufficient balance before constructing transfer/approve transactions — call `balanceOf` or `eth_getBalance` first.
- Double-check the spender address in `approve()` matches the intended protocol.

## Common Mistakes

- **Wrong spender address in approvals.** The spender depends on the operation:
  - Swaps → V3 SwapRouter or V2 Router
  - V3 LP → PositionManager
  - Morpho supply/borrow → Morpho Core (`0xD50F...8aBc`)
  - Morpho leverage loops → Bundler3 (`0xA8C5...48C8`) — **not Morpho Core**
  Passing the wrong spender means the subsequent DeFi tx will revert with an insufficient allowance error.
- **Not checking balances before constructing transactions.** Always call `balanceOf` first. Constructing a transfer or approve for more tokens than the user holds will produce a tx that reverts on submission.
- **Confusing ETH and WETH.** A transfer with native ETH sends via `msg.value`. WETH is the ERC-20 vbETH token at a specific address. Users may say "ETH" when they mean their wrapped balance — check both and confirm with the user.
- **Wrong decimal conversion.** USDC, USDT, and AUSD use 6 decimals. WBTC, LBTC, and BTCK use 8. All others use 18. Always multiply/divide by `10^decimals` when converting between human-readable and raw amounts.

## Cross-References

- **dex**: approvals required before swaps and LP adds (V3 Router, V2 Router, PositionManager)
- **lending**: approvals required before Morpho supply (Morpho Core) and leverage loops (Bundler3)
- **analytics**: on-chain price derivation to show USD values alongside balances
- **kat**: approvals required for VotingEscrow (staking) and avKAT Vault (passive staking)
