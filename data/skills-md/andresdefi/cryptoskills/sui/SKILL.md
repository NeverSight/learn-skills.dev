---
name: sui
description: "Sui Move-based L1 development — object-centric ownership model, Programmable Transaction Blocks (PTBs), Sui SDK (@mysten/sui), shared vs owned objects, Move module publishing, gas sponsorship, zkLogin authentication, and parallel execution via object ownership."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: sui
  category: L2 & Alt-L1
tags:
  - sui
  - move
  - l1
  - object-model
  - ptb
  - mysten
---

# Sui L1 Development

## What You Probably Got Wrong

### Sui Move is NOT Aptos Move

Sui forked Move from Diem and fundamentally changed the storage model. If you learned Move from Aptos, unlearn these things:

| Concept | Aptos Move | Sui Move |
|---------|------------|----------|
| Storage model | Global storage (`move_to`, `borrow_global`) | Object-centric (objects have UIDs) |
| Resource location | Stored under account addresses | Objects exist independently with ownership |
| Transfer | `coin::transfer(from, to)` with signer | `transfer::transfer(obj, recipient)` |
| Entry functions | `public entry fun f(signer: &signer)` | `public entry fun f(ctx: &mut TxContext)` |
| Object identity | No native concept | Every object has `sui::object::UID` |
| Standard library | `aptos_framework` | `sui` (at `0x2`) |
| Coin type | `aptos_framework::coin::Coin<T>` | `sui::coin::Coin<T>` |
| Init function | `init_module(signer: &signer)` | `fun init(ctx: &mut TxContext)` |

### Objects Have Ownership

Every Sui object has an owner. This determines who can use it in transactions and whether transactions can execute in parallel:

- **Owned objects** -- belong to a single address. Only that address can use them. Transactions on different owned objects parallelize.
- **Shared objects** -- accessible by anyone. Requires consensus ordering. Use `transfer::share_object(obj)`.
- **Immutable objects** -- frozen forever. Anyone can read. Use `transfer::freeze_object(obj)`.
- **Wrapped objects** -- stored inside another object's struct field. Not directly accessible on-chain.

The ownership model is WHY Sui achieves parallel execution. Transactions touching different owned objects never conflict.

### PTBs Are Not Just Batching

Programmable Transaction Blocks (PTBs) are Sui's composability primitive. They are NOT just "batch transactions":

- Up to 1024 commands in a single transaction
- Commands can reference outputs of previous commands within the same PTB
- Atomic -- all commands succeed or all revert
- No need for smart contract "router" patterns -- compose at the transaction level
- Move calls, transfers, splits, merges all in one PTB

### The SDK Was Renamed

The old `@mysten/sui.js` package is deprecated. The current package is `@mysten/sui`. If you see imports from `@mysten/sui.js`, update them:

```typescript
// WRONG -- deprecated
import { SuiClient } from "@mysten/sui.js/client";
import { TransactionBlock } from "@mysten/sui.js/transactions";

// CORRECT -- current SDK
import { SuiClient } from "@mysten/sui/client";
import { Transaction } from "@mysten/sui/transactions";
```

Also, `TransactionBlock` was renamed to `Transaction` in the current SDK.

## Chain Configuration

### Mainnet

| Property | Value |
|----------|-------|
| Network | `mainnet` |
| RPC | `https://fullnode.mainnet.sui.io:443` |
| GraphQL | `https://sui-mainnet.mystenlabs.com/graphql` |
| Currency | SUI (9 decimals) |
| Epoch Duration | ~24 hours |
| Max TX Size | 128 KB |
| Max PTB Commands | 1024 |
| Max Pure Arg Size | 16 KB |

### Testnet

| Property | Value |
|----------|-------|
| Network | `testnet` |
| RPC | `https://fullnode.testnet.sui.io:443` |
| GraphQL | `https://sui-testnet.mystenlabs.com/graphql` |
| Faucet | `https://faucet.testnet.sui.io` |
| Explorer | https://suiscan.xyz/testnet |

### Devnet

| Property | Value |
|----------|-------|
| Network | `devnet` |
| RPC | `https://fullnode.devnet.sui.io:443` |
| Faucet | `https://faucet.devnet.sui.io` |
| Explorer | https://suiscan.xyz/devnet |

