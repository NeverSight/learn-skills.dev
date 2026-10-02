---
name: pyth-evm
description: "Pyth pull oracle integration for EVM chains. Covers price feed updates, Hermes API, confidence intervals, sponsored feeds, Express Relay for MEV-protected liquidations, and Solidity/TypeScript patterns."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Oracles
tags:
  - pyth
  - oracle
  - price-feeds
  - pull-oracle
  - hermes
  - express-relay
  - defi
  - evm
  - solidity
  - confidence-interval
---

# Pyth EVM

Pyth Network is a pull-based oracle that delivers high-frequency price data to EVM chains. Unlike push oracles (Chainlink) where oracle nodes update on-chain prices on a schedule, Pyth publishes prices off-chain via Hermes and consumers submit price updates on-chain when they need fresh data. This enables sub-second update latency, lower oracle costs, and prices across 500+ feeds on 70+ chains.

## What You Probably Got Wrong

- **Price updates can be front-run -- ALWAYS combine `updatePriceFeeds` + price consumption in a SINGLE transaction.** If you expose `updatePriceFeeds` as a standalone public function, an attacker can sandwich your price update: observe the pending update, trade before it lands, then trade after. The ONLY safe pattern is a single function that accepts `bytes[] calldata pythUpdateData`, calls `updatePriceFeeds`, and immediately reads the price. Never separate update from read.

- **Confidence interval matters -- wide confidence = unreliable price.** Every Pyth price includes a confidence interval (1 standard deviation). A BTC price of $67,890 with confidence $680 means the true price is between $67,210 and $68,570 with ~68% probability. Reject prices where `conf > price * 0.01` (1%) for lending protocols, or your protocol becomes exploitable during high-volatility events.

- **Update fee is dynamic -- do NOT hardcode `msg.value`.** The fee depends on the number of price updates in the `updateData`. Always call `pyth.getUpdateFee(updateData)` first and pass the exact amount as `msg.value`. Hardcoding `1 wei` will revert when the fee changes.

- **`getPriceUnsafe()` returns arbitrarily stale data.** It is only safe to call immediately after `updatePriceFeeds` in the same transaction. In any other context, use `getPriceNoOlderThan(priceFeedId, maxAge)` which reverts if the price is too old.

- **Pyth uses a PULL model -- prices are NOT already on-chain.** You must fetch price update data from Hermes (off-chain) and submit it on-chain. This is the opposite of Chainlink where oracles push updates on a heartbeat schedule. If your contract tries to read a Pyth price without first calling `updatePriceFeeds`, you get stale or nonexistent data.

- **Price feed IDs are `bytes32`, NOT contract addresses.** Each feed has a unique `bytes32` identifier that is the SAME across all chains. Feed `0xff61491a...` is always ETH/USD whether you are on Ethereum, Arbitrum, or Base. The Pyth contract address varies by chain, but feed IDs do not.

- **Pyth contract addresses VARY by chain.** Ethereum and Avalanche use `0x4305FB66699C3B2702D4d05CF36551390A4c69C6`. Arbitrum, Optimism, and Polygon use `0xff1a0f4744e8582DF1aE09D5611b887B6a12925C`. BNB Chain uses `0x4D7E825f80bDf85e913E0DD2A2D54927e9dE1594`. Always look up the correct address for your target chain.

- **Must call `updatePriceFeeds` BEFORE reading.** If no update has been submitted recently, `getPrice` reverts with `StalePrice` (error selector `0x19abf40e`). The update and read must happen in the same transaction for safety.

- **Update fee is paid in native gas token (~1 wei per feed).** The fee itself is negligible. The real cost is gas: ~120K gas for a single feed update, ~150K for two feeds.

- **Price exponents are NEGATIVE.** Pyth returns `int64 price` and `int32 expo` where `expo` is typically `-8`. A price of `6789000000000` with `expo = -8` means `6789000000000 * 10^(-8) = $67,890.00`. Always apply the exponent correctly.

