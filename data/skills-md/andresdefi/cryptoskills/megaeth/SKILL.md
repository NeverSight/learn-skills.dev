---
name: megaeth
description: MegaETH real-time blockchain development — instant receipts, eth_sendRawTransactionSync, MegaNames, Warren sequencer, ERC-7710 delegations, and sub-millisecond storage optimization.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: megaeth
  category: L2 & Alt-L1
tags:
  - megaeth
  - real-time
  - instant-receipts
  - erc-7710
  - meganames
---

# MegaETH Development

## Quick Start

```bash
# Install dependencies
npm install viem @metamask/smart-accounts-kit

# Check balance
cast balance <address> --rpc-url https://mainnet.megaeth.com/rpc

# Deploy with Foundry
forge script Deploy.s.sol --rpc-url https://mainnet.megaeth.com/rpc --broadcast --skip-simulation
```

```typescript
import { defineChain, createPublicClient, createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

export const megaeth = defineChain({
  id: 4326,
  name: 'MegaETH',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://mainnet.megaeth.com/rpc'] },
  },
  blockExplorers: {
    default: { name: 'Etherscan', url: 'https://mega.etherscan.io' },
  },
});

export const megaethTestnet = defineChain({
  id: 6343,
  name: 'MegaETH Testnet',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://carrot.megaeth.com/rpc'] },
  },
  blockExplorers: {
    default: { name: 'Blockscout', url: 'https://megaeth-testnet-v2.blockscout.com' },
  },
});

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const publicClient = createPublicClient({ chain: megaeth, transport: http() });
const walletClient = createWalletClient({ account, chain: megaeth, transport: http() });
```

## Chain Configuration

| Network | Chain ID | RPC HTTP | RPC WebSocket | Explorer |
|---------|----------|----------|---------------|----------|
| Mainnet | 4326 | `https://mainnet.megaeth.com/rpc` | `wss://mainnet.megaeth.com/ws` | `https://mega.etherscan.io` |
| Testnet | 6343 | `https://carrot.megaeth.com/rpc` | `wss://carrot.megaeth.com/ws` | `https://megaeth-testnet-v2.blockscout.com` |

Third-party RPC providers: Alchemy, QuickNode (recommended for geo-distributed access).

## What You Probably Got Wrong

### 1. Intrinsic gas is NOT 21,000

MegaETH intrinsic gas is **60,000** (21K compute + 39K storage). A simple ETH transfer that costs 21K on Ethereum costs 60K on MegaETH.

```typescript
const tx = await walletClient.sendTransaction({
  to: recipient,
  value: parseEther('0.1'),
  gas: 60000n,
  maxFeePerGas: 1000000n,
  maxPriorityFeePerGas: 0n,
});
```

### 2. Don't poll for receipts

Use `eth_sendRawTransactionSync` (EIP-7966) for instant receipts in <10ms:

```typescript
const receipt = await walletClient.request({
  method: 'eth_sendRawTransactionSync',
  params: [signedTx],
});
```

### 3. Don't simulate gas locally

MegaEVM opcode costs differ from standard EVM. Foundry and Hardhat simulate with standard costs, giving wrong estimates.

```bash
forge script Deploy.s.sol --gas-limit 5000000 --skip-simulation
```

### 4. Storage is expensive, not compute

SSTORE 0-to-nonzero costs 2M+ gas multiplied by a bucket multiplier. Use slot reuse patterns (RedBlackTreeLib, transient storage) instead of dynamic mappings.

### 5. Viem adds a 20% gas buffer

Override the gas price directly:

```typescript
const gasPrice = 1000000n; // 0.001 gwei, no buffer needed
```

### 6. Never use `via_ir=true` in foundry.toml

It silently breaks return values -- functions return 0 instead of correct values with no compiler error. Use `optimizer=true` with `optimizer_runs=200` instead.

## RPC Methods

### Instant Transaction Receipts

Two equivalent methods (both supported, functionally identical):

| Method | Origin | Recommendation |
|--------|--------|----------------|
| `realtime_sendRawTransaction` | MegaETH original | Supported |
| `eth_sendRawTransactionSync` | EIP-7966 standard | Preferred for cross-chain compatibility |

```typescript
const signedTx = await walletClient.signTransaction({
  to: recipient,
  value: parseEther('0.1'),
  gas: 60000n,
  maxFeePerGas: 1000000n,
  maxPriorityFeePerGas: 0n,
});

const receipt = await walletClient.request({
  method: 'eth_sendRawTransactionSync',
  params: [signedTx],
});
```

