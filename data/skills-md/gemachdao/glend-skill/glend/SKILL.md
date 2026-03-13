---
name: glend
description: Agent skill for interacting with the Glend DeFi Lend & Borrow protocol by GemachDAO. Supply, borrow, repay, withdraw assets and monitor account health on EVM chains using viem.
---

# Glend Agent Skill

This file provides instructions for AI agents interacting with the **Glend** DeFi Lend & Borrow platform by GemachDAO.

## What is Glend?

Glend is a decentralized lending and borrowing protocol deployed on multiple EVM chains. It runs as an **Aave V3 fork** on Pharos Testnet and as a **Compound V2 fork** (gTokens/tTokens) on Ethereum and Base. Agents can:

- **Supply / Lend** — deposit assets to earn interest
- **Borrow** — take loans against supplied collateral
- **Repay** — pay back outstanding debt
- **Withdraw** — reclaim supplied assets (subject to utilization and health factor)
- **Monitor health** — track collateral ratio and liquidation risk

All on-chain interactions are performed with **viem**. Contract addresses and chain configuration are pre-loaded — agents only need a wallet private key to start.

- **Glend App**: `https://glendv2.gemach.io`

---

## Environment Variables

```env
AGENT_PRIVATE_KEY=<private_key>     # Agent wallet private key (never commit!)
```

The only **required** variable is `AGENT_PRIVATE_KEY`. All contract addresses, RPC endpoints, and chain configuration are embedded below.

Optional overrides (advanced — use only if connecting to a custom deployment):

```env
GLEND_RPC_URL=<rpc_url>             # Override the default RPC endpoint
GLEND_POOL_ADDRESS=<address>        # Override the default pool contract
GLEND_CHAIN_ID=<chain_id>           # Override the default chain ID
```

---

## Supported Deployments

### Pharos Testnet (default)

| Property | Value |
|----------|-------|
| **Chain ID** | `688688` |
| **RPC URL** | `https://testnet.dplabs-internal.com` |
| **Block Explorer** | `https://testnet.pharosscan.xyz` |
| **Native Token** | PHRS |
| **Pool (Lending Pool)** | `0xe838eb8011297024bca9c09d4e83e2d3cd74b7d0` |
| **WETHGateway** | `0xa8e550710bf113db6a1b38472118b8d6d5176d12` |
| **Faucet** | `0x2e9d89d372837f71cb529e5ba85bfbc1785c69cd` |

### Token Registry — Pharos Testnet

| Token | Address | Decimals |
|-------|---------|----------|
| USDT | `0x0b00fb1f513e02399667fba50772b21f34c1b5d9` | 6 |
| USDC | `0x48249feeb47a8453023f702f15cf00206eebdf08` | 6 |
| BTC | `0xa4a967fc7cf0e9815bf5c2700a055813628b65be` | 8 |

### Ethereum Mainnet (Compound fork)

| Property | Value |
|----------|-------|
| **Chain ID** | `1` |
| **Protocol** | Compound V2 fork (tTokens) |
| **RPC URL** | `https://eth.llamarpc.com` |
| **Block Explorer** | `https://etherscan.io` |
| **Native Token** | ETH |
| **Comptroller (Unitroller)** | `0x4a4c2A16b58bD63d37e999fDE50C2eBfE3182D58` |
| **PriceOracle** | `0x97f602E17ed4e765a6968f295Bdc3F6b4c1Ef93b` |
| **CompoundLens** | `0x47bdd2Ebfd5081c72adb4238E04559576F2c9ba3` |

### Market Tokens — Ethereum Mainnet

| Market | Address | Collateral Factor |
|--------|---------|-------------------|
| tUSDT | `0xfd7E506495fd921a17802Cf523279f01550BE8b6` | 75% |
| tUSDC | `0x1C5215F2fb5417BdF9D93339b0caf20222f210f3` | 75% |
| tETH | `0x6baeCC06B2faFD651B095ab3b7882AEe6EC4369D` | 80% |
| tcbBTC | `0xF4faD7E54bF68344906C2b60fBCDB031cdeaDB52` | 70% |
| tstETH | `0x6e9acC9D6ea3edE1acAE7Eeb2Be2dE1F8572Bc82` | 78% |

### Base (Compound fork)

