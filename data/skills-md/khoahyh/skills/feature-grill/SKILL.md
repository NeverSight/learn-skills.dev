---
name: feature-grill
description: Shape a bounded feature's unresolved product and behavioral decisions into a user-confirmed Feature Contract.
---

# Feature Grill

Agree on a feature's observable behavior before technical design. This skill is design-only: keep the repository read-only and return the contract inline unless the user or calling workflow authorizes writing the design artifact.

Load `grilling` for the conversation. Resolve inspectable facts yourself; reserve questions for consequential product or behavioral choices, and recommend a concrete answer with each question. Inspect only the code, tests, docs, and runtime facts needed to settle the active decision or challenge an assumption.

## Frame The Feature

Bound the feature by its actor or caller, trigger, observable outcome, current gap, goals, explicit non-goals, and success evidence. If the request is broader than one capability, narrow only the decisions needed to name a coherent feature rather than implying the whole direction is resolved.

Use [FEATURE-CONTRACT.md](FEATURE-CONTRACT.md) as a risk map, not a questionnaire. Follow only branches reachable from the agreed behavior and known dependencies, and let settled answers reshape what remains. Surface contradictions between the requested model and the current system; resolve them with the user or retain them as blockers.

Choose direct cutover when no current consumer, retained data, deployment constraint, or user requirement needs the old path. Preserve compatibility only for a named obligation, with a removal condition when temporary. Match proof to important risks and real boundaries; existing thorough evidence may be enough. Prefer the smallest vertical slice with an independently observable result or a named risk retired, excluding adjacent cleanup and speculative infrastructure.

Load `codebase-design` only when an interface or ownership seam is genuinely unsettled. Load `observability-logging` only when detailed signal design is needed. When authorized durable glossary or ADR changes are part of the requested artifact, let `domain-modeling` own them.

## Keep Unknowns Visible

When conversation cannot settle a decision, record the exact uncertainty, needed evidence, owner or method, and downstream decisions it blocks. A bounded `prototype` may answer state-model, business-rule, or UI uncertainty; protocol, migration, deployment, concurrency, or performance questions usually need a repository-native repro, experiment, benchmark, or research task. Recommend the follow-up without running it unless separately authorized.

## Confirm The Contract

Once every applicable branch is resolved or explicitly deferred, render a `Draft` from the template and ask the user to correct or confirm the shared understanding. Explain omissions only when they carry risk. After confirmation, date the contract and use exactly one terminal status:

- `Confirmed - Ready for Spec`: no unresolved decision changes observable behavior, trust, retained data, operability, proof, or the first delivery slice.
- `Confirmed - Blocked`: at least one such decision still needs evidence or a user choice.

The first slice must remain independently observable and verifiable. Return a blocked contract with its evidence needs; hand only `Confirmed - Ready for Spec` to `tech-spec` or the repository's specification flow. Confirmation authorizes neither specification, implementation, nor another durable mutation.
