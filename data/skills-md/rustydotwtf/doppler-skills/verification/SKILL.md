---
name: verification
description: Verify on-chain Doppler behavior with cast, viem, RPC, and explorers for dynamic auctions, multicurve launches, hook initializer state, and migration flows.
metadata:
  author: doppler
  version: "2.0"
---

# Verification

## When to use
- Contract state does not match expected launch/migration behavior
- Rebalances, fee claims, or migration splits need confirmation
- You need deterministic proof from chain data before making changes

## Tool selection
- `cast`: fast reads and direct function checks
- `viem`: precision-safe math and custom scripts
- raw RPC: historical `eth_call` at prior blocks
- explorers/indexer: events, tx traces, and timeline reconstruction

## Core workflow
1. Identify module path:
   - Dynamic (`Doppler`)
   - Multicurve (base/scheduled/decay)
   - Hook-initializer (`DopplerHookInitializer` + hooks)
   - Proceeds split migration (`UniswapV4MigratorSplit`, `TopUpDistributor`)
2. Read primary state directly from source contract.
3. Recompute expected values off-chain (ticks, prices, allocations, proceeds split).
4. Compare against emitted events and token balances.

## High-impact checks
- Auction progression: epochs, proceeds, sold amounts
- Pool status transitions (`Initialized`, `Locked`, `Graduated`, `Exited` where applicable)
- Hook permissions/flags and callback state
- Split recipient payout + top-up pull-up outcomes

## References
- [CAST.md](references/CAST.md)
- [VIEM.md](references/VIEM.md)
- [RPC.md](references/RPC.md)
- [EXPLORERS.md](references/EXPLORERS.md)

## Related skills
- [v4-dynamic-auction](../v4-dynamic-auction/SKILL.md)
- [v4-multicurve-auction](../v4-multicurve-auction/SKILL.md)
- [doppler-hook-initializer](../doppler-hook-initializer/SKILL.md)
- [proceeds-split-migration](../proceeds-split-migration/SKILL.md)
