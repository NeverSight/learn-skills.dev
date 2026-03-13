---
name: xxyy-trade
description: >-
  This skill should be used when the user asks to "buy token", "sell token",
  "swap token", "trade crypto", "check trade status", "query transaction",
  "scan tokens", "feed", "monitor chain", "query token", "token details",
  "check token safety", or mentions trading on Solana/ETH/BSC/Base chains via XXYY.
  Enables on-chain token trading and data queries through the XXYY Open API.
version: 1.1.0
metadata: { "openclaw": { "requires": { "env": ["XXYY_API_KEY"], "bins": ["curl"] }, "primaryEnv": "XXYY_API_KEY", "emoji": "💹", "homepage": "https://www.xxyy.io" } }
---

# XXYY Trade

On-chain token trading and data queries on Solana, Ethereum, BSC, and Base via XXYY Open API.

## Prerequisites

Set environment variables before use:
- `XXYY_API_KEY` (required) -- Your XXYY Open API Key (format: `xxyy_ak_xxxx`). Get one at https://www.xxyy.io/apikey
- `XXYY_API_BASE_URL` (optional) -- API base URL, defaults to `https://www.xxyy.io`

## Authentication

All requests require header: `Authorization: Bearer $XXYY_API_KEY`

## Security Notes

- **⚠️ API Key = Wallet access** -- Your XXYY API Key can execute real on-chain trades using your wallet balance. If it leaks, anyone can buy/sell tokens with your funds. Never share it, never commit it to version control, never expose it in logs or public channels. If you suspect a leak, regenerate the key immediately at https://xxyy.io.
- **Custodial trading model** -- XXYY is a custodial trading platform. You only provide your wallet address (public key) and API Key. No private keys or wallet signing are needed -- XXYY executes trades on your behalf through their platform.
- **No read-only mode** -- The same API Key is used for both data queries (Feed, Token Query) and trading (Buy, Sell). There is currently no separate read-only key.

## API Reference

### Buy Token
`POST ${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/swap`

```json
{
  "chain": "sol",
  "walletAddress": "<user_wallet>",
  "tokenAddress": "<token_contract>",
  "isBuy": true,
  "amount": 0.1,
  "tip": 0.001,
  "slippage": 20
}
```

#### Buy Parameters

| Param | Required | Type | Valid values | Description |
|-------|----------|------|-------------|-------------|
| `chain` | YES | string | `sol` / `eth` / `bsc` / `base` | Only these 4 values accepted |
| `walletAddress` | YES | string | SOL: Base58 32-44 chars; EVM: 0x+40hex | Wallet address on XXYY platform, must match chain |
| `tokenAddress` | YES | string | Valid contract address | Token contract address to buy |
| `isBuy` | YES | boolean | `true` | Must be true for buy |
| `amount` | YES | number | > 0 | Amount in native currency (SOL/ETH/BNB) |
| `tip` | YES | number | SOL: 0.001-0.1 (unit: SOL); EVM: 0.1-100 (unit: Gwei) | Priority fee for all chains. If not provided, falls back to priorityFee |
| `slippage` | NO | number | 0-100 | Slippage tolerance %, default 20 |
| `model` | NO | number | 1 or 2 | 1=anti-sandwich (default), 2=fast mode |
| `priorityFee` | NO | number | >= 0 | Solana chain only. Extra priority fee in addition to tip |

### Sell Token
`POST ${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/swap`

```json
{
  "chain": "sol",
  "walletAddress": "<user_wallet>",
  "tokenAddress": "<token_contract>",
  "isBuy": false,
  "amount": 50,
  "tip": 0.001
}
```

#### Sell Parameters

| Param | Required | Type | Valid values | Description |
|-------|----------|------|-------------|-------------|
| `chain` | YES | string | `sol` / `eth` / `bsc` / `base` | Only these 4 values accepted |
| `walletAddress` | YES | string | SOL: Base58 32-44 chars; EVM: 0x+40hex | Wallet address on XXYY platform, must match chain |
| `tokenAddress` | YES | string | Valid contract address | Token contract address to sell |
| `isBuy` | YES | boolean | `false` | Must be false for sell |
| `amount` | YES | number | 1-100 | Sell percentage. Example: 50 = sell 50% of holdings |
| `tip` | YES | number | SOL: 0.001-0.1 (unit: SOL); EVM: 0.1-100 (unit: Gwei) | Priority fee for all chains. If not provided, falls back to priorityFee |
| `slippage` | NO | number | 0-100 | Slippage tolerance %, default 20 |
| `model` | NO | number | 1 or 2 | 1=anti-sandwich (default), 2=fast mode |
| `priorityFee` | NO | number | >= 0 | Solana chain only. Extra priority fee in addition to tip |

