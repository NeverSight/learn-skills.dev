---
name: polygon
description: Polygon ecosystem development — PoS chain deployment, zkEVM patterns, AggLayer interop, POL token migration, and bridging across Polygon chains.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: polygon
  category: L2 & Alt-L1
tags:
  - polygon
  - matic
  - pol
  - zkevm
  - agglayer
---

# Polygon Ecosystem Development

Build on Polygon's multi-chain ecosystem: PoS sidechain for low-cost EVM transactions, zkEVM for Ethereum-equivalent ZK rollups, and AggLayer for unified cross-chain interop.

## What You Probably Got Wrong

1. **Polygon PoS is not an L2** -- it is a commit chain (sidechain) with its own validator set that checkpoints to Ethereum. It does NOT inherit Ethereum security for individual transactions.
2. **MATIC is being replaced by POL** -- POL (0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6 on Ethereum) is the new native gas and staking token. MATIC holders must migrate via the migration contract.
3. **zkEVM and PoS are completely different chains** -- different chain IDs, different RPCs, different bridge contracts. Code that works on PoS does not automatically work on zkEVM without verifying opcode compatibility.
4. **zkEVM finality depends on proof generation** -- transactions are "trusted" quickly but only final on Ethereum after a ZK proof is submitted and verified (~30 min to hours).
5. **Gas on PoS uses POL (formerly MATIC), gas on zkEVM uses ETH** -- do not confuse the native gas tokens between chains.

## Quick Start

### Install Dependencies

```bash
# viem for TypeScript interaction
npm install viem

# Foundry for Solidity deployment
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

### Environment Setup

```bash
# .env
PRIVATE_KEY=your_private_key_here
POLYGONSCAN_API_KEY=your_polygonscan_key
POLYGON_RPC_URL=https://polygon-rpc.com
ZKEVM_RPC_URL=https://zkevm-rpc.com
```

## Chain Configuration

### Polygon PoS

| Property | Value |
|----------|-------|
| Chain ID | **137** |
| Currency | POL (18 decimals) |
| EVM Version | Shanghai |
| Block Time | ~2 seconds |
| Consensus | PoS + Heimdall (Tendermint BFT) |
| Checkpointing | Every ~30 min to Ethereum |
| Block Gas Limit | 30M |

#### RPC Endpoints (PoS Mainnet)

| URL | Provider | Notes |
|-----|----------|-------|
| `https://polygon-rpc.com` | Polygon Labs | Default public |
| `https://rpc.ankr.com/polygon` | Ankr | Public, rate limited |
| `https://polygon.llamarpc.com` | LlamaNodes | Public |
| `https://polygon-mainnet.g.alchemy.com/v2/<KEY>` | Alchemy | Authenticated |
| `https://polygon-mainnet.infura.io/v3/<KEY>` | Infura | Authenticated |

#### Block Explorers (PoS)

| Explorer | URL |
|----------|-----|
| Polygonscan | https://polygonscan.com |
| Blockscout | https://polygon.blockscout.com |
| OKLink | https://www.oklink.com/polygon |

### Polygon zkEVM

| Property | Value |
|----------|-------|
| Chain ID | **1101** |
| Currency | ETH (18 decimals) |
| ZK Type | Type-2 ZK-EVM |
| Block Time | Variable (~5-10 seconds) |
| Proof Time | ~30 min to finalize on L1 |
| Sequencer | Centralized (Polygon Labs) |

#### RPC Endpoints (zkEVM Mainnet)

| URL | Provider | Notes |
|-----|----------|-------|
| `https://zkevm-rpc.com` | Polygon Labs | Default public |
| `https://rpc.ankr.com/polygon_zkevm` | Ankr | Public |
| `https://polygonzkevm-mainnet.g.alchemy.com/v2/<KEY>` | Alchemy | Authenticated |

#### Block Explorers (zkEVM)

| Explorer | URL |
|----------|-----|
| zkEVM Explorer | https://zkevm.polygonscan.com |
| Blockscout | https://zkevm.blockscout.com |

### Testnets

| Network | Chain ID | Currency | Faucet |
|---------|----------|----------|--------|
| Amoy (PoS testnet) | **80002** | POL | https://faucet.polygon.technology |
| Cardona (zkEVM testnet) | **2442** | ETH | https://faucet.polygon.technology |

#### Testnet RPCs

| Network | URL |
|---------|-----|
| Amoy | `https://rpc-amoy.polygon.technology` |
| Cardona | `https://rpc.cardona.zkevm-rpc.com` |

