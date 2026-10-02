---
name: hyperlane
description: Hyperlane permissionless interoperability — Mailbox messaging, Interchain Security Modules (ISM), Warp Routes for token bridging, hooks, interchain accounts, and permissionless deployment to any chain. Covers Hyperlane SDK, contract interfaces, and custom security configurations.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Cross-Chain
tags:
  - hyperlane
  - cross-chain
  - messaging
  - interoperability
  - warp-routes
  - ism
---

# Hyperlane

Hyperlane is the first permissionless interoperability layer. Unlike bridge protocols that require governance votes or committee approvals to add new chains, anyone can deploy Hyperlane to any blockchain — EVM, Cosmos, Sealevel (Solana), or Move — without permission. Messages are secured by configurable Interchain Security Modules (ISMs), giving developers sovereign control over their cross-chain security model rather than trusting a single validator set.

## What You Probably Got Wrong

> AI agents confuse Hyperlane with traditional bridges and get ISM, Warp Route, and messaging patterns wrong. These are the critical corrections.

- **Hyperlane is permissionless — you CAN deploy to chains not officially supported.** Unlike LayerZero or Wormhole, Hyperlane does not require a governance vote to expand to new chains. You deploy the Mailbox, ISM, and ValidatorAnnounce contracts yourself, run your own validators, and your chain is live. This is the core differentiator.
- **ISMs (Interchain Security Modules) are composable — you are not locked into one security model.** You can combine MultisigISM, RoutingISM, and AggregationISM to build custom security stacks. A message can require 3-of-5 validators AND an optimistic fraud proof AND a ZK proof. Security is modular, not monolithic.
- **Warp Routes are NOT the same as bridges.** Warp Routes are token-specific contract pairs deployed on origin and destination chains. A Warp Route for USDC on Ethereum<->Arbitrum is a separate deployment from USDC on Ethereum<->Optimism. Each route has its own collateral/synthetic relationship and ISM configuration.
- **`dispatch()` returns a message ID, NOT a delivery confirmation.** The `bytes32` returned by `dispatch()` is a unique message identifier. It does NOT mean the message was delivered. Delivery happens asynchronously when a relayer submits the message to the destination chain's Mailbox, which then calls `handle()` on the recipient.
- **Default ISM may differ per chain — always check what ISM your messages route through.** Each Mailbox has a `defaultIsm()` that applies when the recipient contract does not specify its own ISM via `interchainSecurityModule()`. The default ISM is set by the Mailbox owner and varies across deployments.
- **`handle()` function signature is strict: `handle(uint32 _origin, bytes32 _sender, bytes _body)`.** The `_sender` is `bytes32`, not `address`. For EVM origins, the sender address is left-padded with 12 zero bytes to fill 32 bytes. If you cast incorrectly, sender validation will fail silently.
- **Sender addresses are `bytes32` padded, not `address` type.** When dispatching from EVM, `msg.sender` is converted to `bytes32` via left-padding. When receiving, you must convert back: `address(uint160(uint256(_sender)))`. Getting this wrong means your access control checks will always fail.
- **Message delivery is NOT guaranteed — relayers must be running for the destination chain.** Hyperlane's default relayer infrastructure covers major chains, but if you deploy to a new chain, YOU must run a relayer. No relayer = messages sit in the origin Mailbox permanently.
- **Interchain gas payment is separate from dispatch.** You must pay for destination chain gas via the `InterchainGasPaymaster` hook or a post-dispatch hook. If you skip this, the default relayer has no incentive to deliver your message. Use `quoteDispatch()` to estimate the fee.
- **Hyperlane V3 is the current version.** V3 introduced hooks (post-dispatch hooks for gas payment, custom logic), replaced the old `InterchainGasPaymaster.payForGas()` pattern with hook-based gas payment, and uses `mailbox.dispatch()` with metadata and hook parameters.

## Quick Start

### Installation

```bash
npm install @hyperlane-xyz/sdk @hyperlane-xyz/core viem
```

