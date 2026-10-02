---
name: safe
description: "Safe (formerly Gnosis Safe) multisig SDK for creating, managing, and executing multi-signature transactions. Covers Safe{Core} SDK (protocol-kit, api-kit, relay-kit), deploying new Safes, proposing and confirming transactions, modules and guards, EIP-1271 signature validation, and Safe Transaction Service integration. Works on Ethereum, Arbitrum, Base, Optimism, Polygon, and 15+ EVM chains."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - safe
  - multisig
  - gnosis-safe
  - wallet
  - governance
---

# Safe

Safe is the most widely used smart account infrastructure on EVM chains. Over $100B in assets are secured by Safe contracts. It provides programmable multi-signature wallets with modular extensions via modules and guards.

## What You Probably Got Wrong

> The Safe ecosystem rebranded and restructured its SDK in 2023-2024. Most LLM training data references the old package names and deprecated APIs.

- **Gnosis Safe is now just "Safe"** -- The project rebranded. Package scope changed from `@gnosis.pm/safe-*` and `@safe-global/safe-*` (old) to `@safe-global/protocol-kit`, `@safe-global/api-kit`, `@safe-global/relay-kit`. If you see `@gnosis.pm/` imports, you are using deprecated packages.
- **Safe{Core} SDK has three kits, not one** -- `protocol-kit` handles on-chain Safe interactions (deploy, sign, execute). `api-kit` talks to the Safe Transaction Service REST API (propose, confirm, list pending). `relay-kit` sponsors gas via Gelato/relay. They are separate npm packages.
- **`EtherAdapter` is removed** -- The old `EthersAdapter` / `Web3Adapter` pattern is gone. Protocol Kit v4+ takes a `provider` (RPC URL or EIP-1193) and `signer` (private key or passkey) directly. No adapter classes.
- **Transaction Service URLs are chain-specific** -- Each network has its own Transaction Service. Mainnet is `https://safe-transaction-mainnet.safe.global`, not a generic endpoint. Using the wrong URL silently fails. API Kit takes a `chainId` and resolves the URL automatically since v2.
- **Safe modules are NOT the same as guards** -- Modules can execute transactions on behalf of the Safe without owner signatures (powerful, dangerous). Guards are hooks that run pre/post-execution for validation checks (like a firewall). Confusing them leads to security holes.
- **EIP-1271 signature validation requires the Safe, not an EOA** -- When a Safe signs a message, you validate against the Safe contract's `isValidSignature(bytes32, bytes)`, not against individual owner addresses. The hash must be the Safe-specific message hash from `getMessageHash()`.
- **`execTransaction` is not `exec`** -- The on-chain function is `execTransaction` with a specific parameter order. The SDK abstracts this but if you call the contract directly, getting the signature encoding wrong is the most common revert cause.
- **Nonces are sequential, not random** -- Safe uses a sequential nonce starting at 0. Skipping a nonce blocks all subsequent transactions. Use the Transaction Service to get the next nonce.

## Quick Start

### Installation

```bash
npm install @safe-global/protocol-kit @safe-global/api-kit @safe-global/types-kit
```

### Connect to an Existing Safe

```typescript
import Safe from "@safe-global/protocol-kit";

const protocolKit = await Safe.init({
  provider: process.env.RPC_URL!,
  signer: process.env.OWNER_PRIVATE_KEY!,
  safeAddress: "0x...", // existing Safe address
});

const owners = await protocolKit.getOwners();
const threshold = await protocolKit.getThreshold();
const nonce = await protocolKit.getNonce();

console.log({ owners, threshold, nonce });
```

### Initialize API Kit

```typescript
import SafeApiKit from "@safe-global/api-kit";

const apiKit = new SafeApiKit({
  chainId: 1n, // mainnet -- use bigint
});

const pendingTxs = await apiKit.getPendingTransactions("0xSafeAddress");
```

## Creating a Safe

### Deploy a New Safe