### Block Explorers

| Explorer | URL |
|----------|-----|
| SuiScan | https://suiscan.xyz |
| SuiVision | https://suivision.xyz |
| Sui Explorer (official) | https://suiexplorer.com |

## System Packages

Sui has three system packages at well-known addresses:

| Package | Address | Contents |
|---------|---------|----------|
| Move Stdlib | `0x1` | `vector`, `option`, `string`, `ascii` |
| Sui Framework | `0x2` | `object`, `transfer`, `tx_context`, `coin`, `clock`, `table`, `dynamic_field`, `event`, `package`, `display`, `kiosk` |
| Sui System | `0x3` | `sui_system`, `staking_pool`, `validator` |

### Key Singleton Objects

| Object | Address | Usage |
|--------|---------|-------|
| Clock | `0x6` | On-chain timestamp (`sui::clock::Clock`) |
| System State | `0x5` | Validator set, epoch info |
| Random | `0x8` | On-chain randomness (Move `sui::random::Random`) |

## Move Language on Sui

### Module Structure

```move
module my_package::my_module {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;

    /// A custom object. `key` ability makes it a Sui object.
    /// `store` ability allows it to be transferred and stored in other objects.
    public struct MyObject has key, store {
        id: UID,
        value: u64,
    }

    /// Module initializer -- called once at publish time.
    /// Receives a one-time witness if the module name matches the witness type.
    fun init(ctx: &mut TxContext) {
        let obj = MyObject {
            id: object::new(ctx),
            value: 42,
        };
        transfer::transfer(obj, tx_context::sender(ctx));
    }
}
```

### Struct Abilities

| Ability | Meaning | Required For |
|---------|---------|--------------|
| `key` | Is a Sui object (must have `id: UID` as first field) | All Sui objects |
| `store` | Can be stored inside other objects, can be transferred with `public_transfer` | Transferable objects, dynamic fields |
| `copy` | Can be copied by value | Primitives, events |
| `drop` | Can be discarded/destroyed implicitly | Events, witnesses |

Objects that are Sui objects MUST have `key` ability and `id: UID` as their first field.

### Object Creation and Transfer

```move
module my_package::nft {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::string::String;

    public struct NFT has key, store {
        id: UID,
        name: String,
        description: String,
    }

    /// Create and transfer to caller
    public entry fun mint(
        name: String,
        description: String,
        ctx: &mut TxContext,
    ) {
        let nft = NFT {
            id: object::new(ctx),
            name,
            description,
        };
        transfer::public_transfer(nft, tx_context::sender(ctx));
    }

    /// Transfer to a different address
    public entry fun transfer_nft(
        nft: NFT,
        recipient: address,
    ) {
        transfer::public_transfer(nft, recipient);
    }

    /// Destroy the NFT
    public entry fun burn(nft: NFT) {
        let NFT { id, name: _, description: _ } = nft;
        object::delete(id);
    }
}
```

### transfer vs public_transfer

- `transfer::transfer(obj, recipient)` -- for objects WITHOUT `store` ability. Can only be called within the module that defines the type.
- `transfer::public_transfer(obj, recipient)` -- for objects WITH `store` ability. Can be called from any module or PTB.

Same pattern applies to `share_object` / `public_share_object` and `freeze_object` / `public_freeze_object`.

### Shared Objects

```move
module my_package::counter {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::TxContext;

    public struct Counter has key {
        id: UID,
        count: u64,
    }

    /// Create and share -- anyone can mutate
    fun init(ctx: &mut TxContext) {
        let counter = Counter {
            id: object::new(ctx),
            count: 0,
        };
        transfer::share_object(counter);
    }

    /// Requires &mut reference -- consensus-ordered
    public entry fun increment(counter: &mut Counter) {
        counter.count = counter.count + 1;
    }

    /// Read-only reference -- does not require consensus ordering
    public fun value(counter: &Counter): u64 {
        counter.count
    }
}
```

Shared objects require consensus ordering. Prefer owned objects when possible for parallel execution.

### One-Time Witness (OTW) Pattern

Used for operations that should happen exactly once (e.g., creating a coin type):