| Property | Value |
|----------|-------|
| **Chain ID** | `8453` |
| **Protocol** | Compound V2 fork (gTokens) |
| **RPC URL** | `https://mainnet.base.org` |
| **Block Explorer** | `https://basescan.org` |
| **Native Token** | ETH |
| **Comptroller (Unitroller)** | `0x4a4c2A16b58bD63d37e999fDE50C2eBfE3182D58` |
| **PriceOracle** | `0x97f602E17ed4e765a6968f295Bdc3F6b4c1Ef93b` |
| **CompoundLens** | `0x41d9071C885da8dCa042E05AA66D7D5034383C53` |

### Market Tokens — Base

| Market | Address |
|--------|---------|
| gUSDT | `0x6eAB9a4f7fDE8C1Ef0F62DA16549C80Bb7b7f853` |
| gUSDC | `0xfd7E506495fd921a17802Cf523279f01550BE8b6` |
| gETH | `0x1C5215F2fb5417BdF9D93339b0caf20222f210f3` |
| gcbBTC | `0x920D3D27b17DCC16A7263d2ab176ac68C8385cd3` |

---

## Getting Test Tokens (Faucet)

Before interacting with the lending pool, agents need test tokens. Use the on-chain faucet to mint tokens:

```typescript
const FAUCET_ABI = [
  {
    name: "mint",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_asset", type: "address" },
      { name: "_account", type: "address" },
      { name: "_amount", type: "uint256" },
    ],
    outputs: [],
  },
] as const;

const FAUCET_ADDRESS = "0x2e9d89d372837f71cb529e5ba85bfbc1785c69cd" as const;

async function mintTestTokens(
  tokenAddress: `0x${string}`,
  amount: bigint,
) {
  const hash = await walletClient.writeContract({
    address: FAUCET_ADDRESS,
    abi: FAUCET_ABI,
    functionName: "mint",
    args: [tokenAddress, account.address, amount],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Minted test tokens — tx: ${hash}`);
}

