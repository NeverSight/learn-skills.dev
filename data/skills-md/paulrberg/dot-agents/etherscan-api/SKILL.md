---
name: etherscan-api
description: This skill should be used when the user asks to "check ETH balance", "query ERC-20 balance", "get wallet balance", "check token holdings", "query Etherscan", or mentions Etherscan API, blockchain balance queries, or multi-chain balance lookups.
---

# Etherscan API V2

## Overview

Query blockchain balances using Etherscan's unified API V2. This skill covers:

- Native ETH balance queries
- ERC-20 token balance queries
- Multi-chain support via the `chainid` parameter

**Scope:** This skill focuses on balance queries for free-tier accounts. For other Etherscan API features, consult the fallback documentation.

## Prerequisites

### API Key Validation

Before making any API call, verify the `ETHERSCAN_API_KEY` environment variable is set:

```bash
if [ -z "$ETHERSCAN_API_KEY" ]; then
  echo "Error: ETHERSCAN_API_KEY environment variable is not set."
  echo "Get a free API key at: https://etherscan.io/myapikey"
  exit 1
fi
```

If the environment variable is missing, inform the user and halt execution.

## Chain Inference

Do not default to Ethereum Mainnet. Always infer the chain from the user's prompt before making any API call.

### Inference Rules

1. **Explicit chain mention** — If the user mentions a chain name (e.g., "on Polygon", "Arbitrum balance", "Base chain"), use that chain.
2. **Chain-specific tokens** — Some tokens exist primarily on specific chains:
   - POL → Polygon (137)
   - ARB → Arbitrum One (42161)
   - OP → OP Mainnet (10)
   - AVAX → Avalanche C-Chain (43114)
   - BNB → BNB Smart Chain (56)
   - SONIC → Sonic (146)
   - SEI → Sei (1329)
   - MON → Monad (143)
3. **Contract address patterns** — If the user provides a contract address, consider asking which chain it's deployed on (many contracts exist on multiple chains).
4. **Testnet keywords** — Words like "testnet", "Sepolia", "Holesky", "Amoy" indicate testnet chains.
5. **Ambiguous cases** — If the chain cannot be inferred, **ask the user** before proceeding. Do not assume Ethereum Mainnet.

### Unsupported Chains

If the user references a chain not supported by Etherscan (e.g., Solana, Bitcoin), inform them:

```
The chain "[chain name]" is not supported by Etherscan API V2.

Etherscan supports EVM-compatible chains only. For the full list, see:
https://docs.etherscan.io/etherscan-v2/getting-started/supported-chains
```

For the complete list of supported chains and their IDs, see `./references/chains.md`.

## API Base URL

All requests use the unified V2 endpoint:

```
https://api.etherscan.io/v2/api
```

The `chainid` parameter determines which blockchain to query.

## ETH Balance Query

Query native ETH (or native token) balance for an address.

### Endpoint Parameters

| Parameter | Required | Default  | Description                                          |
| --------- | -------- | -------- | ---------------------------------------------------- |
| `chainid` | No       | `1`      | Chain ID (see chains.md)                             |
| `module`  | Yes      | -        | Set to `account`                                     |
| `action`  | Yes      | -        | Set to `balance`                                     |
| `address` | Yes      | -        | Wallet address (supports up to 20 comma-separated)   |
| `tag`     | No       | `latest` | Block tag (`latest`, `pending`, or hex block number) |
| `apikey`  | Yes      | -        | API key from `$ETHERSCAN_API_KEY`                    |

### Single Address Query

```bash
curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe&tag=latest&apikey=$ETHERSCAN_API_KEY"
```

### Multi-Address Query (up to 20)

```bash
curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=balancemulti&address=0xaddress1,0xaddress2,0xaddress3&tag=latest&apikey=$ETHERSCAN_API_KEY"
```

### Response Format

**Single address:**

```json
{
  "status": "1",
  "message": "OK",
  "result": "172774397764084972158218"
}
```

**Multi-address:**

```json
{
  "status": "1",
  "message": "OK",
  "result": [
    {"account": "0xaddress1", "balance": "1000000000000000000"},
    {"account": "0xaddress2", "balance": "2500000000000000000"}
  ]
}
```

