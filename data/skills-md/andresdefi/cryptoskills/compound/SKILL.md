---
name: compound
description: Compound V3 (Comet) lending protocol — supply, borrow, repay, withdraw, liquidation, governance proposals, and cross-chain Comet deployments. Covers Comet interface (single-asset borrowing), Configurator, Bulker for batched operations, and COMP governance across Ethereum, Arbitrum, Base, Optimism, and Polygon.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: DeFi
tags:
  - compound
  - lending
  - borrowing
  - comet
  - defi
  - governance
---

# Compound V3 (Comet)

Compound V3 (codenamed "Comet") is a lending protocol where each market has exactly one borrowable base asset (e.g., USDC or WETH). Users supply collateral to borrow the base asset, or supply the base asset to earn interest. Unlike shared-pool models, each Comet deployment is a standalone contract with its own collateral configuration, interest rate model, and risk parameters.

## What You Probably Got Wrong

> LLMs conflate V2 and V3 constantly. Compound V3 is a ground-up rewrite with a completely different architecture. These corrections are non-negotiable.

- **V3 (Comet) is NOT V2 — completely different architecture.** V3 has one borrowable asset per market (e.g., a USDC market, a WETH market). V2 had shared pools where every asset was both borrowable and suppliable. If you see `cToken`, `mint()`, `redeem()`, or `Comptroller`, you are writing V2 code. Stop.
- **cTokens do NOT exist in V3.** There is no mint/redeem flow. You call `supply()` and `withdraw()` directly on the Comet contract. There are no ERC-20 receipt tokens for collateral positions.
- **Supplying the base asset earns interest. Supplying collateral does NOT.** If you supply USDC to the USDC market, you earn interest. If you supply WETH as collateral to the USDC market, it earns zero yield — it only backs your borrow.
- **`supply()` with the base asset = lending. `supply()` with collateral = collateralize.** Same function, different behavior depending on whether the asset is the market's base asset or a configured collateral asset.
- **`withdraw()` on the base asset when you have a borrow = repaying debt, not withdrawing.** If your base asset balance is negative (you borrowed), calling `withdraw()` does not give you tokens — it increases your debt. Use `supply()` to repay.
- **Liquidation uses `absorb()` not `liquidateBorrow()`.** The protocol absorbs the underwater position, socializing bad debt if any, then sells the seized collateral via `buyCollateral()` at a discount. This is a two-step process, not an atomic liquidation.
- **Interest accrues per-second in V3, not per-block like V2.** The `baseTrackingSupplySpeed` and `baseTrackingBorrowSpeed` are per-second rates. Block-based assumptions from V2 will produce wrong calculations.
- **Account balances can be negative (borrowed).** `balanceOf(user)` returns the base asset balance which is zero for pure collateral suppliers. Use `borrowBalanceOf(user)` for outstanding debt and `collateralBalanceOf(user, asset)` for collateral amounts.
- **Comet is not upgradeable in the traditional proxy sense.** It uses a `Configurator` + `ProxyAdmin` pattern where configuration changes deploy a new implementation and the proxy is pointed to it. The proxy address stays constant.
- **COMP rewards are claimed through CometRewards, not Comet itself.** Call `CometRewards.claim(comet, account, true)` to claim accrued COMP. The Comet contract tracks reward accrual but does not distribute tokens.

## Quick Start

### Installation

```bash
npm install viem
```

Compound V3 does not require a dedicated SDK package. All interaction is through the Comet contract ABI using viem or ethers.

### Minimal ABI Fragments

