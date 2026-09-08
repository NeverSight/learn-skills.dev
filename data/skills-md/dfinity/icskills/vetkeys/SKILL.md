---
name: vetkeys
description: "Build vetKeys cryptography on the Internet Computer via the vetKD system API and the ic-vetkeys (Rust, Motoko) and @icp-sdk/vetkeys (frontend) libraries: identity-based encryption (IBE), threshold BLS signatures, timelock encryption, symmetric key derivation, and offline public-key derivation. Use when implementing IBE, encrypting to a principal, BLS signing, sealed-bid or timelock schemes, deriving encryption keys on-chain, transport keys, or calling vetkd_public_key / vetkd_derive_key. For access-controlled encrypted key-value storage (password managers, encrypted notes), use the encrypted-maps skill instead. Not for authentication — use internet-identity."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2"
metadata:
  title: vetKeys
  category: Security
---

# vetKeys (Verifiable Encrypted Threshold Keys)

vetKeys bring on-chain privacy to the IC via the **vetKD** protocol: a canister requests a key derived by the subnet's threshold key-derivation infrastructure, receives it **encrypted** under a client-supplied transport key, and only the client decrypts it locally. No subnet node ever sees the raw key, and in this standard client-delivery pattern neither does the canister — it relays the still-encrypted key to the client. (Some flows deliberately have the canister obtain key material itself: threshold BLS signing and in-canister timelock decryption — see those sections.) Derivation is **deterministic**: the same `(canister, context, input)` always yields the same key.

Build on the maintained libraries — do not hand-roll the cryptography or the Candid interface:

