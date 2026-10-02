---
name: layerzero
description: LayerZero V2 cross-chain messaging — OApp framework, OFT (Omnichain Fungible Token), DVN configuration, executor setup, message options, and cross-chain deployment patterns. Covers lz-oapp contracts, EndpointV2 interface, message lifecycle, and security configuration across Ethereum, Arbitrum, Base, Optimism, and Polygon.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Cross-Chain
tags:
  - layerzero
  - cross-chain
  - messaging
  - oft
  - oapp
  - bridging
---

# LayerZero

LayerZero V2 is an immutable, censorship-resistant messaging protocol for cross-chain communication. It enables smart contracts on different blockchains to send arbitrary messages to each other through a modular security stack of Decentralized Verifier Networks (DVNs). The core primitive is the OApp (Omnichain Application) — a contract that inherits `OApp.sol` and implements `_lzSend` / `_lzReceive` to send and receive cross-chain messages through `EndpointV2`.

## What You Probably Got Wrong

> AI agents trained before mid-2024 confuse V1 and V2 architecture. These are the critical corrections.

- **V2 is NOT V1 — completely different architecture.** V1 used `LZApp`, `ILayerZeroEndpoint`, and a monolithic oracle+relayer model. V2 uses `OApp`, `EndpointV2`, and modular DVNs+Executors. Do NOT import `@layerzerolabs/solidity-examples` — that is V1. Use `@layerzerolabs/oapp-evm` for V2.
- **OFT burns on source, mints on destination — NOT a lock/mint bridge.** The Omnichain Fungible Token standard burns tokens on the source chain and mints equivalent tokens on the destination. For existing ERC-20s that cannot add burn/mint, use `OFTAdapter` which locks on source and mints an OFT representation on destination.
- **DVNs replace the V1 oracle+relayer model.** V1 had a single Oracle and Relayer operated by LayerZero Labs. V2 decouples verification into configurable DVN sets — you choose which DVNs must verify your messages and set quorum thresholds.
- **`_lzSend` requires proper fee estimation via `quoteSend()` or `_quote()`.** You must call the quote function first to determine the exact `MessagingFee` (native + lzToken), then pass that fee as `msg.value`. Underpaying reverts.
- **Peer addresses must be set on BOTH chains.** Calling `setPeer(dstEid, bytes32(peerAddress))` on chain A is not enough. You must also call `setPeer(srcEid, bytes32(chainAAddress))` on chain B. Unset peers cause `NoPeer` reverts.
- **Message ordering is NOT guaranteed unless you configure ordered delivery.** V2 delivers messages in a nonce-based system, but by default the executor can deliver messages out of order. Use the `OrderedNonce` enforcement option if strict ordering matters.
- **`eid` (Endpoint ID) is NOT the chain ID.** LayerZero uses its own Endpoint ID system. Ethereum mainnet is eid `30101`, Arbitrum is `30110`, Base is `30184`, Optimism is `30111`, Polygon is `30109`. Using chain IDs instead of eids is the most common integration mistake.
- **Peer addresses are `bytes32`, not `address`.** All peer addresses are stored as `bytes32` to support non-EVM chains. For EVM addresses, left-pad with zeros: `bytes32(uint256(uint160(addr)))`. Passing a raw `address` to `setPeer` will fail.
- **The Executor is separate from DVNs.** DVNs verify messages, but the Executor actually calls `lzReceive` on the destination. You can configure a custom Executor or use the LayerZero default. If you set gas limits too low in message options, the Executor will run out of gas on the destination.

## Quick Start

### Installation

```bash
npm install @layerzerolabs/oapp-evm @layerzerolabs/lz-evm-protocol-v2 @openzeppelin/contracts
```

For Foundry projects:

```bash
forge install LayerZero-Labs/LayerZero-v2
```

