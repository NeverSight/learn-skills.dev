---
name: eigenlayer
description: EigenLayer restaking protocol — stake ETH and LSTs to secure AVSs (Actively Validated Services), operator registration and delegation, reward claiming, and slashing conditions. Covers StrategyManager, DelegationManager, AVSDirectory, and the restaking lifecycle on Ethereum mainnet.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - eigenlayer
  - restaking
  - avs
  - staking
  - defi
  - operator
---

# EigenLayer

EigenLayer is a restaking protocol on Ethereum that lets stakers repurpose their staked ETH (native or via LSTs) to provide cryptoeconomic security to additional services called Actively Validated Services (AVSs). Operators run AVS software and register on-chain; stakers delegate their restaked assets to operators. If an operator misbehaves, both the operator and their delegators can be slashed. This creates a shared security marketplace where new protocols bootstrap validator sets without requiring their own token stake.

## What You Probably Got Wrong

- **EigenLayer is NOT a liquid staking protocol** -- it is a restaking protocol. You stake assets that are ALREADY staked (LSTs like stETH, rETH, cbETH) or native beacon chain ETH to provide security to AVSs. EigenLayer does not issue a liquid receipt token for your deposit.
- **Restaked assets are NOT locked permanently** -- there is a withdrawal escrow period (currently 7 days for the `minWithdrawalDelayBlocks` parameter) to allow slashing to be processed before funds are released. You queue a withdrawal, wait, then complete it.
- **Operators and Stakers are different roles** -- Operators register on-chain and run AVS node software. Stakers deposit assets and delegate to an operator. Stakers bear slashing risk proportional to their delegation if their chosen operator misbehaves.
- **Delegation is all-or-nothing per operator** -- you delegate ALL your restaked assets across ALL strategies to ONE operator. You cannot split delegation across multiple operators. To diversify, use separate addresses.
- **EigenLayer contracts use upgradeable proxies** -- always interact with proxy addresses, never implementation addresses. The implementation behind a proxy can be upgraded by the EigenLayer governance multisig.
- **Native restaking requires an EigenPod** -- each restaker deploys a unique EigenPod contract. Your Ethereum validator's withdrawal credentials must point to this EigenPod address. This is a one-time setup per address.
- **`queueWithdrawals()` starts the delay, `completeQueuedWithdrawals()` finalizes** -- these are two separate transactions. You cannot withdraw in a single step. The withdrawal root must exist and the delay must have elapsed.
- **Rewards are distributed via RewardsCoordinator** -- AVSs submit reward roots, and stakers/operators claim via Merkle proofs. Rewards do not arrive as direct token transfers to your address.
- **Slashing is real and live** -- since the SLASHING upgrade, AVS operators can be slashed for misbehavior via the AllocationManager. Delegated stakers bear proportional losses. Evaluate operator track records before delegating.
- **Strategy deposit caps exist** -- each strategy (stETH, rETH, cbETH, etc.) may have a maximum total deposit cap. When the cap is reached, new deposits revert. Check `getTVLLimits()` on the strategy before depositing.

## Quick Start

### Deposit stETH into EigenLayer (TypeScript)

