---
name: "insufficient-randomness-anti-pattern"
description: "Security anti-pattern for insufficient randomness vulnerabilities (CWE-330). Use when generating or reviewing code that creates security tokens, session IDs, encryption keys, nonces, or any security-critical random values. Detects use of Math.random() or predictable seeds."
---

# Insufficient Randomness Anti-Pattern

**Severity:** High

## Summary

Insufficient randomness occurs when security-sensitive values (session tokens, password reset codes, encryption keys) are generated using predictable non-cryptographic PRNGs. AI models frequently suggest `Math.random()` or Python's `random` module for simplicity. These generators enable attackers to predict outputs after observing a few values, allowing token forgery, session hijacking, and cryptographic compromise.

## The Anti-Pattern

Never use predictable, non-cryptographic random number generators for security-sensitive values.

### BAD Code Example

```javascript
// VULNERABLE: Using Math.random() to generate a session token.

function generateSessionToken() {
    let token = '';
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    // Math.random() is a standard PRNG, not a cryptographically secure one.
    // Its output is predictable if an attacker can observe enough previous values
    // or has some knowledge of the initial seed (which can be time-based).
    for (let i = 0; i < 32; i++) {
        token += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return token;
}

// An attacker who obtains a few of these tokens can potentially
// reverse-engineer the PRNG's internal state and predict future tokens.
```

### GOOD Code Example

```javascript
// SECURE: Using a cryptographically secure pseudo-random number generator (CSPRNG).
const crypto = require('crypto');

function generateSessionToken() {
    // `crypto.randomBytes()` generates random data using the operating system's
    // underlying entropy sources, making it unpredictable.
    // It is designed specifically for cryptographic use cases.
    const buffer = crypto.randomBytes(32); // Generate 32 bytes of random data.
    return buffer.toString('hex'); // Convert to a hex string for easy use.
}

// The resulting token is 64 characters long and has 256 bits of entropy,
// making it infeasible for an attacker to guess or predict.
```

### Language-Specific Examples

**Python:**
```python
# VULNERABLE: Using random module for security
import random
import string

def generate_reset_token():
    chars = string.ascii_letters + string.digits
    # random module is predictable - can be reversed with ~624 observations
    return ''.join(random.choice(chars) for _ in range(32))
```

```python
# SECURE: Using secrets module (Python 3.6+)
import secrets

def generate_reset_token():
    # secrets module uses os.urandom() - cryptographically secure
    return secrets.token_urlsafe(32)  # 32 bytes = 256 bits

# Alternative: Using os.urandom directly
import os
import base64

def generate_session_id():
    return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')
```

**Java:**
```java
// VULNERABLE: Using java.util.Random for security
import java.util.Random;

public String generateSessionToken() {
    Random random = new Random(); // Predictable PRNG!
    byte[] bytes = new byte[32];
    random.nextBytes(bytes);
    return Base64.getEncoder().encodeToString(bytes);
}
```

```java
// SECURE: Using SecureRandom
import java.security.SecureRandom;
import java.util.Base64;

public String generateSessionToken() {
    SecureRandom secureRandom = new SecureRandom();
    byte[] bytes = new byte[32];
    secureRandom.nextBytes(bytes);
    return Base64.getEncoder().encodeToString(bytes);
}
```

**C#:**
```csharp
// VULNERABLE: Using System.Random for security
using System;

public string GenerateApiKey()
{
    var random = new Random(); // Predictable!
    var bytes = new byte[32];
    random.NextBytes(bytes);
    return Convert.ToBase64String(bytes);
}
```

```csharp
// SECURE: Using RandomNumberGenerator
using System;
using System.Security.Cryptography;

public string GenerateApiKey()
{
    using (var rng = RandomNumberGenerator.Create())
    {
        var bytes = new byte[32];
        rng.GetBytes(bytes);
        return Convert.ToBase64String(bytes);
    }
}
```

## Detection

- **Search for weak PRNGs in security contexts:** Grep for non-cryptographic random functions:
  - `rg 'Math\.random\(\)' --type js` (JavaScript)
  - `rg 'import random[^_]|from random import' --type py` (Python random module)
  - `rg 'new Random\(\)|Random\.next' --type java` (Java util.Random)
  - `rg '\brand\(|mt_rand\(' --type php` (PHP rand/mt_rand)
- **Identify manual seeding:** Find predictable seeds:
  - `rg 'random\.seed|Random\(time|srand\(time'`
  - CSPRNGs should never be manually seeded
- **Audit token generation:** Find session/token creation logic:
  - `rg 'session.*token|reset.*token|api.*key' -A 10`
  - Verify CSPRNG usage for all security tokens

## Prevention

- [ ] **Always use a cryptographically secure pseudo-random number generator (CSPRNG)** for any security-related value.
- [ ] **Know your language's CSPRNG:**
  - **Python:** Use the `secrets` module or `os.urandom()`.
  - **JavaScript (Node.js):** Use `crypto.randomBytes()` or `crypto.getRandomValues()`.
  - **Java:** Use `java.security.SecureRandom`.
  - **Go:** Use the `crypto/rand` package.
  - **C#:** Use `System.Security.Cryptography.RandomNumberGenerator`.
- [ ] **Ensure sufficient entropy:** Generate at least 128 bits (16 bytes) of randomness for tokens and unique identifiers. Use 256 bits (32 bytes) for encryption keys.
- [ ] **Never seed a CSPRNG manually.** They are designed to automatically draw entropy from the operating system.

## Related Security Patterns & Anti-Patterns

- [Session Fixation Anti-Pattern](../session-fixation/): Secure session ID generation is a key defense against session fixation.
- [Hardcoded Secrets Anti-Pattern](../hardcoded-secrets/): If an encryption key is generated with insufficient randomness, it's as bad as hardcoding a weak key.
- [Weak Encryption Anti-Pattern](../weak-encryption/): The security of an encryption algorithm relies on the unpredictability of its key.

## References

- [OWASP Top 10 A04:2025 - Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)
- [OWASP GenAI LLM06:2025 - Excessive Agency](https://genai.owasp.org/llmrisk/llm06-excessive-agency/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [CWE-330: Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)
- [CAPEC-112: Brute Force](https://capec.mitre.org/data/definitions/112.html)
- [PortSwigger: Authentication](https://portswigger.net/web-security/authentication)
- [BlueKrypt - Cryptographic Key Length Recommendation](https://www.keylength.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
