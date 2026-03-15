---
name: signing
description: "Message signing and verification — SIP-018 structured Clarity data signing (on-chain verifiable), Stacks plain-text message signing (SIWS-compatible), Bitcoin message signing (BIP-137 for legacy/wrapped-SegWit, BIP-322 for native SegWit bc1q and Taproot bc1p), BIP-340 Schnorr signing for Taproot multisig, and Nostr event signing using NIP-06 key derivation. All signing requires an unlocked wallet; hash and verify operations do not."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "sip018-sign | sip018-verify | sip018-hash | stacks-sign | stacks-verify | btc-sign | btc-verify | schnorr-sign-digest | schnorr-verify-digest | nostr-sign-event"
  entry: "signing/signing.ts"
  requires: "wallet"
  tags: "l2, l1"
---

# Signing Skill

Provides cryptographic message signing for the Stacks and Bitcoin ecosystems. Four signing standards are supported:

- **SIP-018** — Structured Clarity data signing. Signatures are verifiable both off-chain and by on-chain smart contracts via `secp256k1-recover?`.
- **Stacks messages** — SIWS-compatible plain-text signing. Used for wallet authentication and proving address ownership.
- **Bitcoin messages** — BIP-137/BIP-322 hybrid. BIP-137 for legacy (1...) and wrapped SegWit (3...) addresses; BIP-322 "simple" for native SegWit (bc1q) and Taproot (bc1p) addresses. Compatible with Electrum, Bitcoin Core, and modern wallets.
- **Schnorr (BIP-340)** — Taproot-native signing over raw 32-byte digests. Used for Taproot script-path spending, multisig coordination, and OP_CHECKSIGADD witness assembly.
- **Nostr events (NIP-06)** — Sign Nostr event objects using the NIP-06 derived key (`m/44'/1237'/0'/0/0`) by default, or from a wallet key path via `keySource`.

## Usage

```
bun run signing/signing.ts <subcommand> [options]
```

## Subcommands

### sip018-sign

Sign structured Clarity data using the SIP-018 standard. The domain binding (name + version + chain-id) prevents cross-app and cross-chain replay attacks. Requires an unlocked wallet.

```
bun run signing/signing.ts sip018-sign \
  --message '{"amount":{"type":"uint","value":100}}' \
  --domain-name "My App" \
  --domain-version "1.0.0"
```

Options:
- `--message` (required) — Structured data as a JSON string. Use type hints for explicit Clarity types:
  - `{"type":"uint","value":100}` → `uint`
  - `{"type":"int","value":-50}` → `int`
  - `{"type":"principal","value":"SP..."}` → `principal`
  - `{"type":"ascii","value":"hello"}` → `string-ascii`
  - `{"type":"utf8","value":"hello"}` → `string-utf8`
  - `{"type":"buff","value":"0x1234"}` → `buff`
  - `{"type":"bool","value":true}` → `bool`
  - `{"type":"none"}` → `none`
  - `{"type":"some","value":...}` → `(some ...)`
  - `{"type":"list","value":[...]}` → `list`
  - `{"type":"tuple","value":{...}}` → `tuple`
  - Implicit: `string → string-utf8`, `number → int`, `boolean → bool`, `null → none`
- `--domain-name` + `--domain-version` (required together) — Flat CLI domain fields
- `--domain` (alternative) — MCP-style JSON object: `{"name":"My App","version":"1.0.0"}` (optional `chainId`)

Output:
```json
{
  "success": true,
  "signature": "abc123...",
  "signatureFormat": "RSV (65 bytes hex)",
  "signer": "SP...",
  "network": "testnet",
  "chainId": 2147483648,
  "hashes": {
    "message": "...",
    "domain": "...",
    "encoded": "...",
    "verification": "...",
    "prefix": "0x534950303138"
  },
  "domain": { "name": "My App", "version": "1.0.0", "chainId": 2147483648 },
  "verificationNote": "Use sip018-verify with the 'verification' hash..."
}
```

### sip018-verify

Verify a SIP-018 signature and recover the signer's Stacks address. Provide the `verification` hash from `sip018-sign` or `sip018-hash`.

```
bun run signing/signing.ts sip018-verify \
  --message-hash <verificationHash> \
  --signature <rsv65BytesHex> \
  [--expected-signer <address>]
```

