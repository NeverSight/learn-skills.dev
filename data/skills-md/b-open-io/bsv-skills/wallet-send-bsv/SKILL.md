---
name: wallet-send-bsv
description: This skill should be used when the user asks to "send BSV", "transfer satoshis", "create payment transaction", "broadcast transaction", "send from WIF", or needs to build, sign, and broadcast P2PKH transactions using @bsv/sdk.
allowed-tools: "Bash(bun:*)"
---

# Wallet Send BSV

Send BSV transactions using @bsv/sdk with WhatsOnChain API.

## When to Use

- Send BSV to a recipient address
- Create simple payment transactions
- Transfer funds from a WIF private key

## Usage

```bash
bun run skills/wallet-send-bsv/scripts/send.ts <from-wif> <to-address> <amount-satoshis>

# Show help
bun run skills/wallet-send-bsv/scripts/send.ts --help

# Example: Send 1000 satoshis
bun run skills/wallet-send-bsv/scripts/send.ts L1abc... 1BvBMSEY... 1000
```

## Arguments

| Argument | Description |
|----------|-------------|
| `from-wif` | Private key in WIF format (starts with K, L, or 5) |
| `to-address` | Recipient BSV address (starts with 1 or 3) |
| `amount-satoshis` | Amount to send (1 BSV = 100,000,000 satoshis) |

## Dependencies

- `@bsv/sdk` - BSV SDK for key/transaction operations
- WhatsOnChain API - UTXO fetching and broadcast

## Transaction Flow

1. Parse and validate WIF private key
2. Validate recipient address format
3. Derive sender address from private key
4. Fetch UTXOs from WhatsOnChain
5. Build transaction with P2PKH inputs/outputs
6. Calculate fee (1 sat/byte)
7. Sign transaction
8. Broadcast via WhatsOnChain API

## Error Handling

- **Invalid WIF**: Clear error with SDK message
- **Invalid address**: Format validation error
- **Insufficient funds**: Shows balance vs required amount
- **Network errors**: Displays raw tx hex for manual broadcast

## Network

Uses BSV mainnet via WhatsOnChain API:
- UTXOs: `GET /v1/bsv/main/address/{address}/unspent`
- Broadcast: `POST /v1/bsv/main/tx/raw`
