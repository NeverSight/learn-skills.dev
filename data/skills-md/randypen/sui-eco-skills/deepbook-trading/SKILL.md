---
name: deepbook-trading
description: Helps Claude Code understand DeepBook V3 SDK usage for order book trading, flash loans, fund management, and market data queries on Sui blockchain. Use when operating DeepBook DEX, executing trading strategies, or querying market data.
---

# DeepBook Trading Skill

## Overview
DeepBook is a decentralized order book exchange (CLOB DEX) on the Sui blockchain. This skill helps Claude Code use the DeepBook V3 SDK to execute trading operations and query market data.

## Quick Start

### 1. Install Dependencies
```bash
pnpm add @mysten/deepbook-v3 @mysten/sui
```

### 2. Initialize Client
See [Basic Setup Example](examples/01-basic-setup.ts)

### 3. Execute Operations
Use the simplified wrapper interfaces provided by this skill.

## Core Functionality

### Trading Execution
- **Limit Orders**: Place limit buy/sell orders with price and quantity
- **Market Orders**: Execute orders at current market price
- **Order Cancellation**: Cancel existing orders
- **Asset Swaps**: Swap between Base and Quote assets
- **Flash Loans**: Borrow assets for arbitrage opportunities

### Market Data Queries
- **Order Book**: Level 2 order book data with depth control
- **Account Information**: User positions, open orders, locked balances
- **Pool Status**: Vault balances, trading parameters, fee information
- **Price Feeds**: Real-time price data from Pyth oracle

### Fund Management
- **BalanceManager**: Deposit/withdraw funds from exchange
- **Balance Checks**: Query available balances across coins
- **Referral System**: Manage referral codes and fee sharing

### Advanced Features
- **Margin Trading**: Leveraged trading with risk management
- **Governance**: Participate in pool governance and voting
- **Admin Functions**: Pool creation and parameter adjustment (admin only)

## Detailed Documentation

### Trading Functions
See [Transaction Wrapper Reference](src/transaction-wrapper.ts) for complete trading API.

### Query Functions
See [Query Wrapper Reference](src/query-wrapper.ts) for market data queries.

### Flash Loan Functions
See [Flash Loan Wrapper Reference](src/flash-loan-wrapper.ts) for arbitrage strategies.

### Fund Management Functions
See [Balance Manager Wrapper Reference](src/balance-manager-wrapper.ts) for fund operations.

## Code Templates

### Market Maker Template
[market-maker.ts](templates/market-maker.ts) - Automated market making with spread control

### Arbitrage Bot Template
[arbitrage-bot.ts](templates/arbitrage-bot.ts) - Flash loan arbitrage between pools

### Data Monitor Template
[data-monitor.ts](templates/data-monitor.ts) - Real-time market data monitoring

### Liquidation Bot Template
[liquidation-bot.ts](templates/liquidation-bot.ts) - Automated liquidation detection

### Portfolio Manager Template
[portfolio-manager.ts](templates/portfolio-manager.ts) - Multi-pool portfolio management

## Common Task Workflows

### Place Limit Order Workflow
1. Initialize trading client with SuiClient and address
2. Query current market price and order book
3. Determine order price and quantity
4. Execute `placeLimitOrder` with appropriate parameters
5. Verify order status using `getOrder` or `accountOpenOrders`

### Execute Flash Loan Arbitrage Workflow
1. Identify arbitrage opportunity (price discrepancy between pools)
2. Borrow asset using `borrowAsset` from flash loan pool
3. Execute profitable trade in target pool
4. Return borrowed asset using `returnAsset`
5. Calculate net profit after fees

### Fund Management Workflow
1. Create BalanceManager for user using `createBalanceManager`
2. Deposit funds into BalanceManager using `deposit`
3. Execute trades using the BalanceManager key
4. Withdraw profits using `withdraw`
5. Monitor balances using `checkBalance`

## Best Practices

### Transaction Safety
- Always check transaction fees and gas budget
- Use try-catch blocks for transaction failure handling
- Verify sufficient balances before executing trades
- Set appropriate slippage tolerance for swaps

### Data Accuracy
- Regularly update price info objects (max age: 5 minutes)
- Validate pool keys and coin types before queries
- Handle network latency in real-time operations
- Cache frequently accessed data where appropriate

### Risk Management
- Monitor account risk ratios for margin trading
- Implement stop-loss mechanisms for automated strategies
- Diversify across multiple pools and assets
- Regular portfolio rebalancing

## Error Handling

### Common Errors and Solutions

#### Transaction Failed: Insufficient Balance
**Solution**: Check account balance using `checkBalance` before trading

#### Query Failed: Invalid Pool Key
**Solution**: Verify pool key exists in config using available pools list

#### Price Info Object Expired
**Solution**: Call `getPriceInfoObject` to refresh price data

#### Network Connection Issues
**Solution**: Implement retry logic with exponential backoff

#### Gas Estimation Errors
**Solution**: Increase gas budget or simplify transaction complexity

## Configuration Reference

### Environment Setup
```typescript
// Mainnet configuration
const mainnetConfig = {
  suiClient: new SuiClient({ url: getFullnodeUrl('mainnet') }),
  address: '0xYourAddress',
  environment: 'mainnet' as const,
};

// Testnet configuration
const testnetConfig = {
  suiClient: new SuiClient({ url: getFullnodeUrl('testnet') }),
  address: '0xYourTestAddress',
  environment: 'testnet' as const,
};
```

### Default Pools and Coins
The skill includes predefined configurations for:
- **Mainnet**: SUI_USDC, SUI_DBUSDC, DEEP_USDC pools
- **Testnet**: Test pools with test assets
- **Devnet**: Development pools for testing

## Performance Optimization

### Query Optimization
- Batch multiple queries where possible
- Use pagination for large datasets
- Implement client-side caching
- Subscribe to real-time updates for active monitoring

### Transaction Optimization
- Combine multiple operations in single transaction
- Use batch processing for high-frequency trading
- Optimize gas usage through transaction batching
- Implement circuit breakers for failed transactions

## Security Considerations

### Private Key Management
- Never hardcode private keys in source code
- Use environment variables or secure vaults
- Implement key rotation policies
- Use hardware wallets for production funds

### Smart Contract Interactions
- Verify contract addresses before interactions
- Audit transaction payloads for correctness
- Implement multi-signature for large transactions
- Regular security audits of trading strategies

### Data Privacy
- Encrypt sensitive configuration data
- Secure API keys and access tokens
- Implement access controls for different user roles
- Regular security compliance checks

## Troubleshooting Guide

### Debugging Transactions
1. Check transaction digest for execution details
2. Verify input parameters match expected format
3. Confirm gas budget is sufficient
4. Check network status and RPC endpoint

### Debugging Queries
1. Validate query parameters and types
2. Check network connectivity
3. Verify pool and coin configurations
4. Test with simplified queries first

### Performance Issues
1. Monitor network latency
2. Check RPC endpoint health
3. Optimize query complexity
4. Implement rate limiting if needed

## References

### Official Documentation
- [DeepBook V3 SDK Documentation](https://docs.mystenlabs.com/deepbook)
- [Sui TypeScript SDK](https://docs.mystenlabs.com/sui-typescript-sdk)
- [Claude Code Skills Guide](https://code.claude.com/docs/en/skills)

### Example Code
- [Basic Setup](examples/01-basic-setup.ts)
- [Limit Order Example](examples/03-limit-order.ts)
- [Market Order Example](examples/04-market-order.ts)
- [Flash Loan Example](examples/06-flash-loan.ts)

### Community Resources
- [Sui Developer Discord](https://discord.gg/sui)
- [DeepBook GitHub Repository](https://github.com/mystenlabs/deepbook)
- [Sui Developer Forum](https://forums.sui.io/)

---

*Last Updated: 2026-01-09*
*Skill Version: 1.0.0*
*Compatible with: DeepBook V3 SDK 0.22+, Sui SDK 1.45+*