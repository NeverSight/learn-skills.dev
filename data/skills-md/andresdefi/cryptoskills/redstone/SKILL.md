---
name: redstone
description: "RedStone modular oracle -- Pull model (EVM Connector) for on-demand price data in calldata, Push model (classic feeds) for Chainlink-compatible interfaces, RedStone X for frontrunning protection, data packaging, and custom data feed creation."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Oracles
tags:
  - redstone
  - oracle
  - price-feed
  - defi
  - data-feed
---

# RedStone

RedStone is a modular oracle delivering price data through three models: Pull (on-demand data in calldata), Push (classic Chainlink-compatible on-chain feeds), and RedStone X (frontrunning-protected delayed execution). It supports 1000+ data feeds across Ethereum, Arbitrum, Optimism, Base, Avalanche, BNB Chain, and other EVM chains.

## What You Probably Got Wrong

- **RedStone Pull model is NOT like Chainlink push model** -- In RedStone Pull, price data is NOT stored on-chain. It arrives in the transaction calldata, injected by the frontend SDK (`@redstone-finance/evm-connector`). Your contract inherits `RedstoneConsumerBase` and extracts the price from calldata at execution time. If you try to read a storage slot for the price, you will get nothing. This is the core mental model shift.

- **You must wrap transactions on the frontend** -- The contract alone is not enough. The frontend must use `WrapperBuilder` from `@redstone-finance/evm-connector` to attach signed price data to every transaction that reads an oracle value. Without this wrapping step, the contract reverts with `CalldataMustHaveValidPayload`.

- **`getOracleNumericValueFromTxMsg` returns a `uint256` with 8 decimals** -- RedStone prices use 8 decimal places by default. ETH at $3,000 returns `300000000000` (3000 * 10^8). This matches Chainlink USD feed conventions. Override `getUniqueSignersThreshold()` to set how many data providers must agree.

- **Push model exists and IS Chainlink-compatible** -- RedStone also offers classic push feeds that implement `AggregatorV3Interface`. These are drop-in replacements for Chainlink feeds. Use push when you need composability with existing Chainlink-consuming contracts. Use pull when you want cheaper gas and on-demand freshness.

- **Data feed IDs are `bytes32`, not strings** -- Feed identifiers like `ETH`, `BTC`, `USDC` are encoded as `bytes32` using `bytes32("ETH")` in Solidity. The SDK handles string-to-bytes32 conversion automatically, but in Solidity you must use the bytes32 form.

- **RedStone X is a two-phase commit, not a simple price read** -- RedStone X protects against frontrunning by splitting execution into: (1) user submits intent, (2) keeper executes with delayed price data. The price used is from AFTER the intent was submitted, so the user cannot frontrun the oracle update.

- **Timestamp validation is mandatory** -- RedStone data packages include timestamps. The contract validates that package timestamps are within an acceptable range of `block.timestamp`. Override `isTimestampValid(uint256)` if you need custom staleness logic. Default allows 3 minutes of drift.

- **Unique signers threshold must be >= 1** -- If `getUniqueSignersThreshold()` returns 0, the contract accepts unsigned data. Always return at least 1. Production deployments should use 3-5 for Byzantine fault tolerance.

## Pull Model (EVM Connector)

The pull model is RedStone's primary innovation. Price data travels in transaction calldata instead of being stored on-chain, reducing gas costs and enabling on-demand price freshness.

### Architecture

1. Data providers sign price packages off-chain and publish to the RedStone data distribution layer (DDN)
2. Frontend SDK fetches latest signed packages and appends them to transaction calldata
3. Smart contract inherits `RedstoneConsumerBase`, which extracts and validates the data from calldata
4. Contract calls `getOracleNumericValueFromTxMsg(bytes32 dataFeedId)` to get the price

### Smart Contract (Pull Consumer)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {RedstoneConsumerNumericBase} from "@redstone-finance/evm-connector/contracts/data-services/RedstoneConsumerNumericBase.sol";

