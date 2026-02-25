---
name: wagmi
description: Wagmi — React/Vue/Solid hooks and Core for Ethereum; config, connectors, read/write contracts, TanStack Query.
metadata:
  author: hairy
  version: "2026.2.9"
  source: Generated from https://github.com/wevm/wagmi, scripts located at https://github.com/antfu/skills
---

> Skill based on Wagmi v3.4.2, generated 2026-02-09. Docs: https://wagmi.sh

Wagmi provides **reactive Ethereum primitives**: React/Vue/Solid hooks and **Wagmi Core** (vanilla). Built on **Viem** and **TanStack Query**. This skill focuses on agent capabilities — config, connectors, connect wallet, read/write contract, query/mutation options, CLI, and TypeScript.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| createConfig | Chains, transports, connectors, storage, Config API | [core-config](references/core-config.md) |
| Transports | http, fallback, webSocket, custom — RPC configuration per chain | [core-transports](references/core-transports.md) |
| Storage | createStorage — custom persistence (cookie, IndexedDB), serialize/deserialize | [core-storage](references/core-storage.md) |
| Core Actions | Vanilla usage: getConnection, ENS, readContract, writeContract | [core-actions](references/core-actions.md) |
| Connectors | injected, WalletConnect, MetaMask, Coinbase, Safe, EIP-6963 | [core-connectors](references/core-connectors.md) |

## React

| Topic | Description | Reference |
|-------|-------------|-----------|
| Setup | WagmiProvider, QueryClientProvider, config | [react-setup](references/react-setup.md) |
| Connect Wallet | useConnect, useAccount, useDisconnect, useConnectors, useConnection | [react-connect-wallet](references/react-connect-wallet.md) |
| Reconnect | useReconnect, reconnectOnMount | [react-reconnect](references/react-reconnect.md) |
| Chain & Network | useChainId, useChains, useSwitchChain | [react-chain-network](references/react-chain-network.md) |
| Block & Balance | useBlockNumber, useBalance | [react-block-balance](references/react-block-balance.md) |
| Send Transaction | useSendTransaction, useWaitForTransactionReceipt — raw ETH/tx | [react-send-transaction](references/react-send-transaction.md) |
| Read/Write Contract | useReadContract, useWriteContract, useSimulateContract, useWaitForTransactionReceipt | [react-read-write-contract](references/react-read-write-contract.md) |
| ENS | useEnsName, useEnsAddress, useEnsAvatar, useEnsResolver, useEnsText | [react-ens](references/react-ens.md) |
| Sign Message | useSignMessage, useSignTypedData — EIP-191 and EIP-712 | [react-sign-message](references/react-sign-message.md) |
| TanStack Query | query/mutation options, caching, SSR, Devtools | [react-tanstack-query](references/react-tanstack-query.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| create-wagmi CLI | Scaffold Next/Nuxt/Vite React/Vue/Vanilla projects | [features-cli](references/features-cli.md) |
| SSR | ssr flag, cookie storage, cookieToInitialState, serialize/deserialize | [features-ssr](references/features-ssr.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| TypeScript | Register config, chain/ABI inference, strict types | [best-practices-typescript](references/best-practices-typescript.md) |
| Error Handling | Typed errors, BaseError, discriminating by error.name | [best-practices-error-handling](references/best-practices-error-handling.md) |

## External Links

- [Wagmi Docs](https://wagmi.sh)
- [wevm/wagmi GitHub](https://github.com/wevm/wagmi)
- [Viem](https://viem.sh)
