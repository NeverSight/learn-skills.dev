---
name: lookup-block-info
description: This skill should be used when the user asks to "get block info", "lookup block by height", "block by hash", "block header details", or needs to retrieve BSV block information.
allowed-tools: "Bash(bun:*)"
---

# Lookup Block Info

Retrieve detailed block information from the BSV blockchain.

## API

Uses WhatsOnChain for complete block data (size, txcount, difficulty, previousblockhash). JungleBus `/v1/block_header/get/{hash}` only provides header fields - use that directly if you only need hash, height, time, merkleroot.

## When to Use

- Get block data by height
- Get block data by hash
- View block statistics (size, tx count, etc.)

## Usage

```bash
# Lookup by height
bun run skills/lookup-block-info/scripts/lookup.ts --height 800000

# Lookup by hash
bun run skills/lookup-block-info/scripts/lookup.ts --hash 00000000000000000320e...

# JSON output
bun run skills/lookup-block-info/scripts/lookup.ts --height 800000 --json

# Show help
bun run skills/lookup-block-info/scripts/lookup.ts --help
```

## Output

### Default Format
```
Block #1
Hash: 00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048
Time: 2009-01-09 02:54:25 UTC
Size: 215 bytes
Transactions: 1
Merkle Root: 0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
Previous: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
Difficulty: 1
```

### JSON Format (--json)
```json
{
  "height": 1,
  "hash": "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048",
  "time": 1231469665,
  "size": 215,
  "txCount": 1,
  "merkleRoot": "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098",
  "previousHash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
  "difficulty": 1
}
```

## Error Handling

- Invalid height (negative): "Error: Height must be non-negative integer", exit 1
- Invalid hash format: "Error: Hash must be 64 hex characters", exit 1
- Block not found: "Error: Block not found", exit 1
- Network/API error: "Error: API request failed: <reason>", exit 1

## Status

**Complete** - All tests pass
