---
name: the-graph
description: "The Graph decentralized indexing protocol — subgraph development (schema.graphql, AssemblyScript mappings, subgraph.yaml manifest), GraphQL queries, Subgraph Studio deployment, hosted service migration, indexing optimization, and Graph Client for type-safe queries."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - the-graph
  - subgraph
  - indexing
  - graphql
  - blockchain-data
  - infrastructure
---

# The Graph

The Graph is a decentralized indexing protocol for querying blockchain data. Subgraphs define which smart contract events to index, how to transform them into entities, and expose them via a GraphQL API. The protocol supports Ethereum, Arbitrum, Optimism, Base, Polygon, Avalanche, BSC, Celo, Gnosis, and 40+ other networks.

## What You Probably Got Wrong

- **Hosted service is DEPRECATED** -- do not use `graph deploy --node https://api.thegraph.com/deploy/`. Use Subgraph Studio exclusively. Hosted service endpoints stopped serving queries in Q2 2024. All documentation referencing `--node https://api.thegraph.com/deploy/` is outdated.

- **Mappings are AssemblyScript, NOT TypeScript** -- despite `.ts` file extensions, subgraph mappings compile to WebAssembly via AssemblyScript. This means: no closures, no union types, no optional chaining (`?.`), no nullish coalescing (`??`), no `Array.map`/`filter`/`reduce`, no `JSON.parse`, no async/await, no try/catch. If you write standard TypeScript, the build will fail with cryptic errors.

- **`graph-ts` types are NOT standard TS types** -- `BigInt`, `BigDecimal`, `Bytes`, `Address`, and `ethereum.Event` come from `@graphprotocol/graph-ts`. They are NOT `bigint`, `number`, or `Uint8Array`. You must use `BigInt.fromI32()`, `BigDecimal.fromString()`, and `Address.fromString()` constructors. Arithmetic uses method calls: `a.plus(b)`, `a.minus(b)`, `a.times(b)`, `a.div(b)`.

- **`graph codegen` must run before build** -- entities and contract bindings are auto-generated from `schema.graphql` and ABIs. If you skip codegen, imports like `import { Transfer } from '../generated/ERC20/ERC20'` will fail. Always run `graph codegen` after ANY change to schema or ABIs.

- **Entity IDs must be `Bytes` or `String`, not numeric** -- the `@entity` directive requires an `id` field of type `ID!` which maps to `Bytes` or `String` in AssemblyScript. Using `BigInt` or `Int` as entity ID causes schema validation failure.

- **`store.get` returns nullable** -- `Entity.load(id)` returns `Entity | null`. You must null-check before accessing fields. AssemblyScript does not have optional chaining, so you need explicit `if (entity != null)` blocks.

- **Subgraph Studio requires authentication per machine** -- `graph auth --studio <deploy-key>` stores the key in `~/.graph`. This is per-machine, not per-project. CI/CD must re-auth on each run.

## Core Packages

```bash
npm install --save-dev @graphprotocol/graph-cli @graphprotocol/graph-ts
```

| Package | Purpose | Min Version |
|---------|---------|-------------|
| `@graphprotocol/graph-cli` | CLI for init, codegen, build, deploy | 0.80.0 |
| `@graphprotocol/graph-ts` | AssemblyScript runtime library (types, store API) | 0.35.0 |

## Subgraph Development Lifecycle

```
graph init --> graph codegen --> graph build --> graph deploy
```

### 1. Initialize a Subgraph

```bash
# Interactive init from a deployed contract
graph init --studio my-subgraph

# Non-interactive: specify all options
graph init --studio my-subgraph \
  --protocol ethereum \
  --network mainnet \
  --contract-name MyContract \
  --contract-address 0x1234567890abcdef1234567890abcdef12345678 \
  --abi ./abis/MyContract.json \
  --start-block 18000000
```

This generates:
- `subgraph.yaml` -- manifest
- `schema.graphql` -- entity definitions
- `src/my-contract.ts` -- mapping stubs (AssemblyScript)
- `abis/MyContract.json` -- contract ABI
- `package.json` with graph-cli and graph-ts

### 2. Define the Schema (`schema.graphql`)

Entities map to database tables. Each entity needs an `id: ID!` field.

