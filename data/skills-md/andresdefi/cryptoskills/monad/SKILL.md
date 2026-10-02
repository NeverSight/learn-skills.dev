---
name: monad
description: Monad L1 development — parallel execution, MonadBFT consensus, 400ms blocks, gas-limit charging, opcode repricing, staking precompile, and deployment patterns.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: monad
  category: L2 & Alt-L1
tags:
  - monad
  - parallel-execution
  - monadbft
  - evm-compatible
---

# Monad L1 Development

## Chain Configuration

### Mainnet

| Property | Value |
|----------|-------|
| Chain ID | **143** |
| Currency | MON (18 decimals) |
| EVM Version | Pectra fork |
| Block Time | 400ms |
| Finality | 800ms (2 slots) |
| Block Gas Limit | 200M |
| Tx Gas Limit | 30M |
| Gas Throughput | 500M gas/sec |
| Min Base Fee | 100 MON-gwei |
| Node Version | v0.12.7 / MONAD_EIGHT |

#### RPC Endpoints (Mainnet)

| URL | Provider | Rate Limit | Batch | Notes |
|-----|----------|------------|-------|-------|
| `https://rpc.monad.xyz` / `wss://rpc.monad.xyz` | QuickNode | 25 rps | 100 | Default |
| `https://rpc1.monad.xyz` / `wss://rpc1.monad.xyz` | Alchemy | 15 rps | 100 | No debug/trace |
| `https://rpc2.monad.xyz` / `wss://rpc2.monad.xyz` | Goldsky Edge | 300/10s | 10 | Historical state |
| `https://rpc3.monad.xyz` / `wss://rpc3.monad.xyz` | Ankr | 300/10s | 10 | No debug |
| `https://rpc-mainnet.monadinfra.com` / `wss://rpc-mainnet.monadinfra.com` | MF | 20 rps | 1 | Historical state |

#### Block Explorers

| Explorer | URL |
|----------|-----|
| MonadVision | https://monadvision.com |
| Monadscan | https://monadscan.com |
| Socialscan | https://monad.socialscan.io |
| Visualization | https://gmonads.com |
| Traces | Phalcon Explorer, Tenderly |
| UserOps | Jiffyscan |

### Testnet

| Property | Value |
|----------|-------|
| Chain ID | **10143** |
| RPC | `https://testnet-rpc.monad.xyz` |
| WebSocket | `wss://testnet-rpc.monad.xyz` |
| Explorer | https://testnet.monadexplorer.com |
| Faucet | https://testnet.monad.xyz |

## Key Differences from Ethereum

| Feature | Ethereum | Monad |
|---------|----------|-------|
| Block time | 12s | 400ms |
| Finality | ~12-18 min | 800ms (2 slots) |
| Throughput | ~10 TPS | 10,000+ TPS |
| Gas charging | Gas **used** | Gas **limit** |
| Max contract size | 24.5 KB | **128 KB** |
| Blob txns (EIP-4844) | Supported | **Not supported** |
| Global mempool | Yes | **No** (leader-based forwarding) |
| Account cold access | 2,600 gas | **10,100 gas** |
| Storage cold access | 2,100 gas | **8,100 gas** |
| Reserve balance | None | **~10 MON** per account |
| `TIMESTAMP` granularity | 1 per block | 2-3 blocks share same second |
| Precompile 0x0100 | N/A | **EIP-7951 secp256r1 (P256)** |
| EIP-7702 min balance | None | **10 MON** for delegated EOAs |
| EIP-7702 CREATE/CREATE2 | Allowed | **Banned** for delegated EOAs |
| Tx types supported | 0,1,2,3,4 | 0,1,2,4 (**no type 3**) |

## Gas Limit Charging Model

Monad charges `gas_limit * price_per_gas`, NOT `gas_used * price_per_gas`. This enables asynchronous execution — execution happens after consensus, so gas used isn't known at inclusion time.

```
gas_paid = gas_limit * price_per_gas
price_per_gas = min(base_price_per_gas + priority_price_per_gas, max_price_per_gas)
```

Set gas limits explicitly for fixed-cost operations (e.g., 21000 for transfers) to avoid overpaying.

### Reserve Balance

Every account maintains a ~10 MON reserve for gas across the next 3 blocks. Transactions that would reduce balance below this threshold are rejected. This prevents DoS during asynchronous execution.

## Block Lifecycle & Finality

```
Proposed → Voted (speculative finality, T+1) → Finalized (T+2) → Verified/state root (T+5)
```

| Phase | Latency | When to Use |
|-------|---------|-------------|
| Voted | 400ms | UI updates, most dApps |
| Finalized | 800ms | Conservative apps |
| Verified | ~2s | Exchanges, bridges, stablecoins |