```move
module my_package::my_coin {
    use sui::coin;
    use sui::transfer;
    use sui::tx_context::TxContext;

    /// OTW must: match module name (uppercase), have only `drop`, no fields
    public struct MY_COIN has drop {}

    fun init(witness: MY_COIN, ctx: &mut TxContext) {
        let (treasury_cap, metadata) = coin::create_currency<MY_COIN>(
            witness,
            9,                              // decimals
            b"MYC",                         // symbol
            b"My Coin",                     // name
            b"A custom fungible token",     // description
            option::none(),                 // icon URL
            ctx,
        );
        transfer::public_freeze_object(metadata);
        transfer::public_transfer(treasury_cap, tx_context::sender(ctx));
    }
}
```

OTW rules: struct name matches MODULE name (uppercased), has only `drop` ability, has no fields.

### Dynamic Fields

Attach arbitrary key-value data to objects at runtime:

```move
module my_package::dynamic_example {
    use sui::object::{Self, UID};
    use sui::dynamic_field;
    use sui::tx_context::TxContext;

    public struct Parent has key {
        id: UID,
    }

    /// Add a dynamic field
    public fun add_field(parent: &mut Parent, key: u64, value: vector<u8>) {
        dynamic_field::add(&mut parent.id, key, value);
    }

    /// Read a dynamic field
    public fun get_field(parent: &Parent, key: u64): &vector<u8> {
        dynamic_field::borrow(&parent.id, key)
    }

    /// Remove a dynamic field
    public fun remove_field(parent: &mut Parent, key: u64): vector<u8> {
        dynamic_field::remove(&mut parent.id, key)
    }
}
```

Use `dynamic_object_field` instead of `dynamic_field` when the value is a Sui object (has `key` ability) and should remain accessible by ID.

### Events

```move
module my_package::events_example {
    use sui::event;

    /// Event structs need `copy` and `drop`
    public struct ItemCreated has copy, drop {
        item_id: address,
        creator: address,
    }

    public fun emit_creation(item_id: address, creator: address) {
        event::emit(ItemCreated { item_id, creator });
    }
}
```

## Sui SDK (TypeScript)

### Installation

```bash
npm install @mysten/sui
```

### Client Setup

```typescript
import { SuiClient, getFullnodeUrl } from "@mysten/sui/client";

const client = new SuiClient({ url: getFullnodeUrl("mainnet") });
// Options: "mainnet", "testnet", "devnet"
```

### Keypair and Signing

```typescript
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";
import { fromBase64 } from "@mysten/sui/utils";

// Generate new keypair
const keypair = new Ed25519Keypair();

// From private key bytes
const keypairFromKey = Ed25519Keypair.fromSecretKey(fromBase64(process.env.SUI_PRIVATE_KEY));

// Derive from mnemonic
const keypairFromMnemonic = Ed25519Keypair.deriveKeypair(
    "word1 word2 ... word12"
);

console.log("Address:", keypair.getPublicKey().toSuiAddress());
```

### Building Transactions (PTBs)

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();

// Split coin -- take 1 SUI (1_000_000_000 MIST) from gas coin
const [coin] = tx.splitCoins(tx.gas, [1_000_000_000]);

// Transfer the split coin
tx.transferObjects([coin], "0xRECIPIENT_ADDRESS");

// Execute
const result = await client.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
    options: {
        showEffects: true,
        showEvents: true,
    },
});
```

### Calling Move Functions

```typescript
const tx = new Transaction();

tx.moveCall({
    target: "0xPACKAGE_ID::module_name::function_name",
    arguments: [
        tx.object("0xOBJECT_ID"),           // object argument
        tx.pure.u64(100),                     // primitive argument
        tx.pure.string("hello"),              // string argument
        tx.pure.address("0xADDRESS"),         // address argument
        tx.pure.bool(true),                   // boolean argument
    ],
    typeArguments: ["0x2::sui::SUI"],         // generic type params
});

const result = await client.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
});
```

### Reading Objects

```typescript
// Get a single object
const object = await client.getObject({
    id: "0xOBJECT_ID",
    options: {
        showContent: true,
        showOwner: true,
        showType: true,
    },
});

