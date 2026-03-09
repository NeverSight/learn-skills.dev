---
name: orderly-api-authentication
description: Complete authentication guide for Orderly Network - EIP-712 wallet signatures for EVM accounts, Ed25519 message signing for Solana accounts, and Ed25519 signatures for API requests
---

# Orderly Network: API Authentication

This skill covers both authentication layers in Orderly Network: **wallet signatures** (EIP-712 for EVM, Ed25519 message signing for Solana) for account registration and key management, and **Ed25519 signatures** for API request authentication.

## When to Use

- Setting up new Orderly accounts and API keys (EVM or Solana)
- Building server-side trading bots
- Implementing direct API calls
- Understanding the two-layer authentication flow
- Debugging signature issues

## Prerequisites

- A Web3 wallet (MetaMask, WalletConnect for EVM; Phantom, Solflare for Solana)
- A Broker ID (e.g., `woofi_dex`, or your own)
- Node.js 18+ installed (for programmatic usage)
- Understanding of EIP-712 typed data signing (EVM) or Ed25519 message signing (Solana) and Ed25519 cryptography

## Authentication Overview

Orderly Network uses a **two-layer authentication system** supporting both EVM and Solana wallets:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Wallet Authentication                             │
│  ─────────────────────────────                              │
│  • Account registration                                     │
│  • API key management (add/remove keys)                     │
│  • Privileged operations (withdrawals, admin)               │
│                                                             │
│  EVM: EIP-712 typed data signing                           │
│  Solana: Ed25519 message signing                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: API Authentication (Ed25519)                      │
│  ─────────────────────────────────────                      │
│  • Trading operations (place/cancel orders)                 │
│  • Reading account data (positions, balances)               │
│  • WebSocket connections                                    │
│                                                             │
│  Signed by: Ed25519 key pair                               │
│  Key type: Locally-generated Ed25519 key pair              │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
1. User connects wallet
2. Wallet signs EIP-712 message to register account
3. Account ID is created
4. User generates Ed25519 key pair
5. Wallet signs EIP-712 message to authorize the Ed25519 key
6. Ed25519 key is used for all subsequent API calls
```

## Environment Configuration

| Environment | API Base URL                      | WebSocket URL                            |
| ----------- | --------------------------------- | ---------------------------------------- |
| Mainnet     | `https://api.orderly.org`         | `wss://ws.orderly.org/ws/stream`         |
| Testnet     | `https://testnet-api.orderly.org` | `wss://testnet-ws.orderly.org/ws/stream` |

**Note**: These API base URLs work for both EVM and Solana wallets. Orderly's API is omnichain - the same endpoints handle both chains.

### Getting Supported Chains

Don't hardcode chain IDs. Fetch them dynamically for your broker:

```typescript
// Get supported chains for your broker
const response = await fetch(`https://api.orderly.org/v1/public/chain_info?broker_id=${BROKER_ID}`);

const { data } = await response.json();
// data.chains contains supported chain_ids
// Use these chain IDs for EIP-712 domain configuration
```

### EIP-712 Domain Configuration

Orderly uses **two different EIP-712 domains** depending on the operation:

| Domain Type   | Use Case                                    | Mainnet                                      | Testnet                                      |
| ------------- | ------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| **Off-chain** | Account registration, API key management    | `0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC` | `0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC` |
| **On-chain**  | Withdrawals, internal transfers, settle PnL | `0x6F7a338F2aA472838dEFD3283eB360d4Dff5D203` | `0x1826B75e2ef249173FC735149AE4B8e9ea10abff` |

> **Important**: The on-chain `verifyingContract` is the **Ledger contract** on Orderly L2. This is a single contract for all chains (not per-chain). Vault contracts exist on each supported EVM chain for deposits, but the Ledger is the source of truth for on-chain operations.

#### Off-Chain Domain (Registration, API Keys)

Used for operations that don't directly interact with smart contracts:

```typescript
const OFFCHAIN_DOMAIN = {
  name: 'Orderly',
  version: '1',
  chainId: 421614, // Connected chain ID (e.g., Arbitrum Sepolia)
  verifyingContract: '0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC',
};
```

#### On-Chain Domain (Withdrawals, Transfers)

Used for operations that interact with the Ledger contract on Orderly L2:

```typescript
const ONCHAIN_DOMAIN = {
  name: 'Orderly',
  version: '1',
  chainId: 42161, // Connected chain ID
  verifyingContract: isTestnet
    ? '0x1826B75e2ef249173FC735149AE4B8e9ea10abff'
    : '0x6F7a338F2aA472838dEFD3283eB360d4Dff5D203',
};
```

---

# Part 1: EIP-712 Wallet Authentication

Wallet authentication is required for account-level operations that need proof of ownership.

## When to Use EIP-712

- **Account Registration**: Creating a new Orderly account
- **API Key Management**: Adding or removing Ed25519 API keys
- **Withdrawals**: Requesting token withdrawals from the vault
- **Admin Operations**: Setting IP restrictions, managing account settings

## Account Registration

### Step 1: Check Existing Account

Before registration, verify if the wallet already has an account:

```typescript
const BROKER_ID = 'woofi_dex'; // Your broker ID
const walletAddress = '0x...'; // User's wallet address

