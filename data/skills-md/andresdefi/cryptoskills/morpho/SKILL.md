---
name: morpho
description: Morpho Blue lending protocol — permissionless market creation, MetaMorpho vaults for curated lending, isolated lending markets with custom parameters (LLTV, oracle, IRM), supply, borrow, liquidation, and market management. Covers Morpho Blue singleton contract, MetaMorpho vault interface, and market ID derivation on Ethereum mainnet.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - morpho
  - lending
  - borrowing
  - vaults
  - defi
  - permissionless
---

# Morpho Blue

Morpho Blue is a permissionless, immutable lending primitive on Ethereum. Unlike Aave or Compound, Morpho Blue has no governance, no upgradeability, and no admin keys. Anyone can create an isolated lending market by specifying a loan token, collateral token, oracle, interest rate model, and liquidation LTV. A single singleton contract holds all markets. MetaMorpho vaults sit on top, providing curated, multi-market lending strategies with ERC-4626 interfaces.

## What You Probably Got Wrong

> LLMs confuse Morpho Optimizer (V1) with Morpho Blue. They also hallucinate Aave-style pooled risk. These corrections are non-negotiable.

- **This is NOT Morpho Optimizer (V1)** -- Morpho Optimizer was a peer-to-peer matching layer on top of Aave/Compound. Morpho Blue is a standalone, independent lending protocol with its own singleton contract. Different addresses, different interfaces, different architecture. If you see `MorphoAaveV2` or `MorphoCompound`, you are writing V1 code. Stop.
- **Market ID = `keccak256(abi.encode(loanToken, collateralToken, oracle, irm, lltv))`** -- The market is identified by a bytes32 hash of its five parameters. Not a numeric index. Not an address. If you are passing a uint256 market index, you are wrong.
- **One singleton contract for ALL markets** -- Every market lives inside the same `Morpho` contract at `0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb`. There are no per-market contracts to deploy or interact with.
- **LLTV is NOT the same as LTV** -- LLTV (Liquidation Loan-To-Value) is the threshold at which a position becomes liquidatable. It is NOT the maximum amount you can borrow. You can borrow up to LLTV, but doing so means instant liquidation risk. Always borrow well below LLTV.
- **MetaMorpho vaults are a separate layer** -- Morpho Blue markets are the primitive. MetaMorpho vaults are ERC-4626 wrappers that allocate deposits across multiple Morpho Blue markets. Supplying to a vault is NOT the same as supplying directly to a market. Different contracts, different interfaces.
- **Shares, not balances** -- Morpho Blue tracks positions using shares internally (like ERC-4626). `supply()` and `borrow()` accept either an `assets` amount OR a `shares` amount, but not both simultaneously. One must be zero. The conversion between shares and assets changes as interest accrues.
- **Oracle price uses 36-decimal scaling** -- Morpho Blue oracles return price with `36 + loanTokenDecimals - collateralTokenDecimals` decimals of precision. This is NOT 18 decimals. Getting this wrong causes catastrophic mispricing. A WETH/USDC oracle returns price with `36 + 6 - 18 = 24` decimals.
- **Markets are immutable once created** -- After `createMarket()`, the parameters (oracle, IRM, LLTV) can never be changed. There is no governance. If the oracle breaks, the market is permanently affected.
- **`liquidate()` uses `seizedAssets` OR `repaidShares`, not both** -- Pass one and set the other to zero. The contract calculates the counterpart. Passing both nonzero reverts.
- **Authorization is per-address, not per-market** -- `setAuthorization(address, bool)` grants or revokes permission for an address to act on behalf of msg.sender across ALL markets, not a specific one.

## Quick Start

### Installation

```bash
npm install viem
```

Morpho Blue has no SDK package to install. Interaction is via the singleton contract ABI directly.

### Minimal ABI Fragments

