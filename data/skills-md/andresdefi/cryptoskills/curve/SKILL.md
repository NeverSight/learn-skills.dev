---
name: curve
description: Curve Finance AMM — StableSwap pools for pegged assets, CryptoSwap (Tricrypto) for volatile pairs, crvUSD stablecoin with LLAMMA soft-liquidation, gauge voting for CRV emissions, factory pools, and LP token staking. Covers pool interfaces (exchange, add_liquidity, remove_liquidity), Router for optimal routing, and gauge system across Ethereum mainnet.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - curve
  - amm
  - stableswap
  - crvusd
  - defi
  - liquidity
---

# Curve Finance

Curve is the dominant AMM for pegged-asset swaps (stablecoins, wrapped tokens, LSTs). Its StableSwap invariant concentrates liquidity around peg, delivering 10-100x lower slippage than constant-product AMMs for like-kind assets. CryptoSwap (Tricrypto) extends this to volatile pairs. The protocol also issues crvUSD, a stablecoin backed by LLAMMA — a soft-liquidation mechanism that gradually converts collateral instead of instant liquidation. CRV emissions are directed to liquidity gauges via vote-escrowed CRV (veCRV).

All Curve pool contracts are written in Vyper. ABI encoding is identical to Solidity — viem works without modification.

## What You Probably Got Wrong

> Curve is one of the most commonly mis-integrated protocols. Each pool type has different interfaces, and token ordering is deployment-specific.

- **Curve pools have DIFFERENT ABIs per pool type** — StableSwap (2-pool, 3-pool), CryptoSwap, Tricrypto, Meta pools, and Factory pools all have different function signatures. There is NO universal pool ABI. Always read the specific pool's ABI from Etherscan or the Curve docs.
- **Token indices are pool-specific and NOT sorted** — The order depends on deployment, not address sorting. Always call `coins(i)` to verify which token is at which index. Getting this wrong swaps the wrong token.
- **`exchange()` uses token indices, not addresses** — You pass `i` (sell token index) and `j` (buy token index), not token addresses. Passing the wrong index silently swaps the wrong token pair.
- **`get_dy()` returns the estimated output BEFORE fees** — The actual received amount is slightly less. Use `get_dy()` for quoting but apply slippage tolerance on top.
- **`add_liquidity()` amounts array length varies per pool** — 2 for 2-pool, 3 for 3-pool, 4 for 4-pool. Passing the wrong array length causes a revert with no useful error message.
- **`exchange()` vs `exchange_underlying()`** — Plain pools use `exchange()`. Meta pools use `exchange_underlying()` to swap between the meta-asset and the underlying basepool tokens. Calling the wrong function reverts.
- **crvUSD uses LLAMMA (soft liquidation), NOT traditional liquidation** — Positions are gradually converted between collateral and crvUSD as price moves through bands. There is no instant liquidation threshold. Health approaching 0 means bands are fully converted.
- **Gauge voting requires veCRV (vote-escrowed CRV)** — Lock CRV for 1-4 years to get voting power. Voting power decays linearly. You cannot transfer or sell veCRV.
- **`remove_liquidity_one_coin()` has high slippage for large withdrawals from imbalanced pools** — The StableSwap invariant penalizes imbalanced withdrawals. Always simulate first.
- **Virtual price only goes up (monotonic)** — `get_virtual_price()` returns the LP token value in underlying. It increases from fees and never decreases. Useful for pricing LP positions but NOT for detecting exploits (it was manipulated in some reentrancy attacks on Vyper <0.3.1 pools).

## Quick Start

### Installation

```bash
npm install viem
```

### Client Setup

```typescript
import { createPublicClient, createWalletClient, http, type Address } from "viem";
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

### Swap USDC to USDT on 3pool

```typescript
const THREE_POOL = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7" as const;