const response = await fetch(
  `https://testnet-api.orderly.org/v1/get_account?broker_id=${BROKER_ID}&user_address=${walletAddress}`
);

const data = await response.json();
// If data.success is true, account already exists
// If not, proceed with registration
```

### Step 2: Fetch Registration Nonce

Retrieve a unique nonce required for registration (valid for 2 minutes):

```typescript
const nonceResponse = await fetch('https://testnet-api.orderly.org/v1/registration_nonce');
const { data: nonce } = await nonceResponse.json();
console.log('Registration nonce:', nonce);
```

### Step 3: Sign Registration Message

Create and sign an EIP-712 typed message:

```typescript
// Registration Message Type
const REGISTRATION_TYPES = {
  Registration: [
    { name: 'brokerId', type: 'string' },
    { name: 'chainId', type: 'uint256' },
    { name: 'timestamp', type: 'uint64' },
    { name: 'registrationNonce', type: 'uint256' },
  ],
};

// Create the message
const registerMessage = {
  brokerId: BROKER_ID,
  chainId: 421614,
  timestamp: Date.now(),
  registrationNonce: nonce,
};

// Sign with wallet (e.g., MetaMask) - Use OFFCHAIN_DOMAIN for registration
const signature = await window.ethereum.request({
  method: 'eth_signTypedData_v4',
  params: [
    walletAddress,
    {
      types: REGISTRATION_TYPES,
      domain: OFFCHAIN_DOMAIN,
      message: registerMessage,
      primaryType: 'Registration',
    },
  ],
});
```

### Step 4: Submit Registration

Send the signed payload to create the Orderly Account ID:

```typescript
const registerResponse = await fetch('https://testnet-api.orderly.org/v1/register_account', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: registerMessage,
    signature: signature,
    userAddress: walletAddress,
  }),
});

const result = await registerResponse.json();
console.log('Account ID:', result.data.account_id);
// Store this account ID - you'll need it for API authentication
```

## API Key Management (Orderly Key)

Once you have an account, you need to register Ed25519 keys for API access.

### Generate Ed25519 Key Pair

```typescript
import { getPublicKeyAsync, utils } from '@noble/ed25519';

// Generate 32-byte private key (cryptographically secure)
const privateKey = utils.randomPrivateKey();

// Derive public key
const publicKey = await getPublicKeyAsync(privateKey);

// Encode public key as base58 (required by Orderly)
function encodeBase58(bytes: Uint8Array): string {
  const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  let result = '';
  let num = 0n;
  for (const byte of bytes) {
    num = num * 256n + BigInt(byte);
  }
  while (num > 0n) {
    result = ALPHABET[Number(num % 58n)] + result;
    num = num / 58n;
  }
  return result;
}

const orderlyKey = `ed25519:${encodeBase58(publicKey)}`;