// Example: mint 1000 USDC (6 decimals)
await mintTestTokens("0x48249feeb47a8453023f702f15cf00206eebdf08", parseUnits("1000", 6));
```

---

## Aave V3 Protocol — Pharos Testnet

All agent operations on **Pharos Testnet** target the **Glend Pool** contract (Aave V3 fork). Interact with it via `viem`'s `writeContract` / `readContract`.

### Minimal ABI (key functions)

```typescript
export const GLEND_POOL_ABI = [
  // ── Read ──────────────────────────────────────────────────────────────────
  {
    name: "getUserAccountData",
    type: "function",
    stateMutability: "view",
    inputs:  [{ name: "user",  type: "address" }],
    outputs: [
      { name: "totalCollateralBase",     type: "uint256" },
      { name: "totalDebtBase",           type: "uint256" },
      { name: "availableBorrowsBase",    type: "uint256" },
      { name: "currentLiquidationThreshold", type: "uint256" },
      { name: "ltv",                     type: "uint256" },
      { name: "healthFactor",            type: "uint256" },
    ],
  },
  {
    name: "getReserveData",
    type: "function",
    stateMutability: "view",
    inputs:  [{ name: "asset", type: "address" }],
    outputs: [
      { name: "configuration",    type: "uint256" },
      { name: "liquidityIndex",   type: "uint128" },
      { name: "variableBorrowIndex", type: "uint128" },
      { name: "currentLiquidityRate",      type: "uint128" },
      { name: "currentVariableBorrowRate", type: "uint128" },
      { name: "lastUpdateTimestamp",       type: "uint40"  },
      { name: "aTokenAddress",             type: "address" },
      { name: "variableDebtTokenAddress",  type: "address" },
      { name: "interestRateStrategyAddress", type: "address" },
      { name: "id",               type: "uint8"   },
    ],
  },
  // ── Write ─────────────────────────────────────────────────────────────────
  {
    name: "supply",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset",          type: "address" },
      { name: "amount",         type: "uint256" },
      { name: "onBehalfOf",     type: "address" },
      { name: "referralCode",   type: "uint16"  },
    ],
    outputs: [],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset",      type: "address" },
      { name: "amount",     type: "uint256" },   // use MaxUint256 to withdraw all
      { name: "to",         type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "borrow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset",              type: "address" },
      { name: "amount",             type: "uint256" },
      { name: "interestRateMode",   type: "uint256" }, // 2 = variable
      { name: "referralCode",       type: "uint16"  },
      { name: "onBehalfOf",         type: "address" },
    ],
    outputs: [],
  },
  {
    name: "repay",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "asset",            type: "address" },
      { name: "amount",           type: "uint256" }, // use MaxUint256 to repay all
      { name: "interestRateMode", type: "uint256" }, // 2 = variable
      { name: "onBehalfOf",       type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;
```

---

## Agent Operations

### 1 · Set up viem clients

```typescript
import {
  createPublicClient,
  createWalletClient,
  http,
  parseUnits,
  formatUnits,
  maxUint256,
  defineChain,
} from "viem";
import { mainnet, base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";
import type { Chain } from "viem";

// ── Pharos Testnet chain definition ────────────────────────────────────────
const pharosTestnet = defineChain({
  id: 688688,
  name: "Pharos Testnet",
  nativeCurrency: { name: "PHRS", symbol: "PHRS", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://testnet.dplabs-internal.com"] },
  },
  blockExplorers: {
    default: { name: "Pharos Explorer", url: "https://testnet.pharosscan.xyz" },
  },
  testnet: true,
});

// ── All supported chains ───────────────────────────────────────────────────
const GLEND_CHAINS: Record<number, Chain> = {
  688688: pharosTestnet,
  1: mainnet,
  8453: base,
};

// ── Aave V3 deployment (Pharos Testnet) ────────────────────────────────────
const PHAROS_DEPLOYMENT = {
  pool: "0xe838eb8011297024bca9c09d4e83e2d3cd74b7d0" as `0x${string}`,
  wethGateway: "0xa8e550710bf113db6a1b38472118b8d6d5176d12" as `0x${string}`,
  faucet: "0x2e9d89d372837f71cb529e5ba85bfbc1785c69cd" as `0x${string}`,
  tokens: {
    USDT: { address: "0x0b00fb1f513e02399667fba50772b21f34c1b5d9" as `0x${string}`, decimals: 6 },
    USDC: { address: "0x48249feeb47a8453023f702f15cf00206eebdf08" as `0x${string}`, decimals: 6 },
    BTC:  { address: "0xa4a967fc7cf0e9815bf5c2700a055813628b65be" as `0x${string}`, decimals: 8 },
  },
};

// ── Compound fork deployment (Ethereum Mainnet) ────────────────────────────
const ETH_DEPLOYMENT = {
  comptroller: "0x4a4c2A16b58bD63d37e999fDE50C2eBfE3182D58" as `0x${string}`,
  priceOracle: "0x97f602E17ed4e765a6968f295Bdc3F6b4c1Ef93b" as `0x${string}`,
  compoundLens: "0x47bdd2Ebfd5081c72adb4238E04559576F2c9ba3" as `0x${string}`,
  markets: {
    tUSDT:  { address: "0xfd7E506495fd921a17802Cf523279f01550BE8b6" as `0x${string}` },
    tUSDC:  { address: "0x1C5215F2fb5417BdF9D93339b0caf20222f210f3" as `0x${string}` },
    tETH:   { address: "0x6baeCC06B2faFD651B095ab3b7882AEe6EC4369D" as `0x${string}` },
    tcbBTC: { address: "0xF4faD7E54bF68344906C2b60fBCDB031cdeaDB52" as `0x${string}` },
    tstETH: { address: "0x6e9acC9D6ea3edE1acAE7Eeb2Be2dE1F8572Bc82" as `0x${string}` },
  },
};

// ── Compound fork deployment (Base) ────────────────────────────────────────
const BASE_DEPLOYMENT = {
  comptroller: "0x4a4c2A16b58bD63d37e999fDE50C2eBfE3182D58" as `0x${string}`,
  priceOracle: "0x97f602E17ed4e765a6968f295Bdc3F6b4c1Ef93b" as `0x${string}`,
  compoundLens: "0x41d9071C885da8dCa042E05AA66D7D5034383C53" as `0x${string}`,
  markets: {
    gUSDT:  { address: "0x6eAB9a4f7fDE8C1Ef0F62DA16549C80Bb7b7f853" as `0x${string}` },
    gUSDC:  { address: "0xfd7E506495fd921a17802Cf523279f01550BE8b6" as `0x${string}` },
    gETH:   { address: "0x1C5215F2fb5417BdF9D93339b0caf20222f210f3" as `0x${string}` },
    gcbBTC: { address: "0x920D3D27b17DCC16A7263d2ab176ac68C8385cd3" as `0x${string}` },
  },
};

// ── Resolve configuration ──────────────────────────────────────────────────
const CHAIN_ID    = Number(process.env.GLEND_CHAIN_ID ?? 688688);
const chain       = GLEND_CHAINS[CHAIN_ID];
if (!chain) {
  throw new Error(`Unsupported chain ID: ${CHAIN_ID}. Supported: ${Object.keys(GLEND_CHAINS).join(", ")}`);
}
const RPC_URL     = process.env.GLEND_RPC_URL ?? chain.rpcUrls.default.http[0];
const PRIVATE_KEY = process.env.AGENT_PRIVATE_KEY as `0x${string}`;

const account      = privateKeyToAccount(PRIVATE_KEY);
const publicClient = createPublicClient({ chain, transport: http(RPC_URL) });
const walletClient = createWalletClient({ account, chain, transport: http(RPC_URL) });

// ── Pharos helpers ─────────────────────────────────────────────────────────
const POOL_ADDRESS = (process.env.GLEND_POOL_ADDRESS ?? PHAROS_DEPLOYMENT.pool) as `0x${string}`;

function getToken(symbol: string) {
  const token = PHAROS_DEPLOYMENT.tokens[symbol as keyof typeof PHAROS_DEPLOYMENT.tokens];
  if (!token) throw new Error(`Unknown token: ${symbol}. Available: ${Object.keys(PHAROS_DEPLOYMENT.tokens).join(", ")}`);
  return token;
}

// ── Compound helpers ───────────────────────────────────────────────────────
function getDeployment() {
  if (CHAIN_ID === 1)    return ETH_DEPLOYMENT;
  if (CHAIN_ID === 8453) return BASE_DEPLOYMENT;
  throw new Error(`Chain ${CHAIN_ID} does not have a Compound V2 deployment. Supported: Ethereum (1), Base (8453). For Aave V3, use Pharos (688688).`);
}

function getComptroller(): `0x${string}` {
  const deployment = getDeployment();
  if (!deployment.comptroller) {
    throw new Error(`Comptroller address not configured for chain ${CHAIN_ID}. Market operations (mint, borrow, etc.) still work directly.`);
  }
  return deployment.comptroller;
}

function getMarket(symbol: string) {
  const deployment = getDeployment();
  const market = deployment.markets[symbol as keyof typeof deployment.markets];
  if (!market) throw new Error(`Unknown market: ${symbol}. Available: ${Object.keys(deployment.markets).join(", ")}`);
  return market;
}
```

### 2 · Approve ERC-20 before supply or repay

```typescript
import { erc20Abi } from "viem";

async function approveToken(tokenAddress: `0x${string}`, amount: bigint) {
  const hash = await walletClient.writeContract({
    address: tokenAddress,
    abi: erc20Abi,
    functionName: "approve",
    args: [POOL_ADDRESS, amount],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log("Approved:", hash);
}
```

### 3 · Supply (lend) assets

```typescript
async function supplyAsset(
  tokenAddress: `0x${string}`,
  humanAmount: string,
  decimals: number,
) {
  const amount = parseUnits(humanAmount, decimals);
  await approveToken(tokenAddress, amount);

  const hash = await walletClient.writeContract({
    address: POOL_ADDRESS,
    abi: GLEND_POOL_ABI,
    functionName: "supply",
    args: [tokenAddress, amount, account.address, 0],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Supplied ${humanAmount} — tx: ${hash}`);
}
```

### 4 · Borrow assets

```typescript
async function borrowAsset(
  tokenAddress: `0x${string}`,
  humanAmount: string,
  decimals: number,
) {
  const amount = parseUnits(humanAmount, decimals);
  const hash = await walletClient.writeContract({
    address: POOL_ADDRESS,
    abi: GLEND_POOL_ABI,
    functionName: "borrow",
    args: [tokenAddress, amount, 2n, 0, account.address], // 2 = variable rate
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Borrowed ${humanAmount} — tx: ${hash}`);
}
```

### 5 · Repay debt

```typescript
import { erc20Abi } from "viem";

/** Fetch the current variable debt balance for a token. */
async function getDebtBalance(
  variableDebtTokenAddress: `0x${string}`,
  userAddress: `0x${string}`,
): Promise<bigint> {
  return publicClient.readContract({
    address: variableDebtTokenAddress,
    abi: erc20Abi,
    functionName: "balanceOf",
    args: [userAddress],
  });
}

async function repayDebt(
  tokenAddress: `0x${string}`,
  variableDebtTokenAddress: `0x${string}`,
  humanAmount: string | "all",
  decimals: number,
) {
  // Determine the repay amount for the Pool call (maxUint256 = repay all debt)
  const repayAmount = humanAmount === "all" ? maxUint256 : parseUnits(humanAmount, decimals);

  // For the ERC-20 approval, always approve the exact token amount being transferred.
  // When repaying "all", query the live debt balance so the approval is not excessive.
  const approvalAmount =
    humanAmount === "all"
      ? await getDebtBalance(variableDebtTokenAddress, account.address)
      : parseUnits(humanAmount, decimals);

  await approveToken(tokenAddress, approvalAmount);

  const hash = await walletClient.writeContract({
    address: POOL_ADDRESS,
    abi: GLEND_POOL_ABI,
    functionName: "repay",
    args: [tokenAddress, repayAmount, 2n, account.address],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Repaid — tx: ${hash}`);
}
```

### 6 · Withdraw supplied assets

```typescript
async function withdrawAsset(
  tokenAddress: `0x${string}`,
  humanAmount: string | "all",
  decimals: number,
) {
  const amount = humanAmount === "all" ? maxUint256 : parseUnits(humanAmount, decimals);

  const hash = await walletClient.writeContract({
    address: POOL_ADDRESS,
    abi: GLEND_POOL_ABI,
    functionName: "withdraw",
    args: [tokenAddress, amount, account.address],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Withdrew — tx: ${hash}`);
}
```

### 7 · Check account health

```typescript
async function getAccountHealth(userAddress: `0x${string}`) {
  const data = await publicClient.readContract({
    address: POOL_ADDRESS,
    abi: GLEND_POOL_ABI,
    functionName: "getUserAccountData",
    args: [userAddress],
  });

  const [
    totalCollateralBase,
    totalDebtBase,
    availableBorrowsBase,
    currentLiquidationThreshold,
    ltv,
    healthFactor,
  ] = data;

  // healthFactor is scaled by 1e18 — values below 1e18 risk liquidation
  const hf = formatUnits(healthFactor, 18);
  console.log({
    totalCollateral: formatUnits(totalCollateralBase, 8),
    totalDebt:       formatUnits(totalDebtBase, 8),
    availableToBorrow: formatUnits(availableBorrowsBase, 8),
    healthFactor: hf,
    atRisk: Number(hf) < 1.1,
  });

  return { totalCollateralBase, totalDebtBase, availableBorrowsBase, healthFactor };
}
```

### 8 · Get reserve (market) data

```typescript
async function getMarketData(tokenAddress: `0x${string}`) {
  const data = await publicClient.readContract({
    address: POOL_ADDRESS,
    abi: GLEND_POOL_ABI,
    functionName: "getReserveData",
    args: [tokenAddress],
  });

  // Rates are per-second values in ray units (1e27).
  // Annualise using compound-interest: APY = (1 + ratePerSecond)^31_536_000 - 1
  const SECONDS_PER_YEAR = 31_536_000n;
  const RAY = 10n ** 27n;

  function rayToAPY(rayRate: bigint): string {
    // Use floating-point for the exponentiation
    const ratePerSecond = Number(rayRate) / Number(RAY);
    const apy = (Math.pow(1 + ratePerSecond, Number(SECONDS_PER_YEAR)) - 1) * 100;
    return `${apy.toFixed(2)}%`;
  }

  const supplyAPY = rayToAPY(data.currentLiquidityRate);
  const borrowAPY = rayToAPY(data.currentVariableBorrowRate);

  console.log({ supplyAPY, borrowAPY });
  return data;
}
```

---

## Compound V2 Protocol — Ethereum & Base

On **Ethereum Mainnet** and **Base**, Glend uses a **Compound V2 fork** architecture. Instead of a single Pool contract, agents interact with individual **gToken/tToken** market contracts and a **Comptroller** for collateral management.

These ABIs match the standard Compound V2 interface — the same functions used by the Glend front-end at `glendv2.gemach.io`.

### gToken / tToken ABI (Compound V2 CToken interface)

```typescript
export const GTOKEN_ABI = [
  // ── Supply: approve underlying ERC-20 to gToken, then call mint ──────────
  {
    name: "mint",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "mintAmount", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }], // 0 = success
  },
  // ── Borrow ───────────────────────────────────────────────────────────────
  {
    name: "borrow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "borrowAmount", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }], // 0 = success
  },
  // ── Repay ────────────────────────────────────────────────────────────────
  {
    name: "repayBorrow",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "repayAmount", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }], // 0 = success
  },
  // ── Withdraw (by underlying amount) ──────────────────────────────────────
  {
    name: "redeemUnderlying",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "redeemAmount", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }], // 0 = success
  },
  // ── Withdraw (by gToken amount) ──────────────────────────────────────────
  {
    name: "redeem",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "redeemTokens", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }], // 0 = success
  },
  // ── Read ──────────────────────────────────────────────────────────────────
  {
    name: "underlying",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "owner", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "balanceOfUnderlying",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "owner", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "borrowBalanceCurrent",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "getAccountSnapshot",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [
      { name: "error",           type: "uint256" },
      { name: "tokenBalance",    type: "uint256" },
      { name: "borrowBalance",   type: "uint256" },
      { name: "exchangeRateMantissa", type: "uint256" },
    ],
  },
  {
    name: "exchangeRateCurrent",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "totalBorrows",
    type: "function",
    stateMutability: "view",
    inputs: [],
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
    name: "getCash",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "supplyRatePerBlock",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "borrowRatePerBlock",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "decimals",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint8" }],
  },
  {
    name: "symbol",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "string" }],
  },
] as const;
```

### Comptroller ABI (Compound V2 Comptroller interface)

```typescript
export const COMPTROLLER_ABI = [
  {
    name: "enterMarkets",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "gTokens", type: "address[]" }],
    outputs: [{ name: "", type: "uint256[]" }], // 0 = success for each
  },
  {
    name: "exitMarket",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "gTokenAddress", type: "address" }],
    outputs: [{ name: "", type: "uint256" }], // 0 = success
  },
  {
    name: "getAccountLiquidity",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [
      { name: "error",     type: "uint256" }, // 0 = no error
      { name: "liquidity",  type: "uint256" }, // excess liquidity (USD, 18 decimals)
      { name: "shortfall",  type: "uint256" }, // shortfall (USD, 18 decimals)
    ],
  },
  {
    name: "markets",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "gToken", type: "address" }],
    outputs: [
      { name: "isListed", type: "bool" },
      { name: "collateralFactorMantissa", type: "uint256" },
    ],
  },
  {
    name: "getAllMarkets",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "address[]" }],
  },
  {
    name: "getAssetsIn",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "address[]" }],
  },
  {
    name: "oracle",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "address" }],
  },
] as const;
```

### Compound Agent Operations

#### 1 · Get the underlying token address

```typescript
async function getUnderlying(gTokenAddress: `0x${string}`): Promise<`0x${string}`> {
  return publicClient.readContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "underlying",
  }) as Promise<`0x${string}`>;
}
```

#### 2 · Enable a market as collateral (enterMarkets)

Before borrowing, the agent must enable supplied markets as collateral via the Comptroller:

```typescript
// Use the Comptroller address from the deployment config
const COMPTROLLER = getComptroller();

