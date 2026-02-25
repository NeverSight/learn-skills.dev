---
name: lookup-bsv-address
description: This skill should be used when the user asks to "lookup address", "check address balance", "address UTXOs", "address history", or needs to retrieve BSV address information from WhatsOnChain API.
allowed-tools: "Bash(bun:*)"
---

# Lookup BSV Address

Look up BSV address information using WhatsOnChain API.

## Status

**Complete** - All tests passing

## When to Use

- Check address balance
- View transaction history
- List unspent outputs (UTXOs)
- Verify address activity

## Usage

```bash
# Get address info
bun run /path/to/skills/lookup-bsv-address/scripts/lookup.ts <address>

# Get address balance only
bun run /path/to/skills/lookup-bsv-address/scripts/lookup.ts <address> balance

# Get transaction history
bun run /path/to/skills/lookup-bsv-address/scripts/lookup.ts <address> history

# Get UTXOs
bun run /path/to/skills/lookup-bsv-address/scripts/lookup.ts <address> utxos
```

## API Endpoints

WhatsOnChain Address API:
- Balance: `GET /v1/bsv/main/address/{address}/balance`
- History: `GET /v1/bsv/main/address/{address}/history`
- UTXOs: `GET /v1/bsv/main/address/{address}/unspent`