// Convert bytes to hex string for storage
function bytesToHex(bytes: Uint8Array): string {
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

console.log('Orderly Key:', orderlyKey);
console.log('Private Key (hex):', bytesToHex(privateKey));
// STORE PRIVATE KEY SECURELY - NEVER SHARE IT
```

### Sign Add Orderly Key Message

Associate the Ed25519 key with your account via EIP-712:

```typescript
const ADD_KEY_TYPES = {
  AddOrderlyKey: [
    { name: 'brokerId', type: 'string' },
    { name: 'chainId', type: 'uint256' },
    { name: 'orderlyKey', type: 'string' },
    { name: 'scope', type: 'string' },
    { name: 'timestamp', type: 'uint64' },
    { name: 'expiration', type: 'uint64' },
  ],
};

const addKeyMessage = {
  brokerId: BROKER_ID,
  chainId: 421614,
  orderlyKey: orderlyKey,
  scope: 'read,trading', // Permissions: read, trading, asset (comma-separated)
  timestamp: Date.now(),
  expiration: Date.now() + 31536000000, // 1 year from now
};

// Use OFFCHAIN_DOMAIN for API key management
const addKeySignature = await window.ethereum.request({
  method: 'eth_signTypedData_v4',
  params: [
    walletAddress,
    {
      types: ADD_KEY_TYPES,
      domain: OFFCHAIN_DOMAIN,
      message: addKeyMessage,
      primaryType: 'AddOrderlyKey',
    },
  ],
});
```

### Submit Orderly Key

Register the API key:

```typescript
const keyResponse = await fetch('https://testnet-api.orderly.org/v1/orderly_key', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: addKeyMessage,
    signature: addKeySignature,
    userAddress: walletAddress,
  }),
});

const keyResult = await keyResponse.json();
console.log('Key registered:', keyResult.success);
```

### Orderly Key Scopes

When registering an API key, specify permissions:

| Scope     | Permissions                          |
| --------- | ------------------------------------ |
| `read`    | Read positions, orders, balance      |
| `trading` | Place, cancel, modify orders         |
| `asset`   | Deposit, withdraw, internal transfer |

Multiple scopes can be combined comma-separated: `'read,trading,asset'`

### Remove Orderly Key

To remove a key (requires Ed25519 authentication with another valid key):

```typescript
// POST /v1/client/remove_orderly_key
const removeResponse = await signAndSendRequest(
  accountId,
  privateKey, // Must be a different valid key
  'https://api.orderly.org/v1/client/remove_orderly_key',
  {
    method: 'POST',
    body: JSON.stringify({
      orderly_key: 'ed25519:...', // Key to remove
    }),
  }
);
```

---

# Solana Wallet Authentication

Solana wallets use **native Ed25519 message signing** (not EIP-712) for account operations. Solana wallets already use Ed25519 keys natively, making the signing process simpler but requiring different message formatting.

## Solana vs EVM Authentication

| Aspect             | EVM Wallets           | Solana Wallets                   |
| ------------------ | --------------------- | -------------------------------- |
| **Signing Method** | EIP-712 typed data    | Plain message signing            |
| **Key Type**       | secp256k1             | Ed25519 (native)                 |
| **Account Lookup** | `/v1/get_account`     | `/v1/get_account?chain_type=SOL` |
| **Message Format** | Structured JSON types | Raw bytes via adapter            |
| **Signature**      | Ethereum signature    | Ed25519 signature                |

## Account Lookup

Check if a Solana wallet already has an Orderly account:

```typescript
import { PublicKey } from '@solana/web3.js';

const BROKER_ID = 'woofi_dex';
const solanaAddress = '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU'; // Base58 address

// Solana accounts require chain_type=SOL parameter
const response = await fetch(
  `https://testnet-api.orderly.org/v1/get_account?` +
    `address=${solanaAddress}&` +
    `broker_id=${BROKER_ID}&` +
    `chain_type=SOL`
);

const data = await response.json();
// data.data.account_id contains the Orderly account ID
// Account ID format is different from EVM (not a keccak256 hash)
```

## Message Signing with Solana Adapter

Orderly provides a Solana adapter to generate properly formatted messages:

```typescript
import { DefaultSolanaWalletAdapter } from '@orderly.network/default-solana-adapter';
import { Connection, clusterApiUrl, Keypair } from '@solana/web3.js';
import { signAsync } from '@noble/ed25519';
import bs58 from 'bs58';

// Setup wallet adapter
const walletAdapter = new DefaultSolanaWalletAdapter();

// Initialize with wallet details
walletAdapter.active({
  address: solanaAddress,
  provider: {
    connection: new Connection(clusterApiUrl('devnet')), // or 'mainnet-beta'
    signMessage: async (msg: Uint8Array) => {
      // Sign with Solana wallet (Ed25519)
      return await signAsync(msg, privateKeyBytes.slice(0, 32));
    },
    sendTransaction: async (tx, conn) => {
      tx.sign([senderKeypair]);
      return conn.sendTransaction(tx);
    },
  },
  chain: {
    id: network === 'mainnet' ? 900900900 : 901901901, // Solana chain IDs
  },
});
```

## Registration Flow

### Step 1: Fetch Registration Nonce

```typescript
const nonceResponse = await fetch('https://testnet-api.orderly.org/v1/registration_nonce');
const { data: nonce } = await nonceResponse.json();
```

### Step 2: Generate and Sign Registration Message

```typescript
// Generate registration message using adapter
const registerMessage = await walletAdapter.generateRegisterMessage({
  brokerId: BROKER_ID,
  timestamp: Date.now(),
  registrationNonce: nonce,
});

