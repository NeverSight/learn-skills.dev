---
name: optimism
description: Optimism and OP Stack development — deployment, cross-chain messaging (CrossDomainMessenger), SuperchainERC20, predeploy contracts, gas model (L1 data fee + EIP-4844), and Superchain interop.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: optimism
  category: L2 & Alt-L1
tags:
  - optimism
  - op-stack
  - layer-2
  - optimistic-rollup
  - superchain
---

# Optimism

Optimism is an EVM-equivalent Layer 2 using optimistic rollups. Transactions execute on L2 with data posted to Ethereum L1 for security. The OP Stack is the modular framework powering OP Mainnet, Base, Zora, Mode, and the broader Superchain. Smart contracts deploy identically to Ethereum — no custom compiler, no special opcodes.

## What You Probably Got Wrong

- **OP Mainnet IS EVM-equivalent, not just EVM-compatible** — Your Solidity contracts deploy without modification. No `--legacy` flag, no custom compiler. `forge create` and `hardhat deploy` work identically to Ethereum. If someone tells you to change your Solidity for "OP compatibility", they are wrong.
- **Gas has two components, not one** — Every transaction pays L2 execution gas AND an L1 data fee for posting calldata/blobs to Ethereum. If you only estimate L2 gas via `eth_estimateGas`, your cost estimate will be wrong. The L1 data fee often dominates total cost. Use the `GasPriceOracle` predeploy at `0x420000000000000000000000000000000000000F`.
- **L2→L1 withdrawals take 7 days, not minutes** — L1→L2 deposits finalize in ~1-3 minutes. L2→L1 withdrawals require a 7-day challenge period (the "fault proof window"). Users must prove the withdrawal, wait 7 days, then finalize. Three separate transactions on L1. If your UX assumes instant bridging both ways, it is broken.
- **`block.number` returns the L2 block number, not L1** — On OP Mainnet, `block.number` is the L2 block number. To get the L1 block number, read the `L1Block` predeploy at `0x4200000000000000000000000000000000000015`. L2 blocks are produced every 2 seconds.
- **`msg.sender` works normally — there is no `tx.origin` aliasing on L2** — Cross-domain messages from L1 to L2 alias the sender address (add `0x1111000000000000000000000000000000001111`). But for normal L2 transactions, `msg.sender` behaves exactly like Ethereum. Only worry about aliasing when receiving L1→L2 messages in your contract.
- **Predeploy contracts live at fixed addresses starting with `0x4200...`** — These are NOT deployed by you. They exist at genesis. `L2CrossDomainMessenger`, `L2StandardBridge`, `GasPriceOracle`, `L1Block`, and others all live at hardcoded addresses in the `0x4200...` range. Do not try to deploy them.
- **The sequencer is centralized but cannot steal funds** — The sequencer orders transactions and proposes state roots. If it goes down, you cannot submit new transactions until it recovers (or until permissionless fault proofs allow forced inclusion). But the sequencer cannot forge invalid state — the fault proof system protects withdrawals.
- **EIP-4844 blob data changed the gas model** — After the Ecotone upgrade (March 2024), OP Mainnet posts data using EIP-4844 blobs instead of calldata. This reduced L1 data fees by ~10-100x. The `GasPriceOracle` methods changed. If you are reading pre-Ecotone documentation, the fee formulas are outdated.
- **SuperchainERC20 is not a standard ERC20** — It is a cross-chain token standard for OP Stack chains that enables native interop between Superchain members. Tokens must implement `ICrosschainERC20` with `crosschainMint` and `crosschainBurn`. Do not assume a regular ERC20 works across chains.

## Quick Start

### Chain Configuration

```typescript
import { defineChain } from "viem";
import { optimism, optimismSepolia } from "viem/chains";

// OP Mainnet is built-in
// Chain ID: 10
// RPC: https://mainnet.optimism.io
// Explorer: https://optimistic.etherscan.io

// OP Sepolia is also built-in
// Chain ID: 11155420
// RPC: https://sepolia.optimism.io
// Explorer: https://sepolia-optimistic.etherscan.io
```