Options:
- `--message-hash` (required) — The SIP-018 verification hash (from `sip018-sign`/`sip018-hash`)
- `--signature` (required) — Signature in RSV format (65 bytes hex)
- `--expected-signer` (optional) — Expected signer address to verify against

Output:
```json
{
  "success": true,
  "recoveredPublicKey": "03...",
  "recoveredAddress": "SP...",
  "network": "testnet",
  "verification": {
    "expectedSigner": "SP...",
    "isValid": true,
    "message": "Signature is valid for the expected signer"
  }
}
```

### sip018-hash

Compute the SIP-018 message hash without signing. Returns all hash components needed for off-chain or on-chain verification. Does not require an unlocked wallet.

```
bun run signing/signing.ts sip018-hash \
  --message '{"amount":{"type":"uint","value":100}}' \
  --domain-name "My App" \
  --domain-version "1.0.0" \
  [--chain-id <id>]
```

Options:
- `--message` (required) — Structured data as a JSON string (same format as sip018-sign)
- `--domain-name` + `--domain-version` (required together) — Flat CLI domain fields
- `--domain` (alternative) — MCP-style JSON object: `{"name":"My App","version":"1.0.0"}` (optional `chainId`)
- `--chain-id` (optional) — Chain ID override (takes precedence over `domain.chainId`)

Output:
```json
{
  "success": true,
  "hashes": {
    "message": "...",
    "domain": "...",
    "encoded": "...",
    "verification": "..."
  },
  "hashConstruction": {
    "prefix": "0x534950303138",
    "formula": "verification = sha256(prefix || domainHash || messageHash)"
  },
  "domain": { "name": "My App", "version": "1.0.0", "chainId": 2147483648 },
  "clarityVerification": {
    "example": "(secp256k1-recover? (sha256 encoded-data) signature)"
  }
}
```

### stacks-sign

Sign a plain text message using the Stacks message signing format. The message is prefixed with `\x17Stacks Signed Message:\n` before hashing (SIWS-compatible). Requires an unlocked wallet.

```
bun run signing/signing.ts stacks-sign --message "Hello, Stacks!"
```

Options:
- `--message` (required) — Plain text message to sign

Output:
```json
{
  "success": true,
  "signature": "abc123...",
  "signatureFormat": "RSV (65 bytes hex)",
  "signer": "SP...",
  "network": "testnet",
  "message": {
    "original": "Hello, Stacks!",
    "prefix": "\u0017Stacks Signed Message:\n",
    "prefixHex": "...",
    "hash": "..."
  },
  "verificationNote": "Use stacks-verify with the original message and signature to verify."
}
```

### stacks-verify

Verify a Stacks message signature and recover the signer's Stacks address. Compatible with SIWS authentication flows.

```
bun run signing/signing.ts stacks-verify \
  --message "Hello, Stacks!" \
  --signature <rsv65BytesHex> \
  [--expected-signer <address>]
```

Options:
- `--message` (required) — The original plain text message that was signed
- `--signature` (required) — Signature in RSV format (65 bytes hex)
- `--expected-signer` (optional) — Expected signer Stacks address

Output:
```json
{
  "success": true,
  "signatureValid": true,
  "recoveredPublicKey": "03...",
  "recoveredAddress": "SP...",
  "network": "testnet",
  "message": {
    "original": "Hello, Stacks!",
    "prefix": "\u0017Stacks Signed Message:\n",
    "hash": "..."
  },
  "verification": {
    "expectedSigner": "SP...",
    "signerMatches": true,
    "isFullyValid": true,
    "message": "Signature is valid and matches expected signer"
  }
}
```

### btc-sign

Sign a plain text message using Bitcoin message signing. Automatically selects the signing format based on address type: BIP-137 (65-byte compact signature) for legacy (1...) and wrapped SegWit (3...) addresses; BIP-322 "simple" (witness-serialized) for native SegWit (bc1q) and Taproot (bc1p) addresses. Compatible with Electrum, Bitcoin Core, and modern wallets. Requires an unlocked wallet with Bitcoin keys.

```
bun run signing/signing.ts btc-sign --message "Hello, Bitcoin!"
```

Options:
- `--message` (required) — Plain text message to sign

