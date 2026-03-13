---
name: hydric-gateway-js-ts-sdk-user
description: Expert skill for integrating the hydric Gateway SDK (@hydric/gateway) in JavaScript and TypeScript. Use this skill to orchestrate multi-chain liquidity, resolve token identities, and build high-fidelity DeFi dashboards with institution-grade precision.
---

# hydric Gateway SDK | Orientation Guide

You are an **SDK Integration Specialist** for `@hydric/gateway`. This skill helps you quickly orient yourself and use the SDK like you built it.

---

## 📚 Where to Find Things

| What You Need            | Where to Look                                                                    |
| :----------------------- | :------------------------------------------------------------------------------- |
| **Full SDK Docs**        | https://docs.hydric.org/sdk-reference/typescript                                 |
| **Live Docs MCP Server** | https://docs.hydric.org/mcp                                                      |
| **Source Code**          | https://github.com/hydric-org/gateway-sdk/tree/main/sdks/typescript              |
| **NPM Package**          | `@hydric/gateway`                                                                |
| **Supported Chains**     | https://docs.hydric.org/overview/supported-blockchains                           |
| **Basket IDs**           | https://docs.hydric.org/sdk-reference/typescript/token-baskets#available-baskets |
| **Supported Protocols**  | https://docs.hydric.org/overview/supported-protocols                             |

---

## Installation

the SDK is available as an npm package. So you can install it using npm, yarn, pnpm, bun, etc. Just run:

```bash
npm install @hydric/gateway
```

Node version >= 18 is recommended.

---

## 🎯 Mental Model: Resources

The SDK has **one client** and **some resources**:

```javascript
import { HydricGateway } from '@hydric/gateway';

const hydric = new HydricGateway({
  apiKey: process.env.HYDRIC_API_KEY,
});

// The resources:
hydric.multichainTokens; // Multi-chain token aggregation
hydric.singleChainTokens; // Single-chain token operations (faster)
hydric.tokenBaskets; // Curated token baskets of many sectors
hydric.liquidityPools; // Global liquidity pool and pair discovery
```

### Resource Selection Rule

- User mentions a **specific chain** to get tokens? → Use `singleChainTokens`
- User wants **global view** of tokens? → Use `multichainTokens`
- User wants **curated groups** of tokens (stablecoins, BTCs, LSTs)? → Use `tokenBaskets`
- User wants to find **DEX pools, liquidity, or token pairs**? → Use `liquidityPools`

---

## ⚡ Quick Start Pattern

```javascript
// 1. Initialize
const hydric = new HydricGateway({ apiKey: 'sk_...' });

// 2. Call a resource method
const { tokens } = await hydric.multichainTokens.search({
  search: 'USDC',
  config: { limit: 10 },
});

// 3. Handle errors
try {
  const data = await hydric.tokenBaskets.getSingleChainById({
    chainId: 8453,
    basketId: 'usd-stablecoins',
  });
} catch (error) {
  if (error instanceof HydricRateLimitError) {
    /* backoff */
  }
  if (error instanceof HydricNotFoundError) {
    /* handle not found */
  }
}
```

---

## 📦 Resource Cheat Sheet

### `multichainTokens`

**When**: User wants tokens across ALL chains or multiple chains at once.
**Methods**: `list()`, `search({ search })`

### `singleChainTokens`

**When**: User specified ONE chain for getting tokens  
**Methods**: `list(chainId, params)`, `search(chainId, { search })`

### `tokenBaskets`

**When**: User wants curated groups of tokens (stablecoins, BTCs, LSTs)  
**Methods**:

- `list()` - All baskets
- `getMultiChainById({ basketId })` - Basket across chains
- `getSingleChainById({ chainId, basketId })` - Basket on one chain

### `liquidityPools`

**When**: User wants to find liquidity pools across Dexes (Uniswap V3/V4, Algebra) matching specific tokens, baskets, TVL, or protocols.  
**Methods**: `search({ tokensA, tokensB, basketsA, basketsB, filters, config })`

> **Agent Pro-Tip:** `basketsA` and `basketsB` enable powerful server-side basket resolution (e.g., finding any stablecoin pool) without needing hundreds of addresses. However, **you MUST know the correct basket IDs** either from a previous `tokenBaskets.list()` call or because the user provided them.
>
> **Pair Matching Logic:**
>
> - `tokensA` only: Returns pools containing at least one token from A.
> - `tokensA` + `tokensB`: Returns pools containing one token from A **AND** one token from B (direct pair matching).
> - This logic applies equally to `basketsA` and `basketsB`, allowing for searches like "Any Stablecoin vs ETH".

---

## 🚨 Critical Gotchas

### 1. Method Signatures Vary

```javascript
// Multi-chain: params object only
hydric.multichainTokens.list({ config, filters });

// Single-chain: chainId FIRST, then params
hydric.singleChainTokens.list(8453, { config, filters });
```

### 2. Addresses Are Always Lowercase

All responses return lowercase addresses. The API accepts any case but normalizes responses to lowercase.

