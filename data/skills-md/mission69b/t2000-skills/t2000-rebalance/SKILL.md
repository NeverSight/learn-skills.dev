---
name: t2000-rebalance
description: >-
  Optimize yield by moving savings to the best rate across protocols and
  stablecoins. Use when asked to optimize yield, rebalance, find better
  rates, maximize APY, or improve returns. Supports dry-run preview
  before execution.
license: MIT
metadata:
  author: t2000
  version: "1.4"
  requires: t2000 CLI (npx @t2000/cli init)
---

# t2000: Rebalance (Yield Optimizer)

## Purpose
Automatically find and execute the best yield across NAVI and Suilend.
Internally optimizes across all 4 stablecoins (USDC, suiUSDT, suiUSDe, USDsui)
— the user doesn't need to think about which stablecoin to hold. One
command moves savings from a lower-yielding position to the highest
available rate, handling withdrawals, swaps, and deposits in sequence.

## Command
```bash
t2000 rebalance --dry-run       # preview the plan without executing
t2000 rebalance                 # execute (prompts for confirmation)
t2000 rebalance --yes           # skip confirmation prompt (for agents)

# With custom thresholds:
t2000 rebalance --min-diff 1.0              # only act on 1%+ APY difference
t2000 rebalance --max-break-even 14         # skip if break-even > 14 days
t2000 rebalance --dry-run --json            # machine-readable plan
```

## Workflow
1. Always run `--dry-run` first to see the plan
2. Review the economics (APY gain, swap cost, break-even days)
3. Run without `--dry-run` to execute (or add `--yes` for agents)

## Output (dry-run)
```
Rebalance Plan
──────────────────────────────────────
  From:    USDC on NAVI Protocol (4.21% APY)
  To:      suiUSDT on Suilend (5.40% APY)
  Amount:  $1,000.00

Economics
──────────────────────────────────────
  APY Gain:     +1.19%
  Annual Gain:  $11.90/year
  Swap Cost:    ~$0.30
  Break-even:   9 days

Steps
──────────────────────────────────────
  1. Withdraw $1,000.00 USDC from navi
  2. Swap USDC → suiUSDT (~$999.70)
  3. Deposit $999.70 suiUSDT into suilend

DRY RUN — Preview only, no transactions executed
  Run `t2000 rebalance` to execute.
```

## Output (executed)
```
  ✓ Rebalanced $1,000.00 → 5.40% APY
  Tx:  https://suiscan.xyz/mainnet/tx/0x...
  Gas:  0.0150 SUI
```

## Options
| Flag | Description | Default |
|------|-------------|---------|
| `--dry-run` | Preview without executing | false |
| `--min-diff <pct>` | Minimum APY difference to trigger | 0.5% |
| `--max-break-even <days>` | Max break-even days for cross-asset moves | 30 |
| `--yes` | Skip confirmation prompt | false |
| `--json` | Machine-readable output | false |

## Safety
- Health factor check: refuses to rebalance if HF < 1.5 (active borrows)
- Break-even filter: skips cross-asset moves with break-even > 30 days
- Minimum yield difference: ignores gains below 0.5% by default
- Confirmation prompt before execution (use `--yes` to skip for agents)
- If any step fails, stops and reports state

## When to use
- Periodically (weekly/monthly) to optimize yield
- After rate changes on protocols
- When new stablecoins offer higher yields
- After `t2000 save` to potentially upgrade to a better rate

## Notes
- Same-asset rebalance (e.g., USDC from NAVI → Suilend): no swap needed, zero cost
- Cross-asset rebalance (e.g., USDC → suiUSDT): swap cost factored into break-even
- Multi-stablecoin optimization is handled internally — users save/withdraw in USDC only
- Withdraw always returns USDC (auto-swaps non-USDC positions back)