```graphql
type Token @entity {
  id: Bytes!
  name: String!
  symbol: String!
  decimals: Int!
  totalSupply: BigInt!
  holders: [TokenHolder!]! @derivedFrom(field: "token")
}

type TokenHolder @entity {
  id: Bytes!
  token: Token!
  address: Bytes!
  balance: BigInt!
  lastTransferBlock: BigInt!
  lastTransferTimestamp: BigInt!
}

type Transfer @entity(immutable: true) {
  id: Bytes!
  from: Bytes!
  to: Bytes!
  value: BigInt!
  token: Token!
  blockNumber: BigInt!
  blockTimestamp: BigInt!
  transactionHash: Bytes!
}
```

**Schema rules:**
- `@entity` marks a type as a stored entity
- `@entity(immutable: true)` for append-only entities (events) -- improves indexing speed significantly
- `@derivedFrom(field: "token")` creates a virtual reverse lookup without storing data
- Supported scalar types: `ID`, `Bytes`, `String`, `Boolean`, `Int` (i32), `BigInt`, `BigDecimal`
- `Bytes!` is preferred over `String!` for IDs derived from addresses or hashes -- it avoids hex encoding overhead

### 3. Write the Manifest (`subgraph.yaml`)

```yaml
specVersion: 1.2.0
indexerHints:
  prune: auto
schema:
  file: ./schema.graphql
dataSources:
  - kind: ethereum
    name: ERC20
    network: mainnet
    source:
      address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
      abi: ERC20
      startBlock: 6082465
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.9
      language: wasm/assemblyscript
      entities:
        - Token
        - TokenHolder
        - Transfer
      abis:
        - name: ERC20
          file: ./abis/ERC20.json
      eventHandlers:
        - event: Transfer(indexed address,indexed address,uint256)
          handler: handleTransfer
        - event: Approval(indexed address,indexed address,uint256)
          handler: handleApproval
      file: ./src/mapping.ts
```

**Manifest rules:**
- `specVersion: 1.2.0` is the current spec
- `startBlock` should be the contract deployment block -- indexing from block 0 wastes hours
- Event signatures must match the ABI exactly, including `indexed` keywords
- `indexerHints.prune: auto` enables automatic pruning of historical entity versions to reduce disk usage
- `apiVersion: 0.0.9` is the current mapping API version

### 4. Write AssemblyScript Mappings

```typescript
// src/mapping.ts -- this is AssemblyScript, NOT TypeScript
import { Transfer as TransferEvent } from "../generated/ERC20/ERC20";
import { Token, TokenHolder, Transfer } from "../generated/schema";
import { BigInt, Bytes, Address } from "@graphprotocol/graph-ts";

// Zero address constant -- reused across handlers
const ZERO_ADDRESS = Address.fromString(
  "0x0000000000000000000000000000000000000000"
);

export function handleTransfer(event: TransferEvent): void {
  // Create immutable Transfer entity (append-only, never updated)
  let transfer = new Transfer(event.transaction.hash.concatI32(event.logIndex.toI32()));
  transfer.from = event.params.from;
  transfer.to = event.params.to;
  transfer.value = event.params.value;
  transfer.blockNumber = event.block.number;
  transfer.blockTimestamp = event.block.timestamp;
  transfer.transactionHash = event.transaction.hash;

  // Load or create Token entity
  let token = Token.load(event.address);
  if (token == null) {
    token = new Token(event.address);
    token.name = "";
    token.symbol = "";
    token.decimals = 0;
    token.totalSupply = BigInt.fromI32(0);
  }

  transfer.token = token.id;
  transfer.save();
  token.save();

  // Update sender balance (skip mint events where from == zero address)
  if (event.params.from != ZERO_ADDRESS) {
    let senderId = event.address.concat(event.params.from);
    let sender = TokenHolder.load(senderId);
    if (sender == null) {
      sender = new TokenHolder(senderId);
      sender.token = token.id;
      sender.address = event.params.from;
      sender.balance = BigInt.fromI32(0);
    }
    sender.balance = sender.balance.minus(event.params.value);
    sender.lastTransferBlock = event.block.number;
    sender.lastTransferTimestamp = event.block.timestamp;
    sender.save();
  }

  // Update receiver balance (skip burn events where to == zero address)
  if (event.params.to != ZERO_ADDRESS) {
    let receiverId = event.address.concat(event.params.to);
    let receiver = TokenHolder.load(receiverId);
    if (receiver == null) {
      receiver = new TokenHolder(receiverId);
      receiver.token = token.id;
      receiver.address = event.params.to;
      receiver.balance = BigInt.fromI32(0);
    }
    receiver.balance = receiver.balance.plus(event.params.value);
    receiver.lastTransferBlock = event.block.number;
    receiver.lastTransferTimestamp = event.block.timestamp;
    receiver.save();
  }
}
```