## ERC-20 Token Balance Query

Query ERC-20 token balance for an address.

### Endpoint Parameters

| Parameter         | Required | Default  | Description                       |
| ----------------- | -------- | -------- | --------------------------------- |
| `chainid`         | No       | `1`      | Chain ID (see chains.md)          |
| `module`          | Yes      | -        | Set to `account`                  |
| `action`          | Yes      | -        | Set to `tokenbalance`             |
| `contractaddress` | Yes      | -        | ERC-20 token contract address     |
| `address`         | Yes      | -        | Wallet address to query           |
| `tag`             | No       | `latest` | Block tag                         |
| `apikey`          | Yes      | -        | API key from `$ETHERSCAN_API_KEY` |

### Example Query

```bash
curl -s "https://api.etherscan.io/v2/api?chainid=1&module=account&action=tokenbalance&contractaddress=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&address=0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe&tag=latest&apikey=$ETHERSCAN_API_KEY"
```

### Response Format

```json
{
  "status": "1",
  "message": "OK",
  "result": "135499000000"
}
```

## Multi-Chain Usage

Specify the `chainid` parameter to query different blockchains.

### Common Chain IDs (Free Tier)

| Chain        | Chain ID |
| ------------ | -------- |
| Ethereum     | `1`      |
| Polygon      | `137`    |
| Arbitrum One | `42161`  |
| Linea        | `59144`  |
| Scroll       | `534352` |
| zkSync       | `324`    |

### Example: Polygon Query

```bash
curl -s "https://api.etherscan.io/v2/api?chainid=137&module=account&action=balance&address=0x...&tag=latest&apikey=$ETHERSCAN_API_KEY"
```

For the complete list of supported chains, see `./references/chains.md`.

## Wei to Human-Readable Conversion

API responses return balances in the smallest unit (wei for ETH, smallest decimals for tokens).

### ETH Conversion

Divide by 10^18:

```bash
# Using bc for precision
echo "scale=18; 172774397764084972158218 / 1000000000000000000" | bc
# Result: 172774.397764084972158218
```

### ERC-20 Conversion

Divide by 10^decimals (typically 18, but varies per token):

| Token       | Decimals |
| ----------- | -------- |
| Most tokens | 18       |
| USDC, USDT  | 6        |
| WBTC        | 8        |

```bash
# USDC example (6 decimals)
echo "scale=6; 135499000000 / 1000000" | bc
# Result: 135499.000000
```

## Output Formatting

**Default behavior:** Present results in a Markdown table:

```markdown
| Address | Balance (ETH) | Chain |
|---------|---------------|-------|
| 0xde0B...7BAe | 172,774.40 | Ethereum |
| 0xabc1...2def | 50.25 | Polygon |
```

**User preference:** If the user requests a specific format (JSON, CSV, plain text, etc.), use that format instead. Do not generate a Markdown table when the user specifies an alternative output format.

## Free Tier Limitations

The following chains require a paid Etherscan plan and are **not available** on free tier:

- Base (`8453`)
- OP Mainnet (`10`)
- Avalanche C-Chain (`43114`)
- BNB Smart Chain (`56`)

If a user requests a query on these chains, inform them that a paid plan is required.

## Error Handling

### Common Error Responses

| Status | Message                  | Cause                           |
| ------ | ------------------------ | ------------------------------- |
| `0`    | `NOTOK`                  | Invalid API key or rate limited |
| `0`    | `Invalid address format` | Malformed address               |
| `0`    | `No transactions found`  | Address has no activity         |

### Rate Limits (Free Tier)

- 5 calls/second
- 100,000 calls/day

If rate limited, wait briefly and retry.

## Reference Files

- **`./references/chains.md`** - Complete list of supported chains with chain IDs

## Fallback Documentation

For use cases not covered by this skill (transaction history, contract verification, gas estimates, etc.), fetch the AI-friendly documentation:

```
https://docs.etherscan.io/llms.txt
```

Use `WebFetch` to retrieve this documentation for extended API capabilities.
