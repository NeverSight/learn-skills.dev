---
name: orbiter-sign-template
description: Generate a signable transaction template with optional RPC enrichment.
---

# Orbiter Sign Template

Generate a signable transaction template (nonce and gas/fee fields can be filled from RPC).

## When to Use
- You want a template suitable for wallet/SDK signing
- You need automatic nonce and gas field population

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
- `rpcUrl` (string, optional)
- `chainId` (string, optional)

## Outputs
- `tx`
- `quote`
- `template` (includes nonce / gas / fee)

## CLI Example
```bash
orbiter bridge sign-template \
  --source-chain 42161 \
  --dest-chain 8453 \
  --source-token 0x0000000000000000000000000000000000000000 \
  --dest-token 0x0000000000000000000000000000000000000000 \
  --amount 300000000000000 \
  --user 0xabc... \
  --recipient 0xabc... \
  --chain 42161
```
