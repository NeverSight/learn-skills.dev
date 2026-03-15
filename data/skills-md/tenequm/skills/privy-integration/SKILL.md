---
name: privy-integration
description: Integrate Privy authentication and wallet infrastructure into web and mobile apps. Covers React SDK setup (PrivyProvider, hooks, whitelabel auth), embedded wallets (EVM + Solana), smart wallets (ERC-4337), wagmi/viem integration, server-side Node.js SDK (@privy-io/node), token verification, gas sponsorship, external wallet connectors, and transaction signing. Use when building apps with Privy auth, creating embedded wallets, integrating web3 login, setting up wagmi with Privy, verifying Privy tokens on the server, sponsoring gas, or working with Privy's wallet API. Triggers on privy, privy auth, privy wallet, privy embedded wallet, privy login, privy react, privy wagmi, privy solana, privy smart wallet, privy server SDK, privy token verification, @privy-io/react-auth, @privy-io/node, @privy-io/wagmi, PrivyProvider.
metadata:
  version: "0.1.0"
---

# Privy Integration

Privy provides authentication and wallet infrastructure for apps built on crypto rails. Embed self-custodial wallets, authenticate users via email/SMS/socials/passkeys/wallets, and transact on EVM and Solana chains.

Key packages:
- `@privy-io/react-auth` - React SDK (auth + wallets)
- `@privy-io/react-auth/solana` - Solana wallet hooks
- `@privy-io/react-auth/smart-wallets` - Smart wallets (ERC-4337)
- `@privy-io/wagmi` - wagmi v2 connector
- `@privy-io/node` - Server-side SDK (replaces deprecated `@privy-io/server-auth`)

Docs index: `https://docs.privy.io/llms.txt`

## Quick Start (React + Next.js)

### 1. Install

```bash
npm i @privy-io/react-auth
```

### 2. Wrap app with PrivyProvider

```tsx
'use client';
import {PrivyProvider} from '@privy-io/react-auth';

export default function Providers({children}: {children: React.ReactNode}) {
  return (
    <PrivyProvider
      appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID!}
      config={{
        embeddedWallets: {
          ethereum: {createOnLogin: 'users-without-wallets'}
        }
      }}
    >
      {children}
    </PrivyProvider>
  );
}
```

### 3. Check readiness before using hooks

```tsx
import {usePrivy} from '@privy-io/react-auth';

function App() {
  const {ready, authenticated, user} = usePrivy();
  if (!ready) return <div>Loading...</div>;
  // Safe to use Privy hooks now
}
```

### 4. Login (email OTP example)

```tsx
import {useLoginWithEmail} from '@privy-io/react-auth';

function LoginForm() {
  const {sendCode, loginWithCode} = useLoginWithEmail();
  // sendCode({email}) then loginWithCode({code})
}
```

### 5. Send a transaction (EVM)

```tsx
import {useSendTransaction} from '@privy-io/react-auth';

function SendButton() {
  const {sendTransaction} = useSendTransaction();
  return (
    <button onClick={() => sendTransaction({to: '0x...', value: 100000})}>
      Send
    </button>
  );
}
```

## PrivyProvider Config

```tsx
config={{
  // Auth methods enabled for login
  loginMethods: ['email', 'sms', 'wallet', 'google', 'apple', 'twitter',
                 'github', 'discord', 'farcaster', 'telegram', 'passkey'],

  // Embedded wallet creation
  embeddedWallets: {
    ethereum: {createOnLogin: 'users-without-wallets'}, // or 'all-users' | 'off'
    solana: {createOnLogin: 'users-without-wallets'}
  },

  // UI appearance
  appearance: {
    showWalletLoginFirst: false,
    walletChainType: 'ethereum-and-solana', // or 'ethereum-only' | 'solana-only'
    theme: 'light', // or 'dark'
    accentColor: '#6A6FF5',
    logo: 'https://your-logo.png'
  },

  // External wallet connectors (Solana)
  externalWallets: {
    solana: {connectors: toSolanaWalletConnectors()}
  },

  // Solana RPC config (required for embedded wallet UIs)
  solana: {
    rpcs: {
      'solana:mainnet': {
        rpc: createSolanaRpc('https://api.mainnet-beta.solana.com'),
        rpcSubscriptions: createSolanaRpcSubscriptions('wss://api.mainnet-beta.solana.com')
      }
    }
  }
}}
```

## Wagmi Integration

Import `createConfig` and `WagmiProvider` from `@privy-io/wagmi` (NOT from `wagmi`).

```bash
npm i @privy-io/react-auth @privy-io/wagmi wagmi @tanstack/react-query
```

