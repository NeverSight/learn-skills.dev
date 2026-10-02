---
name: axelar
description: Axelar cross-chain messaging and token routing — General Message Passing (GMP), Interchain Token Service (ITS) for native multichain tokens, AxelarExecutable contract pattern, gas estimation, and cross-chain token deployment. Covers Axelar SDK, Gateway contract, and GasService integration.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Cross-Chain
tags:
  - axelar
  - cross-chain
  - gmp
  - interchain
  - bridge
  - messaging
---

# Axelar

Axelar is a cross-chain communication network that connects blockchains through a proof-of-stake validator set. It provides two core primitives: General Message Passing (GMP) for sending arbitrary contract calls across chains, and Interchain Token Service (ITS) for deploying and managing tokens that exist natively on multiple chains. Contracts receive cross-chain messages by inheriting `AxelarExecutable` and implementing the `_execute()` callback, which the Axelar Gateway invokes after validator consensus. Gas for destination-chain execution must be prepaid on the source chain via `AxelarGasService`.

## What You Probably Got Wrong

> AI agents frequently confuse Axelar's chain naming, gas payment model, and ITS vs. Gateway token transfers. These corrections are critical.

- **Chain identifiers are STRINGS, not numeric IDs.** Axelar uses human-readable chain names like `"ethereum"`, `"arbitrum"`, `"base"`. These are NOT EVM chain IDs (1, 42161, 8453) and NOT LayerZero eids. Passing a numeric chain ID will silently fail or route to a nonexistent chain. Always use the exact string from Axelar's chain registry.
- **Gas MUST be paid upfront on the source chain.** Unlike protocols with automatic relayers, Axelar requires you to call `AxelarGasService.payNativeGasForContractCall()` (or the `WithToken` variant) BEFORE calling `gateway.callContract()`. If you skip gas payment, the message is submitted to the network but never executed on the destination. There is no retry mechanism -- you must send a new transaction.
- **`_execute()` is the callback, NOT `execute()`.** Your contract inherits `AxelarExecutable` and overrides `_execute(string calldata sourceChain, string calldata sourceAddress, bytes calldata payload)`. The public `execute()` function is called by the Axelar relayer and routes to your `_execute()` after Gateway validation. Never override `execute()` directly.
- **You MUST validate `sourceChain` and `sourceAddress` in `_execute()`.** The Gateway validates that the message came through Axelar, but it does NOT validate the sender's identity. Anyone can send a GMP message. Your `_execute()` must check that `sourceChain` and `sourceAddress` match your trusted remote contract. Without this, any contract on any chain can trigger your `_execute()`.
- **ITS is NOT the same as Gateway token transfers.** `gateway.callContractWithToken()` moves Axelar-wrapped tokens (axlUSDC, axlWETH). ITS (`InterchainTokenService`) deploys and manages tokens that are canonical on every chain -- burn on source, mint on destination with the same token address derivation. Use ITS for new token deployments; use Gateway for existing Axelar-wrapped assets.
- **`sourceAddress` is a STRING, not an address type.** Cross-chain messages come from non-EVM chains too. The `sourceAddress` parameter in `_execute()` is a `string`, which is the lowercase hex representation of the sender address. To compare with an EVM address, convert: `keccak256(bytes(sourceAddress)) == keccak256(bytes(Strings.toHexString(trustedAddress)))`.
- **ITS token IDs are deterministic, derived from the deployer and salt.** The `tokenId` for an ITS-deployed token is `keccak256(abi.encode(address(deployer), salt))`. If you deploy from different addresses or with different salts on different chains, the tokens will NOT be linked. Always use the same deployer and salt on every chain.
- **`callContractWithToken` requires the token to be an Axelar-supported asset.** You cannot send arbitrary ERC-20s through `callContractWithToken`. Only tokens registered in the Axelar Gateway (like axlUSDC, axlWETH, WBTC, etc.) are supported. For arbitrary tokens, use ITS or bridge first.
- **Gas refunds go to the `refundAddress`, not `msg.sender`.** When paying gas via `AxelarGasService`, excess gas is refunded to the `refundAddress` parameter. If you pass `address(0)` or a contract that cannot receive ETH, the refund is lost.

## Quick Start

### Installation

```bash
npm install @axelar-network/axelar-gmp-sdk-solidity @openzeppelin/contracts
```

For Foundry projects:

```bash
forge install axelarnetwork/axelar-gmp-sdk-solidity
```

For the Axelar SDK (TypeScript):

```bash
npm install @axelar-network/axelarjs-sdk viem
```

### Minimal GMP Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import {AxelarExecutable} from "@axelar-network/axelar-gmp-sdk-solidity/contracts/executable/AxelarExecutable.sol";
import {IAxelarGateway} from "@axelar-network/axelar-gmp-sdk-solidity/contracts/interfaces/IAxelarGateway.sol";
import {IAxelarGasService} from "@axelar-network/axelar-gmp-sdk-solidity/contracts/interfaces/IAxelarGasService.sol";

contract MyGMPReceiver is AxelarExecutable {
    IAxelarGasService public immutable GAS_SERVICE;

    /// @dev Trusted remote: sourceChain -> sourceAddress (lowercase hex string)
    mapping(string => string) public trustedRemotes;

    event MessageReceived(string sourceChain, string sourceAddress, bytes payload);
    event MessageSent(string destinationChain, string destinationAddress, bytes payload);

    error UntrustedRemote(string sourceChain, string sourceAddress);
    error InsufficientGasPayment();

    constructor(
        address gateway_,
        address gasService_
    ) AxelarExecutable(gateway_) {
        GAS_SERVICE = IAxelarGasService(gasService_);
    }

    /// @notice Sends a GMP message to a destination chain
    /// @param destinationChain Axelar chain name (e.g., "arbitrum")
    /// @param destinationAddress Contract address on destination (string)
    /// @param payload Arbitrary encoded data
    function sendMessage(
        string calldata destinationChain,
        string calldata destinationAddress,
        bytes calldata payload
    ) external payable {
        if (msg.value == 0) revert InsufficientGasPayment();

        GAS_SERVICE.payNativeGasForContractCall{value: msg.value}(
            address(this),
            destinationChain,
            destinationAddress,
            payload,
            msg.sender
        );

        gateway().callContract(destinationChain, destinationAddress, payload);

        emit MessageSent(destinationChain, destinationAddress, payload);
    }

    /// @dev Called by the Axelar Gateway after validator consensus
    function _execute(
        string calldata sourceChain,
        string calldata sourceAddress,
        bytes calldata payload
    ) internal override {
        // Validate the sender is a trusted remote
        string memory trusted = trustedRemotes[sourceChain];
        if (keccak256(bytes(trusted)) != keccak256(bytes(sourceAddress))) {
            revert UntrustedRemote(sourceChain, sourceAddress);
        }

        emit MessageReceived(sourceChain, sourceAddress, payload);
    }

    /// @notice Sets a trusted remote contract for a given chain
    /// @param chain Axelar chain name
    /// @param remoteAddress Lowercase hex address string of the remote contract
    function setTrustedRemote(
        string calldata chain,
        string calldata remoteAddress
    ) external {
        trustedRemotes[chain] = remoteAddress;
    }
}
```

### Client Setup (TypeScript)

```typescript
import {
  createPublicClient,
  createWalletClient,
  http,
  parseAbi,
  type Address,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet, arbitrum } from "viem/chains";

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const ethereumClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL),
});

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL),
});
```

## Core Concepts

### Architecture Overview

```
Source Chain                              Destination Chain
+-------------+                          +-------------+
| Your        | callContract()           | Your        |
| Contract    | -----> Gateway           | Contract    |
+-------------+        |                +-------------+
      ^                |                       ^
      |                v                       | _execute()
+-------------+  +----------+           +----------+
| GasService  |  | Axelar   |           | Gateway  |
| (pay gas)   |  | Network  |           |          |
+-------------+  +----------+           +----------+
                       |                       ^
                       v                       |
                 +-----------+           +-----------+
                 | Validators|           | Relayer   |
                 | (PoS)     | --------> | (execute) |
                 +-----------+           +-----------+
