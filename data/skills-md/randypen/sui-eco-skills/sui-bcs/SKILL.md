---
name: sui-bcs
description: "Helps Claude Code understand Sui blockchain's BCS (Binary Canonical Serialization) encoding, providing usage guidelines and examples for primitive types, composite types, Sui-specific types, serialization patterns, and transformation support. Use when working with BCS serialization in Sui development or when the user mentions BCS, binary serialization, or Move data encoding."
---

# BCS (Binary Canonical Serialization) Skill

## Overview

BCS (Binary Canonical Serialization) is a binary serialization format designed for the Move programming language and widely used in the Sui blockchain ecosystem. The Sui TypeScript SDK provides a type-safe, efficient serialization system that supports primitive types, composite types, and Sui-specific types.

## Quick Start

### Installation and Import

```typescript
// Import BCS from @mysten/sui (includes Sui-specific types)
import { bcs } from '@mysten/sui/bcs';

// Or import base BCS from @mysten/bcs
import { bcs } from '@mysten/bcs';
```

### Basic Serialization Examples

```typescript
import { bcs } from '@mysten/sui/bcs';

// Serialize primitive types
const u32Bytes = bcs.u32().serialize(42).toBytes();
const stringBytes = bcs.string().serialize("hello").toBytes();

// Deserialize
const value = bcs.u32().parse(u32Bytes);
const text = bcs.string().parse(stringBytes);

// Use Sui-specific types
const addressBytes = bcs.Address.serialize('0x0000...0000');
const address = bcs.Address.parse(addressBytes);
```

## Core Components

### BCS Type System

The BCS type system is built on the `BcsType<T, I>` generic class:
- **Type safety**: Compile-time and runtime type checking
- **Transformation support**: Input/output type transformations
- **Lazy evaluation**: Supports recursive type definitions
- **Validation**: Runtime data validation

### BcsType Base Class

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/bcs/src/bcs-type.ts`

`BcsType` is the abstract base class for all BCS types, providing:
- Serialization/deserialization operations
- Type validation and transformation
- Base encoding support (Base58, Base64, Hex)
- Serialized size calculation

### BCS Factory Methods

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/bcs/src/bcs.ts`

Factory methods create various BCS types:
- **Primitive types**: u8, u16, u32, u64, u128, u256, bool, string
- **Composite types**: struct, enum, tuple, vector, map, option
- **Special types**: Fixed arrays, byte vectors, LEB128 encoding

### Reader/Writer Components

- **BcsReader**: Reads from binary data
- **BcsWriter**: Writes to binary data
- **SerializedBcs**: Wrapper for serialized data, provides encoding methods

## Primitive Types

For detailed information about primitive types including integers, booleans, and strings, see [Primitive Types](reference/primitive-types.md).

BCS supports the following primitive types:
- **Integer types**: u8, u16, u32, u64, u128, u256, uleb128 (variable-length)
- **Boolean type**: bool
- **String type**: UTF-8 encoded strings with LEB128 length prefix

### Basic Usage
```typescript
// Integer serialization
const u32Bytes = bcs.u32().serialize(42).toBytes();

// Boolean serialization
const boolBytes = bcs.bool().serialize(true).toBytes();

// String serialization
const stringBytes = bcs.string().serialize("Hello").toBytes();
```

## Composite Types

For comprehensive coverage of composite types including structs, enums, vectors, tuples, options, and maps, see [Composite Types](reference/composite-types.md).

BCS provides the following composite types:

### Struct
Organize related fields into named structures.

```typescript
const Person = bcs.struct('Person', {
  name: bcs.string(),
  age: bcs.u8(),
  balance: bcs.u64(),
});
```

### Enum
Define variant types with optional associated data.

```typescript
const Status = bcs.enum('Status', {
  Pending: null,
  Active: bcs.u64(),
  Inactive: bcs.string(),
});
```

### Vector
Collections of homogeneous elements.

```typescript
const NumberVector = bcs.vector(bcs.u32());
```

### Tuple
Fixed-size collections of heterogeneous elements.

```typescript
const Pair = bcs.tuple([bcs.string(), bcs.u64()]);
```

### Option
Optional values (Some/None pattern).

```typescript
const OptionalNumber = bcs.option(bcs.u64());
```

