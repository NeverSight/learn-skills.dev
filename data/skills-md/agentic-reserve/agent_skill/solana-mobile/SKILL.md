---
name: solana-mobile
description: Solana Mobile development with Mobile Wallet Adapter (MWA), Seeker device integration, SeedVault secure storage, and React Native dApp patterns for building mobile-first Solana applications.
user-invocable: true
---

# Solana Mobile Development Skill

Expert knowledge for building mobile dApps on Solana with Mobile Wallet Adapter, Seeker device integration, and SeedVault support.

---

## Overview

This skill provides comprehensive guidance for developing mobile applications on the Solana blockchain, with focus on:

- **Mobile Wallet Adapter (MWA)** - Protocol for connecting mobile dApps to wallets
- **Solana Mobile Seeker** - Detecting and optimizing for Seeker devices
- **SeedVault** - Secure key storage on Solana Mobile devices
- **React Native Integration** - Building cross-platform mobile dApps
- **dApp Store Publishing** - Submitting apps to Solana dApp Store

---

## When to Use This Skill

Activate this skill when:
- Building React Native dApps for Solana
- Implementing Mobile Wallet Adapter
- Detecting Solana Mobile Seeker users
- Integrating with SeedVault for secure key storage
- Publishing to Solana dApp Store
- Optimizing mobile user experience
- Implementing Sign-In With Solana (SIWS)

---

## Core Concepts

### Mobile Wallet Adapter (MWA)

MWA is a protocol that enables secure communication between mobile dApps and wallet apps.

**Key Features:**
- Secure WebSocket-based communication
- Session-based authorization
- Transaction signing
- Message signing
- Multi-wallet support

**Protocol Flow:**
1. **Association** - Establish connection via URI scheme
2. **Session Establishment** - ECDH key exchange
3. **Authorization** - Request wallet access
4. **Privileged Methods** - Sign transactions/messages

### Solana Mobile Seeker

Seeker is Solana's flagship mobile device with built-in crypto features.

**Detection Methods:**
1. **Platform Constants** (Client-side, spoofable)
2. **Genesis Token Verification** (On-chain, guaranteed)

**Seeker Features:**
- SeedVault secure storage
- Optimized Solana performance
- Seeker Genesis Token (SGT)
- Native dApp Store integration

### SeedVault

Secure enclave for storing private keys on Solana Mobile devices.

**Benefits:**
- Hardware-backed security
- Biometric authentication
- Secure key derivation
- Isolated from app memory

---

## Implementation Patterns

### 1. Mobile Wallet Adapter Setup

#### Install Dependencies

```bash
npm install @solana-mobile/mobile-wallet-adapter-protocol \
  @solana-mobile/mobile-wallet-adapter-protocol-web3js \
  @solana/web3.js \
  react-native-quick-crypto
```

#### Configure Polyfills

Create `polyfill.js`:

```javascript
import { install } from 'react-native-quick-crypto';
install();
```

Create `index.js`:

```javascript
import './polyfill';
import 'expo-router/entry';
```

Update `package.json`:

```json
{
  "main": "./index.js"
}
```

#### MWA Provider Setup

```typescript
import {
  ConnectionProvider,
  RPC_ENDPOINT,
} from '@solana/web3.js';
import {
  SolanaMobileWalletAdapter,
} from '@solana-mobile/mobile-wallet-adapter-protocol-web3js';

export function MobileWalletProvider({ children }) {
  return (
    <ConnectionProvider endpoint={RPC_ENDPOINT}>
      <SolanaMobileWalletAdapter
        cluster="mainnet-beta"
        appIdentity={{
          name: 'Your dApp',
          uri: 'https://yourdapp.com',
          icon: 'favicon.ico',
        }}
      >
        {children}
      </SolanaMobileWalletAdapter>
    </ConnectionProvider>
  );
}
```

### 2. Authorization Flow

```typescript
import { transact } from '@solana-mobile/mobile-wallet-adapter-protocol-web3js';

async function authorizeWallet() {
  const result = await transact(async (wallet) => {
    const authResult = await wallet.authorize({
      cluster: 'solana:mainnet',
      identity: {
        name: 'Obscura DEX',
        uri: 'https://obscura.finance',
        icon: 'icon.png',
      },
      features: [
        'solana:signMessages',
        'solana:signAndSendTransaction',
      ],
    });

    return {
      accounts: authResult.accounts,
      authToken: authResult.auth_token,
      walletUriBase: authResult.wallet_uri_base,
    };
  });

  return result;
}
```