Output:
```json
{
  "success": true,
  "signature": "abc123...",
  "signatureBase64": "...",
  "signatureFormat": "BIP-137 (65 bytes: 1 header + 32 r + 32 s)",
  "signer": "bc1q...",
  "network": "mainnet",
  "addressType": "P2WPKH (native SegWit)",
  "message": {
    "original": "Hello, Bitcoin!",
    "prefix": "\u0018Bitcoin Signed Message:\n",
    "prefixHex": "...",
    "formattedHex": "...",
    "hash": "..."
  },
  "header": { "value": 39, "recoveryId": 0, "addressType": "P2WPKH (native SegWit)" },
  "verificationNote": "Use btc-verify with the original message and signature to verify."
}
```

### btc-verify

Verify a Bitcoin message signature (BIP-137 or BIP-322) and recover the signer's Bitcoin address. Automatically detects the format: BIP-137 (65-byte compact, hex 130 chars or base64 88 chars) for legacy/wrapped-SegWit addresses, and BIP-322 "simple" (witness-serialized, base64) for native SegWit (bc1q) and Taproot (bc1p) addresses.

```
bun run signing/signing.ts btc-verify \
  --message "Hello, Bitcoin!" \
  --signature <hexOrBase64Sig> \
  [--expected-signer <btcAddress>]
```

Options:
- `--message` (required) — The original plain text message that was signed
- `--signature` (required) — Bitcoin signature: BIP-137 (65 bytes as hex [130 chars] or base64 [88 chars]) for legacy/wrapped-SegWit, or BIP-322 "simple" (witness-serialized, base64) for bc1q/bc1p addresses
- `--expected-signer` (optional) — Expected signer Bitcoin address to verify against

Output:
```json
{
  "success": true,
  "signatureValid": true,
  "recoveredPublicKey": "03...",
  "recoveredAddress": "bc1q...",
  "network": "mainnet",
  "message": { "original": "Hello, Bitcoin!", "prefix": "...", "hash": "..." },
  "header": { "value": 39, "recoveryId": 0, "addressType": "P2WPKH (native SegWit)" },
  "verification": {
    "expectedSigner": "bc1q...",
    "signerMatches": true,
    "isFullyValid": true,
    "message": "Signature is valid and matches expected signer"
  }
}
```

### schnorr-sign-digest

Sign a raw 32-byte digest with Schnorr (BIP-340) using the wallet's Taproot private key. Use for Taproot script-path spending, multisig coordination, or any case where you need a BIP-340 Schnorr signature over a pre-computed hash (e.g., BIP-341 sighash). Includes a blind-signing safety gate — the first call without `--confirm-blind-sign` returns the digest for review. Requires an unlocked wallet with Taproot keys.

```
bun run signing/signing.ts schnorr-sign-digest \
  --digest <64-char-hex> \
  [--aux-rand <64-char-hex>] \
  [--confirm-blind-sign]
```

Options:
- `--digest` (required) — 32-byte hex-encoded digest to sign (e.g., BIP-341 transaction sighash)
- `--aux-rand` (optional) — 32-byte hex auxiliary randomness for BIP-340 (improves side-channel resistance)
- `--confirm-blind-sign` (optional) — Set to confirm you have reviewed the digest and accept blind-signing risk. Without this flag, returns a warning with the digest for review.

Output (without `--confirm-blind-sign`):
```json
{
  "warning": "schnorr-sign-digest signs a raw 32-byte digest...",
  "digestToReview": "abc123...",
  "instructions": "Review the digest above. If you trust its origin..."
}
```

Output (with `--confirm-blind-sign`):
```json
{
  "success": true,
  "signature": "abc123...",
  "publicKey": "def456...",
  "address": "bc1p...",
  "network": "mainnet",
  "signatureFormat": "BIP-340 Schnorr (64 bytes)",
  "publicKeyFormat": "x-only (32 bytes)",
  "note": "For Taproot script-path spending, append sighash type byte..."
}
```

### schnorr-verify-digest

Verify a BIP-340 Schnorr signature over a 32-byte digest. Takes the digest, signature, and x-only public key, returns whether the signature is valid. Use for verifying Taproot signatures from other agents in multisig coordination.

```
bun run signing/signing.ts schnorr-verify-digest \
  --digest <64-char-hex> \
  --signature <128-char-hex> \
  --public-key <64-char-hex>
```

