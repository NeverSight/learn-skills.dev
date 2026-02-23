---
name: cadence
description: The complete reference for writing, auditing, and shipping Cadence smart contracts on Flow. Covers language syntax, resource-oriented programming, capabilities, access control, tokens, and production best practices — with code examples throughout.
---

# Cadence Smart Contract Development

Use this skill whenever you are **writing, reviewing, debugging, or auditing Cadence code** on the Flow blockchain.

## Documentation

| Resource | URL |
|---|---|
| Full docs | https://cadence-lang.org/docs |
| LLM-optimized reference | https://cadence-lang.org/llms.txt |
| Full LLM dump | https://cadence-lang.org/llms-full.txt |
| Security best practices | https://cadence-lang.org/docs/security-best-practices |
| Design patterns | https://cadence-lang.org/docs/design-patterns |
| Anti-patterns | https://cadence-lang.org/docs/anti-patterns |
| Testing framework | https://cadence-lang.org/docs/testing-framework |
| Flow NFT Standard | https://github.com/onflow/flow-nft |
| Flow FT Standard | https://github.com/onflow/flow-ft |

> **Tip:** Append `.mdx` to any `cadence-lang.org` doc URL to get raw markdown.

---

## 1. Language Fundamentals

### Types at a Glance

| Type | Example | Notes |
|------|---------|-------|
| `Int` | `42` | Arbitrary precision |
| `UInt64` | `100` | 64-bit unsigned |
| `UFix64` | `1.5` | Fixed-point, 8 decimals. Use for balances |
| `Bool` | `true` | |
| `String` | `"hello"` | UTF-8 |
| `Address` | `0x1234` | Account address |
| `[T]` | `[1, 2, 3]` | Array |
| `{K: V}` | `{"a": 1}` | Dictionary |
| `T?` | `nil` | Optional — nil-coalesce with `??` |
| `@T` | | **Resource** — unique, non-copyable |
| `&T` | | **Reference** — borrow without moving |

### Variables, Optionals, Functions

```cadence
let x: Int = 42                     // immutable
var name: String = "Cadence"        // mutable

// Optionals
let val: Int? = nil
let result = val ?? 0               // nil-coalescing
if let v = val { }                  // optional binding
let forced = val!                   // force-unwrap — panics, avoid

// Functions
access(all) fun greet(name: String): String {
    return "Hello, \(name)!"
}

// view = read-only (safe in scripts and pre/post)
access(all) view fun getBalance(): UFix64 { return self.balance }

// Pre/post conditions
access(all) fun withdraw(amount: UFix64): @Vault {
    pre  { amount > 0.0:              "Amount must be positive" }
    post { result.balance == amount:  "Withdrawal amount mismatch" }
}
```

### Struct vs Resource

```cadence
// Struct — copyable value type
struct Point {
    let x: Int; let y: Int
    init(x: Int, y: Int) { self.x = x; self.y = y }
}
let a = Point(x: 1, y: 2)
let b = a   // COPY — both exist independently

// Resource — unique, linear type (cannot copy)
resource Token {
    let id: UInt64
    init() { self.id = self.uuid }
}
let t1 <- create Token()
let t2 <- t1   // MOVE — t1 is no longer valid
destroy t2     // must explicitly destroy if not stored
```

**Resource rules:**
1. Resources exist in **exactly one place** at a time.
2. Every resource must be `save`d, moved, or `destroy`ed before the current scope ends.
3. Use `@` in type annotations: `@NFT`, `@{UInt64: NFT}`.
4. Use `<-` to move, `<-!` for force-assign into optional (panics on conflict).

---

## 2. Access Control & Entitlements

### Access Modifiers

| Modifier | Who can access |
|---|---|
| `access(all)` | Everyone (public read, callable by anyone) |
| `access(self)` | Only within the type itself |
| `access(contract)` | Same contract |
| `access(account)` | Same account |
| `access(E)` | Callers holding entitlement `E` |

