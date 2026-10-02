---
name: arbitrum
description: Arbitrum Nitro L2 development — deployment, cross-chain messaging (Retryable Tickets), Orbit chains, ArbOS precompiles, bridging, and gas model differences from Ethereum.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: arbitrum
  category: L2 & Alt-L1
tags:
  - arbitrum
  - nitro
  - layer-2
  - optimistic-rollup
  - orbit
---

# Arbitrum

Arbitrum is the largest Ethereum L2 by TVL, running an optimistic rollup via the Nitro execution engine. Nitro compiles a modified Geth (go-ethereum) to WASM, enabling full EVM equivalence with fraud proofs. Arbitrum One targets general-purpose DeFi, Arbitrum Nova uses AnyTrust (data availability committee) for high-throughput gaming/social, and Orbit lets teams launch custom L3s settling to Arbitrum.

## What You Probably Got Wrong

> AI models trained before late 2024 carry stale assumptions about Arbitrum. These corrections are critical.

- **`block.number` returns the L1 block number, not L2** — On Arbitrum, `block.number` in Solidity returns the L1 Ethereum block number at the time the sequencer processed the transaction. Use `ArbSys(0x64).arbBlockNumber()` for the actual L2 block number.
- **`block.timestamp` is the L1 timestamp** — Same issue. `block.timestamp` reflects L1 time. For L2ley timing use `ArbSys(0x64).arbBlockNumber()` and correlate.
- **Arbitrum does NOT have the same gas model as Ethereum** — Every Arbitrum transaction pays two gas components: (1) L2 execution gas (similar to Ethereum but cheaper), and (2) L1 data posting cost (calldata compressed and posted to Ethereum). The L1 component often dominates for data-heavy transactions. Use `NodeInterface.gasEstimateComponents()` to get the breakdown.
- **You need `--legacy` for Foundry deployments** — Arbitrum's sequencer does not support EIP-1559 type-2 transactions natively in forge scripts. Use `--legacy` flag or your deployment will fail with a cryptic RPC error.
- **`msg.sender` in cross-chain calls is aliased** — When an L1 contract sends a message to L2 via retryable tickets, `msg.sender` on L2 is NOT the L1 contract address. It is the L1 address + `0x1111000000000000000000000000000000001111` (the "address alias"). This prevents L1/L2 address collision attacks.
- **Retryable tickets can fail silently** — An L1-to-L2 retryable ticket that runs out of gas on L2 does NOT revert on L1. It sits in the retry buffer for 7 days. You must monitor and manually redeem failed retryables, or your cross-chain message is lost after the TTL.
- **Withdrawals take 7 days, not minutes** — L2-to-L1 messages go through the optimistic rollup challenge period. After calling `ArbSys.sendTxToL1()`, the user must wait ~7 days, then execute the message on L1 via the Outbox contract. There is no fast path in the native bridge.
- **There is no mempool** — Arbitrum uses a centralized sequencer that orders transactions on a first-come-first-served basis. There is no traditional mempool, so MEV extraction works differently (no frontrunning via gas price bidding).

## Quick Start

### Chain Configuration

```typescript
import { defineChain } from "viem";
import { arbitrum, arbitrumNova, arbitrumSepolia } from "viem/chains";

// Arbitrum One — mainnet
// Chain ID: 42161
// RPC: https://arb1.arbitrum.io/rpc (public, rate-limited)

// Arbitrum Nova — AnyTrust chain for gaming/social
// Chain ID: 42170
// RPC: https://nova.arbitrum.io/rpc

// Arbitrum Sepolia — testnet
// Chain ID: 421614
// RPC: https://sepolia-rollup.arbitrum.io/rpc
```

### Client Setup

```typescript
import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { arbitrum } from "viem/chains";

const publicClient = createPublicClient({
  chain: arbitrum,
  transport: http(process.env.ARBITRUM_RPC_URL),
});

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const walletClient = createWalletClient({
  account,
  chain: arbitrum,
  transport: http(process.env.ARBITRUM_RPC_URL),
});
```