### Client Setup

```typescript
import { createPublicClient, createWalletClient, http } from "viem";
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

### Minimal Message Dispatch

```typescript
import { type Address, encodePacked, pad, toHex } from "viem";

const MAILBOX = "0xc005dc82818d67AF737725bD4bf75435d065D239" as const;

const mailboxAbi = [
  {
    name: "dispatch",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_destinationDomain", type: "uint32" },
      { name: "_recipientAddress", type: "bytes32" },
      { name: "_messageBody", type: "bytes" },
    ],
    outputs: [{ name: "messageId", type: "bytes32" }],
  },
  {
    name: "quoteDispatch",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "_destinationDomain", type: "uint32" },
      { name: "_recipientAddress", type: "bytes32" },
      { name: "_messageBody", type: "bytes" },
    ],
    outputs: [{ name: "fee", type: "uint256" }],
  },
] as const;

// Hyperlane domain ID for Arbitrum
const ARBITRUM_DOMAIN = 42161;

// Recipient contract on Arbitrum (must implement IMessageRecipient)
const recipientAddress = pad(
  "0xYourRecipientContractAddress" as Address,
  { size: 32 }
);

const messageBody = toHex("Hello from Ethereum");

// Quote the interchain gas fee
const fee = await publicClient.readContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "quoteDispatch",
  args: [ARBITRUM_DOMAIN, recipientAddress, messageBody],
});

// Dispatch the message with gas payment
const { request } = await publicClient.simulateContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "dispatch",
  args: [ARBITRUM_DOMAIN, recipientAddress, messageBody],
  value: fee,
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Dispatch reverted");
```

## Core Concepts

### Mailbox

The Mailbox is the core contract on every Hyperlane-enabled chain. It handles message dispatch (sending) and message processing (receiving). Every chain has exactly one Mailbox. Messages dispatched through the Mailbox are assigned a unique `bytes32` message ID and stored in an incremental Merkle tree.

### Domain IDs

Hyperlane identifies chains by `uint32` domain IDs, not chain IDs. For EVM chains, the domain ID typically matches the chain ID, but this is not guaranteed for non-EVM chains.

| Chain | Domain ID |
|-------|-----------|
| Ethereum | `1` |
| Arbitrum | `42161` |
| Optimism | `10` |
| Base | `8453` |
| Polygon | `137` |

### Interchain Security Module (ISM)

ISMs are modular contracts that verify the authenticity of inbound messages. When the Mailbox receives a message for delivery, it queries the recipient contract's `interchainSecurityModule()` function. If the recipient does not implement this, the Mailbox's `defaultIsm()` is used.

ISMs implement a single interface:

```solidity
interface IInterchainSecurityModule {
    function moduleType() external view returns (uint8);
    function verify(
        bytes calldata _metadata,
        bytes calldata _message
    ) external returns (bool);
}
```

### Validators

Validators watch the origin chain Mailbox for dispatched messages, sign attestations of the Merkle root, and publish signatures. Relayers collect these signatures and submit them as metadata when delivering messages on the destination chain. The MultisigISM verifies these signatures against a configured validator set.

### Relayers

Relayers are off-chain agents that deliver messages from origin to destination. They watch origin Mailboxes for `Dispatch` events, gather validator signatures (metadata), and call `process()` on the destination Mailbox. Hyperlane operates default relayers for supported chains, but anyone can run a relayer.

### Hooks

Post-dispatch hooks execute logic after a message is dispatched. The most important hook is the `InterchainGasPaymaster`, which collects payment for destination chain gas. Hooks are configured per-Mailbox and can be overridden per-dispatch.

## Sending & Receiving Messages

### Dispatch Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IMailbox {
    /// @notice Dispatch a message to a destination domain
    /// @param _destinationDomain The domain ID of the destination chain
    /// @param _recipientAddress The recipient contract (bytes32, left-padded for EVM)
    /// @param _messageBody Arbitrary bytes payload
    /// @return messageId Unique message identifier
    function dispatch(
        uint32 _destinationDomain,
        bytes32 _recipientAddress,
        bytes calldata _messageBody
    ) external payable returns (bytes32 messageId);

    /// @notice Quote the fee for dispatching a message
    function quoteDispatch(
        uint32 _destinationDomain,
        bytes32 _recipientAddress,
        bytes calldata _messageBody
    ) external view returns (uint256 fee);

    /// @notice Process a delivered message (called by relayer)
    function process(
        bytes calldata _metadata,
        bytes calldata _message
    ) external;
}
```