async function enableCollateral(gTokenAddresses: `0x${string}`[]) {
  const hash = await walletClient.writeContract({
    address: COMPTROLLER,
    abi: COMPTROLLER_ABI,
    functionName: "enterMarkets",
    args: [gTokenAddresses],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Enabled collateral — tx: ${hash}`);
}
```

#### 3 · Supply (mint gTokens)

```typescript
import { erc20Abi } from "viem";

async function compoundSupply(
  gTokenAddress: `0x${string}`,
  humanAmount: string,
  decimals: number,
) {
  const amount = parseUnits(humanAmount, decimals);
  const underlying = await getUnderlying(gTokenAddress);

  // Approve the underlying token to the gToken contract
  const approveHash = await walletClient.writeContract({
    address: underlying,
    abi: erc20Abi,
    functionName: "approve",
    args: [gTokenAddress, amount],
  });
  await publicClient.waitForTransactionReceipt({ hash: approveHash });

  // Mint gTokens (supply)
  const hash = await walletClient.writeContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "mint",
    args: [amount],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Supplied ${humanAmount} — tx: ${hash}`);
}
```

#### 4 · Borrow

```typescript
async function compoundBorrow(
  gTokenAddress: `0x${string}`,
  humanAmount: string,
  decimals: number,
) {
  const amount = parseUnits(humanAmount, decimals);
  const hash = await walletClient.writeContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "borrow",
    args: [amount],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Borrowed ${humanAmount} — tx: ${hash}`);
}
```

#### 5 · Repay

```typescript
async function compoundRepay(
  gTokenAddress: `0x${string}`,
  humanAmount: string,
  decimals: number,
) {
  const amount = parseUnits(humanAmount, decimals);
  const underlying = await getUnderlying(gTokenAddress);

  // Approve the underlying token
  const approveHash = await walletClient.writeContract({
    address: underlying,
    abi: erc20Abi,
    functionName: "approve",
    args: [gTokenAddress, amount],
  });
  await publicClient.waitForTransactionReceipt({ hash: approveHash });

  const hash = await walletClient.writeContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "repayBorrow",
    args: [amount],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Repaid ${humanAmount} — tx: ${hash}`);
}
```

#### 6 · Withdraw (redeem)

```typescript
async function compoundWithdraw(
  gTokenAddress: `0x${string}`,
  humanAmount: string,
  decimals: number,
) {
  const amount = parseUnits(humanAmount, decimals);
  const hash = await walletClient.writeContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "redeemUnderlying",
    args: [amount],
  });
  await publicClient.waitForTransactionReceipt({ hash });
  console.log(`Withdrew ${humanAmount} — tx: ${hash}`);
}
```

#### 7 · Check account liquidity

```typescript
async function getCompoundAccountHealth(userAddress: `0x${string}`) {
  const [error, liquidity, shortfall] = await publicClient.readContract({
    address: COMPTROLLER,
    abi: COMPTROLLER_ABI,
    functionName: "getAccountLiquidity",
    args: [userAddress],
  });

  console.log({
    error: Number(error),
    excessLiquidity: formatUnits(liquidity, 18),
    shortfall: formatUnits(shortfall, 18),
    atRisk: shortfall > 0n,
  });

  return { error, liquidity, shortfall };
}
```

#### 8 · Get market rates

```typescript
async function getCompoundMarketRates(gTokenAddress: `0x${string}`) {
  const supplyRate = await publicClient.readContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "supplyRatePerBlock",
  });
  const borrowRate = await publicClient.readContract({
    address: gTokenAddress,
    abi: GTOKEN_ABI,
    functionName: "borrowRatePerBlock",
  });

  // Convert per-block rate to APY (assuming ~12s blocks, ~2628000 blocks/year)
  const BLOCKS_PER_YEAR = 2_628_000;
  const supplyAPY = (Math.pow(1 + Number(supplyRate) / 1e18, BLOCKS_PER_YEAR) - 1) * 100;
  const borrowAPY = (Math.pow(1 + Number(borrowRate) / 1e18, BLOCKS_PER_YEAR) - 1) * 100;

  console.log({ supplyAPY: `${supplyAPY.toFixed(2)}%`, borrowAPY: `${borrowAPY.toFixed(2)}%` });
  return { supplyRate, borrowRate };
}
```

---

## Key Safety Rules for Agents

1. **Always check health/liquidity before borrowing** — on Aave V3, keep health factor above **1.5**; on Compound, ensure `liquidity > 0` and `shortfall == 0`.
2. **Approve the exact amount** before `supply`/`mint` and `repay`/`repayBorrow`; never set an open-ended allowance.
3. **On Aave V3**: `maxUint256` in `repay()` means repay all debt — the ERC-20 approval must still use the precise token amount.
4. **On Compound**: call `enterMarkets()` on the Comptroller before borrowing, otherwise supplied assets won't count as collateral.
5. **Simulate transactions** with `publicClient.simulateContract` before sending:

```typescript
// Aave V3 example
const { request } = await publicClient.simulateContract({
  address: POOL_ADDRESS,
  abi: GLEND_POOL_ABI,
  functionName: "borrow",
  args: [tokenAddress, amount, 2n, 0, account.address],
  account,
});
const hash = await walletClient.writeContract(request);
```

6. **Wait for receipt** before assuming a transaction succeeded.
7. **Never log or commit private keys**; read them from environment variables only.
8. **Check return values on Compound** — `mint`, `borrow`, `repayBorrow`, and `redeem` return `0` on success; non-zero means error.

---

## Typical Agent Workflows

### Pharos Testnet (Aave V3)

```
1. mintTestTokens(getToken("USDC").address, parseUnits("1000", 6))
   → get test USDC from faucet

