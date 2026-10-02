---
name: deslop
description: Audit or apply evidence-backed, test-first subtractive cleanup for accumulated agent-created test bloat, verification theater, and defensive or fallback bloat while preserving independent external behavior. Invoke explicitly for semantic simplification, not generic refactoring.
---

# Deslop

Deslop removes complexity accumulated during repeated coding-agent implementation and correction cycles. It is a semantic cleanup policy, not a beautifier, dead-code sweeper, generic refactoring tool, or redesign assistant.

## Priority order

Work in this order. Do not let an easy dead-code deletion displace a higher-priority cluster.

1. **Test-suite bloat.** Treat tests as production code that can accumulate after every agent correction. Remove duplicate, self-referential, implementation-detail, and obsolete tests while retaining a minimum sufficient set of independent behavioral evidence.
2. **Verification theater.** Investigate checksums, receipts, manifests, validators, recomputation, and result envelopes whose producer and verifier share the same information and failure domain.
3. **Defensive and fallback bloat.** Investigate broad catches, catch-and-fallback paths, speculative compatibility branches, repeated validation, and recovery machinery that masks errors without a current contract.

Generic dead code, wrappers, abstractions, comments, and ordinary duplication are secondary. Touch them only when they belong to one of the three target clusters or have direct high-confidence evidence.

**Reduce test surface, not behavior surface.** Evidence that a test is redundant or accumulated test-suite bloat justifies deleting or consolidating that test; it is not independent evidence for changing the production behavior the test exercises. When test-suite bloat is the active target, keep distinct externally observable production semantics—including public success, rejection, error, edge-case, and supported compatibility behavior—outside the deletion target unless the production construct is separately justified for removal by another target cluster, or direct evidence from current requirements, real callers, specifications, or history establishes that the behavior is obsolete or incorrect. Do not reclassify tested behavior as defensive or validation bloat merely because deleting its test leaves nothing else requiring it; the test may be its clearest executable specification.

Adding tests is not the default response to cleanup. When production slop is deleted, tests whose only purpose is to protect that slop should normally be deleted in the same change.

## Test-first evidence pass

When tests are in scope, complete this pass before changing production behavior:

1. Inventory collected test nodes plus their fixtures, fakes, helper stacks, generated inputs, output targets, skips, and deselection rules.
2. Map each test to `current owner -> production branch -> observable result -> independent oracle -> failure domain`.
3. Group tests by failure domain. Consolidate inputs that reach the same branch and result; preserve separate rejection, safety, persistence, protocol, resource, and numerical semantics.
4. Choose the strongest surviving evidence root for each group: a public seam where possible, an independently specified low-level invariant where necessary, and one hermetic cross-layer root for each current delivery path.
5. Remove fixtures and test-only support with the tests they serve. Remove production code in that cluster only when separate caller, contract, history, and reachability evidence also justify it.
6. Re-collect and run the remaining suite. Record skips and deselections, and compare worktree state before and after tests that may generate files.

Do not use coverage, test count, or a test-created configuration as an owner. The output of this pass is a smaller evidence set with the same real failure domains, not a target number of tests.

### Test decision contrast

- **HIGH cleanup:** several tests reach the same public success branch; one asserts the exact externally visible result while the others only repeat construction, type, or non-empty checks. Keep the strongest behavioral root and remove the dominated tests plus support used only by them.
- **PRESERVE:** one test covers successful output and another covers externally visible rejection, safety, persistence, or supported compatibility behavior. They protect different results or failure domains; do not merge or delete one merely to reduce the count.

## Closed justification loops

Production code does not justify a test merely because the test exercises it. A test does not justify production code merely because the production code exists. Follow justification chains outward until they reach an independent evidence root.

A production/test pair is mutual-support slop only when the production construct has no independently meaningful externally observable purpose. A test of a distinct externally observable rejection, error, or supported compatibility behavior is not a closed justification loop merely because the test is its clearest executable specification. Internal checksum or receipt machinery and tests created only for that machinery can form such a loop, as can a speculative fallback and tests created only to exercise it.

If a fallback exists only because a test exercises it, and that test exists only because the fallback was added, neither member is independent evidence. The same closed justification loop can include checksum logic and checksum tests, receipts/manifests and validators, wrappers and wrapper-only tests, obsolete compatibility branches and their tests, or defensive validators and tests that only exercise them. Call this **mutual-support slop**.

Accept a dependency cluster only when its chain reaches a current user requirement, real external caller, public API contract, documented protocol or specification, security/trust boundary, persistence or corruption boundary, or scientific/numerical invariant. If the cluster only justifies itself, prefer deleting the whole cluster rather than preserving each member because another member depends on it.

A closed loop is a finding about evidence that is present, not evidence that is absent. Failing to find a caller, configuration, document, or history inside a small or isolated scope is missing evidence: it caps the finding at MEDIUM and does not make the cluster unreachable or HIGH. A compatibility branch with its own first-class positive test or current documentation explicitly naming it as supported behavior is a preservation root; removing that behavior requires positive evidence that the compatibility promise has ended. A branch reached only through a broad catch, with no test or document of its own, is not such a root.

Trace edges as well as nodes. Separately tested producers, readers, and consumers do not prove that a current production path connects them. Before removing a fixture, validator, registry entry, or wrapper that crosses layers, identify the current producer -> reader -> consumer path and preserve one hermetic integration root when that path carries real behavior.

## Modes and authorization

Interpret invocation from natural language; do not depend on a runtime-specific arguments variable.

- **Default or `audit`:** read-only. Report candidates, evidence, confidence, closed loops, and constructs to preserve. Do not intentionally modify repository-owned content; disable or redirect tool caches and generated outputs when practical.
- **`apply`:** modify files only within the established scope.
- **`tests`:** prioritize test signal and mutual-support slop. Without `apply`, remain read-only.
- **`deep`:** inspect repository-wide. Without `apply`, remain read-only; with `apply`, cleanup is allowed but redesign is not.
- **Explicit paths:** inspect and edit those paths plus the minimum callers, contracts, and tests needed to establish independence.
- **Current branch or no scope inside Git:** use the actual merge base and include staged, unstaged, and untracked work; never assume `main`.

Only `apply` authorizes edits. Do not fetch, reset, switch branches, stage, commit, push, or create backups unless explicitly requested.

## Establish evidence before editing

1. Read the active host's applicable project-instruction files, such as `AGENTS.md` or `CLAUDE.md`, plus repository conventions and the requested scope.
2. Inspect callers, tests, history, specifications, current configuration, registries, public readers, and documented verification commands.
3. Classify the evidence chain before trusting an existing test or fallback.
4. Put explicit current requirements first. A requirement or correction stated in the current task, or recorded in a current authoritative project document, overrides conflicting historical tests. Do not promote an inferred preference or the cleanup objective itself into a requirement.
5. A bug fix should normally replace incorrect behavior, not preserve it behind a fallback.

Prove reachability from a non-test producer such as an active config, external request, public CLI, persisted record, or hardware/runtime selection. A test-injected flag, synthetic future config, diagnostic command, or scripted dry-run does not by itself own a production branch.

Inside trusted code, use a **fail-visible bias**: allow unexpected failures to surface unless there is a concrete recovery, translation, cleanup, protocol, or compatibility contract. Broad `except Exception`, catch-and-fallback, catch-log-rethrow, speculative legacy fallbacks, and compatibility branches without independent evidence are high-priority investigation targets. Do not hide bugs in the name of robustness.

## Confidence and apply behavior

These rules govern every candidate in this file and the references. A listed smell or preferred action does not resolve missing evidence or authorize deletion by itself.

- **HIGH:** redundant, tautological, unreachable, self-justifying, or disconnected from a real contract after the evidence chain is resolved.
- **MEDIUM:** apparently unnecessary, but caller, history, compatibility, or boundary evidence is still missing.
- **LOW / PRESERVE BY DEFAULT:** security, authorization, concurrency, persistence, transactions, external protocols, supported compatibility, resource limits, and scientific invariants whose purpose may be outside the local file.

In apply mode:

- HIGH: delete or simplify once the evidence is resolved.
- MEDIUM: do not modify until the missing evidence question is resolved.
- LOW: preserve unless direct contrary evidence is established.

