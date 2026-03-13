---
name: jupiter-lend
description: Interact with Jupiter Lend Protocol. Read-only SDK (@jup-ag/lend-read) for querying liquidity pools, lending markets (jlTokens), and vaults. Write SDK (@jup-ag/lend) for lending (deposit/withdraw) and vault operations (deposit collateral, borrow, repay, manage positions). No API keys needed for on-chain interactions.
license: MIT
metadata:
  author: jupiter
  version: "1.0.0"
tags:
  - jupiter-lend
  - jup-ag
  - lend
  - borrow
  - earn
  - fluid-protocol
  - jltoken
  - vaults
  - liquidity
  - solana
  - defi
---

# Jupiter Lend Protocol

Jupiter Lend (powered by Fluid Protocol) is a lending and borrowing protocol on Solana. It offers **Liquidity Pools**, **Lending Markets (jlTokens)**, and **Vaults** for leveraged positions.

The protocol uses two main SDKs:

- `@jup-ag/lend-read`: Read-only queries for all programs (Liquidity, Lending, Vaults)
- `@jup-ag/lend`: Write operations (deposit, withdraw, borrow, repay)

## SDK Installation

```bash
# For read operations (queries, prices, positions)
npm install @jup-ag/lend-read

# For write operations (transactions)
npm install @jup-ag/lend
```

---

# 1. Key Concepts & Protocol Jargon

Understanding the architecture and terminology of Jupiter Lend will help you build better integrations.

### Architecture: The Two-Layer Model

- **Liquidity Layer (Single Orderbook)**: The foundational layer where all assets reside. It manages token limits, rate curves, and unified liquidity. Users never interact with this directly.
- **Protocol Layer**: User-facing modules (Lending and Vaults) that sit on top of the Liquidity Layer and interact with it via Cross-Program Invocations (CPIs).

### Terminology

- **jlToken (Jupiter Lend Token)**: The yield-bearing asset you receive when supplying tokens to the Lending protocol (e.g., `jlUSDC`). As interest accrues, the exchange rate increases, making your `jlToken` worth more underlying `USDC`.
- **Exchange Price**: The conversion rate used to translate between "raw" stored amounts and actual token amounts. It continuously increases as interest is earned on supply or accrued on debt.
- **Collateral Factor (CF)**: The maximum Loan-to-Value (LTV) ratio allowed when opening or managing a position.
- **Liquidation Threshold (LT)**: The LTV at which a position becomes undercollateralized and eligible for liquidation.
- **Liquidation Max Limit (LML)**: The absolute maximum LTV limit. If a position's risk ratio exceeds this boundary, it is automatically absorbed by the protocol to protect liquidity providers.
- **Liquidation Penalty**: The discount percentage offered to liquidators when they repay debt on behalf of a risky position.
- **Rebalance**: An operation that synchronizes the upper protocol layer's accounting (Vaults/Lending) with its actual position on the Liquidity layer. It also syncs the orderbook to account for any active accrued rewards.
- **Tick-based Architecture**: The Vaults protocol groups positions into "ticks" based on their risk level (debt-to-collateral ratio). This allows the protocol to efficiently manage risk and process liquidations at scale.
- **Dust Borrow**: A tiny residual amount of debt intentionally kept on positions to handle division rounding complexities.
- **Sentinel Values**: Constants like `MAX_WITHDRAW_AMOUNT` and `MAX_REPAY_AMOUNT` that tell the protocol to dynamically calculate and withdraw/repay the maximum mathematically possible amount for a position.

---

# 2. Reading Data (@jup-ag/lend-read)

The read SDK uses a unified `Client` to query Liquidity, Lending, and Vault modules. All queries are **read-only** and fetch decoded on-chain accounts via RPC. This is how integrators find available markets, rates, and existing user positions.

### Quick Start (Read SDK)

```typescript
import { Client } from "@jup-ag/lend-read";
import { Connection, PublicKey } from "@solana/web3.js";

// Initialize with a connection
const connection = new Connection("https://api.mainnet-beta.solana.com");
const client = new Client(connection);
```

### Finding User Vault Positions

Before making Vault operations (like deposit, borrow, or repay), you need to know a user's existing `positionId` (which maps to an NFT).

```typescript
const userPublicKey = new PublicKey("YOUR_WALLET_PUBKEY");

// Retrieve all positions owned by the user
// Returns both the user position details and the corresponding Vault data
const { userPositions_, vaultsData_ } = await client.vault.positionsByUser(userPublicKey);

for (let i = 0; i < userPositions_.length; i++) {
  console.log(`Position ID (nftId): ${userPositions_[i].nftId}`);
  console.log(`Vault ID: ${vaultsData_[i].constantVariables.vaultId}`);
  console.log(`Collateral Supplied: ${userPositions_[i].supply}`);
  console.log(`Debt Borrowed: ${userPositions_[i].borrow}`);
}
```

