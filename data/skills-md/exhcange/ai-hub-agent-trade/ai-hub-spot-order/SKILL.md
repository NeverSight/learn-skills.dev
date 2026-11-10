---
name: ai-hub-spot-order
version: "0.1.31"
description: Use this Skill when a user asks to retrieve or place supported AI Hub spot or isolated/cross spot-margin orders. Use the local ai-hub CLI with a configured credential profile. Never route to derivatives or accept an explicit leverage multiplier. Every state-changing action requires an exact preview followed by a new manual user confirmation.
---

# AI Hub Spot Orders

## Unified merchant connections

A single MCP server may support both Spot and Futures. Select the configured merchant by `system_get_capabilities`, including `products` and `productAccess`; never infer its product from the server name. Use product-specific tools on that same server. For CLI fallback, use the selected unified merchant profile for either product, replacing legacy `--profile spot` / `--profile futures` examples below. Never switch merchant profiles to recover from a failed request. Existing separate product profiles remain supported.


Use this Skill only for supported spot and spot-margin order operations. Do not infer an order size, symbol, side, price, order ID, or margin mode. For financial actions, preserve the exact values supplied by the user.

## Spot Margin Boundary

- Margin commands mean isolated or cross **spot margin only**. Route explicit Futures or long/short-position requests to ai-hub-futures and the selected connection’s Futures tools; never submit them through spot tools.
- An explicit leverage multiplier such as `10x` is not accepted by the OpenAPI order endpoint. Do not reinterpret it as an order amount, margin mode, or contract request.
- For a request such as “open BTC at 10x”, explain that explicit leverage multiples are unsupported, state that only spot margin is available, and request the supported fields: isolated or cross mode, symbol, BUY or SELL, quantity or quote amount, and order type.
- Every spot-margin write requires an explicit mode: `--isolated true` selects isolated margin and `--isolated false` selects cross margin. Never rely on an upstream default.

The CLI and MCP resolve a display symbol such as `BTCUSDT` or `BTC/USDT` from the selected profile's symbol snapshot before every spot order read or write. A mixed-cloud tenant therefore submits its own physical OpenAPI symbol; do not add a tenant suffix manually.

## MCP First

If AI Hub MCP Tools are available, call the matching read Tool, `spot_prepare_*` Tool, or `margin_prepare_*` Tool directly. Do not read CLI references, run CLI help, or inspect configuration first. After a prepare result, stop for a new user message before `confirm_action`. Use CLI Fast Path only when MCP is unavailable.

Read [references/mcp-routing.md](references/mcp-routing.md) for the shared MCP routing and fallback rules.

## Prerequisites

If the selected profile is already configured, run the focused command directly. Read [references/preflight.md](references/preflight.md) only for first-time setup, a profile change, or a configuration/credential error. Confirm that the user has supplied all mandatory order fields.

For `AI_HUB_OPENAPI_BUSINESS_ERROR`, read [references/openapi-error-diagnosis.md](references/openapi-error-diagnosis.md). Never retry a failed or unknown write until the diagnosis permits it and the user starts a new confirmation flow.

## Fast Path

When a read request has its complete command parameters, run it directly. When a write request has all required fields, run the exact command once to produce its preview, then stop. Read [references/order-commands.md](references/order-commands.md) only for missing or ambiguous fields, a business error, or an unknown write result; never bypass the new-user-confirmation boundary.

## Command Index

| Command | Operation | Description |
| --- | --- | --- |
| `ai-hub spot order test` | Read-like validation | Validate one order without sending it to the matching engine. |
| `ai-hub spot order get` | Read | Get one order by symbol and exactly one of order ID or client order ID. |
| `ai-hub spot order open` | Read | List current open orders. |
| `ai-hub spot order history` | Read | List completed and cancelled orders. |
| `ai-hub spot order fills` | Read | List fills for one symbol. |
| `ai-hub spot order market-buy` | Write | Spend an exact quote-asset amount at market. |
| `ai-hub spot order market-sell` | Write | Sell an exact base-asset quantity at market. |
| `ai-hub spot order sell-available` | Write | Preview the maximum executable available base-asset balance for sale. |
| `ai-hub spot order limit` | Write | Place a LIMIT, IOC, FOK, or POST_ONLY BUY or SELL. |
| `ai-hub spot order stop-limit` | Write | Place a STOP BUY or SELL with a trigger and execution price. |
| `ai-hub spot order stop-market-buy` | Write | Place a STOP_MARKET BUY by quote amount. |
| `ai-hub spot order stop-market-sell` | Write | Place a STOP_MARKET SELL by base quantity. |
| `ai-hub spot order cancel` | Write | Cancel one supported spot order. |
| `ai-hub spot order batch-place` | Write | Place 1–10 orders for one symbol. |
| `ai-hub spot order batch-cancel` | Write | Submit cancellation requests for 1–10 orders for one symbol. |

