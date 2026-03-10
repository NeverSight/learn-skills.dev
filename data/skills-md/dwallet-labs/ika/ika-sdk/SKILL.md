---
name: ika-sdk
description: Guide for building with the Ika TypeScript SDK (@ika.xyz/sdk) on Mysten Sui v2. Use when creating dWallets, signing cross-chain transactions, managing encryption keys, or integrating with the Ika network from TypeScript/JavaScript. Triggers on tasks involving @ika.xyz/sdk, dWallet operations, IkaClient, IkaTransaction, or Ika cross-chain signing.
---

# Ika TypeScript SDK

Build cross-chain signing applications with `@ika.xyz/sdk` on Sui.

## References (detailed patterns and complete API)

- `references/api-reference.md` - Complete API: IkaClient methods, IkaTransaction methods, cryptography functions, UserShareEncryptionKeys
- `references/flows.md` - End-to-end flows: zero-trust dWallet, shared dWallet, imported key, transfer, future signing
- `references/types-and-validation.md` - Type system, enums, curve/sig/hash validation, state narrowing

## Install

```bash
pnpm add @ika.xyz/sdk
# or
npm install @ika.xyz/sdk
```

Requires: `@mysten/sui` ^2.5.0, Node >=18

## Setup

```typescript
import { getNetworkConfig, IkaClient } from '@ika.xyz/sdk';
import { getJsonRpcFullnodeUrl, SuiJsonRpcClient } from '@mysten/sui/jsonRpc';

const suiClient = new SuiJsonRpcClient({
    url: getJsonRpcFullnodeUrl('testnet'),
    network: 'testnet',
});

const ikaClient = new IkaClient({
    suiClient,
    config: getNetworkConfig('testnet'), // or 'mainnet'
    cache: true,
});
await ikaClient.initialize();
```

## Enums

```typescript
import { Curve, SignatureAlgorithm, Hash } from '@ika.xyz/sdk';

// Curves
Curve.SECP256K1   // Bitcoin, Ethereum
Curve.SECP256R1   // WebAuthn, P-256
Curve.ED25519     // Solana, Substrate
Curve.RISTRETTO   // Privacy

// Signature Algorithms
SignatureAlgorithm.ECDSASecp256k1      // SECP256K1
SignatureAlgorithm.Taproot             // SECP256K1
SignatureAlgorithm.ECDSASecp256r1      // SECP256R1
SignatureAlgorithm.EdDSA               // ED25519
SignatureAlgorithm.SchnorrkelSubstrate // RISTRETTO

// Hashes
Hash.KECCAK256     // ECDSASecp256k1
Hash.SHA256        // ECDSASecp256k1, Taproot, ECDSASecp256r1
Hash.DoubleSHA256  // ECDSASecp256k1
Hash.SHA512        // EdDSA
Hash.Merlin        // SchnorrkelSubstrate
```

## Valid Combinations Quick Reference

| Chain | Curve | SignatureAlgorithm | Hash |
|---|---|---|---|
| Ethereum | SECP256K1 | ECDSASecp256k1 | KECCAK256 |
| Bitcoin Taproot | SECP256K1 | Taproot | SHA256 |
| Bitcoin Legacy | SECP256K1 | ECDSASecp256k1 | DoubleSHA256 |
| Solana | ED25519 | EdDSA | SHA512 |
| WebAuthn | SECP256R1 | ECDSASecp256r1 | SHA256 |
| Substrate | RISTRETTO | SchnorrkelSubstrate | Merlin |

## dWallet Types

| Kind | Description | Use Case |
|---|---|---|
| `zero-trust` | Encrypted user share, user must participate in signing | Personal wallets, max security |
| `shared` | Public user share, network signs autonomously | DAOs, contracts, automation |
| `imported-key` | Existing private key imported (encrypted share) | Migrating existing wallets |
| `imported-key-shared` | Imported key with public share | Migrated wallets for contracts |

## Core Flow: Shared dWallet (Most Common)

### 1. Create Encryption Keys

```typescript
import { UserShareEncryptionKeys, Curve } from '@ika.xyz/sdk';

const keys = await UserShareEncryptionKeys.fromRootSeedKey(
    new TextEncoder().encode('your-seed'),
    Curve.SECP256K1,
);
```

### 2. Register Encryption Key

```typescript
import { IkaTransaction } from '@ika.xyz/sdk';
import { Transaction } from '@mysten/sui/transactions';

const tx = new Transaction();
const ikaTx = new IkaTransaction({ ikaClient, transaction: tx, userShareEncryptionKeys: keys });
await ikaTx.registerEncryptionKey({ curve: Curve.SECP256K1 });
await suiClient.core.signAndExecuteTransaction({ transaction: tx, signer: keypair });
```

