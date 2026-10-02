---
name: uniswap
description: Uniswap V3 and V4 DEX integration — exact input/output swaps via SwapRouter02 and UniversalRouter, concentrated liquidity positions via NonfungiblePositionManager, V4 hook architecture with PoolManager singleton, pool state reads (slot0, ticks, TWAP), and Permit2 token approvals. Covers Ethereum, Arbitrum, Base, and Optimism.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - uniswap
  - dex
  - amm
  - liquidity
  - swaps
---

# Uniswap

Uniswap is the dominant on-chain DEX across Ethereum and L2s. V3 introduced concentrated liquidity — LPs allocate capital to specific price ranges instead of the full curve. V4 introduced a singleton PoolManager architecture with customizable hooks that modify pool behavior at every lifecycle point (swap, add/remove liquidity, donate).

## What You Probably Got Wrong

> AI agents trained before mid-2024 confuse V2, V3, and V4 patterns. These are the critical corrections.

- **V3 concentrated liquidity is NOT V2** — V3 positions specify a `tickLower` and `tickUpper` price range. Liquidity outside the current tick earns zero fees. There is no "full range" default. If you want full-range, you must explicitly set tickLower/tickUpper to `MIN_TICK`/`MAX_TICK` (which is capital-inefficient).
- **`sqrtPriceX96` is not a price** — V3/V4 store price as `sqrt(price) * 2^96`, a Q64.96 fixed-point number. To get the human-readable price: `(sqrtPriceX96 / 2^96)^2`. You must also adjust for token decimal differences. Getting this wrong produces prices off by orders of magnitude.
- **Tick math uses `int24`, not `uint256`** — Ticks range from -887272 to 887272. Each tick represents a 0.01% price change. Tick spacing varies by fee tier: 1 (1bp), 10 (5bp), 60 (30bp), 200 (100bp). Positions must align to tick spacing boundaries.
- **V4 is a singleton — one contract holds all pools** — Unlike V3 (one contract per pool), V4's `PoolManager` holds all pool state. Pools are identified by a `PoolKey` (currency0, currency1, fee, tickSpacing, hooks address), not by a contract address. There is no pool factory in V4.
- **V4 hooks are not optional middleware** — Hooks are smart contracts attached to a pool at creation. The hook contract address encodes which callbacks it implements via specific bit flags in the leading bytes. You cannot add or remove hooks after pool creation.
- **SwapRouter02 is the current V3 router, not SwapRouter** — The original `SwapRouter` (0xE592...) is deprecated. Use `SwapRouter02` (0x68b3...) which supports both V2 and V3 in a single interface. Even better: use `UniversalRouter` for V3+V4+Permit2 in one transaction.
- **Fee tiers are in hundredths of a basis point** — The fee parameter `3000` means 0.30%, not 30%. Common tiers: `100` (0.01%), `500` (0.05%), `3000` (0.30%), `10000` (1.00%).
- **Permit2 replaces individual token approvals** — Uniswap's UniversalRouter requires tokens to be approved to the Permit2 contract, not the router. You approve Permit2 once, then sign gasless permits per transaction.

## Quick Start

### Installation

```bash
npm install viem @uniswap/v3-sdk @uniswap/sdk-core @uniswap/universal-router-sdk
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

## Uniswap V3 Patterns

### Exact Input Single Swap (SwapRouter02)

Swap an exact amount of tokenIn for as much tokenOut as possible.

```typescript
const SWAP_ROUTER_02 = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45" as const;

const swapRouterAbi = [
  {
    name: "exactInputSingle",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "tokenIn", type: "address" },
          { name: "tokenOut", type: "address" },
          { name: "fee", type: "uint24" },
          { name: "recipient", type: "address" },
          { name: "amountIn", type: "uint256" },
          { name: "amountOutMinimum", type: "uint256" },
          { name: "sqrtPriceLimitX96", type: "uint160" },
        ],
      },
    ],
    outputs: [{ name: "amountOut", type: "uint256" }],
  },
] as const;

const WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2";
const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";

const { request } = await publicClient.simulateContract({
  address: SWAP_ROUTER_02,
  abi: swapRouterAbi,
  functionName: "exactInputSingle",
  args: [
    {
      tokenIn: WETH,
      tokenOut: USDC,
      fee: 500, // 0.05% pool — highest WETH/USDC liquidity
      recipient: account.address,
      amountIn: 1000000000000000000n, // 1 WETH
      amountOutMinimum: 0n, // SET THIS IN PRODUCTION — see Security section
      sqrtPriceLimitX96: 0n, // no price limit
    },
  ],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Swap reverted");
```

### Exact Output Single Swap

Swap as little tokenIn as necessary to receive an exact amount of tokenOut.

```typescript
const exactOutputAbi = [
  {
    name: "exactOutputSingle",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "tokenIn", type: "address" },
          { name: "tokenOut", type: "address" },
          { name: "fee", type: "uint24" },
          { name: "recipient", type: "address" },
          { name: "amountOut", type: "uint256" },
          { name: "amountInMaximum", type: "uint256" },
          { name: "sqrtPriceLimitX96", type: "uint160" },
        ],
      },
    ],
    outputs: [{ name: "amountIn", type: "uint256" }],
  },
] as const;

const { request } = await publicClient.simulateContract({
  address: SWAP_ROUTER_02,
  abi: exactOutputAbi,
  functionName: "exactOutputSingle",
  args: [
    {
      tokenIn: WETH,
      tokenOut: USDC,
      fee: 500,
      recipient: account.address,
      amountOut: 2000_000000n, // exactly 2000 USDC (6 decimals)
      amountInMaximum: 1200000000000000000n, // cap: 1.2 WETH
      sqrtPriceLimitX96: 0n,
    },
  ],
  account: account.address,
});
```

### Reading Pool State (slot0)

```typescript
const poolAbi = [
  {
    name: "slot0",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [
      { name: "sqrtPriceX96", type: "uint160" },
      { name: "tick", type: "int24" },
      { name: "observationIndex", type: "uint16" },
      { name: "observationCardinality", type: "uint16" },
      { name: "observationCardinalityNext", type: "uint16" },
      { name: "feeProtocol", type: "uint8" },
      { name: "unlocked", type: "bool" },
    ],
  },
  {
    name: "liquidity",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint128" }],
  },
] as const;

// WETH/USDC 0.05% pool
const POOL_ADDRESS = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640";

const [slot0, liquidity] = await Promise.all([
  publicClient.readContract({
    address: POOL_ADDRESS,
    abi: poolAbi,
    functionName: "slot0",
  }),
  publicClient.readContract({
    address: POOL_ADDRESS,
    abi: poolAbi,
    functionName: "liquidity",
  }),
]);

const [sqrtPriceX96, tick] = slot0;

// Convert sqrtPriceX96 to human-readable price
// price = (sqrtPriceX96 / 2^96)^2 * 10^(decimals0 - decimals1)
// WETH (18 dec) is token0, USDC (6 dec) is token1 in this pool
const price =
  (Number(sqrtPriceX96) / 2 ** 96) ** 2 * 10 ** (18 - 6);
```

### Adding Concentrated Liquidity

```typescript
const NFT_POSITION_MANAGER = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88";

const nftManagerAbi = [
  {
    name: "mint",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "token0", type: "address" },
          { name: "token1", type: "address" },
          { name: "fee", type: "uint24" },
          { name: "tickLower", type: "int24" },
          { name: "tickUpper", type: "int24" },
          { name: "amount0Desired", type: "uint256" },
          { name: "amount1Desired", type: "uint256" },
          { name: "amount0Min", type: "uint256" },
          { name: "amount1Min", type: "uint256" },
          { name: "recipient", type: "address" },
          { name: "deadline", type: "uint256" },
        ],
      },
    ],
    outputs: [
      { name: "tokenId", type: "uint256" },
      { name: "liquidity", type: "uint128" },
      { name: "amount0", type: "uint256" },
      { name: "amount1", type: "uint256" },
    ],
  },
] as const;