## Deployment

### Foundry (Polygon PoS)

```bash
# Deploy to Polygon PoS mainnet
forge create src/MyContract.sol:MyContract \
  --rpc-url https://polygon-rpc.com \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --verifier-url https://api.polygonscan.com/api \
  --etherscan-api-key $POLYGONSCAN_API_KEY

# Deploy to Amoy testnet
forge create src/MyContract.sol:MyContract \
  --rpc-url https://rpc-amoy.polygon.technology \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --verifier-url https://api-amoy.polygonscan.com/api \
  --etherscan-api-key $POLYGONSCAN_API_KEY
```

### Foundry (Polygon zkEVM)

```bash
# Deploy to zkEVM mainnet
forge create src/MyContract.sol:MyContract \
  --rpc-url https://zkevm-rpc.com \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --verifier-url https://api-zkevm.polygonscan.com/api \
  --etherscan-api-key $POLYGONSCAN_API_KEY
```

### Hardhat Configuration

```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    polygon: {
      url: process.env.POLYGON_RPC_URL || "https://polygon-rpc.com",
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 137,
    },
    amoy: {
      url: "https://rpc-amoy.polygon.technology",
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 80002,
    },
    zkevm: {
      url: process.env.ZKEVM_RPC_URL || "https://zkevm-rpc.com",
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 1101,
    },
    cardona: {
      url: "https://rpc.cardona.zkevm-rpc.com",
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 2442,
    },
  },
  etherscan: {
    apiKey: {
      polygon: process.env.POLYGONSCAN_API_KEY!,
      polygonAmoy: process.env.POLYGONSCAN_API_KEY!,
      polygonZkEVM: process.env.POLYGONSCAN_API_KEY!,
    },
  },
};

export default config;
```

### Verification

```bash
# Verify on Polygonscan (PoS)
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --chain-id 137 \
  --verifier-url https://api.polygonscan.com/api \
  --etherscan-api-key $POLYGONSCAN_API_KEY

# Verify on zkEVM explorer
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --chain-id 1101 \
  --verifier-url https://api-zkevm.polygonscan.com/api \
  --etherscan-api-key $POLYGONSCAN_API_KEY
```

## Polygon PoS Architecture

Polygon PoS is a commit chain (sidechain) with its own validator set:

- **Bor**: Block production layer (modified Geth). Validators take turns producing blocks in "spans" (~6400 blocks).
- **Heimdall**: Consensus and checkpoint layer (Tendermint BFT). Selects block producers, validates blocks, and submits checkpoints to Ethereum.
- **Checkpoints**: State roots submitted to Ethereum `RootChain` contract every ~30 minutes. This provides data availability, NOT execution validity.
- **Validator Set**: ~100 validators with POL staking. Delegators can stake via `ValidatorShare` contracts.

### PoS Key Contracts (Ethereum L1)

| Contract | Address | Purpose |
|----------|---------|---------|
| RootChain | `0x86E4Dc95c7FBdBf52e33D563BbDB00823894C287` | Checkpoint submission |
| StateSender | `0x28e4F3a7f651294B9564800b2D01f35189A5bFbE` | L1 -> L2 state sync |
| StakeManager | `0x5e3Ef299fDDf15eAa0432E6e66473ace8c13D908` | Validator staking |
| RootChainManager | `0xA0c68C638235ee32657e8f720a23ceC1bFc77C77` | Bridge deposits |
| POL Token | `0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6` | Native token (Ethereum) |
| MATIC Token | `0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0` | Legacy token (Ethereum) |

*Last verified: 2025-12-01*

### PoS Key Contracts (Polygon Chain)

| Contract | Address | Purpose |
|----------|---------|---------|
| ChildChainManager | `0xA6FA4fB5f76172d178d61B04b0ecd319C5d1C0aa` | Bridge withdrawals |
| WPOL (Wrapped POL) | `0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270` | Wrapped native token |
| WETH | `0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619` | Wrapped Ether |
| USDC | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | Native USDC |
| USDC.e | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | Bridged USDC |

*Last verified: 2025-12-01*

## Polygon zkEVM

Polygon zkEVM is a Type-2 ZK-EVM rollup. It aims for full EVM equivalence, meaning standard Solidity contracts deploy without modification in most cases.

### How It Works