### Environment Setup

```bash
# .env
PRIVATE_KEY=your_private_key_here
OP_MAINNET_RPC=https://mainnet.optimism.io
OP_SEPOLIA_RPC=https://sepolia.optimism.io
ETHERSCAN_API_KEY=your_optimistic_etherscan_api_key
```

### Viem Client Setup

```typescript
import { createPublicClient, createWalletClient, http } from "viem";
import { optimism } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(`0x${process.env.PRIVATE_KEY}`);

const publicClient = createPublicClient({
  chain: optimism,
  transport: http(process.env.OP_MAINNET_RPC),
});

const walletClient = createWalletClient({
  account,
  chain: optimism,
  transport: http(process.env.OP_MAINNET_RPC),
});
```

## Chain Configuration

| Property | OP Mainnet | OP Sepolia |
|----------|-----------|------------|
| Chain ID | 10 | 11155420 |
| Currency | ETH | ETH |
| RPC | `https://mainnet.optimism.io` | `https://sepolia.optimism.io` |
| Explorer | `https://optimistic.etherscan.io` | `https://sepolia-optimistic.etherscan.io` |
| Block time | 2 seconds | 2 seconds |
| Withdrawal period | 7 days | ~12 seconds (testnet) |

### Alternative RPCs

| Provider | Endpoint |
|----------|----------|
| Alchemy | `https://opt-mainnet.g.alchemy.com/v2/<KEY>` |
| Infura | `https://optimism-mainnet.infura.io/v3/<KEY>` |
| QuickNode | Custom endpoint per project |
| Conduit | `https://rpc.optimism.io` |

## Deployment

OP Mainnet is EVM-equivalent. Deploy exactly as you would to Ethereum.

### Foundry

```bash
# Deploy to OP Mainnet
forge create src/MyContract.sol:MyContract \
  --rpc-url $OP_MAINNET_RPC \
  --private-key $PRIVATE_KEY \
  --broadcast

# Deploy with constructor args
forge create src/MyToken.sol:MyToken \
  --rpc-url $OP_MAINNET_RPC \
  --private-key $PRIVATE_KEY \
  --constructor-args "MyToken" "MTK" 18 \
  --broadcast

# Deploy via script
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $OP_MAINNET_RPC \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY
```

### Hardhat

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    optimism: {
      url: process.env.OP_MAINNET_RPC || "https://mainnet.optimism.io",
      accounts: [process.env.PRIVATE_KEY!],
    },
    optimismSepolia: {
      url: process.env.OP_SEPOLIA_RPC || "https://sepolia.optimism.io",
      accounts: [process.env.PRIVATE_KEY!],
    },
  },
  etherscan: {
    apiKey: {
      optimisticEthereum: process.env.ETHERSCAN_API_KEY!,
      optimisticSepolia: process.env.ETHERSCAN_API_KEY!,
    },
  },
};

export default config;
```

```bash
npx hardhat run scripts/deploy.ts --network optimism
```

## Verification

### Foundry

```bash
# Verify after deployment
forge verify-contract <DEPLOYED_ADDRESS> src/MyContract.sol:MyContract \
  --chain-id 10 \
  --etherscan-api-key $ETHERSCAN_API_KEY

# Verify with constructor args
forge verify-contract <DEPLOYED_ADDRESS> src/MyToken.sol:MyToken \
  --chain-id 10 \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --constructor-args $(cast abi-encode "constructor(string,string,uint8)" "MyToken" "MTK" 18)
```

### Hardhat

```bash
npx hardhat verify --network optimism <DEPLOYED_ADDRESS> "MyToken" "MTK" 18
```

### Blockscout

OP Mainnet also has a Blockscout explorer at `https://optimism.blockscout.com`. Verification works via the standard Blockscout API — set the verifier URL in Foundry:

```bash
forge verify-contract <DEPLOYED_ADDRESS> src/MyContract.sol:MyContract \
  --verifier blockscout \
  --verifier-url https://optimism.blockscout.com/api/
```

