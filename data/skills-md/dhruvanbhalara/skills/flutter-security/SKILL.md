---
name: flutter-security
description: Security & Data Integrity (Architect Level)
metadata:
    platforms: "flutter, mobile"
    languages: "dart"
    category: "security"
---

# Security & Data Integrity (Architect Level)

-   **AES-256-GCM**: Use Authenticated Encryption for all sensitive storage.
-   **Secret Storage**: Mandatory use of `flutter_secure_storage` for encryption keys and master-derived keys.
-   **Key Derivation**: Mandate NIST-approved hashing (**Argon2id**) for master password derivation before local storage encryption and export.
-   **Memory Safety**: Strictly clear sensitive variables (passwords, keys) from memory when the operation finishes or the app enters the background.
-   **Clipboard Safety**: Mandate programmatic clearing of sensitive data (OTPs, Passwords) after a short duration (30-60s).
-   **Biometric Gate**: Mandatory local authentication for any view, export, or destructive action.
-   **Audit Log**: All security-sensitive actions should be logged via `AppLogger` (excluding raw secrets).

# Input & API Security

-   **Input Validation**: Validate and sanitize all user-facing input fields before processing or storage.
-   **HTTPS Only**: All API communication MUST use HTTPS. Consider certificate pinning for sensitive applications.
-   **Token Storage**: STRICTLY prohibit storing tokens, API keys, or credentials in source code or public repositories. Use `flutter_secure_storage` or environment-based injection.