### Entitlements Pattern

```cadence
access(all) entitlement Withdraw
access(all) entitlement Owner

access(all) resource Vault {
    access(self) var balance: UFix64

    // Anyone can read
    access(all) view fun getBalance(): UFix64 { return self.balance }

    // Anyone can deposit into you
    access(all) fun deposit(from: @Vault) {
        self.balance = self.balance + from.balance
        destroy from
    }

    // Only authorized callers can withdraw
    access(Withdraw) fun withdraw(amount: UFix64): @Vault {
        pre { self.balance >= amount: "Insufficient balance" }
        self.balance = self.balance - amount
        return <- create Vault(balance: amount)
    }
}

// Getting an entitled reference
let vaultRef = signer.storage
    .borrow<auth(Withdraw) &Vault>(from: /storage/vault)
    ?? panic("Could not borrow Vault")
```

### References

```cadence
let ref: &NFT = &myNFT                          // read-only reference
let authRef: auth(Withdraw) &Vault = &myVault   // entitled reference

// From storage
let r = signer.storage.borrow<auth(Withdraw) &Vault>(from: /storage/vault)
    ?? panic("No vault found")
```

---

## 3. Capabilities

Capabilities are the mechanism for sharing access to stored objects. **Nothing is public by default.**

```cadence
// 1. Save object to storage
signer.storage.save(<- create Vault(balance: 0.0), to: /storage/vault)

// 2. Issue a capability (creates a tracked controller)
let receiverCap = signer.capabilities.storage
    .issue<&{FungibleToken.Receiver}>(/storage/vault)

// 3. Publish so others can borrow it
signer.capabilities.publish(receiverCap, at: /public/receiver)

// 4. Borrow from another account
let receiver = getAccount(address).capabilities
    .borrow<&{FungibleToken.Receiver}>(/public/receiver)
    ?? panic("Account has no receiver capability")

// 5. Revoke when needed
let controller = signer.capabilities.storage
    .getController(byCapabilityID: capID) ?? panic("Controller not found")
controller.delete()

// Issue an entitled capability (grants Withdraw to holder)
let ownerCap = signer.capabilities.storage
    .issue<auth(Withdraw) &Vault>(/storage/vault)
```

### Public Capability Acquisition Returns Non-Optional

`capabilities.get<T>` returns an **invalid capability** (not `nil`) when no capability exists or when `T` mismatches. Check validity with `.check()`:

```cadence
let capability = account.capabilities.get<&MyNFT.Collection>(/public/NFTCollection)
if !capability.check() {
    // Handle invalid capability (ID == 0, borrow returns nil)
}
```

---

## 4. Transactions & Scripts

### Transaction Structure

```cadence
transaction(amount: UFix64, recipient: Address) {

    // Declare fields shared across phases
    let vaultRef: auth(FungibleToken.Withdraw) &FungibleToken.Vault

    // Access accounts — the ONLY phase with account access
    prepare(signer: auth(BorrowValue) &Account) {
        self.vaultRef = signer.storage
            .borrow<auth(FungibleToken.Withdraw) &FungibleToken.Vault>(
                from: /storage/vault
            ) ?? panic("No vault found")
    }

    pre  { amount > 0.0: "Amount must be positive" }

    execute {
        let tokens <- self.vaultRef.withdraw(amount: amount)
        let receiver = getAccount(recipient).capabilities
            .borrow<&{FungibleToken.Receiver}>(/public/receiver)
            ?? panic("Recipient has no receiver")
        receiver.deposit(from: <- tokens)
    }

    post { /* verify post-conditions */ }
}
```

**Phases:** `prepare` → `pre` → `execute` → `post`

### Common Signer Authorizations