```typescript
import Safe from "@safe-global/protocol-kit";

const protocolKit = await Safe.init({
  provider: process.env.RPC_URL!,
  signer: process.env.DEPLOYER_PRIVATE_KEY!,
  predictedSafe: {
    safeAccountConfig: {
      owners: [
        "0xOwner1Address",
        "0xOwner2Address",
        "0xOwner3Address",
      ],
      threshold: 2, // 2-of-3 multisig
    },
    // Optional: specify Safe version and salt nonce
    safeDeploymentConfig: {
      saltNonce: BigInt(Date.now()).toString(),
      safeVersion: "1.4.1",
    },
  },
});

// Predict the address before deployment
const predictedAddress = await protocolKit.getAddress();
console.log("Safe will deploy to:", predictedAddress);

// Deploy the Safe
const deploymentResult = await protocolKit.createSafeDeploymentTransaction();

// After deployment, reinitialize with the deployed address
const deployedKit = await Safe.init({
  provider: process.env.RPC_URL!,
  signer: process.env.DEPLOYER_PRIVATE_KEY!,
  safeAddress: predictedAddress,
});

const isDeployed = await deployedKit.isSafeDeployed();
console.log("Deployed:", isDeployed);
```

### Predict Safe Address (Counterfactual)

```typescript
import Safe from "@safe-global/protocol-kit";

const protocolKit = await Safe.init({
  provider: process.env.RPC_URL!,
  signer: process.env.OWNER_PRIVATE_KEY!,
  predictedSafe: {
    safeAccountConfig: {
      owners: ["0xOwner1", "0xOwner2"],
      threshold: 1,
    },
    safeDeploymentConfig: {
      saltNonce: "12345",
      safeVersion: "1.4.1",
    },
  },
});

// Address is deterministic — same inputs always produce same address
const predictedAddress = await protocolKit.getAddress();
```

## Proposing Transactions

### Full Lifecycle: Create, Propose, Confirm, Execute

```typescript
import Safe from "@safe-global/protocol-kit";
import SafeApiKit from "@safe-global/api-kit";
import { MetaTransactionData, OperationType } from "@safe-global/types-kit";

const SAFE_ADDRESS = "0xYourSafeAddress";
const CHAIN_ID = 1n;

// --- Step 1: Owner A creates and proposes the transaction ---

let protocolKit = await Safe.init({
  provider: process.env.RPC_URL!,
  signer: process.env.OWNER_A_PRIVATE_KEY!,
  safeAddress: SAFE_ADDRESS,
});

const apiKit = new SafeApiKit({ chainId: CHAIN_ID });

const txData: MetaTransactionData = {
  to: "0xRecipientAddress",
  value: "500000000000000000", // 0.5 ETH in wei — always a string
  data: "0x", // empty for ETH transfer
  operation: OperationType.Call, // 0 = Call, 1 = DelegateCall
};

const safeTx = await protocolKit.createTransaction({
  transactions: [txData],
});

// Sign the transaction (Owner A)
const signedTx = await protocolKit.signTransaction(safeTx);

const safeTxHash = await protocolKit.getTransactionHash(signedTx);

// Propose to the Transaction Service
await apiKit.proposeTransaction({
  safeAddress: SAFE_ADDRESS,
  safeTransactionData: signedTx.data,
  safeTxHash,
  senderAddress: await protocolKit.getAddress(),
  senderSignature: signedTx.encodedSignatures(),
});

console.log("Proposed tx:", safeTxHash);

// --- Step 2: Owner B confirms the transaction ---

protocolKit = await Safe.init({
  provider: process.env.RPC_URL!,
  signer: process.env.OWNER_B_PRIVATE_KEY!,
  safeAddress: SAFE_ADDRESS,
});

const pendingTx = await apiKit.getTransaction(safeTxHash);
const confirmedTx = await protocolKit.signTransaction(pendingTx);

await apiKit.confirmTransaction(
  safeTxHash,
  confirmedTx.encodedSignatures()
);

console.log("Confirmed by Owner B");

// --- Step 3: Execute once threshold is met ---

const fullySignedTx = await apiKit.getTransaction(safeTxHash);

const executionResult = await protocolKit.executeTransaction(fullySignedTx);
console.log("Executed:", executionResult.hash);
```

