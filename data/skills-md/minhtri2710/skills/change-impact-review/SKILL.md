---
name: change-impact-review
description: Trace what a concrete code change could break beyond direct callers, then test one or two safety-critical assumptions against the real code path. Use when the user asks for change impact, blast radius, or a bounded cross-boundary safety review; do not use for whole-repository audits or API/module design.
disable-model-invocation: true
---

# Change Impact Review

Review one concrete change, not the repository in general. The goal is to find the downstream consumer or boundary a symbol search misses and challenge the small number of facts the safety conclusion depends on.

## Review

1. **Bound the change.** Read the diff and the owning implementation. State what behavior, input, ordering, or representation changed. Follow direct callers only far enough to identify downstream consumers; do not turn the review into a whole-repository audit.
2. **Choose one or two facts.** Name the safety-critical assumptions whose failure would change the outcome. Trace each through the relevant source: pinned dependency/version and local patches; scheduling or lifecycle ordering; API or wire representation; persisted storage and readers; and multi-hop or other-language consumers. Follow only applicable paths, cite source locations, and distinguish a consumer you found from one you did not find.
3. **Write the falsifier before the check.** For each fact, describe the concrete input, state, ordering, or boundary that would make the claim false. A generic concern such as “bad input” is not a falsifier.
4. **Execute the real seam.** Run the smallest check that calls the production function/library at its installed version or drives the actual application route. Capture the exact command and result. Disposable state is acceptable when contained and isolated, but it proves only the code actually executed. A fixture, mock, static scan, or helper-only call is not proof of application integration. If the application route cannot be run, mark that claim unproven rather than substituting a synthetic equivalent.
5. **Report the boundary.** Separate confirmed risks, checked-and-cleared cases, and unproven remainder. For each proof, say which function/version or route ran, what the check observed, and what it cannot establish. Include the cheapest relevant pre-merge check.

Keep scheduling, wire, storage, and dependency tracing proportional to the change: explain why an area applies, or why it does not. A search with no result is not proof that no consumer exists. Do not add a generic runner or invoke an automatic multi-model panel.

## Keep neighboring owners distinct

- `test-proof-debt-audit` evaluates a named claim's existing proof, including what a test observes and whether it should remain. This skill starts from a concrete change and follows its impact to consumers; it does not audit a test suite for proof debt.
- `source-grounded-implementation` owns official documentation and exact installed-version guidance for framework/library APIs. Use it for API-specific implementation choices; this skill checks version/source only when that dependency matters to the change's impact.
- `api-contract-design` designs HTTP/RPC request, response, validation, error, pagination, and retry contracts. `deep-module-design` designs in-process interfaces and seams. This skill traces a change across those contracts without taking over their design.
- Use `bug-diagnosis` when the reported behavior is a hard-to-explain failure; use `test-first-seams` when the user asks for test-first implementation. This review does not replace either workflow.

## Report

State the change and scope; each selected fact and source path; its falsifier; the command actually executed and observed result; confirmed risks, cleared cases, and unproven limits; and the cheapest relevant pre-merge check. Never call a helper-only or synthetic-fixture result production integration proof.