## Quick Start: viem Chain Definition

```typescript
import { defineChain } from "viem";

export const monad = defineChain({
  id: 143,
  name: "Monad",
  nativeCurrency: { name: "MON", symbol: "MON", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://rpc.monad.xyz"], webSocket: ["wss://rpc.monad.xyz"] },
  },
  blockExplorers: {
    default: { name: "MonadVision", url: "https://monadvision.com" },
    monadscan: { name: "Monadscan", url: "https://monadscan.com" },
  },
});

export const monadTestnet = defineChain({
  id: 10143,
  name: "Monad Testnet",
  nativeCurrency: { name: "MON", symbol: "MON", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://testnet-rpc.monad.xyz"], webSocket: ["wss://testnet-rpc.monad.xyz"] },
  },
  blockExplorers: {
    default: { name: "Monad Explorer", url: "https://testnet.monadexplorer.com" },
  },
  testnet: true,
});
```

## Quick Start: Foundry Setup

### Install Monad Foundry Fork

```bash
curl -L https://raw.githubusercontent.com/category-labs/foundry/monad/foundryup/install | bash
foundryup --network monad
```

### Project Init

```bash
forge init --template monad-developers/foundry-monad my-project
```

### foundry.toml

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
evm_version = "prague"

[rpc_endpoints]
monad = "https://rpc.monad.xyz"
monad_testnet = "https://testnet-rpc.monad.xyz"

[etherscan]
monad = { key = "${ETHERSCAN_API_KEY}", chain = 143, url = "https://api.etherscan.io/v2/api?chainid=143" }
monad_testnet = { key = "${ETHERSCAN_API_KEY}", chain = 10143, url = "https://api.etherscan.io/v2/api?chainid=10143" }
```

## Quick Start: Hardhat Configuration (v2)

```typescript
const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.28",
    settings: {
      evmVersion: "prague",
      metadata: { bytecodeHash: "ipfs" },
    },
  },
  networks: {
    monadTestnet: {
      url: "https://testnet-rpc.monad.xyz",
      chainId: 10143,
      accounts: [process.env.PRIVATE_KEY!],
    },
    monadMainnet: {
      url: "https://rpc.monad.xyz",
      chainId: 143,
      accounts: [process.env.PRIVATE_KEY!],
    },
  },
  etherscan: {
    customChains: [{
      network: "monadMainnet",
      chainId: 143,
      urls: {
        apiURL: "https://api.etherscan.io/v2/api?chainid=143",
        browserURL: "https://monadscan.com",
      },
    }],
  },
  sourcify: {
    enabled: true,
    apiUrl: "https://sourcify-api-monad.blockvision.org",
    browserUrl: "https://monadvision.com",
  },
};
```

## Deployment

### Foundry Deploy (Keystore)

```bash
cast wallet import monad-deployer --private-key $(cast wallet new | grep 'Private key:' | awk '{print $3}')

forge create src/MyContract.sol:MyContract \
  --account monad-deployer \
  --rpc-url https://rpc.monad.xyz \
  --broadcast

forge create src/MyToken.sol:MyToken \
  --account monad-deployer \
  --rpc-url https://rpc.monad.xyz \
  --constructor-args "MyToken" "MTK" 18 \
  --broadcast
```

### Foundry Deploy (Script)

```bash
forge script script/Deploy.s.sol \
  --account monad-deployer \
  --rpc-url https://rpc.monad.xyz \
  --broadcast \
  --slow
```

### Hardhat Deploy

```bash
npx hardhat ignition deploy ignition/modules/Counter.ts --network monadMainnet
npx hardhat ignition deploy ignition/modules/Counter.ts --network monadMainnet --reset
```

## Verification

### MonadVision (Sourcify)

```bash
forge verify-contract <address> <ContractName> \
  --chain 143 \
  --verifier sourcify \
  --verifier-url https://sourcify-api-monad.blockvision.org/
```

### Monadscan (Etherscan)

```bash
forge verify-contract <address> <ContractName> \
  --chain 143 \
  --verifier etherscan \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --watch
```

### Socialscan

```bash
forge verify-contract <address> <ContractName> \
  --chain 143 \
  --verifier etherscan \
  --etherscan-api-key $SOCIALSCAN_API_KEY \
  --verifier-url https://api.socialscan.io/monad-mainnet/v1/explorer/command_api/contract \
  --watch