## Chain Details

| Property | Arbitrum One | Arbitrum Nova | Arbitrum Sepolia |
|----------|-------------|---------------|-----------------|
| Chain ID | 42161 | 42170 | 421614 |
| RPC | `https://arb1.arbitrum.io/rpc` | `https://nova.arbitrum.io/rpc` | `https://sepolia-rollup.arbitrum.io/rpc` |
| Explorer | `https://arbiscan.io` | `https://nova.arbiscan.io` | `https://sepolia.arbiscan.io` |
| Bridge | `https://bridge.arbitrum.io` | `https://bridge.arbitrum.io` | `https://bridge.arbitrum.io` |
| Native Token | ETH | ETH | ETH |
| Block Time | ~0.25s | ~0.25s | ~0.25s |
| Finality | ~7 days (challenge period) | ~7 days | ~7 days |

## Deployment

### Foundry Deployment

The `--legacy` flag is required — Arbitrum's sequencer does not natively support EIP-1559 type-2 transaction envelopes in forge broadcast.

```bash
# Deploy to Arbitrum One
forge create src/MyContract.sol:MyContract \
  --rpc-url $ARBITRUM_RPC_URL \
  --private-key $PRIVATE_KEY \
  --legacy

# Deploy to Arbitrum Sepolia (testnet)
forge create src/MyContract.sol:MyContract \
  --rpc-url https://sepolia-rollup.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY \
  --legacy

# Using forge script
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $ARBITRUM_RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --legacy
```

### Hardhat Deployment

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    arbitrumOne: {
      url: process.env.ARBITRUM_RPC_URL ?? "https://arb1.arbitrum.io/rpc",
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 42161,
    },
    arbitrumSepolia: {
      url: "https://sepolia-rollup.arbitrum.io/rpc",
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 421614,
    },
  },
  etherscan: {
    apiKey: {
      arbitrumOne: process.env.ARBISCAN_API_KEY!,
      arbitrumSepolia: process.env.ARBISCAN_API_KEY!,
    },
  },
};

export default config;
```

### Contract Verification

```bash
# Verify on Arbiscan (Foundry)
forge verify-contract \
  --chain-id 42161 \
  --etherscan-api-key $ARBISCAN_API_KEY \
  --compiler-version v0.8.24 \
  $CONTRACT_ADDRESS \
  src/MyContract.sol:MyContract

# Verify with constructor args
forge verify-contract \
  --chain-id 42161 \
  --etherscan-api-key $ARBISCAN_API_KEY \
  --constructor-args $(cast abi-encode "constructor(address,uint256)" 0xYourAddress 1000) \
  $CONTRACT_ADDRESS \
  src/MyContract.sol:MyContract

# Verify on Sourcify
forge verify-contract \
  --chain-id 42161 \
  --verifier sourcify \
  $CONTRACT_ADDRESS \
  src/MyContract.sol:MyContract
```

## Cross-Chain Messaging

### L1 to L2: Retryable Tickets

Retryable tickets are Arbitrum's mechanism for sending messages from Ethereum L1 to Arbitrum L2. The L1 Inbox contract accepts the message and ETH for L2 gas, then the sequencer auto-executes it on L2.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IInbox {
    /// @notice Create a retryable ticket to send an L1→L2 message
    /// @param to L2 destination address
    /// @param l2CallValue ETH value to send to L2 destination
    /// @param maxSubmissionCost Max cost for L2 submission (refund if overestimated)
    /// @param excessFeeRefundAddress L2 address to refund excess fees
    /// @param callValueRefundAddress L2 address to refund call value on failure
    /// @param gasLimit L2 gas limit for execution
    /// @param maxFeePerGas Max L2 gas price
    /// @param data L2 calldata
    function createRetryableTicket(
        address to,
        uint256 l2CallValue,
        uint256 maxSubmissionCost,
        address excessFeeRefundAddress,
        address callValueRefundAddress,
        uint256 gasLimit,
        uint256 maxFeePerGas,
        bytes calldata data
    ) external payable returns (uint256);
}
```

