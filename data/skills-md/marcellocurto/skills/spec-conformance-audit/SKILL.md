---
name: spec-conformance-audit
description: Check whether an implementation matches its source specification and agreed decisions.
---

# Spec Conformance Audit

Determine whether the implementation matches what was authorized.

Audit only. Do not edit files, apply fixes, commit, publish, or mutate external systems unless the user separately asks for implementation.

## Goal

Check each requirement and each rule about what must stay unchanged against the implementation. Identify behavior changed outside the agreed scope.

## Establish the Contract

Establish the requirements from:

- the user's latest explicit decisions and corrections
- the named specification, issue, plan, or selected review feedback
- repository instructions and established contracts that the work did not authorize changing

Later explicit decisions override earlier proposals. A suggestion is not a requirement merely because it appears in a plan or prior model response. Current implementation behavior is evidence, not automatically the intended contract.

Extract only what affects the verdict:

- required outcomes and acceptance criteria
- behavior, data, interfaces, and user flows that must remain unchanged
- work explicitly excluded from the change
- unresolved decisions that were not authorized for implementation

If sources materially conflict and their precedence cannot be established, report the conflict instead of inventing a merged requirement.

## Inspect the Implementation

Inspect the relevant diff, current code, affected callers and consumers, and verification evidence. Read surrounding code only when needed to understand a contract, behavior boundary, or possible spillover.

For each material requirement or protected constraint, classify it as:

- `satisfied`: implemented with adequate evidence
- `partial`: evidence confirms that some required behavior exists and another required part is absent
- `missing`: evidence from the relevant implementation establishes that the required behavior is absent
- `contradicted`: implementation does the opposite of the contract
- `unverified`: available evidence cannot establish satisfaction, including when implementation appears present but necessary execution evidence is missing

Missing execution evidence, inaccessible code, or an inconclusive search does not establish missing implementation. Record what the code does demonstrate and the exact proof still needed. Do not mark a requirement `partial` merely because only part of its verification has run.

Report **unauthorized expansion** separately when the work changes behavior outside the contract, such as unrelated product surfaces, schemas, export formats, business rules, external records, dependencies, or compatibility policy. Extra code is not automatically unauthorized: require a concrete behavioral, operational, or maintenance consequence beyond the approved scope.

## Evidence Standard

- Cite the exact contract source and implementation location for every material finding.
- Separate observed facts from inference.
- Do not credit a requirement based only on naming, comments, or a test that does not exercise the promised behavior.
- Do not fail conformance for style, architecture, complexity, test quantity, or personal preference unless the contract explicitly governs it.
- When acceptance depends on a user-visible path or generated artifact, require evidence from that path to claim satisfaction. Its absence is a verification gap; retain any deviation independently established by code or observed behavior.

## Coordinate journey evidence

Reuse relevant results from `user-journey-verifier` when they cover the same implementation or artifact version, entry point, inputs, and conditions. When a material acceptance gap remains, use the `user-journey-verifier` skill when available, within the request's verification scope. Pass the requirement, expected outcome, actual user or consumer path, and relevant environment rather than requesting another general verification pass. If the skill is unavailable, verify that path directly within the same scope and report the observed outcome or exact evidence gap.

Journey verification may run before the audit or close a gap found during it; a conforming verdict is not a prerequisite. Credit a passing result only for the requirements it directly proves. Classify a failure from its observed mismatch and available implementation evidence, without assuming failed behavior means absent code. An unavailable or inconclusive journey remains a verification gap, not an implementation defect.

## Output

Choose the overall verdict in this order:

1. **Non-conforming:** at least one requirement or unchanged-behavior constraint has a confirmed implementation gap or violation, or the change includes unauthorized behavior. Use the per-requirement statuses to show what is partial, missing, or contradicted.
2. **Unverified:** no confirmed violation determines the verdict, but a required check or fact is missing.
3. **Conforming:** every requirement and unchanged-behavior constraint is satisfied, and no unauthorized expansion remains.

When a confirmed violation and missing verification coexist, report non-conformance and list the unverified requirements separately. A check that was not run is not proof of a defect, and it must not hide one already established.

Lead with that verdict, then show the requirements and evidence in a compact table:

| Requirement or constraint | Source | Implementation and verification evidence | Status |
| --- | --- | --- | --- |

After the table, include only applicable sections:

- **Unauthorized expansion**: behavior changed outside the approved scope
- **Evidence gaps**: claims that cannot yet be verified and the exact proof needed
- **Next step**: the correction or check needed within the agreed scope, without implementing it

If every material requirement and protected constraint is satisfied and no unauthorized expansion exists, say so directly without inventing findings.

## Stop Rules

Stop when every material requirement and protected constraint has a classification, unauthorized expansion has been checked, and the remaining evidence gaps are explicit.