Options:
- `--digest` (required) — 32-byte hex-encoded digest that was signed
- `--signature` (required) — 64-byte hex-encoded BIP-340 Schnorr signature
- `--public-key` (required) — 32-byte hex-encoded x-only public key of the signer

Output:
```json
{
  "success": true,
  "isValid": true,
  "digest": "abc123...",
  "signature": "def456...",
  "publicKey": "789abc...",
  "message": "Signature is valid for the given digest and public key",
  "note": "BIP-340 Schnorr verification. Use for validating signatures in Taproot multisig coordination."
}
```

### nostr-sign-event

Sign a Nostr event object (NIP-01 format) using the wallet's Nostr key. By default the key is derived via NIP-06 (`m/44'/1237'/0'/0/0`) from the wallet mnemonic, producing an `npub` that matches NIP-06 compliant Nostr clients (e.g. Amethyst, Damus, Snort). Requires an unlocked wallet.

```
bun run signing/signing.ts nostr-sign-event \
  --event '{"kind":1,"created_at":1700000000,"tags":[],"content":"Hello, Nostr!"}' \
  [--key-source nostr|taproot|segwit]
```

Options:
- `--event` (required) — Nostr event JSON object (NIP-01 format). Fields `id`, `pubkey`, and `sig` are computed and returned; do not include them in the input.
- `--key-source` (optional, default: `"nostr"`) — Which wallet key to use for signing:
  - `"nostr"` (default) — NIP-06 derived key (`m/44'/1237'/0'/0/0`). Use this for new identities and compatibility with all NIP-06 Nostr clients.
  - `"taproot"` — BIP-86 Taproot key (`m/86'/0'/0'/0/0`). Use if you already have an existing Nostr identity on your Taproot key.
  - `"segwit"` — BIP-84 native SegWit key (`m/84'/0'/0'/0/0`). Use if you already have an existing Nostr identity on your SegWit key.

Output:
```json
{
  "success": true,
  "event": {
    "id": "abc123...",
    "pubkey": "def456...",
    "created_at": 1700000000,
    "kind": 1,
    "tags": [],
    "content": "Hello, Nostr!",
    "sig": "789abc..."
  },
  "npub": "npub1...",
  "keySource": "nostr",
  "derivationPath": "m/44'/1237'/0'/0/0",
  "note": "Key derived via NIP-06. npub matches NIP-06 compliant Nostr clients."
}
```

**Key derivation note:** The default `"nostr"` source uses NIP-06 (`m/44'/1237'/0'/0/0`), the standard Nostr derivation path defined in the [NIP-06 spec](https://github.com/nostr-protocol/nips/blob/master/06.md). Agents should use this default for all Nostr interactions. The `keySource` override is only needed when an existing Nostr identity was previously established on a different key path.

## Signing Standards Reference

| Standard | Prefix | Use Case | On-Chain Verifiable? |
|----------|--------|----------|---------------------|
| SIP-018 | `SIP018` (hex) | Structured Clarity data | Yes (`secp256k1-recover?`) |
| Stacks | `\x17Stacks Signed Message:\n` | Auth, ownership proof | No (off-chain only) |
| BIP-137 / BIP-322 | `\x18Bitcoin Signed Message:\n` | Bitcoin auth, ownership proof (BIP-137 for 1.../3...; BIP-322 for bc1q/bc1p) | No (off-chain only) |
| BIP-340 | None (raw digest) | Taproot multisig, script-path spending | Yes (OP_CHECKSIG/OP_CHECKSIGADD) |
| NIP-06 (Nostr) | None (event hash) | Nostr event signing (NIP-01) | No (Nostr network only) |

## Notes

- SIP-018 signing and Stacks signing require an unlocked wallet (`bun run wallet/wallet.ts unlock`)
- BTC signing additionally requires Bitcoin keys (automatically present in managed wallets)
- Schnorr signing requires Taproot keys (automatically derived in managed wallets)
- `sip018-hash`, both `*-verify` subcommands, and `schnorr-verify-digest` do NOT require an unlocked wallet
- All ECDSA signatures use the secp256k1 curve; Schnorr uses BIP-340 (x-only pubkeys, 64-byte sigs)
- SIP-018 chain IDs: mainnet = 1, testnet = 2147483648 (0x80000000)
