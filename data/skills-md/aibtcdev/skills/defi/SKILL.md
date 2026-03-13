---
name: defi
description: DeFi operations on Stacks — ALEX DEX token swaps and liquidity pool queries, plus Zest Protocol lending (supply, withdraw, borrow, repay, claim rewards). All operations are mainnet-only. Write operations require an unlocked wallet.
author: whoabuddy
author_agent: Trustless Indra
user-invocable: false
arguments: alex-get-swap-quote | alex-swap | alex-get-pool-info | alex-list-pools | zest-list-assets | zest-get-position | zest-supply | zest-withdraw | zest-borrow | zest-repay | zest-claim-rewards
entry: defi/defi.ts
requires: [wallet]
tags: [l2, defi, write, mainnet-only, requires-funds]
---

# DeFi Skill

Provides DeFi operations across two protocols:

- **ALEX DEX** — Automated Market Maker (AMM) on Stacks for token swaps. Uses the alex-sdk for routing and price discovery. Mainnet-only.
- **Zest Protocol** — Lending and borrowing protocol on Stacks. Supply assets to earn interest, borrow against collateral. Mainnet-only.

Write operations (swap, supply, withdraw, borrow, repay, claim-rewards) require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first). Read operations (get-swap-quote, get-pool-info, list-pools, list-assets, get-position) also require an unlocked wallet for routing context.

## Usage

```
bun run defi/defi.ts <subcommand> [options]
```

## Subcommands

### alex-get-swap-quote

Get a swap quote from ALEX DEX. Returns the expected output amount for swapping tokenX to tokenY.

```
bun run defi/defi.ts alex-get-swap-quote --token-x <contractId> --token-y <contractId> --amount-in <units>
```

Options:
- `--token-x` (required) — Input token: contract ID (e.g., `SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.token-wstx-v2`) or symbol (`STX`, `ALEX`)
- `--token-y` (required) — Output token: contract ID or symbol
- `--amount-in` (required) — Amount of tokenX to swap (in smallest units)

Output:
```json
{
  "network": "mainnet",
  "quote": {
    "tokenIn": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.token-wstx-v2",
    "tokenOut": "SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.token-alex",
    "amountIn": "1000000",
    "expectedAmountOut": "52341",
    "route": ["STX", "ALEX"]
  }
}
```

### alex-swap

Execute a token swap on ALEX DEX. Requires an unlocked wallet.

```
bun run defi/defi.ts alex-swap --token-x <contractId> --token-y <contractId> --amount-in <units> [--min-amount-out <units>]
```

Options:
- `--token-x` (required) — Input token: contract ID or symbol
- `--token-y` (required) — Output token: contract ID or symbol
- `--amount-in` (required) — Amount of tokenX to swap (in smallest units)
- `--min-amount-out` (optional) — Minimum acceptable output amount for slippage protection (default: 0)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "swap": {
    "tokenIn": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.token-wstx-v2",
    "tokenOut": "SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.token-alex",
    "amountIn": "1000000",
    "minAmountOut": "0"
  },
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### alex-get-pool-info

Get liquidity pool information from ALEX DEX. Returns reserve balances and pool details for a token pair.

```
bun run defi/defi.ts alex-get-pool-info --token-x <contractId> --token-y <contractId>
```

Options:
- `--token-x` (required) — First token contract ID or symbol
- `--token-y` (required) — Second token contract ID or symbol

Output:
```json
{
  "network": "mainnet",
  "pool": {
    "poolId": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.token-wstx-v2-SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.token-alex",
    "tokenX": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.token-wstx-v2",
    "tokenY": "SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.token-alex",
    "reserveX": "5000000000",
    "reserveY": "12000000000",
    "totalShares": "8000000000"
  }
}
```

### alex-list-pools

List all available trading pools on ALEX DEX.

```
bun run defi/defi.ts alex-list-pools [--limit <n>]
```

Options:
- `--limit` (optional) — Maximum number of pools to return (default: 50)

Output:
```json
{
  "network": "mainnet",
  "poolCount": 3,
  "pools": [
    {
      "id": 1,
      "pair": "wstx-v2/alex",
      "tokenX": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.token-wstx-v2",
      "tokenY": "SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.token-alex",
      "factor": "100000000"
    }
  ],
  "usage": "Use the tokenX and tokenY contract IDs with alex-get-swap-quote or alex-swap"
}
```

### zest-list-assets

List all supported assets on Zest Protocol.

```
bun run defi/defi.ts zest-list-assets
```

Output:
```json
{
  "network": "mainnet",
  "assetCount": 3,
  "assets": [
    {
      "symbol": "sBTC",
      "name": "Stacked Bitcoin",
      "contractId": "SM3VDXK3WZZSA84XXFKAFAF15NNZX32CTSG82JFQ4.sbtc-token"
    },
    {
      "symbol": "stSTX",
      "name": "Stacked STX",
      "contractId": "SP4SZE494VC2YC5JYG7AYFQ44F5Q4PYV7DVMDPBG.ststx-token"
    }
  ],
  "usage": "Use the symbol (e.g., 'stSTX') or full contract ID in other zest-* commands"
}
```

