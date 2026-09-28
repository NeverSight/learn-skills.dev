---
name: pyth-price-feeds
description: >
  Pyth pull price feeds on Hedera. Use when integrating Pyth on Hedera (testnet 296 /
  mainnet 295), fetching Hermes update payloads, paying updatePriceFeeds, calling
  getPriceNoOlderThan, checking confidence, or normalizing signed price + expo to 18 decimals.
---

# Pyth Price Feeds (Hedera)

**Pull pattern:** Pyth is not a fire-and-forget push feed. Fresh reads usually need a Hermes payload submitted on-chain (payable) **before** `getPriceNoOlderThan`.

```text
Hermes → updatePriceFeeds{value: fee}(updateData) → getPriceNoOlderThan(priceId, maxAge)
```

Consumers may wrap Pyth behind a local interface; that is optional. Do not assume a project-specific adapter name.

## Quick Reference

| Piece | Role |
| ----- | ---- |
| Pyth contract | Network `IPyth` address |
| Price ID | `bytes32` feed id (not an aggregator address) |
| Update | Payable `updatePriceFeeds` with Hermes `updateData` |
| Fee | `getUpdateFee(updateData)` — `msg.value` must cover it |
| Read | `getPriceNoOlderThan(priceId, maxAge)` |
| Confidence | Reject when `conf > uint64(price)` |
| Scale | Signed `price` + `expo` → consumer decimals (often 18) |

**Hedera chain IDs:** testnet `296`, mainnet `295`.

See [references/hedera-feeds.md](references/hedera-feeds.md) for where to source the Pyth contract and price IDs. See [references/examples.md](references/examples.md) for update / read / expo sketches.

## Critical: Update Before Fresh Reads

If the on-chain price is older than your staleness bound, fetch Hermes update data and submit it:

```solidity
function updatePrice(bytes[] calldata updateData) external payable {
    uint256 fee = PYTH.getUpdateFee(updateData);
    if (msg.value < fee) revert UpdateFeeTooLow(msg.value, fee);
    PYTH.updatePriceFeeds{ value: msg.value }(updateData);
}
```

Hedera `msg.value` is tinybars via JSON-RPC — attach enough native value for the Pyth fee. Do not treat a stale `getPriceUnsafe` as a valid trading price.

## Critical: Confidence And Signed Expo

After `getPriceNoOlderThan`:

| Check | Why |
| ----- | --- |
| `publishTime != 0` | Incomplete |
| `price > 0` | Invalid / non-positive |
| `conf > uint64(price)` | Confidence wider than the price |
| Normalize `expo` | `expo` is signed; not the same as ERC-20 decimals |

```solidity
PythStructs.Price memory price = PYTH.getPriceNoOlderThan(priceId, maxStaleness);
if (price.publishTime == 0) revert IncompleteRound();
if (price.price <= 0) revert InvalidPrice();
if (price.conf > uint64(price.price)) revert InvalidConfidence();
```

## Checklist

When implementing or reviewing Pyth on Hedera:

- [ ] Pyth contract + price IDs taken from Pyth Hedera / Hermes docs (not Ethereum defaults)
- [ ] Hermes payloads submitted with sufficient `msg.value` before relying on a fresh price
- [ ] Reads use `getPriceNoOlderThan` (or equivalent max-age API), not unbounded unsafe prices for trading
- [ ] Confidence wider than price reverts
- [ ] Signed `expo` normalized to the consumer scale
- [ ] Chain ID is `295` or `296` (or the project’s documented Hedera network)

## References

- [references/examples.md](references/examples.md) — update, read, and expo sketches
- [references/hedera-feeds.md](references/hedera-feeds.md) — where to source Pyth contract and price IDs
- [Pyth Price Feeds](https://docs.pyth.network/price-feeds)
- [Pyth EVM contract addresses](https://docs.pyth.network/price-feeds/core/contract-addresses/evm)
- [Hermes price feeds](https://hermes.pyth.network/v2/price_feeds)
