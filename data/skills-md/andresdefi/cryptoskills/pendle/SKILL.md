---
name: pendle
description: Pendle yield tokenization protocol — split yield-bearing assets into PT (Principal Token) and YT (Yield Token), trade fixed and variable yield on Pendle AMM, SY (Standardized Yield) token wrapping, and market operations. Covers Pendle Router, market math, and yield strategy patterns across Ethereum and Arbitrum.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - pendle
  - yield
  - fixed-rate
  - defi
  - tokenization
  - pt
  - yt
---

# Pendle

Pendle is a yield tokenization protocol that splits yield-bearing assets into two components: PT (Principal Token) and YT (Yield Token). PT represents the principal redeemable at maturity, while YT represents the right to all yield generated until maturity. Both trade on Pendle's custom AMM, enabling users to lock in fixed yields (buy PT at a discount) or take leveraged yield exposure (buy YT). All yield-bearing tokens are first wrapped into SY (Standardized Yield), Pendle's unified yield interface.

## What You Probably Got Wrong

> AI models confuse Pendle's token mechanics with traditional bonds and perpetual yield tokens. These corrections are critical.

- **PT is NOT a bond** -- PT is a claim on the underlying asset at maturity. Before maturity, PT trades at a discount to the underlying. The discount implies a fixed rate, but PT does not pay coupons. At maturity, 1 PT redeems for 1 unit of the underlying asset (e.g., 1 PT-stETH redeems for 1 stETH worth of value).
- **YT is NOT a perpetual yield token** -- YT expires at market maturity. After expiry, YT has zero market value. All yield accrued by YT is claimable separately. If you hold YT past maturity, you get nothing more -- the yield was already distributed. YT does not entitle you to yield after its maturity date.
- **SY (Standardized Yield) is NOT optional** -- Every yield-bearing token must be wrapped as SY before minting PT/YT. SY is Pendle's ERC-5115 adapter that normalizes the yield interface across protocols (stETH, aUSDC, GLP, eETH, etc.). You cannot mint PT/YT directly from the underlying without going through SY.
- **PT + YT = SY always holds (before maturity)** -- This is the core invariant. 1 SY can be split into 1 PT + 1 YT, and 1 PT + 1 YT can be merged back into 1 SY. Arbitrageurs enforce this peg. If PT + YT < SY, buy PT+YT and redeem for SY. If PT + YT > SY, mint PT+YT from SY and sell.
- **Implied APY is NOT guaranteed APY** -- The implied APY you see on Pendle's UI is derived from the current PT discount relative to the underlying. It reflects the market's pricing of future yield at this moment. It changes every block as trades move the PT/SY ratio in the AMM.
- **Post-maturity PT redeems 1:1 for underlying** -- But before maturity, PT price < underlying because of time value. The gap narrows as maturity approaches (PT price converges to underlying). This is NOT a depeg; it is by design.
- **Pendle AMM uses a custom curve, NOT Uniswap-style x*y=k** -- Pendle v2 AMM is optimized for PT/SY trading. It uses a Notional-inspired logit curve with a time-decay parameter that compresses the curve as maturity approaches, naturally converging PT price toward SY.
- **Market has an expiry** -- After the maturity date, the AMM stops accepting new swaps. LPs must withdraw liquidity. You can still redeem PT for underlying and claim accrued YT yield after market expiry. Plan LP exits before maturity.
- **Router is the entrypoint** -- Never interact with PendleMarket, SY, PT, or YT contracts directly for complex operations. Use `PendleRouter` for all swaps, mints, redeems, and liquidity operations. The Router handles multi-step operations atomically (e.g., token -> SY -> PT in one tx).
- **Slippage on Pendle is in exchange rate, not price** -- When swapping on Pendle, slippage protection uses `minTokenOut` or a `guessPtOut` struct with `guessMin`/`guessMax` bounds. The Router's binary search finds the optimal swap amount within these bounds. Setting the guess range too tight causes reverts; too wide wastes gas.

## Quick Start

### Installation

```bash
npm install viem @pendle/sdk-v2
```

### Read Implied APY from a Market

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const PENDLE_MARKET = "0xD0354D4e7bCf345fB117cabe41aCaDb724009CE5" as const;

