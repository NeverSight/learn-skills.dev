---
name: wormhole
description: Wormhole cross-chain messaging and token transfers — NTT (Native Token Transfers) framework, VAA (Verified Action Approvals), guardian network, automatic and manual relayers, Wormhole Queries for cross-chain reads, and Standard Relayer integration. Covers Wormhole SDK, contract interfaces, and deployment across Ethereum, Solana, Arbitrum, Base, and Optimism.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Cross-Chain
tags:
  - wormhole
  - cross-chain
  - messaging
  - ntt
  - bridging
  - vaa
---

# Wormhole

Wormhole is a generic cross-chain messaging protocol secured by a set of 19 Guardian nodes. Each Guardian runs a full node for every connected chain and observes the Wormhole Core Contract. When a contract emits a message via `publishMessage()`, Guardians independently observe the event, sign an attestation, and produce a VAA (Verified Action Approval) once 13-of-19 signatures are collected. The VAA is the fundamental primitive -- a signed, portable proof that something happened on a source chain, verifiable on any destination chain.

## What You Probably Got Wrong

> AI agents confuse Wormhole's multiple transfer mechanisms, chain ID schemes, and delivery semantics. These are the critical corrections.

- **NTT is NOT the Token Bridge** -- NTT (Native Token Transfers) burns tokens on the source chain and mints natively on the destination. The legacy Token Bridge locks tokens on the source and mints wrapped representations (e.g., `WETHwh`). NTT produces canonical tokens; Token Bridge produces wrapped tokens. Choose based on whether you control the token contract.
- **VAAs must be verified on the destination chain** -- A raw VAA is just bytes. The destination chain's Core Bridge contract verifies the guardian signatures against the current guardian set before any action is taken. Never trust unverified VAA bytes.
- **Wormhole chain IDs are NOT EVM chain IDs** -- Wormhole uses its own chain ID scheme. Ethereum = 2, Solana = 1, Arbitrum = 23, Base = 30, Optimism = 24. Using EVM chain IDs (1, 42161, 8453, 10) will silently route messages to the wrong chain or revert.
- **The guardian set rotates** -- Guardian addresses change via governance VAAs. Never hardcode guardian public keys or set hashes. Always read the current guardian set from the Core Bridge contract.
- **`publishMessage()` does NOT deliver the message** -- Publishing only emits an event on the source chain. A relayer (automatic or manual) must fetch the VAA and submit it to the destination chain. Without a relayer, the message sits undelivered forever.
- **Consistency levels matter** -- `consistencyLevel = 1` means "instant" (observed immediately, less safe). `consistencyLevel = 15` waits for 15 block confirmations on Ethereum before Guardians sign. For high-value transfers, use `consistencyLevel = 15` (finalized).
- **Standard Relayer has gas limits** -- The automatic Standard Relayer caps gas on the destination chain. If your `receiveWormholeMessages` handler does significant computation, use manual relaying or increase the gas budget via `quoteDeliveryPrice`.
- **Token Bridge amounts lose precision** -- The Token Bridge normalizes all amounts to 8 decimal places. If your token has 18 decimals, the last 10 digits are truncated. NTT does not have this limitation.
- **Emitter addresses are bytes32, not EVM addresses** -- Wormhole identifies message senders as `bytes32`. For EVM chains, the address is left-padded with zeros. For Solana, it is the program's emitter PDA. Always normalize when comparing emitter addresses cross-chain.

## Quick Start

### Installation

```bash
npm install @wormhole-foundation/sdk viem
```

### Client Setup

```typescript
import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet, arbitrum } from "viem/chains";

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const sourceClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETH_RPC_URL),
});

const sourceWallet = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.ETH_RPC_URL),
});
```

### Send a Cross-Chain Message (Minimal)