## Cross-Chain Messaging

The `CrossDomainMessenger` is the canonical way to send arbitrary messages between L1 and L2. It handles replay protection, sender authentication, and gas forwarding.

### Architecture

```
L1 → L2 (Deposits):
  User → L1CrossDomainMessenger → OptimismPortal → L2CrossDomainMessenger → Target

L2 → L1 (Withdrawals):
  User → L2CrossDomainMessenger → L2ToL1MessagePasser → [7 day wait] → OptimismPortal → L1CrossDomainMessenger → Target
```

### L1 → L2 Message (Deposit)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IL1CrossDomainMessenger {
    function sendMessage(
        address _target,
        bytes calldata _message,
        uint32 _minGasLimit
    ) external payable;
}

contract L1Sender {
    IL1CrossDomainMessenger public immutable messenger;

    constructor(address _messenger) {
        messenger = IL1CrossDomainMessenger(_messenger);
    }

    /// @notice Send a message from L1 to a contract on L2.
    /// @param l2Target The L2 contract address to call.
    /// @param message The calldata to send to the L2 target.
    /// @param minGasLimit Minimum gas for L2 execution. Overestimate — unused gas is NOT refunded to L1.
    function sendToL2(
        address l2Target,
        bytes calldata message,
        uint32 minGasLimit
    ) external payable {
        messenger.sendMessage{value: msg.value}(l2Target, message, minGasLimit);
    }
}
```

### L2 → L1 Message (Withdrawal)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IL2CrossDomainMessenger {
    function sendMessage(
        address _target,
        bytes calldata _message,
        uint32 _minGasLimit
    ) external payable;

    function xDomainMessageSender() external view returns (address);
}

contract L2Sender {
    /// @dev L2CrossDomainMessenger predeploy address — same on all OP Stack chains
    IL2CrossDomainMessenger public constant MESSENGER =
        IL2CrossDomainMessenger(0x4200000000000000000000000000000000000007);

    function sendToL1(
        address l1Target,
        bytes calldata message,
        uint32 minGasLimit
    ) external payable {
        MESSENGER.sendMessage{value: msg.value}(l1Target, message, minGasLimit);
    }
}
```

### Receiving Cross-Chain Messages

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ICrossDomainMessenger {
    function xDomainMessageSender() external view returns (address);
}

contract L2Receiver {
    ICrossDomainMessenger public constant MESSENGER =
        ICrossDomainMessenger(0x4200000000000000000000000000000000000007);

    address public immutable l1Sender;

    constructor(address _l1Sender) {
        l1Sender = _l1Sender;
    }

    modifier onlyFromL1Sender() {
        require(
            msg.sender == address(MESSENGER) &&
            MESSENGER.xDomainMessageSender() == l1Sender,
            "Not authorized L1 sender"
        );
        _;
    }

    function handleMessage(uint256 value) external onlyFromL1Sender {
        // Process the cross-chain message
    }
}
```

### Sender Aliasing

When an L1 contract sends a message to L2, the apparent `msg.sender` on L2 is the aliased address:

```
l2Sender = l1ContractAddress + 0x1111000000000000000000000000000000001111
```

The `CrossDomainMessenger` handles un-aliasing internally. If you bypass the messenger and send directly via `OptimismPortal`, you must account for aliasing yourself.

## Predeploy Contracts

These contracts exist at genesis on every OP Stack chain. Do not deploy them — they are already there.

| Contract | Address | Purpose |
|----------|---------|---------|
| L2ToL1MessagePasser | `0x4200000000000000000000000000000000000016` | Initiates L2→L1 withdrawals |
| L2CrossDomainMessenger | `0x4200000000000000000000000000000000000007` | Sends/receives cross-chain messages |
| L2StandardBridge | `0x4200000000000000000000000000000000000010` | Bridges ETH and ERC20 tokens |
| L2ERC721Bridge | `0x4200000000000000000000000000000000000014` | Bridges ERC721 tokens |
| GasPriceOracle | `0x420000000000000000000000000000000000000F` | L1 data fee calculation |
| L1Block | `0x4200000000000000000000000000000000000015` | Exposes L1 block info on L2 |
| WETH9 | `0x4200000000000000000000000000000000000006` | Wrapped ETH |
| L1BlockNumber | `0x4200000000000000000000000000000000000013` | L1 block number (deprecated, use L1Block) |
| SequencerFeeVault | `0x4200000000000000000000000000000000000011` | Collects sequencer fees |
| BaseFeeVault | `0x4200000000000000000000000000000000000019` | Collects base fees |
| L1FeeVault | `0x420000000000000000000000000000000000001A` | Collects L1 data fees |
| GovernanceToken | `0x4200000000000000000000000000000000000042` | OP token on L2 |

### Reading L1 Block Info

```solidity
interface IL1Block {
    function number() external view returns (uint64);
    function timestamp() external view returns (uint64);
    function basefee() external view returns (uint256);
    function hash() external view returns (bytes32);
    function batcherHash() external view returns (bytes32);
    function l1FeeOverhead() external view returns (uint256);
    function l1FeeScalar() external view returns (uint256);
    function blobBaseFee() external view returns (uint256);
    function baseFeeScalar() external view returns (uint32);
    function blobBaseFeeScalar() external view returns (uint32);
}