const marketAbi = parseAbi([
  "function readState(address router) view returns (int256 totalPt, int256 totalSy, int256 totalLp, address treasury, int256 scalarRoot, int256 expiry, int256 lnFeeRateRoot, uint256 reserveFeePercent, int256 lastLnImpliedRate)",
  "function expiry() view returns (uint256)",
]);

const marketState = await publicClient.readContract({
  address: PENDLE_MARKET,
  abi: marketAbi,
  functionName: "readState",
  args: ["0x888888888889758F76e7103c6CbF23ABbF58F946"],
});

// lastLnImpliedRate is ln(1 + impliedRate) scaled by 1e18
// To get implied APY: e^(lastLnImpliedRate / 1e18) - 1
const lnRate = Number(marketState[8]) / 1e18;
const impliedApy = Math.exp(lnRate) - 1;
console.log(`Implied APY: ${(impliedApy * 100).toFixed(2)}%`);
```

## Core Concepts

### SY (Standardized Yield) — ERC-5115

SY wraps any yield-bearing token into a standard interface. It exposes `deposit()` and `redeem()` for converting between the underlying yield-bearing asset and SY tokens. The SY contract tracks the exchange rate between itself and the underlying.

Key properties:
- SY balance represents a claim on the underlying yield-bearing asset
- Exchange rate between SY and underlying increases over time as yield accrues
- Every Pendle market is built on a specific SY token

### PT (Principal Token)

PT represents the principal component of a yield-bearing asset. It entitles the holder to redeem 1 unit of the underlying at maturity.

Key properties:
- Trades at a discount before maturity (discount = implied fixed rate)
- Price converges to 1:1 with underlying as maturity approaches
- After maturity, redeemable 1:1 for the underlying via `redeemPyToSy`

### YT (Yield Token)

YT represents the yield component. Holding YT entitles you to all yield generated by the underlying from now until maturity.

Key properties:
- Value decreases as maturity approaches (time decay)
- At maturity, YT value = 0 (all yield already distributed)
- Yield accrues in real-time and is claimable via `redeemDueInterestAndRewards`
- Provides leveraged yield exposure (pay YT price << underlying, receive full yield)

### Market

A Pendle Market is an AMM pool that trades PT against SY. YT is traded synthetically through PT (since PT + YT = SY, selling PT is equivalent to buying YT).

### Oracle

Pendle markets have a built-in TWAP oracle for the PT/SY implied rate. DeFi protocols use this to price PT as collateral. The oracle must be initialized with a desired observation window before first use.

## SY (Standardized Yield)

### Wrap Underlying to SY

```typescript
const PENDLE_ROUTER = "0x888888888889758F76e7103c6CbF23ABbF58F946" as const;

const routerAbi = parseAbi([
  "function mintSyFromToken(address receiver, address SY, uint256 minSyOut, (address tokenIn, uint256 netTokenIn, address tokenMintSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) input) payable returns (uint256 netSyOut)",
  "function redeemSyToToken(address receiver, address SY, uint256 netSyIn, (address tokenOut, uint256 minTokenOut, address tokenRedeemSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) output) returns (uint256 netTokenOut)",
]);

// Mint SY from WETH (for SY-wstETH market)
const WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as const;
const SY_WSTETH = "0xcbC72d92b2dc8187414F6734718563898740C0BC" as const;

const mintAmount = 1_000_000_000_000_000_000n; // 1 WETH

const tokenInput = {
  tokenIn: WETH,
  netTokenIn: mintAmount,
  tokenMintSy: WETH,
  pendleSwap: "0x0000000000000000000000000000000000000000" as const,
  swapData: {
    swapType: 0,
    extRouter: "0x0000000000000000000000000000000000000000" as const,
    extCalldata: "0x" as `0x${string}`,
    needScale: false,
  },
};

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: routerAbi,
  functionName: "mintSyFromToken",
  args: [account.address, SY_WSTETH, 0n, tokenInput],
  account: account.address,
  value: mintAmount,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("mintSyFromToken reverted");
```

### Redeem SY to Underlying

```typescript
const netSyIn = 950_000_000_000_000_000n; // SY amount to redeem