```typescript
const cometAbi = [
  {
    name: "supply",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "supplyTo",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "dst", type: "address" },
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "withdrawTo",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "borrowBalanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "collateralBalanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "account", type: "address" },
      { name: "asset", type: "address" },
    ],
    outputs: [{ name: "", type: "uint128" }],
  },
  {
    name: "getAssetInfo",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "i", type: "uint8" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "offset", type: "uint8" },
          { name: "asset", type: "address" },
          { name: "priceFeed", type: "address" },
          { name: "scale", type: "uint64" },
          { name: "borrowCollateralFactor", type: "uint64" },
          { name: "liquidateCollateralFactor", type: "uint64" },
          { name: "liquidationFactor", type: "uint64" },
          { name: "supplyCap", type: "uint128" },
        ],
      },
    ],
  },
  {
    name: "getAssetInfoByAddress",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "asset", type: "address" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "offset", type: "uint8" },
          { name: "asset", type: "address" },
          { name: "priceFeed", type: "address" },
          { name: "scale", type: "uint64" },
          { name: "borrowCollateralFactor", type: "uint64" },
          { name: "liquidateCollateralFactor", type: "uint64" },
          { name: "liquidationFactor", type: "uint64" },
          { name: "supplyCap", type: "uint128" },
        ],
      },
    ],
  },
  {
    name: "numAssets",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint8" }],
  },
  {
    name: "baseToken",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "baseTokenPriceFeed",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "getUtilization",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "getSupplyRate",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "utilization", type: "uint256" }],
    outputs: [{ name: "", type: "uint64" }],
  },
  {
    name: "getBorrowRate",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "utilization", type: "uint256" }],
    outputs: [{ name: "", type: "uint64" }],
  },
  {
    name: "getPrice",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "priceFeed", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "totalSupply",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "totalBorrow",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "isLiquidatable",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "bool" }],
  },
  {
    name: "absorb",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "absorber", type: "address" },
      { name: "accounts", type: "address[]" },
    ],
    outputs: [],
  },
  {
    name: "buyCollateral",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "minAmount", type: "uint256" },
      { name: "baseAmount", type: "uint256" },
      { name: "recipient", type: "address" },
    ],
    outputs: [],
  },
  {
    name: "quoteCollateral",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "asset", type: "address" },
      { name: "baseAmount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "allow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "manager", type: "address" },
      { name: "isAllowed", type: "bool" },
    ],
    outputs: [],
  },
  {
    name: "hasPermission",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "owner", type: "address" },
      { name: "manager", type: "address" },
    ],
    outputs: [{ name: "", type: "bool" }],
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
  {
    name: "allowance",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "owner", type: "address" },
      { name: "spender", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const cometRewardsAbi = [
  {
    name: "claim",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "comet", type: "address" },
      { name: "src", type: "address" },
      { name: "shouldAccrue", type: "bool" },
    ],
    outputs: [],
  },
  {
    name: "getRewardOwed",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "comet", type: "address" },
      { name: "account", type: "address" },
    ],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "token", type: "address" },
          { name: "owed", type: "uint256" },
        ],
      },
    ],
  },
] as const;
```

### Connect to Comet (Ethereum USDC Market)

```typescript
import { createPublicClient, createWalletClient, http, parseUnits } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

// Ethereum mainnet USDC market (cUSDCv3)
const COMET_USDC = "0xc3d688B66703497DAA19211EEdff47f25384cdc3" as const;
const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as const;
const WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as const;
const COMET_REWARDS = "0x1B0e765F6224C21223AeA2af16c1C46E38885a40" as const;

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
```

## Core Architecture

### How Comet Works

Each Comet deployment is a single contract that manages one base asset market:

```
Comet (Proxy)
├── Base Asset (e.g., USDC) — borrowable, earns interest when supplied
├── Collateral Asset 1 (e.g., WETH) — supplies back borrows, no interest
├── Collateral Asset 2 (e.g., WBTC) — supplies back borrows, no interest
├── Collateral Asset N...
├── Interest Rate Model — per-second accrual, utilization-based
├── Price Feeds — Chainlink oracles for each asset
└── Liquidation Engine — absorb() + buyCollateral()
```

### Key Contracts

| Contract | Purpose |
|----------|---------|
| **Comet** (proxy) | Main entry point. Supply, borrow, withdraw, liquidate. One per market. |
| **Configurator** | Governance-controlled. Sets collateral factors, caps, rate curves. |
| **CometRewards** | Distributes COMP rewards. Tracks accrual per Comet instance. |
| **Bulker** | Batches multiple Comet operations in one transaction. Wraps/unwraps ETH. |
| **CometProxyAdmin** | Upgrades Comet proxy to new implementations after Configurator changes. |

### Permission System

Compound V3 uses an `allow()` mechanism instead of ERC-20 approvals for position management. A manager with permission can supply, withdraw, and transfer on behalf of the owner.

```typescript
// Grant permission to a manager (e.g., a contract or another wallet)
const allowHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "allow",
  args: ["0xYourManagerAddress" as `0x${string}`, true],
});
const allowReceipt = await publicClient.waitForTransactionReceipt({ hash: allowHash });
if (allowReceipt.status !== "success") throw new Error("allow() reverted");
```

