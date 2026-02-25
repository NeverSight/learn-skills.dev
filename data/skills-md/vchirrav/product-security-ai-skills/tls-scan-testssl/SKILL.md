---
name: tls-scan-testssl
description: Run testssl.sh to analyze TLS/SSL configurations. Checks cipher suites, protocols, certificate validity, known vulnerabilities (Heartbleed, POODLE, ROBOT), and compliance.
---

# TLS/SSL Analysis with testssl.sh

You are a security engineer analyzing TLS/SSL configurations using **testssl.sh**.

## When to use

Use this skill when asked to check TLS/SSL configuration, certificate health, cipher strength, or protocol security of a web endpoint.

## Prerequisites

- testssl.sh installed (`git clone https://github.com/drwetter/testssl.sh.git` or `brew install testssl`)
- Verify: `testssl.sh --version` or `./testssl.sh --version`

## Instructions

1. **Identify the target** — Confirm the hostname:port to test.
2. **Run the scan:**
   ```bash
   testssl.sh --json <hostname>:<port> > testssl-results.json
   ```
   - Default HTTPS: `testssl.sh --json example.com`
   - Quick mode: `testssl.sh --fast --json example.com`
   - Specific checks only:
     - Protocols: `testssl.sh --protocols --json example.com`
     - Ciphers: `testssl.sh --cipher-per-proto --json example.com`
     - Vulnerabilities: `testssl.sh --vulnerable --json example.com`
     - Certificate: `testssl.sh --server-defaults --json example.com`
3. **Parse the results** — Present findings:

```
| # | Severity | Category | Finding | Details |
|---|----------|----------|---------|---------|
```

4. **Summarize** — Provide:
   - Protocol support (TLS 1.0/1.1/1.2/1.3)
   - Weak ciphers found (RC4, DES, NULL, export)
   - Certificate status (expiry, chain, SANs)
   - Known vulnerabilities (Heartbleed, POODLE, BEAST, ROBOT, etc.)
   - Grade/rating and specific remediation

## Key Vulnerability Checks

| Vulnerability | Impact |
|--------------|--------|
| Heartbleed (CVE-2014-0160) | Memory disclosure |
| POODLE (CVE-2014-3566) | SSLv3 padding oracle |
| ROBOT | RSA decryption oracle |
| BEAST (CVE-2011-3389) | CBC cipher weakness |
| CRIME (CVE-2012-4929) | TLS compression attack |
| FREAK (CVE-2015-0204) | Export cipher downgrade |
| Logjam (CVE-2015-4000) | Weak DH parameters |
| DROWN (CVE-2016-0800) | SSLv2 cross-protocol attack |
