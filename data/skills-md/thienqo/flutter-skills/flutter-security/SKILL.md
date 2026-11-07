---
name: flutter-security
description: Threat-model, audit, or harden Flutter and Dart applications against concrete security and privacy risks involving authorization, secrets, sensitive storage, cryptography, WebViews, deep links, platform exposure, or dependencies. Use for security findings and control requirements; route sign-in and session implementation to flutter-authentication.
---

# Flutter Security

Protect user data and privileged operations with controls that match the actual threat model. Treat code, configuration, storage, logs, and binaries shipped to a user-controlled device as inspectable.

## Establish scope

1. Identify protected assets, actors, trust boundaries, supported platforms, sensitive flows, and realistic abuse cases.
2. Inspect `pubspec.yaml`, `pubspec.lock`, platform manifests and entitlements, environment handling, network configuration, storage, logging, WebViews, links, and release settings relevant to those assets.
3. Distinguish public identifiers from credentials and server-enforced trust. Do not label every client-visible key a secret without checking its provider contract and allowed restrictions.
4. Define whether the work is a static review, hardening change, or authorized runtime assessment. Do not probe external systems, rotate credentials, revoke sessions, or change production policy without explicit authorization.

## Core rules

- Never rely on obfuscation, environment files, or client-side checks to keep a credential secret or enforce authorization.
- Minimize sensitive data collection, retention, exposure, and logging. Clear user-bound caches and credentials when their lifecycle ends.
- Use platform-backed key and credential storage where the threat model requires it; ordinary preferences and databases are not secret vaults.
- Keep authentication state in the client, but enforce authorization and sensitive business rules on a trusted backend.
- Preserve secure transport defaults. Add exceptions or certificate pinning only for a documented requirement and an operationally viable rotation and recovery plan.
- Use maintained, reviewed cryptographic primitives and protocols. Do not invent algorithms, modes, key derivation, or token formats.
- Validate untrusted inputs at deep links, WebViews, platform channels, files, intents, clipboard boundaries, and remote responses.
- Treat dependency scanner output as leads that require applicability analysis, not automatic proof of an exploitable Flutter finding.

## Load references conditionally

- Read [application security](references/application-security.md) for secrets, authentication, storage, network transport, cryptography, privacy, and logging.
- Read [platform attack surfaces](references/platform-attack-surfaces.md) for WebViews, deep links, intents, permissions, backups, screenshots, clipboard, and native boundaries.
- Read [security verification](references/security-verification.md) when performing an audit, validating dependencies or release configuration, or reporting findings.

Route sign-in and session implementation to `flutter-authentication`, ordinary cache and database design to `flutter-persistence`, transport behavior to `flutter-networking`, native implementation mechanics to `flutter-platform-integration`, and release artifact handling to `flutter-build-release`. Security owns the threat and control requirements across those boundaries.

## Report with evidence

For each finding, identify the asset, attack precondition, reachable path, impact, concrete evidence, and the smallest proportionate remediation. Separate confirmed vulnerabilities from defense-in-depth improvements and unresolved questions. Do not claim that a package, scanner, encryption flag, or clean static review proves the application secure.

## Sources

- [Flutter security](https://docs.flutter.dev/security)
- [Flutter code obfuscation limitations](https://docs.flutter.dev/deployment/obfuscate)
- [OWASP MASVS](https://mas.owasp.org/MASVS/)
- [Android security checklist](https://developer.android.com/privacy-and-security/security-tips)
- [Apple App Transport Security](https://developer.apple.com/documentation/security/preventing-insecure-network-connections)