## Supply & Earn

Supply the base asset to earn interest. The Comet contract tracks your balance internally — no receipt tokens.

### Supply Base Asset (TypeScript)

```typescript
const supplyAmount = parseUnits("10000", 6); // 10,000 USDC

// Approve Comet to pull USDC
const approveHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [COMET_USDC, supplyAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveHash });

// Supply USDC to earn interest
const supplyHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "supply",
  args: [USDC, supplyAmount],
});
const supplyReceipt = await publicClient.waitForTransactionReceipt({ hash: supplyHash });

if (supplyReceipt.status !== "success") {
  throw new Error("Supply transaction reverted");
}
```

### Supply Base Asset (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IComet {
    function supply(address asset, uint256 amount) external;
    function withdraw(address asset, uint256 amount) external;
    function balanceOf(address account) external view returns (uint256);
    function baseToken() external view returns (address);
}

/// @notice Supplies base asset to Compound V3 on behalf of msg.sender
contract CometSupplier {
    IComet public immutable comet;
    address public immutable baseToken;

    constructor(address _comet) {
        comet = IComet(_comet);
        baseToken = IComet(_comet).baseToken();
    }

    /// @notice Supply base asset to earn interest
    /// @param amount Amount in base asset's native decimals
    function supplyBase(uint256 amount) external {
        IERC20(baseToken).transferFrom(msg.sender, address(this), amount);
        IERC20(baseToken).approve(address(comet), amount);
        comet.supply(baseToken, amount);
    }
}
```

### Check Supply Rate

```typescript
// Rates are per-second, scaled by 1e18
const utilization = await publicClient.readContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "getUtilization",
});

const supplyRate = await publicClient.readContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "getSupplyRate",
  args: [utilization],
});

// Convert per-second rate to APR: rate * seconds_per_year
const SECONDS_PER_YEAR = 31_536_000n;
const supplyApr = Number(supplyRate * SECONDS_PER_YEAR) / 1e18;
console.log(`Supply APR: ${(supplyApr * 100).toFixed(2)}%`);
```

## Collateral & Borrow

Supply a collateral asset, then borrow the base asset against it. Collateral does not earn interest.

### Supply Collateral and Borrow (TypeScript)

```typescript
const collateralAmount = parseUnits("5", 18); // 5 WETH
const borrowAmount = parseUnits("5000", 6); // 5,000 USDC

// Approve Comet to pull WETH collateral
const approveCollateralHash = await walletClient.writeContract({
  address: WETH,
  abi: erc20Abi,
  functionName: "approve",
  args: [COMET_USDC, collateralAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveCollateralHash });

// Supply WETH as collateral (NOT the base asset — no interest earned)
const supplyCollateralHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "supply",
  args: [WETH, collateralAmount],
});
const collateralReceipt = await publicClient.waitForTransactionReceipt({
  hash: supplyCollateralHash,
});
if (collateralReceipt.status !== "success") {
  throw new Error("Collateral supply reverted");
}

// Borrow USDC against collateral
// withdraw() on the base asset when you have no supply = borrow
const borrowHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "withdraw",
  args: [USDC, borrowAmount],
});
const borrowReceipt = await publicClient.waitForTransactionReceipt({ hash: borrowHash });

if (borrowReceipt.status !== "success") {
  throw new Error("Borrow transaction reverted");
}
```

### Check Borrow Capacity

```typescript
async function getBorrowCapacity(
  userAddress: `0x${string}`,
  collateralAsset: `0x${string}`
): Promise<{ collateralValue: bigint; borrowCapacity: bigint }> {
  const assetInfo = await publicClient.readContract({
    address: COMET_USDC,
    abi: cometAbi,
    functionName: "getAssetInfoByAddress",
    args: [collateralAsset],
  });

  const collateralBalance = await publicClient.readContract({
    address: COMET_USDC,
    abi: cometAbi,
    functionName: "collateralBalanceOf",
    args: [userAddress, collateralAsset],
  });

  const price = await publicClient.readContract({
    address: COMET_USDC,
    abi: cometAbi,
    functionName: "getPrice",
    args: [assetInfo.priceFeed],
  });

  // borrowCollateralFactor is scaled by 1e18
  // price is scaled by 1e8 (Chainlink format)
  // scale normalizes to base asset decimals
  const collateralValue =
    (BigInt(collateralBalance) * price) / BigInt(assetInfo.scale);
  const borrowCapacity =
    (collateralValue * BigInt(assetInfo.borrowCollateralFactor)) / (1n * 10n ** 18n);

  return { collateralValue, borrowCapacity };
}
```

### Check Borrow Rate

```typescript
const borrowRate = await publicClient.readContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "getBorrowRate",
  args: [utilization],
});