- **Sponsored feeds may eliminate the need for `updatePriceFeeds`.** On chains with Pyth-sponsored feeds (Arbitrum, Base, Ethereum mainnet), prices are pushed by sponsored updaters. Check freshness with `getPriceNoOlderThan` first -- if fresh enough, skip the update and save gas.

## Pull Oracle Model

Pyth's pull model inverts the traditional oracle design. Instead of oracle nodes pushing prices on-chain at fixed intervals (Chainlink's heartbeat model), Pyth publishes all prices to an off-chain service (Hermes) and consumers pull updates on-demand.

```
Chainlink (Push):  Data Sources -> Oracle Network -> On-chain Contract -> Your Contract reads
Pyth (Pull):       Data Sources -> Pyth Network -> Hermes (off-chain) -> Your dApp fetches -> Your Contract updates + reads
```

### Decision Matrix

| Use Case | Recommended | Why |
|----------|-------------|-----|
| DeFi lending/borrowing | Pyth or Chainlink | Pyth for cost + freshness, Chainlink for ecosystem trust |
| DEX / perpetuals | Pyth | Sub-second latency, confidence intervals for spread calculation |
| Stablecoin peg monitoring | Chainlink | Push model ensures continuous monitoring without user action |
| Cross-chain pricing | Pyth | Same feed IDs on all chains, Hermes serves globally |
| NFT floor price | Neither | Specialized NFT oracles needed (Reservoir, custom TWAP) |
| Low-frequency reads (< 1/hr) | Chainlink | Push model avoids needing transaction infrastructure |
| High-frequency reads (> 1/min) | Pyth | Pull model lets you update only when needed, saves gas |

## IPyth Interface

The core interface for interacting with Pyth on EVM chains.

```solidity
// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.24;

interface IPyth {
    /// @notice Update price feeds with the given update data.
    /// @dev Reverts if msg.value < getUpdateFee(updateData)
    function updatePriceFeeds(bytes[] calldata updateData) external payable;

    /// @notice Get the current price for a feed. Reverts if price is stale.
    function getPrice(bytes32 id) external view returns (PythStructs.Price memory);

    /// @notice Get the price without staleness check. DANGEROUS outside of atomic update+read.
    function getPriceUnsafe(bytes32 id) external view returns (PythStructs.Price memory);

    /// @notice Get price only if updated within maxAge seconds. Reverts otherwise.
    function getPriceNoOlderThan(bytes32 id, uint256 maxAge)
        external view returns (PythStructs.Price memory);

    /// @notice Get the EMA (exponential moving average) price.
    function getEmaPriceNoOlderThan(bytes32 id, uint256 maxAge)
        external view returns (PythStructs.Price memory);

    /// @notice Parse price feed updates and return the results. Useful for historical/benchmark data.
    /// @dev Requires msg.value >= getUpdateFee(updateData)
    function parsePriceFeedUpdates(
        bytes[] calldata updateData,
        bytes32[] calldata priceIds,
        uint64 minPublishTime,
        uint64 maxPublishTime
    ) external payable returns (PythStructs.PriceFeed[] memory);

    /// @notice Calculate the fee required to update the given price data.
    function getUpdateFee(bytes[] calldata updateData) external view returns (uint256);
}
```

## PythStructs

```solidity
library PythStructs {
    struct Price {
        int64 price;        // Price value (apply expo to get human-readable)
        uint64 conf;        // Confidence interval (1 standard deviation)
        int32 expo;         // Price exponent (typically -8)
        uint256 publishTime; // Unix timestamp of price publication
    }

    struct PriceFeed {
        bytes32 id;
        Price price;
        Price emaPrice;
    }
}
```

### Interpreting Price Data

| Field | Example | Meaning |
|-------|---------|---------|
| `price = 6789000000000` | -- | Raw price value |
| `expo = -8` | -- | Multiply price by 10^expo |
| Result | `6789000000000 * 10^(-8)` | `$67,890.00` |
| `conf = 68000000` | -- | Confidence: `68000000 * 10^(-8) = $0.68` |

## Hermes API

Hermes is Pyth's off-chain price service. Your frontend or backend fetches price update data from Hermes and submits it on-chain.

