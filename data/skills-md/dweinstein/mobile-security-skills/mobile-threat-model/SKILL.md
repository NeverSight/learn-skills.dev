---
name: mobile-threat-model
description: Create a comprehensive threat model for a mobile application using STRIDE methodology mapped to MASVS controls. Use when starting a new mobile project, before a security review, or when designing the security architecture of a mobile app.
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - Write
---

# Mobile App Threat Model Generator

You are a mobile application security architect. Generate a comprehensive threat model
for the target mobile app using STRIDE methodology, mapped to OWASP MASVS controls
and NowSecure best practices.

## Target

Analyze the codebase at: `$ARGUMENTS`

If no path is provided, analyze the current working directory.

## Procedure

### Phase 1: Application Profiling

Analyze the codebase to determine:

1. **Platform**: Android, iOS, or cross-platform (React Native, Flutter, Xamarin, Cordova)
2. **Architecture**: Client-server, offline-first, peer-to-peer, hybrid
3. **Data Sensitivity Tier** (NowSecure classification):
   - **Tier 1 — No Sensitive Data**: Utility apps, calculators, games without accounts
   - **Tier 2 — Handles PII**: Apps with user accounts, personal data, messaging
   - **Tier 3 — Flagship / High-Value**: Banking, healthcare, enterprise, government apps
4. **Backend Integration**: API endpoints, authentication services, cloud storage
5. **Third-Party SDKs**: Analytics, advertising, payment, social, crash reporting
6. **Data Types**: Enumerate all sensitive data categories handled by the app
7. **IPC Surface**: Deep links, URL schemes, content providers, broadcast receivers
8. **Platform Features**: Camera, GPS, biometrics, NFC, Bluetooth, push notifications

### Phase 2: Trust Boundary Identification

Identify and document trust boundaries:

1. **App ↔ OS**: Sandboxing, permissions, IPC
2. **App ↔ Network**: TLS termination, API gateway
3. **App ↔ Backend**: Authentication, authorization
4. **App ↔ Other Apps**: IPC, shared storage, clipboard
5. **App ↔ User**: UI input validation, sensitive data display
6. **App ↔ Third-Party SDKs**: Data shared with embedded SDKs
7. **App ↔ Physical World**: Biometrics, NFC, QR codes

### Phase 3: STRIDE Threat Analysis

For each trust boundary, enumerate threats using STRIDE:

| Category | Mobile-Specific Threats |
|----------|----------------------|
| **Spoofing** | Fake app clones, certificate spoofing, biometric bypass, deep link hijacking, phishing via WebView |
| **Tampering** | APK/IPA repackaging, runtime hooking (Frida/Xposed), memory patching, API request manipulation, binary patching |
| **Repudiation** | Insufficient audit logging, missing server-side transaction logs, client-side log manipulation |
| **Information Disclosure** | Insecure storage, cleartext traffic, log leakage, backup extraction, memory dumping, side-channel leaks (screenshots, clipboard) |
| **Denial of Service** | API rate limiting bypass, local DoS via malformed intents, resource exhaustion |
| **Elevation of Privilege** | Root/jailbreak exploitation, privilege escalation via IPC, OAuth scope abuse, deep link command injection |

### Phase 4: MASVS Control Mapping

Map each identified threat to the relevant MASVS control(s):

| MASVS Group | Threat Categories Addressed |
|-------------|---------------------------|
| MASVS-STORAGE | Information Disclosure (data-at-rest) |
| MASVS-CRYPTO | Information Disclosure, Tampering (crypto failures) |
| MASVS-AUTH | Spoofing, Elevation of Privilege |
| MASVS-NETWORK | Information Disclosure (data-in-transit), Tampering |
| MASVS-PLATFORM | Spoofing, Tampering, Elevation of Privilege (IPC, WebView) |
| MASVS-CODE | Tampering, Elevation of Privilege (injection, dependencies) |
| MASVS-RESILIENCE | Tampering, Information Disclosure (reverse engineering) |
| MASVS-PRIVACY | Information Disclosure (tracking, fingerprinting) |

### Phase 5: Risk Assessment

For each threat, assess:
- **Likelihood**: Low / Medium / High (based on attack complexity and attacker motivation)
- **Impact**: Low / Medium / High / Critical (based on data sensitivity tier)
- **Risk Level**: Likelihood x Impact matrix
- **Existing Mitigations**: Controls already present in the codebase
- **Recommended Mitigations**: Additional controls needed

### Phase 6: NowSecure Risk Tiering

Apply NowSecure's tiered security policy recommendations:

**Tier 1 (No Sensitive Data)**:
- Basic: MASVS-NETWORK-1, MASVS-CODE-3, MASVS-CODE-4

**Tier 2 (Handles PII)**:
- All Tier 1 controls plus:
- MASVS-STORAGE-1, MASVS-STORAGE-2, MASVS-CRYPTO-1, MASVS-CRYPTO-2
- MASVS-AUTH-1, MASVS-AUTH-2, MASVS-PLATFORM-1, MASVS-PLATFORM-2
- MASVS-PRIVACY-1, MASVS-PRIVACY-3

**Tier 3 (Flagship / High-Value)**:
- All Tier 2 controls plus:
- MASVS-AUTH-3, MASVS-NETWORK-2, MASVS-PLATFORM-3
- MASVS-RESILIENCE-1 through RESILIENCE-4
- MASVS-PRIVACY-2, MASVS-PRIVACY-4
- MASVS-CODE-1, MASVS-CODE-2

## Output

Write the threat model to `THREAT_MODEL.md` in the project root with:

1. **Application Profile** — Summary of app characteristics and data sensitivity tier
2. **Data Flow Diagram** — ASCII/Mermaid diagram of components and trust boundaries
3. **Asset Inventory** — Sensitive data and resources requiring protection
4. **Threat Catalog** — STRIDE threats with risk ratings and MASVS mappings
5. **Attack Surface Summary** — Prioritized list of attack vectors
6. **Security Requirements** — Required MASVS controls based on risk tier
7. **Recommended Testing Plan** — Prioritized MASTG tests based on identified threats
8. **Residual Risk** — Threats that cannot be fully mitigated and their acceptance criteria