Apply authorization is permission to edit, not permission to resolve uncertainty in favor of deletion.

Read only the relevant references:

- [test-smells.md](references/test-smells.md) for accumulated test suites and test/production mutual-support clusters.
- [verification-and-trust.md](references/verification-and-trust.md) for checksum, receipt, manifest, provenance, and trust-boundary clusters.
- [code-smells.md](references/code-smells.md) for defensive, fallback, compatibility, wrapper, and abstraction candidates.
- [scientific-code.md](references/scientific-code.md) for numerical, simulation, ML, or engineering invariants.
- [evidence-and-reachability.md](references/evidence-and-reachability.md) when cleanup touches cross-layer fixtures, generated artifacts, active configuration, schema readers, registries/CLIs, or test hermeticity.

## Subtractive workflow

1. Complete the test-first evidence pass before production cleanup when tests are in scope.
2. Before classifying checksum, receipt, manifest, or persisted-validation code for deletion, read [verification-and-trust.md](references/verification-and-trust.md). Trace the whole cluster and remove its support machinery only when no independent root remains.
3. Trace fallback branches to actual supported consumers and failure contracts. Prefer direct failure when the current contract says an operation should fail.
4. Delete tests that exist only to keep deleted production slop green. Add a replacement test only when deleting the old test would leave a real external behavior unprotected and an independent oracle exists.
5. Preserve real public, persistence, security, protocol, compatibility, resource, and scientific boundaries even when their code resembles a smell.
6. Treat declared authoritative inputs as required unless the protocol explicitly marks them optional. Missing and invalid authoritative artifacts should share the same visible failure semantics.
7. For a schema or identity change, enumerate every public reader, including CLIs, tools, visualizers, converters, and resume paths. Follow contract-defined version selection, including supported defaults; do not invent compatibility from a missing field or file.
8. Keep permanent tests hermetic: use repository-managed or test-created inputs, write to temporary outputs, and skip only when the test actually crosses the optional dependency boundary.

## Negative-change budget

Normally reduce structural surface area. New dependencies, abstractions, wrappers, compatibility layers, cryptographic/provenance machinery, and tests have a default budget of zero. New code is acceptable only when it preserves a real behavior while removing more accumulated slop. A small current-path integration root or a direct required-input check can be justified when cleanup exposes a real protection gap. When a repair closes a real fail-open contract, adapt existing coverage to check the required rejection. Keep success and failure assertions readable; add a small test only when the surviving behavior would otherwise lack independent coverage. If a cleanup adds substantial production or test lines, stop and reconsider.

In `deep apply`, exclude generated code, vendored dependencies, `third_party` trees, migration history, lockfiles, and externally generated snapshots or artifacts unless explicitly included or demonstrably repository-owned.

## Proportional verification

Run the narrowest existing checks after each meaningful semantic group and the repository's documented final checks once when feasible. Compare test collection before and after, and explain unexpected skips or deselections. An unexplained drop to zero tests, or loss of required verification for surviving behavior, is a failure. A confirmed-retired target may be removed with all its dedicated tests; a scope that already had no tests should use its applicable existing checks. Explain either case and do not retain or add tests merely to obtain a nonzero count. If deleting a cluster would remove the last test exercising a surviving public contract, adapt an existing test to an independently specified observable result. When no independent oracle is available, report that gap instead of deriving expected values from the implementation.

When tests can generate files, compare the worktree before and after the suite so a green run cannot hide writes to tracked outputs. In read-only modes, use no-write options or temporary locations for caches and generated output when available, and report any incidental tool artifacts left behind. Verification should be independent of the change where possible. Do not create proof files, audit ledgers, checksum reports, or a new verification framework merely to validate a deletion. If a check cannot run without changing repository-owned content, do not run it in audit mode; state that plainly.

## Final report

Report the inspected scope; removed test, verification, and fallback clusters; independent evidence roots; preserved boundaries; tests removed or consolidated; before/after collection plus skips or deselections when available; checks actually run; approximate production/test size changes when useful; and uncertainty intentionally left untouched. Explicitly call out any closed justification loop that drove deletion.