```typescript
import {
  createPublicClient,
  createWalletClient,
  http,
  parseAbi,
  parseEther,
  type Address,
} from "viem";
import { mainnet } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const STRATEGY_MANAGER = "0x858646372CC42E1A627fcE94aa7A7033e7CF075A" as const;
const STETH_STRATEGY = "0x93c4b944D05dfe6df7645A86cd2206016c51564D" as const;
const STETH = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84" as const;

const strategyManagerAbi = parseAbi([
  "function depositIntoStrategy(address strategy, address token, uint256 amount) external returns (uint256 shares)",
  "function stakerStrategyShares(address staker, address strategy) external view returns (uint256)",
]);

const erc20Abi = parseAbi([
  "function approve(address spender, uint256 amount) external returns (bool)",
  "function allowance(address owner, address spender) external view returns (uint256)",
  "function balanceOf(address account) external view returns (uint256)",
]);

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

async function depositStethIntoEigenLayer(amount: bigint) {
  const allowance = await publicClient.readContract({
    address: STETH,
    abi: erc20Abi,
    functionName: "allowance",
    args: [account.address, STRATEGY_MANAGER],
  });

  if (allowance < amount) {
    const approveHash = await walletClient.writeContract({
      address: STETH,
      abi: erc20Abi,
      functionName: "approve",
      args: [STRATEGY_MANAGER, amount],
    });
    const approveReceipt = await publicClient.waitForTransactionReceipt({
      hash: approveHash,
    });
    if (approveReceipt.status !== "success") throw new Error("Approval reverted");
  }

  const { request } = await publicClient.simulateContract({
    address: STRATEGY_MANAGER,
    abi: strategyManagerAbi,
    functionName: "depositIntoStrategy",
    args: [STETH_STRATEGY, STETH, amount],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Deposit reverted");

  return hash;
}
```

## Core Architecture

EigenLayer's on-chain system consists of several coordinated contracts, all behind upgradeable proxies.

### Contract Roles

| Contract | Responsibility |
|----------|---------------|
| **StrategyManager** | Manages LST deposits and withdrawals into strategies |
| **DelegationManager** | Handles operator registration, staker delegation, and withdrawal queueing |
| **EigenPodManager** | Manages native ETH restaking via EigenPods |
| **AVSDirectory** | Tracks which operators are registered to which AVSs |
| **AllocationManager** | Handles operator allocations to AVSs and slashing (post-SLASHING upgrade) |
| **RewardsCoordinator** | Distributes rewards from AVSs to operators and stakers |
| **Slasher** | Legacy slashing contract (pre-SLASHING upgrade, now superseded by AllocationManager) |

### Interaction Flow

```
Staker deposits LST -> StrategyManager -> Strategy contract holds tokens
Staker delegates    -> DelegationManager -> Links staker to operator
Operator registers  -> DelegationManager -> Becomes available for delegation
Operator opts in    -> AVSDirectory -> Links operator to AVS
AVS slashes         -> AllocationManager -> Reduces operator's allocatable magnitude
Staker withdraws    -> DelegationManager -> Queue -> Wait -> Complete
AVS rewards         -> RewardsCoordinator -> Merkle root -> Staker/Operator claims
```

## LST Restaking

### Deposit LSTs into a Strategy

Each supported LST has a corresponding Strategy contract. The flow is: approve the StrategyManager to spend your LST, then call `depositIntoStrategy`.

```typescript
const STRATEGY_MANAGER = "0x858646372CC42E1A627fcE94aa7A7033e7CF075A" as const;

const STRATEGIES: Record<string, { strategy: Address; token: Address }> = {
  stETH: {
    strategy: "0x93c4b944D05dfe6df7645A86cd2206016c51564D",
    token: "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
  },
  rETH: {
    strategy: "0x1BeE69b7dFFfA4E2d53C2a2Df135C388AD25dCD2",
    token: "0xae78736Cd615f374D3085123A210448E74Fc6393",
  },
  cbETH: {
    strategy: "0x54945180dB7943c0ed0FEE7EdaB2Bd24620256bc",
    token: "0xBe9895146f7AF43049ca1c1AE358B0541Ea49BBa",
  },
  wBETH: {
    strategy: "0x7CA911E83dabf90C90dD3De5411a10F1A6112184",
    token: "0xa2E3356610840701BDf5611a53974510Ae27E2e1",
  },
  sfrxETH: {
    strategy: "0x8CA7A5d6f3acd3A7A8bC468a8CD0FB14B6BD28b6",
    token: "0xac3E018457B222d93114458476f3E3416Abbe38F",
  },
};

async function depositLst(
  lstName: string,
  amount: bigint
): Promise<`0x${string}`> {
  const config = STRATEGIES[lstName];
  if (!config) throw new Error(`Unknown LST: ${lstName}`);

  const allowance = await publicClient.readContract({
    address: config.token,
    abi: erc20Abi,
    functionName: "allowance",
    args: [account.address, STRATEGY_MANAGER],
  });

  if (allowance < amount) {
    const approveHash = await walletClient.writeContract({
      address: config.token,
      abi: erc20Abi,
      functionName: "approve",
      args: [STRATEGY_MANAGER, amount],
    });
    const receipt = await publicClient.waitForTransactionReceipt({ hash: approveHash });
    if (receipt.status !== "success") throw new Error("Approval reverted");
  }

  const { request } = await publicClient.simulateContract({
    address: STRATEGY_MANAGER,
    abi: strategyManagerAbi,
    functionName: "depositIntoStrategy",
    args: [config.strategy, config.token, amount],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Deposit reverted");

  return hash;
}
```

