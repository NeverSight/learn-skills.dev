---
name: genesis-token
description: Verify Seeker device ownership using Seeker Genesis Token (SGT) verification. Use when the user wants to gate content to Seeker owners, verify device ownership, implement anti-Sybil measures, or distribute device-specific rewards.
---

# Seeker Genesis Token Verification

Verify that a user owns a Seeker device by confirming they possess the Seeker Genesis Token (SGT) — a unique NFT minted once per Seeker device.

## When to Use

- Gate exclusive content to verified Seeker owners
- Distribute device-specific rewards
- Implement anti-Sybil protections (prevent duplicate claims)
- Verify authentic Seeker device ownership

## Prerequisites

- MWA setup complete (user can connect wallet)
- Backend server for verification (SGT check must be server-side)
- Helius API key for RPC queries

## Two-Step Verification Process

1. **SIWS to prove wallet ownership** — Use Sign-in-with-Solana to prove the user owns the wallet
2. **Check wallet contains SGT** — Verify the wallet contains a Seeker Genesis Token

## Implementation

### Step 1: Client - Sign SIWS Payload

```typescript
import { transact } from '@solana-mobile/mobile-wallet-adapter-protocol-web3js';

const APP_IDENTITY = {
  name: 'Your React Native dApp',
  uri: 'https://yourdapp.com',
  icon: 'favicon.ico',
};

async function signSIWSPayload() {
  const result = await transact(async (wallet) => {
    const authorizationResult = await wallet.authorize({
      cluster: 'solana:mainnet',
      identity: APP_IDENTITY,
      sign_in_payload: {
        domain: 'yourdapp.com',
        statement: 'Sign in to verify Seeker ownership',
        uri: 'https://yourdapp.com',
      },
    });

    return {
      walletAddress: authorizationResult.accounts[0].address,
      signInResult: authorizationResult.sign_in_result,
    };
  });

  return result;
}
```

### Step 2: Backend - Verify SIWS Signature

```typescript
import { verifySignIn } from '@solana/wallet-standard-util';

async function verifySIWS(signInPayload, signInResult): Promise<boolean> {
  const serialisedOutput = {
    account: {
      publicKey: new Uint8Array(signInResult.account.publicKey),
      ...signInResult.account,
    },
    signature: new Uint8Array(signInResult.signature),
    signedMessage: new Uint8Array(signInResult.signedMessage),
  };

  return verifySignIn(signInPayload, serialisedOutput);
}
```

### Step 3: Backend - Check SGT Ownership

See [references/sgt-verification.md](references/sgt-verification.md) for the complete verification script.

### Step 4: Backend - Combine Both Checks

```typescript
async function verifySeekerUser(signInResult) {
  // Verify SIWS signature
  const siwsVerified = await verifySIWS(signInResult);

  // Check SGT ownership
  const hasSGT = await checkWalletForSGT(signInResult.walletAddress);

  // If both true, user is a verified owner of a Seeker device
  return siwsVerified && hasSGT;
}
```


## Backend Dependencies

```bash
npm install @solana/wallet-standard-util @solana/web3.js @solana/spl-token
```

## External Documentation

- **Detecting Seeker Users**: https://docs.solanamobile.com/react-native/detecting-seeker-users
- **Phantom SIWS Spec**: https://github.com/phantom/sign-in-with-solana
