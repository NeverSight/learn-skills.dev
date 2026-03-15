---
name: algorand-ts-migration
description: >
  Migrate smart contracts to Algorand TypeScript 1.0 from either TEALScript or Algorand TypeScript Beta.
  Use when converting TEALScript contracts to Algorand TypeScript, upgrading Algorand TypeScript beta code to 1.0,
  user mentions migrating or upgrading to Algorand TypeScript / puya-ts / algo-ts 1.0, or user has TealScript code
  and wants to modernize it.
---

# Algorand TypeScript Migration

Migrate smart contracts to Algorand TypeScript 1.0 from TEALScript or Algorand TypeScript Beta.

## Migration Workflow

### 1. Identify Source Language

Determine whether the code is **TEALScript** or **Algorand TypeScript Beta**:

| Indicator | TEALScript | Algorand TypeScript Beta |
|-----------|------------|--------------------------|
| Import source | `@algorandfoundation/tealscript` | `@algorandfoundation/algorand-typescript` |
| Global types | Uses `assert`, `uint64` without imports | Requires explicit imports |
| Event logging | `new EventLogger<...>()` | N/A |
| Inner transactions | `sendAssetConfig({...})` | `itxn.assetConfig({...})` |
| Logic sig method | `logic()` | `program()` |
| Type syntax | `uint256`, `uint8` literals | `arc4.UintN<256>`, `arc4.UintN8` |

### 2. Load Migration Guide

Based on the source language, read the appropriate reference:

- **From TEALScript**: Read [references/from-tealscript.md](references/from-tealscript.md)
- **From Algorand TypeScript Beta**: Read [references/from-beta.md](references/from-beta.md)

### 3. Execute Migration

Follow the checklist in the loaded reference file. Apply transformations systematically:

1. Start with imports and type renames (mechanical changes)
2. Update syntax patterns (inner transactions, method calls)
3. Add explicit type annotations where required
4. Handle semantic changes (mutability, resource encoding)
5. Rename test files if applicable

### 4. Verify Migration

After migration:
- Ensure all imports resolve from `@algorandfoundation/algorand-typescript`
- Verify no TypeScript errors remain
- Run the Algorand TypeScript compiler to validate

## Quick Reference

### Common Import Pattern (1.0)

```ts
import {
  Contract,
  GlobalState,
  LocalState,
  Box,
  BoxMap,
  arc4,
  uint64,
  bytes,
  Bytes,
  Uint64,
  assert,
  err,
  emit,
  clone,
  itxn,
  gtxn,
  Txn,
  Global,
  op,
} from '@algorandfoundation/algorand-typescript';
```

### Key Type Changes

| Old | New (1.0) |
|-----|-----------|
| `uint8`, `uint16`, `uint256` | `arc4.Uint<8>`, `arc4.Uint<16>`, `arc4.Uint<256>` |
| `arc4.UintN64`, `arc4.UintN<N>` | `arc4.Uint64`, `arc4.Uint<N>` |
| `arc4.UFixedNxM<N,M>` | `arc4.UFixed<N,M>` |
| `MutableArray` | `ReferenceArray` |
| `BoxRef` | `Box<bytes>` |
| `Address` (TEALScript) | `Account` |
| `AppID` (TEALScript) | `Application` |
| `AssetID` (TEALScript) | `Asset` |

### Key Function Changes

| Old | New (1.0) |
|-----|-----------|
| `x.copy()` | `clone(x)` |
| `arc4EncodedLength<T>()` | `sizeOf<T>()` |
| `arc4.interpretAsArc4<T>(b)` | `arc4.convertBytes<T>(b, { strategy: 'validate' })` |
| `x.native` | `x.asUint64()` or `x.asBigUint()` |
| `sendMethodCall<T>({...})` | `arc4.abiCall({ method: T, ... })` |

## Resources

### references/

- **[from-beta.md](references/from-beta.md)**: Complete migration guide from Algorand TypeScript Beta to 1.0. Includes checklist of 13 breaking changes with before/after examples.

- **[from-tealscript.md](references/from-tealscript.md)**: Complete migration guide from TEALScript to Algorand TypeScript 1.0. Includes type migration table and 13 migration patterns with examples.
