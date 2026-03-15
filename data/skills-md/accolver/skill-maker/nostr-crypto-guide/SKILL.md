---
name: nostr-crypto-guide
description: Guide implementation of Nostr cryptographic operations including NIP-44 encrypted payloads, NIP-59 gift wrap privacy layers, NIP-49 private key encryption (ncryptsec), NIP-06 key derivation from mnemonic, and NIP-46 remote signing. Use when implementing encrypted DMs, private messaging, key backup/export, mnemonic-based key generation, or remote signer integration in Nostr applications.
---

# Nostr Crypto Guide

## Overview

Implement Nostr's cryptographic primitives correctly. This skill covers the five
crypto-related NIPs that agents consistently get wrong: key derivation (NIP-06),
payload encryption (NIP-44), gift wrapping for metadata privacy (NIP-59),
private key encryption for backup (NIP-49), and remote signing (NIP-46).

## When to Use

- Implementing NIP-44 encrypted payloads between two Nostr users
- Building NIP-59 gift-wrapped private messages (rumor/seal/wrap layers)
- Encrypting a private key for backup or export (NIP-49 ncryptsec)
- Deriving Nostr keys from a BIP39 mnemonic seed phrase (NIP-06)
- Integrating a remote signer / bunker via NIP-46
- Debugging encryption/decryption failures in Nostr messaging
- Choosing between NIP-04 (deprecated) and NIP-44 encryption

**Do NOT use when:**

- Working with relay WebSocket protocol or subscription filters
- Building event structures or tag arrays (use nostr-event-builder)
- Implementing NIP-19 bech32 encoding (npub/nsec/note) without crypto context
- General secp256k1 or Schnorr signature questions unrelated to Nostr

## Workflow

### 1. Identify the Crypto Operation

Ask: "What cryptographic operation does the developer need?"

| Intent                                  | NIP    | Key Function                   |
| --------------------------------------- | ------ | ------------------------------ |
| Encrypt a message between two users     | NIP-44 | `conversation_key` + `encrypt` |
| Send a private DM with metadata privacy | NIP-59 | rumor -> seal -> gift wrap     |
| Encrypt a private key for backup        | NIP-49 | scrypt + XChaCha20-Poly1305    |
| Derive keys from mnemonic               | NIP-06 | BIP39 + BIP32 derivation       |
| Sign events without exposing privkey    | NIP-46 | Remote signer via kind:24133   |

### 2. NIP-06 — Key Derivation from Mnemonic

BIP39 mnemonic words produce a binary seed, then BIP32 derives the Nostr key.

**Derivation path:** `m/44'/1237'/<account>'/0/0`

- Coin type `1237` is Nostr's SLIP-44 registration
- Use `account = 0` for a single identity
- Increment `account` for multiple identities from one seed

**Steps:**

1. Validate the mnemonic (12 or 24 words from BIP39 wordlist)
2. Convert mnemonic to binary seed via BIP39 (with optional passphrase)
3. Derive the private key at path `m/44'/1237'/0'/0/0`
4. The 32-byte private key is the Nostr secret key
5. Compute the public key via secp256k1 (x-only, 32 bytes)

**Test vector:**

```
mnemonic: leader monkey parrot ring guide accident before fence cannon height naive bean
privkey:  7f7ff03d123792d6ac594bfa67bf6d0c0ab55b6b1fdb6249303fe861f1ccba9a
pubkey:   17162c921dc4d2518f9a101db33695df1afb56ab82f5ff3e5da6eec3ca5cd917
nsec:     nsec10allq0gjx7fddtzef0ax00mdps9t2kmtrldkyjfs8l5xruwvh2dq0lhhkp
npub:     npub1zutzeysacnf9rru6zqwmxd54mud0k44tst6l70ja5mhv8jjumytsd2x7nu
```

### 3. NIP-44 — Encrypted Payloads (Version 2)

NIP-44v2 is the current standard for encrypting data between two Nostr users. It
replaces NIP-04 (deprecated, insecure). See
[references/nip44-encryption.md](references/nip44-encryption.md) for full
pseudocode.

**Encryption flow:**