const tokenOutput = {
  tokenOut: WETH,
  minTokenOut: 0n, // SET IN PRODUCTION — use oracle rate with slippage
  tokenRedeemSy: WETH,
  pendleSwap: "0x0000000000000000000000000000000000000000" as const,
  swapData: {
    swapType: 0,
    extRouter: "0x0000000000000000000000000000000000000000" as const,
    extCalldata: "0x" as `0x${string}`,
    needScale: false,
  },
};

const { request: redeemRequest } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: routerAbi,
  functionName: "redeemSyToToken",
  args: [account.address, SY_WSTETH, netSyIn, tokenOutput],
  account: account.address,
});

const redeemHash = await walletClient.writeContract(redeemRequest);
const redeemReceipt = await publicClient.waitForTransactionReceipt({ hash: redeemHash });
if (redeemReceipt.status !== "success") throw new Error("redeemSyToToken reverted");
```

## Minting PT/YT

Minting PT and YT from SY splits the yield-bearing position into its principal and yield components. 1 SY produces 1 PT + 1 YT.

### Mint PT + YT from SY

```typescript
const mintPyAbi = parseAbi([
  "function mintPyFromSy(address receiver, address YT, uint256 netSyIn, uint256 minPyOut) returns (uint256 netPyOut)",
]);

const YT_WSTETH = "0x7B6C3e5486D9e6959441ab554A889099ead23c1F" as const;
const netSyToMint = 1_000_000_000_000_000_000n; // 1 SY

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: mintPyAbi,
  functionName: "mintPyFromSy",
  args: [
    account.address,
    YT_WSTETH,
    netSyToMint,
    0n, // minPyOut — SET IN PRODUCTION
  ],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("mintPyFromSy reverted");
```

### Mint PT + YT Directly from Token (One-Step)

The Router can handle token -> SY -> PT+YT in a single transaction.

```typescript
const mintPyFromTokenAbi = parseAbi([
  "function mintPyFromToken(address receiver, address YT, uint256 minPyOut, (address tokenIn, uint256 netTokenIn, address tokenMintSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) input) payable returns (uint256 netPyOut)",
]);

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: mintPyFromTokenAbi,
  functionName: "mintPyFromToken",
  args: [
    account.address,
    YT_WSTETH,
    0n, // minPyOut — SET IN PRODUCTION
    tokenInput,
  ],
  account: account.address,
  value: mintAmount,
});
```

### Redeem PT + YT back to SY

```typescript
const redeemPyAbi = parseAbi([
  "function redeemPyToSy(address receiver, address YT, uint256 netPyIn, uint256 minSyOut) returns (uint256 netSyOut)",
]);

const netPyIn = 1_000_000_000_000_000_000n;

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: redeemPyAbi,
  functionName: "redeemPyToSy",
  args: [
    account.address,
    YT_WSTETH,
    netPyIn,
    0n, // minSyOut — SET IN PRODUCTION
  ],
  account: account.address,
});
```

## Trading on Pendle AMM

### Buy PT (Lock in Fixed Yield)

Buying PT at a discount locks in a fixed yield. If implied APY is 5% and maturity is 1 year away, buying PT gives you ~5% guaranteed return at maturity (assuming the underlying asset redeems 1:1).

```typescript
const swapAbi = parseAbi([
  "function swapExactTokenForPt(address receiver, address market, uint256 minPtOut, (uint256 guessMin, uint256 guessMax, uint256 guessOffchain, uint256 maxIteration, uint256 eps) guessPtOut, (address tokenIn, uint256 netTokenIn, address tokenMintSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) input) payable returns (uint256 netPtOut, uint256 netSyFee)",
  "function swapExactPtForToken(address receiver, address market, uint256 exactPtIn, (address tokenOut, uint256 minTokenOut, address tokenRedeemSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) output) returns (uint256 netTokenOut, uint256 netSyFee)",
]);

const guessPtOut = {
  guessMin: 0n,
  guessMax: 2_000_000_000_000_000_000n, // upper bound for binary search
  guessOffchain: 0n, // 0 = let Router compute; or pass SDK-computed optimal
  maxIteration: 256n,
  // 1e15 = 0.1% precision — lower eps = more iterations but tighter result
  eps: 1_000_000_000_000_000n,
};

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: swapAbi,
  functionName: "swapExactTokenForPt",
  args: [
    account.address,
    PENDLE_MARKET,
    0n, // minPtOut — SET IN PRODUCTION
    guessPtOut,
    tokenInput,
  ],
  account: account.address,
  value: mintAmount,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("swapExactTokenForPt reverted");
