---
name: estimate-transaction-fee
description: This skill should be used when the user asks to "estimate transaction fee", "calculate BSV fee", "fee per byte", "transaction cost", or needs to estimate fees based on transaction size and current rates.
allowed-tools: "Bash(bun:*)"
---

# Estimate Transaction Fee

Estimate fees for BSV transactions based on size and fee rates.

## When to Use

- Estimate fee before sending a transaction
- Calculate size of a transaction
- Understand fee structure

## Usage

```bash
# Estimate by size
bun run skills/estimate-transaction-fee/scripts/estimate.ts --size 226

# Estimate from raw tx hex
bun run skills/estimate-transaction-fee/scripts/estimate.ts --tx <hex>

# Estimate by inputs/outputs
bun run skills/estimate-transaction-fee/scripts/estimate.ts --inputs 2 --outputs 3

# Custom fee rate
bun run skills/estimate-transaction-fee/scripts/estimate.ts --size 226 --rate 2

# JSON output
bun run skills/estimate-transaction-fee/scripts/estimate.ts --size 226 --json

# Show help
bun run skills/estimate-transaction-fee/scripts/estimate.ts --help
```

## Size Estimation

P2PKH transaction size formula:
- Base overhead: 10 bytes
- Per input: ~148 bytes
- Per output: ~34 bytes

Example: 1 input + 2 outputs = 10 + 148 + 68 = 226 bytes

## Output Examples

Default output:
```
Fee Estimation
==============
Size: 226 bytes
Rate: 1 sat/byte
Fee: 226 satoshis (0.00000226 BSV)
```

With --inputs/--outputs (shows breakdown):
```
Fee Estimation
==============
Size: 226 bytes
Rate: 1 sat/byte
Fee: 226 satoshis (0.00000226 BSV)
Breakdown:
  - Inputs (1): ~148 bytes
  - Outputs (2): ~68 bytes
  - Overhead: ~10 bytes
```

JSON output (--json):
```json
{
  "size": 226,
  "rate": 1,
  "fee": 226,
  "feeBsv": 0.00000226
}
```

## Status

Complete
