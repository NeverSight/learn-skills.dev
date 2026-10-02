---
name: gmx
description: "GMX V2 perpetual and spot DEX — spot swaps, perpetual trading (50x leverage), liquidity provision (GM tokens), Chainlink Data Streams, isolated pools, position management, and multicall patterns. TypeScript SDK (@gmx-io/sdk) and direct contract interactions on Arbitrum and Avalanche."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Trading
tags:
  - gmx
  - perpetuals
  - spot
  - dex
  - arbitrum
  - avalanche
---

# GMX

GMX V2 is a decentralized perpetual and spot exchange deployed on Arbitrum and Avalanche. It uses isolated synthetic markets where each market has its own pool of long/short collateral tokens. Orders are created on-chain and executed asynchronously by keeper networks using Chainlink Data Streams for pricing. Supports up to 100x leverage on perpetual positions, spot swaps, and GM token liquidity provision.

## What You Probably Got Wrong

> LLMs trained before late 2024 confuse V1 (GLP) with V2 (GM tokens, isolated pools). These are the critical corrections.

- **V2 is NOT V1** — V1 used a single shared GLP pool for all markets. V2 uses isolated pools per market (e.g., ETH/USD has its own pool with ETH long collateral and USDC short collateral). GLP is deprecated on V2. Do not reference GLP when working with V2.
- **Orders are asynchronous, not atomic** — Unlike Uniswap, GMX orders are two-step: (1) user creates an order on-chain, (2) a keeper executes it using Chainlink Data Stream prices. Your transaction creates the order; execution happens in a separate transaction. You must pay an execution fee (ETH) upfront to compensate keepers.
- **`multicall` is mandatory for order creation** — You cannot call `createOrder` alone. You must batch `sendWnt` (execution fee) + `sendTokens` (collateral) + `createOrder` into a single `multicall` call on the ExchangeRouter. Calling them separately will fail because the vault expects tokens in the same transaction.
- **`sizeDeltaUsd` uses 30 decimals, not 18** — GMX uses 30 decimal precision for USD values internally. A $1000 position is `1000n * 10n**30n`, not `1000n * 10n**18n`. Getting this wrong creates positions orders of magnitude off.
- **Execution fee is ETH, not a token** — The execution fee sent via `sendWnt` is native ETH (wrapped as WETH internally). It compensates keepers for gas. Excess is refunded. Underpaying causes order rejection.
- **GM tokens are NOT fungible across markets** — Each market has its own GM token. The ETH/USD GM token is different from the BTC/USD GM token. They are separate ERC-20 contracts.
- **ExchangeRouter has been upgraded** — The current ExchangeRouter on Arbitrum is `0x69C527fC77291722b52649E45c838e41be8Bf5d5` (V2.1+). Older addresses like `0x7C68C7866A64FA2160F78EEaE12217FFbf871FA8` are deprecated. Always verify the active router on the official docs.
- **Order types are enums, not strings** — `OrderType.MarketSwap = 0`, `MarketIncrease = 2`, `MarketDecrease = 4`, etc. Passing the wrong enum value creates a completely different order type.
- **Leverage is implicit** — There is no "leverage" parameter. Leverage = `sizeDeltaUsd / collateralAmount`. A $10,000 position with $1,000 collateral is 10x leverage. The protocol enforces min/max leverage per market.

## Quick Start

### Installation

```bash
npm install viem @gmx-io/sdk
```

### Client Setup

```typescript
import { createPublicClient, createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { arbitrum } from "viem/chains";

const publicClient = createPublicClient({
  chain: arbitrum,
  transport: http(process.env.ARBITRUM_RPC_URL),
});

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const walletClient = createWalletClient({
  account,
  chain: arbitrum,
  transport: http(process.env.ARBITRUM_RPC_URL),
});
```

## Core Contracts (Arbitrum)

