---
name: offensive-tls-attacks
description: "TLS/SSL and PKI security configuration auditing covering TLS 1.2/1.3 cipher suite selection, forward secrecy (ECDHE), HSTS preload, Certificate Authority Authorization (CAA) DNS records, OCSP stapling, and mTLS validation."
---

# TLS/SSL & PKI Configuration Audit (`offensive-tls-attacks`)

> **Authorization & Scope Notice:** This skill is part of the **REA_Skill + claude-red Unified Security & Reverse Engineering Suite**. It is designed strictly for **authorized security assessments, defensive architecture reviews, vulnerability triage, bug bounty verification, and remediation engineering** on software, infrastructure, and assets you own or have explicit permission to test.

## Overview

TLS/SSL and PKI security configuration auditing covering TLS 1.2/1.3 cipher suite selection, forward secrecy (ECDHE), HSTS preload, Certificate Authority Authorization (CAA) DNS records, OCSP stapling, and mTLS validation.

---

## Operational Workflow

1. **Surface & Architecture Inventory**
   - Identify all entrypoints, trust boundaries, parsers, and configuration files relevant to **TLS/SSL & PKI Configuration Audit** (`crypto` domain).
   - Combine static code/binary inspection (via REA MCP tools, `rg`, AST analysis, or decompilation) with runtime configuration verification.
2. **Hypothesis & Vulnerability Verification**
   - Test each security invariant systematically against known CWE and OWASP patterns.
   - Record concrete evidence: affected file/procedure, line numbers or binary offsets, request/response trace, and root cause.
3. **Impact & Reachability Triage**
   - Evaluate whether the issue is reachable across trust boundaries, whether defense-in-depth controls mitigate it, and compute an accurate CVSS v3.1 / v4.0 score.
4. **Remediation & Regression Verification**
   - Implement or provide production-ready, copy-pasteable remediation code.
   - Write an automated regression test or verification command to prove the flaw is resolved with 0 regressions.

---

## Audit & Verification Checklist

| Phase | Check | Verification Method | Expected Secure State |
| :--- | :--- | :--- | :--- |
| **1. Discovery** | Enumerate all `crypto` surfaces and dependencies | Source search / REA binary & bundle inspection | Complete inventory of trust boundaries |
| **2. Input & State** | Validate parser behavior, type safety, and state transitions | Boundary testing & static taint analysis | Strict schema validation and invariant checks |
| **3. Auth & Isolation** | Verify caller identity, tenant isolation, and least privilege | Horizontal/vertical privilege matrix check | Explicit deny-by-default enforcement |
| **4. Defense-in-Depth** | Inspect secondary controls, logging, and compiler/runtime flags | Config & header/binary flag audit | Full hardening and telemetry enabled |
| **5. Remediation** | Apply fix and execute automated regression test | `npm test` / toolchain build & test suite | 0 vulnerabilities, 0 build errors |

---

## Integration with REA MCP & Tooling

- **Static & Binary Analysis:** Pair with `rea-universal-orchestrator`, `rea-binary-disassembly`, `rea-web-bundle-recovery`, or `rea-mobile-app-recovery` when source code is unavailable.
- **Interactive Scoping:** Invoke `/rea-grill-me` before large-scale assessments to clarify scope, target environments, and acceptance criteria.
- **Reporting:** Pair with `offensive-reporting` to format findings with CVSS vectors, CWE mappings, and remediation patches.