### Map
Key-value mappings.

```typescript
const StringToNumberMap = bcs.map(bcs.string(), bcs.u32());
```

## Sui-Specific Types

For detailed information about Sui blockchain-specific types including addresses, object references, transaction types, and Move types, see [Sui-Specific Types](reference/sui-specific-types.md).

Sui extends the base BCS with blockchain-specific types:

### Address Type
32-byte blockchain addresses with validation.

```typescript
bcs.Address.serialize('0x123...');
```

### Object Reference Types
References to Sui objects (owned, shared, receiving).

```typescript
bcs.SuiObjectRef.serialize(objectRef);
bcs.SharedObjectRef.serialize(sharedObjectRef);
```

### Transaction-Related Types
Transaction data, kind, and gas configuration.

```typescript
bcs.TransactionData.serialize(transactionData);
bcs.GasData.serialize(gasData);
```

### Key and Signature Types
Cryptographic types for transaction authorization.

```typescript
bcs.PublicKey.serialize(publicKeyBytes);
bcs.MultiSig.serialize(multiSigData);
```

### Move Types
Move programming language type system representations.

```typescript
bcs.TypeTag.serialize(typeTag);
bcs.StructTag.serialize(structTag);
```

## Serialization Patterns

For comprehensive examples of serialization patterns including basic operations, complex data structures, and recursive types, see [Serialization Patterns](reference/serialization-patterns.md).

### Basic Patterns
- Direct serialization to bytes
- Encoding to hex, base64, base58
- Parsing from encoded strings

```typescript
const serialized = bcs.u32().serialize(42);
const hex = serialized.toHex();
const value = bcs.u32().parseFromHex(hex);
```

### Complex Structures
Define and serialize hierarchical data structures.

```typescript
const Account = bcs.struct('Account', {
  address: bcs.string(),
  balance: bcs.u64(),
  transactions: bcs.vector(Transaction),
});
```

### Recursive Types
Handle self-referential data structures with lazy evaluation.

```typescript
const TreeNode = bcs.struct('TreeNode', {
  value: bcs.u64(),
  children: bcs.lazy(() => bcs.vector(TreeNode)),
});
```

## Transformation Support

For detailed examples of type transformations, validation patterns, and chained transformations, see [Transformation Support](reference/transformation-support.md).

### Type Transformations
Convert between different data representations during serialization/deserialization.

```typescript
const StringNumber = bcs.string().transform({
  input: (val: number) => val.toString(),
  output: (val: string) => parseInt(val),
});
```

### Validation Transformations
Add data validation logic to ensure data integrity.

```typescript
const PositiveNumber = bcs.u32().transform({
  input: (val: number) => {
    if (val <= 0) throw new Error('Value must be positive');
    return val;
  },
  output: (val: number) => val,
});
```

### Chained Transformations
Combine multiple transformations for complex data processing.

```typescript
const ProcessedString = bcs.string()
  .transform({ /* trim */ })
  .transform({ /* uppercase */ });
```

## Performance Considerations

For detailed performance optimization strategies including size prediction, zero-copy operations, and caching, see [Performance Considerations](reference/performance-considerations.md).

### Size Prediction
Estimate serialized size before actual serialization.

```typescript
const size = schema.serializedSize(data);
```

### Zero-Copy Operations
Minimize data copying for better performance.

```typescript
const ByteVectorType = bcs.byteVector();
const serialized = ByteVectorType.serialize(existingBuffer);
```

### Cache Optimization
Reuse type instances and buffers.

```typescript
const PersonType = bcs.struct('Person', { /* fields */ });
// Reuse across multiple serializations
```

## Integration with Transactions

For comprehensive examples of BCS integration with Sui transactions including argument serialization, transaction data handling, and object references, see [Integration with Transactions](reference/integration-transactions.md).

### Using BCS in Transactions
Serialize custom types for transaction arguments.

```typescript
const tx = new Transaction();
tx.moveCall({
  target: '0x2::example::function',
  arguments: [
    tx.pure(bcs.U64.serialize(100n)),
    tx.pure.address('0xaddress'),
  ],
});
```

### Transaction Data Serialization
Serialize complete transaction data for signing and submission.

```typescript
const serializedTxData = bcs.TransactionData.serialize(transactionData);
```