### Batch Transactions (MultiSend)

```typescript
import { MetaTransactionData, OperationType } from "@safe-global/types-kit";

const transactions: MetaTransactionData[] = [
  {
    to: "0xTokenAddress",
    value: "0",
    // ERC-20 transfer(address,uint256)
    data: "0xa9059cbb000000000000000000000000RecipientAddr0000000000000000000000000000000000000000000000000de0b6b3a7640000",
    operation: OperationType.Call,
  },
  {
    to: "0xAnotherContract",
    value: "0",
    data: "0x...", // another call
    operation: OperationType.Call,
  },
];

// Protocol Kit automatically routes through MultiSend when multiple txs are passed
const batchTx = await protocolKit.createTransaction({ transactions });
const signedBatch = await protocolKit.signTransaction(batchTx);
const result = await protocolKit.executeTransaction(signedBatch);
```

### Reject a Pending Transaction

```typescript
// A rejection is a zero-value transaction to the Safe itself with the same nonce
const rejectionTx = await protocolKit.createRejectionTransaction(
  pendingTx.nonce
);
const signedRejection = await protocolKit.signTransaction(rejectionTx);
const rejectionHash = await protocolKit.getTransactionHash(signedRejection);

await apiKit.proposeTransaction({
  safeAddress: SAFE_ADDRESS,
  safeTransactionData: signedRejection.data,
  safeTxHash: rejectionHash,
  senderAddress: await protocolKit.getAddress(),
  senderSignature: signedRejection.encodedSignatures(),
});
```

## Safe Modules

Modules are contracts authorized to execute transactions on behalf of a Safe without requiring the normal owner signature threshold. They extend Safe functionality but carry high risk since they bypass multisig controls.

### Enable a Module

```typescript
const enableModuleTx = await protocolKit.createEnableModuleTx(
  "0xModuleAddress"
);
const signedTx = await protocolKit.signTransaction(enableModuleTx);
const result = await protocolKit.executeTransaction(signedTx);

const isEnabled = await protocolKit.isModuleEnabled("0xModuleAddress");
console.log("Module enabled:", isEnabled);
```

### Disable a Module

```typescript
const disableModuleTx = await protocolKit.createDisableModuleTx(
  "0xModuleAddress"
);
const signedTx = await protocolKit.signTransaction(disableModuleTx);
await protocolKit.executeTransaction(signedTx);
```

### List Active Modules

```typescript
const modules = await protocolKit.getModules();
console.log("Active modules:", modules);
```

### Common Safe Modules

| Module | Purpose | Risk Level |
|--------|---------|------------|
| Allowance Module | Recurring spending limits for individual owners | Medium -- owner can drain up to allowance |
| Recovery Module | Social recovery via guardians when keys are lost | High -- guardians can take over Safe |
| Delay Module | Enforces a cooldown period before module txs execute | Low -- adds safety to other modules |
| Roles Module (Zodiac) | Role-based access control for granular permissions | Medium -- complexity increases attack surface |

### Guards vs Modules

| Feature | Module | Guard |
|---------|--------|-------|
| Can initiate transactions | Yes | No |
| Runs on every transaction | No | Yes |
| Bypasses threshold | Yes | No (enforces additional checks) |
| Set via | `enableModule` | `setGuard` |
| Use case | Automation, spending limits | Policy enforcement, whitelists |

```typescript
// Set a transaction guard
const setGuardTx = await protocolKit.createEnableGuardTx("0xGuardAddress");
const signed = await protocolKit.signTransaction(setGuardTx);
await protocolKit.executeTransaction(signed);

// Remove a guard (pass zero address)
const removeGuardTx = await protocolKit.createDisableGuardTx();
const signedRemove = await protocolKit.signTransaction(removeGuardTx);
await protocolKit.executeTransaction(signedRemove);
```