```typescript
const morphoAbi = [
  {
    name: "supply",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "assets", type: "uint256" },
      { name: "shares", type: "uint256" },
      { name: "onBehalf", type: "address" },
      { name: "data", type: "bytes" },
    ],
    outputs: [
      { name: "assetsSupplied", type: "uint256" },
      { name: "sharesSupplied", type: "uint256" },
    ],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "assets", type: "uint256" },
      { name: "shares", type: "uint256" },
      { name: "onBehalf", type: "address" },
      { name: "receiver", type: "address" },
    ],
    outputs: [
      { name: "assetsWithdrawn", type: "uint256" },
      { name: "sharesWithdrawn", type: "uint256" },
    ],
  },
  {
    name: "borrow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "assets", type: "uint256" },
      { name: "shares", type: "uint256" },
      { name: "onBehalf", type: "address" },
      { name: "receiver", type: "address" },
    ],
    outputs: [
      { name: "assetsBorrowed", type: "uint256" },
      { name: "sharesBorrowed", type: "uint256" },
    ],
  },
  {
    name: "repay",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "assets", type: "uint256" },
      { name: "shares", type: "uint256" },
      { name: "onBehalf", type: "address" },
      { name: "data", type: "bytes" },
    ],
    outputs: [
      { name: "assetsRepaid", type: "uint256" },
      { name: "sharesRepaid", type: "uint256" },
    ],
  },
  {
    name: "supplyCollateral",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "assets", type: "uint256" },
      { name: "onBehalf", type: "address" },
      { name: "data", type: "bytes" },
    ],
    outputs: [],
  },
  {
    name: "withdrawCollateral",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "assets", type: "uint256" },
      { name: "onBehalf", type: "address" },
      { name: "receiver", type: "address" },
    ],
    outputs: [],
  },
  {
    name: "liquidate",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
      { name: "borrower", type: "address" },
      { name: "seizedAssets", type: "uint256" },
      { name: "repaidShares", type: "uint256" },
      { name: "data", type: "bytes" },
    ],
    outputs: [
      { name: "seizedAssets", type: "uint256" },
      { name: "repaidAssets", type: "uint256" },
    ],
  },
  {
    name: "createMarket",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
    ],
    outputs: [],
  },
  {
    name: "setAuthorization",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "authorized", type: "address" },
      { name: "newIsAuthorized", type: "bool" },
    ],
    outputs: [],
  },
  {
    name: "accrueInterest",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "marketParams",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
    ],
    outputs: [],
  },
  {
    name: "market",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "id", type: "bytes32" }],
    outputs: [
      { name: "totalSupplyAssets", type: "uint128" },
      { name: "totalSupplyShares", type: "uint128" },
      { name: "totalBorrowAssets", type: "uint128" },
      { name: "totalBorrowShares", type: "uint128" },
      { name: "lastUpdate", type: "uint128" },
      { name: "fee", type: "uint128" },
    ],
  },
  {
    name: "position",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "id", type: "bytes32" },
      { name: "user", type: "address" },
    ],
    outputs: [
      { name: "supplyShares", type: "uint256" },
      { name: "borrowShares", type: "uint128" },
      { name: "collateral", type: "uint128" },
    ],
  },
  {
    name: "idToMarketParams",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "id", type: "bytes32" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "loanToken", type: "address" },
          { name: "collateralToken", type: "address" },
          { name: "oracle", type: "address" },
          { name: "irm", type: "address" },
          { name: "lltv", type: "uint256" },
        ],
      },
    ],
  },
] as const;

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
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;
```

### Supply USDC to a Morpho Blue Market (TypeScript)

```typescript
import { createPublicClient, createWalletClient, http, parseUnits, encodeAbiParameters, keccak256 } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const MORPHO = "0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb" as const;
const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as const;

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

// USDC/wstETH market params (example)
const marketParams = {
  loanToken: USDC,
  collateralToken: "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0" as `0x${string}`, // wstETH
  oracle: "0x48F7E36EB6B826B2dF4B2E630B62Cd25e89E40e2" as `0x${string}`,
  irm: "0x870aC11D48B15DB9a138Cf899d20F13F79Ba00BC" as `0x${string}`, // AdaptiveCurveIRM
  lltv: 860000000000000000n, // 86%
} as const;

const amount = parseUnits("1000", 6); // 1000 USDC

// Approve Morpho to spend USDC
const approveHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [MORPHO, amount],
});
await publicClient.waitForTransactionReceipt({ hash: approveHash });

// Supply USDC -- pass assets amount, set shares to 0
const supplyHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "supply",
  args: [marketParams, amount, 0n, account.address, "0x"],
});
const receipt = await publicClient.waitForTransactionReceipt({ hash: supplyHash });

if (receipt.status !== "success") {
  throw new Error("Supply transaction reverted");
}
```