### Minimal OApp Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {OApp, Origin, MessagingFee} from "@layerzerolabs/oapp-evm/contracts/oapp/OApp.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract MyOApp is OApp {
    event MessageSent(uint32 dstEid, bytes payload, uint256 nativeFee);
    event MessageReceived(uint32 srcEid, bytes32 sender, bytes payload);

    constructor(
        address _endpoint,
        address _delegate
    ) OApp(_endpoint, _delegate) Ownable(_delegate) {}

    /// @notice Sends a message to a destination chain
    /// @param _dstEid Destination endpoint ID
    /// @param _payload Arbitrary bytes payload
    /// @param _options Message execution options (gas, value)
    function sendMessage(
        uint32 _dstEid,
        bytes calldata _payload,
        bytes calldata _options
    ) external payable {
        MessagingFee memory fee = _quote(_dstEid, _payload, _options, false);
        if (msg.value < fee.nativeFee) revert InsufficientFee(msg.value, fee.nativeFee);

        _lzSend(_dstEid, _payload, _options, fee, payable(msg.sender));

        emit MessageSent(_dstEid, _payload, fee.nativeFee);
    }

    /// @notice Quotes the fee for sending a message
    /// @param _dstEid Destination endpoint ID
    /// @param _payload Arbitrary bytes payload
    /// @param _options Message execution options
    /// @return fee The messaging fee breakdown
    function quote(
        uint32 _dstEid,
        bytes calldata _payload,
        bytes calldata _options
    ) external view returns (MessagingFee memory fee) {
        return _quote(_dstEid, _payload, _options, false);
    }

    /// @dev Called by EndpointV2 when a message arrives from a source chain
    function _lzReceive(
        Origin calldata _origin,
        bytes32 /*_guid*/,
        bytes calldata _payload,
        address /*_executor*/,
        bytes calldata /*_extraData*/
    ) internal override {
        emit MessageReceived(_origin.srcEid, _origin.sender, _payload);
    }

    error InsufficientFee(uint256 sent, uint256 required);
}
```

### Client Setup (TypeScript)

```typescript
import { createPublicClient, createWalletClient, http, parseAbi, type Address } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});
```

## Core Concepts

### Architecture Overview

```
Source Chain                          Destination Chain
+-----------+                        +-----------+
|  Your     |  _lzSend()             |  Your     |
|  OApp     | -----> EndpointV2      |  OApp     |
+-----------+        |               +-----------+
                     |                     ^
                     v                     | lzReceive()
              +------------+         +------------+
              |  MessageLib |         | EndpointV2 |
              +------------+         +------------+
                     |                     ^
                     v                     |
              +------+------+        +-----+-----+
              | DVN 1 | DVN 2|       | Executor  |
              +------+------+        +-----------+
                     |                     ^
                     +---------------------+
                     (off-chain verification & relay)
```

### OApp

The base contract for all cross-chain applications. Inherits from `OAppSender` and `OAppReceiver`. Manages peer addresses and delegates message send/receive through `EndpointV2`.

### OFT (Omnichain Fungible Token)

An ERC-20 that natively supports cross-chain transfers. Burns on source, mints on destination. For existing tokens, `OFTAdapter` wraps them.

### ONFT (Omnichain Non-Fungible Token)

ERC-721 that supports cross-chain transfers. Locks on source, mints on destination.

### EndpointV2

The immutable on-chain entry point. One per chain. Handles message dispatching, DVN verification, and executor relay. Cannot be upgraded.

### DVN (Decentralized Verifier Network)

Off-chain verifiers that attest to cross-chain message validity. Each OApp configures which DVNs must verify its messages. Multiple DVNs can be required for higher security.

### Executor

Calls `lzReceive()` on the destination contract. The default LayerZero Executor is used unless overridden. Executors are paid via the messaging fee.

### MessageLib

Handles message serialization, DVN verification, and nonce tracking. V2 uses `UltraLightNodeV2 (ULN302)` as the default send/receive library.

## OApp Development

### Sending Messages

```solidity
// _lzSend is inherited from OAppSender
function _lzSend(
    uint32 _dstEid,          // destination endpoint ID
    bytes memory _message,    // encoded payload
    bytes memory _options,    // execution options (gas, value)
    MessagingFee memory _fee, // fee from _quote()
    address payable _refundAddress
) internal returns (MessagingReceipt memory receipt);
```

The full send flow:

```solidity
function sendPing(uint32 _dstEid) external payable {
    bytes memory payload = abi.encode("ping", block.timestamp);

    // Build options: 200k gas for lzReceive on destination
    bytes memory options = OptionsBuilder.newOptions().addExecutorLzReceiveOption(200_000, 0);

    MessagingFee memory fee = _quote(_dstEid, payload, options, false);
    if (msg.value < fee.nativeFee) revert InsufficientFee(msg.value, fee.nativeFee);

    _lzSend(_dstEid, payload, options, fee, payable(msg.sender));
}
```

### Receiving Messages

```solidity
// Override _lzReceive to handle incoming messages
function _lzReceive(
    Origin calldata _origin,   // srcEid, sender (bytes32), nonce
    bytes32 _guid,             // globally unique message ID
    bytes calldata _payload,   // the message bytes
    address _executor,         // executor that delivered this
    bytes calldata _extraData  // additional data from executor
) internal override {
    (string memory message, uint256 timestamp) = abi.decode(_payload, (string, uint256));
    // Process the message
}
```

### Peer Configuration

Peers must be set bidirectionally. The peer address is `bytes32`-encoded.

```solidity
// On Ethereum OApp — register Arbitrum peer
oapp.setPeer(
    30110, // Arbitrum eid
    bytes32(uint256(uint160(arbitrumOAppAddress)))
);