### Liquidity Module

Access liquidity pool data, interest rates, and user supply/borrow positions.

```typescript
const USDC = new PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v");

// Get market data for a token (rates, prices, utilization)
const data = await client.liquidity.getOverallTokenData(USDC);

// View rates (basis points: 10000 = 100%)
const supplyApr = Number(data.supplyRate) / 100;
const borrowApr = Number(data.borrowRate) / 100;
```

### Lending Module (jlTokens)

Access jlToken (Jupiter Lend token) markets, exchange prices, and user positions.

```typescript
// Get all jlToken details at once
const allDetails = await client.lending.getAllJlTokenDetails();

// Get user's jlToken balance
const position = await client.lending.getUserPosition(USDC, userPublicKey);
```

### Vault Module & Discovery

Access vault configurations, positions, exchange prices, and liquidation data. This is crucial for dynamically listing all available leverage markets.

```typescript
// Discover all available vaults
const allVaults = await client.vault.getAllVaultsAddresses();
const totalVaults = await client.vault.getTotalVaults();

// Get comprehensive vault data (config + state + rates + limits) for a specific vault
const vaultId = 1;
const vaultData = await client.vault.getVaultByVaultId(vaultId);

// Check borrowing limits dynamically before prompting users
const borrowLimit = vaultData.limitsAndAvailability.borrowLimit;
const borrowable = vaultData.limitsAndAvailability.borrowable;
```

---

# 3. Writing Data (@jup-ag/lend)

All write operations generate instructions (`ixs`) and Address Lookup Tables (`addressLookupTableAccounts`) that must be wrapped in a **versioned (v0) transaction**.

## Lending (Earn)

Deposit underlying assets to receive yield-bearing tokens, or withdraw them.

```typescript
import { getDepositIxs, getWithdrawIxs } from "@jup-ag/lend/earn";
import BN from "bn.js";

// Deposit 1 USDC (assuming 6 decimals)
const { ixs: depositIxs } = await getDepositIxs({
  amount: new BN(1_000_000),
  asset: USDC_PUBKEY,
  signer: userPublicKey,
  connection,
});

// Withdraw
const { ixs: withdrawIxs } = await getWithdrawIxs({
  amount: new BN(100_000),
  asset: USDC_PUBKEY,
  signer: userPublicKey,
  connection,
});
```

## Vaults (Borrow)

Vaults handle collateral deposits and debt borrowing. **All vault operations use the `getOperateIx` function.**

The direction of the operation is determined by the sign of `colAmount` and `debtAmount`:

- **Deposit**: `colAmount` > 0, `debtAmount` = 0
- **Withdraw**: `colAmount` < 0, `debtAmount` = 0
- **Borrow**: `colAmount` = 0, `debtAmount` > 0
- **Repay**: `colAmount` = 0, `debtAmount` < 0

> **Important**: If `positionId` is `0`, a new position NFT is created, and the SDK returns the new `positionId`.

### Common Vault Patterns

**1. Deposit Collateral**

```typescript
import { getOperateIx } from "@jup-ag/lend/borrow";

// Deposit 1 token (base units)
const { ixs, addressLookupTableAccounts, positionId: newPositionId } = await getOperateIx({
  vaultId: 1,
  positionId: 0, // 0 = create new position
  colAmount: new BN(1_000_000), // Positive = Deposit
  debtAmount: new BN(0),
  connection,
  signer,
});
```

**2. Borrow Debt**

```typescript
// Borrow 0.5 tokens against existing position
const { ixs, addressLookupTableAccounts } = await getOperateIx({
  vaultId: 1,
  positionId: EXISTING_POSITION_ID, // Use the nftId retrieved from the read SDK
  colAmount: new BN(0),
  debtAmount: new BN(500_000), // Positive = Borrow
  connection,
  signer,
});
```

**3. Repay Debt (Using Max Sentinel)**
When users want to repay their *entire* debt, do not try to calculate exact dust amounts. Use the `MAX_REPAY_AMOUNT` sentinel exported by the SDK.

