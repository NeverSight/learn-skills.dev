---
name: fable-security
description: "Conduct threat modeling, vulnerability assessments, secret sanitization, and security reviews across trust boundaries, auth flows, and untrusted inputs. Use when auditing authentication/authorization logic, inspecting APIs for injection/CORS/CSRF risks, checking for hardcoded credentials, or reviewing security-sensitive diffs — even if the user does not explicitly say \"fable-security\" (e.g. \"security audit this code\", \"check for vulnerabilities\", \"verify auth logic\", \"scan for leaked secrets\"). Do NOT use for general style reviews (use fable-review) or non-security bug fixes (use fable-tdd)."
version: 1.3.0
pack: proof
inputs:
  - security_scope
requires:
  - threat_boundary
produces:
  - security_evidence
  - threat_boundary_verdict
gates:
  - threat_surface_checked
  - no_exposed_secrets
fallback: fable-plan
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - fable-verify
    - fable-review
  continuations:
    - fable-release
  lateral_peers:
    - fable-review
  recovery: fable-recover
---

# Fable Security

Reason about attacker-controlled paths and trust boundaries until every security finding has a concrete source, sink, prerequisite, and impact.

## Mission
Security review is not a secret scan plus a generic checklist. It asks what an attacker can control, which privilege/data boundary that input can cross, what enforcement must hold, and whether the changed code preserves that property under failure and concurrency.

A clean scanner is evidence about scanner coverage, not a proof that the design is secure.

## Activate When
- authentication, authorization, sessions, tokens, permissions, tenancy, or privileged actions change;
- untrusted input reaches parsers, queries, templates, files, URLs, shells, webhooks, or deserializers;
- secrets/credentials or cryptographic material are handled;
- a diff changes trust boundaries, network exposure, storage access, package/install logic, or sandboxing;
- a reported vulnerability/finding needs validation or severity calibration;
- repository/package supply-chain behavior needs security review.

## Do Not Activate When
- the task is only functional verification with no security question (`fable-verify`);
- a generic maintainability review has no trust-boundary impact (`fable-review`);
- a vulnerability is already validated and the user wants only a bounded fix (`fable-execute`, while preserving security acceptance).

## Security Work Classification
| Mode | Primary question |
| --- | --- |
| Threat model | what assets/actors/boundaries/abuse paths exist? |
| Security diff review | what security property changed in this diff? |
| Finding validation | can attacker-controlled data actually reach a sensitive sink? |
| Repository audit | which exposed surfaces deserve deeper inspection? |
| Secret hygiene | can sensitive values enter source/logs/artifacts? |
| Supply-chain/package | can dependency/install/build boundaries be abused? |

## Protocol
### Stage 1 — Define assets, actors, and trust boundaries
Identify:
- protected assets/data/operations;
- authenticated/unauthenticated/privileged actors;
- tenant/user ownership boundaries;
- external systems/webhooks/plugins;
- process/filesystem/network privilege transitions.

Security conclusions without a named boundary are usually too vague.

### Stage 2 — Trace attacker-controlled input to effect
For each relevant entrypoint follow:
`source → parsing/normalization → validation → authorization → transformation → sensitive sink/side effect`

Record where each security property is enforced and whether later transformations can invalidate earlier validation.

### Stage 3 — Check the property appropriate to the boundary
Consider as relevant:
- authentication vs authorization separation;
- object/tenant ownership (IDOR/BOLA);
- CSRF/state binding and redirect validation;
- injection/query/template/shell boundaries;
- path traversal/symlink/archive extraction;
- SSRF and URL/DNS/redirect handling;
- file upload content/size/storage/execution boundaries;
- deserialization/parser resource abuse;
- session/token expiry, replay, rotation, audience/issuer;
- secrets in logs/errors/artifacts;
- fail-open error handling;
- race/TOCTOU and check-then-act authorization;
- privilege escalation via configuration/plugins/hooks;
- dependency/install script/supply-chain assumptions.

### Stage 4 — Model failure and alternate paths
Ask:
- What happens when validation service fails?
- Is denial the default or does code continue?
- Can retries duplicate a privileged action?
- Can an attacker alter state between check and use?
- Do background jobs re-check authorization or trust stale caller claims?
- Does a redirect/proxy/parser transform the value after validation?

