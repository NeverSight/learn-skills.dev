---
name: sui-object-model
description: >
  Deep reference for the Sui object model: ownership types, object abilities,
  dynamic fields, collections, versioning, transfer patterns, and derived objects.
  Use this skill whenever the user asks about Sui objects, object ownership
  (address-owned, shared, immutable, wrapped), how to transfer or share or freeze
  objects, dynamic fields vs dynamic object fields, Table vs Bag vs VecMap,
  object versioning, wrapping and unwrapping, the Receiving type, custom transfer
  rules, hot potato pattern, capability pattern, object deletion, Object Display,
  or how to model data (inventories, registries, nested items) in Sui Move. Also
  use when the user needs to choose between ownership types or storage patterns
  for their use case.
---

# Sui Object Model

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io) and [move-book.com](https://move-book.com). When extending or updating this skill, only pull from these two sources. Do not use third-party blogs, tutorials, or unofficial documentation.

Objects are the fundamental unit of storage on Sui. Every resource, asset, and piece of data onchain is an object. Unlike account-based blockchains where state lives in shared mappings inside contracts, Sui gives each piece of state its own identity, version, and owner. Transactions consume objects as inputs and produce modified versions as outputs.

This skill routes to focused reference files. Load only the ones relevant to the current task.

---

## Reference files

### ownership — Ownership Types and Versioning
**Path:** `ownership.md`
**Load when:** asking about ownership types (address-owned, consensus-address-owned, shared, immutable, wrapped), choosing between shared and owned, parallel execution, consensus, Mysticeti, fastpath, object versioning, Lamport timestamps, or frontend access to shared objects.
**Covers:** all five ownership types with consensus implications, consensus-address-owned objects, shared object access mode optimization, frontend PTB access pattern, wrapped object behavior, Lamport timestamp versioning, fastpath vs consensus versioning.

### transfers — Transferring and Deleting Objects
**Path:** `transfers.md`
**Load when:** transferring objects, choosing between `transfer` and `public_transfer`, implementing custom transfer rules, using `Receiving<T>`, transfer-to-object, or deleting/destroying objects.
**Covers:** eight core transfer functions (module-restricted vs public, including party_transfer variants), custom transfer rules, transfer-to-object with `Receiving<T>`, `receive` vs `public_receive`, object deletion/unpacking pattern, dynamic field cleanup warning.

### dynamic-fields-and-collections — Dynamic Fields and Collections
**Path:** `dynamic-fields-and-collections.md`
**Load when:** using dynamic fields, choosing between `dynamic_field` and `dynamic_object_field`, working with collections (`Table`, `Bag`, `VecMap`, `LinkedTable`), or designing storage for large datasets.
**Covers:** dynamic field vs dynamic object field visibility, field naming, core API (add/borrow/remove/exists_), all collection types with decision table, cleanup requirements, system limits (256 KB object size, 2048 objects/txn).

### patterns — Common Patterns and Derived Objects
**Path:** `patterns.md`
**Load when:** implementing hot potato, capability, soulbound, inventory, or borrow patterns, or working with derived objects.
**Covers:** hot potato pattern (no-ability structs), capability pattern (AdminCap/TreasuryCap), borrow pattern with `sui::borrow` module, soulbound objects, inventory pattern (ObjectBag), derived objects with deterministic IDs, derived objects vs dynamic fields comparison.

### display — Object Display (V2)
**Path:** `display.md`
**Load when:** setting up how objects render in wallets, explorers, or apps, working with Display templates, configuring NFT metadata, or migrating from Display V1.
**Covers:** V2 `Display<T>` creation via `display_registry::new_with_publisher`, `DisplayCap<T>` for updates, `set`/`unset`/`clear`/`share` API, `{field_name}` template syntax with nested field access, common display properties, V1 to V2 migration.

---

## Routing guide

| Task | Load |
|------|------|
| What is an object / object structure | SKILL.md only |
| Abilities: key, store, copy, drop | SKILL.md only |
| Ownership types, shared vs owned vs consensus-address-owned | ownership |
| Parallel execution, consensus, fastpath | ownership |
| Object versioning, Lamport timestamps | ownership |
| Wrapped objects and accessibility | ownership |
| Frontend access to shared objects | ownership |
| Transferring objects, transfer vs public_transfer | transfers |
| Custom transfer rules | transfers + patterns |
| Transfer to object, Receiving | transfers |
| Deleting / destroying objects | transfers |
| Dynamic fields, dynamic object fields | dynamic-fields-and-collections |
| Collections: Table, Bag, VecMap, LinkedTable | dynamic-fields-and-collections |
| Scalability, large collection design | dynamic-fields-and-collections |
| Hot potato pattern | patterns |
| Capability pattern, AdminCap | patterns |
| Borrow pattern, cap inside object | patterns |
| Soulbound / non-transferable objects | transfers + patterns |
| Inventory for arbitrary objects | patterns + dynamic-fields-and-collections |
| Derived objects | patterns |
| Object Display, NFT rendering | display |
| Full project / code review | **all reference files** |

---

## Object structure

Every Sui object contains four components:

- **Globally unique ID:** A 32-byte identifier derived from the creation transaction digest plus a generation counter. The ID never changes across the object's lifetime.
- **Version number:** An 8-byte integer that increments with each modification. Uses Lamport timestamps: the new version for all objects a transaction touches is `1 + max(version of all input objects)`.
- **Owner field:** A 32-byte value designating access control (an address, another object's ID, or a sentinel for shared/immutable).
- **Transaction digest:** A 32-byte hash referencing the last transaction that modified the object.

Objects can be referenced three ways: by ID alone (query current state), by versioned ID (read historical state), or by full object reference containing ID + version + digest (transaction inputs, authenticated snapshot).

## Defining objects in Move

A Sui object is a Move struct with the `key` ability and an `id: UID` as the first field:

```move
public struct Sword has key, store {
    id: UID,
    damage: u64,
    element: String,
}
```

`object::new(ctx)` is the only way to create a `UID`. You cannot call `ctx.new()` directly.

## Move abilities and objects

| Ability | What it controls |
|---|---|
| `key` | The struct is a Sui object. Must have `id: UID` as first field. Required for all onchain objects. |
| `store` | The struct can be stored inside other objects, and transferred by any module using `public_transfer`. Without it, only the defining module can transfer the object. Adding `store` permanently removes the ability to enforce custom transfer rules. |
| `copy` | The struct can be duplicated. **Cannot be used on objects** — `UID` lacks `copy`, so any struct with `key` cannot have `copy`. Used only on non-object structs (configs, event data, read-only values). |
| `drop` | The struct can be silently discarded at end of scope. **Cannot be used on objects** — `UID` lacks `drop`, so any struct with `key` cannot have `drop`. Used only on non-object structs (ephemeral receipts, events). Objects must always be explicitly unpacked to destroy. |

### Object ability combinations

Because `UID` has neither `copy` nor `drop`, objects (structs with `key`) can only combine `key` and `store`:

- **`has key`:** Only the defining module can transfer, share, or freeze. Use for custom transfer rules.
- **`has key, store`:** Any module can transfer, share, freeze, or wrap. Use for freely composable assets. Once `store` is granted, you cannot re-add custom transfer restrictions.

### Non-object struct combinations (no `key`)

- **`has store`:** Can be stored as a field inside an object. Cannot exist independently.
- **`has copy, drop`:** A plain data struct for events, intermediate values, and configs.
- **`has copy, drop, store`:** Can be used as dynamic field names.
- **No abilities:** A hot potato. Must be consumed in the same transaction. See patterns reference file.

## Rules

- `object::new(ctx)` is the only way to create a UID. The `id: UID` field must be first.
- Once `store` is added to a type, custom transfer rules are permanently disabled.
- Once an object is shared, it cannot be converted back to address-owned.
- Always remove all dynamic fields before deleting a parent object — orphaned fields become permanently inaccessible.
- Accessing a nonexistent dynamic field (via `borrow`, `borrow_mut`, or `remove`) aborts the transaction. Use `exists_` to check first.
- Wrapping and unwrapping can happen within the same transaction — a PTB can wrap an object and later unwrap it atomically.
- Common capabilities: `AdminCap`, `TreasuryCap`, `UpgradeCap`. Always mention all three when discussing the capability pattern.
- Each `Table` entry is a separate storage operation — gas cost scales linearly with entries accessed per transaction.
- Prefer immutable references (`&`) on shared objects to maximize parallel execution.
- Do not use `VecMap` for collections larger than ~100 entries. Use `Table` instead.

## Common mistakes

- **Adding `store` when you need custom transfer rules.** Once granted, any module can call `public_transfer` and your enforcement logic is bypassed permanently.
- **Using `VecMap` for large collections.** It has O(n) lookup and is stored inline, hitting the 256 KB object size limit quickly.
- **Confusing `dynamic_field` with `dynamic_object_field`.** Use `dynamic_object_field` when the child must remain queryable by ID in explorers. Use `dynamic_field` for plain values.
- **Deleting an object without removing its dynamic fields first.** Those fields become permanently inaccessible.
- **Using the legacy `sui::display` module for new code.** Use `sui::display_registry` (Display V2). V1 was migrated to V2 via a system snapshot migration.
- **Forgetting to `display_registry::share(display)` after setting fields.** The display must be shared to be discoverable.