```cadence
prepare(signer: auth(SaveValue) &Account)                          // save to storage
prepare(signer: auth(BorrowValue) &Account)                        // borrow from storage
prepare(signer: auth(LoadValue) &Account)                          // load (remove) from storage
prepare(signer: auth(IssueStorageCapabilityController) &Account)   // issue capabilities
prepare(signer: auth(PublishCapability) &Account)                  // publish capabilities
prepare(signer: auth(Contracts) &Account)                          // deploy/update contracts
prepare(signer: auth(Keys) &Account)                               // manage account keys
```

### Scripts (read-only, free, no transaction needed)

```cadence
access(all) fun main(address: Address): UFix64 {
    return getAccount(address).capabilities
        .borrow<&{FungibleToken.Balance}>(/public/balance)
        ?.balance ?? 0.0
}
```

---

## 5. Account Storage

```cadence
// Save — moves resource into storage
signer.storage.save(<- create NFT(), to: /storage/myNFT)

// Borrow — get a reference without removing
let ref = signer.storage.borrow<&NFT>(from: /storage/myNFT)

// Load — removes and returns (must handle the resource)
let nft <- signer.storage.load<@NFT>(from: /storage/myNFT)!

// Check existence and type
let t: Type? = signer.storage.type(at: /storage/myNFT)
if t != nil { /* already exists */ }

// Iterate all stored values
signer.storage.forEachStored(fun (path: StoragePath, type: Type): Bool {
    return true  // true = continue, false = stop
})
```

---

## 6. NFT Contract (Production Pattern)

```cadence
access(all) contract BasicNFT {

    access(all) var totalSupply: UInt64
    access(all) event Minted(id: UInt64)
    access(all) event Withdraw(id: UInt64, from: Address?)
    access(all) event Deposit(id: UInt64, to: Address?)
    access(all) entitlement Withdraw

    access(all) let CollectionStoragePath: StoragePath
    access(all) let CollectionPublicPath: PublicPath

    access(all) resource NFT {
        access(all) let id: UInt64
        access(all) let metadata: {String: String}
        init(metadata: {String: String}) {
            self.id = self.uuid
            BasicNFT.totalSupply = BasicNFT.totalSupply + 1
            emit Minted(id: self.id)
        }
    }

    access(all) resource Collection {
        access(self) var ownedNFTs: @{UInt64: NFT}

        access(all) fun deposit(token: @NFT) {
            emit Deposit(id: token.id, to: self.owner?.address)
            self.ownedNFTs[token.id] <-! token
        }

        access(Withdraw) fun withdraw(id: UInt64): @NFT {
            let token <- self.ownedNFTs.remove(key: id)
                ?? panic("NFT \(id) not found in collection")
            emit Withdraw(id: token.id, from: self.owner?.address)
            return <- token
        }

        access(all) fun getIDs(): [UInt64] { return self.ownedNFTs.keys }
        access(all) view fun borrowNFT(_ id: UInt64): &NFT? {
            return &self.ownedNFTs[id]
        }

        init() { self.ownedNFTs <- {} }
    }

    access(all) fun createEmptyCollection(): @Collection {
        return <- create Collection()
    }

    init() {
        self.totalSupply = 0
        self.CollectionStoragePath = /storage/basicNFTCollection
        self.CollectionPublicPath = /public/basicNFTCollection
    }
}
```

### NFT Setup Transaction

```cadence
transaction {
    prepare(signer: auth(SaveValue, IssueStorageCapabilityController, PublishCapability) &Account) {
        // Idempotent — skip if already set up
        if signer.storage.type(at: BasicNFT.CollectionStoragePath) != nil { return }

        signer.storage.save(<- BasicNFT.createEmptyCollection(), to: BasicNFT.CollectionStoragePath)
        let cap = signer.capabilities.storage
            .issue<&BasicNFT.Collection>(BasicNFT.CollectionStoragePath)
        signer.capabilities.publish(cap, at: BasicNFT.CollectionPublicPath)
    }
}
```

### Mint & Transfer

