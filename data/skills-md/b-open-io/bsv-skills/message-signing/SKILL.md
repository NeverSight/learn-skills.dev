---
name: message-signing
description: This skill should be used when the user asks to "sign a message", "verify a signature", "use BSM", "use BRC-77", "implement Sigma signing", "create signed messages", "authenticate with Bitcoin", or mentions message signing, signature verification, or authentication protocols on BSV.
---

# BSV Message Signing

Three approaches for message signing on BSV, from simple to full-featured.

## Quick Reference

| Approach | Package | Use Case |
|----------|---------|----------|
| **Direct SDK** | `@bsv/sdk` | Simple message signing (BSM, BRC-77) |
| **Templates** | `@bopen-io/templates` | Script parsing/creation for protocols |
| **Sigma Protocol** | `sigma-protocol` | Transaction-bound signatures |

## 1. Direct SDK Signing

For simple message authentication without transaction context.

### BSM (Bitcoin Signed Message)

```typescript
import { BSM, PrivateKey, Signature, BigNumber } from "@bsv/sdk";

const privateKey = PrivateKey.fromWif("L1...");
const message = [/* byte array */];

// Sign
const signature = BSM.sign(message, privateKey, "raw") as Signature;
const h = new BigNumber(BSM.magicHash(message));
const recovery = signature.CalculateRecoveryFactor(privateKey.toPublicKey(), h);
const compactSig = signature.toCompact(recovery, true, "base64");

// Verify - recover public key and check address
const sig = Signature.fromCompact(compactSig, "base64");
for (let r = 0; r < 4; r++) {
  try {
    const pubKey = sig.RecoverPublicKey(r, new BigNumber(BSM.magicHash(message)));
    if (BSM.verify(message, sig, pubKey)) {
      console.log("Signer:", pubKey.toAddress());
      break;
    }
  } catch { /* try next */ }
}
```

### BRC-77 (SignedMessage)

```typescript
import { SignedMessage, PrivateKey, PublicKey } from "@bsv/sdk";

const signer = PrivateKey.fromWif("L1...");
const message = [/* byte array */];

// Public signature (anyone can verify)
const sig = SignedMessage.sign(message, signer);
const valid = SignedMessage.verify(message, sig);

// Private signature (only recipient can verify)
const recipientPubKey = PublicKey.fromString("02...");
const privateSig = SignedMessage.sign(message, signer, recipientPubKey);

const recipientKey = PrivateKey.fromWif("K1...");
const privateValid = SignedMessage.verify(message, privateSig, recipientKey);
```

**See:** `examples/bsm-sign-verify.ts`, `examples/brc77-private-sig.ts`

## 2. Template-Based Signing

For working with BitCom protocols and script parsing. Uses `@bopen-io/templates`.

### Sigma Template

```typescript
import { Sigma, SigmaAlgorithm, BitCom } from "@bopen-io/templates";
import { PrivateKey, Hash } from "@bsv/sdk";

// Decode from existing script
const bitcom = BitCom.decode(script);
const sigmas = Sigma.decode(bitcom);

// Create signature (given pre-computed hashes)
const inputHash = Array.from(Hash.sha256(outpointBytes));
const dataHash = Array.from(Hash.sha256(scriptDataBytes));

const sigma = Sigma.sign(inputHash, dataHash, privateKey, {
  algorithm: SigmaAlgorithm.BRC77,  // or SigmaAlgorithm.BSM
  vin: 0
});

// Verify
const valid = sigma.verifyWithHashes(inputHash, dataHash);

// Generate locking script
const lockingScript = sigma.lock();
```

### AIP Template

```typescript
import { AIP, BitCom } from "@bopen-io/templates";

// Decode AIP from script
const bitcom = BitCom.decode(script);
const aips = AIP.decode(bitcom);

// Create AIP signature
const aip = await AIP.sign(dataBytes, privateKey, {
  algorithm: "BITCOIN_ECDSA",
  fieldIndexes: [0, 1, 2]  // optional: specific fields to sign
});

const valid = aip.verify();
```

**See:** `examples/sigma-template.ts`

**Note:** Sigma template requires `sigma-protocol` as peer dependency for Algorithm enum.

## 3. Sigma Protocol (Full Transaction Signing)

