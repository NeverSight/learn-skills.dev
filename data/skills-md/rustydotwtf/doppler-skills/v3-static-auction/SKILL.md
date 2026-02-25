---
name: v3-static-auction
description: Reference for Doppler V3 static auctions using `UniswapV3Initializer` or `LockableUniswapV3Initializer`, including parameters, lifecycle, and far-tick exits.
metadata:
  author: doppler
  version: "2.0"
---

> **Source References**: Code citations link to raw GitHub files pinned to commit `46bad16d`.

# V3 Static Auction

## When to use
- Launches use `UniswapV3Initializer` or `LockableUniswapV3Initializer`
- You need fixed-curve V3 behavior (no epoch rebalance)
- You are debugging far-tick exit gating or beneficiary fee collection in lockable pools

## Prerequisites
- Choose supported V3 fee tier and corresponding tick spacing
- Confirm tick bounds and token ordering implications

## Core workflow
1. Validate `InitData` (ticks, fee, position count, sale share).
2. Initialize positions once through Airlock.
3. Track auction progression passively via market swaps.
4. Exit when far tick is reached (`exitLiquidity`) for migrable pools.
5. For lockable path, use beneficiary fee collection instead of migration exits.

## Quick facts
| Item | Detail |
|---|---|
| Contracts | `src/initializers/UniswapV3Initializer.sol`, `src/initializers/LockableUniswapV3Initializer.sol` |
| Rebalancing | None |
| Exit requirement | Price reaches far tick |
| Lockable add-ons | Beneficiaries, pool status gating, fee collection |

## Failure modes
- Tick bounds not aligned with spacing
- Misinterpreting far-tick direction due to token ordering
- Treating lockable pools as migrable
- Incorrect beneficiary share configuration

## References
- [PARAMETERS.md](references/PARAMETERS.md)
- [FLOW.md](references/FLOW.md)
- [FORMULAS.md](references/FORMULAS.md)
- [GOTCHAS.md](references/GOTCHAS.md)

## Related skills
- [token-lifecycle](../token-lifecycle/SKILL.md)
- [fee-architecture](../fee-architecture/SKILL.md)
- [verification](../verification/SKILL.md)