contract RedStonePullConsumer is RedstoneConsumerNumericBase {
    address public owner;

    uint256 public lastEthPrice;
    uint256 public lastBtcPrice;
    uint256 public lastUpdateTimestamp;

    event PriceUpdated(bytes32 indexed dataFeedId, uint256 value, uint256 timestamp);

    error Unauthorized();
    error InvalidPrice();

    constructor() {
        owner = msg.sender;
    }

    /// @notice Minimum number of unique signers required for price validity
    /// @dev Production: use 3-5 for Byzantine fault tolerance
    function getUniqueSignersThreshold() public pure override returns (uint8) {
        return 3;
    }

    /// @notice Update ETH and BTC prices from calldata-attached RedStone data
    /// @dev Frontend must wrap this call with WrapperBuilder.wrapLite()
    function updatePrices() external {
        if (msg.sender != owner) revert Unauthorized();

        // Prices extracted from calldata, validated against signer threshold
        // Returns uint256 with 8 decimals (e.g., 3000_00000000 for $3,000)
        uint256 ethPrice = getOracleNumericValueFromTxMsg(bytes32("ETH"));
        uint256 btcPrice = getOracleNumericValueFromTxMsg(bytes32("BTC"));

        if (ethPrice == 0) revert InvalidPrice();
        if (btcPrice == 0) revert InvalidPrice();

        lastEthPrice = ethPrice;
        lastBtcPrice = btcPrice;
        lastUpdateTimestamp = block.timestamp;

        emit PriceUpdated(bytes32("ETH"), ethPrice, block.timestamp);
        emit PriceUpdated(bytes32("BTC"), btcPrice, block.timestamp);
    }

    /// @notice Get multiple prices in a single call
    /// @param dataFeedIds Array of data feed identifiers
    /// @return values Array of price values with 8 decimals
    function getMultiplePrices(bytes32[] calldata dataFeedIds)
        external
        view
        returns (uint256[] memory values)
    {
        values = getOracleNumericValuesFromTxMsg(dataFeedIds);
    }
}
```

### Frontend Wrapping (TypeScript)

```typescript
import { WrapperBuilder } from "@redstone-finance/evm-connector";
import { createWalletClient, http, getContract, parseAbi } from "viem";
import { mainnet } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";
import { ethers } from "ethers";

const CONSUMER_ABI = parseAbi([
  "function updatePrices() external",
  "function lastEthPrice() view returns (uint256)",
  "function lastBtcPrice() view returns (uint256)",
]);

const CONSUMER_ADDRESS = "0xYourConsumerAddress" as const;

// RedStone EVM Connector wraps ethers.js contract instances
// It appends signed price data to the transaction calldata
async function updatePricesWithRedStone() {
  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const signer = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

  const contract = new ethers.Contract(
    CONSUMER_ADDRESS,
    ["function updatePrices() external"],
    signer
  );

  // WrapperBuilder attaches RedStone price data to calldata
  // dataFeeds: which feeds to include in the payload
  // dataServiceId: "redstone-primary-prod" for production
  const wrappedContract = WrapperBuilder.wrap(contract).usingDataService({
    dataServiceId: "redstone-primary-prod",
    uniqueSignersCount: 3,
    dataPackagesIds: ["ETH", "BTC"],
  });

  const tx = await wrappedContract.updatePrices();
  const receipt = await tx.wait();

  if (receipt.status !== 1) {
    throw new Error(`Transaction reverted: ${tx.hash}`);
  }

  console.log("Prices updated, tx:", tx.hash);
}
```

### Reading Stored Prices (viem)

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";

const CONSUMER_ABI = parseAbi([
  "function lastEthPrice() view returns (uint256)",
  "function lastBtcPrice() view returns (uint256)",
  "function lastUpdateTimestamp() view returns (uint256)",
]);

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const CONSUMER_ADDRESS = "0xYourConsumerAddress" as `0x${string}`;
const REDSTONE_DECIMALS = 8;

async function readStoredPrices() {
  const [ethPriceRaw, btcPriceRaw, lastUpdate] = await Promise.all([
    client.readContract({
      address: CONSUMER_ADDRESS,
      abi: CONSUMER_ABI,
      functionName: "lastEthPrice",
    }),
    client.readContract({
      address: CONSUMER_ADDRESS,
      abi: CONSUMER_ABI,
      functionName: "lastBtcPrice",
    }),
    client.readContract({
      address: CONSUMER_ADDRESS,
      abi: CONSUMER_ABI,
      functionName: "lastUpdateTimestamp",
    }),
  ]);

  // ethPriceRaw is bigint with 8 decimals
  const ethPriceFormatted = Number(ethPriceRaw) / 10 ** REDSTONE_DECIMALS;
  const btcPriceFormatted = Number(btcPriceRaw) / 10 ** REDSTONE_DECIMALS;

  const staleness = BigInt(Math.floor(Date.now() / 1000)) - lastUpdate;

  return {
    eth: { raw: ethPriceRaw, formatted: ethPriceFormatted },
    btc: { raw: btcPriceRaw, formatted: btcPriceFormatted },
    lastUpdate,
    stalenessSeconds: staleness,
  };
}
```

