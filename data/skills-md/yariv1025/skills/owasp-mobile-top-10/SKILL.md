---
name: owasp-mobile-top-10
description: "OWASP Mobile Top 10 - prevention, detection, and remediation for iOS/Android app security. Use when building or reviewing mobile apps - credentials, supply chain, auth, input/output validation, communication, privacy, binary protection, config, data storage, cryptography."
---

# OWASP Mobile Top 10

This skill encodes the OWASP Mobile Top 10 for secure mobile app design and review. References are loaded per risk (progressive disclosure). Based on OWASP Mobile Top 10 2024.

## When to Read Which Reference

| Risk | Read |
|------|------|
| M1 Improper Credential Usage | [references/m1-improper-credential-usage.md](references/m1-improper-credential-usage.md) |
| M2 Inadequate Supply Chain Security | [references/m2-supply-chain-security.md](references/m2-supply-chain-security.md) |
| M3 Insecure Authentication/Authorization | [references/m3-insecure-auth.md](references/m3-insecure-auth.md) |
| M4 Insufficient Input/Output Validation | [references/m4-input-output-validation.md](references/m4-input-output-validation.md) |
| M5 Insecure Communication | [references/m5-insecure-communication.md](references/m5-insecure-communication.md) |
| M6 Inadequate Privacy Controls | [references/m6-privacy-controls.md](references/m6-privacy-controls.md) |
| M7 Insufficient Binary Protections | [references/m7-binary-protections.md](references/m7-binary-protections.md) |
| M8 Security Misconfiguration | [references/m8-security-misconfiguration.md](references/m8-security-misconfiguration.md) |
| M9 Insecure Data Storage | [references/m9-insecure-data-storage.md](references/m9-insecure-data-storage.md) |
| M10 Insufficient Cryptography | [references/m10-insufficient-cryptography.md](references/m10-insufficient-cryptography.md) |

## Quick Patterns

- Store credentials and API keys in secure storage (keychain/Keystore); never hardcode. Validate all inputs and encode outputs.
- Use certificate pinning and TLS for communication; enforce privacy controls and minimal data collection.
- Harden binary (obfuscation, integrity); use secure defaults and encrypt sensitive data at rest.

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Store credentials | Use iOS Keychain or Android Keystore; never hardcode. See [M1](references/m1-improper-credential-usage.md). |
| Secure network calls | Use TLS 1.2+, implement certificate pinning. See [M5](references/m5-insecure-communication.md). |
| Validate input | Sanitize all user/external input before use. See [M4](references/m4-input-output-validation.md). |
| Protect local data | Encrypt with platform APIs (EncryptedSharedPreferences, Data Protection). See [M9](references/m9-insecure-data-storage.md). |

**Safe - Android Keystore for credentials:**
```kotlin
val keyStore = KeyStore.getInstance("AndroidKeyStore")
keyStore.load(null)
val secretKey = keyStore.getKey("my_key_alias", null) as SecretKey
```

**Unsafe - hardcoded API key:**
```kotlin
val API_KEY = "sk-12345abcdef"  // NEVER do this - extract from APK
```

**Certificate pinning (OkHttp):**
```kotlin
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .build()
```

## Workflow

Load the reference for the risk you are addressing (e.g. credential handling → M1; network → M5; local storage → M9). See [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10/) for the official list.