```cadence
// Mint (admin transaction)
transaction(recipient: Address, name: String) {
    execute {
        let nft <- create BasicNFT.NFT(metadata: {"name": name})
        getAccount(recipient).capabilities
            .borrow<&BasicNFT.Collection>(BasicNFT.CollectionPublicPath)
            ?.deposit(token: <- nft)
            ?? panic("Recipient has no collection")
    }
}

// Transfer (user transaction)
transaction(recipient: Address, nftID: UInt64) {
    let withdrawRef: auth(BasicNFT.Withdraw) &BasicNFT.Collection
    prepare(signer: auth(BorrowValue) &Account) {
        self.withdrawRef = signer.storage
            .borrow<auth(BasicNFT.Withdraw) &BasicNFT.Collection>(
                from: BasicNFT.CollectionStoragePath
            ) ?? panic("No collection")
    }
    execute {
        let nft <- self.withdrawRef.withdraw(id: nftID)
        getAccount(recipient).capabilities
            .borrow<&BasicNFT.Collection>(BasicNFT.CollectionPublicPath)
            ?.deposit(token: <- nft)
            ?? panic("Recipient has no collection")
    }
}
```

---

## 7. Fungible Token (Production Pattern)

```cadence
access(all) contract BasicToken {
    access(all) var totalSupply: UFix64
    access(all) entitlement Withdraw

    access(all) resource Vault {
        access(all) var balance: UFix64
        init(balance: UFix64) { self.balance = balance }

        access(all) fun deposit(from: @Vault) {
            self.balance = self.balance + from.balance
            destroy from
        }

        access(Withdraw) fun withdraw(amount: UFix64): @Vault {
            pre { self.balance >= amount: "Insufficient balance" }
            self.balance = self.balance - amount
            return <- create Vault(balance: amount)
        }
    }

    access(all) fun createEmptyVault(): @Vault {
        return <- create Vault(balance: 0.0)
    }

    init() { self.totalSupply = 0.0 }
}
```

### Cadence 1.0 Token Standard Changes

`FungibleToken.Vault` and `NonFungibleToken.NFT` / `NonFungibleToken.Collection` are now **interfaces**, not concrete types. Update all references:

```cadence
// Before (Cadence 0.x)
fun deposit(from: @FungibleToken.Vault)

// After (Cadence 1.0)
fun deposit(from: @{FungibleToken.Vault})
```

**Why vaults beat ledgers:**

| Ledger (Solidity) | Vault (Cadence) |
|---|---|
| Balances in a contract mapping | Each user holds their own Vault |
| Reentrancy attacks possible | Resources move atomically |
| Admin can modify any balance | Only the holder can access their Vault |

---

## 8. Security Rules (Non-Negotiable)

### S1 — Least Privilege
Start `access(self)`, widen only when justified. Never `access(all)` on state-modifying functions.

```cadence
// BAD — anyone drains your vault
access(all) fun withdraw(amount: UFix64): @Vault { ... }

// GOOD — requires entitlement
access(Withdraw) fun withdraw(amount: UFix64): @Vault { ... }
```

### S2 — Never Pass Fully Authorized Account Refs as Parameters

```cadence
// BAD — gives full storage access to callee
access(all) fun setup(admin: auth(Storage) &Account) { ... }

// GOOD — use a narrowly-scoped capability instead
access(all) fun setup(adminCap: Capability<&Admin>) { ... }
```

### S3 — Always Validate with Pre/Post Conditions

```cadence
access(Withdraw) fun withdraw(amount: UFix64): @Vault {
    pre  { amount > 0.0:                             "Amount must be positive" }
    pre  { self.balance >= amount:                   "Insufficient balance" }
    post { result.balance == amount:                 "Withdrawal amount mismatch" }
    post { self.balance == before(self.balance) - amount: "Balance accounting error" }
}
```

### S4 — Meaningful Panic Messages (Never Force-Unwrap Silently)