## EIP-1271 Signature Validation

Safe supports contract-based signatures per EIP-1271, allowing a Safe to "sign" messages and have dApps verify them.

### Sign a Message

```typescript
import { hashSafeMessage } from "@safe-global/protocol-kit";

const rawMessage = "Hello from Safe";
const messageHash = hashSafeMessage(rawMessage);

const signedMessage = await protocolKit.signMessage(
  protocolKit.createMessage(rawMessage)
);

// On-chain validation via the Safe contract
// Other contracts call: safe.isValidSignature(messageHash, signature)
// Returns 0x20c13b0b for valid signatures (EIP-1271 magic value)
```

### Sign Typed Data (EIP-712)

```typescript
const typedData = {
  types: {
    Order: [
      { name: "maker", type: "address" },
      { name: "amount", type: "uint256" },
    ],
  },
  primaryType: "Order" as const,
  domain: {
    name: "MyDApp",
    version: "1",
    chainId: 1n,
    verifyingContract: "0xContractAddress" as `0x${string}`,
  },
  message: {
    maker: "0xMakerAddress",
    amount: 1000000n,
  },
};

const signedTypedData = await protocolKit.signTypedData(typedData);
```

## Contract Addresses

> **Last verified:** 2025-05-15 (verified onchain via `cast code`)

Safe v1.4.1 uses a deterministic deployment pattern. The singleton and factory addresses are identical across all supported chains.

### Core Contracts (v1.4.1)

| Contract | Address |
|----------|---------|
| Safe Singleton | `0x41675C099F32341bf84BFc5382aF534df5C7461a` |
| Safe Singleton (L2) | `0x29fcB43b46531BcA003ddC8FCB67FFE91900C762` |
| SafeProxyFactory | `0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67` |
| MultiSend | `0x38869bf66a61cF6bDB996A6aE40D5853Fd43B526` |
| MultiSendCallOnly | `0x9641d764fc13c8B624c04430C7356C1C7C8102e2` |
| Compatibility Fallback Handler | `0xfd0732Dc9E303f09fCEf3a7388Ad10A83459Ec99` |
| SignMessageLib | `0xd53cd0aB83D845Ac265BE939c57F53AD838012c9` |
| CreateCall | `0x9b35Af71d77eaf8d7e40252370304687390A1A52` |
| SimulateTxAccessor | `0x3d4BA2E0884aa488718476ca2FB8Efc291A46199` |

> These addresses are the same on Ethereum mainnet, Arbitrum, Base, Optimism, Polygon, Gnosis Chain, Avalanche, BNB Chain, and other supported networks. Safe uses the ERC-2470 singleton factory for deterministic cross-chain deployment.

### Legacy Contracts (v1.3.0) -- Still Widely Used

| Contract | Address |
|----------|---------|
| Safe Singleton | `0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552` |
| Safe Singleton (L2) | `0x3E5c63644E683549055b9Be8653de26E0B4CD36E` |
| SafeProxyFactory | `0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2` |
| MultiSend | `0xA238CBeb142c10Ef7Ad8442C6D1f9E89e07e7761` |
| Compatibility Fallback Handler | `0xf48f2B2d2a534e402487b3ee7C18c33Aec0Fe5e4` |

### Safe Transaction Service URLs

| Network | URL |
|---------|-----|
| Ethereum Mainnet | `https://safe-transaction-mainnet.safe.global` |
| Arbitrum | `https://safe-transaction-arbitrum.safe.global` |
| Base | `https://safe-transaction-base.safe.global` |
| Optimism | `https://safe-transaction-optimism.safe.global` |
| Polygon | `https://safe-transaction-polygon.safe.global` |
| Gnosis Chain | `https://safe-transaction-gnosis-chain.safe.global` |
| Avalanche | `https://safe-transaction-avalanche.safe.global` |
| BNB Chain | `https://safe-transaction-bsc.safe.global` |

