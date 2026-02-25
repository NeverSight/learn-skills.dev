---
name: key-derivation
description: This skill should be used when the user asks to "derive keys", "use Type42", "use BRC-42", "derive child keys", "use BIP32", "use HD keys", "create mnemonic", "convert mnemonic to key", "derive BAP identity keys", "derive encryption keys", or mentions key derivation, hierarchical deterministic wallets, invoice numbers, or child key generation on BSV.
---

# BSV Key Derivation

Two primary approaches for deriving keys on BSV, plus mnemonic support.

## Quick Reference

| Method | Package | Use Case |
|--------|---------|----------|
| **Type42 (BRC-42)** | `@bsv/sdk` | Modern: privacy-preserving, counterparty derivation |
| **BIP32 (BRC-32)** | `@bsv/sdk` | Legacy: HD wallets, sequential paths |
| **Mnemonic** | `@bsv/sdk` | Seed phrase to master key conversion |

## 1. Type42 Key Derivation (Recommended)

Modern approach using ECDH shared secrets. Provides enhanced privacy and unlimited key derivation.

### Basic Usage

```typescript
import { PrivateKey, PublicKey } from "@bsv/sdk";

const masterKey = PrivateKey.fromWif("L1...");
const counterpartyPubKey = masterKey.toPublicKey(); // or another party's key

// Derive child key using invoice number
const childKey = masterKey.deriveChild(counterpartyPubKey, "invoice-123");
const childAddress = childKey.toPublicKey().toAddress();
```

### Invoice Number Format (BRC-43)

For protocol-specific derivations, use the format: `{securityLevel}-{protocol}-{keyId}`

```typescript
// BAP identity signing key
const bapKey = masterKey.deriveChild(masterKey.toPublicKey(), "1-bap-identity");

// Encryption key
const encKey = masterKey.deriveChild(masterKey.toPublicKey(), "2-encryption-default");
```

### Counterparty Derivation

Type42 enables deriving shared keys between parties without revealing private keys:

```typescript
// Alice derives key for Bob
const aliceKey = PrivateKey.fromWif("L1...");
const bobPubKey = PublicKey.fromString("02...");
const sharedKey = aliceKey.deriveChild(bobPubKey, "payment-001");

// Bob derives same address using his private key and Alice's public key
const bobKey = PrivateKey.fromWif("K1...");
const alicePubKey = aliceKey.toPublicKey();
const bobDerived = bobKey.deriveChild(alicePubKey, "payment-001");
// bobDerived.toPublicKey().toAddress() === sharedKey.toPublicKey().toAddress()
```

### Key Advantages

- Privacy: ECDH shared secrets prevent address reuse detection
- Flexibility: Any string as invoice number (no 2^31 limit)
- Auditability: Reveal shared secret to specific parties only
- No public derivation: Enhanced security vs BIP32

## 2. BIP32 HD Key Derivation (Legacy)

Traditional hierarchical deterministic derivation for compatibility.

### Basic Usage

```typescript
import { HD } from "@bsv/sdk";

// From extended private key
const hdKey = HD.fromString("xprv9s21ZrQH143K...");

// Derive child at path
const child = hdKey.derive("m/44'/0'/0'/0/0");
const address = child.pubKey.toAddress();
const privateKey = child.privKey;
```

### Path Format

- `m` = master key
- Numbers = child index (0 to 2^31-1)
- Apostrophe (`'`) = hardened derivation

```typescript
// Standard wallet paths
const receiving = hdKey.derive("m/44'/236'/0'/0/0");   // BSV receiving
const change = hdKey.derive("m/44'/236'/0'/1/0");     // BSV change

// BAP identity path
const bapRoot = hdKey.derive("m/424150'/0'/0'");      // 424150 = BAP in decimal
```

### From Mnemonic

```typescript
import { Mnemonic, HD } from "@bsv/sdk";

const mnemonic = Mnemonic.fromString("word1 word2 word3...");
const seed = mnemonic.toSeed();
const hdKey = HD.fromSeed(seed);
```

