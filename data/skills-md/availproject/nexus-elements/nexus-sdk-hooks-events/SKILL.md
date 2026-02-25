---
name: nexus-sdk-hooks-events
description: Configure Nexus SDK intent/allowance/swap intent hooks and event streaming. Use when integrating approval flows, intent previews, or real-time progress events (NEXUS_EVENTS).
---

# Hooks and Events

## Set up hooks once after SDK init
- Call `sdk.setOnIntentHook(callback)`.
- Call `sdk.setOnAllowanceHook(callback)`.
- Call `sdk.setOnSwapIntentHook(callback)`.
- If a hook is not set, the SDK auto-approves and continues.
- If a hook is set, always call `allow(...)` or `deny()` or the flow will stall.
- Optionally auto-deny after a timeout to avoid hanging UX.

## Handle intent hook (bridge / bridgeAndTransfer / bridgeAndExecute)

### Signature
```ts
sdk.setOnIntentHook((data) => {
  // data: OnIntentHookData
});
```

### OnIntentHookData
- `allow(): void` — continue the flow
- `deny(): void` — reject the flow
- `intent: ReadableIntent` — readable intent info for UI
- `refresh(selectedSources?: number[]): Promise<ReadableIntent>` — refresh the intent

### How to use
- Store `data` in a ref so UI can call `allow()`/`deny()` later.
- Call `refresh()` on an interval (e.g., every 15s) if you show intent details.
- If the user closes the modal or cancels, call `deny()` and clear the ref.

## Handle allowance hook (approval control)

### Signature
```ts
sdk.setOnAllowanceHook((data) => {
  // data: OnAllowanceHookData
});
```

### OnAllowanceHookData
- `allow(decisions): void`
  - `decisions` must match the number of `sources`
  - each entry can be `'min'`, `'max'`, `bigint`, or numeric string
- `deny(): void`
- `sources: AllowanceHookSources`
  - includes chain/token info and current vs required allowance

### How to use
- Present each source to the user (chain + token + required allowance).
- Build the `decisions` array in the same order as `sources`.
- Call `allow(decisions)` to continue, or `deny()` to cancel.
- Ensure `decisions.length === sources.length` or the SDK will reject with `INVALID_VALUES_ALLOWANCE_HOOK`.

## Handle swap intent hook (swap flows)

### Signature
```ts
sdk.setOnSwapIntentHook((data) => {
  // data: OnSwapIntentHookData
});
```

### OnSwapIntentHookData
- `allow(): void`
- `deny(): void`
- `intent: SwapIntent`
- `refresh(): Promise<SwapIntent>`

### How to use
- Store `data` and show a UI summary.
- Call `allow()` to proceed or `deny()` to cancel.

## Stream events for progress UI

### Attach listeners
- All main operations accept `{ onEvent }` in options.

### Event names and payloads
- `NEXUS_EVENTS.STEPS_LIST` → `BridgeStepType[]`
- `NEXUS_EVENTS.STEP_COMPLETE` → `BridgeStepType`
- `NEXUS_EVENTS.SWAP_STEP_COMPLETE` → `SwapStepType`

### Typical usage
- Use `STEPS_LIST` to seed step trackers.
- Use `STEP_COMPLETE` and `SWAP_STEP_COMPLETE` to update progress and explorer links.

## Handle errors and cancellation
- If an operation throws, clear intent/allowance refs to avoid stale state.
- On user cancel, call `deny()` for the active hook and reset UI state.
- If a hook is set but no `allow()`/`deny()` is called, the intent remains pending.

## Expand error-handling patterns

### Normalize errors
- The SDK throws `NexusError` for known failures.
- Import from SDK:
  - `import { NexusError, ERROR_CODES } from '@avail-project/nexus-core'`

### Map common error codes to UX responses
- `USER_DENIED_INTENT` / `USER_DENIED_ALLOWANCE` / `USER_DENIED_INTENT_SIGNATURE`:
  - Treat as user cancel; show a neutral message and reset UI.
- `INVALID_VALUES_ALLOWANCE_HOOK`:
  - Fix `decisions` length/type and resubmit.
- `SDK_NOT_INITIALIZED` / `WALLET_NOT_CONNECTED` / `CONNECT_ACCOUNT_FAILED`:
  - Prompt user to reconnect; re-run `sdk.initialize(...)`.
- `INVALID_INPUT` / `INVALID_ADDRESS_LENGTH`:
  - Validate inputs; block submission until fixed.
- `INSUFFICIENT_BALANCE` / `NO_BALANCE_FOR_ADDRESS`:
  - Prompt user to reduce amount or fund source chain.
- `TOKEN_NOT_SUPPORTED` / `CHAIN_NOT_FOUND`:
  - Block submission and update selectors.
- `QUOTE_FAILED` / `SWAP_FAILED` / `RATES_CHANGED_BEYOND_TOLERANCE` / `SLIPPAGE_EXCEEDED_ALLOWANCE`:
  - Re-run quote or suggest a smaller amount.
- `RFF_FEE_EXPIRED`:
  - Re-simulate and re-submit the transaction.
- `TRANSACTION_TIMEOUT` / `LIQUIDITY_TIMEOUT`:
  - Show “pending” state and allow retry or check intent history.
- `TRANSACTION_REVERTED`:
  - Display failure with explorer link if available.
- `COSMOS_ERROR` / `INTERNAL_ERROR`:
  - Show a generic error and log `err.data?.details` for support.

### Use a helper pattern
```ts
import { NexusError, ERROR_CODES } from '@avail-project/nexus-core';

export function getReadableNexusError(err: unknown): string {
  if (err instanceof NexusError) {
    switch (err.code) {
      case ERROR_CODES.USER_DENIED_INTENT:
      case ERROR_CODES.USER_DENIED_ALLOWANCE:
      case ERROR_CODES.USER_DENIED_INTENT_SIGNATURE:
        return 'Transaction cancelled by user';
      case ERROR_CODES.INSUFFICIENT_BALANCE:
        return 'Insufficient balance';
      case ERROR_CODES.SLIPPAGE_EXCEEDED_ALLOWANCE:
      case ERROR_CODES.RATES_CHANGED_BEYOND_TOLERANCE:
        return 'Price changed too much. Please try again.';
      case ERROR_CODES.TRANSACTION_TIMEOUT:
        return 'Transaction timed out. Please retry.';
      default:
        return err.message;
    }
  }
  if (err instanceof Error) return err.message;
  return 'Unknown error';
}
```

### Clean up on error
- Clear intent/allowance refs and reset progress state:
  - `intentRef.current = null; allowanceRef.current = null; swapIntentRef.current = null;`
  - reset step UI and pending flags