### 5. Codegen and Build

```bash
# Generate types from schema.graphql and ABIs
graph codegen

# Compile AssemblyScript to WebAssembly
graph build
```

Common build errors:
- `ERROR TS2322: Type 'X | null' is not assignable to type 'X'` -- null-check before use
- `ERROR TS2304: Cannot find name 'Transfer'` -- run `graph codegen` first
- `WARNING: using deprecated apiVersion` -- update `apiVersion` in subgraph.yaml

### 6. Deploy to Subgraph Studio

```bash
# Authenticate (one-time per machine)
graph auth --studio <DEPLOY_KEY>

# Deploy with version label
graph deploy --studio my-subgraph --version-label v0.1.0
```

## AssemblyScript Reference

### Type System

| Graph Type | AssemblyScript Class | Constructor |
|------------|---------------------|-------------|
| `Bytes` | `Bytes` | `Bytes.fromHexString("0x...")`, `event.address` |
| `BigInt` | `BigInt` | `BigInt.fromI32(0)`, `BigInt.fromString("1000000")` |
| `BigDecimal` | `BigDecimal` | `BigDecimal.fromString("1.5")` |
| `Address` | `Address` | `Address.fromString("0x...")` |
| `String` | `string` | Standard string literal |
| `Int` | `i32` | Standard i32 literal |
| `Boolean` | `boolean` | `true` / `false` |

### BigInt Arithmetic

```typescript
import { BigInt } from "@graphprotocol/graph-ts";

let a = BigInt.fromI32(100);
let b = BigInt.fromI32(50);

let sum = a.plus(b);          // 150
let diff = a.minus(b);        // 50
let product = a.times(b);     // 5000
let quotient = a.div(b);      // 2
let remainder = a.mod(b);     // 0
let power = a.pow(2);         // 10000

// Comparison
let isGreater = a.gt(b);      // true
let isEqual = a.equals(b);    // false
let isZero = a.isZero();      // false
```

### BigDecimal Arithmetic

```typescript
import { BigDecimal, BigInt } from "@graphprotocol/graph-ts";

let price = BigDecimal.fromString("1234.56");
let amount = BigDecimal.fromString("100");

let total = price.times(amount);       // 123456.00
let divided = price.div(amount);       // 12.3456

// Convert BigInt to BigDecimal for decimal math
let raw = BigInt.fromString("1000000000000000000"); // 1e18
let decimals = BigInt.fromI32(18);
let divisor = BigInt.fromI32(10).pow(decimals.toI32() as u8);
let normalized = raw.toBigDecimal().div(divisor.toBigDecimal()); // 1.0
```

### Bytes Operations

```typescript
import { Bytes, Address, ethereum } from "@graphprotocol/graph-ts";

// Create unique entity IDs from event data
let id = event.transaction.hash.concatI32(event.logIndex.toI32());

// Concatenate two Bytes values
let compositeId = event.address.concat(event.params.user);

// Convert Address to Bytes
let addr: Bytes = event.params.to;

// Hex string from Bytes
let hex = event.transaction.hash.toHexString();
```

### Critical AssemblyScript Restrictions

These will cause build failures. No workaround exists:

```typescript
// FORBIDDEN: closures / arrow functions as callbacks
// array.map(item => item.id)  <-- WILL NOT COMPILE

// FORBIDDEN: union types
// let x: string | null  <-- use nullable: string | null is OK only for class fields

// FORBIDDEN: optional chaining
// entity?.field  <-- WILL NOT COMPILE

// FORBIDDEN: nullish coalescing
// entity ?? defaultValue  <-- WILL NOT COMPILE

// FORBIDDEN: Array.map / filter / reduce
// Use a for loop instead:
let ids = new Array<string>();
for (let i = 0; i < items.length; i++) {
  ids.push(items[i].id.toHexString());
}

// FORBIDDEN: JSON.parse
// Use graph-ts json module if available, or decode manually

// FORBIDDEN: try/catch
// Errors in handlers cause the subgraph to fail and halt indexing

// FORBIDDEN: async/await
// All handlers are synchronous
```

