---
name: account-abstraction
description: "ERC-4337 and EIP-7702 unified reference — EntryPoint v0.7 architecture, UserOperation lifecycle, bundler and paymaster roles, EIP-7702 EOA delegation (Type 0x04 transactions), combined ERC-4337 + EIP-7702 flows, paymaster patterns (verifying, ERC-20, sponsoring), permissionless.js SDK, ZeroDev Kernel, session keys (ERC-7579), gas abstraction, and stack selection guidance."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - account-abstraction
  - erc-4337
  - eip-7702
  - smart-accounts
  - paymasters
  - bundlers
  - session-keys
  - permissionless
  - zerodev
---

# Account Abstraction

Account abstraction replaces the rigid EOA transaction model with programmable accounts that support arbitrary verification logic, gas sponsorship, batched operations, and session-based access control. ERC-4337 introduces an out-of-protocol smart account infrastructure (EntryPoint, bundlers, paymasters), while EIP-7702 adds a protocol-level mechanism for EOAs to temporarily or persistently delegate their execution to smart contract code. Together they form a complete stack: 7702 upgrades existing EOAs without migration, and 4337 provides the off-chain infrastructure for UserOperation bundling, gas abstraction, and paymaster sponsorship.

## What You Probably Got Wrong

- **EIP-7702 does NOT replace ERC-4337** -- they are complementary. EIP-7702 is a protocol-level mechanism that lets EOAs point their code to an implementation contract. ERC-4337 is an off-chain infrastructure layer (bundlers, paymasters, EntryPoint) that processes UserOperations. You need both for a complete account abstraction stack: 7702 makes the EOA programmable, 4337 provides gas sponsorship and bundling.

- **Existing EOAs can upgrade in-place with EIP-7702** -- users do NOT need to deploy a new smart contract wallet and migrate assets. A single Type 0x04 transaction sets a delegation designator on the EOA, making it behave like a smart account while keeping the same address, balances, and history.

- **Paymasters are NOT free gas** -- someone always pays. A verifying paymaster requires off-chain signature approval from the sponsor. An ERC-20 paymaster charges the user in tokens at a markup. A sponsoring paymaster has a deposit in the EntryPoint that drains with each sponsored operation. "Gasless" means gasless for the end user, not gasless for the system.

- **UserOperations are NOT wrapped transactions** -- they are a completely different execution model. A UserOp goes from the client to a bundler (off-chain), the bundler packages multiple UserOps into a single `handleOps` transaction to the EntryPoint contract (on-chain), and the EntryPoint calls each account's `validateUserOp` then `execute`. The account contract itself is the `msg.sender` for the inner calls, not the EOA signer.

- **Session keys are NOT private keys you hand out** -- they are scoped authorizations with explicit constraints: which contracts can be called, which functions, maximum value per call, time window, and total usage count. The session key validator module enforces these constraints on-chain. An expired or over-limit session key is rejected at validation time, not at execution time.

- **EntryPoint v0.7 changed the UserOp struct** -- v0.6 and v0.7 are not compatible. v0.7 packs gas fields (verificationGasLimit + callGasLimit into a single bytes32), uses `accountGasLimits` instead of separate fields, and adds `paymasterAndData` packing. If your bundler returns "invalid UserOp" errors, check which EntryPoint version you are targeting.

- **Nonces are 2D in ERC-4337** -- the nonce field is a `uint256` where the upper 192 bits are the "key" and the lower 64 bits are the sequential nonce for that key. This allows parallel UserOp submission across different nonce keys without blocking. Most SDKs handle this automatically, but raw UserOp construction requires understanding this.

## ERC-4337 Core Architecture

### EntryPoint v0.7

The EntryPoint is a singleton contract deployed at a deterministic address across all EVM chains. It serves as the central coordinator: validating UserOperations, calling smart account contracts, handling paymaster interactions, and managing gas accounting.

> **Last verified:** February 2026

| Contract | Address |
|----------|---------|
| EntryPoint v0.7 | `0x0000000071727De22E5E9d8BAf0edAc6f37da032` |
| EntryPoint v0.6 | `0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789` |

### UserOperation Struct (v0.7)