### IMessageRecipient Interface

Every contract that receives Hyperlane messages must implement `IMessageRecipient`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IMessageRecipient {
    /// @notice Handle a message delivered by the Mailbox
    /// @param _origin Domain ID of the source chain
    /// @param _sender Address of the sender (bytes32, left-padded for EVM)
    /// @param _body The message payload
    function handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _body
    ) external payable;
}
```

### Address Conversion Utilities

```solidity
/// @notice Convert an EVM address to bytes32 (left-pad with zeros)
function addressToBytes32(address _addr) internal pure returns (bytes32) {
    return bytes32(uint256(uint160(_addr)));
}

/// @notice Convert bytes32 back to an EVM address
function bytes32ToAddress(bytes32 _buf) internal pure returns (address) {
    return address(uint160(uint256(_buf)));
}
```

### TypeScript Address Conversion

```typescript
import { pad, type Address } from "viem";

function addressToBytes32(addr: Address): `0x${string}` {
  return pad(addr, { size: 32 });
}

function bytes32ToAddress(buf: `0x${string}`): Address {
  return `0x${buf.slice(26)}` as Address;
}
```

### Sending a Message (TypeScript)

```typescript
import { pad, toHex, type Address, encodeAbiParameters } from "viem";

const MAILBOX = "0xc005dc82818d67AF737725bD4bf75435d065D239" as const;
const DESTINATION_DOMAIN = 42161; // Arbitrum

const recipient: Address = "0xYourRecipientContract";
const recipientBytes32 = pad(recipient, { size: 32 });

// Encode a structured payload
const payload = encodeAbiParameters(
  [
    { name: "action", type: "uint8" },
    { name: "amount", type: "uint256" },
    { name: "recipient", type: "address" },
  ],
  [1, 1000000000000000000n, account.address]
);

const fee = await publicClient.readContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "quoteDispatch",
  args: [DESTINATION_DOMAIN, recipientBytes32, payload],
});

const { request } = await publicClient.simulateContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "dispatch",
  args: [DESTINATION_DOMAIN, recipientBytes32, payload],
  value: fee,
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Dispatch reverted");
```

## Warp Routes

Warp Routes are Hyperlane's token bridging primitive. They consist of paired contracts on origin and destination chains that lock/burn tokens on one side and mint/unlock on the other.

### Warp Route Types

| Type | Origin Behavior | Destination Behavior | Use Case |
|------|----------------|---------------------|----------|
| `HypERC20Collateral` | Locks tokens in contract | Mints synthetic `HypERC20` | Bridge existing ERC-20 |
| `HypERC20` | Burns synthetic tokens | Mints synthetic tokens | Synthetic side of a collateral route |
| `HypNative` | Locks native ETH | Mints synthetic `HypERC20` | Bridge native gas token |
| `HypNativeScaled` | Locks native token (scaled) | Mints scaled synthetic | When decimals differ across chains |

### Deploying a Warp Route (SDK)

```typescript
import { HyperlaneCore, WarpRouteDeployConfig } from "@hyperlane-xyz/sdk";