### Nullable Field Patterns

```typescript
import { Token } from "../generated/schema";

// Loading an entity returns nullable
let token = Token.load(id);
if (token == null) {
  // Entity does not exist yet -- create it
  token = new Token(id);
  token.name = "Unknown";
  token.symbol = "???";
  token.decimals = 18;
  token.totalSupply = BigInt.fromI32(0);
}
// Safe to use token here -- guaranteed non-null
token.totalSupply = token.totalSupply.plus(amount);
token.save();
```

## Handler Types

### Event Handlers (most common)

Triggered when a specific event is emitted. Fastest and most reliable.

```yaml
# subgraph.yaml
eventHandlers:
  - event: Transfer(indexed address,indexed address,uint256)
    handler: handleTransfer
  - event: Approval(indexed address,indexed address,uint256)
    handler: handleApproval
```

```typescript
import { Transfer } from "../generated/ERC20/ERC20";

export function handleTransfer(event: Transfer): void {
  // event.params contains decoded event parameters
  let from = event.params.from;
  let to = event.params.to;
  let value = event.params.value;

  // event.block contains block metadata
  let blockNumber = event.block.number;
  let timestamp = event.block.timestamp;

  // event.transaction contains tx metadata
  let txHash = event.transaction.hash;
  let gasPrice = event.transaction.gasPrice;
}
```

### Call Handlers

Triggered on function calls. Slower than event handlers. Not supported on all networks.

```yaml
callHandlers:
  - function: transfer(address,uint256)
    handler: handleTransferCall
```

```typescript
import { TransferCall } from "../generated/ERC20/ERC20";

export function handleTransferCall(call: TransferCall): void {
  let to = call.inputs._to;
  let value = call.inputs._value;
  let success = call.outputs.value0; // return value
}
```

### Block Handlers

Triggered on every block (or filtered blocks). Use sparingly -- very expensive.

```yaml
blockHandlers:
  - handler: handleBlock
    filter:
      kind: polling
      every: 100
```

```typescript
import { ethereum } from "@graphprotocol/graph-ts";

export function handleBlock(block: ethereum.Block): void {
  let number = block.number;
  let timestamp = block.timestamp;
  let hash = block.hash;
}
```

## GraphQL Query Patterns

Query endpoint: `https://gateway.thegraph.com/api/{api-key}/subgraphs/id/{subgraph-id}`

### Basic Query

```graphql
{
  tokens(first: 10, orderBy: totalSupply, orderDirection: desc) {
    id
    name
    symbol
    totalSupply
  }
}
```

### Filtering with `where`

```graphql
{
  transfers(
    where: {
      value_gt: "1000000000000000000"
      from: "0xabcdef1234567890abcdef1234567890abcdef12"
      blockTimestamp_gte: "1700000000"
    }
    first: 100
    orderBy: blockNumber
    orderDirection: desc
  ) {
    id
    from
    to
    value
    blockNumber
  }
}
```

**Filter suffixes:**
- `field` -- exact match
- `field_not` -- not equal
- `field_gt` / `field_gte` -- greater than / greater or equal
- `field_lt` / `field_lte` -- less than / less or equal
- `field_in` / `field_not_in` -- in array
- `field_contains` -- substring match (String only)
- `field_starts_with` / `field_ends_with` -- prefix/suffix match

### Pagination

The Graph limits results to 1000 per query. For large datasets, paginate using `first` + `skip` or cursor-based pagination with `id_gt`.

```graphql
# Skip-based (simple but slow for deep pages)
{
  transfers(first: 100, skip: 200, orderBy: blockNumber) {
    id
    value
  }
}

# Cursor-based (fast for any depth -- preferred)
{
  transfers(
    first: 1000
    where: { id_gt: "0xlast_seen_id" }
    orderBy: id
  ) {
    id
    from
    to
    value
  }
}
```

