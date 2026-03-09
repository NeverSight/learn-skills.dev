---
name: goldrush-foundational-api
description: "GoldRush Foundational API — REST API for historical and near-real-time blockchain data across 100+ chains. Use this skill whenever the user needs wallet token balances, transaction history, NFT holdings, token prices, token approvals, cross-chain activity, block data, portfolio value tracking, or any on-chain data query via REST. This is the default skill for blockchain data lookups, portfolio dashboards, tax tools, compliance checks, block explorers, and any application that fetches historical or current chain data. If the user needs real-time streaming or WebSocket push data, use goldrush-streaming-api instead. If the user needs pay-per-request access without an API key, use goldrush-x402 instead."
---

# GoldRush Foundational API

REST API providing historical and near-real-time blockchain data across 100+ chains. Endpoints cover token balances, transactions, NFTs, security approvals, cross-chain activity, pricing, and block data.

## Quick Start

**IMPORTANT:**  Always prioritize using the official available GoldRush Client SDK best suited for your development ecosystem:
- [TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk)

```typescript
import { GoldRushClient } from "@covalenthq/client-sdk";

const client = new GoldRushClient("YOUR_API_KEY");

const resp = await client.BalanceService.getTokenBalancesForWalletAddress(
  "eth-mainnet",
  "demo.eth"
);

if (!resp.error) {
  console.log(resp.data.items);
} else {
  console.error(resp.error_message);
}
```

**Install:** `npm install @covalenthq/client-sdk`

**Raw HTTP:**
```bash
curl "https://api.covalenthq.com/v1/eth-mainnet/address/demo.eth/balances_v2/" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Endpoint Categories

Endpoints are organized into categories. Each links to its reference file with full parameters, response schemas, and use cases.

- **Balances** — token balances, native balances, historical balances, portfolio value, ERC20 transfers, token holders, Bitcoin (HD and non-HD). See [endpoints-balances.md](references/endpoints-balances.md).
- **Transactions** — recent transactions, paginated history, single transaction lookup, summaries, block-level transactions, Bitcoin transactions. See [endpoints-transactions.md](references/endpoints-transactions.md).
- **NFT, Security & Cross-Chain** — NFT holdings, ownership verification, token/NFT approvals, address activity, multi-chain balances and transactions. See [endpoints-nft-security-crosschain.md](references/endpoints-nft-security-crosschain.md).
- **Utility** — token prices, blocks, block heights, event logs, gas prices, chain metadata, pool spot prices, address resolution. See [endpoints-utility.md](references/endpoints-utility.md).

## Common Tasks → Endpoint

| Task | Endpoint |
|------|----------|
| Check wallet balance | `getTokenBalancesForWalletAddress` |
| Get native token only (lightweight) | `getNativeTokenBalance` |
| Get recent transactions | `getRecentTransactionsForAddress` |
| Get full transaction history | `getTransactionsForAddressV3` (paginated) |
| Look up a single transaction | `getTransaction` |
| Get ERC20 transfer history | `getErc20TransfersForWalletAddress` |
| Get transaction summary/count | `getTransactionSummary` |
| Check token approvals (security) | `getApprovals` |
| Get NFT holdings | `getNftsForAddress` |
| Verify NFT ownership | `checkOwnershipInNft` |
| Get portfolio value over time | `getHistoricalPortfolioForWalletAddress` |
| Get balance at a specific block | `getHistoricalTokenBalancesForWalletAddress` |
| Get token price history | `getTokenPrices` |
| Find which chains a wallet is active on | `getAddressActivity` |
| Get balances across all chains | `getMultiChainBalances` |
| Get token holders | `getTokenHoldersV2ForTokenAddress` |
| Get Bitcoin balance (HD wallet) | `getBitcoinBalancesForHdAddress` |
| Get contract event logs | `getLogEventsByAddress` |
| Get block details | `getBlock` |

## Critical Rules

1. **Chain names are case-sensitive** — use `eth-mainnet`, not `ethereum` or `Eth-Mainnet`
2. **Authentication** — `Authorization: Bearer YOUR_API_KEY` (HTTPS only)
3. **Pagination is 0-indexed** — first page is `0`, 100 items per page
4. **Always check `resp.error`** before accessing `resp.data`
5. **Token balances are strings** — divide by `10^contract_decimals` for human-readable values
6. **ENS/domain resolution** — pass `vitalik.eth` directly as the wallet address
7. **Foundational-only features** — historical balances, token holders at any block, pool spot prices, tracing flags
8. **Quote currency** — defaults to USD; supported: USD, CAD, EUR, SGD, INR, JPY, and more
9. **Spam filtering** — use `no-spam=true` query parameter to filter spam tokens
10. **SDK handles retries** — the TypeScript SDK has built-in retry logic and rate limit handling

## Reference Files

Read the relevant reference file when you need details beyond what this index provides.

| File | When to read |
|------|-------------|
| [overview.md](references/overview.md) | Need API setup details, authentication methods, or SDK quickstart code |
| [endpoints-balances.md](references/endpoints-balances.md) | Building a balance query — parameters, response schema, Bitcoin-specific endpoints |
| [endpoints-transactions.md](references/endpoints-transactions.md) | Building a transaction query — pagination, decoded logs, block-level queries |
| [endpoints-nft-security-crosschain.md](references/endpoints-nft-security-crosschain.md) | Need NFT metadata, token approvals, or cross-chain activity lookups |
| [endpoints-utility.md](references/endpoints-utility.md) | Need block data, event logs, gas prices, token prices, or chain metadata |
| [integration-guide.md](references/integration-guide.md) | Need full chain names table, validation rules, error codes, or FAQ answers |
| [workflows.md](references/workflows.md) | Planning a multi-step workflow or debugging a common error |