### 3. Sign and Send Transaction

```typescript
import { Transaction } from '@solana/web3.js';
import { transact } from '@solana-mobile/mobile-wallet-adapter-protocol-web3js';

async function signAndSendTransaction(transaction: Transaction) {
  const result = await transact(async (wallet) => {
    // Authorize if needed
    const authResult = await wallet.authorize({
      cluster: 'solana:mainnet',
      identity: APP_IDENTITY,
    });

    // Get latest blockhash
    const { blockhash } = await connection.getLatestBlockhash();
    transaction.recentBlockhash = blockhash;
    transaction.feePayer = authResult.accounts[0].publicKey;

    // Sign and send
    const signedTxs = await wallet.signAndSendTransactions({
      transactions: [transaction],
    });

    return signedTxs[0];
  });

  return result;
}
```

### 4. Sign Message

```typescript
async function signMessage(message: string) {
  const result = await transact(async (wallet) => {
    const authResult = await wallet.authorize({
      cluster: 'solana:mainnet',
      identity: APP_IDENTITY,
    });

    const encodedMessage = new TextEncoder().encode(message);
    
    const signedMessages = await wallet.signMessages({
      addresses: [authResult.accounts[0].address],
      payloads: [encodedMessage],
    });

    return {
      signature: signedMessages.signed_payloads[0],
      address: authResult.accounts[0].address,
    };
  });

  return result;
}
```

### 5. Seeker Detection (Platform Constants)

```typescript
import { Platform } from 'react-native';

function isSeekerDevice(): boolean {
  return Platform.constants?.Model === 'Seeker';
}

function getSeekerInfo() {
  if (!isSeekerDevice()) {
    return null;
  }

  return {
    model: Platform.constants.Model,
    brand: Platform.constants.Brand,
    manufacturer: Platform.constants.Manufacturer,
    fingerprint: Platform.constants.Fingerprint,
  };
}

// Usage
if (isSeekerDevice()) {
  console.log('Running on Seeker device!');
  // Show Seeker-specific UI
}
```

### 6. Seeker Genesis Token Verification

#### Client-Side: Sign-In With Solana (SIWS)

```typescript
async function signInWithSolana() {
  const result = await transact(async (wallet) => {
    const authResult = await wallet.authorize({
      cluster: 'solana:mainnet',
      identity: APP_IDENTITY,
      sign_in_payload: {
        domain: 'obscura.finance',
        statement: 'Sign in to verify Seeker ownership',
        uri: 'https://obscura.finance',
        version: '1',
        chainId: 'solana:mainnet',
        nonce: generateNonce(),
        issuedAt: new Date().toISOString(),
      },
    });

    return {
      walletAddress: authResult.accounts[0].address,
      signInResult: authResult.sign_in_result,
    };
  });

  // Send to backend for verification
  const isVerified = await verifyOnBackend(result);
  return isVerified;
}
```

#### Server-Side: Verify SIWS + Check SGT

```typescript
import { verifySignIn } from '@solana/wallet-standard-util';
import { Connection, PublicKey } from '@solana/web3.js';

// Step 1: Verify SIWS signature
async function verifySIWS(signInPayload, signInResult): Promise<boolean> {
  const serializedOutput = {
    account: {
      publicKey: new Uint8Array(signInResult.account.publicKey),
      ...signInResult.account,
    },
    signature: new Uint8Array(signInResult.signature),
    signedMessage: new Uint8Array(signInResult.signedMessage),
  };
  
  return verifySignIn(signInPayload, serializedOutput);
}

// Step 2: Check for Seeker Genesis Token
async function checkSeekerGenesisToken(
  walletAddress: string,
  heliusApiKey: string
): Promise<boolean> {
  const response = await fetch(
    `https://api.helius.xyz/v0/addresses/${walletAddress}/balances?api-key=${heliusApiKey}`
  );
  
  const data = await response.json();
  
  // Check for Seeker Genesis Token
  // SGT Collection: https://solscan.io/collection/...
  const hasSGT = data.tokens?.some(
    (token) => token.mint === 'SEEKER_GENESIS_TOKEN_MINT'
  );
  
  return hasSGT;
}

