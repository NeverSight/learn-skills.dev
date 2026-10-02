---
name: eth-concepts
description: Core Ethereum development concepts including gas mechanics, transaction types, storage layout, ABI encoding, and EVM execution model. Use as a reference when building on Ethereum or EVM chains.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - ethereum
  - evm
  - gas
  - transactions
  - storage
---

# Ethereum Concepts

Foundational reference for Ethereum and EVM-compatible chain development. Covers the mental models that every other skill assumes you know — gas, transactions, storage, ABI encoding, and the execution environment. This is not a tool skill; it is the conceptual substrate beneath all EVM tooling.

## What You Probably Got Wrong

> LLMs confidently generate Ethereum code with fundamental misconceptions. These are the ones that cause real bugs.

- **Gas is not ETH** — Gas is a unit of computation. You pay `gasUsed * effectiveGasPrice` in wei. Confusing gas units with ether amounts is the most common mental model failure.
- **Transaction types are not interchangeable** — There are four types (0, 1, 2, 3). Type 2 (EIP-1559) is the default since London. Each has different fields and fee semantics. Sending a legacy (type 0) transaction still works but uses the old fee model.
- **Nonce is per-account and sequential** — Skipping a nonce blocks all subsequent transactions. There is no way to "fill" a nonce gap except by sending a transaction with the missing nonce. Nonces start at 0 for EOAs and at 1 for contracts (post-EIP-161).
- **`msg.value` is in wei, not ETH** — `1 ether` in Solidity is `1e18` wei. Passing `1` as msg.value sends 1 wei (0.000000000000000001 ETH), not 1 ETH.
- **Storage slots are 32 bytes** — Every slot holds exactly 32 bytes. Smaller types are packed within a single slot when declared adjacently. Understanding this is critical for gas optimization and direct storage reads.
- **Contract addresses are deterministic** — `CREATE` uses `keccak256(rlp(sender, nonce))`. `CREATE2` uses `keccak256(0xff ++ sender ++ salt ++ keccak256(initCode))`. Same inputs always produce the same address, even before deployment.
- **`address(0)` is not a burn address by design** — It is the zero address. Tokens sent there are irrecoverable, but it has no special EVM semantics. Some protocols use it as a mint/burn signal by convention.
- **`block.timestamp` is set by the block proposer** — It must be greater than the parent timestamp and within ~15 seconds of real time. Do not use it for tight time comparisons or as entropy.

## Gas Mechanics

### The Fee Model (EIP-1559)

Since the London hard fork, Ethereum uses a dual-fee model:

| Term | Definition |
|------|-----------|
| **Base fee** | Protocol-set fee per gas unit. Burns on use. Adjusts up/down 12.5% per block based on target utilization (15M gas target, 30M limit). |
| **Priority fee** (tip) | User-set fee per gas unit paid to the block proposer. Incentivizes inclusion. |
| **Max fee** | User-set ceiling on total fee per gas unit. Must be >= baseFee + priorityFee. |
| **Effective gas price** | `min(maxFee, baseFee + priorityFee)`. Overpayment of maxFee is refunded. |
| **Gas limit** | Maximum gas units the transaction is allowed to consume. Unused gas is refunded. |
| **Gas used** | Actual gas units consumed during execution. |

The total cost in wei:

```
cost = gasUsed * effectiveGasPrice
cost = gasUsed * min(maxFeePerGas, baseFeePerGas + maxPriorityFeePerGas)
```

### Gas Costs Reference