> Since API Kit v2, you pass `chainId` and the URL is resolved automatically. You only need these URLs for direct REST API calls.

## Safe Transaction Service API

### Direct REST API Usage

```typescript
const SAFE_ADDRESS = "0xYourSafe";
const TX_SERVICE = "https://safe-transaction-mainnet.safe.global";

// Fetch all pending transactions
const response = await fetch(
  `${TX_SERVICE}/api/v1/safes/${SAFE_ADDRESS}/multisig-transactions/?executed=false&trusted=true`
);
const data = await response.json();

for (const tx of data.results) {
  console.log({
    nonce: tx.nonce,
    to: tx.to,
    value: tx.value,
    confirmations: tx.confirmations.length,
    confirmationsRequired: tx.confirmationsRequired,
    safeTxHash: tx.safeTxHash,
  });
}
```

### Get Safe Info

```typescript
const apiKit = new SafeApiKit({ chainId: 1n });

const safeInfo = await apiKit.getSafeInfo("0xSafeAddress");
console.log({
  address: safeInfo.address,
  nonce: safeInfo.nonce,
  threshold: safeInfo.threshold,
  owners: safeInfo.owners,
  modules: safeInfo.modules,
  guard: safeInfo.guard,
  version: safeInfo.version,
  fallbackHandler: safeInfo.fallbackHandler,
});
```

### List Safes by Owner

```typescript
const apiKit = new SafeApiKit({ chainId: 1n });

const ownerSafes = await apiKit.getSafesByOwner("0xOwnerAddress");
console.log("Safes owned:", ownerSafes.safes);
```

### Get Transaction History

```typescript
const apiKit = new SafeApiKit({ chainId: 1n });

const allTxs = await apiKit.getAllTransactions("0xSafeAddress", {
  executed: true,
  queued: false,
  trusted: true,
});

for (const tx of allTxs.results) {
  console.log({
    nonce: tx.nonce,
    hash: tx.transactionHash,
    timestamp: tx.executionDate,
  });
}
```

## Owner and Threshold Management

