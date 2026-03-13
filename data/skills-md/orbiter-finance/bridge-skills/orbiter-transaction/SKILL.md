---
name: orbiter-transaction
description: Query a cross-chain transaction by hash.
---

# Orbiter Transaction

Query cross-chain transaction status and results by transaction hash.

## When to Use
- A transaction has been broadcast and you need to track status
- The user provides a transaction hash

## Inputs
- `hash` (string)

## Outputs
- `status` (2=success, 3=failure)
- `opStatus` (payment flow status code)
- `targetChain` / `targetAmount` / `targetAddress`

## CLI Example
```bash
orbiter transaction --hash 0x...
```
