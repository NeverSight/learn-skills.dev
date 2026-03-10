---
name: swap-build
description: This skill should be used when the user asks to "swap-build", "build a swap transaction", "build swap calldata", "create swap tx", "swap tokens", "trade crypto", "execute a token exchange", "swap ETH to USDC", "convert tokens", or needs encoded calldata for on-chain submission. Fetches the best route and builds transaction data via KyberSwap Aggregator.
metadata:
  tags:
    - defi
    - kyberswap
    - swap
    - transaction
    - evm
    - aggregator
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Build Skill

Build swap transactions using the KyberSwap Aggregator. Given a token pair, amount, and sender address, fetch the best route and generate encoded calldata ready for on-chain submission.

**This is a three-step process:**
1. GET the optimal route (same as the quote skill)
2. **Show quote details and ask for user confirmation**
3. POST to build the encoded transaction calldata

## Input Parsing

The user will provide input like:
- `100 USDC to ETH on arbitrum from 0xAbc123...`
- `1 ETH to USDC on ethereum from 0xAbc123... slippage 100`
- `0.5 WBTC to DAI on polygon from 0xAbc123... to 0xDef456...`

Extract these fields:
- **amount** — the human-readable amount to swap
- **tokenIn** — the input token symbol
- **tokenOut** — the output token symbol
- **chain** — the chain slug (default: `ethereum`)
- **sender** — the address that will send the transaction (**required**)
- **recipient** — the address to receive output tokens (default: same as sender). **WARNING: When the recipient address differs from the sender, display a prominent warning: "Output tokens will be sent to a DIFFERENT address than the sender. Please verify the recipient address carefully."**
- **slippageTolerance** — slippage in basis points (see [Slippage Defaults](#slippage-defaults) below)

**If the sender address is not provided, ask the user for it before proceeding.** Do not guess or use a placeholder address.

**Sender address validation — reject or warn before proceeding:**
- **Must not be the zero address** (`0x0000000000000000000000000000000000000000`) — this is an invalid sender and the transaction will fail.
- **Must not be the native token sentinel** (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) — this is a placeholder for native tokens, not a real account.
- **Warn if it matches a known contract address** (e.g., a token address or the router address) — sending from a contract address is unusual and likely a mistake. Ask the user to confirm.

### Slippage Defaults

If the user does not specify slippage, choose based on the token pair:

| Pair type | Default | Rationale |
|---|---|---|
| Stablecoin ↔ Stablecoin (e.g. USDC→USDT) | **5 bps** (0.05%) | Minimal price deviation between pegged assets |
| Common tokens (e.g. ETH→USDC, WBTC→ETH) | **50 bps** (0.50%) | Standard volatility buffer |
| All other / unknown pairs | **100 bps** (1.00%) | Conservative default for long-tail or volatile tokens |

> These are recommended defaults, not official KyberSwap values. The KyberSwap API defaults to slippageTolerance: 0 if omitted.

**Note:** The API defaults to `0` if `slippageTolerance` is omitted. Always pass an explicit value. The range is `[0, 2000]` (0% to 20%). Use `ignoreCappedSlippage: true` to exceed 20%.

## Workflow

### Step 1: Resolve Token Addresses

Read the token registry at `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`.

Look up `tokenIn` and `tokenOut` for the specified chain. Match case-insensitively. Note the **decimals** for each token.

**Aliases to handle:**
- "ETH" on Ethereum/Arbitrum/Optimism/Base/Linea/Unichain → native token address
- "MATIC" or "POL" on Polygon → native token address
- "BNB" on BSC → native token address
- "AVAX" on Avalanche → native token address
- "MNT" on Mantle → native token address
- "S" on Sonic → native token address
- "BERA" on Berachain → native token address
- "RON" on Ronin → native token address
- "XTZ" on Etherlink → native token address
- "MON" on Monad → native token address

**If a token is not found in the registry:**
Use the fallback sequence described at the bottom of `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`:
1. **KyberSwap Token API** (preferred) — search whitelisted tokens first: `https://token-api.kyberswap.com/api/v1/public/tokens?chainIds={chainId}&name={symbol}&isWhitelisted=true` via WebFetch. Pick the result whose `symbol` matches exactly with the highest `marketCap`. If no whitelisted match, retry without `isWhitelisted` (only trust verified or market-cap tokens). If still nothing, browse `page=1&pageSize=100` (try up to 3 pages).
2. **CoinGecko API** (secondary fallback) — search CoinGecko for verified contract addresses if the Token API doesn't have it.
3. **Ask user manually** (final fallback) — if CoinGecko also fails, ask the user to provide the contract address. Never guess or fabricate addresses.

### Step 2: Check Token Safety

For any token **not** in the built-in registry and **not** a native token, check the honeypot/FOT API:

```
GET https://token-api.kyberswap.com/api/v1/public/tokens/honeypot-fot-info?chainId={chainId}&address={tokenAddress}
```

Via **WebFetch**, check both `tokenIn` and `tokenOut`:
- If `isHoneypot: true` — **refuse the swap** and warn the user that this token is flagged as a honeypot (cannot be sold after buying).
- If `isFOT: true` — warn the user that this token has a fee-on-transfer (tax: `{tax}%`). The actual received amount will be less than the swap output. Proceed only if the user acknowledges the tax.

### Step 3: Convert Amount to Wei

```
amountInWei = amount * 10^(tokenIn decimals)
```

The result must be a plain integer string with no decimals, no scientific notation, and no separators.

### Step 4: Get the Route (GET request)

Read the API reference at `${CLAUDE_PLUGIN_ROOT}/references/api-reference.md` for the full specification.

Make the request using **WebFetch**:

```
URL: https://aggregator-api.kyberswap.com/{chain}/api/v1/routes?tokenIn={tokenInAddress}&tokenOut={tokenOutAddress}&amountIn={amountInWei}&source=ai-agent-skills&origin={sender}
Prompt: Return the full JSON response body exactly as received. I need the complete routeSummary object.
```

If the route request fails, check the `code` field in the JSON response:

| Code | Message | Quick Fix |
|------|---------|-----------|
| 4008 | Route not found | No liquidity for this pair/amount. Remove source filters, try a smaller amount, or retry. |
| 4011 | Token not found | Verify the token address is correct for this chain. Use `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` for native tokens. |
| 4000 | Bad request | Read `fieldViolations` in the response. `amountIn` must be a plain integer string in wei. Addresses must be 42-char hex with lowercase `0x`. |
| 4010 / 40011 | No eligible pools / Filtered sources (observed behavior, not in public API docs) | Remove `includedSources`/`excludedSources` filters. |
| 404 | Chain not found | Check chain slug spelling: `ethereum`, `bsc`, `polygon`, `arbitrum`, `optimism`, `avalanche`, `base`, `linea`, `mantle`, `sonic`, `berachain`, `ronin`, `unichain`, `hyperevm`, `plasma`, `etherlink`, `monad`, `megaeth`. |

For any error not listed here, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

Extract the `data.routeSummary` object from the response. You need the **complete** `routeSummary` object for the build step.

### Step 4a: Dust Amount Check

After getting a successful route, check the USD values from the `routeSummary`:

- If `amountInUsd` < **$0.10** — warn the user and **ask for confirmation**: *"This swap amount is extremely small (~$X). Gas fees (~$Y) will far exceed the swap value. Do you still want to proceed?"*
- If `gasUsd` > `amountInUsd` — warn the user and **ask for confirmation**: *"Gas cost (~$Y) exceeds the swap value (~$X). This trade is uneconomical. Do you still want to proceed?"*

If the user declines, abort the swap. Do NOT proceed to the build step.

### Step 4b: Display Quote and Request Confirmation

**CRITICAL: Always show quote details and ask for confirmation before building the transaction.**

Calculate the output amount and rate from the `routeSummary`:
```
amountOut = routeSummary.amountOut / 10^(tokenOut decimals)
rate = amountOut / amount
minAmountOut = amountOut * (1 - slippageTolerance/10000)
```

Present the quote details:

```
## Swap Quote — Confirmation Required

**{amount} {tokenIn} → {amountOut} {tokenOut}** on {Chain}

| Detail | Value |
|---|---|
| You send | {amount} {tokenIn} (~${amountInUsd}) |
| You receive | {amountOut} {tokenOut} (~${amountOutUsd}) |
| Exchange rate | 1 {tokenIn} = {rate} {tokenOut} |
| Minimum received | {minAmountOut} {tokenOut} (after {slippage}% slippage) |
| Price impact | {priceImpact}% *(from routeSummary.extraFee.feeAmount if available)* |
| Gas estimate | {gas} units (~${gasUsd}) |
| Route | {routeSummary.route description — e.g., "Uniswap V3 → Curve"} |

### Addresses

| Field | Value |
|---|---|
| Router | `{routerAddress}` |
| Sender | `{sender}` |
| Recipient | `{recipient}` |

---

⚠️ **Review the quote carefully:**
- Verify the exchange rate is acceptable
- Check the minimum received amount
- Ensure the router address is correct (`0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` on most chains)

**Do you want to proceed with building this swap transaction?** (yes/no)
```

**Wait for the user to explicitly confirm with "yes", "confirm", "proceed", or similar affirmative response before building the transaction.**

If the user says "no", "cancel", or similar, abort and inform them the swap was cancelled. Do NOT proceed to Step 5.

**Note:** Routes expire quickly (~30 seconds). If the user takes too long to confirm, warn them that the quote may be stale and offer to re-fetch.

### Step 5: Build the Transaction (POST request)

**Only proceed to this step after the user confirms in Step 4b.**

**WebFetch only supports GET requests**, so use `Bash(curl)` for this POST request.

Construct the curl command:

```bash
curl -s -X POST "https://aggregator-api.kyberswap.com/{chain}/api/v1/route/build" \
  -H "Content-Type: application/json" \
  -H "X-Client-Id: ai-agent-skills" \
  -d '{
    "routeSummary": {PASTE THE COMPLETE routeSummary OBJECT HERE},
    "sender": "{sender}",
    "recipient": "{recipient}",
    "origin": "{sender}",
    "slippageTolerance": {slippageTolerance},
    "deadline": {CURRENT_UNIX_TIMESTAMP + 1200},
    "source": "ai-agent-skills"
  }'
```

**To get the current unix timestamp + 20 minutes for the deadline:**
```bash
echo $(($(date +%s) + 1200))
```

You can combine this into one command or compute it separately.

**Important:** The `routeSummary` field must contain the **exact** JSON object returned from Step 4. Do not modify, truncate, or reformat it.

**Optional fields** (include if relevant):
- Add `"permit": "{encoded_permit}"` if the user provides an ERC-2612 permit signature (skips the separate approval tx).
- Add `"enableGasEstimation": true` for a more accurate gas figure.
- Add `"ignoreCappedSlippage": true` if the user requests slippage above 20%.

See `${CLAUDE_PLUGIN_ROOT}/references/api-reference.md` for all available fields.

### Step 5b: Handle Build Errors

If the build request fails, check the `code` field in the JSON response:

| Code | Message | Quick Fix |
|------|---------|-----------|
| 4227 | `return amount is not enough` | Price moved since route fetch. **Fetch a fresh route and retry** (recommended). The response includes `suggestedSlippage` (in bps) as a fallback. |
| 4227 | `insufficient funds for gas * price + value` | Sender doesn't have enough native token (ETH/MATIC/etc.) to cover `amountIn` + gas. Reduce amount or top up wallet. |
| 4227 | `TRANSFER_FROM_FAILED` | Sender hasn't approved the router to spend the input token, or token balance is insufficient. Check approval and balance. |
| 4222 | Quoted amount smaller than estimated | RFQ/limit order quote came in lower than estimated. **Fetch a fresh route and retry**. Or use `excludeRFQSources: true` to avoid RFQ sources. |
| 4002 | Request body malformed | Ensure `deadline` and `slippageTolerance` are numbers, booleans are `true`/`false`. Do NOT modify the `routeSummary` object. |
| 40010 (observed behavior, not in public API docs) | Empty sender address | Provide a valid `sender` address, or set `enableGasEstimation: false`. |
| 4000 | Bad request | Read `fieldViolations`. Common: `slippageTolerance` > 2000 needs `ignoreCappedSlippage: true`, `deadline` must be in the future, `recipient` is required. |
| PMM/RFQ errors | Various maker errors | Fetch a fresh route and retry. Or use `excludedSources` to skip the failing maker. See the table below. |

**Common PMM/RFQ error patterns:**

| Pattern | Meaning | Quick Fix |
|---------|---------|-----------|
| Blacklist / Banned | Sender address is on maker's deny list | Use a different sender address |
| Insufficient Liquidity | Maker doesn't have enough balance | Retry or exclude the source |
| Amount Too Small/Large | Trade size outside maker's range | Adjust `amountIn` |
| Market Moved | Price changed between route and build | Fetch fresh route and retry |

For any error not listed here, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

### Step 6: Format the Output

Present the results:

```
## KyberSwap Swap Transaction

**{amount} {tokenIn} → {amountOut} {tokenOut}** on {Chain}

| Detail | Value |
|---|---|
| Input | {amount} {tokenIn} (~${amountInUsd}) |
| Expected output | {amountOut} {tokenOut} (~${amountOutUsd}) |
| Minimum output (after slippage) | {minAmountOut} {tokenOut} |
| Slippage tolerance | {slippageTolerance/100}% |
| Gas estimate | {gas} units (~${gasUsd}) |
| L1 fee (L2 only) | ~${additionalCostUsd} — {additionalCostMessage} *(omit on L1 chains or if absent)* |

### Transaction Details

| Field | Value |
|---|---|
| To (Router) | `{routerAddress}` |
| Value | `{value}` (in wei — non-zero only for native token input) |
| Data | `{encodedCalldata}` |
| Sender | `{sender}` |
| Recipient | `{recipient}` |

> **WARNING:** Review the transaction details carefully before submitting on-chain. This plugin does NOT submit transactions — it only builds the calldata. You are responsible for verifying the router address, amounts, and calldata before signing and broadcasting.
```

### Structured JSON Output

After the markdown table, always include a JSON code block so other plugins or agents can consume the result programmatically:

````
```json
{
  "type": "kyberswap-swap",
  "chain": "{chain}",
  "tokenIn": {
    "symbol": "{tokenIn}",
    "address": "{tokenInAddress}",
    "decimals": {tokenInDecimals},
    "amount": "{amount}",
    "amountWei": "{amountInWei}",
    "amountUsd": "{amountInUsd}"
  },
  "tokenOut": {
    "symbol": "{tokenOut}",
    "address": "{tokenOutAddress}",
    "decimals": {tokenOutDecimals},
    "amount": "{amountOut}",
    "amountWei": "{amountOutWei}",
    "amountUsd": "{amountOutUsd}"
  },
  "tx": {
    "to": "{routerAddress}",
    "data": "{encodedCalldata}",
    "value": "{transactionValue}",
    "gas": "{gas}",
    "gasUsd": "{gasUsd}"
  },
  "sender": "{sender}",
  "recipient": "{recipient}",
  "slippageBps": {slippageTolerance}
}
```
````

This JSON block enables downstream agents or plugins to parse the swap result without scraping the markdown table.

**Calculating minimum output:**
If `outputChange` is provided in the build response, use:
```
minAmountOut = amountOut from build response / 10^(tokenOut decimals)
```

**Value field:**
Use the `transactionValue` field from the build response directly. This is the `value` for the on-chain transaction (in wei). It will be non-zero only for native token input. Do not compute this manually.

### Step 7: ERC-20 Approval Reminder

If `tokenIn` is **not** the native token, add this note after the transaction details:

```
### Token Approval Required

Before submitting this swap, you must approve the KyberSwap router to spend your {tokenIn}:

- **Token contract:** `{tokenIn address}`
- **Spender (router):** `{routerAddress}`
- **Amount:** `{amountInWei}` (exact amount, recommended) or `type(uint256).max` (unlimited — see warning below)

> **Security warning:** Unlimited approvals (`type(uint256).max`) are convenient but risky. If the router contract is ever compromised, an attacker could drain all approved tokens from your wallet. For large holdings, prefer **exact-amount approvals** matching `amountInWei`. Only use unlimited approvals with wallets holding limited funds.

Use your wallet or a tool like `cast` to send the approval transaction first.
```

## Important Notes

- Always read both `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md` and `${CLAUDE_PLUGIN_ROOT}/references/api-reference.md` before making API calls.
- Never guess token addresses or sender addresses.
- If the user doesn't specify a chain, default to `ethereum`.
- If the user specifies a chain not listed in `references/api-reference.md`, query `https://common-service.kyberswap.com/api/v1/aggregator/supported-chains` via WebFetch to check if the chain is supported. Look for a matching `chainName` with `state: "active"` or `state: "new"`. Use the `chainName` value as the path slug.
- If the user doesn't specify slippage, use the smart defaults from the [Slippage Defaults](#slippage-defaults) table.
- Routes should not be cached for more than 5-10 seconds. If the build step fails, re-fetch the route from the GET endpoint and retry.
- This skill does NOT submit transactions on-chain. It only builds the calldata.

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** — Full API specification, error codes, rate limiting
- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** — Token addresses and decimals by chain

### Example Files

Working examples in `${CLAUDE_PLUGIN_ROOT}/skills/swap-build/references/`:
- **`basic-swap.md`** — Simple ETH to USDC swap with native token input
- **`erc20-swap.md`** — ERC-20 swap requiring token approval

## Troubleshooting

For error codes not covered in Steps 4/5b, or for advanced debugging (full PMM/RFQ error catalog, on-chain revert analysis), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
