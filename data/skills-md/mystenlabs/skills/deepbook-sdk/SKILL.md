---
name: deepbook-sdk
description: >
  DeepBook V3 TypeScript SDK integration. Use when building trading applications,
  bots, or scripts that interact with DeepBook pools using the @mysten/deepbook-v3
  SDK. Covers client setup, BalanceManager lifecycle, placing limit and market
  orders, swaps, querying order books, order management, and fee handling.

  For DeepBook architecture and contract addresses, see the `deepbook-overview` skill.
  For Move smart contract integration, see the `deepbook-move` skill.
---

# DeepBook V3 SDK

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io/onchain-finance/deepbook/deepbookv3), the [deepbook-sandbox examples](https://github.com/MystenLabs/deepbook-sandbox/tree/main/examples/sandbox), and the [deepbookv3 repository](https://github.com/MystenLabs/deepbookv3). When extending or updating this skill, only pull from these sources. Do not use third-party blogs, tutorials, or unofficial documentation.

The `@mysten/deepbook-v3` SDK provides a TypeScript client for interacting with DeepBook V3 pools on Sui. This skill covers how to set up the client, manage balances, place orders, execute swaps, and handle fees. Common AI-coding mistakes include hardcoding on-chain IDs instead of using SDK pool/coin keys, creating a new BalanceManager per transaction instead of reusing one, and using non-numeric `clientOrderId` values.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/spot-workflow
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3-sdk
  https://github.com/MystenLabs/deepbook-sandbox/tree/main/examples/sandbox

If unsure about any API, fetch the relevant page before answering.
Do not guess or extrapolate from other SDKs or libraries.

---

## Reference files

### client-setup — Client Initialization and BalanceManager Lifecycle
**Path:** `client-setup.md`
**Load when:** setting up a DeepBook client, creating or reusing a BalanceManager, configuring the SDK for testnet or mainnet, or understanding the three-tier setup pattern (read-only, basic, advanced).
**Covers:** SDK installation, `SuiGrpcClient` construction with `$extend(deepbook({...}))`, keypair setup, BalanceManager creation and reuse, deposits and withdrawals, the sandbox setup patterns.

### trading — Orders, Swaps, and Order Lifecycle
**Path:** `trading.md`
**Load when:** placing limit or market orders, executing swaps, querying order books, checking order status, canceling orders, or understanding the order lifecycle.
**Covers:** limit order placement (`POST_ONLY`, `NO_RESTRICTION`), market order placement with retry patterns, swap functions (with and without BalanceManager), order book queries, open order queries, order cancellation, self-matching behavior, the complete order lifecycle from placement to withdrawal.

### fees — Fee Structure and DEEP Staking
**Path:** `fees.md`
**Load when:** the user asks about trading fees, DEEP token staking, fee discounts, how to fund a BalanceManager with DEEP, or how fees are calculated.
**Covers:** DEEP vs input-token fee payment, fee calculation via `DeepPrice`, governance fee parameters, staking for fee discounts, acquiring testnet DEEP, referral system.

---

## Routing guide

| Task | Load |
|------|------|
| Setting up a DeepBook client | client-setup |
| Creating or reusing a BalanceManager | client-setup |
| Depositing or withdrawing funds | client-setup |
| Placing a limit order | trading |
| Placing a market order | trading |
| Executing a swap | trading |
| Querying the order book | trading |
| Checking or canceling orders | trading |
| Understanding fees or staking | fees |
| Funding a BalanceManager with DEEP | fees |
| Building a complete trading bot | **all reference files** |
| Full spot trading workflow | **all reference files** |

---

## Skill Content

### Key concepts

- **DeepBook client via `$extend`.** The SDK uses the `deepbook` function (imported from `@mysten/deepbook-v3`) with `SuiGrpcClient.$extend(deepbook({...}))` to add DeepBook-specific transaction builders. Methods follow a curried pattern under two namespaces: `client.deepbook.deepBook.method({ params })(tx)` for trading operations and `client.deepbook.balanceManager.method({ params })(tx)` for balance management, where `tx` is a `Transaction` object.

- **Pool and coin keys.** The SDK references pools and coins by string keys (e.g., `"DEEP_SUI"`, `"SUI"`) rather than raw on-chain addresses. The SDK maps these to the correct addresses per network.

- **BalanceManager lifecycle.** A BalanceManager is a shared on-chain object. Create it once, persist its ID, and reuse it across transactions. Creating a new one per transaction wastes gas and creates orphaned objects.

- **Swaps vs orders.** Swaps operate directly on wallet `Coin` objects without a BalanceManager. Orders require a BalanceManager with deposited funds.

### Rules

1. **Always use SDK keys for pools and coins.** Never hardcode on-chain IDs — the SDK handles address resolution per network.
2. **`clientOrderId` must be a numeric string** (encoded as `u64`). Labels like `"order-1"` will fail.
3. **Reuse BalanceManagers.** Persist the ID from creation and pass it when constructing the client.
4. **Size deposits to wallet balance.** The SDK validates at build time — depositing more than the wallet holds causes an `Insufficient balance` error before the transaction is even submitted.
5. **Handle the market maker rebalance window** on localnet/sandbox. The sandbox market maker has a ~15-second rebalance cycle where liquidity temporarily disappears. Use retry helpers.

### Common mistakes

- **Creating a new BalanceManager every run.** This creates orphaned shared objects. Check for existing managers via the indexer or persist the ID.
- **Using `POST_ONLY` for taker orders.** `POST_ONLY` guarantees the order rests on the book. If it would cross and fill, it is silently rejected — no order is returned and no error is thrown.
- **Forgetting to deposit before trading.** Orders draw from BalanceManager balances, not wallet balances. Funds must be deposited first.
- **Not depositing DEEP for fees.** On non-whitelisted pools, DEEP must be in the BalanceManager to pay fees. Without it, trades fail.
- **Ignoring self-matching.** When `selfMatchingOption` is not specified, the SDK defaults to `SelfMatchingOptions.SELF_MATCHING_ALLOWED`, which means your taker order can fill against your own resting maker orders. This is often unintentional. Explicitly set `SelfMatchingOptions.CANCEL_TAKER` or `SelfMatchingOptions.CANCEL_MAKER` to prevent self-fills.