```typescript
const CORE_BRIDGE = "0x98f3c9e6E3fAce36bAAd05FE09d375Ef1464288B" as const;

const coreBridgeAbi = [
  {
    name: "publishMessage",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "nonce", type: "uint32" },
      { name: "payload", type: "bytes" },
      { name: "consistencyLevel", type: "uint8" },
    ],
    outputs: [{ name: "sequence", type: "uint64" }],
  },
  {
    name: "messageFee",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const messageFee = await sourceClient.readContract({
  address: CORE_BRIDGE,
  abi: coreBridgeAbi,
  functionName: "messageFee",
});

const payload = new TextEncoder().encode("Hello from Ethereum");

const { request } = await sourceClient.simulateContract({
  address: CORE_BRIDGE,
  abi: coreBridgeAbi,
  functionName: "publishMessage",
  args: [
    0, // nonce -- use 0 unless batching messages
    `0x${Buffer.from(payload).toString("hex")}`,
    15, // consistencyLevel -- finalized (15 blocks on Ethereum)
  ],
  value: messageFee,
  account: account.address,
});

const hash = await sourceWallet.writeContract(request);
const receipt = await sourceClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("publishMessage reverted");
```

## Core Concepts

### VAA Structure

```
VAA:
├── version (uint8)           -- always 1
├── guardianSetIndex (uint32) -- which guardian set signed this
├── signatures[]              -- 13+ guardian signatures
└── body
    ├── timestamp (uint32)
    ├── nonce (uint32)
    ├── emitterChainId (uint16)   -- Wormhole chain ID, NOT EVM chain ID
    ├── emitterAddress (bytes32)  -- left-padded for EVM
    ├── sequence (uint64)
    ├── consistencyLevel (uint8)
    └── payload (bytes)           -- arbitrary application data
```

### Consistency Levels

| Level | Name | Meaning | Use Case |
|-------|------|---------|----------|
| 1 | Instant | Observed immediately, no finality wait | Low-value messages, latency-sensitive |
| 15 | Finalized | Wait for chain finality (15 blocks on Ethereum) | High-value transfers, security-critical |
| 200 | Safe | Chain-specific "safe" head | Medium-value, balanced latency/security |

### Wormhole Chain IDs (Common)

| Chain | Wormhole ID | EVM Chain ID |
|-------|-------------|-------------|
| Solana | 1 | N/A |
| Ethereum | 2 | 1 |
| BSC | 4 | 56 |
| Polygon | 5 | 137 |
| Avalanche | 6 | 43114 |
| Fantom | 10 | 250 |
| Sui | 21 | N/A |
| Aptos | 22 | N/A |
| Arbitrum | 23 | 42161 |
| Optimism | 24 | 10 |
| Base | 30 | 8453 |

See `resources/chain-ids.md` for the full mapping.

### Emitter Address Normalization

```typescript
import { type Address } from "viem";

function evmAddressToBytes32(address: Address): `0x${string}` {
  return `0x000000000000000000000000${address.slice(2)}` as `0x${string}`;
}

function bytes32ToEvmAddress(bytes32: `0x${string}`): Address {
  return `0x${bytes32.slice(26)}` as Address;
}
```

## NTT (Native Token Transfers)

NTT enables canonical token transfers across chains by burning on the source and minting on the destination. Unlike the Token Bridge, NTT produces native tokens (not wrapped), and the token deployer retains full control.

### Architecture

- **NttManager**: Core contract -- burn/mint logic, rate limiting, peer registration
- **Transceiver**: Transport layer that sends/receives messages via the guardian network
- **Token**: Your ERC-20 with burn/mint capabilities granted to the NttManager

### NTT Token Requirements

Your token must implement burn/mint controlled by the NttManager. See `templates/ntt-starter.sol` for a complete implementation.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

error CallerNotMinter(address caller);

contract NttToken is ERC20, ERC20Burnable, Ownable {
    address public minter;

    event MinterUpdated(address indexed oldMinter, address indexed newMinter);

    constructor(string memory name, string memory symbol, address initialOwner)
        ERC20(name, symbol) Ownable(initialOwner) {}

    /// @notice Set the minter address (NttManager on this chain)
    function setMinter(address newMinter) external onlyOwner {
        address old = minter;
        minter = newMinter;
        emit MinterUpdated(old, newMinter);
    }

    /// @notice Mint tokens -- only callable by the NttManager
    function mint(address to, uint256 amount) external {
        if (msg.sender != minter) revert CallerNotMinter(msg.sender);
        _mint(to, amount);
    }
}
```

### Sending an NTT Transfer

```typescript
import { type Address } from "viem";

const NTT_MANAGER = "0x..." as Address; // Your deployed NttManager
const WORMHOLE_ARBITRUM_CHAIN_ID = 23;