Response: Full transaction receipt (same schema as `eth_getTransactionReceipt`).

### eth_getLogsWithCursor

Paginated log queries for large result sets:

```typescript
const response = await publicClient.request({
  method: 'eth_getLogsWithCursor',
  params: [{
    address: '0x...',
    topics: ['0x...'],
    fromBlock: '0x0',
    toBlock: 'latest',
  }],
});
// Returns { logs: [...], cursor: "..." }
```

### Mini-Block Subscription

```typescript
const ws = new WebSocket('wss://mainnet.megaeth.com/ws');

ws.send(JSON.stringify({
  jsonrpc: '2.0',
  method: 'eth_subscribe',
  params: ['miniBlocks'],
  id: 1,
}));
```

Mini-blocks are ephemeral and cannot be fetched via RPC after assembly into blocks.

### WebSocket Keepalive

Send `eth_chainId` every 30 seconds. Limits: 50 connections per VIP endpoint, 10 subscriptions per connection.

```typescript
const keepalive = setInterval(() => {
  ws.send(JSON.stringify({
    jsonrpc: '2.0',
    method: 'eth_chainId',
    params: [],
    id: Date.now(),
  }));
}, 30000);
```

### RPC Batching (v2.0.14+)

Multicall is preferred for batching `eth_call` requests. `eth_call` is 2-10x faster as of v2.0.14; Multicall amortizes per-RPC overhead.

```typescript
import { multicall } from 'viem/actions';

const results = await multicall(publicClient, {
  contracts: [
    { address: token1, abi: erc20Abi, functionName: 'balanceOf', args: [user] },
    { address: token2, abi: erc20Abi, functionName: 'balanceOf', args: [user] },
    { address: pool, abi: poolAbi, functionName: 'getReserves' },
  ],
});
```

Do not batch `eth_getLogs` with `eth_call` -- logs are always slower and block the entire batch.

## Smart Contracts

### MegaEVM vs Standard EVM

MegaEVM is fully EVM-compatible but has different gas costs (SSTORE), block metadata limits (volatile data access), and contract size limits (512 KB).

| Resource | Limit |
|----------|-------|
| Contract code | 512 KB |
| Calldata | 128 KB |
| eth_call/estimateGas | 10M gas (public), higher on VIP |

### Volatile Data Access Control

After accessing block metadata (`block.timestamp`, `block.number`, `blockhash(n)`), the transaction is limited to 20M additional compute gas.

```solidity
// Access metadata late in execution to avoid the limit
function process() external {
    for (uint i = 0; i < 10000; i++) {
        // Heavy work first
    }
    emit Processed(block.timestamp); // Metadata last
}
```

### High-Precision Timestamps

For microsecond precision, use the predeployed oracle instead of `block.timestamp`:

```solidity
interface ITimestampOracle {
    function timestamp() external view returns (uint256);
}

ITimestampOracle constant ORACLE =
    ITimestampOracle(0x6342000000000000000000000000000000000002);
```

### SSTORE2 (On-Chain Data Storage)

Store large immutable data as contract bytecode instead of storage slots:

| Approach | Write Cost | Read Cost |
|----------|------------|-----------|
| SSTORE (slots) | 2M+ gas per new slot | 100-2100 gas |
| SSTORE2 (bytecode) | ~10K gas per byte | FREE (EXTCODECOPY) |

```solidity
import {SSTORE2} from "solady/src/utils/SSTORE2.sol";

address pointer = SSTORE2.write(data);
bytes memory data = SSTORE2.read(pointer);
```

### EIP-6909 (Minimal Multi-Token)

Prefer EIP-6909 over ERC-1155 on MegaETH: no mandatory callbacks, single contract for multiple tokens (fewer SSTORE operations), granular approvals.

```solidity
import {ERC6909} from "solady/src/tokens/ERC6909.sol";
```

### Contract Verification

```bash
forge verify-contract <address> src/MyContract.sol:MyContract \
  --chain 4326 \
  --etherscan-api-key $ETHERSCAN_KEY \
  --verifier-url "https://api.etherscan.io/v2/api?chainid=4326"
```

## Gas Model

### Base Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Base fee | 0.001 gwei (10^6 wei) | Fixed, no EIP-1559 adjustment |
| Priority fee | 0 | Ignored unless congested |
| Intrinsic gas | 60,000 | 21K compute + 39K storage |
| Gas forwarding | 98/100 | More gas in nested calls than Ethereum's 63/64 |

### Per-Transaction Resource Limits

