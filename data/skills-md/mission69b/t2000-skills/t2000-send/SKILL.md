---
name: t2000-send
description: >-
  Send USDC from the t2000 agent wallet to another address on Sui. Use when
  asked to pay someone, transfer funds, send money, tip a creator, or make a
  payment to a specific Sui address. Do NOT use for API payments — use
  t2000-pay for x402-protected services.
license: MIT
metadata:
  author: t2000
  version: "1.2"
  requires: t2000 CLI (npx @t2000/cli init)
---

# t2000: Send USDC

## Purpose
Transfer USDC from the agent's available balance to any Sui address. Gas is
self-funded from the agent's SUI reserve (auto-topped up if needed).

## Command
```bash
t2000 send <amount> <asset> to <address_or_contact>
t2000 send <amount> <asset> <address_or_contact>

# Examples:
t2000 send 10 USDC to 0x8b3e...d412
t2000 send 50 USDC to Tom
t2000 send 50 USDC 0xabcd...1234
```

The `to` keyword is optional. The recipient can be a Sui address (0x...) or a
saved contact name (e.g. "Tom"). Use `t2000 contacts` to list saved contacts.

## Pre-flight checks (automatic)
1. Sufficient available USDC balance
2. SUI gas reserve present; if not, auto-topup triggers transparently

## Output
```
✓ Sent $XX.XX USDC → 0x8b3e...d412
  Gas: X.XXXX SUI (self-funded)
  Balance: $XX.XX USDC
  Tx: https://suiscan.xyz/mainnet/tx/0x...
```

## Error handling
- `INSUFFICIENT_BALANCE`: available balance is less than the requested amount
- `INVALID_ADDRESS`: destination is not a valid Sui address
- `CONTACT_NOT_FOUND`: name is not a saved contact or valid address
- `SIMULATION_FAILED`: transaction would fail on-chain; details in error message