### Check Restaked Balance

```typescript
async function getRestakedShares(
  staker: Address,
  strategy: Address
): Promise<bigint> {
  return publicClient.readContract({
    address: STRATEGY_MANAGER,
    abi: strategyManagerAbi,
    functionName: "stakerStrategyShares",
    args: [staker, strategy],
  });
}

async function getRestakedBalance(
  staker: Address,
  lstName: string
): Promise<{ shares: bigint; underlyingTokens: bigint }> {
  const config = STRATEGIES[lstName];
  if (!config) throw new Error(`Unknown LST: ${lstName}`);

  const strategyAbi = parseAbi([
    "function sharesToUnderlyingView(uint256 amountShares) external view returns (uint256)",
    "function underlyingToSharesView(uint256 amountUnderlying) external view returns (uint256)",
  ]);

  const shares = await getRestakedShares(staker, config.strategy);

  const underlyingTokens = await publicClient.readContract({
    address: config.strategy,
    abi: strategyAbi,
    functionName: "sharesToUnderlyingView",
    args: [shares],
  });

  return { shares, underlyingTokens };
}
```

### Deposit LSTs in Solidity

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IStrategyManager {
    function depositIntoStrategy(
        address strategy, IERC20 token, uint256 amount
    ) external returns (uint256 shares);
}

contract EigenLayerDepositor {
    IStrategyManager public constant STRATEGY_MANAGER =
        IStrategyManager(0x858646372CC42E1A627fcE94aa7A7033e7CF075A);

    event Deposited(address indexed staker, address indexed strategy, uint256 shares);

    /// @notice Deposit an LST into its EigenLayer strategy
    /// @dev Caller must approve this contract for the token first
    function deposit(
        address strategy, address token, uint256 amount
    ) external returns (uint256 shares) {
        if (amount == 0) revert ZeroAmount();

        IERC20(token).transferFrom(msg.sender, address(this), amount);
        IERC20(token).approve(address(STRATEGY_MANAGER), amount);

        shares = STRATEGY_MANAGER.depositIntoStrategy(strategy, IERC20(token), amount);
        emit Deposited(msg.sender, strategy, shares);
    }

    error ZeroAmount();
}
```

## Native Restaking

Native restaking involves pointing an Ethereum validator's withdrawal credentials to an EigenPod. This requires deploying an EigenPod and verifying validator credentials on-chain via beacon chain state proofs.

### Create an EigenPod

```typescript
const EIGEN_POD_MANAGER = "0x91E677b07F7AF907ec9a428aafA9fc14a0d3A338" as const;

const eigenPodManagerAbi = parseAbi([
  "function createPod() external returns (address)",
  "function getPod(address podOwner) external view returns (address)",
  "function hasPod(address podOwner) external view returns (bool)",
]);

