---
name: sui-transaction-building
description: "Helps Claude Code understand Sui blockchain transaction building, providing guidelines and examples for Transaction class, commands, input types, gas configuration, and serialization. Use when building blockchain transactions on Sui or when the user mentions transaction building, Transaction class, or Move calls."
---

# Sui Transaction Building Skill

## Overview

Transaction building is a core functionality of Sui blockchain development. The Sui TypeScript SDK provides the `Transaction` class, allowing developers to create, serialize, sign, and execute blockchain transactions using a fluent builder pattern. This skill helps Claude Code understand how to assist users in building various types of transactions on Sui.

## Quick Start

### Installation and Import

```typescript
// Import Transaction class
import { Transaction } from '@mysten/sui/transactions';

// Create new transaction
const tx = new Transaction();
```

### Basic Example: Sending SUI

```typescript
import { Transaction } from '@mysten/sui/transactions';

const tx = new Transaction();

// Split 100 units of SUI from gas coin
const [coin] = tx.splitCoins(tx.gas, [100]);

// Transfer the split coin to specified address
tx.transferObjects([coin], '0xSomeSuiAddress');

// Execute transaction using signAndExecuteTransaction
const result = await client.signAndExecuteTransaction({
  signer: keypair,
  transaction: tx
});
```

## Core Components

### Transaction Class

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/transactions/Transaction.ts`

The Transaction class is the core of transaction building, providing the following key features:
- **Builder Pattern**: Fluent interface supporting method chaining
- **Command Support**: Supports all Sui transaction commands (Move calls, transfers, merges, etc.)
- **Plugin System**: Supports transaction parsing plugins
- **Serialization Capability**: Built-in BCS serialization support
- **Async Support**: Supports automatic resolution of async transaction thunks

### TransactionDataBuilder Class

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/transactions/TransactionData.ts`

Handles transaction data structure and serialization:
- Transaction data validation and serialization
- BCS serialization for blockchain compatibility
- Gas configuration and budget management
- Input and command management

### Commands Module

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/transactions/Commands.ts`

Defines all available transaction operations:
- **MoveCall**: Execute Move smart contract functions
- **TransferObjects**: Transfer objects between addresses
- **SplitCoins**: Split a coin into multiple amounts
- **MergeCoins**: Merge multiple coins
- **Publish**: Deploy new Move modules
- **Upgrade**: Upgrade existing Move modules
- **MakeMoveVec**: Create Move vectors

## Detailed Documentation

This skill follows a progressive disclosure pattern. The main file provides an overview and quick start, while detailed information is available in the reference directory.

### Transaction Commands

For detailed information about transaction commands including SplitCoins, MergeCoins, TransferObjects, MoveCall, MakeMoveVec, and Publish, see [Transaction Commands](reference/transaction-commands.md).

### Input Types

Learn about different input types including pure values, object references, and transaction results in [Input Types](reference/input-types.md).

### Gas Configuration

Understand gas coin usage, price setting, budget configuration, and optimization in [Gas Configuration](reference/gas-configuration.md).

### Transaction Serialization

Details about building transaction bytes, deserialization, and offline building in [Transaction Serialization](reference/transaction-serialization.md).

### Advanced Features

Explore transaction intents, sponsored transactions, plugin system, and async support in [Advanced Features](reference/advanced-features.md).

### Usage Patterns

Common patterns for transaction building, signing, execution, testing, and error handling in [Usage Patterns](reference/usage-patterns.md).

### Integration Points

Integration with SuiClient, BCS, keypairs, wallets, and external systems in [Integration Points](reference/integration-points.md).

### Workflows

Complete end-to-end workflows for common scenarios including SUI transfers, NFT minting, and offline building in [Workflows](reference/workflows.md).

### Best Practices

Performance optimization, error handling, security considerations, and code quality guidelines in [Best Practices](reference/best-practices.md).


## Related Skills

- [sui-bcs](./../sui-bcs/SKILL.md): Understand BCS serialization usage in transactions
- [sui-transaction-executors](./../sui-transaction-executors/SKILL.md): Understand advanced usage of transaction executors
- [sui-keypair-cryptography](./../sui-keypair-cryptography/SKILL.md): Understand transaction signing and key management
- [sui-client](./../sui-client/SKILL.md): Understand complete SuiClient API

## References

- **Official Documentation**: https://sdk.mystenlabs.com/typescript/transaction-building
- **Source Code**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/transactions/`
- **Test Cases**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/transactions/__tests__/`
- **TypeScript Type Definitions**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/transactions/types.ts`

---

*This skill helps Claude Code understand Sui transaction building, providing practical code examples and usage guidelines. When users need to build Sui blockchain transactions, referencing this skill can provide accurate TypeScript code and best practices.*