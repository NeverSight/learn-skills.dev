---
name: web3-dapp
description: Web3 DApp development with Next.js, RainbowKit, wagmi, viem for multi-chain Ethereum applications with NFT, DeFi, and smart contract integration
---

# Web3 DApp Development Guide

> **IMPORTANT**: This is a SKILL file, NOT a project. NEVER run npm/bun install in this folder. NEVER create code files here. When creating a new project, ALWAYS ask the user for the project path first or create it in a separate directory (e.g., `~/Projects/dapp-name`).

This guide provides context when working with Web3 DApp projects using Claude Code.

## MANDATORY REQUIREMENTS

When creating a new Web3 DApp, you MUST include ALL of the following:

### Required Pages (ALWAYS CREATE)

- [ ] `app/page.tsx` - Landing page with hero section and connect wallet CTA
- [ ] `app/dashboard/page.tsx` - Main dashboard showing wallet overview, balances, NFTs
- [ ] `app/nfts/page.tsx` - NFT gallery with grid/list view and metadata display
- [ ] `app/swap/page.tsx` - Token swap interface (if DeFi features requested)
- [ ] `app/staking/page.tsx` - Staking interface (if yield farming requested)
- [ ] `app/collection/[address]/page.tsx` - Individual NFT collection view
- [ ] `app/providers.tsx` - Client-side providers wrapper (wagmi, RainbowKit, QueryClient)

### Required Components (ALWAYS CREATE)

- [ ] `components/connect-button.tsx` - RainbowKit ConnectButton with custom styling
- [ ] `components/wallet-info.tsx` - Display connected wallet address, balance, chain
- [ ] `components/nft-card.tsx` - NFT display card with image, name, collection
- [ ] `components/token-balance.tsx` - ERC20 token balance display
- [ ] `components/loading-spinner.tsx` - Loading state for async operations
- [ ] `components/error-boundary.tsx` - Error handling for Web3 operations
- [ ] `components/chain-selector.tsx` - Network switching dropdown

### Required Hooks (ALWAYS CREATE)

- [ ] `hooks/use-contract.ts` - Smart contract interaction hook with ABI typing
- [ ] `hooks/use-nfts.ts` - NFT fetching hook with metadata caching
- [ ] `hooks/use-token-balance.ts` - ERC20 balance tracking
- [ ] `hooks/use-transaction.ts` - Transaction submission with status tracking

### Required Libraries (ALWAYS INSTALL)

```bash
npm install wagmi viem @rainbow-me/rainbowkit
npm install @tanstack/react-query
npm install lucide-react
npm install tailwindcss @radix-ui/react-*
```

Core libraries:
- `wagmi` - React hooks for Ethereum
- `viem` - TypeScript Ethereum library
- `@rainbow-me/rainbowkit` - Wallet connection UI
- `@tanstack/react-query` - Server state management
- `lucide-react` - Icons
- `tailwindcss` - Styling
- `@radix-ui/react-*` - Headless UI primitives

### RainbowKit Configuration (REQUIRED)

You MUST configure RainbowKit in `app/providers.tsx`:

```tsx
'use client';

import { RainbowKitProvider, getDefaultConfig } from '@rainbow-me/rainbowkit';
import { WagmiProvider } from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import {
  mainnet,
  polygon,
  arbitrum,
  base,
  bsc,
  avalanche,
} from 'wagmi/chains';

const config = getDefaultConfig({
  appName: 'Your DApp Name',
  projectId: 'YOUR_WALLETCONNECT_PROJECT_ID', // Required for WalletConnect
  chains: [mainnet, polygon, arbitrum, base, bsc, avalanche],
  ssr: true,
});

const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>{children}</RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

### WalletConnect Project ID (REQUIRED)

You MUST obtain a WalletConnect Project ID from https://cloud.walletconnect.com:

1. Create a free account
2. Create a new project
3. Copy the Project ID
4. Store in `.env.local`:

```env
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_project_id_here
```

### Supported Chains Configuration (REQUIRED)

Always include these chains in order:

1. **Ethereum** (mainnet) - Primary chain
2. **Polygon** - Low fees, fast transactions
3. **Arbitrum** - L2 scaling
4. **Base** - Coinbase's L2
5. **BSC** - Binance Smart Chain
6. **Avalanche** - Fast finality

```tsx
import { mainnet, polygon, arbitrum, base, bsc, avalanche } from 'wagmi/chains';