### 3. Pagination Pattern

```javascript
let cursor = null;
do {
  const { tokens, nextCursor } = await hydric.multichainTokens.list({
    config: { cursor, limit: 100 },
  });
  cursor = nextCursor; // null when done
} while (cursor);
```

### 4. Error Classes

Import and check with `instanceof`:

- `HydricInvalidParamsError` - Client-side validation failed
- `HydricUnauthorizedError` - API key issue
- `HydricNotFoundError` - Specific requested resource doesn't exist
- `HydricRateLimitError` - Too many requests for the API Key tier
- `HydricError` - Generic error

---

## 🧭 Common Workflows

### Workflow 1: Global Token Search

```javascript
// User: "Find USDC everywhere"
const { tokens } = await hydric.multichainTokens.search({ search: 'USDC' });
// Each token has: addresses: [{ chainId: 1, address: '0x...' }, ...]
```

### Workflow 2: Chain-Specific List

```javascript
// User: "Show me top tokens on Base ordered by tvl"
const { tokens } = await hydric.singleChainTokens.list(8453, {
  config: { orderBy: { field: 'tvl', direction: 'desc' } },
});
```

### Workflow 3: Basket Discovery

```javascript
// User: "Get all stablecoins on Ethereum"
const { basket } = await hydric.tokenBaskets.getSingleChainById({
  chainId: 1,
  basketId: 'usd-stablecoins',
});
// basket.tokens = [{ symbol: 'USDC', address: '0x...' }, ...]
```

### Workflow 4: Discover Pair Liquidity

```javascript
// User: "Find high TVL USDC-ETH pools on Base"
const { pools } = await hydric.liquidityPools.search({
  tokensA: [{ chainId: 8453, address: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913' }], // USDC
  tokensB: [{ chainId: 8453, address: '0x0000000000000000000000000000000000000000' }], // ETH
  config: { limit: 5, orderBy: { field: 'tvl', direction: 'desc' } },
  filters: { minimumTotalValueLockedUsd: 100000 },
});
// pools = [{ address: '0x...', protocol: { name: 'Uniswap V3' }, balance: { totalValueLockedUsd: 500000 } }, ...]
```

### Workflow 5: Direct Pair Matching (Basket vs Basket)

```javascript
// User: "I want to see liquidity between any Stablecoin and any BTC-pegged token"
const { pools } = await hydric.liquidityPools.search({
  basketsA: [{ basketId: 'usd-stablecoins' }],
  basketsB: [{ basketId: 'btc-pegged-tokens' }],
  config: { limit: 10 },
});
// The API resolves both baskets and returns only pools matching (any Stable) <-> (any BTC)
```

---

## 🛠️ Implementation Checklist

Before writing code:

- [ ] Is this single-chain or multi-chain? (Choose resource accordingly)
- [ ] Do I have the API key in environment variables?
- [ ] Am I using the correct method signature for the resource?
- [ ] Do I have error handling?
- [ ] If listing many results, did I implement pagination?

---

## 🔍 Quick Method Lookup

| Task                      | Code                                                                  |
| :------------------------ | :-------------------------------------------------------------------- |
| List tokens globally      | `hydric.multichainTokens.list({ config, filters })`                   |
| List tokens on chain      | `hydric.singleChainTokens.list(chainId, { config, filters })`         |
| Search globally           | `hydric.multichainTokens.search({ search, config })`                  |
| Search on chain           | `hydric.singleChainTokens.search(chainId, { search, config })`        |
| Get all baskets           | `hydric.tokenBaskets.list()`                                          |
| Get basket (multi-chain)  | `hydric.tokenBaskets.getMultiChainById({ basketId })`                 |
| Get basket (single chain) | `hydric.tokenBaskets.getSingleChainById({ chainId, basketId })`       |
| Search liquidity pools    | `hydric.liquidityPools.search({ tokensA, tokensB, filters, config })` |
| Search pools by baskets   | `hydric.liquidityPools.search({ basketsA, basketsB, config })`        |

---

## 📖 When You Need More

- **Full parameter docs**: https://docs.hydric.org/sdk-reference/typescript
- **Docs MCP Server**: Use the MCP server at https://docs.hydric.org/mcp for using the docs easily
- **Source code**: https://github.com/hydric-org/gateway-sdk/tree/main/sdks/typescript
- **TypeScript types**: Import from `'@hydric/gateway'` (e.g., `MultiChainTokenMetadata`)

---

## 🎯 Golden Rules

1. **Single-chain = singleChainTokens**. Always prefer it when the chain is known.
2. **ChainId first** for single-chain methods, params object first for multi-chain.
3. **Always lowercase** when comparing addresses.
4. **Paginate** if you're fetching more than 100 results.
5. **Catch errors** with `instanceof` checks for precise handling if needed.

Use this skill to quickly:

- ✅ Choose the right resource
- ✅ Remember method signatures
- ✅ Recall critical gotchas
- ✅ Know where to find complete docs