```typescript
// Add a new owner (threshold stays the same)
const addOwnerTx = await protocolKit.createAddOwnerTx({
  ownerAddress: "0xNewOwner",
});
const signed = await protocolKit.signTransaction(addOwnerTx);
await protocolKit.executeTransaction(signed);

// Add owner AND change threshold
const addWithThresholdTx = await protocolKit.createAddOwnerTx({
  ownerAddress: "0xNewOwner",
  threshold: 3, // new threshold
});

// Remove an owner (must set new threshold if current exceeds owner count)
const removeOwnerTx = await protocolKit.createRemoveOwnerTx({
  ownerAddress: "0xOwnerToRemove",
  threshold: 2, // required: new threshold after removal
});

// Change threshold only
const changeThresholdTx = await protocolKit.createChangeThresholdTx(3);
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `GS001: Internal Error` | Execution reverted inside the target call | Debug the inner call — the Safe executed successfully but the target reverted |
| `GS013: Safe transaction failed` | `execTransaction` itself reverted (often bad signatures) | Check signature encoding, signer count >= threshold, correct nonce |
| `GS020: Signatures data too short` | Not enough signature bytes passed | Ensure all required owners have signed; concatenate signatures in owner-address-sorted order |
| `GS025: Hash not approved` | On-chain approval hash mismatch | Use `approveHash` with the correct `safeTxHash`, not the inner data hash |
| `GS026: Invalid owner` | Signer is not a current owner of the Safe | Verify the signing address is in `getOwners()` |
| `Nonce too high` (API) | Proposed nonce skips a pending transaction | Get next nonce from Transaction Service, not from on-chain if txs are queued |
| `Threshold not set` | Deploying with threshold 0 or > owner count | Threshold must be >= 1 and <= number of owners |
| `Module not enabled` | Calling `execTransactionFromModule` without enabling it | Call `enableModule` first as a Safe transaction |

## Security

### Threshold Best Practices

| Setup | Recommended For | Risk |
|-------|-----------------|------|
| 1-of-1 | Development, testing only | Single point of failure — one compromised key drains everything |
| 2-of-3 | Small teams, moderate value | Losing 2 keys simultaneously locks funds permanently |
| 3-of-5 | DAOs, treasuries, high value | Balance between security and operational overhead |
| 4-of-7 | Protocol treasuries, 8+ figure holdings | High security, requires coordination for execution |

### Module Security

- **Modules bypass the threshold entirely** -- a compromised module contract can drain the Safe. Only enable audited, well-known modules.
- **Audit module code** before enabling. The `enableModule` call itself requires threshold signatures, but after that the module operates independently.
- **Use the Delay Module** as a safety net when enabling other modules. It adds a cooldown period where module-initiated transactions can be vetoed.
- **Monitor enabled modules** -- list them regularly with `getModules()`. Unexpected modules indicate compromise.

### DelegateCall Risks

- `OperationType.DelegateCall` (value `1`) executes code in the Safe's context. It can modify Safe storage, change owners, or drain funds.
- **Never use DelegateCall with untrusted target contracts.** It is the highest-risk operation type.
- MultiSend uses DelegateCall internally (the Safe delegates to MultiSend which then makes individual calls). This is safe because MultiSend is a stateless contract. Custom DelegateCall targets require auditing.

### Guard Patterns

Guards enforce transaction-level policies. A guard's `checkTransaction` runs before execution and `checkAfterExecution` runs after.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {BaseGuard} from "@safe-global/safe-smart-account/contracts/base/GuardManager.sol";
import {Enum} from "@safe-global/safe-smart-account/contracts/common/Enum.sol";

/// @notice Blocks transactions above a value threshold unless to a whitelisted address
contract SpendingGuard is BaseGuard {
    uint256 public immutable maxValuePerTx;
    mapping(address => bool) public whitelisted;
    address public immutable safe;

    error ExceedsSpendingLimit(uint256 value, uint256 limit);
    error DelegateCallBlocked();

    constructor(address _safe, uint256 _maxValuePerTx) {
        safe = _safe;
        maxValuePerTx = _maxValuePerTx;
    }

    function checkTransaction(
        address to,
        uint256 value,
        bytes memory,
        Enum.Operation operation,
        uint256,
        uint256,
        uint256,
        address,
        address payable,
        bytes memory,
        address
    ) external view override {
        if (operation == Enum.Operation.DelegateCall) {
            revert DelegateCallBlocked();
        }
        if (value > maxValuePerTx && !whitelisted[to]) {
            revert ExceedsSpendingLimit(value, maxValuePerTx);
        }
    }

    function checkAfterExecution(bytes32, bool) external view override {}
}
```

### Key Security Checklist

- Store owner keys on separate devices (hardware wallets preferred)
- Never set threshold to 1 for production Safes holding real value
- Test all transactions on a fork before mainnet execution
- Monitor Safe events: `AddedOwner`, `RemovedOwner`, `ChangedThreshold`, `EnabledModule`, `DisabledModule`
- Verify Safe proxy points to a legitimate singleton using `cast storage <safe> 0x0` -- slot 0 stores the singleton address
- Use `SafeL2` singleton on L2 chains for proper event emission

## ERC-7579 Modular Smart Accounts

ERC-7579 defines a standard interface for modular smart accounts. It specifies four module types -- validators, executors, hooks, and fallback handlers -- that extend account functionality without deploying new proxy contracts. Safe supports ERC-7579 through the Safe7579 adapter.

### Safe7579 Adapter

Safe7579 bridges Safe's native Module/Guard system and ERC-7579's standardized module interface. It installs as both a Safe Module and Fallback Handler on an existing Safe, enabling it to accept any ERC-7579-compliant module. Existing Safes can adopt ERC-7579 modules without migration.

### Module Types

