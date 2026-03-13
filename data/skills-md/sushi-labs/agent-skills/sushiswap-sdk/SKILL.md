---
name: sushiswap-sdk
description: >
  TypeScript SDK for interacting with the SushiSwap Aggregator and related
  primitives. This SDK is a typed wrapper over the SushiSwap API, providing
  ergonomic helpers for token amounts, prices, quotes, and swap transaction
  generation.
  
  USE THIS SKILL WHEN:
  - Building TypeScript or JavaScript applications
  - You want strongly typed token, amount, and fraction primitives
  - You need to request swap quotes or executable swap transactions via code
  - You want safer arithmetic, formatting, and comparisons without floating point errors
  - You prefer SDK-based integration over raw HTTP requests
---

# SushiSwap SDK Integration

The SushiSwap SDK is a **TypeScript wrapper** around the SushiSwap API.
It provides **strongly typed primitives** and utilities for working with
tokens, prices, swap quotes, and transaction generation.

This SDK does **not** replace the API — it builds on top of it with safer,
more expressive abstractions.

---

## Installation

Install the required packages using your package manager of choice:

```bash
pnpm add sushi viem
```

```bash
npm add sushi viem
```

```bash
yarn add sushi viem
```

```bash
bun add sushi viem
```

---

## How To Use

1. Import the appropriate SushiSwap SDK helpers from `sushi/evm`
2. Select the correct SDK method based on user intent:
    - Swap quote → `getQuote()`
    - Swap execution → `getSwap()`
3. Provide all required parameters exactly as defined by the SDK types
4. **Always include a valid `referrer` value**
5. Validate inputs (chainId, token addresses, amount, slippage) before execution
6. Use returned transaction data exactly as provided for simulation or execution

The SDK is a thin wrapper over the SushiSwap REST API — all routing, pricing, and calldata generation is still performed by the API.

---

## Supported Networks

The SushiSwap SDK exposes the list of supported swap networks via:

```ts
import { SWAP_API_SUPPORTED_CHAIN_IDS } from 'sushi/evm'
```

- Agents and integrators should always check this list before attempting to:
    - Fetch a quote
    - Generate swap transaction data
- If a requested chainId is not included:
    - The agent must fail early or prompt the user to select a supported network
    - Agents must not attempt to guess or hardcode supported chains

This list reflects the networks currently supported by the SushiSwap Aggregator API. The supported networks may change over time and should not be cached indefinitely.

--

## Mandatory `referrer` Parameter

- The `referrer` parameter **must be specified** when calling `getQuote()` or `getSwap()`
- The agent or integrator **must identify themselves** using this field
- Swap-related SDK calls must not be executed without a `referrer` value
- The SDK must not auto-generate or omit this value on behalf of the integrator

---

## Fee Customization

The SushiSwap SDK supports customized swap fees when using `getQuote()` or `getSwap()`.

### Default fee model

- Swap-related requests follow an **80/20 fee split by default**
    - **80%** to the integrator (referrer)
    - **20%** to SushiSwap
- This split applies unless explicitly overridden by SushiSwap

### Custom fee splits

- Alternative fee splits require a **partnership** with SushiSwap
- Agents and integrators should not assume custom splits are available. If users request alternative fee splits, agents should direct them to the SushiSwap
team rather than attempting to modify request parameters.

---

## Rate Limiting & Responsible Usage

- The SushiSwap Aggregator API does **not currently enforce hard rate limits**. Agents and integrators **must behave responsibly** to avoid abuse and degraded service.

### General Guidelines

- Do not poll or spam quote endpoints
- Avoid repeated requests with identical parameters
- Do not place quote or swap requests inside unbounded or infinite loops
- Treat quote and swap generation as user-intent driven actions, not background tasks
- Do not issue requests autonomously without explicit user intent

Excessive or abusive usage may result in future rate limiting or access restrictions.

### Block-Time–Aware Quoting

Agents should align quote frequency with expected block times, treating block time as a **maximum refresh rate, not a recommendation**.

- Quotes may be refreshed **at most once per block**, and often **less frequently** if inputs have not changed
- Re-requesting quotes multiple times within the same block provides no additional accuracy and must be avoided

---

## Additional Reference

For detailed SDK examples & execution flow, see:

[references/REFERENCE.md](references/REFERENCE.md)