Spot-margin commands use the corresponding `ai-hub margin order ...` paths for `get`, `open`, `fills`, `market-buy`, `market-sell`, `limit`, `stop-limit`, `stop-market-buy`, `stop-market-sell`, and `cancel`. Every margin write also requires `--isolated true|false`.

## Read and Test Workflow

1. Use `test` when the user wants parameter validation without a matching-engine submission.
2. Use `get`, `open`, `history`, or `fills` to inspect an existing order or activity.
3. If a previous write has an unknown outcome, query by order ID or client order ID before any further action.

## Write Workflow

1. Use `market-buy` only for a market BUY with `--quote-amount`: this is the exact quote asset to spend. Never reinterpret a requested base-asset quantity as a quote amount.
2. Use `market-sell` only for a market SELL with `--base-quantity`: this is the exact base asset to sell.
3. Use `limit` with `--type LIMIT|IOC|FOK|POST_ONLY`, `--base-quantity`, and `--price`. The server receives this value directly as `type`; do not use a `timeInForce` parameter.
4. Use `stop-limit` with `--base-quantity`, `--price`, and `--trigger-price` for `STOP` orders.
5. Use `stop-market-buy` with `--quote-amount` and `--trigger-price`, or `stop-market-sell` with `--base-quantity` and `--trigger-price`. Never supply a price to STOP_MARKET.
6. Before preview, shared Core applies the exact OpenAPI symbol rule: MARKET and STOP_MARKET BUY compare the quote amount with `marketBuyMin`; MARKET and STOP_MARKET SELL compare the base quantity with `marketSellMin`. The same rule applies to spot, margin, and batch orders. Missing or zero fields defer validation to OpenAPI; do not derive another minimum.
7. Use `sell-available` only when the user explicitly asks to sell all available balance. It floors the available base balance to the configured quantity precision and displays the executable amount and remainder in the preview. For `market-sell`, never change the exact quantity supplied by the user.
8. Run the write command once, optionally with `--prepare`. It prints `executionMode: LIVE`, `executed: false`, `requiresNewUserConfirmation: true`, `confirmationId`, and `expiresAt`. Every order preview identifies both `symbol` and `apiSymbol`, states `quantityOrAmount` and `priceOrMarket`, and includes `estimatedNotional`.
9. Treat `estimatedNotional.status` literally: `DETERMINISTIC` means a limit-style quantity × price or exact market-BUY quote amount; `INDICATIVE` means a market-SELL quantity × a live ticker and is not a guaranteed fill; `UNAVAILABLE` means no amount can be shown. Do not show or estimate fees before execution.
10. For an immediate market order, the preview captures a live ticker. At confirmation, a BUY price rise or SELL price fall greater than 5% rejects the request; prepare a new preview instead of bypassing the guard. STOP_MARKET sell remains unavailable until triggered.
11. Stop and wait for a new explicit user message. Only then run `ai-hub confirm --confirmation-id <id> --user-confirmation <message>` exactly once.
12. Never type, pipe, generate, or infer a confirmation. Never use `--confirm`; it is intentionally rejected.
13. Do not automatically retry an uncertain result. Query the order first.

For spot margin, apply the same unit, precision, preview, and confirmation rules. Require `--isolated true` or `--isolated false` on every write. If the user supplies a leverage multiplier, stop before preview and explain that the multiplier is unsupported.

For `batch-place`, provide semantic order items only: `MARKET BUY` uses `quoteAmount`; `MARKET SELL` uses `baseQuantity`; `LIMIT`, `IOC`, `FOK`, and `POST_ONLY` use `baseQuantity` plus `price`. Each item can provide `newClientOrderId`; otherwise the CLI generates one. The Core compiles this to the OpenAPI's `batchType`, `volume`, and `client_order_id` fields only after preflight. Do not supply raw `volume` or `client_order_id` yourself.

Only read [references/order-commands.md](references/order-commands.md) when Fast Path does not apply.
