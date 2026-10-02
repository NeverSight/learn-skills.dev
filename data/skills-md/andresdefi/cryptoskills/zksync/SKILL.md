---
name: zksync
description: zkSync Era development — ZK-specific deployment patterns, native account abstraction, paymasters for gasless transactions, system contracts, and EVM differences.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: zksync
  category: L2 & Alt-L1
tags:
  - zksync
  - zk-rollup
  - layer-2
  - account-abstraction
  - paymaster
---

# zkSync Era Development

## What You Probably Got Wrong

1. **Bytecode is NOT EVM bytecode** — zkSync compiles to zkEVM bytecode via `zksolc`/`zkvyper`. You cannot deploy raw EVM bytecode. Standard `solc` output does not work.
2. **CREATE/CREATE2 behave differently** — Address derivation uses the bytecode hash, not the creation code. CREATE2 addresses differ from Ethereum for the same inputs.
3. **All accounts are smart accounts** — EOAs are implemented as a default account contract. Native account abstraction means every account goes through `validateTransaction` / `executeTransaction`.
4. **Gas has two components** — L2 execution gas + L1 pubdata gas. The `gas_per_pubdata_byte_limit` field is mandatory on every transaction.
5. **No `SELFDESTRUCT`** — The opcode is a no-op. Contracts cannot be destroyed.
6. **No `EXTCODECOPY` of other contracts** — You can only `EXTCODECOPY` your own bytecode. Copying another contract's code returns zeros.
7. **`msg.value` works differently** — Handled by the `MsgValueSimulator` system contract, not natively at the EVM level.
8. **Contract deployment uses a system contract** — All deployments go through the `ContractDeployer` system contract, not raw CREATE opcodes.

## Quick Start

### Install Tools

```bash
# Hardhat-zksync (recommended for most projects)
npm install -D @matterlabs/hardhat-zksync

# zksync-ethers (SDK for interacting with zkSync)
npm install zksync-ethers ethers

# Foundry-zksync (alternative — install the zkSync fork)
curl -L https://raw.githubusercontent.com/matter-labs/foundry-zksync/main/install-foundry-zksync | bash
foundryup-zksync
```

### Environment Setup

```bash
# .env
PRIVATE_KEY=your_private_key_here
ZKSYNC_MAINNET_RPC=https://mainnet.era.zksync.io
ZKSYNC_SEPOLIA_RPC=https://sepolia.era.zksync.dev
```

## Chain Configuration

### zkSync Era Mainnet

| Property | Value |
|----------|-------|
| Chain ID | **324** |
| Currency | ETH (18 decimals) |
| RPC (HTTP) | `https://mainnet.era.zksync.io` |
| RPC (WebSocket) | `wss://mainnet.era.zksync.io/ws` |
| Explorer | `https://explorer.zksync.io` |
| Bridge | `https://bridge.zksync.io` |
| Verification API | `https://zksync2-mainnet-explorer.zksync.io/contract_verification` |
| L1 Settlement | Ethereum Mainnet |

### zkSync Era Sepolia Testnet

| Property | Value |
|----------|-------|
| Chain ID | **300** |
| Currency | ETH (18 decimals) |
| RPC (HTTP) | `https://sepolia.era.zksync.dev` |
| RPC (WebSocket) | `wss://sepolia.era.zksync.dev/ws` |
| Explorer | `https://sepolia.explorer.zksync.io` |
| Bridge | `https://bridge.zksync.io` |
| Faucet | `https://faucet.zksync.io` |
| L1 Settlement | Ethereum Sepolia |

### Viem Chain Config

```typescript
import { zkSync, zkSyncSepoliaTestnet } from "viem/chains";
import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";

const publicClient = createPublicClient({
  chain: zkSync,
  transport: http(),
});

const account = privateKeyToAccount(`0x${process.env.PRIVATE_KEY}`);

const walletClient = createWalletClient({
  account,
  chain: zkSync,
  transport: http(),
});
```

### zksync-ethers Provider

```typescript
import { Provider, Wallet } from "zksync-ethers";
import { ethers } from "ethers";

const provider = new Provider("https://mainnet.era.zksync.io");
const ethProvider = ethers.getDefaultProvider("mainnet");
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider, ethProvider);

const balance = await provider.getBalance(wallet.address);
const blockNumber = await provider.getBlockNumber();
```