```

### Gateway

The on-chain entry point for Axelar GMP. One per chain. Handles `callContract()` for sending messages and validates incoming messages before invoking `_execute()` on receiving contracts.

### GasService

Pays for destination-chain execution. You call `payNativeGasForContractCall()` with native tokens on the source chain. The Axelar relayer uses these funds to pay for gas on the destination chain. Excess is refunded to the `refundAddress`.

### AxelarExecutable

The base contract your GMP receiver inherits. Provides the `execute()` entry point (called by the relayer) and the `_execute()` hook (overridden by you). The `execute()` function validates the message through the Gateway before calling `_execute()`.

### Interchain Token Service (ITS)

Deploys tokens that exist natively on multiple chains. Unlike wrapped tokens, ITS tokens are canonical on every chain -- same tokenId, same supply accounting, burn-on-source/mint-on-destination. ITS handles the cross-chain token transfer lifecycle.

### Interchain Token Factory

A convenience contract for deploying ITS tokens. Provides `deployInterchainToken()` for new tokens and `deployRemoteInterchainToken()` to extend an existing ITS token to a new chain.

## General Message Passing (GMP)

### Sending a Message

```solidity
/// @notice GMP message flow: pay gas, then call Gateway
function sendCrossChain(
    string calldata destChain,
    string calldata destAddress,
    bytes calldata payload
) external payable {
    if (msg.value == 0) revert InsufficientGasPayment();

    // Step 1: Pay gas on source chain
    GAS_SERVICE.payNativeGasForContractCall{value: msg.value}(
        address(this),   // sender
        destChain,       // "arbitrum", "base", etc.
        destAddress,     // "0x1234..." as string
        payload,
        msg.sender       // refundAddress for excess gas
    );

    // Step 2: Submit message to Gateway
    gateway().callContract(destChain, destAddress, payload);
}
```

### Sending a Message with Token

```solidity
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice GMP + token transfer (Axelar-wrapped tokens only)
function sendWithToken(
    string calldata destChain,
    string calldata destAddress,
    bytes calldata payload,
    string calldata symbol,
    uint256 amount
) external payable {
    if (msg.value == 0) revert InsufficientGasPayment();

    address tokenAddress = gateway().tokenAddresses(symbol);
    IERC20(tokenAddress).transferFrom(msg.sender, address(this), amount);
    IERC20(tokenAddress).approve(address(gateway()), amount);

    GAS_SERVICE.payNativeGasForContractCallWithToken{value: msg.value}(
        address(this),
        destChain,
        destAddress,
        payload,
        symbol,
        amount,
        msg.sender
    );

    gateway().callContractWithToken(
        destChain,
        destAddress,
        payload,
        symbol,
        amount
    );
}
```

### Receiving a Message

```solidity
/// @dev Override for GMP messages without tokens
function _execute(
    string calldata sourceChain,
    string calldata sourceAddress,
    bytes calldata payload
) internal override {
    // ALWAYS validate the remote sender
    _validateRemote(sourceChain, sourceAddress);

    (address recipient, uint256 amount) = abi.decode(payload, (address, uint256));
    // Process the decoded data
}

/// @dev Override for GMP messages WITH tokens
function _executeWithToken(
    string calldata sourceChain,
    string calldata sourceAddress,
    bytes calldata payload,
    string calldata tokenSymbol,
    uint256 amount
) internal override {
    _validateRemote(sourceChain, sourceAddress);

    address tokenAddress = gateway().tokenAddresses(tokenSymbol);
    (address recipient) = abi.decode(payload, (address));

    // CEI: effects before interactions
    // (state updates would go here)

    IERC20(tokenAddress).transfer(recipient, amount);
}
```

### Trusted Remote Validation Pattern

```solidity
mapping(string => string) public trustedRemotes;

error UntrustedRemote(string chain, string sender);

function _validateRemote(
    string calldata sourceChain,
    string calldata sourceAddress
) internal view {
    string memory trusted = trustedRemotes[sourceChain];
    if (bytes(trusted).length == 0) {
        revert UntrustedRemote(sourceChain, sourceAddress);
    }
    if (keccak256(bytes(trusted)) != keccak256(bytes(sourceAddress))) {
        revert UntrustedRemote(sourceChain, sourceAddress);
    }
}

