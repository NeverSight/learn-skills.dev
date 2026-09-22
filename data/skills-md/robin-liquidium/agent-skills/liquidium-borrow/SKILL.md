---
name: liquidium-borrow
description: Liquidium @liquidium/client borrow/supply/repay/portfolio; default accountless instant loans.
allowed-tools: Bash(./scripts/liquidium-borrow:*)
license: MIT
metadata:
  title: Liquidium Borrow
  category: DeFi SDK
---

# Liquidium Borrow

Liquidium is a decentralized, non-custodial cross-chain lending protocol. The default agent flow is an accountless instant loan: the user provides collateral and destination addresses, Liquidium returns deposit and repayment targets, and the agent stores the loan reference for later status, repayment, or collateral top-up.

Liquidium docs: `https://liquidium.fi/docs` and SDK docs: `https://liquidium.fi/docs/sdk`.

## Load The Right Reference

- Instant loans, manual wallet users, wallet-access agents, saved loan records, repayment, add-collateral, and status tracking: read `references/instant-loans.md`.
- Connected-wallet profile flows for supply, borrow, repay, withdraw, and portfolio dashboards: read `references/profile-flows.md`.
- LTV, APY, health factor, liquidation thresholds, high-LTV warnings, and risk copy: read `references/risk-and-liquidation.md`.
- SDK method shapes, CLI details, TypeScript examples, and troubleshooting: read `references/sdk-methods.md`.

## Quick Start CLI

Run the wrapper from this skill directory:

```bash
<skill-path>/scripts/liquidium-borrow pools
```

The CLI bootstraps a pinned `@liquidium/client` package into `~/.cache/liquidium-borrow/node` on first real CLI use. This requires npm/network access, installs with lifecycle scripts disabled, and is excluded from the packaged skill. Set `LIQUIDIUM_CLI_CACHE_DIR` to use a different cache location.

Created instant loans are saved by default under `~/.local/share/liquidium-borrow/loans/<ref>.json`; local loan records live outside the repo. Set `LIQUIDIUM_CLI_DATA_DIR` to store records elsewhere. Use `--no-save` only when the caller has another durable record system.

Common commands:

```bash
<skill-path>/scripts/liquidium-borrow max-borrow --collateral-asset BTC --borrow-asset USDC --collateral-amount-decimal 0.0005
<skill-path>/scripts/liquidium-borrow quote --collateral-asset BTC --borrow-asset USDC --collateral-amount-decimal 0.0005 --borrow-amount-decimal 9
<skill-path>/scripts/liquidium-borrow instant-create --collateral-asset BTC --borrow-asset USDC --collateral-amount-decimal 0.0005 --borrow-amount-decimal 9 --borrow-destination 0x2222222222222222222222222222222222222222 --refund-destination bc1qrefunddestination
<skill-path>/scripts/liquidium-borrow loan-instructions --ref 8Y9AQQ --action status
<skill-path>/scripts/liquidium-borrow loan-instructions --ref 8Y9AQQ --action repay
<skill-path>/scripts/liquidium-borrow loan-instructions --ref 8Y9AQQ --action add-collateral
<skill-path>/scripts/liquidium-borrow deposit-status --ref 8Y9AQQ --txid <txid>
<skill-path>/scripts/liquidium-borrow instant-activities --ref 8Y9AQQ --filter active
<skill-path>/scripts/liquidium-borrow loan-list
<skill-path>/scripts/liquidium-borrow loan-show --ref 8Y9AQQ
<skill-path>/scripts/liquidium-borrow loan-tx --ref 8Y9AQQ --kind collateral --txid <txid>
<skill-path>/scripts/liquidium-borrow profile-summary --profile-id <profile-id>
```

The CLI prints JSON for reads and summaries. Use `--json` for raw SDK output where supported. It does not sign messages or broadcast wallet transactions; use wallet tools only after explicit user confirmation.

## Decision Tree

1. If the user wants to borrow without a Liquidium profile or wallet connection, use instant loans. Read `references/instant-loans.md`.
2. If the user asks "how much can I borrow?", run `max-borrow`, then explain LTV and liquidation risk. Read `references/risk-and-liquidation.md`.
3. If the user wants to create, fund, repay, add collateral, or check an instant loan, use `instant-create`, `loan-instructions`, `deposit-status`, `instant-get`, `instant-activities`, and local loan records.
4. If the user lost the instant-loan reference, use `instant-find --address <address>` only to find candidates, then hydrate with `instant-get` or `loan-instructions`.
5. If the user wants a portfolio dashboard, repeated borrowing, connected-wallet supply, withdraw, or profile-level repay, use profile flows. Read `references/profile-flows.md`.
6. If the user wants ETH ERC-20 contract-interaction deposits, use profile-based `client.lending.supply({ mechanism: "contractInteraction", ... })` with an EVM RPC and wallet adapter.

## Safety Rules

- Creating an instant loan request is not the same as transferring collateral. Before broadcasting any on-chain transfer, sending funds, or signing a wallet message, get explicit user confirmation of asset, amount, destination, chain, fee assumptions, and refund/borrow destination.
- Treat borrow, supply, repay, and withdraw as financially consequential. Validate amounts, LTV, pool status, destination addresses, chain, and base-unit conversions before execution.
- Always explain liquidation risk when discussing borrow capacity or high LTV. Include current LTV, max allowed LTV, liquidation threshold LTV, and estimated collateral liquidation price when available. Default to the short warning from `references/risk-and-liquidation.md`; add the high-LTV warning only when the quote is close to max LTV.
- For instant loans, never reuse a collateral deposit target as a repayment target. Always refresh loan state and use the target for the exact action: collateral/add-collateral uses `depositTarget`; repayment uses `repayment.target`.
- When returning instant-loan funding instructions, include `depositWindowSeconds`, an estimated absolute deposit deadline timestamp when available, and make the final line exactly specify the next transfer: `Send <amount> <asset> to <deposit address>`.
- When the user says they sent collateral, run `deposit-status --ref <ref>`; include `--txid <txid>` if they provide one. Explain that Liquidium detection can take a few minutes after broadcast/confirmation, and report activity status, confirmations, and required confirmations when available.
- Include the current borrowing interest rate/APY from the SDK when available. Never display raw scaled rate integers to users.
- For instant loans, explain that the refund address is where collateral is returned after full repayment or when collateral cannot be applied, including failed/late/expired deposit cases. Explain that sending more collateral to the deposit target after the loan starts is a top-up that lowers LTV and improves health.
- For instant loans, explain that partial repayments may reduce debt/LTV but do not trigger collateral withdrawal. The loan must be repaid in full to receive the full collateral amount back.
- Do not expose, request, or store wallet private keys or seed phrases. Use existing wallet providers/adapters.
- If the environment lacks a wallet or transfer tool, return exact transfer instructions rather than pretending to move funds.

## Common Mistakes

- Requiring a wallet adapter for instant loans. Instant loans do not need one.
- Calling `client.lending.borrow(...)` for the default accountless flow. Use `client.instantLoans.create(...)`.
- Treating address recovery as canonical loan state. Hydrate candidates with `instant-get`.
- Displaying raw bigint base units or raw fixed-point rates to users.
- Ignoring frozen pools or `validationErrors`.
- Confusing instant-loan collateral deposit targets with repayment targets.
- Assuming profile-flow `outflow.txid` is present immediately after borrow.
