---
name: code-review-security
description: "Run security-focused code review when changes cross trust boundaries or may affect authentication, authorization, input validation, secrets handling, or sensitive-data exposure. Use for merge decisions requiring explicit security findings; do not use for non-security-only review scope."
---

# Code Review Security

## Overview
Use this skill to identify exploitable weaknesses and data-protection risks before merge.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Changed trust boundaries (external input, authn/authz, storage, outbound calls).
- Sensitive data categories and handling paths.
- Existing security controls (validation, encoding, policy checks, audit logs).
- Threat model assumptions relevant to the changed area.

## Deliverables
- Security findings with exploit path and severity.
- Risk acceptance/escalation items for unresolved issues.
- Required remediation and verification actions.

## Finding Focus Areas
- Input validation and injection paths.
- Authn/authz bypass and privilege escalation.
- Secret leakage in code, logs, or telemetry.
- Sensitive data exposure at rest/in transit/in logs.
- Unsafe defaults, fallback auth, or policy bypass paths.

## Quick Example
- Diff adds debug log containing full JWT token.
- Finding: high-severity secret exposure risk.
- Fix direction: redact token, log token hash/metadata only.

## Quality Standard
- Findings describe concrete exploit scenario, not vague concern.
- Severity reflects impact + exploitability.
- Fix guidance removes root cause and prevents recurrence.
- Residual risk is explicit when immediate full fix is infeasible.

## Workflow
1. Map changed code to trust boundaries and assets.
2. Evaluate exploit paths across input, auth, and data handling.
3. Verify security controls are present and correctly ordered.
4. Identify regressions introduced by fallback or bypass logic.
5. Publish prioritized findings and remediation requirements.

## Failure Conditions
- Stop when high-severity vulnerabilities remain unresolved.
- Escalate when risk acceptance exceeds policy or lacks approver.