// Tick spacing for 0.05% fee tier is 10
// These ticks represent a ~$1500-$2500 USDC/WETH range (example)
const tickLower = -202200; // must be divisible by tickSpacing (10)
const tickUpper = -197800;

const deadline = BigInt(Math.floor(Date.now() / 1000) + 600); // 10 minutes

const { request } = await publicClient.simulateContract({
  address: NFT_POSITION_MANAGER,
  abi: nftManagerAbi,
  functionName: "mint",
  args: [
    {
      token0: WETH,
      token1: USDC,
      fee: 500,
      tickLower,
      tickUpper,
      amount0Desired: 500000000000000000n, // 0.5 WETH
      amount1Desired: 1000_000000n, // 1000 USDC
      amount0Min: 0n, // SET IN PRODUCTION
      amount1Min: 0n, // SET IN PRODUCTION
      recipient: account.address,
      deadline,
    },
  ],
  account: account.address,
});
```

### Quoting Before Swapping

Always quote before executing to calculate `amountOutMinimum` for slippage protection.

```typescript
const QUOTER_V2 = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e";

const quoterAbi = [
  {
    name: "quoteExactInputSingle",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "tokenIn", type: "address" },
          { name: "tokenOut", type: "address" },
          { name: "amountIn", type: "uint256" },
          { name: "fee", type: "uint24" },
          { name: "sqrtPriceLimitX96", type: "uint160" },
        ],
      },
    ],
    outputs: [
      { name: "amountOut", type: "uint256" },
      { name: "sqrtPriceX96After", type: "uint160" },
      { name: "initializedTicksCrossed", type: "uint32" },
      { name: "gasEstimate", type: "uint256" },
    ],
  },
] as const;

// QuoterV2 uses staticcall simulation — must use simulateContract
const { result } = await publicClient.simulateContract({
  address: QUOTER_V2,
  abi: quoterAbi,
  functionName: "quoteExactInputSingle",
  args: [
    {
      tokenIn: WETH,
      tokenOut: USDC,
      amountIn: 1000000000000000000n,
      fee: 500,
      sqrtPriceLimitX96: 0n,
    },
  ],
});

const [quotedAmountOut] = result;
// Apply 0.5% slippage tolerance
const amountOutMinimum = (quotedAmountOut * 995n) / 1000n;
```

## Uniswap V4 Patterns

V4 uses a singleton `PoolManager` that holds all pool state. Pools are created by calling `initialize` on the PoolManager. Custom hooks modify behavior at every lifecycle point.

### PoolKey Structure

Every V4 pool is identified by a `PoolKey`, not a contract address.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {PoolKey} from "v4-core/types/PoolKey.sol";
import {Currency} from "v4-core/types/Currency.sol";
import {IHooks} from "v4-core/interfaces/IHooks.sol";

// currency0 MUST be numerically less than currency1
// address(0) represents native ETH
PoolKey memory key = PoolKey({
    currency0: Currency.wrap(address(0)),          // ETH
    currency1: Currency.wrap(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48), // USDC
    fee: 3000,        // 0.30% — same encoding as V3
    tickSpacing: 60,  // must match fee tier conventions
    hooks: IHooks(address(0)) // no hooks
});
```

### Initializing a V4 Pool

```solidity
import {IPoolManager} from "v4-core/interfaces/IPoolManager.sol";
import {TickMath} from "v4-core/libraries/TickMath.sol";

IPoolManager poolManager = IPoolManager(POOL_MANAGER_ADDRESS);

// sqrtPriceX96 for initial price — same Q64.96 format as V3
uint160 startingPrice = TickMath.getSqrtPriceAtTick(0); // price ratio = 1:1

poolManager.initialize(key, startingPrice);
```