## Core Architecture

### Singleton Contract

All Morpho Blue markets live inside one immutable contract:

```
0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb
```

There are no proxy patterns, no admin functions, no upgradeability. The contract is deployed and final.

### MarketParams

Every market is defined by exactly five parameters:

```typescript
type MarketParams = {
  loanToken: `0x${string}`;        // Token being lent and borrowed
  collateralToken: `0x${string}`;  // Token used as collateral
  oracle: `0x${string}`;           // Oracle contract for price feed
  irm: `0x${string}`;             // Interest Rate Model contract
  lltv: bigint;                    // Liquidation LTV (18 decimals, e.g. 0.86e18 = 86%)
};
```

### Market ID Derivation

The market ID is a `bytes32` computed deterministically from MarketParams:

```typescript
import { encodeAbiParameters, keccak256 } from "viem";

function computeMarketId(params: MarketParams): `0x${string}` {
  const encoded = encodeAbiParameters(
    [
      { type: "address" }, // loanToken
      { type: "address" }, // collateralToken
      { type: "address" }, // oracle
      { type: "address" }, // irm
      { type: "uint256" }, // lltv
    ],
    [
      params.loanToken,
      params.collateralToken,
      params.oracle,
      params.irm,
      params.lltv,
    ]
  );
  return keccak256(encoded);
}
```

Equivalent Solidity:

```solidity
bytes32 marketId = keccak256(abi.encode(
    marketParams.loanToken,
    marketParams.collateralToken,
    marketParams.oracle,
    marketParams.irm,
    marketParams.lltv
));
```

### Authorization

Morpho uses a simple authorization model. You can authorize another address to act on your behalf across all markets:

```typescript
// Authorize the Morpho Bundler to manage positions on your behalf
const authHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "setAuthorization",
  args: ["0x4095F064B8d3c3548A3bebfd0Bbfd04750E30077" as `0x${string}`, true],
});
await publicClient.waitForTransactionReceipt({ hash: authHash });
```

## Market Creation

Anyone can create a market. There are no fees, no governance approvals, and no caps on market creation.

### Prerequisites

1. **Oracle** must implement `IOracle` (single function: `price() returns (uint256)`)
2. **IRM** must be enabled by Morpho governance via `enableIrm(address)`
3. **LLTV** must be enabled by Morpho governance via `enableLltv(uint256)`

### Create a New Market

```typescript
// Oracle must be deployed and returning valid prices
// IRM and LLTV must be governance-approved
const newMarketParams = {
  loanToken: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as `0x${string}`,  // USDC
  collateralToken: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as `0x${string}`, // WETH
  oracle: "0x..." as `0x${string}`, // Your deployed oracle
  irm: "0x870aC11D48B15DB9a138Cf899d20F13F79Ba00BC" as `0x${string}`, // AdaptiveCurveIRM
  lltv: 860000000000000000n, // 86% -- must be governance-enabled
} as const;

const createHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "createMarket",
  args: [newMarketParams],
});
const createReceipt = await publicClient.waitForTransactionReceipt({ hash: createHash });

if (createReceipt.status !== "success") {
  throw new Error("createMarket reverted");
}

// Compute the market ID for future reference
const marketId = computeMarketId(newMarketParams);
console.log(`Market created with ID: ${marketId}`);
```

### Governance-Enabled LLTVs

Morpho governance has enabled a specific set of LLTVs. Using a non-enabled LLTV will revert `createMarket()`.

| LLTV | Percentage | Typical Use Case |
|------|-----------|-----------------|
| `0` | 0% | No collateral (unsecured -- only for special cases) |
| `385000000000000000n` | 38.5% | Volatile pairs |
| `625000000000000000n` | 62.5% | Moderate correlation |
| `770000000000000000n` | 77% | Correlated assets |
| `860000000000000000n` | 86% | Highly correlated (ETH/wstETH) |
| `915000000000000000n` | 91.5% | Stablecoin pairs |
| `945000000000000000n` | 94.5% | Tight peg (USDC/USDT) |
| `965000000000000000n` | 96.5% | Near-identical assets |

### Create Market (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IMorpho, MarketParams} from "@morpho-org/morpho-blue/src/interfaces/IMorpho.sol";