/// @notice Register a trusted remote contract
/// @dev sourceAddress must be the lowercase hex string of the contract address
function setTrustedRemote(
    string calldata chain,
    string calldata addr
) external onlyOwner {
    trustedRemotes[chain] = addr;
}
```

## Interchain Token Service (ITS)

### Deploy a New Interchain Token

ITS tokens are deployed through the `InterchainTokenFactory`. The same `salt` and deployer address must be used on every chain to produce linked tokens.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import {IInterchainTokenFactory} from "@axelar-network/interchain-token-service/contracts/interfaces/IInterchainTokenFactory.sol";
import {IInterchainTokenService} from "@axelar-network/interchain-token-service/contracts/interfaces/IInterchainTokenService.sol";

contract TokenDeployer {
    IInterchainTokenFactory public immutable FACTORY;
    IInterchainTokenService public immutable ITS;

    constructor(address factory_, address its_) {
        FACTORY = IInterchainTokenFactory(factory_);
        ITS = IInterchainTokenService(its_);
    }

    /// @notice Deploy a new interchain token on this chain
    /// @param salt Unique salt (must be the same on all chains)
    /// @param name Token name
    /// @param symbol Token symbol
    /// @param decimals Token decimals
    /// @param initialSupply Mint this amount to msg.sender on this chain
    function deployToken(
        bytes32 salt,
        string calldata name,
        string calldata symbol,
        uint8 decimals,
        uint256 initialSupply
    ) external payable returns (bytes32 tokenId) {
        tokenId = FACTORY.deployInterchainToken(
            salt,
            name,
            symbol,
            decimals,
            initialSupply,
            msg.sender
        );
    }

    /// @notice Deploy this token remotely on another chain
    /// @param salt Same salt used in the original deployment
    /// @param destinationChain Axelar chain name to deploy to
    /// @param gasValue Native token to pay for remote deployment gas
    function deployRemote(
        bytes32 salt,
        string calldata destinationChain,
        uint256 gasValue
    ) external payable returns (bytes32 tokenId) {
        tokenId = FACTORY.deployRemoteInterchainToken{value: gasValue}(
            "",
            salt,
            msg.sender,
            destinationChain,
            gasValue
        );
    }
}
```

### Send ITS Tokens Cross-Chain

```typescript
const itsAbi = parseAbi([
  "function interchainTransfer(bytes32 tokenId, string calldata destinationChain, bytes calldata destinationAddress, uint256 amount, bytes calldata metadata, uint256 gasValue) payable",
  "function interchainTransferFrom(address sender, bytes32 tokenId, string calldata destinationChain, bytes calldata destinationAddress, uint256 amount, bytes calldata metadata, uint256 gasValue) payable",
]);

const ITS_ADDRESS = "0xB5FB4BE02232B1bBA4dC8f81dc24C26980dE9e3C" as const;
const TOKEN_ID = "0x..." as `0x${string}`; // from deployInterchainToken
const AMOUNT = 1000_000000000000000000n; // 1000 tokens, 18 decimals

// Estimate gas for the cross-chain transfer
const gasValue = 500000000000000n; // 0.0005 ETH -- use Axelar gas estimator

const { request } = await ethereumClient.simulateContract({
  address: ITS_ADDRESS,
  abi: itsAbi,
  functionName: "interchainTransfer",
  args: [
    TOKEN_ID,
    "arbitrum",
    `0x${account.address.slice(2).padStart(64, "0")}` as `0x${string}`,
    AMOUNT,
    "0x" as `0x${string}`,
    gasValue,
  ],
  value: gasValue,
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await ethereumClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("ITS transfer reverted");
```

### Register an Existing ERC-20 with ITS

For existing tokens that cannot be modified, use `registerCanonicalInterchainToken`:

```solidity
/// @notice Register an existing ERC-20 as a canonical interchain token
/// @param tokenAddress The existing ERC-20 on this chain
function registerExisting(address tokenAddress) external returns (bytes32 tokenId) {
    tokenId = FACTORY.registerCanonicalInterchainToken(tokenAddress);
}

/// @notice Deploy a remote representation of the canonical token
/// @param tokenAddress The original token on this chain
/// @param destinationChain Target chain name
/// @param gasValue Gas payment for remote deployment
function deployCanonicalRemote(
    address tokenAddress,
    string calldata destinationChain,
    uint256 gasValue
) external payable returns (bytes32 tokenId) {
    tokenId = FACTORY.deployRemoteCanonicalInterchainToken{value: gasValue}(
        "",
        tokenAddress,
        destinationChain,
        gasValue
    );
}
```

## Gas Estimation

### Using the Axelar SDK