// On Arbitrum OApp — register Ethereum peer
oapp.setPeer(
    30101, // Ethereum eid
    bytes32(uint256(uint160(ethereumOAppAddress)))
);
```

From TypeScript:

```typescript
const oappAbi = parseAbi([
  "function setPeer(uint32 eid, bytes32 peer) external",
]);

function addressToBytes32(addr: Address): `0x${string}` {
  return `0x${addr.slice(2).padStart(64, "0")}` as `0x${string}`;
}

const { request } = await publicClient.simulateContract({
  address: ethereumOApp,
  abi: oappAbi,
  functionName: "setPeer",
  args: [30110, addressToBytes32(arbitrumOApp)],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("setPeer reverted");
```

## OFT (Omnichain Fungible Token)

### Deploy a New OFT

For new tokens that do not already exist on any chain:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {OFT} from "@layerzerolabs/oft-evm/contracts/OFT.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is OFT {
    constructor(
        string memory _name,
        string memory _symbol,
        address _lzEndpoint,
        address _delegate
    ) OFT(_name, _symbol, _lzEndpoint, _delegate) Ownable(_delegate) {
        // Mint initial supply to deployer
        _mint(_delegate, 1_000_000 * 10 ** decimals());
    }
}
```

### OFTAdapter for Existing ERC-20s

If an ERC-20 already exists and cannot be modified, deploy `OFTAdapter` on the token's home chain. It locks the original token and coordinates minting on remote chains.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {OFTAdapter} from "@layerzerolabs/oft-evm/contracts/OFTAdapter.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract MyTokenAdapter is OFTAdapter {
    constructor(
        address _token,       // existing ERC-20 address
        address _lzEndpoint,
        address _delegate
    ) OFTAdapter(_token, _lzEndpoint, _delegate) Ownable(_delegate) {}
}
```

### Sending OFT Cross-Chain

```typescript
const oftAbi = parseAbi([
  "function send((uint32 dstEid, bytes32 to, uint256 amountLD, uint256 minAmountLD, bytes extraOptions, bytes composeMsg, bytes oftCmd) calldata sendParam, (uint256 nativeFee, uint256 lzTokenFee) calldata fee, address refundAddress) payable returns ((bytes32 guid, uint64 nonce, (uint256 nativeFee, uint256 lzTokenFee) fee) receipt)",
  "function quoteSend((uint32 dstEid, bytes32 to, uint256 amountLD, uint256 minAmountLD, bytes extraOptions, bytes composeMsg, bytes oftCmd) calldata sendParam, bool payInLzToken) view returns ((uint256 nativeFee, uint256 lzTokenFee) fee)",
]);

const DST_EID = 30110; // Arbitrum
const AMOUNT = 1000_000000000000000000n; // 1000 tokens (18 decimals)

const sendParam = {
  dstEid: DST_EID,
  to: addressToBytes32(account.address),
  amountLD: AMOUNT,
  minAmountLD: (AMOUNT * 995n) / 1000n, // 0.5% slippage
  extraOptions: "0x" as `0x${string}`,
  composeMsg: "0x" as `0x${string}`,
  oftCmd: "0x" as `0x${string}`,
};

// Quote the fee
const fee = await publicClient.readContract({
  address: oftAddress,
  abi: oftAbi,
  functionName: "quoteSend",
  args: [sendParam, false],
});

// Execute the send
const { request } = await publicClient.simulateContract({
  address: oftAddress,
  abi: oftAbi,
  functionName: "send",
  args: [sendParam, fee, account.address],
  value: fee.nativeFee,
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("OFT send reverted");
```

### OFT Shared Decimals

OFT uses a concept of "shared decimals" to normalize precision across chains. The default shared decimals is 6. Tokens with more than 6 decimals will have dust removed during transfers.

```
Local Decimals: 18 (standard ERC-20)
Shared Decimals: 6 (LayerZero default)
Dust removed: 12 decimal places

Sending 1.123456789012345678 tokens
Actually transferred: 1.123456000000000000 tokens
Dust lost: 0.000000789012345678 tokens
```

Override `sharedDecimals()` to change this behavior:

```solidity
function sharedDecimals() public pure override returns (uint8) {
    return 8; // higher precision cross-chain
}
```

## DVN & Security Configuration

### Setting Required and Optional DVNs

Each OApp configures its security stack through the EndpointV2's delegate (typically the OApp owner).

```solidity
import {SetConfigParam} from "@layerzerolabs/lz-evm-protocol-v2/contracts/interfaces/IMessageLibManager.sol";

struct UlnConfig {
    uint64 confirmations;         // block confirmations before DVN can verify
    uint8 requiredDVNCount;       // DVNs that MUST verify (all required)
    uint8 optionalDVNCount;       // DVNs from optional pool
    uint8 optionalDVNThreshold;   // how many optional DVNs must verify
    address[] requiredDVNs;       // addresses of required DVNs
    address[] optionalDVNs;       // addresses of optional DVNs
}
```

Example configuration — require LayerZero Labs DVN and one of two optional DVNs:

```solidity
UlnConfig memory ulnConfig = UlnConfig({
    confirmations: 15,                  // 15 block confirmations
    requiredDVNCount: 1,
    optionalDVNCount: 2,
    optionalDVNThreshold: 1,            // 1 of 2 optional must verify
    requiredDVNs: [LZ_DVN_ADDRESS],
    optionalDVNs: [GOOGLE_DVN_ADDRESS, POLYHEDRA_DVN_ADDRESS]
});
```

### Configuring via EndpointV2

```typescript
const endpointAbi = parseAbi([
  "function setConfig(address oapp, address lib, (uint32 eid, uint32 configType, bytes config)[] calldata params) external",
]);

// ULN config type for send library
const CONFIG_TYPE_ULN = 2;

// Encode the ULN config
// confirmations(uint64) + requiredDVNCount(uint8) + optionalDVNCount(uint8)
// + optionalDVNThreshold(uint8) + requiredDVNs(address[]) + optionalDVNs(address[])
import { encodeAbiParameters, parseAbiParameters } from "viem";

const ulnConfigEncoded = encodeAbiParameters(
  parseAbiParameters("uint64, uint8, uint8, uint8, address[], address[]"),
  [
    15n,                                // confirmations
    1,                                  // requiredDVNCount
    2,                                  // optionalDVNCount
    1,                                  // optionalDVNThreshold
    [LZ_DVN],                           // requiredDVNs
    [GOOGLE_DVN, POLYHEDRA_DVN],        // optionalDVNs
  ]
);
```

### Security Best Practices

- **Always set at least one required DVN.** The default config uses the LayerZero Labs DVN. For production, add at least one additional DVN (Google Cloud, Polyhedra, etc.).
- **Set block confirmations appropriate to the chain.** Ethereum: 15+, L2s (Arbitrum, Base, Optimism): 5+. Higher confirmations reduce reorg risk.
- **Configure BOTH send and receive libraries.** Security config applies per-direction. A message sent from Ethereum to Arbitrum uses Ethereum's send config AND Arbitrum's receive config. Configure both.

## Message Options

### Building Options with OptionsBuilder

```solidity
import {OptionsBuilder} from "@layerzerolabs/oapp-evm/contracts/oapp/libs/OptionsBuilder.sol";

using OptionsBuilder for bytes;

// Gas limit for lzReceive execution on destination
bytes memory options = OptionsBuilder.newOptions()
    .addExecutorLzReceiveOption(200_000, 0);

// Gas limit + native airdrop to recipient on destination
bytes memory optionsWithDrop = OptionsBuilder.newOptions()
    .addExecutorLzReceiveOption(200_000, 0)
    .addExecutorNativeDropOption(1 ether, receiverAddress);

// Composed message — triggers lzCompose after lzReceive
bytes memory composedOptions = OptionsBuilder.newOptions()
    .addExecutorLzReceiveOption(200_000, 0)
    .addExecutorLzComposeOption(0, 100_000, 0); // index, gas, value

// Ordered delivery — enforce nonce ordering
bytes memory orderedOptions = OptionsBuilder.newOptions()
    .addExecutorLzReceiveOption(200_000, 0)
    .addExecutorOrderedExecutionOption();
```

### Options Encoding in TypeScript

```typescript
import { encodePacked } from "viem";

// Option type constants
const EXECUTOR_WORKER_ID = 1;
const OPTION_TYPE_LZRECEIVE = 1;
const OPTION_TYPE_NATIVE_DROP = 2;

// Encode lzReceive option: 200k gas, 0 value
// Format: workerID(uint8) + optionLength(uint16) + optionType(uint8) + gas(uint128) + value(uint128)
function buildLzReceiveOption(gasLimit: bigint, value: bigint = 0n): `0x${string}` {
  // Options V2 encoding
  const TYPE_3 = "0x0003" as `0x${string}`;
  const workerIdAndOption = encodePacked(
    ["uint8", "uint16", "uint8", "uint128", "uint128"],
    [EXECUTOR_WORKER_ID, 34, OPTION_TYPE_LZRECEIVE, gasLimit, value]
  );
  return `${TYPE_3}${workerIdAndOption.slice(2)}` as `0x${string}`;
}

const options = buildLzReceiveOption(200_000n);
```

### Composed Messages

Composed messages allow an OApp to trigger follow-up logic after the initial `lzReceive`. The destination contract receives the message in `lzReceive`, then the Executor calls `lzCompose` separately.

```solidity
// In your OApp
function _lzReceive(
    Origin calldata _origin,
    bytes32 _guid,
    bytes calldata _payload,
    address _executor,
    bytes calldata _extraData
) internal override {
    // Decode and store state from the message

    // Queue a composed message for follow-up execution
    endpoint.sendCompose(
        address(this), // composeTo — typically self
        _guid,
        0,             // compose index
        _payload       // data for lzCompose
    );
}

// Called by the Executor after lzReceive completes
function lzCompose(
    address _from,
    bytes32 _guid,
    bytes calldata _message,
    address _executor,
    bytes calldata _extraData
) external payable {
    require(msg.sender == address(endpoint), "Only endpoint");
    // Execute follow-up logic (swap, stake, etc.)
}
```

## Deployment Pattern

### Multi-Chain Deploy Sequence

1. Deploy OApp on each chain (with that chain's EndpointV2 address)
2. Set peers bidirectionally between every chain pair
3. Configure DVNs for each pathway
4. Verify with a test message

```typescript
const ENDPOINT_V2: Record<number, Address> = {
  30101: "0x1a44076050125825900e736c501f859c50fE728c", // Ethereum
  30110: "0x1a44076050125825900e736c501f859c50fE728c", // Arbitrum
  30184: "0x1a44076050125825900e736c501f859c50fE728c", // Base
  30111: "0x1a44076050125825900e736c501f859c50fE728c", // Optimism
  30109: "0x1a44076050125825900e736c501f859c50fE728c", // Polygon
};

// After deploying OApp on each chain, set peers pairwise
async function setPeers(
  deployments: Map<number, Address>,
  walletClients: Map<number, typeof walletClient>,
  publicClients: Map<number, typeof publicClient>,
) {
  const eids = [...deployments.keys()];

  for (const srcEid of eids) {
    for (const dstEid of eids) {
      if (srcEid === dstEid) continue;

      const oapp = deployments.get(srcEid)!;
      const peer = deployments.get(dstEid)!;
      const client = walletClients.get(srcEid)!;
      const pub = publicClients.get(srcEid)!;

      const { request } = await pub.simulateContract({
        address: oapp,
        abi: oappAbi,
        functionName: "setPeer",
        args: [dstEid, addressToBytes32(peer)],
        account: account.address,
      });

      const hash = await client.writeContract(request);
      const receipt = await pub.waitForTransactionReceipt({ hash });
      if (receipt.status !== "success") {
        throw new Error(`setPeer failed: ${srcEid} -> ${dstEid}`);
      }
    }
  }
}
```

### Hardhat Deploy Script

```typescript
import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  const endpointV2 = "0x1a44076050125825900e736c501f859c50fE728c";

  const MyOApp = await ethers.getContractFactory("MyOApp");
  const oapp = await MyOApp.deploy(endpointV2, deployer.address);
  await oapp.waitForDeployment();

  const address = await oapp.getAddress();
  console.log(`MyOApp deployed at: ${address}`);

  // Verify on explorer
  await run("verify:verify", {
    address,
    constructorArguments: [endpointV2, deployer.address],
  });
}

main().catch(console.error);
```

### Foundry Deploy Script

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Script, console} from "forge-std/Script.sol";
import {MyOApp} from "../src/MyOApp.sol";

contract DeployOApp is Script {
    function run() external {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");
        address endpoint = 0x1a44076050125825900e736c501f859c50fE728c;
        address delegate = vm.addr(deployerKey);

        vm.startBroadcast(deployerKey);
        MyOApp oapp = new MyOApp(endpoint, delegate);
        console.log("MyOApp deployed:", address(oapp));
        vm.stopBroadcast();
    }
}
```

## Fee Estimation

### Quoting Send Fees

Always quote before sending. The fee depends on payload size, message options (gas, native drop), DVN configuration, and destination chain gas prices.

```typescript
const oappAbi = parseAbi([
  "function quote(uint32 dstEid, bytes calldata payload, bytes calldata options) view returns ((uint256 nativeFee, uint256 lzTokenFee) fee)",
]);

const fee = await publicClient.readContract({
  address: oappAddress,
  abi: oappAbi,
  functionName: "quote",
  args: [30110, payload, options],
});

// fee.nativeFee — amount of ETH/native token to send as msg.value
// fee.lzTokenFee — if paying with ZRO token (usually 0)
```

### Fee Breakdown

| Component | Determines |
|-----------|------------|
| DVN fees | Cost of DVN verification (based on DVN count and destination) |
| Executor fee | Gas cost of calling lzReceive on destination + native drop |
| Treasury fee | Protocol fee paid to LayerZero treasury |

### Paying with LZ Token (ZRO)

```solidity
// To pay with ZRO instead of native:
// 1. Approve ZRO token to EndpointV2
// 2. Pass payInLzToken = true in quote
// 3. lzTokenFee will be non-zero, nativeFee reduced
MessagingFee memory fee = _quote(_dstEid, _payload, _options, true);
// fee.lzTokenFee > 0, fee.nativeFee may be lower
```

## Error Handling

### Common Reverts

| Error | Cause | Fix |
|-------|-------|-----|
| `NoPeer` | Peer not set for destination eid | Call `setPeer(dstEid, peerBytes32)` on source |
| `OnlyPeer` | Message from unregistered sender | Set peer on the receiving chain |
| `InvalidEndpointCall` | Direct call instead of via endpoint | Only EndpointV2 can call `lzReceive` |
| `InsufficientFee` | `msg.value` less than quoted fee | Call `_quote()` or `quoteSend()` first, pass exact fee |
| `LzTokenUnavailable` | Trying to pay with ZRO when not enabled | Pass `false` for `payInLzToken` parameter |
| `InvalidOptions` | Malformed options bytes | Use `OptionsBuilder` to construct options |
| `SlippageExceeded` | OFT `minAmountLD` check failed | Increase `minAmountLD` tolerance or retry |
| `InvalidAmount` | OFT amount below shared decimal minimum | Send larger amount; dust below shared decimals is removed |
| `Unauthorized` | Caller is not the delegate/owner | Check OApp ownership and delegate settings |
| `InvalidEid` | Endpoint ID does not exist | Use correct eid from LayerZero docs (NOT chain ID) |

### Debugging Cross-Chain Failures

1. **Check source chain transaction.** If it reverted, the message was never sent. Fix the source-side issue (fee, peer, options).

2. **Use LayerZero Scan.** Go to `layerzeroscan.com` and enter the source tx hash. It shows message status: Sent, Verifying, Verified, Delivered, or Failed.

3. **Check DVN verification status.** If stuck at "Verifying", DVNs have not confirmed yet. Wait for block confirmations, or check if your DVN config is valid.

4. **Check executor delivery.** If verified but not delivered, the Executor may have failed. Common cause: insufficient gas in options. Increase `lzReceiveOption` gas limit.

5. **Retry failed messages.** If `lzReceive` reverted on destination, the message is stored and can be retried:

```typescript
const endpointAbi = parseAbi([
  "function retryPayload(uint32 srcEid, bytes32 sender, uint64 nonce, bytes calldata payload) external payable",
]);
```

6. **Common debugging commands:**

```bash
# Check if peer is set
cast call <oapp_address> "peers(uint32)(bytes32)" 30110 --rpc-url $RPC_URL

# Check endpoint delegate
cast call <oapp_address> "endpoint()(address)" --rpc-url $RPC_URL

# Verify contract has code
cast code <oapp_address> --rpc-url $RPC_URL
```

## Contract Addresses

> **Last verified:** February 2026

### EndpointV2

| Chain | eid | EndpointV2 |
|-------|-----|------------|
| Ethereum | `30101` | `0x1a44076050125825900e736c501f859c50fE728c` |
| Arbitrum | `30110` | `0x1a44076050125825900e736c501f859c50fE728c` |
| Optimism | `30111` | `0x1a44076050125825900e736c501f859c50fE728c` |
| Polygon | `30109` | `0x1a44076050125825900e736c501f859c50fE728c` |
| Base | `30184` | `0x1a44076050125825900e736c501f859c50fE728c` |

### Send/Receive Libraries (ULN302)

| Chain | SendUln302 | ReceiveUln302 |
|-------|------------|---------------|
| Ethereum | `0xbB2Ea70C9E858123480642Cf96acbcCE1372dCe1` | `0xc02Ab410f0734EFa3F14628780e6e695156024C2` |
| Arbitrum | `0x975bcD720be66659e3EB3C0e4F1866a3020E493A` | `0x7B9E184e07a6EE1aC23eAe0fe8D6Be60f4f19eF3` |
| Base | `0xB5320B0B3a13cC860893E2Bd79FCd7e13484Dda2` | `0xc70AB6f32772f59fBfc23889Caf4Ba3376C84bAf` |
| Optimism | `0x1322871e4ab09Bc7f5717189434f97bBD9546e95` | `0x3c4962Ff6258dcfCafD23a814237571571899985` |
| Polygon | `0x6c26c61a97006888ea9E4FA36584c7df57Cd9dA3` | `0x1322871e4ab09Bc7f5717189434f97bBD9546e95` |

### LayerZero Labs DVN

| Chain | Address |
|-------|---------|
| Ethereum | `0x589dEDbD617eE7783Ae3a7427E16b13280a2C00C` |
| Arbitrum | `0x2f55C492897526677C5B68fb199ea31E2c126416` |
| Base | `0x9e059a54699a285714207b43B055483E78FAac25` |
| Optimism | `0x6A02D83e8d433304bba74EF1c427913958187142` |
| Polygon | `0x23DE2FE932d9043291f870F07B7D2Bbca42e46c6` |

### Default Executor

| Chain | Address |
|-------|---------|
| Ethereum | `0x173272739Bd7Aa6e4e214714048a9fE699453059` |
| Arbitrum | `0x31CAe3B7fB82d847621859571BF619D4600e37c8` |
| Base | `0x2CCA08ae69E0C44b18a57Ab36A1CCb013C54B1d3` |
| Optimism | `0x2D2ea0697bdbede3F01553D2Ae4B8d0c486B666e` |
| Polygon | `0xCd3F213AD101472e1713C72B1697E727C803885b` |

## References

- [LayerZero V2 Docs](https://docs.layerzero.network/v2)
- [OApp Developer Guide](https://docs.layerzero.network/v2/developers/evm/oapp/overview)
- [OFT Developer Guide](https://docs.layerzero.network/v2/developers/evm/oft/quickstart)
- [EndpointV2 Reference](https://docs.layerzero.network/v2/developers/evm/technical-reference/deployed-contracts)
- [DVN Addresses](https://docs.layerzero.network/v2/developers/evm/technical-reference/dvn-addresses)
- [LayerZero Scan](https://layerzeroscan.com)
- [LayerZero V2 GitHub](https://github.com/LayerZero-Labs/LayerZero-v2)
- [OptionsBuilder Reference](https://docs.layerzero.network/v2/developers/evm/oapp/message-design)
- [@layerzerolabs/oapp-evm](https://www.npmjs.com/package/@layerzerolabs/oapp-evm)