**Pagination limit:** `skip` maxes out at 5000. For datasets beyond 5000, use cursor-based pagination with `id_gt`.

### Time-Travel Queries

Query entity state at a specific block number.

```graphql
{
  tokens(block: { number: 18000000 }) {
    id
    name
    totalSupply
  }
}
```

### Full-Text Search

Requires a `@fulltext` directive in the schema.

```graphql
# schema.graphql
type _Schema_
  @fulltext(
    name: "tokenSearch"
    language: en
    algorithm: rank
    include: [{ entity: "Token", fields: [{ name: "name" }, { name: "symbol" }] }]
  )
```

```graphql
{
  tokenSearch(text: "USDC") {
    id
    name
    symbol
  }
}
```

## Data Source Templates (Dynamic Contracts)

For factory patterns where new contracts are deployed at runtime (e.g., Uniswap pairs, lending pools).

```yaml
# subgraph.yaml
templates:
  - kind: ethereum
    name: Pair
    network: mainnet
    source:
      abi: Pair
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.9
      language: wasm/assemblyscript
      entities:
        - Swap
      abis:
        - name: Pair
          file: ./abis/Pair.json
      eventHandlers:
        - event: Swap(indexed address,uint256,uint256,uint256,uint256,indexed address)
          handler: handleSwap
      file: ./src/pair.ts
```

```typescript
// In factory handler -- dynamically create a new data source
import { Pair as PairTemplate } from "../generated/templates";

export function handlePairCreated(event: PairCreated): void {
  // Start indexing the new pair contract
  PairTemplate.create(event.params.pair);
}
```

## Contract Reads (eth_call in Mappings)

Read on-chain state from within a mapping handler.

```typescript
import { ERC20 } from "../generated/ERC20/ERC20";
import { Address } from "@graphprotocol/graph-ts";

export function handleTransfer(event: TransferEvent): void {
  // Bind to the contract at its address
  let contract = ERC20.bind(event.address);

  // try_ methods return ethereum.CallResult which has reverted flag
  let nameResult = contract.try_name();
  let symbolResult = contract.try_symbol();
  let decimalsResult = contract.try_decimals();

  let token = new Token(event.address);

  // Always use try_ to handle contracts that revert on view calls
  if (!nameResult.reverted) {
    token.name = nameResult.value;
  } else {
    token.name = "Unknown";
  }

  if (!symbolResult.reverted) {
    token.symbol = symbolResult.value;
  } else {
    token.symbol = "???";
  }

  if (!decimalsResult.reverted) {
    token.decimals = decimalsResult.value;
  } else {
    token.decimals = 18;
  }

  token.save();
}
```

**Contract read rules:**
- Always use `try_` prefixed methods -- non-try methods abort the handler on revert
- Contract reads are `eth_call`s at the handler's block -- they see state at that block
- Reads are slow compared to event data -- minimize them
- Some contracts (proxies, non-standard ERC20s) revert on `name()` or `symbol()` -- always handle reverts

## Indexing Performance Tips

### Use Immutable Entities

Entities marked `@entity(immutable: true)` are append-only. The indexer skips update tracking, reducing storage I/O by up to 80% for high-volume event entities.

```graphql
type Transfer @entity(immutable: true) {
  id: Bytes!
  from: Bytes!
  to: Bytes!
  value: BigInt!
  blockTimestamp: BigInt!
  transactionHash: Bytes!
}
```

### Use `Bytes` for Entity IDs

`Bytes` IDs are stored as raw bytes. `String` IDs require hex encoding/decoding on every load/save. For entities keyed by address or tx hash, `Bytes` is 2-3x faster.

### Set `startBlock` Correctly

Never index from block 0. Set `startBlock` to the contract's deployment block or the block of the first relevant event.

```bash
# Find deployment block using cast
cast receipt <TX_HASH> --rpc-url $RPC_URL | grep blockNumber
```

### Enable Pruning

```yaml
indexerHints:
  prune: auto
```

Prune removes historical entity versions. Subgraphs that do not need time-travel queries should enable pruning.

### Minimize Contract Reads

Each `try_*` call is an RPC request during indexing. Cache values in entities instead of re-reading on every event.