// Usage
IL1Block constant L1_BLOCK = IL1Block(0x4200000000000000000000000000000000000015);
uint64 l1BlockNumber = L1_BLOCK.number();
uint256 l1BaseFee = L1_BLOCK.basefee();
```

## Gas Model

Every OP Mainnet transaction pays two fees:

1. **L2 execution fee** — Standard EVM gas, priced by L2 `basefee` + optional priority fee. Calculated identically to Ethereum.
2. **L1 data fee** — Cost of posting the transaction's data to Ethereum L1 as calldata or blob data. This is the OP-specific component.

### Post-Ecotone Formula (Current)

After the Ecotone upgrade (March 2024), L1 data fee uses a two-component formula based on calldata gas and blob gas:

```
l1DataFee = (l1BaseFeeScalar * l1BaseFee * 16 + l1BlobBaseFeeScalar * l1BlobBaseFee) * compressedTxSize / 1e6
```

- `l1BaseFee` — Ethereum L1 base fee (from `L1Block` predeploy)
- `l1BlobBaseFee` — EIP-4844 blob base fee (from `L1Block` predeploy)
- `l1BaseFeeScalar` — System-configured scalar for calldata cost component
- `l1BlobBaseFeeScalar` — System-configured scalar for blob cost component
- `compressedTxSize` — Estimated compressed size of the signed transaction

### GasPriceOracle

```solidity
interface IGasPriceOracle {
    /// @notice Estimate L1 data fee for raw signed transaction bytes
    function getL1Fee(bytes memory _data) external view returns (uint256);

    /// @notice Get current L1 base fee (read from L1Block)
    function l1BaseFee() external view returns (uint256);

    /// @notice Ecotone: get blob base fee
    function blobBaseFee() external view returns (uint256);

    /// @notice Ecotone: get base fee scalar
    function baseFeeScalar() external view returns (uint32);

    /// @notice Ecotone: get blob base fee scalar
    function blobBaseFeeScalar() external view returns (uint32);

    /// @notice Check if Ecotone is active
    function isEcotone() external view returns (bool);

    /// @notice Check if Fjord is active
    function isFjord() external view returns (bool);

    /// @notice Fjord: estimate compressed size using FastLZ
    function getL1GasUsed(bytes memory _data) external view returns (uint256);
}

IGasPriceOracle constant GAS_ORACLE =
    IGasPriceOracle(0x420000000000000000000000000000000000000F);