```

### Sell PT for Token

```typescript
const PT_WSTETH = "0xB253A3370B1Db752D65b890B1fE093A26C398bDE" as const;
const exactPtIn = 1_000_000_000_000_000_000n;

const tokenOutput = {
  tokenOut: WETH,
  minTokenOut: 0n, // SET IN PRODUCTION
  tokenRedeemSy: WETH,
  pendleSwap: "0x0000000000000000000000000000000000000000" as const,
  swapData: {
    swapType: 0,
    extRouter: "0x0000000000000000000000000000000000000000" as const,
    extCalldata: "0x" as `0x${string}`,
    needScale: false,
  },
};

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: swapAbi,
  functionName: "swapExactPtForToken",
  args: [
    account.address,
    PENDLE_MARKET,
    exactPtIn,
    tokenOutput,
  ],
  account: account.address,
});
```

### Buy YT (Leveraged Yield Exposure)

YT is traded synthetically. Buying YT is economically equivalent to minting PT+YT from SY and selling PT. The Router handles this atomically.

```typescript
const swapYtAbi = parseAbi([
  "function swapExactTokenForYt(address receiver, address market, uint256 minYtOut, (uint256 guessMin, uint256 guessMax, uint256 guessOffchain, uint256 maxIteration, uint256 eps) guessYtOut, (address tokenIn, uint256 netTokenIn, address tokenMintSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) input) payable returns (uint256 netYtOut, uint256 netSyFee)",
  "function swapExactYtForToken(address receiver, address market, uint256 exactYtIn, (address tokenOut, uint256 minTokenOut, address tokenRedeemSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) output) returns (uint256 netTokenOut, uint256 netSyFee)",
]);

const guessYtOut = {
  guessMin: 0n,
  guessMax: 10_000_000_000_000_000_000n,
  guessOffchain: 0n,
  maxIteration: 256n,
  eps: 1_000_000_000_000_000n,
};

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: swapYtAbi,
  functionName: "swapExactTokenForYt",
  args: [
    account.address,
    PENDLE_MARKET,
    0n, // minYtOut — SET IN PRODUCTION
    guessYtOut,
    tokenInput,
  ],
  account: account.address,
  value: mintAmount,
});
```

## Liquidity Provision

Pendle LPs provide PT + SY liquidity to the AMM. LP rewards include:
1. Swap fees from PT/SY trading
2. The underlying yield from the SY component
3. PENDLE incentive emissions (on incentivized markets)

### Add Liquidity with Single Token

```typescript
const lpAbi = parseAbi([
  "function addLiquiditySingleToken(address receiver, address market, uint256 minLpOut, (uint256 guessMin, uint256 guessMax, uint256 guessOffchain, uint256 maxIteration, uint256 eps) guessPtReceivedFromSy, (address tokenIn, uint256 netTokenIn, address tokenMintSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) input) payable returns (uint256 netLpOut, uint256 netSyFee)",
  "function removeLiquiditySingleToken(address receiver, address market, uint256 netLpIn, (address tokenOut, uint256 minTokenOut, address tokenRedeemSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) output) returns (uint256 netTokenOut, uint256 netSyFee)",
]);

const guessPtReceivedFromSy = {
  guessMin: 0n,
  guessMax: 1_000_000_000_000_000_000n,
  guessOffchain: 0n,
  maxIteration: 256n,
  eps: 1_000_000_000_000_000n,
};

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: lpAbi,
  functionName: "addLiquiditySingleToken",
  args: [
    account.address,
    PENDLE_MARKET,
    0n, // minLpOut — SET IN PRODUCTION
    guessPtReceivedFromSy,
    tokenInput,
  ],
  account: account.address,
  value: mintAmount,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("addLiquiditySingleToken reverted");
