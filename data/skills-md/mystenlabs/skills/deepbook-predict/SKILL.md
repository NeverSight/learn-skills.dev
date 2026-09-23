---
name: deepbook-predict
description: >
  DeepBook Predict — expiry-based prediction market protocol on Sui. Use when
  building prediction market applications, minting binary or vertical range
  positions, understanding oracle lifecycle, working with PredictManager accounts,
  or integrating vault liquidity (PLP). Also use when the user asks about
  DeepBook binary options, range positions, DUSDC, OracleSVI, or settlement.

  Note: DeepBook Predict is currently on Testnet only. Smart contracts may change
  before Mainnet deployment.

  For spot trading, see the `deepbook-sdk` skill.
  For margin trading, see the `deepbook-margin` skill.
  For DeepBook architecture, see the `deepbook-overview` skill.
---

# DeepBook Predict

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io/onchain-finance/deepbook/deepbook-predict), the [deepbookv3 repository](https://github.com/MystenLabs/deepbookv3) (`predict-testnet-4-16` branch), and the [`@mysten/deepbook-predict` npm package](https://www.npmjs.com/package/@mysten/deepbook-predict). When extending or updating this skill, only pull from these sources. Do not use third-party blogs, tutorials, or unofficial documentation.

DeepBook Predict is an expiry-based prediction market protocol on Sui where applications establish markets and users take binary or vertical range positions priced against oracle data. The `@mysten/deepbook-predict` npm package (v0.2.1) provides a dedicated TypeScript SDK for interacting with the protocol; alternatively, developers can build transactions directly using the Sui TypeScript SDK (`@mysten/sui`). Common mistakes include treating Predict as a perpetual market (it is expiry-based), minting and depositing in the same transaction as PredictManager creation (the manager must be shared first), and using hardcoded testnet IDs as permanent addresses. Smart contracts are currently on Testnet and may change before Mainnet deployment.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/onchain-finance/deepbook/deepbook-predict
  https://docs.sui.io/onchain-finance/deepbook/deepbook-predict/design
  https://docs.sui.io/onchain-finance/deepbook/deepbook-predict/tutorial
  https://github.com/MystenLabs/deepbookv3/tree/main/packages/predict

If unsure about any API or parameter, fetch the relevant page before answering.
Do not guess or extrapolate from other prediction market protocols.

---

## Reference files

### positions-and-oracles — Position Types, Oracle Lifecycle, and Pricing
**Path:** `positions-and-oracles.md`
**Load when:** the user asks about binary positions, vertical range positions, how oracles work, oracle states, settlement mechanics, pricing, or the vault/PLP model.
**Covers:** binary position keys and payoff, vertical range position keys and payoff, oracle lifecycle (inactive → active → pending settlement → settled), settlement mechanics, vault and PLP liquidity model, pricing and exposure.

### workflow — Testnet Integration Workflow
**Path:** `workflow.md`
**Load when:** the user wants to mint positions, redeem positions, create a PredictManager, supply or withdraw PLP, or build transactions against the Predict protocol.
**Covers:** SDK setup, configuration, PredictManager creation, depositing DUSDC, minting binary positions, minting vertical range positions, redemption (live and settled), LP operations (supply and withdraw PLP), verification steps, key constraints.

### contract-info — Testnet Contract Addresses
**Path:** `contract-info.md`
**Load when:** the user needs testnet package IDs, the Predict object ID, DUSDC type address, the public server URL, or oracle event types.
**Covers:** testnet package ID, registry ID, Predict object ID, DUSDC specifications, PLP coin type, public server endpoint, oracle event types.

---

## Routing guide

| Task | Load |
|------|------|
| Understanding binary vs range positions | positions-and-oracles |
| Understanding oracle lifecycle and settlement | positions-and-oracles |
| Understanding the vault and PLP model | positions-and-oracles |
| Minting a binary position | workflow |
| Minting a vertical range position | workflow |
| Redeeming a position | workflow |
| Creating a PredictManager | workflow |
| Supplying or withdrawing PLP | workflow |
| Looking up testnet addresses | contract-info |
| Finding the public server endpoint | contract-info |
| Building a prediction market app | **all reference files** |
| Full Predict integration | **all reference files** |

---

## Skill Content

### Key concepts

- **Expiry-based protocol.** Predict is not a perpetual market. Every position has an expiry timestamp. After expiry, positions settle against the oracle's recorded price at that timestamp.

- **Binary positions.** Pay fixed notional if the settlement price is above (up) or at/below (down) the strike price. Key structure: `(oracle_id, expiry, strike, is_up)`.

- **Vertical range positions.** Pay fixed notional if the settlement price falls within a band between two strikes. Key structure: `(oracle_id, expiry, lower_strike, higher_strike)`. The lower strike must be less than the higher strike.

- **PredictManager.** A shared account wrapping a DeepBook BalanceManager. Holds DUSDC quote balances and tracks position quantities. Must be created and shared in a separate transaction before depositing or minting.

- **OracleSVI.** Market state container for a specific asset and expiry. Stores spot/forward prices, SVI parameters, activation status, and settlement data. Transitions through four states: inactive → active → pending settlement → settled.

- **Vault and PLP.** The vault takes the opposite side of every trade. Liquidity providers deposit DUSDC to receive PLP (Predict LP) tokens. The vault enforces exposure limits against total mark-to-market liability.

- **DUSDC.** The quote asset used for all Predict operations. Obtained via the testnet token request form.

- **Dedicated SDK available.** The `@mysten/deepbook-predict` npm package (v0.2.1) provides a dedicated TypeScript SDK for interacting with DeepBook Predict. Install via `npm install @mysten/deepbook-predict`. You can also build transactions directly using `@mysten/sui` if you prefer lower-level control.

### Rules

1. **Create PredictManager in a separate transaction.** Because `create_manager` shares the manager during the transaction, you deposit into it and mint from it in a later transaction, not the same one.
2. **Fetch oracle data from the public server** (`https://predict-server.testnet.mystenlabs.com`), not hardcoded values. Oracle IDs, expiries, and strikes are dynamic.
3. **All testnet IDs are provisional.** Smart contracts may change before Mainnet. Do not treat current package IDs or object layouts as permanent.
4. **Minting requires an active oracle.** The oracle must be in the "active" state. Inactive, pending settlement, and settled oracles do not accept new mints.
5. **Redemption works against both live and settled oracles.** Before settlement, payouts reflect current bid values. After settlement, binary positions yield fixed fair value; ranges pay full notional if in-band, zero otherwise.
6. **LP withdrawals are constrained.** Withdrawals require sufficient available liquidity after covering maximum payout obligations, and a rate limiter may throttle large withdrawals.

### Common mistakes

- **Minting and depositing in the same transaction as manager creation.** The PredictManager must be shared first (transaction 1), then deposits and mints happen in subsequent transactions.
- **Hardcoding testnet addresses.** These will change at Mainnet launch. Fetch configuration dynamically or maintain a config file.
- **Assuming perpetual positions.** All positions expire. After expiry, the oracle enters pending settlement and then settled state. Unresolved positions must be redeemed post-settlement.
- **Not validating oracle state before minting.** The mint succeeds only when the oracle is live, the quote asset is accepted, the market key matches the oracle, and the manager holds enough deposited DUSDC.
- **Not knowing which SDK to use.** The `@mysten/deepbook-predict` package (v0.2.1) provides high-level helpers for Predict operations. For lower-level control, build transactions directly with `@mysten/sui`. Both approaches work — choose based on how much control you need.
- **Using wrong strike ordering for ranges.** Vertical range keys require `lower_strike < higher_strike`. Reversed strikes cause the mint to fail.
