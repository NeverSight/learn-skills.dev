---
name: aptos
description: "Aptos Move-based L1 development — Move modules with global storage, resource accounts, Aptos SDK (@aptos-labs/ts-sdk), Coin standard, Token V2 (Digital Assets), view functions, multi-agent transactions, gas estimation, and Block-STM parallel execution."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: aptos
  category: L2 & Alt-L1
tags:
  - aptos
  - move
  - l1
  - parallel-execution
  - digital-assets
---

# Aptos Move L1 Development

Aptos is a Layer 1 blockchain built on Move, the language originally developed for Meta's Diem project. It achieves high throughput via Block-STM, a parallel execution engine that processes transactions optimistically and re-executes on conflicts. Smart contracts are called **modules**, and data is stored as **resources** at account addresses in a global storage model.

## What You Probably Got Wrong

> AI agents trained on Sui Move or Solidity make critical errors when generating Aptos Move code. Fix these first.

- **Aptos Move uses global storage, NOT Sui's object model** — Resources are stored at addresses using `move_to`, `move_from`, `borrow_global`, and `borrow_global_mut`. There is no `object::ObjectID` or `sui::object::UID`. When you want to store data, you `move_to<T>(signer, resource)` to place it at the signer's address. To read it, you `borrow_global<T>(address)`.

- **Resource accounts are NOT regular accounts** — A resource account is a special account with no private key, controlled by its creating module. You create one with `account::create_resource_account(origin, seed)`. The module publishes to the resource account's address. This is how protocols deploy immutable, admin-less contracts.

- **Token V1 is deprecated — use Token V2 (Digital Assets)** — The `aptos_token` module (V1) is legacy. Use `aptos_token_objects` (V2), which uses the Move Object model. V2 tokens are stored as objects at their own addresses, not in a creator's TokenStore. Collections and tokens are first-class objects.

- **`@aptos-labs/ts-sdk` replaces the old `aptos` package** — The npm package `aptos` is deprecated. Use `@aptos-labs/ts-sdk`. The entry point is `new Aptos(new AptosConfig({ network: Network.MAINNET }))`. Do not import from `aptos`.

- **Coin standard is NOT ERC-20** — Aptos uses `aptos_framework::coin` with generics. A coin type is `Coin<CoinType>` where `CoinType` is a phantom type parameter defined by the deploying module. There is no approval/allowance pattern — coins are moved directly.

- **`signer` is not `msg.sender`** — In Aptos Move, the `signer` is passed as a function parameter. A function must explicitly accept `&signer` to access the caller's address and perform operations on their account. Use `signer::address_of(account)` to get the address.

- **View functions are explicit** — You must annotate functions with `#[view]` to make them callable off-chain without a transaction. They cannot modify state. They are called via the `/view` API endpoint, not through transaction submission.

- **`u256` exists but `u64` is standard for amounts** — Unlike Solidity's `uint256` default, Aptos uses `u64` for coin amounts and most counters. `u256` exists but is rarely used. APT has 8 decimals (not 18). 1 APT = 100,000,000 octas.

## Chain Configuration

### Mainnet

| Property | Value |
|----------|-------|
| Chain ID | **1** |
| Currency | APT (8 decimals) |
| Block Time | ~100-300ms (sub-second) |
| Finality | ~900ms |
| Max Gas Unit | 2,000,000 |
| Gas Unit Price | Min 100 octas |
| VM | Move VM with Block-STM |
| Consensus | AptosBFT (DiemBFT v4) |

#### RPC Endpoints

| URL | Provider | Notes |
|-----|----------|-------|
| `https://fullnode.mainnet.aptoslabs.com/v1` | Aptos Labs | Default REST API |
| `https://mainnet.aptoslabs.com/v1` | Aptos Labs | Alternative |
| `https://aptos-mainnet.nodereal.io/v1` | NodeReal | Rate-limited |

#### Block Explorers

| Explorer | URL |
|----------|-----|
| Aptos Explorer | https://explorer.aptoslabs.com |
| Aptscan | https://aptscan.ai |

### Testnet

| Property | Value |
|----------|-------|
| Chain ID | **2** |
| RPC | `https://fullnode.testnet.aptoslabs.com/v1` |
| Faucet | `https://faucet.testnet.aptoslabs.com` |
| Explorer | https://explorer.aptoslabs.com/?network=testnet |

### Devnet

| Property | Value |
|----------|-------|
| Chain ID | **varies** (resets frequently) |
| RPC | `https://fullnode.devnet.aptoslabs.com/v1` |
| Faucet | `https://faucet.devnet.aptoslabs.com` |