| Type | Role | Example |
|------|------|---------|
| Validator | Controls who can execute UserOps (signature/auth logic) | OwnableValidator, WebAuthn (passkeys) |
| Executor | Performs automated actions on behalf of the Safe | Scheduled transfers, auto-compounding |
| Hook | Pre/post execution checks on every transaction | Spending limits, address allowlists |
| Fallback | Extends the Safe interface with new function selectors | Custom callback handlers |

### Key Modules (Rhinestone)

- **OwnableValidator** -- simple ECDSA owner check, single or multi-owner
- **SmartSessions** -- session keys with policies (time window, value cap, contract/function allowlist)
- **WebAuthn Validator** -- passkey-based signing via the WebAuthn standard
- **Social Recovery** -- guardian-based recovery with threshold and timelock
- **Scheduled Orders** -- cron-like automated execution via keeper network

### Module Registry (ERC-7484)

The Module Registry at `0x000000000069E2a187AEFFb852bF3cCdC95151B2` (same address all EVM chains) provides on-chain attestations for module safety. Rhinestone serves as the primary attester. Safes can require registry attestation before module installation as a trust anchor.

### Installing a Module

```typescript
import { installModule } from "@rhinestone/module-sdk";
import { sendUserOperation } from "permissionless";
import { erc7579Actions } from "permissionless/actions/erc7579";

const smartAccountClient = walletClient.extend(
  erc7579Actions({ entryPoint: { address: entryPoint07Address, version: "0.7" } })
);

const txHash = await smartAccountClient.installModule({
  type: "validator",
  address: "0xOwnableValidatorAddress",
  context: encodePacked(["address"], [ownerAddress]),
});
```

### Security Considerations

**Storage collisions (ERC-7201):** Modules sharing storage slots with the Safe proxy can corrupt state. All ERC-7579 modules MUST use ERC-7201 namespaced storage to isolate their state from the Safe's core storage layout.

**Fallback handler hijacking:** A malicious fallback module intercepts ANY unrecognized function call to the Safe. An attacker who installs a rogue fallback can silently redirect calls meant for legitimate interfaces.

**`onInstall` reentrancy:** The module `onInstall` callback executes in Safe context during `execTransactionFromModule`. A malicious module can call back into the Safe during installation to add owners, change threshold, or drain funds before the installation transaction completes.

**Validator front-running:** An attacker observing `validateUserOp` calls on the public mempool can front-run to change validator state (e.g., rotate the approved signer) before the bundler's transaction lands.

Additional risks:
- Module installation requires owner threshold approval -- a compromised owner set can install malicious modules
- Malicious validators can approve arbitrary UserOps; malicious executors can drain the Safe
- A hook that reverts blocks ALL Safe transactions including module removal -- test hooks on a fork first
- Modules that revert in `onUninstall` become permanently irremovable

### When to Use ERC-7579 Modules

| Scenario | Approach |
|----------|----------|
| Simple multisig, no automation | Direct Safe (protocol-kit) |
| Session keys for dApp interactions | Safe + SmartSessions module |
| Automated recurring actions | Safe + Scheduled Orders executor |
| Passkey authentication | Safe + WebAuthn validator |
| Spending policy enforcement | Safe + hook modules |

> For the full module catalog, installation walkthrough, and production addresses, see `docs/erc-7579-modules.md`. For general account abstraction context (EntryPoint, bundlers, paymasters), see the `account-abstraction` skill.

## References

- [Safe SDK Documentation](https://docs.safe.global/sdk/overview)
- [Protocol Kit Reference](https://docs.safe.global/sdk/protocol-kit)
- [API Kit Reference](https://docs.safe.global/sdk/api-kit)
- [Safe Smart Account Source](https://github.com/safe-global/safe-smart-account)
- [Safe Contract Deployments](https://github.com/safe-global/safe-deployments)
- [Safe Transaction Service API Docs](https://safe-transaction-mainnet.safe.global/)
- [EIP-1271: Standard Signature Validation](https://eips.ethereum.org/EIPS/eip-1271)
- [Zodiac Modules Collection](https://github.com/gnosis/zodiac)