// Step 3: Combined verification
async function verifySeekerUser(signInResult, heliusApiKey): Promise<boolean> {
  // Verify SIWS signature
  const siwsVerified = await verifySIWS(
    signInResult.payload,
    signInResult.result
  );
  
  if (!siwsVerified) {
    return false;
  }
  
  // Check SGT ownership
  const hasSGT = await checkSeekerGenesisToken(
    signInResult.walletAddress,
    heliusApiKey
  );
  
  return hasSGT;
}
```

### 7. SeedVault Integration

```typescript
// SeedVault is automatically used by MWA-compatible wallets
// No additional code needed - keys are stored securely

// To leverage SeedVault features:
async function requestBiometricAuth() {
  // Wallet apps handle biometric auth automatically
  // when accessing SeedVault keys
  
  const result = await transact(async (wallet) => {
    // This will trigger biometric prompt if enabled
    const authResult = await wallet.authorize({
      cluster: 'solana:mainnet',
      identity: APP_IDENTITY,
    });
    
    return authResult;
  });
  
  return result;
}
```

### 8. Reauthorization (Persistent Sessions)

```typescript
// Store auth token securely
import AsyncStorage from '@react-native-async-storage/async-storage';

async function saveAuthToken(authToken: string) {
  await AsyncStorage.setItem('mwa_auth_token', authToken);
}

async function getAuthToken(): Promise<string | null> {
  return await AsyncStorage.getItem('mwa_auth_token');
}

// Reauthorize with stored token
async function reauthorize() {
  const authToken = await getAuthToken();
  
  if (!authToken) {
    return authorizeWallet(); // First time auth
  }
  
  try {
    const result = await transact(async (wallet) => {
      const authResult = await wallet.authorize({
        cluster: 'solana:mainnet',
        identity: APP_IDENTITY,
        auth_token: authToken, // Reuse token
      });
      
      // Save new token if updated
      await saveAuthToken(authResult.auth_token);
      
      return authResult;
    });
    
    return result;
  } catch (error) {
    // Token expired, request new auth
    await AsyncStorage.removeItem('mwa_auth_token');
    return authorizeWallet();
  }
}
```

---

## Best Practices

### Security

1. **Never Request Private Keys**
   - Always use MWA signing methods
   - Never ask users for seed phrases
   - Trust wallet apps for key management

2. **Verify Signatures**
   - Always verify SIWS signatures on backend
   - Use on-chain verification for critical features
   - Don't trust client-side checks alone

3. **Secure Token Storage**
   - Use AsyncStorage for auth tokens
   - Encrypt sensitive data
   - Clear tokens on logout

### User Experience

1. **Handle Wallet Not Installed**
   ```typescript
   try {
     await transact(async (wallet) => {
       // ... wallet operations
     });
   } catch (error) {
     if (error.message.includes('No wallet found')) {
       // Show wallet installation prompt
       showInstallWalletDialog();
     }
   }
   ```

2. **Loading States**
   ```typescript
   const [isConnecting, setIsConnecting] = useState(false);
   
   async function connect() {
     setIsConnecting(true);
     try {
       await authorizeWallet();
     } finally {
       setIsConnecting(false);
     }
   }
   ```

3. **Error Handling**
   ```typescript
   try {
     await signAndSendTransaction(tx);
   } catch (error) {
     if (error.message.includes('User rejected')) {
       showToast('Transaction cancelled');
     } else if (error.message.includes('Insufficient funds')) {
       showToast('Insufficient SOL balance');
     } else {
       showToast('Transaction failed');
     }
   }
   ```

### Performance

1. **Reuse Connections**
   - Store auth tokens
   - Reauthorize instead of fresh auth
   - Use wallet_uri_base for faster connections

2. **Batch Transactions**
   ```typescript
   await wallet.signAndSendTransactions({
     transactions: [tx1, tx2, tx3], // Batch multiple
   });
   ```

3. **Optimize for Seeker**
   ```typescript
   if (isSeekerDevice()) {
     // Use optimized settings for Seeker
     connection.commitment = 'confirmed'; // Faster
   }
   ```

---

## Common Patterns

### Pattern 1: Connect Button

```typescript
function ConnectWalletButton() {
  const [wallet, setWallet] = useState(null);
  const [loading, setLoading] = useState(false);
  
  async function handleConnect() {
    setLoading(true);
    try {
      const result = await reauthorize();
      setWallet(result.accounts[0]);
    } catch (error) {
      console.error('Connection failed:', error);
    } finally {
      setLoading(false);
    }
  }
  
  if (wallet) {
    return (
      <View>
        <Text>Connected: {wallet.address.slice(0, 8)}...</Text>
      </View>
    );
  }
  
  return (
    <Button
      title={loading ? 'Connecting...' : 'Connect Wallet'}
      onPress={handleConnect}
      disabled={loading}
    />
  );
}
```

### Pattern 2: Seeker-Specific UI

```typescript
function SeekerBanner() {
  const isSeeker = isSeekerDevice();
  const [hasGenesisToken, setHasGenesisToken] = useState(false);
  
  useEffect(() => {
    if (isSeeker) {
      verifyGenesisToken().then(setHasGenesisToken);
    }
  }, [isSeeker]);
  
  if (!isSeeker) return null;
  
  return (
    <View style={styles.seekerBanner}>
      <Text>🎉 Seeker Device Detected!</Text>
      {hasGenesisToken && (
        <Text>✅ Genesis Token Verified</Text>
      )}
    </View>
  );
}
```

### Pattern 3: Transaction with Confirmation

```typescript
async function sendTransactionWithConfirmation(transaction: Transaction) {
  // Sign and send
  const signature = await signAndSendTransaction(transaction);
  
  // Wait for confirmation
  const confirmation = await connection.confirmTransaction(
    signature,
    'confirmed'
  );
  
  if (confirmation.value.err) {
    throw new Error('Transaction failed');
  }
  
  return signature;
}
```

---

## Publishing to dApp Store

### 1. Build APK

```bash
# For Expo
eas build --platform android --profile production