## Quick Start

### Install Aptos CLI

```bash
# macOS
brew install aptos

# Linux / manual
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3

# Verify
aptos --version
```

### Create a New Move Project

```bash
# Initialize a new Move package
aptos move init --name my_module

# Project structure:
# my_module/
# ├── Move.toml
# └── sources/
#     └── my_module.move
```

### Move.toml Configuration

```toml
[package]
name = "my_module"
version = "0.1.0"

[addresses]
my_addr = "_"

[dependencies]
AptosFramework = { git = "https://github.com/aptos-labs/aptos-core.git", subdir = "aptos-move/framework/aptos-framework", rev = "mainnet" }
AptosTokenObjects = { git = "https://github.com/aptos-labs/aptos-core.git", subdir = "aptos-move/framework/aptos-token-objects", rev = "mainnet" }
```

### TypeScript SDK Setup

```bash
npm install @aptos-labs/ts-sdk
```

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const config = new AptosConfig({ network: Network.MAINNET });
const aptos = new Aptos(config);
```

## Move Module Development

### Module Structure

```move
module my_addr::counter {
    use std::signer;

    struct Counter has key {
        value: u64,
    }

    /// Initialize a counter resource at the signer's address
    public entry fun initialize(account: &signer) {
        let counter = Counter { value: 0 };
        move_to(account, counter);
    }

    /// Increment the counter stored at the signer's address
    public entry fun increment(account: &signer) acquires Counter {
        let addr = signer::address_of(account);
        let counter = borrow_global_mut<Counter>(addr);
        counter.value = counter.value + 1;
    }

    /// Read the counter value at any address
    #[view]
    public fun get_count(addr: address): u64 acquires Counter {
        borrow_global<Counter>(addr).value
    }
}
```

### Key Move Concepts

#### Global Storage Operations

```move
// Store a resource at signer's address (signer must not already have one)
move_to<T>(signer, resource);

// Remove and return a resource from an address
let resource = move_from<T>(addr);

// Immutable reference to resource at address
let ref = borrow_global<T>(addr);

// Mutable reference to resource at address
let ref_mut = borrow_global_mut<T>(addr);

// Check if a resource exists at address
let exists = exists<T>(addr);
```

#### Abilities

```move
// has copy — value can be copied
// has drop — value can be dropped (destroyed implicitly)
// has store — value can be stored inside another struct
// has key — value can be stored as a top-level resource in global storage

struct Coin has store {
    value: u64,
}

struct CoinStore has key {
    coin: Coin,
}
```

#### Access Control Pattern

```move
module my_addr::admin {
    use std::signer;

    struct AdminConfig has key {
        admin: address,
    }

    const E_NOT_ADMIN: u64 = 1;
    const E_ALREADY_INITIALIZED: u64 = 2;

    public entry fun initialize(account: &signer) {
        let addr = signer::address_of(account);
        assert!(!exists<AdminConfig>(addr), E_ALREADY_INITIALIZED);
        move_to(account, AdminConfig { admin: addr });
    }

    public entry fun admin_only_action(account: &signer, config_addr: address) acquires AdminConfig {
        let config = borrow_global<AdminConfig>(config_addr);
        assert!(signer::address_of(account) == config.admin, E_NOT_ADMIN);
        // perform privileged action
    }
}
```

### Events

```move
module my_addr::events_example {
    use aptos_framework::event;

    #[event]
    struct TransferEvent has drop, store {
        from: address,
        to: address,
        amount: u64,
    }

    public entry fun transfer(from: &signer, to: address, amount: u64) {
        // ... transfer logic ...
        event::emit(TransferEvent {
            from: signer::address_of(from),
            to,
            amount,
        });
    }
}
```

### Resource Accounts

```move
module my_addr::resource_account_example {
    use std::signer;
    use aptos_framework::account;
    use aptos_framework::resource_account;

    struct ModuleData has key {
        resource_signer_cap: account::SignerCapability,
    }

    /// Called once during module publication to a resource account.
    /// The resource account's signer capability is stored for later use.
    fun init_module(resource_signer: &signer) {
        let resource_signer_cap = resource_account::retrieve_resource_account_cap(
            resource_signer,
            @source_addr
        );
        move_to(resource_signer, ModuleData {
            resource_signer_cap,
        });
    }

