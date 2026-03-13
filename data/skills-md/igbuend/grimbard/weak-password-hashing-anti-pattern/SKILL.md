---
name: "weak-password-hashing-anti-pattern"
description: "Security anti-pattern for weak password hashing (CWE-327, CWE-759). Use when generating or reviewing code that stores or verifies user passwords. Detects use of MD5, SHA1, SHA256 without salt, or missing password hashing entirely. Recommends bcrypt, Argon2, or scrypt."
---

# Weak Password Hashing Anti-Pattern

**Severity:** High

## Summary

Applications use fast general-purpose hash functions (MD5, SHA-1, SHA-256) without salting for password storage, enabling rapid cracking via rainbow tables or GPU-accelerated brute-force (billions of hashes per second). Results in mass account compromise and credential stuffing attacks.

## The Anti-Pattern

The anti-pattern is using cryptographic hash functions that are too fast or lack essential features like salting and adjustable work factors, making them vulnerable to offline attacks.

### BAD Code Example

```python
# VULNERABLE: Using MD5 for password hashing.
import hashlib

def hash_password_md5(password):
    # MD5 is a cryptographically broken hash function.
    # It is extremely fast, and rainbow tables for MD5 are widely available.
    return hashlib.md5(password.encode()).hexdigest()

def verify_password_md5(password, stored_hash):
    return hash_password_md5(password) == stored_hash

# Another example: plain SHA-256 without salting.
def hash_password_sha256_unsalted(password):
    # SHA-256 is a strong hash for data integrity, but too fast for passwords.
    # Without a salt, identical passwords result in identical hashes.
    return hashlib.sha256(password.encode()).hexdigest()

# Problems:
# - Speed: MD5/SHA-256 can compute billions of hashes per second.
# - No Salt: Allows rainbow table attacks and reveals users with identical passwords.
# - No Work Factor: Cannot be slowed down to resist brute-force attacks.
```

### GOOD Code Example

```python
# SECURE: Use a password-hashing algorithm designed to be slow and include a unique salt.
import bcrypt # Or Argon2, scrypt

def hash_password_secure(password):
    # bcrypt generates unique salt per password and supports adjustable work factor.
    # Higher rounds = slower hashing = better brute-force resistance.
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    return hashed_password.decode('utf-8') # Store the hashed password as a string.

def verify_password_secure(password, stored_hash):
    # checkpw() verifies password against stored hash with constant-time comparison.
    # Extracts salt and work factor from stored hash to prevent timing attacks.
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

# Recommended algorithms (in order of current preference):
# 1. Argon2id (best practice for new applications)
# 2. bcrypt
# 3. scrypt

# Always use libraries for password hashing; never implement your own.
```

## Detection

- **Code Review:** Search your codebase for password hashing implementations.
  - Look for `hashlib.md5()`, `hashlib.sha1()`, or `hashlib.sha256()` being used for passwords.
  - Check if `bcrypt`, `argon2`, or `scrypt` libraries are used.
  - Verify that a unique, cryptographically secure salt is generated for each password.
- **Database Inspection:** Look at the `password` or `password_hash` column in your user database.
  - Are the hashes all of the same length and format? (Suggests no salt or static salt).
  - Do they start with prefixes like `$2a$` (bcrypt), `$argon2id$` (Argon2), or `$s2$` (scrypt)?
- **Check for plaintext passwords:** Ensure that passwords are never stored in plaintext.

## Prevention

- [ ] **Use strong, slow, adaptive password-hashing functions.**
  - **Argon2id:** Currently the recommended algorithm for new applications.
  - **bcrypt:** A widely used and strong algorithm.
  - **scrypt:** Another strong algorithm.
- [ ] **Always use a unique, cryptographically secure salt** for each password. bcrypt and Argon2 generate salts automatically.
- [ ] **Adjust the work factor (cost) appropriately.** Increase the number of rounds (bcrypt) or memory/time cost (Argon2) until hashing takes about 250-500 milliseconds on your server hardware. This makes brute-forcing expensive for attackers.
- [ ] **Never use fast, general-purpose hash functions** like MD5, SHA-1, or plain SHA-256 for passwords. These are designed for speed, not for password storage.
- [ ] **Never store plaintext passwords.**

## Related Security Patterns & Anti-Patterns

- [Hardcoded Secrets Anti-Pattern](../hardcoded-secrets/): Password hashes are sensitive data and should be protected.
- [Missing Authentication Anti-Pattern](../missing-authentication/): Weak password hashing undermines the entire authentication process.
- [Timing Attacks Anti-Pattern](../timing-attacks/): Proper password-hashing libraries use constant-time comparisons to prevent timing attacks during verification.

## References

- [OWASP Top 10 A04:2025 - Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)
- [CWE-759: Use of a One-Way Hash without a Salt](https://cwe.mitre.org/data/definitions/759.html)
- [CAPEC-55: Rainbow Table Password Cracking](https://capec.mitre.org/data/definitions/55.html)
- [PortSwigger: Authentication](https://portswigger.net/web-security/authentication)
- [BlueKrypt - Cryptographic Key Length Recommendation](https://www.keylength.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