| Operation | Gas Cost | Notes |
|-----------|----------|-------|
| ETH transfer | 21,000 | Base cost for any transaction |
| SSTORE (zero to non-zero) | 20,000 | Most expensive common opcode |
| SSTORE (non-zero to non-zero) | 5,000 | Cheaper update |
| SSTORE (non-zero to zero) | 5,000 + 4,800 refund | Net cost ~200 gas |
| SLOAD (cold) | 2,100 | First access in transaction |
| SLOAD (warm) | 100 | Already accessed this transaction |
| CALL (cold account) | 2,600 | First call to an address |
| CALL (warm account) | 100 | Already accessed this transaction |
| Memory expansion | Quadratic | Cost grows with `memory_size^2 / 512` |
| Calldata (zero byte) | 4 | Per zero byte in tx data |
| Calldata (non-zero byte) | 16 | Per non-zero byte in tx data |
| LOG0 | 375 | Base event cost |
| LOG per topic | +375 | Per indexed parameter |
| LOG per data byte | +8 | Event data cost |

### Blob Gas (EIP-4844)

Type 3 transactions (Dencun, March 2024) carry blob data for L2 data availability:

- Blob gas is priced independently from execution gas
- Target: 3 blobs per block (384 KB), max 6 blobs (768 KB)
- Each blob is 128 KB of data committed via KZG
- Blob base fee adjusts independently using the same EIP-1559 mechanism
- Blobs are pruned from consensus nodes after ~18 days — not permanently stored

## Transaction Types

### Type Comparison

| Field | Type 0 (Legacy) | Type 1 (Access List) | Type 2 (EIP-1559) | Type 3 (Blob) |
|-------|-----------------|---------------------|-------------------|---------------|
| EIP | Pre-EIP-2718 | EIP-2930 | EIP-1559 | EIP-4844 |
| `gasPrice` | Yes | Yes | No | No |
| `maxFeePerGas` | No | No | Yes | Yes |
| `maxPriorityFeePerGas` | No | No | Yes | Yes |
| `accessList` | No | Yes | Yes | Yes |
| `maxFeePerBlobGas` | No | No | No | Yes |
| `blobVersionedHashes` | No | No | No | Yes |
| Fee mechanism | Single price | Single price | Base + priority | Base + priority + blob |

### Type 0 — Legacy

Original transaction format. Single `gasPrice` field. Still valid on all EVM chains.

```
{nonce, gasPrice, gasLimit, to, value, data, v, r, s}
```

### Type 1 — Access List (EIP-2930)

Adds `accessList` to pre-declare storage slots and addresses. Reduces cold access costs from 2,600 to 2,400 gas for addresses and 2,100 to 1,900 for storage slots. Useful for contracts accessing many storage slots.

```
0x01 || rlp([chainId, nonce, gasPrice, gasLimit, to, value, data, accessList, v, r, s])
```

### Type 2 — EIP-1559

Default since London. Separates fee into `maxFeePerGas` and `maxPriorityFeePerGas`. The base fee portion burns.

```
0x02 || rlp([chainId, nonce, maxPriorityFeePerGas, maxFeePerGas, gasLimit, to, value, data, accessList, v, r, s])
```

### Type 3 — Blob (EIP-4844)

Carries sidecar blob data for L2 rollup data availability. The `to` field is mandatory (no contract creation). Includes `maxFeePerBlobGas` for the separate blob fee market.

```
0x03 || rlp([chainId, nonce, maxPriorityFeePerGas, maxFeePerGas, gasLimit, to, value, data, accessList,
             maxFeePerBlobGas, blobVersionedHashes, v, r, s])
```

## Storage Layout

### Slot Allocation

The EVM provides 2^256 storage slots per contract, each 32 bytes wide. State variables are allocated sequentially starting at slot 0.

```solidity
contract Layout {
    uint256 a;       // slot 0 (full 32 bytes)
    uint256 b;       // slot 1
    uint128 c;       // slot 2 (16 bytes, left-aligned)
    uint128 d;       // slot 2 (packed into remaining 16 bytes)
    uint256 e;       // slot 3 (c+d filled slot 2)
}
```

### Packing Rules

- Variables are packed into a slot if they fit in the remaining space
- Packing order is right-to-left within a slot (lower-order bits first)
- Structs and arrays always start a new slot
- `mapping` and dynamic `array` values never share a slot with other variables
- Constants and immutables do not use storage slots

### Dynamic Arrays

The length is stored at the declared slot `p`. Elements start at `keccak256(p)`:

```
array.length  →  slot p
array[0]      →  slot keccak256(p)
array[1]      →  slot keccak256(p) + 1
array[n]      →  slot keccak256(p) + n
```

### Mappings

Mappings store nothing at their declared slot `p`. Each value is at:

```
mapping[key]  →  slot keccak256(key . p)
```

Where `.` is concatenation and both `key` and `p` are left-padded to 32 bytes. Nested mappings compose:

```
mapping[k1][k2]  →  slot keccak256(k2 . keccak256(k1 . p))
```

### Strings and Bytes

Short strings/bytes (31 bytes or less) store data and length in the same slot. The lowest-order byte stores `length * 2`. Long strings/bytes (32+ bytes) store `length * 2 + 1` at slot `p`, and data starts at `keccak256(p)`.

### Reading Storage Directly

```bash
# Read slot 0 of a contract
cast storage 0xContractAddress 0

# Read a mapping value (e.g., balanceOf at slot 3, for address 0xUser)
cast index address 0xUserAddress 3 | xargs cast storage 0xContractAddress
```

## ABI Encoding

### Function Selectors

The first 4 bytes of calldata identify the function:

```
selector = keccak256("functionName(type1,type2)")[:4]
```

No parameter names, no spaces, canonical types (`uint256` not `uint`). Structs are expanded as tuples.

```bash
# Compute a selector
cast sig "transfer(address,uint256)"
# Output: 0xa9059cbb
```

### Calldata Layout

After the 4-byte selector, arguments are ABI-encoded in 32-byte words:

```
[4-byte selector][32-byte arg0][32-byte arg1]...
```

Static types (uint256, address, bool, bytesN) are padded to 32 bytes in place. Dynamic types (bytes, string, arrays) are encoded as a 32-byte offset pointer, with the actual data appended at the end of the calldata.

### Static vs Dynamic Types

| Static | Dynamic |
|--------|---------|
| `uint<N>`, `int<N>` | `bytes` |
| `address` | `string` |
| `bool` | `T[]` (dynamic array) |
| `bytes<N>` (1-32) | `(T1, T2)` if any Ti is dynamic |
| `T[N]` (fixed array of static T) | |

### abi.encode vs abi.encodePacked

```solidity
// abi.encode: standard ABI encoding with 32-byte padding
abi.encode(uint8(1), uint8(2))
// → 0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002

// abi.encodePacked: tight packing, no padding
abi.encodePacked(uint8(1), uint8(2))
// → 0x0102
```

`abi.encodePacked` is ambiguous for dynamic types — two different inputs can produce the same output. Never use it for hashing multiple dynamic-length values (hash collision vulnerability). Use `abi.encode` when computing hashes for signatures or storage keys.

## EVM Execution Model

### Stack Machine

The EVM is a stack-based virtual machine:

- **Stack**: 1024 elements max, each 256 bits. Operations pop inputs, push outputs.
- **Memory**: Byte-addressable, linear, volatile. Expands in 32-byte words. Costs grow quadratically with size. Zeroed at the start of each call context.
- **Storage**: Key-value store, 256-bit keys to 256-bit values. Persistent across transactions. Most expensive data location.
- **Calldata**: Read-only byte array containing transaction input data. Cheaper than memory for read-only access.
- **Return data**: Output buffer from the last external call. Accessible via `RETURNDATASIZE` and `RETURNDATACOPY`.

### Memory vs Storage vs Calldata

| Property | Storage | Memory | Calldata |
|----------|---------|--------|----------|
| Persistence | Permanent | Call duration | Call duration |
| Cost | High (5k-20k gas) | Low (3 gas + expansion) | Very low (read-only) |
| Access | SLOAD/SSTORE | MLOAD/MSTORE | CALLDATALOAD/CALLDATACOPY |
| Mutability | Read/write | Read/write | Read-only |
| Size | 2^256 slots | Linear (grows) | Fixed per call |

### External Call Types