    /// Use the stored signer capability to act as the resource account
    public entry fun do_something(caller: &signer) acquires ModuleData {
        let module_data = borrow_global<ModuleData>(@my_addr);
        let resource_signer = account::create_signer_with_capability(
            &module_data.resource_signer_cap
        );
        // resource_signer can now sign transactions on behalf of the resource account
    }
}
```

## Coin Standard

### Creating a Custom Coin

```move
module my_addr::my_coin {
    use std::signer;
    use std::string;
    use aptos_framework::coin;

    /// Phantom type marker for the coin — defines the coin type globally
    struct MyCoin {}

    struct CoinCapabilities has key {
        burn_cap: coin::BurnCapability<MyCoin>,
        freeze_cap: coin::FreezeCapability<MyCoin>,
        mint_cap: coin::MintCapability<MyCoin>,
    }

    const E_NOT_ADMIN: u64 = 1;

    public entry fun initialize(account: &signer) {
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<MyCoin>(
            account,
            string::utf8(b"My Coin"),
            string::utf8(b"MYC"),
            8, // decimals
            true, // monitor_supply
        );
        move_to(account, CoinCapabilities {
            burn_cap,
            freeze_cap,
            mint_cap,
        });
    }

    public entry fun mint(
        account: &signer,
        to: address,
        amount: u64,
    ) acquires CoinCapabilities {
        let addr = signer::address_of(account);
        let caps = borrow_global<CoinCapabilities>(addr);
        let coins = coin::mint(amount, &caps.mint_cap);
        coin::deposit(to, coins);
    }

    public entry fun burn(
        account: &signer,
        amount: u64,
    ) acquires CoinCapabilities {
        let addr = signer::address_of(account);
        let caps = borrow_global<CoinCapabilities>(addr);
        let coins = coin::withdraw<MyCoin>(account, amount);
        coin::burn(coins, &caps.burn_cap);
    }
}
```

### Registering for a Coin

```move
// Before receiving any coin type, an account must register for it
public entry fun register_coin<CoinType>(account: &signer) {
    coin::register<CoinType>(account);
}
```

## Token V2 — Digital Assets

### Creating a Collection and Token

```move
module my_addr::nft {
    use std::signer;
    use std::string::{Self, String};
    use std::option;
    use aptos_token_objects::collection;
    use aptos_token_objects::token;

    struct TokenRefs has key {
        burn_ref: token::BurnRef,
        transfer_ref: option::Option<object::TransferRef>,
        mutator_ref: token::MutatorRef,
    }

    public entry fun create_collection(creator: &signer) {
        collection::create_unlimited_collection(
            creator,
            string::utf8(b"Collection description"),
            string::utf8(b"My Collection"),
            option::none(), // no royalty
            string::utf8(b"https://example.com/collection"),
        );
    }

    public entry fun mint_token(creator: &signer) {
        let constructor_ref = token::create_named_token(
            creator,
            string::utf8(b"My Collection"),
            string::utf8(b"Token description"),
            string::utf8(b"Token #1"),
            option::none(), // no royalty
            string::utf8(b"https://example.com/token/1"),
        );

        let token_signer = object::generate_signer(&constructor_ref);
        let burn_ref = token::generate_burn_ref(&constructor_ref);
        let mutator_ref = token::generate_mutator_ref(&constructor_ref);

        move_to(&token_signer, TokenRefs {
            burn_ref,
            transfer_ref: option::none(),
            mutator_ref,
        });
    }
}
```

## TypeScript SDK (@aptos-labs/ts-sdk)

### Client Initialization

```typescript
import {
  Aptos,
  AptosConfig,
  Network,
  Account,
  Ed25519PrivateKey,
  AccountAddress,
} from "@aptos-labs/ts-sdk";

// Mainnet
const aptos = new Aptos(new AptosConfig({ network: Network.MAINNET }));

// Testnet
const aptosTestnet = new Aptos(new AptosConfig({ network: Network.TESTNET }));

// Custom node
const aptosCustom = new Aptos(
  new AptosConfig({
    fullnode: "https://my-node.example.com/v1",
    indexer: "https://my-indexer.example.com/v1/graphql",
  })
);
```

### Account Management

```typescript
// Generate a new account
const account = Account.generate();
console.log("Address:", account.accountAddress.toString());
console.log("Private key:", account.privateKey.toString());

// From existing private key
const privateKey = new Ed25519PrivateKey("0x...");
const existingAccount = Account.fromPrivateKey({ privateKey });