1. **Conversation key** (one-time per pair):
   - ECDH: `shared_x = secp256k1_ecdh(privkey_a, pubkey_b)` (unhashed 32-byte
     x-coordinate)
   - `conversation_key = hkdf_extract(sha256, IKM=shared_x, salt="nip44-v2")`
   - Symmetric: `conv(a, B) == conv(b, A)`

2. **Per-message encryption:**
   - Generate 32-byte random nonce (CSPRNG, never reuse)
   - `hkdf_expand(conversation_key, nonce, 76)` ->
     `chacha_key(32) | chacha_nonce(12) | hmac_key(32)`
   - Pad plaintext: power-of-2 scheme, min 32 bytes, max 65535 bytes
   - Encrypt padded plaintext with ChaCha20
   - MAC: `hmac_sha256(hmac_key, nonce || ciphertext)`
   - Output: `base64(version_byte(0x02) || nonce(32) || ciphertext || mac(32))`

3. **Decryption:**
   - **CRITICAL: Validate the outer event's signature BEFORE decrypting**
   - Decode base64, extract version + nonce + ciphertext + mac
   - Recompute conversation key and message keys
   - Verify MAC (constant-time comparison)
   - Decrypt with ChaCha20, remove padding

**Padding algorithm:**

```
calc_padded_len(unpadded_len):
  if unpadded_len <= 32: return 32
  next_power = 1 << (floor(log2(unpadded_len - 1)) + 1)
  chunk = 32 if next_power <= 256 else next_power / 8
  return chunk * (floor((unpadded_len - 1) / chunk) + 1)
```

Padded format: `[plaintext_length: u16_be][plaintext][zero_padding]`

### 4. NIP-59 — Gift Wrap (Privacy Layer)

Three nested layers provide metadata privacy for messages. See
[references/gift-wrap-flow.md](references/gift-wrap-flow.md) for the complete
flow with code examples.

**Layer 1 — Rumor (unsigned event):**

- The actual content (e.g., a kind:1 message)
- Has `id` and `pubkey` but NO `sig`
- Deniable: cannot be verified if leaked

**Layer 2 — Seal (kind:13):**

- `content`: rumor encrypted with NIP-44 to recipient's pubkey
- Signed by the real author
- Tags MUST be empty (`[]`)
- `created_at` SHOULD be randomized (up to 2 days in past)
- Reveals: who signed it. Hides: content, recipient

**Layer 3 — Gift Wrap (kind:1059):**

- `content`: seal encrypted with NIP-44 using a random ephemeral key
- Signed by the random ephemeral key (one-time use)
- Tags: `[["p", "<recipient_pubkey>"]]` for routing
- `created_at` SHOULD be randomized (up to 2 days in past)
- Reveals: recipient (via p-tag). Hides: author, content

**Construction steps:**

```
1. Create rumor = { kind, content, tags, pubkey: author, created_at }
   Compute id = sha256(serialize(rumor))
   Do NOT sign

2. Create seal = {
     kind: 13,
     content: nip44_encrypt(JSON.stringify(rumor), author_privkey, recipient_pubkey),
     created_at: random_past_timestamp(),
     tags: [],
     pubkey: author_pubkey
   }
   Sign seal with author_privkey

3. Generate ephemeral_key = random_keypair()
   Create wrap = {
     kind: 1059,
     content: nip44_encrypt(JSON.stringify(seal), ephemeral_privkey, recipient_pubkey),
     created_at: random_past_timestamp(),
     tags: [["p", recipient_pubkey]],
     pubkey: ephemeral_pubkey
   }
   Sign wrap with ephemeral_privkey

4. Send wrap to recipient's relays. Discard ephemeral_key.
```

**Unwrapping (recipient):**

```
1. Decrypt wrap.content with NIP-44 using (recipient_privkey, wrap.pubkey)
   -> seal (JSON)
2. Verify seal.sig against seal.pubkey
3. Decrypt seal.content with NIP-44 using (recipient_privkey, seal.pubkey)
   -> rumor (JSON)
4. Verify rumor.pubkey matches seal.pubkey (author consistency)
5. rumor.content is the actual message
```