### tip / priorityFee Rules

- `tip` (required) -- Universal priority fee for ALL chains. EVM chains (eth/bsc/base) use tip as the priority fee. If tip is not provided, the API falls back to priorityFee.
  - SOL chain: unit is SOL (1 = 1 SOL, very expensive). Recommended range: 0.001 - 0.1
  - EVM chains (eth/bsc/base): unit is Gwei. Recommended range: 0.1 - 100
- `priorityFee` (optional) -- Only effective on Solana chain. Solana supports both tip and priorityFee simultaneously.

### Query Trade
`GET ${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/trade?txId=<tx_id>`

Response fields: txId, status (pending/success/failed), statusDesc, chain, tokenAddress, walletAddress, isBuy, baseAmount, quoteAmount

### Ping
`GET ${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/ping`

Returns "pong" if API key is valid.

### Feed (Scan Tokens)
`POST ${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/feed/{type}?chain={chain}`

Retrieve Meme token lists: newly launched, almost graduated, or graduated.

#### Path & Query Parameters

| Param | Required | Type | Valid values | Description |
|-------|----------|------|-------------|-------------|
| `type` | YES | path string | `NEW` / `ALMOST` / `COMPLETED` | NEW = newly launched, ALMOST = almost graduated, COMPLETED = graduated |
| `chain` | NO | query string | `sol` / `bsc` | Only these 2 chains supported. Default `sol` |

#### Body (Filter Parameters)

All filters are optional. Range parameters use comma-separated string format `"min,max"`. Leave one side empty to set only min or max (e.g. `"100,"` = min 100, `",50"` = max 50).

| Param | Type | Description | Example |
|-------|------|-------------|---------|
| `dex` | string[] | DEX platform filter | See DEX Values by Chain below |
| `quoteTokens` | string[] | Quote token filter | See quoteTokens Values by Chain below |
| `link` | string[] | Social media link filter | `["x","tg","web"]` |
| `keywords` | string[] | Token name/symbol keyword match | `["pepe","doge"]` |
| `ignoreWords` | string[] | Ignore keywords | `["scam"]` |
| `mc` | string | Market cap range (USD) | `"10000,500000"` |
| `liq` | string | Liquidity range (USD) | `"1000,"` |
| `vol` | string | Trading volume range (USD) | `"5000,100000"` |
| `holder` | string | Holder count range | `"50,"` |
| `createTime` | string | Creation time range (minutes from now) | `"1,20"` |
| `tradeCount` | string | Trade count range | `"100,"` |
| `buyCount` | string | Buy count range | `"50,"` |
| `sellCount` | string | Sell count range | `"10,"` |
| `devBuy` | string | Dev buy amount range (native token) | `"0.001,"` |
| `devSell` | string | Dev sell amount range (native token) | `"0.001,"` |
| `devHp` | string | Dev holding % range | `",60"` |
| `topHp` | string | Top10 holding % range | `",60"` |
| `insiderHp` | string | Insider holding % range | `",50"` |
| `bundleHp` | string | Bundle holding % range | `",60"` |
| `newWalletHp` | string | New wallet holding % range | `",30"` |
| `progress` | string | Graduation progress % range (NEW/ALMOST only) | `"1,90"` |
| `snipers` | string | Sniper count range | `",5"` |
| `xnameCount` | string | Twitter rename count range | `",3"` |
| `tagHolder` | string | Watched wallet buy count range | `"1,2"` |
| `kol` | string | KOL buy count range | `"1,2"` |
| `dexPay` | int | DexScreener paid, `1` = filter paid only | `1` |
| `oneLink` | int | At least one social link, `1` = enabled | `1` |
| `live` | int | Currently live streaming, `1` = filter live | `1` |

#### DEX Values by Chain

- **SOL**: `pump`, `pumpmayhem`, `bonk`, `heaven`, `believe`, `daosfun`, `launchlab`, `mdbc`, `jupstudio`, `mdbcbags`, `trends`, `moonshotn`, `boop`, `moon`, `time`
- **BSC**: `four`, `four_agent`, `bnonly`, `flap`

