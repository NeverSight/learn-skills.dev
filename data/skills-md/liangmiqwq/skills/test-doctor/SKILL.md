---
name: test-doctor
description: Audit and improve an existing software project's automated tests as regression protection. Use when Codex needs to assess test quality, map tests to user-visible capabilities or documented contracts, find implementation-coupled, over-mocked, dead, duplicate, fragile, or low-value tests, reduce CI cost, design a test migration plan, or refactor tests while preserving meaningful coverage. Applies to unit, integration, contract, component, and end-to-end suites across languages and frameworks.
---

# Test Doctor

Treat tests as product protection, not implementation proof. Ask of each test: "If this fails, which user-visible capability or documented contract is probably broken?" If there is no concrete answer, require evidence that the test deserves to remain.

## Select the operating mode

- For audit, analysis, diagnosis, or planning requests, inspect and report without editing files.
- For explicit change requests, audit first, then make the smallest test changes that preserve or improve regression protection.
- Do not change production behavior merely to satisfy a test unless the user explicitly requests that fix.
- Read repository instructions and the relevant design or contract documents before evaluating intended behavior. Report a contract mismatch instead of guessing which side is correct.

## Build an evidence base

1. Locate test files, fixtures, helpers, configuration, package scripts, and CI workflows.
2. Identify source-package boundaries and public entry points.
3. Read relevant feature, architecture, API, and bug-fix documentation.
4. Inspect focused git history when it explains why a suspicious test exists.
5. Record the available test commands and their scope. Run only commands needed to verify a finding or requested change.

For a large repository, start with package-level inventory and high-risk paths. Expand to individual tests only where evidence indicates low signal, duplication, fragility, or missing protection.

## Map tests to protected capabilities

Create a compact map with one row per test file or coherent test group:

| Field | Meaning |
| --- | --- |
| Test | File and test or suite name |
| Type | Unit, integration, contract, component, or E2E |
| Protected capability | User behavior or documented contract detected by failure |
| Boundary | Real dependencies and substituted dependencies |
| Risk | Impact and likelihood of regression |
| Cost | Runtime, setup complexity, brittleness, and maintenance burden |
| Confidence | High, medium, or low, with evidence |

Mark the protected capability as `unclear` when evidence is insufficient. Do not invent intent from test names alone.

## Evaluate test value

Use this as a relative heuristic, not a fabricated numeric measurement:

```text
Test value = user impact × regression risk × bug-detection strength
             --------------------------------------------------------
                            maintenance cost
```

Rate each factor as high, medium, or low and explain disputed ratings.

Prioritize tests that protect:

- User workflows, data correctness, security, compatibility, and recovery.
- Public APIs, provider interfaces, persistence formats, migrations, and cross-package contracts.
- Core runtime orchestration, file handling, session state, and important failure paths.
- Boundary conditions that have failed before or are easy to regress.

Discount tests that primarily protect:

- Private helpers, internal object shape, exact call order, or incidental function counts.
- Mock configuration rather than observable behavior.
- Static formatting with no contract or user impact.
- Duplicate paths already protected more directly at a stronger boundary.

Increase the maintenance-cost rating for heavy snapshots, excessive mocks, fragile selectors, internal API coupling, large duplicated fixtures, timing dependence, and slow environment setup.

## Detect test smells

### Implementation coupling

Flag assertions about private methods, internal state, exact call order, or incidental calls. Recommend assertions on returned state, persisted data, emitted public events, rendered semantics, or externally observable errors.

Do not flag interaction assertions automatically. Keep them when the interaction itself is the contract, such as authorization checks, idempotency, transaction boundaries, or required protocol calls.

### Excessive mocking

Flag suites where most collaborators are mocked and the assertions only restate mock behavior. Prefer the narrowest realistic boundary:

- Real domain logic and stores.
- In-memory databases or filesystems when faithful.
- Small deterministic fakes for network or model providers.
- Mocks only at expensive, nondeterministic, destructive, or externally owned boundaries.

### Dead or vacuous tests

Find skipped or focused tests, empty tests, tautological assertions, obsolete APIs, unreachable setup, tests that cannot fail after the exercised code is removed, and snapshots that accept meaningless churn.

Classify skipped tests carefully: a linked known issue may be deferred coverage rather than dead code.

### Duplicate coverage

Group tests by capability and failure mode, not by similar names. Call coverage duplicate only when removing one test would not reduce detection of a distinct regression. Prefer merging repeated setup and closely related lifecycle behavior into one coherent integration or contract suite.

### Snapshot overuse

Keep snapshots for stable, reviewable contracts such as accessibility output, serialized protocols, or critical UI states. Replace broad generated markup and noisy component snapshots with focused semantic assertions.

### Missing negative and boundary coverage

Look for happy-path-only suites around validation, permissions, cancellation, retries, partial failure, concurrency, migration, recovery, and unknown variants. Recommend additions only when a concrete contract and credible regression are identifiable.

## Choose a treatment

Choose exactly one primary action per finding:

- **Keep**: The test protects distinct behavior at reasonable cost.
- **Delete**: The test is dead, vacuous, or fully redundant and retained coverage is identified.
- **Merge**: Several tests protect one capability with duplicated setup or assertions.
- **Move**: The behavior belongs at a different boundary, usually integration or contract level.
- **Rewrite**: The capability matters, but the current assertions protect the wrong abstraction.
- **Promote**: Repeated lower-level cases reveal a missing public contract or end-to-end workflow test.
- **Add**: A high-risk capability has no effective regression protection.

Never recommend deletion without naming the retained protection or explicitly identifying the accepted coverage gap.

## Handle agent and Electron applications

When relevant, inspect these high-value contracts:

- Provider: initialization, model discovery, streaming, tool calls, reasoning support, usage reporting, cancellation, and errors.
- Runtime: user input, context assembly, model request, tool execution, persistence, and final response.
- Storage: session creation, message append, history loading, migration, recovery, and corruption handling.
- Skills and plugins: install, discovery, loading, execution, permissions, and failure isolation.
- Desktop UI: renderer behavior through public preload or IPC contracts, accessible interaction, persisted state, and platform differences.

Keep provider-specific cases only where providers genuinely differ. Put shared behavior in a reusable contract suite.

## Validate requested changes

Before editing, identify the capability protected before and after the change. Preserve evidence of replacement coverage when deleting or merging tests.

Verify proportionally:

1. Run the smallest affected test target.
2. Run the owning package's broader target only when boundary changes justify it.
3. Use existing coverage or mutation tooling when it answers a disputed finding.
4. Introduce a targeted mutation only when authorized and safe; verify the test fails, restore the source exactly, then verify the test passes.

Do not claim stronger protection merely because tests pass. Explain which realistic regressions the assertions can detect.

## Report results

Lead with actionable findings ordered by capability risk. For each finding, include:

```text
Priority:
Location:
Protected capability:
Evidence:
Problem:
Primary action:
Replacement or retained coverage:
Expected benefit:
Confidence:
```

Then provide:

1. A summary of high-, medium-, and low-value coverage. Use counts only when the inventory is complete.
2. A migration plan ordered so replacement coverage lands before deletion.
3. Missing high-risk coverage backed by documented behavior.
4. Verification performed and remaining evidence gaps.

If there are no actionable findings, say so directly and list residual coverage or verification gaps. Separate observed facts from recommendations and label uncertain inferences.
