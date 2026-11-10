---
name: ai-hub-futures
version: "0.1.31"
description: Route Futures account and trading requests to the installed AI Hub tools.
---

# Ai Hub Futures

## Unified merchant connections

A single MCP server may support both Spot and Futures. Select the configured merchant by `system_get_capabilities`, including `products` and `productAccess`; never infer its product from the server name. Use product-specific tools on that same server. For CLI fallback, use the selected unified merchant profile for either product, replacing legacy `--profile spot` / `--profile futures` examples below. Never switch merchant profiles to recover from a failed request. Existing separate product profiles remain supported.


Use the selected unified merchant profile for both products, or the matching legacy `futures` / `spot` profiles when the installation uses separate servers. Check the installed server's product capabilities when selecting a server; do not infer product from its label or fall back to smoke/default.

For an unspecified balance request, query spot and Futures separately and display both without adding equity, margin or unrealized PnL together. Preserve partial failures and never replace failure with zero. Do not assert that profiles belong to the same user without verified pairing.

Route market questions to `ai-hub-futures-common`, balances/positions/PnL/transactions to `ai-hub-futures-account`, order lookup/fills/cancellation to `ai-hub-futures-order`, placements/settings to `ai-hub-futures-trade`, and transfers to `ai-hub-futures-transfer`. Use the matching available MCP tool directly; load a focused Skill when its workflow needs clarification.

Excluded this release: public recent market trades, ordinary batch placement, selected ordinary batch cancellation, ticker_all, WebSocket and strategy/copy/robot operations. Do not synthesize missing batches by repeatedly invoking single writes.

## Execution boundary

Prefer the available MCP tool. Use CLI only if MCP is unavailable before dispatch; never retry a possibly submitted write through another transport. Profile configuration errors are not permission to choose a different account.

For every write, prepare, display the complete preview, stop, and wait for a NEW explicit user message before `confirm_action` or `ai-hub confirm --profile <original-profile> --confirmation-id <id> --user-confirmation <message>`. Never infer confirmation from the original request. Core binds the preview and permits one dispatch.

If the result is unknown, do not resend or create a replacement client ID. Use supported read-only evidence and report unresolved status when it cannot be established. Core limits same-interface calls to at least one second apart; do not evade limits with alternate processes or profiles.

Do not request or expose API credentials in chat. Configure credentials only through the local profile workflow.
