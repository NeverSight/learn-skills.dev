---
name: superior-logic
description: Implement or review application behavior, APIs, state transitions, data flow, and business rules with explicit contracts and failure handling. Use for logic-bearing changes across frontend or backend systems. Do not use for visual-only or copy-only work.
---

# Superior Logic

Keep correctness visible from input to observable outcome. Fit the solution to the repository's existing architecture and update every affected side of a contract together.

Use `superior-code-review` instead when the primary outcome is findings on a diff, commit, branch, pull request, or working tree. Use this skill for a focused domain-logic review or for implementing confirmed behavioral changes.

## Model the behavior

Before choosing code, identify:

- trusted and untrusted inputs;
- outputs and observable side effects;
- invariants and authorization rules;
- consumers and compatibility constraints;
- expected failure, retry, duplication, ordering, and concurrency conditions.

State a material assumption only when code and documentation cannot establish it. Ask the user when competing answers would change the product contract.

Read [references/contract-evolution-and-workflows.md](references/contract-evolution-and-workflows.md) when changing a shared API, event, file format, client/server contract, state machine, or multi-step workflow that can span versions, retries, or partial deployment.

Load `superior-architecture` when designing or assessing project structure, module ownership, dependency boundaries, or structural refactoring is a primary concern. Keep routine feature placement and domain contracts in this skill.

## Place responsibility

- Inspect the framework's discovery conventions and the repository's existing feature and module owners before choosing a location. For a new project or feature without an established owner, group code by real responsibility and create folders only when they improve navigation or enforce a useful boundary.
- Keep domain decisions separate from rendering, transport, and persistence when the existing architecture supports that boundary.
- Validate at the point data crosses into a trusted system. Client validation improves experience but does not enforce server correctness.
- Maintain one authoritative owner for a state transition; derive dependent state instead of synchronizing copies.
- Use shared schemas and types when they are the repository's source of truth.
- Change producers, consumers, validation, tests, and documentation together when a shared contract changes.

## Protect state and side effects

- Make related writes atomic when partial completion violates an invariant; otherwise define a recoverable partial state or compensation.
- Make repeatable operations idempotent where retries or duplicate delivery could double-create, double-charge, or corrupt data.
- Define ordering and concurrency behavior where work can race. Arbitrary delay is not synchronization.
- Use timeouts, cancellation, and bounded retries for remote work according to established project patterns; retry transient conditions only.
- Preserve user input and useful recovery options after expected failures when safe.

Load `superior-database` when schema design, query shape, indexes, transaction isolation, migrations, backfills, or datastore rollout safety becomes a primary part of the request. Keep routine persistence orchestration here when the underlying data contract is unchanged.

Load `superior-performance` when latency, throughput, resource use, capacity, or scalability is a primary concern requiring measurement and profiling. Ordinary boundedness and avoiding obviously unnecessary work remain part of this skill.

Load `superior-reliability` when service objectives, failure isolation, graceful degradation, failover, or operational recovery is primary. Load `superior-delivery` when the task owns pipeline, artifact, environment promotion, rollout, or rollback behavior.

## Enforce security at trusted boundaries

- Authentication identifies a caller; authorization still governs each resource and action.
- Scope reads and writes to the authorized subject where possible.
- Treat route parameters, headers, hidden fields, filenames, client state, webhooks, and external payloads as untrusted.
- Use maintained libraries for credentials and cryptography. Never design custom token, encryption, signature, or secret-storage schemes.
- Keep secrets, sensitive personal data, and payment details out of logs and user-visible errors.

Load `superior-api-security` when API hardening, rate limiting, token security, abuse prevention, SSRF, or a dedicated security review is part of the request. Keep `superior-logic` responsible for domain contracts and invariants; use the security skill for threat-driven controls and negative verification.

## Diagnose uncertain failures

Load `superior-debugging` when a concrete failure exists but its cause is uncertain, environment-specific, intermittent, or requires causal tracing. Once the cause is established, use this skill for any in-scope repair to domain rules, state, persistence, or API behavior. A straightforward implementation defect with an already-proven cause does not require the dedicated debugging workflow.

## Keep failure observable

- Handle an error at the layer that can recover, translate, or add useful context.
- Preserve the original cause when wrapping errors.
- Never convert an unknown failure into success or swallow it solely to keep a flow moving.
- Give users safe, actionable messages and send diagnostic detail through the project's established observability path.
- Bound data-dependent loops, queues, result sets, recursion, retries, and in-memory accumulation.

## Verify the contract

Test observable behavior rather than private steps. Cover the normal path and the material boundary, invalid-input, authorization, partial-failure, duplication, retry, or concurrency cases affected by the change. Reproduce a bug with a focused failing test when practical.

Load `superior-testing` when test design, level selection, fixtures, doubles, flaky behavior, or suite reliability is a primary part of the request. Ordinary implementation verification remains part of this skill and does not require loading the dedicated testing workflow.

Load `superior-ux` when domain behavior must be shaped around a multi-step user journey, information architecture, feedback, or recovery experience. Keep enforceable state transitions, invariants, APIs, and persistence in this skill.

Use existing test conventions and run the narrowest relevant lint, type, test, and build checks. Report unverified conditions and compatibility risk explicitly.

Report the final contract, affected producers and consumers, failure behavior, compatibility or rollout assumptions, and checks actually performed. Do not describe a workflow as atomic or exactly-once unless the implementation and underlying systems prove that guarantee.