// Warp Route config: bridge USDC from Ethereum to Arbitrum
const warpConfig: WarpRouteDeployConfig = {
  ethereum: {
    type: "collateral",
    token: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC on Ethereum
    mailbox: "0xc005dc82818d67AF737725bD4bf75435d065D239",
    interchainSecurityModule: "0x...", // optional: custom ISM
  },
  arbitrum: {
    type: "synthetic",
    mailbox: "0x979Ca5202784112f4738403dBec5D0F3B9daabB9",
    interchainSecurityModule: "0x...", // optional: custom ISM
  },
};
```

### Transferring Tokens via Warp Route

```typescript
const warpRouteAbi = [
  {
    name: "transferRemote",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_destination", type: "uint32" },
      { name: "_recipient", type: "bytes32" },
      { name: "_amountOrId", type: "uint256" },
    ],
    outputs: [{ name: "messageId", type: "bytes32" }],
  },
  {
    name: "quoteGasPayment",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "_destinationDomain", type: "uint32" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const WARP_ROUTE_COLLATERAL = "0xYourWarpRouteCollateralContract" as const;
const ARBITRUM_DOMAIN = 42161;
const amount = 1000_000000n; // 1000 USDC (6 decimals)

// ERC-20 approval to Warp Route contract
const erc20Abi = [
  {
    name: "approve",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as const;

const { request: approveRequest } = await publicClient.simulateContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [WARP_ROUTE_COLLATERAL, amount],
  account: account.address,
});
const approveHash = await walletClient.writeContract(approveRequest);
const approveReceipt = await publicClient.waitForTransactionReceipt({
  hash: approveHash,
});
if (approveReceipt.status !== "success") throw new Error("Approval reverted");

// Quote interchain gas
const gasFee = await publicClient.readContract({
  address: WARP_ROUTE_COLLATERAL,
  abi: warpRouteAbi,
  functionName: "quoteGasPayment",
  args: [ARBITRUM_DOMAIN],
});

// Execute cross-chain transfer
const recipientBytes32 = pad(account.address, { size: 32 });

const { request: transferRequest } = await publicClient.simulateContract({
  address: WARP_ROUTE_COLLATERAL,
  abi: warpRouteAbi,
  functionName: "transferRemote",
  args: [ARBITRUM_DOMAIN, recipientBytes32, amount],
  value: gasFee,
  account: account.address,
});

const transferHash = await walletClient.writeContract(transferRequest);
const transferReceipt = await publicClient.waitForTransactionReceipt({
  hash: transferHash,
});
if (transferReceipt.status !== "success") throw new Error("Transfer reverted");
```

## Interchain Security Modules (ISM)

### ISM Types

| Type | Module Type ID | Security Model | When to Use |
|------|---------------|----------------|-------------|
| `MultisigISM` | `3` | M-of-N validator signatures | Default for most deployments |
| `RoutingISM` | `4` | Routes to different ISMs per origin domain | Different security per source chain |
| `AggregationISM` | `6` | Requires multiple ISMs to pass (AND logic) | Defense in depth — combine models |
| `OptimisticISM` | Custom | Optimistic verification with fraud proofs | Lower latency, higher trust assumption |
| `WasmISM` | Custom | Custom verification logic in WASM | Non-EVM verification, ZK proofs |

### Configuring a MultisigISM

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {StaticMultisigISMFactory} from "@hyperlane-xyz/core/contracts/isms/multisig/StaticMultisigISMFactory.sol";

// Deploy a MultisigISM that requires 3-of-5 validator signatures
// for messages from Ethereum (domain 1)
address[] memory validators = new address[](5);
validators[0] = 0x1111111111111111111111111111111111111111;
validators[1] = 0x2222222222222222222222222222222222222222;
validators[2] = 0x3333333333333333333333333333333333333333;
validators[3] = 0x4444444444444444444444444444444444444444;
validators[4] = 0x5555555555555555555555555555555555555555;

uint8 threshold = 3;

IStaticMultisigISMFactory factory = IStaticMultisigISMFactory(
    MULTISIG_ISM_FACTORY_ADDRESS
);
address ism = factory.deploy(validators, threshold);
```

### Setting a Custom ISM on Your Recipient

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {IInterchainSecurityModule} from "@hyperlane-xyz/core/contracts/interfaces/IInterchainSecurityModule.sol";
import {IMessageRecipient} from "@hyperlane-xyz/core/contracts/interfaces/IMessageRecipient.sol";

contract MyRecipient is IMessageRecipient {
    IInterchainSecurityModule public interchainSecurityModule;
    address public immutable mailbox;

    error Unauthorized();
    error InvalidOrigin(uint32 origin);

    event MessageReceived(uint32 indexed origin, bytes32 indexed sender, bytes body);

    constructor(address _mailbox, address _ism) {
        mailbox = _mailbox;
        interchainSecurityModule = IInterchainSecurityModule(_ism);
    }

    function handle(
        uint32 _origin,
        bytes32 _sender,
        bytes calldata _body
    ) external payable override {
        if (msg.sender != mailbox) revert Unauthorized();

        emit MessageReceived(_origin, _sender, _body);
    }
}
```

### AggregationISM (Combine Multiple Security Models)

```solidity
import {StaticAggregationISMFactory} from "@hyperlane-xyz/core/contracts/isms/aggregation/StaticAggregationISMFactory.sol";

// Require BOTH a MultisigISM AND a custom verification ISM to pass
address[] memory modules = new address[](2);
modules[0] = address(multisigIsm);    // 3-of-5 validator signatures
modules[1] = address(customVerifier); // additional verification

uint8 threshold = 2; // all modules must pass

IStaticAggregationISMFactory factory = IStaticAggregationISMFactory(
    AGGREGATION_ISM_FACTORY_ADDRESS
);
address aggregationIsm = factory.deploy(modules, threshold);
```

### RoutingISM (Per-Origin Security)

```solidity
import {DomainRoutingISMFactory} from "@hyperlane-xyz/core/contracts/isms/routing/DomainRoutingISMFactory.sol";

// Use different ISMs for messages from different origin chains
uint32[] memory domains = new uint32[](2);
domains[0] = 1;     // Ethereum
domains[1] = 42161;  // Arbitrum

address[] memory isms = new address[](2);
isms[0] = address(ethereumMultisigIsm);  // stricter for Ethereum
isms[1] = address(arbitrumMultisigIsm);  // different validators for Arbitrum

IDomainRoutingISMFactory factory = IDomainRoutingISMFactory(
    DOMAIN_ROUTING_ISM_FACTORY_ADDRESS
);
address routingIsm = factory.deploy(msg.sender, domains, isms);
```

## Hooks

### Post-Dispatch Hooks

Hooks execute after `dispatch()` and before the function returns. The primary use is interchain gas payment, but hooks support arbitrary logic.

```solidity
interface IPostDispatchHook {
    /// @notice Type identifier for this hook
    function hookType() external view returns (uint8);

    /// @notice Returns whether the hook supports metadata
    function supportsMetadata(
        bytes calldata metadata
    ) external view returns (bool);

    /// @notice Post-dispatch hook logic
    function postDispatch(
        bytes calldata metadata,
        bytes calldata message
    ) external payable;

    /// @notice Quote the fee for this hook
    function quoteDispatch(
        bytes calldata metadata,
        bytes calldata message
    ) external view returns (uint256);
}
```

### Dispatch with Custom Hook and Metadata

```solidity
interface IMailboxV3 {
    /// @notice Dispatch with explicit hook and metadata
    function dispatch(
        uint32 _destinationDomain,
        bytes32 _recipientAddress,
        bytes calldata _messageBody,
        bytes calldata _hookMetadata,
        IPostDispatchHook _hook
    ) external payable returns (bytes32 messageId);
}
```

### Interchain Gas Payment

```typescript
// The standard dispatch with value covers gas payment via the default hook
const fee = await publicClient.readContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "quoteDispatch",
  args: [destinationDomain, recipientBytes32, messageBody],
});

