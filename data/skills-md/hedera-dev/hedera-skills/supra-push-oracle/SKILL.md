---
name: supra-push-oracle
description: >
  Supra S-Value push oracle on Hedera. Use when reading getSvalue price feeds on Hedera
  (testnet 296 / mainnet 295), mapping pair IDs, converting millisecond timestamps to unix
  seconds, or quoting USDT pairs where USD is unavailable.
---

# Supra Push Oracle (Hedera)

**Push S-Value pattern:** Supra updates an on-chain feed; readers call `getSvalue(pairId)` and must reject empty, zero, or stale quotes.

```text
Supra push oracle → getSvalue(pairId) → consumer
```

Consumers may wrap the feed behind a local interface; that is optional. Do not assume a project-specific adapter name.

## Quick Reference

| Piece | Role |
| ----- | ---- |
| Push oracle | Immutable `ISupraSValueFeed` address for the network |
| Pair ID | Numeric Supra pair id (not an EVM aggregator address) |
| Read | `getSvalue(pairId)` → price, decimals, time |
| Time | Often **milliseconds** on Hedera — convert when `time > 1e10` |
| Quote asset | Hedera feeds are often **USDT**, not USD |
| Freshness | Compare unix **seconds** to a max staleness |

**Hedera chain IDs:** testnet `296`, mainnet `295`.

See [references/hedera-feeds.md](references/hedera-feeds.md) for where to source push-oracle addresses and pair IDs. See [references/examples.md](references/examples.md) for read sketches.

## Critical: Millisecond Timestamps

Supra `time` on Hedera is frequently milliseconds. Treat values `> 10_000_000_000` as ms and convert before staleness checks:

```solidity
uint256 updatedAt = pf.time > 10_000_000_000 ? pf.time / 1_000 : pf.time;
if (block.timestamp - updatedAt > maxStaleness) revert StalePrice(updatedAt, maxStaleness);
```

Comparing a millisecond timestamp to `block.timestamp` (seconds) will look “in the future” or skip staleness incorrectly.

## Critical: USDT Pairs On Hedera

Current Hedera Supra feeds often quote **USDT**, not USD. Pair keys / symbols must match the actual quote (`HBAR`/`USDT`, `BTC`/`USDT`). Do not label a USDT feed as USD.

## Completeness And Invalid Prices

Revert when:

| Condition | Why |
| --------- | --- |
| `pf.time == 0` | No successful update |
| `pf.price == 0` | Invalid price |
| Stale after converting to seconds | Older than `maxStaleness` |
| Unknown pair ID | Do not return zero |

Normalize `pf.price` with `pf.decimals` to the consumer scale (often 18).

## Checklist

When implementing or reviewing Supra reads on Hedera:

- [ ] Push-oracle address and pair IDs taken from Supra Hedera docs (not Ethereum)
- [ ] Timestamps converted to unix seconds when they look like milliseconds
- [ ] Pair symbols match the real quote asset (often USDT)
- [ ] Zero / missing updates revert
- [ ] Staleness bound is enforced in seconds
- [ ] Decimals normalized to the consumer scale

## References

- [references/examples.md](references/examples.md) — `getSvalue` and timestamp sketches
- [references/hedera-feeds.md](references/hedera-feeds.md) — where to source push-oracle addresses and pair IDs
- [Supra push oracle networks](https://docs.supra.com/oracles/data-feeds/push-oracle/networks)
- [Supra data feeds index](https://docs.supra.com/oracles/data-feeds/data-feeds-index)