```solidity
struct PackedUserOperation {
    address sender;
    uint256 nonce;
    bytes initCode;
    bytes callData;
    bytes32 accountGasLimits;      // verificationGasLimit (16 bytes) || callGasLimit (16 bytes)
    uint256 preVerificationGas;
    bytes32 gasFees;               // maxPriorityFeePerGas (16 bytes) || maxFeePerGas (16 bytes)
    bytes paymasterAndData;        // paymaster (20 bytes) || paymasterVerificationGasLimit (16 bytes) || paymasterPostOpGasLimit (16 bytes) || paymasterData
    bytes signature;
}
```

| Field | Purpose |
|-------|---------|
| `sender` | Smart account address that will execute the operation |
| `nonce` | Anti-replay value (upper 192 bits = key, lower 64 bits = sequence) |
| `initCode` | Factory address + calldata for first-time account deployment (empty if account exists) |
| `callData` | Encoded call to the account's `execute` function |
| `accountGasLimits` | Packed verification and call gas limits |
| `preVerificationGas` | Gas to compensate bundler for calldata and overhead costs |
| `gasFees` | Packed EIP-1559 gas price fields |
| `paymasterAndData` | Paymaster address + gas limits + custom data (empty if self-paying) |
| `signature` | Signature validated by the account's `validateUserOp` |

### Smart Account Interface

Every ERC-4337 smart account must implement:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IAccount {
    /// @notice Validates a UserOperation
    /// @param userOp The packed user operation
    /// @param userOpHash Hash of the user operation (used for signature verification)
    /// @param missingAccountFunds Amount the account must prefund the EntryPoint
    /// @return validationData 0 for success, 1 for failure, or packed (authorizer, validUntil, validAfter)
    function validateUserOp(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash,
        uint256 missingAccountFunds
    ) external returns (uint256 validationData);
}
```

## UserOperation Lifecycle

```
1. Client constructs UserOp (callData, gas limits, signature)
         |
2. Client sends UserOp to bundler via eth_sendUserOperation RPC
         |
3. Bundler validates UserOp locally (simulation, gas checks, signature)
         |
4. Bundler packages UserOps into a bundle transaction
         |
5. Bundler calls EntryPoint.handleOps(ops[], beneficiary)
         |
6. EntryPoint loops through each UserOp:
   a. If initCode present -> deploy account via factory
   b. Call account.validateUserOp() -> must return 0 for success
   c. If paymaster present -> call paymaster.validatePaymasterUserOp()
   d. Call account with callData (the actual operation)
   e. If paymaster present -> call paymaster.postOp()
         |
7. EntryPoint settles gas: refunds excess, pays bundler from account/paymaster deposit
```

### Validation Phase

The validation phase runs with a restricted opcode set (no TIMESTAMP, BLOCKHASH, etc. relative to other accounts) to ensure simulation determinism. The account's `validateUserOp` must:

1. Verify the signature over `userOpHash`
2. Pay `missingAccountFunds` to the EntryPoint (or have sufficient deposit)
3. Return `0` for valid, `1` for invalid, or a packed value with time-range validity

### Execution Phase

After all UserOps in a bundle pass validation, the EntryPoint calls each account with the `callData`. The account contract is `msg.sender` for any downstream calls. If execution reverts, the gas is still consumed and paid for.

## Bundler Role

Bundlers are off-chain services that collect UserOperations from users, validate them, and submit them as bundle transactions to the EntryPoint. They earn gas refunds as compensation.

### Bundler RPC Methods

| Method | Purpose |
|--------|---------|
| `eth_sendUserOperation` | Submit a UserOp for inclusion |
| `eth_estimateUserOperationGas` | Estimate gas limits for a UserOp |
| `eth_getUserOperationByHash` | Look up a UserOp by its hash |
| `eth_getUserOperationReceipt` | Get execution receipt for a UserOp |
| `eth_supportedEntryPoints` | List EntryPoint addresses the bundler supports |
| `eth_chainId` | Return the chain ID |

### Major Bundler Providers

| Provider | Endpoint Format | Notes |
|----------|----------------|-------|
| Pimlico | `https://api.pimlico.io/v2/{chain}/rpc?apikey={key}` | Alto bundler, widest chain support |
| Alchemy | `https://{chain}.g.alchemy.com/v2/{key}` | Rundler, integrated with Alchemy platform |
| Stackup | `https://api.stackup.sh/v1/node/{key}` | Stackup bundler, ERC-4337 pioneers |