```typescript
import { getOperateIx, MAX_REPAY_AMOUNT } from "@jup-ag/lend/borrow";

const { ixs, addressLookupTableAccounts } = await getOperateIx({
  vaultId: 1,
  positionId: EXISTING_POSITION_ID,
  colAmount: new BN(0),
  debtAmount: MAX_REPAY_AMOUNT, // Tells the protocol to clear the full debt
  connection,
  signer,
});
```

**4. Withdraw Collateral (Using Max Sentinel)**
Similarly, to withdraw all available collateral, use the `MAX_WITHDRAW_AMOUNT` sentinel.

```typescript
import { getOperateIx, MAX_WITHDRAW_AMOUNT } from "@jup-ag/lend/borrow";

const { ixs, addressLookupTableAccounts } = await getOperateIx({
  vaultId: 1,
  positionId: EXISTING_POSITION_ID,
  colAmount: MAX_WITHDRAW_AMOUNT, // Tells the protocol to withdraw everything
  debtAmount: new BN(0),
  connection,
  signer,
});
```

**5. Combined operate**

You can batch multiple operations—such as depositing + borrowing, or repaying + withdrawing—in a single transaction using `getOperateIx`:

- **a. Deposit + Borrow in one Tx:**
  Pass both `colAmount` and `debtAmount` to deposit collateral and borrow simultaneously.

  ```typescript
  const { ixs, addressLookupTableAccounts } = await getOperateIx({
    vaultId: 1,
    positionId: 0, // Create new position
    colAmount: new BN(1_000_000), // Deposit collateral
    debtAmount: new BN(500_000),  // Borrow
    connection,
    signer,
  });
  ```

- **b. Repay + Withdraw in one Tx:**
  Repay debt and withdraw collateral at once. Use max sentinels for a full repayment or to withdraw the maximum available.

  ```typescript
  import { getOperateIx, MAX_WITHDRAW_AMOUNT, MAX_REPAY_AMOUNT } from "@jup-ag/lend/borrow";

  const { ixs, addressLookupTableAccounts } = await getOperateIx({
    vaultId: 1,
    positionId: EXISTING_POSITION_ID,
    colAmount: MAX_WITHDRAW_AMOUNT, // Withdraw all collateral
    debtAmount: MAX_REPAY_AMOUNT,   // Repay all debt
    connection,
    signer,
  });
  ```

---

# 4. Jupiter Lend Build Kit

The Jupiter Lend Build Kit provides UI components, utilities, and extensive documentation to easily integrate Jupiter Lend into your application. It serves as a comprehensive reference for both humans and AI agents.

