---
name: owasp-iot-top-10
description: "OWASP IoT Top 10 - prevention, detection, and remediation for IoT device and ecosystem security. Use when designing or reviewing IoT devices - passwords, network services, ecosystem interfaces, secure updates, components, data transfer/storage, device management, default settings, physical hardening, privacy."
---

# OWASP IoT Top 10

This skill encodes the OWASP IoT Top 10 for secure IoT device and ecosystem design and review. References are loaded per risk. Based on OWASP IoT Top 10 2018.

## When to Read Which Reference

| Risk | Read |
|------|------|
| I1 Weak, Guessable, or Hardcoded Passwords | [references/i1-weak-passwords.md](references/i1-weak-passwords.md) |
| I2 Insecure Network Services | [references/i2-insecure-network-services.md](references/i2-insecure-network-services.md) |
| I3 Insecure Ecosystem Interfaces | [references/i3-insecure-ecosystem-interfaces.md](references/i3-insecure-ecosystem-interfaces.md) |
| I4 Lack of Secure Update Mechanism | [references/i4-secure-update-mechanism.md](references/i4-secure-update-mechanism.md) |
| I5 Using Insecure or Outdated Components | [references/i5-outdated-components.md](references/i5-outdated-components.md) |
| I6 Insecure Data Transfer and Storage | [references/i6-insecure-data-transfer-storage.md](references/i6-insecure-data-transfer-storage.md) |
| I7 Absence of Device Management | [references/i7-device-management.md](references/i7-device-management.md) |
| I8 Insecure Default Settings | [references/i8-insecure-default-settings.md](references/i8-insecure-default-settings.md) |
| I9 Lack of Physical Hardening | [references/i9-physical-hardening.md](references/i9-physical-hardening.md) |
| I10 Insufficient Privacy Protection | [references/i10-privacy-protection.md](references/i10-privacy-protection.md) |

## Quick Patterns

- Eliminate default/hardcoded passwords; use secure update with signing; minimize exposed network services. Encrypt data in transit and at rest; support device lifecycle and decommissioning. Harden physically and protect user privacy.

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Eliminate default passwords | Force password change on first use; generate unique per-device. See [I1](references/i1-weak-passwords.md). |
| Secure updates | Sign firmware, verify before install, support rollback. See [I4](references/i4-secure-update-mechanism.md). |
| Minimize attack surface | Disable unused services, close unnecessary ports. See [I2](references/i2-insecure-network-services.md). |
| Encrypt data | TLS for transit, AES for storage, secure key storage. See [I6](references/i6-insecure-data-transfer-storage.md). |
| Physical hardening | Disable debug interfaces (JTAG/UART), tamper detection. See [I9](references/i9-physical-hardening.md). |

**Safe - firmware signature verification (pseudocode):**
```c
bool verify_firmware(uint8_t* firmware, size_t len, uint8_t* signature) {
    // Verify Ed25519 signature with embedded public key
    return ed25519_verify(signature, firmware, len, VENDOR_PUBLIC_KEY);
}
// Only install if verify_firmware() returns true
```

**Unsafe - no update verification:**
```c
void install_firmware(uint8_t* firmware) {
    flash_write(firmware);  // No signature check - accepts malicious updates
}
```

**Unique per-device credentials (manufacturing):**
```python
# During manufacturing, generate and store unique credentials
device_password = secrets.token_urlsafe(16)
store_in_secure_element(device_id, device_password)
```

## Workflow

Load the reference for the risk you are addressing. See [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things-top-10/) for the official list.
