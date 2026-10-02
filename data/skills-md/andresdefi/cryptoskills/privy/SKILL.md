---
name: privy
description: "Embedded wallet SDK for dApps with social login, email, and passkey auth. Covers React SDK, server-side JWT verification, wallet management, and smart wallet integration. Acquired by Stripe (2025)."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: Frontend
tags:
  - embedded-wallet
  - social-auth
  - privy
  - jwt
  - react
  - wallet-management
  - passkeys
  - waas
  - authentication
---

# Privy

Privy is an embedded wallet and authentication SDK that lets dApps onboard users with email, phone, social logins, passkeys, or existing wallets -- without requiring users to install a browser extension or manage seed phrases. The SDK creates non-custodial embedded wallets using 2-of-3 Shamir Secret Sharing (SSS) with TEE (Trusted Execution Environment) infrastructure. Privy was acquired by Stripe in June 2025, signaling deeper payment-rails integration ahead.

## What You Probably Got Wrong

- **HTTPS is required -- WebCrypto fails silently on HTTP** -- Privy's key sharding relies on the Web Crypto API, which only works in secure contexts. Loading your app over `http://` (except `localhost`) silently fails with no error message. The SDK initializes but wallet operations produce cryptic failures. Always deploy behind HTTPS. On local dev, `localhost` gets a browser exception, but `http://192.168.x.x` does not. The primary threat vector for SSS key sharding is browser malware on the device share. In the 2-of-3 SSS model, compromising ANY 2 shares reconstructs the full private key: device share (browser malware) + Privy share (Privy infrastructure breach) = full key compromise. The recovery share alone cannot reconstruct the key, but it reduces the attack surface to 2 parties instead of 3.

- **Creating a Solana embedded wallet before EVM permanently blocks EVM wallet creation** -- Privy creates embedded wallets lazily after first login. If you call `createWallet({ type: 'solana' })` before the EVM wallet exists, the EVM wallet slot is permanently blocked for that user. Always create the EVM wallet first, or use `createOnLogin: 'all-users'` to auto-create both in the correct order.

- **Farcaster login + `createOnLogin: 'users-without-wallets'` blocks embedded wallet creation** -- Farcaster accounts already have a custody wallet, so Privy treats them as "users with wallets" and skips embedded wallet creation. But the Farcaster custody wallet is not usable in-browser for signing transactions. Use `createOnLogin: 'all-users'` if you support Farcaster login, or manually call `createWallet()` after login.

- **`verifyAuthToken` only works on ACCESS tokens, not identity tokens** -- Privy issues two token types: access tokens (short-lived, for API auth) and identity tokens (contain user profile data). Calling `verifyAuthToken(identityToken)` silently fails or throws a misleading error. For identity tokens, use `getUser({ idToken })` instead. Server-side verification requires your app SECRET (not app ID).

- **v3 Solana peer dep migration is the #1 upgrade failure point** -- Privy v3 dropped `@solana/web3.js` in favor of `@solana/kit`. If you see peer dependency conflicts or runtime errors after upgrading, remove `@solana/web3.js` entirely and install `@solana/kit`. The API surface changed significantly -- `Connection` becomes `createSolanaRpc`, `PublicKey` becomes `address()`.

- **Privy wallets are NOT custodial** -- The private key is split into 3 shares via Shamir Secret Sharing: (1) device share stored in the browser, (2) Privy share stored in TEE infrastructure, (3) recovery share set up by the user. Any 2 of 3 shares reconstruct the key. Privy alone cannot access user funds.

- **Embedded wallets are created AFTER first login, not during** -- The `PrivyProvider` config `createOnLogin` controls this. The wallet does not exist during the login callback. Check for wallet existence after the login flow completes and the `useWallets()` hook updates.

- **`useWallets()` returns ALL connected wallets, not just embedded** -- If a user connects MetaMask AND has a Privy embedded wallet, `useWallets()` returns both. Filter by `wallet.walletClientType === 'privy'` for embedded wallets, or `wallet.walletClientType === 'metamask'` for MetaMask.