2. getAccountHealth(agentAddress)
   → confirm healthFactor > 1.5 before borrowing

3. supplyAsset(getToken("USDC").address, "1000", 6)
   → deposit 1000 USDC as collateral

4. getAccountHealth(agentAddress)
   → verify collateral registered, check availableBorrowsBase

5. borrowAsset(getToken("USDT").address, "500", 6)
   → borrow 500 USDT against USDC collateral

6. [... use borrowed funds ...]

7. repayDebt(getToken("USDT").address, variableDebtTokenAddress, "all", 6)
   → repay full USDT debt

8. withdrawAsset(getToken("USDC").address, "all", 6)
   → recover USDC collateral
```

### Ethereum & Base (Compound V2)

```
1. compoundSupply(getMarket("gUSDC").address, "1000", 6)
   → supply 1000 USDC, receive gUSDC tokens

2. enableCollateral([getMarket("gUSDC").address])
   → enable gUSDC as collateral on the Comptroller

3. getCompoundAccountHealth(agentAddress)
   → confirm liquidity > 0 and shortfall == 0

4. compoundBorrow(getMarket("gUSDT").address, "500", 6)
   → borrow 500 USDT against gUSDC collateral

5. [... use borrowed funds ...]

6. compoundRepay(getMarket("gUSDT").address, "500", 6)
   → repay USDT debt