| Opcode | `msg.sender` | `address(this)` | Storage context | Can send ETH |
|--------|-------------|-----------------|-----------------|-------------|
| `CALL` | Caller contract | Called contract | Called contract | Yes |
| `DELEGATECALL` | Original `msg.sender` | Caller contract | Caller contract | No (inherits value) |
| `STATICCALL` | Caller contract | Called contract | Called contract (read-only) | No |
| `CALLCODE` | Caller contract | Caller contract | Caller contract | Yes (deprecated) |

**DELEGATECALL** executes the target's code in the caller's context. This is how proxies work — the proxy's storage is modified by the implementation's logic. Storage layout between proxy and implementation must match exactly.

**STATICCALL** reverts if the called code attempts any state modification (SSTORE, LOG, CREATE, SELFDESTRUCT, or calls with value). Used by `view`/`pure` external calls.

### Revert Reasons

When a call reverts, the return data contains the error:

```
// Solidity require/revert with string
0x08c379a0 + abi.encode(string)   // Error(string) selector

// Custom error
bytes4(keccak256("InsufficientBalance(uint256,uint256)")) + abi.encode(args)

// Panic codes (assert failures, overflow, division by zero)
0x4e487b71 + abi.encode(uint256 code)
```

Common panic codes: `0x01` (assert), `0x11` (overflow), `0x12` (divide by zero), `0x21` (invalid enum), `0x31` (empty array pop), `0x32` (array out of bounds).

## Account Types

### EOA (Externally Owned Account)

- Controlled by a private key
- Has nonce (transaction count, starts at 0) and balance
- No code, no storage
- Can initiate transactions
- Address derived from public key: `keccak256(publicKey)[12:]`

### Contract Account

- Controlled by code
- Has nonce (starts at 1 post-EIP-161, incremented on CREATE), balance, code, and storage
- Cannot initiate transactions — only responds to calls
- Code is immutable after deployment (except via proxy patterns or SELFDESTRUCT)
- Code hash: `keccak256(deployedBytecode)`. Empty accounts have `keccak256("")`

### Address Derivation

```
# EOA
address = keccak256(publicKey)[12:]

# CREATE (contract deployment)
address = keccak256(rlp([sender, nonce]))[12:]

# CREATE2 (deterministic deployment)
address = keccak256(0xff ++ sender ++ salt ++ keccak256(initCode))[12:]
```

CREATE2 enables counterfactual addresses — you can compute the address before deployment and even send funds to it. The address depends only on the deployer, salt, and init code.

### SELFDESTRUCT (Deprecated)

EIP-6780 (Dencun, March 2024) neutered SELFDESTRUCT. It now only sends the contract's ETH balance to the target — it no longer deletes code or storage unless called in the same transaction as contract creation. Do not rely on SELFDESTRUCT for any logic.

## Common Units

### ETH Denominations

| Unit | Wei | Decimal |
|------|-----|---------|
| **wei** | 1 | 10^0 |
| **kwei** (babbage) | 1,000 | 10^3 |
| **mwei** (lovelace) | 1,000,000 | 10^6 |
| **gwei** (shannon) | 1,000,000,000 | 10^9 |
| **microether** (szabo) | 1,000,000,000,000 | 10^12 |
| **milliether** (finney) | 1,000,000,000,000,000 | 10^15 |
| **ether** | 1,000,000,000,000,000,000 | 10^18 |

In practice, only three matter: **wei** (base unit), **gwei** (gas prices), **ether** (human-readable amounts).

### Common Token Decimals

| Token | Decimals | 1 Token in Base Unit |
|-------|----------|---------------------|
| ETH / WETH | 18 | 1e18 |
| USDC | 6 | 1e6 |
| USDT | 6 | 1e6 |
| WBTC | 8 | 1e8 |
| DAI | 18 | 1e18 |
| LINK | 18 | 1e18 |

Never assume 18 decimals. Always read `decimals()` from the token contract. Arithmetic with mismatched decimals silently produces wrong results by orders of magnitude.

