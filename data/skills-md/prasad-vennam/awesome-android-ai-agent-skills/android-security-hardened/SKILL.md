---
name: android-security-hardened
description: "Use when securing Android applications, implementing Biometric auth, or encrypting sensitive data locally."
category: security
risk: high
source: community
date_added: "2026-03-31"
metadata:
  triggers:
    - "@android-security"
    - "biometric-auth"
    - "keystore"
    - "encrypted-prefs"
    - "root-detection"
---

# Android Security Hardening 🛡️🔐

Professional security practices for protecting sensitive user data, identity, and application integrity on Android devices.

## ⚡ When to Use
- **Biometric Authentication**: Fingerprint/Face ID for app lock.
- **Local Encryption**: Securing login tokens or user profiles.
- **Keystore Management**: Safe storage of cryptographic keys.
- **Root/Emulator Detection**: Verifying device integrity for high-risk apps.
- **Certificate Pinning**: Hardening HTTPS via network security config.

## 🏗️ The 5 Pillars of Security

1.  **Identity**: Strong authentication (OIDC, Biometrics).
2.  **Confidentiality**: Encrypting data at rest and in transit.
3.  **Integrity**: Preventing tampering (App signing, Root check).
4.  **Available**: Ensuring resilience (DDoS protection, Offline access control).
5.  **Audit**: Logging security-relevant events safely.

## 🔑 KeyStore & Cryptography

### 1. Android Keystore System
- **Rule**: NEVER store encryption keys in resources or hardcoded.
- Use `KeyGenerator` with `purpose(PURPOSE_ENCRYPT | PURPOSE_DECRYPT)` and `blockMode(BLOCK_MODE_GCM)`.
- Use **GCM (Galois/Counter Mode)** for authenticated encryption.

### 2. EncryptedSharedPreferences
- **Rule**: Use `Jetpack Security` to encrypt standard `SharedPreferences`.
  ```kotlin
  val masterKey = MasterKey.Builder(context).setKeyScheme(AES256_GCM).build()
  val sharedPrefs = EncryptedSharedPreferences.create(
      context, "secret_prefs", masterKey, AES256_SIV, AES256_GCM
  )
  ```

## 🔐 Biometric Auth (BiometricPrompt)

- Use the **androidx.biometric** library for consistent UI across devices.
- **Class 3 (Strong)**: Highest security, requires biological match.
- **Class 2 (Weak)**: Fallback for older devices.

## 🛡️ Device Integrity & Hardening

- [ ] **Root Detection**: Use libraries like `RootBeer` or `Google Play Integrity API`.
- [ ] **Emulator Detection**: Verify system properties (`ro.product.model`, `ro.hardware`).
- [ ] **Certificate Pinning**: Use the `network-security-config.xml` to limit trusted CAs.
- [ ] **ProGuard/R8**: Obfuscate sensitive classes and strings. **CRITICAL WARNING**: Misconfigured R8 rules *will* crash the app if reflection relies on stripped classes. (See [CI/CD Expert Skill](../android-ci-cd-expert/SKILL.md) for R8 configuration guidelines).
- [ ] **No Backup**: Use `android:allowBackup="false"` for sensitive data.

## 📐 Networking Best Practices

- Always use **HTTPS** (TLS 1.2+).
- Use `android:usesCleartextTraffic="false"` in the manifest.
- Sanitize all external inputs (Intents, WebViews).

## 🧪 Testing and Verification

- **MobSF**: Use Mobile Security Framework to scan for vulnerabilities.
- **Runtime Checks**: Use ADB to verify private data is NOT accessible to other apps.
- **OWASP MSTG**: Follow the Mobile Security Testing Guide.

## 🔗 Related Resources
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
- [Jetpack Security (Crypto)](https://developer.android.com/topic/security/data)
- [Play Integrity API](https://developer.android.com/google/play/integrity)
