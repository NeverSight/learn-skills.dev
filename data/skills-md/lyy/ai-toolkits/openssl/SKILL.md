---
name: openssl
description: >-
  Use when a task needs certificate, key, CSR, TLS inspection, or format
  conversion work with openssl from the terminal.
---

# OpenSSL

## Overview

Use OpenSSL for terminal-driven certificate and key workflows: generating keys, creating CSRs, issuing self-signed certificates, checking remote TLS state, and converting certificate formats. Keep commands minimal and always verify outputs before using generated material downstream.

## Use When

- you need a private key or public key pair
- you need to create or inspect a CSR
- you need a self-signed certificate for local or internal use
- you need to inspect or verify a certificate or TLS endpoint
- you need PEM / DER / PKCS#12 conversion

## Quick Reference

```bash
# Generate a private key
openssl genrsa -aes256 -out private.key 4096

# Extract public key
openssl rsa -in private.key -pubout -out public.key

# Create CSR
openssl req -new -key private.key -out request.csr

# Create self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365

# Inspect cert or CSR
openssl x509 -in cert.pem -noout -text
openssl req -in request.csr -noout -text -verify

# Verify remote TLS endpoint
openssl s_client -connect example.com:443 -servername example.com

# Convert PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der
```

## Common Workflows

### Keys

- Prefer RSA 2048+ or EC P-256/P-384.
- Encrypt private keys unless the consuming system explicitly requires an unencrypted key.
- After generating a key, immediately verify you can read it back.

### CSRs

- Create the CSR from the intended private key.
- Include SAN values when the certificate will be used by browsers, TLS clients, or modern infrastructure.
- Verify the CSR before submitting it to a CA.

### Self-Signed Certificates

- Good for local development, internal testing, or bootstrap trust flows.
- Not appropriate as a drop-in replacement for publicly trusted production certificates.

### Inspection & Verification

- Read certificates with `openssl x509 -noout -text`.
- Check dates, issuer, subject, and SANs before deployment.
- Use `openssl verify` when you have the CA chain and need trust validation.

### Format Conversion

- PEM/DER conversion is common for platform compatibility.
- PKCS#12 is useful when a system expects a bundled certificate + private key file.
- Run inspection commands after conversion instead of assuming the output is valid.

## Safety Checks

- **Protect private keys.** Never expose them in logs, commits, screenshots, or chat output.
- **Check cert/key match** before deployment:

```bash
openssl x509 -noout -modulus -in cert.pem | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5
```

- **Use SANs.** Relying on `CN` alone is not enough for modern TLS clients.
- **Prefer SHA-256 or stronger.** Avoid weak defaults such as MD5 or SHA-1.
- **Know when `-nodes` is acceptable.** It removes the key passphrase and is convenient, but increases exposure risk.

## Gotchas

- OpenSSL commands happily produce files even when the inputs or subject details are wrong; inspect outputs immediately.
- Remote TLS checks with `s_client` are noisy; focus on certificate chain, hostname, dates, and verification result.
- Self-signed certificates can validate syntactically and still fail real client trust checks.
- Format conversion does not repair a bad certificate or mismatched key.

## Recovery & Fallbacks

- If a generated certificate looks wrong, inspect it first instead of regenerating blindly.
- If a cert and key do not match, stop and locate the correct pair before deploying anything.
- If OpenSSL output is too low-level for the task, use it to extract the raw facts, then hand the results to the higher-level tool or platform that consumes them.