// Sign with Solana wallet (raw message bytes, not EIP-712)
const signature = await wallet.signMessage(registerMessage.message);
```

### Step 3: Submit Registration

```typescript
const registerResponse = await fetch('https://testnet-api.orderly.org/v1/register_account', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: registerMessage.message,
    signature: signature,
    userAddress: solanaAddress,
    chainType: 'SOL', // Required for Solana
  }),
});

const result = await registerResponse.json();
console.log('Account ID:', result.data.account_id);
```

## API Key Management (Orderly Key)

### Generate Ed25519 Key Pair

Same as EVM - locally generate an Ed25519 key pair:

```typescript
import { getPublicKeyAsync, utils } from '@noble/ed25519';
import bs58 from 'bs58';

// Generate key pair
const privateKey = utils.randomPrivateKey();
const publicKey = await getPublicKeyAsync(privateKey);
const orderlyKey = `ed25519:${bs58.encode(publicKey)}`;
```

### Sign Add Orderly Key Message

```typescript
// Generate add key message using adapter
const addKeyMessage = await walletAdapter.generateAddKeyMessage({
  brokerId: BROKER_ID,
  orderlyKey: orderlyKey,
  scope: 'read,trading',
  timestamp: Date.now(),
  expiration: Date.now() + 31536000000, // 1 year
});

// Sign with Solana wallet
const signature = await wallet.signMessage(addKeyMessage.message);
```

### Submit Orderly Key

```typescript
const keyResponse = await fetch('https://testnet-api.orderly.org/v1/orderly_key', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: addKeyMessage.message,
    signature: signature,
    userAddress: solanaAddress,
    chainType: 'SOL',
  }),
});
```

## Withdrawal Signing

Withdrawals require wallet signature on both EVM and Solana:

```typescript
// Fetch withdraw nonce
const nonceRes = await fetch(`${BASE_URL}/v1/withdraw_nonce`);
const {
  data: { withdraw_nonce },
} = await nonceRes.json();

// Generate withdraw message
const withdrawMessage = await walletAdapter.generateWithdrawMessage({
  brokerId: BROKER_ID,
  receiver: solanaAddress,
  token: 'USDC',
  amount: '1000',
  timestamp: Date.now(),
  nonce: Number(withdraw_nonce),
});

// Sign with Solana wallet
const signature = await wallet.signMessage(withdrawMessage.message);

// Submit withdrawal request
const res = await fetch(`${BASE_URL}/v1/withdraw_request`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: withdrawMessage.message,
    signature: signature,
    userAddress: solanaAddress,
    verifyingContract: '0x6F7a338F2aA472838dEFD3283eB360d4Dff5D203', // Mainnet
    // verifyingContract: '0x1826B75e2ef249173FC735149AE4B8e9ea10abff', // Testnet
  }),
});
```

## Settle PnL Signing

```typescript
// Fetch settle nonce
const nonceRes = await fetch(`${BASE_URL}/v1/settle_nonce`);
const {
  data: { settle_nonce },
} = await nonceRes.json();

// Generate settle message
const settleMessage = await walletAdapter.generateSettleMessage({
  brokerId: BROKER_ID,
  timestamp: Date.now(),
  settlePnlNonce: settle_nonce,
});

// Sign with Solana wallet
const signature = await wallet.signMessage(settleMessage.message);

