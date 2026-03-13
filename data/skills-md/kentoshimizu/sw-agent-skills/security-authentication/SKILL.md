---
name: security-authentication
description: "Security workflow for authentication architecture, credential lifecycle, and session/token assurance. Use when login, identity proofing, MFA, or session security decisions are required; do not use for authorization policy design or non-security quality tuning."
---

# Security Authentication

## Overview
Use this skill to design and review authentication flows that resist account takeover while preserving acceptable user friction.

## Scope Boundaries
- Authentication factors, login flows, or account-recovery behavior are being introduced or changed.
- Session management (cookie/token TTL, refresh policy, revocation) needs to be defined.
- Risk-based controls (MFA, step-up auth, suspicious login handling) are required.

## Templates And Assets
- Authentication assurance matrix:
  - `assets/auth-assurance-matrix-template.md`

## Inputs To Gather
- Identity sources and trust level requirements (internal users, external users, federated identities).
- Threat assumptions (credential stuffing, phishing, token theft, session hijacking).
- Regulatory and product constraints (MFA mandates, session timeout policy, UX limits).
- Operational constraints (IdP availability, incident response expectations, observability baseline).

## Deliverables
- Authentication flow map for primary login, re-auth, and recovery paths.
- Credential and token/session policy (issuance, storage, rotation, revocation, expiry).
- Control matrix for anti-abuse protections and detection signals.
- Residual risk list with owners and verification checkpoints.

## Workflow
1. Define assurance targets by action sensitivity using `assets/auth-assurance-matrix-template.md`.
2. Select factor strategy (password, passkey, OTP, federated SSO) using attacker capability and usability constraints.
3. Design session/token lifecycle with explicit expiry, refresh, revocation, and device binding rules.
4. Add anti-automation and abuse controls for login and recovery endpoints.
5. Specify fallback and lockout policy that avoids permanent user denial while blocking attacker persistence.
6. Define telemetry for login success/failure, suspicious patterns, and step-up triggers.
7. Validate flows with negative scenarios: replay, stolen token use, brute-force, and recovery abuse.

## Quality Standard
- Every sensitive action has a declared required assurance level.
- Session/token invalidation behavior is explicit and testable.
- Recovery flow is at least as strong as primary authentication assurance.
- Audit signals are actionable for incident triage.

## Failure Conditions
- Stop when account recovery can bypass primary assurance guarantees.
- Stop when token/session revocation behavior is undefined.
- Escalate when control strength cannot meet required risk level.
