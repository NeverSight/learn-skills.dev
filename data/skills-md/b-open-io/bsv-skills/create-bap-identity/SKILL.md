---
name: create-bap-identity
description: This skill should be used when the user asks to "create BAP identity", "new BAP", "Type42 identity", "Legacy BAP identity", "generate BAP", "set up BAP identity", "initialize BAP", or needs to create Bitcoin Attestation Protocol identities using the bap CLI.
---

# Create BAP Identity

Create and manage BAP (Bitcoin Attestation Protocol) identities using the `bsv-bap` library.

## Installation

```bash
bun add bsv-bap @bsv/sdk
```

## Creating an Identity

```typescript
import { BAP } from "bsv-bap";
import { PrivateKey } from "@bsv/sdk";

// Create BAP instance with new key
const privateKey = PrivateKey.fromRandom();
const bap = new BAP({ rootPk: privateKey.toWif() });

// Create identity
const identity = bap.newId("Alice Smith");

console.log("Identity Key:", identity.getIdentityKey());
console.log("Root Address:", identity.rootAddress);
console.log("Signing Address:", identity.getCurrentAddress());
```

## Key Derivation

BAP uses Type42 (BRC-42) key derivation with BRC-43 invoice numbers:

| Purpose | Invoice Number | Security Level |
|---------|---------------|----------------|
| Signing key | `1-bap-identity` | 1 (public protocol) |
| Friend encryption | `2-friend-{sha256(friendBapId)}` | 2 (user-approved) |

## Signing Messages

```typescript
import { Utils } from "@bsv/sdk";
const { toArray } = Utils;

// Sign a message
const message = toArray("Hello World", "utf8");
const { address, signature } = identity.signMessage(message);

// Verify (on any BAP instance)
const isValid = bap.verifySignature("Hello World", address, signature);
```

## Friend Encryption

Derive friend-specific encryption keys for private communication:

```typescript
// Get encryption pubkey for a friend (share in friend requests)
const friendPubKey = identity.getEncryptionPublicKeyWithSeed(friendBapId);

// Encrypt data for friend
const ciphertext = identity.encryptWithSeed("secret message", friendBapId);

// Decrypt data from friend
const plaintext = identity.decryptWithSeed(ciphertext, friendBapId);
```

## Export/Import

```typescript
// Export for backup
const backup = bap.exportForBackup("My Identity");
// { ids: "...", createdAt: "...", rootPk: "..." }

// Import from backup
const bap2 = new BAP({ rootPk: backup.rootPk });
bap2.importIds(backup.ids);
```

## CLI Option

For quick operations, the `bsv-bap` package includes a CLI:

```bash
npm install -g bsv-bap

bap create --name "Alice"     # Create identity (~/.bap/identity.json)
bap sign "Hello World"        # Sign message
bap verify "msg" "sig" "addr" # Verify signature
bap info                      # Show identity info
bap friend-pubkey <bapId>     # Get friend encryption pubkey
bap encrypt <data> <bapId>    # Encrypt for friend
bap decrypt <text> <bapId>    # Decrypt from friend
bap export                    # Export backup JSON
bap import <file>             # Import from backup
```

## Next Steps

After creating an identity:
1. Sign messages for authentication
2. Share encryption pubkeys in friend requests
3. Publish identity to blockchain for on-chain reputation
4. Integrate with Sigma Identity for OAuth (`@sigma-auth/better-auth-plugin`)

## Related Skills

- **`key-derivation`** - Type42 and BRC-43 key derivation patterns
- **`message-signing`** - BSM, BRC-77, and Sigma signing protocols
- **`encrypt-decrypt-backup`** - bitcoin-backup CLI for .bep encrypted backups