### 3. DKG (Create dWallet)

```typescript
import { prepareDKGAsync, createRandomSessionIdentifier } from '@ika.xyz/sdk';

const sessionIdBytes = createRandomSessionIdentifier();
const dkgData = await prepareDKGAsync(ikaClient, Curve.SECP256K1, keys, sessionIdBytes, senderAddress);
const networkKey = await ikaClient.getLatestNetworkEncryptionKey();

const tx = new Transaction();
const ikaTx = new IkaTransaction({ ikaClient, transaction: tx, userShareEncryptionKeys: keys });
const sessionId = ikaTx.registerSessionIdentifier(sessionIdBytes);
const [dwalletCap, signId] = await ikaTx.requestDWalletDKG({
    dkgRequestInput: dkgData,
    ikaCoin: tx.splitCoins(tx.object(ikaCoinId), [1_000_000]),
    suiCoin: tx.splitCoins(tx.gas, [1_000_000]),
    sessionIdentifier: sessionId,
    dwalletNetworkEncryptionKeyId: networkKey.id,
    curve: Curve.SECP256K1,
});
const result = await suiClient.core.signAndExecuteTransaction({ transaction: tx, signer: keypair });
```

### 4. Get dWallet & Public Key

```typescript
import { publicKeyFromDWalletOutput } from '@ika.xyz/sdk';

const dWallet = await ikaClient.getDWalletInParticularState(dwalletId, 'Active');
const publicKey = await publicKeyFromDWalletOutput(Curve.SECP256K1, Uint8Array.from(dWallet.state.Active.public_output));
```

### 5. Request Presign

```typescript
const tx = new Transaction();
const ikaTx = new IkaTransaction({ ikaClient, transaction: tx });
ikaTx.requestGlobalPresign({
    dwalletNetworkEncryptionKeyId: networkKey.id,
    curve: Curve.SECP256K1,
    signatureAlgorithm: SignatureAlgorithm.Taproot,
    ikaCoin: tx.splitCoins(tx.object(ikaCoinId), [1_000_000]),
    suiCoin: tx.splitCoins(tx.gas, [1_000_000]),
});
```

### 6. Sign Message

```typescript
import { createUserSignMessageWithPublicOutput } from '@ika.xyz/sdk';

// Wait for presign completion
const presign = await ikaClient.getPresignInParticularState(presignId, 'Completed');
const pp = await ikaClient.getProtocolPublicParameters(dWallet);

// Create user signature
const msgSig = await createUserSignMessageWithPublicOutput(
    pp, Uint8Array.from(dWallet.state.Active.public_output),
    Uint8Array.from(dWallet.public_user_secret_key_share),
    Uint8Array.from(presign.state.Completed.presign),
    message, Hash.SHA256, SignatureAlgorithm.Taproot, Curve.SECP256K1,
);

// Build & execute sign transaction
const tx = new Transaction();
const ikaTx = new IkaTransaction({ ikaClient, transaction: tx, userShareEncryptionKeys: keys });
const signRef = await ikaTx.requestSign({
    dWallet, messageApproval: ikaTx.approveMessage({
        dWalletCap, curve: Curve.SECP256K1,
        signatureAlgorithm: SignatureAlgorithm.Taproot,
        hashScheme: Hash.SHA256, message,
    }),
    hashScheme: Hash.SHA256,
    verifiedPresignCap: ikaTx.verifyPresignCap({ presign }),
    presign, message,
    signatureScheme: SignatureAlgorithm.Taproot,
    ikaCoin: tx.splitCoins(tx.object(ikaCoinId), [1_000_000]),
    suiCoin: tx.splitCoins(tx.gas, [1_000_000]),
});
```

### 7. Retrieve Signature

```typescript
import { parseSignatureFromSignOutput } from '@ika.xyz/sdk';

const sign = await ikaClient.getSignInParticularState(
    signId, Curve.SECP256K1, SignatureAlgorithm.Taproot, 'Completed',
);
// sign.state.Completed.signature is already parsed
```

## IkaClient Key Methods