### Writing a V4 Hook

Hooks implement callbacks that fire at specific pool lifecycle events. The hook address must encode which callbacks are active via flag bits in the address prefix.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {BaseHook} from "v4-periphery/src/utils/BaseHook.sol";
import {Hooks} from "v4-core/libraries/Hooks.sol";
import {IPoolManager} from "v4-core/interfaces/IPoolManager.sol";
import {PoolKey} from "v4-core/types/PoolKey.sol";
import {BalanceDelta} from "v4-core/types/BalanceDelta.sol";
import {BeforeSwapDelta, BeforeSwapDeltaLibrary} from "v4-core/types/BeforeSwapDelta.sol";

contract SwapFeeHook is BaseHook {
    constructor(IPoolManager _poolManager) BaseHook(_poolManager) {}

    function getHookPermissions()
        public
        pure
        override
        returns (Hooks.Permissions memory)
    {
        return Hooks.Permissions({
            beforeInitialize: false,
            afterInitialize: false,
            beforeAddLiquidity: false,
            afterAddLiquidity: false,
            beforeRemoveLiquidity: false,
            afterRemoveLiquidity: false,
            beforeSwap: true,           // enabled
            afterSwap: true,            // enabled
            beforeDonate: false,
            afterDonate: false,
            beforeSwapReturnDelta: false,
            afterSwapReturnDelta: false,
            afterAddLiquidityReturnDelta: false,
            afterRemoveLiquidityReturnDelta: false
        });
    }

    function beforeSwap(
        address sender,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        bytes calldata hookData
    ) external override returns (bytes4, BeforeSwapDelta, uint24) {
        // Custom logic: logging, dynamic fees, access control, etc.
        return (
            BaseHook.beforeSwap.selector,
            BeforeSwapDeltaLibrary.ZERO_DELTA,
            0
        );
    }

    function afterSwap(
        address sender,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        BalanceDelta delta,
        bytes calldata hookData
    ) external override returns (bytes4, int128) {
        // Post-swap logic: fee collection, rebalancing, analytics
        return (BaseHook.afterSwap.selector, 0);
    }
}
```

### Hook Lifecycle Callbacks

| Callback | Fires When | Use Cases |
|----------|-----------|-----------|
| `beforeInitialize` | Pool created | Whitelist checks, parameter validation |
| `afterInitialize` | Pool created (after) | Oracle setup, initial state |
| `beforeAddLiquidity` | LP deposits | KYC gates, deposit caps |
| `afterAddLiquidity` | LP deposits (after) | Receipt tokens, accounting |
| `beforeRemoveLiquidity` | LP withdraws | Lockup enforcement, cooldowns |
| `afterRemoveLiquidity` | LP withdraws (after) | Cleanup, fee distribution |
| `beforeSwap` | Trade executes | Dynamic fees, circuit breakers, MEV protection |
| `afterSwap` | Trade executes (after) | Fee sharing, oracle updates, rebalancing |
| `beforeDonate` | Donation to pool | Access control |
| `afterDonate` | Donation (after) | Accounting |

### V4 Hook Address Mining

The hook address must have specific bits set to match the enabled callbacks. Use `CREATE2` with a salt to mine a valid address.

```solidity
import {HookMiner} from "v4-periphery/test/utils/HookMiner.sol";

// Compute the flags from your permissions
uint160 flags = uint160(Hooks.BEFORE_SWAP_FLAG | Hooks.AFTER_SWAP_FLAG);

