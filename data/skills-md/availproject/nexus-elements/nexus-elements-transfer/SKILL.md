---
name: nexus-elements-transfer
description: Integrate the Transfer element (registry name `transfer`) for bridge-to-recipient flows in React/TypeScript apps. Use when installing or debugging cross-chain recipient transfers, allowance/intent approvals, source-selection constraints, and `sdk.bridgeAndTransfer` step execution.
---

# Nexus Elements - Transfer

## Install
- Install widget:
  - `npx shadcn@latest add @nexus-elements/transfer`
- Ensure `NexusProvider` is installed and initialized before rendering.

## Required setup before rendering
- Ensure `useNexus().nexusSDK` is initialized.
- Ensure `bridgableBalance` has loaded.
- Ensure recipient is valid EVM address (prefill or user input).

## Initialize SDK (required once per app)
- On wallet connect, resolve an EIP-1193 provider and call `useNexus().handleInit(provider)`.
- Wait for `useNexus().nexusSDK` before allowing transfer actions.
- Re-run init after reconnect if wallet session resets.

## Render widget
```tsx
"use client";

import FastTransfer from "@/components/transfer/transfer";
import { SUPPORTED_CHAINS } from "@avail-project/nexus-core";

export function TransferPanel() {
  return (
    <FastTransfer
      prefill={{
        token: "USDC",
        chainId: SUPPORTED_CHAINS.BASE,
        recipient: "0x000000000000000000000000000000000000dead",
      }}
      onStart={() => {
        // pending
      }}
      onComplete={() => {
        // success
      }}
      onError={(message) => {
        console.error(message);
      }}
    />
  );
}
```

## Live prop contract
- `prefill?`:
  - `token`, `chainId`, optional `amount`, optional `recipient`.
- `maxAmount?`: cap transferable amount.
- `onStart?`, `onComplete?`, `onError?(message)` callbacks.

## SDK flow details (under the hood)
- Primary execute call:
  - `sdk.bridgeAndTransfer({ token, amount, toChainId, recipient, sourceChains }, { onEvent })`
- Pre-execution checks:
  - validate recipient + amount
  - compute max available via `sdk.calculateMaxForBridge(...)`
  - enforce selected-source sufficiency
- Hook usage:
  - `intent.current` for transfer intent preview/refresh/allow
  - `allowance.current` for source-specific allowance decisions
- Event mapping:
  - `NEXUS_EVENTS.STEPS_LIST` -> initialize step tracker
  - `NEXUS_EVENTS.STEP_COMPLETE` -> progress update and elapsed timer

## Understand recipient behavior
- Transfer flow requires recipient address.
- Prefill recipient locks input.
- Without prefill, UI validates recipient and blocks invalid addresses.

## E2E verification
- Fill token/chain/amount/recipient and confirm intent preview appears.
- Adjust source chains and confirm coverage indicators update.
- Accept and verify allowance step when required.
- Confirm success updates explorer URL and refreshes balances.
- Confirm history refresh event appears in `ViewHistory` (when present).

## Common failure cases
- Invalid recipient:
  - pass a checksummed or valid hex address.
- Exceeds selected source max:
  - reduce amount or enable more source chains.
- Flow canceled:
  - expect `onError` with user-cancel message and reset state.
