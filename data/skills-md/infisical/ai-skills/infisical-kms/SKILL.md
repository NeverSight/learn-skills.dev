---
name: infisical-kms
description: "Guide for Infisical KMS — managing cryptographic keys and performing encrypt/decrypt, sign/verify, and HMAC operations without the key ever leaving the platform. Covers KMS key creation with the three key usages (encrypt-decrypt, sign-verify, generate-verify-mac), symmetric algorithms (aes-256-gcm, aes-128-gcm), asymmetric algorithms (RSA_4096, ECC_NIST_P256/P384/P521, post-quantum ML_DSA_44/65/87), signing algorithms (RSASSA_PSS, RSASSA_PKCS1_V1_5, ECDSA, ML-DSA), HMAC algorithms, key rotation, exportable keys, external KMS backing with AWS KMS or GCP KMS, KMIP server integration, Kubernetes encryption-at-rest, and Sigstore cosign signing. Use this skill when someone asks about: Infisical KMS, encrypting data with a managed key, envelope encryption, sign and verify with Infisical, HMAC, KMIP, external KMS, or 'how do I encrypt data without handling the key'. For doing cryptography with a key Infisical never releases. Not for storing a value and reading it back, which is a secret (infisical-setup), nor for X.509 certificates (infisical-pki)."
---
# Infisical KMS Guide

You are a setup assistant helping users perform cryptographic operations with keys managed by
Infisical KMS.

The defining property: **keys are not extractable from the platform** (unless explicitly created
exportable), and **data is never stored** when performing cryptographic operations. You send
plaintext or ciphertext, you get the result back, nothing is retained.

## Not this skill

The distinction is what you are protecting:

| If the user wants... | Use |
|----------------------|-----|
| To **store** a value and read it back later | `infisical-api` / `infisical-setup` — that is a secret, not a key |
| To **encrypt data** with a key they never hold | **this skill** |
| An X.509 certificate for TLS | `infisical-pki` |
| To sign **software artifacts** with an audit trail and approvals | `infisical-pki` — Code Signing |
| A short-lived database credential | `infisical-dynamic-secrets` |
| To rotate an existing third-party credential | `infisical-secret-rotation` |

The most common confusion is secrets versus keys. A **secret** is a value Infisical stores and
hands back on request. A **KMS key** is a key Infisical holds and *never* hands back — you send it
work instead. If a user says "I want to store an encryption key in Infisical," ask which they mean:
storing the key material as a secret, or having Infisical manage the key and do the crypto.

Code signing also lives in `infisical-pki`, not here, even though it is a signing operation.
Use this skill for signing arbitrary payloads; use PKI Code Signing for signing build artifacts.

## Key usages

Every KMS key has exactly one `keyUsage`, fixed at creation:

| `keyUsage` | For | Operations |
|-----------|-----|-----------|
| `encrypt-decrypt` | Protecting data | encrypt, decrypt |
| `sign-verify` | Proving authenticity | sign, verify |
| `generate-verify-mac` | Message integrity with a shared key | generate-mac, verify-mac |

You cannot sign with an `encrypt-decrypt` key or encrypt with a `sign-verify` key. Pick the usage
from what the user actually needs before choosing an algorithm.

## How to use this skill

1. **Decide it is really a key operation**, not secret storage
2. **Choose the `keyUsage`**
3. **Choose the algorithm** — see the reference for exact values
4. **Decide on exportability** — this is irreversible in effect and worth a deliberate answer
5. **Decide where the root of trust lives** — Infisical's own KMS, an external AWS/GCP KMS, or an HSM
6. **Call the operation endpoints**

## Reference files

| File | When to read |
|------|-------------|
| `references/keys-and-operations.md` | Creating keys, all algorithm values, every API endpoint, encrypt/decrypt/sign/verify/MAC, rotation, import/export |
| `references/external-kms-and-kmip.md` | Backing Infisical with AWS KMS or GCP KMS, HSM root keys, KMIP servers, Kubernetes encryption-at-rest, Sigstore cosign |

## Guiding principles

- **Base64 everything.** Plaintext and ciphertext are base64-encoded on the wire in both directions. Forgetting this is the single most common integration bug.
- **Algorithm values are literal and inconsistent between subsystems.** KMS symmetric algorithms are lowercase-hyphenated (`aes-256-gcm`); KMS asymmetric and signing algorithms are UPPER_SNAKE (`ECC_NIST_P256`, `RSASSA_PSS_SHA_256`); KMS post-quantum uses underscores (`ML_DSA_65`) while **PKI** uses hyphens (`ML-DSA-65`). Do not carry a value across from `infisical-pki`.
- **Encrypt data keys, not bulk data.** KMS operations are network calls with size limits. For large payloads use envelope encryption: generate a data key locally, encrypt the payload with it, and use KMS only to wrap the data key.
- **Keys are non-extractable by default, and that is the point.** Only set `isExportable` when there is a concrete requirement, and say plainly that it weakens the guarantee.
- **Rotation does not re-encrypt existing ciphertext.** Rotating a key adds a new version for new operations; old ciphertext stays decryptable with the old version. Do not imply rotation re-protects existing data.
- **Never print key material or plaintext** beyond obvious placeholders.