## EIP-7702 EOA Delegation

EIP-7702 introduces Type 0x04 transactions that let EOAs set a delegation designator, making the EOA's code point to a smart contract implementation. This is a protocol-level change (Pectra upgrade) that does not require ERC-4337 infrastructure.

### How Delegation Works

A Type 0x04 transaction includes an `authorizationList` -- an array of signed authorization tuples. When processed, the EOA's code is set to `0xef0100 || address`, a special delegation designator prefix. Any call to the EOA now delegates execution to the implementation contract at `address`.

### Authorization Tuple

```typescript
interface Authorization {
  chainId: bigint;    // 0 for chain-agnostic, or specific chain ID
  address: Address;   // Implementation contract to delegate to
  nonce: bigint;      // EOA's current nonce (prevents replay)
  yParity: number;    // Signature recovery parameter
  r: `0x${string}`;   // Signature component
  s: `0x${string}`;   // Signature component
}
```

### Delegation with viem

```typescript
import { createWalletClient, http, parseEther } from "viem";
import { mainnet } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";
import { eip7702Actions } from "viem/experimental";

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
}).extend(eip7702Actions());

// BatchExecutor is a contract that implements execute(Call[]) for batching
const BATCH_EXECUTOR = "0x..." as const; // Your batch executor implementation

async function delegateAndBatch() {
  const authorization = await walletClient.signAuthorization({
    contractAddress: BATCH_EXECUTOR,
  });

  const hash = await walletClient.sendTransaction({
    authorizationList: [authorization],
    to: account.address,
    data: encodeFunctionData({
      abi: batchExecutorAbi,
      functionName: "execute",
      args: [
        [
          { target: TOKEN_A, value: 0n, data: approveCalldata },
          { target: ROUTER, value: 0n, data: swapCalldata },
        ],
      ],
    }),
  });

  return hash;
}
```

### Per-Transaction vs Persistent Delegation

- **Per-transaction:** Sign an authorization with `chainId: 0` or the specific chain. The delegation persists until explicitly cleared or overwritten by another Type 0x04 transaction. There is no automatic expiry.
- **Clearing delegation:** Send a Type 0x04 transaction with an authorization pointing to `address(0)` to remove the delegation designator and restore the EOA to its original state.
- **Key insight:** The EOA retains its private key and can always send a new Type 0x04 transaction to change or clear delegation. The delegated code cannot lock out the EOA owner.

## ERC-4337 + EIP-7702 Combined

The most powerful pattern combines both standards: EIP-7702 makes the EOA behave like a smart account, and ERC-4337 provides bundler infrastructure and paymaster sponsorship for that account.

### How It Works

1. User signs an EIP-7702 authorization delegating their EOA to a smart account implementation (e.g., SimpleAccount, Kernel)
2. The UserOp includes the `eip7702Auth` in its authorization list
3. The bundler submits a Type 0x04 transaction that both sets the delegation and processes the UserOp through the EntryPoint
4. The EOA now has smart account capabilities (validation logic, execute function) and can use paymasters

```typescript
import { toSmartAccount } from "permissionless/accounts";
import { createSmartAccountClient } from "permissionless";
import { createPimlicoClient } from "permissionless/clients/pimlico";
import { http } from "viem";
import { mainnet } from "viem/chains";
import { entryPoint07Address } from "viem/account-abstraction";
import { privateKeyToAccount } from "viem/accounts";
import { eip7702Actions } from "viem/experimental";

const owner = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const pimlicoClient = createPimlicoClient({
  transport: http(
    `https://api.pimlico.io/v2/1/rpc?apikey=${process.env.PIMLICO_API_KEY}`
  ),
  entryPoint: {
    address: entryPoint07Address,
    version: "0.7",
  },
});

// The EOA becomes the smart account via 7702 delegation
const smartAccount = await toSmartAccount({
  client: publicClient,
  entryPoint: {
    address: entryPoint07Address,
    version: "0.7",
  },
  owner,
  // 7702 delegation target -- the EOA will delegate to this implementation
  implementation: SMART_ACCOUNT_IMPLEMENTATION,
});