### Conversion in Solidity

```solidity
1 wei    == 1;
1 gwei   == 1e9;
1 ether  == 1e18;

1 seconds == 1;
1 minutes == 60;
1 hours   == 3600;
1 days    == 86400;
1 weeks   == 604800;
```

These are compile-time constants, not runtime calls. `1 ether` is syntactic sugar for the literal `1000000000000000000`.

## Ethereum Network Evolution (2025-2026)

### Pectra Upgrade (May 7, 2025)

The Prague-Electra (Pectra) upgrade combined execution and consensus layer changes:

**EIP-7702 — EOA Delegation**: EOAs can temporarily delegate to smart contract code within a transaction. Type 0x04 transactions include an `authorizationList` — signed tuples of `(chainId, address, nonce)` that set the EOA's code to point at a delegation target. This enables batch transactions, gas sponsorship, and smart account features for existing EOAs without migration.

**EIP-2537 — BLS12-381 Precompile**: Native BLS signature operations at addresses 0x0b-0x13. Enables efficient BLS signature verification onchain — critical for bridges, zero-knowledge proofs, and cross-chain messaging that rely on BLS aggregate signatures. Previously required expensive Solidity implementations (~100k+ gas vs ~45k with precompile).

**EIP-2935 — Historical Block Hashes in State**: The BLOCKHASH opcode previously only accessed the last 256 blocks. EIP-2935 stores block hashes in a system contract at `0x0000...0025` (ring buffer of 8191 slots), enabling smart contracts to verify historical state up to ~27 hours back. Useful for trustless bridges and optimistic rollup proofs.

**EIP-7685 — Execution Layer Requests**: General-purpose framework for the execution layer to trigger consensus layer actions. Replaces ad-hoc mechanisms with a unified request type system. Used by EIP-6110 (validator deposits) and EIP-7002 (execution-triggered withdrawals).

**Blob Target Increase**: Blob target increased from 3 to 6 per block, doubling L2 data availability capacity. Max blobs increased from 6 to 9. Reduced L2 transaction costs further.

```solidity
// EIP-7702: Check if EOA has delegated code
// After delegation, EOA's code returns the delegation target
function isDelegated(address account) external view returns (bool) {
    uint256 size;
    assembly { size := extcodesize(account) }
    return size > 0; // EOAs normally have size 0
}
```

### Fusaka Upgrade (Dec 3, 2025)

The Fusaka upgrade focused on scaling and efficiency:

**EIP-7594 — PeerDAS (Peer Data Availability Sampling)**: Nodes only download a subset of blob data columns and reconstruct the rest via erasure coding. Reduces bandwidth requirements for validators while maintaining data availability guarantees. Enables future blob count increases without proportional bandwidth growth.

**EIP-7935 — Gas Limit 60M**: Block gas limit raised from 36M to 60M, increasing L1 throughput by ~67%. Combined with EIP-4844 blob improvements, this nearly doubled effective L1 capacity compared to pre-Pectra levels.

**EIP-7825 — Transaction Gas Cap**: Individual transaction gas limit capped at 16.78M (2^24 - 2^14). Prevents single transactions from consuming more than ~28% of block gas, improving block production reliability and reducing worst-case execution times.

**EIP-7951 — secp256r1 Precompile (Passkey Support)**: Native verification of P-256 (secp256r1) signatures at a precompile address. WebAuthn/passkey authentication can now be verified cheaply onchain (~3,450 gas vs ~300k+ in Solidity). Enables hardware security key and biometric-based wallet authentication without account abstraction overhead.

### Sub-Gwei Gas Reality

Post-Dencun blob transactions fundamentally changed Ethereum's fee landscape:

| Period | Avg Base Fee | Cause |
|--------|-------------|-------|
| Early 2024 | 30-72 gwei | Pre-blob, L2 data on calldata |
| Late 2024 | 3-10 gwei | Blobs absorb L2 data, reduced calldata demand |
| 2025-2026 | 0.05-0.3 gwei | Increased blob capacity, activity shift to L2s |

