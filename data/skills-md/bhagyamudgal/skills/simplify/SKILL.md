---
name: simplify
description: Reduce unnecessary complexity in a completed code or workflow diff without changing intended behavior. Use after implementation and review, or when a fix grew beyond the request.
---

# Simplify

I make the smallest behavior-preserving cleanup that leaves the finished change easier to maintain. Less code, same behavior. That is the whole job.

## 1. Bind the change

I record the originating request, review baseline, changed paths, and current diff or content hash. I read the complete diff and the surrounding code for every cleanup I propose.

The cleanup scope is the current task diff. Unrelated pre-existing code stays untouched, and I say so as the gate. I do not wander.

## 2. Find removable complexity

I inspect only for these.

- Duplication the change introduced.
- Abstractions, branches, configuration, or error handling the request does not need.
- Dead imports, variables, functions, files, or indirection the change introduced.
- Control flow or naming that can turn clearer without changing the public contract.
- Added comments that fail the added-comment scan below.

I prefer deletion and direct code over a new helper. I reuse an existing local pattern when it removes a fork. I preserve required guards, evidence, recovery behavior, tests, and user-confirmed decisions.

### Added-comment scan

I inspect every comment the change adds under the global comment rule. A comment stays only when it is a one-line `/** */` contract on an exported symbol, or a one-line citation carrying a URL, a spec section, an ADR or `docs/` path, or an issue number. I delete everything else on sight, including any comment that explains what the code does, why it has its shape, or what would break. I run the rule's grep over the diff and delete every comment it prints. A project rule may tighten this scan, never loosen it.

Every proposed edit names what turns simpler and why observable behavior stays equivalent, and no uncited comment the change adds remains. This scan blocks. The caller cannot report the work complete while one remains in the diff.

## 3. Apply and verify

I apply only cleanups whose equivalence the code and existing tests support. When a cleanup changes behavior, requirements, public output, persistence, authorization, or failure semantics, I return it as a separate proposal instead of applying it.

I re-run the checks my cleanup invalidated and compare the final diff with the originating request. When the cleanup changes content a completed review covered, I invalidate and rerun only that coverage through `converge-reviews`. A stale convergence result cannot verify the simplified diff. I report the edits I made, or `No simplification needed`, plus the exact verification results.

I call the diff done when it runs no broader than the request, every retained line has a task reason, and applicable checks still pass.