const smartAccountClient = createSmartAccountClient({
  account: smartAccount,
  chain: mainnet,
  bundlerTransport: http(
    `https://api.pimlico.io/v2/1/rpc?apikey=${process.env.PIMLICO_API_KEY}`
  ),
  paymaster: pimlicoClient,
});
```

### Benefits of Combined Approach

| Capability | 4337 Only | 7702 Only | Combined |
|-----------|-----------|-----------|----------|
| Same EOA address | No (new contract) | Yes | Yes |
| Gas sponsorship | Yes (paymasters) | No | Yes |
| Batched calls | Yes | Yes | Yes |
| Session keys | Yes (modules) | Requires custom impl | Yes (modules) |
| Works without bundler | No | Yes | Flexible |
| Cross-chain replay protection | Via nonce keys | Via chainId in auth | Both |

## Paymaster Patterns

### Verifying Paymaster

A verifying paymaster sponsors gas for UserOps that carry a valid off-chain signature from the paymaster operator. The operator controls who gets sponsored.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IPaymaster} from "account-abstraction/interfaces/IPaymaster.sol";
import {PackedUserOperation} from "account-abstraction/interfaces/PackedUserOperation.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {MessageHashUtils} from "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";

/// @notice Sponsors UserOps that carry a valid signature from the verifying signer
contract VerifyingPaymaster is IPaymaster {
    using ECDSA for bytes32;
    using MessageHashUtils for bytes32;

    address public immutable entryPoint;
    address public verifyingSigner;

    error InvalidSignature();
    error CallerNotEntryPoint();

    modifier onlyEntryPoint() {
        if (msg.sender != entryPoint) revert CallerNotEntryPoint();
        _;
    }

    constructor(address _entryPoint, address _signer) {
        entryPoint = _entryPoint;
        verifyingSigner = _signer;
    }

    function validatePaymasterUserOp(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash,
        uint256 maxCost
    ) external onlyEntryPoint returns (bytes memory context, uint256 validationData) {
        // paymasterData layout: signature (65 bytes)
        bytes calldata paymasterData = userOp.paymasterAndData[52:];

        bytes32 hash = keccak256(
            abi.encode(userOp.sender, userOp.nonce, userOpHash)
        ).toEthSignedMessageHash();

        address recovered = hash.recover(paymasterData[:65]);
        if (recovered != verifyingSigner) revert InvalidSignature();

        return (abi.encode(userOp.sender), 0);
    }

    function postOp(
        PostOpMode mode,
        bytes calldata context,
        uint256 actualGasCost,
        uint256 actualUserOpFeePerGas
    ) external onlyEntryPoint {}
}
```

### ERC-20 Paymaster

An ERC-20 paymaster lets users pay gas fees in ERC-20 tokens instead of ETH. The paymaster holds an ETH deposit in the EntryPoint and charges the user's tokens in `postOp`.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IPaymaster} from "account-abstraction/interfaces/IPaymaster.sol";
import {PackedUserOperation} from "account-abstraction/interfaces/PackedUserOperation.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IEntryPoint} from "account-abstraction/interfaces/IEntryPoint.sol";

/// @notice Charges users in ERC-20 tokens for gas sponsorship
/// @dev Users must approve this paymaster for the payment token
contract ERC20Paymaster is IPaymaster {
    address public immutable entryPoint;
    IERC20 public immutable token;
    // Price oracle would set this -- simplified for reference
    uint256 public tokenPricePerGas;

    error CallerNotEntryPoint();
    error InsufficientTokenBalance();

    modifier onlyEntryPoint() {
        if (msg.sender != entryPoint) revert CallerNotEntryPoint();
        _;
    }

    constructor(address _entryPoint, address _token, uint256 _tokenPricePerGas) {
        entryPoint = _entryPoint;
        token = IERC20(_token);
        tokenPricePerGas = _tokenPricePerGas;
    }

    function validatePaymasterUserOp(
        PackedUserOperation calldata userOp,
        bytes32,
        uint256 maxCost
    ) external onlyEntryPoint returns (bytes memory context, uint256 validationData) {
        uint256 maxTokenCost = maxCost * tokenPricePerGas;
        uint256 balance = token.balanceOf(userOp.sender);
        if (balance < maxTokenCost) revert InsufficientTokenBalance();

        return (abi.encode(userOp.sender, maxTokenCost), 0);
    }

    function postOp(
        PostOpMode,
        bytes calldata context,
        uint256 actualGasCost,
        uint256
    ) external onlyEntryPoint {
        (address sender, ) = abi.decode(context, (address, uint256));
        uint256 actualTokenCost = actualGasCost * tokenPricePerGas;

        // CEI: state is updated via token transfer, then no further external calls
        token.transferFrom(sender, address(this), actualTokenCost);
    }
}
```

### Client-Side Paymaster Integration

```typescript
import { createSmartAccountClient } from "permissionless";
import { createPimlicoClient } from "permissionless/clients/pimlico";
import { http } from "viem";
import { entryPoint07Address } from "viem/account-abstraction";