```typescript
// TypeScript: send L1→L2 message via retryable ticket
import { createPublicClient, createWalletClient, http, parseEther } from "viem";
import { mainnet } from "viem/chains";

const INBOX = "0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f" as const;

const inboxAbi = [
  {
    name: "createRetryableTicket",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "to", type: "address" },
      { name: "l2CallValue", type: "uint256" },
      { name: "maxSubmissionCost", type: "uint256" },
      { name: "excessFeeRefundAddress", type: "address" },
      { name: "callValueRefundAddress", type: "address" },
      { name: "gasLimit", type: "uint256" },
      { name: "maxFeePerGas", type: "uint256" },
      { name: "data", type: "bytes" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const l1PublicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.ETHEREUM_RPC_URL),
});

const maxSubmissionCost = parseEther("0.001");
const gasLimit = 1_000_000n;
const maxFeePerGas = 100_000_000n; // 0.1 gwei

// Total ETH needed: l2CallValue + maxSubmissionCost + (gasLimit * maxFeePerGas)
const totalValue = 0n + maxSubmissionCost + gasLimit * maxFeePerGas;

const { request } = await l1PublicClient.simulateContract({
  address: INBOX,
  abi: inboxAbi,
  functionName: "createRetryableTicket",
  args: [
    "0xYourL2ContractAddress",     // to
    0n,                             // l2CallValue
    maxSubmissionCost,              // maxSubmissionCost
    account.address,                // excessFeeRefundAddress
    account.address,                // callValueRefundAddress
    gasLimit,                       // gasLimit
    maxFeePerGas,                   // maxFeePerGas
    "0x",                           // data (encoded L2 function call)
  ],
  value: totalValue,
  account: account.address,
});

const hash = await walletClient.writeContract(request);
```

### L2 to L1: ArbSys.sendTxToL1

L2-to-L1 messages go through the 7-day challenge period before they can be executed on L1.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IArbSys {
    /// @notice Send a transaction from L2 to L1
    /// @param destination L1 destination address
    /// @param data L1 calldata
    /// @return unique message ID
    function sendTxToL1(
        address destination,
        bytes calldata data
    ) external payable returns (uint256);

    /// @notice Get the current L2 block number
    function arbBlockNumber() external view returns (uint256);
}

// ArbSys is at a fixed precompile address on all Arbitrum chains
IArbSys constant ARBSYS = IArbSys(0x0000000000000000000000000000000000000064);

contract L2ToL1Sender {
    event L2ToL1MessageSent(uint256 indexed messageId, address destination);

    function sendMessageToL1(
        address l1Target,
        bytes calldata l1Calldata
    ) external payable {
        uint256 messageId = ARBSYS.sendTxToL1{value: msg.value}(
            l1Target,
            l1Calldata
        );
        emit L2ToL1MessageSent(messageId, l1Target);
    }
}
```

### Address Aliasing

When an L1 contract sends a retryable ticket, the `msg.sender` seen on L2 is the aliased address:

```
L2 alias = L1 address + 0x1111000000000000000000000000000000001111
```

```solidity
// Reverse the alias to get the original L1 sender
function undoL1ToL2Alias(address l2Address) internal pure returns (address) {
    uint160 offset = uint160(0x1111000000000000000000000000000000001111);
    unchecked {
        return address(uint160(l2Address) - offset);
    }
}

