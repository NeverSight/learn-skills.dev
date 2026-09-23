---
name: sui-for-ethereum
description: >
  Migrating from Ethereum/EVM/Solidity to Sui Move. Use when the user is an
  Ethereum developer learning Sui, comparing Solidity patterns to Move equivalents,
  asking about differences between EVM and MoveVM, mapping Ethereum token standards
  to Sui standards, or translating access control, state storage, contract upgrade,
  or composability patterns from Ethereum to Sui.
---

# Sui for Ethereum Developers

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io/getting-started/sui-for-ethereum](https://docs.sui.io/getting-started/sui-for-ethereum). When extending or updating this skill, only pull from this source. Do not use third-party blogs, tutorials, or unofficial documentation.

This skill helps Ethereum/EVM/Solidity developers understand how Sui Move differs from the patterns they already know. It covers conceptual model shifts, pattern mappings, and concrete comparisons between the two ecosystems.

---

## Reference files

### patterns — Pattern Mappings and Comparisons
**Path:** `patterns.md`
**Load when:** the user asks about specific Ethereum-to-Sui pattern mappings, token standard equivalents, technical comparisons (signatures, consensus, VM), access control differences, data storage differences, contract upgrade approaches, or composability differences.
**Covers:** account vs object model, data storage, inheritance and polymorphism, asset accessibility, access control patterns (with Move capability example), contract upgrades, development environment, state mutation, object model fundamentals, object ownership types, mutating objects, PTBs, standards mapping (ERC-20/ERC-721/ERC-1155 to Sui equivalents), and full technical comparison table.

---

## Routing guide

| Task | Load |
|------|------|
| High-level "what is different about Sui vs Ethereum" | SKILL.md only |
| Specific pattern mapping (access control, storage, tokens) | patterns |
| Token standard equivalents (ERC-20, ERC-721, ERC-1155) | patterns |
| Technical comparisons (signatures, consensus, VM, execution) | patterns |
| How PTBs replace multi-transaction workflows | patterns |
| Contract upgrade differences | patterns |
| Capability-based vs role-based access control | patterns |

---

## Core conceptual shifts

### Programming language
Sui uses Move; the EVM uses Solidity. Move enforces resource safety at both compile time and through bytecode verification. Objects cannot be duplicated or silently dropped. Solidity relies on the EVM for runtime safety.

### Account-centric vs object-centric
Ethereum uses an account-centric model. Solidity implements custom ownership logic within contracts using mappings. Only Ethereum's native currency (ETH) is a first-class citizen with global APIs. Sui uses an object-centric model. Object ownership is inherent to the protocol. Objects are first-class citizens encompassing everything owned on Sui. Any currency on Sui has the same properties as SUI.

### Data storage
In Solidity, data is stored in the smart contract. In Move, data is stored in Move objects. Logic is defined in the contract (package), but the data lives in objects separate from the contract itself. Object behavior (creation, modification, ownership, and deletion) is defined by a package.

### Object model fundamentals
Objects store data in Move and everything in Move is an object. This includes smart contracts (Move packages), onchain addresses, coins, and NFTs.

### Object ownership
- **Address-owned objects:** Single address ownership. Transferable without smart contract interaction.
- **Shared objects:** Publicly accessible objects anyone can use.

### Programmable transaction blocks (PTBs)
PTBs give builders the ability to chain contract calls together with atomicity guarantees during runtime. A Sui PTB can have up to 1,024 different contract calls. This replaces the pattern in Ethereum where each call is its own transaction and is not atomic.

---

## Rules

- Always frame migration advice around the shift from account-centric to object-centric thinking.
- When comparing access control, emphasize that Sui uses capability-based access control through owned objects, not identity/role-based access control through Ownable or AccessControl contracts.
- When discussing token standards, map ERC-20 and ERC-721 to the Sui Currency Standard and Closed-Loop Token. Do not invent Sui equivalents for standards not covered in the source material.
- When discussing contract upgrades, explain that Sui requires layout compatibility, not proxy contracts.
- When discussing composability, emphasize PTBs as the mechanism for atomic multi-call transactions.
- Do not describe Sui as "just another EVM chain." The programming model is fundamentally different.
- Do not invent information beyond what is provided in the source material from docs.sui.io/getting-started/sui-for-ethereum.

## Common mistakes

- **Assuming Solidity inheritance patterns work in Move.** Move has no interfaces, no polymorphism, and no dynamic dispatch. It uses composition through module imports and generics (`Type<T>`) instead.
- **Assuming only role-based access control works.** Sui can implement role-based access control, but the idiomatic pattern is capability-based access through owned objects (e.g., `AdminCap`). Capabilities cheaply objectify ownership transfer rules.
- **Thinking data is stored in the contract like Solidity.** In Sui, logic lives in the contract (package) but data lives in Move objects.
- **Expecting proxy-based contract upgrades.** Sui can have proxy-like patterns, but they must operate on the same object types across upgrades. Layout compatibility is required — new contracts must be layout-compatible with the old one. Upgrades are controlled through `UpgradeCap`.
- **Treating each Move function call as a separate transaction.** Use PTBs to chain up to 1,024 contract calls into a single atomic transaction.
- **Assuming tokens are bound to a smart contract like in Solidity.** On Sui, anyone can access shared objects, and owned objects are directly accessible by their owner without going through a contract.
