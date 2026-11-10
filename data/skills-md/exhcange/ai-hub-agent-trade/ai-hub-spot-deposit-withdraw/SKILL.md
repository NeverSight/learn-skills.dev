---
name: ai-hub-spot-deposit-withdraw
version: "0.1.31"
description: Use this Skill when a user asks about AI Hub wallet assets, deposit history or addresses, withdrawal addresses or history, transferable assets, wallet transfer history, wallet transfers, or withdrawals. Use the local ai-hub CLI with a configured credential profile. Wallet transfers and withdrawals require the mandatory preview and new manual confirmation boundary.
---

# AI Hub Deposits and Withdrawals

## Unified merchant connections

A single MCP server may support both Spot and Futures. Select the configured merchant by `system_get_capabilities`, including `products` and `productAccess`; never infer its product from the server name. Use product-specific tools on that same server. For CLI fallback, use the selected unified merchant profile for either product, replacing legacy `--profile spot` / `--profile futures` examples below. Never switch merchant profiles to recover from a failed request. Existing separate product profiles remain supported.


Use this Skill for supported wallet operations. Treat asset balances, addresses, and transaction history as sensitive user data. Do not fabricate an address, network detail, account type, or transfer direction.

Account types are fixed: `1` Spot, `2` Isolated Margin, `3` Cross Margin, `4` C2C, and `5` Derivatives. Account type `2` is never Derivatives. A wallet transfer involving type `2` requires the isolated-margin trading pair in `symbol`.

## MCP First

If AI Hub MCP Tools are available, call the matching `wallet_*` Tool directly. For writes, use only `wallet_prepare_*`, then stop for a new user message before `confirm_action`. Do not read CLI references, run CLI help, or inspect configuration first. Use CLI Fast Path only when MCP is unavailable.

Read [references/mcp-routing.md](references/mcp-routing.md) for the shared MCP/CLI fallback boundary.

## Prerequisites

If the selected profile is already configured, run the focused command directly. Read [references/preflight.md](references/preflight.md) only for first-time setup, a profile change, or a configuration/credential error.

For `AI_HUB_OPENAPI_BUSINESS_ERROR`, read [references/openapi-error-diagnosis.md](references/openapi-error-diagnosis.md). In particular, a withdrawal-history permission diagnosis requires an API-key permission change, not a retry.

## Fast Path

When one read command has complete parameters, run it directly. When a transfer or withdrawal has all required fields, generate exactly one preview and stop for a new user confirmation. Load the reference only for missing/ambiguous fields, setup, business errors, or uncertain write outcomes.

## Command Index

| Command | Operation | Description |
| --- | --- | --- |
| `ai-hub wallet transferable-assets` | Read | Get assets transferable from an account type. |
| `ai-hub wallet transfer-history` | Read | Get universal transfer history. |
| `ai-hub wallet deposit-history` | Read | Get deposit history. |
| `ai-hub wallet deposit-address` | Read | Get deposit addresses for a main coin. |
| `ai-hub wallet withdraw-address` | Read | Get withdrawal addresses for a main coin. |
| `ai-hub wallet withdraw-history` | Read | Get withdrawal request history. |
| `ai-hub wallet transfer` | Write | Transfer assets between account types. |
| `ai-hub wallet withdraw` | Write | Submit a withdrawal request. |

## Read Workflow

1. Identify whether the user needs an account asset, address, history, or transferable-asset query.
2. Require the main coin symbol for address queries and the account type for transferable-asset queries.
3. Return only the requested information. Never reformat an address in a way that can change it.

## Asset Movement Workflow

1. For a wallet transfer, collect source and destination account types, coin symbol, amount, and optional symbol exactly. State both the numeric type and its account name in the preview.
2. If either account type is `2` (Isolated Margin), require `symbol` as the isolated-margin trading pair; it is not a Derivatives identifier.
3. Do not use wallet account type `2` for a user request that says Derivatives.
4. For a withdrawal, collect the withdrawal order ID, coin symbol, amount, exact address, and optional label. Do not infer a label or destination.
5. Show a plain-language summary before executing the command.
6. Run the command once. It prints the exact preview.
7. Stop and wait for a new explicit user message. Then run `ai-hub confirm --confirmation-id <id> --user-confirmation <message>` once; never enter, pipe, or infer it.
8. If the write outcome is unknown, query its relevant history before any retry.

Only read [references/wallet-commands.md](references/wallet-commands.md) when Fast Path does not apply.