```typescript
import { AxelarQueryAPI, Environment } from "@axelar-network/axelarjs-sdk";

const axelarQuery = new AxelarQueryAPI({
  environment: Environment.MAINNET,
});

async function estimateGasFee(
  sourceChain: string,
  destinationChain: string,
  gasLimit: bigint
): Promise<bigint> {
  const gasFee = await axelarQuery.estimateGasFee(
    sourceChain,
    destinationChain,
    Number(gasLimit),
    "auto",
    undefined,
    undefined,
  );

  // gasFee is returned as a string in wei
  return BigInt(gasFee as string);
}

const fee = await estimateGasFee("ethereum", "arbitrum", 250000n);
```

### Using the GasService Contract Directly

```typescript
const gasServiceAbi = parseAbi([
  "function payNativeGasForContractCall(address sender, string calldata destinationChain, string calldata destinationAddress, bytes calldata payload, address refundAddress) payable",
  "function payNativeGasForContractCallWithToken(address sender, string calldata destinationChain, string calldata destinationAddress, bytes calldata payload, string calldata symbol, uint256 amount, address refundAddress) payable",
]);

const GAS_SERVICE: Address = "0x2d5d7d31F671F86C782533cc367F14109a082712";

async function payGasAndSend(
  destinationChain: string,
  destinationAddress: string,
  payload: `0x${string}`,
  gasValue: bigint
): Promise<`0x${string}`> {
  // Pay gas first
  const { request: gasRequest } = await ethereumClient.simulateContract({
    address: GAS_SERVICE,
    abi: gasServiceAbi,
    functionName: "payNativeGasForContractCall",
    args: [
      account.address,
      destinationChain,
      destinationAddress,
      payload,
      account.address,
    ],
    value: gasValue,
    account: account.address,
  });

  const gasHash = await walletClient.writeContract(gasRequest);
  const gasReceipt = await ethereumClient.waitForTransactionReceipt({ hash: gasHash });
  if (gasReceipt.status !== "success") throw new Error("Gas payment reverted");

  // Then call Gateway
  const gatewayAbi = parseAbi([
    "function callContract(string calldata destinationChain, string calldata contractAddress, bytes calldata payload) external",
  ]);

  const GATEWAY: Address = "0x4F4495243837681061C4743b74B3eEdf548D56A5";

  const { request: callRequest } = await ethereumClient.simulateContract({
    address: GATEWAY,
    abi: gatewayAbi,
    functionName: "callContract",
    args: [destinationChain, destinationAddress, payload],
    account: account.address,
  });

  const callHash = await walletClient.writeContract(callRequest);
  const callReceipt = await ethereumClient.waitForTransactionReceipt({ hash: callHash });
  if (callReceipt.status !== "success") throw new Error("callContract reverted");

  return callHash;
}
```

### Gas Estimation Guidelines

| Route | Typical Gas Limit | Estimated Cost (ETH) |
|-------|------------------|---------------------|
| Ethereum -> Arbitrum | 250,000 | ~0.0003 |
| Ethereum -> Base | 250,000 | ~0.0003 |
| Ethereum -> Polygon | 250,000 | ~0.0005 |
| Arbitrum -> Ethereum | 250,000 | ~0.002 |
| L2 -> L2 | 250,000 | ~0.0001 |

Costs vary with gas prices. Always use the SDK estimator for production.

## Deployment Pattern

### Multi-Chain Deploy Sequence

