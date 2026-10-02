---
name: aave
description: Aave V3 lending protocol integration — supply, borrow, repay, withdraw, flash loans, E-Mode, and health factor monitoring. Covers IPool interface in Solidity and viem-based TypeScript for reading protocol state, executing transactions, and managing positions across Ethereum, Arbitrum, Optimism, Base, and Polygon.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: DeFi
tags:
  - aave
  - lending
  - borrowing
  - flash-loans
  - defi
---

# Aave V3

Aave V3 is the dominant on-chain lending protocol. Users supply assets to earn yield and borrow against collateral. The protocol runs on Ethereum, Arbitrum, Optimism, Base, Polygon, and other EVM chains with identical interfaces. All interaction goes through the `IPool` contract.

## What You Probably Got Wrong

> LLMs confuse V2 and V3 constantly. V3 has different interfaces, different addresses, and different behavior. These corrections are non-negotiable.

- **V3 is not V2 — different interfaces everywhere** — V2 uses `LendingPool` with `deposit()`. V3 uses `Pool` with `supply()`. The function signatures, events, and return types differ. If you see `ILendingPool` or `deposit()`, you are writing V2 code. Stop.
- **aTokens rebase — balance changes every block** — `aToken.balanceOf(user)` increases each block as interest accrues. This is not a transfer. Do not try to track balances with Transfer events alone. Use `balanceOf()` at read time or `scaledBalanceOf()` for the underlying non-rebasing amount.
- **Stable rate borrowing is deprecated on most markets** — Aave governance disabled stable rate borrows on Ethereum mainnet and most L2 deployments. Use `VARIABLE_RATE = 2` for the `interestRateMode` parameter. Passing `STABLE_RATE = 1` will revert on markets where it is disabled.
- **Health factor is 18-decimal fixed point, not a percentage** — `getUserAccountData()` returns `healthFactor` as a `uint256` with 18 decimals. A health factor of `1e18` means liquidation threshold. Below `1e18` = liquidatable. Do not divide by 100.
- **Flash loan fee is 0.05% on V3, not 0.09%** — V3 reduced the default flash loan premium from 0.09% (V2) to 0.05%. The exact fee is configurable per market via governance. Check `FLASHLOAN_PREMIUM_TOTAL` on the Pool contract.
- **E-Mode changes collateral/borrow parameters** — Enabling E-Mode (Efficiency Mode) overrides LTV, liquidation threshold, and liquidation bonus for assets in the same category (e.g., stablecoins). It does NOT change the underlying asset. Forgetting this causes incorrect health factor calculations.
- **Supply caps exist in V3** — V3 introduced per-asset supply and borrow caps. `supply()` will revert if the cap is reached. Always check `getReserveData()` for `supplyCap` before large deposits.
- **V3 addresses are different per chain AND per market** — Ethereum has a "Main" market and a "Lido" market with completely different Pool addresses. Always verify you are targeting the correct market.

## Quick Start

### Installation

```bash
npm install @aave/aave-v3-core viem
```

For TypeScript projects, the `@aave/aave-v3-core` package provides Solidity interfaces. For frontend/backend interaction, use viem directly with the ABIs below.

### Minimal ABI Fragments

```typescript
const poolAbi = [
  {
    name: "supply",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "onBehalfOf", type: "address" },
      { name: "referralCode", type: "uint16" },
    ],
    outputs: [],
  },
  {
    name: "borrow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "interestRateMode", type: "uint256" },
      { name: "referralCode", type: "uint16" },
      { name: "onBehalfOf", type: "address" },
    ],
    outputs: [],
  },
  {
    name: "repay",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "interestRateMode", type: "uint256" },
      { name: "onBehalfOf", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "to", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "getUserAccountData",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "user", type: "address" }],
    outputs: [
      { name: "totalCollateralBase", type: "uint256" },
      { name: "totalDebtBase", type: "uint256" },
      { name: "availableBorrowsBase", type: "uint256" },
      { name: "currentLiquidationThreshold", type: "uint256" },
      { name: "ltv", type: "uint256" },
      { name: "healthFactor", type: "uint256" },
    ],
  },
  {
    name: "flashLoanSimple",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "receiverAddress", type: "address" },
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "params", type: "bytes" },
      { name: "referralCode", type: "uint16" },
    ],
    outputs: [],
  },
  {
    name: "setUserEMode",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "categoryId", type: "uint8" }],
    outputs: [],
  },
  {
    name: "getReserveData",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "asset", type: "address" }],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          { name: "configuration", type: "uint256" },
          { name: "liquidityIndex", type: "uint128" },
          { name: "currentLiquidityRate", type: "uint128" },
          { name: "variableBorrowIndex", type: "uint128" },
          { name: "currentVariableBorrowRate", type: "uint128" },
          { name: "currentStableBorrowRate", type: "uint128" },
          { name: "lastUpdateTimestamp", type: "uint40" },
          { name: "id", type: "uint16" },
          { name: "aTokenAddress", type: "address" },
          { name: "stableDebtTokenAddress", type: "address" },
          { name: "variableDebtTokenAddress", type: "address" },
          { name: "interestRateStrategyAddress", type: "address" },
          { name: "accruedToTreasury", type: "uint128" },
          { name: "unbacked", type: "uint128" },
          { name: "isolationModeTotalDebt", type: "uint128" },
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

### Basic Supply (TypeScript)

```typescript
import { createPublicClient, createWalletClient, http, parseUnits } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2" as const;
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