- **Staging Documentation**: [instadapp.mintlify.app](https://instadapp.mintlify.app) (Currently available at `instadapp.mintlify.app`)

*(Note: The build kit is currently in development on staging. Production URLs will be updated here once officially deployed.)*

### Build Kit Documentation Index

The Build Kit documentation covers the following core integration topics. When referencing the build kit, you can explore these pages for specific examples and concepts:

**Developers & Core Concepts:**
- `overview`: Core concepts and getting started.
- `api-vs-sdk`: Guidance on choosing between the Jupiter API and the `@jup-ag/lend` SDKs for integration.

**Earn Module (Lending):**
- `earn-overview`: Fetching market configurations, supply caps, and yield metrics for tokens.
- `user-position`: Fetching a user's supplied balance and accrued yield.
- **Operations**:
  - `deposit-earn`: Supplying assets to the protocol.
  - `withdraw-earn`: Removing supplied assets and yield.

**Borrow Module (Vaults):**
- `overview-borrow`: Core Vault concepts, LTV limits, and borrowing caps.
- `vault-data`: Fetching dynamic vault configurations, risk metrics, rates, and limits.
- **Operations**:
  - `create-position`: Minting a new position NFT to start borrowing.
  - `deposit-borrow`: Supplying collateral to a specific vault.
  - `borrow`: Drawing debt against deposited collateral.
  - `repay`: Repaying outstanding debt.
  - `withdraw-borrow`: Withdrawing deposited collateral.
  - `operate-combined`: Batching multiple actions (e.g., Deposit + Borrow, Repay + Withdraw) in a single transaction.
  - `liquidate`: Mechanics of liquidating unhealthy positions.

**Flashloan Module:**
- `flashloan-overview`: Core concepts and use cases for flashloans.
- `flashloan-operate`: Executing flashloans using `getFlashloanIx` with custom intermediate logic.

**Resources:**
- `program-addresses`: Official Mainnet Program IDs for Liquidity, Lending, Vaults, and Oracles.
- `idl-and-types`: Accessing raw IDLs for building CPIs and parsing on-chain state.


---

# 5. Complete Working Examples

> Copy-paste-ready scripts. Install dependencies: `npm install @solana/web3.js bn.js @jup-ag/lend @jup-ag/lend-read`

### Example 1 — Discover Position and Deposit (Read then Write)

This example demonstrates how to use the read-only SDK (`@jup-ag/lend-read`) to query a user's existing vault positions. If a position for the target vault exists, it uses that NFT ID. If not, it falls back to creating a new position. Finally, it uses the write SDK (`@jup-ag/lend`) to deposit collateral into the position.

```typescript
import {
  Connection,
  Keypair,
  PublicKey,
  TransactionMessage,
  VersionedTransaction,
} from "@solana/web3.js";
import BN from "bn.js";
import { Client } from "@jup-ag/lend-read";
import { getOperateIx } from "@jup-ag/lend/borrow";
import fs from "fs";
import path from "path";

const KEYPAIR_PATH = "/path/to/your/keypair.json";
const RPC_URL = "https://api.mainnet-beta.solana.com";
const VAULT_ID = 1;

const DEPOSIT_AMOUNT = new BN(1_000_000);

function loadKeypair(keypairPath: string): Keypair {
  const fullPath = path.resolve(keypairPath);
  const secret = JSON.parse(fs.readFileSync(fullPath, "utf8"));
  return Keypair.fromSecretKey(new Uint8Array(secret));
}

async function main() {
  const userKeypair = loadKeypair(KEYPAIR_PATH);
  const connection = new Connection(RPC_URL, { commitment: "confirmed" });
  const signer = userKeypair.publicKey;

  // 1. Read Data: Find existing user positions for the vault
  const client = new Client(connection);
  const { userPositions_, vaultsData_ } = await client.vault.positionsByUser(signer);

  let targetPositionId = 0; // Default to 0 (create new position)

  // Find an existing position for our target Vault ID
  for (let i = 0; i < userPositions_.length; i++) {
    if (vaultsData_[i].constantVariables.vaultId === VAULT_ID) {
      targetPositionId = userPositions_[i].nftId;
      console.log(`Found existing position NFT: ${targetPositionId}`);
      break;
    }
  }

  if (targetPositionId === 0) {
    console.log("No existing position found. Will create a new one.");
  }

  // 2. Write Data: Execute deposit
  const { ixs, addressLookupTableAccounts, nftId } = await getOperateIx({
    vaultId: VAULT_ID,
    positionId: targetPositionId,
    colAmount: DEPOSIT_AMOUNT,
    debtAmount: new BN(0), // Deposit only
    connection,
    signer,
  });

  if (!ixs?.length) throw new Error("No instructions returned.");

  // 3. Build the V0 Transaction Message
  const latestBlockhash = await connection.getLatestBlockhash();
  const message = new TransactionMessage({
    payerKey: signer,
    recentBlockhash: latestBlockhash.blockhash,
    instructions: ixs,
  }).compileToV0Message(addressLookupTableAccounts ?? []);

  // 4. Sign and Send
  const transaction = new VersionedTransaction(message);
  transaction.sign([userKeypair]);

  const signature = await connection.sendTransaction(transaction, {
    skipPreflight: false,
    maxRetries: 3,
    preflightCommitment: "confirmed",
  });

  await connection.confirmTransaction({ signature, ...latestBlockhash }, "confirmed");

  console.log(`Deposit successful! Signature: ${signature}`);
  if (targetPositionId === 0) {
    console.log(`New position created with NFT ID: ${nftId}`);
  }
}

main().catch(console.error);
```

---

### Example 2 — Combined Operations (Deposit, Borrow, Repay, Withdraw)

This example demonstrates how to create a position, deposit collateral, and borrow debt in a single transaction. Then, it repays the debt and withdraws the collateral using the exact same `getOperateIx` function in a follow-up transaction. It also shows the critical step of **deduplicating Address Lookup Tables (ALTs)** when merging multiple instruction sets.

```typescript
import {
  Connection,
  Keypair,
  TransactionMessage,
  VersionedTransaction,
} from "@solana/web3.js";
import BN from "bn.js";
import { getOperateIx } from "@jup-ag/lend/borrow";
import fs from "fs";
import path from "path";

const KEYPAIR_PATH = "/path/to/your/keypair.json";
const RPC_URL = "https://api.mainnet-beta.solana.com";
const VAULT_ID = 1;

const DEPOSIT_AMOUNT = new BN(1_000_000);
const BORROW_AMOUNT = new BN(500_000);
const REPAY_AMOUNT = new BN(100_000);
const WITHDRAW_AMOUNT = new BN(200_000);

function loadKeypair(keypairPath: string): Keypair {
  const fullPath = path.resolve(keypairPath);
  const secret = JSON.parse(fs.readFileSync(fullPath, "utf8"));
  return Keypair.fromSecretKey(new Uint8Array(secret));
}

async function main() {
  const userKeypair = loadKeypair(KEYPAIR_PATH);
  const connection = new Connection(RPC_URL, { commitment: "confirmed" });
  const signer = userKeypair.publicKey;

  // 1. Create position + Deposit + Borrow
  const { ixs: depositBorrowIxs, addressLookupTableAccounts: depositBorrowAlts, positionId } = await getOperateIx({
    vaultId: VAULT_ID,
    positionId: 0,
    colAmount: DEPOSIT_AMOUNT,
    debtAmount: BORROW_AMOUNT,
    connection,
    signer,
  });

  // 2. Repay + Withdraw
  const repayWithdrawResult = await getOperateIx({
    vaultId: VAULT_ID,
    positionId: positionId!,
    colAmount: WITHDRAW_AMOUNT.neg(),
    debtAmount: REPAY_AMOUNT.neg(),
    connection,
    signer,
  });

  // Merge instructions
  const allIxs = [...(depositBorrowIxs ?? []), ...(repayWithdrawResult.ixs ?? [])];

  // Merge and Deduplicate Address Lookup Tables (ALTs)
  const allAlts = [
    ...(depositBorrowAlts ?? []),
    ...(repayWithdrawResult.addressLookupTableAccounts ?? []),
  ];
  const seenKeys = new Set<string>();
  const mergedAlts = allAlts.filter((alt) => {
    const k = alt.key.toString();
    if (seenKeys.has(k)) return false;
    seenKeys.add(k);
    return true;
  });

  if (!allIxs.length) throw new Error("No instructions returned.");

  // Build the V0 Transaction Message
  const latestBlockhash = await connection.getLatestBlockhash();
  const message = new TransactionMessage({
    payerKey: signer,
    recentBlockhash: latestBlockhash.blockhash,
    instructions: allIxs,
  }).compileToV0Message(mergedAlts);

  // Sign and Send
  const transaction = new VersionedTransaction(message);
  transaction.sign([userKeypair]);

  const signature = await connection.sendTransaction(transaction, {
    skipPreflight: false,
    maxRetries: 3,
    preflightCommitment: "confirmed",
  });

  await connection.confirmTransaction({ signature, ...latestBlockhash }, "confirmed");

  console.log("Combined operate successful! Signature:", signature);
}

main().catch(console.error);
```

---

# Resources

## API Documentation

- **Jupiter Lend Overview**: [dev.jup.ag/docs/lend](https://dev.jup.ag/docs/lend)
- **Lend API (Earn)**: [dev.jup.ag/docs/lend/earn](https://dev.jup.ag/docs/lend/earn) | REST API for Earn operations (deposit/withdraw)
- **Lend API (Borrow)**: *(Coming Soon)*

## SDKs

- **Read SDK (`@jup-ag/lend-read`)**: [NPM](https://www.npmjs.com/package/@jup-ag/lend-read) | Read-only SDK for querying liquidity pools, lending markets (jlTokens), and vaults
- **Write SDK (`@jup-ag/lend`)**: [NPM](https://www.npmjs.com/package/@jup-ag/lend) | Core SDK for building write transactions (deposits, withdraws, operates)

## Smart Contracts

- **Public Repository**: [Instadapp/fluid-solana-programs](https://github.com/Instadapp/fluid-solana-programs/)
- **IDLs and Types**: [IDLs & types (`/target` folder)](https://github.com/jup-ag/jupiter-lend/tree/main/target)

## Program IDs (Mainnet)


| Program                   | Address                                       |
| ------------------------- | --------------------------------------------- |
| Liquidity                 | `jupeiUmn818Jg1ekPURTpr4mFo29p46vygyykFJ3wZC` |
| Lending                   | `jup3YeL8QhtSx1e253b2FDvsMNC87fDrgQZivbrndc9` |
| Lending Reward Rate Model | `jup7TthsMgcR9Y3L277b8Eo9uboVSmu1utkuXHNUKar` |
| Vaults                    | `jupr81YtYssSyPt8jbnGuiWon5f6x9TcDEFxYe3Bdzi` |
| Oracle                    | `jupnw4B6Eqs7ft6rxpzYLJZYSnrpRgPcr589n5Kv4oc` |
| Flashloan                 | `jupgfSgfuAXv4B6R2Uxu85Z1qdzgju79s6MfZekN6XS` |
