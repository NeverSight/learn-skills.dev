---
name: calculate-mining-difficulty
description: This skill should be used when the user asks to "calculate mining difficulty", "convert target to difficulty", "analyze block difficulty", "BSV difficulty calculation", or needs to compute difficulty from block headers.
allowed-tools: "Bash(bun:*)"
---

# Calculate Mining Difficulty

Calculate and analyze BSV mining difficulty from targets, bits, and network data.

## When to Use

- Get current network difficulty from WhatsOnChain
- Convert between target and difficulty
- Decode compact bits representation
- Understand expected hash calculations for mining

## Usage

```bash
# Get current network difficulty
bun run skills/calculate-mining-difficulty/scripts/difficulty.ts --current

# Calculate from compact bits (e.g., genesis block)
bun run skills/calculate-mining-difficulty/scripts/difficulty.ts --bits 0x1d00ffff

# Calculate from target hex (64 characters)
bun run skills/calculate-mining-difficulty/scripts/difficulty.ts --target 00000000ffff0000000000000000000000000000000000000000000000000000

# JSON output for scripting
bun run skills/calculate-mining-difficulty/scripts/difficulty.ts --bits 0x1d00ffff --json

# Show help
bun run skills/calculate-mining-difficulty/scripts/difficulty.ts --help
```

## Output

Default output:
```
Mining Difficulty Analysis
==========================
Difficulty: 1
Target: 0x00000000ffff0000000000000000000000000000000000000000000000000000
Bits: 0x1d00ffff
Expected hashes: 4.29e+9
```

JSON output (--json):
```json
{
  "difficulty": 1,
  "target": "00000000ffff0000000000000000000000000000000000000000000000000000",
  "bits": "1d00ffff",
  "expectedHashes": "4.29e+9"
}
```

## Difficulty Math

The script uses the standard Bitcoin difficulty formula:

- **Max target**: `0x00000000FFFF0000000000000000000000000000000000000000000000000000` (difficulty 1)
- **Difficulty**: `max_target / current_target`
- **Compact bits format**: First byte = exponent, next 3 bytes = mantissa
  - `target = mantissa * 2^(8*(exponent-3))`
- **Expected hashes**: `difficulty * 2^32`

## API Integration

Uses [WhatsOnChain API](https://docs.whatsonchain.com) for current network data:
- Chain info endpoint: `GET https://api.whatsonchain.com/v1/bsv/main/chain/info`

## Status

Complete - All functionality implemented and tested.