```

### Hardhat Verify

```bash
npx hardhat verify <address> --network monadMainnet
```

For testnet verification, replace `--chain 143` with `--chain 10143` and use testnet RPC/explorer URLs.

## Opcode Repricing Summary

Cold state access is ~4x more expensive on Monad than Ethereum. Warm access is identical.

| Access Type | Ethereum | Monad |
|-------------|----------|-------|
| Account (cold) | 2,600 | **10,100** |
| Storage slot (cold) | 2,100 | **8,100** |
| Account (warm) | 100 | 100 |
| Storage slot (warm) | 100 | 100 |

Selected precompile repricing:

| Precompile | Ethereum | Monad | Multiplier |
|------------|----------|-------|------------|
| ecRecover (0x01) | 3,000 | **6,000** | 2x |
| ecMul (0x07) | 6,000 | **30,000** | 5x |
| ecPairing (0x08) | 45,000 | **225,000** | 5x |
| point evaluation (0x0a) | 50,000 | **200,000** | 4x |

Monad-specific precompile: **secp256r1 (P256)** at `0x0100` for WebAuthn/passkey signature verification (EIP-7951).

## EIP-1559 Parameters

| Parameter | Value |
|-----------|-------|
| Block gas limit | 200M |
| Block gas target | 160M (80% of limit) |
| Per-transaction gas limit | 30M |
| Min base fee | 100 MON-gwei |
| Base fee max step size | 1/28 |
| Base fee decay factor | 0.96 |

The base fee controller increases **slower** and decreases **faster** than Ethereum's to prevent blockspace underutilization on a high-throughput chain.

## Gas Optimization Tips

1. **Warm your storage** — cold reads are 4x more expensive; use access lists (type 1/2 txns) for known slots
2. **Set explicit gas limits** — you're charged for the limit, not usage
3. **Batch operations** — high throughput means batching is less critical, but still saves gas limit overhead
4. **Avoid unnecessary cold precompile calls** — ecPairing is 5x more expensive than Ethereum
5. **Design for parallel execution** — per-user mappings over global counters where possible
6. **No blob transactions** — use calldata for data availability

## Parallel Execution

Monad executes transactions concurrently with optimistic conflict detection. No Solidity changes needed.

1. Multiple virtual executors process transactions simultaneously
2. Each generates "pending results" (inputs: SLOADs, outputs: SSTOREs)
3. Serial commitment validates each result's inputs remain valid
4. Conflict detected -> re-execute the affected transaction
5. Results committed in **original transaction order**

Every transaction executes **at most twice**. Most transactions don't conflict, achieving near-linear speedup.

### Parallel-Friendly Contract Design

| Pattern | Parallelizes Well | Why |
|---------|-------------------|-----|
| Per-user mappings | Yes | Independent state per user |
| ERC-20 transfers between different pairs | Yes | Different storage slots |
| Global counter increment | No | All txns write same slot |
| AMM swaps on same pool | No | Same reserves storage |
| Independent NFT mints (incremental ID) | Partially | tokenId counter serializes |

## Staking Precompile

Address: `0x0000000000000000000000000000000000001000`

Only standard `CALL` is allowed. `STATICCALL`, `DELEGATECALL`, and `CALLCODE` are not permitted.

### Core Functions

| Function | Selector | Gas Cost |
|----------|----------|----------|
| `delegate(uint64)` | `0x84994fec` | 260,850 |
| `undelegate(uint64,uint256,uint8)` | `0x5cf41514` | 147,750 |
| `compound(uint64)` | `0xb34fea67` | 285,050 |
| `claimRewards(uint64)` | `0xa76e2ca5` | 155,375 |
| `withdraw(uint64,uint8)` | `0xaed2ee73` | 68,675 |

### Delegate (Solidity)

```solidity
address constant STAKING = 0x0000000000000000000000000000000000001000;

function delegateToValidator(uint64 validatorId) external payable {
    (bool success,) = STAKING.call{value: msg.value}(
        abi.encodeWithSelector(0x84994fec, validatorId)
    );
    require(success, "Delegation failed");
}
```

### Delegate (viem)

```typescript
import { encodeFunctionData } from "viem";

const STAKING_ADDRESS = "0x0000000000000000000000000000000000001000";

const hash = await walletClient.sendTransaction({
  to: STAKING_ADDRESS,
  value: parseEther("100"),
  data: encodeFunctionData({
    abi: [{ name: "delegate", type: "function", inputs: [{ name: "validatorId", type: "uint64" }], outputs: [] }],
    functionName: "delegate",
    args: [1n],
  }),
});
```

## EIP-7702 on Monad

Allows EOAs to gain smart contract capabilities via code delegation.

| Restriction | Detail |
|-------------|--------|
| Minimum balance | Delegated EOAs cannot drop below **10 MON** |
| CREATE/CREATE2 | **Banned** when delegated EOAs execute as smart contracts |
| Clearing delegation | Send type 0x04 pointing to `address(0)` |

```typescript
import { walletClient } from "./client";