7. compoundWithdraw(getMarket("gUSDC").address, "1000", 6)
   → redeem gUSDC for underlying USDC
```

---

## Troubleshooting

### Aave V3 (Pharos Testnet)

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `CALLER_NOT_IN_WHITELIST` | Protocol access control | Confirm the agent wallet is allowed |
| `HEALTH_FACTOR_LOWER_THAN_LIQUIDATION_THRESHOLD` | Borrow would make account unsafe | Reduce borrow amount |
| `NO_ACTIVE_RESERVE` | Wrong token address or chain | Use addresses from the Token Registry above |
| `TRANSFER_AMOUNT_EXCEEDS_BALANCE` | Insufficient token balance | Use the faucet to mint test tokens |
| ERC-20 allowance error | `approve()` not called first | Call `approveToken()` before supply/repay |

### Compound V2 (Ethereum & Base)

| Error / Return Code | Likely cause | Fix |
|---------------------|-------------|-----|
| `mint` returns non-zero | Insufficient balance or allowance | Approve underlying token first |
| `borrow` returns non-zero | Insufficient collateral | Call `enterMarkets()` or supply more |
| `COMPTROLLER_REJECTION` | Collateral not enabled | Call `enableCollateral()` before borrowing |
| `shortfall > 0` | Account is undercollateralized | Repay debt or supply more collateral |
| `redeemUnderlying` returns non-zero | Withdrawal would cause shortfall | Repay debt first |

---

## Resources

- Glend App: `https://glendv2.gemach.io`
- Pharos Testnet Explorer: `https://testnet.pharosscan.xyz`
- Ethereum Explorer: `https://etherscan.io`
- Base Explorer: `https://basescan.org`
- GemachDAO: `https://github.com/GemachDAO`
- viem docs: `https://viem.sh`