const pimlicoClient = createPimlicoClient({
  transport: http(
    `https://api.pimlico.io/v2/1/rpc?apikey=${process.env.PIMLICO_API_KEY}`
  ),
  entryPoint: {
    address: entryPoint07Address,
    version: "0.7",
  },
});

const smartAccountClient = createSmartAccountClient({
  account: smartAccount,
  chain: mainnet,
  bundlerTransport: http(
    `https://api.pimlico.io/v2/1/rpc?apikey=${process.env.PIMLICO_API_KEY}`
  ),
  paymaster: pimlicoClient,
  userOperation: {
    estimateFeesPerGas: async () => {
      return (await pimlicoClient.getUserOperationGasPrice()).fast;
    },
  },
});

const txHash = await smartAccountClient.sendTransaction({
  to: "0xRecipient..." as `0x${string}`,
  value: parseEther("0.01"),
  data: "0x",
});
```

## SDK: permissionless.js

permissionless.js is a TypeScript SDK built on viem for ERC-4337 smart accounts. It supports multiple smart account implementations, bundlers, and paymasters.

### Setup

```bash
npm install permissionless viem
```

### Create Smart Account Client

```typescript
import { createSmartAccountClient } from "permissionless";
import { toSimpleSmartAccount } from "permissionless/accounts";
import { createPublicClient, http } from "viem";
import { sepolia } from "viem/chains";
import { entryPoint07Address } from "viem/account-abstraction";
import { privateKeyToAccount } from "viem/accounts";

const publicClient = createPublicClient({
  chain: sepolia,
  transport: http(process.env.RPC_URL),
});

const owner = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const simpleAccount = await toSimpleSmartAccount({
  client: publicClient,
  owner,
  entryPoint: {
    address: entryPoint07Address,
    version: "0.7",
  },
});

const smartAccountClient = createSmartAccountClient({
  account: simpleAccount,
  chain: sepolia,
  bundlerTransport: http(
    `https://api.pimlico.io/v2/sepolia/rpc?apikey=${process.env.PIMLICO_API_KEY}`
  ),
});
```

### Send a UserOp

```typescript
const txHash = await smartAccountClient.sendTransaction({
  to: "0xRecipient..." as `0x${string}`,
  value: parseEther("0.01"),
  data: "0x",
});

console.log(`Transaction hash: ${txHash}`);
```

### Batch Transactions

```typescript
const txHash = await smartAccountClient.sendUserOperation({
  calls: [
    {
      to: TOKEN_ADDRESS,
      abi: erc20Abi,
      functionName: "approve",
      args: [SPENDER, parseEther("100")],
    },
    {
      to: PROTOCOL_ADDRESS,
      abi: protocolAbi,
      functionName: "deposit",
      args: [parseEther("100")],
    },
  ],
});

const receipt = await smartAccountClient.waitForUserOperationReceipt({
  hash: txHash,
});

if (!receipt.success) {
  throw new Error(`UserOp failed: ${receipt.reason}`);
}
```

## SDK: ZeroDev

ZeroDev provides the Kernel smart account -- a modular ERC-7579 compatible smart account with plugin support for session keys, passkeys, and recovery.

### Kernel Account Setup

```bash
npm install @zerodev/sdk @zerodev/ecdsa-validator permissionless viem
```

```typescript
import { createKernelAccount, createKernelAccountClient } from "@zerodev/sdk";
import { signerToEcdsaValidator } from "@zerodev/ecdsa-validator";
import { createPublicClient, http } from "viem";
import { sepolia } from "viem/chains";
import { entryPoint07Address } from "viem/account-abstraction";
import { privateKeyToAccount } from "viem/accounts";