## Deployment

### Hardhat-zksync Setup

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
import "@matterlabs/hardhat-zksync";

const config: HardhatUserConfig = {
  defaultNetwork: "zkSyncSepolia",
  networks: {
    zkSyncSepolia: {
      url: "https://sepolia.era.zksync.dev",
      ethNetwork: "sepolia",
      zksync: true,
      verifyURL: "https://explorer.sepolia.era.zksync.dev/contract_verification",
    },
    zkSyncMainnet: {
      url: "https://mainnet.era.zksync.io",
      ethNetwork: "mainnet",
      zksync: true,
      verifyURL: "https://zksync2-mainnet-explorer.zksync.io/contract_verification",
    },
  },
  zksolc: {
    version: "latest",
    settings: {
      // enableEraVMExtensions: true, // only for system contract calls
    },
  },
  solidity: {
    version: "0.8.24",
  },
};

export default config;
```

### Deployment Script (Hardhat-zksync)

```typescript
// deploy/deploy.ts
import { Deployer } from "@matterlabs/hardhat-zksync";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { Wallet } from "zksync-ethers";

export default async function (hre: HardhatRuntimeEnvironment) {
  const wallet = new Wallet(process.env.PRIVATE_KEY!);
  const deployer = new Deployer(hre, wallet);

  const artifact = await deployer.loadArtifact("MyContract");
  const contract = await deployer.deploy(artifact, [
    /* constructor args */
  ]);

  await contract.waitForDeployment();
  const address = await contract.getAddress();
  console.log(`MyContract deployed to: ${address}`);

  // Verify
  await hre.run("verify:verify", {
    address,
    constructorArguments: [],
  });
}
```

```bash
# Deploy
npx hardhat deploy-zksync --script deploy.ts --network zkSyncSepolia
```

### Foundry-zksync Deployment

```bash
# Compile with zksolc
forge build --zksync

# Deploy
forge create src/MyContract.sol:MyContract \
  --rpc-url https://sepolia.era.zksync.dev \
  --private-key $PRIVATE_KEY \
  --zksync

# Deploy with constructor args
forge create src/MyContract.sol:MyContract \
  --rpc-url https://sepolia.era.zksync.dev \
  --private-key $PRIVATE_KEY \
  --zksync \
  --constructor-args "arg1" 42

# Verify
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --zksync \
  --verifier zksync \
  --verifier-url https://explorer.sepolia.era.zksync.dev/contract_verification
```

### CREATE2 on zkSync

CREATE2 address derivation differs from Ethereum. zkSync uses the bytecode **hash** (not creation code) in the salt computation.

```solidity
// Ethereum CREATE2: keccak256(0xff ++ deployer ++ salt ++ keccak256(creationCode))
// zkSync CREATE2:   keccak256(0xff ++ deployer ++ salt ++ keccak256(bytecodeHash) ++ keccak256(constructorInput))
```

```typescript
import { utils } from "zksync-ethers";

// Compute CREATE2 address on zkSync
const address = utils.create2Address(
  senderAddress,
  bytecodeHash,  // hash of the contract bytecode
  salt,
  constructorInput // ABI-encoded constructor arguments
);
```

## EVM Differences

### Opcodes That Differ

| Opcode | Ethereum | zkSync Era |
|--------|----------|------------|
| `SELFDESTRUCT` | Destroys contract | No-op (does nothing) |
| `EXTCODECOPY` | Copies any contract's code | Only works on `address(this)` |
| `EXTCODEHASH` | Hash of any contract's code | Works, but returns zkEVM bytecode hash |
| `CODECOPY` | Copies current contract code | Returns zkEVM bytecode |
| `CREATE` | Deploys from creation code | Calls `ContractDeployer` system contract |
| `CREATE2` | Deterministic deploy | Calls `ContractDeployer`, different address derivation |
| `CODESIZE` | Size of current contract | Returns zkEVM bytecode size |
| `EXTCODESIZE` | Size of any contract | Works normally |
| `COINBASE` | Block coinbase | Returns the bootloader address |
| `DIFFICULTY` / `PREVRANDAO` | Block difficulty/randomness | Returns a constant; not a source of randomness |
| `BASEFEE` | Current base fee | Returns 0.25 gwei (may change) |

### Key Behavioral Differences

```solidity
// WRONG: Checking code size to detect EOA
// On zkSync, EOAs have code (default account implementation)
function isContract(address account) internal view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(account) }
    return size > 0; // Returns true for BOTH contracts AND EOAs on zkSync
}

