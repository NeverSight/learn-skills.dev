---
name: chainlink
description: Chainlink oracle integration — price feeds (AggregatorV3Interface), VRF v2.5 verifiable randomness, Automation (Keepers) for conditional execution, and CCIP cross-chain messaging. Covers staleness checks, decimal normalization, subscription management, and upkeep patterns across Ethereum, Arbitrum, and Base.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - chainlink
  - oracle
  - price-feed
  - vrf
  - automation
  - ccip
---

# Chainlink

Chainlink provides decentralized oracle infrastructure: price feeds for DeFi pricing, VRF for provably fair randomness, Automation for scheduled/conditional on-chain execution, and CCIP for cross-chain messaging and token transfers.

## What You Probably Got Wrong

- **`latestRoundData()` returns `int256`, not `uint256`** — Price can be negative (e.g., oil futures in 2020). Always check `answer > 0` before casting.
- **Decimals vary per feed** — ETH/USD has 8 decimals, ETH/BTC has 18 decimals, USDC/USD has 8. Always call `decimals()` or hardcode per known feed. Never assume 8.
- **VRF v2 is deprecated — use VRF v2.5** — VRF v2.5 supports both LINK and native payment, uses `requestRandomWords()` with a struct parameter, and has a different coordinator interface. Most LLM training data references VRF v2.
- **Staleness is not optional** — A price feed can return a stale answer if the oracle network stops updating. You must check `updatedAt` against a heartbeat threshold. Feeds without staleness checks have caused protocol-draining exploits.
- **`roundId` can be zero on L2s** — On Arbitrum/Optimism sequencer feeds, round semantics differ. Do not rely on `roundId` for ordering on L2 feeds.
- **CCIP is not Chainlink VRF** — They are separate products. CCIP handles cross-chain messaging; VRF handles randomness. Different contracts, different billing.
- **Automation renamed from Keepers** — The product is now called Chainlink Automation, not Keepers. The interface names changed: `KeeperCompatibleInterface` is now `AutomationCompatibleInterface`.

## Price Feeds

### AggregatorV3Interface

The core interface for reading Chainlink price data on-chain.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

