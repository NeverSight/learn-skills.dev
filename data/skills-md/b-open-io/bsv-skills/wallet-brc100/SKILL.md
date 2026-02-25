---
name: wallet-brc100
description: This skill should be used when the user asks to "implement BRC-100 wallet", "use wallet-toolbox", "TypeScript BSV wallet", "BRC-100 implementation", "desktop wallet", "Electron wallet", "browser wallet", "IndexedDB wallet storage", "wallet actions", "wallet baskets", "UTXO management", "createAction", "listOutputs", "wallet certificates", or needs guidance on building conforming wallets using @bsv/wallet-toolbox.
---

# BRC-100 Wallet Implementation Guide

This skill provides comprehensive guidance for implementing BRC-100 conforming wallets using the `@bsv/wallet-toolbox` package (v1.7.18+).

**Getting Started**: Before implementing, review the [Strategic Questionnaire](./references/strategic-questionnaire.md) to determine the right architecture for your wallet type.

## Quick Reference

### Core Dependencies

```json
{
  "@bsv/wallet-toolbox": "^1.7.18",
  "@bsv/sdk": "^1.9.29"
}
```

### Main Classes

| Class | Purpose | Use When |
|-------|---------|----------|
| **Wallet** | Full BRC-100 wallet | Building production wallet apps |
| **SimpleWalletManager** | Lightweight wrapper | Simple key-based authentication |
| **CWIStyleWalletManager** | Multi-profile wallet | Advanced UMP token flows |
| **WalletSigner** | Transaction signing | Custom signing logic |

---

## Table of Contents