### 5. NIP-49 — Private Key Encryption (ncryptsec)

Encrypt a Nostr private key with a password for safe backup/export.

**Encryption steps:**

1. Normalize password to NFKC unicode form
2. Generate 16 random bytes for salt
3. Choose `log_n` (scrypt cost parameter):
   - `16` = 64 MiB, ~100ms (minimum recommended)
   - `20` = 1 GiB, ~2s (good default)
   - `22` = 4 GiB (high security)
4. Derive symmetric key: `scrypt(password_nfkc, salt, log_n, r=8, p=1)` -> 32
   bytes
5. Generate 24-byte random nonce
6. Set key security byte:
   - `0x00` = key was handled insecurely (copy/paste, stored plaintext)
   - `0x01` = key was handled securely
   - `0x02` = unknown/untracked
7. Encrypt:
   `XChaCha20-Poly1305(plaintext=privkey_32bytes, aad=key_security_byte, nonce, key=symmetric_key)`
8. Concatenate:
   `version(0x02) || log_n || salt(16) || nonce(24) || aad(1) || ciphertext(48)`
   - Total: 91 bytes before bech32 encoding
9. Encode: `bech32("ncryptsec", concatenated_bytes)`

**Decryption:**

1. Decode bech32 with "ncryptsec" prefix
2. Parse: version, log_n, salt, nonce, key_security_byte, ciphertext
3. Normalize password to NFKC
4. Derive key: `scrypt(password_nfkc, salt, log_n, r=8, p=1)`
5. Decrypt: `XChaCha20-Poly1305(ciphertext, aad=key_security_byte, nonce, key)`
6. Result is the 32-byte private key

**Test vector:**

```
ncryptsec: ncryptsec1qgg9947rlpvqu76pj5ecreduf9jxhselq2nae2kghhvd5g7dgjtcxfqtd67p9m0w57lspw8gsq6yphnm8623nsl8xn9j4jdzz84zm3frztj3z7s35vpzmqf6ksu8r89qk5z2zxfmu5gv8th8wclt0h4p
password: nostr
log_n: 16
privkey: 3501454135014541350145413501453fefb02227e449e57cf4d3a3ce05378683
```

### 6. NIP-46 — Remote Signing

Remote signing keeps the private key on a dedicated signer (hardware device,
server, mobile app) while the client application never sees it.

**Architecture:**

```
Client App  <--kind:24133 (NIP-44 encrypted)--> Remote Signer (has privkey)
            via Nostr relays
```

**Connection flow:**

1. Client generates a disposable `client_keypair`
2. Connection established via one of:
   - `bunker://<remote-signer-pubkey>?relay=wss://...&secret=<optional>`
     (signer-initiated, client sends `connect` request)
   - `nostrconnect://<client-pubkey>?relay=wss://...&secret=<required>&name=...`
     (client-initiated, signer sends `connect` response)
3. All messages are kind:24133 events, content encrypted with NIP-44
4. Client calls `get_public_key` to learn the user's actual pubkey

**Request format (kind:24133):**

```json
{
  "kind": 24133,
  "pubkey": "<client_pubkey>",
  "content": "<nip44_encrypted({id, method, params})>",
  "tags": [["p", "<remote_signer_pubkey>"]]
}
```

**Available methods:**

| Method           | Params                                    | Result                     |
| ---------------- | ----------------------------------------- | -------------------------- |
| `connect`        | `[remote_signer_pubkey, secret?, perms?]` | `"ack"` or secret          |
| `sign_event`     | `[json_stringified_unsigned_event]`       | `json_stringified(signed)` |
| `ping`           | `[]`                                      | `"pong"`                   |
| `get_public_key` | `[]`                                      | `<user_pubkey_hex>`        |
| `nip44_encrypt`  | `[third_party_pubkey, plaintext]`         | `<ciphertext>`             |
| `nip44_decrypt`  | `[third_party_pubkey, ciphertext]`        | `<plaintext>`              |

**Key distinction:** `remote-signer-pubkey` (used for NIP-44 transport
encryption) may differ from `user-pubkey` (the actual identity that signs
events). Always call `get_public_key` after connecting.

## Common Mistakes

