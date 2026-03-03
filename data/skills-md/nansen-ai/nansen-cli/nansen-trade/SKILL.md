---
name: nansen-trade
description: Execute DEX swaps on Solana or Base. Use when buying or selling a token, getting a swap quote, or executing a trade.
allowed-tools: Bash
---

# Trade

Two-step flow: quote then execute. **Trades are irreversible once on-chain.**

**Prerequisite:** You need a wallet first. Run `nansen wallet create` before trading.

## Quote

```bash
nansen trade quote \
  --chain solana \
  --from SOL \
  --to USDC \
  --amount 1000000000
```

Symbols resolve automatically: `SOL`, `ETH`, `USDC`, `USDT`, `WETH`. Raw addresses also work.

## Execute

```bash
nansen trade execute --quote <quote-id>
```

## Agent pattern

```bash
# Pipe quote ID directly into execute
QUOTE_ID=$(nansen trade quote --chain solana --from SOL --to USDC --amount 1000000000 2>&1 | grep "Quote ID:" | awk '{print $NF}')
nansen trade execute --quote "$QUOTE_ID"
```

## Common Token Addresses

| Token | Chain | Address |
|-------|-------|---------|
| SOL | Solana | `So11111111111111111111111111111111111111112` |
| USDC | Solana | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| ETH | Base | `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` |
| USDC | Base | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

## Amounts are in base units

| Token | Decimals | 1 token = |
|-------|----------|-----------|
| SOL | 9 | `1000000000` |
| ETH | 18 | `1000000000000000000` |
| USDC | 6 | `1000000` |

## Flags

| Flag | Purpose |
|------|---------|
| `--chain` | `solana` or `base` |
| `--from` | Source token (symbol or address) |
| `--to` | Destination token (symbol or address) |
| `--amount` | Amount in base units (integer) |
| `--wallet` | Wallet name (default: default wallet) |
| `--slippage` | Slippage tolerance as decimal (e.g. 0.03) |
| `--quote` | Quote ID for execute |
| `--no-simulate` | Skip pre-broadcast simulation |

## Environment Variables

| Var | Purpose |
|-----|---------|
| `NANSEN_WALLET_PASSWORD` | **Required for `trade execute`.** Wallet encryption password — persisted in `~/.nansen/.env`. Source before executing: `source ~/.nansen/.env && nansen trade execute ...` |
| `NANSEN_API_KEY` | API key (also set via `nansen login`) |

> **Agents:** Never hold a wallet password only in session memory. If `NANSEN_WALLET_PASSWORD` is not in `~/.nansen/.env`, follow the setup flow in the nansen-wallet skill Password Policy to generate and persist one before proceeding.

## Notes

- Quotes expire after ~1 hour. If execute fails, get a fresh quote.
- A wallet is required even for quotes (the API builds sender-specific transactions).
- ERC-20 swaps may require an approval step — execute handles this automatically.
