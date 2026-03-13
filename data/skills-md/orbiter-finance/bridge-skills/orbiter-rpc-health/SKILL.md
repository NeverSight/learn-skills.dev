---
name: orbiter-rpc-health
description: Check RPC availability, chain id, and latency.
---

# Orbiter RPC Health

Check RPC availability and whether the chain ID matches.

## When to Use
- You need to validate an RPC endpoint
- You are debugging simulation or broadcast failures

## Inputs
- `rpcUrl` (string, optional)
- `chainId` (string, optional)

## Outputs
- `rpcChainId`
- `clientVersion`
- `latencyMs`

## CLI Example
```bash
orbiter rpc health --chain 42161
```