// Send dispatch with the quoted fee as msg.value
const { request } = await publicClient.simulateContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "dispatch",
  args: [destinationDomain, recipientBytes32, messageBody],
  value: fee,
  account: account.address,
});
```

## Interchain Accounts

Interchain Accounts (ICA) allow you to execute transactions on remote chains. When you send an ICA call from Chain A, Hyperlane creates a deterministic account on Chain B that only Chain A can control. This account can call any contract on Chain B.

### ICA Call Structure

```solidity
struct CallLib.Call {
    address to;       // target contract on destination
    uint256 value;    // ETH value to send
    bytes data;       // calldata to execute
}
```

### Executing a Remote Transaction

```typescript
const ICA_ROUTER = "0xYourICARouterAddress" as const;

const icaRouterAbi = [
  {
    name: "callRemote",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_destinationDomain", type: "uint32" },
      {
        name: "_calls",
        type: "tuple[]",
        components: [
          { name: "to", type: "address" },
          { name: "value", type: "uint256" },
          { name: "data", type: "bytes" },
        ],
      },
    ],
    outputs: [{ name: "messageId", type: "bytes32" }],
  },
  {
    name: "quoteGasPayment",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "_destinationDomain", type: "uint32" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "getRemoteInterchainAccount",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "_destination", type: "uint32" },
      { name: "_owner", type: "address" },
      { name: "_router", type: "address" },
      { name: "_ism", type: "address" },
    ],
    outputs: [{ name: "", type: "address" }],
  },
] as const;