contract MarketCreator {
    IMorpho public immutable morpho;

    constructor(address _morpho) {
        morpho = IMorpho(_morpho);
    }

    /// @notice Create a new Morpho Blue market
    /// @dev IRM and LLTV must be governance-enabled or this reverts
    function createNewMarket(MarketParams calldata params) external {
        morpho.createMarket(params);
    }
}
```

## Supply and Withdraw

### Supply Loan Token (Lender Side)

Supplying means depositing loan tokens into a market to earn interest from borrowers.

```typescript
// Supply 5000 USDC to earn yield
const supplyAmount = parseUnits("5000", 6);

const approveHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [MORPHO, supplyAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveHash });

// assets = amount to supply, shares = 0 (let contract calculate shares)
const { result } = await publicClient.simulateContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "supply",
  args: [marketParams, supplyAmount, 0n, account.address, "0x"],
  account: account.address,
});

const [assetsSupplied, sharesReceived] = result;

const supplyHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "supply",
  args: [marketParams, supplyAmount, 0n, account.address, "0x"],
});
const supplyReceipt = await publicClient.waitForTransactionReceipt({ hash: supplyHash });

if (supplyReceipt.status !== "success") {
  throw new Error("Supply reverted");
}
```

### Withdraw

```typescript
// Withdraw all supply shares -- pass shares amount, set assets to 0
const position = await publicClient.readContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "position",
  args: [marketId, account.address],
});
const supplyShares = position[0]; // supplyShares

const withdrawHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "withdraw",
  args: [marketParams, 0n, supplyShares, account.address, account.address],
});
const withdrawReceipt = await publicClient.waitForTransactionReceipt({ hash: withdrawHash });

if (withdrawReceipt.status !== "success") {
  throw new Error("Withdraw reverted");
}
```

### Shares vs Assets

Every supply/withdraw/borrow/repay function takes both `assets` and `shares`. Set one to zero and the other to the desired amount.

| Intent | `assets` | `shares` |
|--------|----------|----------|
| Supply 1000 USDC exactly | `1000e6` | `0` |
| Withdraw all supply | `0` | `supplyShares` |
| Borrow exact amount | `500e6` | `0` |
| Repay all debt | `0` | `borrowShares` |

Setting both nonzero reverts. Passing both as zero does nothing.

## Borrow and Repay

### Supply Collateral + Borrow

```typescript
const WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as const;
const collateralAmount = parseUnits("2", 18); // 2 WETH
const borrowAmount = parseUnits("3000", 6); // 3000 USDC

// 1. Approve collateral token
const approveCollateralHash = await walletClient.writeContract({
  address: WETH,
  abi: erc20Abi,
  functionName: "approve",
  args: [MORPHO, collateralAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveCollateralHash });

// 2. Supply collateral (separate function from supply)
const collateralHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "supplyCollateral",
  args: [marketParams, collateralAmount, account.address, "0x"],
});
const collateralReceipt = await publicClient.waitForTransactionReceipt({ hash: collateralHash });

if (collateralReceipt.status !== "success") {
  throw new Error("Supply collateral reverted");
}

// 3. Borrow loan token -- assets = borrow amount, shares = 0
const borrowHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "borrow",
  args: [marketParams, borrowAmount, 0n, account.address, account.address],
});
const borrowReceipt = await publicClient.waitForTransactionReceipt({ hash: borrowHash });

if (borrowReceipt.status !== "success") {
  throw new Error("Borrow reverted");
}
```

### Repay Debt

```typescript
const repayAmount = parseUnits("3000", 6);

// Approve loan token for repayment
const approveRepayHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [MORPHO, repayAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveRepayHash });

// Repay by assets (exact amount) -- set shares to 0
const repayHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "repay",
  args: [marketParams, repayAmount, 0n, account.address, "0x"],
});
const repayReceipt = await publicClient.waitForTransactionReceipt({ hash: repayHash });

if (repayReceipt.status !== "success") {
  throw new Error("Repay reverted");
}
```

### Repay Full Debt and Withdraw Collateral

```typescript
// Get current borrow shares to repay everything
const pos = await publicClient.readContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "position",
  args: [marketId, account.address],
});
const borrowShares = pos[1]; // borrowShares
const collateral = pos[2]; // collateral

// Accrue interest first to get accurate share-to-asset conversion
const accrueHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "accrueInterest",
  args: [marketParams],
});
await publicClient.waitForTransactionReceipt({ hash: accrueHash });