const SECONDS_PER_YEAR = 31_536_000n;
const borrowApr = Number(borrowRate * SECONDS_PER_YEAR) / 1e18;
console.log(`Borrow APR: ${(borrowApr * 100).toFixed(2)}%`);
```

## Repay & Withdraw

### Repay Borrow (TypeScript)

To repay a borrow, `supply()` the base asset. This reduces your negative balance.

```typescript
const repayAmount = parseUnits("5000", 6); // Repay 5,000 USDC

// Approve Comet to pull USDC for repayment
const approveRepayHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [COMET_USDC, repayAmount],
});
await publicClient.waitForTransactionReceipt({ hash: approveRepayHash });

// supply() the base asset to repay debt
const repayHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "supply",
  args: [USDC, repayAmount],
});
const repayReceipt = await publicClient.waitForTransactionReceipt({ hash: repayHash });

if (repayReceipt.status !== "success") {
  throw new Error("Repay transaction reverted");
}

// Verify remaining debt
const remainingDebt = await publicClient.readContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "borrowBalanceOf",
  args: [account.address],
});
console.log(`Remaining debt: ${Number(remainingDebt) / 1e6} USDC`);
```

### Withdraw Collateral (TypeScript)

After repaying debt, withdraw collateral. Reverts if withdrawal would make the position liquidatable.

```typescript
const withdrawCollateralAmount = parseUnits("5", 18); // 5 WETH

const withdrawHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "withdraw",
  args: [WETH, withdrawCollateralAmount],
});
const withdrawReceipt = await publicClient.waitForTransactionReceipt({
  hash: withdrawHash,
});

if (withdrawReceipt.status !== "success") {
  throw new Error("Withdraw collateral reverted");
}
```

### Repay Full Debt (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IComet {
    function supply(address asset, uint256 amount) external;
    function withdraw(address asset, uint256 amount) external;
    function borrowBalanceOf(address account) external view returns (uint256);
    function baseToken() external view returns (address);
}

/// @notice Repays full Compound V3 debt and withdraws collateral
contract CometRepayer {
    IComet public immutable comet;
    address public immutable baseToken;

    constructor(address _comet) {
        comet = IComet(_comet);
        baseToken = IComet(_comet).baseToken();
    }

    /// @notice Repay entire borrow balance
    /// @dev Caller must approve this contract for at least borrowBalanceOf(msg.sender)
    function repayFullDebt() external {
        uint256 debt = comet.borrowBalanceOf(msg.sender);
        if (debt == 0) revert("No debt to repay");

        IERC20(baseToken).transferFrom(msg.sender, address(this), debt);
        IERC20(baseToken).approve(address(comet), debt);
        // supply() base asset to repay the negative balance
        comet.supply(baseToken, debt);
    }

    /// @notice Withdraw collateral after debt is repaid
    /// @param collateral Collateral asset address
    /// @param amount Amount to withdraw in collateral's native decimals
    function withdrawCollateral(address collateral, uint256 amount) external {
        // Comet checks that withdrawal does not make position liquidatable
        comet.withdraw(collateral, amount);
    }
}
```

## Liquidation

Compound V3 liquidation is a two-step process: `absorb()` seizes the underwater position, then `buyCollateral()` lets anyone purchase the seized collateral at a discount.

### Step 1: Absorb

Anyone can call `absorb()` on a liquidatable account. The protocol takes over the position, clearing the borrower's debt and seizing their collateral into the protocol's reserves.

