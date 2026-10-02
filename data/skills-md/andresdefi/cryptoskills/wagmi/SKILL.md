---
name: wagmi
description: "wagmi React hooks for Ethereum — createConfig, useAccount, useReadContract, useWriteContract, useWaitForTransactionReceipt, wallet connectors, SSR/Next.js patterns, and TanStack Query integration. Build type-safe dApp frontends with viem under the hood."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Dev Tools
tags:
  - wagmi
  - react
  - hooks
  - ethereum
  - dapp
  - frontend
---

# wagmi

React hooks for Ethereum and EVM-compatible chains. Provides type-safe, composable primitives for wallet connection, contract reads/writes, transaction tracking, chain switching, and ENS resolution. Built on top of viem with TanStack Query for caching and state management.

## What You Probably Got Wrong

> Agents trained on pre-2024 data generate wagmi v1 code. wagmi v2 shipped breaking changes across the entire API surface. Every pattern below is different from v1.

- **`WagmiConfig` is removed -- use `WagmiProvider`** -- v1 used `<WagmiConfig client={client}>`. v2 uses `<WagmiProvider config={config}>`. Using the old component will throw "WagmiConfig is not exported".
- **`QueryClientProvider` is mandatory** -- wagmi v2 delegates all caching to TanStack Query. You must wrap your app in both `<WagmiProvider>` and `<QueryClientProvider>`. Without it, every hook throws "No QueryClient set".
- **`createConfig` replaces `createClient`** -- v1 used `createClient({ autoConnect, provider })`. v2 uses `createConfig({ chains, connectors, transports })`. The config shape is completely different.
- **Hook names changed** -- `useContractRead` -> `useReadContract`. `useContractWrite` -> `useWriteContract`. `useWaitForTransaction` -> `useWaitForTransactionReceipt`. `usePrepareContractWrite` is removed entirely.
- **`usePrepareContractWrite` no longer exists** -- v2 removes the prepare/write split. Use `useWriteContract` directly; it handles simulation internally via `useSimulateContract` if you need pre-flight checks.
- **Transports are per-chain, not global** -- v2 config requires a `transports` map keyed by chain ID: `transports: { [mainnet.id]: http(), [sepolia.id]: http() }`. There is no single global transport.
- **Connector imports changed** -- `import { injected, walletConnect, coinbaseWallet } from "wagmi/connectors"`, not from `wagmi` directly or `@wagmi/connectors`.
- **All token amounts are `bigint`** -- wagmi v2 returns raw `bigint` for balances, allowances, and contract return values. Never use JavaScript `number` for on-chain values.
- **ABIs must use `as const`** -- For type inference on `useReadContract`/`useWriteContract` args and return types, ABI arrays require `as const`. Without it, args become `unknown[]`.
- **`useChainId` replaces `useNetwork`** -- v1's `useNetwork()` returning `{ chain, chains }` is gone. Use `useChainId()` for the current chain ID and `useSwitchChain()` for switching.

## Quick Start

### Installation

```bash
npm install wagmi viem @tanstack/react-query
```

### Minimal Config

```typescript
import { http, createConfig } from "wagmi";
import { mainnet, sepolia } from "wagmi/chains";
import { injected, walletConnect } from "wagmi/connectors";

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [
    injected(),
    walletConnect({ projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID! }),
  ],
  transports: {
    [mainnet.id]: http(process.env.NEXT_PUBLIC_RPC_MAINNET),
    [sepolia.id]: http(process.env.NEXT_PUBLIC_RPC_SEPOLIA),
  },
});
```

### Provider Setup

```tsx
import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { config } from "./config";

const queryClient = new QueryClient();

function App({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## Core Hooks

### useAccount -- Connection State

```tsx
import { useAccount } from "wagmi";