// Repay all debt by shares -- set assets to 0
// Need to approve enough loan tokens (slightly over-approve for interest)
const overApproveAmount = parseUnits("10000", 6);
const approveFullHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [MORPHO, overApproveAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveFullHash });

const repayAllHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "repay",
  args: [marketParams, 0n, borrowShares, account.address, "0x"],
});
await publicClient.waitForTransactionReceipt({ hash: repayAllHash });

// Withdraw all collateral
const withdrawCollateralHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "withdrawCollateral",
  args: [marketParams, collateral, account.address, account.address],
});
const wcReceipt = await publicClient.waitForTransactionReceipt({ hash: withdrawCollateralHash });

if (wcReceipt.status !== "success") {
  throw new Error("Withdraw collateral reverted");
}
```

## Liquidation

A position is liquidatable when `borrowed / (collateral * oraclePrice) > LLTV`. Liquidators repay part of the borrower's debt and seize their collateral at a discount.

### Liquidation Incentive

The liquidation incentive factor (LIF) determines how much collateral the liquidator receives per unit of debt repaid:

```
LIF = min(maxLIF, 1 / (1 - cursor * (1 - LLTV)))
```

Where `cursor = 0.3` and `maxLIF = 1.15` are protocol constants.

### Liquidate a Position

```typescript
const borrowerAddress = "0x...BORROWER..." as `0x${string}`;

// Option A: specify seized collateral assets, let contract compute repaid shares
const liqHash = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "liquidate",
  args: [
    marketParams,
    borrowerAddress,
    parseUnits("1", 18), // seize 1 WETH of collateral
    0n,                   // repaidShares = 0 (contract calculates)
    "0x",
  ],
});

// Option B: specify repaid debt shares, let contract compute seized assets
const liqHash2 = await walletClient.writeContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "liquidate",
  args: [
    marketParams,
    borrowerAddress,
    0n,                    // seizedAssets = 0 (contract calculates)
    1000000000000000000n,  // repaid shares amount
    "0x",
  ],
});
```

### Bad Debt Handling

When a position's collateral is worth less than its debt, full liquidation creates bad debt. Morpho Blue socializes bad debt across all suppliers in that market by reducing total supply shares proportionally. There is no insurance fund.

### Liquidation (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IMorpho, MarketParams} from "@morpho-org/morpho-blue/src/interfaces/IMorpho.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MorphoLiquidator {
    IMorpho public immutable morpho;

    constructor(address _morpho) {
        morpho = IMorpho(_morpho);
    }

    /// @notice Liquidate a borrower by specifying collateral to seize
    /// @dev Caller must have approved loanToken to this contract
    /// @param params Market parameters identifying the market
    /// @param borrower Address of the undercollateralized borrower
    /// @param seizedAssets Amount of collateral to seize (in collateral token decimals)
    function liquidateByCollateral(
        MarketParams calldata params,
        address borrower,
        uint256 seizedAssets
    ) external {
        // Pull loan tokens from caller to repay borrower's debt
        // Exact amount needed is unknown upfront -- approve generously
        IERC20(params.loanToken).transferFrom(msg.sender, address(this), type(uint256).max);
        IERC20(params.loanToken).approve(address(morpho), type(uint256).max);

        (uint256 seized, uint256 repaid) = morpho.liquidate(
            params,
            borrower,
            seizedAssets,
            0, // repaidShares = 0 -- seizedAssets determines repayment
            ""
        );

        // Return unused loan tokens and seized collateral to caller
        IERC20(params.loanToken).transfer(msg.sender, IERC20(params.loanToken).balanceOf(address(this)));
        IERC20(params.collateralToken).transfer(msg.sender, seized);
    }
}
```

## MetaMorpho Vaults

MetaMorpho vaults are ERC-4626 compliant vaults that allocate deposited assets across multiple Morpho Blue markets. A curator manages the allocation strategy. Depositors receive vault shares representing their proportional claim.

### Vault Architecture

```
Depositor -> MetaMorpho Vault -> Morpho Blue Market 1
                               -> Morpho Blue Market 2
                               -> Morpho Blue Market 3
```

### Deposit into a MetaMorpho Vault