1. **Sequencer** receives transactions and produces L2 batches.
2. **Aggregator** generates ZK proofs for batches.
3. **Proofs are verified** on Ethereum via the `PolygonZkEVM` contract.
4. **State transitions** become final on L1 once proof is accepted (~30 min to hours).

### Transaction States on zkEVM

| State | Meaning | Time |
|-------|---------|------|
| Trusted | Sequencer included it | Seconds |
| Virtual | Batch posted to L1 | Minutes |
| Consolidated | ZK proof verified on L1 | ~30 min to hours |

### EVM Compatibility Notes

zkEVM targets full EVM equivalence but some edge cases differ:

- `DIFFICULTY` / `PREVRANDAO` opcode returns `0` (no randomness source like Ethereum beacon chain)
- `SELFDESTRUCT` is disabled (per EIP-6049 deprecation)
- Precompiled contracts: `ecAdd`, `ecMul`, `ecPairing` behave identically; `modexp` may have higher gas costs
- `BLOCKHASH` only returns hashes for the last 256 blocks (same as Ethereum spec, but be aware proof timing may affect behavior)
- Gas costs for some operations differ slightly due to proof generation overhead

### zkEVM Gas Model

Gas on zkEVM is paid in ETH. The cost includes:

- **L2 execution gas**: Similar to Ethereum gas pricing
- **L1 data availability cost**: Posting batch data to Ethereum
- **Proof overhead**: Indirectly amortized across all transactions in a batch

```typescript
import { createPublicClient, http } from "viem";
import { polygonZkEvm } from "viem/chains";

const zkEvmClient = createPublicClient({
  chain: polygonZkEvm,
  transport: http("https://zkevm-rpc.com"),
});

const gasPrice = await zkEvmClient.getGasPrice();
const estimatedGas = await zkEvmClient.estimateGas({
  account: "0xYourAddress",
  to: "0xRecipient",
  value: 0n,
  data: "0x...",
});

const totalCostWei = gasPrice * estimatedGas;
```

## POL Token

POL replaced MATIC as Polygon's native token via a migration contract on Ethereum.

### Migration (MATIC to POL)

The migration is 1:1. Call the migration contract on Ethereum:

```typescript
import { createWalletClient, http, parseAbi } from "viem";
import { mainnet } from "viem/chains";

// Migration contract on Ethereum
// Converts MATIC -> POL at 1:1 ratio
const MIGRATION_CONTRACT = "0x29e7DF7b6c1264C3F63e2E7bB27143EeB8A05fe3" as const;

const migrationAbi = parseAbi([
  "function migrate(uint256 amount) external",
  "function unmigrate(uint256 amount) external",
]);

const MATIC_TOKEN = "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0" as const;
const POL_TOKEN = "0x455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6" as const;

// Step 1: Approve MATIC spend
// Step 2: Call migrate()
```

### POL Staking

POL is staked on Ethereum via the `StakeManager` contract. Delegators use `ValidatorShare` contracts:

```typescript
import { parseAbi } from "viem";

const validatorShareAbi = parseAbi([
  "function buyVoucher(uint256 _amount, uint256 _minSharesToMint) external returns (uint256)",
  "function sellVoucher_new(uint256 claimAmount, uint256 maximumSharesToBurn) external",
  "function restake() external returns (uint256, uint256)",
  "function withdrawRewards() external",
  "function getLiquidRewards(address user) external view returns (uint256)",
  "function getTotalStake(address user) external view returns (uint256, uint256)",
]);
```

## AggLayer

AggLayer (Aggregation Layer) is Polygon's vision for unifying multiple chains under a single ZK-proven interop layer.

### Core Concepts

- **Unified Bridge**: Single bridge contract on Ethereum shared by all AggLayer-connected chains. Each chain gets a unique `networkId`.
- **Pessimistic Proofs**: AggLayer validates cross-chain claims using pessimistic proofs -- it assumes the worst case and only releases funds if the proof confirms solvency.
- **Chain Interop**: Chains connected to AggLayer can transfer assets without going through Ethereum L1 as intermediary. Assets move via the LxLy bridge with AggLayer verification.
- **Shared Liquidity**: All chains on AggLayer share a unified liquidity pool, reducing fragmentation.

### AggLayer Architecture