```

### Estimating Total Cost in TypeScript

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { optimism } from "viem/chains";

const client = createPublicClient({
  chain: optimism,
  transport: http(),
});

const GAS_ORACLE = "0x420000000000000000000000000000000000000F" as const;

const gasPriceOracleAbi = parseAbi([
  "function getL1Fee(bytes memory _data) external view returns (uint256)",
  "function l1BaseFee() external view returns (uint256)",
  "function blobBaseFee() external view returns (uint256)",
  "function baseFeeScalar() external view returns (uint32)",
  "function blobBaseFeeScalar() external view returns (uint32)",
]);

async function estimateTotalCost(serializedTx: `0x${string}`) {
  const [l2GasEstimate, gasPrice, l1DataFee] = await Promise.all([
    client.estimateGas({ data: serializedTx }),
    client.getGasPrice(),
    client.readContract({
      address: GAS_ORACLE,
      abi: gasPriceOracleAbi,
      functionName: "getL1Fee",
      args: [serializedTx],
    }),
  ]);

  const l2ExecutionFee = l2GasEstimate * gasPrice;
  const totalFee = l2ExecutionFee + l1DataFee;

  return {
    l2ExecutionFee,
    l1DataFee,
    totalFee,
  };
}
```

### Gas Optimization Tips

- Minimize calldata: the L1 data fee scales with transaction data size. Fewer bytes = lower L1 fee.
- Use `0` bytes when possible: zero bytes cost 4 gas in calldata vs 16 gas for non-zero bytes.
- Batch operations: one large transaction costs less in L1 data fee overhead than many small ones.
- After Ecotone, blob pricing makes L1 data fees much cheaper and more stable than pre-Ecotone calldata pricing.

## Standard Bridge

The Standard Bridge enables ETH and ERC20 transfers between L1 and L2. It is a pair of contracts: `L1StandardBridge` on Ethereum and `L2StandardBridge` (predeploy) on OP Mainnet.

### Bridge ETH: L1 → L2

```solidity
interface IL1StandardBridge {
    /// @notice Bridge ETH to L2. Appears at recipient address on L2 after ~1-3 min.
    function depositETH(uint32 _minGasLimit, bytes calldata _extraData) external payable;

    /// @notice Bridge ETH to a different address on L2.
    function depositETHTo(
        address _to,
        uint32 _minGasLimit,
        bytes calldata _extraData
    ) external payable;
}
```

### Bridge ETH: L2 → L1

```solidity
interface IL2StandardBridge {
    /// @notice Initiate ETH withdrawal to L1. Requires prove + finalize after 7 days.
    function withdraw(
        address _l2Token,
        uint256 _amount,
        uint32 _minGasLimit,
        bytes calldata _extraData
    ) external payable;
}

// Withdraw ETH from L2 to L1
// _l2Token = 0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000 (legacy ETH representation)
// Send ETH as msg.value, set _amount to the same value
```

### Bridge ERC20: L1 → L2

```solidity
interface IL1StandardBridge {
    /// @notice Bridge ERC20 to L2. Token must have a corresponding L2 representation.
    function depositERC20(
        address _l1Token,
        address _l2Token,
        uint256 _amount,
        uint32 _minGasLimit,
        bytes calldata _extraData
    ) external;

    function depositERC20To(
        address _l1Token,
        address _l2Token,
        uint256 _amount,
        address _to,
        uint32 _minGasLimit,
        bytes calldata _extraData
    ) external;
}
```

### Bridge ERC20: L2 → L1

```solidity
interface IL2StandardBridge {
    function withdraw(
        address _l2Token,
        uint256 _amount,
        uint32 _minGasLimit,
        bytes calldata _extraData
    ) external payable;

    function withdrawTo(
        address _l2Token,
        address _to,
        uint256 _amount,
        uint32 _minGasLimit,
        bytes calldata _extraData
    ) external payable;
}
```

### Withdrawal Lifecycle (L2 → L1)

Every L2→L1 withdrawal requires three L1 transactions:

1. **Initiate** — Call `withdraw` on `L2StandardBridge` or `L2CrossDomainMessenger`. Produces a withdrawal hash.
2. **Prove** — After the L2 output root containing your withdrawal is proposed on L1 (~1 hour), call `proveWithdrawalTransaction` on `OptimismPortal`.
3. **Finalize** — After the 7-day challenge period, call `finalizeWithdrawalTransaction` on `OptimismPortal`.

```typescript
import { getWithdrawals, getL2Output } from "viem/op-stack";

// After initiating withdrawal on L2, get the receipt
const l2Receipt = await publicClient.getTransactionReceipt({ hash: l2TxHash });

// Build withdrawal proof (after output root is proposed, ~1 hour)
const output = await getL2Output(l1Client, {
  l2BlockNumber: l2Receipt.blockNumber,
  targetChain: optimism,
});

// Prove on L1
const proveHash = await walletClient.proveWithdrawal({
  output,
  withdrawal: withdrawals[0],
  targetChain: optimism,
});

// Wait 7 days, then finalize on L1
const finalizeHash = await walletClient.finalizeWithdrawal({
  withdrawal: withdrawals[0],
  targetChain: optimism,
});
```

## SuperchainERC20

SuperchainERC20 is a cross-chain token standard enabling native token transfers between OP Stack chains in the Superchain. Tokens implementing this standard can move between chains without traditional bridge locking.

### Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice Interface for tokens that support cross-chain transfers within the Superchain.
interface ICrosschainERC20 {
    /// @notice Emitted when tokens are minted via a cross-chain transfer.
    event CrosschainMint(address indexed to, uint256 amount, address indexed sender);

    /// @notice Emitted when tokens are burned for a cross-chain transfer.
    event CrosschainBurn(address indexed from, uint256 amount, address indexed sender);

    /// @notice Mint tokens on this chain as part of a cross-chain transfer.
    /// @dev Only callable by the SuperchainTokenBridge.
    function crosschainMint(address _to, uint256 _amount) external;

    /// @notice Burn tokens on this chain to initiate a cross-chain transfer.
    /// @dev Only callable by the SuperchainTokenBridge.
    function crosschainBurn(address _from, uint256 _amount) external;
}
```

### Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ICrosschainERC20} from "./ICrosschainERC20.sol";

/// @dev SuperchainTokenBridge predeploy address — same on all OP Stack chains
address constant SUPERCHAIN_TOKEN_BRIDGE = 0x4200000000000000000000000000000000000028;

contract MySuperchainToken is ERC20, ICrosschainERC20 {
    constructor() ERC20("MySuperchainToken", "MST") {
        _mint(msg.sender, 1_000_000 * 1e18);
    }

    function crosschainMint(address _to, uint256 _amount) external override {
        require(msg.sender == SUPERCHAIN_TOKEN_BRIDGE, "Only bridge");
        _mint(_to, _amount);
        emit CrosschainMint(_to, _amount, msg.sender);
    }

    function crosschainBurn(address _from, uint256 _amount) external override {
        require(msg.sender == SUPERCHAIN_TOKEN_BRIDGE, "Only bridge");
        _burn(_from, _amount);
        emit CrosschainBurn(_from, _amount, msg.sender);
    }
}
```

### Cross-Chain Transfer Flow

1. User calls `SuperchainTokenBridge.sendERC20` on the source chain
2. Bridge calls `crosschainBurn` on the token contract (burns on source)
3. A cross-chain message is relayed to the destination chain
4. Bridge calls `crosschainMint` on the destination chain's token contract (mints on destination)

## OP Stack

The OP Stack is the modular, open-source framework for building L2 blockchains. OP Mainnet, Base, Zora, Mode, and others are all OP Stack chains forming the Superchain.

### Key Components

| Component | Description |
|-----------|-------------|
| **op-node** | Consensus client — derives L2 blocks from L1 data |
| **op-geth** | Execution client — modified go-ethereum |
| **op-batcher** | Posts transaction data to L1 (calldata or blobs) |
| **op-proposer** | Proposes L2 output roots to L1 |
| **op-challenger** | Runs fault proof games to challenge invalid proposals |