// 3pool indices: 0 = DAI, 1 = USDC, 2 = USDT
// Always verify with coins(i) before swapping
const threePoolAbi = [
  {
    name: "exchange",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "i", type: "int128" },
      { name: "j", type: "int128" },
      { name: "dx", type: "uint256" },
      { name: "min_dy", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "get_dy",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "i", type: "int128" },
      { name: "j", type: "int128" },
      { name: "dx", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "coins",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "i", type: "uint256" }],
    outputs: [{ name: "", type: "address" }],
  },
] as const;

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as const;
const USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7" as const;

const amountIn = 10_000_000000n; // 10,000 USDC (6 decimals)

// Verify token indices
const coin1 = await publicClient.readContract({
  address: THREE_POOL,
  abi: threePoolAbi,
  functionName: "coins",
  args: [1n],
});
if (coin1.toLowerCase() !== USDC.toLowerCase()) {
  throw new Error(`Expected USDC at index 1, got ${coin1}`);
}

// Quote expected output
const expectedOut = await publicClient.readContract({
  address: THREE_POOL,
  abi: threePoolAbi,
  functionName: "get_dy",
  args: [1n, 2n, amountIn], // i=1 (USDC) -> j=2 (USDT)
});

// 0.1% slippage tolerance (stableswap pools have tight spreads)
const minDy = (expectedOut * 999n) / 1000n;

// Approve 3pool to spend USDC
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

const { request: approveRequest } = await publicClient.simulateContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [THREE_POOL, amountIn],
  account: account.address,
});
const approveHash = await walletClient.writeContract(approveRequest);
await publicClient.waitForTransactionReceipt({ hash: approveHash });

