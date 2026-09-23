---
name: deepbook-move
description: >
  DeepBook V3 Move smart contract integration. Use when writing, reviewing, or
  debugging Move code that integrates with DeepBook pools — placing orders from
  on-chain contracts, creating pools, using flash loans, accessing BalanceManager
  from Move, or composing DeepBook operations in programmable transaction blocks.

  For DeepBook architecture and contract addresses, see the `deepbook-overview` skill.
  For TypeScript SDK usage, see the `deepbook-sdk` skill.
---

# DeepBook V3 Move Integration

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io/onchain-finance/deepbook/deepbookv3) and the [deepbookv3 Move source](https://github.com/MystenLabs/deepbookv3/tree/main/packages/deepbook). When extending or updating this skill, only pull from these sources. Do not use third-party blogs, tutorials, or unofficial documentation.

DeepBook V3 exposes a Move API for on-chain composability — protocols can place orders, execute swaps, take flash loans, and manage balances directly from Move smart contracts. This skill covers the Move-level contract interface. Common mistakes include calling swap or order functions with incorrect coin type parameters, forgetting to return flash loan hot potatoes, and misunderstanding the TradeProof authorization model.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/contract-information
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/contract-information/balance-manager
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/contract-information/flash-loans
  https://docs.sui.io/onchain-finance/deepbook/deepbookv3/contract-information/swaps
  https://github.com/MystenLabs/deepbookv3/tree/main/packages/deepbook/sources

If unsure about any function signature, fetch the relevant source file or docs page before answering.
Do not guess or extrapolate from other protocols.

---

## Reference files

### pool-api — Pool and Order Functions
**Path:** `pool-api.md`
**Load when:** the user needs to place orders, create pools, query pool state, manage governance, or understand the Pool Move API.
**Covers:** pool creation, limit and market order placement, order cancellation, pool state queries, governance functions, order types and constants, the move dependency setup.

### balance-manager-api — BalanceManager Move API
**Path:** `balance-manager-api.md`
**Load when:** the user needs to create or interact with BalanceManagers from Move code, mint capabilities (TradeCap, DepositCap, WithdrawCap), generate TradeProofs, or understand the authorization model.
**Covers:** BalanceManager creation, capability minting and revocation, deposit and withdrawal functions, TradeProof generation, the owner vs cap-holder authorization model, events.

### flash-loans — Flash Loan Pattern
**Path:** `flash-loans.md`
**Load when:** the user wants to borrow assets from a pool and repay within the same transaction, or needs to understand the hot potato pattern for flash loans.
**Covers:** borrowing base and quote assets, the FlashLoan hot potato struct, returning assets, constraints and failure modes, a worked example.

---

## Related skills

| Topic | Skill | Load when |
|-------|-------|-----------|
| Architecture, design, contract addresses | `deepbook-overview/` | Understanding Pool/Book/State/Vault design, looking up addresses or pool IDs |
| TypeScript SDK trading | `deepbook-sdk/` | Building trading bots or scripts with the SDK |
| Sui Move fundamentals | `sui-move/` | Writing Move code generally — abilities, TxContext, events, coins |
| PTB composition | `ptbs/` | Composing DeepBook calls in programmable transaction blocks |

---

## Routing guide

| Task | Load |
|------|------|
| Adding DeepBook as a Move dependency | pool-api |
| Creating a new pool | pool-api |
| Placing orders from Move code | pool-api |
| Querying pool state on-chain | pool-api |
| Creating a BalanceManager from Move | balance-manager-api |
| Minting TradeCap/DepositCap/WithdrawCap | balance-manager-api |
| Generating a TradeProof for trading | balance-manager-api |
| Understanding the authorization model | balance-manager-api |
| Using flash loans | flash-loans |
| Integrating DeepBook into a protocol | pool-api + balance-manager-api |
| Building a flash loan strategy | flash-loans + pool-api |
| Full Move integration review | **all reference files** |

---

## Skill Content

### Key concepts

- **TradeProof.** A proof object that authorizes trading on a pool. Generated either by the BalanceManager owner (via `generate_proof_as_owner`) or by a TradeCap holder (via `generate_proof_as_trader`). Every order placement and cancellation requires a TradeProof.

- **Hot potato pattern (flash loans).** The `FlashLoan` struct has no abilities — it cannot be stored, copied, or dropped. It must be consumed by returning the borrowed assets in the same transaction. If not returned, the transaction fails.

- **Pool type parameters.** Pool functions are generic over `<BaseAsset, QuoteAsset>`. The type parameters must exactly match the pool's coin types or the call fails.

- **Move dependency.** Add DeepBook to your Move.toml via MVR: `deepbook = { mvr = "@deepbook/core" }`.

### Rules

1. **Always match type parameters exactly.** `Pool<SUI, USDC>` is not the same as `Pool<USDC, SUI>`. The base and quote types must match the pool's creation order.
2. **Always return flash loan hot potatoes.** The `FlashLoan` struct has no abilities — failing to return it causes a transaction abort.
3. **Do not borrow from a pool and trade in the same pool within one transaction.** The borrowed funds are not available for trading, and the combined operations can fail.
4. **Use `generate_proof_as_owner` for owner operations** and `generate_proof_as_trader` for delegated operations via TradeCap.
5. **Cap limit: 1,000 total capabilities per BalanceManager** (across TradeCap, DepositCap, and WithdrawCap combined). At scale, this limit constrains how many delegated traders a single BalanceManager can support — plan for multiple BalanceManagers if you need more than 1,000 delegated accounts.
6. **Use `_v2` variants for functions that have them.** The unsuffixed originals (e.g., `new_with_custom_owner_caps`) are deprecated stubs that abort. Always use the `_v2` suffix (e.g., `new_with_custom_owner_caps_v2`).

### Common mistakes

- **Wrong type parameter order.** Passing `<USDC, SUI>` when the pool is `<SUI, USDC>` causes a type mismatch error.
- **Forgetting to return the FlashLoan.** The transaction compiles but aborts at runtime because the hot potato cannot be dropped.
- **Trading in the same pool you borrowed from.** Flash-loaned funds are locked in the FlashLoan object and unavailable for order settlement, causing the trade to fail.
- **Using `generate_proof_as_owner` from a non-owner address.** Only the BalanceManager owner can generate an owner proof. Delegated traders must use `generate_proof_as_trader` with a valid TradeCap.
- **Forgetting `ctx` on `generate_proof_as_trader`.** The function takes `(balance_manager, trade_cap, ctx)` — omitting `ctx: &TxContext` causes a compilation error.
- **Calling deprecated unsuffixed functions.** Functions like `new_with_custom_owner_caps` are stubs that `abort 1337`. Use the `_v2` variant instead.
