---
name: orbiter-bridge-quote
description: Get a cross-chain quote and optimal route with fees and steps.
---

# Orbiter Bridge Quote

Get a cross-chain quote and optimal route. This is the first step for "one-click" cross-chain onboarding.

## When to Use
- The user wants to send a token from chain A to chain B
- You need fee breakdowns, ETA, or routing selection

## Inputs
- `sourceChainId` (string)
- `destChainId` (string)
- `sourceToken` (string)
- `destToken` (string)
- `amount` (string)
- `userAddress` (string)
- `targetRecipient` (string)
- `slippage` (number, optional)
- `feeConfig` (object, optional)
- `channel` (string, optional)

## Outputs
- `fees`
- `steps` (may include `approve`, `swap`, and `bridge` depending on route)
- `details`

## Recommended Flow
1. `orbiter_chains` (optional)
2. `orbiter_tokens` (optional)
3. `orbiter_bridge_quote`
4. `orbiter_bridge_tx` (optional)
5. Client-side signing
6. `orbiter_tx_simulate`
7. `orbiter_tx_broadcast`
8. `orbiter_transaction`

## Fast Path
- Use `orbiter_bridge_flow` to get `quote + signableTx + approve + simulate` in one call
- Use `orbiter_sign_template` to generate a signable transaction template
- Use `orbiter_sign_broadcast` to sign and broadcast in one step

## CLI Example
```bash
orbiter bridge quote \
  --source-chain 42161 \
  --dest-chain 8453 \
  --source-token 0x0000000000000000000000000000000000000000 \
  --dest-token 0x0000000000000000000000000000000000000000 \
  --amount 300000000000000 \
  --user 0xabc... \
  --recipient 0xabc...
```