const nttManagerAbi = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "amount", type: "uint256" },
      { name: "recipientChain", type: "uint16" },
      { name: "recipient", type: "bytes32" },
    ],
    outputs: [{ name: "messageSequence", type: "uint64" }],
  },
] as const;

const amount = 1000_000000000000000000n; // 1000 tokens (18 decimals)
const recipientBytes32 = evmAddressToBytes32(account.address);

// Approve NttManager, then transfer
const { request } = await sourceClient.simulateContract({
  address: NTT_MANAGER,
  abi: nttManagerAbi,
  functionName: "transfer",
  args: [amount, WORMHOLE_ARBITRUM_CHAIN_ID, recipientBytes32],
  value: 0n,
  account: account.address,
});

const hash = await sourceWallet.writeContract(request);
const receipt = await sourceClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("NTT transfer reverted");
```

### NTT Rate Limiting

NTT includes built-in rate limiting per peer chain. Both inbound and outbound limits are configurable. If a transfer exceeds the limit and `shouldQueue = true`, it enters a queue. If `shouldQueue = false`, the transfer reverts. See `examples/deploy-ntt/` for full deployment setup including peer registration and rate limit configuration.

## Cross-Chain Messaging

### Publishing a Message (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {IWormhole} from "@wormhole-foundation/sdk-solidity/interfaces/IWormhole.sol";

error InsufficientFee(uint256 required, uint256 provided);

contract CrossChainSender {
    IWormhole public immutable wormhole;
    event MessageSent(uint64 indexed sequence, bytes payload);

    constructor(address wormholeCoreBridge) {
        wormhole = IWormhole(wormholeCoreBridge);
    }

    /// @notice Send a cross-chain message via Wormhole
    /// @param payload Arbitrary bytes to deliver to the destination
    /// @param consistencyLevel Finality requirement (1 = instant, 15 = finalized)
    /// @return sequence The Wormhole sequence number for tracking
    function sendMessage(bytes memory payload, uint8 consistencyLevel)
        external payable returns (uint64 sequence)
    {
        uint256 fee = wormhole.messageFee();
        if (msg.value < fee) revert InsufficientFee(fee, msg.value);

        sequence = wormhole.publishMessage{value: fee}(0, payload, consistencyLevel);
        emit MessageSent(sequence, payload);
    }
}
```

### Receiving a Message (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {IWormhole} from "@wormhole-foundation/sdk-solidity/interfaces/IWormhole.sol";

error InvalidEmitterChain(uint16 expected, uint16 actual);
error InvalidEmitterAddress(bytes32 expected, bytes32 actual);
error MessageAlreadyConsumed(bytes32 hash);

contract CrossChainReceiver {
    IWormhole public immutable wormhole;
    uint16 public immutable sourceChainId;
    bytes32 public immutable sourceEmitter;
    mapping(bytes32 => bool) public consumedMessages;

    event MessageReceived(uint16 indexed emitterChainId, bytes32 indexed emitterAddress, uint64 sequence, bytes payload);

    constructor(address wormholeCoreBridge, uint16 _sourceChainId, bytes32 _sourceEmitter) {
        wormhole = IWormhole(wormholeCoreBridge);
        sourceChainId = _sourceChainId;
        sourceEmitter = _sourceEmitter;
    }

    /// @notice Receive and verify a cross-chain message
    /// @param encodedVaa The full VAA bytes from the Guardian network
    function receiveMessage(bytes memory encodedVaa) external {
        (IWormhole.VM memory vm, bool valid, string memory reason) =
            wormhole.parseAndVerifyVM(encodedVaa);
        require(valid, reason);

        if (vm.emitterChainId != sourceChainId) revert InvalidEmitterChain(sourceChainId, vm.emitterChainId);
        if (vm.emitterAddress != sourceEmitter) revert InvalidEmitterAddress(sourceEmitter, vm.emitterAddress);

        bytes32 vaaHash = keccak256(encodedVaa);
        if (consumedMessages[vaaHash]) revert MessageAlreadyConsumed(vaaHash);
        consumedMessages[vaaHash] = true;

        emit MessageReceived(vm.emitterChainId, vm.emitterAddress, vm.sequence, vm.payload);
        _processPayload(vm.payload);
    }

    function _processPayload(bytes memory payload) internal {}
}
```

### Fetching a VAA (TypeScript)

```typescript
const WORMHOLE_API = "https://api.wormholescan.io/api/v1";