# For React Native
cd android
./gradlew assembleRelease
```

### 2. Sign APK

```bash
# Generate keystore
keytool -genkey -v -keystore my-release-key.keystore \
  -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# Sign APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore my-release-key.keystore \
  app-release-unsigned.apk my-key-alias
```

### 3. Submit to dApp Store

```bash
# Install publishing CLI
npm install -g @solana-mobile/dapp-store-cli

# Login
dapp-store login

# Create app NFT (first time only)
dapp-store create

# Submit release
dapp-store publish \
  --apk ./app-release.apk \
  --requestor-is-authorized \
  --complies-with-solana-dapp-store-policies
```

---

## Troubleshooting

### Issue: Wallet Not Connecting

**Solutions:**
1. Check if wallet app is installed
2. Verify network (devnet/mainnet)
3. Clear app cache
4. Reinstall wallet app

### Issue: Transaction Fails

**Solutions:**
1. Check SOL balance for fees
2. Verify recent blockhash
3. Check transaction size
4. Ensure correct cluster

### Issue: Seeker Not Detected

**Solutions:**
1. Verify Platform.constants.Model
2. Check device fingerprint
3. Use Genesis Token verification
4. Test on actual Seeker device

### Issue: Auth Token Expired

**Solutions:**
1. Clear stored token
2. Request fresh authorization
3. Implement token refresh logic
4. Handle ERROR_AUTHORIZATION_FAILED

---

## Resources

### Documentation
- [Solana Mobile Docs](https://docs.solanamobile.com)
- [MWA Specification](https://solana-mobile.github.io/mobile-wallet-adapter/spec/spec.html)
- [React Native Guide](https://docs.solanamobile.com/get-started/react-native/quickstart)
- [dApp Store Guide](https://docs.solanamobile.com/dapp-store/intro)

### Tools
- [MWA Protocol](https://github.com/solana-mobile/mobile-wallet-adapter)
- [Solana Mobile SDK](https://github.com/solana-mobile/solana-mobile-stack-sdk)
- [dApp Store CLI](https://www.npmjs.com/package/@solana-mobile/dapp-store-cli)

### Example Apps
- [Solana Mobile Sample Apps](https://github.com/solana-mobile/solana-mobile-stack-sdk/tree/main/samples)
- [Anchor Counter dApp](https://github.com/solana-mobile/tutorial-apps/tree/main/AnchorCounterDapp)

---

## Integration with Obscura DEX

### Mobile-Specific Features

1. **Seeker Rewards**
   - Detect Seeker users
   - Offer reduced trading fees
   - Exclusive features for SGT holders

2. **Mobile-Optimized UI**
   - Touch-friendly controls
   - Simplified trading interface
   - Biometric authentication

3. **Push Notifications**
   - Price alerts
   - Order fills
   - Market updates

4. **Offline Capabilities**
   - Cache market data
   - Queue transactions
   - Sync when online

---

**Last Updated**: February 18, 2026