#### quoteTokens Values by Chain

- **SOL**: `sol`, `usdc`, `usd1`
- **BSC**: `bnb`, `usdt`, `usdc`, `usd1`, `aster`, `u`

#### Feed Response

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "items": [
      {
        "tokenAddress": "...",
        "symbol": "TOKEN",
        "name": "Token Name",
        "createTime": 1773140232851,
        "dexName": "PUMPFUN",
        "launchPlatform": { "name": "PUMPFUN", "progress": "12.89", "completed": false },
        "holders": 3,
        "priceUSD": 0.000003046,
        "marketCapUSD": 3046.80,
        "devHoldPercent": 12.48,
        "hasLink": false,
        "snipers": 0,
        "quoteToken": "sol"
      }
    ]
  },
  "success": true
}
```

Key response fields: `tokenAddress`, `symbol`, `name`, `createTime`, `dexName`, `launchPlatform` (name/progress/completed), `holders`, `priceUSD`, `marketCapUSD`, `devHoldPercent`, `hasLink`, `snipers`, `volume`, `tradeCount`, `buyCount`, `sellCount`, `topHolderPercent`, `insiderHp`, `bundleHp`

### Token Query
`GET ${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/query?ca={contract_address}&chain={chain}`

Query token details: price, security checks, tax rates, holder distribution, etc.

#### Token Query Parameters

| Param | Required | Type | Valid values | Description |
|-------|----------|------|-------------|-------------|
| `ca` | YES | string | Contract address | Token contract address |
| `chain` | NO | string | `sol` / `eth` / `bsc` / `base` | Default `sol`. All 4 chains supported |

#### Token Query Response

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "chainId": "bsc",
    "tokenAddress": "0x...",
    "baseSymbol": "TOKEN",
    "tradeInfo": {
      "marketCapUsd": 15464629.87,
      "price": 0.01546,
      "holder": 7596,
      "hourTradeNum": 20611,
      "hourTradeVolume": 2564705.05
    },
    "pairInfo": {
      "pairAddress": "0x...",
      "pair": "TOKEN - WBNB",
      "liquidateUsd": 581750.57,
      "createTime": 1772182240000
    },
    "securityInfo": {
      "honeyPot": false,
      "openSource": true,
      "noOwner": true,
      "locked": true
    },
    "taxInfo": { "buy": "0", "sell": "0" },
    "linkInfo": { "tg": "", "x": "", "web": "" },
    "dev": { "address": "0x...", "pct": 0.0 },
    "topHolderPct": 25.14,
    "topHolderList": [
      { "address": "0x...", "balance": 98665702.34, "pct": 9.86 }
    ]
  },
  "success": true
}
```

Response groups:
- **tradeInfo**: marketCapUsd, price, holder, hourTradeNum, hourTradeVolume
- **pairInfo**: pairAddress, pair, liquidateUsd, createTime
- **securityInfo**: honeyPot, openSource, noOwner, locked
- **taxInfo**: buy, sell (percentage strings)
- **dev**: address, pct
- **topHolderPct** and **topHolderList**: top 10 holder distribution

## Execution Rules

1. **Always confirm before trading** -- Ask user to confirm: chain, token address, amount/percentage, buy or sell
2. **Use Bash with curl** to call the API
3. **Poll trade result** -- After swap submission, query trade status up to 3 times with 5s intervals
4. **Show transaction link** -- Always display the block explorer URL with the txId
5. **Never retry** failed swap requests -- show the error to user instead
6. **Chain-wallet validation** -- walletAddress must match the selected chain. A Solana wallet cannot be used for BSC/ETH/Base trades and vice versa. If the user provides a mismatched wallet/chain combination, warn them and ask to correct before proceeding.
7. **Strict parameter validation** -- Before calling the API, validate EVERY field:
   - All required parameters must be present and have legal values
   - `chain` must be one of `sol`/`eth`/`bsc`/`base`
   - `isBuy` must be boolean `true` or `false`
   - `amount` for buy: must be > 0; for sell: must be 1-100
   - `tip` must be provided; SOL chain: 0.001-0.1 (unit: SOL); EVM chains: 0.1-100 (unit: Gwei). **If tip is outside the recommended range, must warn the user about potentially high cost and require explicit confirmation before proceeding**
   - `model` if provided must be 1 or 2
   - `priorityFee` if provided only applies to Solana chain
   - **Do NOT send any field names outside the parameter tables above**
   - If any validation fails, refuse to send the request and ask the user to correct

## Feed Rules

1. **type validation** -- Only accept `NEW`, `ALMOST`, `COMPLETED` (uppercase). Reject any other value.
2. **chain validation** -- Feed only supports `sol` and `bsc`. If user specifies `eth` or `base`, reject and inform them that Feed scanning is only available on Solana and BSC chains.
3. **Single query mode (default)** -- Call the Feed API once, format and display key info for each token: symbol, priceUSD, marketCapUSD, holders, devHoldPercent, launchPlatform (name + progress).
4. **Continuous monitor mode** -- Activate only when user explicitly says "持续监控", "monitor", or "watch":
   - Use a Bash polling loop, calling Feed API every 5 seconds
   - Deduplicate by `tokenAddress` — only display newly appeared tokens
   - Loop limit: 480 seconds (8 minutes). Set Bash timeout to 540000ms
   - After loop ends, use AskUserQuestion to ask: continue monitoring / view token details / buy a token / stop
   - When continuing, preserve the seen `tokenAddress` set to avoid repeats
5. **Filter guidance** -- Before querying, optionally ask user about filter preferences (market cap range, liquidity, holder count, etc.). If not asked, use no filters (return all).
6. **No auto-trading** -- Feed scanning is for observation only. NEVER automatically buy or sell based on scan results.
7. **Error handling** -- See Error Codes table. For data query APIs: `code == 200` with `success == true` means success; `code == 300` is server error (inform user to retry later); `code == 8060/8061` means stop immediately; `code == 8062` means wait 2 seconds and retry.

## Token Query Rules

1. **ca required** -- Contract address (`ca`) must be provided. If missing, ask user for it.
2. **chain validation** -- Supports all 4 chains: `sol`, `eth`, `bsc`, `base`. Default `sol`.
3. **HoneyPot warning** -- If `securityInfo.honeyPot == true`, display a **prominent warning** that this token is a honeypot and trading it is extremely risky.
4. **High tax alert** -- If `taxInfo.buy` or `taxInfo.sell` > 5%, warn user about high tax rates.
5. **Display format** -- Present results in groups: Trade Info → Security Check → Tax Rates → Holder Distribution → Social Links.
6. **Trade follow-up** -- After displaying query results, optionally ask user if they want to buy this token, linking to the Buy Token flow.
7. **Error handling** -- Same as Feed Rules (see Error Codes table).

## Wallet Address Formats

| Chain | Format | Example pattern |
|-------|--------|-----------------|
| SOL | Base58, 32-44 characters | `7xKX...` |
| ETH / BSC / Base | 0x + 40 hex characters | `0x1a2B...` |

## Block Explorer URLs
- SOL: `https://solscan.io/tx/{txId}`
- ETH: `https://etherscan.io/tx/{txId}`
- BSC: `https://bscscan.com/tx/{txId}`
- BASE: `https://basescan.org/tx/{txId}`

## Error Codes

| Code | Meaning | Scope |
|------|---------|-------|
| 200 | Success | Data query APIs (Feed, Token Query) |
| 300 | Server error — inform user to retry later | Data query APIs (Feed, Token Query) |
| 8060 | API Key invalid | All APIs |
| 8061 | API Key disabled | All APIs |
| 8062 | Rate limited | All APIs — data query: retry after 2s; trade: retry after 1s (except swap, see Execution Rules #5) |

## Example curl

```bash
# Buy
curl -s -X POST "${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/swap" \
  -H "Authorization: Bearer $XXYY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chain":"sol","walletAddress":"...","tokenAddress":"...","isBuy":true,"amount":0.1,"tip":0.001}'

# Query Trade
curl -s "${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/trade?txId=..." \
  -H "Authorization: Bearer $XXYY_API_KEY"

# Feed - Scan newly launched tokens on SOL (with filters)
curl -s -X POST "${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/feed/NEW?chain=sol" \
  -H "Authorization: Bearer $XXYY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mc":"10000,500000","holder":"50,","insiderHp":",50"}'

# Token Query
curl -s "${XXYY_API_BASE_URL:-https://www.xxyy.io}/api/trade/open/api/query?ca=TOKEN_ADDRESS&chain=sol" \
  -H "Authorization: Bearer $XXYY_API_KEY"
```