const publicClient = createPublicClient({
  chain: sepolia,
  transport: http(process.env.RPC_URL),
});

const signer = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const ecdsaValidator = await signerToEcdsaValidator(publicClient, {
  signer,
  entryPoint: entryPoint07Address,
});

const kernelAccount = await createKernelAccount(publicClient, {
  plugins: {
    sudo: ecdsaValidator,
  },
  entryPoint: entryPoint07Address,
});

const kernelClient = createKernelAccountClient({
  account: kernelAccount,
  chain: sepolia,
  bundlerTransport: http(process.env.BUNDLER_URL),
  paymaster: {
    getPaymasterData: async (userOperation) => {
      // Return paymaster data from your paymaster service
      return { paymasterAndData: "0x" };
    },
  },
});
```

### Send Transaction with Kernel

```typescript
const txHash = await kernelClient.sendTransaction({
  to: "0xRecipient..." as `0x${string}`,
  value: parseEther("0.01"),
  data: "0x",
});
```

## Session Keys

Session keys are scoped signing keys that allow limited actions without requiring the main account owner's signature for every operation. They are implemented as ERC-7579 validator modules.

### Session Key Constraints

| Constraint | Description |
|-----------|-------------|
| Contract whitelist | Only specific contract addresses can be called |
| Function whitelist | Only specific function selectors are allowed |
| Value limit | Maximum ETH value per call |
| Time window | Valid only between `validAfter` and `validUntil` timestamps |
| Usage count | Maximum number of times the session key can be used |
| Spending limit | Maximum total token spend across all calls |

### Creating a Session Key with ZeroDev

```typescript
import {
  createKernelAccount,
  createKernelAccountClient,
} from "@zerodev/sdk";
import {
  toPermissionValidator,
  toSudoPolicy,
  toCallPolicy,
  CallPolicyVersion,
  ParamCondition,
} from "@zerodev/permissions";
import { toECDSASigner } from "@zerodev/permissions/signers";
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";

// Generate a temporary session key
const sessionPrivateKey = generatePrivateKey();
const sessionKeySigner = privateKeyToAccount(sessionPrivateKey);

const ecdsaSigner = toECDSASigner({
  signer: sessionKeySigner,
});

const permissionValidator = await toPermissionValidator(publicClient, {
  entryPoint: entryPoint07Address,
  signer: ecdsaSigner,
  policies: [
    toCallPolicy({
      policyVersion: CallPolicyVersion.V0_0_4,
      permissions: [
        {
          target: TOKEN_ADDRESS,
          abi: erc20Abi,
          functionName: "transfer",
          args: [
            {
              condition: ParamCondition.EQUAL,
              value: ALLOWED_RECIPIENT,
            },
            null, // Any amount (or add a condition)
          ],
        },
      ],
    }),
  ],
});

const sessionKeyAccount = await createKernelAccount(publicClient, {
  plugins: {
    sudo: ecdsaValidator,
    regular: permissionValidator,
  },
  entryPoint: entryPoint07Address,
});
```

### Using a Session Key

```typescript
const sessionClient = createKernelAccountClient({
  account: sessionKeyAccount,
  chain: sepolia,
  bundlerTransport: http(process.env.BUNDLER_URL),
});

// This transaction is signed by the session key, validated by the permission module
const txHash = await sessionClient.sendTransaction({
  to: TOKEN_ADDRESS,
  abi: erc20Abi,
  functionName: "transfer",
  args: [ALLOWED_RECIPIENT, parseEther("10")],
});
```

### Revoking a Session Key

Session keys can be revoked by the account owner by disabling the permission validator or removing the specific session from the validator's storage:

```typescript
const revokeTx = await kernelClient.sendUserOperation({
  calls: [
    {
      to: kernelAccount.address,
      data: encodeFunctionData({
        abi: kernelAccountAbi,
        functionName: "disablePlugin",
        args: [permissionValidatorAddress],
      }),
    },
  ],
});
```

## Gas Abstraction in Practice

To build a fully gasless flow, create a `smartAccountClient` with a `paymaster` parameter. The paymaster's EntryPoint deposit covers all gas costs. See the `examples/simple-smart-account/` example for a complete working implementation.

### Gas Estimation for UserOps

```typescript
const gasEstimate = await pimlicoClient.estimateUserOperationGas({
  sender: account.address,
  nonce: await account.getNonce(),
  callData: await account.encodeCalls([
    { to: recipient, value: parseEther("0.01"), data: "0x" },
  ]),
  signature: await account.getDummySignature(),
});