```typescript
// Check if account is liquidatable
const isLiquidatable = await publicClient.readContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "isLiquidatable",
  args: ["0xBorrowerAddress" as `0x${string}`],
});

if (!isLiquidatable) {
  throw new Error("Account is not liquidatable");
}

// Absorb the underwater position
const absorbHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "absorb",
  args: [
    account.address, // absorber receives no direct reward; incentive is buyCollateral discount
    ["0xBorrowerAddress" as `0x${string}`], // can batch multiple accounts
  ],
});
const absorbReceipt = await publicClient.waitForTransactionReceipt({ hash: absorbHash });

if (absorbReceipt.status !== "success") {
  throw new Error("Absorb transaction reverted");
}
```

### Step 2: Buy Collateral

After absorption, the protocol holds collateral in its reserves. Anyone can buy it at a discount by paying the base asset.

```typescript
const WETH_COLLATERAL = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as const;

// Quote how much collateral you get for a given base amount
const baseAmountToPay = parseUnits("1000", 6); // 1,000 USDC
const collateralOut = await publicClient.readContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "quoteCollateral",
  args: [WETH_COLLATERAL, baseAmountToPay],
});
console.log(`Collateral out: ${Number(collateralOut) / 1e18} WETH`);

// Approve Comet to pull base asset
const approveForBuyHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [COMET_USDC, baseAmountToPay],
});
await publicClient.waitForTransactionReceipt({ hash: approveForBuyHash });

// Buy collateral at a discount
// minAmount protects against price changes between quote and execution
const minCollateralOut = (collateralOut * 99n) / 100n; // 1% slippage
const buyHash = await walletClient.writeContract({
  address: COMET_USDC,
  abi: cometAbi,
  functionName: "buyCollateral",
  args: [WETH_COLLATERAL, minCollateralOut, baseAmountToPay, account.address],
});
const buyReceipt = await publicClient.waitForTransactionReceipt({ hash: buyHash });

if (buyReceipt.status !== "success") {
  throw new Error("buyCollateral reverted");
}
```

## Governance

Compound governance uses COMP tokens, GovernorBravo, and a Timelock for protocol changes.

### Governance Contracts

| Contract | Ethereum Address |
|----------|-----------------|
| COMP Token | `0xc00e94Cb662C3520282E6f5717214004A7f26888` |
| GovernorBravo | `0xc0Da02939E1441F497fd74F78cE7Decb17B66529` |
| Timelock | `0x6d903f6003cca6255D85CcA4D3B5E5146dC33925` |

### Create a Proposal (TypeScript)

```typescript
const governorBravoAbi = [
  {
    name: "propose",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "targets", type: "address[]" },
      { name: "values", type: "uint256[]" },
      { name: "signatures", type: "string[]" },
      { name: "calldatas", type: "bytes[]" },
      { name: "description", type: "string" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "castVote",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "proposalId", type: "uint256" },
      { name: "support", type: "uint8" },
    ],
    outputs: [],
  },
  {
    name: "state",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "proposalId", type: "uint256" }],
    outputs: [{ name: "", type: "uint8" }],
  },
] as const;

const GOVERNOR_BRAVO = "0xc0Da02939E1441F497fd74F78cE7Decb17B66529" as const;

// Proposer needs >= 25,000 COMP delegated to their address
const proposeHash = await walletClient.writeContract({
  address: GOVERNOR_BRAVO,
  abi: governorBravoAbi,
  functionName: "propose",
  args: [
    ["0xTargetContractAddress" as `0x${string}`], // targets
    [0n], // values (ETH to send)
    ["setBaseTrackingSupplySpeed(address,uint64)"], // function signatures
    ["0x..." as `0x${string}`], // encoded calldata
    "Proposal #X: Adjust supply rewards for USDC market", // description
  ],
});
const proposeReceipt = await publicClient.waitForTransactionReceipt({ hash: proposeHash });
if (proposeReceipt.status !== "success") throw new Error("Propose reverted");
```

### Vote on a Proposal

```typescript
// support: 0 = Against, 1 = For, 2 = Abstain
const voteHash = await walletClient.writeContract({
  address: GOVERNOR_BRAVO,
  abi: governorBravoAbi,
  functionName: "castVote",
  args: [42n, 1], // proposalId, support (For)
});
const voteReceipt = await publicClient.waitForTransactionReceipt({ hash: voteHash });
if (voteReceipt.status !== "success") throw new Error("Vote reverted");
```

## Bulker (Batched Operations)

The Bulker contract batches multiple Comet operations into one transaction and handles ETH wrapping/unwrapping.