```cadence
// BAD — silent crash
let ref = cap.borrow()!

// GOOD — actionable message
let ref = cap.borrow()
    ?? panic("Could not borrow Vault — capability may be revoked or incorrect type")
```

### S5 — Private Data Is Not Secret
`access(self)` controls *programmatic access*, not blockchain visibility. All storage is publicly readable off-chain. **Never store secrets, private keys, or PII on-chain.**

### S6 — Never Hard-Code Addresses

```cadence
// BAD
import FungibleToken from 0xf233dcee88fe0abe

// GOOD (uses flow.json aliases, resolved at deployment)
import "FungibleToken"
```

### S7 — Check Before Setup (Idempotent Transactions)

```cadence
transaction {
    prepare(signer: auth(SaveValue) &Account) {
        if signer.storage.type(at: /storage/vault) != nil { return }
        signer.storage.save(<- MyToken.createEmptyVault(), to: /storage/vault)
    }
}
```

### S8 — Matching Access Modifiers Required for Interface Implementations

Implementation members must use **exactly** the same access modifier as the interface:

```cadence
access(all) resource interface I {
    access(account) fun foo()
}

// BAD — access(all) is more permissive than access(account)
access(all) resource R: I {
    access(all) fun foo() {}
}

// GOOD
access(all) resource R: I {
    access(account) fun foo() {}
}
```

---

## 9. Testing

Tests are Cadence files using the `Test` standard library, executed via Flow CLI.

```cadence
import Test

let blockchain = Test.newEmulatorBlockchain()
let admin = blockchain.createAccount()

access(all) fun setup() {
    let err = blockchain.deployContract(
        name: "MyNFT",
        code: Test.readFile("../contracts/MyNFT.cdc"),
        account: admin,
        arguments: []
    )
    Test.expect(err, Test.beNil())
}

access(all) fun testMint() {
    let tx = Test.Transaction(
        code: Test.readFile("../transactions/mint.cdc"),
        authorizers: [admin.address],
        signers: [admin],
        arguments: ["My NFT"]
    )
    Test.expect(blockchain.executeTransaction(tx), Test.beSucceeded())

    let events = Test.eventsOfType(Type<MyNFT.Minted>())
    Test.assertEqual(1, events.length)
}

access(all) fun testQuery() {
    let result = blockchain.executeScript(
        Test.readFile("../scripts/get_ids.cdc"),
        [admin.address]
    )
    let ids = result.returnValue! as! [UInt64]
    Test.assertEqual(1, ids.length)
}
```

**Common assertions:**
```cadence
Test.assertEqual(expected, actual)
Test.assert(condition, message: "reason")
Test.expect(result, Test.beSucceeded())
Test.expect(result, Test.beFailed())
Test.expect(err, Test.beNil())
```

**Run tests:**
```bash
flow test tests/my_test.cdc
flow test --cover tests/my_test.cdc
```

---

## 10. Naming Conventions

| Construct | Convention | Example |
|---|---|---|
| Contract, Resource, Struct, Interface, Event | `PascalCase` | `FlowToken`, `TokenVault` |
| Function, variable, parameter | `camelCase` | `getBalance()`, `totalSupply` |
| Storage/public paths | `let` fields on the contract | `let VaultStoragePath: StoragePath` |
| Entitlements | `PascalCase` | `entitlement Withdraw` |

**Never hardcode path strings in transactions** — always reference the contract's published path constants.

---

## 11. Anti-Patterns

### A1 — Never Pass Fully Authorized Account Refs as Parameters

A function accepting `auth(Storage) &Account` can access *all* storage — drain vaults, steal NFTs.

```cadence
// BAD — callee can withdraw FLOW or modify anything
access(all) fun transferNFT(id: UInt64, owner: auth(Storage) &Account) { ... }

// GOOD — authenticate via resources/capabilities
access(all) fun transferNFT(id: UInt64, collectionCap: Capability<auth(Withdraw) &Collection>) { ... }
```

### A2 — Public Functions Should Be Read-Only or Explicitly Entitled