```
┌──────────────────────────────────────────────┐
│                   Ethereum                    │
│  ┌─────────────────────────────────────────┐  │
│  │          Unified Bridge Contract         │  │
│  │  (shared by all AggLayer chains)         │  │
│  └─────────────────────────────────────────┘  │
│         ▲              ▲             ▲         │
│   Proofs│        Proofs│       Proofs│         │
│         │              │             │         │
│  ┌──────┴──────────────┴─────────────┴──────┐ │
│  │              AggLayer                     │ │
│  │   (pessimistic proof verification)        │ │
│  └──────┬──────────────┬─────────────┬──────┘ │
└─────────┼──────────────┼─────────────┼────────┘
          │              │             │
   ┌──────┴──┐    ┌──────┴──┐   ┌─────┴───┐
   │  PoS    │    │  zkEVM  │   │  CDK     │
   │  Chain  │    │  Chain  │   │  Chain   │
   └─────────┘    └─────────┘   └──────────┘
```

## Bridging

### PoS Bridge (Polygon PoS <-> Ethereum)

The PoS bridge uses `RootChainManager` (Ethereum) and `ChildChainManager` (Polygon PoS).

**Deposit (Ethereum -> Polygon PoS):**

1. Approve token to `RootChainManager`'s `ERC20Predicate`
2. Call `RootChainManager.depositFor(user, rootToken, depositData)`
3. Wait ~7-8 minutes for state sync to Polygon PoS

**Withdraw (Polygon PoS -> Ethereum):**

1. Burn tokens on Polygon PoS (transfer to `0x0` or call burn function)
2. Wait for checkpoint inclusion (~30 minutes)
3. Call `RootChainManager.exit(burnTxProof)` on Ethereum

```typescript
import { createWalletClient, http, parseAbi, encodePacked } from "viem";
import { mainnet, polygon } from "viem/chains";

const ROOT_CHAIN_MANAGER = "0xA0c68C638235ee32657e8f720a23ceC1bFc77C77" as const;
const ERC20_PREDICATE = "0x40ec5B33f54e0E8A33A975908C5BA1c14e5BbbDf" as const;

const rootChainManagerAbi = parseAbi([
  "function depositFor(address user, address rootToken, bytes calldata depositData) external",
  "function exit(bytes calldata inputData) external",
]);

// depositData is ABI-encoded amount
// encodePacked would be wrong here -- use encodeAbiParameters
import { encodeAbiParameters, parseAbiParameters } from "viem";

const depositData = encodeAbiParameters(
  parseAbiParameters("uint256"),
  [1000000n] // amount in token's smallest unit
);
```

### zkEVM LxLy Bridge (zkEVM <-> Ethereum)

The zkEVM uses the LxLy bridge contract (also used by AggLayer chains).

**Bridge Asset (L1 -> zkEVM):**

```typescript
const ZKEVM_BRIDGE = "0x2a3DD3EB832aF982ec71669E178424b10Dca2EDe" as const;

const bridgeAbi = parseAbi([
  "function bridgeAsset(uint32 destinationNetwork, address destinationAddress, uint256 amount, address token, bool forceUpdateGlobalExitRoot, bytes calldata permitData) external payable",
  "function claimAsset(bytes32[32] calldata smtProofLocalExitRoot, bytes32[32] calldata smtProofRollupExitRoot, uint256 globalIndex, bytes32 mainnetExitRoot, bytes32 rollupExitRoot, uint32 originNetwork, address originTokenAddress, uint32 destinationNetwork, address destinationAddress, uint256 amount, bytes calldata metadata) external",
]);

// networkId 0 = Ethereum mainnet
// networkId 1 = Polygon zkEVM mainnet
```

**Claiming on Destination:**

After the bridge transaction is included and proof is generated, call `claimAsset` on the destination chain with the Merkle proof from the bridge API.

### Bridge Monitoring

```typescript
// Polygon PoS bridge API
const POS_BRIDGE_API = "https://proof-generator.polygon.technology/api/v1";

// Check if checkpoint included (for PoS withdrawals)
const checkpointStatus = await fetch(
  `${POS_BRIDGE_API}/matic/block-included/${blockNumber}?networkType=mainnet`
);

// zkEVM bridge API
const ZKEVM_BRIDGE_API = "https://bridge-api.zkevm-rpc.com";

// Get bridge deposit status
const depositStatus = await fetch(
  `${ZKEVM_BRIDGE_API}/bridges/${depositAddress}?offset=0&limit=25`
);

// Get Merkle proof for claiming
const merkleProof = await fetch(
  `${ZKEVM_BRIDGE_API}/merkle-proof?deposit_cnt=${depositCount}&net_id=${networkId}`
);
```

## Gas Model

