---
name: nexus-sdk-setup
description: Set up and initialize Nexus SDK in any JS/TS frontend project. Use when configuring wallet provider, SDK instance lifecycle, network selection, or adding a minimal wallet connection path.
---

# Nexus SDK Setup

## Install dependency
- Install the SDK package:
  - `npm install @avail-project/nexus-core`
  - or `pnpm add @avail-project/nexus-core`
  - or `yarn add @avail-project/nexus-core`

## Obtain an EIP-1193 provider
- Use any wallet connection stack to get a provider.
- Ensure the provider has a `request` method.
- Use a browser fallback only when appropriate:
  - `const provider = (window as any).ethereum`

## Construct the SDK instance
- Create `new NexusSDK({ network, debug, siweChain })`.
- Provide `network`:
  - `'mainnet'` or `'testnet'` to use default endpoints.
  - `NetworkConfig` to use custom endpoints.
- Provide `debug?: boolean` to enable verbose SDK logging.
- Provide `siweChain?: number` to set the SIWE chain id (if you use SIWE).

## Initialize once
- Create a single instance and reuse it.
- Store the instance in a module singleton or a React ref.
- Guard with `sdk.isInitialized()` to avoid re-init.

### Minimal example
```ts
import { NexusSDK, type EthereumProvider } from '@avail-project/nexus-core';

const sdk = new NexusSDK({ network: 'mainnet' });

export async function initNexus(provider: EthereumProvider) {
  if (sdk.isInitialized()) return sdk;
  if (!provider || typeof provider.request !== 'function') {
    throw new Error('Invalid EIP-1193 provider');
  }
  await sdk.initialize(provider);
  return sdk;
}
```

## Initialize when a wallet kit is already integrated (FamilyKit / wagmi-based)
- If your kit exposes a wagmi connector, derive an EIP-1193 provider from it.
- Use the same pattern as Nexus Elements: prefer `connector.getProvider()` on desktop and a `walletClient.request` wrapper on mobile.
- Example (adapt to your hooks and UI state):
```ts
import { NexusSDK, type EthereumProvider } from '@avail-project/nexus-core';
import { useAccount, useConnectorClient } from 'wagmi';

const sdk = new NexusSDK({ network: 'mainnet', debug: false });

async function initFromWalletKit(isMobile: boolean) {
  const { connector } = useAccount();
  const { data: walletClient } = useConnectorClient();

  const mobileProvider =
    walletClient &&
    ({
      request: (args: unknown) => walletClient.request(args as never),
    } as EthereumProvider);

  const desktopProvider = await connector?.getProvider();
  const effectiveProvider = isMobile ? mobileProvider : desktopProvider;

  if (!effectiveProvider || typeof effectiveProvider.request !== 'function') {
    throw new Error('Invalid EIP-1193 provider from wallet kit');
  }

  if (!sdk.isInitialized()) {
    await sdk.initialize(effectiveProvider);
  }

  return sdk;
}
```

## Handle disconnect / teardown
- On wallet disconnect, call `await sdk.deinit()`.
- Clear state (balances, hook refs, cached intents).

## Use provider-only mode (optional)
- If you need balances before full init, call:
  - `await sdk.setEVMProvider(provider)`
- Check `sdk.hasEvmProvider` to confirm.

## Handle SSR / client-only execution
- Initialize in client-only code (`useEffect` or dynamic import) to avoid SSR issues.

## Handle account changes
- If provider supports events, re-fetch balances on `accountsChanged`.
- If provider lacks `.on`/`.removeListener`, call:
  - `sdk.triggerAccountChange()` after the wallet address changes.

## Handle init errors
- Wrap `sdk.initialize` in try/catch.
- If `SDK_INIT_STATE_NOT_EXPECTED`, call `await sdk.deinit()` and retry.
- If `WALLET_NOT_CONNECTED` or `CONNECT_ACCOUNT_FAILED`, prompt user to reconnect.