const amount = parseUnits("1000", 6); // 1000 USDC

// Approve Pool to spend USDC
const approveHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [POOL, amount],
});
await publicClient.waitForTransactionReceipt({ hash: approveHash });

// Supply USDC to Aave
const supplyHash = await walletClient.writeContract({
  address: POOL,
  abi: poolAbi,
  functionName: "supply",
  args: [USDC, amount, account.address, 0],
});
const receipt = await publicClient.waitForTransactionReceipt({ hash: supplyHash });

if (receipt.status !== "success") {
  throw new Error("Supply transaction reverted");
}
```

## Core Operations

### Supply (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IPool} from "@aave/aave-v3-core/contracts/interfaces/IPool.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AaveSupplier {
    IPool public immutable pool;

    constructor(address _pool) {
        pool = IPool(_pool);
    }

    /// @notice Supply asset to Aave V3 on behalf of msg.sender
    /// @param asset ERC20 token to supply
    /// @param amount Amount in token's native decimals
    function supplyToAave(address asset, uint256 amount) external {
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
        IERC20(asset).approve(address(pool), amount);
        pool.supply(asset, amount, msg.sender, 0);
    }
}
```

### Borrow (TypeScript)

```typescript
// Variable rate = 2. Stable rate (1) is deprecated on most markets.
const VARIABLE_RATE = 2n;

const borrowHash = await walletClient.writeContract({
  address: POOL,
  abi: poolAbi,
  functionName: "borrow",
  args: [USDC, parseUnits("500", 6), VARIABLE_RATE, 0, account.address],
});
const borrowReceipt = await publicClient.waitForTransactionReceipt({ hash: borrowHash });

if (borrowReceipt.status !== "success") {
  throw new Error("Borrow transaction reverted");
}
```

### Repay (TypeScript)

```typescript
const repayAmount = parseUnits("500", 6);

// Approve Pool to pull repayment
const repayApproveHash = await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [POOL, repayAmount],
});
await publicClient.waitForTransactionReceipt({ hash: repayApproveHash });

// type(uint256).max to repay entire debt
const repayHash = await walletClient.writeContract({
  address: POOL,
  abi: poolAbi,
  functionName: "repay",
  args: [USDC, repayAmount, 2n, account.address],
});
const repayReceipt = await publicClient.waitForTransactionReceipt({ hash: repayHash });

if (repayReceipt.status !== "success") {
  throw new Error("Repay transaction reverted");
}
```

### Withdraw (TypeScript)

```typescript
// type(uint256).max withdraws entire balance
const maxUint256 = 2n ** 256n - 1n;

const withdrawHash = await walletClient.writeContract({
  address: POOL,
  abi: poolAbi,
  functionName: "withdraw",
  args: [USDC, maxUint256, account.address],
});
const withdrawReceipt = await publicClient.waitForTransactionReceipt({
  hash: withdrawHash,
});

if (withdrawReceipt.status !== "success") {
  throw new Error("Withdraw transaction reverted");
}
```