const chains = [mainnet, polygon, arbitrum, base, bsc, avalanche] as const;
```

### FORBIDDEN (NEVER USE)

- ❌ `web3.js` - Use viem instead
- ❌ `ethers.js` v5 - Use viem or ethers v6
- ❌ Direct private key storage in frontend
- ❌ Hardcoded RPC URLs without fallback
- ❌ `window.ethereum` direct access - Always use wagmi
- ❌ Storing sensitive data in localStorage
- ❌ Any UI library other than shadcn/ui + Tailwind
- ❌ Server components for Web3 interactions (use 'use client')
- ❌ Mutating state directly in render

### Wagmi Hook Usage (IMPORTANT)

NEVER call wagmi hooks conditionally or inside callbacks. Always at component top level.

❌ WRONG:

```tsx
const handleClick = () => {
  const { address } = useAccount(); // ERROR! Hook inside callback
  // ...
};
```

✅ CORRECT:

```tsx
function MyComponent() {
  const { address, isConnected } = useAccount(); // Top level
  
  const handleClick = () => {
    if (address) {
      // Use address here
    }
  };
  
  return <button onClick={handleClick}>Click</button>;
}
```

### POST-CREATION CLEANUP (ALWAYS DO)

After creating a new Next.js project, you MUST:

1. Remove default Next.js styling and components:

```bash
rm app/globals.css app/page.module.css
rm -rf public/*
```

2. Update `tailwind.config.ts` with custom colors and animations

3. Add RainbowKit CSS import in `app/layout.tsx`:

```tsx
import '@rainbow-me/rainbowkit/styles.css';
```

4. Configure `next.config.js` for static export (optional):

```js
const nextConfig = {
  output: 'export',
  distDir: 'dist',
}
module.exports = nextConfig
```

### AFTER COMPLETING CODE (ALWAYS RUN)

When you finish writing/modifying code, you MUST run these commands:

```bash
npm run build
npm run lint
```

1. `build` ensures no TypeScript or bundling errors
2. `lint` checks code quality

Do NOT skip these steps.

---

## Project Creation

When user asks to create a Web3 DApp, you MUST:

1. FIRST ask for the project name and WalletConnect Project ID:
   - "What is the project name? (e.g., 'nft-marketplace')"
   - "Do you have a WalletConnect Project ID? (Get one free at cloud.walletconnect.com)"

2. Create the project using:

```bash
npx shadcn@latest init --yes --template next --base-color zinc
```

3. Install required dependencies:

```bash
npm install wagmi viem @rainbow-me/rainbowkit @tanstack/react-query lucide-react
```

4. Add shadcn/ui components:

```bash
npx shadcn add button card dialog dropdown-menu input select tabs
```

5. Create `.env.local` with WalletConnect Project ID

6. Set up providers, components, and pages

## Technology Stack

- **Framework**: Next.js 14+ with App Router
- **Web3**: wagmi 2.x, viem 2.x, RainbowKit 2.x
- **Styling**: Tailwind CSS 3.4+
- **UI Components**: shadcn/ui + Radix UI
- **State Management**: TanStack Query (React Query)
- **Icons**: Lucide React
- **Types**: TypeScript (strict mode)

> **WARNING**: DO NOT use class components! Always use functional components with hooks.

> **WARNING**: Web3 interactions MUST be in client components (`'use client'` directive)

## Project Structure

```
project-root/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── layout.tsx                  # Root layout with providers
│   ├── providers.tsx               # Wagmi + RainbowKit providers
│   ├── globals.css                 # Global styles + Tailwind
│   ├── dashboard/
│   │   └── page.tsx                # Dashboard overview
│   ├── nfts/
│   │   └── page.tsx                # NFT gallery
│   ├── swap/
│   │   └── page.tsx                # Token swap
│   ├── staking/
│   │   └── page.tsx                # Staking interface
│   └── collection/
│       └── [address]/
│           └── page.tsx            # Collection details
├── components/
│   ├── ui/                         # shadcn/ui components
│   ├── connect-button.tsx          # Wallet connect button
│   ├── wallet-info.tsx             # Wallet details display
│   ├── nft-card.tsx                # NFT card component
│   ├── nft-grid.tsx                # NFT grid layout
│   ├── token-balance.tsx           # Token balance display
│   ├── chain-selector.tsx          # Network switcher
│   ├── loading-spinner.tsx         # Loading states
│   └── error-boundary.tsx          # Error handling
├── hooks/
│   ├── use-contract.ts             # Contract interactions
│   ├── use-nfts.ts                 # NFT data fetching
│   ├── use-token-balance.ts        # Token balance hook
│   └── use-transaction.ts          # Transaction handling
├── lib/
│   ├── utils.ts                    # Utility functions (cn helper)
│   ├── contracts.ts                # Contract ABIs and addresses
│   └── chains.ts                   # Chain configurations
├── types/
│   ├── nft.ts                      # NFT TypeScript types
│   └── token.ts                    # Token types
├── public/
│   └── images/                     # Static assets
├── .env.local                      # Environment variables
├── next.config.js                  # Next.js config
├── tailwind.config.ts              # Tailwind config
└── tsconfig.json                   # TypeScript config
```

## RainbowKit Integration

### Basic Setup

```tsx
// app/providers.tsx
'use client';

import { RainbowKitProvider, getDefaultConfig } from '@rainbow-me/rainbowkit';
import { WagmiProvider } from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { mainnet, polygon, arbitrum, base, bsc, avalanche } from 'wagmi/chains';

const config = getDefaultConfig({
  appName: 'Web3 DApp',
  projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID!,
  chains: [mainnet, polygon, arbitrum, base, bsc, avalanche],
  ssr: true,
});

const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider>{children}</RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

### Custom Connect Button

```tsx
// components/connect-button.tsx
'use client';

import { ConnectButton } from '@rainbow-me/rainbowkit';
import { Button } from '@/components/ui/button';

export function CustomConnectButton() {
  return (
    <ConnectButton.Custom>
      {({
        account,
        chain,
        openAccountModal,
        openChainModal,
        openConnectModal,
        mounted,
      }) => {
        const ready = mounted;
        const connected = ready && account && chain;

        return (
          <div
            {...(!ready && {
              'aria-hidden': true,
              style: {
                opacity: 0,
                pointerEvents: 'none',
                userSelect: 'none',
              },
            })}
          >
            {(() => {
              if (!connected) {
                return (
                  <Button onClick={openConnectModal}>
                    Connect Wallet
                  </Button>
                );
              }

              if (chain.unsupported) {
                return (
                  <Button onClick={openChainModal} variant="destructive">
                    Wrong Network
                  </Button>
                );
              }

              return (
                <div className="flex gap-2">
                  <Button onClick={openChainModal} variant="outline">
                    {chain.name}
                  </Button>
                  <Button onClick={openAccountModal}>
                    {account.displayName}
                  </Button>
                </div>
              );
            })()}
          </div>
        );
      }}
    </ConnectButton.Custom>
  );
}
```

## Wagmi Hooks Usage

### useAccount - Wallet Connection State

```tsx
import { useAccount, useDisconnect } from 'wagmi';

function WalletStatus() {
  const { address, isConnected, chain } = useAccount();
  const { disconnect } = useDisconnect();

  if (!isConnected) {
    return <div>Not connected</div>;
  }

  return (
    <div>
      <p>Address: {address}</p>
      <p>Chain: {chain?.name}</p>
      <button onClick={() => disconnect()}>Disconnect</button>
    </div>
  );
}
```

### useBalance - Native Token Balance

```tsx
import { useBalance } from 'wagmi';
import { formatEther } from 'viem';

function EthBalance({ address }: { address: `0x${string}` }) {
  const { data, isLoading } = useBalance({ address });

  if (isLoading) return <div>Loading...</div>;
  if (!data) return <div>No balance</div>;

  return (
    <div>
      {formatEther(data.value)} {data.symbol}
    </div>
  );
}
```

### useReadContract - Read Smart Contract

```tsx
import { useReadContract } from 'wagmi';
import { erc721Abi } from 'viem';

function TokenOwner({ 
  contractAddress, 
  tokenId 
}: { 
  contractAddress: `0x${string}`; 
  tokenId: bigint;
}) {
  const { data: owner, isLoading } = useReadContract({
    address: contractAddress,
    abi: erc721Abi,
    functionName: 'ownerOf',
    args: [tokenId],
  });

  if (isLoading) return <div>Loading...</div>;
  
  return <div>Owner: {owner}</div>;
}
```

### useWriteContract - Write to Smart Contract

```tsx
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { parseEther } from 'viem';

function TransferButton({
  contractAddress,
  to,
  amount,
}: {
  contractAddress: `0x${string}`;
  to: `0x${string}`;
  amount: string;
}) {
  const { 
    writeContract, 
    data: hash,
    isPending,
    error 
  } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  const handleTransfer = () => {
    writeContract({
      address: contractAddress,
      abi: erc20Abi,
      functionName: 'transfer',
      args: [to, parseEther(amount)],
    });
  };

  return (
    <div>
      <button 
        onClick={handleTransfer}
        disabled={isPending || isConfirming}
      >
        {isPending ? 'Confirm in wallet...' : 
         isConfirming ? 'Confirming...' : 
         'Transfer'}
      </button>
      {isSuccess && <div>Transaction confirmed!</div>}
      {error && <div>Error: {error.message}</div>}
    </div>
  );
}
```

## NFT Implementation

### NFT Type Definition

```tsx
// types/nft.ts
export interface NFT {
  id: string;
  tokenId: string;
  contractAddress: `0x${string}`;
  name: string;
  description?: string;
  image: string;
  collection?: {
    name: string;
    address: `0x${string}`;
  };
  attributes?: Array<{
    trait_type: string;
    value: string | number;
  }>;
}
```

### NFT Card Component

```tsx
// components/nft-card.tsx
'use client';

import Image from 'next/image';
import { NFT } from '@/types/nft';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

interface NFTCardProps {
  nft: NFT;
  onClick?: (nft: NFT) => void;
}

export function NFTCard({ nft, onClick }: NFTCardProps) {
  return (
    <Card 
      className="overflow-hidden cursor-pointer transition-transform hover:scale-105"
      onClick={() => onClick?.(nft)}
    >
      <div className="aspect-square relative">
        <Image
          src={nft.image}
          alt={nft.name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
      </div>
      <CardHeader className="p-4">
        <h3 className="font-semibold truncate">{nft.name}</h3>
        {nft.collection && (
          <p className="text-sm text-muted-foreground">
            {nft.collection.name}
          </p>
        )}
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <p className="text-xs text-muted-foreground">
          Token ID: {nft.tokenId}
        </p>
      </CardContent>
    </Card>
  );
}
```

### NFT Grid Component

```tsx
// components/nft-grid.tsx
'use client';

import { NFT } from '@/types/nft';
import { NFTCard } from './nft-card';

interface NFTGridProps {
  nfts: NFT[];
  isLoading?: boolean;
  onNFTClick?: (nft: NFT) => void;
}

export function NFTGrid({ nfts, isLoading, onNFTClick }: NFTGridProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div 
            key={i} 
            className="aspect-square bg-muted animate-pulse rounded-lg"
          />
        ))}
      </div>
    );
  }

  if (nfts.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No NFTs found</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {nfts.map((nft) => (
        <NFTCard 
          key={`${nft.contractAddress}-${nft.tokenId}`} 
          nft={nft} 
          onClick={onNFTClick}
        />
      ))}
    </div>
  );
}
```

### useNFTs Hook

```tsx
// hooks/use-nfts.ts
'use client';

import { useAccount } from 'wagmi';
import { useQuery } from '@tanstack/react-query';
import { NFT } from '@/types/nft';

async function fetchNFTs(address: `0x${string}`, chainId: number): Promise<NFT[]> {
  // Use Alchemy, Infura, or OpenSea API
  const response = await fetch(
    `/api/nfts?address=${address}&chainId=${chainId}`
  );
  
  if (!response.ok) {
    throw new Error('Failed to fetch NFTs');
  }
  
  return response.json();
}

export function useNFTs() {
  const { address, chainId } = useAccount();

  return useQuery({
    queryKey: ['nfts', address, chainId],
    queryFn: () => fetchNFTs(address!, chainId!),
    enabled: !!address && !!chainId,
    staleTime: 60000, // 1 minute
  });
}
```

## Token Swap Implementation

### Swap Interface

```tsx
// app/swap/page.tsx
'use client';

import { useState } from 'react';
import { useAccount } from 'wagmi';
import { parseEther, formatEther } from 'viem';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { CustomConnectButton } from '@/components/connect-button';

export default function SwapPage() {
  const { isConnected } = useAccount();
  const [fromToken, setFromToken] = useState('ETH');
  const [toToken, setToToken] = useState('USDC');
  const [fromAmount, setFromAmount] = useState('');

  if (!isConnected) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <h1 className="text-2xl font-bold">Connect Your Wallet</h1>
        <p className="text-muted-foreground">
          Please connect your wallet to swap tokens
        </p>
        <CustomConnectButton />
      </div>
    );
  }

  return (
    <div className="container max-w-md mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Swap Tokens</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">From</label>
            <div className="flex gap-2">
              <Input
                type="number"
                placeholder="0.0"
                value={fromAmount}
                onChange={(e) => setFromAmount(e.target.value)}
              />
              <select 
                value={fromToken}
                onChange={(e) => setFromToken(e.target.value)}
                className="border rounded px-2"
              >
                <option value="ETH">ETH</option>
                <option value="USDC">USDC</option>
                <option value="USDT">USDT</option>
              </select>
            </div>
          </div>

          <div className="flex justify-center">
            <Button variant="outline" size="icon">
              ↓
            </Button>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">To</label>
            <div className="flex gap-2">
              <Input type="number" placeholder="0.0" readOnly />
              <select 
                value={toToken}
                onChange={(e) => setToToken(e.target.value)}
                className="border rounded px-2"
              >
                <option value="USDC">USDC</option>
                <option value="ETH">ETH</option>
                <option value="USDT">USDT</option>
              </select>
            </div>
          </div>

          <Button className="w-full">Swap</Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Smart Contract Integration

### Contract Configuration

```tsx
// lib/contracts.ts
import { erc20Abi, erc721Abi } from 'viem';

export const CONTRACTS = {
  usdc: {
    address: '0xA0b86a33E6441E6C7D3D4B4f6c7e8f9a0B1c2D3e' as `0x${string}`,
    abi: erc20Abi,
  },
  nftCollection: {
    address: '0xB1c2D3e4F5a6B7c8D9e0F1a2B3c4D5e6F7a8B9c0' as `0x${string}`,
    abi: erc721Abi,
  },
} as const;

// Custom contract ABIs
export const stakingAbi = [
  {
    inputs: [{ name: 'amount', type: 'uint256' }],
    name: 'stake',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
  {
    inputs: [],
    name: 'unstake',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
  {
    inputs: [{ name: 'account', type: 'address' }],
    name: 'balanceOf',
    outputs: [{ name: '', type: 'uint256' }],
    stateMutability: 'view',
    type: 'function',
  },
] as const;
```

### useContract Hook

```tsx
// hooks/use-contract.ts
'use client';

import { useReadContract, useWriteContract } from 'wagmi';
import { Abi, Address } from 'viem';

interface UseContractReadProps<TAbi extends Abi> {
  address: Address;
  abi: TAbi;
  functionName: string;
  args?: unknown[];
}

export function useContractRead<TAbi extends Abi>({
  address,
  abi,
  functionName,
  args,
}: UseContractReadProps<TAbi>) {
  return useReadContract({
    address,
    abi,
    functionName,
    args,
  });
}

interface UseContractWriteProps<TAbi extends Abi> {
  address: Address;
  abi: TAbi;
  functionName: string;
}

export function useContractWrite<TAbi extends Abi>({
  address,
  abi,
  functionName,
}: UseContractWriteProps<TAbi>) {
  const { writeContract, ...rest } = useWriteContract();

  return {
    write: (args: unknown[]) =>
      writeContract({
        address,
        abi,
        functionName,
        args,
      }),
    ...rest,
  };
}
```

## Web3 Auth & Token Gating

### NFT Gated Content

```tsx
// components/gated-content.tsx
'use client';

import { useAccount } from 'wagmi';
import { useReadContract } from 'wagmi';
import { erc721Abi } from 'viem';
import { CustomConnectButton } from './connect-button';

interface GatedContentProps {
  nftContract: `0x${string}`;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function GatedContent({ 
  nftContract, 
  children, 
  fallback 
}: GatedContentProps) {
  const { address, isConnected } = useAccount();
  
  const { data: balance, isLoading } = useReadContract({
    address: nftContract,
    abi: erc721Abi,
    functionName: 'balanceOf',
    args: address ? [address] : undefined,
    query: {
      enabled: !!address,
    },
  });

  const hasNFT = balance && balance > 0n;

  if (!isConnected) {
    return (
      <div className="text-center py-8">
        <p className="mb-4">Connect your wallet to access this content</p>
        <CustomConnectButton />
      </div>
    );
  }

  if (isLoading) {
    return <div className="text-center py-8">Checking access...</div>;
  }

  if (!hasNFT) {
    return (
      fallback || (
        <div className="text-center py-8">
          <p>You need to own an NFT to access this content</p>
        </div>
      )
    );
  }

  return <>{children}</>;
}
```

## Staking Implementation

### Staking Interface

```tsx
// app/staking/page.tsx
'use client';

import { useState } from 'react';
import { useAccount } from 'wagmi';
import { parseEther, formatEther } from 'viem';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useContractRead, useContractWrite } from '@/hooks/use-contract';
import { stakingAbi } from '@/lib/contracts';

const STAKING_CONTRACT = '0x...' as `0x${string}`;

export default function StakingPage() {
  const { address } = useAccount();
  const [stakeAmount, setStakeAmount] = useState('');

  const { data: stakedBalance } = useContractRead({
    address: STAKING_CONTRACT,
    abi: stakingAbi,
    functionName: 'balanceOf',
    args: address ? [address] : undefined,
  });

  const { write: stake, isPending: isStaking } = useContractWrite({
    address: STAKING_CONTRACT,
    abi: stakingAbi,
    functionName: 'stake',
  });

  const { write: unstake, isPending: isUnstaking } = useContractWrite({
    address: STAKING_CONTRACT,
    abi: stakingAbi,
    functionName: 'unstake',
  });

  const handleStake = () => {
    if (!stakeAmount) return;
    stake([parseEther(stakeAmount)]);
  };

  return (
    <div className="container max-w-2xl mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Staking</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="p-4 bg-muted rounded-lg">
            <p className="text-sm text-muted-foreground">Your Staked Balance</p>
            <p className="text-2xl font-bold">
              {stakedBalance ? formatEther(stakedBalance) : '0'} ETH
            </p>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Stake Amount</label>
            <div className="flex gap-2">
              <Input
                type="number"
                placeholder="0.0"
                value={stakeAmount}
                onChange={(e) => setStakeAmount(e.target.value)}
              />
              <Button 
                onClick={handleStake}
                disabled={isStaking || !stakeAmount}
              >
                {isStaking ? 'Staking...' : 'Stake'}
              </Button>
            </div>
          </div>

          <Button 
            variant="outline" 
            onClick={() => unstake([])}
            disabled={isUnstaking || !stakedBalance}
            className="w-full"
          >
            {isUnstaking ? 'Unstaking...' : 'Unstake All'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Error Handling

### Web3 Error Boundary

```tsx
// components/web3-error-boundary.tsx
'use client';

import { Component, ReactNode } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class Web3ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Web3 Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Card className="m-4">
          <CardHeader>
            <CardTitle>Something went wrong</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <Button onClick={() => window.location.reload()}>
              Reload Page
            </Button>
          </CardContent>
        </Card>
      );
    }

    return this.props.children;
  }
}
```

## Environment Variables

### Required .env.local

```env
# WalletConnect Project ID (Required)
# Get one free at: https://cloud.walletconnect.com
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_project_id_here

# Optional: Alchemy/Infura API Keys for enhanced data fetching
NEXT_PUBLIC_ALCHEMY_API_KEY=your_alchemy_key
NEXT_PUBLIC_INFURA_API_KEY=your_infura_key

# Optional: Analytics
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
```

## Development Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint

# Type check
npx tsc --noEmit
```

## Testing Checklist

- [ ] Wallet connection works on all supported chains
- [ ] Network switching functions correctly
- [ ] NFT metadata loads and displays properly
- [ ] Token balances update after transactions
- [ ] Transaction states (pending, success, error) display correctly
- [ ] Mobile responsive design works
- [ ] Dark/Light mode toggle functions
- [ ] Error boundaries catch and display errors
- [ ] Loading states are implemented
- [ ] Gas estimation works for write operations

## Security Best Practices

1. **NEVER** store private keys in frontend code
2. **NEVER** expose sensitive API keys in client-side code
3. Always use `use client` directive for Web3 components
4. Validate all user inputs before contract interactions
5. Use type-safe ABIs from viem or generated from verified contracts
6. Implement proper error handling for all async operations
7. Use `parseEther`/`formatEther` for ETH amount conversions
8. Always check `isConnected` before requiring wallet interactions
9. Implement proper loading states to prevent double-submissions
10. Use testnets for development (Goerli, Sepolia, Mumbai)

## Deployment

### Vercel Deployment

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variables in Vercel dashboard
4. Deploy!

### IPFS Deployment (Optional)

```bash
# Build static export
npm run build

# Deploy to IPFS using Pinata or similar
npx pinata-cli upload dist/
```

## After Development

```bash
# Final build check
npm run build

# Run all checks
npm run lint && npx tsc --noEmit

# Test on different networks
# - Local (Hardhat/Anvil)
# - Testnet (Sepolia/Goerli)
# - Mainnet (with caution)
```

> NOTE: Always test thoroughly on testnets before mainnet deployment!

## Common Pitfalls

1. **Missing 'use client'** - Web3 hooks only work in client components
2. **Wrong chain configuration** - Ensure chain IDs match between wagmi and RainbowKit
3. **ABI mismatches** - Use viem's built-in ABIs or verify contract ABIs
4. **Gas estimation failures** - Handle errors when estimating gas
5. **CORS issues** - Configure API endpoints to allow frontend origin
6. **Image loading** - Use Next.js Image component with proper domains config
7. **BigInt serialization** - Convert BigInt to string before JSON operations

## Resources

- [wagmi Documentation](https://wagmi.sh)
- [viem Documentation](https://viem.sh)
- [RainbowKit Documentation](https://rainbowkit.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