### Stage 5 — Validate findings skeptically
For each candidate finding establish:
- attacker prerequisites/control;
- reachable source;
- exact sink/privileged effect;
- missing/bypassed control;
- realistic exploitation path;
- impact/scope;
- existing mitigations that may invalidate or reduce severity.

Do not report a vulnerability merely because a dangerous API exists.

### Stage 6 — Calibrate severity
Severity depends on exploitability + privilege gained + data/tenant scope + required conditions, not scanner labels alone.

Use `blocking` for plausible exploitable issues that violate a required security property. Mark uncertain candidates as needing validation instead of inflating them.

### Stage 7 — Produce bounded remediation evidence
A repair recommendation should name the property to restore and how to prove it, e.g. tenant ownership enforced atomically before mutation, canonical path contained after symlink resolution, redirect allowlist applied to normalized destination.

### Stage 8 — Keep security and functionality separate
Security evidence can block release, but does not substitute for functional test/build/runtime evidence. After repair, both security-specific and functional verification may be required.

## Decision Rules
- Authentication proves identity; it does not prove authorization for a resource/action.
- Validate/authorize as close as practical to the sensitive side effect, especially across async/background boundaries.
- Normalize/canonicalize before containment/allowlist checks when transformations can change meaning.
- Prefer allowlists/capability checks over blocklists for constrained destinations/actions.
- A secret removed from current source may still exist in Git history/logs/artifacts; rotate exposed credentials when exposure is credible.
- Scanner finding with no reachable attacker-controlled path is not automatically exploitable; validate source-to-sink.
- Scanner clean result does not close design-level authz/logic threats.
- Do not execute destructive exploit payloads against real systems; use safe local/fixture proof or code-path reasoning.
- If remediation changes product behavior, hand to TDD/execute and require functional verification afterward.

## Invariants
- Raw secrets are never reproduced in evidence or logs.
- Every reported vulnerability has a concrete failure property and reachable path or is clearly labeled unvalidated.
- Tenant/resource authorization is evaluated independently from login status.
- Security review remains read-only unless explicitly shifted to remediation.
- Functional correctness and security correctness remain separate evidence classes.

## Failure Taxonomy
### False positive
Dangerous primitive exists but attacker cannot control source/reach sink or mitigation blocks it. Downgrade/drop with evidence.

### Hidden trust transition
Code crosses queue/plugin/proxy/background/storage boundary and assumes upstream validation. Trace/revalidate required property.

### Fail-open path
Control error/timeout falls through to privileged behavior. Treat as high-priority boundary failure.

### TOCTOU/race
Authorization/containment check is separated from side effect and mutable state can change. Seek atomic primitive/revalidation.

### Sanitization mismatch
Validation occurs before decode/normalization/redirect/symlink resolution. Check canonical value at sink boundary.

### Secret exposure
Credential entered source/log/artifact/history. Remove exposure path and require rotation/containment as applicable.

## Anti-Patterns
- "no high CVEs, therefore secure";
- generic OWASP checklist without tracing changed paths;
- equating authenticated user with authorized user;
- regex path checks before canonical resolution;
- trusting webhook fields solely because request reached a webhook endpoint;
- reporting theoretical API danger with no attacker path;
- logging raw tokens to debug auth;
- testing exploitability against production without authorization;
- fixing security by disabling validation or broadening permissions to make tests pass.

## Security Finding Packet
```text
Security property:
Asset/boundary:
Attacker prerequisites:
Source → transformations → control → sink:
Concrete failure scenario:
Existing mitigations:
Severity + rationale:
Evidence/location:
Bounded remediation property:
Security re-test:
Functional verification still required:
```

## Completion Criteria
Security work completes when:
- relevant trust boundaries and attacker-controlled paths were traced;
- candidate findings were validated/calibrated rather than pattern-matched;
- secrets were not exposed during analysis;
- blocking findings have bounded remediation/verification criteria;
- verdict states exactly what security property was checked and what remains not checked.

## Progressive Resources
- Deep guide: `references/trust-boundary-and-finding-validation.md`
- Existing threat matrix: `references/threat-modeling-matrix.md`
- Secret hygiene: `references/secret-sanitization.md`
- Example: `examples/security-audit-walkthrough.md`