**Base URL:** `https://hermes.pyth.network`

### Get Latest Price Update

```
GET /v2/updates/price/latest?ids[]={feed_id_1}&ids[]={feed_id_2}&encoding=hex&parsed=true
```

Response includes `binary.data` -- an array of hex-encoded update data bytes to pass to `updatePriceFeeds`.

### SSE Streaming

```
GET /v2/updates/price/stream?ids[]={feed_id}&encoding=hex&parsed=true
```

Returns a Server-Sent Events stream with real-time price updates. Useful for frontends that need to display live prices before submitting transactions.

### TypeScript Client

```typescript
import { HermesClient } from "@pythnetwork/hermes-client";

const hermes = new HermesClient("https://hermes.pyth.network");

const ETH_USD = "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace";

const priceUpdates = await hermes.getLatestPriceUpdates([ETH_USD]);

// Binary data to submit on-chain
const updateData = priceUpdates.binary.data.map(
  (hex: string) => `0x${hex}` as `0x${string}`
);

// Parsed price for display
const parsed = priceUpdates.parsed?.[0];
if (parsed) {
  const price = Number(parsed.price.price) * Math.pow(10, parsed.price.expo);
  console.log(`ETH/USD: $${price.toFixed(2)}`);
}
```

## Price Feed IDs

Feed IDs are `bytes32` identifiers, consistent across ALL EVM chains.

> **Last verified:** March 2026

| Pair | Feed ID |
|------|---------|
| BTC/USD | `0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43` |
| ETH/USD | `0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace` |
| SOL/USD | `0xef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d` |
| USDC/USD | `0xeaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a` |
| USDT/USD | `0x2b89b9dc8fdf9f34709a5b106b472f0f39bb6ca9ce04b0fd7f2e971688e2e53b` |
| ARB/USD | `0x3fa4252848f9f0a1480be62745a4629d9eb1322aebab8a791e344b3b9c1adcf5` |
| MATIC/USD | `0x5de33440f6c868ee8c5fc9463ee6f6deca96e7bf3bd3e8c3e6b3b6e73e8b3b6e` |

Full feed list: https://pyth.network/developers/price-feed-ids

## Confidence Intervals

Every Pyth price includes a confidence value representing 1 standard deviation. This quantifies price uncertainty -- wider confidence means less reliable pricing.

### Validation Pattern

```solidity
/// @notice Reject prices with confidence wider than maxConfRatio basis points
/// @dev 100 basis points = 1%. For lending, use 100 (1%). For perps, 50 (0.5%).
function _validateConfidence(
    PythStructs.Price memory pythPrice,
    uint256 maxConfRatioBps
) internal pure {
    // conf and price share the same exponent, so ratio is dimensionless
    uint256 absPrice = pythPrice.price < 0
        ? uint256(uint64(-pythPrice.price))
        : uint256(uint64(pythPrice.price));
    if (absPrice == 0) revert ZeroPrice();
    // Confidence ratio: (conf * 10000) / |price| must be <= maxConfRatioBps
    if ((uint256(pythPrice.conf) * 10_000) / absPrice > maxConfRatioBps) {
        revert ConfidenceTooWide();
    }
}

error ZeroPrice();
error ConfidenceTooWide();
```

## Solidity Integration Patterns

### Safe Price Consumer (Anti-Sandwich)

This is the ONLY correct pattern. Update and read happen in a single function call. Never expose `updatePriceFeeds` as a standalone public function.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@pythnetwork/pyth-sdk-solidity/IPyth.sol";
import "@pythnetwork/pyth-sdk-solidity/PythStructs.sol";