```typescript
// ERC-4626 interface
const vaultAbi = [
  {
    name: "deposit",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "assets", type: "uint256" },
      { name: "receiver", type: "address" },
    ],
    outputs: [{ name: "shares", type: "uint256" }],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "assets", type: "uint256" },
      { name: "receiver", type: "address" },
      { name: "owner", type: "address" },
    ],
    outputs: [{ name: "shares", type: "uint256" }],
  },
  {
    name: "redeem",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "shares", type: "uint256" },
      { name: "receiver", type: "address" },
      { name: "owner", type: "address" },
    ],
    outputs: [{ name: "assets", type: "uint256" }],
  },
  {
    name: "totalAssets",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "convertToAssets",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "shares", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "convertToShares",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "assets", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "maxDeposit",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "receiver", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Steakhouse USDC vault (example)
const VAULT = "0xBEEF01735c132Ada46AA9aA9B6290e7a2CE81cd" as `0x${string}`;
const depositAmount = parseUnits("10000", 6); // 10,000 USDC

// Check deposit cap
const maxDeposit = await publicClient.readContract({
  address: VAULT,
  abi: vaultAbi,
  functionName: "maxDeposit",
  args: [account.address],
});

if (depositAmount > maxDeposit) {
  throw new Error(`Deposit exceeds vault cap. Max: ${maxDeposit}`);
}

// Approve vault to spend USDC
const approveVaultHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [VAULT, depositAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveVaultHash });

// Deposit into vault
const depositHash = await walletClient.writeContract({
  address: VAULT,
  abi: vaultAbi,
  functionName: "deposit",
  args: [depositAmount, account.address],
});
const depositReceipt = await publicClient.waitForTransactionReceipt({ hash: depositHash });

if (depositReceipt.status !== "success") {
  throw new Error("Vault deposit reverted");
}
```

### Withdraw from a MetaMorpho Vault

```typescript
// Withdraw by specifying assets (exact USDC amount to receive)
const withdrawAmount = parseUnits("5000", 6);

const vaultWithdrawHash = await walletClient.writeContract({
  address: VAULT,
  abi: vaultAbi,
  functionName: "withdraw",
  args: [withdrawAmount, account.address, account.address],
});
const vaultWithdrawReceipt = await publicClient.waitForTransactionReceipt({ hash: vaultWithdrawHash });

if (vaultWithdrawReceipt.status !== "success") {
  throw new Error("Vault withdraw reverted");
}
```

### Vault Roles

| Role | Permissions |
|------|------------|
| **Owner** | Set curator, guardian, fee recipient, timelock |
| **Curator** | Set supply queue, withdraw queue, caps per market |
| **Guardian** | Revoke pending timelocked actions |
| **Allocator** | Reallocate funds between queued markets |

## Oracles

### 36-Decimal Price Scaling

Morpho Blue oracles return price with a specific decimal scaling:

```
priceDecimals = 36 + loanTokenDecimals - collateralTokenDecimals
```

This ensures the internal math works correctly regardless of token decimal differences.

| Market (loan/collateral) | Loan Decimals | Collateral Decimals | Oracle Decimals |
|-------------------------|---------------|--------------------|-----------------
| USDC/WETH | 6 | 18 | 36 + 6 - 18 = 24 |
| USDC/wstETH | 6 | 18 | 24 |
| DAI/WETH | 18 | 18 | 36 |
| USDT/WBTC | 6 | 8 | 34 |

### Oracle Interface

```solidity
interface IOracle {
    /// @notice Returns the price of 1 unit of collateral token quoted in loan token
    /// @dev Price is scaled to 36 + loanTokenDecimals - collateralTokenDecimals decimals
    function price() external view returns (uint256);
}
```

### Reading Oracle Price

```typescript
const oracleAbi = [
  {
    name: "price",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const rawPrice = await publicClient.readContract({
  address: marketParams.oracle,
  abi: oracleAbi,
  functionName: "price",
});

// For USDC/WETH market: price has 24 decimals
// Convert to human-readable price of 1 ETH in USDC
const ethPriceUsd = Number(rawPrice) / 1e24;
console.log(`ETH price: $${ethPriceUsd}`);
```

### Morpho Oracle Adapters

Morpho provides oracle adapter contracts that wrap Chainlink feeds into the required 36-decimal format. Use `MorphoChainlinkOracleV2` for new deployments.

## Interest Rate Model