async function fetchVaa(
  emitterChain: number,
  emitterAddress: string,
  sequence: bigint,
  maxRetries = 30,
  delayMs = 2000
): Promise<Uint8Array> {
  const url = `${WORMHOLE_API}/vaas/${emitterChain}/${emitterAddress}/${sequence}`;

  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url);
    if (response.ok) {
      const json = (await response.json()) as { data: { vaa: string } };
      return Uint8Array.from(atob(json.data.vaa), (c) => c.charCodeAt(0));
    }
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  throw new Error(
    `VAA not found after ${maxRetries} retries: chain=${emitterChain} emitter=${emitterAddress} seq=${sequence}`
  );
}
```

## Wormhole Queries

Wormhole Queries enable cross-chain reads without sending a transaction. Guardians execute the read on the target chain and return a signed response. No gas is spent on the target chain.

| Query Type | Description | Use Case |
|-----------|-------------|----------|
| `EthCallQueryRequest` | Execute `eth_call` on a remote chain | Read contract state |
| `EthCallByTimestampQueryRequest` | `eth_call` at a specific timestamp | Historical state reads |
| `EthCallWithFinalityQueryRequest` | `eth_call` with explicit finality | Reads requiring finalized state |

```typescript
import { QueryRequest, EthCallQueryRequest, PerChainQueryRequest } from "@wormhole-foundation/sdk";
import { encodeFunctionData } from "viem";

const callData = encodeFunctionData({
  abi: [{ name: "balanceOf", type: "function", stateMutability: "view",
    inputs: [{ name: "account", type: "address" }], outputs: [{ name: "", type: "uint256" }] }] as const,
  functionName: "balanceOf",
  args: [account.address],
});

const ethCall = new EthCallQueryRequest("latest", [
  { to: "0x..." as const, data: callData },
]);

const query = new QueryRequest(0, [
  new PerChainQueryRequest(23, ethCall), // Arbitrum
]);

const response = await fetch("https://query.wormhole.com/v1/query", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ bytes: Buffer.from(query.serialize()).toString("hex") }),
});

if (!response.ok) throw new Error(`Query failed: ${response.status}`);
```

See `examples/query-crosschain/` for full examples including on-chain verification.

## Standard Relayer

The Standard Relayer handles VAA delivery automatically -- pay upfront on the source chain, the relayer delivers to the destination.

### Sending via Standard Relayer

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {IWormholeRelayer} from "@wormhole-foundation/sdk-solidity/interfaces/IWormholeRelayer.sol";

error InsufficientRelayerPayment(uint256 required, uint256 provided);

contract RelayedSender {
    IWormholeRelayer public immutable relayer;
    uint256 public constant DESTINATION_GAS_LIMIT = 300_000;

    event CrossChainMessageSent(uint16 indexed targetChain, address indexed targetAddress, uint64 sequence);

    constructor(address wormholeRelayer) {
        relayer = IWormholeRelayer(wormholeRelayer);
    }

    /// @notice Send a message via the Standard Relayer
    /// @param targetChain Wormhole chain ID of destination
    /// @param targetAddress Receiver contract on destination
    /// @param payload Message to deliver
    function sendMessage(uint16 targetChain, address targetAddress, bytes memory payload) external payable {
        (uint256 deliveryCost, ) = relayer.quoteEVMDeliveryPrice(targetChain, 0, DESTINATION_GAS_LIMIT);
        if (msg.value < deliveryCost) revert InsufficientRelayerPayment(deliveryCost, msg.value);

        uint64 sequence = relayer.sendPayloadToEvm{value: deliveryCost}(
            targetChain, targetAddress, payload, 0, DESTINATION_GAS_LIMIT
        );
        emit CrossChainMessageSent(targetChain, targetAddress, sequence);
    }
}
```

### Receiving via Standard Relayer

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {IWormholeReceiver} from "@wormhole-foundation/sdk-solidity/interfaces/IWormholeReceiver.sol";

error OnlyRelayer(address caller, address expected);
error UnregisteredSender(uint16 sourceChain, bytes32 sourceAddress);

