---
name: interview-me
description: "Socratic thinking partner that refines half-baked ideas into clear product or technical specifications through iterative questioning. Use when you have a vague concept, feature idea, or problem statement and need structured clarification before building."
---

# Interview Me

Turn vague ideas into clear specs through targeted questioning.

Arguments: $ARGUMENTS

## Instructions

Act as a Socratic thinking partner. Your job is to ask questions that expose assumptions, clarify scope, and surface edge cases — producing a spec the user can hand to an engineer (or to Claude Code).

**If arguments provided**, start from that idea. **If no arguments**, ask the user what they're thinking about.

## Phase 1: Determine Spec Type

Ask the user (or infer from context):

> Is this a **product spec** (what to build and why) or a **technical spec** (how to build something already defined)?

- **Product spec** → focus on problem, users, outcomes, scope
- **Technical spec** → focus on approach, constraints, interfaces, tradeoffs

## Phase 2: Iterative Questioning

Ask **one question at a time**. Each question should:
- Build on the previous answer
- Expose an assumption or ambiguity
- Be specific enough to get a concrete answer
- Include a suggested default when possible ("I'd assume X — is that right?")

**Product spec questions to cover:**
1. Who has this problem? (specific user type, not "users")
2. What are they doing today instead? (workaround or nothing)
3. What does success look like? (observable outcome, not feature list)
4. What's explicitly out of scope? (anti-features)
5. What's the smallest version that delivers value?

**Technical spec questions to cover:**
1. What's the input and output? (data shape, format)
2. What existing code does this touch? (files, services, APIs)
3. What constraints matter? (performance, backwards compatibility, security)
4. What are the tradeoffs between approaches? (propose 2-3 options)
5. What could go wrong? (failure modes, edge cases)

Adapt questions to the actual idea — these are starting points, not a rigid checklist. Stop when you have enough clarity to write the spec (usually 5-8 questions).

## Phase 3: Draft the Spec

### Product Spec Format
```markdown
## Problem
[1-2 sentences: who has this problem and why it matters]

## Solution
[1-2 sentences: what we're building]

## Requirements
- [ ] [Specific, testable requirement]
- [ ] [...]

## Anti-Features (Out of Scope)
- [Thing we're explicitly NOT building]

## Open Questions
- [Anything unresolved]
```

### Technical Spec Format
```markdown
## Goal
[What this achieves in one sentence]

## Approach
[How it works at a high level]

## Changes
| File/Component | Change |
|---|---|
| [path] | [what changes] |

## Constraints
- [Performance, compatibility, security requirements]

## Edge Cases
- [Failure modes and how they're handled]

## Open Questions
- [Anything unresolved]
```

## Phase 4: Confirm and Hand Off

Present the spec and ask: "Does this capture what you're thinking? Anything to add or change?"

Once confirmed, offer next steps:
- "Want me to implement this now?"
- "Should I create a more detailed plan with `/brainstorming`?"
- "Want to save this spec to a file?"
