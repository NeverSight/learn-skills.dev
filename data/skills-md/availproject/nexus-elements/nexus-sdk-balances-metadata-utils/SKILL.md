---
name: nexus-sdk-balances-metadata-utils
description: Fetch balances, supported chains/tokens, intent history, and use Nexus SDK formatter utilities. Use when building token/chain selectors, showing balances, or formatting UI values.
---

# Balances, Metadata, and Utilities

## Fetch bridge balances
- Call `sdk.getBalancesForBridge()` to list assets usable in bridge flows.
- Typical fields on each asset:
  - `symbol`, `decimals`, `balance`, `balanceInFiat`, `breakdown[]`
- Use for:
  - token selectors
  - max amount validation
  - per-chain balance breakdown

## Fetch swap balances
- Call `sdk.getBalancesForSwap(onlyNativesAndStables?)` to list assets usable in swap flows.
- Use for:
  - swap token selectors
  - swap input validation
  - source selection for exact-in swaps

## Fetch supported chains/tokens
- Call `sdk.utils.getSupportedChains(env?)` for supported chains + tokens.
- Call `sdk.utils.getSwapSupportedChainsAndTokens()` for swap-supported chains/tokens.
- Call `sdk.getSwapSupportedChains()` for chains where swaps are supported.

## Fetch intent history
- Call `sdk.getMyIntents(page = 1)` to retrieve `RequestForFunds[]`.
- Use history to show status updates or allow retries.

## Use constants for UI
- Use `SUPPORTED_CHAINS` for chain IDs.
- Use `CHAIN_METADATA` for names, logos, explorers, native currency.
- Use `TOKEN_CONTRACT_ADDRESSES` for token addresses by chain.
- Use `NEXUS_EVENTS` for event name constants.

## Use formatter utilities
- Call `sdk.utils.formatTokenBalance(value, { symbol, decimals })`.
- Call `sdk.utils.formatTokenBalanceParts(...)`.
- Call `sdk.utils.formatUnits(value, decimals)`.
- Call `sdk.utils.parseUnits(value, decimals)`.
- Call `sdk.utils.truncateAddress(address, start?, end?)`.
- Call `sdk.utils.isValidAddress(address)`.
- Call `sdk.utils.getCoinbaseRates()` for optional fiat rates.
- Call `sdk.convertTokenReadableAmountToBigInt(value, tokenSymbol, chainId)` when decimals vary by chain.