```

### Remove Liquidity to Single Token

```typescript
const netLpIn = 500_000_000_000_000_000n; // LP tokens to withdraw

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: lpAbi,
  functionName: "removeLiquiditySingleToken",
  args: [
    account.address,
    PENDLE_MARKET,
    netLpIn,
    tokenOutput,
  ],
  account: account.address,
});
```

### Impermanent Loss Profile

Pendle LP impermanent loss is different from standard AMM IL:
- Before maturity: IL comes from PT price moving relative to SY. If implied rates move significantly, LPs experience IL.
- At maturity: PT converges to SY value. The time-decay parameter compresses the AMM curve, reducing IL as maturity approaches.
- Post-maturity: No more IL since the AMM is inactive.

The closer to maturity you provide liquidity, the lower your IL risk, but also the fewer fees you earn.

## Fixed Rate Strategies

### Strategy 1: Buy PT for Fixed Yield

The simplest fixed-yield strategy. Buy PT at a discount, hold to maturity, redeem 1:1.

Example: PT-stETH trading at 0.95 stETH with 6 months to maturity.
- You pay 0.95 stETH equivalent
- At maturity, redeem for 1 stETH equivalent
- Fixed return: ~10.5% annualized (0.05/0.95 * 2)

Risk: The underlying protocol (e.g., Lido) must remain solvent. PT does NOT guarantee the underlying asset's value.

### Strategy 2: Buy YT for Leveraged Yield

Buy YT to get leveraged exposure to variable yield.

Example: YT-stETH at 0.05 stETH equivalent, stETH yielding 4% APY.
- For 0.05 stETH, you receive yield on 1 full stETH until maturity
- Leverage: ~20x yield exposure
- Break-even: If average yield > implied rate, you profit

Risk: If actual yield < implied rate, you lose money. YT value decays to zero at maturity regardless.

### Strategy 3: LP for Enhanced Yield

Provide liquidity to earn swap fees + SY yield + PENDLE emissions.

- Best entered when implied rates are stable (low volatility)
- Avoid entering right before major rate-changing events
- Exit before maturity to avoid forced withdrawal at suboptimal prices

## Reading Market State

### Get Implied Rate, Exchange Rate, and Reserves

```typescript
const PENDLE_ROUTER_STATIC = "0x263833d47eA3fA4a30d59B2E6C1A0e682eF1C078" as const;

const routerStaticAbi = parseAbi([
  "function getMarketState(address market) view returns (address pt, address sy, address yt, int256 impliedYield, uint256 exchangeRate, uint256 totalPt, uint256 totalSy, uint256 totalLp)",
]);

const oracleAbi = parseAbi([
  "function getPtToAssetRate(address market, uint32 duration) view returns (uint256)",
  "function getYtToAssetRate(address market, uint32 duration) view returns (uint256)",
  "function getPtToSyRate(address market, uint32 duration) view returns (uint256)",
]);

const PENDLE_PT_ORACLE = "0x66a1096C6366b2529274dF4f5D8f56DA60a2CacD" as const;

// PT/Asset TWAP rate (e.g., for collateral pricing)
// Duration in seconds — must match initialized observation window
const ptToAssetRate = await publicClient.readContract({
  address: PENDLE_PT_ORACLE,
  abi: oracleAbi,
  functionName: "getPtToAssetRate",
  args: [PENDLE_MARKET, 900], // 15-minute TWAP
});

// Rate is scaled to 1e18. A value of 0.95e18 means 1 PT = 0.95 underlying
console.log(`PT/Asset rate: ${Number(ptToAssetRate) / 1e18}`);
```

### Initialize Oracle (Required Before First Use)

```typescript
const marketOracleAbi = parseAbi([
  "function increaseObservationsCardinalityNext(uint16 cardinalityNext) external",
  "function observe(uint32[] secondsAgos) view returns (uint216[] lnImpliedRateCumulatives)",
]);

// Must be called on the market contract itself, not the oracle
// Cardinality determines how far back the TWAP can look
// For a 15-minute TWAP, you need enough observations to cover 900 seconds
const { request } = await publicClient.simulateContract({
  address: PENDLE_MARKET,
  abi: marketOracleAbi,
  functionName: "increaseObservationsCardinalityNext",
  args: [100], // 100 observation slots
  account: account.address,
});
```

### Read Market Expiry

```typescript
const expiry = await publicClient.readContract({
  address: PENDLE_MARKET,
  abi: marketAbi,
  functionName: "expiry",
});