// Get objects owned by an address
const ownedObjects = await client.getOwnedObjects({
    owner: "0xADDRESS",
    filter: {
        StructType: "0xPACKAGE::module::StructName",
    },
    options: { showContent: true },
});

// Get dynamic fields on an object
const dynamicFields = await client.getDynamicFields({
    parentId: "0xPARENT_OBJECT_ID",
});
```

### Querying Events

```typescript
const events = await client.queryEvents({
    query: {
        MoveEventType: "0xPACKAGE::module::EventStruct",
    },
    limit: 50,
    order: "descending",
});
```

### Multi-Command PTB

```typescript
const tx = new Transaction();

// Step 1: Split gas coin into two amounts
const [coin1, coin2] = tx.splitCoins(tx.gas, [1_000_000_000, 2_000_000_000]);

// Step 2: Use coin1 in a move call
tx.moveCall({
    target: "0xPACKAGE::module::deposit",
    arguments: [tx.object("0xVAULT_ID"), coin1],
});

// Step 3: Transfer coin2 to someone else
tx.transferObjects([coin2], "0xRECIPIENT");

// Step 4: Call another function
const [result] = tx.moveCall({
    target: "0xPACKAGE::module::claim_reward",
    arguments: [tx.object("0xPOOL_ID")],
});

// Step 5: Use the result from step 4
tx.transferObjects([result], "0xOWNER");

// All 5 steps execute atomically
const txResult = await client.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
});
```

### Gas Sponsorship

Sponsor transactions so users do not pay gas:

```typescript
// Sponsor builds the transaction
const tx = new Transaction();
tx.setSender(userAddress);
tx.setGasOwner(sponsorAddress);
tx.setGasBudget(10_000_000);

// User signs
const userBytes = await tx.build({ client });
const userSignature = await userKeypair.signTransaction(userBytes);

// Sponsor signs
const sponsorSignature = await sponsorKeypair.signTransaction(userBytes);

// Execute with both signatures
const result = await client.executeTransaction({
    transaction: userBytes,
    signature: [userSignature.signature, sponsorSignature.signature],
});
```

### Coin Operations

```typescript
// Get all coins of a type
const coins = await client.getCoins({
    owner: "0xADDRESS",
    coinType: "0x2::sui::SUI",
});

// Get total balance
const balance = await client.getBalance({
    owner: "0xADDRESS",
    coinType: "0x2::sui::SUI",
});
console.log("Balance:", balance.totalBalance); // string in MIST

// Merge coins in a PTB (consolidate dust)
const tx = new Transaction();
const allCoins = coins.data.map((c) => tx.object(c.coinObjectId));
if (allCoins.length > 1) {
    tx.mergeCoins(allCoins[0], allCoins.slice(1));
}
```

## Publishing Move Packages

### CLI

```bash
# Build the package
sui move build

# Run tests
sui move test

# Publish to testnet
sui client publish --gas-budget 100000000

# Publish with specific environment
sui client publish --gas-budget 100000000 --skip-dependency-verification
```

### Programmatic Publishing

```typescript
import { Transaction } from "@mysten/sui/transactions";
import { readFileSync } from "fs";
import { execSync } from "child_process";

// Build the package first
execSync("sui move build", { cwd: "./my_package" });

// Read compiled modules and dependencies
const { modules, dependencies } = JSON.parse(
    execSync("sui move build --dump-bytecode-as-base64", {
        cwd: "./my_package",
        encoding: "utf-8",
    })
);

const tx = new Transaction();

const [upgradeCap] = tx.publish({
    modules,
    dependencies,
});

// Transfer the UpgradeCap to the publisher
tx.transferObjects([upgradeCap], keypair.getPublicKey().toSuiAddress());

const result = await client.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
    options: { showObjectChanges: true },
});

// Extract the published package ID
const publishedPackage = result.objectChanges?.find(
    (change) => change.type === "published"
);
console.log("Package ID:", publishedPackage?.packageId);
```

## zkLogin

zkLogin allows users to authenticate with OAuth providers (Google, Facebook, Twitch, etc.) without managing private keys:

```typescript
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";
import { generateNonce, generateRandomness, jwtToAddress } from "@mysten/zklogin";