contract PythPriceConsumer {
    IPyth public immutable pyth;
    bytes32 public immutable priceFeedId;

    /// @dev 1% max confidence ratio for price validity
    uint256 private constant MAX_CONF_RATIO_BPS = 100;
    uint256 private constant MAX_PRICE_AGE_SECONDS = 60;

    error StalePrice();
    error NegativePrice();
    error ConfidenceTooWide();

    constructor(address _pyth, bytes32 _priceFeedId) {
        pyth = IPyth(_pyth);
        priceFeedId = _priceFeedId;
    }

    /// @notice Update price and return validated result in single atomic call
    /// @param pythUpdateData Price update bytes from Hermes API
    /// @return price The validated price (apply expo for human-readable)
    /// @return expo The price exponent
    /// @return publishTime The timestamp of the price
    function updateAndGetPrice(bytes[] calldata pythUpdateData)
        external
        payable
        returns (int64 price, int32 expo, uint256 publishTime)
    {
        uint256 updateFee = pyth.getUpdateFee(pythUpdateData);
        pyth.updatePriceFeeds{value: updateFee}(pythUpdateData);

        PythStructs.Price memory pythPrice = pyth.getPriceNoOlderThan(
            priceFeedId,
            MAX_PRICE_AGE_SECONDS
        );

        if (pythPrice.price <= 0) revert NegativePrice();
        _validateConfidence(pythPrice);

        return (pythPrice.price, pythPrice.expo, pythPrice.publishTime);
    }

    function _validateConfidence(PythStructs.Price memory pythPrice) internal pure {
        uint256 absPrice = uint256(uint64(pythPrice.price));
        if ((uint256(pythPrice.conf) * 10_000) / absPrice > MAX_CONF_RATIO_BPS) {
            revert ConfidenceTooWide();
        }
    }
}
```

## TypeScript Integration

### Dependencies

```bash
npm install @pythnetwork/hermes-client@^3.1.0 viem
```

### Fetch and Submit Price Update

```typescript
import { HermesClient } from "@pythnetwork/hermes-client";
import {
  createPublicClient,
  createWalletClient,
  http,
  parseAbi,
  type Address,
} from "viem";
import { arbitrum } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const PYTH_ABI = parseAbi([
  "function updatePriceFeeds(bytes[] calldata updateData) external payable",
  "function getUpdateFee(bytes[] calldata updateData) external view returns (uint256)",
  "function getPriceNoOlderThan(bytes32 id, uint256 age) external view returns (tuple(int64 price, uint64 conf, int32 expo, uint256 publishTime))",
]);

const ETH_USD_FEED = "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace" as `0x${string}`;
const PYTH_ADDRESS = "0xff1a0f4744e8582DF1aE09D5611b887B6a12925C" as Address;

const hermes = new HermesClient("https://hermes.pyth.network");

const publicClient = createPublicClient({
  chain: arbitrum,
  transport: http(process.env.RPC_URL),
});

const walletClient = createWalletClient({
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
  chain: arbitrum,
  transport: http(process.env.RPC_URL),
});

