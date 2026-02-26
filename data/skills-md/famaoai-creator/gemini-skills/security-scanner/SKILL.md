---
name: security-scanner
description: Scans the codebase for security risks, including hardcoded secrets (API keys, tokens), dangerous code patterns (eval, shell injection), and insecure configurations. Use to audit code before committing or reviewing.
status: implemented
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - compliance
  - gemini-skill
  - integration
  - security
related_skills:
  - html-reporter
  - project-health-check
---

# Security Scanner

## Overview

This skill performs a security audit on the current project using **Trivy** (if available) or a lightweight internal scanner. It detects vulnerabilities, secrets, and dangerous patterns.

## Capabilities

### 1. Advanced Scan (via Trivy)

If `trivy` is installed, this skill leverages it for enterprise-grade auditing:

- **Vulnerabilities (SCA)**: Checks `package.json`, `go.mod`, `requirements.txt`, etc., for known CVEs.
- **Misconfigurations (IaC)**: Scans Dockerfiles, Terraform, and Kubernetes manifests for security best practices.
- **Secret Scanning**: Deep inspection for leaked API keys and tokens.
- **License Compliance**: Checks for license risks in dependencies.

### 2. Lightweight Scan (Fallback)

If `trivy` is missing, it falls back to a fast, pattern-based internal scanner:

- **Secret Detection**: AWS keys, GitHub tokens, generic secrets.
- **Dangerous Code**: `eval()`, `dangerouslySetInnerHTML`, command injection risks.
- **PII Leakage Audit**: Identifies potential logging of sensitive data (emails, PII) based on [Modern SRE Best Practices](../knowledge/operations/modern_sre_best_practices.md).

## Usage

Run the scanner from the root of your project.

```bash
node scripts/scan.cjs
```

## Configuration

- **Trivy**: Uses default settings.
- **Internal Scanner**:
  - **Proprietary Patterns**: Automatically checks `knowledge/confidential/skills/security-scanner/` for internal regex rules. These rules are prioritized over general ones to detect company-specific security risks.
  - **General Patterns**: Uses `knowledge/security/scan-patterns.yaml`.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