// gasEstimate contains:
// - preVerificationGas: bundler overhead compensation
// - verificationGasLimit: gas for validateUserOp
// - callGasLimit: gas for the actual execution
```

### preVerificationGas Calculation

`preVerificationGas` compensates the bundler for calldata costs and fixed overhead. On L2s with L1 data posting costs (Arbitrum, Optimism, Base), this value is significantly higher because it includes the L1 data fee.

```typescript
// L1 chains: ~21000 + calldata_cost
// L2 chains: ~21000 + calldata_cost + l1_data_fee
// Always use bundler estimation -- manual calculation is error-prone on L2s
const gasPrice = await pimlicoClient.getUserOperationGasPrice();
```

## Choosing Your Stack

| Use Case | Recommendation | Why |
|----------|---------------|-----|
| New app, new users, gasless onboarding | ERC-4337 + permissionless.js + Pimlico | Full gas abstraction, paymaster sponsoring, widest tooling |
| Existing app, users have EOAs | EIP-7702 only | No migration needed, no new addresses, works with existing wallets |
| DeFi power users wanting batching | EIP-7702 only | Minimal overhead, batch calls in single tx, keep same address |
| Gaming with session-based actions | ERC-4337 + ZeroDev Kernel | Session keys for in-game actions, modular validators |
| Enterprise with compliance needs | ERC-4337 + Safe | Multisig, role-based access, audit trail |
| Maximum flexibility | ERC-4337 + EIP-7702 combined | EOA upgrades in-place, gets paymaster + session key support |
| Mobile wallet | ERC-4337 + passkey signer | WebAuthn/passkey as account signer, no seed phrase |

### When to Use 4337 Only

- You need paymaster gas sponsorship
- You need modular validator/executor plugins (ERC-7579)
- Your users are creating new accounts (onboarding flow)
- You need bundler infrastructure (high throughput, MEV protection)

### When to Use 7702 Only

- Your users already have EOAs with assets
- You need batching but not gas sponsorship
- You want minimal infrastructure overhead
- You are building a wallet upgrade feature

### When to Combine

- You want EOAs to get paymaster sponsorship
- You need session keys on existing EOA addresses
- You want the "best of both worlds" without address migration

## Contract Addresses

> **Last verified:** February 2026. EntryPoint is deployed at deterministic addresses via CREATE2 across all EVM chains.

| Contract | Address | Chains |
|----------|---------|--------|
| EntryPoint v0.7 | `0x0000000071727De22E5E9d8BAf0edAc6f37da032` | All EVM chains |
| EntryPoint v0.6 | `0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789` | All EVM chains |
| SimpleAccountFactory (v0.7) | `0x91E60e0613810449d098b0b5Ec8b51A0FE8c8985` | Ethereum, Arbitrum, Base, Optimism, Polygon |

```bash
# Verify EntryPoint deployment on any chain
cast code 0x0000000071727De22E5E9d8BAf0edAc6f37da032 --rpc-url $RPC_URL
```

## References

- [ERC-4337: Account Abstraction Using Alt Mempool](https://eips.ethereum.org/EIPS/eip-4337)
- [EIP-7702: Set EOA Account Code](https://eips.ethereum.org/EIPS/eip-7702)
- [ERC-7579: Minimal Modular Smart Accounts](https://eips.ethereum.org/EIPS/eip-7579)
- [EntryPoint v0.7 Source (eth-infinitism)](https://github.com/eth-infinitism/account-abstraction/tree/develop/contracts)
- [permissionless.js Docs](https://docs.pimlico.io/permissionless)
- [ZeroDev Docs](https://docs.zerodev.app)
- [Pimlico Docs](https://docs.pimlico.io)
- [Alchemy Account Kit Docs](https://accountkit.alchemy.com/react/overview)
- [viem EIP-7702 Experimental](https://viem.sh/experimental/eip7702)