// CORRECT: Use the AccountCodeStorage system contract or accept
// that all accounts are "smart accounts" on zkSync
```

### msg.value Handling

`msg.value` is simulated via the `MsgValueSimulator` system contract. This means:
- Ether transfers in internal calls have slightly different gas costs
- `msg.value` in constructors works but goes through the system contract
- Reentrancy via `msg.value` follows the same CEI pattern as Ethereum

### Nonce Model

zkSync uses two nonces per account:
- **Transaction nonce** — incremented with each transaction (like Ethereum)
- **Deployment nonce** — incremented with each contract deployment via CREATE

```typescript
import { Provider } from "zksync-ethers";

const provider = new Provider("https://mainnet.era.zksync.io");

// Get transaction nonce
const txNonce = await provider.getTransactionCount(address);

// Get full nonce (both components) via NonceHolder system contract
```

## Native Account Abstraction

Every account on zkSync is a smart account. EOAs use a built-in default implementation. Custom accounts implement `IAccount`.

### IAccount Interface

Custom accounts implement five functions. See `examples/account-abstraction/README.md` for a full multi-sig implementation.

| Function | Purpose |
|----------|---------|
| `validateTransaction` | Verify signature/authorization (called by bootloader) |
| `executeTransaction` | Execute the transaction logic (called by bootloader) |
| `executeTransactionFromOutside` | Allow relay-style execution (called by anyone) |
| `payForTransaction` | Pay gas to bootloader (when no paymaster) |
| `prepareForPaymaster` | Set up ERC-20 approval for paymaster |

### Deploying a Smart Account

Smart accounts must be deployed via the `ContractDeployer` system contract using `"createAccount"` deployment type.

```typescript
import { ContractFactory } from "zksync-ethers";

const factory = new ContractFactory(
  accountAbi,
  accountBytecode,
  wallet,
  "createAccount" // tells ContractDeployer this is an account, not a regular contract
);

const account = await factory.deploy(/* constructor args */);
await account.waitForDeployment();
```

### AA Transaction Flow

1. User submits transaction to the operator
2. Bootloader calls `validateTransaction` on the sender account
3. If validation returns success magic, bootloader calls `payForTransaction` (or `prepareForPaymaster` if using a paymaster)
4. Bootloader calls `executeTransaction`
5. If any step fails, the transaction is reverted

## Paymasters

Paymasters sponsor gas fees for users. Two built-in flows exist.

### IPaymaster Interface

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@matterlabs/zk-contracts/l2/system-contracts/interfaces/IPaymaster.sol";
import "@matterlabs/zk-contracts/l2/system-contracts/interfaces/IPaymasterFlow.sol";
import "@matterlabs/zk-contracts/l2/system-contracts/Constants.sol";

contract GeneralPaymaster is IPaymaster {
    modifier onlyBootloader() {
        require(msg.sender == BOOTLOADER_FORMAL_ADDRESS, "Only bootloader");
        _;
    }

    // Called during validation to decide whether to sponsor the transaction
    function validateAndPayForPaymasterTransaction(
        bytes32, // _txHash
        bytes32, // _suggestedSignedHash
        Transaction calldata _transaction
    )
        external
        payable
        onlyBootloader
        returns (bytes4 magic, bytes memory context)
    {
        magic = PAYMASTER_VALIDATION_SUCCESS_MAGIC;

        // Verify this is a general flow
        require(
            _transaction.paymasterInput.length >= 4,
            "Invalid paymaster input"
        );
        bytes4 paymasterInputSelector = bytes4(_transaction.paymasterInput[0:4]);
        require(
            paymasterInputSelector == IPaymasterFlow.general.selector,
            "Unsupported flow"
        );

        // Pay the bootloader
        uint256 requiredETH = _transaction.gasLimit * _transaction.maxFeePerGas;
        (bool success, ) = payable(BOOTLOADER_FORMAL_ADDRESS).call{value: requiredETH}("");
        require(success, "Paymaster payment failed");
    }

    // Called after transaction execution (refund unused gas)
    function postTransaction(
        bytes calldata _context,
        Transaction calldata _transaction,
        bytes32, // _txHash
        bytes32, // _suggestedSignedHash
        ExecutionResult _txResult,
        uint256 _maxRefundedGas
    ) external payable onlyBootloader {
        // Optional: handle refunds or post-execution logic
    }

    receive() external payable {}
}
```