- **Privy is NOT RainbowKit** -- Privy is auth-first (email/social login that optionally creates a wallet). RainbowKit is wallet-first (user picks a wallet, then connects). They serve different user journeys. Privy targets web2 users who don't have wallets. RainbowKit targets web3 users who already do.

- **Embedded wallets do NOT persist across browsers or devices** -- The device share is stored in browser local storage. A user logging in on a new device must complete recovery (or re-create a wallet) to access the same embedded wallet. Always prompt users to set up recovery during onboarding.

- **`usePrivy()` returns `authenticated` but wallet might not be ready** -- Authentication and wallet initialization are separate states. After `authenticated === true`, the embedded wallet may still be loading. Check `wallet.ready` from `useWallets()` before attempting any signing or transaction operations.

- **Privy does NOT include WalletConnect by default** -- To support external mobile wallets via WalletConnect, you must install `@privy-io/react-auth` with the WalletConnect connector and provide a WalletConnect project ID in the config. Without this, mobile users with external wallets cannot connect.

## Critical Context

> **Stripe acquisition:** June 2025. Privy is now a Stripe company. The SDK continues under the `@privy-io` npm scope.
> **Current version:** `@privy-io/react-auth` v3.14.1 (last verified March 2026)
> **Security model:** 2-of-3 Shamir Secret Sharing + TEE. Device share (browser), Privy share (TEE infra), recovery share (user-configured).
> **Supported chains:** All EVM chains + Solana. Chain configuration is per-app in the Privy dashboard.

## Auth Methods

Privy supports 15+ authentication methods. Configure in `PrivyProvider` via `loginMethods`.

| Method | Config Key | Notes |
|--------|-----------|-------|
| Email (magic link) | `'email'` | Default. Sends OTP or magic link. |
| Phone (SMS) | `'sms'` | Sends OTP via SMS. |
| Google | `'google'` | OAuth 2.0. Requires Google client ID in dashboard. |
| Apple | `'apple'` | OAuth 2.0. Requires Apple Services ID. |
| Twitter/X | `'twitter'` | OAuth 1.0a. |
| Discord | `'discord'` | OAuth 2.0. |
| GitHub | `'github'` | OAuth 2.0. |
| LinkedIn | `'linkedin'` | OAuth 2.0. |
| Spotify | `'spotify'` | OAuth 2.0. |
| TikTok | `'tiktok'` | OAuth 2.0. |
| Farcaster | `'farcaster'` | Sign-in with Farcaster. Wallet NOT usable in-browser. |
| Passkey | `'passkey'` | WebAuthn. Device-bound. |
| Wallet (external) | `'wallet'` | MetaMask, Coinbase, WalletConnect, etc. |
| Telegram | `'telegram'` | Telegram Login Widget. |
| Custom auth | `'custom'` | Bring your own JWT. |

```typescript
import { PrivyProvider } from "@privy-io/react-auth";

<PrivyProvider
  appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID!}
  config={{
    loginMethods: ["email", "google", "passkey", "wallet"],
  }}
>
  {children}
</PrivyProvider>
```

## React SDK

### Installation

```bash
npm install @privy-io/react-auth
```

### PrivyProvider Setup

Wrap your app with `PrivyProvider` at the root. Must be inside a React tree (not in a Server Component for Next.js App Router).

```tsx
"use client";

import { PrivyProvider } from "@privy-io/react-auth";
import type { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <PrivyProvider
      appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID!}
      config={{
        appearance: {
          theme: "dark",
          accentColor: "#6366f1",
        },
        loginMethods: ["email", "google", "passkey", "wallet"],
        embeddedWallets: {
          createOnLogin: "all-users",
          requireUserPasswordOnCreate: false,
        },
        defaultChain: mainnet,
        supportedChains: [mainnet, base, arbitrum, optimism, polygon],
      }}
    >
      {children}
    </PrivyProvider>
  );
}
```

### usePrivy Hook

The primary hook for authentication state and actions.