contract RelayedReceiver is IWormholeReceiver {
    address public immutable wormholeRelayer;
    mapping(uint16 => bytes32) public registeredSenders;

    event CrossChainMessageReceived(uint16 indexed sourceChain, bytes32 indexed sourceAddress, bytes payload);

    constructor(address _wormholeRelayer) { wormholeRelayer = _wormholeRelayer; }

    /// @notice Register a trusted sender on a remote chain
    function registerSender(uint16 chainId, bytes32 sender) external {
        registeredSenders[chainId] = sender;
    }

    /// @notice Called by the Wormhole Relayer to deliver a message
    function receiveWormholeMessages(
        bytes memory payload, bytes[] memory, bytes32 sourceAddress,
        uint16 sourceChain, bytes32
    ) external payable override {
        if (msg.sender != wormholeRelayer) revert OnlyRelayer(msg.sender, wormholeRelayer);
        if (registeredSenders[sourceChain] != sourceAddress) revert UnregisteredSender(sourceChain, sourceAddress);

        emit CrossChainMessageReceived(sourceChain, sourceAddress, payload);
        _handlePayload(sourceChain, payload);
    }

    function _handlePayload(uint16 sourceChain, bytes memory payload) internal {}
}
```

### Gas Estimation

```typescript
const WORMHOLE_RELAYER = "0x27428DD2d3DD32A4D7f7C497eAaa23130d894911" as const;

const relayerAbi = [
  {
    name: "quoteEVMDeliveryPrice",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "targetChain", type: "uint16" },
      { name: "receiverValue", type: "uint256" },
      { name: "gasLimit", type: "uint256" },
    ],
    outputs: [
      { name: "nativePriceQuote", type: "uint256" },
      { name: "targetChainRefundPerGasUnused", type: "uint256" },
    ],
  },
] as const;

const [deliveryCost] = await sourceClient.readContract({
  address: WORMHOLE_RELAYER,
  abi: relayerAbi,
  functionName: "quoteEVMDeliveryPrice",
  args: [23, 0n, 300_000n], // Arbitrum, no receiver value, 300k gas
});
```

## Token Bridge (Legacy)

The Token Bridge locks tokens on the source chain and mints wrapped representations on the destination. Use NTT for new deployments where you control the token.

| Criteria | Token Bridge | NTT |
|----------|-------------|-----|
| Token ownership | Third-party tokens you don't control | Tokens you deploy and control |
| Token representation | Wrapped (e.g., `WETHwh`) | Native (canonical) |
| Decimal precision | Truncated to 8 decimals | Full precision preserved |
| Rate limiting | None built-in | Built-in, configurable |

### Transfer Flow

1. **Attest** (one-time): call `attestToken()` on source, fetch VAA, call `createWrapped()` on destination
2. **Transfer**: approve Token Bridge, call `transferTokens()`, fetch VAA
3. **Redeem**: submit VAA to destination Token Bridge via `completeTransfer()`

See `examples/token-bridge/` for a complete working example with attestation, transfer, and redemption.

```typescript
const TOKEN_BRIDGE = "0x3ee18B2214AFF97000D974cf647E7C347E8fa585" as const;

const tokenBridgeAbi = [
  { name: "attestToken", type: "function", stateMutability: "payable",
    inputs: [{ name: "tokenAddress", type: "address" }, { name: "nonce", type: "uint32" }],
    outputs: [{ name: "sequence", type: "uint64" }] },
  { name: "transferTokens", type: "function", stateMutability: "payable",
    inputs: [
      { name: "token", type: "address" }, { name: "amount", type: "uint256" },
      { name: "recipientChain", type: "uint16" }, { name: "recipient", type: "bytes32" },
      { name: "arbiterFee", type: "uint256" }, { name: "nonce", type: "uint32" },
    ],
    outputs: [{ name: "sequence", type: "uint64" }] },
  { name: "completeTransfer", type: "function", stateMutability: "nonpayable",
    inputs: [{ name: "encodedVm", type: "bytes" }], outputs: [] },
] as const;
```

## Deployment Pattern

### Multi-Chain NTT Setup

1. Deploy your token on each chain
2. Deploy NttManager on each chain
3. Deploy Transceiver on each chain
4. Register peers bidirectionally (`setPeer` on both NttManagers)
5. Configure rate limits (inbound and outbound)
6. Set the NttManager as the minter on each token contract

```typescript
const setPeerAbi = [
  { name: "setPeer", type: "function", stateMutability: "nonpayable",
    inputs: [
      { name: "peerChainId", type: "uint16" }, { name: "peerContract", type: "bytes32" },
      { name: "decimals", type: "uint8" }, { name: "inboundLimit", type: "uint256" },
    ], outputs: [] },
] as const;

