---
name: technical-writer
description: Write technical tutorials, blog posts, and educational content with pedagogical structure. Covers concept explanations, how-to guides, deep dives, and developer education. Triggers on tutorial, technical article, blog post, explain concept, teach, educational content, developer guide.
---

# Technical Writer

For README-specific patterns (hero, TL;DR, quick start), see `readme-craft` skill.

## Content Types & Writing Guidelines

### 1. Concept Explanation

Build mental models for abstract ideas.

```markdown
# [Concept Name]

## The Problem It Solves

[Concrete scenario where this matters - make the reader FEEL the pain]

## The Core Idea

[One paragraph, one analogy, zero jargon]

## How It Works

[Visual or step-by-step breakdown]

### Step 1: [First thing that happens]
### Step 2: [Next thing]
### Step 3: [Result]

## In Practice

[Code example with annotations]

## Common Misconceptions

- **Myth:** [What people wrongly believe]
- **Reality:** [What's actually true]

## When NOT to Use This

[Explicit boundaries - this builds trust]
```

**Opening example:**
> Bad: "Dependency injection is a design pattern where..."
> Good: "Your class needs a database connection. Do you create it inside the class, or pass it in from outside? This choice determines whether your code is testable or a nightmare."

**Voice:** "This works because..." not "As you can see...". "You might expect X, but actually Y" not "Obviously...". Never "simply" or "just" (these dismiss difficulty).

### 2. How-To Guide

Get the reader from A to B with minimum friction.

```markdown
# How to [Accomplish Specific Goal]

**Time:** X minutes | **Difficulty:** Beginner/Intermediate/Advanced

## What You'll Build

[Screenshot or description of end result]

## Prerequisites

- [Specific tool/version]
- [Knowledge assumed]

## Steps

### 1. [Action verb] [Object]

[Why this step matters - one sentence]

```code
[Exact command or code]
```

**Expected result:** [What they should see]

### 2. [Next action]

[Continue pattern]

## Verify It Works

[Test command or manual verification]

## Troubleshooting

### [Error message or symptom]

**Cause:** [Why this happens]
**Fix:** [Exact solution]

## Next Steps

- [Related guide]
- [Advanced topic]
```

**Rules:** One action per step. Every step has expected output. Code is copy-paste ready.

### 3. Tutorial (Teaching Through Building)

Teach concepts by building something real.

```markdown
# Build [Something Concrete]

## What You'll Learn

By the end, you'll understand:
- [Concept 1]
- [Concept 2]
- [Concept 3]

## The Project

[Description of what we're building and why it's useful]

## Part 1: [Foundation]

### The Concept

[Brief explanation of the underlying idea]

### Implementing It

[Code with inline explanation]

### What Just Happened

[Reinforce the concept with what they just did]

## Part 2: [Build on Foundation]

[Repeat pattern, each part introducing one new concept]

## Recap

| Concept | Where We Used It |
|---------|------------------|
| [Concept 1] | Part 1 - [specific code] |
| [Concept 2] | Part 2 - [specific code] |

## Challenges

1. **[Easy extension]** - [Hint]
2. **[Medium extension]** - [Hint]
3. **[Hard extension]** - [Hint]
```

**Rules:** One concept per section. Build something that actually works. Show mistakes and corrections. Include checkpoints to verify progress.

### 4. Deep Dive / Technical Article

Comprehensive exploration for mastery-level readers.

```markdown
# [Topic]: A Deep Dive

**Reading time:** X minutes | **Audience:** [Intermediate/Advanced] developers

## TL;DR

[3-5 bullet points covering the key insights]

## The Landscape

[Context: what exists, what problem space we're in]

## How [Thing] Actually Works

### Under the Hood

[Technical explanation with diagrams/code]

### The Tradeoffs

| Approach | Pros | Cons | Use When |
|----------|------|------|----------|
| A | | | |
| B | | | |

## Real-World Patterns

### Pattern 1: [Name]

[Code example from production-quality source]

## Common Pitfalls

### Pitfall 1: [Name]

**The mistake:**
```code
[Bad code]
```

**The fix:**
```code
[Good code]
```

**Why:** [Explanation]

## Further Reading

- [Resource 1] - [What it covers]
```

## Code Examples

**Every code block needs:**
1. Context (what file, what situation)
2. Working code (not pseudocode unless explicitly stated)
3. Key lines highlighted or annotated

```python
# user_service.py - handling authentication

def authenticate(self, credentials):
    user = self.repository.find_by_email(credentials.email)
    if not user:
        return AuthResult.failure("User not found")  # <- Early return pattern

    if not user.verify_password(credentials.password):
        return AuthResult.failure("Invalid password")

    return AuthResult.success(user)  # <- Only success path reaches here
```

**Explaining code:**
Bad: "This code authenticates the user."
Good: "We check for failure conditions first (lines 4-8), returning early. Only valid credentials reach the success path on line 10. This 'guard clause' pattern keeps the happy path unindented."

## Analogies

Bridge unfamiliar concepts to familiar ones:

| Concept | Analogy |
|---------|---------|
| API rate limiting | Bouncer at a club only letting in X people per hour |
| Database indexing | Index in a textbook vs. reading every page |
| Caching | Keeping frequently-used items on your desk vs. filing cabinet |
| Load balancing | Multiple checkout lanes at a grocery store |

**Rules:** Map key properties (not just surface similarity). Acknowledge where the analogy breaks down. Use familiar domains (not other technical concepts).

## Handling Complexity

1. **Start with the simple case** - "In the basic scenario, X happens"
2. **Add one complication** - "But what if Y?" Show how the solution adapts
3. **Show the full picture** - "In production, you'll also handle Z"

## Common Failures

| Failure | Fix |
|---------|-----|
| Wall of code, then explanation | Interleave code and explanation |
| "First, let me explain the history of..." | Start with the problem, not the history |
| Assuming knowledge ("as you know...") | Either explain it or link to prerequisite |
| Magic numbers/values in examples | Use realistic, explained values |
| Only happy path | Show error handling |
| Abstract examples (Foo, Bar, Widget) | Concrete domains (User, Order, Payment) |

## Quality Checklist

**Structure:**
- [ ] Opens with WHY (motivation)
- [ ] Progressive complexity (simple -> complex)
- [ ] Each section provides standalone value

**Code:**
- [ ] All code is tested and works
- [ ] Copy-paste ready (no hidden dependencies)
- [ ] Key lines annotated

**Clarity:**
- [ ] No undefined jargon
- [ ] Analogies for abstract concepts
- [ ] Explicit prerequisites listed

**Trust:**
- [ ] Acknowledges limitations
- [ ] Shows when NOT to use this approach

## Anti-Patterns

| Pattern | Fix |
|---------|-----|
| "Simply do X" | Remove "simply" |
| "It's obvious that..." | Explain anyway |
| Screenshot-only instructions | Add text/code |
| Massive code dump | Break into pieces |
| "Exercise left to reader" | Show the solution |
| "See the docs" | Summarize key points |

## Reference

- [Sentence Structures](references/sentence-structures.md) - Intro, transition, caveat, and reinforcement phrases
