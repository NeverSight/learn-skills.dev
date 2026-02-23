---
name: sui-client
description: Comprehensive SuiClient skill for interacting with the Sui blockchain using @mysten/sui SDK. Use this skill when you need to connect to Sui blockchain, read data, execute transactions, manage staking positions, or query network information.
---

# SuiClient Skill

A comprehensive Claude Code skill for interacting with the Sui blockchain using the official `@mysten/sui` SDK.

## Instructions

Use this skill when you need to interact with the Sui blockchain. Includes:

1. **Network Connection**: Connect to mainnet, testnet, devnet, or localnet
2. **Data Reading**: Get tokens, objects, transactions, and balances
3. **Transaction Execution**: Build, sign, and execute transactions
4. **Network Information**: Get system state, gas prices, and protocol configuration
5. **Move Package Interactions**: Query normalized Move data
6. **Event Handling**: Query and subscribe to blockchain events
7. **Staking Operations**: Manage staking positions
8. **Error Handling**: Implement comprehensive error handling patterns

## Quick Start

```typescript
import { SuiClient } from '@mysten/sui/client';

// Connect to mainnet
const client = new SuiClient({
  url: 'https://sui-mainnet.nodeinfra.com'
});

// Get account balance
const balance = await client.getBalance({
  owner: '0x123...',
  coinType: '0x2::sui::SUI'
});
```

## Installation

```bash
# Install the skill
claude skills install sui-client

# Install dependencies
bun add @mysten/sui
```

## Features

- **Client Management**: Connect to mainnet, testnet, devnet, and localnet
- **Data Reading**: Get tokens, objects, transactions, and balances
- **Transaction Execution**: Build, sign, and execute transactions
- **Network Information**: Get system state, gas prices, and protocol configuration
- **Move Package Interactions**: Query normalized Move data
- **Event Handling**: Query and subscribe to blockchain events
- **Staking Operations**: Manage staking positions
- **Error Handling**: Comprehensive error handling patterns

## Examples

Check the `examples/` directory for complete usage examples:

- `basic-usage.ts` - Basic client setup and data reading
- `transactions.ts` - Transaction building and execution
- `advanced.ts` - Advanced patterns and error handling

## API Reference

This skill provides comprehensive coverage of the SuiClient API including:

- **Reading Data**: `getObject()`, `getCoins()`, `getTransactionBlock()`
- **Writing Data**: `signAndExecuteTransaction()`, `executeTransactionBlock()`
- **Network Information**: `getLatestSuiSystemState()`, `getReferenceGasPrice()`
- **Events**: `queryEvents()`, `subscribeEvent()`
- **Staking**: `getStakes()`, `getStakesByIds()`

## Detailed Documentation

- [Source Code](src/index.ts) - Complete SuiClient API implementation
- [Type Definitions](types/index.d.ts) - TypeScript type definitions
- [Code Templates](templates/) - Common code templates
- [Example Code](examples/) - Complete usage examples

## Dependencies

- `@mysten/sui`: ^1.45.0 (managed via package.json)

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## License

MIT