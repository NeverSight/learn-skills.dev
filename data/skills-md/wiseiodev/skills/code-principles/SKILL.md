---
name: code-principles
description: Software engineering principles for code review, planning validation, and learning. Covers SOLID, DRY, YAGNI, design heuristics, testing, API design, architecture patterns, and React best practices. Use when reviewing code, validating plans/specs, injecting review criteria into council sessions, or when user asks about a specific principle. Triggers on "principles", "code review checklist", "SOLID", "DRY", "design heuristics", "review criteria", "best practices", or any named principle like "Law of Demeter", "Liskov", "YAGNI", etc.
---

# Code Principles

## Principle Index

| Principle | Group | One-liner |
|-----------|-------|-----------|
| SRP | [solid](references/solid.md) | One reason to change |
| OCP | [solid](references/solid.md) | Open for extension, closed for modification |
| LSP | [solid](references/solid.md) | Subtypes must be substitutable |
| ISP | [solid](references/solid.md) | Small interfaces > fat interfaces |
| DIP | [solid](references/solid.md) | Depend on abstractions |
| DRY | [simplicity](references/simplicity.md) | Don't repeat yourself |
| YAGNI | [simplicity](references/simplicity.md) | You aren't gonna need it |
| AHA | [simplicity](references/simplicity.md) | Avoid hasty abstractions |
| Rule of Three | [simplicity](references/simplicity.md) | Abstract after 3 occurrences |
| CQS | [design](references/design.md) | Commands mutate, queries return |
| Law of Demeter | [design](references/design.md) | Don't talk to strangers |
| Tell Don't Ask | [design](references/design.md) | Push logic to the object |
| POLA | [design](references/design.md) | Code should behave as expected |
| Composition > Inheritance | [design](references/design.md) | Compose behavior from small pieces |
| IoC | [design](references/design.md) | Framework calls you |
| Fail Fast | [resilience](references/resilience.md) | Validate early, throw early |
| Robustness Principle | [resilience](references/resilience.md) | Liberal in, strict out |
| Least Privilege | [resilience](references/resilience.md) | Minimum access needed |
| Hyrum's Law | [meta](references/meta.md) | All observable behavior becomes API |
| Connascence | [meta](references/meta.md) | Measure and minimize coupling |
| Locality of Behavior | [meta](references/meta.md) | Understand code in one place |
| Pit of Success | [meta](references/meta.md) | Easiest path = correct path |
| TDD | [testing](references/testing.md) | Red-green-refactor |
| AAA | [testing](references/testing.md) | Arrange-Act-Assert |
| Test Isolation | [testing](references/testing.md) | Tests don't affect each other |
| Test Behavior | [testing](references/testing.md) | Test what, not how |
| Testing Pyramid | [testing](references/testing.md) | Many unit, fewer integration, few e2e |
| Idempotency | [api-design](references/api-design.md) | Same request = same result |
| Backwards Compat | [api-design](references/api-design.md) | Don't break existing consumers |
| Semver | [api-design](references/api-design.md) | Communicate change impact |
| Defensive Coding | [api-design](references/api-design.md) | Validate at boundaries |
| SoC | [architecture](references/architecture.md) | Each layer handles one concern |
| CQRS | [architecture](references/architecture.md) | Separate read and write models |
| Hexagonal Architecture | [architecture](references/architecture.md) | Ports and adapters |
| Bounded Contexts | [architecture](references/architecture.md) | Explicit domain boundaries |
| Feature Directories | [react](references/react.md) | Organize by feature, not type |
| Component SRP | [react](references/react.md) | One job per component |
| Colocation | [react](references/react.md) | Keep related files together |
| Unidirectional Flow | [react](references/react.md) | Data down, events up |
| State Placement | [react](references/react.md) | State at lowest common ancestor |
| Barrel Exports | [react](references/react.md) | Public API via index.ts |

## Usage Modes

### 1. Checklist mode (default)

Scan code or a plan against relevant principles. Read the reference files for the groups most relevant to the task, then output a checklist:

```
- [ ] SRP: Does each module have one reason to change?
- [ ] DRY: Is logic duplicated unnecessarily?
- [x] YAGNI: No speculative features found
...
```

Select groups based on context:
- **Code review** → solid, simplicity, design, testing
- **Architecture/design review** → architecture, design, resilience, meta
- **API review** → api-design, design, resilience
- **React review** → react, solid, simplicity

### 2. Council mode

Generate a review criteria block for injection into review-council prompts. Read the reference files for the persona's relevant groups (see review-council personas), extract the "Review question" from each principle, and format as:

```markdown
## Code Principles Review Criteria
- SRP: Does each class/module have exactly one reason to change?
- OCP: Can behavior be extended without modifying existing code?
...
```

### 3. Deep-dive mode

When user asks about a specific principle ("what is the Law of Demeter?", "explain CQS"), read the relevant reference file and present the full entry: rule, violation example, correct example, when to break it.