```typescript
import { usePrivy } from "@privy-io/react-auth";

function AuthComponent() {
  const {
    ready,           // boolean -- SDK initialized
    authenticated,   // boolean -- user logged in
    user,            // PrivyUser | null -- user object with linked accounts
    login,           // () => void -- opens login modal
    logout,          // () => Promise<void> -- logs out, clears session
    linkEmail,       // () => void -- link email to existing account
    linkGoogle,      // () => void -- link Google to existing account
    linkWallet,      // () => void -- link external wallet
    getAccessToken,  // () => Promise<string | null> -- JWT for API calls
  } = usePrivy();

  if (!ready) return <div>Loading...</div>;

  if (!authenticated) {
    return <button onClick={login}>Log In</button>;
  }

  return (
    <div>
      <p>User ID: {user?.id}</p>
      <button onClick={logout}>Log Out</button>
    </div>
  );
}
```

### useWallets Hook

Returns all connected wallets (embedded + external). Always filter by type.

```typescript
import { useWallets } from "@privy-io/react-auth";

function WalletDisplay() {
  const { ready, wallets } = useWallets();

  if (!ready) return <div>Loading wallets...</div>;

  const embeddedWallet = wallets.find(
    (w) => w.walletClientType === "privy"
  );
  const externalWallets = wallets.filter(
    (w) => w.walletClientType !== "privy"
  );

  return (
    <div>
      {embeddedWallet && (
        <p>Embedded: {embeddedWallet.address}</p>
      )}
      {externalWallets.map((w) => (
        <p key={w.address}>
          {w.walletClientType}: {w.address}
        </p>
      ))}
    </div>
  );
}
```

### useEmbeddedWallet Hook

Direct access to the embedded wallet for creation and management.

```typescript
import {
  useEmbeddedWallet,
  isNotCreated,
  isConnected,
} from "@privy-io/react-auth";

function EmbeddedWalletManager() {
  const wallet = useEmbeddedWallet();

  if (isNotCreated(wallet)) {
    return (
      <button onClick={() => wallet.create()}>
        Create Embedded Wallet
      </button>
    );
  }

  if (!isConnected(wallet)) {
    return <div>Connecting wallet...</div>;
  }

  return <p>Wallet: {wallet.address}</p>;
}
```

## Embedded Wallet Management

### Sign a Message

```typescript
import { useWallets } from "@privy-io/react-auth";

async function signMessage(wallets: ReturnType<typeof useWallets>["wallets"]) {
  const embeddedWallet = wallets.find(
    (w) => w.walletClientType === "privy"
  );
  if (!embeddedWallet) throw new Error("No embedded wallet found");

  const provider = await embeddedWallet.getEthereumProvider();
  const signature = await provider.request({
    method: "personal_sign",
    params: ["Hello from Privy!", embeddedWallet.address],
  });

  return signature;
}
```

### Send a Transaction

```typescript
import { useWallets } from "@privy-io/react-auth";
import { createWalletClient, custom, parseEther } from "viem";
import { base } from "viem/chains";

async function sendTransaction(
  wallets: ReturnType<typeof useWallets>["wallets"]
) {
  const embeddedWallet = wallets.find(
    (w) => w.walletClientType === "privy"
  );
  if (!embeddedWallet) throw new Error("No embedded wallet found");

  await embeddedWallet.switchChain(base.id);

  const provider = await embeddedWallet.getEthereumProvider();
  const walletClient = createWalletClient({
    chain: base,
    transport: custom(provider),
  });

  const [address] = await walletClient.getAddresses();
  const hash = await walletClient.sendTransaction({
    account: address,
    to: "0xRecipient..." as `0x${string}`,
    value: parseEther("0.001"),
  });

  return hash;
}
```

### Export Private Key

Users can export their embedded wallet private key. This is a user-initiated action that requires Privy's export UI.

```typescript
import {
  useEmbeddedWallet,
  isConnected,
} from "@privy-io/react-auth";

function ExportWallet() {
  const wallet = useEmbeddedWallet();

  if (!isConnected(wallet)) return null;

  return (
    <button onClick={() => wallet.export()}>
      Export Private Key
    </button>
  );
}
```

## Server-Side Auth

Privy issues JWTs for authenticated users. Use these to protect your API routes.

### Access Token vs Identity Token

