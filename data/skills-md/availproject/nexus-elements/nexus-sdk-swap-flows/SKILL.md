---
name: nexus-sdk-swap-flows
description: Implement swapWithExactIn, swapWithExactOut, and swapAndExecute flows with Nexus SDK. Use when wiring swap operations, swap intent hooks, or swap event progress updates.
---

# Swap Flows

## Call swapWithExactIn(input, options?)
- Use when input amount is fixed and sources are known.
- Signature:
  - `sdk.swapWithExactIn(input, { onEvent? })`
- Params (`ExactInSwapInput`):
  - `from: { chainId: number; amount: bigint; tokenAddress: Hex }[]`
  - `toChainId: number`
  - `toTokenAddress: Hex`
- Notes:
  - Ensure `from` amounts are in smallest units.
  - Use chain-specific token addresses (see `TOKEN_CONTRACT_ADDRESSES`).
- Result (`SwapResult`):
  - `{ success: true; result: SuccessfulSwapResult }`

## Call swapWithExactOut(input, options?)
- Use when desired output amount is fixed.
- Signature:
  - `sdk.swapWithExactOut(input, { onEvent? })`
- Params (`ExactOutSwapInput`):
  - `toChainId: number`
  - `toTokenAddress: Hex`
  - `toAmount: bigint`
  - `toNativeAmount?: bigint` (optional native token output)
  - `fromSources?: { chainId: number; tokenAddress: Hex }[]` (optional)
- Notes:
  - If `fromSources` is omitted, SDK auto-selects sources.

## Call swapAndExecute(input, options?)
- Use to perform swap (if needed) and then execute a contract call.
- Signature:
  - `sdk.swapAndExecute(input, { onEvent? })`
- Params (`SwapAndExecuteParams`):
  - `toChainId: number`
  - `toTokenAddress: Hex`
  - `toAmount: bigint`
  - `fromSources?: { chainId: number; tokenAddress: Hex }[]`
  - `execute: SwapExecuteParams`
- `SwapExecuteParams`:
  - `to: Hex`
  - `data?: Hex`
  - `value?: bigint`
  - `gas: bigint`
  - `gasPrice?: 'low' | 'medium' | 'high'`
  - `tokenApproval?: { token: Hex; amount: bigint; spender: Hex }`
- Result (`SwapAndExecuteResult`):
  - `swapResult: SuccessfulSwapResult | null` (null if swap skipped)

## Use token addresses and chains
- Use SDK constants for addresses and chain IDs:
  - `SUPPORTED_CHAINS`
  - `TOKEN_CONTRACT_ADDRESSES`

## Attach swap intent hook
- Set `sdk.setOnSwapIntentHook(...)` and call `allow()` to proceed.
- If the hook is not set, the SDK auto-approves.

## Stream swap events
- Listen for `NEXUS_EVENTS.SWAP_STEP_COMPLETE`.
- Handle special cases like swap skipped (e.g., already on destination token).

## Convert amounts to bigint
- Use `sdk.utils.parseUnits(value, decimals)` or
- `sdk.convertTokenReadableAmountToBigInt(value, tokenSymbol, chainId)` when decimals vary by chain.
