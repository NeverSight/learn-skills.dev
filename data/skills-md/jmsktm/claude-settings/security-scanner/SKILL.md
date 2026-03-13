---
name: Security Scanner
slug: security-scanner
description: Scan code and infrastructure for security vulnerabilities and compliance issues
category: technical
complexity: advanced
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "security scan"
  - "vulnerability check"
  - "security audit"
tags:
  - security
  - vulnerabilities
  - compliance
---

# Security Scanner

Scan code and infrastructure for security vulnerabilities. Identify issues before they become breaches with systematic security analysis.

## Core Workflows

### Workflow 1: Code Security Scan
1. **SAST** - Static application security testing
2. **Dependency Check** - Scan for vulnerable dependencies
3. **Secrets Detection** - Find hardcoded credentials
4. **OWASP Check** - Review against OWASP Top 10
5. **Report** - Generate findings report

### Workflow 2: Infrastructure Security
1. **Configuration Audit** - Check security settings
2. **Network Scan** - Identify exposed services
3. **Access Review** - Audit permissions and IAM
4. **Compliance Check** - Verify against standards
5. **Remediation Plan** - Prioritize and fix issues

## Quick Reference

| Action | Command |
|--------|---------|
| Scan code | "Run security scan on [repo]" |
| Check dependencies | "Scan for vulnerable dependencies" |
| Audit infrastructure | "Security audit [environment]" |