function AccountInfo() {
  const { address, isConnected, isConnecting, isReconnecting, chain, connector } =
    useAccount();

  if (isConnecting || isReconnecting) {
    return <div>Connecting...</div>;
  }

  if (!isConnected || !address) {
    return <div>Not connected</div>;
  }

  return (
    <div>
      <p>Address: {address}</p>
      <p>Chain: {chain?.name ?? "Unknown"}</p>
      <p>Connector: {connector?.name ?? "Unknown"}</p>
    </div>
  );
}
```

### useConnect / useDisconnect -- Wallet Connection

```tsx
import { useConnect, useDisconnect } from "wagmi";

function ConnectButton() {
  const { connect, connectors, isPending, error } = useConnect();
  const { disconnect } = useDisconnect();
  const { isConnected } = useAccount();

  if (isConnected) {
    return <button onClick={() => disconnect()}>Disconnect</button>;
  }

  return (
    <div>
      {connectors.map((connector) => (
        <button
          key={connector.uid}
          onClick={() => connect({ connector })}
          disabled={isPending}
        >
          {connector.name}
        </button>
      ))}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

### useBalance -- Native and ERC-20 Balances

```tsx
import { useBalance } from "wagmi";

function Balance({ address }: { address: `0x${string}` }) {
  const { data, isLoading, error } = useBalance({ address });

  if (isLoading) return <span>Loading...</span>;
  if (error) return <span>Error: {error.message}</span>;
  if (!data) return null;

  return (
    <span>
      {data.formatted} {data.symbol}
    </span>
  );
}

// ERC-20 balance -- pass the token contract address
function TokenBalance({
  address,
  token,
}: {
  address: `0x${string}`;
  token: `0x${string}`;
}) {
  const { data } = useBalance({ address, token });

  if (!data) return null;

  // data.value is bigint, data.formatted is the human-readable string
  return (
    <span>
      {data.formatted} {data.symbol}
    </span>
  );
}
```

### useReadContract -- Reading On-Chain State

```tsx
import { useReadContract } from "wagmi";

const erc20Abi = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

function TokenBalanceOf({
  token,
  account,
}: {
  token: `0x${string}`;
  account: `0x${string}`;
}) {
  const { data, isLoading, error, refetch } = useReadContract({
    address: token,
    abi: erc20Abi,
    functionName: "balanceOf",
    args: [account],
  });

  if (isLoading) return <span>Loading...</span>;
  if (error) return <span>Error: {error.message}</span>;

  // data is bigint (uint256)
  return <span>Raw balance: {data?.toString()}</span>;
}
```

### useWriteContract -- Sending Transactions

```tsx
import { useWriteContract, useWaitForTransactionReceipt } from "wagmi";
import { parseUnits } from "viem";

const erc20Abi = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

function TransferToken({
  token,
  decimals,
}: {
  token: `0x${string}`;
  decimals: number;
}) {
  const { writeContract, data: hash, isPending, error } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  function handleTransfer(to: `0x${string}`, amount: string) {
    const parsedAmount = parseUnits(amount, decimals);

    writeContract({
      address: token,
      abi: erc20Abi,
      functionName: "transfer",
      args: [to, parsedAmount],
    });
  }

  return (
    <div>
      <button
        onClick={() =>
          handleTransfer("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "10")
        }
        disabled={isPending || isConfirming}
      >
        {isPending ? "Signing..." : isConfirming ? "Confirming..." : "Transfer"}
      </button>
      {isSuccess && <p>Transaction confirmed: {hash}</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

### useSimulateContract -- Pre-flight Validation

```tsx
import { useSimulateContract, useWriteContract } from "wagmi";
import { parseEther } from "viem";

const wethAbi = [
  {
    name: "deposit",
    type: "function",
    stateMutability: "payable",
    inputs: [],
    outputs: [],
  },
] as const;

const WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2" as const;

function WrapEth() {
  const { data: simulationResult, error: simulateError } = useSimulateContract({
    address: WETH_ADDRESS,
    abi: wethAbi,
    functionName: "deposit",
    value: parseEther("0.1"),
  });

  const { writeContract, isPending } = useWriteContract();

  return (
    <div>
      <button
        onClick={() => {
          if (simulationResult) {
            writeContract(simulationResult.request);
          }
        }}
        disabled={isPending || !simulationResult}
      >
        Wrap 0.1 ETH
      </button>
      {simulateError && <p>Simulation failed: {simulateError.message}</p>}
    </div>
  );
}
```

### useWaitForTransactionReceipt -- Transaction Tracking

```tsx
import { useWaitForTransactionReceipt } from "wagmi";

function TransactionStatus({ hash }: { hash: `0x${string}` | undefined }) {
  const { data: receipt, isLoading, error } = useWaitForTransactionReceipt({
    hash,
    // confirmations defaults to 1
    confirmations: 1,
  });

  if (!hash) return null;
  if (isLoading) return <p>Waiting for confirmation...</p>;
  if (error) return <p>Error: {error.message}</p>;

  if (receipt?.status === "reverted") {
    return <p>Transaction reverted in block {receipt.blockNumber.toString()}</p>;
  }

  return (
    <div>
      <p>Confirmed in block {receipt?.blockNumber.toString()}</p>
      <p>Gas used: {receipt?.gasUsed.toString()}</p>
    </div>
  );
}
```

### useChainId / useSwitchChain -- Chain Management

```tsx
import { useChainId, useSwitchChain } from "wagmi";

function ChainSwitcher() {
  const chainId = useChainId();
  const { chains, switchChain, isPending, error } = useSwitchChain();

  return (
    <div>
      <p>Current chain ID: {chainId}</p>
      {chains.map((chain) => (
        <button
          key={chain.id}
          onClick={() => switchChain({ chainId: chain.id })}
          disabled={isPending || chain.id === chainId}
        >
          {chain.name}
        </button>
      ))}
      {error && <p>Switch failed: {error.message}</p>}
    </div>
  );
}
```

### useEnsName / useEnsAddress -- ENS Resolution

```tsx
import { useEnsName, useEnsAddress } from "wagmi";

function DisplayName({ address }: { address: `0x${string}` }) {
  const { data: ensName } = useEnsName({ address });

  return <span>{ensName ?? `${address.slice(0, 6)}...${address.slice(-4)}`}</span>;
}

function ResolveEns({ name }: { name: string }) {
  const { data: address, isLoading, error } = useEnsAddress({ name });

  if (isLoading) return <span>Resolving...</span>;
  if (error) return <span>Resolution failed</span>;

  return <span>{address ?? "Not found"}</span>;
}
```

### useBlockNumber -- Block Tracking

```tsx
import { useBlockNumber } from "wagmi";

function LatestBlock() {
  const { data: blockNumber } = useBlockNumber({ watch: true });

  return <p>Latest block: {blockNumber?.toString()}</p>;
}
```

## Advanced Patterns

### Typed Contract Hook Factory

Create a reusable hook for a specific contract to avoid repeating address and ABI.

```tsx
import { useReadContract, useWriteContract, useSimulateContract } from "wagmi";
import type { Abi } from "viem";

const USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" as const;

const usdcAbi = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "approve",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
  {
    name: "allowance",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "owner", type: "address" },
      { name: "spender", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

function useUsdcBalance(account: `0x${string}`) {
  return useReadContract({
    address: USDC_ADDRESS,
    abi: usdcAbi,
    functionName: "balanceOf",
    args: [account],
  });
}

function useUsdcAllowance(owner: `0x${string}`, spender: `0x${string}`) {
  return useReadContract({
    address: USDC_ADDRESS,
    abi: usdcAbi,
    functionName: "allowance",
    args: [owner, spender],
  });
}

function useApproveUsdc(spender: `0x${string}`, amount: bigint) {
  return useSimulateContract({
    address: USDC_ADDRESS,
    abi: usdcAbi,
    functionName: "approve",
    args: [spender, amount],
  });
}
```

### Approve-Then-Execute Pattern

Most DeFi interactions require an ERC-20 approval before the main transaction.

```tsx
import {
  useReadContract,
  useWriteContract,
  useWaitForTransactionReceipt,
} from "wagmi";
import { parseUnits } from "viem";

const erc20Abi = [
  {
    name: "allowance",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "owner", type: "address" },
      { name: "spender", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "approve",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

function useApproveIfNeeded({
  token,
  owner,
  spender,
  amount,
}: {
  token: `0x${string}`;
  owner: `0x${string}`;
  spender: `0x${string}`;
  amount: bigint;
}) {
  const { data: currentAllowance, refetch: refetchAllowance } = useReadContract({
    address: token,
    abi: erc20Abi,
    functionName: "allowance",
    args: [owner, spender],
  });

  const { writeContract, data: approveHash, isPending } = useWriteContract();

  const { isLoading: isApproving, isSuccess: approvalConfirmed } =
    useWaitForTransactionReceipt({
      hash: approveHash,
    });

  const needsApproval =
    currentAllowance !== undefined && currentAllowance < amount;

  function approve() {
    writeContract({
      address: token,
      abi: erc20Abi,
      functionName: "approve",
      args: [spender, amount],
    });
  }

  return {
    needsApproval,
    approve,
    isPending,
    isApproving,
    approvalConfirmed,
    refetchAllowance,
  };
}
```

### SSR / Next.js Integration

wagmi supports server-side rendering but requires careful hydration handling.

```tsx
// config.ts -- shared config with SSR flag
import { http, createConfig, cookieStorage, createStorage } from "wagmi";
import { mainnet, sepolia } from "wagmi/chains";
import { injected } from "wagmi/connectors";

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [injected()],
  // SSR: use cookie storage to persist state across server/client
  ssr: true,
  storage: createStorage({
    storage: cookieStorage,
  }),
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
  },
});
```

```tsx
// providers.tsx -- client component wrapping providers
"use client";

import { WagmiProvider } from "wagmi";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { config } from "./config";
import { useState, type ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  // Create QueryClient inside component to avoid sharing between requests
  const [queryClient] = useState(() => new QueryClient());

  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

```tsx
// layout.tsx -- root layout using the provider
import { Providers } from "./providers";
import { headers } from "next/headers";
import { cookieToInitialState } from "wagmi";
import { config } from "./config";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const headerList = await headers();
  const cookie = headerList.get("cookie");
  // Rehydrate wagmi state from cookies to avoid flash of disconnected state
  const initialState = cookieToInitialState(config, cookie);

  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Watching Contract Events

```tsx
import { useWatchContractEvent } from "wagmi";

const erc20Abi = [
  {
    name: "Transfer",
    type: "event",
    inputs: [
      { name: "from", type: "address", indexed: true },
      { name: "to", type: "address", indexed: true },
      { name: "value", type: "uint256", indexed: false },
    ],
  },
] as const;

function TransferWatcher({ token }: { token: `0x${string}` }) {
  useWatchContractEvent({
    address: token,
    abi: erc20Abi,
    eventName: "Transfer",
    onLogs(logs) {
      for (const log of logs) {
        console.log(
          `Transfer: ${log.args.from} -> ${log.args.to}: ${log.args.value?.toString()}`
        );
      }
    },
    onError(error) {
      console.error("Event watch error:", error.message);
    },
  });

  return null;
}
```

### Multicall (Batched Reads)

```tsx
import { useReadContracts } from "wagmi";

const erc20Abi = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "symbol",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "string" }],
  },
] as const;