```typescript
// Initialization
await ikaClient.initialize();

// Query dWallets
const dWallet = await ikaClient.getDWallet(id);
const dWallet = await ikaClient.getDWalletInParticularState(id, 'Active', { timeout: 60000 });
const dWallets = await ikaClient.getMultipleDWallets([id1, id2]);
const caps = await ikaClient.getOwnedDWalletCaps(address);

// Query presigns, signs, partial sigs (all support InParticularState polling)
const presign = await ikaClient.getPresign(id);
const presign = await ikaClient.getPresignInParticularState(id, 'Completed');
const sign = await ikaClient.getSign(id, Curve.SECP256K1, SignatureAlgorithm.Taproot);
const sign = await ikaClient.getSignInParticularState(id, curve, sigAlgo, 'Completed');

// Encryption keys
const key = await ikaClient.getLatestNetworkEncryptionKey();
const keys = await ikaClient.getAllNetworkEncryptionKeys();

// Protocol parameters
const pp = await ikaClient.getProtocolPublicParameters(dWallet);

// Cache management
ikaClient.invalidateCache();
ikaClient.invalidateObjectCache();
ikaClient.invalidateEncryptionKeyCache();
```

## Polling Options

All `*InParticularState` methods accept:

```typescript
{
    timeout?: number,          // default: 30000ms
    interval?: number,         // default: 1000ms (initial)
    maxInterval?: number,      // default: 5000ms (with backoff)
    backoffMultiplier?: number, // default: 1.5
    signal?: AbortSignal,      // for cancellation
}
```

## UserShareEncryptionKeys

```typescript
// Create from seed
const keys = await UserShareEncryptionKeys.fromRootSeedKey(seed, curve);

// Serialize/deserialize for storage
const bytes = keys.toShareEncryptionKeysBytes();
const restored = UserShareEncryptionKeys.fromShareEncryptionKeysBytes(bytes);

// Properties
keys.getSuiAddress();            // Sui address for registration
keys.getSigningPublicKeyBytes(); // Ed25519 public key bytes
keys.encryptionKey;              // Class-groups public key
keys.decryptionKey;              // Class-groups private key
keys.curve;                      // Curve used

// Operations
await keys.getEncryptionKeySignature();     // Proof of ownership
await keys.getUserOutputSignature(dWallet, userPublicOutput); // Authorize dWallet
await keys.decryptUserShare(dWallet, encShare, pp); // Decrypt secret share
```

## Network Config

```typescript
import { getNetworkConfig } from '@ika.xyz/sdk';

const config = getNetworkConfig('testnet'); // or 'mainnet'
// config.packages.ikaPackage
// config.packages.ikaDwallet2pcMpcPackage
// config.objects.ikaDWalletCoordinator.objectID
// config.objects.ikaSystemObject.objectID
```

## Error Classes

```typescript
import {
    IkaClientError,       // Base error
    ObjectNotFoundError,  // Object not found on chain
    InvalidObjectError,   // Object parsing failed
    NetworkError,         // Network operation failure
    CacheError,           // Caching operation failure
} from '@ika.xyz/sdk';
```

## Low-Level Transaction Builders

For direct Move call construction (bypassing IkaTransaction):

```typescript
import { coordinatorTransactions } from '@ika.xyz/sdk';

// All functions follow: (ikaConfig, coordinatorObjectRef, ...params, tx)
coordinatorTransactions.registerSessionIdentifier(config, coordRef, sessionBytes, tx);
coordinatorTransactions.requestDWalletDKGWithPublicUserSecretKeyShare(config, coordRef, ...params, tx);
coordinatorTransactions.requestGlobalPresign(config, coordRef, ...params, tx);
coordinatorTransactions.requestSignAndReturnId(config, coordRef, ...params, tx);
coordinatorTransactions.approveMessage(config, coordRef, ...params, tx);
// ... etc (50+ functions)
```

## Key Imports Summary

```typescript
// Core
import { IkaClient, IkaTransaction, getNetworkConfig } from '@ika.xyz/sdk';

// Keys
import { UserShareEncryptionKeys } from '@ika.xyz/sdk';

// Cryptography
import {
    prepareDKGAsync, createRandomSessionIdentifier,
    createUserSignMessageWithPublicOutput, publicKeyFromDWalletOutput,
    parseSignatureFromSignOutput, prepareImportedKeyDWalletVerification,
} from '@ika.xyz/sdk';

// Types
import { Curve, SignatureAlgorithm, Hash } from '@ika.xyz/sdk';
import type { DWallet, SharedDWallet, ZeroTrustDWallet, ImportedKeyDWallet } from '@ika.xyz/sdk';
import type { Presign, Sign, EncryptedUserSecretKeyShare } from '@ika.xyz/sdk';
import type { DWalletWithState, PresignWithState, SignWithState } from '@ika.xyz/sdk';

// Validation
import {
    validateHashSignatureCombination, validateCurveSignatureAlgorithm,
    fromCurveToNumber, fromSignatureAlgorithmToNumber, fromHashToNumber,
} from '@ika.xyz/sdk';

// Low-level
import { coordinatorTransactions, systemTransactions } from '@ika.xyz/sdk';
```