const expiryDate = new Date(Number(expiry) * 1000);
const isExpired = Date.now() > Number(expiry) * 1000;
console.log(`Market expiry: ${expiryDate.toISOString()}`);
console.log(`Expired: ${isExpired}`);
```

## Maturity & Redemption

### Redeem PT After Maturity

After maturity, PT redeems 1:1 for the underlying. The redemption path is: PT -> SY -> underlying token.

```typescript
const redeemAfterMaturityAbi = parseAbi([
  "function redeemPyToToken(address receiver, address YT, uint256 netPyIn, (address tokenOut, uint256 minTokenOut, address tokenRedeemSy, address pendleSwap, (uint8 swapType, address extRouter, bytes extCalldata, bool needScale) swapData) output) returns (uint256 netTokenOut)",
]);

// After maturity, you only need PT (YT is worthless). Pass equal PT amount.
// If you don't have matching YT, use redeemPyToSy which handles post-maturity redemption
const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: redeemAfterMaturityAbi,
  functionName: "redeemPyToToken",
  args: [
    account.address,
    YT_WSTETH,
    exactPtIn,
    tokenOutput,
  ],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Redemption reverted");
```

### Claim Accrued YT Yield

YT yield accrues in real-time. Claim it at any point (before or after maturity).

```typescript
const claimAbi = parseAbi([
  "function redeemDueInterestAndRewards(address user, address[] SYs, address[] PTs, address[] YTs, address[] markets) returns (uint256[][] netSyOut, uint256[][] netRewardOut)",
]);

const { request } = await publicClient.simulateContract({
  address: PENDLE_ROUTER,
  abi: claimAbi,
  functionName: "redeemDueInterestAndRewards",
  args: [
    account.address,
    [SY_WSTETH],
    [PT_WSTETH],
    [YT_WSTETH],
    [PENDLE_MARKET],
  ],
  account: account.address,
});

const hash = await walletClient.writeContract(request);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
if (receipt.status !== "success") throw new Error("Claim reverted");
```

### Post-Expiry Behavior

| Action | Before Maturity | After Maturity |
|--------|----------------|----------------|
| Trade PT on AMM | Yes | No (AMM inactive) |
| Trade YT on AMM | Yes (synthetic) | No |
| Redeem PT for underlying | No (must sell on AMM) | Yes (1:1 via Router) |
| Claim YT yield | Yes (accrued so far) | Yes (all remaining) |
| LP withdrawal | Yes | Yes (mandatory) |
| Mint PT+YT from SY | Yes | No |

## Contract Addresses

> **Last verified:** February 2026

### Ethereum Mainnet

| Contract | Address |
|----------|---------|
| PendleRouter | `0x888888888889758F76e7103c6CbF23ABbF58F946` |
| PendleRouterStatic | `0x263833d47eA3fA4a30d59B2E6C1A0e682eF1C078` |
| PendleMarketFactoryV3 | `0x1A6fCc85557BC4fB7B534ed835a03EF056c222E2` |
| PendlePtOracle | `0x66a1096C6366b2529274dF4f5D8f56DA60a2CacD` |
| vePENDLE | `0x4f30A9D41B80ecC5B94306AB4364951AE3170210` |
| PENDLE token | `0x808507121B80c02388fAd14726482e061B8da827` |

### Arbitrum

| Contract | Address |
|----------|---------|
| PendleRouter | `0x888888888889758F76e7103c6CbF23ABbF58F946` |
| PendleRouterStatic | `0x263833d47eA3fA4a30d59B2E6C1A0e682eF1C078` |
| PendleMarketFactoryV3 | `0x2FCb47B58350cD377f94d3821e7373Df60bD9Ced` |
| PendlePtOracle | `0x66a1096C6366b2529274dF4f5D8f56DA60a2CacD` |
| PENDLE token | `0x0c880f6761F1af8d9Aa9C466984b80DAb9a8c9e8` |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `MarketExpired()` | Attempting to trade on a market past maturity | Check `market.expiry()` before trading. Use redeem functions post-maturity |
| `RouterInsufficientPtOut()` | PT received is below `minPtOut` | Increase slippage tolerance or re-quote with fresh market state |
| `RouterInsufficientSyOut()` | SY received is below `minSyOut` | Widen slippage. Check if the underlying rate changed significantly |
| `RouterInsufficientYtOut()` | YT received is below `minYtOut` | Re-quote. YT pricing is more volatile near maturity |
| `RouterInsufficientLpOut()` | LP tokens received below `minLpOut` | Re-compute expected LP amount with current reserves |
| `ApproxFail()` | Binary search for optimal swap amount failed | Widen `guessMin`/`guessMax` range, increase `maxIteration`, or decrease `eps` |
| `MarketProportionTooHigh()` | Trade would consume too much of the pool's reserves | Reduce trade size or split into multiple transactions |
| `SYInvalidTokenIn()` | Token passed is not a valid input for this SY contract | Check `SY.getTokensIn()` for valid deposit tokens |
| `SYInvalidTokenOut()` | Token passed is not a valid output for this SY contract | Check `SY.getTokensOut()` for valid redemption tokens |

## Security

### Slippage Protection

Never set `minPtOut`, `minSyOut`, `minYtOut`, or `minLpOut` to 0 in production. Always compute expected output first and apply a slippage tolerance.

```typescript
// Use PendleRouterStatic to preview expected output
const previewAbi = parseAbi([
  "function swapExactTokenForPtStatic(address market, address tokenIn, uint256 netTokenIn) view returns (uint256 netPtOut, uint256 netSyFee, uint256 priceImpact)",
]);