// Verify an L2 call came from a specific L1 contract
modifier onlyFromL1Contract(address expectedL1Sender) {
    require(
        undoL1ToL2Alias(msg.sender) == expectedL1Sender,
        "NOT_FROM_L1_CONTRACT"
    );
    _;
}
```

## ArbOS Precompiles

Arbitrum provides system-level functionality through precompile contracts at fixed addresses. These are available on all Arbitrum chains.

### ArbSys (0x0000000000000000000000000000000000000064)

Core system functions for L2 operations.

```solidity
interface IArbSys {
    function arbBlockNumber() external view returns (uint256);
    function arbBlockHash(uint256 blockNumber) external view returns (bytes32);
    function arbChainID() external view returns (uint256);
    function arbOSVersion() external view returns (uint256);
    function sendTxToL1(address dest, bytes calldata data) external payable returns (uint256);
    function withdrawEth(address dest) external payable returns (uint256);
}
```

```typescript
const arbSysAbi = [
  {
    name: "arbBlockNumber",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "withdrawEth",
    type: "function",
    stateMutability: "payable",
    inputs: [{ name: "destination", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const ARBSYS = "0x0000000000000000000000000000000000000064" as const;

const l2BlockNumber = await publicClient.readContract({
  address: ARBSYS,
  abi: arbSysAbi,
  functionName: "arbBlockNumber",
});
```

### ArbRetryableTx (0x000000000000000000000000000000000000006E)

Manage retryable tickets on L2.

```solidity
interface IArbRetryableTx {
    /// @notice Redeem a retryable ticket that failed auto-execution
    function redeem(bytes32 ticketId) external;
    /// @notice Get the TTL for retryable tickets (default: 7 days)
    function getLifetime() external view returns (uint256);
    /// @notice Get the timeout timestamp for a specific ticket
    function getTimeout(bytes32 ticketId) external view returns (uint256);
    /// @notice Extend the lifetime of a retryable ticket
    function keepalive(bytes32 ticketId) external returns (uint256);
}
```

### ArbGasInfo (0x000000000000000000000000000000000000006C)

Gas pricing information, especially the L1 data cost component.

```solidity
interface IArbGasInfo {
    /// @notice Get gas prices: [perL2Tx, perL1CalldataUnit, perStorageAlloc, perArbGasBase, perArbGasCongestion, perArbGasTotal]
    function getPricesInWei() external view returns (uint256, uint256, uint256, uint256, uint256, uint256);
    /// @notice Get estimated L1 base fee
    function getL1BaseFeeEstimate() external view returns (uint256);
    /// @notice Get L1 gas pricing parameters
    function getL1GasPriceEstimate() external view returns (uint256);
}
```

```typescript
const arbGasInfoAbi = [
  {
    name: "getPricesInWei",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [
      { name: "perL2Tx", type: "uint256" },
      { name: "perL1CalldataUnit", type: "uint256" },
      { name: "perStorageAlloc", type: "uint256" },
      { name: "perArbGasBase", type: "uint256" },
      { name: "perArbGasCongestion", type: "uint256" },
      { name: "perArbGasTotal", type: "uint256" },
    ],
  },
  {
    name: "getL1BaseFeeEstimate",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const ARBGASINFO = "0x000000000000000000000000000000000000006C" as const;

const prices = await publicClient.readContract({
  address: ARBGASINFO,
  abi: arbGasInfoAbi,
  functionName: "getPricesInWei",
});

const l1BaseFee = await publicClient.readContract({
  address: ARBGASINFO,
  abi: arbGasInfoAbi,
  functionName: "getL1BaseFeeEstimate",
});
```

### NodeInterface (0x00000000000000000000000000000000000000C8)

Virtual contract for gas estimation — not callable from other contracts, only via `eth_call` / `eth_estimateGas`.

```solidity
interface INodeInterface {
    /// @notice Estimate gas for a retryable ticket submission
    function estimateRetryableTicket(
        address sender,
        uint256 deposit,
        address to,
        uint256 l2CallValue,
        address excessFeeRefundAddress,
        address callValueRefundAddress,
        bytes calldata data
    ) external;

    /// @notice Get gas cost breakdown: gasEstimate, gasEstimateForL1, baseFee, l1BaseFeeEstimate
    function gasEstimateComponents(
        address to,
        bool contractCreation,
        bytes calldata data
    ) external payable returns (uint64, uint64, uint256, uint256);
}
```

```typescript
const nodeInterfaceAbi = [
  {
    name: "gasEstimateComponents",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "to", type: "address" },
      { name: "contractCreation", type: "bool" },
      { name: "data", type: "bytes" },
    ],
    outputs: [
      { name: "gasEstimate", type: "uint64" },
      { name: "gasEstimateForL1", type: "uint64" },
      { name: "baseFee", type: "uint256" },
      { name: "l1BaseFeeEstimate", type: "uint256" },
    ],
  },
] as const;

const NODE_INTERFACE = "0x00000000000000000000000000000000000000C8" as const;

// Estimate gas with L1/L2 breakdown
const result = await publicClient.simulateContract({
  address: NODE_INTERFACE,
  abi: nodeInterfaceAbi,
  functionName: "gasEstimateComponents",
  args: [
    "0xTargetContract",
    false,
    "0xEncodedCalldata",
  ],
});

const [totalGas, l1Gas, baseFee, l1BaseFee] = result.result;
// L2 gas = totalGas - l1Gas
```

## Gas Model

Arbitrum's gas model has two components. Understanding this is critical for accurate cost estimation.

### Two-Component Gas

| Component | Source | Scales With |
|-----------|--------|------------|
| L2 execution gas | ArbOS computation | Opcodes executed (similar to Ethereum) |
| L1 data posting cost | Calldata posted to Ethereum | Transaction size in bytes |

The L1 data cost is computed as:

```
L1 cost = L1 base fee * (calldata bytes * 16 + overhead)
```

This L1 cost is converted to L2 gas units and added to the total gas used. For data-heavy transactions (large calldata, many storage writes that get batched), the L1 component can be 80%+ of total cost.

### Gas Estimation

```typescript
import { encodeFunctionData, formatEther } from "viem";

async function estimateArbitrumGas(
  publicClient: PublicClient,
  to: `0x${string}`,
  data: `0x${string}`
) {
  const nodeInterfaceAbi = [
    {
      name: "gasEstimateComponents",
      type: "function",
      stateMutability: "payable",
      inputs: [
        { name: "to", type: "address" },
        { name: "contractCreation", type: "bool" },
        { name: "data", type: "bytes" },
      ],
      outputs: [
        { name: "gasEstimate", type: "uint64" },
        { name: "gasEstimateForL1", type: "uint64" },
        { name: "baseFee", type: "uint256" },
        { name: "l1BaseFeeEstimate", type: "uint256" },
      ],
    },
  ] as const;

  const { result } = await publicClient.simulateContract({
    address: "0x00000000000000000000000000000000000000C8",
    abi: nodeInterfaceAbi,
    functionName: "gasEstimateComponents",
    args: [to, false, data],
  });

  const [totalGas, l1Gas, baseFee, l1BaseFee] = result;
  const l2Gas = totalGas - l1Gas;

  return {
    totalGas,
    l1Gas,
    l2Gas,
    baseFee,
    l1BaseFee,
    estimatedCostWei: BigInt(totalGas) * baseFee,
    estimatedCostEth: formatEther(BigInt(totalGas) * baseFee),
  };
}
```

## Token Bridge

### Bridging ETH (L1 to L2)

```typescript
const INBOX = "0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f" as const;

const inboxAbi = [
  {
    name: "depositEth",
    type: "function",
    stateMutability: "payable",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Deposit 0.1 ETH from L1 to L2 (arrives at same address on L2)
const { request } = await l1PublicClient.simulateContract({
  address: INBOX,
  abi: inboxAbi,
  functionName: "depositEth",
  value: parseEther("0.1"),
  account: account.address,
});

const hash = await l1WalletClient.writeContract(request);
const receipt = await l1PublicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("ETH deposit failed");
// ETH appears on L2 within ~10 minutes
```

### Bridging ETH (L2 to L1)

```typescript
// Withdraw ETH from L2 to L1 via ArbSys precompile
const ARBSYS = "0x0000000000000000000000000000000000000064" as const;

const arbSysAbi = [
  {
    name: "withdrawEth",
    type: "function",
    stateMutability: "payable",
    inputs: [{ name: "destination", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const { request } = await l2PublicClient.simulateContract({
  address: ARBSYS,
  abi: arbSysAbi,
  functionName: "withdrawEth",
  args: [account.address], // L1 destination
  value: parseEther("0.1"),
  account: account.address,
});

const hash = await l2WalletClient.writeContract(request);
// After 7-day challenge period, claim on L1 via Outbox contract
```

### Bridging ERC20 Tokens (L1 to L2)

ERC20 tokens bridge through the Gateway Router, which routes to the appropriate gateway (standard, custom, or WETH).

```typescript
const GATEWAY_ROUTER = "0x72Ce9c846789fdB6fC1f34aC4AD25Dd9ef7031ef" as const;

const gatewayRouterAbi = [
  {
    name: "outboundTransfer",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_token", type: "address" },
      { name: "_to", type: "address" },
      { name: "_amount", type: "uint256" },
      { name: "_maxGas", type: "uint256" },
      { name: "_gasPriceBid", type: "uint256" },
      { name: "_data", type: "bytes" },
    ],
    outputs: [{ name: "", type: "bytes" }],
  },
  {
    name: "getGateway",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "_token", type: "address" }],
    outputs: [{ name: "", type: "address" }],
  },
] as const;

const USDC_L1 = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as const;

// Step 1: Approve the gateway (not the router) to spend tokens
const gateway = await l1PublicClient.readContract({
  address: GATEWAY_ROUTER,
  abi: gatewayRouterAbi,
  functionName: "getGateway",
  args: [USDC_L1],
});

// Step 2: approve gateway, then call outboundTransfer on the router
// The _data param encodes maxSubmissionCost and extra data
import { encodeAbiParameters, parseAbiParameters } from "viem";

const maxSubmissionCost = parseEther("0.001");
const extraData = encodeAbiParameters(
  parseAbiParameters("uint256, bytes"),
  [maxSubmissionCost, "0x"]
);

const bridgeAmount = 1000_000000n; // 1000 USDC (6 decimals)
const gasLimit = 300_000n;
const gasPriceBid = 100_000_000n; // 0.1 gwei

const totalValue = maxSubmissionCost + gasLimit * gasPriceBid;

const { request } = await l1PublicClient.simulateContract({
  address: GATEWAY_ROUTER,
  abi: gatewayRouterAbi,
  functionName: "outboundTransfer",
  args: [
    USDC_L1,
    account.address,
    bridgeAmount,
    gasLimit,
    gasPriceBid,
    extraData,
  ],
  value: totalValue,
  account: account.address,
});
```

### Gateway Types

| Gateway | Address (L1) | Purpose |
|---------|-------------|---------|
| Standard ERC20 | `0xa3A7B6F88361F48403514059F1F16C8E78d60EeC` | Default for most ERC20 tokens |
| Custom | Varies per token | Tokens needing custom L1/L2 logic |
| WETH | `0xd92023E9d9911199a6711321D1277285e6d4e2db` | Handles WETH unwrap/wrap across bridge |

## Orbit Chains

Orbit allows teams to launch custom L3 chains that settle to Arbitrum One or Nova. These are independent chains with configurable parameters.

### Orbit Architecture

```
Ethereum L1 (settlement)
  └── Arbitrum One L2 (execution + DA)
       └── Your Orbit L3 (custom chain)
```

### Orbit SDK Setup

```typescript
import { createRollupPrepareConfig, createRollupPrepareTransactionRequest } from "@arbitrum/orbit-sdk";

// Prepare Orbit chain configuration
const config = createRollupPrepareConfig({
  chainId: BigInt(YOUR_CHAIN_ID),
  owner: "0xYourOwnerAddress",
  chainConfig: {
    // Custom gas token, data availability, etc.
    homesteadBlock: 0,
    daoForkBlock: null,
    daoForkSupport: true,
    eip150Block: 0,
    eip150Hash: "0x0000000000000000000000000000000000000000000000000000000000000000",
    eip155Block: 0,
    eip158Block: 0,
    byzantiumBlock: 0,
    constantinopleBlock: 0,
    petersburgBlock: 0,
    istanbulBlock: 0,
    muirGlacierBlock: 0,
    berlinBlock: 0,
    londonBlock: 0,
    clique: { period: 0, epoch: 0 },
    arbitrum: {
      EnableArbOS: true,
      AllowDebugPrecompiles: false,
      DataAvailabilityCommittee: false, // true for AnyTrust
      InitialArbOSVersion: 20,
      InitialChainOwner: "0xYourOwnerAddress",
      GenesisBlockNum: 0,
    },
  },
});
```

### When to Use Orbit

| Use Case | Recommendation |
|----------|---------------|
| App-specific chain with custom gas token | Orbit L3 |
| High-throughput gaming with cheap DA | Orbit L3 + AnyTrust |
| General DeFi app | Deploy to Arbitrum One directly |
| Cross-chain interop needed | Deploy to Arbitrum One (better liquidity) |

## Key Differences from Ethereum

| Behavior | Ethereum | Arbitrum |
|----------|----------|---------|
| `block.number` | Current L1 block | L1 block number (NOT L2) |
| `block.timestamp` | L1 timestamp | L1 timestamp |
| L2 block number | N/A | `ArbSys(0x64).arbBlockNumber()` |
| Gas model | Single gas price | L2 gas + L1 data posting cost |
| Transaction type | EIP-1559 (type 2) | Legacy (type 0) recommended |
| Mempool | Public, competitive | No mempool (FCFS sequencer) |
| Finality | ~12 seconds (1 epoch) | ~0.25s soft, ~7 days hard |
| `msg.sender` cross-chain | Same address | Aliased (+0x1111...1111 offset) |
| `SELFDESTRUCT` | Deprecated (EIP-6780) | Same as Ethereum post-Dencun |
| Contract size limit | 24KB (EIP-170) | 24KB (same) |
| `PUSH0` opcode | Supported (Shanghai) | Supported (Nitro supports it) |

## Contract Addresses

> **Last verified:** February 2026

### Core Contracts (Arbitrum One)

| Contract | Address |
|----------|---------|
| Rollup | `0x5eF0D09d1E6204141B4d37530808eD19f60FBa35` |
| Inbox | `0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f` |
| Outbox | `0x0B9857ae2D4A3DBe74ffE1d7DF045bb7F96E4840` |
| Bridge | `0x8315177aB297bA92A06054cE80a67Ed4DBd7ed3a` |
| SequencerInbox | `0x1c479675ad559DC151F6Ec7ed3FbF8ceE79582B6` |
| Gateway Router (L1) | `0x72Ce9c846789fdB6fC1f34aC4AD25Dd9ef7031ef` |
| Standard Gateway (L1) | `0xa3A7B6F88361F48403514059F1F16C8E78d60EeC` |
| WETH Gateway (L1) | `0xd92023E9d9911199a6711321D1277285e6d4e2db` |
| Gateway Router (L2) | `0x5288c571Fd7aD117beA99bF60FE0846C4E84F933` |
| Standard Gateway (L2) | `0x09e9222E96E7B4AE2a407B98d48e330053351EEe` |

### ArbOS Precompiles

| Precompile | Address |
|------------|---------|
| ArbSys | `0x0000000000000000000000000000000000000064` |
| ArbInfo | `0x0000000000000000000000000000000000000065` |
| ArbAddressTable | `0x0000000000000000000000000000000000000066` |
| ArbBLS (deprecated) | `0x0000000000000000000000000000000000000067` |
| ArbFunctionTable (deprecated) | `0x0000000000000000000000000000000000000068` |
| ArbosTest | `0x0000000000000000000000000000000000000069` |
| ArbOwner | `0x0000000000000000000000000000000000000070` |
| ArbGasInfo | `0x000000000000000000000000000000000000006C` |
| ArbAggregator | `0x000000000000000000000000000000000000006D` |
| ArbRetryableTx | `0x000000000000000000000000000000000000006E` |
| ArbStatistics | `0x000000000000000000000000000000000000006F` |
| NodeInterface | `0x00000000000000000000000000000000000000C8` |

### Token Addresses (Arbitrum One)

| Token | Address |
|-------|---------|
| ARB | `0x912CE59144191C1204E64559FE8253a0e49E6548` |
| WETH | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` |
| USDC (native) | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| USDC.e (bridged) | `0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8` |
| USDT | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` |
| DAI | `0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1` |
| WBTC | `0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f` |
| GMX | `0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a` |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `NOT_ENOUGH_FUNDS` | Insufficient ETH for L2 gas + L1 data cost | Account for both gas components in estimation |
| `RETRYABLE_TICKET_CREATION_FAILED` | Retryable ticket underfunded | Increase `maxSubmissionCost` or `gasLimit * maxFeePerGas` |
| `ONLY_ROLLUP_OR_OWNER` | Calling admin precompile without permission | These are restricted to chain owner |
| `NO_TICKET_WITH_ID` | Redeeming non-existent or expired retryable | Check ticket still exists with `getTimeout()` |
| `ALREADY_REDEEMED` | Retryable ticket already executed | No action needed — message was delivered |
| `L1_MSG_NOT_CONFIRMED` | Trying to execute L2→L1 message too early | Wait for the 7-day challenge period to elapse |
| Nonce too high/low | Sequencer nonce mismatch | Reset nonce or wait for pending transactions |

## Security

### Cross-Chain Message Validation

```solidity
// Always verify the sender of cross-chain messages
// L1→L2: check aliased sender
modifier onlyL1Contract(address expectedL1Sender) {
    uint160 offset = uint160(0x1111000000000000000000000000000000001111);
    unchecked {
        require(
            address(uint160(msg.sender) - offset) == expectedL1Sender,
            "ONLY_L1_CONTRACT"
        );
    }
    _;
}

// L2→L1: verify via Outbox on L1
modifier onlyL2Contract(address outbox) {
    // The Outbox contract provides l2ToL1Sender() during execution
    IOutbox(outbox).l2ToL1Sender();
    _;
}
```

### Gas Estimation Safety

- Always use `NodeInterface.gasEstimateComponents()` instead of plain `eth_estimateGas` — the latter may not account for L1 data costs correctly in all cases.
- Add a 20-30% buffer to gas estimates for L1 data cost fluctuations.
- For retryable tickets, overestimate `maxSubmissionCost` — excess is refunded.

### Retryable Ticket Monitoring

- Monitor all retryable tickets for auto-redeem failure.
- Failed retryables expire after 7 days — set up alerts.
- Use the `ArbRetryableTx` precompile to check status and manually redeem.

## References

- [Arbitrum Docs](https://docs.arbitrum.io)
- [Arbitrum Nitro Whitepaper](https://github.com/OffchainLabs/nitro/blob/master/docs/Nitro-whitepaper.pdf)
- [Arbitrum SDK](https://github.com/OffchainLabs/arbitrum-sdk)
- [Orbit SDK](https://github.com/OffchainLabs/arbitrum-orbit-sdk)
- [ArbOS Precompiles Reference](https://docs.arbitrum.io/build-decentralized-apps/precompiles/reference)
- [Retryable Tickets](https://docs.arbitrum.io/arbos/l1-to-l2-messaging)
- [Arbitrum One Contract Addresses](https://docs.arbitrum.io/build-decentralized-apps/reference/useful-addresses)
- [Arbiscan Explorer](https://arbiscan.io)
- [Arbitrum Bridge](https://bridge.arbitrum.io)
