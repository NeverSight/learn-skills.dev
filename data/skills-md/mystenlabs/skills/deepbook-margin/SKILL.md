---
name: deepbook-margin
description: >
  DeepBook Margin leveraged trading on Sui. Use when building margin trading
  applications, understanding leveraged positions, risk ratios, liquidation
  mechanics, interest rate models, MarginManager lifecycle, or integrating
  margin trading into a protocol. Also use when the user asks about borrowing
  against collateral on DeepBook, margin pool parameters, or the differences
  between spot and margin trading.

  For spot trading and the DeepBook SDK, see the `deepbook-sdk` skill.
  For DeepBook architecture and contract addresses, see the `deepbook-overview` skill.
  For Move smart contract integration, see the `deepbook-move` skill.
---

# DeepBook Margin

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io/onchain-finance/deepbook/deepbook-margin) and the [deepbookv3 repository](https://github.com/MystenLabs/deepbookv3). When extending or updating this skill, only pull from these sources. Do not use third-party blogs, tutorials, or unofficial documentation.

DeepBook Margin enables leveraged trading by allowing users to post collateral, borrow from lending pools, and trade borrowed funds on spot order books. This skill covers the margin system architecture, risk model, and SDK integration. Common mistakes include ignoring continuous interest accrual on borrowed positions, not monitoring risk ratios for liquidation proximity, and creating new MarginManagers per session instead of reusing existing ones.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
  https://docs.sui.io/onchain-finance/deepbook/deepbook-margin
  https://docs.sui.io/onchain-finance/deepbook/deepbook-margin/design
  https://docs.sui.io/onchain-finance/deepbook/deepbook-margin/leveraged-workflow
  https://docs.sui.io/onchain-finance/deepbook/deepbook-margin/margin-integration
  https://docs.sui.io/onchain-finance/deepbook/deepbook-margin/margin-risks
  https://github.com/MystenLabs/deepbookv3/tree/main/packages/deepbook_margin

If unsure about any API or parameter, fetch the relevant page before answering.
Do not guess or extrapolate from other leverage protocols.

---

## Reference files

### risk-model — Risk Ratio, Interest Rates, and Liquidation
**Path:** `risk-model.md`
**Load when:** the user asks about risk ratios, leverage calculations, liquidation thresholds, interest rate formulas, the kinked utilization model, or margin risks.
**Covers:** risk ratio formula, four risk thresholds, leverage calculation table, interest rate kinked model with formulas and per-pool parameters, liquidation mechanics and rewards, oracle considerations, comprehensive risk categories.

### trading-workflow — Leveraged Position Lifecycle
**Path:** `trading-workflow.md`
**Load when:** the user wants to open, monitor, or close a leveraged position, create a MarginManager, deposit collateral, borrow funds, place margin orders, or withdraw.
**Covers:** SDK setup, MarginManager creation and reuse, reading risk parameters, checking borrow liquidity, depositing collateral, borrowing, placing margin orders, monitoring risk status, closing positions (reduce-only + repay), withdrawing collateral, troubleshooting.

### contract-info — Contract Addresses and Pool Parameters
**Path:** `contract-info.md`
**Load when:** the user needs margin package IDs, supported assets, margin pool IDs and supply caps, trading pair risk parameters, or the spot-vs-margin comparison matrix.
**Covers:** current package version, registry ID, supported tokens, margin pool configurations, trading pair risk parameters and leverage levels, spot-vs-margin structural comparison.

---

## Routing guide

| Task | Load |
|------|------|
| Understanding margin risk and liquidation | risk-model |
| Calculating leverage or risk ratio | risk-model |
| Understanding interest rates | risk-model |
| Opening a leveraged position | trading-workflow |
| Creating or reusing a MarginManager | trading-workflow |
| Depositing collateral and borrowing | trading-workflow |
| Monitoring position health | trading-workflow |
| Closing a position and withdrawing | trading-workflow |
| Looking up margin contract addresses | contract-info |
| Comparing spot vs margin integration | contract-info |
| Building a margin trading application | **all reference files** |
| Integrating margin into a protocol | **all reference files** |

---

## Skill Content

### Key concepts

- **MarginManager.** A shared object that wraps a DeepBook BalanceManager, holds collateral, and tracks borrowing. Each MarginManager is bound to exactly one DeepBook pool (isolated margin, not cross-pool).

- **Risk ratio.** The central metric: `total_assets / total_debt`. This single number controls what operations are allowed. It changes with market price movements and interest accrual.

- **Four risk thresholds.** All stored per-pool in the MarginRegistry and set by governance:
  - **Min withdraw risk ratio** — withdrawal blocked below this (typically 2.0)
  - **Min borrow risk ratio** — borrowing blocked below this; sets max leverage
  - **Target liquidation risk ratio** — liquidation restores position to this level
  - **Liquidation risk ratio** — permissionless liquidation triggered at or below this

- **Kinked interest model.** Borrow rates rise gently below optimal utilization (typically 80%), then spike sharply above it. Interest accrues at event-driven intervals (whenever pool state changes), not continuously — but the effect is that debt grows over time even when prices are stable.

- **Permissionless liquidation.** Once risk ratio reaches the liquidation threshold, anyone can liquidate the position. There is no grace period. Liquidators receive collateral rewards (typically 2%) and the pool takes additional rewards (typically 3%).

### Rules

1. **Read risk parameters on-chain.** All thresholds are governance-set and can change. Never hardcode them.
2. **Use `_v2` functions for margin orders** (`place_limit_order_v2`, `place_market_order_v2`). The unsuffixed originals are deprecated.
3. **Every margin operation requires Pyth `PriceInfoObject` arguments.** Unlike spot trading, margin has an oracle dependency for all operations (borrow, withdraw, risk reads, trading).
4. **Reuse MarginManagers.** Creating a new one per session fragments collateral across orphaned shared objects. Discover existing managers via the registry.
5. **Size borrows from risk parameters, not trial and error.** The min borrow risk ratio defines your maximum leverage per unit of collateral.
6. **`clientOrderId` must be a numeric string** (encoded as u64), same as spot.

### Common mistakes

- **Ignoring interest accrual.** Debt grows at event-driven intervals (whenever pool state changes — borrows, repays, liquidations). A position can drift toward liquidation purely from accumulated interest, even with stable prices.
- **Not monitoring risk ratio.** There is no grace period before liquidation. Integrators must surface the risk ratio and its distance to the liquidation threshold to users.
- **Creating new MarginManagers per run.** This fragments collateral. Use `findMarginManagerId` to discover existing managers before creating new ones.
- **Borrowing and trading in the same pool without oracle freshness checks.** If the Pyth price exceeds the pool's maximum age, the operation reverts.
- **Confusing margin order entry with spot.** Margin orders route through a pool proxy with risk checks, not the direct spot order entry.