### Approval-Based Paymaster

The approval-based flow lets users pay gas in ERC-20 tokens. The paymaster pulls tokens from the user, then pays the bootloader in ETH. See `examples/paymaster/README.md` for the full contract implementation.

### Using a Paymaster from TypeScript

```typescript
import { Provider, Wallet, utils } from "zksync-ethers";

const provider = new Provider("https://sepolia.era.zksync.dev");
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const paymasterAddress = "0xYourPaymasterAddress";

// General flow — paymaster sponsors all gas
const tx = await wallet.sendTransaction({
  to: "0xRecipientAddress",
  value: 0n,
  data: "0x",
  customData: {
    paymasterParams: utils.getPaymasterParams(paymasterAddress, {
      type: "General",
      innerInput: new Uint8Array(),
    }),
    gasPerPubdata: utils.DEFAULT_GAS_PER_PUBDATA_LIMIT,
  },
});
await tx.wait();

// Approval-based flow — user pays in ERC20
const paymasterParams = utils.getPaymasterParams(paymasterAddress, {
  type: "ApprovalBased",
  token: tokenAddress,
  minimalAllowance: BigInt(1),
  innerInput: new Uint8Array(),
});

const txWithERC20 = await wallet.sendTransaction({
  to: contractAddress,
  data: encodedFunctionData,
  customData: {
    paymasterParams,
    gasPerPubdata: utils.DEFAULT_GAS_PER_PUBDATA_LIMIT,
  },
});
await txWithERC20.wait();
```

## System Contracts

zkSync Era uses system contracts deployed at low addresses for core functionality. These are not user-deployable.

| Contract | Address | Purpose |
|----------|---------|---------|
| ContractDeployer | `0x0000000000000000000000000000000000008006` | All contract deployments (CREATE, CREATE2, createAccount) |
| NonceHolder | `0x0000000000000000000000000000000000008003` | Manages transaction and deployment nonces |
| L1Messenger | `0x0000000000000000000000000000000000008008` | Sends messages from L2 to L1 |
| MsgValueSimulator | `0x0000000000000000000000000000000000008009` | Simulates `msg.value` behavior |
| KnownCodesStorage | `0x0000000000000000000000000000000000008004` | Stores hashes of known contract bytecodes |
| SystemContext | `0x000000000000000000000000000000000000800b` | Block/tx context (block.number, block.timestamp, etc.) |
| Bootloader | `0x0000000000000000000000000000000000008001` | Transaction processing entry point |
| AccountCodeStorage | `0x0000000000000000000000000000000000008002` | Stores account bytecode hashes |
| ImmutableSimulator | `0x0000000000000000000000000000000000008005` | Simulates Solidity immutable variables |
| L2BaseToken | `0x000000000000000000000000000000000000800a` | ETH balance management on L2 |
| Compressor | `0x000000000000000000000000000000000000800e` | Bytecode and state diff compression |
| PubdataChunkPublisher | `0x0000000000000000000000000000000000008011` | Publishes pubdata to L1 |

### Calling System Contracts

System contracts require the `isSystem` flag. In `hardhat-zksync`, enable `enableEraVMExtensions` in `zksolc` settings.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@matterlabs/zk-contracts/l2/system-contracts/Constants.sol";
import "@matterlabs/zk-contracts/l2/system-contracts/interfaces/INonceHolder.sol";

contract NonceReader {
    function getMinNonce(address account) external view returns (uint256) {
        return INonceHolder(NONCE_HOLDER_SYSTEM_CONTRACT).getMinNonce(account);
    }
}
```

```typescript
// hardhat.config.ts — enable system contract calls
zksolc: {
  version: "latest",
  settings: {
    enableEraVMExtensions: true,
  },
},
```

## Bridging

The `zksync-ethers` Wallet provides high-level bridging methods. See `examples/bridge/README.md` for full examples including ERC-20 deposits, withdrawal finalization, and L2-to-L1 messaging.

```typescript
import { Provider, Wallet } from "zksync-ethers";
import { ethers } from "ethers";

const l1Provider = ethers.getDefaultProvider("mainnet");
const l2Provider = new Provider("https://mainnet.era.zksync.io");
// Wallet needs both L2 and L1 providers for bridging
const wallet = new Wallet(process.env.PRIVATE_KEY!, l2Provider, l1Provider);

// L1 -> L2 deposit (ETH) — takes ~1-3 minutes
const depositTx = await wallet.deposit({
  token: ethers.ZeroAddress,
  amount: ethers.parseEther("0.1"),
});
const l2Receipt = await depositTx.waitFinalize();

// L2 -> L1 withdrawal — must finalize on L1 after ZK proof (1-3 hours)
const withdrawTx = await wallet.withdraw({
  token: ethers.ZeroAddress,
  amount: ethers.parseEther("0.05"),
  to: wallet.address,
});
await withdrawTx.waitFinalize();

// Check if withdrawal can be finalized, then claim on L1
const ready = await wallet.isWithdrawalFinalized(withdrawTxHash);
if (ready) {
  const finalizeTx = await wallet.finalizeWithdrawal(withdrawTxHash);
  await finalizeTx.wait();
}
```

### L2 to L1 Messaging

Arbitrary messages from L2 to L1 use the `L1Messenger` system contract.

```solidity
import "@matterlabs/zk-contracts/l2/system-contracts/Constants.sol";
import "@matterlabs/zk-contracts/l2/system-contracts/interfaces/IL1Messenger.sol";

contract L2ToL1Example {
    function sendMessage(bytes calldata message) external {
        IL1Messenger(L1_MESSENGER_SYSTEM_CONTRACT).sendToL1(message);
    }
}
```

## Gas Model

zkSync Era gas has two components:

### L2 Execution Gas
Computational cost on the zkEVM. Similar to Ethereum gas but with different opcode pricing.

### L1 Pubdata Gas
Cost of publishing state diffs and calldata to Ethereum L1. This is the dominant cost for most transactions.

### gas_per_pubdata_byte_limit

Every transaction must specify this field. It caps how much the user is willing to pay per byte of pubdata.

```typescript
import { utils } from "zksync-ethers";

// Default value — suitable for most transactions
const gasPerPubdata = utils.DEFAULT_GAS_PER_PUBDATA_LIMIT; // 50000

// Include in transaction
const tx = await wallet.sendTransaction({
  to: recipient,
  value: amount,
  customData: {
    gasPerPubdata,
  },
});
```

### Gas Estimation

```typescript
const provider = new Provider("https://mainnet.era.zksync.io");

// Estimate gas (includes both L2 execution and L1 pubdata)
const gasEstimate = await provider.estimateGas({
  from: wallet.address,
  to: contractAddress,
  data: encodedData,
  customData: {
    gasPerPubdata: utils.DEFAULT_GAS_PER_PUBDATA_LIMIT,
  },
});

// Get current gas price
const gasPrice = await provider.getGasPrice();

// Total cost estimate
const totalCost = gasEstimate * gasPrice;
```

### Fee Model Details

| Component | Description |
|-----------|-------------|
| `maxFeePerGas` | Maximum fee per unit of gas (like EIP-1559) |
| `maxPriorityFeePerGas` | Not used — set to `maxFeePerGas` |
| `gasLimit` | Total gas units (L2 execution + L1 pubdata) |
| `gas_per_pubdata_byte_limit` | Max gas per byte of published data |

## Testing

### era_test_node (In-Memory Node)

Fast local testing without a full node.

```bash
# Install
cargo install --git https://github.com/matter-labs/era-test-node

# Run (forks mainnet by default)
era_test_node run

# Fork from a specific block
era_test_node fork mainnet --fork-at 20000000