async function updateAndReadPrice(): Promise<{
  price: number;
  confidence: number;
}> {
  const priceUpdates = await hermes.getLatestPriceUpdates([ETH_USD_FEED]);

  const updateData = priceUpdates.binary.data.map(
    (hex: string) => `0x${hex}` as `0x${string}`
  );

  const updateFee = await publicClient.readContract({
    address: PYTH_ADDRESS,
    abi: PYTH_ABI,
    functionName: "getUpdateFee",
    args: [updateData],
  });

  const hash = await walletClient.writeContract({
    address: PYTH_ADDRESS,
    abi: PYTH_ABI,
    functionName: "updatePriceFeeds",
    args: [updateData],
    value: updateFee,
  });

  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status === "reverted") {
    throw new Error("Price update transaction reverted");
  }

  const pythPrice = await publicClient.readContract({
    address: PYTH_ADDRESS,
    abi: PYTH_ABI,
    functionName: "getPriceNoOlderThan",
    args: [ETH_USD_FEED, 60n],
  });

  const price = Number(pythPrice.price) * Math.pow(10, pythPrice.expo);
  const confidence = Number(pythPrice.conf) * Math.pow(10, pythPrice.expo);

  return { price, confidence };
}
```

## Contract Addresses

> **Last verified:** March 2026. Addresses differ per chain -- always verify before deployment.

| Chain | Pyth Contract Address |
|-------|-----------------------|
| Ethereum | `0x4305FB66699C3B2702D4d05CF36551390A4c69C6` |
| Arbitrum | `0xff1a0f4744e8582DF1aE09D5611b887B6a12925C` |
| Optimism | `0xff1a0f4744e8582DF1aE09D5611b887B6a12925C` |
| Base | `0xff1a0f4744e8582DF1aE09D5611b887B6a12925C` |
| Polygon | `0xff1a0f4744e8582DF1aE09D5611b887B6a12925C` |
| Avalanche | `0x4305FB66699C3B2702D4d05CF36551390A4c69C6` |
| BNB Chain | `0x4D7E825f80bDf85e913E0DD2A2D54927e9dE1594` |
| Gnosis | `0x2880aB155794e7179c9eE2e38200202908C17B43` |
| Fantom | `0xff1a0f4744e8582DF1aE09D5611b887B6a12925C` |

```bash
# Verify Pyth deployment on any chain
cast code 0xff1a0f4744e8582DF1aE09D5611b887B6a12925C --rpc-url $RPC_URL
```

## Gas Costs

> **Last verified:** March 2026

| Operation | Gas (approx) | Notes |
|-----------|-------------|-------|
| `updatePriceFeeds` (1 feed) | ~120,000 | First update in a block costs more |
| `updatePriceFeeds` (2 feeds) | ~150,000 | Marginal cost per additional feed ~30K |
| `updatePriceFeeds` (5 feeds) | ~240,000 | Batch updates are efficient |
| `getPriceUnsafe` (read) | ~2,500 | View call, no state change |
| `getPriceNoOlderThan` (read) | ~3,000 | View call with staleness check |
| `parsePriceFeedUpdates` (1 feed) | ~130,000 | Slightly more than updatePriceFeeds |

## Sponsored Feeds

On select chains, Pyth sponsors price feed updates through dedicated updater services. These chains have reasonably fresh prices available without users needing to call `updatePriceFeeds`.

### Chains with Sponsored Feeds

- **Ethereum mainnet** -- major pairs (BTC, ETH, stablecoins)
- **Arbitrum** -- broad feed coverage
- **Base** -- major pairs

### Using Sponsored Feeds

```solidity
function getPriceWithFallback(bytes[] calldata pythUpdateData)
    external payable returns (int64 price, int32 expo)
{
    // Attempt to read sponsored (already-fresh) price
    try pyth.getPriceNoOlderThan(priceFeedId, 60) returns (
        PythStructs.Price memory freshPrice
    ) {
        if (freshPrice.price <= 0) revert NegativePrice();
        return (freshPrice.price, freshPrice.expo);
    } catch {
        // Fall back to user-submitted update
        uint256 fee = pyth.getUpdateFee(pythUpdateData);
        pyth.updatePriceFeeds{value: fee}(pythUpdateData);

        PythStructs.Price memory updatedPrice = pyth.getPriceNoOlderThan(
            priceFeedId, 60
        );
        if (updatedPrice.price <= 0) revert NegativePrice();
        return (updatedPrice.price, updatedPrice.expo);
    }
}
```

## Benchmarks

Pyth supports historical price queries via `parsePriceFeedUpdates`. This is useful for settlement, TWAP calculations, and dispute resolution.

```solidity
function getHistoricalPrice(
    bytes[] calldata updateData,
    bytes32 feedId,
    uint64 targetTimestamp
) external payable returns (PythStructs.Price memory) {
    bytes32[] memory ids = new bytes32[](1);
    ids[0] = feedId;

    uint256 fee = pyth.getUpdateFee(updateData);

    // Window: targetTimestamp +/- 30 seconds
    PythStructs.PriceFeed[] memory feeds = pyth.parsePriceFeedUpdates{value: fee}(
        updateData,
        ids,
        targetTimestamp - 30,
        targetTimestamp + 30
    );

    return feeds[0].price;
}
```

### Fetching Historical Data from Hermes

```
GET /v2/updates/price/{publishTime}?ids[]={feed_id}&encoding=hex&parsed=true
```

The `publishTime` parameter is a Unix timestamp. Hermes returns the closest price update to that timestamp.

## Express Relay

Express Relay is Pyth's MEV protection layer for DeFi liquidations. Instead of exposing liquidation opportunities to the public mempool (where MEV bots extract value via sandwich attacks and priority gas auctions), Express Relay routes liquidation opportunities through a sealed-bid auction.

### How It Works

1. Protocol registers liquidation conditions with Express Relay
2. When a position becomes liquidatable, Express Relay runs a sealed-bid auction among searchers
3. Winning searcher executes the liquidation
4. Auction proceeds go to the protocol (not to MEV bots)

### Supported Chains (11+)

Ethereum, Arbitrum, Optimism, Base, Polygon, Avalanche, BNB Chain, Monad (testnet), Sei, Blast, Mode

### Integration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@pythnetwork/express-relay-sdk-solidity/IExpressRelayFeeReceiver.sol";

contract LendingProtocol is IExpressRelayFeeReceiver {
    address public immutable expressRelay;

    error CallerNotExpressRelay();

    constructor(address _expressRelay) {
        expressRelay = _expressRelay;
    }

    /// @notice Called by Express Relay to distribute auction proceeds
    function receiveAuctionProceedings() external payable {
        if (msg.sender != expressRelay) revert CallerNotExpressRelay();
        // Auction proceeds received -- credit to protocol treasury
    }

    function liquidate(
        address borrower,
        bytes[] calldata pythUpdateData
    ) external payable {
        // Only Express Relay can call this, or allow public liquidations
        // with MEV protection via the auction mechanism

        // Update prices atomically
        uint256 fee = IPyth(pyth).getUpdateFee(pythUpdateData);
        IPyth(pyth).updatePriceFeeds{value: fee}(pythUpdateData);

        // Check if position is liquidatable using fresh prices
        // ... liquidation logic ...
    }
}
```

