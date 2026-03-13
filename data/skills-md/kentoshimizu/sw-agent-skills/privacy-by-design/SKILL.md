---
name: privacy-by-design
description: "Privacy-by-design workflow for embedding data minimization, lawful basis, retention, and user-rights readiness into product decisions. Use when a feature touches personal data and privacy controls must be defined before implementation; do not use for narrow infrastructure tuning that does not affect personal-data handling."
---

# Privacy By Design

## Overview
Use this skill to make privacy requirements explicit, enforceable, and testable before implementation.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Lawful basis and minimization rules:
  - `references/lawful-basis-and-minimization-rules.md`

## Templates And Assets
- Privacy control matrix template:
  - `assets/privacy-control-matrix-template.csv`
- Data lifecycle map template:
  - `assets/data-lifecycle-map-template.md`

## Inputs To Gather
- Feature scope and personal-data touchpoints.
- Applicable legal/policy obligations for target markets.
- Data flow boundaries and third-party transfers.
- Retention and user-rights operational capabilities.

## Deliverables
- Privacy control matrix with ownership.
- Data lifecycle map from collection to deletion.
- Consent/notice and user-rights requirements.
- Residual privacy risk and approval record.

## Workflow
1. Map lifecycle with `assets/data-lifecycle-map-template.md`.
2. Define controls in `assets/privacy-control-matrix-template.csv`.
3. Validate decisions against `references/lawful-basis-and-minimization-rules.md`.
4. Confirm operational feasibility for retention/deletion/rights handling.
5. Publish controls and unresolved risks.

## Quality Standard
- Every data element has explicit purpose and legal basis/authorization.
- Data collection is minimized and retention is bounded.
- User-rights handling is operationally executable.

## Failure Conditions
- Stop when lawful basis or purpose limitation is undefined.
- Stop when retention/deletion controls cannot be enforced.
- Escalate when transfer safeguards or approvals are missing.