```typescript
const bulkerAbi = [
  {
    name: "invoke",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "actions", type: "bytes32[]" },
      { name: "data", type: "bytes[]" },
    ],
    outputs: [],
  },
] as const;

// Ethereum mainnet Bulker
const BULKER = "0xa397a8C2086C554B531c02E29f3291c9704B2DCf" as const;

// Action codes
// ACTION_SUPPLY_ASSET = 0x414354494f4e5f535550504c595f41535345540000000000000000000000000000
// ACTION_SUPPLY_NATIVE_TOKEN = 0x414354494f4e5f535550504c595f4e41544956455f544f4b454e000000000000
// ACTION_WITHDRAW_ASSET = 0x414354494f4e5f57495448445241575f4153534554000000000000000000000000
// ACTION_WITHDRAW_NATIVE_TOKEN = 0x414354494f4e5f57495448445241575f4e41544956455f544f4b454e00000000
// ACTION_CLAIM_REWARD = 0x414354494f4e5f434c41494d5f524557415244000000000000000000000000000

import { encodeAbiParameters, parseAbiParameters } from "viem";

// Supply ETH as collateral (Bulker wraps to WETH)
const supplyNativeAction =
  "0x414354494f4e5f535550504c595f4e41544956455f544f4b454e000000000000" as `0x${string}`;

const supplyNativeData = encodeAbiParameters(
  parseAbiParameters("address comet, address to, uint amount"),
  [COMET_USDC, account.address, parseUnits("1", 18)]
);

const bulkerHash = await walletClient.writeContract({
  address: BULKER,
  abi: bulkerAbi,
  functionName: "invoke",
  args: [[supplyNativeAction], [supplyNativeData]],
  value: parseUnits("1", 18), // Send ETH with the transaction
});
const bulkerReceipt = await publicClient.waitForTransactionReceipt({ hash: bulkerHash });
if (bulkerReceipt.status !== "success") throw new Error("Bulker invoke reverted");
```

## Reading Account State

### Complete Account Summary

```typescript
async function getAccountSummary(userAddress: `0x${string}`) {
  const [baseBalance, borrowBalance, numAssets] = await Promise.all([
    publicClient.readContract({
      address: COMET_USDC,
      abi: cometAbi,
      functionName: "balanceOf",
      args: [userAddress],
    }),
    publicClient.readContract({
      address: COMET_USDC,
      abi: cometAbi,
      functionName: "borrowBalanceOf",
      args: [userAddress],
    }),
    publicClient.readContract({
      address: COMET_USDC,
      abi: cometAbi,
      functionName: "numAssets",
    }),
  ]);

  // Read collateral balances for all configured assets
  const collaterals: { asset: `0x${string}`; balance: bigint }[] = [];
  for (let i = 0; i < numAssets; i++) {
    const assetInfo = await publicClient.readContract({
      address: COMET_USDC,
      abi: cometAbi,
      functionName: "getAssetInfo",
      args: [i],
    });

    const collateralBalance = await publicClient.readContract({
      address: COMET_USDC,
      abi: cometAbi,
      functionName: "collateralBalanceOf",
      args: [userAddress, assetInfo.asset],
    });

    if (collateralBalance > 0n) {
      collaterals.push({ asset: assetInfo.asset, balance: BigInt(collateralBalance) });
    }
  }

  return {
    baseSupplied: baseBalance, // USDC supplied (earning interest)
    baseBorrowed: borrowBalance, // USDC borrowed (accruing debt)
    collaterals, // Non-zero collateral positions
    isLiquidatable: await publicClient.readContract({
      address: COMET_USDC,
      abi: cometAbi,
      functionName: "isLiquidatable",
      args: [userAddress],
    }),
  };
}
```

### Claim COMP Rewards

```typescript
const rewardOwed = await publicClient.readContract({
  address: COMET_REWARDS,
  abi: cometRewardsAbi,
  functionName: "getRewardOwed",
  args: [COMET_USDC, account.address],
});
console.log(`COMP owed: ${Number(rewardOwed.owed) / 1e18}`);

const claimHash = await walletClient.writeContract({
  address: COMET_REWARDS,
  abi: cometRewardsAbi,
  functionName: "claim",
  args: [COMET_USDC, account.address, true],
});
const claimReceipt = await publicClient.waitForTransactionReceipt({ hash: claimHash });
if (claimReceipt.status !== "success") throw new Error("Claim reverted");
```