// Fund on testnet
const aptosTestnet = new Aptos(new AptosConfig({ network: Network.TESTNET }));
await aptosTestnet.fundAccount({
  accountAddress: account.accountAddress,
  amount: 100_000_000, // 1 APT = 100,000,000 octas
});
```

### Transfer APT

```typescript
async function transferAPT(
  aptos: Aptos,
  sender: Account,
  recipientAddress: string,
  amountOctas: number
): Promise<string> {
  const transaction = await aptos.transaction.build.simple({
    sender: sender.accountAddress,
    data: {
      function: "0x1::aptos_account::transfer",
      functionArguments: [AccountAddress.from(recipientAddress), amountOctas],
    },
  });

  const pendingTx = await aptos.signAndSubmitTransaction({
    signer: sender,
    transaction,
  });

  const committedTx = await aptos.waitForTransaction({
    transactionHash: pendingTx.hash,
  });

  return committedTx.hash;
}
```

### View Functions

```typescript
async function getBalance(aptos: Aptos, address: string): Promise<bigint> {
  const result = await aptos.view({
    payload: {
      function: "0x1::coin::balance",
      typeArguments: ["0x1::aptos_coin::AptosCoin"],
      functionArguments: [AccountAddress.from(address)],
    },
  });
  return BigInt(result[0] as string);
}
```

### Read Account Resources

```typescript
async function getCoinStore(aptos: Aptos, address: string) {
  return aptos.getAccountResource({
    accountAddress: AccountAddress.from(address),
    resourceType: "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",
  });
}
```

### Multi-Agent Transactions

```typescript
// Multi-agent: multiple signers for one transaction
async function multiAgentTransfer(
  aptos: Aptos,
  sender: Account,
  secondSigner: Account
) {
  const transaction = await aptos.transaction.build.multiAgent({
    sender: sender.accountAddress,
    secondarySignerAddresses: [secondSigner.accountAddress],
    data: {
      function: "0xmodule::my_module::multi_signer_action",
      functionArguments: [],
    },
  });

  const senderAuth = aptos.transaction.sign({
    signer: sender,
    transaction,
  });

  const secondAuth = aptos.transaction.sign({
    signer: secondSigner,
    transaction,
  });

  const pendingTx = await aptos.transaction.submit.multiAgent({
    transaction,
    senderAuthenticator: senderAuth,
    additionalSignersAuthenticators: [secondAuth],
  });

  return aptos.waitForTransaction({ transactionHash: pendingTx.hash });
}
```

### Gas Estimation

```typescript
async function estimateGas(aptos: Aptos, sender: Account) {
  const transaction = await aptos.transaction.build.simple({
    sender: sender.accountAddress,
    data: {
      function: "0x1::aptos_account::transfer",
      functionArguments: [
        AccountAddress.from("0xrecipient"),
        100_000_000,
      ],
    },
  });

  // Simulate to get gas estimate
  const simulation = await aptos.transaction.simulate.simple({
    signerPublicKey: sender.publicKey,
    transaction,
  });

  const gasUsed = BigInt(simulation[0].gas_used);
  const gasUnitPrice = BigInt(simulation[0].gas_unit_price);
  const totalCost = gasUsed * gasUnitPrice;

  return { gasUsed, gasUnitPrice, totalCost };
}
```

## Compile and Deploy

### Compile Module

```bash
# Compile
aptos move compile --named-addresses my_addr=default

# Run tests
aptos move test --named-addresses my_addr=default

# Publish to testnet (requires funded account)
aptos move publish --named-addresses my_addr=default --profile testnet
```

### CLI Account Setup

```bash
# Initialize a new profile (generates keypair, funds on devnet/testnet)
aptos init --profile testnet --network testnet

# Initialize with existing private key
aptos init --profile mainnet --private-key 0x... --network mainnet

# Check account balance
aptos account balance --profile testnet
```

See `examples/deploy-module/` for full SDK deployment code.

## Testing Move Modules

```move
#[test_only]
module my_addr::counter_tests {
    use std::signer;
    use my_addr::counter;

    #[test(account = @0x1)]
    fun test_initialize(account: &signer) {
        counter::initialize(account);
        let addr = signer::address_of(account);
        assert!(counter::get_count(addr) == 0, 0);
    }

    #[test(account = @0x1)]
    fun test_increment(account: &signer) {
        counter::initialize(account);
        counter::increment(account);
        let addr = signer::address_of(account);
        assert!(counter::get_count(addr) == 1, 0);
    }