```typescript
// BAD: reads contract on every Transfer event
let name = contract.try_name();

// GOOD: read once, store in entity
let token = Token.load(event.address);
if (token == null) {
  token = new Token(event.address);
  let name = contract.try_name();
  token.name = name.reverted ? "Unknown" : name.value;
}
```

### Batch Entity IDs

Use `event.transaction.hash.concatI32(event.logIndex.toI32())` for unique IDs per event within a transaction. This avoids string concatenation overhead.

## Graph Client (Frontend Integration)

Type-safe GraphQL client for querying subgraphs from frontend or Node.js.

### Installation

```bash
npm install @graphprotocol/client-cli graphql
npx graphclient init
```

### Configuration (`.graphclientrc.yml`)

```yaml
sources:
  - name: MySubgraph
    handler:
      graphql:
        endpoint: https://gateway.thegraph.com/api/{api-key}/subgraphs/id/{subgraph-id}
```

### Usage in Application

```typescript
import { execute } from "../.graphclient";
import { gql } from "graphql";

const GET_TOKENS = gql`
  query GetTokens($first: Int!) {
    tokens(first: $first, orderBy: totalSupply, orderDirection: desc) {
      id
      name
      symbol
      totalSupply
    }
  }
`;

async function fetchTokens(): Promise<void> {
  const result = await execute(GET_TOKENS, { first: 10 });
  if (result.errors) {
    throw new Error(`Query failed: ${result.errors[0].message}`);
  }
  const tokens = result.data.tokens;
  for (const token of tokens) {
    console.log(`${token.symbol}: ${token.totalSupply}`);
  }
}
```

## Subgraph Composition (Multiple Data Sources)

Index multiple contracts in a single subgraph.

```yaml
dataSources:
  - kind: ethereum
    name: USDC
    network: mainnet
    source:
      address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
      abi: ERC20
      startBlock: 6082465
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.9
      language: wasm/assemblyscript
      entities:
        - Token
        - Transfer
      abis:
        - name: ERC20
          file: ./abis/ERC20.json
      eventHandlers:
        - event: Transfer(indexed address,indexed address,uint256)
          handler: handleTransfer
      file: ./src/mapping.ts

  - kind: ethereum
    name: WETH
    network: mainnet
    source:
      address: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
      abi: ERC20
      startBlock: 4719568
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.9
      language: wasm/assemblyscript
      entities:
        - Token
        - Transfer
      abis:
        - name: ERC20
          file: ./abis/ERC20.json
      eventHandlers:
        - event: Transfer(indexed address,indexed address,uint256)
          handler: handleTransfer
      file: ./src/mapping.ts
```

Both data sources share the same mapping file and entity types. The mapping code must handle both contracts.

## Grafting (Resume from Existing Subgraph)

Deploy a new subgraph version that starts from an existing subgraph's indexed state instead of re-indexing from scratch.

```yaml
features:
  - grafting
graft:
  base: QmExistingSubgraphDeploymentId
  block: 18500000
```

**Grafting rules:**
- `base` is the deployment ID (Qm... hash) of the source subgraph
- `block` is the block to graft from -- the new subgraph inherits all entity state at this block
- Grafting is for development iteration -- production subgraphs should be indexed from scratch
- Grafted subgraphs cannot be published to the decentralized network

## Common File Structure

```
my-subgraph/
  abis/
    ERC20.json
    Factory.json
  src/
    mapping.ts          # AssemblyScript event handlers
    factory.ts          # Factory pattern handlers
    helpers.ts          # Shared utility functions
  generated/
    schema.ts           # Auto-generated from schema.graphql (do not edit)
    ERC20/ERC20.ts      # Auto-generated from ABI (do not edit)
  schema.graphql        # Entity definitions
  subgraph.yaml         # Manifest
  package.json
  tsconfig.json
```

## Indexing Alternatives

The Graph is the standard for decentralized indexing, but it's not always the best fit. Consider alternatives for specific use cases.

### When NOT to Use The Graph

- **Small projects** (<5 entity types, simple queries): Setup overhead exceeds benefit
- **TypeScript-first teams**: AssemblyScript mapping layer adds friction
- **Real-time data** (<2 second freshness): Subgraph indexing has inherent latency (block confirmation + indexing time)
- **Complex joins/aggregations**: GraphQL limitations make multi-entity analytics painful
- **Rapid iteration**: Subgraph deployment and syncing takes minutes to hours