L1 is cheap again for simple operations. A basic ETH transfer costs $0.01-0.05. However, this reduced ETH burn rate significantly — issuance now exceeds burn, making ETH net inflationary since mid-2024.

```typescript
// Gas cost estimation in the sub-gwei era
const gasPrice = await client.getGasPrice(); // ~0.1 gwei
const ethTransferCost = gasPrice * 21000n; // ~2,100 gwei = 0.0000021 ETH
// At $3,500 ETH: ~$0.007 per transfer
```

### MEV Landscape 2026

**Flashbots BuilderNet** (launched Dec 2024): Decentralized block building network using TEEs (Trusted Execution Environments). Builders run in secure enclaves, preventing them from frontrunning or censoring transactions. Aims to replace the centralized builder oligopoly.

**MEV-Share**: Redistribution protocol where searchers share MEV revenue with users whose transactions create the MEV opportunity. Users submit transactions to MEV-Share's matchmaker, receive a portion of backrun profits.

**Flashbots Protect RPC**: Drop-in RPC endpoint (`https://rpc.flashbots.net`) that prevents frontrunning by sending transactions directly to Flashbots builders, bypassing the public mempool. Supports `fast` mode (shared with all builders) and `privacy` mode (Flashbots builder only).

**Block Builder Ecosystem**: ~90% of Ethereum blocks are built by specialized builders via MEV-Boost. Top builders (Flashbots, beaverbuild, Titan) compete on bundle inclusion and gas price optimization. Proposer-Builder Separation (PBS) is de facto standard.

### Validator Economics

Current validator landscape (early 2026):
- **Staking yield**: ~3.0-3.5% APR (consensus + execution rewards)
- **MEV-Boost revenue**: Additional 0.3-0.8% APR via block building auctions
- **Restaking**: EigenLayer allows validators to secure additional services (AVSs) for extra yield, adding 1-5% APR depending on risk
- **Hardware**: PeerDAS increases bandwidth requirements (~1-2 Mbps sustained upload for blob sampling)
- **Minimum stake**: 32 ETH per validator, with EIP-7251 (Pectra) allowing consolidation up to 2048 ETH per validator

## References

- [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf) — Formal EVM specification
- [EIP-1559: Fee Market Change](https://eips.ethereum.org/EIPS/eip-1559) — Base fee + priority fee model
- [EIP-2718: Typed Transaction Envelope](https://eips.ethereum.org/EIPS/eip-2718) — Transaction type framework
- [EIP-2930: Access List](https://eips.ethereum.org/EIPS/eip-2930) — Type 1 transactions
- [EIP-4844: Shard Blob Transactions](https://eips.ethereum.org/EIPS/eip-4844) — Type 3 blob transactions
- [EIP-6780: SELFDESTRUCT Restriction](https://eips.ethereum.org/EIPS/eip-6780) — Dencun nerf
- [Solidity Storage Layout Docs](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)
- [Solidity ABI Specification](https://docs.soliditylang.org/en/latest/abi-spec.html)
- [EVM Opcodes Reference](https://www.evm.codes/) — Interactive opcode table with gas costs
- [EVM Deep Dives (noxx)](https://noxx.substack.com/) — Excellent visual EVM internals series
- [EIP-7702: Set EOA Account Code](https://eips.ethereum.org/EIPS/eip-7702) — EOA delegation for smart account features
- [EIP-2537: BLS12-381 Precompile](https://eips.ethereum.org/EIPS/eip-2537) — Native BLS operations
- [EIP-7594: PeerDAS](https://eips.ethereum.org/EIPS/eip-7594) — Peer Data Availability Sampling
- [EIP-7951: secp256r1 Precompile](https://eips.ethereum.org/EIPS/eip-7951) — Passkey signature verification
- [Flashbots Docs](https://docs.flashbots.net/) — MEV infrastructure and Protect RPC
- [ultrasound.money](https://ultrasound.money/) — ETH supply and burn tracking