For complete transaction-bound signatures. Use when:
- Signing OP_RETURN data in transactions
- Need multiple signatures on same output
- Want automatic hash calculation from transaction context

```bash
bun add sigma-protocol
```

```typescript
import { Sigma, Algorithm } from "sigma-protocol";
import { Transaction, PrivateKey } from "@bsv/sdk";

// Create Sigma instance
const sigma = new Sigma(tx, targetVout, sigmaInstance, refVin);

// Sign with BSM (default)
const { signedTx } = sigma.sign(privateKey);

// Sign with BRC-77
const { signedTx: tx2 } = sigma.sign(privateKey, Algorithm.BRC77);

// Sign with BRC-77 for specific verifier (private)
const { signedTx: tx3 } = sigma.sign(privateKey, Algorithm.BRC77, verifierPubKey);

// Verify
const valid = sigma.verify();
const privateValid = sigma.verify(recipientPrivateKey);  // for private BRC-77
```

### Multiple Signatures

```typescript
// First signature (user with BSM)
const sigma1 = new Sigma(tx, 0, 0);
const { signedTx } = sigma1.sign(userKey, Algorithm.BSM);

// Second signature (platform with BRC-77)
const sigma2 = new Sigma(signedTx, 0, 1);
sigma2.sign(platformKey, Algorithm.BRC77);

// Verify each
sigma2.setSigmaInstance(0);
sigma2.verify();  // User

sigma2.setSigmaInstance(1);
sigma2.verify();  // Platform
```

**See:** `examples/sigma-multi-sig.ts`

## Algorithm Comparison

| Feature | BSM | BRC-77 |
|---------|-----|--------|
| Key derivation | Direct | Child key per message |
| Recovery | From signature | Embedded in signature |
| Private verify | No | Yes (with recipient key) |
| SDK module | `BSM` | `SignedMessage` |

## When to Use What

| Scenario | Approach |
|----------|----------|
| Simple message auth | Direct SDK (BSM or BRC-77) |
| BAP identity signing | `bsv-bap` library |
| Parse existing Sigma/AIP scripts | Templates |
| Build BitCom transaction outputs | Templates |
| Sign transaction OP_RETURN data | sigma-protocol |
| Multiple signatures per output | sigma-protocol |
| Platform + user dual signing | sigma-protocol |

## BAP Identity Signing (BSM)

BAP identities use BSM for signing. The `bsv-bap` library handles this:

```typescript
import { BAP } from "bsv-bap";
import { Utils } from "@bsv/sdk";
const { toArray } = Utils;

const bap = new BAP({ rootPk: wif });
const identity = bap.getId(bap.listIds()[0]);

// Sign with BSM (uses derived identity signing key)
const message = toArray("Hello World", "utf8");
const { address, signature } = identity.signMessage(message);

// Verify BSM signature
const isValid = bap.verifySignature("Hello World", address, signature);
```

A CLI is also available: `npm install -g bsv-bap` (see **`create-bap-identity`** skill).

## Sigma Signing via @1sat/actions

The `inscribe` action from `@1sat/actions` supports a `signWithBAP` parameter that applies a Sigma BSM signature using the wallet's BAP identity key. This is the recommended approach when signing inscriptions through the actions framework — it handles anchor tx construction, sigma hash computation, and broadcast automatically.

```typescript
import { inscribe, createContext } from '@1sat/actions'

const result = await inscribe.execute(ctx, {
  base64Content: btoa('Hello Sigma'),
  contentType: 'text/plain',
  signWithBAP: true,  // Signs with BAP identity via Sigma protocol
})
```

The resulting transaction carries a Sigma signature that can be verified with `sigma-protocol`:

```typescript
import { Sigma } from 'sigma-protocol'
const sigma = new Sigma(tx, 0, 0, 0)
sigma.verify() // true
```

## Additional Resources

### Reference Files

- **`references/brc-77-spec.md`** - Full BRC-77 specification
- **`references/sigma-advanced.md`** - Remote signing, hash details, advanced patterns

### Examples

- **`examples/bsm-sign-verify.ts`** - Direct BSM signing
- **`examples/brc77-private-sig.ts`** - BRC-77 private signatures
- **`examples/sigma-template.ts`** - Template-based Sigma operations
- **`examples/sigma-multi-sig.ts`** - Full sigma-protocol with multi-sig