// Execute swap
const { request } = await publicClient.simulateContract({
  address: THREE_POOL,
  abi: threePoolAbi,
  functionName: "exchange",
  args: [1n, 2n, amountIn, minDy],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Swap reverted");
```

## Pool Types

### StableSwap Pools (Pegged Assets)

The original Curve pool type. Optimized for assets that trade near 1:1 (stablecoins, wrapped tokens). Uses the StableSwap invariant which blends constant-sum and constant-product formulas, controlled by the amplification parameter `A`.

| Pool | Address | Coins | Indices |
|------|---------|-------|---------|
| 3pool | `0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7` | DAI, USDC, USDT | 0, 1, 2 |
| stETH/ETH | `0xDC24316b9AE028F1497c275EB9192a3Ea0f67022` | ETH, stETH | 0, 1 |
| frxETH/ETH | `0xa1F8A6807c402E4A15ef4EBa36528A3FED24E577` | ETH, frxETH | 0, 1 |

Key parameters:
- **A (amplification)** — Higher A means tighter peg. 3pool uses A=2000. Ranges from 1 (constant product) to ~5000.
- **Fee** — Typically 0.01%-0.04% for stableswap pools. Read via `fee()` (returns value in 1e10 precision, so `4000000` = 0.04%).

### CryptoSwap Pools (Volatile Pairs)

Two-token pools for non-pegged assets using the CryptoSwap invariant. Internally re-pegs around the current price, providing concentrated liquidity that auto-rebalances.

| Pool | Address | Coins |
|------|---------|-------|
| tricrypto2 | `0xD51a44d3FaE010294C616388b506AcdA1bfAAE46` | USDT, WBTC, WETH |

### Meta Pools

Pools that pair a single token against an existing basepool's LP token. For example, FRAX/3CRV pairs FRAX against the 3pool LP token, giving FRAX access to DAI/USDC/USDT liquidity.

```typescript
// Meta pool: exchange_underlying() swaps between the meta-asset
// and any token in the basepool
const metaPoolAbi = [
  {
    name: "exchange_underlying",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "i", type: "int128" },
      { name: "j", type: "int128" },
      { name: "dx", type: "uint256" },
      { name: "min_dy", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// LUSD/3CRV meta pool
// Underlying indices: 0 = LUSD, 1 = DAI, 2 = USDC, 3 = USDT
// exchange_underlying(0, 2, amount, minOut) swaps LUSD -> USDC
```

### Factory Pools

User-deployed pools created through the Curve Factory. They follow the same interface as their pool type (StableSwap or CryptoSwap) but are created permissionlessly.

```typescript
const CURVE_FACTORY = "0xB9fC157394Af804a3578134A6585C0dc9cc990d4" as const;

const factoryAbi = [
  {
    name: "pool_count",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "pool_list",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "i", type: "uint256" }],
    outputs: [{ name: "", type: "address" }],
  },
] as const;

const poolCount = await publicClient.readContract({
  address: CURVE_FACTORY,
  abi: factoryAbi,
  functionName: "pool_count",
});
```

## Swapping

### Basic Exchange (StableSwap)

All StableSwap pools use `exchange(i, j, dx, min_dy)` where `i` and `j` are token indices.

```typescript
// Older pools (like 3pool) use int128 for indices
const stableSwapExchangeAbi = [
  {
    name: "exchange",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "i", type: "int128" },
      { name: "j", type: "int128" },
      { name: "dx", type: "uint256" },
      { name: "min_dy", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Newer factory pools may use uint256 for indices
const factoryExchangeAbi = [
  {
    name: "exchange",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "i", type: "uint256" },
      { name: "j", type: "uint256" },
      { name: "dx", type: "uint256" },
      { name: "min_dy", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;
```

### Exchange with ETH

ETH pools (stETH/ETH, frxETH/ETH) accept native ETH via `msg.value`. Pass ETH as value, not as an ERC-20 approval.

```typescript
const STETH_POOL = "0xDC24316b9AE028F1497c275EB9192a3Ea0f67022" as const;

// stETH/ETH pool: 0 = ETH, 1 = stETH
const ethPoolExchangeAbi = [
  {
    name: "exchange",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "i", type: "int128" },
      { name: "j", type: "int128" },
      { name: "dx", type: "uint256" },
      { name: "min_dy", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const ethAmount = 1_000_000_000_000_000_000n; // 1 ETH

const expectedSteth = await publicClient.readContract({
  address: STETH_POOL,
  abi: threePoolAbi, // get_dy has same signature
  functionName: "get_dy",
  args: [0n, 1n, ethAmount],
});

const minSteth = (expectedSteth * 999n) / 1000n;

const { request } = await publicClient.simulateContract({
  address: STETH_POOL,
  abi: ethPoolExchangeAbi,
  functionName: "exchange",
  args: [0n, 1n, ethAmount, minSteth],
  value: ethAmount, // send ETH with the call
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Swap reverted");
```

### Curve Router

For optimal routing across multiple pools, use the Curve Router. It finds the best path automatically.

```typescript
const CURVE_ROUTER = "0xF0d4c12A5768D806021F80a262B4d39d26C58b8D" as const;

const routerAbi = [
  {
    name: "exchange",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_route", type: "address[11]" },
      { name: "_swap_params", type: "uint256[5][5]" },
      { name: "_amount", type: "uint256" },
      { name: "_min_dy", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "get_dy",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "_route", type: "address[11]" },
      { name: "_swap_params", type: "uint256[5][5]" },
      { name: "_amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Route encoding: alternating [token, pool, token, pool, ..., token]
// padded with zero addresses to length 11
// swap_params[i] = [i, j, swap_type, pool_type, n_coins]
// swap_type: 1 = exchange, 2 = exchange_underlying, 3 = exchange on underlying
// pool_type: 1 = stableswap, 2 = cryptoswap, 3 = tricrypto
```

## Liquidity

### Add Liquidity (Balanced)

Provide all tokens proportionally to minimize slippage.

```typescript
const addLiquidityAbi = [
  {
    name: "add_liquidity",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "amounts", type: "uint256[3]" },
      { name: "min_mint_amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "calc_token_amount",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "amounts", type: "uint256[3]" },
      { name: "is_deposit", type: "bool" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Deposit 1000 of each stablecoin into 3pool
const amounts: readonly [bigint, bigint, bigint] = [
  1000_000000000000000000n, // 1000 DAI  (18 decimals)
  1000_000000n,             // 1000 USDC (6 decimals)
  1000_000000n,             // 1000 USDT (6 decimals)
];

// Estimate LP tokens received
const expectedLp = await publicClient.readContract({
  address: THREE_POOL,
  abi: addLiquidityAbi,
  functionName: "calc_token_amount",
  args: [amounts, true],
});

// 0.5% slippage on LP token mint
const minMintAmount = (expectedLp * 995n) / 1000n;

// Approve all three tokens to the pool
// (omitted for brevity — same pattern as swap approval)

const { request } = await publicClient.simulateContract({
  address: THREE_POOL,
  abi: addLiquidityAbi,
  functionName: "add_liquidity",
  args: [amounts, minMintAmount],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Add liquidity reverted");
```

### Add Liquidity (Single-Sided)

Deposit only one token. The pool rebalances internally, charging a small imbalance fee.

```typescript
// Deposit 5000 USDC only into 3pool
const singleSidedAmounts: readonly [bigint, bigint, bigint] = [
  0n,           // 0 DAI
  5000_000000n, // 5000 USDC
  0n,           // 0 USDT
];

const expectedLp = await publicClient.readContract({
  address: THREE_POOL,
  abi: addLiquidityAbi,
  functionName: "calc_token_amount",
  args: [singleSidedAmounts, true],
});

// Wider slippage for single-sided (imbalance fee applies)
const minMintAmount = (expectedLp * 990n) / 1000n;

const { request } = await publicClient.simulateContract({
  address: THREE_POOL,
  abi: addLiquidityAbi,
  functionName: "add_liquidity",
  args: [singleSidedAmounts, minMintAmount],
  account: account.address,
});
```

### Remove Liquidity (Proportional)

Withdraw all tokens proportionally — no slippage from imbalance.

```typescript
const removeLiquidityAbi = [
  {
    name: "remove_liquidity",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_amount", type: "uint256" },
      { name: "min_amounts", type: "uint256[3]" },
    ],
    outputs: [{ name: "", type: "uint256[3]" }],
  },
] as const;

const lpAmount = 3000_000000000000000000n; // 3000 LP tokens

const { request } = await publicClient.simulateContract({
  address: THREE_POOL,
  abi: removeLiquidityAbi,
  functionName: "remove_liquidity",
  args: [lpAmount, [0n, 0n, 0n]], // SET MIN AMOUNTS IN PRODUCTION
  account: account.address,
});
```

### Remove Liquidity (Single Coin)

Withdraw everything as a single token. Higher slippage for large amounts or imbalanced pools.

```typescript
const removeOneCoinAbi = [
  {
    name: "remove_liquidity_one_coin",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_token_amount", type: "uint256" },
      { name: "i", type: "int128" },
      { name: "_min_amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "calc_withdraw_one_coin",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "_token_amount", type: "uint256" },
      { name: "i", type: "int128" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const lpToWithdraw = 1000_000000000000000000n; // 1000 LP tokens

// Estimate how much USDC we get
const expectedUsdc = await publicClient.readContract({
  address: THREE_POOL,
  abi: removeOneCoinAbi,
  functionName: "calc_withdraw_one_coin",
  args: [lpToWithdraw, 1n], // index 1 = USDC
});

const minUsdc = (expectedUsdc * 995n) / 1000n;

const { request } = await publicClient.simulateContract({
  address: THREE_POOL,
  abi: removeOneCoinAbi,
  functionName: "remove_liquidity_one_coin",
  args: [lpToWithdraw, 1n, minUsdc],
  account: account.address,
});
```

### Remove Liquidity (Imbalanced)

Withdraw specific amounts of each token.

```typescript
const removeImbalanceAbi = [
  {
    name: "remove_liquidity_imbalance",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "amounts", type: "uint256[3]" },
      { name: "max_burn_amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Withdraw exactly 500 DAI and 500 USDC, no USDT
const withdrawAmounts: readonly [bigint, bigint, bigint] = [
  500_000000000000000000n, // 500 DAI
  500_000000n,             // 500 USDC
  0n,                      // 0 USDT
];

// Estimate LP tokens burned
const estimatedBurn = await publicClient.readContract({
  address: THREE_POOL,
  abi: addLiquidityAbi,
  functionName: "calc_token_amount",
  args: [withdrawAmounts, false], // false = withdrawal
});

// Allow 1% more LP burn than estimated
const maxBurnAmount = (estimatedBurn * 1010n) / 1000n;

const { request } = await publicClient.simulateContract({
  address: THREE_POOL,
  abi: removeImbalanceAbi,
  functionName: "remove_liquidity_imbalance",
  args: [withdrawAmounts, maxBurnAmount],
  account: account.address,
});
```

## crvUSD (LLAMMA)

crvUSD is Curve's stablecoin. Loans are backed by collateral deposited into LLAMMA (Lending-Liquidating AMM Algorithm). Instead of instant liquidation at a threshold, LLAMMA gradually converts collateral to crvUSD as the collateral price drops through user-defined bands. If the price recovers, it converts back.

### Create a crvUSD Loan

```typescript
// crvUSD Controller for WETH collateral
const CRVUSD_WETH_CONTROLLER = "0xA920De414eA4Ab66b97dA1bFE9e6EcA7d4219635" as const;

const controllerAbi = [
  {
    name: "create_loan",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "collateral", type: "uint256" },
      { name: "debt", type: "uint256" },
      { name: "N", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "max_borrowable",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "collateral", type: "uint256" },
      { name: "N", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "health",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "user", type: "address" },
    ],
    outputs: [{ name: "", type: "int256" }],
  },
  {
    name: "user_state",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "user", type: "address" },
    ],
    outputs: [
      { name: "collateral", type: "uint256" },
      { name: "stablecoin", type: "uint256" },
      { name: "debt", type: "uint256" },
      { name: "N", type: "uint256" },
    ],
  },
] as const;

const WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as const;
const collateralAmount = 10_000000000000000000n; // 10 WETH

// N = number of bands (4-50). More bands = wider liquidation range = safer but lower LTV
const numBands = 10n;

// Check max borrowable amount
const maxDebt = await publicClient.readContract({
  address: CRVUSD_WETH_CONTROLLER,
  abi: controllerAbi,
  functionName: "max_borrowable",
  args: [collateralAmount, numBands],
});

// Borrow 80% of max for safety margin
const debtAmount = (maxDebt * 80n) / 100n;

// Approve WETH to controller
const { request: approveReq } = await publicClient.simulateContract({
  address: WETH,
  abi: erc20Abi,
  functionName: "approve",
  args: [CRVUSD_WETH_CONTROLLER, collateralAmount],
  account: account.address,
});
await walletClient.writeContract(approveReq);

// Create loan
const { request } = await publicClient.simulateContract({
  address: CRVUSD_WETH_CONTROLLER,
  abi: controllerAbi,
  functionName: "create_loan",
  args: [collateralAmount, debtAmount, numBands],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Loan creation reverted");
```

### Monitor Loan Health

```typescript
// Health > 0 means position is safe
// Health approaching 0 means bands are being converted (soft liquidation)
// Health < 0 means position can be hard-liquidated
const health = await publicClient.readContract({
  address: CRVUSD_WETH_CONTROLLER,
  abi: controllerAbi,
  functionName: "health",
  args: [account.address],
});

// Health is returned in 1e18 precision
// health = 100e18 means 100% above liquidation
const healthPercent = Number(health) / 1e18;

if (healthPercent < 10) {
  console.warn(`Low health: ${healthPercent.toFixed(2)}% — consider repaying or adding collateral`);
}

// Read full user state
const [collateral, stablecoin, debt, bands] = await publicClient.readContract({
  address: CRVUSD_WETH_CONTROLLER,
  abi: controllerAbi,
  functionName: "user_state",
  args: [account.address],
});
```

### Repay crvUSD Loan

```typescript
const repayAbi = [
  {
    name: "repay",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_d_debt", type: "uint256" },
    ],
    outputs: [],
  },
] as const;

const CRVUSD = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E" as const;

const repayAmount = 5000_000000000000000000n; // repay 5000 crvUSD

// Approve crvUSD to controller
const { request: approveReq } = await publicClient.simulateContract({
  address: CRVUSD,
  abi: erc20Abi,
  functionName: "approve",
  args: [CRVUSD_WETH_CONTROLLER, repayAmount],
  account: account.address,
});
await walletClient.writeContract(approveReq);

const { request } = await publicClient.simulateContract({
  address: CRVUSD_WETH_CONTROLLER,
  abi: repayAbi,
  functionName: "repay",
  args: [repayAmount],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Repay reverted");
```

## Gauge System

Curve directs CRV emissions to liquidity providers via gauges. Deposit your LP tokens into a gauge to earn CRV rewards. Boost your rewards up to 2.5x by holding veCRV.

### Deposit LP Tokens into Gauge

```typescript
// 3pool gauge
const THREE_POOL_GAUGE = "0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A" as const;
const THREE_POOL_LP = "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490" as const;

const gaugeAbi = [
  {
    name: "deposit",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "_value", type: "uint256" }],
    outputs: [],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "_value", type: "uint256" }],
    outputs: [],
  },
  {
    name: "claimable_tokens",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "addr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const lpAmount = 1000_000000000000000000n; // 1000 LP tokens

// Approve gauge to spend LP tokens
const { request: approveReq } = await publicClient.simulateContract({
  address: THREE_POOL_LP,
  abi: erc20Abi,
  functionName: "approve",
  args: [THREE_POOL_GAUGE, lpAmount],
  account: account.address,
});
await walletClient.writeContract(approveReq);

// Deposit into gauge
const { request } = await publicClient.simulateContract({
  address: THREE_POOL_GAUGE,
  abi: gaugeAbi,
  functionName: "deposit",
  args: [lpAmount],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Gauge deposit reverted");
```

### Claim CRV Rewards

```typescript
const MINTER = "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0" as const;

const minterAbi = [
  {
    name: "mint",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "gauge_addr", type: "address" }],
    outputs: [],
  },
] as const;

// Check claimable amount
const claimable = await publicClient.simulateContract({
  address: THREE_POOL_GAUGE,
  abi: gaugeAbi,
  functionName: "claimable_tokens",
  args: [account.address],
});

// Mint (claim) CRV rewards
const { request } = await publicClient.simulateContract({
  address: MINTER,
  abi: minterAbi,
  functionName: "mint",
  args: [THREE_POOL_GAUGE],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("CRV claim reverted");
```

## Gauge Voting

### Lock CRV for veCRV

Lock CRV tokens to receive vote-escrowed CRV (veCRV). Longer lock = more voting power. Lock duration: 1 week to 4 years. Voting power decays linearly toward the unlock date.

```typescript
const CRV = "0xD533a949740bb3306d119CC777fa900bA034cd52" as const;
const VECRV = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2" as const;

const veCrvAbi = [
  {
    name: "create_lock",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_value", type: "uint256" },
      { name: "_unlock_time", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "increase_amount",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "_value", type: "uint256" }],
    outputs: [],
  },
  {
    name: "increase_unlock_time",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "_unlock_time", type: "uint256" }],
    outputs: [],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [],
    outputs: [],
  },
] as const;

const lockAmount = 10000_000000000000000000n; // 10,000 CRV

// Lock for 4 years (max voting power)
// unlock_time must be rounded down to the nearest week (Thursday 00:00 UTC)
const WEEK = 7n * 24n * 60n * 60n;
const FOUR_YEARS = 4n * 365n * 24n * 60n * 60n;
const now = BigInt(Math.floor(Date.now() / 1000));
const unlockTime = ((now + FOUR_YEARS) / WEEK) * WEEK;

// Approve CRV to veCRV
const { request: approveReq } = await publicClient.simulateContract({
  address: CRV,
  abi: erc20Abi,
  functionName: "approve",
  args: [VECRV, lockAmount],
  account: account.address,
});
await walletClient.writeContract(approveReq);

// Create lock
const { request } = await publicClient.simulateContract({
  address: VECRV,
  abi: veCrvAbi,
  functionName: "create_lock",
  args: [lockAmount, unlockTime],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("veCRV lock reverted");
```

### Vote on Gauge Weights

Direct CRV emissions to specific gauges. Votes persist until changed. Each veCRV holder gets 10,000 vote points (100%) to allocate across gauges.

```typescript
const GAUGE_CONTROLLER = "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB" as const;

const gaugeControllerAbi = [
  {
    name: "vote_for_gauge_weights",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_gauge_addr", type: "address" },
      { name: "_user_weight", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "gauge_relative_weight",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "addr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "vote_user_power",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "user", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Allocate 50% of voting power to 3pool gauge
// Weight is in basis points: 5000 = 50%
const { request } = await publicClient.simulateContract({
  address: GAUGE_CONTROLLER,
  abi: gaugeControllerAbi,
  functionName: "vote_for_gauge_weights",
  args: [THREE_POOL_GAUGE, 5000n],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Gauge vote reverted");
```

### Check Voting Power Usage

```typescript
// Returns total weight used out of 10000 (100%)
const usedPower = await publicClient.readContract({
  address: GAUGE_CONTROLLER,
  abi: gaugeControllerAbi,
  functionName: "vote_user_power",
  args: [account.address],
});

const remainingBps = 10000n - usedPower;
```

## Pool Discovery

### MetaRegistry

The MetaRegistry aggregates all pool registries (main, factory, crypto factory) into a single interface.

```typescript
const META_REGISTRY = "0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC" as const;

const metaRegistryAbi = [
  {
    name: "find_pool_for_coins",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "_from", type: "address" },
      { name: "_to", type: "address" },
    ],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "find_pools_for_coins",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "_from", type: "address" },
      { name: "_to", type: "address" },
    ],
    outputs: [{ name: "", type: "address[]" }],
  },
  {
    name: "get_coins",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "_pool", type: "address" }],
    outputs: [{ name: "", type: "address[8]" }],
  },
  {
    name: "get_balances",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "_pool", type: "address" }],
    outputs: [{ name: "", type: "uint256[8]" }],
  },
] as const;

// Find the best pool for USDC -> USDT
const pool = await publicClient.readContract({
  address: META_REGISTRY,
  abi: metaRegistryAbi,
  functionName: "find_pool_for_coins",
  args: [USDC, USDT],
});

// Find ALL pools for a pair
const pools = await publicClient.readContract({
  address: META_REGISTRY,
  abi: metaRegistryAbi,
  functionName: "find_pools_for_coins",
  args: [USDC, USDT],
});
```

## Reading Pool State

### Virtual Price

Virtual price represents the LP token value in terms of the underlying asset. It only increases over time from trading fees.

```typescript
const poolStateAbi = [
  {
    name: "get_virtual_price",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "balances",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "i", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "A",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "fee",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// Virtual price is 1e18 precision
const virtualPrice = await publicClient.readContract({
  address: THREE_POOL,
  abi: poolStateAbi,
  functionName: "get_virtual_price",
});

// LP token value in USD (assuming underlying = $1)
const lpValueUsd = Number(virtualPrice) / 1e18;

// Pool balances per coin index
const [daiBalance, usdcBalance, usdtBalance] = await Promise.all([
  publicClient.readContract({ address: THREE_POOL, abi: poolStateAbi, functionName: "balances", args: [0n] }),
  publicClient.readContract({ address: THREE_POOL, abi: poolStateAbi, functionName: "balances", args: [1n] }),
  publicClient.readContract({ address: THREE_POOL, abi: poolStateAbi, functionName: "balances", args: [2n] }),
]);

// Amplification parameter
const amplification = await publicClient.readContract({
  address: THREE_POOL,
  abi: poolStateAbi,
  functionName: "A",
});

// Fee in 1e10 precision (4000000 = 0.04%)
const poolFee = await publicClient.readContract({
  address: THREE_POOL,
  abi: poolStateAbi,
  functionName: "fee",
});
const feePercent = Number(poolFee) / 1e10 * 100;
```

## Contract Addresses

> **Last verified:** February 2026

See [resources/contract-addresses.md](resources/contract-addresses.md) for the full address table.

| Contract | Ethereum |
|----------|----------|
| 3pool | `0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7` |
| stETH/ETH | `0xDC24316b9AE028F1497c275EB9192a3Ea0f67022` |
| Tricrypto2 | `0xD51a44d3FaE010294C616388b506AcdA1bfAAE46` |
| CRV Token | `0xD533a949740bb3306d119CC777fa900bA034cd52` |
| veCRV | `0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2` |
| Curve Router | `0xF0d4c12A5768D806021F80a262B4d39d26C58b8D` |
| MetaRegistry | `0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC` |
| crvUSD | `0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E` |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Exchange resulted in fewer coins than expected` | Output below `min_dy` | Increase slippage tolerance or re-quote |
| `Exceeds allowance` | Pool not approved to spend token | Call `approve()` with sufficient amount |
| `Insufficient funds` | Balance below swap amount | Check `balanceOf` before calling exchange |
| Empty revert (Vyper) | Wrong function signature or invalid index | Verify ABI matches pool type, check coin indices |
| `dev: exceeds allowance` | Vyper dev error for allowance check | Approve token to the correct pool address |
| `Lock expired` | Trying to increase amount on expired veCRV lock | Withdraw first, then create new lock |
| `Withdraw old tokens first` | Creating veCRV lock when one already exists | Call `withdraw()` on expired lock first |

## Security

### Slippage Protection

Never set `min_dy` to 0 in production. Always quote with `get_dy()` first.

```typescript
const expectedOut = await publicClient.readContract({
  address: poolAddress,
  abi: threePoolAbi,
  functionName: "get_dy",
  args: [i, j, amountIn],
});

// For stableswap: 10-50 bps is reasonable
const minDy = (expectedOut * 9990n) / 10000n; // 10 bps

// For cryptoswap/volatile: 50-200 bps
const minDyCrypto = (expectedOut * 9950n) / 10000n; // 50 bps
```

### USDT Approval Reset

USDT requires setting allowance to 0 before setting a new non-zero value.

```typescript
async function approveUsdt(spender: Address, amount: bigint): Promise<void> {
  const currentAllowance = await publicClient.readContract({
    address: USDT,
    abi: erc20Abi,
    functionName: "allowance",
    args: [account.address, spender],
  });

  if (currentAllowance > 0n && currentAllowance < amount) {
    const { request: resetReq } = await publicClient.simulateContract({
      address: USDT,
      abi: erc20Abi,
      functionName: "approve",
      args: [spender, 0n],
      account: account.address,
    });
    const resetHash = await walletClient.writeContract(resetReq);
    await publicClient.waitForTransactionReceipt({ hash: resetHash });
  }

  const { request } = await publicClient.simulateContract({
    address: USDT,
    abi: erc20Abi,
    functionName: "approve",
    args: [spender, amount],
    account: account.address,
  });
  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("USDT approval failed");
}
```

### Front-Running Mitigation

- Use tight `min_dy` on every swap (quote + slippage)
- Use [Flashbots Protect RPC](https://rpc.flashbots.net) for mainnet transactions
- Large liquidity operations should use proportional add/remove to minimize extractable value
- For large single-sided deposits, split into multiple smaller transactions

## References

- [Curve Technical Docs](https://docs.curve.fi)
- [Curve StableSwap Whitepaper](https://classic.curve.fi/files/stableswap-paper.pdf)
- [Curve CryptoSwap Whitepaper](https://classic.curve.fi/files/crypto-pools-paper.pdf)
- [crvUSD Whitepaper](https://github.com/curvefi/curve-stablecoin/blob/master/doc/curve-stablecoin.pdf)
- [Curve Contract Registry](https://github.com/curvefi/curve-contract)
- [Curve Factory](https://github.com/curvefi/curve-factory)
- [Curve Router Source](https://github.com/curvefi/curve-router-ng)
- [Curve Addresses (Official)](https://docs.curve.fi/references/deployed-contracts/)