## Contract Addresses

> **Last verified:** February 2026

See `resources/contract-addresses.md` for the full multi-chain address table.

### Ethereum Mainnet (Key Addresses)

| Contract | Address |
|----------|---------|
| Comet USDC (cUSDCv3) | `0xc3d688B66703497DAA19211EEdff47f25384cdc3` |
| Comet WETH (cWETHv3) | `0xA17581A9E3356d9A858b789D68B4d866e593aE94` |
| CometRewards | `0x1B0e765F6224C21223AeA2af16c1C46E38885a40` |
| Configurator | `0x316f9708bB98af7dA9c68C1C3b5e79039cD336E3` |
| Bulker | `0xa397a8C2086C554B531c02E29f3291c9704B2DCf` |
| COMP Token | `0xc00e94Cb662C3520282E6f5717214004A7f26888` |
| GovernorBravo | `0xc0Da02939E1441F497fd74F78cE7Decb17B66529` |
| Timelock | `0x6d903f6003cca6255D85CcA4D3B5E5146dC33925` |

> Verify any address before mainnet use: `cast code <address> --rpc-url $RPC_URL`

## Error Handling

### Handling Reverts in TypeScript

```typescript
import { BaseError, ContractFunctionRevertedError } from "viem";

try {
  await publicClient.simulateContract({
    address: COMET_USDC,
    abi: cometAbi,
    functionName: "withdraw",
    args: [USDC, parseUnits("50000", 6)],
    account: account.address,
  });
} catch (err) {
  if (err instanceof BaseError) {
    const revertError = err.walk(
      (e) => e instanceof ContractFunctionRevertedError
    );
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName;
      console.error(`Comet revert: ${errorName}`);
    }
  }
}
```

### Common Custom Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Absurd` | Internal math overflow | Check input amounts |
| `AlreadyInitialized` | Proxy already set up | Use existing deployment |
| `BadAsset` | Asset not configured in this Comet | Verify collateral asset address |
| `BadDecimals` | Asset decimal mismatch | Check token decimals match config |
| `BadPrice` | Price feed returned zero or negative | Wait for oracle update or check feed |
| `BorrowTooSmall` | Borrow below minimum threshold | Increase borrow amount |
| `InsufficientReserves` | Not enough protocol reserves | Wait for reserves to build up |
| `InvalidInt128` / `InvalidUInt128` | Value exceeds int128/uint128 | Reduce amount |
| `NotCollateralized` | Position would be undercollateralized | Add more collateral or reduce borrow |
| `NotForSale` | No absorbed collateral available | Wait for absorb or check asset |
| `Paused` | Market is paused by governance | Wait for unpause |
| `SupplyCapExceeded` | Collateral supply cap reached | Wait for withdrawals or use different collateral |
| `TimestampTooLarge` | Block timestamp overflow | Should not occur in practice |
| `TooMuchSlippage` | buyCollateral price moved | Increase slippage tolerance or retry |
| `TransferInFailed` | ERC-20 transferFrom failed | Check approval and balance |
| `TransferOutFailed` | ERC-20 transfer failed | Check contract has sufficient tokens |
| `Unauthorized` | Caller lacks permission | Call `allow()` first or use correct account |

## Security Best Practices

1. **Simulate before executing** — Always call `simulateContract` before `writeContract` to catch reverts without spending gas.
2. **Check `receipt.status`** — A confirmed transaction can still revert. Always verify `receipt.status === "success"`.
3. **Monitor liquidation risk** — Use `isLiquidatable()` and track collateral prices. Set alerts well before the threshold.
4. **Approve exact amounts** — Do not give Comet unlimited approval. Approve only the amount needed per transaction.
5. **Use `allow()` carefully** — Granting permission lets a manager fully control your Comet position. Only grant to audited contracts.
6. **Understand the base asset** — Know which asset is the base for each Comet. Supplying the wrong asset type changes behavior entirely.

## References

- [Compound V3 Technical Docs](https://docs.compound.finance/)
- [Comet GitHub Repository](https://github.com/compound-finance/comet)
- [Compound Governance](https://compound.finance/governance)
- [Compound V3 Deployed Addresses](https://docs.compound.finance/#networks)
- [COMP Token Distribution](https://compound.finance/governance/comp)
- [Compound Forum](https://www.comp.xyz/)
