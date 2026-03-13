---
name: tool-plan-interviewer
description: This skill should be used when the agent enters plan mode, when the user mentions "plan file", "spec file", "interview me about the plan", "help me think through this", or when starting implementation planning. Conducts in-depth, multi-round interviews using AskUserQuestion to surface non-obvious requirements, edge cases, and tradeoffs before writing specifications.
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# Plan Interviewer

Conduct comprehensive, multi-round interviews when entering plan mode to ensure thorough understanding before implementation.

## Purpose

Transform shallow feature requests into well-specified plans by asking probing, non-obvious questions that surface hidden complexity, edge cases, architectural decisions, and user experience considerations.

## When to Use

- Upon entering plan mode for any non-trivial task
- When a spec file or plan file is mentioned
- Before writing or updating implementation specifications
- When the user asks to "think through" or "help me plan" something

## Core Process

### Phase 1: Context Gathering

1. **Read existing artifacts**: If a plan file or spec file exists (or is mentioned), read it first to understand current state
2. **Identify the domain**: Determine whether this is frontend, backend, full-stack, infrastructure, data, etc.
3. **Assess complexity**: Estimate how many rounds of questioning are needed

### Phase 2: Multi-Round Interview

Conduct interviews using **AskUserQuestion** tool. Each round should explore different dimensions. Never ask obvious questions like "what framework?" or "what language?" when context already provides this.

**Interview Dimensions (cycle through these):**

#### Technical Implementation
- Data flow edge cases (What happens when X fails mid-operation?)
- State management boundaries (Where does this state live? Who owns it?)
- Concurrency considerations (What if two users do this simultaneously?)
- Migration paths (How do we get from current state to this without breaking things?)
- Performance cliffs (At what scale does this approach break down?)

#### UX & Interaction Design
- Error recovery flows (User does X wrong—then what?)
- Loading/empty/error states (What does the user see during transitions?)
- Undo/redo expectations (Should this be reversible? How far back?)
- Accessibility edge cases (How does a screen reader announce this state change?)
- Mobile-first considerations (Does this gesture conflict with system gestures?)

#### Business Logic & Domain
- Edge case ownership (Who decides what happens when rules conflict?)
- Audit/compliance needs (Does this action need to be logged? For how long?)
- Multi-tenancy implications (How does this behave across different accounts/orgs?)
- Internationalization (Does this text expand 40% in German? RTL support?)

#### Architecture & Tradeoffs
- Consistency vs availability (What's acceptable during network partition?)
- Coupling concerns (Does this create a dependency we'll regret?)
- Testability (How do we verify this works without manual testing?)
- Observability (How do we know this is broken in production?)

#### Security & Privacy
- Trust boundaries (What if this input comes from an attacker?)
- Data exposure (What PII touches this flow? Who can see it?)
- Rate limiting (What happens if someone calls this 10,000 times?)

### Phase 3: Synthesis & Specification

After sufficient interview rounds (typically 3-7 depending on complexity):

1. **Summarize findings**: Recap the key decisions made during interview
2. **Write specification**: Create or update the spec/plan file with:
   - Clear problem statement
   - Decided approach with rationale
   - Edge cases and their handling
   - Open questions (if any remain)
   - Implementation notes

## Interview Technique Guidelines

### Question Quality Rules

**Avoid obvious questions:**
- ❌ "What tech stack?" (look at the codebase)
- ❌ "What should the button say?" (context usually provides this)
- ❌ "Should we use TypeScript?" (check existing code)

**Ask revealing questions:**
- ✅ "If the webhook fails after the database write succeeds, should we retry, rollback, or alert?"
- ✅ "When the cache is stale but the origin is down, do we serve stale or error?"
- ✅ "If a user is mid-edit and their session expires, do we save their work or lose it?"

### Question Framing

Frame questions to surface hidden assumptions:
- "What's the worst thing that could happen if..."
- "When you say X, do you mean A or B? Because they have different implications for..."
- "I notice the current system does Y—should we preserve that behavior or is this a chance to fix it?"
- "Who's the angriest user for this feature and what would make them happy?"

### Pacing

- Ask 2-4 questions per round maximum
- Group related questions together
- After each round, briefly acknowledge answers before next questions
- Stop when answers start repeating or user indicates completion

## AskUserQuestion Tool Usage

Structure questions for maximum clarity:

```
Use AskUserQuestion with:
- 2-4 questions per invocation
- Each question has 2-4 concrete options
- Options should represent real tradeoffs, not obvious choices
- Include brief description explaining implications of each option
```

**Example question structure:**
```
Question: "When a background sync fails, how should we handle it?"
Options:
1. Silent retry (3x with backoff) - User unaware, but may see stale data
2. Toast notification - User informed but may be annoyed
3. Badge indicator - Subtle, user can investigate when ready
4. Block UI until resolved - Safest but worst UX
```

## Spec File Format

When writing the specification, use this structure:

```markdown
# [Feature Name] Specification

## Problem Statement
[1-2 paragraphs on what we're solving and why]

## Decided Approach
[High-level approach with key architectural decisions]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Topic]  | [What] | [Why]     |

## Edge Cases
- **[Scenario]**: [How we handle it]

## Out of Scope
- [What we're explicitly NOT doing]

## Open Questions
- [ ] [Anything still unresolved]

## Implementation Notes
[Technical details, gotchas, dependencies]
```

## Completion Criteria

Stop interviewing when:
- All major dimensions have been covered
- User indicates readiness to proceed
- Answers are becoming repetitive
- Core architecture and edge cases are documented

Then write the spec to the designated file and confirm with user.

## Additional Resources

### Reference Files
- **`references/question-bank.md`** - Extended list of probing questions by domain
