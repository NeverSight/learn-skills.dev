---
name: security-secure-coding
description: "Security workflow for secure-by-default coding decisions and vulnerability prevention in implementation changes. Use when application code paths process untrusted input, sensitive data, or privileged operations; do not use for policy-only governance without code impact."
---

# Security Secure Coding

## Overview
Use this skill to prevent introducing exploitable code patterns and to enforce explicit security invariants during implementation.

## Scope Boundaries
- New endpoints, parsers, deserializers, or command execution paths are added.
- Sensitive data handling or trust-boundary crossing logic changes.
- High-risk dependency or framework behavior needs secure usage decisions.

## Templates And Assets
- Secure coding review checklist:
  - `assets/secure-coding-review-checklist.md`

## Inputs To Gather
- Trust boundaries and untrusted input entry points.
- Sensitive data flows and storage/transmission requirements.
- Language/framework-specific risk patterns.
- Existing test coverage and security tooling signals.

## Deliverables
- Security invariants for the changed code path.
- Mitigation mapping for relevant threat classes.
- Targeted secure coding checks and tests.
- Residual risk notes for deferred hardening work.

## Workflow
1. Identify attack surfaces for the change (input parsing, file/network access, auth context, templating).
2. Run checklist from `assets/secure-coding-review-checklist.md`.
3. Apply allowlist validation and context-appropriate encoding/sanitization at boundaries.
4. Remove or harden dangerous patterns (shell concatenation, unsafe deserialization, path traversal gaps, SSRF primitives).
5. Enforce explicit authorization checks in server-side handlers for sensitive operations.
6. Protect secrets and PII in logs, errors, and telemetry outputs.
7. Add or update negative tests for malicious payload classes.
8. Verify dependencies and transitive packages for known critical vulnerabilities.

## Quality Standard
- Security-relevant assumptions are explicit in code and tests.
- Error paths fail closed for sensitive operations.
- No sensitive data leaks through logs or debug output.
- High-risk operations are wrapped with deliberate validation and policy checks.

## Failure Conditions
- Stop when trust-boundary validation is missing or implicit.
- Stop when privileged operations execute without explicit authorization checks.
- Escalate when unresolved critical vulnerabilities remain in production-bound paths.