// Mine a salt that produces an address with the correct prefix
(address hookAddress, bytes32 salt) = HookMiner.find(
    CREATE2_DEPLOYER,
    flags,
    type(SwapFeeHook).creationCode,
    abi.encode(address(poolManager))
);
```

## Contract Addresses

> **Last verified:** February 2026

### Uniswap V3

| Contract | Ethereum | Arbitrum | Base | Optimism |
|----------|----------|----------|------|----------|
| Factory | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | `0x33128a8fC17869897dcE68Ed026d694621f6FDfD` | `0x1F98431c8aD98523631AE4a59f267346ea31F984` |
| SwapRouter02 | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` | `0x2626664c2603336E57B271c5C0b26F421741e481` | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` |
| NonfungiblePositionManager | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | `0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1` | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` |
| QuoterV2 | `0x61fFE014bA17989E743c5F6cB21bF9697530B21e` | `0x61fFE014bA17989E743c5F6cB21bF9697530B21e` | `0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a` | `0x61fFE014bA17989E743c5F6cB21bF9697530B21e` |
| UniversalRouter | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` | `0x5E325eDA8064b456f4781070C0738d849c824258` | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` | `0xCb1355ff08Ab38bBCE60111F1bb2B784bE25D7e8` |

### Uniswap V4

| Contract | Ethereum |
|----------|----------|
| PoolManager | `0x000000000004444c5dc75cB358380D2e3dE08A90` |
| Permit2 | `0x000000000022D473030F116dDEE9F6B43aC78BA3` |

### Common Token Addresses (Ethereum)

| Token | Address |
|-------|---------|
| WETH | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` |
| USDC | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` |
| USDT | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| DAI | `0x6B175474E89094C44Da98b954EedeAC495271d0F` |
| WBTC | `0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599` |

## Common Patterns

### Multi-Hop Swap (V3)

Route through multiple pools when no direct pool exists or for better pricing.

```typescript
import { encodePacked } from "viem";

const multiHopAbi = [
  {
    name: "exactInput",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "path", type: "bytes" },
          { name: "recipient", type: "address" },
          { name: "amountIn", type: "uint256" },
          { name: "amountOutMinimum", type: "uint256" },
        ],
      },
    ],
    outputs: [{ name: "amountOut", type: "uint256" }],
  },
] as const;

// Path encoding: token0 + fee + token1 + fee + token2
// WBTC -> (0.05%) WETH -> (0.05%) USDC
const WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599";

const path = encodePacked(
  ["address", "uint24", "address", "uint24", "address"],
  [WBTC, 500, WETH, 500, USDC]
);

const { request } = await publicClient.simulateContract({
  address: SWAP_ROUTER_02,
  abi: multiHopAbi,
  functionName: "exactInput",
  args: [
    {
      path,
      recipient: account.address,
      amountIn: 10000000n, // 0.1 WBTC (8 decimals)
      amountOutMinimum: 0n, // SET IN PRODUCTION
    },
  ],
  account: account.address,
});
```

### TWAP Observation (V3)

Read time-weighted average price from the pool's built-in oracle.

```typescript
const observeAbi = [
  {
    name: "observe",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "secondsAgos", type: "uint32[]" }],
    outputs: [
      { name: "tickCumulatives", type: "int56[]" },
      { name: "secondsPerLiquidityCumulativeX128s", type: "uint160[]" },
    ],
  },
] as const;

// 30-minute TWAP
const [tickCumulatives] = await publicClient.readContract({
  address: POOL_ADDRESS,
  abi: observeAbi,
  functionName: "observe",
  args: [[1800, 0]], // [30 min ago, now]
});

const twapTick =
  Number(tickCumulatives[1] - tickCumulatives[0]) / 1800;
// Convert tick to price: price = 1.0001^tick
const twapPrice = 1.0001 ** twapTick;
```

### Permit2 Approval Flow

UniversalRouter requires Permit2 approvals instead of direct token approvals.