// Step 1: Generate ephemeral keypair
const ephemeralKeypair = new Ed25519Keypair();
const randomness = generateRandomness();
const maxEpoch = currentEpoch + 2; // valid for 2 epochs

// Step 2: Create nonce from ephemeral public key
const nonce = generateNonce(
    ephemeralKeypair.getPublicKey(),
    maxEpoch,
    randomness
);

// Step 3: Redirect user to OAuth provider with nonce
const googleLoginUrl = `https://accounts.google.com/o/oauth2/v2/auth?` +
    `client_id=${CLIENT_ID}&` +
    `response_type=id_token&` +
    `redirect_uri=${REDIRECT_URI}&` +
    `scope=openid&` +
    `nonce=${nonce}`;

// Step 4: After callback, derive Sui address from JWT
const jwt = "eyJ..."; // from OAuth callback
const salt = "user-specific-salt"; // must be consistent per user
const suiAddress = jwtToAddress(jwt, salt);

// Step 5: Get ZK proof from prover service
// Step 6: Sign transactions with ephemeral keypair + ZK proof
```

## Kiosk Framework

The Kiosk framework provides a standard for trading objects with enforced royalties:

```move
module my_package::my_policy {
    use sui::transfer_policy;

    /// Create a TransferPolicy for a type (one-time setup)
    public fun create_policy<T: key + store>(
        publisher: &Publisher,
        ctx: &mut TxContext,
    ) {
        let (policy, cap) = transfer_policy::new<T>(publisher, ctx);
        transfer::public_share_object(policy);
        transfer::public_transfer(cap, tx_context::sender(ctx));
    }
}
```

TypeScript Kiosk operations:

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();

// Create a kiosk
const [kiosk, kioskCap] = tx.moveCall({
    target: "0x2::kiosk::new",
    arguments: [],
});

tx.moveCall({
    target: "0x2::transfer::public_share_object",
    arguments: [kiosk],
    typeArguments: ["0x2::kiosk::Kiosk"],
});

tx.transferObjects([kioskCap], ownerAddress);
```

## Package Upgrades

Sui supports upgrading published packages using the UpgradeCap:

```typescript
const tx = new Transaction();

// Authorize the upgrade
const upgradeTicket = tx.moveCall({
    target: "0x2::package::authorize_upgrade",
    arguments: [
        tx.object(upgradeCapId),
        tx.pure.u8(0), // upgrade policy: 0 = compatible
        tx.pure(digestBytes),
    ],
});

// Perform the upgrade
const upgradeReceipt = tx.upgrade({
    modules,
    dependencies,
    package: currentPackageId,
    ticket: upgradeTicket,
});

// Commit the upgrade
tx.moveCall({
    target: "0x2::package::commit_upgrade",
    arguments: [tx.object(upgradeCapId), upgradeReceipt],
});

const result = await client.signAndExecuteTransaction({
    transaction: tx,
    signer: keypair,
});
```

Upgrade policies:
- `0` (compatible) -- can add new functions, new modules; cannot change existing signatures
- `128` (additive) -- can only add new modules
- `192` (dependency-only) -- can only change dependencies
- `255` (immutable) -- no further upgrades

To make a package permanently immutable, destroy the UpgradeCap:

```move
public entry fun make_immutable(cap: UpgradeCap) {
    package::make_immutable(cap);
}
```

## Display Standard

Set how objects appear in wallets and explorers:

```move
module my_package::my_nft {
    use sui::display;
    use sui::package;

    public struct MyNFT has key, store {
        id: UID,
        name: String,
        image_url: String,
    }

    fun init(otw: MY_NFT, ctx: &mut TxContext) {
        let publisher = package::claim(otw, ctx);

        let mut disp = display::new_with_fields<MyNFT>(
            &publisher,
            vector[
                string::utf8(b"name"),
                string::utf8(b"image_url"),
                string::utf8(b"project_url"),
            ],
            vector[
                string::utf8(b"{name}"),
                string::utf8(b"{image_url}"),
                string::utf8(b"https://myproject.com"),
            ],
            ctx,
        );
        display::update_version(&mut disp);

        transfer::public_transfer(publisher, tx_context::sender(ctx));
        transfer::public_transfer(disp, tx_context::sender(ctx));
    }
}
```