### Object Argument Types
Serialize different types of object references.

```typescript
bcs.ObjectArg.serialize(objectArg);
```

## Custom BCS Types

For detailed guidance on creating custom BCS types, extending existing types, and type registration, see [Custom BCS Types](reference/custom-types.md).

### Creating Custom Types
Implement custom serialization logic for specialized data formats.

```typescript
const CustomType = new BcsType<MyType, MyInput>({
  name: 'CustomType',
  read: (reader) => { /* deserialization */ },
  write: (value, writer) => { /* serialization */ },
});
```

### Extending Existing Types
Add custom behavior to built-in types using transformations.

```typescript
const enhancedU32 = bcs.u32().transform({
  input: (val) => val * 2,
  output: (val) => val / 2,
});
```

### Type Registration
Register application-specific types for reuse.

```typescript
bcs.registerStructType('User', {
  id: 'address',
  name: 'string',
  age: 'u8',
});
```

## Workflows

For complete workflow examples including Sui object serialization, transaction validation, and custom type registration, see [Workflows](reference/workflows.md).

### Common Workflows
- **Sui Object Serialization**: Serialize and deserialize blockchain objects
- **Transaction Data Validation**: Validate transaction formats using BCS
- **Custom Type Registration**: Register application-specific types
- **Batch Processing**: Process multiple operations efficiently
- **Error Handling**: Graceful error recovery patterns

### Example: Transaction Validation
```typescript
function validateTransactionData(data: any): boolean {
  try {
    bcs.TransactionData.serialize(data);
    return true;
  } catch {
    return false;
  }
}
```

### Example: Type Registration
```typescript
function registerAppTypes() {
  bcs.registerStructType('User', {
    id: 'address',
    name: 'string',
    age: 'u8',
  });
}
```

## Best Practices

For comprehensive best practices covering type safety, performance optimization, compatibility, and security, see [Best Practices](reference/best-practices.md).

### Key Recommendations
- **Type Safety**: Use TypeScript interfaces and runtime validation
- **Performance**: Reuse type instances and predict sizes
- **Compatibility**: Add version fields and maintain backward compatibility
- **Security**: Validate input and enforce size limits
- **Documentation**: Document schemas and provide usage examples

### Essential Practices
1. Always validate external input before serialization
2. Use TypeScript for compile-time type checking
3. Implement proper error handling and recovery
4. Test serialization/deserialization round trips
5. Document data formats and versioning strategies

## Reference Files

For detailed information on specific topics, refer to the following files in the `reference/` directory:

- **[Primitive Types](reference/primitive-types.md)**: Integer, boolean, and string types
- **[Composite Types](reference/composite-types.md)**: Structs, enums, vectors, tuples, options, and maps
- **[Sui-Specific Types](reference/sui-specific-types.md)**: Addresses, object references, transaction types, and Move types
- **[Serialization Patterns](reference/serialization-patterns.md)**: Basic and complex serialization patterns, recursive types
- **[Transformation Support](reference/transformation-support.md)**: Type transformations, validation, and chained transformations
- **[Performance Considerations](reference/performance-considerations.md)**: Size prediction, zero-copy operations, caching, and optimization
- **[Integration with Transactions](reference/integration-transactions.md)**: BCS usage in Sui transactions, argument serialization
- **[Custom BCS Types](reference/custom-types.md)**: Creating custom types, extending existing types, type registration
- **[Workflows](reference/workflows.md)**: Complete workflow examples and patterns
- **[Best Practices](reference/best-practices.md)**: Type safety, performance, compatibility, and security guidelines

## Related Skills

- [sui-transaction-building](./../sui-transaction-building/SKILL.md): Understand BCS usage in transaction building
- [sui-keypair-cryptography](./../sui-keypair-cryptography/SKILL.md): Understand BCS serialization of public keys and signatures

## References

- **Official documentation**: https://sdk.mystenlabs.com/bcs
- **Source code**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/bcs/src/` and `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/bcs/`
- **Test cases**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/bcs/tests/`
- **TypeScript type definitions**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/bcs/src/types.ts`

---

*This skill helps Claude Code understand Sui BCS serialization, providing practical code examples and usage guidelines. When users need to handle Sui blockchain data serialization, referencing this skill can provide accurate TypeScript code and best practices.*