## 3. Mnemonic to Single Master Key

For Type42, convert mnemonic to a single master key (not extended key):

```typescript
import { Mnemonic, Hash, PrivateKey, Utils } from "@bsv/sdk";
const { toHex } = Utils;

const mnemonic = Mnemonic.fromString("dial tunnel valid cry exhaust...");
const seed = mnemonic.toSeed();

// SHA256 of seed produces 256-bit private key
const keyBytes = Hash.sha256(seed);
const masterKey = PrivateKey.fromString(toHex(keyBytes), "hex");

// Use with Type42 derivation
const childKey = masterKey.deriveChild(masterKey.toPublicKey(), "bap:0");
```

This approach:
- Maintains familiar mnemonic backup
- Produces single key for Type42 (not HD extended key)
- Remains compatible with existing BIP39 mnemonics

## Choosing Between Methods

| Scenario | Recommended |
|----------|-------------|
| New wallet/identity system | Type42 |
| Privacy-preserving payments | Type42 |
| Counterparty key agreement | Type42 |
| Legacy wallet compatibility | BIP32 |
| Sequential address generation | BIP32 |
| Migration from existing HD wallet | Both (see migration) |

## BAP Identity Key Derivation

BAP uses a two-level derivation hierarchy:

```typescript
// Level 1: Member key from path
const memberKey = masterKey.deriveChild(masterKey.toPublicKey(), "bap:0");

// Level 2: Identity signing key using BAP invoice number
const signingKey = memberKey.deriveChild(memberKey.toPublicKey(), "1-bap-identity");
const signingAddress = signingKey.toPublicKey().toAddress();
```

For BIP32 legacy:
```typescript
const memberHD = hdKey.derive("m/424150'/0'/0'/0/0/0");
// Then apply Type42 for signing key
const signingKey = memberHD.privKey.deriveChild(memberHD.pubKey, "1-bap-identity");
```

## Security Considerations

1. **Never expose master keys**: Derive child keys for operations
2. **Use hardened paths** for BIP32 when privacy matters (apostrophe)
3. **Type42 prevents public derivation**: Cannot derive child public keys from parent public key alone
4. **Invoice numbers are not secret**: They can be shared

## bsv-bap Library

The `bsv-bap` library implements Type42 with BRC-43 invoice numbers for BAP identities:

```typescript
import { BAP } from "bsv-bap";
import { PrivateKey } from "@bsv/sdk";

const bap = new BAP({ rootPk: PrivateKey.fromRandom().toWif() });
const identity = bap.newId("Alice");

// Signing key derived with "1-bap-identity"
const { address, signature } = identity.signMessage(messageBytes);

// Friend encryption key derived with "2-friend-{sha256(friendBapId)}"
const friendPubKey = identity.getEncryptionPublicKeyWithSeed(friendBapId);
const ciphertext = identity.encryptWithSeed("secret", friendBapId);
```

A CLI is also available: `npm install -g bsv-bap` (see **`create-bap-identity`** skill).

## Official Specifications

All BSV key derivation standards are documented at:

**https://bsv.brc.dev/key-derivation**

Key specifications:
- **BRC-42**: Type42 key derivation scheme
- **BRC-32**: BIP32 HD key derivation
- **BRC-43**: Security levels, protocol IDs, key IDs
- **BRC-69**: Revealing key linkages
- **BRC-72**: Protecting key linkage information

## Additional Resources

### Reference Files

- **`references/brc-42-type42.md`** - Complete Type42 specification and advanced patterns
- **`references/brc-32-bip32.md`** - BIP32 legacy derivation details
- **`references/bap-derivation.md`** - BAP identity key derivation patterns and migration

### Examples

- **`examples/type42-derivation.ts`** - Type42 counterparty key derivation
- **`examples/bip32-wallet.ts`** - BIP32 HD wallet with standard paths
- **`examples/mnemonic-to-type42.ts`** - Convert mnemonic to Type42 master key