## Pyth Lazer

Pyth Lazer is a separate product optimized for ultra-low-latency applications (HFT, perpetual DEXes). It delivers prices with ~1ms latency via WebSocket, compared to ~400ms for standard Pyth/Hermes.

- Separate subscription required
- Different data format (not compatible with standard Pyth SDK)
- Currently supports select feeds on select chains
- Documentation: https://docs.pyth.network/lazer

## Recommended Function Usage

| Use Case | Function | Why |
|----------|----------|-----|
| Standard price read | `getPriceNoOlderThan(id, maxAge)` | Reverts if stale, configurable freshness |
| Gas-optimized read (after update in same tx) | `getPriceUnsafe(id)` | Cheapest read, safe only after atomic update |
| Historical / settlement | `parsePriceFeedUpdates(data, ids, minTime, maxTime)` | Returns price at specific timestamp |
| Liquidation threshold | `getEmaPriceNoOlderThan(id, maxAge)` | EMA smooths volatility spikes, reduces false liquidations |
| Sponsored chain check | `getPriceNoOlderThan(id, 60)` in try/catch | Skip update if feed is already fresh |

## Related Skills

- **chainlink** -- Push-based oracle, complementary to Pyth for multi-oracle fallback strategies
- **redstone** -- Another pull oracle with modular design, ERC-7412 compatible
- **pyth** -- Pyth on Solana (native, non-EVM integration)

## References

- [Pyth Network Documentation](https://docs.pyth.network)
- [Pyth EVM SDK (pyth-sdk-solidity)](https://github.com/pyth-network/pyth-crosschain/tree/main/target_chains/ethereum/sdk/solidity)
- [Hermes API Reference](https://hermes.pyth.network/docs)
- [Price Feed IDs](https://pyth.network/developers/price-feed-ids)
- [Express Relay Documentation](https://docs.pyth.network/express-relay)
- [Pyth Lazer Documentation](https://docs.pyth.network/lazer)
- [Pyth Contract Addresses](https://docs.pyth.network/price-feeds/contract-addresses/evm)
- [@pythnetwork/hermes-client npm](https://www.npmjs.com/package/@pythnetwork/hermes-client)
- [Pyth Best Practices](https://docs.pyth.network/price-feeds/best-practices)