Only `view` functions and functions everyone should call should be `access(all)`. State-modifying functions require entitlements.

### A3 — Capability-Typed Public Fields Are Security Holes

Capabilities are value types — a public field can be copied by anyone:

```cadence
// BAD — anyone copies the capability and calls its functions
access(all) var adminCap: Capability<&Admin>

// GOOD
access(self) var adminCap: Capability<&Admin>
access(Owner) fun getAdminCap(): Capability<&Admin> { return self.adminCap }
```

### A4 — Never Make Admin Creation Functions Public

```cadence
// BAD — anyone mints admin access
access(all) fun createAdmin(): @Admin { return <- create Admin() }

// GOOD — create once in init, existing admins create new ones
init() {
    self.account.storage.save(<- create Admin(), to: /storage/currencyAdmin)
}
```

### A5 — Never Emit Events or Modify Contract State in Struct Initializers

Structs are public and can be created by anyone. Side effects in `init()` can be exploited:

```cadence
// BAD — anyone spams events and overflows nextPlayID
access(all) struct Play {
    init() {
        TopShot.nextPlayID = TopShot.nextPlayID + 1  // BAD
        emit PlayCreated(id: self.playID)             // BAD
    }
}

// GOOD — state changes happen only inside admin resource
access(all) resource Admin {
    access(all) fun createPlay() {
        var newPlay = Play()
        TopShot.nextPlayID = TopShot.nextPlayID + UInt32(1)
        emit PlayCreated(id: newPlay.playID)
    }
}
```

### A6 — Complex/Capability Fields Must Be `access(self)`

`access(all)` on arrays, dictionaries, structs, resources, or capabilities allows direct mutation:

```cadence
// BAD
access(all) var adminCap: Capability<&Admin>

// GOOD
access(self) var adminCap: Capability<&Admin>
```

---

## 12. Capability Bootstrapping (Inbox API)

When account A needs to send a capability to account B, a single transaction cannot be signed by both accounts simultaneously. Use the **Inbox API**:

**Step 1 — Provider publishes the capability to recipient's inbox:**

```cadence
import "BasicNFT"

transaction(receiver: Address, name: String) {
    prepare(signer: auth(IssueStorageCapabilityController, PublishInboxCapability) &Account) {
        let capability = signer.capabilities.storage
            .issue<&BasicNFT.Minter>(BasicNFT.minterPath)

        let controller = signer.capabilities.storage
            .getController(byCapabilityID: capability.id)
            ?? panic("Controller not found")
        controller.setTag(name)

        signer.inbox.publish(capability, name: name, recipient: receiver)
    }
}
```

**Step 2 — Recipient claims the capability:**

```cadence
import "BasicNFT"

transaction(provider: Address, name: String) {
    prepare(signer: auth(ClaimInboxCapability, SaveValue) &Account) {
        let capability = signer.inbox.claim<&BasicNFT.Minter>(name, provider: provider)
            ?? panic("No capability named '\(name)' from \(provider)")
        signer.storage.save(capability, to: BasicNFT.minterPath)
    }
}
```

> The provider can call `signer.inbox.unpublish(name)` to retract before the recipient claims.

---

## 13. Performance: Prefer `borrow` Over `load`/`save`

`load()` moves the resource out of storage (expensive), `save()` moves it back (expensive again). `borrow()` returns an in-place reference — **always prefer it**.

```cadence
// BAD — unnecessary round-trip moves the entire resource
transaction {
    prepare(acct: auth(LoadValue, SaveValue) &Account) {
        let vault <- acct.storage.load<@ExampleToken.Vault>(from: /storage/exampleToken)!
        let burned <- vault.withdraw(amount: 10)
        destroy burned
        acct.storage.save(<- vault, to: /storage/exampleToken)
    }
}

// GOOD — borrow a reference, mutate in-place, no save needed
transaction {
    prepare(acct: auth(BorrowValue) &Account) {
        let vault = acct.storage.borrow<&ExampleToken.Vault>(from: /storage/exampleToken)!
        let burned <- vault.withdraw(amount: 10)
        destroy burned
    }
}
```