| Token | Purpose | Verification Method | Contains |
|-------|---------|-------------------|----------|
| Access token | API authorization | `privy.verifyAuthToken(token)` | User ID, app ID, expiry |
| Identity token | User profile data | `privy.getUser({ idToken })` | Linked accounts, email, wallet addresses |

### Express Middleware

```typescript
import { PrivyClient } from "@privy-io/server-auth";
import type { Request, Response, NextFunction } from "express";

const privy = new PrivyClient(
  process.env.PRIVY_APP_ID!,
  process.env.PRIVY_APP_SECRET!
);

async function requireAuth(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith("Bearer ")) {
    res.status(401).json({ error: "Missing authorization header" });
    return;
  }

  const token = authHeader.slice(7);

  try {
    const claims = await privy.verifyAuthToken(token);
    req.privyUserId = claims.userId;
    next();
  } catch (error) {
    res.status(401).json({ error: "Invalid or expired token" });
    return;
  }
}
```

### Client-Side: Sending the Token

```typescript
import { usePrivy } from "@privy-io/react-auth";

async function fetchProtectedData() {
  const { getAccessToken } = usePrivy();
  const token = await getAccessToken();

  const response = await fetch("/api/protected", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.json();
}
```

### Getting User Profile (Identity Token)

Use `getUser({ idToken })` for identity tokens (NOT `verifyAuthToken`).

```typescript
const user = await privy.getUser({ idToken });
// user.email?.address, user.wallet?.address, user.linkedAccounts
```

## Cross-Chain Support

Privy embedded wallets support both EVM and Solana from the same authenticated user session.

### EVM Chain Switching

```typescript
const embeddedWallet = wallets.find(
  (w) => w.walletClientType === "privy"
);

// Switch to Arbitrum
await embeddedWallet.switchChain(42161);

// Switch to Base
await embeddedWallet.switchChain(8453);
```

### Solana Embedded Wallet

```typescript
import { useWallets } from "@privy-io/react-auth";

function SolanaWallet() {
  const { wallets } = useWallets();

  const solanaWallet = wallets.find(
    (w) => w.walletClientType === "privy" && w.chainType === "solana"
  );

  if (!solanaWallet) return null;

  return <p>Solana address: {solanaWallet.address}</p>;
}
```

## Smart Wallet Integration

### Privy + Safe (Account Abstraction)

Privy embedded wallets can serve as the signer/owner for a Safe smart account, enabling gas sponsorship and batched transactions.

```typescript
import { PrivyProvider } from "@privy-io/react-auth";

<PrivyProvider
  appId={process.env.NEXT_PUBLIC_PRIVY_APP_ID!}
  config={{
    embeddedWallets: {
      createOnLogin: "all-users",
    },
    // Privy's built-in smart wallet support uses Safe under the hood
    smartWallets: {
      enabled: true,
    },
  }}
>
  {children}
</PrivyProvider>
```

### Using Smart Wallets

When smart wallets are enabled, Privy creates a Safe smart account with the embedded wallet as the owner. The smart wallet address is different from the embedded wallet address.

```typescript
import { useWallets } from "@privy-io/react-auth";

function SmartWalletInfo() {
  const { wallets } = useWallets();

  const smartWallet = wallets.find(
    (w) => w.walletClientType === "privy_smart_wallet"
  );
  const embeddedWallet = wallets.find(
    (w) => w.walletClientType === "privy"
  );

  return (
    <div>
      {embeddedWallet && (
        <p>Signer (EOA): {embeddedWallet.address}</p>
      )}
      {smartWallet && (
        <p>Smart Wallet (Safe): {smartWallet.address}</p>
      )}
    </div>
  );
}
```

### Sponsored Transactions with Smart Wallets

Smart wallets enable gas sponsorship through Privy's paymaster. Users pay zero gas.

```typescript
async function sendSponsoredTx(
  smartWallet: ConnectedWallet
) {
  const provider = await smartWallet.getEthereumProvider();
  const walletClient = createWalletClient({
    chain: base,
    transport: custom(provider),
  });

  const [account] = await walletClient.getAddresses();

  // Gas is sponsored by the paymaster -- user pays nothing
  const hash = await walletClient.sendTransaction({
    account,
    to: "0xRecipient..." as `0x${string}`,
    value: parseEther("0.001"),
  });

  return hash;
}
```

