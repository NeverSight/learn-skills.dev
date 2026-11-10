---
name: ai-hub-futures-trade
version: "0.1.31"
description: Prepare Futures ordinary, conditional and TP/SL orders and trading settings.
---

# Ai Hub Futures Trade

## Unified merchant connections

A single MCP server may support both Spot and Futures. Select the configured merchant by `system_get_capabilities`, including `products` and `productAccess`; never infer its product from the server name. Use product-specific tools on that same server. For CLI fallback, use the selected unified merchant profile for either product, replacing legacy `--profile spot` / `--profile futures` examples below. Never switch merchant profiles to recover from a failed request. Existing separate product profiles remain supported.


Use `futures_prepare_place_order`, `futures_prepare_place_condition_order`, `futures_prepare_place_profit_loss_order`, `futures_prepare_set_position_mode`, `futures_prepare_set_margin_mode`, `futures_prepare_adjust_position_margin`, and `futures_prepare_set_leverage`. CLI uses `ai-hub futures <operation> --profile futures`.

Ordinary/conditional placement requires exact contract, open-long/open-short/close-long/close-short intent, LIMIT/MARKET, one explicit quantity unit (coin/contracts/value), quantity and cross/isolated margin mode. Do not convert order value to margin using assumed leverage. LIMIT requires price; MARKET omits price and timeInForce. Keep generated clientOrderId unchanged.

A conditional or TP/SL order is submitted now with its trigger price after confirmation. The exchange watches prices and triggers it. Do not run an Agent price watcher and place an ordinary order later. Condition directions 3UP/4DOWN are distinct from TP/SL stop-loss/take-profit enums. TP/SL supports up to five positive integer-contract items; do not promise OCO or sibling cancellation.

Position-mode changes are account-wide; margin mode and leverage are contract-specific. Isolated margin adjustment targets a position, with positive amount adding and negative amount removing margin. Show actual scope and current-to-target values when known. Never auto-close positions, cancel orders or change another setting to satisfy prerequisites.

## User-facing error rendering

MCP and CLI error envelopes are machine-readable transport results. Do not paste the JSON envelope into an ordinary user reply. Translate a verified Futures diagnosis into one concise Chinese explanation, while keeping the underlying code available to the caller for logging and troubleshooting. For example, `-1154` / `ORDER_PRICE_OUT_OF_RANGE` should be reported as: “下单失败：委托价格超出交易所允许的价格偏差范围，请调整价格后重试。” Mention request IDs or the raw envelope only when the user asks for technical diagnostics. An explicit rejection is different from an unknown write: say that the order was rejected and was not submitted; for an unknown write, say that execution cannot yet be established and never suggest resubmitting.

## Execution boundary

Prefer the available MCP tool. Use CLI only if MCP is unavailable before dispatch; never retry a possibly submitted write through another transport. Profile configuration errors are not permission to choose a different account.

For every write, prepare, display the complete preview, stop, and wait for a NEW explicit user message before `confirm_action` or `ai-hub confirm --profile <original-profile> --confirmation-id <id> --user-confirmation <message>`. Never infer confirmation from the original request. Core binds the preview and permits one dispatch.

If the result is unknown, do not resend or create a replacement client ID. Use supported read-only evidence and report unresolved status when it cannot be established. Core limits same-interface calls to at least one second apart; do not evade limits with alternate processes or profiles.

Do not request or expose API credentials in chat. Configure credentials only through the local profile workflow.