const authorization = await walletClient.signAuthorization({
  account,
  contractAddress: "0xFBA3912Ca04dd458c843e2EE08967fC04f3579c2",
});

const hash = await walletClient.sendTransaction({
  authorizationList: [authorization],
  data: "0xdeadbeef",
  to: walletClient.account.address,
});
```

## WebSocket Subscriptions

Standard `eth_subscribe` plus Monad-specific extensions:

```
newHeads        — standard new block headers
logs            — standard log filtering
monadNewHeads   — Monad-specific block headers with extra fields
monadLogs       — Monad-specific log events
```

## Execution Events (Advanced)

For ultra-low-latency data consumption, Monad exposes execution events via shared-memory ring buffers. Consumer runs on same host as node. ~1 microsecond latency. Supported in C, C++, and Rust only.

Use execution events when JSON-RPC can't keep up with 10,000 TPS throughput. For most dApps, standard WebSocket subscriptions are sufficient.

## Canonical Contracts

| Contract | Address |
|----------|---------|
| Wrapped MON (WMON) | `0x3bd359C1119dA7Da1D913D1C4D2B7c461115433A` |
| Staking Precompile | `0x0000000000000000000000000000000000001000` |
| Multicall3 | `0xcA11bde05977b3631167028862bE2a173976CA11` |
| USDC | `0x754704Bc059F8C67012fEd69BC8A327a5aafb603` |
| USDT0 | `0xe7cd86e13AC4309349F30B3435a9d337750fC82D` |
| WETH | `0xEE8c0E9f1BFFb4Eb878d8f15f368A02a35481242` |
| WBTC | `0x0555E30da8f98308EdB960aa94C0Db47230d2B9c` |
| ERC-4337 EntryPoint v0.7 | `0x0000000071727De22E5E9d8BAf0edAc6f37da032` |
| Safe | `0x69f4D1788e39c87893C980c06EdF4b7f686e2938` |

## Supported Transaction Types

| Type | Name | Supported | Notes |
|------|------|-----------|-------|
| 0 | Legacy | Yes | Pre-EIP-155 allowed but discouraged |
| 1 | EIP-2930 (access list) | Yes | |
| 2 | EIP-1559 (dynamic fee) | Yes | Recommended |
| 3 | EIP-4844 (blob) | **No** | Not supported on Monad |
| 4 | EIP-7702 (delegation) | Yes | With Monad-specific restrictions |

## Smart Contract Tips

- **Gas optimization still matters** — even with cheap gas, optimize for users
- **Same security model** — all Solidity best practices (CEI, reentrancy guards) apply
- **Parallel-friendly design** — contracts with per-user mappings parallelize better than global counters
- **128 KB contract limit** — larger contracts are possible but still optimize for gas
- **No code changes needed** for parallelism — it's at the runtime level
- **`block.timestamp`** — 2-3 blocks may share the same second; don't rely on sub-second granularity
- **No blob transactions** — EIP-4844 type 3 txns are not supported

## Required Tooling Versions

| Tool | Minimum Version |
|------|----------------|
| Foundry | Monad fork (`foundryup --network monad`) |
| viem | 2.40.0+ |
| alloy-chains | 0.2.20+ |
| Hardhat Solidity | evmVersion: "prague" |

## Pre-Deployment Checklist

- [ ] Using Monad Foundry fork or Hardhat with `evmVersion: "prague"`
- [ ] Correct chain ID (143 mainnet / 10143 testnet)
- [ ] Account funded with MON (remember ~10 MON reserve)
- [ ] Gas limit set explicitly for predictable cost (gas limit is charged, not gas used)
- [ ] Private key in env var, not hardcoded
- [ ] Contract size under 128 KB
- [ ] No EIP-4844 blob transactions (type 3 not supported)
- [ ] Verified on at least one explorer after deploy

## Additional Reference

| File | Contents |
|------|----------|
| `docs/architecture.md` | MonadBFT consensus, parallel execution, deferred execution, MonadDb, JIT, RaptorCast |
| `docs/deployment.md` | Foundry + Hardhat deploy/verify step-by-step guides |
| `docs/gas-and-opcodes.md` | Gas pricing model, opcode repricing tables, precompile costs |
| `docs/staking.md` | Staking precompile ABI, functions, events, epoch mechanics |
| `docs/ecosystem.md` | Token addresses, bridges, oracles, indexers, canonical contracts |
| `docs/troubleshooting.md` | Common issues and fixes for Monad development |
| `resources/contract-addresses.md` | Key Monad contract addresses |
| `templates/deploy-monad.sh` | Shell script for deploying to Monad |