const TOKENS: `0x${string}`[] = [
  "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
  "0xdAC17F958D2ee523a2206206994597C13D831ec7", // USDT
  "0x6B175474E89094C44Da98b954EedeAC495271d0F", // DAI
];

function MultiTokenBalances({ account }: { account: `0x${string}` }) {
  const { data, isLoading } = useReadContracts({
    contracts: TOKENS.flatMap((token) => [
      {
        address: token,
        abi: erc20Abi,
        functionName: "symbol" as const,
      },
      {
        address: token,
        abi: erc20Abi,
        functionName: "balanceOf" as const,
        args: [account] as const,
      },
    ]),
  });

  if (isLoading || !data) return <p>Loading balances...</p>;

  return (
    <ul>
      {TOKENS.map((token, i) => {
        const symbolResult = data[i * 2];
        const balanceResult = data[i * 2 + 1];
        const symbol = symbolResult.status === "success" ? symbolResult.result : "???";
        const balance =
          balanceResult.status === "success"
            ? (balanceResult.result as bigint).toString()
            : "Error";

        return (
          <li key={token}>
            {symbol as string}: {balance}
          </li>
        );
      })}
    </ul>
  );
}
```

### Send Native ETH

```tsx
import { useSendTransaction, useWaitForTransactionReceipt } from "wagmi";
import { parseEther } from "viem";

