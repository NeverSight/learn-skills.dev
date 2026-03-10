---
name: t2000-check-balance
description: >-
  Check the t2000 agent wallet balance on Sui. Use when asked about wallet
  balance, how much USDC is available, savings balance, gas reserve, total
  funds, or portfolio value. Also use before any send or borrow operation
  to confirm sufficient funds exist.
license: MIT
metadata:
  author: t2000
  version: "1.5"
  requires: t2000 CLI (npx @t2000/cli init)
---

# t2000: Check Balance

## Purpose
Fetch the current balance across all accounts: available USDC,
savings (NAVI + Suilend), gas reserve (SUI), and total portfolio value.

## Commands
```bash
t2000 balance                 # human-readable summary
t2000 balance --show-limits   # includes maxWithdraw, maxBorrow, healthFactor
t2000 balance --json          # machine-parseable JSON (works on all commands)
```

## Output (default)
```
Available:  $150.00  (checking — spendable)
Savings:    $2,000.00  (earning 5.10% APY)
Gas:        0.50 SUI    (~$0.50)
──────────────────────────────────────
Total:      $2,150.50
Earning ~$0.27/day
```

## Output (--show-limits)
Appends to the above:
```
Limits:
  Max withdraw:   $XX.XX
  Max borrow:     $XX.XX
  Health factor:  X.XX          (∞ if no active loan)
```

## Notes
- `gasReserve.usdEquiv` is an estimate at current SUI price; it fluctuates
  without any swap occurring
- If balance shows $0.00 available and wallet was just created, fund it first
  via Coinbase Onramp or a direct USDC transfer to the wallet address
- `--json` is a global flag that works on all t2000 commands, not just balance
- Internally, savings may be held in non-USDC stablecoins due to rebalance;
  the balance shows the USDC-equivalent value