### Repay and Withdraw (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IPool} from "@aave/aave-v3-core/contracts/interfaces/IPool.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AavePositionManager {
    IPool public immutable pool;

    constructor(address _pool) {
        pool = IPool(_pool);
    }

    /// @notice Repay variable-rate debt on behalf of msg.sender
    function repayDebt(address asset, uint256 amount) external {
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
        IERC20(asset).approve(address(pool), amount);
        // interestRateMode 2 = variable rate
        pool.repay(asset, amount, 2, msg.sender);
    }

    /// @notice Withdraw supplied asset back to msg.sender
    /// @param amount Use type(uint256).max to withdraw entire balance
    function withdrawFromAave(address asset, uint256 amount) external {
        pool.withdraw(asset, amount, msg.sender);
    }
}
```

## Flash Loans

V3 provides `flashLoanSimple` for single-asset flash loans (simpler interface, lower gas) and `flashLoan` for multi-asset. The fee is 0.05% by default.

### Flash Loan Receiver (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IPool} from "@aave/aave-v3-core/contracts/interfaces/IPool.sol";
import {IFlashLoanSimpleReceiver} from
    "@aave/aave-v3-core/contracts/flashloan/base/FlashLoanSimpleReceiver.sol";
import {IPoolAddressesProvider} from
    "@aave/aave-v3-core/contracts/interfaces/IPoolAddressesProvider.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract SimpleFlashLoan is IFlashLoanSimpleReceiver {
    IPoolAddressesProvider public immutable override ADDRESSES_PROVIDER;
    IPool public immutable override POOL;

    constructor(address provider) {
        ADDRESSES_PROVIDER = IPoolAddressesProvider(provider);
        POOL = IPool(IPoolAddressesProvider(provider).getPool());
    }

    /// @notice Called by Aave Pool after flash loan funds are transferred
    /// @dev Must approve Pool to pull back (amount + premium) before returning
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata /* params */
    ) external override returns (bool) {
        if (msg.sender != address(POOL)) revert("Caller not Pool");
        if (initiator != address(this)) revert("Initiator not this contract");

        // --- Custom logic here ---
        // You have `amount` of `asset` available in this contract.
        // Do arbitrage, liquidation, collateral swap, etc.

        // Repay flash loan: approve Pool to pull amount + fee
        uint256 amountOwed = amount + premium;
        IERC20(asset).approve(address(POOL), amountOwed);

        return true;
    }

    /// @notice Trigger a flash loan
    /// @param asset Token to borrow
    /// @param amount Amount to flash borrow
    function requestFlashLoan(address asset, uint256 amount) external {
        POOL.flashLoanSimple(address(this), asset, amount, "", 0);
    }
}
```

### Trigger Flash Loan (TypeScript)

```typescript
const flashLoanContractAddress = "0x...YOUR_DEPLOYED_CONTRACT..." as `0x${string}`;

const flashLoanAbi = [
  {
    name: "requestFlashLoan",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
] as const;

// Flash borrow 1M USDC
const txHash = await walletClient.writeContract({
  address: flashLoanContractAddress,
  abi: flashLoanAbi,
  functionName: "requestFlashLoan",
  args: [USDC, parseUnits("1000000", 6)],
});

const flashReceipt = await publicClient.waitForTransactionReceipt({ hash: txHash });

if (flashReceipt.status !== "success") {
  throw new Error("Flash loan reverted");
}
```

## Reading Protocol State

### Get User Account Data

```typescript
const [
  totalCollateralBase,
  totalDebtBase,
  availableBorrowsBase,
  currentLiquidationThreshold,
  ltv,
  healthFactor,
] = await publicClient.readContract({
  address: POOL,
  abi: poolAbi,
  functionName: "getUserAccountData",
  args: [account.address],
});

// All "Base" values are in USD with 8 decimals (Aave oracle base currency)
const collateralUsd = Number(totalCollateralBase) / 1e8;
const debtUsd = Number(totalDebtBase) / 1e8;

// healthFactor has 18 decimals. Below 1e18 = liquidatable.
const hf = Number(healthFactor) / 1e18;
console.log(`Health Factor: ${hf}`);
console.log(`Collateral: $${collateralUsd}, Debt: $${debtUsd}`);
```

### Get Reserve Data

```typescript
const reserveData = await publicClient.readContract({
  address: POOL,
  abi: poolAbi,
  functionName: "getReserveData",
  args: [USDC],
});

// Supply APY: currentLiquidityRate is a ray (27 decimals)
const supplyRateRay = reserveData.currentLiquidityRate;
const supplyAPY = Number(supplyRateRay) / 1e27;
console.log(`USDC Supply APY: ${(supplyAPY * 100).toFixed(2)}%`);

// aToken address for this reserve
const aTokenAddress = reserveData.aTokenAddress;
```

