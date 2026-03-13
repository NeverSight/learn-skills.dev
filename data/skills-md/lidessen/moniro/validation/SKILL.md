---
name: validation
description: Unified validation orchestration for code quality, consistency, and project health. Auto-triggers on code changes, PR creation, or explicit validation requests. Coordinates refining, housekeeping, and custom validators into cohesive pipelines. Use for "validate", "check", "verify", "验证", "检查", or when quality assurance is needed.
---

# Validation

Unified validation orchestration that coordinates quality checks into cohesive pipelines.

## Philosophy

### Why Validate?

Validation exists because **confidence without evidence is dangerous**.

The core question isn't "what checks should I run?" but "how do I know this actually works?"

```
The Fundamental Insight:
├── Humans forget, misremember, rationalize
├── Environments change between runs
├── "It worked before" proves nothing about now
└── Fresh evidence is the only reliable evidence
```

### Continuous Feedback, Not Gates

```
Traditional: Code → Gate → Pass/Fail (binary, blocking)
This:        Code → Insight → Learn → Improve → Code (circular, evolving)
```

Validation is a **learning loop**, not a checkpoint. Each validation teaches something about the codebase, the workflow, and the patterns that emerge.

### No Universal Workflow

There is no perfect validation pipeline. The ability to **adapt and create workflows** matters more than following a fixed process.

Ask:

- What's the smallest unit I can verify?
- What evidence would convince me this works?
- How do I know when to stop validating?

### Divide and Conquer

Large problems are unsolvable. Small problems are trivial.

```
Validation Strategy:
1. Decompose: What are the independent pieces?
2. Identify: What's the smallest verifiable unit?
3. Order: What depends on what?
4. Compose: Build confidence from small to large
```

### Memory as Evolution

Recording validation results isn't storage—it's the foundation for learning.

```
Without memory: Same mistakes, forever
With memory:    Patterns emerge → Predictions possible → Prevention achievable
```

See [reference/feedback-loop.md](reference/feedback-loop.md) for how learning works.

## Core Concepts

### Pipelines Are Tools, Not Rules

A pipeline is a **reusable composition** of validators. Think of it as a recipe you can modify, not a law you must follow.

```
Default pipelines exist as starting points:
├── quick      → Fast feedback (syntax, obvious issues)
├── standard   → Pre-commit confidence (+ security, consistency)
├── comprehensive → Pre-PR thoroughness (+ impact, architecture)

But the real skill is knowing when to:
├── Skip a validator (it's not relevant here)
├── Add a custom check (domain-specific concern)
├── Change the order (dependency requires it)
└── Create a new pipeline (novel workflow)
```

### Built-in Validators

These exist because they're commonly useful, not because they're mandatory:

| Validator         | What it answers             | When useful              |
| ----------------- | --------------------------- | ------------------------ |
| **reviewability** | "Is this easy to review?"   | Before asking for review |
| **impact**        | "What might break?"         | Changing shared code     |
| **consistency**   | "Does this match the rest?" | Touching documentation   |
| **security**      | "Is this safe?"             | Handling user input      |
| **architecture**  | "Does this fit the design?" | Structural changes       |

See [reference/validators.md](reference/validators.md) for details on each.

## When to Validate

Validation triggers on context, but **you decide the depth**:

| Signal              | Default Response | But consider...                      |
| ------------------- | ---------------- | ------------------------------------ |
| Code changed        | quick scan       | Is it a critical path? Go deeper.    |
| Before commit       | standard checks  | Trivial fix? Maybe quick is enough.  |
| Before PR           | comprehensive    | Already well-tested? Adapt.          |
| Explicit "validate" | standard         | What are you actually worried about? |

The defaults are sensible starting points. Override them when you understand why.

## The Validation Loop

```
1. Ask: What would prove this works?
      ↓
2. Do: Run the minimum checks that answer that question
      ↓
3. Learn: Record what you found (especially surprises)
      ↓
4. Adapt: Next time, you know more
```

Results persist to `.memory/validations/` for pattern detection.

See [reference/persistence.md](reference/persistence.md) for format.

## Collaboration

Validation coordinates, doesn't replace. It asks other skills for their perspective:

- **refining** → "Is this reviewable? What's the blast radius?"
- **housekeeping** → "Is this consistent with the rest?"
- **engineering** → "Does this fit the architecture?"
- **memory** → "What patterns have we seen before?"

## Configuration

Customize in `.validation.yml`. See [reference/pipelines.md](reference/pipelines.md).

```yaml
# Example: domain-specific validator
custom_validators:
  - name: business-rules
    command: ./scripts/check-invariants.sh
```

## Reference

Load these **as needed**, not upfront:

- [reference/validators.md](reference/validators.md) - Validator details
- [reference/pipelines.md](reference/pipelines.md) - Pipeline configuration
- [reference/custom-validators.md](reference/custom-validators.md) - Custom validators
- [reference/persistence.md](reference/persistence.md) - Result storage
- [reference/feedback-loop.md](reference/feedback-loop.md) - Learning mechanism
- [reference/verification-gate.md](reference/verification-gate.md) - Evidence protocols
- [reference/defense-in-depth.md](reference/defense-in-depth.md) - Layered validation
- [reference/metrics-tracking.md](reference/metrics-tracking.md) - Cost and performance

## Understanding, Not Rules

Instead of memorizing anti-patterns, understand the underlying tensions:

| Tension                    | Resolution                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------- |
| Speed vs Thoroughness      | Match depth to risk. Trivial change? Quick check. Critical path? Go deep.          |
| Confidence vs Evidence     | Confidence without evidence is wishful thinking. Always prefer fresh verification. |
| Flexibility vs Consistency | Adapt workflows to context, but record decisions so patterns can emerge.           |
| Automation vs Judgment     | Automate the tedious, but judgment for "is this right?" remains yours.             |

The goal isn't to follow a checklist. It's to **know when you know** something works.