// Submit settle request
const res = await fetch(`${BASE_URL}/v1/settle_pnl`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: settleMessage.message,
    signature: signature,
    userAddress: solanaAddress,
    verifyingContract: '0x6F7a338F2aA472838dEFD3283eB360d4Dff5D203',
  }),
});
```

## Solana-Specific Configuration

| Environment | Solana Chain ID | Solana Cluster | Orderly Vault Address                          | Verifying Contract                           |
| ----------- | --------------- | -------------- | ---------------------------------------------- | -------------------------------------------- |
| Mainnet     | 900900900       | `mainnet-beta` | `ErBmAD61mGFKvrFNaTJuxoPwqrS8GgtwtqJTJVjFWx9Q` | `0x6F7a338F2aA472838dEFD3283eB360d4Dff5D203` |
| Testnet     | 901901901       | `devnet`       | `9shwxWDUNhtwkHocsUAmrNAQfBH2DHh4njdAEdHZZkF2` | `0x1826B75e2ef249173FC735149AE4B8e9ea10abff` |

**Note**: API base URLs are the same for EVM and Solana. See the [Environment Configuration](#environment-configuration) section at the top of this skill.

## Important Differences

### Account ID Generation

- **EVM**: `keccak256(address, keccak256(brokerId))`
- **Solana**: Returned from `/v1/get_account` API (not a hash)

### Message Signing

- **EVM**: Uses `eth_signTypedData_v4` with structured EIP-712 types
- **Solana**: Uses raw message bytes signed with Ed25519

### No Domain Separator

Solana doesn't use EIP-712 domain configuration:

```typescript
// EVM - requires domain
domain: {
  name: 'Orderly',
  version: '1',
  chainId: 42161,
  verifyingContract: '0x...',
}

// Solana - no domain, just raw message
const message = await walletAdapter.generateRegisterMessage({...});
```

---

# Part 2: Ed25519 API Authentication

Once you have registered an Ed25519 key via wallet signing (EIP-712 for EVM or Ed25519 message signing for Solana), you use that key for all API operations.

## Required Headers

| Header               | Description                              |
| -------------------- | ---------------------------------------- |
| `orderly-timestamp`  | Unix timestamp in milliseconds           |
| `orderly-account-id` | Your Orderly account ID                  |
| `orderly-key`        | Your public key prefixed with `ed25519:` |
| `orderly-signature`  | Base64url-encoded Ed25519 signature      |

## Generating Ed25519 Key Pair

```typescript
import { getPublicKeyAsync, utils } from '@noble/ed25519';

// Generate private key (32 cryptographically secure random bytes)
const privateKey = utils.randomPrivateKey();

// Derive public key
const publicKey = await getPublicKeyAsync(privateKey);

// Encode public key as base58 (required by Orderly)
function encodeBase58(bytes: Uint8Array): string {
  const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  const BASE = 58n;

  let num = 0n;
  for (const byte of bytes) {
    num = num * 256n + BigInt(byte);
  }

  let result = '';
  while (num > 0n) {
    result = ALPHABET[Number(num % BASE)] + result;
    num = num / BASE;
  }

  // Handle leading zeros
  for (const byte of bytes) {
    if (byte === 0) {
      result = '1' + result;
    } else {
      break;
    }
  }

  return result;
}

const orderlyKey = `ed25519:${encodeBase58(publicKey)}`;