# Fork testnet
era_test_node fork sepolia-testnet
```

### Hardhat-zksync Testing

```typescript
// hardhat.config.ts — add in-memory node network
networks: {
  hardhat: {
    zksync: true,
  },
  inMemoryNode: {
    url: "http://127.0.0.1:8011",
    ethNetwork: "",
    zksync: true,
  },
},
```

```typescript
// test/MyContract.test.ts
import { expect } from "chai";
import { Deployer } from "@matterlabs/hardhat-zksync";
import { Wallet, Provider } from "zksync-ethers";
import hre from "hardhat";

describe("MyContract", function () {
  it("should deploy and interact", async function () {
    const provider = new Provider(hre.network.config.url);
    // era_test_node rich wallets (pre-funded)
    const wallet = new Wallet(
      "0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110",
      provider
    );

    const deployer = new Deployer(hre, wallet);
    const artifact = await deployer.loadArtifact("MyContract");
    const contract = await deployer.deploy(artifact, []);
    await contract.waitForDeployment();

    const result = await contract.someFunction();
    expect(result).to.equal(expectedValue);
  });
});
```

```bash
# Run tests against in-memory node
npx hardhat test --network inMemoryNode
```

### Rich Wallets (era_test_node)

Pre-funded accounts for local testing:

| Address | Private Key |
|---------|-------------|
| `0x36615Cf349d7F6344891B1e7CA7C72883F5dc049` | `0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110` |
| `0xa61464658AfeAf65CccaaFD3a512b69A83B77618` | `0xac1e735be8536c6534bb4f17f06f6afc73b2b5ba84ac2cfb12f7461b20c0bbe3` |
| `0x0D43eB5B8a47bA8900d64O6a548a778c4a6a4E04` | `0xd293c684d884d56f8d6abd64fc76757d3664904e309a0645baf8522ab6366d9e` |

## Key Differences Summary

| Feature | Ethereum | zkSync Era |
|---------|----------|------------|
| Bytecode | EVM bytecode | zkEVM bytecode (compiled via zksolc) |
| Compiler | solc | zksolc (wraps solc) |
| Contract Deploy | CREATE opcode | ContractDeployer system contract |
| CREATE2 Address | `keccak256(0xff, deployer, salt, initCodeHash)` | `keccak256(0xff, deployer, salt, bytecodeHash, constructorInputHash)` |
| Account Model | EOA or Smart Contract | All accounts are smart accounts |
| Account Abstraction | ERC-4337 (userops, bundlers) | Native (built into protocol) |
| Paymasters | ERC-4337 paymasters | Native paymasters (IPaymaster) |
| Gas | Single gas price | L2 gas + L1 pubdata gas |
| SELFDESTRUCT | Destroys contract | No-op |
| EXTCODECOPY | Any contract | Only self |
| msg.value | Native EVM | MsgValueSimulator system contract |
| Nonces | Single nonce | Transaction nonce + deployment nonce |
| Block Time | ~12 seconds | ~1-2 seconds |
| Finality | ~12 minutes (64 blocks) | ~1 hour (ZK proof on L1) |
| Tooling | Hardhat, Foundry | hardhat-zksync, foundry-zksync |

## Resources

- [zkSync Era Documentation](https://docs.zksync.io)
- [zkSync Era Explorer](https://explorer.zksync.io)
- [zksync-ethers SDK](https://github.com/zksync-sdk/zksync-ethers)
- [hardhat-zksync Plugins](https://github.com/matter-labs/hardhat-zksync)
- [foundry-zksync](https://github.com/matter-labs/foundry-zksync)
- [era-test-node](https://github.com/matter-labs/era-test-node)
- [zkSync System Contracts](https://github.com/matter-labs/era-contracts)
- [zkSync Bridge](https://bridge.zksync.io)
- [Faucet (Sepolia)](https://faucet.zksync.io)

## Skill Structure

```
zksync/
├── SKILL.md                          # This file
├── examples/
│   ├── deploy-contract/README.md     # Deployment patterns
│   ├── paymaster/README.md           # Paymaster implementation
│   ├── account-abstraction/README.md # Native AA
│   └── bridge/README.md              # L1<>L2 bridging
├── resources/
│   ├── contract-addresses.md         # System + L1 contract addresses
│   └── error-codes.md               # Common errors and fixes
├── docs/
│   └── troubleshooting.md           # Debugging guide
└── templates/
    └── zksync-deploy.ts             # Starter deployment template
```