| Contract | Address | Role |
|----------|---------|------|
| ExchangeRouter | `0x69C527fC77291722b52649E45c838e41be8Bf5d5` | Entry point for orders, deposits, withdrawals |
| Router | `0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6` | Token approval target |
| Reader | `0x22199a49A999c351eF7927602CFB187ec3cae489` | Read market data, positions, orders |
| DataStore | `0xFD70de6b91282D8017aA4E741e9Ae325CAb992d8` | Protocol state storage |
| OrderVault | `0x31eF83a530Fde1B38EE9A18093A333D8Bbbc40D5` | Holds order collateral |
| DepositVault | `0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55` | Holds liquidity deposit tokens |
| WithdrawalVault | `0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701c55` | Holds withdrawal tokens |

> Last verified: February 2026. Always confirm addresses at [docs.gmx.io/docs/api/contracts](https://docs.gmx.io/docs/api/contracts/).

## Order Types

```typescript
enum OrderType {
  MarketSwap = 0,
  LimitSwap = 1,
  MarketIncrease = 2,
  LimitIncrease = 3,
  MarketDecrease = 4,
  LimitDecrease = 5,
  StopLossDecrease = 6,
  Liquidation = 7,
}
```

## Spot Swap

Swap one token for another through a GMX market. Uses `OrderType.MarketSwap`.

```typescript
import { encodeFunctionData, parseEther, type Address } from "viem";

const EXCHANGE_ROUTER = "0x69C527fC77291722b52649E45c838e41be8Bf5d5" as const;
const ORDER_VAULT = "0x31eF83a530Fde1B38EE9A18093A333D8Bbbc40D5" as const;
const WETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1" as const;
const USDC = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831" as const;
// ETH/USD market token
const ETH_USD_MARKET = "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336" as const;

const exchangeRouterAbi = [
  {
    name: "multicall",
    type: "function",
    stateMutability: "payable",
    inputs: [{ name: "data", type: "bytes[]" }],
    outputs: [{ name: "results", type: "bytes[]" }],
  },
  {
    name: "sendWnt",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "receiver", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "sendTokens",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "token", type: "address" },
      { name: "receiver", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "createOrder",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          {
            name: "addresses",
            type: "tuple",
            components: [
              { name: "receiver", type: "address" },
              { name: "cancellationReceiver", type: "address" },
              { name: "callbackContract", type: "address" },
              { name: "uiFeeReceiver", type: "address" },
              { name: "market", type: "address" },
              { name: "initialCollateralToken", type: "address" },
              { name: "swapPath", type: "address[]" },
            ],
          },
          {
            name: "numbers",
            type: "tuple",
            components: [
              { name: "sizeDeltaUsd", type: "uint256" },
              { name: "initialCollateralDeltaAmount", type: "uint256" },
              { name: "triggerPrice", type: "uint256" },
              { name: "acceptablePrice", type: "uint256" },
              { name: "executionFee", type: "uint256" },
              { name: "callbackGasLimit", type: "uint256" },
              { name: "minOutputAmount", type: "uint256" },
            ],
          },
          { name: "orderType", type: "uint8" },
          { name: "decreasePositionSwapType", type: "uint8" },
          { name: "isLong", type: "bool" },
          { name: "shouldUnwrapNativeToken", type: "bool" },
          { name: "autoCancel", type: "bool" },
          { name: "referralCode", type: "bytes32" },
        ],
      },
    ],
    outputs: [{ name: "", type: "bytes32" }],
  },
] as const;

const executionFee = parseEther("0.001");
const swapAmount = 1_000_000n; // 1 USDC (6 decimals)

const sendWntData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendWnt",
  args: [ORDER_VAULT, executionFee],
});

const sendTokensData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendTokens",
  args: [USDC, ORDER_VAULT, swapAmount],
});

const createOrderData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "createOrder",
  args: [
    {
      addresses: {
        receiver: account.address,
        cancellationReceiver: account.address,
        callbackContract: "0x0000000000000000000000000000000000000000",
        uiFeeReceiver: "0x0000000000000000000000000000000000000000",
        market: ETH_USD_MARKET,
        initialCollateralToken: USDC,
        swapPath: [ETH_USD_MARKET],
      },
      numbers: {
        sizeDeltaUsd: 0n, // 0 for swaps
        initialCollateralDeltaAmount: 0n,
        triggerPrice: 0n,
        acceptablePrice: 0n,
        executionFee,
        callbackGasLimit: 0n,
        minOutputAmount: 0n, // set slippage protection in production
      },
      orderType: 0, // MarketSwap
      decreasePositionSwapType: 0,
      isLong: false,
      shouldUnwrapNativeToken: false,
      autoCancel: false,
      referralCode: "0x0000000000000000000000000000000000000000000000000000000000000000",
    },
  ],
});

const hash = await walletClient.writeContract({
  address: EXCHANGE_ROUTER,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [[sendWntData, sendTokensData, createOrderData]],
  value: executionFee,
});
```

## Open Perpetual Position

Open a leveraged long or short position. Uses `OrderType.MarketIncrease`.

```typescript
// 30-decimal precision for USD values
const USD_DECIMALS = 30n;
const toUsd30 = (usd: number) => BigInt(Math.round(usd * 1e6)) * 10n ** 24n;

const collateralAmount = parseEther("0.5"); // 0.5 ETH as collateral
const positionSizeUsd = toUsd30(5000); // $5,000 position (~10x leverage on 0.5 ETH)

const sendWntData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendWnt",
  args: [ORDER_VAULT, collateralAmount + executionFee],
});

const createOrderData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "createOrder",
  args: [
    {
      addresses: {
        receiver: account.address,
        cancellationReceiver: account.address,
        callbackContract: "0x0000000000000000000000000000000000000000",
        uiFeeReceiver: "0x0000000000000000000000000000000000000000",
        market: ETH_USD_MARKET,
        initialCollateralToken: WETH,
        swapPath: [],
      },
      numbers: {
        sizeDeltaUsd: positionSizeUsd,
        initialCollateralDeltaAmount: 0n,
        triggerPrice: 0n,
        // acceptablePrice: max price willing to pay for longs, min for shorts
        acceptablePrice: BigInt("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"),
        executionFee,
        callbackGasLimit: 0n,
        minOutputAmount: 0n,
      },
      orderType: 2, // MarketIncrease
      decreasePositionSwapType: 0,
      isLong: true,
      shouldUnwrapNativeToken: false,
      autoCancel: false,
      referralCode: "0x0000000000000000000000000000000000000000000000000000000000000000",
    },
  ],
});

const hash = await walletClient.writeContract({
  address: EXCHANGE_ROUTER,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  // sendWnt sends both collateral + execution fee to OrderVault
  args: [[sendWntData, createOrderData]],
  value: collateralAmount + executionFee,
});
```

## Close / Decrease Position

Reduce or close an existing position. Uses `OrderType.MarketDecrease`.

```typescript
const decreaseOrderData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "createOrder",
  args: [
    {
      addresses: {
        receiver: account.address,
        cancellationReceiver: account.address,
        callbackContract: "0x0000000000000000000000000000000000000000",
        uiFeeReceiver: "0x0000000000000000000000000000000000000000",
        market: ETH_USD_MARKET,
        initialCollateralToken: WETH,
        swapPath: [],
      },
      numbers: {
        sizeDeltaUsd: positionSizeUsd, // close entire position
        initialCollateralDeltaAmount: 0n, // withdraw all remaining collateral
        triggerPrice: 0n,
        // acceptablePrice: min price for longs (slippage protection)
        acceptablePrice: 0n,
        executionFee,
        callbackGasLimit: 0n,
        minOutputAmount: 0n,
      },
      orderType: 4, // MarketDecrease
      decreasePositionSwapType: 0,
      isLong: true,
      shouldUnwrapNativeToken: true,
      autoCancel: false,
      referralCode: "0x0000000000000000000000000000000000000000000000000000000000000000",
    },
  ],
});

const sendWntForFee = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendWnt",
  args: [ORDER_VAULT, executionFee],
});

const hash = await walletClient.writeContract({
  address: EXCHANGE_ROUTER,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [[sendWntForFee, decreaseOrderData]],
  value: executionFee,
});
```

## Take-Profit and Stop-Loss Orders

Attach conditional orders to an existing position.

```typescript
// Take-profit: LimitDecrease (orderType = 5)
// Triggers when market price reaches triggerPrice
const takeProfitData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "createOrder",
  args: [
    {
      addresses: {
        receiver: account.address,
        cancellationReceiver: account.address,
        callbackContract: "0x0000000000000000000000000000000000000000",
        uiFeeReceiver: "0x0000000000000000000000000000000000000000",
        market: ETH_USD_MARKET,
        initialCollateralToken: WETH,
        swapPath: [],
      },
      numbers: {
        sizeDeltaUsd: positionSizeUsd,
        initialCollateralDeltaAmount: 0n,
        // trigger at $4000 — 30-decimal precision
        triggerPrice: toUsd30(4000),
        acceptablePrice: toUsd30(3950), // min acceptable price for long TP
        executionFee,
        callbackGasLimit: 0n,
        minOutputAmount: 0n,
      },
      orderType: 5, // LimitDecrease (take-profit)
      decreasePositionSwapType: 0,
      isLong: true,
      shouldUnwrapNativeToken: true,
      autoCancel: false,
      referralCode: "0x0000000000000000000000000000000000000000000000000000000000000000",
    },
  ],
});

// Stop-loss: StopLossDecrease (orderType = 6)
const stopLossData = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "createOrder",
  args: [
    {
      addresses: {
        receiver: account.address,
        cancellationReceiver: account.address,
        callbackContract: "0x0000000000000000000000000000000000000000",
        uiFeeReceiver: "0x0000000000000000000000000000000000000000",
        market: ETH_USD_MARKET,
        initialCollateralToken: WETH,
        swapPath: [],
      },
      numbers: {
        sizeDeltaUsd: positionSizeUsd,
        initialCollateralDeltaAmount: 0n,
        // trigger at $2800
        triggerPrice: toUsd30(2800),
        acceptablePrice: 0n, // min price for long SL
        executionFee,
        callbackGasLimit: 0n,
        minOutputAmount: 0n,
      },
      orderType: 6, // StopLossDecrease
      decreasePositionSwapType: 0,
      isLong: true,
      shouldUnwrapNativeToken: true,
      autoCancel: false,
      referralCode: "0x0000000000000000000000000000000000000000000000000000000000000000",
    },
  ],
});
```

## GM Token Liquidity (Deposits and Withdrawals)

### Buy GM Tokens (Add Liquidity)

```typescript
const DEPOSIT_VAULT = "0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55" as const;

const createDepositAbi = [
  {
    name: "createDeposit",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "receiver", type: "address" },
          { name: "callbackContract", type: "address" },
          { name: "uiFeeReceiver", type: "address" },
          { name: "market", type: "address" },
          { name: "initialLongToken", type: "address" },
          { name: "initialShortToken", type: "address" },
          { name: "longTokenSwapPath", type: "address[]" },
          { name: "shortTokenSwapPath", type: "address[]" },
          { name: "minMarketTokens", type: "uint256" },
          { name: "shouldUnwrapNativeToken", type: "bool" },
          { name: "executionFee", type: "uint256" },
          { name: "callbackGasLimit", type: "uint256" },
        ],
      },
    ],
    outputs: [{ name: "", type: "bytes32" }],
  },
] as const;

const depositAmount = parseEther("1"); // 1 ETH

const sendWntDeposit = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendWnt",
  args: [DEPOSIT_VAULT, depositAmount + executionFee],
});

const createDepositData = encodeFunctionData({
  abi: [...exchangeRouterAbi, ...createDepositAbi],
  functionName: "createDeposit",
  args: [
    {
      receiver: account.address,
      callbackContract: "0x0000000000000000000000000000000000000000",
      uiFeeReceiver: "0x0000000000000000000000000000000000000000",
      market: ETH_USD_MARKET,
      initialLongToken: WETH,
      initialShortToken: "0x0000000000000000000000000000000000000000",
      longTokenSwapPath: [],
      shortTokenSwapPath: [],
      minMarketTokens: 0n,
      shouldUnwrapNativeToken: false,
      executionFee,
      callbackGasLimit: 0n,
    },
  ],
});

const hash = await walletClient.writeContract({
  address: EXCHANGE_ROUTER,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [[sendWntDeposit, createDepositData]],
  value: depositAmount + executionFee,
});
```

### Sell GM Tokens (Remove Liquidity)

```typescript
const WITHDRAWAL_VAULT = "0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701c55" as const;

const createWithdrawalAbi = [
  {
    name: "createWithdrawal",
    type: "function",
    stateMutability: "payable",
    inputs: [
      {
        name: "params",
        type: "tuple",
        components: [
          { name: "receiver", type: "address" },
          { name: "callbackContract", type: "address" },
          { name: "uiFeeReceiver", type: "address" },
          { name: "market", type: "address" },
          { name: "longTokenSwapPath", type: "address[]" },
          { name: "shortTokenSwapPath", type: "address[]" },
          { name: "minLongTokenAmount", type: "uint256" },
          { name: "minShortTokenAmount", type: "uint256" },
          { name: "shouldUnwrapNativeToken", type: "bool" },
          { name: "executionFee", type: "uint256" },
          { name: "callbackGasLimit", type: "uint256" },
        ],
      },
    ],
    outputs: [{ name: "", type: "bytes32" }],
  },
] as const;

// First: approve GM token spending to Router (not ExchangeRouter)
// Then: send GM tokens to WithdrawalVault via sendTokens
const gmTokenAmount = 500000000000000000n; // amount of GM tokens to redeem

const sendGmTokens = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendTokens",
  args: [ETH_USD_MARKET, WITHDRAWAL_VAULT, gmTokenAmount],
});

const sendWntWithdraw = encodeFunctionData({
  abi: exchangeRouterAbi,
  functionName: "sendWnt",
  args: [WITHDRAWAL_VAULT, executionFee],
});

const createWithdrawalData = encodeFunctionData({
  abi: [...exchangeRouterAbi, ...createWithdrawalAbi],
  functionName: "createWithdrawal",
  args: [
    {
      receiver: account.address,
      callbackContract: "0x0000000000000000000000000000000000000000",
      uiFeeReceiver: "0x0000000000000000000000000000000000000000",
      market: ETH_USD_MARKET,
      longTokenSwapPath: [],
      shortTokenSwapPath: [],
      minLongTokenAmount: 0n,
      minShortTokenAmount: 0n,
      shouldUnwrapNativeToken: true,
      executionFee,
      callbackGasLimit: 0n,
    },
  ],
});

const hash = await walletClient.writeContract({
  address: EXCHANGE_ROUTER,
  abi: exchangeRouterAbi,
  functionName: "multicall",
  args: [[sendWntWithdraw, sendGmTokens, createWithdrawalData]],
  value: executionFee,
});
```

## Reading Market Data (Reader Contract)

```typescript
const READER = "0x22199a49A999c351eF7927602CFB187ec3cae489" as const;
const DATA_STORE = "0xFD70de6b91282D8017aA4E741e9Ae325CAb992d8" as const;

const readerAbi = [
  {
    name: "getMarkets",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "dataStore", type: "address" },
      { name: "start", type: "uint256" },
      { name: "end", type: "uint256" },
    ],
    outputs: [
      {
        name: "",
        type: "tuple[]",
        components: [
          { name: "marketToken", type: "address" },
          { name: "indexToken", type: "address" },
          { name: "longToken", type: "address" },
          { name: "shortToken", type: "address" },
        ],
      },
    ],
  },
  {
    name: "getAccountPositions",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "dataStore", type: "address" },
      { name: "account", type: "address" },
      { name: "start", type: "uint256" },
      { name: "end", type: "uint256" },
    ],
    outputs: [
      {
        name: "",
        type: "tuple[]",
        components: [
          {
            name: "addresses",
            type: "tuple",
            components: [
              { name: "account", type: "address" },
              { name: "market", type: "address" },
              { name: "collateralToken", type: "address" },
            ],
          },
          {
            name: "numbers",
            type: "tuple",
            components: [
              { name: "sizeInUsd", type: "uint256" },
              { name: "sizeInTokens", type: "uint256" },
              { name: "collateralAmount", type: "uint256" },
              { name: "borrowingFactor", type: "uint256" },
              { name: "fundingFeeAmountPerSize", type: "uint256" },
              { name: "longTokenClaimableFundingAmountPerSize", type: "uint256" },
              { name: "shortTokenClaimableFundingAmountPerSize", type: "uint256" },
              { name: "increasedAtTime", type: "uint256" },
              { name: "decreasedAtTime", type: "uint256" },
            ],
          },
          {
            name: "flags",
            type: "tuple",
            components: [{ name: "isLong", type: "bool" }],
          },
        ],
      },
    ],
  },
  {
    name: "getAccountOrders",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "dataStore", type: "address" },
      { name: "account", type: "address" },
      { name: "start", type: "uint256" },
      { name: "end", type: "uint256" },
    ],
    outputs: [{ name: "", type: "tuple[]", components: [] }],
  },
] as const;

const markets = await publicClient.readContract({
  address: READER,
  abi: readerAbi,
  functionName: "getMarkets",
  args: [DATA_STORE, 0n, 100n],
});

const positions = await publicClient.readContract({
  address: READER,
  abi: readerAbi,
  functionName: "getAccountPositions",
  args: [DATA_STORE, account.address, 0n, 100n],
});
```

## SDK Usage (@gmx-io/sdk)

The official SDK abstracts direct contract interaction.

### Initialization

```typescript
import { GmxSdk } from "@gmx-io/sdk";

const sdk = new GmxSdk({
  chainId: 42161,
  rpcUrl: process.env.ARBITRUM_RPC_URL!,
  oracleUrl: "https://arbitrum-api.gmxinfra.io",
  walletClient,
  subsquidUrl:
    "https://gmx.squids.live/gmx-synthetics-arbitrum:prod/api/graphql",
});
```

### Read Markets and Positions

```typescript
const { marketsInfoData, tokensData } = await sdk.markets.getMarketsInfo();

sdk.setAccount(account.address);
const positions = await sdk.positions.getPositions();
```

## Token Approvals

Before sending ERC-20 tokens through the ExchangeRouter, approve the Router contract (not ExchangeRouter):

```typescript
import { erc20Abi } from "viem";

const ROUTER = "0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6" as const;

await walletClient.writeContract({
  address: USDC,
  abi: erc20Abi,
  functionName: "approve",
  args: [ROUTER, 2n ** 256n - 1n],
});
```

## Multicall Pattern for Batched Reads

Batch multiple Reader calls into one RPC request:

```typescript
const results = await publicClient.multicall({
  contracts: [
    {
      address: READER,
      abi: readerAbi,
      functionName: "getMarkets",
      args: [DATA_STORE, 0n, 50n],
    },
    {
      address: READER,
      abi: readerAbi,
      functionName: "getAccountPositions",
      args: [DATA_STORE, account.address, 0n, 50n],
    },
  ],
});

const [marketsResult, positionsResult] = results;
```

## Key Concepts

### Isolated Pools
Each market (e.g., ETH/USD) has its own pool with long collateral (ETH) and short collateral (USDC). Risk is isolated — a liquidation cascade in the DOGE/USD market does not affect the ETH/USD pool.

### Chainlink Data Streams
GMX V2 uses Chainlink Data Streams (not standard Chainlink price feeds) for order execution pricing. Keepers fetch signed price updates from Chainlink's off-chain Data Streams and submit them alongside order execution transactions. This provides low-latency pricing with front-running protection.

### Execution Fee Refunds
If the keeper uses less gas than the execution fee you provided, the excess is refunded to your address. If the fee is insufficient, the order is rejected and the collateral is returned (minus any gas consumed).

### Funding and Borrowing Fees
Positions accrue funding fees (paid between longs and shorts to balance open interest) and borrowing fees (paid for using pool liquidity). These are calculated per second and deducted from collateral on position decrease.

## References

- [GMX V2 Documentation](https://docs.gmx.io/docs/trading/v2/)
- [GMX Contracts Reference](https://docs.gmx.io/docs/api/contracts/)
- [gmx-synthetics GitHub](https://github.com/gmx-io/gmx-synthetics)
- [gmx-interface GitHub](https://github.com/gmx-io/gmx-interface)
- [@gmx-io/sdk on npm](https://www.npmjs.com/package/@gmx-io/sdk)
- [SDK V2 Docs](https://docs.gmx.io/docs/api/sdk-v2/)