## SUI Denomination

| Unit | MIST Value | Readable |
|------|-----------|----------|
| 1 MIST | 1 | Smallest unit |
| 1 SUI | 1,000,000,000 | 10^9 MIST |

Always use MIST (integer) in code. SUI has 9 decimals.

## Common Patterns

### Capability Pattern (Access Control)

```move
module my_package::admin {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    /// Whoever owns this can call admin functions
    public struct AdminCap has key, store {
        id: UID,
    }

    fun init(ctx: &mut TxContext) {
        transfer::transfer(AdminCap {
            id: object::new(ctx),
        }, tx_context::sender(ctx));
    }

    /// Only callable if you own an AdminCap
    public entry fun admin_only_action(
        _cap: &AdminCap,
        // ... other params
    ) {
        // perform privileged action
    }
}
```

### Witness Pattern (Type Authorization)

```move
module my_package::witness_example {
    /// Witness type -- no fields, only `drop` ability
    public struct WITNESS has drop {}

    /// Function requiring proof of module authority
    public fun authorized_action<T: drop>(_witness: T) {
        // only callers that can construct T can call this
    }
}
```

### Hot Potato Pattern (Forced Completion)

```move
module my_package::hot_potato {
    /// No abilities -- MUST be consumed; cannot be stored, copied, or dropped
    public struct Receipt {
        amount: u64,
    }

    public fun borrow(amount: u64): (Coin<SUI>, Receipt) {
        // return coin and receipt
    }

    /// Caller MUST call this to consume the Receipt
    public fun repay(coin: Coin<SUI>, receipt: Receipt) {
        let Receipt { amount } = receipt;
        assert!(coin::value(&coin) >= amount, EInsufficientRepayment);
        // process repayment
    }
}
```

## CLI Reference

```bash
# Environment management
sui client envs                      # List environments
sui client switch --env testnet      # Switch network
sui client active-address            # Show current address
sui client active-env                # Show current environment

# Object queries
sui client objects                   # List owned objects
sui client object <ID>               # Get object details
sui client object <ID> --json        # JSON output

# Transaction execution
sui client call --package <PKG> --module <MOD> --function <FN> \
    --args <ARG1> <ARG2> --gas-budget 10000000

# Coin operations
sui client gas                       # List gas coins
sui client pay-sui --amounts 1000000000 --recipients <ADDR> \
    --input-coins <COIN_ID> --gas-budget 10000000

# Package management
sui move new <project_name>          # Create new Move project
sui move build                       # Compile
sui move test                        # Run unit tests
sui move test --filter <test_name>   # Run specific test
sui client publish --gas-budget 100000000

# Faucet
sui client faucet                    # Request testnet/devnet tokens
```

## Unit Testing in Move

```move
#[test_only]
module my_package::my_module_tests {
    use sui::test_scenario;
    use my_package::counter::{Self, Counter};

    #[test]
    fun test_counter_increment() {
        let admin = @0xAD;
        let mut scenario = test_scenario::begin(admin);

        // Transaction 1: publish module (init called automatically)
        test_scenario::next_tx(&mut scenario, admin);

        // Transaction 2: increment
        {
            let mut counter = test_scenario::take_shared<Counter>(&scenario);
            counter::increment(&mut counter);
            assert!(counter::value(&counter) == 1);
            test_scenario::return_shared(counter);
        };

        test_scenario::end(scenario);
    }
}
```

## Move.toml Configuration

```toml
[package]
name = "my_package"
edition = "2024.beta"

[dependencies]
Sui = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "framework/mainnet" }

[addresses]
my_package = "0x0"
```

Use `rev = "framework/testnet"` or `"framework/devnet"` for other networks.

## References

- Sui Documentation: https://docs.sui.io
- Move Reference: https://docs.sui.io/concepts/sui-move-concepts
- Sui TypeScript SDK: https://sdk.mystenlabs.com/typescript
- Sui CLI Reference: https://docs.sui.io/references/cli
- Move Book (Sui): https://move-book.com
- Sui GitHub: https://github.com/MystenLabs/sui