| Resource | Limit |
|----------|-------|
| Compute gas | 200M |
| KV updates | 500K |
| State growth slots | 1,000 |
| Data size | 12.5 MB |
| Contract code | 512 KB |
| Calldata | 128 KB |

### SSTORE Costs

| Bucket Multiplier | Storage Gas | Total Gas |
|-------------------|-------------|-----------|
| 1 | 0 | 22,100 |
| 2 | 20,000 | 42,100 |
| 10 | 180,000 | 202,100 |
| 100 | 1,980,000 | 2,002,100 |

When multiplier = 1, storage gas is zero. This is why slot reuse patterns matter.

### LOG Opcode Costs

LOG opcodes have quadratic cost above 4KB data. Contracts emitting large events should emit a hash and store data off-chain.

## Storage Optimization

MegaETH charges high gas for new storage slot creation:

```
SSTORE (0 -> non-zero): 2,000,000 gas x bucket_multiplier
```

### Solady RedBlackTreeLib

Replace Solidity mappings with contiguous slot-reusing storage:

```solidity
import {RedBlackTreeLib} from "solady/src/utils/RedBlackTreeLib.sol";

contract StorageOptimized {
    using RedBlackTreeLib for RedBlackTreeLib.Tree;
    RedBlackTreeLib.Tree private _tree;
}
```

### Transient Storage (EIP-1153)

Use `TSTORE`/`TLOAD` for temporary data within a transaction -- avoids storage gas entirely:

```solidity
assembly {
    tstore(0, value)
    let v := tload(0)
}
```

### Circular Buffer Pattern

```solidity
uint256[100] public buffer;
uint256 public head;

function process(uint256 value) external {
    buffer[head] = value; // Reuses existing slot
    head = (head + 1) % 100;
}
```

### ZK Compression

For apps with large state: store only a hash/commitment on-chain, provide pre-state + proof per transaction.

## Testing and Debugging

### mega-evme CLI

```bash
git clone https://github.com/megaeth-labs/mega-evm
cd mega-evm/bin/mega-evme
cargo build --release

mega-evme replay <txhash> --rpc https://mainnet.megaeth.com/rpc
mega-evme replay <txhash> --trace --trace.output trace.json --rpc <endpoint>
```

### Gas Profiling

```bash
cast run <txhash> --rpc-url <vip-endpoint> > trace.json
python scripts/trace_opcode_gas.py trace.json
```

### Fork Testing

```solidity
contract MyTest is Test {
    function setUp() public {
        vm.createSelectFork("https://carrot.megaeth.com/rpc");
    }

    function testGasCost() public {
        uint256 gasBefore = gasleft();
        // operation
        uint256 gasUsed = gasBefore - gasleft();
        console.log("Gas used:", gasUsed);
    }
}
```

## MegaNames (.mega Naming Service)

### Contract Addresses (Mainnet, Chain ID: 4326)

| Contract | Address |
|----------|---------|
| MegaNames | `0x5B424C6CCba77b32b9625a6fd5A30D409d20d997` |
| MegaNameRenderer | `0x8d206c277E709c8F4f8882fc0157bE76dA0C48C4` |
| SubdomainRouter | `0xdB5e5Ab907e62714D7d9Ffde209A4E770a0507Fe` |
| SubdomainLogic | `0xf09fB5cB77b570A30D68b1Aa1d944256171C5172` |
| USDM | `0xFAfDdbb3FC7688494971a79cc65DCa3EF82079E7` |

### Fee Structure

| Label Length | Annual Fee (USDM) |
|-------------|-------------------|
| 1 character | $1,000 |
| 2 characters | $500 |
| 3 characters | $100 |
| 4 characters | $10 |
| 5+ characters | $1 |

### Registration

```solidity
IERC20(0xFAfDdbb3FC7688494971a79cc65DCa3EF82079E7).approve(
    0x5B424C6CCba77b32b9625a6fd5A30D409d20d997,
    fee
);
uint256 tokenId = megaNames.register("yourname", msg.sender, 1);
```

### Resolution

```solidity
address resolved = megaNames.addr(tokenId);     // Forward: name -> address
string memory name = megaNames.getName(userAddr); // Reverse: address -> name
```

See [docs/meganames.md](docs/meganames.md) for subdomains, marketplace, text records, and cross-chain interop.

## ERC-7710 Delegations

Scoped, revocable, composable on-chain permissions. A delegator grants a delegate authority to act on their behalf, constrained by caveat enforcers.