// Convert bytes to hex string (browser & Node.js compatible)
function bytesToHex(bytes: Uint8Array): string {
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

console.log('Private Key (hex):', bytesToHex(privateKey));
console.log('Public Key (base58):', orderlyKey);

// STORE PRIVATE KEY SECURELY - NEVER SHARE IT
```

## Signing Requests

### Message Construction

```typescript
function buildSignMessage(timestamp: number, method: string, path: string, body?: string): string {
  // Message format: timestamp + method + path + body
  // Note: No spaces or separators between parts
  return `${timestamp}${method}${path}${body || ''}`;
}

// Examples
const timestamp = Date.now();

// GET request (no body)
const getMessage = buildSignMessage(timestamp, 'GET', '/v1/positions');

// POST request (with body)
const body = JSON.stringify({
  symbol: 'PERP_ETH_USDC',
  side: 'BUY',
  order_type: 'LIMIT',
  order_price: '3000',
  order_quantity: '0.1',
});
const postMessage = buildSignMessage(timestamp, 'POST', '/v1/order', body);
```

### Creating the Signature

```typescript
import { signAsync } from '@noble/ed25519';

async function signRequest(
  timestamp: number,
  method: string,
  path: string,
  body: string | undefined,
  privateKey: Uint8Array
): Promise<string> {
  const message = buildSignMessage(timestamp, method, path, body);

  // Sign with Ed25519
  const signatureBytes = await signAsync(new TextEncoder().encode(message), privateKey);

  // Encode as base64url (NOT base64)
  // Convert to base64, then make it URL-safe
  const base64 = btoa(String.fromCharCode(...signatureBytes));
  return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
```

## Sign and Send Request Helper

For a simple, standalone authentication helper that always works correctly with query parameters and proper Content-Type headers:

```typescript
import { getPublicKeyAsync, signAsync } from '@noble/ed25519';
import { encodeBase58 } from 'ethers';

export async function signAndSendRequest(
  orderlyAccountId: string,
  privateKey: Uint8Array | string,
  input: URL | string,
  init?: RequestInit | undefined
): Promise<Response> {
  const timestamp = Date.now();
  const encoder = new TextEncoder();

  const url = new URL(input);
  let message = `${String(timestamp)}${init?.method ?? 'GET'}${url.pathname}${url.search}`;
  if (init?.body) {
    message += init.body;
  }
  const orderlySignature = await signAsync(encoder.encode(message), privateKey);

  return fetch(input, {
    headers: {
      'Content-Type':
        init?.method !== 'GET' && init?.method !== 'DELETE'
          ? 'application/json'
          : 'application/x-www-form-urlencoded',
      'orderly-timestamp': String(timestamp),
      'orderly-account-id': orderlyAccountId,
      'orderly-key': `ed25519:${encodeBase58(await getPublicKeyAsync(privateKey))}`,
      'orderly-signature': Buffer.from(orderlySignature).toString('base64url'),
      ...(init?.headers ?? {}),
    },
    ...(init ?? {}),
  });
}
```

This helper function:

- Properly parses the URL to extract both pathname and search (query) parameters
- Correctly sets Content-Type based on HTTP method (GET/DELETE use `application/x-www-form-urlencoded`, others use `application/json`)
- Constructs the signature message with timestamp + method + pathname + search + body
- Returns the fetch response for further processing

### Usage Examples

```typescript
const baseUrl = 'https://api.orderly.org';
const accountId = '0x123...';
const privateKey = new Uint8Array(32); // Your private key

// GET request with query parameters
const positions = await signAndSendRequest(accountId, privateKey, `${baseUrl}/v1/positions`);
const positionsData = await positions.json();

// GET request with query params
const orders = await signAndSendRequest(
  accountId,
  privateKey,
  `${baseUrl}/v1/orders?symbol=PERP_ETH_USDC&status=INCOMPLETE`
);
const ordersData = await orders.json();

// POST request with body
const order = await signAndSendRequest(accountId, privateKey, `${baseUrl}/v1/order`, {
  method: 'POST',
  body: JSON.stringify({
    symbol: 'PERP_ETH_USDC',
    side: 'BUY',
    order_type: 'LIMIT',
    order_price: '3000',
    order_quantity: '0.1',
  }),
});
const orderData = await order.json();

// DELETE request
const cancel = await signAndSendRequest(
  accountId,
  privateKey,
  `${baseUrl}/v1/order?order_id=123&symbol=PERP_ETH_USDC`,
  { method: 'DELETE' }
);
```

### Error Handling Helper

```typescript
class OrderlyApiError extends Error {
  code: number;
  details: any;

  constructor(response: any) {
    super(response.message || 'API Error');
    this.code = response.code;
    this.details = response;
  }
}

// Usage with error handling
async function apiRequest(
  accountId: string,
  privateKey: Uint8Array,
  url: string,
  init?: RequestInit
) {
  const response = await signAndSendRequest(accountId, privateKey, url, init);
  const result = await response.json();

  if (!result.success) {
    throw new OrderlyApiError(result);
  }

  return result.data;
}
```

## Query Parameters

Query parameters must be included in the signature message. The URL is parsed to extract both pathname and search parameters:

```typescript
// Correct - query params are parsed from the URL
const url = new URL('/v1/orders?symbol=PERP_ETH_USDC&status=INCOMPLETE', baseUrl);
// Message: timestamp + method + pathname + search
// Result: "1234567890123GET/v1/orders?symbol=PERP_ETH_USDC&status=INCOMPLETE"

// Wrong - query params added separately after signing
const path = '/v1/orders';
const signature = await sign(timestamp, 'GET', path);
const url = `${path}?symbol=PERP_ETH_USDC`; // Signature mismatch!
```

## Common Errors

### Signature Mismatch (Code 10016)

```
Cause: Signature doesn't match expected value

Check:
1. Message format: timestamp + method + path + body (no spaces)
2. Method is uppercase: GET, POST, DELETE, PUT
3. Path includes query parameters
4. Body is exact JSON string (same whitespace)
5. Signature is base64url encoded (not base64)
```

### Timestamp Expired (Code 10017)

```
Cause: Timestamp is too old or too far in the future

Solution:
- Ensure server clock is synchronized
- Timestamp must be within ±30 seconds
- Generate timestamp immediately before signing
```

### Invalid Orderly Key (Code 10019)

```
Cause: Public key format incorrect

Solution:
- Must be prefixed with 'ed25519:'
- Public key must be base58 encoded
- Key must be registered to account
```

## Orderly Key Scopes

When registering an API key, specify permissions:

| Scope     | Permissions                          |
| --------- | ------------------------------------ |
| `read`    | Read positions, orders, balance      |
| `trading` | Place, cancel, modify orders         |
| `asset`   | Deposit, withdraw, internal transfer |

```typescript
// When adding key via EIP-712 signing
const addKeyMessage = {
  brokerId: 'woofi_dex',
  chainId: 42161,
  orderlyKey: 'ed25519:...',
  scope: 'read,trading', // Multiple scopes comma-separated
  timestamp: Date.now(),
  expiration: Date.now() + 31536000000, // 1 year
};
```

## Security Best Practices

### Store Private Keys Securely

```typescript
// NEVER hardcode private keys
// BAD:
const privateKey = new Uint8Array([1, 2, 3, ...]);

// GOOD: Load from environment
const privateKeyHex = process.env.ORDERLY_PRIVATE_KEY;
// Convert hex string to Uint8Array (browser & Node.js compatible)
function hexToBytes(hex: string): Uint8Array {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
  }
  return bytes;
}
const privateKey = hexToBytes(privateKeyHex);

// BETTER: Use secure key management
// AWS KMS, HashiCorp Vault, etc.
```

### Key Rotation

Rotate your API keys periodically for security:

```typescript
// Generate new key pair
const newPrivateKey = utils.randomPrivateKey();
const newPublicKey = await getPublicKeyAsync(newPrivateKey);

// Register new key (requires wallet signature via EIP-712)
// POST /v1/orderly_key - No Ed25519 auth required
const orderlyKey = `ed25519:${encodeBase58(newPublicKey)}`;
const timestamp = Date.now();
const expiration = timestamp + 31536000000; // 1 year

const addKeyMessage = {
  brokerId: 'your_broker_id',
  chainId: 42161, // Arbitrum mainnet
  orderlyKey: orderlyKey,
  scope: 'read,trading', // Comma-separated scopes
  timestamp: timestamp,
  expiration: expiration,
};

// Sign with wallet (EIP-712)
const addKeySignature = await wallet.signTypedData({
  domain: {
    name: 'Orderly',
    version: '1',
    chainId: 42161,
    verifyingContract: '0x...', // Contract address
  },
  types: {
    EIP712Domain: [
      { name: 'name', type: 'string' },
      { name: 'version', type: 'string' },
      { name: 'chainId', type: 'uint256' },
      { name: 'verifyingContract', type: 'address' },
    ],
    AddOrderlyKey: [
      { name: 'brokerId', type: 'string' },
      { name: 'chainId', type: 'uint256' },
      { name: 'orderlyKey', type: 'string' },
      { name: 'scope', type: 'string' },
      { name: 'timestamp', type: 'uint256' },
      { name: 'expiration', type: 'uint256' },
    ],
  },
  primaryType: 'AddOrderlyKey',
  message: addKeyMessage,
});

const registerResponse = await fetch('https://api.orderly.org/v1/orderly_key', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: addKeyMessage,
    signature: addKeySignature,
    userAddress: walletAddress,
  }),
});