```typescript
const PERMIT2 = "0x000000000022D473030F116dDEE9F6B43aC78BA3";

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

// Step 1: Approve Permit2 to spend your tokens (one-time, max approval)
const { request: approveRequest } = await publicClient.simulateContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [PERMIT2, 2n ** 160n - 1n], // max uint160 — Permit2's allowance cap
  account: account.address,
});
await walletClient.writeContract(approveRequest);

// Step 2: For each swap, sign a Permit2 message (gasless)
// The UniversalRouter SDK handles Permit2 signature construction
// See @uniswap/universal-router-sdk for full integration
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `STF` (SafeTransferFrom) | Token transfer failed — insufficient balance or missing approval | Check balance with `balanceOf`, ensure `approve` to router or Permit2 |
| `TF` (Transfer Failed) | Output token transfer to recipient failed | Verify recipient is not a contract that rejects transfers |
| `SPL` (sqrtPriceLimitX96) | Swap would push price past the limit | Set `sqrtPriceLimitX96` to 0 to remove limit, or widen the bound |
| `LOK` (Locked) | Pool reentrancy guard triggered | Do not call the pool from within a callback |
| `AS` (Already Started) | V4 pool already initialized | Check if pool exists before calling `initialize` |
| `TLU` (tickLower >= tickUpper) | Invalid tick range | Ensure `tickLower < tickUpper` and both are divisible by `tickSpacing` |
| `TLM` (Tick Lower Minimum) | tickLower below MIN_TICK (-887272) | Use a higher tickLower |
| `TUM` (Tick Upper Maximum) | tickUpper above MAX_TICK (887272) | Use a lower tickUpper |
| `Transaction too old` | Deadline passed before tx was mined | Increase deadline or use a more generous timestamp |

## Security

### Slippage Protection (Non-Negotiable)

Never set `amountOutMinimum` to 0 in production. Always quote first, then apply a tolerance.

```typescript
// Quote the expected output
const { result } = await publicClient.simulateContract({
  address: QUOTER_V2,
  abi: quoterAbi,
  functionName: "quoteExactInputSingle",
  args: [{ tokenIn: WETH, tokenOut: USDC, amountIn, fee: 500, sqrtPriceLimitX96: 0n }],
});

const [expectedOut] = result;
// 50 basis points (0.5%) slippage tolerance
const slippageBps = 50n;
const amountOutMinimum = expectedOut - (expectedOut * slippageBps) / 10000n;
```

### Deadline Parameter

Always set a deadline on liquidity operations. Prevents transactions from sitting in the mempool and executing at unfavorable prices hours later.

```typescript
const deadline = BigInt(Math.floor(Date.now() / 1000) + 300); // 5 minutes
```

### Front-Running Mitigation

- Use `amountOutMinimum` with tight slippage on every swap
- Set `sqrtPriceLimitX96` to bound maximum price impact
- Use Flashbots Protect RPC (`https://rpc.flashbots.net`) to submit transactions privately on mainnet
- For large swaps, split into smaller chunks or use TWAP execution

### Permit2 Security

- Approve Permit2 for `type(uint160).max`, not `type(uint256).max` — Permit2 caps allowances at uint160
- Permit2 signatures include a deadline and nonce — always verify both
- Revoke Permit2 allowances for contracts you no longer use via `permit2.approve(token, spender, 0, 0)`

## References

- [Uniswap V3 Docs](https://docs.uniswap.org/contracts/v3/overview)
- [Uniswap V4 Docs](https://docs.uniswap.org/contracts/v4/overview)
- [V3 Contract Addresses](https://docs.uniswap.org/contracts/v3/reference/deployments)
- [V4 GitHub (v4-core)](https://github.com/Uniswap/v4-core)
- [V4 Periphery (hooks, routers)](https://github.com/Uniswap/v4-periphery)
- [Permit2 GitHub](https://github.com/Uniswap/permit2)
- [Universal Router SDK](https://github.com/Uniswap/universal-router-sdk)
- [@uniswap/v3-sdk](https://github.com/Uniswap/v3-sdk)
- [Uniswap V3 Whitepaper](https://uniswap.org/whitepaper-v3.pdf)