    #[test(account = @0x1)]
    #[expected_failure(abort_code = 0x60001, location = aptos_framework::account)]
    fun test_double_initialize(account: &signer) {
        counter::initialize(account);
        counter::initialize(account); // should fail: resource already exists
    }
}
```

## Block-STM Parallel Execution

Aptos uses Block-STM for optimistic parallel execution. Transactions within a block execute concurrently. If two transactions conflict (read/write to the same resource), one is re-executed.

### What This Means for Developers

- **Independent transactions run in parallel** — Transactions touching different accounts or resources execute simultaneously.
- **Contention on hot resources serializes execution** — If your contract uses a single global counter that every transaction increments, Block-STM will detect the conflict and serialize those transactions. Performance degrades to sequential.
- **Design for parallelism** — Use per-user resources instead of global state when possible. Example: instead of a global `TotalDeposits` counter, track deposits per-user and aggregate off-chain.

### Anti-Pattern: Global Hot Resource

```move
// BAD: Every deposit transaction conflicts on the same resource
struct GlobalState has key {
    total_deposits: u64,
}

public entry fun deposit(account: &signer, amount: u64) acquires GlobalState {
    let state = borrow_global_mut<GlobalState>(@module_addr);
    state.total_deposits = state.total_deposits + amount;
    // every deposit serializes here
}
```

### Pattern: Per-User State

```move
// GOOD: Each user's deposit is independent — parallel-friendly
struct UserDeposit has key {
    amount: u64,
}

public entry fun deposit(account: &signer, amount: u64) acquires UserDeposit {
    let addr = signer::address_of(account);
    if (exists<UserDeposit>(addr)) {
        let deposit = borrow_global_mut<UserDeposit>(addr);
        deposit.amount = deposit.amount + amount;
    } else {
        move_to(account, UserDeposit { amount });
    };
}
```

## Move Object Model

The Move Object model (used by Token V2) creates objects at deterministic addresses. Objects are distinct from resources stored at user addresses.

```move
module my_addr::object_example {
    use aptos_framework::object::{Self, Object, ConstructorRef};
    use std::signer;

    struct MyObject has key {
        value: u64,
    }

    /// Create a named object at a deterministic address
    public entry fun create(creator: &signer) {
        let constructor_ref = object::create_named_object(
            creator,
            b"my_object_seed",
        );
        let object_signer = object::generate_signer(&constructor_ref);
        move_to(&object_signer, MyObject { value: 42 });
    }

    /// Transfer ownership of an object
    public entry fun transfer_object(
        owner: &signer,
        obj: Object<MyObject>,
        to: address,
    ) {
        object::transfer(owner, obj, to);
    }

    #[view]
    public fun get_value(obj: Object<MyObject>): u64 acquires MyObject {
        let obj_addr = object::object_address(&obj);
        borrow_global<MyObject>(obj_addr).value
    }
}
```

## Common Patterns

### Table Storage (Key-Value Map)

```move
use aptos_std::table::{Self, Table};

struct Registry has key {
    entries: Table<address, u64>,
}

public entry fun add_entry(account: &signer, key: address, value: u64) acquires Registry {
    let registry = borrow_global_mut<Registry>(signer::address_of(account));
    table::upsert(&mut registry.entries, key, value);
}

#[view]
public fun get_entry(registry_addr: address, key: address): u64 acquires Registry {
    let registry = borrow_global<Registry>(registry_addr);
    *table::borrow(&registry.entries, key)
}
```

### Timestamp

```move
use aptos_framework::timestamp;

public fun is_expired(deadline: u64): bool {
    timestamp::now_seconds() > deadline
}
```

## Indexer and GraphQL

Aptos provides a GraphQL indexer for querying historical data, events, and token ownership.

| Network | Indexer URL |
|---------|-------------|
| Mainnet | `https://indexer.mainnet.aptoslabs.com/v1/graphql` |
| Testnet | `https://indexer.testnet.aptoslabs.com/v1/graphql` |

Key tables: `current_token_ownerships_v2` (NFT ownership), `current_token_datas_v2` (token metadata), `coin_activities` (transfer history), `account_transactions` (transaction history).

See `examples/read-resources/` for full GraphQL query patterns.

## Reference Links

- Official Docs: https://aptos.dev
- Move Language Reference: https://aptos.dev/en/build/smart-contracts/book
- TypeScript SDK: https://github.com/aptos-labs/aptos-ts-sdk
- Framework Source: https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/framework
- Token V2 Standard: https://aptos.dev/en/build/smart-contracts/digital-asset
- Move Prover: https://aptos.dev/en/build/smart-contracts/prover

Last verified: 2025-12-01
