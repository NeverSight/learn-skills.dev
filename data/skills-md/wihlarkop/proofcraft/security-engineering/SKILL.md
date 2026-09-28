---
name: security-engineering
description: >-
  Design or review software security around trust boundaries, authentication, authorization,
  secrets, untrusted input, file/network exposure, tenant isolation, abuse resistance, and supply
  chain risk. Use when a change crosses a security boundary or requests threat modeling, secure
  design, or security review. Validate exploitability/context before reporting findings; do not
  conflate privacy lifecycle requirements with security implementation.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Security Engineering

Protect trust boundaries with evidence, not generic fear lists.

## Modes

- threat model;
- secure design;
- security review.

## Workflow

1. Identify assets, actors, trust boundaries, privileged actions, and untrusted inputs.
2. Trace the actual data/control path before proposing controls or reporting a vulnerability.
3. Define authentication and authorization at the resource/action boundary; avoid relying on UI visibility or client-supplied identity.
4. Keep secrets out of source/client bundles/logs and minimize credential scope/lifetime.
5. Validate/parsing/file/network boundaries according to the actual downstream capability and framework protections.
6. For reviews, confirm whether the suspected issue is reachable/exploitable in context and account for existing framework/transport protections.
7. Report residual risk and supporting privacy/reliability/platform concerns without taking over their ownership.

## Stop

Stop when material trust-boundary risks are mitigated, explicitly accepted, or evidenced as non-issues. Do not inflate low-confidence speculative findings.
## Reference Guide

Load only the references needed for the current task:

- [authz secrets](references/authz-secrets.md)
- [security review](references/security-review.md)
- [threat model](references/threat-model.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