function SendEth() {
  const { sendTransaction, data: hash, isPending, error } = useSendTransaction();
  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  function handleSend(to: `0x${string}`, ethAmount: string) {
    sendTransaction({
      to,
      value: parseEther(ethAmount),
    });
  }

  return (
    <div>
      <button
        onClick={() =>
          handleSend("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "0.01")
        }
        disabled={isPending || isConfirming}
      >
        {isPending ? "Signing..." : isConfirming ? "Confirming..." : "Send 0.01 ETH"}
      </button>
      {isSuccess && <p>Sent! Hash: {hash}</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

### Sign Message / Verify Signature

```tsx
import { useSignMessage, useVerifyMessage } from "wagmi";

function SignAndVerify() {
  const { signMessage, data: signature, isPending } = useSignMessage();

  const { data: isValid } = useVerifyMessage({
    address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    message: "Hello wagmi",
    signature,
  });

  return (
    <div>
      <button
        onClick={() => signMessage({ message: "Hello wagmi" })}
        disabled={isPending}
      >
        Sign Message
      </button>
      {signature && <p>Signature: {signature}</p>}
      {isValid !== undefined && (
        <p>Signature valid: {isValid ? "Yes" : "No"}</p>
      )}
    </div>
  );
}
```

## TanStack Query Integration

wagmi v2 delegates all data fetching, caching, and refetching to TanStack Query. This gives you full control over stale times, refetch intervals, and cache invalidation.

### Custom Query Options

```tsx
import { useReadContract } from "wagmi";

function SlowPollingBalance({
  token,
  account,
}: {
  token: `0x${string}`;
  account: `0x${string}`;
}) {
  const { data } = useReadContract({
    address: token,
    abi: erc20Abi,
    functionName: "balanceOf",
    args: [account],
    query: {
      // Refetch every 30 seconds instead of on every block
      refetchInterval: 30_000,
      // Consider data stale after 10 seconds
      staleTime: 10_000,
      // Keep previous data while refetching
      placeholderData: (previousData: bigint | undefined) => previousData,
    },
  });

  return <span>{data?.toString()}</span>;
}
```

### Manual Cache Invalidation

```tsx
import { useQueryClient } from "@tanstack/react-query";

function InvalidateAfterAction() {
  const queryClient = useQueryClient();

  async function handleAction() {
    // After a write transaction confirms, invalidate all wagmi queries
    // to refresh balances, allowances, etc.
    await queryClient.invalidateQueries();
  }

  return <button onClick={handleAction}>Refresh All Data</button>;
}
```

## Config Reference

### createConfig Options

```typescript
import { http, createConfig, createStorage, cookieStorage } from "wagmi";
import { mainnet, sepolia, arbitrum, base, optimism } from "wagmi/chains";
import {
  injected,
  walletConnect,
  coinbaseWallet,
} from "wagmi/connectors";

export const config = createConfig({
  // Required: at least one chain
  chains: [mainnet, sepolia, arbitrum, base, optimism],

  // Required: one transport per chain
  transports: {
    [mainnet.id]: http("https://eth.llamarpc.com"),
    [sepolia.id]: http(),
    [arbitrum.id]: http(),
    [base.id]: http(),
    [optimism.id]: http(),
  },

  // Optional: wallet connectors
  connectors: [
    injected(),
    walletConnect({
      projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID!,
    }),
    coinbaseWallet({
      appName: "My dApp",
    }),
  ],

  // Optional: enable SSR support
  ssr: true,

  // Optional: custom storage (default is localStorage)
  storage: createStorage({ storage: cookieStorage }),

  // Optional: enable multiInjectedProviderDiscovery (EIP-6963)
  // Automatically detects multiple injected wallets
  multiInjectedProviderDiscovery: true,
});
```

### Connector Configuration

```typescript
import { injected, walletConnect, coinbaseWallet } from "wagmi/connectors";

// Browser extension wallets (MetaMask, Rabby, etc.)
injected({
  // Attempt to connect on page load if previously connected
  shimDisconnect: true,
})

// WalletConnect v2 -- requires a projectId from cloud.walletconnect.com
walletConnect({
  projectId: "YOUR_PROJECT_ID",
  showQrModal: true,
  metadata: {
    name: "My dApp",
    description: "Description",
    url: "https://mydapp.com",
    icons: ["https://mydapp.com/icon.png"],
  },
})

// Coinbase Wallet
coinbaseWallet({
  appName: "My dApp",
  appLogoUrl: "https://mydapp.com/logo.png",
})
```

## Common Patterns

### Conditional Hook Execution

Pass `undefined` to disable a hook until prerequisites are met.

```tsx
import { useReadContract, useAccount } from "wagmi";

function ConditionalRead({ token }: { token: `0x${string}` }) {
  const { address } = useAccount();

  // Only runs when address is defined -- wagmi skips the query when args contain undefined
  const { data } = useReadContract({
    address: token,
    abi: erc20Abi,
    functionName: "balanceOf",
    args: address ? [address] : undefined,
    query: {
      enabled: !!address,
    },
  });

  return <span>{data?.toString() ?? "Connect wallet"}</span>;
}
```

### Error Handling for Transactions

```tsx
import { useWriteContract, useWaitForTransactionReceipt } from "wagmi";
import { BaseError, ContractFunctionRevertedError } from "viem";

function WriteWithErrorHandling() {
  const { writeContract, data: hash, error: writeError } = useWriteContract();
  const { error: receiptError, data: receipt } = useWaitForTransactionReceipt({
    hash,
  });

  function extractError(error: Error | null): string | null {
    if (!error) return null;

    if (error instanceof BaseError) {
      const revert = error.walk(
        (e) => e instanceof ContractFunctionRevertedError
      );
      if (revert instanceof ContractFunctionRevertedError) {
        return revert.data?.errorName ?? revert.reason ?? "Unknown revert";
      }
      return error.shortMessage;
    }

    return error.message;
  }

  // Check receipt status for on-chain reverts
  const isReverted = receipt?.status === "reverted";

  return (
    <div>
      {writeError && <p>Write error: {extractError(writeError)}</p>}
      {receiptError && <p>Receipt error: {extractError(receiptError)}</p>}
      {isReverted && <p>Transaction reverted on-chain</p>}
    </div>
  );
}
```

## Debugging

### Common Diagnostic Checks

```tsx
import { useAccount, useChainId } from "wagmi";

function DiagnosticsPanel() {
  const { address, isConnected, connector } = useAccount();
  const chainId = useChainId();

  return (
    <pre>
      {JSON.stringify(
        {
          isConnected,
          address,
          chainId,
          connector: connector?.name,
        },
        null,
        2
      )}
    </pre>
  );
}
```

### React DevTools Integration

wagmi queries show up in TanStack Query DevTools. Install for inspection:

```bash
npm install @tanstack/react-query-devtools
```

```tsx
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

function App({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

## References

- wagmi docs: https://wagmi.sh
- wagmi v2 migration guide: https://wagmi.sh/react/guides/migrate-from-v1-to-v2
- TanStack Query: https://tanstack.com/query
- viem docs: https://viem.sh
- WalletConnect Cloud (for projectId): https://cloud.walletconnect.com
- EIP-6963 (multi-injected provider): https://eips.ethereum.org/EIPS/eip-6963