| Layer | Rust | Motoko | Frontend |
|-------|------|--------|----------|
| Package | `ic-vetkeys` **0.9** ([crates.io](https://crates.io/crates/ic-vetkeys)) | `ic-vetkeys` **0.6** ([mops](https://mops.one/ic-vetkeys)) | `@icp-sdk/vetkeys` **0.5** ([npm](https://www.npmjs.com/package/@icp-sdk/vetkeys)) |
| Management API | `ic-cdk-management-canister`, `ic_vetkeys::management_canister` | `mo:ic-vetkeys/ManagementCanister` | — |
| Low-level primitives | crate root (`ic_vetkeys::…`) | — (**not available**, see below) | package root (`@icp-sdk/vetkeys`) |

> **`@dfinity/vetkeys` is legacy** (frozen at 0.4.0). The package was renamed to `@icp-sdk/vetkeys` at 0.5.0. Frontend agent/identity types come from `@icp-sdk/core` (`@icp-sdk/core/agent`, `@icp-sdk/core/principal`), **not** `@dfinity/agent`/`@dfinity/principal`.

Also required: Rust `ic-cdk = "0.20"` + `ic-cdk-management-canister = "0.1"` (and `ic-dummy-getrandom-for-wasm` for IBE); Motoko `ic-vetkeys` 0.6 needs `moc ≥ 1.13.0` / `core ≥ 2.6.1`; frontend also `@icp-sdk/core ^5.4`.

## Which skill / which feature

| You want to… | Use |
|--------------|-----|
| Store & share encrypted key-value data (password manager, notes, vault) | **`encrypted-maps` skill** (higher-level, start there) |
| Encrypt to a principal so only they can decrypt (messaging) | **IBE** → `references/ibe.md` |
| Reveal data only after a deadline (sealed-bid auction, timelock) | **Timelock IBE** → `references/ibe.md` |
| Have the canister produce a signature verifiable by anyone | **Threshold BLS** → `references/bls-signing.md` |
| Derive a per-user/per-resource symmetric (AES) key | **Symmetric derivation** → this file |
| Encrypt to a principal without any canister call | **Offline public-key derivation** → this file |
| Produce on-chain verifiable randomness | **Verifiable randomness (VRF)** → this file |
| Authenticate users / logins | not vetKeys — use the **`internet-identity` skill** |

## Core concepts

- **context** — a domain-separator blob that namespaces derived keys within a canister (e.g. `"my_app"`, or a per-purpose value like `"symmetric_key"`). It **must be identical** between the public-key call, the derive call, and any client-side verify/decrypt, or the keys will not match — `decryptAndVerify` then throws (the Rust APIs return an error), so handle that failure rather than assuming success.
- **input** — application data identifying *which* key to derive (e.g. a caller principal, a document ID). It is sent to the management canister **in plaintext** — use it as an identifier, never for secret data.
- **transport key** — an ephemeral key pair the client generates per request. The public half is sent so the subnet can encrypt the derived key for delivery; only the holder of the secret half can decrypt. Generate a **fresh** one each request (`TransportSecretKey.random()`).
- **encrypted vs unencrypted vetKeys** — IBE and symmetric derivation use the **encrypted** delivery flow (transport key → `decryptAndVerify` → `VetKey`). Threshold BLS uses the **unencrypted** vetKey directly; the library's `sign_with_bls` / `signWithBls` handles that — never feed an encrypted vetKey into BLS.
- **Motoko asymmetry** — the Motoko `ic-vetkeys` library exposes only the management API + `KeyManager`/`EncryptedMaps`. It has **no** IBE, transport keys, `MasterPublicKey`/`DerivedPublicKey`, or vetKey decryption. In a Motoko app the canister returns the *encrypted* vetKey and the **frontend** (`@icp-sdk/vetkeys`) does transport-key generation, `decryptAndVerify`, IBE, and symmetric derivation. Those primitives exist in Rust and TypeScript only.

### Key names & cycles

| Key name | Where | `vetkd_derive_key` cost |
|----------|-------|-------------------------|
| `test_key_1` | local + mainnet (testing) | 10_000_000_000 |
| `key_1` | local + mainnet (production) | 26_153_846_153 |

`vetkd_public_key` is **free**; `vetkd_derive_key` costs cycles. `test_key_1` and `key_1` behave the same locally and on mainnet. Let the helpers handle the amount: the Rust binding computes the exact cost, and the Motoko `ManagementCanister` attaches `26_153_846_153` with any excess refunded — you only need to keep the canister funded. The management canister is `aaaaa-aa`; calls are routed to the subnet holding the master key.

- **Rust** reads the key name from an `#[init]` argument (passed via `init_args` in `icp.yaml`).
- **Motoko** reads it from the `VETKD_KEY_NAME` canister environment variable, defaulting to `test_key_1`. The name is captured into stable state at first install and is **immutable** for the life of the canister's data — changing it later is silently ignored (only a `reinstall`, which drops state, switches keys). Because `test_key_1` is also a valid mainnet key, a production deploy that forgets to set `VETKD_KEY_NAME` silently runs on it — assert the expected key at deploy time if that matters.

## The vetKD management API (foundation + symmetric encryption)

The management API has two endpoints: `vetkd_public_key` (verification / offline-encryption public key) and `vetkd_derive_key` (the caller's encrypted key). This is the foundation for symmetric encryption, IBE, and BLS. Call it through the library helpers so the Candid types and cycles are correct.

### Backend — Rust

```rust
use ic_cdk::update;
use ic_cdk_management_canister::{VetKDCurve, VetKDDeriveKeyArgs, VetKDKeyId, VetKDPublicKeyArgs};

const CONTEXT: &[u8] = b"symmetric_key"; // domain separator; must match on the client

fn key_id() -> VetKDKeyId {
    // name comes from an #[init] arg in real code; "test_key_1" for local + mainnet testing
    VetKDKeyId { curve: VetKDCurve::Bls12_381_G2, name: "test_key_1".to_string() }
}

#[update]
async fn symmetric_verification_key() -> Vec<u8> {
    let res = ic_cdk_management_canister::vetkd_public_key(&VetKDPublicKeyArgs {
        canister_id: None, // defaults to this canister
        context: CONTEXT.to_vec(),
        key_id: key_id(),
    })
    .await
    .expect("vetkd_public_key failed");
    res.public_key // no cycles required
}

#[update]
async fn encrypted_symmetric_key_for_caller(transport_public_key: Vec<u8>) -> Vec<u8> {
    let caller = ic_cdk::api::msg_caller(); // capture BEFORE the await
    let res = ic_cdk_management_canister::vetkd_derive_key(&VetKDDeriveKeyArgs {
        input: caller.as_slice().to_vec(), // key identifier (plaintext) — never secret data
        context: CONTEXT.to_vec(),
        transport_public_key,
        key_id: key_id(),
    })
    .await // the binding attaches the required cycles automatically
    .expect("vetkd_derive_key failed");
    res.encrypted_key
}
```

### Backend — Motoko

```motoko
import ManagementCanister "mo:ic-vetkeys/ManagementCanister";
import Principal "mo:core/Principal";
import Text "mo:core/Text";
import Runtime "mo:core/Runtime";

persistent actor {
  // Captured into keyId at first install and fixed for the life of the canister's derived keys;
  // changing VETKD_KEY_NAME on a later upgrade has no effect (see the key-name warning above).
  let keyName = Runtime.envVar<system>("VETKD_KEY_NAME") ?? "test_key_1";
  let keyId : ManagementCanister.VetKdKeyid = { curve = #bls12_381_g2; name = keyName };

  public shared func symmetricVerificationKey() : async Blob {
    // context / domain separator; no cycles required
    await ManagementCanister.vetKdPublicKey(null, Text.encodeUtf8("symmetric_key"), keyId);
  };

  public shared ({ caller }) func encryptedSymmetricKeyForCaller(transportPublicKey : Blob) : async Blob {
    // signature is (input, context, keyId, transportPublicKey); helper attaches cycles automatically
    await ManagementCanister.vetKdDeriveKey(
      Principal.toBlob(caller), Text.encodeUtf8("symmetric_key"), keyId, transportPublicKey);
  };
};
```

### Frontend — derive an AES-GCM key (TypeScript)

The canister returns the *encrypted* vetKey; the frontend generates the transport key, decrypts & verifies it into a `VetKey`, then derives AES-GCM key material.

```typescript
import { TransportSecretKey, DerivedPublicKey, EncryptedVetKey } from "@icp-sdk/vetkeys";
// `backend` is your actor; `myPrincipal` is the authenticated caller's Principal (@icp-sdk/core/principal)

// 1. Fresh transport key per request
const tsk = TransportSecretKey.random();

// 2. Fetch the encrypted derived key + the public verification key
const [encryptedKeyBytes, publicKeyBytes] = await Promise.all([
  backend.encrypted_symmetric_key_for_caller(tsk.publicKeyBytes()),
  backend.symmetric_verification_key(),
]);

// 3. Decrypt & verify -> VetKey. The identity bytes MUST equal the backend `input`
//    (here the caller principal), or verification throws.
const vetKey = EncryptedVetKey.deserialize(new Uint8Array(encryptedKeyBytes)).decryptAndVerify(
  tsk,
  DerivedPublicKey.deserialize(new Uint8Array(publicKeyBytes)),
  myPrincipal.toUint8Array(),
);

// 4. Derive AES-GCM key material and encrypt/decrypt. There is NO `toDerivedKeyMaterial()`.
const keyMaterial = await vetKey.asDerivedKeyMaterial();
const domainSep = "my_app:notes"; // unique per app + usage
const ciphertext = await keyMaterial.encryptMessage("secret message", domainSep, ""); // (msg, domainSep, associatedData)
const plaintext = await keyMaterial.decryptMessage(ciphertext, domainSep, "");
// new TextDecoder().decode(plaintext) === "secret message"
```

## Offline public-key derivation

Derive a canister's public key for a context **without any canister call**, starting from the known mainnet master public key. Used to encrypt (IBE) to a principal when neither the recipient nor the canister is online.

**TypeScript:**

```typescript
import { MasterPublicKey } from "@icp-sdk/vetkeys";
import { Principal } from "@icp-sdk/core/principal";

const derivedPublicKey = MasterPublicKey.productionKey()            // key_1 (default); MasterPublicKey.pocketicKey() for local
  .deriveCanisterKey(Principal.fromText(canisterId).toUint8Array())
  .deriveSubKey(new TextEncoder().encode("my_app"));               // the context / domain separator
// derivedPublicKey (a DerivedPublicKey) can now be used for IBE encryption offline
```

**Rust:**

```rust
use ic_vetkeys::{MasterPublicKey, DerivedPublicKey};
use ic_cdk_management_canister::{VetKDCurve, VetKDKeyId};

let master = MasterPublicKey::for_mainnet_key(&VetKDKeyId {
    curve: VetKDCurve::Bls12_381_G2,
    name: "key_1".to_string(),
}).expect("unknown key name");                     // for_pocketic_key(..) for local
let derived: DerivedPublicKey = master
    .derive_canister_key(canister_id.as_slice())
    .derive_sub_key(b"my_app");
```

## Verifiable randomness (VRF)

A vetKey can be turned into **verifiable randomness**: a Rust canister calls `ic_vetkeys::management_canister::compute_vrf(input, context, key_id) -> VrfOutput` (scope `input`/`context` to the draw, e.g. a lottery round or leader election), and the frontend verifies the proof with `VrfOutput.deserialize(...)` from `@icp-sdk/vetkeys`. No canonical end-to-end example ships yet. (Not available in the Motoko library — derive on a Rust canister.)

## Pitfalls

1. **Wrong package / imports.** Use `@icp-sdk/vetkeys` (≥0.5), not `@dfinity/vetkeys` (frozen at 0.4). Import agent/identity from `@icp-sdk/core` (`@icp-sdk/core/agent`, `@icp-sdk/core/principal`), and build the agent with `await HttpAgent.create({ identity, host, rootKey })` — the client classes take a ready `HttpAgent`, not options. Get `rootKey` from `safeGetCanisterEnv()` (`@icp-sdk/core/agent/canister-env`); never call `fetchRootKey()` in shipped code (see the `icp-cli` skill).

2. **`toDerivedKeyMaterial()` does not exist.** For symmetric encryption: `const dkm = await vetKey.asDerivedKeyMaterial()`, then `await dkm.encryptMessage(msg, domainSep, associatedData)` / `await dkm.decryptMessage(ct, domainSep, associatedData)` (all async). Never use the raw decrypted vetKey bytes directly as an AES key.

3. **Don't hand-roll the management interface.** Rust: `ic-cdk-management-canister` (`vetkd_public_key`/`vetkd_derive_key`) or `ic_vetkeys::management_canister` (also `sign_with_bls`). Motoko: `mo:ic-vetkeys/ManagementCanister` (`vetKdPublicKey`, `vetKdDeriveKey`, `signWithBls`, `blsPublicKey`). These carry the correct Candid types and attach the right cycles automatically. Hand-declaring `actor "aaaaa-aa"` and the `vetkd_*` records is unnecessary and error-prone.

4. **Motoko has no low-level crypto.** No IBE, transport keys, `MasterPublicKey`/`DerivedPublicKey`, or vetKey decryption in the Motoko library. The Motoko canister returns the *encrypted* vetKey; the frontend `@icp-sdk/vetkeys` (or a Rust off-chain client) does the rest.

5. **Fund the canister for derivations.** `vetkd_derive_key` costs cycles (`key_1` = 26_153_846_153, `test_key_1` = 10_000_000_000 — the same locally and on mainnet); `vetkd_public_key` is free. Let the helpers attach the amount — the Rust binding computes the exact cost, the Motoko helper attaches 26_153_846_153 and the excess is refunded — and keep the canister topped up.

6. **`context` and `input` must match end to end.** A different `context` (or a different `input`) produces a different key; `decryptAndVerify` then throws (the Rust APIs return an error) rather than returning wrong plaintext — handle it, and keep `context`/`input` byte-identical across public-key, derive, and client verify/decrypt.

7. **`input` is plaintext.** It is a key identifier sent to the management canister — use IDs (principal, document ID), never secret data.

8. **Capture the caller before `await`.** `ic_cdk::api::msg_caller()` (Rust) / destructure `({ caller })` (Motoko) before the async derive call.

9. **Enforce authorization when hand-rolling derivation.** If you call `vetkd_derive_key` directly (not via `KeyManager`/`EncryptedMaps`), the canister must ensure it only derives for an `input` the caller is entitled to (e.g. their own principal). Otherwise any caller can obtain anyone's key.

10. **BLS uses the unencrypted key.** Use `sign_with_bls`/`signWithBls`; don't feed an encrypted vetKey into BLS, and don't reuse the same `context`/`input` across IBE and BLS.

11. **Rust randomness on Wasm.** IBE seeds need randomness; add `ic-dummy-getrandom-for-wasm` (or a `getrandom` wasm shim) or the canister traps. (The frontend uses WebCrypto — fine.)

12. **Modern ic-cdk call API.** Use `ic_cdk::api::msg_caller()` (not `ic_cdk::caller()`). If you ever call the management canister without the binding, use `ic_cdk::call::Call::unbounded_wait(..).with_cycles(..)` — the legacy `ic_cdk::api::call::call*` API is removed in ic-cdk 0.20+.

## Feature guides

- **Identity-Based Encryption (IBE) & timelock** — encrypt with `IbeCiphertext.encrypt(publicKey, IbeIdentity.fromPrincipal(recipient), plaintext, IbeSeed.random())`; the recipient decrypts with `IbeCiphertext.deserialize(ct).decrypt(vetKey)`. Full backend + frontend + timelock: `references/ibe.md`.
- **Threshold BLS signatures** — sign with `ic_vetkeys::management_canister::sign_with_bls` (Rust) / `ManagementCanister.signWithBls` (Motoko); verify with `verifyBlsSignature(derivedPublicKey, message, signature)`. Details: `references/bls-signing.md`.
- **Encrypted key-value storage (EncryptedMaps / KeyManager)** — the **`encrypted-maps`** skill.

## Deploy & verify

Provisioning, `icp.yaml`, and generic deploy steps belong to the **`icp-cli`** skill. vetKeys-specific checks:

```bash
icp deploy backend                                    # local replica provisions test_key_1
icp canister call backend symmetric_verification_key '()'   # non-empty BLS public-key blob
# derive needs a 48-byte transport public key from the frontend; different callers get different keys
```