### Polygon PoS

- Gas is paid in POL (native token, formerly MATIC)
- Gas prices typically 30-100 gwei, significantly lower than Ethereum
- EIP-1559 is supported (base fee + priority fee)
- During congestion, gas can spike to 500+ gwei

```typescript
import { createPublicClient, http } from "viem";
import { polygon } from "viem/chains";

const posClient = createPublicClient({
  chain: polygon,
  transport: http("https://polygon-rpc.com"),
});

const gasPrice = await posClient.getGasPrice();
const block = await posClient.getBlock();
// block.baseFeePerGas gives current base fee
```

### Polygon zkEVM

- Gas is paid in ETH
- Pricing reflects L2 execution + L1 data posting cost
- Generally cheaper than Ethereum mainnet but more expensive than PoS
- Gas varies with L1 gas prices (data availability cost)

## Ecosystem

### Major Protocols on Polygon PoS

| Protocol | Category | Notes |
|----------|----------|-------|
| QuickSwap | DEX | Largest Polygon-native DEX, UniV3-style |
| Aave V3 | Lending | Major lending market on Polygon |
| Uniswap V3 | DEX | Deployed on PoS |
| Balancer | DEX | Multi-token pools |
| Curve | DEX | Stablecoin DEX |
| 0x / Matcha | Aggregator | DEX aggregation |
| Polymarket | Prediction | Largest prediction market (on PoS) |

### Infrastructure

| Service | Purpose |
|---------|---------|
| Polygonscan | Block explorer and verification |
| The Graph | Subgraph indexing (PoS + zkEVM) |
| Chainlink | Oracle feeds on PoS and zkEVM |
| Gelato | Automation and relaying |
| Polygon CDK | Chain Development Kit for custom chains |

## Key Differences: PoS vs zkEVM vs Ethereum

| Feature | Polygon PoS | Polygon zkEVM | Ethereum |
|---------|------------|---------------|----------|
| Chain ID | 137 | 1101 | 1 |
| Gas Token | POL | ETH | ETH |
| Consensus | Tendermint BFT | ZK rollup | PoS (Casper) |
| Block Time | ~2s | ~5-10s | ~12s |
| Finality | ~30 min (checkpoint) | ~30 min (proof) | ~13 min |
| Security Model | Own validators | Ethereum (ZK proof) | Native |
| EVM Compat | Full | Type-2 ZK-EVM | Native |
| Gas Cost | Very low | Low-medium | High |
| Decentralization | ~100 validators | Centralized sequencer | ~900k validators |

## Viem Chain Definitions

```typescript
import { defineChain } from "viem";

// Polygon PoS (built into viem)
import { polygon } from "viem/chains";

// Polygon zkEVM (built into viem)
import { polygonZkEvm } from "viem/chains";

// Amoy testnet (built into viem)
import { polygonAmoy } from "viem/chains";

// Cardona testnet (may need manual definition)
const polygonZkEvmCardona = defineChain({
  id: 2442,
  name: "Polygon zkEVM Cardona",
  nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://rpc.cardona.zkevm-rpc.com"] },
  },
  blockExplorers: {
    default: { name: "Blockscout", url: "https://cardona-zkevm.polygonscan.com" },
  },
  testnet: true,
});
```

## Resources

- [Polygon Documentation](https://docs.polygon.technology)
- [Polygon zkEVM Docs](https://docs.polygon.technology/zkEVM)
- [AggLayer Docs](https://docs.polygon.technology/agglayer)
- [Polygonscan](https://polygonscan.com)
- [zkEVM Explorer](https://zkevm.polygonscan.com)
- [Polygon Faucet](https://faucet.polygon.technology)
- [Polygon CDK](https://docs.polygon.technology/cdk)
- [POL Token Migration](https://polygon.technology/pol)
- [Bridge UI](https://portal.polygon.technology/bridge)

## Skill Structure

```
polygon/
├── SKILL.md                        # This file
├── examples/
│   ├── deploy-contract/            # Deployment to PoS and zkEVM
│   ├── bridge-tokens/              # PoS bridge and LxLy bridge
│   ├── zkevm-patterns/             # zkEVM-specific patterns
│   └── pol-staking/                # POL staking and delegation
├── resources/
│   ├── contract-addresses.md       # All key addresses
│   └── error-codes.md             # Common errors
├── docs/
│   └── troubleshooting.md         # Common issues and fixes
└── templates/
    └── polygon-client.ts          # Starter template
```