### zest-get-position

Get a user's lending position on Zest Protocol.

```
bun run defi/defi.ts zest-get-position --asset <symbolOrContractId> [--address <addr>]
```

Options:
- `--asset` (required) — Asset symbol (e.g., `stSTX`, `aeUSDC`) or full contract ID
- `--address` (optional) — User address (uses active wallet if omitted)

Output:
```json
{
  "network": "mainnet",
  "address": "SP2...",
  "position": {
    "asset": "SP4SZE494VC2YC5JYG7AYFQ44F5Q4PYV7DVMDPBG.ststx-token",
    "supplied": "5000000",
    "borrowed": "0"
  }
}
```

### zest-supply

Supply assets to the Zest Protocol lending pool to earn interest. Requires an unlocked wallet.

```
bun run defi/defi.ts zest-supply --asset <symbolOrContractId> --amount <units> [--on-behalf-of <addr>]
```

Options:
- `--asset` (required) — Asset symbol or full contract ID
- `--amount` (required) — Amount to supply (in smallest units)
- `--on-behalf-of` (optional) — Supply on behalf of another address

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "action": "supply",
  "asset": "SP4SZE494VC2YC5JYG7AYFQ44F5Q4PYV7DVMDPBG.ststx-token",
  "amount": "5000000",
  "onBehalfOf": "SP2...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### zest-withdraw

Withdraw assets from the Zest Protocol lending pool. Requires an unlocked wallet.

```
bun run defi/defi.ts zest-withdraw --asset <symbolOrContractId> --amount <units>
```

Options:
- `--asset` (required) — Asset symbol or full contract ID
- `--amount` (required) — Amount to withdraw (in smallest units)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "action": "withdraw",
  "asset": "SP4SZE494VC2YC5JYG7AYFQ44F5Q4PYV7DVMDPBG.ststx-token",
  "amount": "5000000",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### zest-borrow

Borrow assets from Zest Protocol against supplied collateral. Requires an unlocked wallet.

```
bun run defi/defi.ts zest-borrow --asset <symbolOrContractId> --amount <units>
```

Options:
- `--asset` (required) — Asset symbol or full contract ID
- `--amount` (required) — Amount to borrow (in smallest units)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "action": "borrow",
  "asset": "SM3VDXK3WZZSA84XXFKAFAF15NNZX32CTSG82JFQ4.sbtc-token",
  "amount": "100000",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### zest-repay

Repay borrowed assets to Zest Protocol. Requires an unlocked wallet.

```
bun run defi/defi.ts zest-repay --asset <symbolOrContractId> --amount <units> [--on-behalf-of <addr>]
```

Options:
- `--asset` (required) — Asset symbol or full contract ID
- `--amount` (required) — Amount to repay (in smallest units)
- `--on-behalf-of` (optional) — Repay on behalf of another address

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "action": "repay",
  "asset": "SM3VDXK3WZZSA84XXFKAFAF15NNZX32CTSG82JFQ4.sbtc-token",
  "amount": "100000",
  "onBehalfOf": "SP2...",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet"
}
```

### zest-claim-rewards

Claim accumulated rewards from the Zest Protocol incentives program. sBTC suppliers earn wSTX rewards. Requires an unlocked wallet.

```
bun run defi/defi.ts zest-claim-rewards [--asset <symbolOrContractId>]
```

Options:
- `--asset` (optional) — Asset you supplied to earn rewards (default: `sBTC`)

Output:
```json
{
  "success": true,
  "txid": "abc123...",
  "action": "claim_rewards",
  "asset": "SM3VDXK3WZZSA84XXFKAFAF15NNZX32CTSG82JFQ4.sbtc-token",
  "rewardAsset": "wSTX",
  "network": "mainnet",
  "explorerUrl": "https://explorer.hiro.so/txid/abc123...?chain=mainnet",
  "note": "Rewards will be sent to your wallet once the transaction confirms."
}
```

## Notes

- ALEX DEX and Zest Protocol are **mainnet-only**. Calls on testnet will return an error.
- For ALEX swap quotes, you can use token symbols (`STX`, `ALEX`) or full contract IDs. Use `alex-list-pools` to discover available pairs.
- For Zest operations, you can use asset symbols (`stSTX`, `aeUSDC`, `sBTC`) or full contract IDs. Use `zest-list-assets` to discover supported assets.
- Wallet operations require an unlocked wallet (use `bun run wallet/wallet.ts unlock` first).
- Borrow operations require sufficient collateral in the protocol. Ensure you have supplied assets before borrowing.
