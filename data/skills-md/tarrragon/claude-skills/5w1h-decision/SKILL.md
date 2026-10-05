---
name: 5w1h-decision
description: "5W1H Decision Framework Tool. Use for: (1) Systematic decision-making before creating todos, (2) Preventing duplicate implementation, (3) Detecting avoidance behavior, (4) Ensuring agile refactor compliance with executor/dispatcher separation"
metadata:
  version: 1.3.2
  portable: true

---

# 5W1H Decision Framework - Systematic Decision Making

## Core Principles

| Principle           | Description                           | Validation               |
| ------------------- | ------------------------------------- | ------------------------ |
| Systematic Thinking | Every decision requires 5W1H analysis | All 6 questions answered |
| No Duplication      | Check existing implementation first   | Who analysis complete    |
| No Avoidance        | Reject escape language                | Why validation passed    |
| Agile Compliance    | Executor/Dispatcher separation        | How task type matched    |
| TDD Integration     | Test-first strategy required          | How includes TDD steps   |

---

## 5W1H Framework Quick Reference

### Who (Responsibility Attribution)

```markdown
Who: {Executor Agent} (executor) | rosemary-project-manager (dispatcher)
- Domain: {Responsible class/module}
- Existing: {Search result for duplicates}
```

**Valid Patterns**: `parsley-flutter-developer (executor) | rosemary-project-manager (dispatcher)`

---

### What (Function Definition)

```markdown
What: {Function Name}
- Description: {One sentence description}
- Input: {Explicit input types}
- Output: {Explicit output types}
- Exception: {Error handling}
```

---

### When (Trigger Timing)

```markdown
When: {Event Name}
- Trigger: {User action / System event}
- Side Effects: {List all side effects}
- Integration: {Event system integration point}
```

---

### Where (Execution Location)

```markdown
Where: {Layer} / {Component}
- Architecture: {Domain/Application/Infrastructure/Presentation}
- Component: {Specific class or module}
- UseCase: {UseCase call chain}
```

---

### Why (Motivation Validation)

```markdown
Why: {Requirement Reference}
- Requirement ID: {UC-XXX}
- Business Value: {User benefit}
- User Scenario: {Specific use case}
```

**Avoidance Language Detection** (BLOCKED):

- Quality compromise: "too complex", "workaround", "temporary fix", "quick fix"
- Simplification: "simpler approach", "easier way", "simplify"
- Problem ignoring: "ignore for now", "skip for now", "deal with later"
- Test compromise: "simplify test", "lower test standard", "basic test only"
- Code escape: "comment out", "disable", "temporarily disable"

---

### How (Implementation Strategy)

```markdown
How: [Task Type: {TYPE}] {Strategy Description}
```

**Task Type vs Executor Mapping**:

| Task Type      | Valid Executor        | Invalid Executor    |
| -------------- | --------------------- | ------------------- |
| Implementation | parsley, sage, pepper | rosemary (BLOCKED)  |
| Dispatch       | rosemary              | Any agent (BLOCKED) |
| Review         | rosemary              | Any agent (BLOCKED) |
| Documentation  | thyme, rosemary       | -                   |
| Analysis       | lavender, rosemary    | -                   |
| Planning       | rosemary, lavender    | -                   |

---

## Checklist Before Todo Creation

### Completeness Check

- [ ] **Who**: Executor/Dispatcher clearly identified, no duplicate implementation
- [ ] **What**: Single responsibility, clear I/O definition
- [ ] **When**: Trigger timing explicit, side effects identified
- [ ] **Where**: Correct architecture layer, UseCase path clear
- [ ] **Why**: Requirement reference, no avoidance language
- [ ] **How**: Task Type present, TDD strategy, matches executor

### Agile Refactor Compliance Check

- [ ] Who has `(executor) | (dispatcher)` format
- [ ] How has `[Task Type: XXX]` prefix
- [ ] Implementation tasks assigned to agents (not main thread)
- [ ] Dispatch/Review tasks assigned to main thread

### Quality Gate

**ALL items must be checked before creating todo.**

Missing any item = BLOCKED

---

## Key References

| Reference                                                                         | Purpose                                   |
| --------------------------------------------------------------------------------- | ----------------------------------------- |
| [Complete Template](./references/5w1h-template.md)                                | Full template format and token generation |
| [Common Violations](./references/common-violations.md)                            | Violation patterns and fixes              |
| [Integration Details](./references/integration-details.md)                        | Hook/Output Style/Token validation engine |
| `5w1h-self-awareness-methodology`（各專案自有）      | Complete methodology                      |
| `agile-refactor-methodology`（各專案自有） | Executor/Dispatcher separation rules      |

---

## Quick Reference Card

### Required Format

```text
5W1H-{TOKEN}

Who: {agent} (executor) | rosemary-project-manager (dispatcher)
What: {Single responsibility function}
When: {Event trigger with side effects}
Where: {Architecture layer / Component}
Why: {Requirement ID + Business value}
How: [Task Type: {TYPE}] {TDD strategy steps}
```

### System-Level Enforcement

5W1H format is automatically enforced via:

- **Output Style** (system prompt injection) - Always active
- **PreToolUse Hook** - Validates todo creation
- **UserPromptSubmit Hook** - Generates session token

---

## Collaboration: when `neurodivergent-output` is also active

5W1H runs fully standalone. When the `neurodivergent-output` skill is also active, its cross-message state ledger becomes the persistent surface for decisions, and 5W1H adapts to the reader's cognitive-load rules. The composition triggers through that ledger (which fires every turn), so the compressed-5W1H rows ride on it rather than being a separate step to remember. Details:

- **Surface decisions in the ledger, compressed.** When a 5W1H decision is made, put a compressed form — What, Why, next step — into the ledger's decisions section so it persists across messages. Do not dump the full six-field record, the session token, or the executor/dispatcher and Task-Type scaffolding into the ledger; keep the full record in its normal place and surface a pointer.
- **Respect the reader's load rules on the ledger.** The ledger obeys neurodivergent-output's base layer (reduce overload, cap lists at five). Compress the 5W1H entry to fit; the ledger is a low-load anchor, not a full decision record.
- **Scope avoidance-language detection to decision content.** Blocking "simplify / simpler / easier" applies to the work being decided, not to how the reply is shaped. Do not flag reader-facing output being compressed for an ADHD reader as avoidance.
- **Soften the gate under PDA.** 5W1H's "all items must pass or BLOCKED" is a hard gate. When neurodivergent-output's PDA mode is on, present running 5W1H before a commit as an invitation with control left to the reader, not a block.

- **Verify it manifested — do not just declare it.** When both skills are active, check each reply: are the ledger's decision rows really in compressed 5W1H form, or did only the ledger (the visible half) appear? The effortful half (5W1H structuring) silently drops if you rely on "both skills active" instead of checking the output. Declaration is not execution.

Neither skill depends on the other; this section only changes behavior when both are on.

---

**Last Updated**: 2026-07-21

版本紀錄在同目錄的 `CHANGELOG.md`。