1. [Installation & Setup](#1-installation--setup)
2. [Wallet Initialization](#2-wallet-initialization)
3. [Transaction Operations](#3-transaction-operations)
4. [Key Management](#4-key-management)
5. [Storage Configuration](#5-storage-configuration)
6. [Certificate Operations](#6-certificate-operations)
7. [Error Handling](#7-error-handling)
8. [Production Patterns](#8-production-patterns)

---

## 1. Installation & Setup

### Install Dependencies

```bash
npm install @bsv/wallet-toolbox @bsv/sdk
# Optional storage backends:
npm install knex sqlite3          # SQLite
npm install knex mysql2           # MySQL
npm install idb                   # IndexedDB (browser)
```

### Basic Imports

```typescript
import {
  Wallet,
  WalletStorageManager,
  StorageKnex,
  StorageIdb,
  Services,
  WalletServices,
  PrivilegedKeyManager
} from '@bsv/wallet-toolbox'

import {
  PrivateKey,
  KeyDeriver,
  Random,
  Utils
} from '@bsv/sdk'
```

---

## 2. Wallet Initialization

### Pattern A: Simple Wallet (Node.js with SQLite)

```typescript
import { Wallet, StorageKnex, Services } from '@bsv/wallet-toolbox'
import { PrivateKey, Random } from '@bsv/sdk'
import Knex from 'knex'

async function createSimpleWallet() {
  // 1. Create root private key (or derive from mnemonic)
  const rootKey = new PrivateKey(Random(32))
  // Use KeyDeriver from @bsv/sdk for proper BRC-42 key derivation
  const keyDeriver = new KeyDeriver(rootKey)

  // 2. Configure SQLite storage
  const knex = Knex({
    client: 'sqlite3',
    connection: { filename: './wallet.db' },
    useNullAsDefault: true
  })

  const storage = new StorageKnex({
    knex,
    storageIdentityKey: rootKey.toPublicKey().toString(),
    storageName: 'my-wallet-storage'
  })

  await storage.makeAvailable()

  // 3. Configure services (mainnet)
  const services = new Services({
    chain: 'main',
    bsvExchangeRate: { timestamp: new Date(), base: 'USD', rate: 50 },
    bsvUpdateMsecs: 15 * 60 * 1000,
    fiatExchangeRates: {
      timestamp: new Date(),
      base: 'USD',
      rates: { EUR: 0.85, GBP: 0.73 }
    },
    fiatUpdateMsecs: 24 * 60 * 60 * 1000,
    arcUrl: 'https://arc.taal.com',
    arcConfig: {}
  })

  // 4. Create wallet
  const wallet = new Wallet({
    chain: 'main',
    keyDeriver,
    storage,
    services
  })

  return wallet
}
```

### Pattern B: Browser Wallet (IndexedDB)

```typescript
import { Wallet, StorageIdb, Services } from '@bsv/wallet-toolbox'
import { PrivateKey, Random } from '@bsv/sdk'

async function createBrowserWallet() {
  const rootKey = new PrivateKey(Random(32))

  // Use IndexedDB for browser storage
  const storage = new StorageIdb({
    idb: await openDB('my-wallet-db', 1),
    storageIdentityKey: rootKey.toPublicKey().toString(),
    storageName: 'browser-wallet'
  })

  await storage.makeAvailable()

  const services = new Services({
    chain: 'main',
    // ... services config
  })

  const wallet = new Wallet({
    chain: 'main',
    keyDeriver: createKeyDeriver(rootKey),
    storage,
    services
  })

  return wallet
}
```

### Pattern C: Multi-Profile Wallet

```typescript
import { CWIStyleWalletManager, OverlayUMPTokenInteractor } from '@bsv/wallet-toolbox'

async function createMultiProfileWallet() {
  const manager = new CWIStyleWalletManager(
    'example.com', // Admin originator
    async (profilePrimaryKey, profilePrivilegedKeyManager, profileId) => {
      // Build wallet for specific profile
      const keyDeriver = createKeyDeriver(new PrivateKey(profilePrimaryKey))
      const storage = await createStorage(profileId)
      const services = new Services({ chain: 'main', /* ... */ })

      return new Wallet({
        chain: 'main',
        keyDeriver,
        storage,
        services,
        privilegedKeyManager: profilePrivilegedKeyManager
      })
    },
    new OverlayUMPTokenInteractor(), // UMP token interactor
    async (recoveryKey) => {
      // Save recovery key (e.g., prompt user to write it down)
      console.log('SAVE THIS RECOVERY KEY:', Utils.toBase64(recoveryKey))
      return true
    },
    async (reason, test) => {
      // Retrieve password from user
      const password = prompt(`Enter password for: ${reason}`)
      if (!password) throw new Error('Password required')
      if (!test(password)) throw new Error('Invalid password')
      return password
    }
  )

  // Provide presentation key (e.g., from QR code scan)
  const presentationKey = Random(32)
  await manager.providePresentationKey(presentationKey)

  // Provide password
  await manager.providePassword('user-password')

  // Now authenticated and ready to use
  return manager
}
```

---

## 3. Transaction Operations

### Create a Transaction

```typescript
import { CreateActionArgs, CreateActionResult } from '@bsv/sdk'

async function sendBSV(
  wallet: Wallet,
  recipientAddress: string,
  satoshis: number
) {
  const args: CreateActionArgs = {
    description: 'Send BSV payment',
    outputs: [{
      lockingScript: Script.fromAddress(recipientAddress).toHex(),
      satoshis,
      outputDescription: `Payment to ${recipientAddress}`,
      basket: 'default',
      tags: ['payment']
    }],
    options: {
      acceptDelayedBroadcast: false, // Broadcast immediately
      randomizeOutputs: true          // Privacy
    }
  }

  const result: CreateActionResult = await wallet.createAction(args)

  if (result.txid) {
    console.log('Transaction created:', result.txid)
    return result.txid
  } else {
    console.log('Transaction pending signature')
    return result.signableTransaction
  }
}
```

### Sign a Transaction

```typescript
async function signTransaction(
  wallet: Wallet,
  reference: string,
  unlockingScripts: Record<number, { unlockingScript: string }>
) {
  const result = await wallet.signAction({
    reference,
    spends: unlockingScripts
  })

  console.log('Transaction signed:', result.txid)
  return result
}
```

### Check Wallet Balance

```typescript
async function getWalletBalance(wallet: Wallet) {
  // Method 1: Quick balance (uses special operation)
  const balance = await wallet.balance()
  console.log(`Balance: ${balance} satoshis`)

  // Method 2: Detailed balance with UTXOs
  const detailed = await wallet.balanceAndUtxos('default')
  console.log(`Total: ${detailed.total} satoshis`)
  console.log(`UTXOs: ${detailed.utxos.length}`)
  detailed.utxos.forEach(utxo => {
    console.log(`  ${utxo.outpoint}: ${utxo.satoshis} sats`)
  })

  return balance
}
```

### List Outputs

```typescript
import { ListOutputsArgs, ListOutputsResult } from '@bsv/sdk'

async function listSpendableOutputs(wallet: Wallet) {
  const args: ListOutputsArgs = {
    basket: 'default',  // Change basket
    spendable: true,    // Only spendable outputs
    limit: 100,
    offset: 0,
    tags: ['payment']   // Optional: filter by tags
  }

  const result: ListOutputsResult = await wallet.listOutputs(args)

  console.log(`Found ${result.totalOutputs} outputs`)
  result.outputs.forEach(output => {
    console.log(`  ${output.outpoint}: ${output.satoshis} sats`)
  })

  return result
}
```

### List Actions (Transactions)

```typescript
async function listTransactionHistory(wallet: Wallet) {
  const result = await wallet.listActions({
    labels: [],
    labelQueryMode: 'any',
    limit: 50,
    offset: 0
  })

  console.log(`Found ${result.totalActions} actions`)
  result.actions.forEach(action => {
    console.log(`  ${action.txid}: ${action.status} - ${action.description}`)
  })

  return result
}
```

---

## 4. Key Management

### Get Public Key

```typescript
async function getIdentityKey(wallet: Wallet) {
  // Get wallet's identity key
  const result = await wallet.getPublicKey({ identityKey: true })
  console.log('Identity Key:', result.publicKey)
  return result.publicKey
}

async function getDerivedKey(wallet: Wallet) {
  // Get derived key for specific protocol
  const result = await wallet.getPublicKey({
    protocolID: [2, 'my-app'],
    keyID: 'encryption-key-1',
    counterparty: 'recipient-identity-key'
  })

  return result.publicKey
}
```

### Encrypt/Decrypt Data

```typescript
async function encryptMessage(
  wallet: Wallet,
  plaintext: string,
  recipientPubKey: string
) {
  const result = await wallet.encrypt({
    plaintext: Utils.toArray(plaintext, 'utf8'),
    protocolID: [2, 'secure-messaging'],
    keyID: 'msg-key',
    counterparty: recipientPubKey
  })

  return Utils.toBase64(result.ciphertext)
}

async function decryptMessage(
  wallet: Wallet,
  ciphertext: string,
  senderPubKey: string
) {
  const result = await wallet.decrypt({
    ciphertext: Utils.toArray(ciphertext, 'base64'),
    protocolID: [2, 'secure-messaging'],
    keyID: 'msg-key',
    counterparty: senderPubKey
  })

  return Utils.toUTF8(result.plaintext)
}
```

### Create Signature

```typescript
async function signData(wallet: Wallet, data: string) {
  const result = await wallet.createSignature({
    data: Utils.toArray(data, 'utf8'),
    protocolID: [2, 'document-signing'],
    keyID: 'sig-key',
    counterparty: 'self'
  })

  return Utils.toBase64(result.signature)
}
```

---

## 5. Storage Configuration

### SQLite Storage (Node.js)

```typescript
import Knex from 'knex'
import { StorageKnex } from '@bsv/wallet-toolbox'

async function setupSQLiteStorage() {
  const knex = Knex({
    client: 'sqlite3',
    connection: { filename: './wallet.db' },
    useNullAsDefault: true
  })

  const storage = new StorageKnex({
    knex,
    storageIdentityKey: 'your-identity-key',
    storageName: 'main-storage'
  })

  await storage.makeAvailable()
  return storage
}
```

### MySQL Storage

```typescript
async function setupMySQLStorage() {
  const knex = Knex({
    client: 'mysql2',
    connection: {
      host: 'localhost',
      user: 'wallet_user',
      password: 'secure_password',
      database: 'wallet_db'
    }
  })

  const storage = new StorageKnex({
    knex,
    storageIdentityKey: 'your-identity-key',
    storageName: 'mysql-storage'
  })

  await storage.makeAvailable()
  return storage
}
```

### IndexedDB Storage (Browser)

```typescript
import { openDB, DBSchema } from 'idb'
import { StorageIdb } from '@bsv/wallet-toolbox'

interface WalletDB extends DBSchema {
  // Storage schema is managed by StorageIdb
}

async function setupIndexedDBStorage() {
  const db = await openDB<WalletDB>('wallet-db', 1, {
    upgrade(db) {
      // StorageIdb creates necessary object stores
    }
  })

  const storage = new StorageIdb({
    idb: db,
    storageIdentityKey: 'your-identity-key',
    storageName: 'browser-storage'
  })

  await storage.makeAvailable()
  return storage
}
```

### Multi-Storage Manager

```typescript
import { WalletStorageManager } from '@bsv/wallet-toolbox'

async function setupMultiStorage() {
  const primaryStorage = await setupSQLiteStorage()
  const backupStorage = await setupMySQLStorage()

  const manager = new WalletStorageManager(
    primaryStorage,
    [backupStorage]
  )

  return manager
}
```

---

## 6. Certificate Operations

### Acquire Certificate (Direct Protocol)

```typescript
import { AcquireCertificateArgs } from '@bsv/sdk'

async function acquireDirectCertificate(wallet: Wallet) {
  const args: AcquireCertificateArgs = {
    acquisitionProtocol: 'direct',
    type: 'https://example.com/user-certificate',
    certifier: 'certifier-identity-key',
    serialNumber: Utils.toArray('cert-serial-123', 'utf8'),
    subject: await wallet.getIdentityKey(),
    revocationOutpoint: 'txid.vout',
    fields: {
      name: Utils.toArray('Alice Smith', 'utf8'),
      email: Utils.toArray('alice@example.com', 'utf8')
    },
    keyringForSubject: { /* master keyring */ },
    signature: Utils.toArray('signature-bytes', 'base64')
  }

  const result = await wallet.acquireCertificate(args)
  console.log('Certificate acquired:', result.certificateId)
  return result
}
```

### Acquire Certificate (Issuance Protocol)

```typescript
async function requestCertificateIssuance(wallet: Wallet) {
  const args: AcquireCertificateArgs = {
    acquisitionProtocol: 'issuance',
    type: 'https://example.com/kyc-certificate',
    certifier: 'certifier-identity-key',
    certifierUrl: 'https://certifier.example.com',
    fields: {
      name: 'Alice Smith',
      birthdate: '1990-01-01',
      country: 'US'
    }
  }

  const result = await wallet.acquireCertificate(args)
  console.log('Certificate issued:', result.certificateId)
  return result
}
```

### List Certificates

```typescript
async function listMyCertificates(wallet: Wallet) {
  const result = await wallet.listCertificates({
    certifiers: ['certifier-identity-key'],
    types: ['https://example.com/user-certificate'],
    limit: 50,
    offset: 0
  })

  console.log(`Found ${result.totalCertificates} certificates`)
  result.certificates.forEach(cert => {
    console.log(`  Type: ${cert.type}, Certifier: ${cert.certifier}`)
  })

  return result
}
```

### Prove Certificate

```typescript
async function proveCertificate(wallet: Wallet, certificateId: string) {
  const result = await wallet.proveCertificate({
    certificateId,
    fieldsToReveal: ['name', 'email'],
    verifier: 'verifier-identity-key',
    privileged: false
  })

  console.log('Certificate proof:', result.keyringForVerifier)
  return result
}
```

---

## 7. Error Handling

### Standard Error Types

```typescript
import {
  WalletError,
  WERR_INVALID_PARAMETER,
  WERR_INTERNAL,
  WERR_REVIEW_ACTIONS
} from '@bsv/wallet-toolbox'

try {
  const result = await wallet.createAction({
    description: 'Test transaction',
    outputs: [/* ... */]
  })
} catch (eu: unknown) {
  const error = WalletError.fromUnknown(eu)

  if (error.name === 'WERR_INVALID_PARAMETER') {
    console.error('Invalid parameter:', error.message)
    console.error('Stack:', error.stack)
  } else if (error.name === 'WERR_REVIEW_ACTIONS') {
    // Handle transaction review errors
    console.error('Review required:', error.details)
  } else {
    console.error('Wallet error:', error.message)
  }
}
```

### Review Actions Error (Transaction Failed)

```typescript
async function handleCreateAction(wallet: Wallet) {
  try {
    return await wallet.createAction({
      description: 'Payment',
      outputs: [/* ... */]
    })
  } catch (eu: unknown) {
    const error = WalletError.fromUnknown(eu)

    if (error.name === 'WERR_REVIEW_ACTIONS') {
      // Access detailed failure info
      const details = error as any
      console.error('Delayed results:', details.notDelayedResults)
      console.error('Send results:', details.sendWithResults)
      console.error('Failed txid:', details.txid)

      // Handle double-spend
      if (details.notDelayedResults?.some(r => r.status === 'doubleSpend')) {
        console.error('Double-spend detected!')
        console.error('Competing txs:', details.notDelayedResults[0].competingTxs)
      }
    }

    throw error
  }
}
```

---

## 8. Production Patterns

### Pattern: Wallet State Management

```typescript
class WalletManager {
  private wallet: Wallet | null = null

  async initialize(rootKey: PrivateKey) {
    if (this.wallet) {
      throw new Error('Wallet already initialized')
    }

    const storage = await this.setupStorage()
    const services = this.setupServices()
    const keyDeriver = this.createKeyDeriver(rootKey)

    this.wallet = new Wallet({
      chain: 'main',
      keyDeriver,
      storage,
      services
    })

    return this.wallet
  }

  async destroy() {
    if (this.wallet) {
      await this.wallet.destroy()
      this.wallet = null
    }
  }

  getWallet(): Wallet {
    if (!this.wallet) {
      throw new Error('Wallet not initialized')
    }
    return this.wallet
  }

  private async setupStorage() {
    // Storage setup logic
    return await setupSQLiteStorage()
  }

  private setupServices() {
    return new Services({
      chain: 'main',
      // ... config
    })
  }

  private createKeyDeriver(rootKey: PrivateKey) {
    // Key derivation logic
    return {
      rootKey,
      identityKey: rootKey.toPublicKey().toString(),
      // ... derivation methods
    }
  }
}
```

### Pattern: Transaction Retry Logic

```typescript
async function sendWithRetry(
  wallet: Wallet,
  args: CreateActionArgs,
  maxRetries = 3
): Promise<string> {
  let lastError: Error | null = null

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await wallet.createAction(args)

      if (result.txid) {
        return result.txid
      }

      // Handle signature if needed
      if (result.signableTransaction) {
        const signed = await wallet.signAction({
          reference: result.signableTransaction.reference,
          spends: {} // Provide unlocking scripts
        })
        return signed.txid!
      }

      throw new Error('Unexpected result format')

    } catch (error) {
      lastError = error as Error
      console.error(`Attempt ${attempt} failed:`, error)

      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt))
      }
    }
  }

  throw lastError || new Error('All retries failed')
}
```

### Pattern: Background Transaction Monitor

```typescript
import { Monitor } from '@bsv/wallet-toolbox'

async function setupMonitor(wallet: Wallet) {
  const monitor = new Monitor({
    storage: wallet.storage,
    services: wallet.services,
    chain: 'main'
  })

  monitor.on('transaction', (status) => {
    console.log('Transaction update:', status.txid, status.blockHeight)
  })

  monitor.on('error', (error) => {
    console.error('Monitor error:', error)
  })

  await monitor.start()

  return monitor
}
```

---

## Related Skills

For comprehensive wallet development, also reference these skills:

| Skill | Relationship |
|-------|--------------|
| `encrypt-decrypt-backup` | Standard backup formats (.bep files, AES-256-GCM) |
| `junglebus` | Populate UTXO set from blockchain, real-time streaming |
| `key-derivation` | Type42/BRC-42 and BIP32 key derivation details |
| `wallet-encrypt-decrypt` | ECDH message encryption patterns |
| `wallet-send-bsv` | Basic transaction creation (simpler than BRC-100) |

**For 1Sat Ordinals / Token Support:**

If your BRC-100 wallet needs to handle 1Sat Ordinals, BSV-20/BSV-21 tokens, or inscriptions, use `@1sat/wallet-toolbox` which wraps the core wallet-toolbox with ordinals capabilities.

See [1sat-skills](https://github.com/b-open-io/1sat-skills) for:
- `wallet-create-ordinals` - Mint inscriptions
- `extract-blockchain-media` - Extract media from transactions
- `ordinals-marketplace` - Browse GorillaPool marketplace

---

## Additional Resources

- **BRC-100 Specification**: https://bsv.brc.dev/wallet/0100
- **BRC-42 (BKDS)**: https://bsv.brc.dev/wallet/0042
- **BRC-43 (Security Levels)**: https://bsv.brc.dev/wallet/0043
- **Wallet Toolbox Docs**: https://bsv-blockchain.github.io/wallet-toolbox
- **BSV SDK Docs**: https://bsv-blockchain.github.io/ts-sdk
- **@1sat/wallet-toolbox**: BRC-100 wallet with 1Sat Ordinals support (wraps @bsv/wallet-toolbox)
- **1sat-skills**: https://github.com/b-open-io/1sat-skills - Ordinals minting and management
- **bsv-desktop (Reference Implementation)**: https://github.com/bsv-blockchain/bsv-desktop
  - Real-world Electron wallet with BRC-100 support
  - IPC architecture for storage isolation
  - Background monitoring patterns
  - HTTPS server on port 2121 for BRC-100 interface

**Research**: For deep dives into BRC specifications or implementation patterns, use the browser-agent to fetch current documentation from bsv.brc.dev.

---

## Platform Guides

Platform-specific implementation guides:

| Platform | Guide | Reference Implementation |
|----------|-------|-------------------------|
| Browser Extension | [extension-guide.md](./references/extension-guide.md) | [yours-wallet](https://github.com/AustinKelsay/yours-wallet) |
| Desktop (Electron) | [desktop-guide.md](./references/desktop-guide.md) | [bsv-desktop](https://github.com/bsv-blockchain/bsv-desktop) |
| Web Application | [web-guide.md](./references/web-guide.md) | - |
| Mobile (React Native) | [mobile-guide.md](./references/mobile-guide.md) | - |
| Node.js Service/CLI | [nodejs-guide.md](./references/nodejs-guide.md) | - |

See [references/key-concepts.md](./references/key-concepts.md) for BRC-100 unique concepts:
- Actions vs Transactions
- Baskets and Tags
- Certificate system (BRC-52/53/64/65)
- Background Monitoring

---

## Common Patterns Summary

| Task | Method | Key Args |
|------|--------|----------|
| Send BSV | `createAction()` | `outputs`, `options` |
| Check balance | `balance()` | None |
| List UTXOs | `listOutputs()` | `basket`, `spendable` |
| Get history | `listActions()` | `labels`, `limit` |
| Get pubkey | `getPublicKey()` | `protocolID`, `keyID` |
| Encrypt data | `encrypt()` | `plaintext`, `counterparty` |
| Get certificate | `acquireCertificate()` | `type`, `certifier` |

---

**Remember**: Always handle errors properly, use privileged keys securely, and follow BRC-100 security levels for sensitive operations!