| Mistake                                                   | Fix                                                                                                                                          |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Using NIP-04 for new implementations                      | NIP-04 is deprecated. Always use NIP-44v2 for encryption                                                                                     |
| Hashing the ECDH shared point                             | NIP-44 uses the raw unhashed x-coordinate. Some libraries (libsecp256k1) hash by default — use `secp256k1_ec_pubkey_tweak_mul` or equivalent |
| Reusing nonces in NIP-44                                  | Every message MUST use a fresh 32-byte CSPRNG nonce. Reuse makes messages decryptable                                                        |
| Adding tags to kind:13 seal events                        | Seal tags MUST always be empty `[]`. Tags on the seal leak metadata                                                                          |
| Signing the rumor in NIP-59                               | Rumors are intentionally unsigned for deniability. Only compute the `id`, never sign                                                         |
| Using real timestamps on seal/wrap                        | Both seal and gift wrap `created_at` SHOULD be randomized (up to 2 days in past) to prevent timing analysis                                  |
| Skipping signature validation before NIP-44 decrypt       | ALWAYS validate the outer event signature before decrypting content                                                                          |
| Not normalizing password to NFKC in NIP-49                | Passwords MUST be NFKC-normalized for cross-platform compatibility                                                                           |
| Confusing remote-signer-pubkey with user-pubkey in NIP-46 | They may differ. Always call `get_public_key` after `connect`                                                                                |
| Using wrong derivation path for NIP-06                    | Path is `m/44'/1237'/<account>'/0/0`. Coin type 1237, not 0 or other values                                                                  |

## Quick Reference

| Operation               | Algorithm                                       | Key Output                                       |
| ----------------------- | ----------------------------------------------- | ------------------------------------------------ |
| NIP-44 conversation key | ECDH + HKDF-extract(sha256, salt="nip44-v2")    | 32-byte symmetric key                            |
| NIP-44 message keys     | HKDF-expand(conv_key, nonce, 76)                | chacha_key(32) + chacha_nonce(12) + hmac_key(32) |
| NIP-44 encrypt          | ChaCha20 + HMAC-SHA256(nonce as AAD)            | base64(0x02 \|\| nonce \|\| ciphertext \|\| mac) |
| NIP-49 key derivation   | scrypt(password_nfkc, salt, log_n, r=8, p=1)    | 32-byte symmetric key                            |
| NIP-49 encrypt          | XChaCha20-Poly1305(privkey, aad=security_byte)  | bech32("ncryptsec", 91 bytes)                    |
| NIP-06 key derivation   | BIP39 mnemonic -> BIP32 `m/44'/1237'/0'/0/0`    | 32-byte secp256k1 privkey                        |
| NIP-59 seal             | kind:13, NIP-44 encrypt rumor, empty tags       | Signed by real author                            |
| NIP-59 gift wrap        | kind:1059, NIP-44 encrypt seal, p-tag recipient | Signed by ephemeral key                          |
| NIP-46 transport        | kind:24133, NIP-44 encrypted JSON-RPC           | Request/response via relays                      |

## Key Principles

1. **Validate before decrypt** — Always verify the outer event's Schnorr
   signature before attempting NIP-44 decryption. Decrypting unverified payloads
   is a security vulnerability.

2. **Never reuse nonces** — NIP-44 nonces must be 32 bytes from a CSPRNG, unique
   per message. NIP-49 nonces must be 24 bytes, unique per encryption. Nonce
   reuse breaks confidentiality.

3. **Layers isolate metadata** — NIP-59's three layers each reveal exactly one
   piece of information: the rumor reveals content (but is deniable), the seal
   reveals the author (but not content or recipient), the gift wrap reveals the
   recipient (but not author or content). Never collapse or skip layers.

4. **Conversation keys are symmetric** — `conv(a, B) == conv(b, A)`. Compute
   once per user pair and cache if needed. The ECDH output must NOT be hashed
   before HKDF — NIP-44 uses the raw x-coordinate.

5. **Normalize passwords** — NIP-49 requires NFKC unicode normalization of
   passwords before use in scrypt. Without this, the same password typed on
   different systems produces different keys.
