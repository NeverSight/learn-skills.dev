---
name: wallet-encrypt-decrypt
description: This skill should be used when the user asks to "encrypt message with BSV key", "decrypt with private key", "ECDH encryption", "AES-256-GCM BSV", "EncryptedMessage", "BRC-2 encryption", or needs to encrypt/decrypt data using BSV keys and @bsv/sdk.
---

# BSV Message Encryption

Encrypt and decrypt messages between parties using `@bsv/sdk`.

## Recommended: Use EncryptedMessage from @bsv/sdk

The `@bsv/sdk` provides `EncryptedMessage` for secure message encryption. This is the preferred approach - avoid rolling custom encryption implementations.

```typescript
import { PrivateKey, EncryptedMessage, Utils } from '@bsv/sdk'

const sender = PrivateKey.fromRandom()
const recipient = PrivateKey.fromRandom()

// Encrypt: sender uses their private key + recipient's public key
const message = Utils.toArray('Secret message', 'utf8')
const encrypted = EncryptedMessage.encrypt(message, sender, recipient.toPublicKey())

// Decrypt: recipient uses their private key
const decrypted = EncryptedMessage.decrypt(encrypted, recipient)
const plaintext = Utils.toUTF8(decrypted)
```

## Two Encryption Patterns

### Pattern 1: Static-Static ECDH (Both Parties Have Keys)

Use when both parties have established keypairs (e.g., BAP identities, paymail addresses).

```typescript
import { PrivateKey, EncryptedMessage, Utils } from '@bsv/sdk'

// Alice and Bob both have persistent keys
const alice = PrivateKey.fromWif('L1...')
const bob = PrivateKey.fromWif('K1...')

// Alice encrypts to Bob
const ciphertext = EncryptedMessage.encrypt(
  Utils.toArray('Hello Bob', 'utf8'),
  alice,
  bob.toPublicKey()
)

// Bob decrypts from Alice
const plaintext = EncryptedMessage.decrypt(ciphertext, bob)
```

**Use cases:**
- Peer-to-peer encrypted messaging
- Encrypted backups to your own key
- Communication between known identities

### Pattern 2: ECIES-Style (Ephemeral Sender Key)

Use when sender doesn't have a persistent identity (e.g., browser-to-server).

```typescript
import { PrivateKey, EncryptedMessage, Utils } from '@bsv/sdk'

// Server has persistent key, client generates ephemeral
const serverKey = PrivateKey.fromWif('L1...')
const ephemeralClient = PrivateKey.fromRandom()

// Client encrypts (ephemeral → server)
const encrypted = EncryptedMessage.encrypt(
  Utils.toArray('sensitive data', 'utf8'),
  ephemeralClient,
  serverKey.toPublicKey()
)

// Include ephemeral public key so server can decrypt
const payload = {
  ephemeralPub: ephemeralClient.toPublicKey().toString(),
  ciphertext: Utils.toHex(encrypted)
}

// Server decrypts using ephemeral pubkey
const clientPub = PublicKey.fromString(payload.ephemeralPub)
// Note: EncryptedMessage.decrypt needs the sender info embedded in ciphertext
```

**Use cases:**
- Browser-to-server encryption
- One-way secure channels
- Forward secrecy (fresh key per message)

## How ECDH Key Agreement Works

Both parties derive the same shared secret:

```
Alice: alicePrivKey × bobPubKey = sharedPoint
Bob:   bobPrivKey × alicePubKey = sharedPoint
```

The shared point is then used to derive a symmetric key for AES-256-GCM encryption.

## API Reference

### EncryptedMessage.encrypt()

```typescript
static encrypt(
  message: number[],      // Plaintext as byte array
  sender: PrivateKey,     // Sender's private key
  recipient: PublicKey    // Recipient's public key
): number[]               // Encrypted bytes
```

### EncryptedMessage.decrypt()

```typescript
static decrypt(
  ciphertext: number[],   // Encrypted bytes from encrypt()
  recipient: PrivateKey   // Recipient's private key
): number[]               // Decrypted plaintext bytes
```

### Utility Functions

```typescript
// String to bytes
Utils.toArray('hello', 'utf8')  // number[]

// Bytes to string
Utils.toUTF8([104, 101, 108, 108, 111])  // 'hello'

// Bytes to hex
Utils.toHex([1, 2, 3])  // '010203'

// Hex to bytes
Utils.toArray('010203', 'hex')  // [1, 2, 3]
```

## Security Properties

- **Authenticated encryption**: AES-256-GCM provides confidentiality + integrity
- **Key agreement**: ECDH ensures only intended recipient can decrypt
- **No key transmission**: Private keys never leave their owner

## Common Mistakes

### Don't roll your own crypto

❌ **Wrong**: Implementing ECDH + AES manually
```typescript
// Don't do this - use EncryptedMessage instead
const sharedSecret = myPrivKey.deriveSharedSecret(theirPubKey)
const aesKey = sha256(sharedSecret)
// ... manual AES encryption
```

✅ **Correct**: Use the SDK's built-in class
```typescript
const encrypted = EncryptedMessage.encrypt(message, sender, recipient)
```

### Don't confuse encryption with authentication

- **Encryption** (this skill): Hides message content
- **Authentication** (`bitcoin-auth`): Proves sender identity

For authenticated + encrypted communication, use both:
```typescript
// Encrypt the payload
const encrypted = EncryptedMessage.encrypt(payload, sender, recipient)

// Sign the request (proves sender identity)
const authToken = getAuthToken({ privateKeyWif, requestPath, body })
```