```tsx
import {PrivyProvider} from '@privy-io/react-auth';
import {WagmiProvider, createConfig} from '@privy-io/wagmi';
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';
import {mainnet, base} from 'viem/chains';
import {http} from 'wagmi';

const queryClient = new QueryClient();
const wagmiConfig = createConfig({
  chains: [mainnet, base],
  transports: {[mainnet.id]: http(), [base.id]: http()}
});

// Nesting order: PrivyProvider > QueryClientProvider > WagmiProvider
export default function Providers({children}: {children: React.ReactNode}) {
  return (
    <PrivyProvider appId="your-app-id" config={privyConfig}>
      <QueryClientProvider client={queryClient}>
        <WagmiProvider config={wagmiConfig}>{children}</WagmiProvider>
      </QueryClientProvider>
    </PrivyProvider>
  );
}
```

Use wagmi hooks (useAccount, useSendTransaction, etc.) for read/write actions. Use Privy hooks for wallet connection/creation.

## Server-Side Token Verification

```bash
npm i @privy-io/node
```

```ts
import {PrivyClient} from '@privy-io/node';

const privy = new PrivyClient({
  appId: process.env.PRIVY_APP_ID!,
  appSecret: process.env.PRIVY_APP_SECRET!
});

// Verify access token from Authorization header
const {userId} = await privy.verifyAuthToken(accessToken);
```

## Whitelabel Authentication

All auth flows can be fully whitelabeled with custom UI. Key hooks:

| Hook | Auth method |
|------|------------|
| `useLoginWithEmail` | Email OTP (`sendCode`, `loginWithCode`) |
| `useLoginWithSms` | SMS OTP |
| `useLoginWithOAuth` | Social logins (`initOAuth({provider: 'google'})`) |
| `useLoginWithPasskey` | Passkeys |
| `useSignupWithPasskey` | Passkey signup |
| `useLoginWithTelegram` | Telegram |
| `useLogin` | General login with callbacks |

## Reference Docs

Read the appropriate reference file for detailed integration guides:

- **[references/react-sdk.md](references/react-sdk.md)** - All React hooks, PrivyProvider config, wagmi/viem setup, appearance config, whitelabel patterns, wallet UI components
- **[references/server-sdk.md](references/server-sdk.md)** - Node.js SDK (`@privy-io/node`), token types and verification, user management API, REST API, webhooks
- **[references/wallets.md](references/wallets.md)** - Embedded wallets (EVM + Solana), smart wallets (ERC-4337), gas sponsorship, external connectors, policies and controls, funding, wallet export
- **[references/solana.md](references/solana.md)** - Solana-specific setup, connectors, @solana/kit and @solana/web3.js integration, transaction signing, gas sponsorship via fee payer

## Key Documentation URLs

| Topic | URL |
|-------|-----|
| Full docs index (LLM-friendly) | https://docs.privy.io/llms.txt |
| React setup | https://docs.privy.io/basics/react/setup |
| React quickstart | https://docs.privy.io/basics/react/quickstart |
| Auth overview | https://docs.privy.io/authentication/overview |
| Whitelabel auth | https://docs.privy.io/authentication/user-authentication/whitelabel |
| Tokens (access/refresh/identity) | https://docs.privy.io/authentication/user-authentication/tokens |
| Wallets overview | https://docs.privy.io/wallets/overview |
| Wagmi integration | https://docs.privy.io/wallets/connectors/ethereum/integrations/wagmi |
| Viem integration | https://docs.privy.io/wallets/connectors/ethereum/integrations/viem |
| Smart wallets | https://docs.privy.io/wallets/using-wallets/evm-smart-wallets/overview |
| Smart wallets SDK config | https://docs.privy.io/wallets/using-wallets/evm-smart-wallets/setup/configuring-sdk |
| Gas sponsorship | https://docs.privy.io/wallets/gas-and-asset-management/gas/overview |
| Gas on Ethereum | https://docs.privy.io/wallets/gas-and-asset-management/gas/ethereum |
| Gas on Solana | https://docs.privy.io/wallets/gas-and-asset-management/gas/solana |
| Node.js SDK quickstart | https://docs.privy.io/basics/nodeJS/quickstart |
| Solana recipe | https://docs.privy.io/recipes/solana/getting-started-with-privy-and-solana |
| Connectors overview | https://docs.privy.io/wallets/connectors/overview |
| Custom auth provider | https://docs.privy.io/authentication/user-authentication/custom-auth |
| Webhooks | https://docs.privy.io/wallets/webhooks/overview |
