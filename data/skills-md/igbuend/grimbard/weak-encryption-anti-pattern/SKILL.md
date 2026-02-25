---
name: "weak-encryption-anti-pattern"
description: "Security anti-pattern for weak encryption (CWE-326, CWE-327). Use when generating or reviewing code that encrypts data, handles encryption keys, or uses cryptographic modes. Detects DES, ECB mode, static IVs, and custom crypto implementations."
---

# Weak Encryption Anti-Pattern

**Severity:** High

## Summary

Applications use outdated algorithms (DES, RC4), insecure modes (ECB), or mismanage IVs/nonces (static, reused), enabling easy decryption. AI models suggest these weak practices from older tutorials, leading to data breaches and compliance failures.

## The Anti-Pattern

The anti-pattern involves using cryptographic techniques that are no longer considered secure for protecting sensitive data.

### 1. Outdated or Broken Algorithms

Using algorithms like DES, 3DES, or RC4 is a critical flaw. These algorithms have known vulnerabilities and are easily broken with modern computing power.

#### BAD Code Example

```python
# VULNERABLE: Using the outdated DES algorithm.
from Crypto.Cipher import DES
from Crypto import Random

key = Random.get_random_bytes(8) # DES uses an 8-byte (64-bit) key, but only 56 bits are effective.

def encrypt_data_des(plaintext):
    cipher = DES.new(key, DES.MODE_ECB) # ECB mode is also insecure.
    # Pad the plaintext to be a multiple of 8 bytes (DES block size).
    padded_plaintext = plaintext + (8 - len(plaintext) % 8) * chr(8 - len(plaintext) % 8)
    ciphertext = cipher.encrypt(padded_plaintext.encode('utf-8'))
    return ciphertext

# DES can be brute-forced in under 24 hours with commodity hardware.
```

### 2. Insecure Modes of Operation (e.g., ECB)

Even if using a strong algorithm like AES, using it in Electronic Codebook (ECB) mode is highly insecure. ECB encrypts identical blocks of plaintext into identical blocks of ciphertext, revealing patterns in the data.

#### BAD Code Example

```python
# VULNERABLE: Using AES in ECB mode.
from Crypto.Cipher import AES
from Crypto import Random

key = Random.get_random_bytes(16) # AES-128 key.

def encrypt_data_ecb(plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    # Pad the plaintext to be a multiple of 16 bytes (AES block size).
    padded_plaintext = plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)
    ciphertext = cipher.encrypt(padded_plaintext.encode('utf-8'))
    return ciphertext

# If you encrypt an image with many identical color blocks using AES-ECB,
# the encrypted image will still show the original image's outline and patterns.
# This leaks significant information about the plaintext.
```

### GOOD Code Example

```python
# SECURE: Use a modern, authenticated encryption mode like AES-256-GCM.
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import os

# Generate a strong, random key. AES-256 uses a 32-byte key.
key = AESGCM.generate_key(bit_length=256)

def encrypt_data_gcm(plaintext):
    aesgcm = AESGCM(key)
    # GCM requires a unique, unpredictable nonce (Initialization Vector).
    # It must never be reused with the same key. A 12-byte nonce is standard.
    nonce = os.urandom(12)

    # AES-GCM performs both encryption and provides an authentication tag (integrity check).
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

    # Store and transmit the nonce along with the ciphertext.
    return nonce + ciphertext

def decrypt_data_gcm(encrypted_data_with_nonce):
    aesgcm = AESGCM(key)
    nonce = encrypted_data_with_nonce[:12]
    ciphertext = encrypted_data_with_nonce[12:]

    try:
        # The decrypt method will also verify the authentication tag.
        # If the data is tampered with, it will raise an `InvalidTag` exception.
        plaintext = aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
        return plaintext
    except InvalidTag:
        raise ValueError("Decryption failed: data may have been tampered with or corrupted.")

# AES-256-GCM provides strong confidentiality, integrity, and authenticity.
# Each encryption is unique due to the nonce, preventing pattern leakage.
```

## Detection

- **Code review for algorithm choice:** Search your codebase for calls to cryptographic functions using `DES`, `3DES`, `RC4`, `MD5` (for encryption), or `SHA-1` (for encryption/signatures).
- **Check modes of operation:** Look for `ECB` mode being used with block ciphers like AES.
- **Inspect IV/Nonce generation:** Verify how initialization vectors (IVs) or nonces are generated. Are they random and unique for each encryption? Avoid static, predictable, or reused IVs.
- **Custom crypto implementations:** Be extremely wary of any "homegrown" encryption algorithms. These are almost always insecure.

## Prevention

- [ ] **Use strong, modern algorithms:** For symmetric encryption, always use **AES-256**. For authenticated encryption, prefer **AES-256-GCM** or **ChaCha20-Poly1305**.
- [ ] **Avoid insecure modes of operation:** Never use ECB mode. If using CBC mode, always pair it with a strong MAC (Message Authentication Code) in an Encrypt-then-MAC scheme. Better yet, use AEAD modes like GCM.
- [ ] **Generate random, unique IVs/Nonces:** Generate a unique, unpredictable IV (CBC) or nonce (GCM) for every encryption using a cryptographically secure random number generator. Never reuse a nonce with the same key in GCM (enables catastrophic key recovery).
- [ ] **Use established cryptographic libraries:** Never "roll your own" encryption. Use well-vetted, standard libraries (e.g., `cryptography` in Python, `javax.crypto` in Java).
- [ ] **Ensure key strength:** Use sufficiently long keys (e.g., 256 bits for AES).

## Related Security Patterns & Anti-Patterns

- [Hardcoded Secrets Anti-Pattern](../hardcoded-secrets/): Encryption keys are critical secrets that must be managed securely.
- [Insufficient Randomness Anti-Pattern](../insufficient-randomness/): The randomness used for IVs/nonces must be cryptographically secure.
- [Padding Oracle Anti-Pattern](../padding-oracle/): A specific attack against block ciphers used in CBC mode without proper authentication.

## References

- [OWASP Top 10 A04:2025 - Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [CWE-326: Inadequate Encryption Strength](https://cwe.mitre.org/data/definitions/326.html)
- [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)
- [CAPEC-97: Cryptanalysis](https://capec.mitre.org/data/definitions/97.html)
- [BlueKrypt - Cryptographic Key Length Recommendation](https://www.keylength.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