### AdaptiveCurveIRM

Morpho Blue uses an adaptive interest rate model that adjusts rates based on utilization. The model has no governance-controlled parameters -- it self-adjusts.

**Key properties:**
- Rate increases when utilization is above target (90%)
- Rate decreases when utilization is below target
- Adjustment speed is proportional to distance from target
- The curve is exponential, not linear

### Rate Curve Behavior

```
Utilization < 90%  -> Rate decreases over time
Utilization = 90%  -> Rate stable
Utilization > 90%  -> Rate increases over time
```

### Reading Current Rates

```typescript
const marketData = await publicClient.readContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "market",
  args: [marketId],
});

const [
  totalSupplyAssets,
  totalSupplyShares,
  totalBorrowAssets,
  totalBorrowShares,
  lastUpdate,
  fee,
] = marketData;

// Utilization = totalBorrowAssets / totalSupplyAssets
const utilization = totalSupplyAssets > 0n
  ? (totalBorrowAssets * 10000n) / totalSupplyAssets
  : 0n;

console.log(`Utilization: ${Number(utilization) / 100}%`);
console.log(`Total supply: ${totalSupplyAssets}`);
console.log(`Total borrow: ${totalBorrowAssets}`);
```

## Contract Addresses

> **Last verified:** February 2026

### Core Contracts (Ethereum Mainnet)

| Contract | Address |
|----------|---------|
| Morpho Blue (Singleton) | `0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb` |
| AdaptiveCurveIRM | `0x870aC11D48B15DB9a138Cf899d20F13F79Ba00BC` |
| MetaMorpho Factory | `0xA9c3D3a366466Fa809d1Ae982Fb2c46E5fC41101` |
| Morpho Bundler V2 | `0x4095F064B8d3c3548A3bebfd0Bbfd04750E30077` |
| MorphoChainlinkOracleV2 Factory | `0x3A7bB36Ee3f3eE32A60e9a666B659756A49eFFa3` |

### Common Token Addresses (Ethereum Mainnet)

| Token | Address | Decimals |
|-------|---------|----------|
| WETH | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | 18 |
| USDC | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | 6 |
| USDT | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | 6 |
| DAI | `0x6B175474E89094C44Da98b954EedeAC495271d0F` | 18 |
| wstETH | `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0` | 18 |
| WBTC | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` | 8 |

> Verify any address before mainnet use: `cast code <address> --rpc-url $RPC_URL`

## Reading Protocol State

### Get Market Data

```typescript
const marketId = computeMarketId(marketParams);

const marketData = await publicClient.readContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "market",
  args: [marketId],
});

const [
  totalSupplyAssets,
  totalSupplyShares,
  totalBorrowAssets,
  totalBorrowShares,
  lastUpdate,
  fee,
] = marketData;

console.log(`Total supply: ${totalSupplyAssets}`);
console.log(`Total borrow: ${totalBorrowAssets}`);
// Fee is in WAD (18 decimals), 0 = no fee, 0.1e18 = 10%
console.log(`Fee: ${Number(fee) / 1e18 * 100}%`);
```

### Get User Position

```typescript
const position = await publicClient.readContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "position",
  args: [marketId, account.address],
});

const [supplyShares, borrowShares, collateral] = position;
console.log(`Supply shares: ${supplyShares}`);
console.log(`Borrow shares: ${borrowShares}`);
console.log(`Collateral: ${collateral}`);
```

### Convert Shares to Assets

```typescript
// To convert supply shares to asset amount:
// assets = shares * totalSupplyAssets / totalSupplyShares
function sharesToAssets(
  shares: bigint,
  totalAssets: bigint,
  totalShares: bigint
): bigint {
  if (totalShares === 0n) return 0n;
  return (shares * totalAssets) / totalShares;
}

const supplyAssets = sharesToAssets(
  supplyShares,
  totalSupplyAssets,
  totalSupplyShares
);
console.log(`Supply value: ${supplyAssets}`);
```

### Reverse-Lookup Market Params from ID

```typescript
const params = await publicClient.readContract({
  address: MORPHO,
  abi: morphoAbi,
  functionName: "idToMarketParams",
  args: [marketId],
});
console.log(`Loan token: ${params.loanToken}`);
console.log(`Collateral token: ${params.collateralToken}`);
```

## Error Handling

```typescript
import { BaseError, ContractFunctionRevertedError } from "viem";