const registerResult = await registerResponse.json();
if (!registerResult.success) {
  throw new Error(`Failed to register key: ${registerResult.message}`);
}

// Update your application config
config.privateKey = newPrivateKey;
config.orderlyKey = orderlyKey;

// Remove old key using authenticated request
// POST /v1/client/remove_orderly_key - Requires Ed25519 auth
const oldOrderlyKey = `ed25519:${encodeBase58(oldPublicKey)}`;
const removeResponse = await signAndSendRequest(
  accountId,
  newPrivateKey, // Use the NEW key to authenticate
  'https://api.orderly.org/v1/client/remove_orderly_key',
  {
    method: 'POST',
    body: JSON.stringify({
      orderly_key: oldOrderlyKey,
    }),
  }
);

const removeResult = await removeResponse.json();
if (!removeResult.success) {
  throw new Error(`Failed to remove old key: ${removeResult.message}`);
}
```

### IP Restrictions

```typescript
// Set IP restriction for key
POST /v1/client/set_orderly_key_ip_restriction
Body: {
  orderly_key: 'ed25519:...',
  ip_list: ['1.2.3.4', '5.6.7.8'],
}

// Get current restrictions
GET /v1/client/orderly_key_ip_restriction?orderly_key={key}

// Reset (remove) restrictions
POST /v1/client/reset_orderly_key_ip_restriction
Body: { orderly_key: 'ed25519:...' }
```

## WebSocket Authentication

WebSocket also requires Ed25519 authentication:

```typescript
const ws = new WebSocket(`wss://ws-private-evm.orderly.org/v2/ws/private/stream/${accountId}`);

