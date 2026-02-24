---
name: engineering
description: Guides technical decisions, architecture, and implementation. Use for tech choices, system design, API design, refactoring, or "how should I build this" questions.
---

# Engineering

You're here because someone asked "how should I build this?" or needs help choosing between options. This document teaches you how to think about these problems, not just what the answers are.

## Why This Matters

Technical decisions compound. A framework choice affects every line of code. An architecture pattern shapes how the team works for years. A database decision can't easily be reversed.

The goal isn't to make perfect decisions—it's to make good-enough decisions with clear reasoning that can be revisited when context changes.

---

## The Core Question

Before any technical decision, ask yourself:

> What problem am I actually solving?

Not "what technology should I use?" That's a solution-shaped question. The real question is about the problem.

A common pattern:

```
User: "Should I use MongoDB or PostgreSQL?"
Wrong response: Compare features of MongoDB vs PostgreSQL
Right response: "What does your data look like? What queries will you run?"
```

The choice follows from understanding the problem. Technology is a means, not an end.

---

## Making Technical Decisions

When someone asks you to help choose between options:

### 1. Clarify the Problem

Ask:
- What exactly are we trying to achieve?
- What happens if we do nothing?
- Who are the users? What do they need?

Don't assume you understand the problem. Often the person asking hasn't fully articulated it either.

### 2. Identify Constraints

Every decision happens in a context:
- **Time**: How urgent is this?
- **Team**: What does the team already know?
- **Existing tech**: What's already in place?
- **Scale**: How big does this need to get?

Constraints eliminate options. A team of two shouldn't build microservices. A system processing billions of rows can't use SQLite.

### 3. Consider Reversibility

```
Easy to reverse          Hard to reverse
←─────────────────────────────────────→
Library choice    Database    Language
Config change     Schema      Architecture
```

For reversible decisions: decide quickly and move on.
For irreversible decisions: invest more time, consider more carefully.

### 4. Make a Recommendation

Don't just present options. Make a call:

```
"I recommend PostgreSQL because:
- Your data is relational (foreign keys, joins)
- Team already knows SQL
- Query patterns are complex and variable

The trade-off: If you need to scale beyond a single database, you'll need to add read replicas or sharding later. But you're not there yet."
```

State the recommendation, the reasoning, and the trade-offs. Let the human decide, but don't make them do your thinking.

---

## Thinking About Architecture

Architecture is about structure: what are the pieces, and how do they connect?

### The Questions That Matter

When designing or evaluating architecture:

1. **What changes often?** Put those things together.
2. **What changes rarely?** Those can be coupled more tightly.
3. **What would be expensive to get wrong?** Invest more thought there.
4. **What can be deferred?** Don't design what you don't need yet.

### Common Traps

**Over-engineering**: Building for scale you don't have.
- A startup doesn't need microservices.
- A side project doesn't need Kubernetes.
- YAGNI: You Aren't Gonna Need It.

**Under-engineering**: No structure at all.
- When everything talks to everything, changes become terrifying.
- Some boundaries are worth the upfront cost.

**Copying without understanding**: Using patterns because "that's how X does it."
- Netflix's architecture solves Netflix's problems.
- Your problems are different.

### The Progression

Most projects should follow this path:

```
Start here: Simple script or monolith
            ↓ when code becomes tangled
Then: Clear module boundaries
            ↓ when modules need to scale independently
Then: Extract services
            ↓ when you hit specific bottlenecks
Then: Specialized solutions
```

Don't skip steps. Each step teaches you what you actually need.

---

## Thinking About Implementation

When writing or reviewing code:

### Clarity Over Cleverness

Code is read more than written. The "clever" solution that saves three lines but takes five minutes to understand is the wrong choice.

```
Wrong: x?.y ?? z || w && v
Right: Explicit conditions with clear names
```

### The Rule of Three

- First time you see a pattern: just write the code.
- Second time: note the duplication.
- Third time: consider abstraction.

Premature abstraction is worse than duplication. Wait until you see the pattern clearly.

### Fail Fast

Detect errors early and surface them clearly:
- Validate inputs at the boundary
- Throw exceptions instead of returning null
- Make invalid states unrepresentable

The worst bugs are the ones that silently corrupt data and only surface weeks later.

---

## When to Use Reference Files

This document teaches you how to think. The reference files provide specific knowledge for specific situations.

| Situation | Reference |
|-----------|-----------|
| Choosing between technologies | [technical-decisions.md](technical-decisions.md) |
| Designing system structure | [architecture/patterns.md](architecture/patterns.md) |
| Defining module boundaries | [architecture/boundaries.md](architecture/boundaries.md) |
| Planning data flow | [architecture/data-flow.md](architecture/data-flow.md) |
| Writing quality code | [implementation/best-practices.md](implementation/best-practices.md) |
| Applying design patterns | [implementation/patterns.md](implementation/patterns.md) |
| Restructuring existing code | [refactoring.md](refactoring.md) |
| Designing APIs | [api-design.md](api-design.md) |
| Improving performance | [performance.md](performance.md) |
| Building CI/CD pipelines | [cicd-architecture.md](cicd-architecture.md) |

Don't read them all. Read the one you need, when you need it.

---

## What Engineering Is Not

**Engineering is not housekeeping.**
- Engineering: "How should we structure authentication?"
- Housekeeping: "Let's remove these unused imports."

**Engineering is not validation.**
- Engineering: "Should we use Jest or Vitest?"
- Validation: "Do the tests pass?"

**Engineering is not implementation.**
- Engineering: "Here's the architecture for this feature."
- Implementation: Actually writing the code.

Engineering guides the work. Other skills (and humans) do the work.

---

## The Mindset

Good engineering comes from asking good questions:

- What problem are we solving?
- What are the constraints?
- What are the trade-offs?
- What's the simplest thing that could work?
- What would we do if we're wrong?

You won't always have perfect information. That's fine. Make the best decision you can with what you know, document your reasoning, and stay ready to adapt.

> "Make it work, make it right, make it fast—in that order."

Working software beats elegant architecture. Clarity beats cleverness. Simple solutions beat complex ones.

When in doubt, choose the option that's easier to change later.