const [expectedPtOut] = await publicClient.readContract({
  address: PENDLE_ROUTER_STATIC,
  abi: previewAbi,
  functionName: "swapExactTokenForPtStatic",
  args: [PENDLE_MARKET, WETH, mintAmount],
});

// 1% slippage tolerance for Pendle (higher than standard DEX due to binary search)
const slippageBps = 100n;
const minPtOut = expectedPtOut - (expectedPtOut * slippageBps) / 10000n;
```

### Oracle Integration for Lending Protocols

When using PT as collateral, always use the TWAP oracle with a sufficient observation window. Instantaneous rates are manipulable.

```typescript
// Initialize oracle with enough cardinality BEFORE relying on it
// Wait for the observation window to fill before using the TWAP
// 15-minute minimum recommended for lending protocols

// WRONG: Instantaneous rate (manipulable in same tx)
// const rate = await market.readState(router);

// CORRECT: TWAP from dedicated oracle
const rate = await publicClient.readContract({
  address: PENDLE_PT_ORACLE,
  abi: oracleAbi,
  functionName: "getPtToAssetRate",
  args: [PENDLE_MARKET, 900], // 15-minute TWAP
});
```

### Approval Pattern

Approve the Router for SY, PT, and YT tokens. The Router handles all multi-step operations.

```typescript
const erc20Abi = parseAbi([
  "function approve(address spender, uint256 amount) returns (bool)",
]);

// Approve Router to spend SY, PT, and YT
for (const token of [SY_WSTETH, PT_WSTETH, YT_WSTETH]) {
  const { request } = await publicClient.simulateContract({
    address: token,
    abi: erc20Abi,
    functionName: "approve",
    args: [PENDLE_ROUTER, 2n ** 256n - 1n],
    account: account.address,
  });
  const hash = await walletClient.writeContract(request);
  await publicClient.waitForTransactionReceipt({ hash });
}
```

## References

- [Pendle Docs](https://docs.pendle.finance)
- [Pendle V2 Contracts (GitHub)](https://github.com/pendle-finance/pendle-core-v2-public)
- [Pendle SDK](https://github.com/pendle-finance/pendle-sdk-core-v2-public)
- [ERC-5115 (Standardized Yield)](https://eips.ethereum.org/EIPS/eip-5115)
- [Pendle Deployed Addresses](https://docs.pendle.finance/Developers/Deployments/Ethereum)
- [Pendle AMM Whitepaper](https://github.com/pendle-finance/pendle-v2-resources/blob/main/whitepapers/V2_AMM.pdf)
- [Pendle Oracle Integration Guide](https://docs.pendle.finance/Developers/Oracles/IntroductionOfPtOracle)
- [Pendle Market List (App)](https://app.pendle.finance/trade/markets)
