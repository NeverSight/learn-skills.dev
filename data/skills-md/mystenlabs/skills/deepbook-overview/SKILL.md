---
name: deepbook-overview
description: >
  High-level overview of DeepBook V3 on Sui — architecture, key concepts,
  integration models, contract addresses, supported coins, and pool information.
  Use when explaining DeepBook to someone new, comparing integration approaches
  (Move vs SDK vs read-only), looking up mainnet/testnet contract addresses,
  or understanding the Pool/Book/State/Vault design.

  For TypeScript SDK usage and trading, see the `deepbook-sdk` skill.
  For Move smart contract integration, see the `deepbook-move` skill.
---

# DeepBook V3 Overview

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io/onchain-finance/deepbook/deepbookv3/deepbook) and the [deepbookv3 GitHub repository](https://github.com/MystenLabs/deepbookv3). When extending or updating this skill, only pull from these sources. Do not use third-party blogs, tutorials, or unofficial documentation.

DeepBook V3 is a next-generation decentralized central limit order book (CLOB) built on Sui, providing a highly performant, low-latency exchange on-chain. This skill covers the high-level architecture and key concepts. Common mistakes include confusing DeepBook with an AMM (it is an order book), misunderstanding the role of the DEEP token in fee payments, and not knowing which integration model to use.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/deepbook
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/deepbook/design
  https://github.com/MystenLabs/deepbookv3

If unsure about any detail, fetch the relevant page before answering. Do not guess or extrapolate.

---

## Reference files

### design — Architecture and Design
**Path:** `design.md`
**Load when:** the user asks how DeepBook works internally, about Pool/Book/State/Vault architecture, the order placement flow, BigVector, governance mechanics, or how fees are calculated.
**Covers:** the three-part Pool structure (Book, State, Vault), order matching and injection, governance and voting, History and epoch tracking, BigVector implementation, the full order placement workflow.

### contract-info — Contract Addresses, Coins, and Pools
**Path:** `contract-info.md`
**Load when:** the user needs mainnet package IDs, pool object IDs, supported coin types and decimals, pool fee configurations, or registry addresses.
**Covers:** current and historical package versions, all supported tokens with type addresses and decimals, all 23 mainnet trading pools with IDs and fee tiers.

---

## Routing guide

| Task | Load |
|------|------|
| Explaining what DeepBook is | skill content only |
| Choosing an integration model (Move vs SDK vs read-only) | skill content only |
| Understanding Pool/Book/State/Vault architecture | design |
| Understanding the order placement flow | design |
| Understanding governance and fee voting | design |
| Looking up a contract address or pool ID | contract-info |
| Finding a supported coin's type address or decimals | contract-info |
| Full deep dive on DeepBook | **all reference files** |

---

## Skill Content

### Key concepts

- **Central limit order book (CLOB).** DeepBook is not an AMM. It maintains a full order book with bids and asks, matching orders by price-time priority. This enables limit orders, market orders, and precise price discovery.

- **Pool.** A single market (e.g., DEEP/SUI) represented as a shared object. Each Pool contains three components: Book (order storage and matching), State (accounts, governance, history), and Vault (asset settlement).

- **BalanceManager.** A shared object that holds a user's balances across all pools. Required for all trading operations (except direct swaps). Supports delegated access via TradeCap, DepositCap, and WithdrawCap.

- **DEEP token.** The protocol's governance and fee token. Users stake DEEP for reduced taker fees (staking can halve taker fees when stake and volume thresholds are met) and can propose/vote on pool parameters (taker/maker fees, stake requirements). Fees can be paid in DEEP (default) or in the input token (at a 25% premium).

- **Whitelisted pools.** DEEP/SUI and DEEP/USDC pools have 0% taker and maker fees, serving as gateway liquidity for the DEEP token.

- **Flash loans.** Pools support uncollateralized flash loans via a hot potato pattern — borrow and repay within the same PTB.

- **DeepBook does not include an end-user interface.** It is infrastructure that trading applications, bots, and protocols build on top of.

### Integration models

| Model | Use case | Dependency |
|-------|----------|------------|
| Move package | Protocols requiring on-chain logic guarantees and composability | `deepbook = { mvr = "@deepbook/core" }` |
| SDK & PTBs | Apps, bots, and wallets submitting trades via TypeScript | `npm install @mysten/deepbook-v3` |
| Read-only data | Price/order book queries via indexer or RPC | No dependency — query endpoints directly |

### Rules

1. **Always use SDK pool/coin keys, not hardcoded on-chain IDs** when building with the TypeScript SDK. The SDK maps keys to the correct addresses per network.
2. **Read fee parameters on-chain** rather than hardcoding. Governance can change taker/maker fees and stake requirements at any time.
3. **Reuse BalanceManagers.** Creating a new one per transaction wastes gas and creates orphaned shared objects.

### Common mistakes

- **Treating DeepBook like an AMM.** DeepBook uses a central limit order book with discrete price levels (tick size) and quantity increments (lot size). Orders must respect these parameters or they are rejected.
- **Forgetting DEEP for fees.** Most pools require DEEP tokens to pay trading fees. Without DEEP in the BalanceManager, trades fail. Whitelisted pools (DEEP/SUI, DEEP/USDC) are the exception.
- **Ignoring tick and lot sizes.** Each pool has specific tick sizes (minimum price increment) and lot sizes (minimum quantity increment). Orders that don't align are rejected.