### Track aToken Balance

```typescript
// aToken balance includes accrued interest (rebases every block)
const aUsdcBalance = await publicClient.readContract({
  address: reserveData.aTokenAddress,
  abi: erc20Abi,
  functionName: "balanceOf",
  args: [account.address],
});

// Balance in human-readable format (USDC has 6 decimals)
const balanceFormatted = Number(aUsdcBalance) / 1e6;
console.log(`aUSDC balance: ${balanceFormatted}`);
```

## Contract Addresses

> **Last verified:** 2025-05-01

All Aave V3 deployments share the same interface. Addresses sourced from `@bgd-labs/aave-address-book` and official Aave governance.

### Pool (main entry point for all operations)

| Chain | Address |
|-------|---------|
| Ethereum | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` |
| Arbitrum | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Optimism | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Polygon  | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| Base     | `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5` |

### PoolAddressesProvider

| Chain | Address |
|-------|---------|
| Ethereum | `0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e` |
| Arbitrum | `0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb` |
| Optimism | `0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb` |
| Polygon  | `0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb` |
| Base     | `0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D` |

### Aave Oracle

| Chain | Address |
|-------|---------|
| Ethereum | `0x54586bE62E3c3580375aE3723C145253060Ca0C2` |
| Arbitrum | `0xb56c2F0B653B2e0b10C9b928C8580Ac5Df02C7C7` |
| Optimism | `0xD81eb3728a631871a7eBBaD631b5f424909f0c77` |
| Polygon  | `0xb023e699F5a33916Ea823A16485e259257cA8Bd1` |
| Base     | `0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156` |

### Common Token Addresses (Ethereum Mainnet)

| Token | Address |
|-------|---------|
| WETH  | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |
| USDC  | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| USDT  | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| DAI   | `0x6B175474E89094C44Da98b954EedeAC495271d0F` |
| WBTC  | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` |

> Verify any address before mainnet use: `cast code <address> --rpc-url $RPC_URL`

## E-Mode (Efficiency Mode)

E-Mode lets users achieve higher capital efficiency when borrowing and supplying correlated assets (e.g., stablecoins against stablecoins, ETH against stETH).

### How It Works

Each E-Mode category defines:
- **Higher LTV** (e.g., 97% for stablecoins vs 75% default)
- **Higher liquidation threshold** (e.g., 97.5%)
- **Lower liquidation bonus** (e.g., 1% vs 5%)
- **Optional oracle override** for the category

### Common E-Mode Categories

| ID | Label | Typical LTV | Use Case |
|----|-------|-------------|----------|
| 0  | None (default) | Varies per asset | General lending |
| 1  | Stablecoins | 97% | Borrow USDT against USDC |
| 2  | ETH correlated | 93% | Borrow WETH against wstETH |

> Category IDs and parameters vary by chain and market. Query on-chain.

### Enable E-Mode (TypeScript)

```typescript
// Enable stablecoin E-Mode (category 1)
const emodeHash = await walletClient.writeContract({
  address: POOL,
  abi: poolAbi,
  functionName: "setUserEMode",
  args: [1],
});
await publicClient.waitForTransactionReceipt({ hash: emodeHash });
```

### Enable E-Mode (Solidity)

```solidity
// Enable E-Mode before supplying/borrowing for higher LTV
pool.setUserEMode(1); // 1 = stablecoins category

// To disable, set back to 0
// Reverts if current position would be undercollateralized without E-Mode
pool.setUserEMode(0);
```

### E-Mode Constraint

You can only borrow assets that belong to the active E-Mode category. Supplying is unrestricted. Setting E-Mode to 0 reverts if your position would become unhealthy at default LTV/threshold.

## Error Handling

