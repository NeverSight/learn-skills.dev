---
name: testing-strategy
description: "Selects the one owning test for each acceptance criterion at the boundary where its behavior is observable, using repository evidence and maintenance cost. Use when deciding integration or E2E coverage."
---

# Test Strategy

## Purpose

Select one owning test per behavioral claim at the boundary where the claim is observable, as `testing` defines. Candidate discovery does not create an obligation to implement every technically valid test.

## Selection Process

For each acceptance criterion that may require integration or E2E proof:

1. **Name the observable boundary**: Identify the interaction, persisted effect, process, or user journey that must be proven.
2. **Check the existing owner**: When an established test owns the claim at that boundary with assertions that detect its material failure, update it rather than adding another.
3. **Select the owning level**:
   - use integration when the behavior is observable at a component, persistence, or process boundary;
   - use E2E when the behavior is observable only across the complete journey;
   - leave the cases of a calculation, parsing, or branching rule inside the behavior to that rule's unit test.
4. **Compare cost**: Consider setup, execution time, brittleness, maintenance, and diagnostic value using repository evidence rather than fixed universal scores.
5. **Retain valuable proof**: Select a new test only when its regression-detection value justifies that cost.

No new integration or E2E test is a valid conclusion when existing tests already own each claim.

## Priority

Prioritize proof for:

- core user or consumer journeys;
- shared or public contracts;
- persisted state transitions;
- security, authorization, compliance, or irreversible effects;
- integrations with demonstrated failure risk.

Priority does not determine test level. Use the narrowest boundary that can observe the prioritized behavior.

## Deduplication

Before adding a test:

- search the existing suite for equivalent behavior;
- identify overlapping proof at other levels;
- extend existing coverage when that remains clear and maintainable;
- keep one representative proof when several candidates observe the same risk.

## Selection Record

Record only decisions needed by planning or review:

```text
Acceptance criterion: [identifier or behavior]
Selected proof: existing | unit | integration | E2E | none
Boundary observed: [observable interaction or result]
Reason: [why this test owns the claim at this boundary]
```

## Completion Check

- Every selected test traces to an observable requirement or accepted contract.
- Each claim has one owning test, and an existing owner was updated rather than duplicated.
