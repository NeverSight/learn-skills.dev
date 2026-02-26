---
name: solidity
description: Solidity language and compiler — source layout, types, contracts, control flow, security, compiler, ABI, internals.
metadata:
  author: hairy
  version: "2026.2.9"
  source: Generated from https://github.com/ethereum/solidity (docs), scripts at https://github.com/antfu/skills
---

> Skill based on Solidity (ethereum/solidity) docs, generated at 2026-02-09.

Solidity is a statically typed, object-oriented language for EVM smart contracts. This skill covers source layout, types, contract structure, control flow, security patterns, compiler usage, and ABI/internals.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Source Layout | SPDX, pragma, import, comments | [core-layout](references/core-layout.md) |
| Contract Structure | State, functions, modifiers, events, errors, structs, enums | [core-structure](references/core-structure.md) |
| Types | Value/reference/mapping types, operators, conversions | [core-types](references/core-types.md) |
| Control Structures | if/loop, internal/external calls, revert, try/catch | [core-control](references/core-control.md) |
| Units and Globals | Ether/time units, block/msg/tx, ABI/hash helpers | [core-units-globals](references/core-units-globals.md) |

## Features

### Contracts

| Topic | Description | Reference |
|-------|-------------|-----------|
| Contracts | Creation, visibility, modifiers, functions, events, errors, inheritance, interfaces, libraries, using-for | [features-contracts](references/features-contracts.md) |
| Inline Assembly | Yul in Solidity, access to variables, safety | [features-assembly](references/features-assembly.md) |
| Yul | Intermediate language, EVM opcodes, objects | [features-yul](references/features-yul.md) |
| NatSpec | Tags, userdoc/devdoc output, @inheritdoc, @custom | [features-natspec](references/features-natspec.md) |
| Events | Indexed, anonymous, topics, selector, emit | [features-events](references/features-events.md) |
| Custom Errors | revert/require, selector, try/catch, ABI | [features-errors](references/features-errors.md) |
| Libraries | DELEGATECALL, internal vs external, linking | [features-libraries](references/features-libraries.md) |
| Inheritance | virtual/override, super, C3, base constructors | [features-inheritance](references/features-inheritance.md) |
| Interfaces | Restrictions, enum/struct, ABI alignment | [features-interfaces](references/features-interfaces.md) |
| Transient Storage | EIP-1153, transaction-scoped, reentrancy locks | [features-transient-storage](references/features-transient-storage.md) |
| Visibility and Getters | external/public/internal/private, getter generation | [features-visibility-getters](references/features-visibility-getters.md) |

### Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security | Reentrancy, gas, visibility, randomness, front-running | [best-practices-security](references/best-practices-security.md) |
| Common Patterns | Withdrawal, access control, checks-effects-interactions, proxies | [best-practices-patterns](references/best-practices-patterns.md) |
| Style and Layout | File/contract order, modifier order, naming | [best-practices-style](references/best-practices-style.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Compiler | solc CLI, Standard JSON, optimizer, libraries, path resolution | [advanced-compiler](references/advanced-compiler.md) |
| Internals | Storage/memory/calldata layout, optimizer, source mappings | [advanced-internals](references/advanced-internals.md) |
| ABI and Metadata | ABI spec, contract metadata, NatSpec | [advanced-abi-metadata](references/advanced-abi-metadata.md) |
| SMTChecker | Formal verification, engines, targets, options | [advanced-smtchecker](references/advanced-smtchecker.md) |
| Path Resolution | VFS, base/include paths, remapping, allowed paths | [advanced-path-resolution](references/advanced-path-resolution.md) |
| Compilation Output | Bytecode, --asm, optimized vs non-optimized | [advanced-compilation-output](references/advanced-compilation-output.md) |