```typescript
import { createDelegation } from '@metamask/smart-accounts-kit';

const delegation = createDelegation({
  from: smartAccount.address,
  to: delegateAddress,
  environment,
  scope: {
    type: 'erc20TransferAmount',
    tokenAddress: USDC_ADDRESS,
    maxAmount: parseUnits('100', 6),
  },
  caveats: [
    { type: 'timestamp', afterThreshold: now, beforeThreshold: expiry },
    { type: 'limitedCalls', limit: 10 },
  ],
});
```

Use `eth_sendRawTransactionSync` for instant delegation redemption -- receipt in <10ms instead of polling.

See [docs/erc7710-delegations.md](docs/erc7710-delegations.md) for full lifecycle, caveat enforcers, and redelegation chains.

## Warren Protocol

On-chain website hosting via SSTORE2 storage. Sites are referenced by NFT ownership (Master NFT or Container NFT) and resolved through MegaNames contenthash.

See [docs/warren.md](docs/warren.md) for contenthash encoding, Solidity helpers, and gateway resolution.

## Wallet Operations

### Token Swaps (Kyber Network)

```typescript
const KYBER_API = 'https://aggregator-api.kyberswap.com/megaeth/api/v1';

const quoteRes = await fetch(
  `${KYBER_API}/routes?` + new URLSearchParams({
    tokenIn: '0x...',
    tokenOut: '0x...',
    amountIn: amount.toString(),
    gasInclude: 'true',
  })
);
const quote = await quoteRes.json();
```

### Bridging ETH (from Ethereum)

```typescript
const bridgeAddress = '0x0CA3A2FBC3D770b578223FBB6b062fa875a2eE75';

const tx = await wallet.sendTransaction({
  to: bridgeAddress,
  value: parseEther('0.1'),
});
```

See [docs/wallet-operations.md](docs/wallet-operations.md) for full wallet setup, nonce management, and error handling.

## Frontend Patterns

**Never open per-user WebSocket connections.** Use one server-side connection, broadcast to users.

```typescript
async function warmupRpcConnection(client: PublicClient) {
  await client.getChainId();
}
```

See [docs/frontend-patterns.md](docs/frontend-patterns.md) for WebSocket manager, real-time hooks, and error handling.

## Security

### MegaETH-Specific Risks

1. **Storage cost attacks** -- attacker triggers expensive SSTORE operations
2. **Volatile data timing attacks** -- `block.timestamp` has 1s granularity but mini-blocks happen every 10ms
3. **Reorg considerations** -- fast finality but reorgs possible until L1 finalization
4. **Input validation** -- always use allowlists over blocklists

See [docs/security.md](docs/security.md) for prevention patterns and audit recommendations.

## Progressive Disclosure

| Topic | Reference |
|-------|-----------|
| RPC methods | [docs/rpc-methods.md](docs/rpc-methods.md) |
| Smart contract patterns | [docs/smart-contracts.md](docs/smart-contracts.md) |
| Gas model | [docs/gas-model.md](docs/gas-model.md) |
| Storage optimization | [docs/storage-optimization.md](docs/storage-optimization.md) |
| Testing & debugging | [docs/testing.md](docs/testing.md) |
| Frontend patterns | [docs/frontend-patterns.md](docs/frontend-patterns.md) |
| Wallet operations | [docs/wallet-operations.md](docs/wallet-operations.md) |
| MegaNames | [docs/meganames.md](docs/meganames.md) |
| Warren Protocol | [docs/warren.md](docs/warren.md) |
| ERC-7710 delegations | [docs/erc7710-delegations.md](docs/erc7710-delegations.md) |
| Smart accounts | [docs/smart-accounts.md](docs/smart-accounts.md) |
| Security | [docs/security.md](docs/security.md) |
| Troubleshooting | [docs/troubleshooting.md](docs/troubleshooting.md) |
| Contract addresses | [resources/contract-addresses.md](resources/contract-addresses.md) |
| Client template | [templates/megaeth-client.ts](templates/megaeth-client.ts) |

## Attribution

| Source | What it validates |
|--------|-------------------|
| [MegaEVM Spec](https://github.com/megaeth-labs/mega-evm) | Gas model, resource limits, intrinsic gas, SSTORE formula |
| [MegaETH Docs](https://docs.megaeth.com) | RPC methods, real-time API, chain configuration |
| [Foundry Prompting Guide](https://getfoundry.sh/introduction/prompting/) | Testing patterns, project structure, deployment scripts |

Contributors:
- Original patterns: [0xBreadguy/megaeth-ai-developer-skills](https://github.com/0xBreadguy/megaeth-ai-developer-skills)
- Foundry integration: [clawdybotty/megaeth-foundry-developer](https://github.com/clawdybotty/megaeth-foundry-developer)
