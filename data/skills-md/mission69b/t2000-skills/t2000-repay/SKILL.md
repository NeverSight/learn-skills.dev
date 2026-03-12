---
name: t2000-repay
description: >-
  Repay outstanding debt. Use when asked to repay a loan, pay back debt,
  reduce outstanding balance, or clear borrows. Supports partial and
  full repayment. User pays with USDC — if debt is in a non-USDC
  stablecoin (from rebalance), USDC is auto-swapped to the borrowed
  asset atomically.
license: MIT
metadata:
  author: t2000
  version: "1.5"
  requires: t2000 CLI (npx @t2000/cli init)
---

# t2000: Repay Borrow

## Purpose
Repay outstanding debt. User always pays with USDC. If savings were
rebalanced into a non-USDC stablecoin (suiUSDT, suiUSDe, USDsui), the
repay auto-swaps USDC to the borrowed asset atomically within the same
transaction. Supports specific amounts or `repay all` to clear the full
balance including accrued interest across all protocols.

## Command
```bash
t2000 repay <amount>
t2000 repay all

# Examples:
t2000 repay 20
t2000 repay all
```

## Fees
- No protocol fee on repayment

## Output
```
✓ Repaid $XX.XX USDC
  Remaining Debt: $XX.XX
  Tx: https://suiscan.xyz/mainnet/tx/0x...
```

## Notes
- `repay all` calculates full outstanding principal + accrued interest across all protocols
- Non-USDC debt (from rebalance) is auto-handled — USDC is swapped to the borrowed asset in the same transaction
- Available USDC balance must cover the repayment amount