// On Ethereum: register Arbitrum NttManager as peer
const { request } = await sourceClient.simulateContract({
  address: ETH_NTT_MANAGER,
  abi: setPeerAbi,
  functionName: "setPeer",
  args: [23, evmAddressToBytes32(ARB_NTT_MANAGER), 18, 1_000_000_000000000000000000n],
  account: account.address,
});
```

See `examples/deploy-ntt/` for the complete deployment walkthrough.

## Fee & Gas Estimation

### Core Bridge Message Fee

```typescript
const messageFee = await sourceClient.readContract({
  address: CORE_BRIDGE,
  abi: coreBridgeAbi,
  functionName: "messageFee",
});
// Always read dynamically -- never hardcode as 0
```

### Standard Relayer Delivery Price

```typescript
const [deliveryCost, refundPerGas] = await sourceClient.readContract({
  address: WORMHOLE_RELAYER,
  abi: relayerAbi,
  functionName: "quoteEVMDeliveryPrice",
  args: [targetChainId, receiverValue, gasLimit],
});
```

## Contract Addresses

> **Last verified:** February 2026

| Contract | Ethereum | Arbitrum | Base | Optimism | Solana |
|----------|----------|----------|------|----------|--------|
| Core Bridge | `0x98f3c9e6E3fAce36bAAd05FE09d375Ef1464288B` | `0xa5f208e072434bC67592E4C49C1B991BA79BCA46` | `0xbebdb6C8ddC678FfA9f8748f85C815C556Dd8ac6` | `0xEe91C335eab126dF5fDB3797EA9d6aD93aeC9722` | `worm2ZoG2kUd4vFXhvjh93UUH596ayRfgQ2MgjNMTth` |
| Token Bridge | `0x3ee18B2214AFF97000D974cf647E7C347E8fa585` | `0x0b2402144Bb366A632D14B83F244D2e0e21bD39c` | `0x8d2de8d2f73F1F4cAB472AC9A881C9b123C79627` | `0x1D68124e65faFC907325e3EDbF8c4d84499DAa8b` | `wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb` |
| Standard Relayer | `0x27428DD2d3DD32A4D7f7C497eAaa23130d894911` | `0x27428DD2d3DD32A4D7f7C497eAaa23130d894911` | `0x706F82e9bb5b0813f02e75c3e0a2ead1b0F4E9Cb` | `0x27428DD2d3DD32A4D7f7C497eAaa23130d894911` | N/A |

See `resources/contract-addresses.md` for NFT Bridge addresses and verification commands.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `InvalidVAA` | VAA signature verification failed | Ensure correct guardian set and uncorrupted VAA |
| `GuardianSetExpired` | Signed by an old guardian set | Refetch a fresh VAA from the Guardian network |
| `InsufficientFee` | msg.value < messageFee | Read `messageFee()` and send at least that amount |
| `TransferAmountTooSmall` | Token Bridge normalized amount to 0 | Amount must be >= 10^(decimals - 8) |
| `ReplayProtection` | VAA already consumed | Each VAA can only be redeemed once per chain |
| `OnlyRelayer` | Non-relayer called receiveWormholeMessages | Only the Wormhole Relayer contract can call this |
| `RateLimitExceeded` | NTT transfer exceeds configured limit | Wait for replenishment or set `shouldQueue = true` |

See `resources/error-codes.md` for the complete error reference.

## References

- [Wormhole Documentation](https://docs.wormhole.com/)
- [Wormhole SDK (TypeScript)](https://github.com/wormhole-foundation/wormhole-sdk-ts)
- [Wormhole Solidity SDK](https://github.com/wormhole-foundation/wormhole-solidity-sdk)
- [NTT Documentation](https://docs.wormhole.com/docs/learn/messaging/native-token-transfers/overview/)
- [Wormhole Queries](https://docs.wormhole.com/docs/queries/overview/)
- [Wormholescan Explorer](https://wormholescan.io/)
- [Wormhole Chain IDs](https://docs.wormhole.com/docs/build/reference/chain-ids/)
- [Contract Addresses](https://docs.wormhole.com/docs/build/reference/contract-addresses/)