| Error Code | Name | Cause | Fix |
|------------|------|-------|-----|
| 1 | `CALLER_NOT_POOL_ADMIN` | Non-admin calling admin function | Use correct admin account |
| 26 | `COLLATERAL_CANNOT_COVER_NEW_BORROW` | Insufficient collateral for borrow | Supply more collateral or borrow less |
| 27 | `COLLATERAL_SAME_AS_BORROWING_CURRENCY` | Cannot use same asset as collateral and borrow in isolation mode | Use a different collateral |
| 28 | `AMOUNT_BIGGER_THAN_MAX_LOAN_SIZE_STABLE` | Stable rate borrow exceeds limit | Use variable rate (`interestRateMode = 2`) |
| 29 | `NO_DEBT_OF_SELECTED_TYPE` | Repaying debt type that does not exist | Check `interestRateMode` matches your debt |
| 30 | `NO_EXPLICIT_AMOUNT_TO_REPAY_ON_BEHALF` | Repaying on behalf with `type(uint256).max` | Specify exact repay amount when paying for another user |
| 35 | `HEALTH_FACTOR_LOWER_THAN_LIQUIDATION_THRESHOLD` | Action would make position liquidatable | Reduce borrow amount or add collateral |
| 36 | `INCONSISTENT_EMODE_CATEGORY` | Borrowing asset outside active E-Mode category | Switch E-Mode or borrow a compatible asset |
| 50 | `SUPPLY_CAP_EXCEEDED` | Asset supply cap reached | Wait for withdrawals or use a different market |
| 51 | `BORROW_CAP_EXCEEDED` | Asset borrow cap reached | Wait for repayments or use a different market |

> Full error code list: `contracts/protocol/libraries/helpers/Errors.sol` in aave-v3-core

### Handling Reverts in TypeScript

```typescript
import { BaseError, ContractFunctionRevertedError } from "viem";

try {
  await publicClient.simulateContract({
    address: POOL,
    abi: poolAbi,
    functionName: "borrow",
    args: [USDC, parseUnits("500", 6), 2n, 0, account.address],
    account: account.address,
  });
} catch (err) {
  if (err instanceof BaseError) {
    const revertError = err.walk(
      (e) => e instanceof ContractFunctionRevertedError
    );
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName;
      console.error(`Aave revert: ${errorName}`);
    }
  }
}
```

## Security

### Health Factor Monitoring

A health factor below 1.0 means the position is liquidatable. Third-party liquidators actively monitor the mempool. Always maintain a buffer.

```typescript
async function checkHealthFactor(
  userAddress: `0x${string}`
): Promise<{ safe: boolean; healthFactor: number }> {
  const [, , , , , healthFactor] = await publicClient.readContract({
    address: POOL,
    abi: poolAbi,
    functionName: "getUserAccountData",
    args: [userAddress],
  });

  const hf = Number(healthFactor) / 1e18;

  // 1.5 is a conservative safety buffer
  return { safe: hf > 1.5, healthFactor: hf };
}
```

### Liquidation Risk Factors

- **Oracle price movement** — If collateral price drops or debt price increases, health factor drops. Aave uses Chainlink oracles; check feed freshness.
- **Accruing interest** — Variable borrow rates compound. A 50% APY borrow accumulates debt faster than most users expect.
- **E-Mode exit** — Disabling E-Mode instantly applies lower LTV/thresholds. A safe E-Mode position may become liquidatable at default parameters.
- **Supply cap filling** — If you need to add emergency collateral and the supply cap is full, you cannot. Diversify collateral types.

### Best Practices

1. **Simulate before executing** — Always call `simulateContract` before `writeContract` to catch reverts without spending gas.
2. **Check `receipt.status`** — A confirmed transaction can still revert. Always verify `receipt.status === "success"`.
3. **Monitor health factor off-chain** — Set up alerts when HF drops below 2.0. Automate repayment or collateral addition below 1.5.
4. **Never hardcode gas limits for Aave calls** — Pool operations have variable gas costs depending on reserves touched, E-Mode state, and isolation mode. Let the node estimate.
5. **Approve exact amounts** — Avoid `type(uint256).max` approvals in production. Approve only what is needed per transaction.

## References

- [Aave V3 Technical Docs](https://docs.aave.com/developers)
- [Aave V3 Core GitHub](https://github.com/aave/aave-v3-core)
- [BGD Labs Address Book](https://github.com/bgd-labs/aave-address-book)
- [Aave V3 Error Codes](https://github.com/aave/aave-v3-core/blob/master/contracts/protocol/libraries/helpers/Errors.sol)
- [Aave Governance Forum](https://governance.aave.com)
- [Aave V3 Deployed Addresses](https://docs.aave.com/developers/deployed-contracts/v3-mainnet)
