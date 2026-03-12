---
name: t2000-withdraw
description: >-
  Withdraw from savings and receive USDC. Use when asked to withdraw from
  savings, access deposited funds, pull money out of savings, or reduce
  yield position. Non-USDC positions are auto-swapped back to USDC.
  For sending to another address, use t2000-send.
license: MIT
metadata:
  author: t2000
  version: "1.3"
  requires: t2000 CLI (npx @t2000/cli init)
---

# t2000: Withdraw from Savings

## Purpose
Withdraw from savings and receive USDC. If savings are held in a
non-USDC stablecoin (due to rebalance), t2000 auto-swaps back to
USDC before returning funds to the checking balance.

## Command
```bash
t2000 withdraw <amount>
t2000 withdraw all

# Examples:
t2000 withdraw 25
t2000 withdraw all
```

You always receive USDC regardless of which stablecoin your savings
are held in internally.

## Fees
- No protocol fee on withdrawals
- Standard DEX fees apply if an auto-swap from non-USDC is needed

## Output
```
✓ Withdrew $XX.XX USDC
  Tx: https://suiscan.xyz/mainnet/tx/0x...
```

## Safety
If there's an active borrow, t2000 checks the health factor before
withdrawing. If the withdrawal would drop HF below 1.5, it throws
`WITHDRAW_WOULD_LIQUIDATE` with a `safeWithdrawAmount`.

## Error handling
- `WITHDRAW_WOULD_LIQUIDATE`: withdrawal would make health factor unsafe. Check `safeWithdrawAmount` in error data.
- `NO_COLLATERAL`: no savings to withdraw
- `INSUFFICIENT_BALANCE`: requested amount exceeds savings balance