contract PriceConsumer {
    AggregatorV3Interface internal immutable priceFeed;

    // ETH/USD heartbeat: 3600s on mainnet, 86400s on Arbitrum
    uint256 private constant STALENESS_THRESHOLD = 3600;

    constructor(address feedAddress) {
        priceFeed = AggregatorV3Interface(feedAddress);
    }

    function getLatestPrice() public view returns (int256 price, uint8 feedDecimals) {
        (
            uint80 roundId,
            int256 answer,
            /* uint256 startedAt */,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();

        if (answer <= 0) revert InvalidPrice();
        if (updatedAt == 0) revert RoundNotComplete();
        if (block.timestamp - updatedAt > STALENESS_THRESHOLD) revert StalePrice();
        if (answeredInRound < roundId) revert StaleRound();

        return (answer, priceFeed.decimals());
    }

    /// @notice Normalize a feed answer to 18 decimals
    function normalizeToWad(int256 answer, uint8 feedDecimals) public pure returns (uint256) {
        if (answer <= 0) revert InvalidPrice();
        if (feedDecimals <= 18) {
            return uint256(answer) * 10 ** (18 - feedDecimals);
        }
        return uint256(answer) / 10 ** (feedDecimals - 18);
    }

    error InvalidPrice();
    error RoundNotComplete();
    error StalePrice();
    error StaleRound();
}
```

### Reading Price Feeds with TypeScript (viem)

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";

const AGGREGATOR_V3_ABI = parseAbi([
  "function latestRoundData() external view returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)",
  "function decimals() external view returns (uint8)",
  "function description() external view returns (string)",
]);

// ETH/USD on Ethereum mainnet
const ETH_USD_FEED = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419" as const;
const STALENESS_THRESHOLD = 3600n;

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

async function getPrice(feedAddress: `0x${string}`) {
  const [roundData, feedDecimals] = await Promise.all([
    client.readContract({
      address: feedAddress,
      abi: AGGREGATOR_V3_ABI,
      functionName: "latestRoundData",
    }),
    client.readContract({
      address: feedAddress,
      abi: AGGREGATOR_V3_ABI,
      functionName: "decimals",
    }),
  ]);

  const [roundId, answer, , updatedAt, answeredInRound] = roundData;

  if (answer <= 0n) throw new Error("Invalid price: non-positive");
  if (updatedAt === 0n) throw new Error("Round not complete");

  const now = BigInt(Math.floor(Date.now() / 1000));
  if (now - updatedAt > STALENESS_THRESHOLD) {
    throw new Error(`Stale price: ${now - updatedAt}s old`);
  }
  if (answeredInRound < roundId) {
    throw new Error("Stale round: answeredInRound < roundId");
  }

  // Normalize to 18 decimals
  const normalized =
    feedDecimals <= 18
      ? answer * 10n ** (18n - BigInt(feedDecimals))
      : answer / 10n ** (BigInt(feedDecimals) - 18n);

  return {
    raw: answer,
    decimals: feedDecimals,
    normalized,
    updatedAt,
  };
}

// Usage
const ethPrice = await getPrice(ETH_USD_FEED);
console.log(`ETH/USD: $${Number(ethPrice.raw) / 10 ** ethPrice.decimals}`);
```

### L2 Sequencer Uptime Feed

On L2s, check the sequencer uptime feed before trusting price data. If the sequencer was recently restarted, prices may be stale while oracles catch up.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

contract L2PriceConsumer {
    AggregatorV3Interface internal immutable sequencerUptimeFeed;
    AggregatorV3Interface internal immutable priceFeed;

    // Grace period after sequencer comes back online
    uint256 private constant GRACE_PERIOD = 3600;

    constructor(address _sequencerFeed, address _priceFeed) {
        sequencerUptimeFeed = AggregatorV3Interface(_sequencerFeed);
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function getPrice() external view returns (int256) {
        (, int256 sequencerAnswer, , uint256 sequencerUpdatedAt, ) =
            sequencerUptimeFeed.latestRoundData();

        // answer == 0 means sequencer is up, answer == 1 means down
        if (sequencerAnswer != 0) revert SequencerDown();
        if (block.timestamp - sequencerUpdatedAt < GRACE_PERIOD) revert GracePeriodNotOver();

        (, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
        if (price <= 0) revert InvalidPrice();
        if (block.timestamp - updatedAt > 86400) revert StalePrice();

        return price;
    }

    error SequencerDown();
    error GracePeriodNotOver();
    error InvalidPrice();
    error StalePrice();
}
```

## VRF v2.5

Chainlink VRF v2.5 provides provably fair, verifiable randomness. It uses subscription-based billing and supports payment in LINK or native token.

### Requesting Randomness

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {VRFConsumerBaseV2Plus} from "@chainlink/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";

contract RandomConsumer is VRFConsumerBaseV2Plus {
    uint256 public immutable subscriptionId;
    bytes32 public immutable keyHash;

    // 200k gas covers most callbacks; increase for complex logic
    uint32 private constant CALLBACK_GAS_LIMIT = 200_000;
    uint16 private constant REQUEST_CONFIRMATIONS = 3;
    uint32 private constant NUM_WORDS = 1;

    mapping(uint256 => address) public requestToSender;
    mapping(address => uint256) public results;

    event RandomnessRequested(uint256 indexed requestId, address indexed requester);
    event RandomnessFulfilled(uint256 indexed requestId, uint256 randomWord);

    constructor(
        uint256 _subscriptionId,
        address _vrfCoordinator,
        bytes32 _keyHash
    ) VRFConsumerBaseV2Plus(_vrfCoordinator) {
        subscriptionId = _subscriptionId;
        keyHash = _keyHash;
    }

    function requestRandom() external returns (uint256 requestId) {
        requestId = s_vrfCoordinator.requestRandomWords(
            VRFV2PlusClient.RandomWordsRequest({
                keyHash: keyHash,
                subId: subscriptionId,
                requestConfirmations: REQUEST_CONFIRMATIONS,
                callbackGasLimit: CALLBACK_GAS_LIMIT,
                numWords: NUM_WORDS,
                extraArgs: VRFV2PlusClient._argsToBytes(
                    // false = pay with LINK, true = pay with native
                    VRFV2PlusClient.ExtraArgsV1({nativePayment: false})
                )
            })
        );

        requestToSender[requestId] = msg.sender;
        emit RandomnessRequested(requestId, msg.sender);
    }

    function fulfillRandomWords(
        uint256 requestId,
        uint256[] calldata randomWords
    ) internal override {
        address requester = requestToSender[requestId];
        results[requester] = randomWords[0];
        emit RandomnessFulfilled(requestId, randomWords[0]);
    }
}
```

### VRF Subscription Management (TypeScript)

```typescript
import { createWalletClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const VRF_COORDINATOR_ABI = parseAbi([
  "function createSubscription() external returns (uint256 subId)",
  "function addConsumer(uint256 subId, address consumer) external",
  "function removeConsumer(uint256 subId, address consumer) external",
  "function getSubscription(uint256 subId) external view returns (uint96 balance, uint96 nativeBalance, uint64 reqCount, address subOwner, address[] consumers)",
  "function fundSubscriptionWithNative(uint256 subId) external payable",
]);

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

// Ethereum mainnet VRF Coordinator v2.5
const VRF_COORDINATOR = "0xD7f86b4b8Cae7D942340FF628F82735b7a20893a" as const;

async function createSubscription() {
  const hash = await walletClient.writeContract({
    address: VRF_COORDINATOR,
    abi: VRF_COORDINATOR_ABI,
    functionName: "createSubscription",
  });
  console.log("Subscription created, tx:", hash);
  return hash;
}

async function addConsumer(subId: bigint, consumerAddress: `0x${string}`) {
  const hash = await walletClient.writeContract({
    address: VRF_COORDINATOR,
    abi: VRF_COORDINATOR_ABI,
    functionName: "addConsumer",
    args: [subId, consumerAddress],
  });
  console.log("Consumer added, tx:", hash);
  return hash;
}
```

## Automation (Keepers)

Chainlink Automation executes on-chain functions when conditions are met. Your contract implements `checkUpkeep` (off-chain simulation) and `performUpkeep` (on-chain execution).

### AutomationCompatible Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AutomationCompatibleInterface} from "@chainlink/contracts/src/v0.8/automation/AutomationCompatible.sol";

contract AutomatedCounter is AutomationCompatibleInterface {
    uint256 public counter;
    uint256 public lastTimestamp;
    uint256 public immutable interval;

    event CounterIncremented(uint256 indexed newValue, uint256 timestamp);

    constructor(uint256 _interval) {
        interval = _interval;
        lastTimestamp = block.timestamp;
    }

    /// @notice Called off-chain by Automation nodes to check if upkeep is needed
    /// @dev Must NOT modify state. Gas cost does not matter (simulated off-chain).
    function checkUpkeep(bytes calldata)
        external
        view
        override
        returns (bool upkeepNeeded, bytes memory performData)
    {
        upkeepNeeded = (block.timestamp - lastTimestamp) >= interval;
        performData = abi.encode(counter);
    }

    /// @notice Called on-chain when checkUpkeep returns true
    /// @dev Re-validate the condition — checkUpkeep result may be stale
    function performUpkeep(bytes calldata) external override {
        if ((block.timestamp - lastTimestamp) < interval) revert UpkeepNotNeeded();

        lastTimestamp = block.timestamp;
        counter += 1;
        emit CounterIncremented(counter, block.timestamp);
    }

    error UpkeepNotNeeded();
}
```

### Log-Triggered Automation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ILogAutomation, Log} from "@chainlink/contracts/src/v0.8/automation/interfaces/ILogAutomation.sol";

contract LogTriggeredUpkeep is ILogAutomation {
    event ActionPerformed(address indexed sender, uint256 amount);

    /// @notice Called when a matching log event is detected
    function checkLog(Log calldata log, bytes memory)
        external
        pure
        returns (bool upkeepNeeded, bytes memory performData)
    {
        upkeepNeeded = true;
        performData = log.data;
    }

    function performUpkeep(bytes calldata performData) external {
        (address sender, uint256 amount) = abi.decode(performData, (address, uint256));
        emit ActionPerformed(sender, amount);
    }
}
```

## CCIP (Cross-Chain Interoperability Protocol)

CCIP enables sending arbitrary messages and tokens between supported chains.

### Sending a Cross-Chain Message

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IRouterClient} from "@chainlink/contracts-ccip/src/v0.8/ccip/interfaces/IRouterClient.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CCIPSender {
    IRouterClient public immutable router;
    IERC20 public immutable linkToken;

    event MessageSent(bytes32 indexed messageId, uint64 indexed destinationChain);

    constructor(address _router, address _link) {
        router = IRouterClient(_router);
        linkToken = IERC20(_link);
    }

    function sendMessage(
        uint64 destinationChainSelector,
        address receiver,
        bytes calldata data
    ) external returns (bytes32 messageId) {
        Client.EVM2AnyMessage memory message = Client.EVM2AnyMessage({
            receiver: abi.encode(receiver),
            data: data,
            tokenAmounts: new Client.EVMTokenAmount[](0),
            extraArgs: Client._argsToBytes(
                Client.EVMExtraArgsV2({gasLimit: 200_000, allowOutOfOrderExecution: true})
            ),
            feeToken: address(linkToken)
        });

        uint256 fees = router.getFee(destinationChainSelector, message);
        linkToken.approve(address(router), fees);

        messageId = router.ccipSend(destinationChainSelector, message);
        emit MessageSent(messageId, destinationChainSelector);
    }
}
```

### Receiving a Cross-Chain Message

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {CCIPReceiver} from "@chainlink/contracts-ccip/src/v0.8/ccip/applications/CCIPReceiver.sol";
import {Client} from "@chainlink/contracts-ccip/src/v0.8/ccip/libraries/Client.sol";

contract CCIPReceiverExample is CCIPReceiver {
    // Allowlist source chains and senders to prevent unauthorized messages
    mapping(uint64 => mapping(address => bool)) public allowlistedSenders;
    address public owner;

    event MessageReceived(
        bytes32 indexed messageId,
        uint64 indexed sourceChainSelector,
        address sender,
        bytes data
    );

    constructor(address _router) CCIPReceiver(_router) {
        owner = msg.sender;
    }

    function allowlistSender(
        uint64 chainSelector,
        address sender,
        bool allowed
    ) external {
        if (msg.sender != owner) revert Unauthorized();
        allowlistedSenders[chainSelector][sender] = allowed;
    }

    function _ccipReceive(Client.Any2EVMMessage memory message) internal override {
        address sender = abi.decode(message.sender, (address));
        if (!allowlistedSenders[message.sourceChainSelector][sender]) {
            revert SenderNotAllowlisted();
        }

        emit MessageReceived(
            message.messageId,
            message.sourceChainSelector,
            sender,
            message.data
        );
    }

    error Unauthorized();
    error SenderNotAllowlisted();
}
```

## Contract Addresses

> **Last verified:** 2025-05-01

### Price Feeds

| Pair | Ethereum Mainnet | Arbitrum One | Base |
|------|-----------------|--------------|------|
| ETH/USD | `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` | `0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612` | `0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70` |
| BTC/USD | `0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c` | `0x6ce185860a4963106506C203335A2910413708e9` | `0x64c911996D3c6aC71f9b455B1E8E7M1BbDC942BAe` |
| USDC/USD | `0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6` | `0x50834F3163758fcC1Df9973b6e91f0F0F0434aD3` | `0x7e860098F58bBFC8648a4311b374B1D669a2bc6B` |
| LINK/USD | `0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c` | `0x86E53CF1B870786351Da77A57575e79CB55812CB` | `0x17CAb8FE31cA45e4684E33E3D258F20E88B8fD8B` |

### Sequencer Uptime Feeds

| Chain | Address |
|-------|---------|
| Arbitrum | `0xFdB631F5EE196F0ed6FAa767959853A9F217697D` |
| Base | `0xBCF85224fc0756B9Fa45aAb7d2257eC1673570EF` |
| Optimism | `0x371EAD81c9102C9BF4874A9075FFFf170F2Ee389` |

### VRF v2.5 Coordinators

| Chain | Coordinator |
|-------|-------------|
| Ethereum | `0xD7f86b4b8Cae7D942340FF628F82735b7a20893a` |
| Arbitrum | `0x3C0Ca683b403E37668AE3DC4FB62F4B29B6f7a3e` |
| Base | `0xd5D517aBE5cF79B7e95eC98dB0f0277788aFF634` |

### CCIP Routers

| Chain | Router | Chain Selector |
|-------|--------|----------------|
| Ethereum | `0x80226fc0Ee2b096224EeAc085Bb9a8cba1146f7D` | `5009297550715157269` |
| Arbitrum | `0x141fa059441E0ca23ce184B6A78bafD2A517DdE8` | `4949039107694359620` |
| Base | `0x881e3A65B4d4a04dD529061dd0071cf975F58bCD` | `15971525489660198786` |

### LINK Token

| Chain | Address |
|-------|---------|
| Ethereum | `0x514910771AF9Ca656af840dff83E8264EcF986CA` |
| Arbitrum | `0xf97f4df75117a78c1A5a0DBb814Af92458539FB4` |
| Base | `0x88Fb150BDc53A65fe94Dea0c9BA0a6dAf8C6e196` |

## Error Handling

| Error / Symptom | Cause | Fix |
|-----------------|-------|-----|
| `answer <= 0` from price feed | Feed returning invalid/negative price | Check `answer > 0` before using; revert or use fallback oracle |
| `block.timestamp - updatedAt > threshold` | Oracle stopped updating (network congestion, feed deprecation) | Implement staleness check with per-feed heartbeat threshold |
| `answeredInRound < roundId` | Answer is from a previous round | Reject stale round data |
| VRF callback reverts | `callbackGasLimit` too low for your `fulfillRandomWords` logic | Increase `callbackGasLimit`; test gas usage on fork |
| VRF request pending indefinitely | Subscription underfunded, consumer not added, or wrong `keyHash` | Fund subscription, verify consumer is registered, use correct key hash for your chain |
| Automation `performUpkeep` not firing | `checkUpkeep` returns false, upkeep underfunded, or gas price too high | Debug `checkUpkeep` locally; fund upkeep; check min balance requirements |
| CCIP `InsufficientFeeTokenAmount` | Not enough LINK approved for fees | Call `router.getFee()` first, then approve that amount + buffer |
| CCIP message not delivered | Destination contract reverts, sender not allowlisted, or chain selector wrong | Check receiver contract, verify allowlist, confirm chain selectors from docs |

## Security Considerations

### Price Feed Safety

1. **Always check staleness** — Every `latestRoundData()` call must validate `updatedAt` against the feed's heartbeat. ETH/USD on mainnet has a 3600s heartbeat; on Arbitrum it is 86400s. Check [Chainlink's feed page](https://data.chain.link) for per-feed heartbeats.

2. **Sanity-bound oracle prices** — If a feed reports ETH at $0.01 or $1,000,000, something is wrong. Add upper and lower bounds based on reasonable price ranges and revert or pause if breached.

```solidity
uint256 private constant MIN_ETH_PRICE = 100e8;       // $100
uint256 private constant MAX_ETH_PRICE = 100_000e8;    // $100,000

function getSafePrice(AggregatorV3Interface feed) internal view returns (uint256) {
    (, int256 answer, , uint256 updatedAt, ) = feed.latestRoundData();
    if (answer <= 0) revert InvalidPrice();
    if (block.timestamp - updatedAt > 3600) revert StalePrice();
    if (uint256(answer) < MIN_ETH_PRICE || uint256(answer) > MAX_ETH_PRICE) {
        revert PriceOutOfBounds();
    }
    return uint256(answer);
}
```

3. **L2 sequencer check** — On Arbitrum, Base, and Optimism, always check the sequencer uptime feed. A sequencer outage means oracle updates are delayed; using stale prices during recovery has caused exploits.

4. **Decimal normalization** — Never assume 8 decimals. Always call `feed.decimals()` or use known constants per feed. When combining two feeds (e.g., TOKEN/ETH and ETH/USD), handle decimals carefully to avoid overflow or truncation.

5. **Multi-oracle fallback** — For critical DeFi protocols, use Chainlink as primary but have a fallback (e.g., Uniswap TWAP or Pyth) to prevent single oracle dependency from freezing your protocol.

### VRF Safety

- Never use block values (`block.timestamp`, `block.prevrandao`) as randomness — they are manipulable by validators.
- Store the `requestId` -> user mapping before the callback. The callback is asynchronous and you need to know who requested it.
- Set `callbackGasLimit` high enough for your logic but not excessively — you pay for unused gas.

### Automation Safety

- Always re-validate conditions in `performUpkeep`. The `checkUpkeep` result may be stale by the time `performUpkeep` executes on-chain.
- `checkUpkeep` runs off-chain in simulation — it cannot modify state. Any state changes will be reverted.

### CCIP Safety

- Always allowlist source chains and sender addresses on your receiver contract. Without this, anyone on any supported chain can send messages to your contract.
- Handle message failures gracefully. If `_ccipReceive` reverts, the message can be manually executed later, but your contract should not end up in an inconsistent state from partial execution.

## Alternative Oracles

For use cases where Chainlink's push model isn't optimal, consider these alternatives:

**Pyth Network** (`pyth-evm` skill) — Pull oracle model where consumers fetch and submit price updates on-demand. Best for: sub-second price freshness (~400ms on Pythnet), confidence intervals (statistical uncertainty bounds), MEV-protected liquidations via Express Relay, and non-EVM chains (Solana, Sui, Aptos). Trade-off: consumers pay gas for price updates (~120-150K gas per feed).

**When to use Chainlink vs Pyth:**
- **Chainlink**: Zero-cost reads (DON sponsors updates), broadest EVM feed coverage (1000+), VRF/CCIP/Automation ecosystem, well-established data quality
- **Pyth**: Sub-second freshness, confidence intervals, historical price verification, MEV protection, 50+ EVM chains + non-EVM

See also: `redstone` skill for another pull oracle alternative.

## References

- [Chainlink Price Feed Addresses](https://docs.chain.link/data-feeds/price-feeds/addresses)
- [Chainlink VRF v2.5 Docs](https://docs.chain.link/vrf/v2-5/overview)
- [Chainlink Automation Docs](https://docs.chain.link/chainlink-automation)
- [Chainlink CCIP Docs](https://docs.chain.link/ccip)
- [data.chain.link — Feed Explorer](https://data.chain.link)
- [Chainlink GitHub — contracts](https://github.com/smartcontractkit/chainlink)
- [CCIP Chain Selectors](https://docs.chain.link/ccip/supported-networks)
