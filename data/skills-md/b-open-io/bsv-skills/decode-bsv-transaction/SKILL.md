---
name: decode-bsv-transaction
description: This skill should be used when the user asks to "decode transaction", "parse tx hex", "transaction details", "analyze transaction", or needs to decode BSV transaction hex into human-readable format.
allowed-tools: "Bash(bun:*)"
---

# Decode BSV Transaction

Decode BSV transaction hex into human-readable format.

## Status

**Complete** - All tests passing

## When to Use

- Decode raw transaction hex
- Analyze transaction structure
- View inputs and outputs
- Inspect scripts and signatures

## Usage

```bash
# Decode transaction by hex
bun run /path/to/skills/decode-bsv-transaction/scripts/decode.ts <tx-hex>

# Decode transaction by txid (fetches from chain)
bun run /path/to/skills/decode-bsv-transaction/scripts/decode.ts <txid>
```

## API Endpoints

JungleBus (primary):
- `GET https://junglebus.gorillapool.io/v1/transaction/get/{txid}`

WhatsOnChain (fallback):
- `GET https://api.whatsonchain.com/v1/bsv/main/tx/{txid}/hex`

## Response

Returns decoded transaction with:
- Version, locktime
- Inputs (previous outputs, scripts, signatures)
- Outputs (value, addresses, scripts)
- Transaction size and fees