ws.onopen = async () => {
  const timestamp = Date.now();
  const message = timestamp.toString();

  const signature = await signAsync(new TextEncoder().encode(message), privateKey);

  // Convert to base64url (browser & Node.js compatible)
  const base64 = btoa(String.fromCharCode(...signature));
  const base64url = base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

  ws.send(
    JSON.stringify({
      id: 'auth_1',
      event: 'auth',
      params: {
        orderly_key: orderlyKey,
        sign: base64url,
        timestamp: timestamp,
      },
    })
  );
};
```

## Testing Authentication

```typescript
// Verify key is valid
GET /v1/get_orderly_key?orderly_key={key}

// Response
{
  "success": true,
  "data": {
    "account_id": "0x...",
    "valid": true,
    "scope": "read,trading",
    "expires_at": 1735689600000
  }
}
```

## Supported Chains

| Chain    | Chain ID              | Mainnet | Testnet |
| -------- | --------------------- | ------- | ------- |
| Arbitrum | 42161 / 421614        | ✅      | ✅      |
| Optimism | 10 / 11155420         | ✅      | ✅      |
| Base     | 8453 / 84532          | ✅      | ✅      |
| Ethereum | 1 / 11155111          | ✅      | ✅      |
| Solana   | 900900900 / 901901901 | ✅      | ✅      |
| Mantle   | 5000 / 5003           | ✅      | ✅      |

## Common Issues

### EIP-712 Errors

**"Nonce expired" error**

- Nonces are valid for 2 minutes only
- Fetch a new nonce and retry

**"Account already exists" error**

- The wallet is already registered with this broker
- Use `/v1/get_account` to retrieve existing account info

**"Invalid signature" error**

- Ensure the EIP-712 domain matches exactly (name, version, chainId, verifyingContract)
- Check chain ID matches your network
- Verify the message structure matches the types
- Use `eth_signTypedData_v4` not `eth_signTypedData`

### Ed25519 Errors

**Signature Mismatch (Code 10016)**

```
Cause: Signature doesn't match expected value

Check:
1. Message format: timestamp + method + path + body (no spaces)
2. Method is uppercase: GET, POST, DELETE, PUT
3. Path includes query parameters
4. Body is exact JSON string (same whitespace)
5. Signature is base64url encoded (not base64)
```

**Timestamp Expired (Code 10017)**

```
Cause: Timestamp is too old or too far in the future

Solution:
- Ensure server clock is synchronized
- Timestamp must be within ±30 seconds
- Generate timestamp immediately before signing
```

**Invalid Orderly Key (Code 10019)**

```
Cause: Public key format incorrect

Solution:
- Must be prefixed with 'ed25519:'
- Public key must be base58 encoded
- Key must be registered to account
```

## Authentication Comparison

| Aspect             | EIP-712 Wallet Auth                       | Ed25519 API Auth              |
| ------------------ | ----------------------------------------- | ----------------------------- |
| **Purpose**        | Account operations, key management        | Trading, reading data         |
| **Signer**         | User's Web3 wallet                        | Locally-generated Ed25519 key |
| **Key type**       | Ethereum private key                      | Ed25519 key pair              |
| **Endpoints**      | `/v1/register_account`, `/v1/orderly_key` | All other endpoints           |
| **Signature type** | EIP-712 typed data                        | Raw Ed25519 + base64url       |
| **Scope**          | Create/manage API keys                    | Use API keys for trading      |

## Related Skills

- **orderly-trading-orders** - Using authenticated endpoints
- **orderly-websocket-streaming** - WebSocket authentication
- **orderly-sdk-react-hooks** - React SDK for simplified auth
- **orderly-deposit-withdraw** - Fund your account