### Privy + ZeroDev

For advanced account abstraction (session keys, custom validators), use ZeroDev's Kernel with Privy as the signer.

```typescript
import { createKernelAccount } from "@zerodev/sdk";
import { signerToEcdsaValidator } from "@zerodev/ecdsa-validator";
import { providerToSmartAccountSigner } from "permissionless";

async function createZeroDevAccount(
  embeddedWallet: ConnectedWallet
) {
  const provider = await embeddedWallet.getEthereumProvider();
  const signer = await providerToSmartAccountSigner(provider);

  const ecdsaValidator = await signerToEcdsaValidator(publicClient, {
    signer,
    entryPoint: entryPoint07Address,
  });

  const kernelAccount = await createKernelAccount(publicClient, {
    plugins: { sudo: ecdsaValidator },
    entryPoint: entryPoint07Address,
  });

  return kernelAccount;
}
```

## Custom UI / Headless Mode

Privy provides a default login modal, but you can build fully custom UI using headless hooks.

Each auth method has a headless hook: `useLoginWithEmail` (sendCode/loginWithCode flow), `useLoginWithOAuth` (initOAuth with provider), `useLoginWithPasskey`, `useLoginWithWallet`, `useLoginWithFarcaster`, and `useLoginWithCustomAuth`. Each hook exposes a `state` object for tracking the multi-step flow.

```typescript
import { useLoginWithEmail } from "@privy-io/react-auth";

function CustomEmailLogin() {
  const { sendCode, loginWithCode, state } = useLoginWithEmail();

  if (state.status === "awaiting-code-input") {
    return <button onClick={() => loginWithCode({ code })}>Verify</button>;
  }

  return <button onClick={() => sendCode({ email })}>Send Code</button>;
}
```

```typescript
import { useLoginWithOAuth } from "@privy-io/react-auth";

function GoogleLogin() {
  const { initOAuth } = useLoginWithOAuth();
  return (
    <button onClick={() => initOAuth({ provider: "google" })}>
      Continue with Google
    </button>
  );
}
```

## Alternatives Comparison

| Feature | Privy | Dynamic | Web3Auth | Magic |
|---------|-------|---------|----------|-------|
| Auth-first (social login) | Yes | Yes | Yes | Yes |
| Embedded wallets | Yes (SSS + TEE) | Yes (MPC) | Yes (MPC/TSS) | Yes (delegated key) |
| Smart wallet (AA) built-in | Yes (Safe) | Yes | No (BYO) | No |
| Solana support | Yes | Yes | Yes | Limited |
| Passkey support | Yes | Yes | Yes | No |
| Headless mode | Yes | Yes | Yes | Yes |
| Farcaster login | Yes | No | No | No |
| WalletConnect built-in | Opt-in | Yes | Opt-in | No |
| Stripe integration | Native (acquired) | No | No | No |
| Pricing | Free tier + usage | Free tier + usage | Free tier + usage | Free tier + usage |

## Related Skills

- **frontend-ux** -- dApp UX patterns, transaction lifecycle, error handling. Privy handles auth; frontend-ux handles everything after.
- **wagmi** -- React hooks for Ethereum. Privy's embedded wallet provider is compatible with wagmi's `custom` transport.
- **safe** -- Safe smart accounts. Privy's smart wallet mode uses Safe under the hood. See safe skill for multisig patterns.
- **account-abstraction** -- ERC-4337 and EIP-7702 deep dive. Privy's smart wallets build on this infrastructure.

## References

- Privy Documentation: https://docs.privy.io
- Privy React SDK: https://www.npmjs.com/package/@privy-io/react-auth
- Privy Server Auth: https://www.npmjs.com/package/@privy-io/server-auth
- Privy Dashboard: https://dashboard.privy.io
- Privy GitHub: https://github.com/privy-io
- Privy Security Model: https://docs.privy.io/guide/security
- Stripe Acquisition Announcement: https://stripe.com/blog/privy (June 2025)
- Shamir Secret Sharing: https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing
