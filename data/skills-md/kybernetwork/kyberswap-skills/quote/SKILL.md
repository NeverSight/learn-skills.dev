---
name: quote
description: This skill should be used when the user asks to "get a swap quote", "check swap price", "compare token rates", "see exchange rates", "how much would I get for", "price check", or wants to know the expected output for a token trade. Fetches the best route from KyberSwap Aggregator across 18 EVM chains.
metadata:
  tags:
    - defi
    - kyberswap
    - swap
    - quote
    - evm
    - aggregator
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Quote Skill

Fetch swap quotes from the KyberSwap Aggregator. Given a token pair and amount, retrieve the best route and present a clear summary including expected output, exchange rate, and gas cost.

## Input Parsing

The user will provide input like:
- `1 ETH to USDC on ethereum`
- `100 USDC to WBTC on arbitrum`
- `0.5 WBTC to DAI on polygon`
- `1000 USDT to ETH` (default chain: ethereum)

Extract these fields:
- **amount** — the human-readable amount to swap
- **tokenIn** — the input token symbol
- **tokenOut** — the output token symbol
- **chain** — the chain slug (default: `ethereum`)

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

For any token **not** in the built-in registry and **not** a native token, check the honeypot/FOT API. (Note: registry tokens are assumed safe, but a compromised proxy token could theoretically be updated. For high-value swaps involving proxy tokens, consider checking the safety API even for registry tokens.)

```
GET https://token-api.kyberswap.com/api/v1/public/tokens/honeypot-fot-info?chainId={chainId}&address={tokenAddress}
```

Via **WebFetch**, check both `tokenIn` and `tokenOut`:
- If `isHoneypot: true` — **warn the user** that this token is flagged as a honeypot (cannot be sold after buying). Display the warning prominently.
- If `isFOT: true` — warn the user that this token has a fee-on-transfer (tax: `{tax}%`). The actual received amount will be less than the quoted output. Display the adjusted estimate: `adjustedAmount = quotedAmount * (1 - tax/100)`. Example: if the quote shows 100 USDC and tax is 5%, display "~95 USDC after tax".

### Step 3: Convert Amount to Wei

```
amountInWei = amount * 10^(tokenIn decimals)
```

The result must be a plain integer string with no decimals, no scientific notation, and no separators.

**For wei conversion, use a deterministic method instead of relying on AI mental math:**
```bash
python3 -c "print(int(AMOUNT * 10**DECIMALS))"
# or
echo "AMOUNT * 10^DECIMALS" | bc
```
**Verify known reference values:** 1 ETH = 1000000000000000000 (18 decimals), 1 USDC = 1000000 (6 decimals)

Examples:
- 1 ETH (18 decimals) = `1000000000000000000`
- 100 USDC (6 decimals) = `100000000`
- 0.5 WBTC (8 decimals) = `50000000`

### Step 4: Call the Routes API (GET request)

Read the API reference at `${CLAUDE_PLUGIN_ROOT}/references/api-reference.md` for the full specification.

Make the request using **WebFetch**:

```
URL: https://aggregator-api.kyberswap.com/{chain}/api/v1/routes?tokenIn={tokenInAddress}&tokenOut={tokenOutAddress}&amountIn={amountInWei}&source=ai-agent-skills
Prompt: Return the full JSON response body
```

### Step 5: Handle Errors

Check the `code` field in the JSON response and handle common errors inline:

| Code | Message | Quick Fix |
|------|---------|-----------|
| 4008 | Route not found | No liquidity for this pair/amount. Remove source filters (`includedSources`/`excludedSources`), try a smaller amount, or retry after a few seconds. |
| 4011 | Token not found | Verify the token address is correct for this chain. Use `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE` for native tokens. Check spelling and `0x` prefix. |
| 4000 | Bad request | Read the `fieldViolations` array in the response. Common issues: `amountIn` must be a plain integer string in wei (no decimals, no scientific notation), addresses must be 42-char hex with lowercase `0x`. |
| 4010 / 40011 | No eligible pools / Filtered sources (observed behavior, not in public API docs) | Remove `includedSources`/`excludedSources` filters. The pair may have liquidity only on specific DEXs. |
| 404 | Chain not found | Check chain slug spelling. Supported: `ethereum`, `bsc`, `polygon`, `arbitrum`, `optimism`, `avalanche`, `base`, `linea`, `mantle`, `sonic`, `berachain`, `ronin`, `unichain`, `hyperevm`, `plasma`, `etherlink`, `monad`, `megaeth`. |
| 4990 | Request canceled | Retry the request. Likely a timeout or network issue. |
| 500 | Internal server error | Verify all addresses are valid hex. Retry — may be transient. |

For any error code not listed above, or for deeper troubleshooting, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`** for the comprehensive error reference.

### Step 5b: Dust Amount Warning

After getting a successful route, check the USD values from the response:

- If `amountInUsd` < **$0.10** — warn the user: *"This swap amount is extremely small (~$X). Gas fees (~$Y) will far exceed the swap value. Consider using a larger amount."*
- If `gasUsd` > `amountInUsd` — warn the user: *"Gas cost (~$Y) exceeds the swap value (~$X). This trade is uneconomical."*

Still show the quote, but include the warning prominently before the results table.

### Step 6: Format the Output

Present the results in this format:

```
## KyberSwap Quote

**{amount} {tokenIn} → {amountOut} {tokenOut}** on {Chain}

| Detail | Value |
|---|---|
| Input | {amount} {tokenIn} (~${amountInUsd}) |
| Output | {amountOut} {tokenOut} (~${amountOutUsd}) |
| Rate | 1 {tokenIn} = {rate} {tokenOut} |
| Gas estimate | {gas} units (~${gasUsd}) |
| L1 fee (L2 only) | ~${l1FeeUsd} *(omit this row on L1 chains or if `l1FeeUsd` is `"0"`)* |
| Router | `{routerAddress}` |

### Route
{For each split in the route, show: tokenIn → tokenOut via [exchange name]}
```

**Calculating the output amount:**
Convert `amountOut` from wei back to human-readable using tokenOut's decimals:
```
humanAmount = amountOut / 10^(tokenOut decimals)
```

**Calculating the rate:**
```
rate = humanAmountOut / humanAmountIn
```

Display rates with appropriate precision (up to 6 significant digits).

### Structured JSON Output

After the markdown table, always include a JSON code block so other plugins or agents can consume the result programmatically:

````
```json
{
  "type": "kyberswap-quote",
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
  "rate": "{rate}",
  "gas": "{gas}",
  "gasUsd": "{gasUsd}",
  "routerAddress": "{routerAddress}"
}
```
````

This JSON block enables downstream agents or plugins to parse the quote result without scraping the markdown table.

## Important Notes

- Always read both `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md` and `${CLAUDE_PLUGIN_ROOT}/references/api-reference.md` before making API calls.
- Never guess token addresses. Always verify from the registry or via the Token API / search.
- If the user doesn't specify a chain, default to `ethereum`.
- If the user specifies a chain not listed in `references/api-reference.md`, query `https://common-service.kyberswap.com/api/v1/aggregator/supported-chains` via WebFetch to check if the chain is supported. Look for a matching `chainName` with `state: "active"` or `state: "new"`. Use the `chainName` value as the path slug.
- The quote is informational only — no transaction is built or submitted.

## Additional Resources

### Reference Files

- **`${CLAUDE_PLUGIN_ROOT}/references/api-reference.md`** — Full API specification, error codes, rate limiting
- **`${CLAUDE_PLUGIN_ROOT}/references/token-registry.md`** — Token addresses and decimals by chain

### Example Files

Working examples in `${CLAUDE_PLUGIN_ROOT}/skills/quote/references/`:
- **`basic-quote.md`** — Simple ETH to USDC quote on Ethereum
- **`multi-chain-quote.md`** — Quote on L2 chain with L1 fee

## Troubleshooting

For error codes not covered in Step 5, or for advanced debugging (PMM/RFQ errors, edge cases), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