---

## 14. Measuring Time

Flow produces blocks approximately every **0.8 seconds**. Both block timestamp and block height are available on-chain.

```cadence
let block = getCurrentBlock()
block.timestamp   // Unix timestamp (UFix64, seconds)
block.height      // Block number (UInt64)

let pastBlock = getBlock(at: 70001)
pastBlock?.timestamp
pastBlock?.height
```

| Method | Use when |
|---|---|
| `getCurrentBlock().timestamp` | Acceptable for events lasting hours/days. Accurate to ~10 seconds. |
| `getCurrentBlock().height` | More manipulation-resistant. Requires off-chain rate estimation. |

**Rules:**
- Timestamps cannot go backwards and cannot be more than 10 seconds ahead of the previous block.
- **Never hardcode an assumed block rate** — it changes over time.
- Auctions and time-locks should have an **extension mechanism**.

---

## 15. Contract Upgrades

### Compatible Changes (Preferred)

Cadence supports in-place upgrades for additive changes: adding new fields (with defaults), new functions, new events. Use `flow contracts update`.

### Incompatible Changes

**Option A — New address (safest):**
1. Deploy new contract to a **new account**.
2. Increment path suffixes (`/public/MyVault002`).
3. Write upgrade transactions to migrate users' resources.

**Option B — Same address (risky, last resort):**
1. Delete all resources in the contract account (e.g., Admin resource).
2. Delete the contract from the account.
3. Deploy the new contract.

> ⚠️ If any user account holds `structs` or `resources` from the old contract version, those will **fail to load** and crash any transaction that touches them. Only do this before any users have received such objects.

**Always communicate upgrades in advance** — at least one week before deploying, share the proposed transaction and branch/commit hash with the community.

---

## 16. Cadence 1.0 Key Changes Summary

Cadence 1.0 (Crescendo upgrade, September 2024) introduced breaking changes. Key highlights:

| Change | Impact |
|---|---|
| **View functions** | `view` keyword enforces no mutations; required in pre/post conditions. |
| **Interface inheritance** | Interfaces can inherit from other interfaces of the same kind. |
| **Entitlements** | Replace restricted types; control access via `access(E)` and `auth(E) &T`. |
| **`pub`/`priv` removed** | Use `access(all)` and `access(self)` instead. |
| **Intersection types** | `{I1, I2}` replaces `AnyStruct{I1, I2}` restricted types. |
| **Account API** | `AuthAccount`/`PublicAccount` replaced by `&Account` with entitlements. |
| **Capability Controllers** | Replace linking-based API; use `capabilities.storage.issue`, `publish`, `getController`. |
| **Resource reference invalidation** | References invalidated when referenced resource is moved. |
| **Force destruction** | `destroy` methods removed; resources destroyed implicitly; use `ResourceDestroyed` event. |
| **Token standards** | `FungibleToken.Vault`, `NonFungibleToken.NFT`, `NonFungibleToken.Collection` are now interfaces (`@{Type}`). |

### Emulator Import Addresses (Cadence 1.0)

| Contract | Emulator | Testing Framework |
|---|---|---|
| `FungibleToken` | `0xee82856bf20e2aa6` | `0x0000000000000002` |
| `NonFungibleToken` | `0xf8d6e0586b0a20c7` | `0x0000000000000001` |
| `MetadataViews` | `0xf8d6e0586b0a20c7` | `0x0000000000000001` |
| `ViewResolver` | `0xf8d6e0586b0a20c7` | `0x0000000000000001` |
| `Burner` | `0xf8d6e0586b0a20c7` | `0x0000000000000001` |
| `FlowToken` | `0x0ae53cb6e3f42a79` | `0x0000000000000003` |