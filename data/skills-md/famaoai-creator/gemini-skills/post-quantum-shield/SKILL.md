---
name: post-quantum-shield
description: Audits codebases for quantum-vulnerable cryptography and plans migration to Post-Quantum Cryptography (PQC) standards to ensure long-term data security.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Project directory
  - name: out
    short: o
    type: string
    description: Output file path
category: Utilities
last_updated: '2026-02-13'
tags:
  - compliance
  - data-engineering
  - gemini-skill
  - security
---

# Post-Quantum Shield

This skill prepares your system for the era of quantum computing by securing data against future decryption threats.

## Capabilities

### 1. Quantum Vulnerability Scan

- Identifies usage of algorithms like RSA, ECC, and Diffie-Hellman that are vulnerable to Shor's algorithm.
- Audits TLS configurations and SSH keys.

### 2. PQC Migration Planning

- Recommends replacement with NIST-approved PQC algorithms (e.g., Kyber, Dilithium).
- Helps implement hybrid cryptographic schemes for a safe transition.

## Usage

- "Perform a quantum vulnerability audit on our encryption layer."
- "Generate a migration plan to upgrade our root certificates to post-quantum standards."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
