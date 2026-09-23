---
name: professional-engineering
description: "Apply pragmatic professional engineering judgment to software changes: make code clear, safe, testable, diagnosable, and reviewable without speculative architecture. Use for features, bug fixes, refactors, integrations, API/domain design, error handling, tests, and code-change plans."
---

# Professional Engineering

Make the next change safer. Optimize for reduced surprise: an engineer should be able to understand the behavior, identify failure paths, and safely modify or revert the change.

Use this skill alongside the repository's own instructions and conventions. Those conventions take precedence unless they create a concrete correctness, security, or operational risk. Do not turn this skill into a reason to redesign unrelated code.

## Work deliberately

Before changing code, inspect the requirement and the relevant implementation, tests, types, and integration points. Identify only the risks that apply:

- control flow and important failure paths;
- domain terms and ambiguous names;
- external inputs, representations, and contracts;
- meaningful lifecycle states and valid transitions;
- business decisions and side effects;
- error, logging, and tracing needs;
- change scope, tests, and rollback implications.

Choose the smallest change that satisfies the request while making material behavior explicit. Do not add an abstraction merely because it is a familiar pattern.

## Apply the relevant patterns

### 1. Keep the main flow visible

Handle invalid prerequisites, authorization failures, and other terminal paths early when that makes the success path flatter and easier to read. Keep nesting when it represents a real hierarchy, such as recursive structures, parsing, or an intrinsically nested workflow.

### 2. Name domain meaning

For concepts that carry business risk, use names that communicate what the value, state, or decision means in the domain. Generic names such as `data`, `result`, `item`, `payload`, `value`, and `isValid` are acceptable only when their scope makes the meaning genuinely obvious. Prefer a precise name over a short but vague one.

### 3. Contain external representations

Do not let API payloads, SDK objects, persistence rows, framework objects, environment values, or webhook formats become the domain model by accident. When an external shape is used beyond a small local area or its semantics differ from the internal model, normalize it at an adapter, mapper, or validation boundary. Keep domain logic expressed in internal language.

Read [references/boundaries-and-state.md](references/boundaries-and-state.md) when designing integrations, persistence mapping, validation boundaries, or state transitions.

### 4. Make important invalid states difficult to express

Use the language's appropriate tools—distinct types, finite values, constructors, validation, or explicit transition functions—to encode real prerequisites and lifecycles. Do not turn a simple record into an elaborate state machine unless invalid combinations are a realistic source of bugs.

### 5. Separate material decisions from effects

When a business rule is risky, branch-heavy, likely to change, or deserves a test matrix, make the decision inspectable and testable independently from database writes, network calls, notifications, queues, and other effects. Keep trivial logic local if extraction would obscure the flow.

Read [references/decisions-errors-testing.md](references/decisions-errors-testing.md) for decision design, useful errors, safe observability, and risk-based tests.

### 6. Make failures actionable

Follow existing error conventions. For contracts consumed by code, prefer stable machine-readable codes plus a human-readable message and safe, relevant details. Add diagnostic context for important operations when it supports production investigation, and never expose secrets, credentials, tokens, private keys, or unnecessary sensitive data.

### 7. Optimize for the diff

Keep unrelated cleanup, broad renames, and behavior changes separate where practical. Verify the actual diff, identify configuration or migration impact, and add tests that protect the behavior most expensive to break. A change is complete when it is understandable, reviewable, testable in proportion to risk, and reasonably reversible—not merely when its happy path runs.

## Restraint is required

Complexity must earn its place. Before adding a layer, interface, service, repository, factory, event bus, or pattern, be able to state the concrete complexity or coupling it reduces and why direct code is less safe or clear. Do not abstract for hypothetical future needs.

When a task is simple, the professional result is often a direct, well-named change with focused tests. When a task has material integration, state, or operational risk, add only the structure that contains that risk.

Read [references/change-review.md](references/change-review.md) before finalizing a substantial implementation, refactor, or plan.

## Completion review

Before reporting completion, check the applicable items:

- The requirement and important failure behavior are covered.
- The primary path is readable and business-critical names are meaningful.
- External shapes are contained where reuse or volatility warrants it.
- Important states and transitions are honest about their prerequisites.
- Risky decisions are not obscured by side effects.
- Errors and logs are useful and do not leak sensitive data.
- Tests target changed behavior and meaningful risk.
- The diff is focused; unrelated complexity has not been introduced.

Keep status updates and final handoff concise. Mention material trade-offs, boundaries, tests, or unresolved risks; do not give a lecture when the change is straightforward.