try {
  await publicClient.simulateContract({
    address: MORPHO,
    abi: morphoAbi,
    functionName: "borrow",
    args: [marketParams, parseUnits("1000", 6), 0n, account.address, account.address],
    account: account.address,
  });
} catch (err) {
  if (err instanceof BaseError) {
    const revertError = err.walk(
      (e) => e instanceof ContractFunctionRevertedError
    );
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName;
      console.error(`Morpho revert: ${errorName}`);
    }
  }
}
```

## Security

### Position Health Monitoring

Unlike Aave, Morpho Blue does not have a built-in health factor getter. You must compute it manually:

```typescript
async function isLiquidatable(
  marketParams: MarketParams,
  borrower: `0x${string}`
): Promise<{ liquidatable: boolean; ltv: number }> {
  const marketId = computeMarketId(marketParams);

  const [marketData, position, oraclePrice] = await Promise.all([
    publicClient.readContract({
      address: MORPHO,
      abi: morphoAbi,
      functionName: "market",
      args: [marketId],
    }),
    publicClient.readContract({
      address: MORPHO,
      abi: morphoAbi,
      functionName: "position",
      args: [marketId, borrower],
    }),
    publicClient.readContract({
      address: marketParams.oracle,
      abi: [{ name: "price", type: "function", stateMutability: "view", inputs: [], outputs: [{ name: "", type: "uint256" }] }] as const,
      functionName: "price",
    }),
  ]);

  const [totalSupplyAssets, totalSupplyShares, totalBorrowAssets, totalBorrowShares] = marketData;
  const [, borrowShares, collateral] = position;

  if (borrowShares === 0n) return { liquidatable: false, ltv: 0 };
  if (collateral === 0n) return { liquidatable: true, ltv: Infinity };

  // Convert borrow shares to assets
  const borrowAssets = (BigInt(borrowShares) * totalBorrowAssets) / totalBorrowShares;

  // collateralValue in loan token terms = collateral * oraclePrice / ORACLE_PRICE_SCALE
  // ORACLE_PRICE_SCALE = 10^(36 + loanDecimals - collateralDecimals)
  const ORACLE_PRICE_SCALE = 10n ** 36n; // simplified for same-decimal tokens; adjust per market
  const collateralValueInLoanToken = (BigInt(collateral) * oraclePrice) / ORACLE_PRICE_SCALE;

  const currentLtv = collateralValueInLoanToken > 0n
    ? Number(borrowAssets * 10000n / collateralValueInLoanToken) / 100
    : Infinity;

  const lltvPercent = Number(marketParams.lltv) / 1e18 * 100;

  return {
    liquidatable: currentLtv >= lltvPercent,
    ltv: currentLtv,
  };
}
```

### Best Practices

1. **Simulate before executing** -- Always call `simulateContract` before `writeContract` to catch reverts without spending gas.
2. **Check `receipt.status`** -- A confirmed transaction can still revert. Always verify `receipt.status === "success"`.
3. **Monitor position health off-chain** -- Set alerts when LTV approaches LLTV. Morpho Blue has no safety buffer built in.
4. **Use shares for full repayment** -- When repaying all debt, pass `borrowShares` (not assets) to avoid dust remaining from interest accrual between blocks.
5. **Accrue interest before reads** -- Call `accrueInterest()` before reading market state for accurate share-to-asset conversion.
6. **Approve exact amounts** -- Avoid unlimited approvals in production. Approve only what is needed per transaction.
7. **Verify oracle freshness** -- Morpho Blue does not validate oracle staleness. If the oracle stops updating, liquidations may execute at stale prices.

## References

- [Morpho Blue Technical Docs](https://docs.morpho.org)
- [Morpho Blue GitHub](https://github.com/morpho-org/morpho-blue)
- [MetaMorpho GitHub](https://github.com/morpho-org/metamorpho)
- [Morpho Blue Whitepaper](https://github.com/morpho-org/morpho-blue/blob/main/morpho-blue-whitepaper.pdf)
- [AdaptiveCurveIRM](https://github.com/morpho-org/morpho-blue-irm)
- [Morpho Oracle Adapters](https://github.com/morpho-org/morpho-blue-oracles)
- [Morpho App](https://app.morpho.org)