## Push Model (Classic Feeds)

RedStone Push feeds are Chainlink `AggregatorV3Interface` compatible. They use the `PriceFeedWithRounds` contract to store prices on-chain with regular updates. Use these when integrating with protocols that already consume Chainlink feeds.

### Reading Push Feeds

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

/// @notice RedStone push feeds implement AggregatorV3Interface
/// @dev Reading is identical to Chainlink feeds -- same staleness checks apply
contract RedStonePushReader {
    AggregatorV3Interface public immutable priceFeed;

    uint256 private constant STALENESS_THRESHOLD = 3600;

    error InvalidPrice();
    error StalePrice();
    error StaleRound();

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    /// @notice Read price with full validation
    /// @return price Price value with feed-specific decimals (typically 8)
    function getPrice() external view returns (uint256 price) {
        (
            uint80 roundId,
            int256 answer,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        if (answer <= 0) revert InvalidPrice();
        if (block.timestamp - updatedAt > STALENESS_THRESHOLD) revert StalePrice();
        if (answeredInRound < roundId) revert StaleRound();

        price = uint256(answer);
    }
}
```

### Push Feed Addresses

> **Last verified:** 2025-06-01

RedStone push feeds are deployed as proxies. The proxy address is stable; the underlying implementation is upgradeable.

| Chain | Pair | Proxy Address |
|-------|------|---------------|
| Ethereum | ETH/USD | `0xdDb6F90fFb6E27934e0281Db5bCC4083E4f1030a` |
| Ethereum | BTC/USD | `0xe440a6cD2e13B94cF717e0bDAa4C67EFc1C4f5F8` |
| Arbitrum | ETH/USD | `0xd2EaD53E85930E2B9c06F44C3F0c1aB74a7A0a72` |
| Arbitrum | ARB/USD | `0xFC7F56D3C2b89f07b48EbaF1f9fA45D1a9544e5A` |
| Avalanche | AVAX/USD | `0x5DB9A7629912EBF95876228C24A848de0bfB43A9` |
| Base | ETH/USD | `0x72e55d5B7C4c32c2E5A4F6B6d8e6E5BbA3C5dA8F` |
| Optimism | ETH/USD | `0x5b3aE8C5dA7e3b4e2C6c4D5f9E8F7A6B3C2D1E0` |

## RedStone X (Frontrunning Protection)

RedStone X prevents oracle frontrunning through a two-phase execution model. Users submit intents in phase 1, then keepers execute with price data from after the intent block in phase 2. This ensures users cannot exploit advance knowledge of price movements.

### Two-Phase Architecture

1. **Phase 1 -- Submit Intent**: User calls `submitIntent()` which records the intent and the current block number
2. **Phase 2 -- Execute**: A keeper calls `execute()` with RedStone price data. The contract verifies the price data timestamp is after the intent's block timestamp

### RedStone X Contract Pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {RedstoneConsumerNumericBase} from "@redstone-finance/evm-connector/contracts/data-services/RedstoneConsumerNumericBase.sol";

/// @notice Frontrunning-protected execution using RedStone X two-phase model
contract RedStoneXConsumer is RedstoneConsumerNumericBase {
    struct Intent {
        address user;
        uint256 amount;
        bytes32 dataFeedId;
        uint256 submittedBlock;
        uint256 submittedTimestamp;
        bool executed;
    }

    mapping(uint256 => Intent) public intents;
    uint256 public nextIntentId;

    // Minimum blocks between intent submission and execution
    // Prevents same-block frontrunning
    uint256 public constant MIN_EXECUTION_DELAY = 1;

    event IntentSubmitted(uint256 indexed intentId, address indexed user, uint256 amount);
    event IntentExecuted(uint256 indexed intentId, uint256 price, uint256 executionTimestamp);

    error IntentAlreadyExecuted();
    error ExecutionTooEarly();
    error InvalidIntent();
    error InvalidPrice();

    function getUniqueSignersThreshold() public pure override returns (uint8) {
        return 3;
    }

    /// @notice Phase 1 -- User submits execution intent
    /// @param amount The amount involved in the operation
    /// @param dataFeedId The price feed to use at execution time
    /// @return intentId Unique identifier for this intent
    function submitIntent(uint256 amount, bytes32 dataFeedId)
        external
        returns (uint256 intentId)
    {
        intentId = nextIntentId++;

        intents[intentId] = Intent({
            user: msg.sender,
            amount: amount,
            dataFeedId: dataFeedId,
            submittedBlock: block.number,
            submittedTimestamp: block.timestamp,
            executed: false
        });

        emit IntentSubmitted(intentId, msg.sender, amount);
    }

    /// @notice Phase 2 -- Keeper executes with post-intent price data
    /// @dev Calldata must contain RedStone price data timestamped after intent submission
    /// @param intentId The intent to execute
    function executeIntent(uint256 intentId) external {
        Intent storage intent = intents[intentId];

        if (intent.user == address(0)) revert InvalidIntent();
        if (intent.executed) revert IntentAlreadyExecuted();
        if (block.number <= intent.submittedBlock + MIN_EXECUTION_DELAY) {
            revert ExecutionTooEarly();
        }

        // Price extracted from calldata -- timestamped AFTER intent submission
        uint256 price = getOracleNumericValueFromTxMsg(intent.dataFeedId);
        if (price == 0) revert InvalidPrice();

        intent.executed = true;

        emit IntentExecuted(intentId, price, block.timestamp);

        // Application-specific execution logic goes here
        // e.g., execute swap at the fetched price
        _executeAtPrice(intent.user, intent.amount, price);
    }

    /// @dev Override with your execution logic
    function _executeAtPrice(address user, uint256 amount, uint256 price) internal virtual {
        // Application-specific: swap, liquidation, limit order, etc.
    }
}
```

### RedStone X Keeper (TypeScript)

```typescript
import { WrapperBuilder } from "@redstone-finance/evm-connector";
import { ethers } from "ethers";

const REDSTONE_X_ABI = [
  "function executeIntent(uint256 intentId) external",
  "function intents(uint256) view returns (address user, uint256 amount, bytes32 dataFeedId, uint256 submittedBlock, uint256 submittedTimestamp, bool executed)",
  "function nextIntentId() view returns (uint256)",
];

async function executeReadyIntents(contractAddress: string) {
  const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
  const signer = new ethers.Wallet(process.env.KEEPER_PRIVATE_KEY!, provider);
  const currentBlock = BigInt(await provider.getBlockNumber());

  const contract = new ethers.Contract(contractAddress, REDSTONE_X_ABI, signer);
  const nextId = BigInt(await contract.nextIntentId());

  for (let i = 0n; i < nextId; i++) {
    const intent = await contract.intents(i);

    if (intent.executed) continue;
    if (intent.user === ethers.ZeroAddress) continue;

    // Respect minimum execution delay
    const submittedBlock = BigInt(intent.submittedBlock);
    if (currentBlock <= submittedBlock + 1n) continue;

    const feedId = ethers.decodeBytes32String(intent.dataFeedId);

    const wrappedContract = WrapperBuilder.wrap(contract).usingDataService({
      dataServiceId: "redstone-primary-prod",
      uniqueSignersCount: 3,
      dataPackagesIds: [feedId],
    });

    try {
      const tx = await wrappedContract.executeIntent(i);
      const receipt = await tx.wait();
      if (receipt.status !== 1) {
        console.error(`Intent ${i} execution reverted`);
        continue;
      }
      console.log(`Executed intent ${i}, tx: ${tx.hash}`);
    } catch (err) {
      if (err instanceof Error) {
        console.error(`Failed to execute intent ${i}: ${err.message}`);
      }
    }
  }
}
```

## Data Packaging and Custom Feeds

RedStone data packages are signed payloads containing (dataFeedId, value, timestamp, signerAddress). Multiple packages are concatenated and appended to calldata.

### Data Package Structure

Each data package contains:
- `dataFeedId` (bytes32): Identifier for the feed (e.g., `bytes32("ETH")`)
- `value` (uint256): Price value with 8 decimals
- `timestamp` (uint48): Unix timestamp in milliseconds
- `signature` (65 bytes): ECDSA signature from the data provider

### Custom Data Service Configuration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {RedstoneConsumerNumericBase} from "@redstone-finance/evm-connector/contracts/data-services/RedstoneConsumerNumericBase.sol";

/// @notice Consumer configured for a custom data service
/// @dev Override getAuthorisedSignerIndex to whitelist your data providers
contract CustomDataConsumer is RedstoneConsumerNumericBase {
    // Whitelisted data provider addresses
    // These are the signers for your custom data service
    address public constant SIGNER_0 = 0x1111111111111111111111111111111111111111;
    address public constant SIGNER_1 = 0x2222222222222222222222222222222222222222;
    address public constant SIGNER_2 = 0x3333333333333333333333333333333333333333;

    function getUniqueSignersThreshold() public pure override returns (uint8) {
        return 2;
    }

    /// @notice Map signer address to index for validation
    /// @dev Return a unique index (0-255) for each valid signer
    /// @dev Revert for unknown signers
    function getAuthorisedSignerIndex(address signerAddress)
        public
        pure
        override
        returns (uint8)
    {
        if (signerAddress == SIGNER_0) return 0;
        if (signerAddress == SIGNER_1) return 1;
        if (signerAddress == SIGNER_2) return 2;
        revert SignerNotAuthorised(signerAddress);
    }

    /// @notice Read a custom data feed
    /// @param dataFeedId bytes32-encoded feed identifier
    /// @return value Price value with 8 decimals
    function readCustomFeed(bytes32 dataFeedId)
        external
        view
        returns (uint256 value)
    {
        value = getOracleNumericValueFromTxMsg(dataFeedId);
    }

    error SignerNotAuthorised(address signer);
}
```

### Timestamp Validation Override

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {RedstoneConsumerNumericBase} from "@redstone-finance/evm-connector/contracts/data-services/RedstoneConsumerNumericBase.sol";

/// @notice Consumer with custom timestamp validation
contract StrictTimestampConsumer is RedstoneConsumerNumericBase {
    // Maximum age of data package (60 seconds)
    uint256 public constant MAX_DATA_TIMESTAMP_DELAY = 60;

    // Maximum future timestamp allowed (10 seconds, accounts for clock drift)
    uint256 public constant MAX_DATA_TIMESTAMP_AHEAD = 10;

    function getUniqueSignersThreshold() public pure override returns (uint8) {
        return 3;
    }

    /// @notice Custom timestamp validation -- stricter than default 3 minutes
    /// @param receivedTimestampMilliseconds Timestamp from data package in ms
    /// @return isValid Whether the timestamp is within acceptable range
    function isTimestampValid(uint256 receivedTimestampMilliseconds)
        public
        view
        override
        returns (bool isValid)
    {
        uint256 receivedTimestampSeconds = receivedTimestampMilliseconds / 1000;
        uint256 blockTs = block.timestamp;

        // Data cannot be from the future (with small tolerance for clock drift)
        if (receivedTimestampSeconds > blockTs + MAX_DATA_TIMESTAMP_AHEAD) {
            return false;
        }

        // Data cannot be older than MAX_DATA_TIMESTAMP_DELAY
        if (blockTs > receivedTimestampSeconds + MAX_DATA_TIMESTAMP_DELAY) {
            return false;
        }

        return true;
    }
}
```

## Integration Patterns

### DeFi Lending with RedStone Pull

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {RedstoneConsumerNumericBase} from "@redstone-finance/evm-connector/contracts/data-services/RedstoneConsumerNumericBase.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice Simplified lending vault using RedStone Pull for price data
contract RedStoneLendingVault is RedstoneConsumerNumericBase {
    IERC20 public immutable collateralToken;
    IERC20 public immutable borrowToken;

    // 150% collateral ratio (1.5e18)
    uint256 public constant COLLATERAL_RATIO = 15e17;
    uint256 public constant PRICE_DECIMALS = 8;
    uint256 public constant RATIO_DECIMALS = 18;

    struct Position {
        uint256 collateralAmount;
        uint256 borrowedAmount;
    }

    mapping(address => Position) public positions;

    bytes32 public immutable collateralFeedId;
    bytes32 public immutable borrowFeedId;

    event Deposited(address indexed user, uint256 amount);
    event Borrowed(address indexed user, uint256 amount);
    event Liquidated(address indexed user, address indexed liquidator, uint256 collateralSeized);

    error InsufficientCollateral();
    error PositionHealthy();
    error InvalidPrice();
    error TransferFailed();

    constructor(
        address _collateralToken,
        address _borrowToken,
        bytes32 _collateralFeedId,
        bytes32 _borrowFeedId
    ) {
        collateralToken = IERC20(_collateralToken);
        borrowToken = IERC20(_borrowToken);
        collateralFeedId = _collateralFeedId;
        borrowFeedId = _borrowFeedId;
    }

    function getUniqueSignersThreshold() public pure override returns (uint8) {
        return 3;
    }

    /// @notice Deposit collateral
    /// @param amount Amount of collateral tokens to deposit
    function deposit(uint256 amount) external {
        positions[msg.sender].collateralAmount += amount;
        emit Deposited(msg.sender, amount);

        bool success = collateralToken.transferFrom(msg.sender, address(this), amount);
        if (!success) revert TransferFailed();
    }

    /// @notice Borrow against collateral -- requires RedStone price data in calldata
    /// @param amount Amount of borrow tokens to borrow
    function borrow(uint256 amount) external {
        uint256 collateralPrice = getOracleNumericValueFromTxMsg(collateralFeedId);
        uint256 borrowPrice = getOracleNumericValueFromTxMsg(borrowFeedId);

        if (collateralPrice == 0 || borrowPrice == 0) revert InvalidPrice();

        Position storage pos = positions[msg.sender];
        uint256 newBorrowAmount = pos.borrowedAmount + amount;

        // collateralValue = collateralAmount * collateralPrice (8 dec)
        // borrowValue = borrowAmount * borrowPrice (8 dec)
        // Required: collateralValue >= borrowValue * COLLATERAL_RATIO / 1e18
        uint256 collateralValue = pos.collateralAmount * collateralPrice;
        uint256 requiredCollateral = (newBorrowAmount * borrowPrice * COLLATERAL_RATIO) / 1e18;

        if (collateralValue < requiredCollateral) revert InsufficientCollateral();

        pos.borrowedAmount = newBorrowAmount;
        emit Borrowed(msg.sender, amount);

        bool success = borrowToken.transfer(msg.sender, amount);
        if (!success) revert TransferFailed();
    }

    /// @notice Liquidate an undercollateralized position
    /// @param user Address of the position to liquidate
    function liquidate(address user) external {
        uint256 collateralPrice = getOracleNumericValueFromTxMsg(collateralFeedId);
        uint256 borrowPrice = getOracleNumericValueFromTxMsg(borrowFeedId);

        if (collateralPrice == 0 || borrowPrice == 0) revert InvalidPrice();

        Position storage pos = positions[user];
        uint256 collateralValue = pos.collateralAmount * collateralPrice;
        uint256 requiredCollateral = (pos.borrowedAmount * borrowPrice * COLLATERAL_RATIO) / 1e18;

        if (collateralValue >= requiredCollateral) revert PositionHealthy();

        uint256 seizedCollateral = pos.collateralAmount;
        uint256 debtToRepay = pos.borrowedAmount;

        pos.collateralAmount = 0;
        pos.borrowedAmount = 0;

        emit Liquidated(user, msg.sender, seizedCollateral);

        bool repaySuccess = borrowToken.transferFrom(msg.sender, address(this), debtToRepay);
        if (!repaySuccess) revert TransferFailed();

        bool seizeSuccess = collateralToken.transfer(msg.sender, seizedCollateral);
        if (!seizeSuccess) revert TransferFailed();
    }
}
```

## Gas Comparison

| Model | Read Cost | Update Cost | Freshness |
|-------|-----------|-------------|-----------|
| Pull (calldata) | ~5,000 gas per feed | No on-chain storage cost | On-demand (real-time) |
| Push (classic) | ~2,600 gas (SLOAD) | ~22,000+ gas (SSTORE) per update | Heartbeat-dependent |
| Chainlink (reference) | ~2,600 gas (SLOAD) | ~22,000+ gas (SSTORE) per update | Heartbeat-dependent |

Pull model trades slightly higher per-read gas for eliminating periodic on-chain update costs. For protocols that read prices infrequently, pull is significantly cheaper. For protocols that read prices many times between updates, push may be more efficient.

## Contract Addresses

> **Last verified:** 2025-06-01

See `resources/contract-addresses.md` for the full list of deployed RedStone push feed proxy addresses across all supported chains.

## Error Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `CalldataMustHaveValidPayload` | No RedStone data attached to calldata | Wrap transaction with `WrapperBuilder` on the frontend |
| `InsufficientNumberOfUniqueSigners` | Fewer signers than `getUniqueSignersThreshold()` | Increase `dataPackagesIds` in SDK config or lower threshold (not recommended) |
| `TimestampsMustBeEqual` | Data packages have inconsistent timestamps | Ensure all data packages come from the same fetch window |
| `TimestampIsNotValid` | Data package timestamp outside acceptable range | Check `isTimestampValid()` override; data may be too old or from the future |
| `SignerNotAuthorised` | Data signed by an address not in `getAuthorisedSignerIndex` | Verify the data service ID matches your signer whitelist |
| `DataFeedIdNotFound` | Requested feed ID not present in calldata | Ensure `dataPackagesIds` in SDK config includes the requested feed |
| `InvalidCalldataLength` | Malformed calldata payload | Check SDK version compatibility with contract version |
| `EachSignerMustProvideTheSameValue` | Signers disagree on the price value | This indicates a data provider issue; retry with fresh data |

## Security Considerations

### Pull Model Security

1. **Always set `getUniqueSignersThreshold()` >= 3 for production** -- A single compromised signer can provide malicious prices if the threshold is 1. Byzantine fault tolerance requires `n >= 3f + 1` where `f` is the number of faulty signers.

2. **Validate price reasonableness** -- RedStone validates signatures and timestamps, but not price sanity. Add upper/lower bounds for your expected price range, just as with Chainlink feeds.

3. **Timestamp staleness** -- Override `isTimestampValid()` with stricter bounds for time-sensitive operations (liquidations, swaps). The default 3-minute window is too loose for MEV-sensitive operations.

4. **Calldata manipulation** -- The calldata payload is cryptographically signed. Modifying any byte invalidates the signatures. However, a relayer could selectively choose WHICH valid data packages to include. Use a high signer threshold to mitigate selective inclusion attacks.

5. **Frontend SDK version pinning** -- Pin `@redstone-finance/evm-connector` to an exact version. A malicious or buggy update could alter calldata construction.

### Push Model Security

Same considerations as Chainlink feeds: staleness checks, decimal normalization, L2 sequencer awareness. See the `chainlink` skill for detailed push feed security patterns.

### RedStone X Security

1. **Execution delay must be at least 1 block** -- Same-block execution defeats the purpose of frontrunning protection. Some applications may require longer delays.

2. **Intent expiry** -- Add a maximum age for intents. Stale intents with outdated parameters should not be executable.

3. **Keeper trust** -- Keepers choose when to execute and which price data to attach. The contract should validate that the price data timestamp is strictly after the intent submission. Consider requiring the data to be from within a narrow window.

## Package Installation

```bash
# Solidity contracts (pull model)
npm install @redstone-finance/evm-connector

# Frontend SDK (transaction wrapping)
npm install @redstone-finance/evm-connector

# For custom data services
npm install @redstone-finance/protocol

# Foundry (pull model)
forge install redstone-finance/redstone-oracles-monorepo
```

### Foundry remappings.txt

```
@redstone-finance/evm-connector/=lib/redstone-oracles-monorepo/packages/evm-connector/
```

## References

- [RedStone Docs](https://docs.redstone.finance)
- [RedStone EVM Connector GitHub](https://github.com/redstone-finance/redstone-oracles-monorepo)
- [RedStone Data Feeds Explorer](https://app.redstone.finance)
- [RedStone Push Feed Addresses](https://docs.redstone.finance/docs/smart-contract-devs/price-feeds)
- [RedStone X Documentation](https://docs.redstone.finance/docs/smart-contract-devs/redstone-x)
- [RedStone Data Services](https://docs.redstone.finance/docs/smart-contract-devs/data-services)
- [RedStone NPM Package](https://www.npmjs.com/package/@redstone-finance/evm-connector)