### Superchain

The Superchain is a network of OP Stack chains sharing:
- Bridge contracts on L1
- Sequencer coordination
- Governance via the Optimism Collective
- Interoperability messaging

Current Superchain members include OP Mainnet, Base, Zora, Mode, Fraxtal, Metal, and others. All share the same upgrade path and security model.

### Building a Custom OP Chain

Use the OP Stack to launch your own chain:

```bash
# Clone the optimism monorepo
git clone https://github.com/ethereum-optimism/optimism.git
cd optimism

# Install dependencies
pnpm install

# Configure your chain (edit deploy-config)
# Deploy L1 contracts
# Start op-node, op-geth, op-batcher, op-proposer
```

Refer to the [OP Stack Getting Started Guide](https://docs.optimism.io/builders/chain-operators/tutorials/create-l2-rollup) for complete chain deployment.

## Governance

The Optimism Collective governs the protocol through a bicameral system:

- **Token House** — OP token holders vote on protocol upgrades, incentive programs, and treasury allocations
- **Citizens' House** — Soulbound "citizen" badges vote on retroactive public goods funding (RetroPGF)

### OP Token

| Property | Value |
|----------|-------|
| Address (L2) | `0x4200000000000000000000000000000000000042` |
| Address (L1) | `0x4200000000000000000000000000000000000042` is the L2 predeploy; L1 address is `0x4200000000000000000000000000000000000042` bridged |
| Total supply | 4,294,967,296 (2^32) |
| Type | Governance only (no fee burn or staking yield) |

### Delegation

OP token holders delegate voting power to active governance participants:

```typescript
import { parseAbi } from "viem";

const opTokenAbi = parseAbi([
  "function delegate(address delegatee) external",
  "function delegates(address account) external view returns (address)",
  "function getVotes(address account) external view returns (uint256)",
]);

const OP_TOKEN = "0x4200000000000000000000000000000000000042" as const;

// Delegate voting power
const hash = await walletClient.writeContract({
  address: OP_TOKEN,
  abi: opTokenAbi,
  functionName: "delegate",
  args: [delegateAddress],
});
```

## Key Differences from Ethereum

| Feature | Ethereum | OP Mainnet |
|---------|----------|------------|
| Block time | 12 seconds | 2 seconds |
| Gas pricing | Single base fee | L2 execution + L1 data fee |
| `block.number` | L1 block number | L2 block number |
| Finality | ~15 minutes (2 epochs) | 7 days for L2→L1 (challenge period) |
| Sequencing | Decentralized validators | Centralized sequencer (OP Labs) |
| `PREVRANDAO` | Beacon chain randomness | Sequencer-set value (NOT random, do NOT use for randomness) |
| `PUSH0` | Supported (Shanghai+) | Supported |
| `block.difficulty` | Always 0 post-merge | Always 0 |

### Opcodes Differences

- `PREVRANDAO` (formerly `DIFFICULTY`) — Returns the sequencer-set value, NOT true randomness. Never use for on-chain randomness. Use Chainlink VRF or a commit-reveal scheme.
- `ORIGIN` / `CALLER` — Work normally for L2 transactions. For L1→L2 deposits, the `origin` is aliased (see Sender Aliasing).
- All other opcodes behave identically to Ethereum.

### Unsupported Features

- **No native account abstraction (EIP-4337)** — Use third-party bundlers (Pimlico, Alchemy, Stackup).
- **No `eth_getProof` with pending block tag** — Use `latest` instead.

## Useful Links

- [Optimism Docs](https://docs.optimism.io)
- [OP Mainnet Status](https://status.optimism.io)
- [Optimistic Etherscan](https://optimistic.etherscan.io)
- [Superchain Faucet (Testnet)](https://app.optimism.io/faucet)
- [OP Stack Source](https://github.com/ethereum-optimism/optimism)
- [Optimism Governance](https://vote.optimism.io)
- [Superchain Registry](https://github.com/ethereum-optimism/superchain-registry)