### Ponder

TypeScript-native indexing framework. Write handlers in TS (not AssemblyScript), get automatic GraphQL API, and iterate with hot reloading.

```typescript
// ponder.config.ts
import { createConfig } from "@ponder/core";
import { http } from "viem";
import { ERC20Abi } from "./abis/ERC20";

export default createConfig({
  networks: {
    mainnet: { chainId: 1, transport: http(process.env.PONDER_RPC_URL_1) },
  },
  contracts: {
    ERC20: {
      network: "mainnet",
      abi: ERC20Abi,
      address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
      startBlock: 6_082_465,
    },
  },
});

// src/ERC20.ts — event handler in TypeScript (not AssemblyScript)
import { ponder } from "@/generated";

ponder.on("ERC20:Transfer", async ({ event, context }) => {
  const { Account, Transfer } = context.db;

  await Account.upsert({ id: event.args.from });
  await Account.upsert({ id: event.args.to });

  await Transfer.create({
    id: event.log.id,
    data: {
      from: event.args.from,
      to: event.args.to,
      amount: event.args.value,
      timestamp: Number(event.block.timestamp),
    },
  });
});
```

**Why choose Ponder**: 10-15x faster iteration (hot reload, no deploy wait), full TypeScript (no AssemblyScript learning curve), viem types, automatic GraphQL API, runs locally or self-hosted. Best for teams that want subgraph-like indexing without the AssemblyScript tax.

### Dune Analytics

SQL-based blockchain analytics platform. Best for historical analysis, cross-protocol queries, and dashboards -- not real-time application backends.

```sql
-- Top USDC transfers in last 24 hours
SELECT
  "from",
  "to",
  value / 1e6 AS usdc_amount,
  block_time
FROM erc20_ethereum.evt_Transfer
WHERE contract_address = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
  AND block_time > now() - interval '24 hours'
ORDER BY value DESC
LIMIT 20;
```

**Why choose Dune**: Pre-indexed data across all major chains, SQL interface, community dashboards, no infrastructure to manage. **Not suitable for**: real-time dApp backends (query latency 5-30s), programmatic API access requires paid plan.

### Direct RPC + Multicall3

For simple read-heavy patterns, skip indexing entirely. Batch onchain reads with Multicall3.

```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({
  chain: mainnet,
  transport: http(),
});

// Batch multiple reads in a single RPC call
const results = await client.multicall({
  contracts: [
    { address: tokenA, abi: erc20Abi, functionName: 'balanceOf', args: [user] },
    { address: tokenB, abi: erc20Abi, functionName: 'balanceOf', args: [user] },
    { address: pool, abi: poolAbi, functionName: 'slot0' },
    { address: pool, abi: poolAbi, functionName: 'liquidity' },
  ],
});
```

Multicall3 is deployed at `0xcA11bde05977b3631167028862bE2a173976CA11` on 70+ chains (same address everywhere via CREATE2).

**Why choose direct RPC**: Zero infrastructure, real-time data, simple reads. **Not suitable for**: historical queries, event aggregation, complex entity relationships.

### Decision Matrix

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Production dApp backend | The Graph | Decentralized, reliable, GraphQL API |
| Rapid prototyping | Ponder | Hot reload, TypeScript, fast iteration |
| Analytics dashboard | Dune | SQL, pre-indexed, cross-protocol |
| Simple token balances | Multicall3 | Zero infra, real-time, trivial setup |
| Historical event aggregation | The Graph or Ponder | Both handle event indexing well |
| Cross-chain queries | Dune | Pre-indexed multi-chain data |
| Real-time price feeds | Direct RPC | Lowest latency |

## References

- Subgraph Studio: https://thegraph.com/studio/
- Official docs: https://thegraph.com/docs/en/
- Graph Explorer (find existing subgraphs): https://thegraph.com/explorer
- AssemblyScript docs: https://www.assemblyscript.org/
- graph-ts API reference: https://thegraph.com/docs/en/developing/graph-ts/api/
- Supported networks: https://thegraph.com/docs/en/developing/supported-networks/