1. Deploy your `AxelarExecutable` contract on each chain (with that chain's Gateway and GasService)
2. Call `setTrustedRemote()` on every chain for every other chain's contract address
3. Test with a small GMP message before production use
4. For ITS: deploy token on origin chain first, then `deployRemoteInterchainToken` to each target

```typescript
const AXELAR_CONTRACTS: Record<string, { gateway: Address; gasService: Address }> = {
  ethereum: {
    gateway: "0x4F4495243837681061C4743b74B3eEdf548D56A5",
    gasService: "0x2d5d7d31F671F86C782533cc367F14109a082712",
  },
  arbitrum: {
    gateway: "0xe432150cce91c13a887f7D836923d5597adD8E31",
    gasService: "0x2d5d7d31F671F86C782533cc367F14109a082712",
  },
  base: {
    gateway: "0xe432150cce91c13a887f7D836923d5597adD8E31",
    gasService: "0x2d5d7d31F671F86C782533cc367F14109a082712",
  },
  optimism: {
    gateway: "0xe432150cce91c13a887f7D836923d5597adD8E31",
    gasService: "0x2d5d7d31F671F86C782533cc367F14109a082712",
  },
  polygon: {
    gateway: "0xe432150cce91c13a887f7D836923d5597adD8E31",
    gasService: "0x2d5d7d31F671F86C782533cc367F14109a082712",
  },
};

async function setTrustedRemotes(
  deployments: Map<string, Address>,
  sendTx: (chain: string, to: Address, data: `0x${string}`) => Promise<void>
) {
  const chains = [...deployments.keys()];
  const setRemoteAbi = parseAbi([
    "function setTrustedRemote(string calldata chain, string calldata addr) external",
  ]);

  for (const srcChain of chains) {
    for (const dstChain of chains) {
      if (srcChain === dstChain) continue;

      const srcContract = deployments.get(srcChain)!;
      const dstContract = deployments.get(dstChain)!;

      const data = encodeFunctionData({
        abi: setRemoteAbi,
        functionName: "setTrustedRemote",
        args: [dstChain, dstContract.toLowerCase()],
      });

      await sendTx(srcChain, srcContract, data);
    }
  }
}
```

### Foundry Deploy Script

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import {Script, console} from "forge-std/Script.sol";
import {MyGMPReceiver} from "../src/MyGMPReceiver.sol";

contract DeployGMP is Script {
    function run() external {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");
        address gateway = vm.envAddress("AXELAR_GATEWAY");
        address gasService = vm.envAddress("AXELAR_GAS_SERVICE");

        vm.startBroadcast(deployerKey);
        MyGMPReceiver receiver = new MyGMPReceiver(gateway, gasService);
        console.log("MyGMPReceiver deployed:", address(receiver));
        vm.stopBroadcast();
    }
}
```

## Tracking Cross-Chain Messages

### Using Axelarscan

After a GMP transaction, track delivery status at `axelarscan.io`. Enter the source transaction hash to see:
- Message submitted (source chain)
- Gas paid (source chain)
- Confirmed by validators
- Approved on destination Gateway
- Executed on destination chain

### Programmatic Status Check

```typescript
import { AxelarGMPRecoveryAPI, Environment } from "@axelar-network/axelarjs-sdk";

const gmpApi = new AxelarGMPRecoveryAPI({
  environment: Environment.MAINNET,
});

async function checkStatus(txHash: string): Promise<string> {
  const status = await gmpApi.queryTransactionStatus(txHash);
  // Returns: "source_gateway_called" | "confirmed" | "approved" | "executed" | "error"
  return status.status;
}
```

### Manually Execute a Stuck Message

If a message is approved but not executed (relayer missed it):

```typescript
async function manuallyExecute(txHash: string): Promise<void> {
  const result = await gmpApi.manualRelayToDestChain(txHash);
  if (!result.success) {
    throw new Error(`Manual relay failed: ${result.error}`);
  }
}
```

## Error Handling

### Common Reverts

| Error | Cause | Fix |
|-------|-------|-----|
| `NotApprovedByGateway` | Message not yet approved by validators | Wait for Axelar consensus, check axelarscan |
| `InvalidAddress` | Empty or malformed destination address string | Pass valid lowercase hex address string |
| `TokenDoesNotExist` | Token symbol not registered in Gateway | Use only Axelar-supported token symbols |
| `InsufficientBalance` | Contract does not hold enough tokens for `callContractWithToken` | Transfer and approve tokens to the sender contract first |
| `AlreadyExecuted` | Message already processed on destination | This is expected for replay protection -- no action needed |
| `NotSelf` | ITS function called externally that should be internal | Use the ITS SDK or Factory pattern instead of direct calls |

### Debugging Cross-Chain Failures

1. **Check source transaction on explorer.** If it reverted, the message was never submitted. Fix gas payment or Gateway call.

2. **Verify gas was paid.** Search for `GasPaidForContractCall` event on the source chain in the same transaction. If missing, gas was not paid and the message will not be relayed.

3. **Check axelarscan.io.** Enter the source tx hash. Status flow: `source_gateway_called` -> `confirmed` -> `approved` -> `executed`.

4. **If stuck at "confirmed"**, validators approved but the destination Gateway has not received the approval. This is rare and usually resolves automatically.

5. **If stuck at "approved"**, the relayer failed to execute. Use `manualRelayToDestChain()` from the SDK or submit the execute transaction manually.

6. **If "executed" but your logic failed**, the `_execute()` callback reverted. Debug your implementation -- check payload encoding matches decoding, check trusted remote is set.

```bash
# Verify Gateway has code
cast code 0x4F4495243837681061C4743b74B3eEdf548D56A5 --rpc-url $ETH_RPC_URL

# Check if a command is approved
cast call 0x4F4495243837681061C4743b74B3eEdf548D56A5 \
  "isCommandExecuted(bytes32)(bool)" <commandId> --rpc-url $ETH_RPC_URL

# Check token address for a symbol
cast call 0x4F4495243837681061C4743b74B3eEdf548D56A5 \
  "tokenAddresses(string)(address)" "axlUSDC" --rpc-url $ETH_RPC_URL
```

## Contract Addresses

> **Last verified:** 2025-05-01

### Gateway

| Chain | Address |
|-------|---------|
| Ethereum | `0x4F4495243837681061C4743b74B3eEdf548D56A5` |
| Arbitrum | `0xe432150cce91c13a887f7D836923d5597adD8E31` |
| Base | `0xe432150cce91c13a887f7D836923d5597adD8E31` |
| Optimism | `0xe432150cce91c13a887f7D836923d5597adD8E31` |
| Polygon | `0xe432150cce91c13a887f7D836923d5597adD8E31` |
| Avalanche | `0x5029C0EFf6C34351a0CEc334542cDb22c7928f78` |
| BNB Chain | `0x304acf330bbE08d1e512eefaa92F6a57871fD895` |
| Fantom | `0x304acf330bbE08d1e512eefaa92F6a57871fD895` |

### GasService

| Chain | Address |
|-------|---------|
| Ethereum | `0x2d5d7d31F671F86C782533cc367F14109a082712` |
| Arbitrum | `0x2d5d7d31F671F86C782533cc367F14109a082712` |
| Base | `0x2d5d7d31F671F86C782533cc367F14109a082712` |
| Optimism | `0x2d5d7d31F671F86C782533cc367F14109a082712` |
| Polygon | `0x2d5d7d31F671F86C782533cc367F14109a082712` |
| Avalanche | `0x2d5d7d31F671F86C782533cc367F14109a082712` |
| BNB Chain | `0x2d5d7d31F671F86C782533cc367F14109a082712` |

### Interchain Token Service (ITS)

| Chain | Address |
|-------|---------|
| Ethereum | `0xB5FB4BE02232B1bBA4dC8f81dc24C26980dE9e3C` |
| Arbitrum | `0xB5FB4BE02232B1bBA4dC8f81dc24C26980dE9e3C` |
| Base | `0xB5FB4BE02232B1bBA4dC8f81dc24C26980dE9e3C` |
| Optimism | `0xB5FB4BE02232B1bBA4dC8f81dc24C26980dE9e3C` |
| Polygon | `0xB5FB4BE02232B1bBA4dC8f81dc24C26980dE9e3C` |

### Interchain Token Factory

| Chain | Address |
|-------|---------|
| Ethereum | `0x83a93500d23Fbc3e82B410aD07A6a9F7A0670D12` |
| Arbitrum | `0x83a93500d23Fbc3e82B410aD07A6a9F7A0670D12` |
| Base | `0x83a93500d23Fbc3e82B410aD07A6a9F7A0670D12` |
| Optimism | `0x83a93500d23Fbc3e82B410aD07A6a9F7A0670D12` |
| Polygon | `0x83a93500d23Fbc3e82B410aD07A6a9F7A0670D12` |

## References

- [Axelar Documentation](https://docs.axelar.dev/)
- [GMP Developer Guide](https://docs.axelar.dev/dev/general-message-passing/overview)
- [Interchain Token Service](https://docs.axelar.dev/dev/send-tokens/interchain-tokens/intro)
- [Axelar GMP SDK (Solidity)](https://github.com/axelarnetwork/axelar-gmp-sdk-solidity)
- [Axelar JS SDK](https://github.com/axelarnetwork/axelarjs-sdk)
- [Axelarscan Explorer](https://axelarscan.io)
- [Contract Addresses](https://docs.axelar.dev/resources/contract-addresses/mainnet)
- [Supported Chains](https://docs.axelar.dev/resources/contract-addresses/mainnet)
- [Gas Estimation API](https://docs.axelar.dev/dev/general-message-passing/gas-services/pay-gas)