async function createEigenPod(): Promise<Address> {
  const hasPod = await publicClient.readContract({
    address: EIGEN_POD_MANAGER,
    abi: eigenPodManagerAbi,
    functionName: "hasPod",
    args: [account.address],
  });

  if (hasPod) {
    const existingPod = await publicClient.readContract({
      address: EIGEN_POD_MANAGER,
      abi: eigenPodManagerAbi,
      functionName: "getPod",
      args: [account.address],
    });
    return existingPod;
  }

  const { request } = await publicClient.simulateContract({
    address: EIGEN_POD_MANAGER,
    abi: eigenPodManagerAbi,
    functionName: "createPod",
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("EigenPod creation reverted");

  const podAddress = await publicClient.readContract({
    address: EIGEN_POD_MANAGER,
    abi: eigenPodManagerAbi,
    functionName: "getPod",
    args: [account.address],
  });

  return podAddress;
}
```

### Native Restaking Flow

1. Call `EigenPodManager.createPod()` to deploy your EigenPod
2. Set your Ethereum validator's withdrawal credentials to your EigenPod address (this happens at validator creation time or via a BLS-to-execution-layer withdrawal credential change)
3. Verify your validator credentials on-chain by submitting a beacon state proof via `EigenPod.verifyWithdrawalCredentials()`
4. Your restaked ETH is now tracked by EigenLayer and can be delegated to an operator

> **Important:** The withdrawal credential verification requires beacon chain state proofs. Use the EigenLayer CLI or the `eigenpod-proofs-generation` tool from the Layr-Labs GitHub to generate these proofs. This is not a simple contract call -- it requires off-chain proof generation.

## Delegation

### Delegate to an Operator

Delegation assigns all your restaked assets (across all strategies) to a single operator. The operator must be registered in the DelegationManager.

```typescript
const DELEGATION_MANAGER = "0x39053D51B77DC0d36036Fc1fCc8Cb819df8Ef37A" as const;

const delegationManagerAbi = parseAbi([
  "function delegateTo(address operator, (bytes signature, uint256 expiry) approverSignatureAndExpiry, bytes32 approverSalt) external",
  "function undelegate(address staker) external returns (bytes32[] withdrawalRoots)",
  "function delegatedTo(address staker) external view returns (address)",
  "function isDelegated(address staker) external view returns (bool)",
  "function isOperator(address operator) external view returns (bool)",
]);

async function delegateToOperator(operatorAddress: Address): Promise<`0x${string}`> {
  const isOperator = await publicClient.readContract({
    address: DELEGATION_MANAGER,
    abi: delegationManagerAbi,
    functionName: "isOperator",
    args: [operatorAddress],
  });
  if (!isOperator) throw new Error("Address is not a registered operator");

  const isDelegated = await publicClient.readContract({
    address: DELEGATION_MANAGER,
    abi: delegationManagerAbi,
    functionName: "isDelegated",
    args: [account.address],
  });
  if (isDelegated) throw new Error("Already delegated -- undelegate first");

  // Empty signature for operators that don't require approval
  const emptySignature: `0x${string}` = "0x";
  const noExpiry = 0n;
  const emptySalt = "0x0000000000000000000000000000000000000000000000000000000000000000" as `0x${string}`;

  const { request } = await publicClient.simulateContract({
    address: DELEGATION_MANAGER,
    abi: delegationManagerAbi,
    functionName: "delegateTo",
    args: [
      operatorAddress,
      { signature: emptySignature, expiry: noExpiry },
      emptySalt,
    ],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Delegation reverted");

  return hash;
}
```

### Check Delegation Status

```typescript
async function getDelegationStatus(staker: Address): Promise<{
  isDelegated: boolean;
  operator: Address;
}> {
  const [isDelegated, operator] = await Promise.all([
    publicClient.readContract({
      address: DELEGATION_MANAGER,
      abi: delegationManagerAbi,
      functionName: "isDelegated",
      args: [staker],
    }),
    publicClient.readContract({
      address: DELEGATION_MANAGER,
      abi: delegationManagerAbi,
      functionName: "delegatedTo",
      args: [staker],
    }),
  ]);

  return { isDelegated, operator };
}
```

### Undelegate

Undelegating automatically queues withdrawals for all your restaked assets. You must complete the withdrawals after the escrow period.

```typescript
async function undelegate(): Promise<`0x${string}`> {
  const { request } = await publicClient.simulateContract({
    address: DELEGATION_MANAGER,
    abi: delegationManagerAbi,
    functionName: "undelegate",
    args: [account.address],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Undelegate reverted");

  return hash;
}
```

## Operators

### Register as an Operator

An operator is an address that has registered with the DelegationManager. Operators can then opt into AVSs and accept delegations from stakers.

```typescript
const operatorRegistrationAbi = parseAbi([
  "function registerAsOperator((address earningsReceiver, address delegationApprover, uint32 stakerOptOutWindowBlocks) registeringOperatorDetails, string metadataURI) external",
  "function modifyOperatorDetails((address earningsReceiver, address delegationApprover, uint32 stakerOptOutWindowBlocks) newOperatorDetails) external",
  "function updateOperatorMetadataURI(string metadataURI) external",
  "function operatorDetails(address operator) external view returns ((address earningsReceiver, address delegationApprover, uint32 stakerOptOutWindowBlocks))",
]);

async function registerAsOperator(params: {
  earningsReceiver: Address;
  metadataURI: string;
  delegationApprover?: Address;
  stakerOptOutWindowBlocks?: number;
}): Promise<`0x${string}`> {
  const zeroAddress = "0x0000000000000000000000000000000000000000" as Address;

  const { request } = await publicClient.simulateContract({
    address: DELEGATION_MANAGER,
    abi: operatorRegistrationAbi,
    functionName: "registerAsOperator",
    args: [
      {
        earningsReceiver: params.earningsReceiver,
        delegationApprover: params.delegationApprover ?? zeroAddress,
        // Minimum blocks a staker must wait after opting out before withdrawal
        stakerOptOutWindowBlocks: params.stakerOptOutWindowBlocks ?? 0,
      },
      params.metadataURI,
    ],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Operator registration reverted");

  return hash;
}
```

### Operator Metadata

The `metadataURI` should point to a JSON file following the EigenLayer operator metadata schema:

```json
{
  "name": "My Operator",
  "website": "https://myoperator.xyz",
  "description": "Professional EigenLayer operator",
  "logo": "https://myoperator.xyz/logo.png",
  "twitter": "https://twitter.com/myoperator"
}
```

Host this JSON at a publicly accessible URL (IPFS, HTTPS) and pass it as the `metadataURI` during registration.

## AVS Integration

### AVSDirectory: Operator Registration to AVS

AVSs register operators through the AVSDirectory. The operator must sign a message authorizing their registration to the specific AVS.

```typescript
const AVS_DIRECTORY = "0x135DDa560e946695d6f155dACaFC6f1F25C1F5AF" as const;

const avsDirectoryAbi = parseAbi([
  "function registerOperatorToAVS(address operator, (bytes signature, bytes32 salt, uint256 expiry) operatorSignature) external",
  "function deregisterOperatorFromAVS(address operator) external",
  "function calculateOperatorAVSRegistrationDigestHash(address operator, address avs, bytes32 salt, uint256 expiry) external view returns (bytes32)",
  "function operatorSaltIsSpent(address operator, bytes32 salt) external view returns (bool)",
]);

async function generateAvsRegistrationSignature(
  operatorAddress: Address,
  avsAddress: Address,
  salt: `0x${string}`,
  expiry: bigint
): Promise<`0x${string}`> {
  const digestHash = await publicClient.readContract({
    address: AVS_DIRECTORY,
    abi: avsDirectoryAbi,
    functionName: "calculateOperatorAVSRegistrationDigestHash",
    args: [operatorAddress, avsAddress, salt, expiry],
  });

  const signature = await walletClient.signMessage({
    message: { raw: digestHash },
  });

  return signature;
}
```

### What AVS Builders Need to Know

1. **ServiceManager contract** -- Your AVS needs a ServiceManager that calls `AVSDirectory.registerOperatorToAVS()`. This is the entry point for operators joining your AVS.
2. **Operator set management** -- Track your active operator set. Validate operator registration status before assigning tasks.
3. **Slashing conditions** -- Define clear, objectively verifiable slashing conditions. Submit slashing requests to the AllocationManager when violations occur.
4. **Reward distribution** -- Submit reward roots to the RewardsCoordinator. Rewards are distributed via Merkle proofs to operators and stakers.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IAVSDirectory {
    struct SignatureWithSaltAndExpiry {
        bytes signature;
        bytes32 salt;
        uint256 expiry;
    }

    function registerOperatorToAVS(
        address operator,
        SignatureWithSaltAndExpiry memory operatorSignature
    ) external;

    function deregisterOperatorFromAVS(address operator) external;
}

/// @notice Minimal AVS ServiceManager that registers/deregisters operators
contract MinimalServiceManager {
    IAVSDirectory public constant AVS_DIRECTORY =
        IAVSDirectory(0x135DDa560e946695d6f155dACaFC6f1F25C1F5AF);

    address public owner;
    mapping(address => bool) public registeredOperators;

    event OperatorRegistered(address indexed operator);
    event OperatorDeregistered(address indexed operator);

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /// @notice Register an operator to this AVS
    /// @param operator The operator address to register
    /// @param operatorSignature The operator's EIP-712 signature authorizing registration
    function registerOperator(
        address operator,
        IAVSDirectory.SignatureWithSaltAndExpiry memory operatorSignature
    ) external onlyOwner {
        if (registeredOperators[operator]) revert AlreadyRegistered();

        AVS_DIRECTORY.registerOperatorToAVS(operator, operatorSignature);
        registeredOperators[operator] = true;

        emit OperatorRegistered(operator);
    }

    /// @notice Deregister an operator from this AVS
    function deregisterOperator(address operator) external onlyOwner {
        if (!registeredOperators[operator]) revert NotRegistered();

        AVS_DIRECTORY.deregisterOperatorFromAVS(operator);
        registeredOperators[operator] = false;

        emit OperatorDeregistered(operator);
    }

    error NotOwner();
    error AlreadyRegistered();
    error NotRegistered();
}
```

## Withdrawals

### Queue Withdrawals

Withdrawals go through DelegationManager. You specify which strategies and how many shares to withdraw. The withdrawal enters an escrow period before it can be completed.

```typescript
const withdrawalAbi = parseAbi([
  "function queueWithdrawals((address[] strategies, uint256[] shares, address withdrawer)[] queuedWithdrawalParams) external returns (bytes32[] withdrawalRoots)",
  "function completeQueuedWithdrawals((address staker, address delegatedTo, address withdrawer, uint256 nonce, uint32 startBlock, address[] strategies, uint256[] shares)[] withdrawals, address[][] tokens, uint256[] middlewareTimesIndexes, bool[] receiveAsTokens) external",
  "function calculateWithdrawalRoot((address staker, address delegatedTo, address withdrawer, uint256 nonce, uint32 startBlock, address[] strategies, uint256[] shares) withdrawal) external pure returns (bytes32)",
  "function minWithdrawalDelayBlocks() external view returns (uint256)",
  "function cumulativeWithdrawalsQueued(address staker) external view returns (uint256)",
]);

async function queueWithdrawal(
  strategies: Address[],
  shares: bigint[]
): Promise<{ hash: `0x${string}`; withdrawalRoots: readonly `0x${string}`[] }> {
  if (strategies.length !== shares.length) {
    throw new Error("Strategies and shares arrays must have equal length");
  }
  if (strategies.length === 0) {
    throw new Error("Must withdraw from at least one strategy");
  }

  const { request, result } = await publicClient.simulateContract({
    address: DELEGATION_MANAGER,
    abi: withdrawalAbi,
    functionName: "queueWithdrawals",
    args: [
      [
        {
          strategies,
          shares,
          withdrawer: account.address,
        },
      ],
    ],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Queue withdrawal reverted");

  return { hash, withdrawalRoots: result };
}
```

### Complete Queued Withdrawals

After the escrow period (check `minWithdrawalDelayBlocks`), complete the withdrawal. Set `receiveAsTokens` to `true` to get underlying tokens back, or `false` to re-deposit as shares.

```typescript
interface QueuedWithdrawal {
  staker: Address;
  delegatedTo: Address;
  withdrawer: Address;
  nonce: bigint;
  startBlock: number;
  strategies: Address[];
  shares: bigint[];
}

async function completeWithdrawal(
  withdrawal: QueuedWithdrawal,
  tokens: Address[],
  receiveAsTokens: boolean
): Promise<`0x${string}`> {
  const currentBlock = await publicClient.getBlockNumber();
  const minDelay = await publicClient.readContract({
    address: DELEGATION_MANAGER,
    abi: withdrawalAbi,
    functionName: "minWithdrawalDelayBlocks",
  });

  const blocksElapsed = currentBlock - BigInt(withdrawal.startBlock);
  if (blocksElapsed < minDelay) {
    throw new Error(
      `Withdrawal not ready. ${minDelay - blocksElapsed} blocks remaining.`
    );
  }

  const { request } = await publicClient.simulateContract({
    address: DELEGATION_MANAGER,
    abi: withdrawalAbi,
    functionName: "completeQueuedWithdrawals",
    args: [
      [withdrawal],
      [tokens],
      [0n],
      [receiveAsTokens],
    ],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Complete withdrawal reverted");

  return hash;
}
```

## Rewards & Slashing

### Claiming Rewards

Rewards are distributed by AVSs through the RewardsCoordinator. AVSs submit Merkle roots, and stakers/operators claim by providing Merkle proofs.

```typescript
const REWARDS_COORDINATOR = "0x7750d328b314EfFa365A0402CcfD489B80B0adda" as const;

const rewardsCoordinatorAbi = parseAbi([
  "function processClaim((uint32 rootIndex, uint32 earnerIndex, bytes earnerTreeProof, (address earner, bytes32 earnerTokenRoot) earnerLeaf, uint32[] tokenIndices, bytes[] tokenTreeProofs, (address token, uint256 cumulativeEarnings)[] tokenLeaves) claim, address recipient) external",
  "function cumulativeClaimed(address earner, address token) external view returns (uint256)",
]);

async function checkClaimedRewards(
  earner: Address,
  token: Address
): Promise<bigint> {
  return publicClient.readContract({
    address: REWARDS_COORDINATOR,
    abi: rewardsCoordinatorAbi,
    functionName: "cumulativeClaimed",
    args: [earner, token],
  });
}
```

> **Note:** Generating the Merkle proofs for reward claims requires off-chain computation. EigenLayer provides the reward claim data through their API and the EigenLayer app. You do not manually construct these proofs -- use the EigenLayer webapp or SDK to fetch the claim data.

### Slashing

Since the SLASHING upgrade, AVSs can slash operators through the AllocationManager. Operators allocate a portion of their restaked security (magnitude) to each AVS. Slashing reduces this allocated magnitude, which proportionally affects delegated stakers.

```typescript
const ALLOCATION_MANAGER = "0xAbC000003ca6769b5bc218E94e0296b39a19A8c3" as const;

const allocationManagerAbi = parseAbi([
  "function getAllocatedSets(address operator) external view returns ((address avs, uint32 operatorSetId)[])",
  "function getAllocation(address operator, address strategy, (address avs, uint32 operatorSetId) operatorSet) external view returns ((uint64 currentMagnitude, int128 pendingDiff, uint32 effectBlock))",
  "function getMaxMagnitudes(address operator, address[] strategies) external view returns (uint64[])",
]);

async function getOperatorAllocations(operator: Address) {
  const allocatedSets = await publicClient.readContract({
    address: ALLOCATION_MANAGER,
    abi: allocationManagerAbi,
    functionName: "getAllocatedSets",
    args: [operator],
  });

  return allocatedSets;
}
```

### Slashing Risk Assessment

Before delegating to an operator, assess their slashing risk:

1. **Check how many AVSs the operator is registered to** -- more AVSs means more potential slashing vectors
2. **Review the operator's allocation magnitudes** -- higher allocations to risky AVSs increase exposure
3. **Check operator history** -- has the operator been slashed before?
4. **Evaluate AVS slashing conditions** -- each AVS defines its own misbehavior criteria

## Contract Addresses

> **Last verified:** February 2026. All addresses are proxy contracts on Ethereum mainnet.

| Contract | Address |
|----------|---------|
| StrategyManager (proxy) | `0x858646372CC42E1A627fcE94aa7A7033e7CF075A` |
| DelegationManager (proxy) | `0x39053D51B77DC0d36036Fc1fCc8Cb819df8Ef37A` |
| EigenPodManager (proxy) | `0x91E677b07F7AF907ec9a428aafA9fc14a0d3A338` |
| AVSDirectory (proxy) | `0x135DDa560e946695d6f155dACaFC6f1F25C1F5AF` |
| RewardsCoordinator (proxy) | `0x7750d328b314EfFa365A0402CcfD489B80B0adda` |
| AllocationManager (proxy) | `0xAbC000003ca6769b5bc218E94e0296b39a19A8c3` |
| Slasher (legacy, proxy) | `0xD92145c07f8Ed1D392c1B88017934E301CC1c3Cd` |
| EIGEN token | `0xec53bF9167f50cDEB3Ae105f56099aaaB9061F83` |
| bEIGEN (backing EIGEN) | `0x83E9115d334D248Ce39a6f36144aEaB5b3456e75` |

### Strategy Contracts (LST Strategies)

| LST | Strategy Address | Token Address |
|-----|-----------------|---------------|
| stETH | `0x93c4b944D05dfe6df7645A86cd2206016c51564D` | `0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84` |
| rETH | `0x1BeE69b7dFFfA4E2d53C2a2Df135C388AD25dCD2` | `0xae78736Cd615f374D3085123A210448E74Fc6393` |
| cbETH | `0x54945180dB7943c0ed0FEE7EdaB2Bd24620256bc` | `0xBe9895146f7AF43049ca1c1AE358B0541Ea49BBa` |
| wBETH | `0x7CA911E83dabf90C90dD3De5411a10F1A6112184` | `0xa2E3356610840701BDf5611a53974510Ae27E2e1` |
| sfrxETH | `0x8CA7A5d6f3acd3A7A8bC468a8CD0FB14B6BD28b6` | `0xac3E018457B222d93114458476f3E3416Abbe38F` |
| ETHx | `0x9d7eD45EE2E8FC5482fa2428f15C971e6369011d` | `0xA35b1B31Ce002FBF2058D22F30f95D405200A15b` |
| osETH | `0x57ba429517c3473B6d34CA9aCd56c0e735b94c02` | `0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38` |
| swETH | `0x0Fe4F44beE93503346A3Ac9EE5A26b130a5796d6` | `0xf951E335afb289353dc249e82926178EaC7DEd78` |
| mETH | `0x298aFB19A105D59E74658C4C334Ff360BadE6dd2` | `0xd5F7838F5C461fefF7FE49ea5ebaF7728bB0ADfa` |

## References

- [EigenLayer Docs](https://docs.eigenlayer.xyz)
- [EigenLayer Contracts GitHub](https://github.com/Layr-Labs/eigenlayer-contracts)
- [EigenLayer Middleware GitHub](https://github.com/Layr-Labs/eigenlayer-middleware)
- [EigenLayer App](https://app.eigenlayer.xyz)
- [ELIP-002: Slashing](https://github.com/eigenfoundation/ELIPs/blob/main/ELIPs/ELIP-002.md)
- [EigenLayer Operator Guide](https://docs.eigenlayer.xyz/eigenlayer/operator-guides/operator-introduction)
- [AVS Developer Guide](https://docs.eigenlayer.xyz/eigenlayer/avs-guides/avs-developer-guide)
- [EigenPod Proofs Generation](https://github.com/Layr-Labs/eigenpod-proofs-generation)