import { encodeFunctionData } from "viem";

// Encode the call you want to execute on the destination chain
const remoteCalldata = encodeFunctionData({
  abi: [
    {
      name: "transfer",
      type: "function",
      stateMutability: "nonpayable",
      inputs: [
        { name: "to", type: "address" },
        { name: "amount", type: "uint256" },
      ],
      outputs: [{ name: "", type: "bool" }],
    },
  ],
  functionName: "transfer",
  args: ["0xRecipientAddress" as Address, 1000_000000n],
});

const ARBITRUM_DOMAIN = 42161;

const gasFee = await publicClient.readContract({
  address: ICA_ROUTER,
  abi: icaRouterAbi,
  functionName: "quoteGasPayment",
  args: [ARBITRUM_DOMAIN],
});

const { request } = await publicClient.simulateContract({
  address: ICA_ROUTER,
  abi: icaRouterAbi,
  functionName: "callRemote",
  args: [
    ARBITRUM_DOMAIN,
    [
      {
        to: "0xTokenContractOnArbitrum" as Address,
        value: 0n,
        data: remoteCalldata,
      },
    ],
  ],
  value: gasFee,
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("ICA call reverted");
```

### Getting Your ICA Address

The ICA address on the destination chain is deterministic based on your origin address, the ICA router, and the ISM:

```typescript
const icaAddress = await publicClient.readContract({
  address: ICA_ROUTER,
  abi: icaRouterAbi,
  functionName: "getRemoteInterchainAccount",
  args: [
    ARBITRUM_DOMAIN,
    account.address,
    ICA_ROUTER,
    "0x0000000000000000000000000000000000000000", // default ISM
  ],
});
```

## Permissionless Deployment

### Deploy Hyperlane to a New Chain

Hyperlane can be deployed to any chain without permission. The process:

1. **Deploy core contracts** — Mailbox, ProxyAdmin, ISM factories
2. **Configure default ISM** — Set the security model for inbound messages
3. **Deploy ValidatorAnnounce** — Validators publish their signing locations here
4. **Run validators** — At least one validator must attest to messages
5. **Run a relayer** — Delivers messages from/to your chain

### Using the Hyperlane CLI

```bash
# Install the CLI
npm install -g @hyperlane-xyz/cli

# Initialize a chain config for your new chain
hyperlane config create chain

# Deploy core contracts
hyperlane deploy core \
  --chain your-chain-name \
  --key $PRIVATE_KEY

# Deploy a Warp Route
hyperlane deploy warp \
  --config warp-route-config.yaml \
  --key $PRIVATE_KEY

# Run a validator
hyperlane validator \
  --chain your-chain-name \
  --key $VALIDATOR_PRIVATE_KEY

# Run a relayer
hyperlane relayer \
  --chains your-chain-name,ethereum,arbitrum
```

### Chain Configuration

```yaml
# chain-config.yaml
yourchain:
  chainId: 123456
  domainId: 123456
  name: yourchain
  protocol: ethereum
  rpcUrls:
    - http: https://rpc.yourchain.com
  nativeToken:
    name: ETH
    symbol: ETH
    decimals: 18
  blockExplorers:
    - name: YourChainExplorer
      url: https://explorer.yourchain.com
      apiUrl: https://api.explorer.yourchain.com/api
```

## Fee Estimation

### quoteDispatch

Always call `quoteDispatch()` before dispatching to determine the required `msg.value` for interchain gas payment:

```typescript
const fee = await publicClient.readContract({
  address: MAILBOX,
  abi: [
    {
      name: "quoteDispatch",
      type: "function",
      stateMutability: "view",
      inputs: [
        { name: "_destinationDomain", type: "uint32" },
        { name: "_recipientAddress", type: "bytes32" },
        { name: "_messageBody", type: "bytes" },
      ],
      outputs: [{ name: "fee", type: "uint256" }],
    },
  ] as const,
  functionName: "quoteDispatch",
  args: [destinationDomain, recipientBytes32, messageBody],
});

// Always send at least the quoted fee — overpayment is refunded by some hooks
const { request } = await publicClient.simulateContract({
  address: MAILBOX,
  abi: mailboxAbi,
  functionName: "dispatch",
  args: [destinationDomain, recipientBytes32, messageBody],
  value: fee,
  account: account.address,
});
```

### Gas Overhead Estimation

Interchain gas fees account for:
- Destination chain gas price (estimated by the relayer)
- `handle()` execution gas on the destination
- ISM verification gas (signature checks)
- Relayer operational overhead

For large payloads or complex `handle()` logic, gas costs scale linearly. Estimate your `handle()` gas usage on a fork and add a safety margin.

## Contract Addresses

> **Last verified:** February 2026

### Core Contracts

| Contract | Ethereum | Arbitrum | Base | Optimism | Polygon |
|----------|----------|----------|------|----------|---------|
| Mailbox | `0xc005dc82818d67AF737725bD4bf75435d065D239` | `0x979Ca5202784112f4738403dBec5D0F3B9daabB9` | `0xeA87ae93Fa0019a82A727bfd3eBd1cFCa8f64f1D` | `0xd4C1905BB739D293F7a14F97241A65a7458291c3` | `0x5d934f4e2f797775e53561bB72aca21ba36B96BB` |
| DefaultISM | `0x6b1bb4ce664Bb4164AEB4d3D2E7DE7450DD8084C` | `0x8105a095368f1a184CceA86cDB98920e74Ffb992` | `0x60448b880c8Aa3fef44dCcc2CaAB4FD178DeE46f` | `0xAa4Fe29e0db0D2891352e2770b400B1e0B0C2D67` | `0x9C2ae13212B89Ced2027c2a7Ef26eb3eEf143867` |
| InterchainGasPaymaster | `0x6cA0B6D22da47f091B7613C7A727eC00ac3486d2` | `0x3b6044acd6767f017e99318AA6Ef93b7B06A5a22` | `0xc3F23848Ed2e04C0c6d41bd7804fa8f89F940B94` | `0xD8A76C4D91fCbB7Cc8eA795DFDF870E48368995C` | `0x0071740Bf129b05C4684abfbBeD248D80971cce2` |
| ValidatorAnnounce | `0x9bBdef63594D5FFc2f370Fe52115DdAAFBA66D76` | `0x9bBdef63594D5FFc2f370Fe52115DdAAFBA66D76` | `0x9bBdef63594D5FFc2f370Fe52115DdAAFBA66D76` | `0x9bBdef63594D5FFc2f370Fe52115DdAAFBA66D76` | `0x9bBdef63594D5FFc2f370Fe52115DdAAFBA66D76` |

### ISM Factory Contracts

| Contract | Ethereum | Arbitrum |
|----------|----------|----------|
| StaticMultisigISMFactory | `0x8b83fefd896fAa52057798f6426E9f0B080FCCcE` | `0x8b83fefd896fAa52057798f6426E9f0B080FCCcE` |
| StaticAggregationISMFactory | `0x8F7454AC98228f3504bB91eA3D0281e457E00385` | `0x8F7454AC98228f3504bB91eA3D0281e457E00385` |
| DomainRoutingISMFactory | `0xC2E36cd6e32e194EE11f15D9273B64461A4D694A` | `0xC2E36cd6e32e194EE11f15D9273B64461A4D694A` |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `!msg.value` | Insufficient gas payment sent with dispatch | Call `quoteDispatch()` and send the returned fee as `msg.value` |
| `!module` | ISM verification failed | Check validator signatures, ensure correct ISM is configured |
| `!recipient.ism` | Recipient's ISM address is invalid | Verify recipient implements `interchainSecurityModule()` returning a valid address |
| `delivered` | Message already processed on destination | This is idempotent — the message was already delivered. No action needed |
| `!paused` | Mailbox is paused | Wait for Mailbox owner to unpause, or use an alternative Mailbox |
| `!threshold` | MultisigISM threshold not met | Ensure enough validators have signed — check validator set and threshold |
| `!signer` | Validator signature is invalid | Verify the signing validator is in the ISM's validator set |

## Security

### Sender Verification (Non-Negotiable)

Always verify `msg.sender == mailbox` in `handle()`. Without this check, anyone can call your recipient contract directly, bypassing cross-chain verification.

```solidity
function handle(
    uint32 _origin,
    bytes32 _sender,
    bytes calldata _body
) external payable override {
    if (msg.sender != address(mailbox)) revert Unauthorized();
    // Safe to process
}
```

### Origin and Sender Validation

Validate both the origin domain and the sender address to prevent unauthorized cross-chain calls:

```solidity
error UnauthorizedSender(uint32 origin, bytes32 sender);

mapping(uint32 => bytes32) public authorizedSenders;

function handle(
    uint32 _origin,
    bytes32 _sender,
    bytes calldata _body
) external payable override {
    if (msg.sender != address(mailbox)) revert Unauthorized();
    if (authorizedSenders[_origin] != _sender) {
        revert UnauthorizedSender(_origin, _sender);
    }
    // Safe to process
}
```

### ISM Selection

- For high-value operations: use `AggregationISM` combining MultisigISM + an additional verification layer
- For standard messaging: `MultisigISM` with a reputable validator set and appropriate threshold
- For per-chain granularity: `RoutingISM` to apply different security per origin chain
- Never rely solely on the default ISM for high-value operations — deploy your own

## References

- [Hyperlane Documentation](https://docs.hyperlane.xyz)
- [Hyperlane GitHub](https://github.com/hyperlane-xyz/hyperlane-monorepo)
- [Hyperlane Explorer](https://explorer.hyperlane.xyz)
- [Hyperlane Registry (chain/contract addresses)](https://github.com/hyperlane-xyz/hyperlane-registry)
- [@hyperlane-xyz/sdk](https://www.npmjs.com/package/@hyperlane-xyz/sdk)
- [@hyperlane-xyz/core](https://www.npmjs.com/package/@hyperlane-xyz/core)
- [@hyperlane-xyz/cli](https://www.npmjs.com/package/@hyperlane-xyz/cli)
- [Warp Route Documentation](https://docs.hyperlane.xyz/docs/guides/deploy-warp-route)
- [ISM Documentation](https://docs.hyperlane.xyz/docs/reference/ISM)
